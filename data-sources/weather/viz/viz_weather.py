#!/usr/bin/env python
"""Visualize a weather field at NATIVE 0.25° resolution over the Lake Erie scope.

Deliberately native — one rectangle per 0.25° grid cell, no spatial averaging (project
rule: never aggregate without explicit permission; if too heavy, shrink scope not
resolution). Works on either a forecast GRIB2 (ECMWF open data) or an ERA5 GRIB.

Outputs (../outputs/):
  * `<var>_<step_or_time>_map.html`  interactive Folium per-cell map (gitignored — heavy)
  * `<var>_<step_or_time>.png`       small static proof (tracked)

Usage
-----
python viz_weather.py --file ../data/raw/forecast/<run>-oper-fc-0p25.grib2 --var t2m --step 72
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

_DATA_SOURCES = Path(__file__).resolve().parents[2]
if str(_DATA_SOURCES) not in sys.path:
    sys.path.insert(0, str(_DATA_SOURCES))
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except Exception:
        pass

_OUT = _DATA_SOURCES / "weather" / "outputs"
LAKE_ERIE_BBOX = dict(north=42.5, west=-84.5, south=41.0, east=-82.0)


def _open_field(path: Path, var: str, step_h):
    import cfgrib
    import numpy as np
    for ds in cfgrib.open_datasets(str(path)):
        if var not in ds.data_vars:
            continue
        # crop native
        lat, lon = ds["latitude"], ds["longitude"]
        ds = ds.isel(
            latitude=((lat <= LAKE_ERIE_BBOX["north"]) & (lat >= LAKE_ERIE_BBOX["south"])).values.nonzero()[0],
            longitude=((lon <= LAKE_ERIE_BBOX["east"]) & (lon >= LAKE_ERIE_BBOX["west"])).values.nonzero()[0],
        )
        da = ds[var]
        if "step" in da.dims and step_h is not None:
            steps_h = (np.atleast_1d(da["step"].values).astype("timedelta64[h]").astype(int))
            i = int(np.argmin(np.abs(steps_h - step_h)))
            da = da.isel(step=i)
        # squeeze any remaining singleton dims
        for d in list(da.dims):
            if d not in ("latitude", "longitude") and da.sizes[d] == 1:
                da = da.isel({d: 0})
        return da
    raise SystemExit(f"Variable {var!r} not found in {path.name}")


def render(path: Path, var: str, step_h):
    import numpy as np
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    da = _open_field(path, var, step_h)
    lat = da["latitude"].values
    lon = da["longitude"].values
    vals = da.values
    units = da.attrs.get("units", "")
    long_name = da.attrs.get("long_name", var)
    tag = f"step{step_h}" if step_h is not None else "t0"
    _OUT.mkdir(parents=True, exist_ok=True)

    # --- static PNG (tracked proof) ---
    fig, ax = plt.subplots(figsize=(5, 4))
    m = ax.pcolormesh(lon, lat, vals, shading="nearest", cmap="viridis")
    fig.colorbar(m, ax=ax, label=f"{var} [{units}]")
    ax.set_title(f"{long_name}\n{path.stem} — {tag} (native 0.25°, W. Lake Erie)", fontsize=8)
    ax.set_xlabel("lon"); ax.set_ylabel("lat")
    png = _OUT / f"{var}_{tag}.png"
    fig.tight_layout(); fig.savefig(png, dpi=120); plt.close(fig)

    # --- interactive Folium per-cell map (heavy → gitignored) ---
    try:
        import folium
        import branca.colormap as bcm
        finite = vals[np.isfinite(vals)]
        cmap = bcm.linear.viridis.scale(float(finite.min()), float(finite.max()))
        fmap = folium.Map(location=[float(lat.mean()), float(lon.mean())], zoom_start=8,
                          tiles="CartoDB positron")
        d = 0.125  # half a 0.25° cell
        for i, la in enumerate(lat):
            for j, lo in enumerate(lon):
                v = float(vals[i, j])
                if not np.isfinite(v):
                    continue
                folium.Rectangle(
                    bounds=[[la - d, lo - d], [la + d, lo + d]],
                    color=None, weight=0, fill=True, fill_color=cmap(v), fill_opacity=0.6,
                    tooltip=f"{la:.2f},{lo:.2f}: {v:.3g} {units}",
                ).add_to(fmap)
        cmap.caption = f"{long_name} [{units}] — native 0.25°"
        cmap.add_to(fmap)
        html = _OUT / f"{var}_{tag}_map.html"
        fmap.save(str(html))
        print(f"Wrote {png.name} + {html.name} ({finite.size} native cells)")
    except Exception as e:
        print(f"Wrote {png.name}; Folium map skipped ({type(e).__name__}: {e})")


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--file", type=Path, required=True, help="GRIB/GRIB2 file to render")
    p.add_argument("--var", default="t2m", help="variable short name (default t2m)")
    p.add_argument("--step", type=int, default=None, help="forecast step hours (nearest)")
    args = p.parse_args(argv)
    render(args.file, args.var, args.step)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
