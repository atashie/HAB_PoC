"""HTTP helpers shared across datasets: retrying sessions, Earthdata auth, cached downloads.

Design goals (per project fidelity/reproducibility rules):
- Every download is *cached* — never re-fetched if already present and non-empty.
- Every download is *logged* to a JSONL manifest with sha256, byte size, source URL,
  and access timestamp, so any figure/metric can be traced to the exact bytes used.
- Credentials are read from the environment / a gitignored .env, never committed.
"""
from __future__ import annotations

import hashlib
import json
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# --------------------------------------------------------------------------- #
# Credentials
# --------------------------------------------------------------------------- #
def load_dotenv(dotenv_path: Path) -> None:
    """Minimal .env loader (no dependency on python-dotenv).

    Lines of the form KEY=VALUE are pushed into os.environ if not already set.
    Existing environment variables win (so CI / shell overrides take precedence).
    """
    if not dotenv_path.is_file():
        return
    for raw in dotenv_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        key, val = key.strip(), val.strip().strip('"').strip("'")
        os.environ.setdefault(key, val)


def resolve_appkey(dotenv_path: Optional[Path] = None) -> Optional[str]:
    """Return the OB.DAAC Earthdata AppKey from env or a .env file, or None.

    Precedence: existing OB_DAAC_APPKEY env var, then the .env file.
    Generate a key at https://oceandata.sci.gsfc.nasa.gov/appkey/ (needs a free
    Earthdata Login: https://urs.earthdata.nasa.gov/users/new).
    """
    if dotenv_path is not None:
        load_dotenv(dotenv_path)
    key = os.environ.get("OB_DAAC_APPKEY", "").strip()
    return key or None


def resolve_edl_token(dotenv_path: Optional[Path] = None) -> Optional[str]:
    """Return an Earthdata Login (EDL) JWT bearer token from env or a .env file.

    Used as ``Authorization: Bearer <token>`` for OB.DAAC getfile downloads
    (verified working 2026-07-01). Generate at
    https://urs.earthdata.nasa.gov/ (Generate Token). Preferred over AppKey here.
    """
    if dotenv_path is not None:
        load_dotenv(dotenv_path)
    tok = os.environ.get("OB_DAAC_EDL_TOKEN", "").strip()
    return tok or None


# --------------------------------------------------------------------------- #
# Sessions & requests
# --------------------------------------------------------------------------- #
def make_session(
    total_retries: int = 5,
    backoff_factor: float = 1.5,
    status_forcelist: tuple[int, ...] = (429, 500, 502, 503, 504),
    user_agent: str = "SePRO-HAB-PoC/0.1 (data-sources; contact: repo maintainer)",
) -> requests.Session:
    """A requests.Session with sane retry/backoff for flaky federal endpoints.

    The CyAN file-search endpoint intermittently returns 502 (observed 2026-07-01),
    so retrying transient 5xx is essential. .netrc is honored automatically by
    requests for hosts not otherwise authenticated (Earthdata fallback).
    """
    retry = Retry(
        total=total_retries,
        connect=total_retries,
        read=total_retries,
        status=total_retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
        allowed_methods=frozenset(["GET", "POST", "HEAD"]),
        raise_on_status=False,
        respect_retry_after_header=True,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    session.headers.update({"User-Agent": user_agent})
    return session


# --------------------------------------------------------------------------- #
# Cached, manifested downloads
# --------------------------------------------------------------------------- #
@dataclass
class DownloadResult:
    url: str
    path: Path
    bytes: int
    sha256: str
    cached: bool          # True if it already existed and we skipped the fetch
    accessed_utc: str     # ISO8601 timestamp (UTC) when fetched or verified
    integrity: str = "unverified"
    # integrity values:
    #   'verified'              sha matches the expected (prior-manifest) sha
    #   'refetched_stale_cache' cached bytes were stale/corrupt -> refetched, now matches expected
    #   'mismatch'              freshly-fetched bytes STILL differ from expected (upstream drift/reprocessing)
    #   'unverified'            no expected sha was supplied to check against


def _sha256(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def _utc_now_iso() -> str:
    # UTC timestamp without relying on external tz data.
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def download_file(
    session: requests.Session,
    url: str,
    dest: Path,
    appkey: Optional[str] = None,
    bearer_token: Optional[str] = None,
    expected_sha256: Optional[str] = None,
    timeout: int = 300,
    min_bytes: int = 1,
) -> DownloadResult:
    """Download ``url`` to ``dest`` (cached). Returns a DownloadResult.

    - Cache hit (``dest`` exists and is >= ``min_bytes``): the existing file's sha256
      is computed. If ``expected_sha256`` is provided (e.g. from a prior manifest),
      it is VALIDATED — a match returns cached+integrity='verified'; a MISMATCH means
      the on-disk bytes are stale/corrupt, so the cached file is discarded and the URL
      is re-fetched (integrity='mismatch'). Without an expected sha the cache hit is
      returned as-is but marked integrity='unverified' (so callers/QA can flag it).
    - Auth precedence: ``bearer_token`` (sent as ``Authorization: Bearer``, the
      preferred Earthdata path) → ``appkey`` (appended as a query parameter) →
      requests' ~/.netrc fallback for urs.earthdata.nasa.gov.
    - Streams to a .part temp file, verifies size, then atomically renames.
    """
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)

    integrity = "unverified"
    if dest.is_file() and dest.stat().st_size >= min_bytes:
        have = _sha256(dest)
        if expected_sha256 is None:
            return DownloadResult(url, dest, dest.stat().st_size, have,
                                  cached=True, accessed_utc=_utc_now_iso(),
                                  integrity="unverified")
        if have == expected_sha256:
            return DownloadResult(url, dest, dest.stat().st_size, have,
                                  cached=True, accessed_utc=_utc_now_iso(),
                                  integrity="verified")
        # Bytes differ from the manifest -> do not bless them; refetch.
        integrity = "mismatch"
        dest.unlink()

    fetch_url = url
    headers = {}
    if bearer_token:
        headers["Authorization"] = f"Bearer {bearer_token}"
    elif appkey:
        sep = "&" if "?" in fetch_url else "?"
        fetch_url = f"{fetch_url}{sep}appkey={appkey}"

    tmp = dest.with_suffix(dest.suffix + ".part")
    with session.get(fetch_url, headers=headers, stream=True, timeout=timeout,
                     allow_redirects=True) as r:
        # A landing on the Earthdata login page means auth failed; surface it clearly.
        ctype = r.headers.get("Content-Type", "")
        if r.status_code == 200 and "text/html" in ctype and "earthdata" in r.url.lower():
            raise PermissionError(
                f"Download for {url} redirected to Earthdata Login — authentication "
                f"missing/invalid. Set OB_DAAC_APPKEY (see data-sources/cyan/METADATA.md §7.2)."
            )
        r.raise_for_status()
        written = 0
        with tmp.open("wb") as f:
            for chunk in r.iter_content(chunk_size=1 << 20):
                if chunk:
                    f.write(chunk)
                    written += len(chunk)

    if written < min_bytes:
        tmp.unlink(missing_ok=True)
        raise IOError(f"Downloaded {written} bytes for {url} (< min_bytes={min_bytes}); treating as failure.")

    tmp.replace(dest)
    fetched_sha = _sha256(dest)
    cache_was_stale = (integrity == "mismatch")   # set on the cache-hit path above
    if expected_sha256 is None:
        final_integrity = "unverified"
    elif fetched_sha == expected_sha256:
        # matched expected; note if we got here by healing a stale cache
        final_integrity = "refetched_stale_cache" if cache_was_stale else "verified"
    else:
        # fresh bytes still differ from the manifest -> upstream changed (reprocessing)
        final_integrity = "mismatch"
    return DownloadResult(url, dest, dest.stat().st_size, fetched_sha,
                          cached=False, accessed_utc=_utc_now_iso(),
                          integrity=final_integrity)


def append_manifest(manifest_path: Path, record: dict) -> None:
    """Append one JSON record per line to a download manifest (audit trail)."""
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with manifest_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, sort_keys=True) + "\n")


def read_manifest(manifest_path: Path) -> list[dict]:
    if not Path(manifest_path).is_file():
        return []
    out = []
    for line in Path(manifest_path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            out.append(json.loads(line))
    return out
