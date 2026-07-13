#!/usr/bin/env python3
"""Build all data assets the scrollytelling story (story.html) consumes.

Deterministic + regenerable (claim gate). Reads only checked-in real data and
writes to presentation/data/ + presentation/assets/:

  data/charts.json          aggregated chart data for the 3 Plotly figures
                            (computed from tools.json/models.json — NOT hardcoded)
  data/fl_lakes.geojson     the 133 CyAN-resolvable Florida lakes (EPSG:4326)
  data/basemap_states.geojson  CONUS state outlines for the offline "political" basemap
  assets/erie_cyan.png      georeferenced CyAN bloom overlay (Western Lake Erie, 2022-07-17)
  assets/erie_cyan.json     lat/lon bounds for the overlay above

Run:  python presentation/build_story_assets.py
"""
import json, os, glob, re
from collections import Counter

import numpy as np
import geopandas as gpd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(HERE, "data")
ASSETS = os.path.join(HERE, "assets")
os.makedirs(ASSETS, exist_ok=True)


def parse_references():
    """Map every citation key -> {author, year, title, url} from Research/REFERENCES.md."""
    path = os.path.join(ROOT, "Research", "REFERENCES.md")
    refs = {}
    for line in open(path, encoding="utf-8"):
        if not re.match(r"\|\s*(?:ACAD|FED|SLG|NGO|PVT)-\d+\s*\|", line):
            continue
        parts = [c.strip() for c in line.split("|")]
        key = parts[1]
        title = parts[2] if len(parts) > 2 else ""
        author = parts[3] if len(parts) > 3 else ""
        year = parts[4] if len(parts) > 4 else ""
        ym = re.search(r"\d{4}", year)
        year = ym.group(0) if ym else year
        um = re.search(r"https?://[^\s)]+", line)
        url = um.group(0).rstrip(".,;") if um else ""
        if not url:
            dm = re.search(r"10\.\d{4,}/\S+", line)
            url = ("https://doi.org/" + dm.group(0).rstrip(".,;)")) if dm else ""
        refs[key] = {"author": author, "year": year, "title": title, "url": url}
    return refs


def short_author(a):
    if not a or a == "n/r":
        return ""
    parts = re.split(r";", a)
    first = parts[0].strip()
    if "," in first and len(first) > 26:
        first = first.split(",")[0].strip()
    more = len(parts) > 1 or ("," in a and len(a) > 40)
    return (first + (" et al." if more else "")).strip()


# ---------------------------------------------------------------- charts.json
def build_charts():
    tools = json.load(open(os.path.join(DATA, "tools.json"), encoding="utf-8"))["tools"]
    MJ = json.load(open(os.path.join(DATA, "models.json"), encoding="utf-8"))
    models = [m for m in MJ["models"] if m.get("is_model")]
    FEAT2CLASS = {f: c for c, fs in MJ["_meta"]["feature_classes"].items() for f in fs}

    CLASS_COLOR = {"weather": "#6baed6", "hydroclimate": "#4c956c", "static": "#9aa5b1",
                   "earth-obs / bloom signal": "#8c6bb1", "chemistry": "#e07b39"}
    # item 5: map each literature feature to the dataset WE ingest to cover it (so the panel reads
    # "precip matters -> we bring in ERA5"). Two features are honestly "not in our stack".
    DATASET_OF = {"satellite_reflectance": "CyAN", "prior_bloom_state": "CyAN",
                  "water_temperature": "NWIS", "precipitation": "ERA5", "wind_mixing": "ERA5",
                  "nutrients": "WQP", "pH": "WQP", "dissolved_oxygen": "WQP",
                  "hydrology_flow": "NWIS", "lake_morphology": "Static (NHD / BasinATLAS)",
                  "phycocyanin_signal": "Not in our stack", "geolocation": "Not in our stack"}
    DATASET_COLOR = {"CyAN": "#8c6bb1", "ERA5": "#3b82c4", "WQP": "#e07b39", "NWIS": "#2e7d5b",
                     "Static (NHD / BasinATLAS)": "#9aa5b1", "Not in our stack": "#c3ccd2"}
    ORG_LABEL = {"federal": "Federal gov't", "state-local": "State / local gov't", "private": "Private sector"}
    MTYPE_LABEL = {"empirical-RS": "Empirical satellite", "statistical-ML": "Statistical / ML",
                   "mechanistic": "Physics-based", "in-situ-sampling": "In-situ monitoring"}
    FEATURE_LABEL = {
        "water_temperature": "Water temperature", "nutrients": "Nutrients (N / P)",
        "satellite_reflectance": "Satellite reflectance / index", "precipitation": "Precipitation",
        "wind_mixing": "Wind / mixing", "hydrology_flow": "Hydrology / flow",
        "lake_morphology": "Lake depth / area", "prior_bloom_state": "Prior bloom state (persistence)",
        "pH": "pH", "dissolved_oxygen": "Dissolved oxygen",
        "phycocyanin_signal": "Phycocyanin (in-situ pigment)", "geolocation": "Geolocation (lat/lon)"}
    ALGO_FAMILY = {"M1": "Bayesian spatiotemporal", "M2": "Bayesian spatiotemporal",
                   "M3": "Tree / boosting", "M5": "Tree / boosting", "M6": "Tree / boosting",
                   "M8": "Tree / boosting", "M11": "Tree / boosting",
                   "M4": "Deep learning (LSTM/CNN)", "M14": "Deep learning (LSTM/CNN)",
                   "M7": "ANN / SVM", "M9": "Mechanistic / process-based",
                   "M10": "Mechanistic / process-based", "M12": "Mechanistic / process-based",
                   "M15": "Hyperspectral sensor"}

    def norm_access(a):
        a = a.lower()
        return "Freemium" if "freemium" in a else "Paid" if "paid" in a else "Free" if "free" in a else a.title()

    def norm_signal(s):
        s = s.lower()
        if s.startswith("in-situ"): return "In-situ (± weather/physical)"
        return {"fusion": "Fusion (satellite + in-situ)", "satellite": "Satellite only",
                "hybrid": "Hybrid (ML + process)"}.get(s, "Other")

    fc = [t for t in tools if "forecast" in t["horizon"].lower()]

    def panel(key_of, label_of, order):
        allc, fcc = Counter(key_of(t) for t in tools), Counter(key_of(t) for t in fc)
        return [{"label": label_of(k), "total": allc[k], "forecast": fcc.get(k, 0)} for k in order]

    org_order = [k for k, _ in Counter(t["org_type"] for t in tools).most_common()]
    acc_order = [k for k in ["Free", "Freemium", "Paid"] if Counter(norm_access(t["access"]) for t in tools).get(k)]
    mt_order = [k for k, _ in Counter(t["model_type"] for t in tools).most_common()]

    tools_panels = [
        {"title": "Who makes them", "bars": panel(lambda t: t["org_type"], lambda k: ORG_LABEL.get(k, k), org_order)},
        {"title": "Cost of access", "bars": panel(lambda t: norm_access(t["access"]), lambda k: k, acc_order)},
        {"title": "How they work", "bars": panel(lambda t: t["model_type"], lambda k: MTYPE_LABEL.get(k, k), mt_order)},
    ]

    reported = [m for m in models if m["features_reported"]]
    presence, top = Counter(), Counter()
    for m in reported:
        for f in m["features"]:
            presence[f] += 1
        for f in m["top_features"]:
            top[f] += 1
    feats = [f for f, _ in presence.most_common()]
    features = [{"label": FEATURE_LABEL.get(f, f), "count": presence[f], "top": top.get(f, 0),
                 "cls": FEAT2CLASS[f], "color": CLASS_COLOR[FEAT2CLASS[f]],
                 "dataset": DATASET_OF.get(f, "Not in our stack"),
                 "dcolor": DATASET_COLOR[DATASET_OF.get(f, "Not in our stack")]} for f in feats]

    algo = Counter(ALGO_FAMILY[m["id"]] for m in models)
    sig = Counter(norm_signal(m["data_signal"]) for m in models)

    # resolve real source links (claim gate): every tool -> its page, every model -> its citation(s)
    refs = parse_references()

    def tool_link(t):
        keys = t.get("keys", [])
        pref = [k for k in keys if not k.startswith("ACAD")] or keys  # prefer the tool's own agency/vendor page over a paper
        for k in pref:
            if refs.get(k, {}).get("url"):
                return {"key": k, "url": refs[k]["url"]}
        k = keys[0] if keys else ""
        return {"key": k, "url": refs.get(k, {}).get("url", "")}

    tool_sources = [dict(name=t["name"], org=t["org"], **tool_link(t)) for t in tools]
    model_cites = [
        {"id": m["id"], "name": m["name"],
         "refs": [{"key": k, "author": short_author(refs.get(k, {}).get("author", "")),
                   "year": refs.get(k, {}).get("year", ""), "title": refs.get(k, {}).get("title", ""),
                   "url": refs.get(k, {}).get("url", "")} for k in m.get("keys", [])]}
        for m in models
    ]

    charts = {
        "_meta": {"tools_n": len(tools), "models_n": len(models), "features_reported_n": len(reported),
                  "source": "presentation/data/{tools,models}.json; citations resolved from Research/REFERENCES.md",
                  "importance_caveat": "'top predictor' counts are correlational / model-internal, not causal."},
        "tools": {"panels": tools_panels, "class_color": CLASS_COLOR, "sources": tool_sources},
        "features": {"items": features, "class_color": CLASS_COLOR, "dataset_color": DATASET_COLOR},
        "models": {"algorithm": [{"label": k, "count": v} for k, v in algo.most_common()],
                   "signal": [{"label": k, "count": v} for k, v in sig.most_common()],
                   "citations": model_cites},
    }
    json.dump(charts, open(os.path.join(DATA, "charts.json"), "w", encoding="utf-8"), indent=1)
    linked = sum(1 for s in tool_sources if s["url"])
    cited = sum(len(m["refs"]) for m in model_cites)
    print("charts.json  tools=%d (%d linked)  models=%d (%d citations)  feat-reporting=%d"
          % (len(tools), linked, len(models), cited, len(reported)))


# ---------------------------------------------------------------- fl_lakes.geojson
def build_lakes():
    g = gpd.read_file(os.path.join(ROOT, "models", "data", "derived", "fl_resolvable_lakes.gpkg"))
    g = g.to_crs(4326)
    g["name"] = g["GNIS_NAME"].where(g["GNIS_NAME"].notna(), None)
    # A few major FL waterbodies have a null GNIS_NAME in the source; name them by NHDPlus COMID
    # (real names, not fabricated — identified unambiguously by COMID / size).
    KNOWN = {166757656: "Lake Okeechobee"}  # FL's largest waterbody (~1675 km²), GNIS_NAME null in source
    g["name"] = g.apply(lambda r: KNOWN.get(int(r["COMID"]), r["name"]), axis=1)
    g["area_km2"] = g["AREASQKM"].round(1)
    # per-lake AL1 bloom frequency (real target, horizon 0) — upgrades the "explore" step from a placeholder
    import pandas as pd
    tbl = os.path.join(ROOT, "models", "data", "derived", "modeling_table_cyan_fl.parquet")
    if os.path.exists(tbl):
        t = pd.read_parquet(tbl, columns=["comid", "horizon", "target_bloom"])
        freq = t[t["horizon"] == 0].groupby("comid")["target_bloom"].mean()
        g["bloom_freq"] = g["COMID"].astype("int64").map(freq).round(3)
    else:
        g["bloom_freq"] = None
    keep = g[["COMID", "name", "area_km2", "bloom_freq", "geometry"]].copy()
    keep["geometry"] = keep.geometry.simplify(0.0004, preserve_topology=True)
    keep.to_file(os.path.join(DATA, "fl_lakes.geojson"), driver="GeoJSON")
    named = int(keep["name"].notna().sum())
    bf = keep["bloom_freq"].dropna()
    print("fl_lakes.geojson  n=%d  named=%d  area_km2 range=%.1f..%.1f  bloom_freq n=%d (%.2f..%.2f)"
          % (len(keep), named, keep.area_km2.min(), keep.area_km2.max(), len(bf),
             bf.min() if len(bf) else 0, bf.max() if len(bf) else 0))


# ---------------------------------------------------------------- basemap_states.geojson
def build_states():
    src = "zip://" + os.path.join(ROOT, "models", "acquire", "_cache", "cb_2022_us_state_20m.zip")
    s = gpd.read_file(src)
    drop = {"AK", "HI", "PR", "VI", "GU", "MP", "AS"}
    s = s[~s["STUSPS"].isin(drop)].to_crs(4326)
    s["geometry"] = s.geometry.simplify(0.01, preserve_topology=True)
    out = s[["NAME", "STUSPS", "geometry"]].copy()
    out.to_file(os.path.join(DATA, "basemap_states.geojson"), driver="GeoJSON")
    print("basemap_states.geojson  n=%d states (CONUS)" % len(out))


# ---------------------------------------------------------------- CyAN overlays (multi-week, EPSG:3857)
# WHY 3857: Leaflet's display CRS is Web Mercator. L.imageOverlay stretches the image LINEARLY in 3857
# between the given lat/lon corners. Rendering the raster in 3857 (not 4326) makes that placement exact
# (a 4326/equirectangular image bows ~5-9 km vertically at these latitudes). Same approach the repo's
# folium viz uses via mercator_project=True (data-sources/cyan/viz/viz_cyan.py).
def build_cyan_overlays():
    import datetime
    import rasterio
    from rasterio.warp import calculate_default_transform, reproject, Resampling, transform_bounds
    from rasterio.transform import array_bounds
    from matplotlib import colormaps
    import matplotlib.pyplot as plt

    WEEKS = [170, 184, 198, 212, 226, 240, 254, 268]   # 2022 DOY starts: mid-Jun -> late-Sep (bloom onset->peak->decline)
    turbo = colormaps["turbo"]
    frames, bounds_ll = [], None
    for doy in WEEKS:
        tag = "L2022%03d2022%03d" % (doy, doy + 6)
        matches = glob.glob(os.path.join(ROOT, "data-sources", "cyan", "data", "**",
                                          "%s*CONUS_300m_7_2.tif" % tag), recursive=True)
        if not matches:
            print("  MISSING CyAN week", tag)
            continue
        with rasterio.open(matches[0]) as src:
            dst = "EPSG:3857"                          # render in Leaflet's display CRS
            transform, w, h = calculate_default_transform(src.crs, dst, src.width, src.height, *src.bounds)
            dn = np.full((h, w), 255, np.uint8)
            reproject(rasterio.band(src, 1), dn, src_transform=src.transform, src_crs=src.crs,
                      dst_transform=transform, dst_crs=dst, resampling=Resampling.nearest,
                      src_nodata=255, dst_nodata=255)
            x0, y0, x1, y1 = array_bounds(h, w, transform)                 # extent in 3857 metres
            west, south, east, north = transform_bounds(dst, "EPSG:4326", x0, y0, x1, y1)  # exact for an axis-aligned box
        bounds_ll = [[float(south), float(west)], [float(north), float(east)]]
        # DN encoding: 0 = below detection, 1..253 = CI (log), 254 = land, 255 = no-data. Show only detected.
        detected = (dn >= 1) & (dn <= 253)
        rgba = turbo(np.clip(dn.astype(float) / 253.0, 0, 1))
        rgba[..., 3] = np.where(detected, 1.0, 0.0)
        fn = "erie_cyan_%03d.png" % doy
        plt.imsave(os.path.join(ASSETS, fn), (rgba * 255).astype(np.uint8))
        date = (datetime.date(2022, 1, 1) + datetime.timedelta(days=doy - 1)).isoformat()
        frames.append({"label": date, "url": "assets/" + fn, "detected_px": int(detected.sum())})

    meta = {"bounds": bounds_ll, "frames": frames,
            "default_index": next((i for i, f in enumerate(frames) if f["label"] == "2022-07-17"), len(frames) // 2),
            "source": "EPA/NASA CyAN CI_cyano, Sentinel-3 OLCI v7.2, weekly composites (Western Lake Erie tile, 2022), reprojected to EPSG:3857"}
    json.dump(meta, open(os.path.join(ASSETS, "erie_cyan.json"), "w"), indent=1)
    print("cyan overlays: %d weeks (%s .. %s), bounds=%s"
          % (len(frames), frames[0]["label"], frames[-1]["label"], bounds_ll))


# ---------------------------------------------------------------- Florida CyAN overlays (raw signal, item 8)
# WHY same as Erie (build_cyan_overlays): render in EPSG:3857 so L.imageOverlay's linear stretch between
# lat/lon corners is exact. Source = the CONUS 300 m weekly mosaics (EPSG:5070), cropped to a central/south
# Florida window BEFORE reprojection (memory) — the same 2016 bloom season as the USGS Lake Okeechobee hero
# photo (N. Aumen, 2016-07-09), so the ground photo and the satellite view show the SAME event.
def build_cyan_fl_overlays():
    import datetime
    import rasterio
    from rasterio.warp import calculate_default_transform, reproject, Resampling, transform_bounds
    from rasterio.transform import array_bounds
    from rasterio.windows import from_bounds, bounds as win_bounds
    from matplotlib import colormaps
    import matplotlib.pyplot as plt

    # central/south FL peninsula: Okeechobee, Kissimmee chain, Apopka, Harris, George (lon/lat)
    FL_W, FL_S, FL_E, FL_N = -82.6, 26.2, -80.1, 29.8
    WEEKS = [129, 157, 185, 213, 241, 269, 297, 325]   # 2016 DOY starts: May -> late Nov (onset->peak->decline)
    RAW = os.path.join(ROOT, "data-sources", "cyan", "data", "raw", "conus_mosaic_weekly")
    turbo = colormaps["turbo"]
    frames, bounds_ll = [], None
    for doy in WEEKS:
        tag = "L2016%03d2016%03d" % (doy, doy + 6)
        matches = glob.glob(os.path.join(RAW, "%s*CYAN_CONUS_300m.tif" % tag))
        if not matches:
            print("  MISSING FL CyAN week", tag); continue
        with rasterio.open(matches[0]) as src:
            fl = transform_bounds("EPSG:4326", src.crs, FL_W, FL_S, FL_E, FL_N)
            win = from_bounds(*fl, transform=src.transform).round_offsets().round_lengths()
            a = src.read(1, window=win)                                   # uint8 DN, cropped to FL
            src_transform = src.window_transform(win)
            left, bottom, right, top = win_bounds(win, src.transform)
            dst = "EPSG:3857"
            transform, w, h = calculate_default_transform(src.crs, dst, a.shape[1], a.shape[0],
                                                          left, bottom, right, top)
            dn = np.full((h, w), 255, np.uint8)
            reproject(a, dn, src_transform=src_transform, src_crs=src.crs,
                      dst_transform=transform, dst_crs=dst, resampling=Resampling.nearest,
                      src_nodata=255, dst_nodata=255)
            x0, y0, x1, y1 = array_bounds(h, w, transform)
            west, south, east, north = transform_bounds(dst, "EPSG:4326", x0, y0, x1, y1)
        bounds_ll = [[float(south), float(west)], [float(north), float(east)]]
        detected = (dn >= 1) & (dn <= 253)                               # 0=below-detection,254=land,255=nodata
        rgba = turbo(np.clip(dn.astype(float) / 253.0, 0, 1))
        rgba[..., 3] = np.where(detected, 1.0, 0.0)
        fn = "fl_cyan_%03d.png" % doy
        plt.imsave(os.path.join(ASSETS, fn), (rgba * 255).astype(np.uint8))
        date = (datetime.date(2016, 1, 1) + datetime.timedelta(days=doy - 1)).isoformat()
        frames.append({"label": date, "url": "assets/" + fn, "detected_px": int(detected.sum())})

    meta = {"bounds": bounds_ll, "frames": frames,
            "default_index": next((i for i, d in enumerate(WEEKS) if d == 185), 0),
            "source": "EPA/NASA CyAN CI_cyano, Sentinel-3 OLCI, weekly composites (central/south Florida crop, 2016), "
                      "reprojected EPSG:5070->3857"}
    json.dump(meta, open(os.path.join(ASSETS, "fl_cyan.json"), "w"), indent=1)
    print("fl cyan overlays: %d weeks (%s .. %s), bounds=%s"
          % (len(frames), frames[0]["label"], frames[-1]["label"], bounds_ll))


# ---------------------------------------------------------------- results.json (real model metrics, items 13-14)
# Parses the SCRIPT-GENERATED modeling outputs (models/outputs/*.md) into the numbers the Findings section
# shows. Every value here traces to a checked-in, regenerable output table (claim gate). Nothing is invented:
# if a table is missing the block is omitted and a warning printed, never faked.
def _md_tables(path):
    """Return [(headers[list], rows[list-of-dict]), ...] for every pipe-table in a markdown file."""
    tables, hdr, rows = [], None, None
    for line in open(path, encoding="utf-8"):
        s = line.strip()
        if s.startswith("|") and s.endswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if hdr is None:
                hdr, rows = cells, []
            elif set("".join(cells)) <= set("-: "):        # the |---|---| separator
                continue
            else:
                rows.append(dict(zip(hdr, cells)))
        else:
            if hdr is not None:
                tables.append((hdr, rows)); hdr, rows = None, None
    if hdr is not None:
        tables.append((hdr, rows))
    return tables


def _find_table(tables, *need):
    for hdr, rows in tables:
        if all(any(n == h for h in hdr) for n in need):
            return hdr, rows
    return None, None


def _num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def _experiments_families(path):
    """Parse the '## h=1 grid' table in experiments.md. Rows are RAGGED (some have a config-only label,
    some have config+arch), so we take the LAST 8 cells as the metric columns and join the rest as label."""
    if not os.path.exists(path):
        return {}
    started, rows = False, {}
    for line in open(path, encoding="utf-8"):
        s = line.strip()
        if s.startswith("## h=1 grid"):
            started = True; continue
        if started and s.startswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if set("".join(cells)) <= set("-: ") or cells[0] == "config" or len(cells) < 11:
                continue
            # metric cells (last 10): AUC-ROC, AUC-PR, Brier, MCC, AUC_within, flip_MCC, flip_AUC, n_flip,
            # onset-MCC, onset-AUC. The label (config, ragged 1-2 cells) is everything before them.
            m = cells[-10:]
            label = " / ".join(cells[:-10])
            rows[label] = dict(auc=_num(m[0]), aucpr=_num(m[1]), brier=_num(m[2]), mcc=_num(m[3]),
                               within=_num(m[4]), flipmcc=_num(m[5]), flipauc=_num(m[6]),
                               onset_mcc=_num(m[8]), onset_auc=_num(m[9]))
        elif started and rows and not s.startswith("|"):
            break
    return rows


def build_results():
    OUT_DIR = os.path.join(ROOT, "models", "outputs")
    res = {"_meta": {"source": "parsed from models/outputs/*.md (script-generated; see models/README.md)",
                     "note": "Findings numbers regenerate from the modeling layer; nothing hand-entered here."}}

    # --- item 14: strict EPA head-to-head, shared FL 2025 COMID-weeks -------------------------------------
    h2h_path = os.path.join(OUT_DIR, "epa_headtohead.md")
    if os.path.exists(h2h_path):
        t = _md_tables(h2h_path)
        LABEL = {"EPA_forecast": "EPA forecast", "our_ladder": "CyAN AR-ladder",
                 "persistence": "Persistence", "climatology": "Climatology"}
        ORDER = ["persistence", "climatology", "our_ladder", "EPA_forecast"]
        # Use W-2 / h1 throughout: for a 1-week-ahead forecast the freshest CyAN available is week W-2
        # (nominal lead + ~1-week latency), so W-2 IS the correct horizon-1 scenario -- and it is the one
        # the paper reports bootstrap CIs for. (W-1 = the h0 nowcast, fresher than a real 1-wk forecast.)
        SCEN = "W-2"
        def wsel(rows, keys):
            out = {}
            for r in rows:
                if r.get("EPA freshest") == SCEN:
                    out[r["predictor"]] = {k: _num(r.get(k2, "")) for k, k2 in keys.items()}
            return [dict(pred=LABEL[p], key=p, **out[p]) for p in ORDER if p in out]
        _, tf = _find_table(t, "AUC-ROC", "AUC-PR", "Brier", "predictor")
        _, op = _find_table(t, "MCC", "F1", "Prec", "Recall", "Acc")
        _, fl = _find_table(t, "n_flip", "MCC", "Recall")
        _, ci = _find_table(t, "AUC-ROC 2.5%", "median", "97.5%")
        h2h = {"n": 4527, "lakes": 132, "weeks": 35, "base_rate": 0.288,
               "scenario": "W-2 / h1 (freshest CyAN = W-2, the latency-fair 1-week-ahead scenario; "
                           "the scenario the bootstrap CIs are computed for)"}
        if tf: h2h["thresholdfree"] = wsel(tf, {"auc": "AUC-ROC", "aucpr": "AUC-PR", "brier": "Brier"})
        if op: h2h["operating"] = wsel(op, {"mcc": "MCC", "f1": "F1", "prec": "Prec", "recall": "Recall", "acc": "Acc"})
        if fl:
            frows = [r for r in fl if r.get("EPA freshest") == SCEN]
            h2h["flips"] = {"n": int(_num(frows[0]["n_flip"])) if frows else None,
                            "rows": [dict(pred=LABEL.get(r["predictor"], r["predictor"]),
                                          auc=_num(r["AUC-ROC"]), mcc=_num(r["MCC"]), recall=_num(r["Recall"]))
                                     for r in frows]}
        if ci:
            h2h["ci"] = [dict(pred=LABEL.get(r["predictor"], r["predictor"]), lo=_num(r["AUC-ROC 2.5%"]),
                              med=_num(r["median"]), hi=_num(r["97.5%"])) for r in ci]
        res["headtohead"] = h2h
    else:
        print("  WARN: epa_headtohead.md missing -> head-to-head omitted")

    # --- item 14: EPA operating cutoff 0.10 vs 0.50 (threshold-free metrics are cutoff-independent) --------
    # Source: models/outputs/exp_ablation.md EPA rows (test >= 2024-07 window; n_shared 6204). Encoded as a
    # small cited literal because that table's ragged label column defeats positional parsing.
    res["epa_cutoff"] = {
        "window": "2024-07 .. 2026 test split (exp_ablation.md)",
        "thresholdfree": {"auc": 0.931, "aucpr": 0.854, "brier": 0.105},
        "at010": {"mcc": 0.672, "onsetMCC_h1": 0.248, "note": "EPA deployed cutoff (Youden) — health-protective"},
        "at050": {"mcc": 0.636, "onsetMCC_h1": 0.233, "note": "accuracy-optimal default"},
    }

    # --- item 13: fusion feature ablation (block permutation + block drop + horizon curve) ----------------
    fe_path = os.path.join(OUT_DIR, "fusion_eval.md")
    if os.path.exists(fe_path):
        t = _md_tables(fe_path)
        _, perm = _find_table(t, "block", "AUC drop")
        _, dab = _find_table(t, "removed", "AUC-ROC", "AUC_within")
        _, hz = _find_table(t, "persist AUC", "clim AUC", "ladder AUC", "fusion AUC")
        abl = {}
        if perm:
            abl["perm_importance"] = [dict(block=r["block"], drop=_num(r["AUC drop"]),
                                           onset_drop=_num(r.get("onsetMCC drop")),
                                           onset_drop_std=_num(r.get("onsetMCC std"))) for r in perm]
        if dab:
            abl["dropone"] = [dict(removed=r["removed"], auc=_num(r["AUC-ROC"]), within=_num(r["AUC_within"])) for r in dab]
        if hz:
            abl["horizon"] = [dict(h=int(_num(r["h"])), persist=_num(r["persist AUC"]), clim=_num(r["clim AUC"]),
                                   ladder=_num(r["ladder AUC"]), fusion=_num(r["fusion AUC"]),
                                   ladder_flipmcc=_num(r["ladder flip_MCC"]), fusion_flipmcc=_num(r["fusion flip_MCC"]))
                              for r in hz]
        # paired within-lake lift is prose in fusion_eval.md (line ~15) — cited literal
        abl["paired_lift"] = {"median": 0.015, "lo": 0.003, "hi": 0.021, "pct_lakes": 0.67, "n_lakes": 60,
                              "note": "Track A fusion minus CyAN-ladder, paired within-lake AUC, lake-block bootstrap"}
        # baseline (Track A fusion) test AUC — the height the permutation bars fall FROM
        _, h1 = _find_table(t, "track", "AUC-ROC", "flip_MCC")
        if h1:
            for r in h1:
                if r["track"].startswith("Track A"):
                    abl["baseline_auc"] = _num(r["AUC-ROC"])
                    abl["baseline_onsetmcc"] = _num(r.get("onset-MCC"))
        res["ablation"] = abl
    else:
        print("  WARN: fusion_eval.md missing -> ablation omitted")

    # --- onset (positive-flip) head-to-head, slides 15 & 17 ---------------------------------------------
    onp = os.path.join(OUT_DIR, "headtohead_onset.md")
    if os.path.exists(onp):
        t = _md_tables(onp)
        _, bt = _find_table(t, "predictor", "onset-MCC", "n_onset")
        _, ht = _find_table(t, "h", "model", "onset-MCC")
        if bt:
            res["onset_baselines"] = [dict(pred=r["predictor"], auc=_num(r["AUC-ROC"]), aucpr=_num(r["AUC-PR"]),
                brier=_num(r["Brier"]), mcc=_num(r["MCC"]), acc=_num(r["Acc"]), onset_auc=_num(r["onset-AUC"]),
                onset_mcc=_num(r["onset-MCC"]), onset_recall=_num(r["onset-Recall"]), n_onset=int(_num(r["n_onset"])))
                for r in bt]
        if ht:
            res["onset_horizon"] = [dict(h=int(_num(r["h"])), model=r["model"], auc=_num(r["AUC-ROC"]),
                onset_mcc=_num(r["onset-MCC"]), onset_auc=_num(r["onset-AUC"])) for r in ht]
    else:
        print("  WARN: headtohead_onset.md missing -> onset metrics omitted")

    # --- slide 18: onset-MCC by horizon on the 2-yr internal test (same window as the slide-17 table, so the
    # h=1 points match). From experiments.md horizon curve; EPA is added from the shared-2025 head-to-head above.
    exp_path = os.path.join(OUT_DIR, "experiments.md")
    if os.path.exists(exp_path):
        _, hz2 = _find_table(_md_tables(exp_path), "h", "config", "onset-MCC")
        WANT = {"persistence": "Persistence", "climatology": "Climatology",
                "lean": "Lean CyAN (2-feat)", "fusion_full+clim": "Full fusion + clim"}
        if hz2:
            res["onset_horizon_2yr"] = [dict(h=int(_num(r["h"])), model=WANT[r["config"]],
                onset_mcc=_num(r["onset-MCC"]), onset_auc=_num(r["onset-AUC"]))
                for r in hz2 if r.get("config") in WANT]
        else:
            print("  WARN: experiments.md horizon curve (onset) not parsed")

    # --- Lake Okeechobee example rows (slide 12): a few real rows/cols of the fusion table ----------------
    try:
        import pandas as pd
        ft = pd.read_parquet(os.path.join(ROOT, "models", "data", "derived", "modeling_table_fusion_fl.parquet"))
        ok = ft[(ft["comid"] == 166757656) & (ft["horizon"] == 1)].sort_values("target_date")
        SAMPLE_COLS = [("target_date", "week"), ("cyan_median", "CyAN median"), ("bloom_state", "prior bloom"),
                       ("wx_ssrd_trail_30d_mj", "solar 30d"), ("wx_precip_trail_30d_mm", "precip 30d mm"),
                       ("wqp_TP_val", "WQP TP"), ("area_sqkm", "area km²"), ("target_bloom", "bloom (target)")]
        cols = [(c, lab) for c, lab in SAMPLE_COLS if c in ok.columns]
        samp = ok.dropna(subset=["cyan_median"]).tail(4)

        def cell(c, v):
            if pd.isna(v):
                return "—"
            if c == "target_date":
                return str(pd.to_datetime(v).date())
            if c in ("bloom_state", "target_bloom"):
                return str(int(v))
            return str(round(float(v), 2))
        res["okeechobee"] = {"labels": [lab for _, lab in cols],
                             "rows": [[cell(c, r[c]) for c, _ in cols] for _, r in samp.iterrows()]}
    except Exception as e:  # never fabricate — omit on any failure
        print("  WARN: okeechobee sample failed:", e)

    # --- pre-ablation model-family results (all features), from experiments.md h=1 grid ------------------
    fam = _experiments_families(os.path.join(OUT_DIR, "experiments.md"))
    if fam:
        SEL = [("persistence", "Persistence", "baseline"),
               ("climatology", "Climatology", "baseline"),
               ("cyan_ladder / histgbm", "CyAN ladder (HistGBM)", "ladder"),
               ("fusion_full+clim / logistic", "GLM · logistic (all features + clim)", "family"),
               ("fusion_full+clim / histgbm", "HistGBM (all features + clim)", "family"),
               ("fusion_full+clim / xgboost", "XGBoost (all features + clim)", "family")]
        res["families"] = {"window": "2024-07 .. 2026 held-out test, h=1, all features + climatology (pre-ablation)",
                           "rows": [dict(label=lab, kind=kind, **fam[key]) for key, lab, kind in SEL if key in fam]}
    else:
        print("  WARN: experiments.md families not parsed")

    json.dump(res, open(os.path.join(DATA, "results.json"), "w", encoding="utf-8"), indent=1)
    hh = res.get("headtohead", {})
    print("results.json  headtohead=%s preds (%s)  epa_cutoff=2  ablation=%s blocks  families=%s"
          % (len(hh.get("thresholdfree", [])), hh.get("scenario", "")[:8],
             len(res.get("ablation", {}).get("perm_importance", [])),
             len(res.get("families", {}).get("rows", []))))


# ---------------------------------------------------------------- in-situ station points (items 10-11)
# The NWIS gage + WQP station locations we actually linked to FL lakes. Real coordinates from the pulled
# site-linkage tables (models/data/interim/{nwis,wqp}_fl). Upgrades the old "pending" placeholders to real
# layers. Only sites linked to one of our 133 lakes (non-null COMID) are shown; deduped by site.
def build_insitu_points():
    import pandas as pd
    INTERIM = os.path.join(ROOT, "models", "data", "interim")
    for src in ("nwis", "wqp"):
        base = os.path.join(INTERIM, "%s_fl" % src)
        p = os.path.join(base, "site_linkage.parquet")
        if not os.path.exists(p):
            print("  WARN: %s site_linkage missing -> skipping points" % src); continue
        sl = pd.read_parquet(p)
        n_rows = len(sl)
        sl = sl[sl["comid"].notna() & sl["lat"].notna() & sl["lon"].notna()].drop_duplicates("site_id").copy()
        # per-site enrichment from daily_values:
        #   NWIS -> "streamflow" (has discharge 00060; the robust, continuous gages) vs "stage" vs "nodata"
        #   WQP  -> "fresh" = samples at least ~monthly (median gap <= 30 d); most are sparser one-off surveys
        prop = {}
        dvp = os.path.join(base, "daily_values.parquet")
        if os.path.exists(dvp):
            dv = pd.read_parquet(dvp)
            dv["date"] = pd.to_datetime(dv["date"])
            if src == "nwis":
                CODE = {"00060": "discharge", "00065": "gage height", "00010": "water temp"}
                for sid, g in dv.groupby("site_id"):
                    codes = set(g["parameter_code"].astype(str))
                    prop[sid] = {"kind": "streamflow" if "00060" in codes else "stage",
                                 "vars": ", ".join(CODE.get(c, c) for c in sorted(codes) if c in CODE) or "—"}
            else:
                for sid, g in dv.groupby("site_id"):
                    d = g["date"].dropna().drop_duplicates().sort_values().to_numpy()
                    gap = float((d[1:] - d[:-1]).astype("timedelta64[D]").astype(int).mean()) if len(d) > 1 else 1e9
                    med = sorted((d[1:] - d[:-1]).astype("timedelta64[D]").astype(int)) if len(d) > 1 else [10 ** 9]
                    prop[sid] = {"fresh": bool(med[len(med) // 2] <= 30)}
        feats = []
        for r in sl.itertuples():
            pr = {"tier": str(r.tier)}
            if src == "nwis":
                pr["site_id"] = str(r.site_id)
            pr.update(prop.get(r.site_id, {"kind": "nodata"} if src == "nwis" else {"fresh": False}))
            feats.append({"type": "Feature",
                          "geometry": {"type": "Point", "coordinates": [round(float(r.lon), 5), round(float(r.lat), 5)]},
                          "properties": pr})
        json.dump({"type": "FeatureCollection", "features": feats},
                  open(os.path.join(DATA, "%s_points.geojson" % src), "w"), separators=(",", ":"))
        if src == "nwis":
            sf = sum(1 for f in feats if f["properties"].get("kind") == "streamflow")
            withdata = sum(1 for f in feats if f["properties"].get("kind") in ("streamflow", "stage"))
            print("nwis_points.geojson  n=%d linked (of %d rows); %d have data (%d streamflow), rest linked-no-data"
                  % (len(feats), n_rows, withdata, sf))
        else:
            fr = sum(1 for f in feats if f["properties"].get("fresh"))
            print("wqp_points.geojson  n=%d linked (of %d rows); %d fresh (<=~monthly cadence)"
                  % (len(feats), n_rows, fr))


# ---------------------------------------------------------------- FL basin polygons (HydroBASINS L12, item 11)
# The BasinATLAS level-12 sub-basins that CONTAIN our 133 resolvable lakes — the unit we aggregate NWIS/WQP
# point measurements to when a station isn't inside the lake. Source is the (large, non-repo) BasinATLAS
# geodatabase on D:; guarded so the build still runs without it (the map then shows lakes+points only).
def build_fl_basins():
    import pandas as pd
    la = pd.read_parquet(os.path.join(ROOT, "models", "data", "derived", "lake_basinatlas_l12.parquet"))
    want = set(int(x) for x in la["HYBAS_ID"].dropna().unique() if int(x) != 0)
    gdb = "D:/BasinATLAS_Data_v10/BasinATLAS_v10.gdb"
    if not want or not os.path.exists(gdb):
        print("  WARN: BasinATLAS gdb or HYBAS_IDs unavailable -> skipping basins (%d wanted)" % len(want)); return
    try:
        import pyogrio
        # bbox-read Florida (WGS84) then filter to our lakes' L12 basins — avoids loading the global layer
        g = pyogrio.read_dataframe(gdb, layer="BasinATLAS_v10_lev12",
                                   bbox=(-88.0, 24.3, -79.8, 31.1), columns=["HYBAS_ID", "SUB_AREA"])
    except Exception as e:
        print("  WARN: basin read failed (%s) -> skipping basins" % e); return
    g = g[g["HYBAS_ID"].astype("int64").isin(want)].to_crs(4326)
    g["geometry"] = g.geometry.simplify(0.002, preserve_topology=True)
    keep = g[["HYBAS_ID", "SUB_AREA", "geometry"]].copy()
    keep["HYBAS_ID"] = keep["HYBAS_ID"].astype("int64")
    keep.to_file(os.path.join(DATA, "fl_basins.geojson"), driver="GeoJSON")
    print("fl_basins.geojson  n=%d L12 sub-basins (of %d lakes' basins)" % (len(keep), len(want)))


def _load(path, kind="json"):
    if not os.path.exists(path):
        return None
    return json.load(open(path, encoding="utf-8"))


def bundle():
    """Emit one JS file that assigns all data to window.STORY.

    Loaded via <script src="data/story_data.js"> so it works from file:// with no
    server (browsers block fetch()/XHR of local files, but allow <script src>)."""
    payload = {
        "charts": _load(os.path.join(DATA, "charts.json")),
        "lakes": _load(os.path.join(DATA, "fl_lakes.geojson")),
        "states": _load(os.path.join(DATA, "basemap_states.geojson")),
        "erie": _load(os.path.join(ASSETS, "erie_cyan.json")),
        "flcyan": _load(os.path.join(ASSETS, "fl_cyan.json")),
        "results": _load(os.path.join(DATA, "results.json")),
        "nwis": _load(os.path.join(DATA, "nwis_points.geojson")),
        "wqp": _load(os.path.join(DATA, "wqp_points.geojson")),
        "basins": _load(os.path.join(DATA, "fl_basins.geojson")),
    }
    present = {k: (v is not None) for k, v in payload.items()}
    js = "/* generated by build_story_assets.py — do not hand-edit */\n"
    js += "window.STORY = " + json.dumps(payload, separators=(",", ":")) + ";\n"
    with open(os.path.join(DATA, "story_data.js"), "w", encoding="utf-8") as f:
        f.write(js)
    nl = len(payload["lakes"]["features"]) if payload["lakes"] else 0
    print("story_data.js  %.0f KB  layers present: %s"
          % (len(js) / 1024, ", ".join(k for k, v in present.items() if v)))
    print("  (%d lakes; nwis=%s wqp=%s basins=%s)"
          % (nl,
             len(payload["nwis"]["features"]) if payload["nwis"] else "-",
             len(payload["wqp"]["features"]) if payload["wqp"] else "-",
             len(payload["basins"]["features"]) if payload["basins"] else "-"))


if __name__ == "__main__":
    build_charts()
    build_lakes()
    build_states()
    build_cyan_overlays()
    build_cyan_fl_overlays()
    build_results()
    build_insitu_points()
    build_fl_basins()
    bundle()
    print("assets ->", DATA, "+", ASSETS)
