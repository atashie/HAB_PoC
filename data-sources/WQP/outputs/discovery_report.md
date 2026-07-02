# WQP discovery — US39095

- **Scope:** `{'countycode': 'US:39:095'}`
- **Legacy Summary (periodOfRecord), summaryYears=5** — source-provided per site×year×characteristic inventory (NOT our aggregation).
- **Cached source of truth:** `WQP\data\raw\summary_legacy_1959a01f510f.csv` (sha256 `ee0caf0f88e5…`, 585,866 bytes, accessed 2026-07-02T02:18:46Z).
- **Inventory:** 45 monitoring locations · 427 distinct characteristics · 1,903 summary rows.

> ⚠ Legacy Summary omits USGS data added/modified after 2024-03-11. See the freshness probe below for what WQX3 adds.

## HAB-relevant availability (counts, not values)

| Characteristic | Sites | Results | Latest yr | Last submitted | Providers |
|---|--:|--:|--:|---|---|
| Temperature, water | 33 | 543 | 2024 | 2025-08-29 | NWIS,STORET |
| Dissolved oxygen (DO) | 29 | 442 | 2024 | 2025-08-29 | STORET |
| Orthophosphate | 12 | 237 | 2024 | 2025-08-28 | NWIS,STORET |
| Ammonia | 11 | 135 | 2024 | 2025-08-28 | STORET |
| Nitrate + Nitrite | 11 | 135 | 2024 | 2025-08-28 | STORET |
| Total Kjeldahl nitrogen (Organic N & NH3) | 11 | 135 | 2024 | 2025-08-28 | STORET |
| Total Phosphorus, mixed forms | 11 | 135 | 2024 | 2025-08-28 | STORET |
| Turbidity | 10 | 190 | 2024 | 2025-08-28 | NWIS,STORET |
| Nitrite | 8 | 232 | 2024 | 2025-08-28 | NWIS,STORET |
| Dissolved oxygen saturation | 8 | 25 | 2024 | 2025-08-29 | STORET |
| Chlorophyll a, corrected for pheophytin | 6 | 119 | 2024 | 2025-08-28 | STORET |
| Temperature, air | 3 | 49 | 2024 | 2023-12-18 | NWIS,STORET |
| Chemical oxygen demand | 3 | 12 | 2024 | 2025-08-28 | STORET |
| Carbonaceous biochemical oxygen demand, standard conditions | 3 | 3 | 2024 | 2025-08-28 | STORET |
| Oxygen | 2 | 131 | 2024 | — | NWIS |
| pH | 2 | 104 | 2024 | — | NWIS |
| Depth, Secchi disk depth | 2 | 5 | 2023 | 2023-12-18 | STORET |
| Nitrogen, mixed forms (NH3), (NH4), organic, (NO2) and (NO3) | 1 | 110 | 2023 | — | NWIS |
| Ammonia and ammonium | 1 | 102 | 2023 | — | NWIS |
| Nitrate | 1 | 102 | 2023 | — | NWIS |
| Phosphorus | 1 | 80 | 2023 | — | NWIS |
| Organic Nitrogen | 1 | 78 | 2023 | — | NWIS |
| Kjeldahl nitrogen | 1 | 57 | 2023 | — | NWIS |
| Inorganic nitrogen (nitrate and nitrite) | 1 | 51 | 2023 | — | NWIS |
| Nitrogen | 1 | 35 | 2023 | — | NWIS |

## Provider inventory (distinct sites)

- **STORET**: 43
- **NWIS**: 2

## Site-type inventory (distinct sites)

- Stream: 30
- Lake, Reservoir, Impoundment: 10
- Facility: 3
- Ocean: 2

## Post-2024-03-11 USGS freshness (legacy vs WQX3)

Bounded probe: USGS (`providers=NWIS`) Results (any characteristic) with `startDateLo=2024-03-12`, this scope.

- **legacy WQX 2.2:** 0 results (via header)
- **WQX 3.0 beta:** 7528 results (via rowcount)

If WQX3 > legacy, that gap is recent USGS data reachable **only** via WQX3 — the operational reason to prefer WQX3 for USGS (METADATA §2, §10).

---
*Regenerate: `python data-sources/WQP/access/discover_wqp.py --countycode US:39:095`*
