## ❌ Why Naive Averaging Models Are Excluded from Forecast-Kernel Baselines

### 1. Structural Misfit for Intermittent Demand

Averaging models (e.g., `SimpleAverage`, `RollingMean`, `ExponentialMovingAverage`) fail in zero-heavy or sparse demand contexts. For intermittent demand types (ADI ≥ 1.32), these models blur out signal and amplify lag-induced error, leading to structural mismatches.

> Recommended: Use `CrostonSBA` or `CrostonOptimized` based on CV². These preserve intermittency structure and outperform naive averages in error metrics.

---

### 2. Fails CI Gate: Score Threshold

Forecast-Kernel's Phase 1 CI rule:

> **"Model must beat `min(ensemble_naive, holt_winters)` on Score (MAE + |Bias|)"**

Averaging models usually underperform these thresholds due to:

* Smoothing that lags real trend/seasonality
* Instability in zero-heavy series
* Lack of any uplift vs. ensemble baselines

---

### 3. Low CI Value and No Drift Utility

Averaging models contribute zero leverage in downstream phases:

* **No drift monitoring capability**
* **No forecastability classification**
* **No continuity into feature-aware phases (Phase 7+)**

They violate the Codex principle of compound uplift and CI-tracked lineage.

---

### ✅ When Averaging Is Acceptable (Edge Cases Only)

| Condition                         | Use Model         | Justified | Use Case Description                         |
| --------------------------------- | ----------------- | --------- | -------------------------------------------- |
| Spectral Entropy > 0.6            | `HistoricAverage` | ✅         | Random/noisy series as sanity-check fallback |
| CV² < 0.1 and ADI < 1.1           | `RollingMean`     | ✅         | Dense, stable SKUs without drift tracking    |
| Feature or model failure fallback | `RollingMean`     | ✅         | Only under ops failure, must log `ci_bypass` |

---

### ❌ Never Use Averaging Models When:

* Series is intermittent or lumpy
* CI Score threshold is enforced
* Confidence intervals or drift triggers are in play
* You need to scale to Phase 7+ with feature-aware models

---

### 🧠 Conclusion

Averaging models are **non-informative**, **non-scalable**, and **CI-incompatible** under Kernel logic. They serve only as fallback under documented exception cases — never as primary baseline.

Use them with caution and always with lineage logging and CI flagging in place.
