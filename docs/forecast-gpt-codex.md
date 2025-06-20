# 🛭 FORECAST ‒ GPT CODEX — Forecast ‒ Kernel v∞ (PyOD Extended Variant)

**Author**: Pranav Sharma
**Variant**: Anomaly Overlay Logic

---

## 🌌 Strategic Intent

Design a sovereign, scalable, and cost ‒ conscious forecasting system that runs locally or in the cloud, using ≤12 core tools. It supports reproducible logic, structure ‒ aware aggregation descent, anomaly overlays, and phase-gated CI/CD.

---

## 🚩 1. North ‒ Star Drivers

| Driver          | Win Definition                                                                        | Guardrail                                       |
| --------------- | ------------------------------------------------------------------------------------- | ----------------------------------------------- |
| Sovereignty     | Swap any vendor in a weekend **and redeploy, full test ‒ suite green in ≤ 48 h**      | No closed SaaS allowed                          |
| Leverage        | Every artefact compounds velocity                                                     | Max 12 primary tools                            |
| Scalable Uplift | 1 series → 10 000 FM without rewrite **and trains 10 000 FM in < 30 min wall ‒ time** | Bootstrap ≤5 min · Ops ≤2 h/week · < \$25/month |

**🧹 Kill ‒ List** Delete anything that hasn’t saved ≥ 1 hour *or* caught a bug in 90 days.

---

## 🧰 2. Tool Stack

* **Core (11 / 12 limit)**: `git`, `uv`, `pandas`, `statsmodels`, `StatsForecast`, `Pandera`, `MLflow`, `DVC`, `FastAPI`, `Docker`, `PyOD`
* **Optional (+4)**: `Polars`, `DuckDB`, `RAPIDS`, `Prefect`

---

## 🕦 4. Metrics Logic

* **MAE** Mean Absolute Error
* **Bias** Signed average error
* **Score** Composite KPI = MAE + |Bias|
* **CI Rule** `Score ≤ min(ensemble_naive, holt_winters)`
* **Anchor Rule** `anchor_bias = atomic_forecast − aggregate_forecast`

### Additional Metrics

| Metric     | Use-case              | Calc                                                |
| ---------- | --------------------- | --------------------------------------------------- |
| **CRPS**   | Distribution accuracy | `properscoring.crps_ensemble`                       |
| **PICP**   | Interval coverage     | hits / total                                        |
| **ACE**    | Avg coverage error    | `abs(PICP − α)`                                     |
| **VOI\_€** | Value-of-Information  | Δ expected cost between current & improved forecast |

---

## 🧮 Decision Value Metrics in Ops

- Calculate and track **Decision Value Added (DVA)** for all major actions:  
  `% reduction in cost/stockouts/emissions due to forecast-driven actions.`

- Track and require **Forecast Value Coefficient (FVC)**:  
  `FVC = (Cost without model – Cost with model) / Cost without model`  
  **Deploy only if FVC ≥ 0.35.**


## 🔢 4b. Decision ‒ Kernel Integration *(PFOD)*

> Source chapters: 7.1–7.4, 12.1–12.4, 13.1–13.4 from *Probabilistic Forecasts & Optimal Decisions* (Krzysztofowicz, 2024)

### Core Formulas

| Function             | Formula                                   | Description                           |                                   |
| -------------------- | ----------------------------------------- | ------------------------------------- | --------------------------------- |
| **Critical Ratio**   | `CR = Cu / (Cu + Co)`                     | Cu = underage cost, Co = overage cost |                                   |
| **Optimal Quantity** | `Q* = F⁻¹(CR)`                            | Inverse CDF of demand distribution    |                                   |
| **Bayes Action**     | \`a\* = arg minₐ ∫ L(a, θ)p(θ             | data)dθ\`                             | Minimises posterior expected loss |
| **VOI**              | `VOI = E_cost(current) − E_cost(perfect)` | ROI of perfect forecast vs current    |                                   |

### Microservice Endpoints

| Endpoint              | Payload                     | Returns                  |
| --------------------- | --------------------------- | ------------------------ |
| `POST /recommend_qty` | `{mu, sigma, Cu, Co}`       | `{q_opt, expected_cost}` |
| `POST /voi`           | `{dist_params, cost_curve}` | `{voi_euro}`             |

---

## 🗂️ Glossary *(Key Short ‒ Hands)*

| Term              | Definition                                                              |
| ----------------- | ----------------------------------------------------------------------- |
| `anchor_bias`     | Difference between atomic and aggregate forecasts                       |
| `recommend_qty`   | Endpoint for cost-optimal order quantity                                |
| `VOI_€`           | € benefit of perfect information                                        |
| `CR`              | Critical ratio Cu / (Cu + Co)                                           |
| `Q*`              | Optimal quantity = F⁻¹(CR)                                              |
| `Bayes Action`    | Action that minimises expected posterior loss                           |
| `CRPS`            | Continuous Ranked Probability Score                                     |
| `PICP / ACE`      | Coverage probability and associated error                               |
| `FPR`             | False Positive Rate from anomaly detection                              |
| `CI descent`      | Cross-impact consistency during hierarchical descent                    |
| `Edge Smoke-Test` | Offline test to validate container readiness without cloud dependencies |

---

## 🧠 5. Forecasting Principles

* CI descent must pass before propagating to lower levels
* Residuals and raw features are both inputs to anomaly detection
* Forecast errors are recycled as learning signals (features)
* Feedback loops must be tracked and linked to correction events

### Aggregation & Granularity

* L1/L2: Holt-Winters, SES
* L3/L4: Croston (SBA/Opt)

### Anomaly Overlay

* PyOD detects on residuals and raw inputs
* Flags feed override logic, retraining, and planner feedback

---

## 🩌 6. Operating Principles

1. **No fluff. Only signal.**
2. **Forecasts are inputs, not commands.**
3. **Institutionalise feedback** — every error is recycled as training signal.

### 6a — Process‑Filter Gate *(NEW)*

| Gate                       | Yes/No Question                                 | If **No** → Action      |
| -------------------------- | ----------------------------------------------- | ----------------------- |
| **G1 · Leverage Fit**      | Moves KPI ≥ 10% or unlocks module in ≤ 30 days? | Archive to Later        |
| **G2 · Re‑Use Radius**     | Usable in ≥ 2 domains?                          | Skim + Atomic Notes     |
| **G3 · Time‑to‑Prototype** | Shippable in ≤ 5 Pomodoros?                     | Defer until next sprint |
| **G4 · Metric Tie‑In**     | Tied to Grafana metric?                         | Define or discard       |
| **G5 · Opportunity Cost**  | Better than refining 80% module?                | Finish existing first   |

> **Mantra**: “If it doesn’t move a Grafana metric this sprint, it waits.”

---

## 🧪 7. Quick Build Loop

1. Charter → `/docs/charter.md`
2. Audit → `src/utils/data_audit.py`
3. EDA → `/notebooks/`
4. Model Select → `src/pipelines/model_selection.py`
5. Diagnostics → `src/evaluation/residuals.py`
6. Deploy → `src/pipelines/production.py`
7. Tests → `tests/test_contracts.py`

---

## 🔍 8. Model Selection Heuristics

| Data Pattern              | Model              | Why                       |
| ------------------------- | ------------------ | ------------------------- |
| Flat mean, no seasonality | MeanForecast       | Tough to beat             |
| Random walk               | Naïve              | Efficient‑markets model   |
| Stable seasonality        | SeasonalNaïve, ETS | Low tuning cost           |
| Trend + seasonality       | ETS Add/SARIMA     | Captures joint structure  |
| Multiple seasonalities    | TBATS / Prophet    | Flexible seasonal windows |
| External drivers          | ARIMAX / Dyn Reg   | Injects causality         |

---

## 🛱️ 9. Communication of Uncertainty

* Always return prediction intervals
* Show horizon-wise widening of intervals
* Pair forecasts with narrative overlays for planning

---

## 🔐 10. Governance Principles

| Area      | Practice                                   |
| --------- | ------------------------------------------ |
| Privacy   | Block cloud burst if PII detected          |
| Overrides | Require manager review if GoalPressure = Y |
| Lineage   | Log SHA‑256 snapshot of training data      |
| Data Ops  | Version both raw + overridden datasets     |
| Feedback  | Dashboards must track model accuracy       |
| Detection | Watch level + variance shifts over time    |

---

## ⚠️ 11. Pitfalls Checklist

* Seasonal‑Naïve not beaten
* No calendar effects modeled
* Residuals autocorrelated (Ljung-Box p ≤ 0.05)
* Fat tails left unmodeled
* VOI\_€ < 15% of baseline ordering cost

---

## 🔧 12. Kernel Extensions

| Horizon | Modules                                   |
| ------- | ----------------------------------------- |
| 0–6 m   | Real-time anomalies, staffing triggers    |
| 6 m–2 y | S\&OP scenario generation, error learning |
| 2–10 y  | Monte-Carlo macro simulators              |

---
