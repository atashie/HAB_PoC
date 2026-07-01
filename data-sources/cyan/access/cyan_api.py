"""CyAN CI_cyano product: encoding constants, DN<->CI math, filename parsing, file search.

Everything here is grounded in the V6 release notes (see
``data-sources/cyan/reference/CyAN_V6_release_notes_extracted.txt``) and the
empirical API checks documented in ``data-sources/cyan/METADATA.md``.

No network side effects on import. ``search_files`` is the only function that hits
the network, and it takes a caller-provided requests.Session (see _common.net).
"""
from __future__ import annotations

import datetime as _dt
import re
from dataclasses import dataclass, asdict
from typing import Iterable, Optional

import numpy as np


# --------------------------------------------------------------------------- #
# DN encoding (authoritative — V6 release notes, GeoTIFF section)
# --------------------------------------------------------------------------- #
DN_BELOW_DETECTION = 0          # water observed, no cyano above detection limit (NOT missing)
DN_VALID_MIN = 1
DN_VALID_MAX = 253              # 1..253 inclusive are valid CI data
DN_LAND = 254
DN_NODATA = 255                 # cloud, ice, or no valid retrieval

# DN -> CI_cyano (index, sr^-1):  CI = 10 ** (DN * slope + intercept)
CI_SLOPE = 0.011714
CI_INTERCEPT = -4.1870866

# CI_cyano -> approximate cyanobacteria cell density (cells/mL).
# Standard CyAN relation cells/mL ~= 1e8 * CI_cyano (Lunetta et al. 2015). This maps
# the valid DN range (1..253) to ~6.7e3 .. ~6.0e6 cells/mL. APPROXIMATE: the CI-to-cell
# relationship carries real scatter/uncertainty and varies by assemblage — never quote
# it as an exact measurement.
CELLS_PER_ML_FACTOR = 1.0e8

# NOAA/NCCOS CI uses a DIFFERENT encoding (land=252, valid 0-250). These files are
# NOT that product — see METADATA.md §4.1. Guard constants kept for clarity/tests.
NOAA_DN_LAND = 252


def dn_to_ci(dn: np.ndarray) -> np.ndarray:
    """Vectorized DN -> CI_cyano. Non-valid DN (0, 254, 255) become NaN.

    Note: DN 0 (below detection) is returned as NaN here *for the CI magnitude*,
    because there is no meaningful CI value below the detection threshold. Callers
    that need to distinguish 'non-detect' from 'no-data' should use ``classify_dn``.
    """
    dn = np.asarray(dn)
    valid = (dn >= DN_VALID_MIN) & (dn <= DN_VALID_MAX)
    out = np.full(dn.shape, np.nan, dtype="float64")
    out[valid] = 10.0 ** (dn[valid].astype("float64") * CI_SLOPE + CI_INTERCEPT)
    return out


def read_processing_version(path) -> Optional[str]:
    """Read the CyAN processing version from a GeoTIFF's metadata tags (e.g. '6.0',
    '6T'). Returns None if no version tag is present. Verified from the DATA, not the
    filename (see METADATA.md §10). Opens metadata only — does not read pixels.
    """
    import rasterio
    with rasterio.open(path) as ds:
        tags = ds.tags()
    for k, v in tags.items():
        if "version" in k.lower():
            return str(v)
    for k, v in tags.items():                       # fallback: version embedded in a value
        if isinstance(v, str) and "CYAN" in v.upper() and "V" in v.upper():
            return str(v)
    return None


def ci_to_cells_per_ml(ci: np.ndarray) -> np.ndarray:
    """Approximate cyanobacteria cell density (cells/mL) from CI_cyano.

    cells/mL ~= 1e8 * CI (Lunetta et al. 2015). APPROXIMATE — see CELLS_PER_ML_FACTOR.
    """
    return np.asarray(ci) * CELLS_PER_ML_FACTOR


def classify_dn(dn: np.ndarray) -> dict[str, np.ndarray]:
    """Return boolean masks for each DN category (mutually exclusive)."""
    dn = np.asarray(dn)
    return {
        "below_detection": dn == DN_BELOW_DETECTION,
        "valid": (dn >= DN_VALID_MIN) & (dn <= DN_VALID_MAX),
        "land": dn == DN_LAND,
        "nodata": dn == DN_NODATA,
    }


# --------------------------------------------------------------------------- #
# API vocabulary (cyan_file_search form params)
# --------------------------------------------------------------------------- #
SEARCH_URL = "https://oceandata.sci.gsfc.nasa.gov/api/cyan_file_search"
GETFILE_BASE = "https://oceandata.sci.gsfc.nasa.gov/getfile/"

REGION = {"conus": 1, "alaska": 0, "ak": 0}
PERIOD = {"daily": 2, "weekly": 1}          # weekly == 7-day max composite
PRODUCT = {"ci": 1, "ci_cyano": 1, "truecolor": 2, "tc": 2}

# A few reference tiles (col_row) confirmed from the V6 release notes examples.
# Not exhaustive — use the published tile-grid shapefile for authoritative lookup.
REFERENCE_TILES = {
    "lake_erie": "7_2",
    "utah_lake": "3_3",
    "central_wisconsin": "6_2",
    "florida": "6_2",            # note: release notes text is internally inconsistent
    "lake_pontchartrain": "7_2",
    "central_california": "1_3",
}


# --------------------------------------------------------------------------- #
# Filename parsing
# --------------------------------------------------------------------------- #
_SENSOR = {"L": "OLCI/Sentinel-3", "M": "MERIS/Envisat"}


def _yyyyddd_to_date(token: str) -> _dt.date:
    year = int(token[:4])
    doy = int(token[4:7])
    return _dt.date(year, 1, 1) + _dt.timedelta(days=doy - 1)


@dataclass
class CyanFile:
    filename: str
    url: str
    sensor: str            # 'OLCI/Sentinel-3' | 'MERIS/Envisat'
    sensor_code: str       # 'L' | 'M'
    start_date: str        # ISO date
    end_date: str          # ISO date (== start_date for dailies)
    temporal: str          # 'DAY' | '7D'
    stream: str            # 'CYANV6T' | 'CYAN'
    product: str           # 'CI_cyano' | 'tc' | ...
    region: str            # 'CONUS' | 'AK'
    resolution: str        # '300m'
    tile: str              # '<col>_<row>' for tiles; '<region>_mosaic' for mosaics
    is_mosaic: bool = False  # True for whole-region mosaics (areaids=all)

    def as_dict(self) -> dict:
        return asdict(self)


_DATE_RE = re.compile(r"^([LM])(\d{7})(\d{7})?$")


def parse_cyan_filename(name_or_url: str) -> Optional[CyanFile]:
    """Parse a CyAN L3m GeoTIFF filename (or getfile URL) into structured fields.

    Returns None if the name doesn't match the expected CI_cyano tile pattern
    (e.g. true-color files, or unexpected formats) so callers can filter cleanly.
    """
    url = name_or_url
    filename = name_or_url.rsplit("/", 1)[-1]
    stem = filename[:-4] if filename.lower().endswith(".tif") else filename

    if "." not in stem:
        return None
    datepart, _, rest = stem.partition(".")
    m = _DATE_RE.match(datepart)
    if not m:
        return None
    sensor_code = m.group(1)
    start_tok = m.group(2)
    end_tok = m.group(3) or m.group(2)
    try:
        start_date = _yyyyddd_to_date(start_tok).isoformat()
        end_date = _yyyyddd_to_date(end_tok).isoformat()
    except ValueError:
        return None

    tokens = rest.split("_")
    # Tile:   L3m, DAY|7D, STREAM, CI, cyano, CYAN, CONUS|AK, 300m, col, row  (10 tokens)
    # Mosaic: L3m, DAY|7D, STREAM, CI, cyano, CYAN, CONUS|AK, 300m            (8 tokens)
    if len(tokens) < 8 or "CI" not in tokens or "cyano" not in tokens:
        return None
    level = tokens[0]                       # L3m (validated below)
    temporal = tokens[1]                    # DAY | 7D
    stream = tokens[2]                      # CYANV6T | CYAN
    if level != "L3m" or temporal not in ("DAY", "7D"):
        return None
    region = "AK" if "AK" in tokens else ("CONUS" if "CONUS" in tokens else "?")
    res_idx = next((i for i, t in enumerate(tokens)
                    if t.endswith("m") and t[:-1].isdigit()), None)
    if res_idx is None:
        return None
    resolution = tokens[res_idx]
    trailing = tokens[res_idx + 1:]        # tile -> [col, row]; mosaic -> []
    if len(trailing) >= 2 and trailing[-2].isdigit() and trailing[-1].isdigit():
        tile, is_mosaic = f"{trailing[-2]}_{trailing[-1]}", False
    elif len(trailing) == 0:
        tile, is_mosaic = f"{region}_mosaic", True
    else:
        return None

    return CyanFile(
        filename=filename, url=url, sensor=_SENSOR.get(sensor_code, sensor_code),
        sensor_code=sensor_code, start_date=start_date, end_date=end_date,
        temporal=temporal, stream=stream, product="CI_cyano",
        region=region, resolution=resolution, tile=tile, is_mosaic=is_mosaic,
    )


_PER_SATELLITE_RE = re.compile(r"^S3[AB]_OLCI", re.IGNORECASE)


def categorize_search_results(urls: Iterable[str]) -> dict[str, list]:
    """Split raw search URLs into merged CI tiles / per-satellite / other.

    A cyan_file_search response mixes the MERGED S3A+3B product (``L…`` names)
    with single-sensor products (``S3A_OLCI_EFRNT…`` / ``S3B_…``). We use only the
    merged product; this function makes the split explicit so nothing is dropped
    silently (see METADATA.md §7.1).

    Returns dict with keys: 'merged' (list[CyanFile]), 'per_satellite' (list[str]),
    'other' (list[str]).
    """
    merged: list[CyanFile] = []
    per_satellite: list[str] = []
    other: list[str] = []
    for u in urls:
        fn = u.rsplit("/", 1)[-1]
        parsed = parse_cyan_filename(u)
        if parsed is not None:
            merged.append(parsed)
        elif _PER_SATELLITE_RE.match(fn):
            per_satellite.append(u)
        else:
            other.append(u)
    return {"merged": merged, "per_satellite": per_satellite, "other": other}


def prefer_stream(files: Iterable[CyanFile], preferred: str = "CYAN") -> list[CyanFile]:
    """Collapse duplicate (date, tile, temporal) entries to one file per group.

    Both 'CYANV6T' and plain 'CYAN' variants can coexist for a date (see
    METADATA.md §10). We keep ``preferred`` when present, else the other.
    Default is 'CYAN' (OBPG_version 6.0), which spans the whole record -> a
    consistent series; 'CYANV6T' exists only for a subset and would mix batches.
    """
    by_key: dict[tuple, CyanFile] = {}
    for f in files:
        key = (f.temporal, f.region, f.tile, f.start_date, f.end_date)
        cur = by_key.get(key)
        if cur is None:
            by_key[key] = f
        elif f.stream == preferred and cur.stream != preferred:
            by_key[key] = f
    return sorted(by_key.values(), key=lambda x: (x.start_date, x.tile))


# --------------------------------------------------------------------------- #
# File search (cyan_file_search)
# --------------------------------------------------------------------------- #
def search_files(
    session,
    region: str,
    period: str,
    product: str,
    areaids: str,
    sdate: str,
    edate: str,
    tries: int = 6,
) -> list[str]:
    """Query cyan_file_search and return a list of getfile URLs.

    Raises RuntimeError if the endpoint never returns a usable body (it
    intermittently 502s; the session already retries, and we add an app-level
    retry loop as belt-and-suspenders).
    """
    form = {
        "region": REGION[region.lower()],
        "period": PERIOD[period.lower()],
        "product": PRODUCT[product.lower()],
        "areaids": areaids,
        "sdate": sdate,
        "edate": edate,
        "addurl": 1,
        "results_as_file": 1,
        "wgetflag": 1,
    }
    last = None
    for _ in range(tries):
        resp = session.post(SEARCH_URL, data=form, timeout=90)
        last = resp
        body = resp.text or ""
        if resp.status_code == 200:
            if "getfile" in body:
                return [ln.strip() for ln in body.splitlines()
                        if ln.strip().startswith("http")]
            # No matches: the API may return a plain "No Results", an empty body, or
            # (with results_as_file=1) the full HTML search-UI page — e.g. for the
            # 2012-2016 gap. All mean "nothing available", not a transient error.
            low = body.lower()
            if (not body.strip() or "no results" in low
                    or "<!doctype html" in low or "<html" in low):
                return []
    raise RuntimeError(
        f"cyan_file_search failed after {tries} attempts "
        f"(last status={getattr(last, 'status_code', '?')}). "
        f"Params={form}. The endpoint is known to 502 intermittently — try again."
    )
