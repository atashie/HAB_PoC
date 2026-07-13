"""Central configuration for the lean 2-feature operational HAB forecaster.

One place for every path, constant, and split boundary the pipeline uses. Keeping
them here (rather than scattered through the numbered scripts) is what makes the
workflow auditable: change a boundary or a threshold in exactly one spot.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent

# --- Data locations -------------------------------------------------------
# CyAN weekly CONUS mosaics. Default reuses the repo's already-pulled cache so the
# pipeline runs end-to-end without re-downloading multi-GB rasters. Point this at a
# fresh/empty dir and 01_ingest will point you to the repo's cited CyAN pull to populate it.
CYAN_RAW_DIR = REPO / "data-sources" / "cyan" / "data" / "raw" / "conus_mosaic_weekly"

# Florida resolvable-lakes layer (COMID + AREASQKM + geometry, EPSG:5070). This is
# the lake universe AND the source of the static `area_sqkm` feature.
FL_LAKES_GPKG = REPO / "models" / "data" / "derived" / "fl_resolvable_lakes.gpkg"

DATA = ROOT / "data"          # gitignored intermediate (the lake-week panel)
OUTPUTS = ROOT / "outputs"    # committed, real outputs (models, metrics, predictions)
LAKE_WEEK_PARQUET = DATA / "lake_week.parquet"

# --- CyAN encoding (uint8 "DN") -------------------------------------------
DN_VALID_MAX = 253    # 0..253 are valid measurements (0 = below-detection, still valid/low)
DN_LAND = 254         # masked
DN_NODATA = 255       # cloud / no-data -> masked
AL1_THRESHOLD = 130   # WHO Alert Level 1: per-lake median DN >= 130 (~12 ug/L chl-a); EPA/Schaeffer
# Minimum valid (cloud-free) pixels for a lake-week to be labelled. Default 1 = EPA/Schaeffer
# parity (his na.rm median has no coverage guard), so our label stays comparable to the
# benchmark; we SURFACE the low-coverage fraction rather than silently threshold (matching
# ../models DESIGN sec.4). Raise this for a stricter operational coverage floor.
MIN_VALID_PIXELS = 1

# --- Sensor / period ------------------------------------------------------
# CyAN weekly filenames start with the sensor letter: 'L' = OLCI era (2016->present),
# 'M' = MERIS (2008-2012). We use a SINGLE sensor (OLCI) so there is no cross-sensor
# discontinuity in the target/feature by construction.
OLCI_PREFIX = "L"

# --- Model & temporal split ----------------------------------------------
HORIZONS = [0, 1, 2, 3, 4]                 # forecast lead times, in weeks
FEATURES = ["cyan_median", "area_sqkm"]    # the entire feature set (lean, 2 features)
TARGET = "bloom"
TRAIN_END = "2022-07-01"                   # train:  target week <  TRAIN_END
VAL_END = "2024-07-01"                     # val:    TRAIN_END <= target week < VAL_END
#                                            test:   target week >= VAL_END
SEED = 42

# --- Model architecture: the OPTIMIZED lean model -------------------------
# We ship a HistGradientBoostingClassifier on the two lean features. This is the
# architecture the full study selected: on the identical greedy 2-feature set, the
# gradient-boosted trees materially out-discriminate a logistic GLM on the decision-
# relevant early-warning metric (h=1 onset-AUC 0.916 vs 0.823, onset-MCC 0.314 vs 0.158;
# see ../models/outputs/exp_feature_ablation.md and presentation/story.html). The trees
# capture the non-linear cyan_median x area interaction a linear logit cannot. These
# hyperparameters are copied verbatim from the study harness (../models/model/
# experiment_lib.py::_hgb) so this operational pipeline reproduces the shipped model.
HGB_PARAMS = dict(
    max_iter=400,
    learning_rate=0.06,
    max_leaf_nodes=31,
    l2_regularization=1.0,
    early_stopping=True,       # internal early stop on a seeded 10% holdout of the fit data
    validation_fraction=0.1,
    n_iter_no_change=20,
)
# Where 03_train persists one fitted booster per horizon (a serialized sklearn estimator,
# read back by 04_evaluate). Trees are not human-readable coefficients like the old GLM,
# so we preserve the "why" via permutation importance + a partial-dependence readout in
# models.json rather than by inspecting weights.
MODEL_DIR = OUTPUTS / "models"
