# NWIS in-situ series — QA/QC report

*Generated 2026-07-02T15:02:38Z · today=2026-07-02 · 12 series from `C:\Users\arikt\Documents\GitHub\HAB_PoC\data-sources\NWIS\data\raw`*

**0 of 12 series carry QA flags.**


## Site tables

| File | Sites | By type | Missing lat/lon | Missing HUC | Non-USGS agency |
|------|-------|---------|-----------------|-------------|-----------------|
| huc_02070008_sites.csv | 6 | {'ST': 6} | 0 | 0 | 0 |
| sites_01637000_sites.csv | 1 | {'ST': 1} | 0 | 0 | 0 |
| sites_01646500_01638500_sites.csv | 2 | {'ST': 2} | 0 | 0 | 0 |

## By parameter

| Parameter | Name | Series | Rows |
|-----------|------|--------|------|
| 00010 | Water temperature | 4 | 5,551 |
| 00060 | Discharge | 6 | 11,146 |
| 00095 | Specific conductance | 2 | 2,409 |

## Per-series

| Series | Svc | Param | Rows | Dates | Value min/med/max | %prov | Qualifiers | Flags |
|--------|-----|-------|------|-------|-------------------|-------|------------|-------|
| USGS-01636690__00060__00003.csv | dail | 00060 | 1,096 | 2022-01-01→2024-12-31 | 0.07/5.05/311 | 0.0 | ESTIMATED,ICE | ok |
| USGS-01636845__00010__00003.csv | dail | 00010 | 1,186 | 2016-11-30→2020-07-05 | -0.1/13.7/29.1 | 0.0 | ICE | ok |
| USGS-01636845__00060__00003.csv | dail | 00060 | 1,374 | 2016-10-01→2020-07-05 | 0.4/2.83/582 | 0.0 | EQUIP,ESTIMATED,ICE,FLOOD,REVISED | ok |
| USGS-01636845__00095__00003.csv | dail | 00095 | 1,167 | 2016-11-30→2020-07-05 | 174/315/735 | 0.0 | — | ok |
| USGS-01636846__00010__00003.csv | dail | 00010 | 1,268 | 2016-12-28→2020-06-30 | -0.1/13.3/29.8 | 0.0 | ICE | ok |
| USGS-01636846__00060__00003.csv | dail | 00060 | 1,369 | 2016-10-01→2020-06-30 | 0.43/3.32/732 | 0.0 | ESTIMATED | ok |
| USGS-01636846__00095__00003.csv | dail | 00095 | 1,242 | 2016-12-28→2020-06-30 | 113/321/766 | 0.0 | — | ok |
| USGS-01637500__00060__00003.csv | dail | 00060 | 3,653 | 2015-01-01→2024-12-31 | 1/41.5/1.34e+03 | 0.0 | ESTIMATED | ok |
| USGS-01638500__00010__00003.csv | dail | 00010 | 1,329 | 2021-05-08→2024-12-31 | -0/16.3/31.2 | 0.0 | EQUIP | ok |
| USGS-01638500__00060__00003.csv | dail | 00060 | 1,827 | 2020-01-01→2024-12-31 | 915/5.22e+03/9.45e+04 | 0.0 | ESTIMATED | ok |
| USGS-01646500__00010__00003.csv | dail | 00010 | 1,768 | 2020-01-01→2024-12-31 | -0/15.9/32.4 | 0.0 | EQUIP | ok |
| USGS-01646500__00060__00003.csv | dail | 00060 | 1,827 | 2020-01-01→2024-12-31 | 450/6.1e+03/1.02e+05 | 0.0 | ESTIMATED,REVISED | ok |

## Notes

- **Provisional** data are subject to revision; **Approved** data are final (but can still change on reprocessing — track `last_modified`). See METADATA.md §4/§5.
- Plausibility ranges are LOOSE encoding-sanity bounds, not scientific limits.
- `recent_in_pulled_window` = latest obs in the *pulled file* is within 60 d of `today` — it reflects the pulled date window, **not** live catalog activity (for that, read `end` from time-series-metadata).
