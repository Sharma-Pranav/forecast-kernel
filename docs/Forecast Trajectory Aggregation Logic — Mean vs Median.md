# Forecast Trajectory Aggregation Logic — Mean vs Median

## Purpose

To define the logic and criteria for selecting between mean and median trajectory forecasts for any model producing probabilistic or simulation-based forecast outputs, ensuring strict compliance with Forecast-Kernel CI, auditability, and best-practice forecasting principles.

---

## 1. Context: Trajectory Forecasts

Many advanced models (e.g., quantile regressors, Bayesian, simulation-based) output a *distribution* of possible future values for each time step, not just a single-point estimate. These can be summarized into a trajectory using:

* **Mean Trajectory:** At each horizon, forecast is the arithmetic mean across all sampled scenarios.
* **Median Trajectory:** At each horizon, forecast is the median (50th percentile) across all sampled scenarios.

---

## 2. Selection Logic

### Step 1: Metric Computation

* For both mean and median trajectories, compute core forecast metrics over the forecast horizon:

  * **MAE** (Mean Absolute Error)
  * **Bias** (Mean Error)
  * **Score** (Composite: MAE + |Bias|)

### Step 2: Baseline Comparison (Forecast-Kernel CI Gate)

* **Rule:** A candidate trajectory is eligible for promotion only if:

  * `Score ≤ min(ensemble_naive.Score, holt_winters.Score)`
  * All core metrics are logged with full lineage
* If neither mean nor median trajectory passes the CI threshold, fallback or model revision is required.

### Step 3: Model Promotion

* Select the trajectory (mean or median) with the **lowest Score** *among those that pass the CI gate*.
* Always document which trajectory was selected and why (including Score and CI gate outcome).

---

## 3. Model/Distribution Considerations

| Distribution at Each Horizon | Recommended Trajectory | Rationale                                         |
| ---------------------------- | ---------------------- | ------------------------------------------------- |
| Symmetric/Normal             | Mean or Median         | Similar results; mean conventional                |
| Skewed/Fat-Tailed            | Median                 | Robust to outliers, minimizes error spikes        |
| Highly Volatile/Regime Shift | Median                 | Less sensitive to simulation or outlier artifacts |

---

## 4. CI-Compliant Logging Example

```json
"metrics": {
  "mean_trajectory":   { "MAE": 12.1, "Bias": -1.1, "Score": 13.2 },
  "median_trajectory": { "MAE": 11.8, "Bias": -0.7, "Score": 12.5 },
  "ensemble_naive":    { "Score": 15.0 },
  "holt_winters":      { "Score": 13.0 }
},
"selected_model": "median_trajectory",
"pass_ci": true
```

---

## 5. Operational Guidance

* **Never** use mean/median of *historical actuals* as forecast except for high-entropy fallback (with flag).
* If both trajectories fail CI, model is not promotable—must retrain or fallback.
* For regulatory/audit environments, always prefer the trajectory with lowest Score and highest robustness.

---

## 6. Summary Table

| Step              | Action                                                                |
| ----------------- | --------------------------------------------------------------------- |
| 1. Metric Logging | Compute MAE, Bias, Score for both mean and median trajectories        |
| 2. CI Check       | Discard trajectories failing the Score ≤ min(ensemble, holt\_winters) |
| 3. Selection      | Promote trajectory with lowest passing Score                          |
| 4. Documentation  | Log full metrics, selection reason, and CI pass/fail flag             |

---

## 7. References

* Forecast-GPT Codex
* Hyndman & Athanasopoulos — Forecasting Best Practices
* Forecast-Kernel Phase 1/3 Documentation
