#!/usr/bin/env python
"""PROTOTYPE: CyAN CI_cyano <-> NLA 2022 in-situ matchup (national).

Question (from the modeling-utility discussion, scoped per Codex review):
    How well does the CyAN satellite cyanobacteria index (CI) track NLA's lab
    chlorophyll-a and microcystin -- and, first, HOW MANY usable matches even survive
    the resolution / cloud / timing constraints?

What it does (per-lake, no cross-lake aggregation):
  1. Take each NLA 2022 SAMPLED lake-visit (unit = UID) with a collection date, and its
     lab chlorophyll-a (CHLA) and microcystin (MICX, with non-detect flag).
  2. Attach the lake POLYGON from nla2022_lakes.zip (EPSG:5070, same grid as CyAN).
  3. Temporally match the visit date to the CyAN weekly (7-day) CONUS mosaic whose window
     contains it (else nearest within a tolerance); record the day offset.
  4. Zonal-extract CI over the lake footprint: classify the in-lake 300m pixels
     (water below-detection / valid-CI / cloud=nodata / land), and summarize CI.
  5. Report the ATTRITION FUNNEL (how many lakes survive polygon / resolution / cloud
     filters) and, on survivors, the CI<->chl-a and CI<->microcystin relationships.

Honest scope (this is a prototype, not a validated product):
  * CI over a lake is a per-lake spatial reduction (user-authorized: "polygon-extract CI
    over the footprints"). We never aggregate ACROSS lakes.
  * CyAN is 300m: many NLA lakes are 1-2 pixels -> unresolvable. That attrition is a headline
    finding, not a nuisance.
  * A weekly composite is not same-day; matches are "near-date within tolerance", not exact.
  * Cross-sectional & correlational: this measures signal agreement, not causation, and
    cannot by itself validate an operational forecast.
  * chl-a, CI, and microcystin are DIFFERENT targets (biomass proxy vs spectral index vs
    toxin); we report each separately and never treat them as interchangeable.

Run:  cd analysis/cyan_nla_matchup && python matchup.py
      python matchup.py --tol-days 8 --stat max
"""
from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import geopandas as gpd
import rasterio
from rasterio.features import geometry_mask

_HERE = Path(__file__).resolve().parent
_REPO = _HERE.parents[1]
_DS = _REPO / "data-sources"
sys.path.insert(0, str(_DS))
from cyan.access import cyan_api as c  # noqa: E402

_NLA_RAW = _DS / "EPA-NARS" / "data" / "raw" / "nla2022"
_MOSAIC_DIR = _DS / "cyan" / "data" / "raw" / "conus_mosaic_weekly"
_OUT = _HERE / "outputs"

# CI at DN=0 (formal floor) — used to represent "water observed, cyano below detection"
# as a left-censored low CI so those lakes are kept (not dropped) in the CI~chl-a relation.
CI_FLOOR = 10.0 ** c.CI_INTERCEPT
MICX_CRITERION = 8.0  # EPA recreational criterion (ug/L)


# --------------------------------------------------------------------------- #
# load NLA lake-visits (unit = UID) with chl-a + microcystin
# --------------------------------------------------------------------------- #
def _read(p: Path) -> pd.DataFrame:
    return pd.read_csv(p, dtype=str, keep_default_na=False, na_values=[""])


def load_visits(rawdir: Path) -> pd.DataFrame:
    site = _read(rawdir / "nla22_siteinfo.csv")
    chem = _read(rawdir / "nla22_waterchem_wide.csv")
    tox = _read(rawdir / "nla22_algaltoxins.csv")

    # sampled visits only (have an index-site coordinate == physically sampled)
    site = site[site["INDEX_LAT_DD"].notna()].copy()
    v = site[["UID", "SITE_ID", "VISIT_NO", "DATE_COL", "PSTL_CODE", "AREA_HA",
              "NARS_NAME", "US_L3NAME"]].copy()
    v["date"] = pd.to_datetime(v["DATE_COL"], errors="coerce").dt.date
    v["AREA_HA"] = pd.to_numeric(v["AREA_HA"], errors="coerce")

    chla = chem[["UID", "CHLA_RESULT"]].copy()
    chla["CHLA"] = pd.to_numeric(chla["CHLA_RESULT"], errors="coerce")
    v = v.merge(chla[["UID", "CHLA"]], on="UID", how="left")

    micx = tox[tox["ANALYTE"] == "MICX"].copy()
    micx["MICX"] = pd.to_numeric(micx["RESULT"], errors="coerce")
    micx["MICX_ND"] = micx["NARS_FLAG"].fillna("").str.contains("ND")
    v = v.merge(micx[["UID", "MICX", "MICX_ND"]], on="UID", how="left")
    return v


def load_polygons(zip_path: Path) -> gpd.GeoDataFrame:
    gdf = gpd.read_file(f"zip://{zip_path}")
    if gdf.crs is None or gdf.crs.to_epsg() != 5070:
        gdf = gdf.to_crs(5070)
    return gdf[["SITE_ID", "geometry"]].dissolve(by="SITE_ID").reset_index()


# --------------------------------------------------------------------------- #
# temporal match: visit date -> weekly mosaic
# --------------------------------------------------------------------------- #
def index_mosaics(mosaic_dir: Path, year: int) -> list[tuple[date, date, Path]]:
    out = []
    for f in sorted(mosaic_dir.glob("*.tif")):
        p = c.parse_cyan_filename(f.name)
        if p and p.temporal == "7D" and p.start_date.startswith(str(year)):
            out.append((date.fromisoformat(p.start_date), date.fromisoformat(p.end_date), f))
    return sorted(out)


def match_mosaic(d: date, mosaics: list[tuple[date, date, Path]], tol_days: int):
    """Return (path, offset_days) for the weekly window containing d, else nearest
    within tol_days (offset = signed gap to the nearest window edge), else None."""
    if d is None:
        return None
    best = None
    for s, e, f in mosaics:
        if s <= d <= e:
            return f, 0
        gap = (s - d).days if d < s else (d - e).days
        if best is None or gap < best[1]:
            best = (f, gap)
    if best and best[1] <= tol_days:
        return best
    return None


# --------------------------------------------------------------------------- #
# zonal CI extraction over one lake polygon
# --------------------------------------------------------------------------- #
def extract_ci(ds: rasterio.DatasetReader, geom, ci_stat: str) -> dict:
    """Classify in-lake 300m pixels and summarize CI. Strict pixels (center-in-polygon).

    Returns counts (land/cloud/below-detection/valid) and CI summary over water pixels,
    with below-detection contributing CI_FLOOR (left-censored low, not dropped).
    """
    minx, miny, maxx, maxy = geom.bounds
    try:
        win = ds.window(minx, miny, maxx, maxy)
        win = win.round_offsets().round_lengths()
        # pad by 1 px so tiny lakes aren't lost at window edges
        from rasterio.windows import Window
        win = Window(max(win.col_off - 1, 0), max(win.row_off - 1, 0),
                     win.width + 2, win.height + 2)
        dn = ds.read(1, window=win)
    except Exception:
        return {"n_inside": 0}
    if dn.size == 0:
        return {"n_inside": 0}
    transform = ds.window_transform(win)
    inside = geometry_mask([geom], out_shape=dn.shape, transform=transform,
                           invert=True, all_touched=False)
    n_strict = int(inside.sum())
    if n_strict == 0:
        # fall back to any-touched, to report whether the lake is simply sub-pixel
        inside = geometry_mask([geom], out_shape=dn.shape, transform=transform,
                               invert=True, all_touched=True)
        touched = int(inside.sum())
        return {"n_inside": 0, "n_touched": touched}

    vals = dn[inside]
    n_land = int((vals == c.DN_LAND).sum())
    n_cloud = int((vals == c.DN_NODATA).sum())
    n_bd = int((vals == c.DN_BELOW_DETECTION).sum())
    valid = (vals >= c.DN_VALID_MIN) & (vals <= c.DN_VALID_MAX)
    n_valid = int(valid.sum())
    n_water = n_bd + n_valid

    res = {"n_inside": n_strict, "n_land": n_land, "n_cloud": n_cloud,
           "n_below_detection": n_bd, "n_valid": n_valid, "n_water": n_water}
    if n_water == 0:
        res["ci_lake"] = np.nan          # all cloud/land -> no observation
        res["ci_detected"] = np.nan
        return res
    if n_valid == 0:
        res["ci_lake"] = CI_FLOOR        # water seen, cyano below detection
        res["ci_detected"] = 0
        return res
    ci = c.dn_to_ci(vals[valid].astype("uint8"))
    ci = ci[np.isfinite(ci)]
    agg = float(np.nanmax(ci)) if ci_stat == "max" else float(np.nanmean(ci))
    res["ci_lake"] = max(agg, CI_FLOOR)
    res["ci_detected"] = 1
    return res


# --------------------------------------------------------------------------- #
# stats + report
# --------------------------------------------------------------------------- #
def spearman(a: pd.Series, b: pd.Series) -> tuple[float, int]:
    d = pd.DataFrame({"a": a, "b": b}).dropna()
    if len(d) < 5:
        return float("nan"), len(d)
    return round(d["a"].corr(d["b"], method="spearman"), 3), len(d)


def run(args) -> int:
    _OUT.mkdir(parents=True, exist_ok=True)
    visits = load_visits(_NLA_RAW)
    polys = load_polygons(_NLA_RAW / "nla2022_lakes.zip")
    mosaics = index_mosaics(_MOSAIC_DIR, 2022)
    print(f"visits(sampled)={len(visits)}  polygons={len(polys)}  mosaics2022={len(mosaics)}")

    # Stage A: sampled visits with chl-a
    A = visits[visits["CHLA"].notna()].copy()
    # Stage B: attach polygon
    poly_map = polys.set_index("SITE_ID")["geometry"].to_dict()
    A["geometry"] = A["SITE_ID"].map(poly_map)
    B = A[A["geometry"].notna()].copy()
    # Stage C: temporal match
    matched = [match_mosaic(d, mosaics, args.tol_days) for d in B["date"]]
    B["mosaic"] = [m[0] if m else None for m in matched]
    B["offset_days"] = [m[1] if m else np.nan for m in matched]
    C = B[B["mosaic"].notna()].copy()

    # Stage D/E: extract CI per lake, grouped by mosaic (open each raster once)
    recs = []
    for mpath, grp in C.groupby(C["mosaic"].astype(str)):
        with rasterio.open(mpath) as ds:
            for _, r in grp.iterrows():
                ex = extract_ci(ds, r["geometry"], args.stat)
                recs.append({**r.drop(labels=["geometry"]).to_dict(), **ex})
    M = pd.DataFrame(recs)

    D = M[M["n_inside"] > 0].copy()                          # lake resolvable (>=1 strict px)
    E = D[D["ci_lake"].notna()].copy()                       # >=1 non-cloud water px -> usable

    # ---- attrition funnel ----
    funnel = [
        ("A. Sampled lake-visits with lab chl-a", len(A)),
        ("B. + matched to a lake polygon", len(B)),
        (f"C. + temporally matched to a weekly mosaic (<= {args.tol_days}d)", len(C)),
        ("D. + lake resolvable at 300m (>=1 in-lake pixel)", len(D)),
        ("E. + >=1 cloud-free water pixel (USABLE match)", len(E)),
    ]

    # ---- relationships on usable set E ----
    E["log_ci"] = np.log10(E["ci_lake"])
    E["log_chla"] = np.log10(pd.to_numeric(E["CHLA"], errors="coerce").clip(lower=1e-3))
    rho_ci_chla, n1 = spearman(E["log_ci"], E["log_chla"])

    micx_det = E[(E["MICX_ND"] == False) & (pd.to_numeric(E["MICX"], errors="coerce") > 0)].copy()
    micx_det["log_micx"] = np.log10(pd.to_numeric(micx_det["MICX"], errors="coerce"))
    rho_ci_micx, n2 = spearman(micx_det["log_ci"], micx_det["log_micx"])

    # CI-detection vs microcystin-detection contingency (E rows with a toxin measurement)
    ct = E.dropna(subset=["ci_detected"]).copy()
    ct = ct[ct["MICX_ND"].notna()]
    ct["ci_pos"] = ct["ci_detected"].astype(float) > 0
    ct["tox_pos"] = ~ct["MICX_ND"].astype(bool)
    tab = pd.crosstab(ct["ci_pos"], ct["tox_pos"]) if len(ct) else pd.DataFrame()

    _write_report(funnel, E, rho_ci_chla, n1, rho_ci_micx, n2, micx_det, tab, args)
    _plot(E, micx_det, args)
    E.drop(columns=[cc for cc in ("geometry",) if cc in E.columns], errors="ignore") \
     .to_csv(_OUT / "cyan_nla_matched.csv", index=False)
    print(f"USABLE matches: {len(E)} / {len(A)} sampled-with-chla "
          f"({100*len(E)/max(len(A),1):.1f}%). rho(CI,chla)={rho_ci_chla} (n={n1}); "
          f"rho(CI,micx)={rho_ci_micx} (n={n2}).")
    print(f"Wrote {_OUT/'matchup_report.md'}, matchup_scatter.png, cyan_nla_matched.csv")
    return 0


def _write_report(funnel, E, rho_ci_chla, n1, rho_ci_micx, n2, micx_det, tab, args):
    L = ["# CyAN CI_cyano <-> NLA 2022 matchup - PROTOTYPE", "",
         f"CI summary stat per lake: **{args.stat}** over in-lake valid pixels; temporal "
         f"tolerance **{args.tol_days} d**; below-detection water -> CI floor "
         f"({c.CI_INTERCEPT:.3f} log10).", "",
         "> Per-lake spatial extraction (user-authorized); no cross-lake aggregation. "
         "Cross-sectional & correlational - measures *signal agreement*, not causation, and "
         "does not validate an operational forecast.", "",
         "## 1. Attrition funnel (the headline)"]
    base = funnel[0][1]
    for label, n in funnel:
        L.append(f"- {label}: **{n}**  ({100*n/max(base,1):.1f}% of A)")
    dropped = funnel[3][1] - funnel[4][1]
    L += ["",
          f"Of lakes resolvable at 300m, **{dropped}** lost the week to cloud "
          f"(no cloud-free water pixel). Temporal matching was cheap (weekly mosaics are "
          f"continuous); the binding constraints are **lake size (300m)** and **cloud**.", ""]

    # pixel-size context
    if "n_inside" in E:
        med_px = int(E["n_inside"].median())
        L += ["## 2. What the usable lakes look like",
              f"- Usable lakes have a median of **{med_px}** in-lake 300m pixels "
              f"(area median **{E['AREA_HA'].median():.0f} ha**).",
              f"- Median cloud-free water pixels/lake: **{int(E['n_water'].median())}**; "
              f"median in-lake cloud pixels: **{int(E['n_cloud'].median())}**.", ""]

    L += ["## 3. Does CI track the in-situ measurements?",
          f"- **CI vs lab chlorophyll-a** (log-log Spearman): rho = **{rho_ci_chla}** "
          f"(n = {n1}). [biomass proxy vs spectral index]",
          f"- **CI vs microcystin** (detections only, log-log Spearman): rho = "
          f"**{rho_ci_micx}** (n = {n2}). [toxin - a different target]"]
    if len(tab):
        L += ["", "### CI-detection vs microcystin-detection (usable lakes)",
              "```", tab.to_string(), "```",
              "Rows = CI detected (satellite sees cyano); Cols = microcystin detected (lab). "
              "Off-diagonal = disagreement; recall chl-a/CI proxies over-predict toxin risk."]
    L += ["",
          "## 4. Honest caveats",
          "- 300m CyAN under-resolves small lakes; the usable set is biased toward LARGER "
          "lakes -> not representative of the NLA lake population (survey weights would not "
          "fix a resolution-induced exclusion).",
          "- A weekly composite is not same-day; CI and the grab sample can be days apart and "
          "a bloom is patchy in space and time.",
          "- `max` CI is sensitive to a single bright/edge pixel; `--stat mean` is the "
          "conservative alternative (re-run to compare).",
          "- chl-a, CI, microcystin are distinct targets; agreement on one does not transfer.",
          "- Correlational only. This prototype sizes the opportunity; it is not a validation.", ""]
    (_OUT / "matchup_report.md").write_text("\n".join(L), encoding="utf-8")


def _plot(E, micx_det, args):
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.6))
    e = E.dropna(subset=["ci_lake", "CHLA"])
    ax[0].scatter(pd.to_numeric(e["CHLA"], errors="coerce"), e["ci_lake"], s=14,
                  alpha=0.5, c="#238b45", edgecolors="none")
    ax[0].set_xscale("log"); ax[0].set_yscale("log")
    ax[0].set_xlabel("NLA lab chlorophyll-a (ug/L)")
    ax[0].set_ylabel(f"CyAN CI_cyano ({args.stat} in-lake)")
    ax[0].set_title(f"CI vs chl-a  (n={len(e)})")
    ax[0].grid(True, which="both", alpha=0.25)

    if len(micx_det):
        ax[1].scatter(pd.to_numeric(micx_det["MICX"], errors="coerce"), micx_det["ci_lake"],
                      s=16, alpha=0.6, c="#d7191c", edgecolors="none")
        ax[1].axvline(MICX_CRITERION, ls="--", c="k", lw=1, label="EPA 8 ug/L")
        ax[1].legend(fontsize=8)
    ax[1].set_xscale("log"); ax[1].set_yscale("log")
    ax[1].set_xlabel("NLA microcystin (ug/L, detections)")
    ax[1].set_ylabel(f"CyAN CI_cyano ({args.stat} in-lake)")
    ax[1].set_title(f"CI vs microcystin  (n={len(micx_det)})")
    ax[1].grid(True, which="both", alpha=0.25)

    fig.suptitle("CyAN CI_cyano vs NLA 2022 in-situ (PROTOTYPE; usable near-date matches; "
                 "correlational, per-lake, not a validation)", fontsize=10)
    fig.tight_layout()
    fig.savefig(_OUT / "matchup_scatter.png", dpi=115)
    plt.close(fig)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tol-days", type=int, default=8,
                    help="max |days| from the weekly window when no containing week exists")
    ap.add_argument("--stat", choices=["max", "mean"], default="max",
                    help="per-lake CI summary over valid in-lake pixels")
    return run(ap.parse_args(argv))


if __name__ == "__main__":
    raise SystemExit(main())
