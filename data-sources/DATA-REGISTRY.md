# Data Registry — public sources for the SePRO HAB PoC

One row per dataset. Status reflects the **data-sources acquisition layer** (not the literature
review in `../Research/`). "Access date" is when we last verified access details.

| ID | Dataset | Modality | Role | Access method (auth) | Spatial / temporal | Status | Access date | Docs |
|----|---------|----------|------|----------------------|--------------------|--------|-------------|------|
| `cyan` | EPA/NASA **CyAN** CI_cyano | Remote sensing (satellite) | Target / label + lagged feature + water mask | OB.DAAC `cyan_file_search` (no auth) + `getfile` (**Earthdata bearer token**) | ~300 m EPSG:5070, CONUS+AK; weekly (default) & daily; POR 2008–Apr 2012 + 2016-04-24→present | 🟢 **Full weekly CONUS-mosaic POR (6.0) downloaded & verified** → `cyan/data/raw/conus_mosaic_weekly/` (752 files, 4.04 GB, 0 failed). Demo tile `7_2` 2022 + maps built; cost model + policies documented | 2026-07-01 | [`cyan/METADATA.md`](cyan/METADATA.md) |
| `wqp` | **Water Quality Portal** (USGS/EPA/400+ agencies) | In-situ chemistry | Feature + in-situ validation of CI | REST (no auth) / `dataretrieval` | Point stations, national; irregular | ⬜ Planned | — | — |
| `nwis` | USGS **NWIS** | In-situ hydrology (streamflow/gage) | Feature (hydrology) | `dataretrieval` (no auth) | Point gages, national; sub-daily–daily | ⬜ Planned | — | — |
| `nars_nla` | EPA **NARS / National Lakes Assessment** | In-situ lake condition/nutrients | Feature + context | Downloadable tables (no auth) | Probabilistic national survey; multi-year | ⬜ Planned | — | — |
| `noaa_ncei` | **NOAA / NCEI** climate (temp, precip) | Weather/climate | Feature (drivers) | REST / bulk (token for some) | Station + gridded; daily+ | ⬜ Planned | — | — |
| `state_deq` | **State DEQ** bloom advisories/monitoring | In-situ advisories | Label validation (advisories) | Varies by state | State-specific | ⬜ Planned | — | — |

**Legend:** 🟢 live & validated · 🟡 in progress / blocked on a dependency · ⬜ planned.

Sources palette per the brief (`../docs/brief_extracted.txt`) and `../CLAUDE.md`. Each new dataset
follows the same discipline: document (METADATA.md) → scripted pull → QA → viz → registry row.
