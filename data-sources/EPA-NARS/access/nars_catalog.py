"""Catalog of EPA National Lakes Assessment (NLA) downloadable data files.

Why this module exists
----------------------
NARS has **no REST API**. Data are published as static, flat CSV files (each with a
companion ``.txt`` metadata dictionary) at stable ``epa.gov`` URLs, plus an interactive
R-Shiny "NARS Data Download Tool" (https://rconnect-public.epa.gov/nars-data-download/)
that is a browser app, not machine-callable. The files are small and static per 5-year
cycle, so the right strategy is: **mirror the flat files locally, cache with sha256.**

This module provides two things, kept deliberately separate:

1. ``PINNED`` — a curated, *verified* manifest of NLA file URLs (harvested and checked
   on 2026-07-01). This is the reproducible source of truth: pinning URLs means a pull
   regenerates the exact same bytes regardless of later page edits.

2. ``discover()`` + ``reconcile()`` — parse the live NARS data page and diff it against
   ``PINNED`` so we *notice* when EPA adds or revises a file (they publish indicators
   incrementally — e.g. NLA22 phytoplankton landed 2025-01, ~2.5 yr after fieldwork).
   Drift is surfaced, never silently absorbed.

The pure parsing helpers (``cycle_of``, ``indicator_of``, ``kind_of``) are unit-tested.
Downloading lives in ``pull_nars.py``; this module performs no I/O except ``discover()``.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Iterable, Optional

NARS_DATA_PAGE = (
    "https://www.epa.gov/national-aquatic-resource-surveys/"
    "data-national-aquatic-resource-surveys"
)

# Base for all NLA file URLs used below (keeps the PINNED table readable).
_SYS = "https://www.epa.gov/system/files/other-files"
_SITES = "https://www.epa.gov/sites/default/files"


# --------------------------------------------------------------------------- #
# File reference
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class FileRef:
    """One logical NLA data file: the data payload + (optional) metadata dictionary."""

    data_url: str
    meta_url: Optional[str] = None  # companion .txt field dictionary, if published
    note: str = ""


# --------------------------------------------------------------------------- #
# Pure filename parsers (unit-tested)
# --------------------------------------------------------------------------- #
# NLA filenames use two cycle spellings: 2-digit (nla22_) and 4-digit (nla2022_ / nla_2022_).
# Other NARS surveys (nrsa/nwca/ncca/wsa/nca) must NOT be read as NLA.
_TWO_DIGIT = {"07": 2007, "12": 2012, "17": 2017, "22": 2022}


def cycle_of(name: str) -> Optional[int]:
    """Return the NLA survey cycle year for a filename, or None if not an NLA file.

    Handles ``nla22_``, ``nla2022_``, ``nla_2017_`` and the multi-cycle
    ``nla2007-2022_...`` population-estimate file (anchored to the newest year).
    """
    base = name.rsplit("/", 1)[-1].lower()
    if not base.startswith("nla"):
        return None

    # Multi-cycle span like "nla2007-2022_..." -> newest year in the span.
    span = re.match(r"nla(\d{4})-(\d{4})", base)
    if span:
        return max(int(span.group(1)), int(span.group(2)))

    # 4-digit: nla2022_ / nla_2022_
    four = re.match(r"nla_?(\d{4})", base)
    if four:
        yr = int(four.group(1))
        return yr if yr in _TWO_DIGIT.values() else None

    # 2-digit: nla22_ / nla07_ ...
    two = re.match(r"nla(\d{2})[_\.]", base)
    if two:
        return _TWO_DIGIT.get(two.group(1))

    return None


# Canonical indicator <- ordered list of substring tokens that identify it.
# Order matters: more specific patterns first (e.g. site_information before generic).
_INDICATOR_TOKENS: list[tuple[str, tuple[str, ...]]] = [
    ("siteinfo", ("siteinfo", "site_information", "site_info")),
    ("popest", ("forpopestimates", "popestimates", "popest")),
    ("condition", ("condition",)),
    ("waterchem", ("waterchem",)),
    ("algaltoxins", ("algaltoxin",)),
    ("atrazine", ("atrazine",)),
    ("chla", ("chlorophyll", "chla")),
    ("secchi", ("secchi",)),
    ("profile", ("profile",)),
    ("phab", ("phab",)),           # phab_wide and phabmets_wide both -> phab theme
    ("landscape", ("landscape",)),
    ("benthic", ("benthic",)),
    ("zooplankton", ("zooplankton",)),
    ("phytoplankton", ("phytoplankton",)),
    ("enterococci", ("enterococci",)),
    ("sample_grid", ("sample_grid",)),
    ("lakes_shp", ("_lakes.zip", "lakes.zip")),
    ("basins_shp", ("_basins.zip", "basins.zip")),
]


def indicator_of(name: str) -> Optional[str]:
    """Return the canonical indicator key for an NLA filename, or None if unrecognized."""
    base = name.rsplit("/", 1)[-1].lower()
    for key, tokens in _INDICATOR_TOKENS:
        if any(tok in base for tok in tokens):
            return key
    return None


def kind_of(name: str) -> Optional[str]:
    """Classify a file as 'data' (.csv), 'meta' (.txt dictionary), or 'spatial' (.zip)."""
    base = name.rsplit("/", 1)[-1].lower()
    if base.endswith(".csv"):
        return "data"
    if base.endswith(".txt"):
        return "meta"
    if base.endswith(".zip"):
        return "spatial"
    return None


# --------------------------------------------------------------------------- #
# PINNED manifest — verified 2026-07-01 from the NARS data page
# --------------------------------------------------------------------------- #
# NLA 2022. Data (.csv/.zip) URLs harvested from the live page and each downloaded &
# inspected. Companion metadata .txt dictionaries paired where published. The mixed
# date folders (2024-04 / 2024-08 / 2025-01) reflect EPA's incremental publication.
#
# Each indicator maps to a LIST of FileRefs because several themes ship multiple files
# (e.g. benthic = counts + metrics + taxa + MMI). Pinning them all makes --check-drift
# a clean baseline: it then lights up only on a genuine future addition/re-publish.
PINNED: dict[int, dict[str, list[FileRef]]] = {
    2022: {
        # ---- core HAB-relevant indicators (single file each) ----
        "siteinfo": [FileRef(
            f"{_SYS}/2024-08/nla22_siteinfo.csv",
            f"{_SYS}/2024-04/nla22_siteinfo.txt",
            note="Site descriptors + full geospatial/hydrography linkage (COMID, HUC8, "
                 "lat/lon NAD83, ecoregions) + survey design weights. The join hub.",
        )],
        "waterchem": [FileRef(
            f"{_SYS}/2024-08/nla22_waterchem_wide.csv",
            f"{_SYS}/2024-08/nla22_waterchem_wide.txt",
            note="Wide: NTL, PTL, dissolved N/P, nitrate, ammonia, DOC, turbidity, pH, "
                 "conductivity, ANC, color, silica, major ions, and CHLA (chlorophyll-a). "
                 "Each analyte carries RESULT/UNITS/MDL/RL/NARS_FLAG/QA_FLAG.",
        )],
        "algaltoxins": [FileRef(
            f"{_SYS}/2024-08/nla22_algaltoxins.csv",
            f"{_SYS}/2024-04/nla22_algaltoxins.txt",
            note="Long: ANALYTE in {MICX=microcystin, CYLSPER=cylindrospermopsin}; "
                 "RESULT/MDL/RL + NARS_FLAG (ND=non-detect etc). Keyed by UID.",
        )],
        "secchi": [FileRef(
            f"{_SYS}/2024-08/nla22_secchi.csv",
            f"{_SYS}/2024-04/nla22_secchi.txt",
            note="Secchi transparency (clarity).",
        )],
        "profile": [FileRef(
            f"{_SYS}/2024-08/nla2022_profile_wide.csv",
            f"{_SYS}/2024-08/nla2022_profile_wide.txt",
            note="Depth profile (temp / DO / pH / conductivity vs depth).",
        )],
        # ---- watershed / physical context ----
        "phab": [
            FileRef(
                f"{_SYS}/2024-08/nla2022_phab_wide.csv",
                f"{_SYS}/2024-08/nla2022_phab_wide.txt",
                note="Physical habitat, raw wide.",
            ),
            FileRef(
                f"{_SYS}/2024-08/nla2022_phabmets_wide_0.csv",
                f"{_SYS}/2024-08/nla2022_phabmets_wide.txt",
                note="Physical habitat, derived metrics.",
            ),
        ],
        "landscape": [FileRef(
            f"{_SYS}/2024-08/nla2022_landscape_wide_0.csv",
            f"{_SYS}/2024-08/nla2022_landscape_wide_0.txt",
            note="Watershed/landscape metrics (LakeCat-style) keyed to the lake.",
        )],
        "atrazine": [FileRef(
            f"{_SYS}/2024-08/nla22_atrazine.csv",
            f"{_SYS}/2024-04/nla22_atrazine.txt",
            note="Atrazine herbicide screen.",
        )],
        # ---- biology (multi-file themes) ----
        "phytoplankton": [
            FileRef(
                f"{_SYS}/2025-01/nla2022_phytoplanktoncount_wide.csv",
                f"{_SYS}/2025-01/nla2022_phytoplanktoncount_wide.txt",
                note="Phytoplankton counts (published 2025-01, ~2.5 yr post-fieldwork).",
            ),
            FileRef(
                f"{_SYS}/2025-01/nla2022_phytoplanktontaxa.csv",
                f"{_SYS}/2025-01/nla2022_phytoplanktontaxa.txt",
                note="Phytoplankton taxa list.",
            ),
        ],
        "zooplankton": [
            FileRef(f"{_SYS}/2024-08/nla22_zooplanktoncount_wide.csv",
                    f"{_SYS}/2024-04/nla22_zooplanktoncount_wide.txt", note="Zooplankton counts."),
            FileRef(f"{_SYS}/2024-08/nla22_zooplanktontaxa.csv",
                    f"{_SYS}/2024-04/nla22_zooplanktontaxa.txt", note="Zooplankton taxa."),
            FileRef(f"{_SYS}/2024-08/nla22_zooplankton_metrics.csv",
                    f"{_SYS}/2024-08/nla22_zooplankton_metrics.txt", note="Zooplankton metrics."),
            FileRef(f"{_SYS}/2024-08/nla22_zooplankton_mmi_1.csv",
                    f"{_SYS}/2024-08/nla22_zooplankton_mmi.txt", note="Zooplankton MMI."),
        ],
        "benthic": [
            FileRef(f"{_SYS}/2024-08/nla22_benthic_counts.csv",
                    f"{_SYS}/2024-04/nla22_benthic_counts.txt", note="Benthic macroinvert counts."),
            FileRef(f"{_SYS}/2024-08/nla22_benthic_metrics.csv",
                    f"{_SYS}/2024-04/nla22_benthic_metrics.txt", note="Benthic metrics."),
            FileRef(f"{_SYS}/2024-08/nla22_benthic_taxa.csv",
                    f"{_SYS}/2024-04/nla22_benthic_taxa.txt", note="Benthic taxa."),
            FileRef(f"{_SYS}/2024-08/nla22_benthic_mmi_0.csv",
                    f"{_SYS}/2024-08/nla22_benthic_mmi.txt", note="Benthic MMI."),
        ],
        "enterococci": [FileRef(
            f"{_SYS}/2024-08/nla22_enterococci.csv",
            f"{_SYS}/2024-04/nla22_enterococci.txt",
            note="Enterococci (recreational pathogen indicator).",
        )],
        # ---- design / assessment products ----
        "condition": [FileRef(
            f"{_SYS}/2024-08/nla22_condition_combined_2024-08-13_0.csv",
            f"{_SYS}/2024-08/nla2022_condition_estimates_metadata_0.txt",
            note="Per-lake condition class assignments used for the report.",
        )],
        "popest": [FileRef(
            f"{_SYS}/2024-08/nla2007-2022_data_forpopestimates_indexvisits_probsites_0.csv",
            f"{_SYS}/2024-08/nla2007-2022_metadata_forpopestimates_allvisits_allsitetypes_0.txt",
            note="Multi-cycle (2007-2022) probability-site index visits prepared for "
                 "WEIGHTED population estimation. Use the design weights, not raw counts.",
        )],
        "sample_grid": [FileRef(
            f"{_SYS}/2024-08/nla2022_sample_grid.csv",
            f"{_SYS}/2024-04/nla2022_sample_grid.txt",
            note="Survey design sample grid.",
        )],
        # ---- spatial (shapefile zips; no .txt dictionary) ----
        "lakes_shp": [FileRef(
            f"{_SYS}/2024-08/nla2022_lakes.zip",
            None,
            note="Sampled-lake polygons (NHD-derived). Enables polygon-based CyAN pixel "
                 "extraction instead of a single centroid point.",
        )],
        "basins_shp": [FileRef(
            f"{_SYS}/2024-08/nla2022_basins.zip",
            None,
            note="Lake watershed/basin polygons.",
        )],
    }
}

# Default set pulled by pull_nars.py when --indicators is not given: the minimum needed
# to fuse an in-situ HAB signal with CyAN and to build the WQP/NWIS linkage.
DEFAULT_INDICATORS: tuple[str, ...] = (
    "siteinfo",
    "waterchem",
    "algaltoxins",
    "secchi",
    "lakes_shp",
)


# --------------------------------------------------------------------------- #
# Discovery + drift reconciliation
# --------------------------------------------------------------------------- #
_HREF_RE = re.compile(r'href="([^"]+)"', re.IGNORECASE)


def discover(session, page_url: str = NARS_DATA_PAGE) -> set[str]:
    """Fetch the NARS data page and return the set of NLA data-file *basenames* on it.

    Only counts real data payloads (.csv / .zip), not the .txt dictionaries, so the
    drift diff compares like with like. Requires a live session (the only I/O here).
    """
    resp = session.get(page_url, timeout=120)
    resp.raise_for_status()
    names: set[str] = set()
    for href in _HREF_RE.findall(resp.text):
        base = href.rsplit("/", 1)[-1]
        if cycle_of(base) is not None and kind_of(base) in ("data", "spatial"):
            names.add(base)
    return names


@dataclass
class DriftReport:
    cycle: int
    n_matched: int
    new_on_page: list[str] = field(default_factory=list)      # live but not pinned
    missing_from_page: list[str] = field(default_factory=list)  # pinned but not live

    @property
    def is_clean(self) -> bool:
        return not self.new_on_page and not self.missing_from_page


def reconcile(cycle: int, discovered: Iterable[str]) -> DriftReport:
    """Diff a set of discovered filenames for ``cycle`` against the PINNED manifest.

    ``new_on_page``  -> EPA published/renamed a file we haven't pinned (review it).
    ``missing_from_page`` -> a pinned URL is no longer linked (possible re-publish).
    Only NLA files for the given cycle are considered.
    """
    discovered = {d for d in discovered if cycle_of(d) == cycle}
    pinned = {
        ref.data_url.rsplit("/", 1)[-1]
        for refs in PINNED.get(cycle, {}).values()
        for ref in refs
    }
    matched = discovered & pinned
    return DriftReport(
        cycle=cycle,
        n_matched=len(matched),
        new_on_page=sorted(discovered - pinned),
        missing_from_page=sorted(pinned - discovered),
    )
