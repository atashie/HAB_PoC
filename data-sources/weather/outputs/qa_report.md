# Weather layer — QA report

Region sanity stats are a **labeled diagnostic over the western Lake Erie crop at native 0.25° resolution** — not a model input and not a spatial aggregation of the stored grids (GRIB stays native).

## `weather\data\raw\forecast\20260702060000-oper-fc-0p25.grib2`
- flags: none
- integrity: verified (13,799,517 bytes)
- grid: 721×1440 @ dlat=0.25 dlon=0.25° (-180..180); lat -90.0..90.0, lon -180.0..179.75
- steps (h): [0, 24, 48, 72]
- expver: (none — forecast or single-provenance netCDF)

| variable | long name | units | stepType | accum? | region min | max | mean | cells |
|---|---|---|---|---|---|---|---|---|
| `u10` | 10 metre U wind component | m s**-1 | instant | no | -3.06 | 7.32 | 2.27 | 77 |
| `v10` | 10 metre V wind component | m s**-1 | instant | no | -3.12 | 4.49 | 0.978 | 77 |
| `t2m` | 2 metre temperature | K | instant | no | 292 | 303 | 298 | 77 |
| `msl` | Mean sea level pressure | Pa | instant | no | 1.01e+05 | 1.02e+05 | 1.02e+05 | 77 |
| `tp` | Total precipitation | m | accum | yes | 0 | 0.0222 | 0.00484 | 77 |

## `weather\data\raw\era5\era5_sl_202208-202208.grib`
- flags: none
- integrity: verified (1,834 bytes)
- grid: 7×11 @ dlat=0.25 dlon=0.25° (-180..180); lat 41.0..42.5, lon -84.5..-82.0
- steps (h): [0, 6]
- expver: (none — forecast or single-provenance netCDF)

| variable | long name | units | stepType | accum? | region min | max | mean | cells |
|---|---|---|---|---|---|---|---|---|
| `msl` | Mean sea level pressure | Pa | instant | no | 1.01e+05 | 1.01e+05 | 1.01e+05 | 77 |
| `u10` | 10 metre U wind component | m s**-1 | instant | no | 0.504 | 4.78 | 2.32 | 77 |
| `v10` | 10 metre V wind component | m s**-1 | instant | no | 3.21 | 6.98 | 4.63 | 77 |
| `t2m` | 2 metre temperature | K | instant | no | 293 | 296 | 295 | 77 |
| `d2m` | 2 metre dewpoint temperature | K | instant | no | 291 | 293 | 292 | 77 |
| `ssrd` | Surface short-wave (solar) radiation downwards | J m**-2 | accum | yes | 1.55e+05 | 4.19e+05 | 2.72e+05 | 77 |
| `tp` | Total precipitation | m | accum | yes | 0 | 8.25e-05 | 1.1e-05 | 77 |
