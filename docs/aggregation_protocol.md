# Forecast-Kernel Aggregation Protocol (L1 → L4)

## Purpose

Enable CI-passable, cost-efficient forecasts by beginning at high-signal aggregate levels (L1), cascading to atomic granularity (L4) only after structure stabilizes and drift is controlled.

Use the `cascade.py` helper to enforce these checks and launch a child run:

```bash
python -m forecastkernel.scripts.cascade \
  --parent_run path/to/parent_run -- \
  --data path/to/new.csv --horizon 14
```

---

## Aggregation Levels (Examples)

| Level | Example          | Class           | Traits                      |
| ----- | ---------------- | --------------- | --------------------------- |
| L1    | Department-Month | Smooth Seasonal | Low entropy, stable trend   |
| L2    | Category-Week    | Semi-Seasonal   | Promo variance, some signal |
| L3    | SKU-Region-Week  | Intermittent    | Sparse, zero-heavy, spiky   |
| L4    | SKU-Store-Day    | Lumpy/Noisy     | High CV², stochastic demand |

---

## Cascade Criteria

### ✅ Proceed if:

* Upstream level `pass_ci == true` in `baseline_metrics.json`
* Drift monitor is active (`drift_detected == false`)
* Anchor forecast available (`anchor_bias` in `error_breakdown.json`)

### ❌ Reject if:

* CI failed at upstream level
* Drift unresolved
* Atomic forecast has no anchor lineage

---

## Anchor Rule

```python
anchor_bias = atomic_forecast - aggregate_forecast
```

Must be logged for each L3/L4 forecast in `error_breakdown.json`.

---

## Enforcement Tags

Use Git and MLflow metadata:

```json
"metadata": {
  "tag": "level-L2",
  "phase": 2
}
```

---

## CI Logging Fields

* `aggregation_level`
* `anchor_bias`
* `forecastability.classification`
* `drift_detected`

---

## Version

Tag: `aggregation-v1`
