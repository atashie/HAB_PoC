"""Phase-0 golden regression gate for the features.py refactor.

The refactor split the old single-pass `add_spei` into `fit_spei_climatology` (frozen per-month
Pearson III moments) + `apply_spei` (standardize only), wrapped by `fit_climatology` /
`apply_features`. Because fit-then-apply is the SAME arithmetic reorganized, the new path must be
BIT-IDENTICAL to the pre-refactor output.

`fixtures/features_golden.npz` was captured from the pre-refactor code (commit dcc10e4) on the
deterministic synthetic data in `_synth.py`. These tests assert the new path reproduces it exactly,
and that the frozen-climatology API cannot leak (no re-fit on serve data; lossless serialization).

Run: python -m pytest data-sources/weather/tests/test_features_regression.py -q
"""
import sys
from pathlib import Path

import numpy as np
import pytest

_DATA_SOURCES = Path(__file__).resolve().parents[2]
if str(_DATA_SOURCES) not in sys.path:
    sys.path.insert(0, str(_DATA_SOURCES))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from weather.derive import features as F      # noqa: E402
from _synth import make_synthetic_daily       # noqa: E402

_GOLDEN = Path(__file__).resolve().parent / "fixtures" / "features_golden.npz"


def _new_feats():
    ds = make_synthetic_daily()
    clim = F.fit_climatology(ds, F.DEFAULT_GDD_BASE_C)
    feats = F.apply_features(ds, clim, F.DEFAULT_GDD_BASE_C)
    return ds, clim, feats


def test_golden_fixture_present():
    assert _GOLDEN.exists(), "run scratchpad/capture_golden.py against the pre-refactor code first"


def test_refactor_is_bit_identical_to_pre_refactor_golden():
    golden = np.load(_GOLDEN)
    _, _, feats = _new_feats()
    feat_vars = sorted(feats.data_vars)
    golden_vars = sorted(k for k in golden.files if not k.startswith("__"))
    assert feat_vars == golden_vars, (set(feat_vars) ^ set(golden_vars))

    for name in feat_vars:
        got = feats[name].transpose("date", "latitude", "longitude").values.astype("float64")
        # assert_array_equal treats NaN-in-same-position as equal and is otherwise bit-exact.
        np.testing.assert_array_equal(got, golden[name], err_msg=f"{name} drifted from golden")


def test_calibration_years_unchanged():
    golden = np.load(_GOLDEN)
    _, clim, _ = _new_feats()
    assert int(clim.attrs["cal0"]) == int(golden["__cal0__"][0])
    assert int(clim.attrs["cal1"]) == int(golden["__cal1__"][0])


def test_apply_features_refuses_to_fit_without_climatology():
    ds = make_synthetic_daily()
    with pytest.raises(ValueError, match="never fits|requires a fitted climatology"):
        F.apply_features(ds, None)


def test_apply_spei_refuses_to_fit_without_climatology():
    ds = make_synthetic_daily()
    pet = F.hargreaves_pet(ds)
    with pytest.raises(ValueError, match="no re-fit|requires a fitted climatology"):
        F.apply_spei(ds, pet, None)


def test_frozen_climatology_does_not_refit_on_serve_data():
    """Perturbing only the LAST day must change SPEI only on that day. If apply_features secretly
    re-fit the climatology on the served series, the shifted moments would change many earlier days'
    SPEI too. So: fit once (clean), apply to clean and to tail-perturbed series with the SAME clim."""
    ds = make_synthetic_daily()
    clim = F.fit_climatology(ds)                       # frozen on clean data
    base = F.apply_features(ds, clim)

    ds2 = ds.copy(deep=True)
    tp = ds2["tp_sum_mm"].values
    tp[-1, :, :] = tp[-1, :, :] + 1.0e5               # absurd rainfall spike on the final day only
    ds2["tp_sum_mm"].values[...] = tp
    pert = F.apply_features(ds2, clim)                 # SAME frozen climatology

    for scale in F.SPEI_SCALES:
        v = f"spei_{scale}"
        a = base[v].transpose("date", "latitude", "longitude").values
        b = pert[v].transpose("date", "latitude", "longitude").values
        # every day except the last must be untouched (proves no re-fit on the perturbed series)
        np.testing.assert_array_equal(a[:-1], b[:-1], err_msg=f"{v} changed before the perturbed day")
        # and the last day's water balance genuinely moved, so its SPEI must differ
        assert not np.array_equal(a[-1], b[-1]), f"{v} last day should reflect the perturbation"


def test_climatology_netcdf_roundtrip_is_lossless(tmp_path):
    """The forecast pipeline serves via a persisted climatology file — that round-trip must not
    change any served feature value."""
    ds, clim, feats_mem = _new_feats()
    path = F.write_climatology(clim, tmp_path / "clim.nc")
    clim2 = F.open_climatology(path)
    assert clim2.attrs["climatology_sha256"] == clim.attrs["climatology_sha256"]
    feats_disk = F.apply_features(ds, clim2, F.DEFAULT_GDD_BASE_C)
    for name in feats_mem.data_vars:
        a = feats_mem[name].transpose("date", "latitude", "longitude").values
        b = feats_disk[name].transpose("date", "latitude", "longitude").values
        np.testing.assert_array_equal(a, b, err_msg=f"{name} changed across climatology round-trip")
