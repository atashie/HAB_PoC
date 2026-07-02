"""Anonymous Qlik Sense QIX-engine client for EPA's PUBLIC forecast dashboards.

⚠️ REVERSE-ENGINEERED / UNOFFICIAL. EPA publishes the experimental cyanoHAB forecast only through
interactive Qlik Sense dashboards (host ``awsedap.epa.gov``, anonymous ``public`` virtual proxy);
there is **no official REST/CSV/file API** (verified: ``/hub``, ``/api``, ``/sense`` all require
forms auth — see ``../METADATA.md`` §7.2 and ``../reference/PRIMARY-SOURCES.md`` §7). This module
speaks the same **QIX JSON-RPC-over-WebSocket** protocol the dashboard's own browser client uses, to
extract the underlying per-lake-week table. It is not an EPA-supported interface and may break when
EPA re-publishes an app; the pinned app IDs + virtual proxy below are the things to update, and the
extraction contract fails LOUDLY (row-count assertions) rather than truncating silently.

The extraction contract (``extract_table``):
  1. establish the anonymous public session (HTTP GET -> ``X-Qlik-Session-public`` cookie),
  2. open the QIX WebSocket (xrfkey in query AND header — Qlik CSRF),
  3. ``OpenDoc`` -> record selection state -> ``ClearAll`` (default selections would silently
     restrict output) -> record selection state again,
  4. create a straight-table hypercube of EXACTLY the requested fields; read ``qSize`` (rows x cols),
  5. page ``GetHyperCubeData`` in <=10,000-cell pages until EXACTLY ``qSize.qcy`` rows are read,
     asserting the count and the column width.

Parsing helpers (``matrix_to_rows``) are pure functions so they can be unit-tested against a saved
QIX response fixture without touching the network (see ``../tests/``).
"""
from __future__ import annotations

import json
import secrets
import ssl
import urllib.request
from dataclasses import dataclass, field
from typing import Any, Optional

import websocket  # websocket-client (pinned in ../requirements.txt)

# --- pinned public dashboard config (verified 2026-07-02; see METADATA §7.3) --------------------- #
HOST = "awsedap.epa.gov"
VIRTUAL_PROXY = "public"                       # inferred from the X-Qlik-Session-public cookie name
USER_AGENT = "SePRO-HAB-PoC/0.1 (research; contact: repo maintainer)"

# The three embedded apps. AllWeeks apps are the canonical pull targets; app1 opens with a default
# single-week selection and must NOT be used for a full extract.
APPS = {
    "allweeks_a": "9727f5d1-11d5-4522-9a59-1835a1885159",   # AllWeeks_CyanForecasts (canonical)
    "allweeks_b": "c00e1007-19bc-48c1-9a93-2c6f54569778",   # AllWeeks_CyanForecasts (+MaxYear)
    "currentweek": "c98935c5-a660-41b9-b1c0-abe31e649bf7",  # Data (default-selected week — cross-check only)
}
CANONICAL_APP = "allweeks_a"

# The 10 fields of AllWeeks_CyanForecasts, in the order we pin for a stable CSV/sha256.
ALLWEEKS_FIELDS = [
    "COMID", "Lake_name_for_public", "State", "EPA_region",
    "WeekEndDate", "Year", "Percent_chance_of_cyanoHAB",
    "Lat_centroid", "Lon_centroid", "Date",
]

_QIX_CELL_PAGE_LIMIT = 10_000   # Qlik caps GetHyperCubeData at ~10k cells per call


class QixError(RuntimeError):
    """Any failure of the (unofficial) QIX extraction contract — including short/over-long pages."""


@dataclass
class Cell:
    """One QIX hypercube cell: keep BOTH the display text and the numeric value (Qlik duals)."""
    text: str
    num: Optional[float]
    is_null: bool

    @classmethod
    def from_qix(cls, c: dict) -> "Cell":
        num = c.get("qNum")
        # Qlik uses the sentinel "NaN" (a large negative magic number) for non-numeric cells.
        if isinstance(num, str) or num is None:
            num = None
        return cls(text=c.get("qText", ""), num=num, is_null=bool(c.get("qIsNull", False)))


@dataclass
class ExtractMeta:
    """Provenance of one extraction — folded into the acquisition manifest (METADATA §10)."""
    appid: str
    engine_url: str
    single_url: str
    virtual_proxy: str
    xrfkey_present: bool
    field_order: list
    hypercube_def: dict
    q_size: dict                       # {"qcx": cols, "qcy": rows}
    page_rows: int
    n_pages: int
    row_count: int
    selection_before: list = field(default_factory=list)
    selection_after: list = field(default_factory=list)


def matrix_to_rows(fields: list, matrix: list) -> list:
    """Pure: convert a QIX qMatrix (list of rows of qCells) into a list of ``dict[field] -> Cell``.

    Raises ``QixError`` on a width mismatch so a schema change cannot be silently mis-aligned.
    """
    rows = []
    for r in matrix:
        if len(r) != len(fields):
            raise QixError(f"row width {len(r)} != expected {len(fields)} (schema drift?)")
        rows.append({f: Cell.from_qix(c) for f, c in zip(fields, r)})
    return rows


class QlikPublicClient:
    """Minimal anonymous QIX client. Use as a context manager."""

    def __init__(self, appid: str, host: str = HOST, virtual_proxy: str = VIRTUAL_PROXY,
                 user_agent: str = USER_AGENT, timeout: int = 60, verify_tls: bool = True):
        self.appid = appid
        self.host = host
        self.vp = virtual_proxy
        self.user_agent = user_agent
        self.timeout = timeout
        self.verify_tls = verify_tls
        self.xrfkey = secrets.token_hex(8)      # 16 hex chars; value is arbitrary, must match query+header
        self.single_url = f"https://{host}/{virtual_proxy}/single/?appid={appid}"
        self.engine_url = f"wss://{host}/{virtual_proxy}/app/{appid}?Xrfkey={self.xrfkey}"
        self._ws: Optional[websocket.WebSocket] = None
        self._id = 0
        self._doc_handle: Optional[int] = None

    # -- lifecycle -------------------------------------------------------------------------------- #
    def __enter__(self) -> "QlikPublicClient":
        self.connect()
        return self

    def __exit__(self, *exc) -> None:
        self.close()

    def _session_cookie(self) -> str:
        req = urllib.request.Request(self.single_url, headers={"User-Agent": self.user_agent})
        ctx = ssl.create_default_context() if self.verify_tls else ssl._create_unverified_context()
        with urllib.request.urlopen(req, timeout=self.timeout, context=ctx) as resp:
            for c in (resp.headers.get_all("Set-Cookie") or []):
                if c.startswith("X-Qlik-Session"):
                    return c.split(";")[0]
        raise QixError("no X-Qlik-Session cookie from the public single URL — anonymous access changed?")

    def connect(self) -> None:
        cookie = self._session_cookie()
        sslopt = None if self.verify_tls else {"cert_reqs": ssl.CERT_NONE}
        self._ws = websocket.create_connection(
            self.engine_url, header=[f"X-Qlik-Xrfkey: {self.xrfkey}"], cookie=cookie,
            origin=f"https://{self.host}", sslopt=sslopt, timeout=self.timeout)
        self._ws.settimeout(self.timeout)

    def close(self) -> None:
        if self._ws is not None:
            try:
                self._ws.close()
            finally:
                self._ws = None

    # -- JSON-RPC --------------------------------------------------------------------------------- #
    def _rpc(self, method: str, params: Any, handle: int = -1) -> dict:
        self._id += 1
        self._ws.send(json.dumps({"jsonrpc": "2.0", "id": self._id,
                                  "handle": handle, "method": method, "params": params}))
        for _ in range(30):                 # skip async change/notification frames
            msg = json.loads(self._ws.recv())
            if msg.get("id") == self._id:
                if "error" in msg:
                    raise QixError(f"{method} -> {msg['error']}")
                return msg
        raise QixError(f"no response to {method} after draining async frames")

    def open_doc(self) -> int:
        r = self._rpc("OpenDoc", [self.appid, "", "", "", False])
        self._doc_handle = r["result"]["qReturn"]["qHandle"]
        return self._doc_handle

    def get_selections(self) -> list:
        """Current selection state (empty list == no selections)."""
        obj = {"qInfo": {"qType": "sel"}, "qSelectionObjectDef": {}}
        h = self._rpc("CreateSessionObject", [obj], handle=self._doc_handle)["result"]["qReturn"]["qHandle"]
        lay = self._rpc("GetLayout", [], handle=h)["result"]["qLayout"]
        return lay.get("qSelectionObject", {}).get("qSelections", [])

    def clear_all(self) -> None:
        self._rpc("ClearAll", [True], handle=self._doc_handle)

    def data_model(self) -> list:
        """GetTablesAndKeys -> the app's tables + fields (for schema inspection / QA)."""
        r = self._rpc("GetTablesAndKeys",
                      [{"qcx": 1000, "qcy": 1000}, {"qcx": 0, "qcy": 0}, 30, True, False],
                      handle=self._doc_handle)
        return r["result"]["qtr"]

    # -- the extraction contract ------------------------------------------------------------------ #
    def extract_table(self, fields: list, clear_first: bool = True):
        """Extract EXACTLY ``fields`` as a full straight-table hypercube. Returns (rows, ExtractMeta).

        Fails closed: asserts column width and that the number of rows read equals ``qSize.qcy``.
        """
        if self._doc_handle is None:
            self.open_doc()
        sel_before = self.get_selections()
        if clear_first:
            self.clear_all()                # drop any default selection state (app1 defaults to 1 week)
        sel_after = self.get_selections()

        hc_def = {
            "qInfo": {"qType": "haf-extract"},
            "qHyperCubeDef": {
                "qDimensions": [{"qDef": {"qFieldDefs": [f]}} for f in fields],
                "qMeasures": [],
                "qMode": "S",               # straight table
                "qInitialDataFetch": [{"qTop": 0, "qLeft": 0, "qHeight": 1, "qWidth": len(fields)}],
            },
        }
        h = self._rpc("CreateSessionObject", [hc_def], handle=self._doc_handle)["result"]["qReturn"]["qHandle"]
        hc = self._rpc("GetLayout", [], handle=h)["result"]["qLayout"]["qHyperCube"]
        qsize = hc["qSize"]
        cols, total = qsize["qcx"], qsize["qcy"]
        if cols != len(fields):
            raise QixError(f"hypercube width {cols} != requested fields {len(fields)} (schema drift?)")

        page_rows = max(1, _QIX_CELL_PAGE_LIMIT // cols)
        rows: list = []
        n_pages = 0
        top = 0
        while top < total:
            height = min(page_rows, total - top)
            pg = self._rpc("GetHyperCubeData",
                           ["/qHyperCubeDef", [{"qTop": top, "qLeft": 0, "qHeight": height, "qWidth": cols}]],
                           handle=h)
            matrix = pg["result"]["qDataPages"][0]["qMatrix"]
            n_pages += 1
            if not matrix:
                raise QixError(f"empty page at top={top} of {total} (expected {height} rows)")
            rows.extend(matrix_to_rows(fields, matrix))
            top += len(matrix)

        if len(rows) != total:
            raise QixError(f"extraction incomplete: read {len(rows)} rows != qSize.qcy {total}")

        meta = ExtractMeta(
            appid=self.appid, engine_url=self.engine_url, single_url=self.single_url,
            virtual_proxy=self.vp, xrfkey_present=True, field_order=list(fields),
            hypercube_def={"qDimensions": [f for f in fields], "qMode": "S"},
            q_size=dict(qsize), page_rows=page_rows, n_pages=n_pages, row_count=len(rows),
            selection_before=sel_before, selection_after=sel_after,
        )
        return rows, meta
