# Operational forecast - issued from CyAN week 2026-06-21

- Model: lean logistic regression on `cyan_median + area_sqkm`, one per horizon, refit on all labelled history.
- Target weeks: {'h0': '2026-06-28', 'h1': '2026-07-05', 'h2': '2026-07-12', 'h3': '2026-07-19', 'h4': '2026-07-26'}
- Lakes forecast: 133   |   currently blooming: 47
- h1 alert threshold (val-tuned): 55%

## Top-10 new-bloom risk (currently clear, ranked by 1-week risk)

| lake | comid | CyAN now | 1-wk risk | 2-wk | 3-wk | 4-wk |
|--|--:|--:|--:|--:|--:|--:|
| Buffum, Lake | 16799991 | 127 | 55% | 55% | 54% | 54% |
| Haines, Lake | 16793645 | 126 | 54% | 54% | 54% | 53% |
| Eloise, Lake | 16798691 | 125 | 53% | 53% | 52% | 52% |
| (unnamed) | 10996929 | 112 | 39% | 40% | 41% | 41% |
| (unnamed) | 21475236 | 111 | 37% | 39% | 40% | 40% |
| Arbuckle, Lake | 21480390 | 105 | 31% | 34% | 35% | 35% |
| Lake Winder | 10998263 | 100 | 27% | 30% | 31% | 32% |
| Livingston, Lake | 21480452 | 98 | 25% | 27% | 29% | 30% |
| (unnamed) | 16631376 | 97 | 24% | 27% | 28% | 29% |
| (unnamed) | 166757656 | 95 | 13% | 15% | 16% | 17% |

Risks are probabilities of a WHO-AL1 bloom, not chlorophyll values; tiers near the threshold are not sharply separable. Risk is nearly flat across h0-h4 by design - all horizons are scored from the same freshest antecedent CyAN, so a 2-feature snapshot barely separates 1-week from 4-week lead. Correlation, not causation.