# WQP cross-check — raw-REST vs dataretrieval

- **Scope:** `{'countycode': 'US:39:095'}` · **characteristic:** `Phosphorus`
- dataretrieval is an INDEPENDENT check, not a canonical source (METADATA §7.4).

| Metric | ours (wqp_api) | dataretrieval | verdict |
|---|--:|--:|---|
| legacy sites | 119 | 119 | MATCH |
| legacy results | 7163 | 7163 | MATCH |
| wqx3 results | 7320 | 39 | DIFF (7320 vs 39) |

⚠️ Disagreement — investigate (schema/profile difference or a bug).

_Note: small diffs can be legitimate (dataretrieval may request a different default profile, or counts vs rows differ by dedup); large diffs are a real signal._