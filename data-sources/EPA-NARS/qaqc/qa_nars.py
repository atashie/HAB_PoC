#!/usr/bin/env python
"""QA/QC for the pulled NLA data: integrity, structure-vs-dictionary, distributions, joins.

Verifies the data from the bytes themselves - not from assumptions - and writes both a
machine-readable JSON (outputs/qa_summary.json) and a human report (outputs/qa_report.md).

Checks
------
1. Integrity      - recompute sha256 for each manifest entry; flag mismatches.
2. Dictionary     - compare each CSV's header against its companion .txt dictionary
                    (columns in data-not-dictionary and dictionary-not-data).
3. Site structure - row/unique-id counts; visit & sample distributions; reconcile the
                    file's sampled-lake count against the published ~981 probability lakes.
4. Geotag         - % populated + range sanity for lat/lon (NAD83) and the hydrography
                    linkage keys (COMID, REACHCODE, PERM_ID, GNIS_ID, HUC2/HUC8).
5. Joins          - every toxin/chem UID must resolve to a site row (orphan count).
6. Toxins         - per-analyte detect vs *measured* non-detect (NARS_FLAG=ND is NOT
                    missing), detection rate, and detected-value ranges.
7. Water chem     - populated/flagged counts + ranges for the HAB-relevant analytes,
                    incl. CHLA (the satellite comparison variable), NTL, PTL.
8. Design caveat  - presence of survey weights and the "raw file != 981" reconciliation.

Run:  cd data-sources/EPA-NARS/qaqc && python qa_nars.py            # uses data/raw/nla2022
      python qa_nars.py --cycle 2022 --rawdir ../data/raw/nla2022
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

_HERE = Path(__file__).resolve().parent
_NARS_DIR = _HERE.parent
_DATA_SOURCES = _NARS_DIR.parent
if str(_DATA_SOURCES) not in sys.path:
    sys.path.insert(0, str(_DATA_SOURCES))
from _common import net  # noqa: E402

_DEFAULT_RAW = _NARS_DIR / "data" / "raw" / "nla2022"
_OUTPUTS = _NARS_DIR / "outputs"

# Published NLA 2022 headline (EPA National Lakes Assessment 2022 Key Findings):
# 981 probability-sampled lakes representing an estimated 268,020-lake population.
PUBLISHED_PROB_LAKES = 981

# HAB-relevant water-chem analytes worth summarizing (prefix of the *_RESULT columns).
CHEM_ANALYTES = ["CHLA", "NTL", "PTL", "NTL_DISS", "PTL_DISS",
                 "NITRATE_N", "AMMONIA_N", "DOC", "TURB", "COND", "PH", "ANC"]

# Geotag / hydrography-linkage columns we expect in siteinfo.
GEOTAG_COLS = ["LAT_DD83", "LON_DD83", "INDEX_LAT_DD", "INDEX_LON_DD",
               "COMID", "REACHCODE", "PERM_ID", "GNIS_ID", "HUC2", "HUC8",
               "US_L3CODE", "AG_ECO9"]


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _sha256(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def dictionary_columns(meta_path: Path) -> list[str]:
    """Declared column names from a NARS metadata .txt (handles both formats).

    Format A: header 'COLUMN_NAME\\tLABEL\\t...'   -> names in column 0.
    Format B: header 'SAMPLE_TYPE\\tPARAMETER\\t...' -> names in column 1 (PARAMETER).
    """
    with meta_path.open(encoding="utf-8", errors="replace", newline="") as f:
        rows = list(csv.reader(f, delimiter="\t"))
    if not rows:
        return []
    header = [h.strip().upper() for h in rows[0]]
    idx = 1 if header[:2] == ["SAMPLE_TYPE", "PARAMETER"] else 0
    out = []
    for r in rows[1:]:
        if len(r) > idx and r[idx].strip():
            out.append(r[idx].strip())
    return out


def _read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, dtype=str, keep_default_na=False, na_values=[""])


def _num(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def _pct(n: int, d: int) -> float:
    return round(100.0 * n / d, 2) if d else 0.0


# --------------------------------------------------------------------------- #
# checks
# --------------------------------------------------------------------------- #
def check_integrity(rawdir: Path) -> dict:
    manifest = net.read_manifest(rawdir / "manifest.jsonl")
    results, n_ok, n_bad, n_missing = [], 0, 0, 0
    for rec in manifest:
        fp = _NARS_DIR / rec["path"]
        if not fp.is_file():
            results.append({"file": rec["path"], "status": "MISSING"})
            n_missing += 1
            continue
        ok = _sha256(fp) == rec["sha256"]
        results.append({"file": rec["path"], "status": "ok" if ok else "SHA256_MISMATCH",
                        "bytes": rec["bytes"]})
        n_ok += ok
        n_bad += (not ok)
    return {"n_files": len(manifest), "n_ok": n_ok, "n_mismatch": n_bad,
            "n_missing": n_missing, "detail": results}


def check_dictionary(data_path: Path, meta_path: Path) -> dict:
    df_cols = set(pd.read_csv(data_path, nrows=0).columns)
    dict_cols = set(dictionary_columns(meta_path))
    return {
        "n_data_cols": len(df_cols),
        "n_dict_cols": len(dict_cols),
        "in_data_not_dict": sorted(df_cols - dict_cols),
        "in_dict_not_data": sorted(dict_cols - df_cols),
    }


def check_siteinfo(df: pd.DataFrame) -> dict:
    sampled = df["SITESAMP"].fillna("").str.upper().eq("YES").sum() if "SITESAMP" in df else None
    out = {
        "n_rows": len(df),
        "n_unique_site_id": int(df["SITE_ID"].nunique()) if "SITE_ID" in df else None,
        "n_unique_unique_id": int(df["UNIQUE_ID"].nunique()) if "UNIQUE_ID" in df else None,
        "n_unique_uid": int(df["UID"].nunique()) if "UID" in df else None,
        "n_sampled_sitesamp_yes": int(sampled) if sampled is not None else None,
        "visit_no_counts": df["VISIT_NO"].fillna("(blank)").value_counts().to_dict()
        if "VISIT_NO" in df else {},
        "lake_orgn_counts": df["LAKE_ORGN"].fillna("(blank)").value_counts().to_dict()
        if "LAKE_ORGN" in df else {},
        "published_prob_lakes": PUBLISHED_PROB_LAKES,
    }
    # Geotag completeness + coordinate sanity.
    geo = {}
    for c in GEOTAG_COLS:
        if c in df:
            nonempty = int(df[c].notna().sum())
            geo[c] = {"pct_populated": _pct(nonempty, len(df)), "n": nonempty}
    lat = _num(df["LAT_DD83"]) if "LAT_DD83" in df else pd.Series(dtype=float)
    lon = _num(df["LON_DD83"]) if "LON_DD83" in df else pd.Series(dtype=float)
    out["geotag"] = geo
    out["coord_datum"] = "NAD83 (LAT_DD83/LON_DD83); index-site coords in INDEX_LAT_DD/INDEX_LON_DD"
    if len(lat):
        out["lat_range"] = [round(float(lat.min()), 4), round(float(lat.max()), 4)]
        out["lon_range"] = [round(float(lon.min()), 4), round(float(lon.max()), 4)]
        out["coord_out_of_conus_box"] = int(
            ((lat < 17) | (lat > 72) | (lon < -180) | (lon > -64)).sum()
        )
    # Survey-design columns present?
    out["weight_cols_present"] = [c for c in
                                  ["WGT_TP_CORE_NLA", "WGT_TP_EXT_NLA", "WGT_DSGN", "STRATUM", "PROB_CAT"]
                                  if c in df]
    return out


def check_join(site_df: pd.DataFrame, other: pd.DataFrame, name: str) -> dict:
    if "UID" not in site_df or "UID" not in other:
        return {"name": name, "note": "no UID column to join on"}
    site_uids = set(site_df["UID"].dropna())
    other_uids = set(other["UID"].dropna())
    orphans = other_uids - site_uids
    return {"name": name, "n_uid_other": len(other_uids),
            "n_orphans_not_in_siteinfo": len(orphans),
            "orphans_sample": sorted(orphans)[:5]}


def check_toxins(df: pd.DataFrame) -> dict:
    out = {"n_rows": len(df), "analytes": {}}
    flag = df["NARS_FLAG"].fillna("") if "NARS_FLAG" in df else pd.Series([""] * len(df))
    res = _num(df["RESULT"]) if "RESULT" in df else pd.Series([np.nan] * len(df))
    for analyte, sub_idx in df.groupby("ANALYTE").groups.items() if "ANALYTE" in df else []:
        idx = list(sub_idx)
        f = flag.loc[idx]
        r = res.loc[idx]
        is_nd = f.str.contains("ND", na=False)
        detects = r[(~is_nd) & r.notna() & (r > 0)]
        units = df.loc[idx, "RESULT_UNITS"].dropna().unique().tolist() if "RESULT_UNITS" in df else []
        mdl = _num(df.loc[idx, "MDL"]) if "MDL" in df else pd.Series(dtype=float)
        out["analytes"][analyte] = {
            "n": len(idx),
            "n_nondetect_measured": int(is_nd.sum()),
            "n_detect": int(len(detects)),
            "detection_rate_pct": _pct(len(detects), len(idx)),
            "flag_counts": f.replace("", "(none)").value_counts().to_dict(),
            "detected_min": round(float(detects.min()), 4) if len(detects) else None,
            "detected_median": round(float(detects.median()), 4) if len(detects) else None,
            "detected_max": round(float(detects.max()), 4) if len(detects) else None,
            "units": units,
            "mdl_range": [round(float(mdl.min()), 4), round(float(mdl.max()), 4)]
            if mdl.notna().any() else None,
        }
    return out


def check_waterchem(df: pd.DataFrame) -> dict:
    n = len(df)
    out = {"n_rows": n, "analytes": {}}
    for a in CHEM_ANALYTES:
        rcol, fcol = f"{a}_RESULT", f"{a}_NARS_FLAG"
        if rcol not in df:
            continue
        r = _num(df[rcol])
        flags = df[fcol].fillna("") if fcol in df else pd.Series([""] * n)
        # Units column is usually {A}_UNITS but a few (e.g. CHLA) use {A}_RESULT_UNITS.
        ucol = next((c for c in (f"{a}_UNITS", f"{a}_RESULT_UNITS") if c in df), None)
        units = df[ucol].dropna().unique().tolist() if ucol else []
        out["analytes"][a] = {
            "n_populated": int(r.notna().sum()),
            "pct_populated": _pct(int(r.notna().sum()), n),
            "n_flagged": int((flags != "").sum()),
            "min": round(float(r.min()), 4) if r.notna().any() else None,
            "median": round(float(r.median()), 4) if r.notna().any() else None,
            "max": round(float(r.max()), 4) if r.notna().any() else None,
            "units": units,
        }
    return out


# --------------------------------------------------------------------------- #
# report writer
# --------------------------------------------------------------------------- #
def write_reports(summary: dict, outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "qa_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    L = []
    A = L.append
    A("# NLA 2022 - QA/QC report")
    A("")
    A(f"Generated by `qaqc/qa_nars.py` from the pulled files in `{summary['rawdir']}`.")
    A("Every number below is recomputed from the downloaded bytes; see "
      "`qa_summary.json` for the machine-readable version.")
    A("")

    ig = summary["integrity"]
    A("## 1. Integrity (sha256 vs manifest)")
    A(f"- Files in manifest: **{ig['n_files']}**; verified OK: **{ig['n_ok']}**; "
      f"mismatches: **{ig['n_mismatch']}**; missing: **{ig['n_missing']}**.")
    A("")

    if "dictionary" in summary:
        A("## 2. Header vs data dictionary (.txt)")
        for name, d in summary["dictionary"].items():
            extra = d["in_data_not_dict"]
            miss = d["in_dict_not_data"]
            status = "match" if not extra and not miss else "REVIEW"
            A(f"- **{name}** ({d['n_data_cols']} data cols vs {d['n_dict_cols']} dict cols): {status}")
            if extra:
                A(f"    - in data, not in dictionary: {extra}")
            if miss:
                A(f"    - in dictionary, not in data: {miss}")
        A("")

    if "siteinfo" in summary:
        s = summary["siteinfo"]
        A("## 3. Site structure & the '981' reconciliation")
        A(f"- Rows: **{s['n_rows']}**; unique lakes (UNIQUE_ID): **{s['n_unique_unique_id']}**; "
          f"unique site-visits (UID): **{s['n_unique_uid']}**; "
          f"sampled (SITESAMP=YES): **{s['n_sampled_sitesamp_yes']}**.")
        A(f"- VISIT_NO: {s['visit_no_counts']}")
        A(f"- LAKE_ORGN: {s['lake_orgn_counts']}")
        A(f"- **Reconciliation:** the file holds the full evaluated frame (oversample, "
          f"hand-picked, NES, revisits) - NOT just the **{s['published_prob_lakes']}** "
          f"probability lakes in the published headline. Any national/regional statistic "
          f"MUST filter to probability sites and apply the survey weights "
          f"(`WGT_TP_CORE_NLA` etc.), never raw counts. Weight cols present: "
          f"{s['weight_cols_present']}. (`WGT_DSGN` is explicitly *do-not-use* for estimation.)")
        A("")
        A("## 4. Geotagging & hydrography linkage completeness")
        A(f"- Coordinate datum: {s['coord_datum']}.")
        if "lat_range" in s:
            A(f"- LAT_DD83 range {s['lat_range']}, LON_DD83 range {s['lon_range']}; "
              f"points outside a generous US box: **{s['coord_out_of_conus_box']}**.")
        for c, v in s["geotag"].items():
            A(f"    - `{c}`: {v['pct_populated']}% populated ({v['n']})")
        A("")

    if "joins" in summary:
        A("## 5. Join-key integrity (UID -> siteinfo)")
        for j in summary["joins"]:
            if "note" in j:
                A(f"- **{j['name']}**: {j['note']}")
            else:
                A(f"- **{j['name']}**: {j['n_uid_other']} UIDs, "
                  f"orphans not in siteinfo: **{j['n_orphans_not_in_siteinfo']}**")
        A("")

    if "toxins" in summary:
        t = summary["toxins"]
        A("## 6. Algal toxins - detect vs *measured* non-detect")
        A("> NARS_FLAG=ND is a **measured** below-detection result, not a missing value. "
          "It is counted separately below and must never be silently coerced to 0 or NaN.")
        for analyte, d in t["analytes"].items():
            A(f"- **{analyte}**: n={d['n']}, detects={d['n_detect']} "
              f"({d['detection_rate_pct']}%), measured non-detects={d['n_nondetect_measured']}, "
              f"units={d['units']}")
            A(f"    - detected range: min {d['detected_min']}, median {d['detected_median']}, "
              f"max {d['detected_max']}; MDL range {d['mdl_range']}")
            A(f"    - flag counts: {d['flag_counts']}")
        A("")

    if "waterchem" in summary:
        w = summary["waterchem"]
        A("## 7. Water chemistry (HAB-relevant analytes)")
        A(f"- Rows (site-visits): **{w['n_rows']}**")
        A("| analyte | % populated | n flagged | min | median | max | units |")
        A("|---|---|---|---|---|---|---|")
        for a, d in w["analytes"].items():
            A(f"| {a} | {d['pct_populated']}% | {d['n_flagged']} | {d['min']} | "
              f"{d['median']} | {d['max']} | {','.join(d['units'])} |")
        A("")

    A("## Honest flags & limitations")
    for f in summary.get("flags", []):
        A(f"- {f}")
    A("")
    (outdir / "qa_report.md").write_text("\n".join(L), encoding="utf-8")


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
def parse_args(argv=None):
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--cycle", type=int, default=2022)
    p.add_argument("--rawdir", default=str(_DEFAULT_RAW), help="pulled data dir (with manifest.jsonl)")
    p.add_argument("--outdir", default=str(_OUTPUTS))
    return p.parse_args(argv)


def _find(rawdir: Path, needle: str) -> Path | None:
    hits = sorted(rawdir.glob(f"*{needle}*.csv"))
    return hits[0] if hits else None


def main(argv=None) -> int:
    args = parse_args(argv)
    rawdir = Path(args.rawdir)
    if not (rawdir / "manifest.jsonl").is_file():
        raise SystemExit(f"No manifest at {rawdir}. Run access/pull_nars.py first.")

    summary: dict = {"cycle": args.cycle, "rawdir": str(rawdir.relative_to(_NARS_DIR)),
                     "flags": []}
    summary["integrity"] = check_integrity(rawdir)

    # Locate the core files.
    site_csv = _find(rawdir, "siteinfo")
    chem_csv = _find(rawdir, "waterchem_wide")
    tox_csv = _find(rawdir, "algaltoxins")

    # Dictionary comparisons (data vs .txt) where both exist.
    summary["dictionary"] = {}
    for csvp in [site_csv, chem_csv, tox_csv]:
        if csvp is None:
            continue
        metap = csvp.with_suffix(".txt")
        if metap.is_file():
            summary["dictionary"][csvp.name] = check_dictionary(csvp, metap)

    site_df = _read_csv(site_csv) if site_csv else None
    if site_df is not None:
        summary["siteinfo"] = check_siteinfo(site_df)

    summary["joins"] = []
    if tox_csv:
        tox_df = _read_csv(tox_csv)
        summary["toxins"] = check_toxins(tox_df)
        if site_df is not None:
            summary["joins"].append(check_join(site_df, tox_df, "algaltoxins"))
    if chem_csv:
        chem_df = _read_csv(chem_csv)
        summary["waterchem"] = check_waterchem(chem_df)
        if site_df is not None:
            summary["joins"].append(check_join(site_df, chem_df, "waterchem"))

    # Standing honest flags (data-independent, always worth restating).
    summary["flags"] = [
        "NLA is a **probability survey**, not a monitoring time series: one index visit "
        "per lake (a subset revisited) in a single summer; 5-year cycles with multi-year gaps.",
        "Only **2 cyanotoxins** are measured (microcystin, cylindrospermopsin); this is not a "
        "full toxin panel and detection is class-specific.",
        "Non-detects (NARS_FLAG=ND) are **measured** below-detection results - handle as "
        "left-censored data, do not treat as missing or as zero without justification.",
        "The raw file is NOT the published 981-lake sample; national/regional percentages "
        "require the design weights and probability-site filter (see section 3).",
        "Geotag is lake **centroid** (LAT_DD83) vs **index sampling point** (INDEX_LAT_DD) - "
        "use INDEX_* for matchups to a satellite pixel or an in-situ station.",
        "Correlation != causation: nutrient/clarity associations with toxins here are "
        "cross-sectional and cannot establish drivers on their own.",
    ]

    write_reports(summary, Path(args.outdir))
    ig = summary["integrity"]
    print(f"QA done. integrity: {ig['n_ok']}/{ig['n_files']} ok, "
          f"{ig['n_mismatch']} mismatch, {ig['n_missing']} missing.")
    print(f"Wrote {Path(args.outdir) / 'qa_report.md'} and qa_summary.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
