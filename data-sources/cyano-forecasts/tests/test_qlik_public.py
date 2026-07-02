"""Offline unit tests for the QIX parser + row normalizer — no network, no EPA hit.

Exercises the pure functions against a saved QIX response fixture
(``reference/qix_allweeks.sample.json``) so the reverse-engineered protocol's PARSING can be
regression-tested even when EPA is unreachable or the app changes. Run: ``pytest`` (or directly).
"""
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_MODULE_DIR = _HERE.parent
_ACCESS = _MODULE_DIR / "access"
_DATA_SOURCES = _MODULE_DIR.parent
for _p in (str(_ACCESS), str(_DATA_SOURCES)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import qlik_public as qp          # noqa: E402
import pull_forecasts as pf       # noqa: E402

_FIXTURE = _MODULE_DIR / "reference" / "qix_allweeks.sample.json"


def _load_fixture():
    d = json.loads(_FIXTURE.read_text(encoding="utf-8"))
    return d["fields"], d["qMatrix"]


def test_matrix_to_rows_shapes_cells():
    fields, matrix = _load_fixture()
    rows = qp.matrix_to_rows(fields, matrix)
    assert len(rows) == 3
    assert set(rows[0]) == set(fields)
    # numeric cell keeps qNum; text cell has qNum None (Qlik "NaN")
    assert rows[0]["COMID"].num == 120052700
    assert rows[0]["Lake_name_for_public"].num is None
    assert rows[0]["Lake_name_for_public"].text == "Grand Lake St Marys"


def test_matrix_to_rows_rejects_width_mismatch():
    fields, matrix = _load_fixture()
    bad = [matrix[0][:-1]]           # drop a cell -> width 9 != 10
    try:
        qp.matrix_to_rows(fields, bad)
    except qp.QixError:
        return
    raise AssertionError("expected QixError on width mismatch")


def test_qlik_serial_to_iso():
    # 2025-08-23 is Qlik/Excel serial 45892
    assert pf._iso_from_serial(45892) == "2025-08-23"


def test_normalize_clean_row():
    fields, matrix = _load_fixture()
    rows = qp.matrix_to_rows(fields, matrix)
    rec = pf.normalize_row(rows[0])
    assert rec["comid"] == 120052700
    assert rec["week_end_date"] == "2025-08-23"
    assert rec["year"] == 2025
    assert rec["percent_chance"] == 99.0
    assert rec["state"] == "OH"
    assert rec["flags"] == ""        # Saturday, in-range, year agrees -> clean


def test_normalize_flags_bad_row():
    fields, matrix = _load_fixture()
    rows = qp.matrix_to_rows(fields, matrix)
    rec = pf.normalize_row(rows[2])
    # 08/24/2025 is a Sunday; year 2024 disagrees; pct 150 out of range
    assert "not_saturday" in rec["flags"]
    assert "Year:disagrees_with_weekenddate" in rec["flags"]
    assert "percent_chance:out_of_range" in rec["flags"]
    # value still parsed (flags don't drop data)
    assert rec["comid"] == 999999
    assert rec["week_end_date"] == "2025-08-24"


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"ok {name}")
    print("all tests passed")
