"""Tests for nars_catalog: filename parsing, pinned-manifest integrity, drift reconcile.

These cover the only real *logic* in the acquisition layer. Downloading, QA, and viz
are verified by running them against the real (small, public) NLA files.

Run:  cd data-sources/EPA-NARS && python -m pytest tests/ -q
"""
from __future__ import annotations

import sys
from pathlib import Path

# make the access/ modules importable when running from EPA-NARS/
_PKG = Path(__file__).resolve().parents[1]
for p in (_PKG / "access",):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import nars_catalog as cat  # noqa: E402


# --------------------------------------------------------------------------- #
# cycle_of — map a NARS/NLA filename to its survey cycle year
# --------------------------------------------------------------------------- #
def test_cycle_of_2022_variants():
    assert cat.cycle_of("nla22_siteinfo.csv") == 2022
    assert cat.cycle_of("nla2022_phab_wide.csv") == 2022
    assert cat.cycle_of("nla_2022_something.csv") == 2022
    # combined multi-cycle population-estimate file is anchored to the newest cycle
    assert cat.cycle_of("nla2007-2022_data_forpopestimates_indexvisits_probsites_0.csv") == 2022


def test_cycle_of_older_cycles():
    assert cat.cycle_of("nla_2017_site_information-data.csv") == 2017
    assert cat.cycle_of("nla2012_wide_siteinfo_08232016.csv") == 2012
    assert cat.cycle_of("nla2007_profile.csv") == 2007


def test_cycle_of_non_nla_returns_none():
    # Other NARS surveys must not be misread as NLA cycles.
    assert cat.cycle_of("nrsa1819_siteinfo.csv") is None
    assert cat.cycle_of("nwca21_siteinfo-data.csv") is None
    assert cat.cycle_of("wsa_siteinfo_ts_final.csv") is None


# --------------------------------------------------------------------------- #
# indicator_of — canonicalize the indicator/theme from a filename
# --------------------------------------------------------------------------- #
def test_indicator_of_core_hab_indicators():
    assert cat.indicator_of("nla22_siteinfo.csv") == "siteinfo"
    assert cat.indicator_of("nla_2017_site_information-data.csv") == "siteinfo"
    assert cat.indicator_of("nla2012_wide_siteinfo_08232016.csv") == "siteinfo"
    assert cat.indicator_of("nla22_waterchem_wide.csv") == "waterchem"
    assert cat.indicator_of("nla22_algaltoxins.csv") == "algaltoxins"
    assert cat.indicator_of("nla22_secchi.csv") == "secchi"
    assert cat.indicator_of("nla2022_profile_wide.csv") == "profile"


def test_indicator_of_spatial_and_other():
    assert cat.indicator_of("nla2022_lakes.zip") == "lakes_shp"
    assert cat.indicator_of("nla2022_basins.zip") == "basins_shp"
    assert cat.indicator_of("nla2022_phytoplanktoncount_wide.csv") == "phytoplankton"
    assert cat.indicator_of("nla2007-2022_data_forpopestimates_indexvisits_probsites_0.csv") == "popest"


def test_indicator_of_unknown_returns_none():
    assert cat.indicator_of("nla22_mystery_indicator.csv") is None


# --------------------------------------------------------------------------- #
# kind_of — data (csv) vs metadata dictionary (txt) vs spatial (zip)
# --------------------------------------------------------------------------- #
def test_kind_of():
    assert cat.kind_of("nla22_siteinfo.csv") == "data"
    assert cat.kind_of("nla22_siteinfo.txt") == "meta"
    assert cat.kind_of("nla2022_lakes.zip") == "spatial"


# --------------------------------------------------------------------------- #
# PINNED manifest integrity — the reproducible, verified 2022 file set
# --------------------------------------------------------------------------- #
def test_pinned_has_2022_and_core_indicators():
    assert 2022 in cat.PINNED
    files = cat.PINNED[2022]
    for ind in ("siteinfo", "waterchem", "algaltoxins"):
        assert ind in files, f"pinned 2022 missing core indicator {ind}"


def test_pinned_urls_are_public_epa_https():
    for cycle, files in cat.PINNED.items():
        for ind, refs in files.items():
            for ref in refs:
                assert ref.data_url.startswith("https://www.epa.gov/"), (cycle, ind, ref.data_url)
                if ref.meta_url is not None:
                    assert ref.meta_url.startswith("https://www.epa.gov/"), (cycle, ind, ref.meta_url)


def test_pinned_filenames_roundtrip_through_parsers():
    # Every pinned data file must parse back to the cycle+indicator it is filed under.
    for cycle, files in cat.PINNED.items():
        for ind, refs in files.items():
            for ref in refs:
                name = ref.data_url.rsplit("/", 1)[-1]
                assert cat.cycle_of(name) == cycle, (name, cat.cycle_of(name), cycle)
                assert cat.indicator_of(name) == ind, (name, cat.indicator_of(name), ind)


def test_pinned_data_filenames_unique():
    # No file should be pinned under two indicators.
    names = [
        ref.data_url.rsplit("/", 1)[-1]
        for refs in cat.PINNED[2022].values()
        for ref in refs
    ]
    assert len(names) == len(set(names)), "duplicate pinned data file"


def test_default_indicels_subset_of_pinned_2022():
    assert set(cat.DEFAULT_INDICATORS).issubset(set(cat.PINNED[2022])), (
        "default pull set references an indicator not in the pinned 2022 manifest"
    )


# --------------------------------------------------------------------------- #
# reconcile — drift detection between pinned manifest and what's live on the page
# --------------------------------------------------------------------------- #
def test_reconcile_flags_new_and_missing():
    pinned_names = {
        ref.data_url.rsplit("/", 1)[-1]
        for refs in cat.PINNED[2022].values()
        for ref in refs
    }
    # Simulate the live page: same set, minus one pinned file, plus a brand-new one.
    a_pinned = sorted(pinned_names)[0]
    discovered = (pinned_names - {a_pinned}) | {"nla22_newthing_wide.csv"}

    rep = cat.reconcile(2022, discovered)
    assert "nla22_newthing_wide.csv" in rep.new_on_page
    assert a_pinned in rep.missing_from_page
    # Files present in both should be counted as matched.
    assert rep.n_matched == len(pinned_names) - 1
