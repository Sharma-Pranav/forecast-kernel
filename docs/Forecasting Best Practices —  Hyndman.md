Forecasting Best Practices — Kernel-Aligned

This repository codifies core forecasting principles from "Hyndman & Athanasopoulos" into CI-enforceable, structure-aware forecasting logic, aligned with the Forecast-Kernel Codex.

---

1. Core Forecasting Foundations

- Forecast Only When Viable
  Avoid forecasting in high-randomness or feedback-driven systems (e.g., exchange rates).

- Structure-Driven Model Selection
  Choose models using demand structure: intermittent → Croston, seasonal → Holt-Winters, low-signal → HistoricAverage.

- Visual Inspection First
  Begin every project with time plots, seasonal plots, lag plots, and scatterplots.

---

2. Forecasting Project Setup

- Define Forecast Intent Early
  Lock use case, granularity, and time horizon before modeling.

- User Alignment
  Validate decision-use cases with stakeholders upfront.

- Combine Historical + Expert Input
  Especially important during regime shifts or sparse-data conditions.

---

3. Model Selection & Evaluation

- Match Baselines to Forecastability
  Use CrostonSBA/Opt for intermittent; HoltWinters for seasonal; SES/Theta for moderate patterns.

- Avoid Averaging in Intermittent Forecasts
  Naive averages distort signal — strictly use Croston variants.

- Point + Interval Forecasts Required
  Report upper/lower bounds and standard error from Phase 3 onward.

- Track Forecast Accuracy Post-Hoc
  Evaluate with MAE, Bias, Score, and error breakdown.

---

4. CI Compliance & Rigor

- Baseline Gate Rule
  A model must beat min(ensemble_naive, holt_winters) on Score to pass.

- Forecastability Metrics Logging
  Always include: ADI, CV², SpectralEntropy, classification in baseline_metrics.json.

- Diebold-Mariano Test
  Use dm_stat, p_value to validate uplift (pass if p_value < 0.05).

---

5. Seasonality & Decomposition

- Use STL/X-13ARIMA for Decomposition
  Apply STL for robustness; X-13ARIMA for macroeconomic data.

- Transform Carefully
  Use log or Box-Cox to stabilize variance.

- Always Visualize Seasonal Patterns
  Detect drift or holiday effects with subseries plots.

---

6. Aggregation Protocol

- Top-Down Forecasting First
  Start at L1 (e.g., Dept-Month). Only descend to L4 (SKU-Day) if:
    pass_ci: true,
    drift_detected: false,
    anchor_bias: <computed>

- Anchor Bias Logging
  Must log: anchor_bias = atomic_forecast - aggregate_forecast in error_breakdown.json.

---

Summary

These best practices ensure:
- CI Compliance
- Structure-Aware Modeling
- Auditable Forecast Lineage
- Minimal Ops Overhead

Use them as hard gates from Phase 1 onward.

Version: forecasting-principles-v1
