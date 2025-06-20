# 🛭 FORECAST ‒ GPT CODEX — Forecast ‒ Kernel v∞ — Decision Velocity × Decision Quality

**Author**: Pranav Sharma
**Variant**: Anomaly Overlay Logic

---

## 🌌 Strategic Intent

Design a sovereign, scalable, and cost‑conscious forecasting kernel that runs locally or in the cloud, using **≤ 12 core tools**. It supports reproducible logic, structure‑aware aggregation descent, anomaly overlays, and phase‑gated CI/CD.

---

## 🚩 1. North‑Star Drivers

| Driver              | Win Definition                                                                | Guardrail                                         |
| ------------------- | ----------------------------------------------------------------------------- | ------------------------------------------------- |
| **Sovereignty**     | Swap any vendor in a weekend & redeploy full test‑suite green in ≤ 48 h       | No closed SaaS allowed                            |
| **Leverage**        | Every artefact compounds velocity                                             | ≤ 12 primary tools                                |
| **Scalable Uplift** | 1 series → 10 000 FM without rewrite & trains 10 000 FM in < 30 min wall‑time | Bootstrap ≤ 5 min · Ops ≤ 2 h/week · < \$25/month |

**🧹 Kill‑List** Delete anything that hasn’t saved ≥ 1 hour *or* caught a bug in 90 days.

---

## 🧰 2. Tool Stack

* **Core (11 / 12 limit)**: `git`, `uv`, `pandas`, `statsmodels`, `StatsForecast`, `Pandera`, `MLflow`, `DVC`, `FastAPI`, `Docker`, `PyOD`
* **Optional (+4)**: `Polars`, `DuckDB`, `RAPIDS`, `Prefect`
  *Grafana & scipy are bundled inside Docker images and do **not** consume tool‑cap slots.*

---

## 🧭 3. Phase Roadmap (0–10)

Each phase lists **GOAL · PASS IF · BENEFIT · TOOLS**. Sub‑phases (lettered) appear only when they’re strict prerequisites.

### Phase 0 — Bootstrap

**Goal** Deterministic environment setup
**Pass** `.venv` activates and prints “hello” in < 5 min
**Benefit** Cold‑start to CI‑ready in < 300 s
**Tools** git, uv, .venv, `scripts/bootstrap.ps1`
**Secrets** managed via **Doppler / AWS Secrets Manager**; kernel endpoints secured with **JWT auth** Manager\*\*; kernel endpoints secured with **JWT auth**, `scripts/bootstrap.ps1`

### Phase 0a — Data Pre‑Flight *(NEW)*

**Goal** Catch schema drift before code runs
**Pass** `preflight_report.json` matches contract
**Benefit** Fail‑fast on bad data
**Tools** Pandera, Great Expectations, DuckDB

### Phase 1 — Baseline Forecast Battery

**Goal** Benchmarks & metrics
**Pass** `baseline_metrics.json`; MAPE ≥ 5 % over Naïve
**Tools** Naïve, SeasonalNaïve, Drift, Holt‑Winters, Croston

### Phase 1b — Aggregation‑Aware CI Descent

**Goal** Cascade L1 (Dept‑Month) → L4 (SKU‑Store‑Day)
**Pass** CI tests green; `anchor_bias` logged
**Benefit** Cheaper compute + full traceability
**Tools** pandas, FastAPI, MinT‑Shrink reconciliation

### Phase 1c — Feature Registry Stub *(NEW)*

**Goal** One YAML maps raw → engineered features
**Pass** `features.yaml` committed—no hard‑coded names
**Tools** yaml, pandas

### Phase 2 — Schema + MLflow + PyOD Overlay

**Goal** Drift diagnostics + governance
**Pass** Schema validates; MLflow run; FPR ≤ 0.05; VOI\_€ ≥ 15 % of baseline cost
**Tools** Pandera, MLflow, PyOD

### Phase 2b — Back‑Test Grid & Hyper‑Search *(NEW)*

**Goal** Rolling‑origin search
**Pass** `grid_metrics.parquet`; ΔMAE ≥ 3 %
**Tools** `StatsForecast.grid`, joblib

### Phase 2c — Decision‑Kernel Build (PFOD)

**Goal** Cost‑optimising Bayes decision service
**Pass** `decision_kernel.py` unit‑tests + FastAPI `/recommend_qty` & `/voi` return values
**Benefit** Turns forecasts into € actions; feeds every later phase
**Tools** numpy, scipy, FastAPI

### Phase 3 — DVC Reproducibility + Audit Hardening

**Goal** Full rollback & SHA audit
**Pass** `dvc repro` & `audit_log.json` archived
**Tools** DVC

### Phase 4 — Serve & Visual Audit (Edge‑Ready)

**Goal** Containerised API + anomaly plots, including offline smoke‑test
**Pass** `docker compose up` then `curl localhost/ping` ⇒ `{status:"ok"}` < 10 s; < 5 % false spikes
**Tools** FastAPI, Docker, Grafana

### Phase 4.5 — Scenario Framing Layer *(INSERTED)*

**Goal** Simulate macro/promo overrides
**Pass** Multiple `scenario_*.json` → simulation charts rendered
**Tools** pandas, Jupyter, FastAPI

### Phase 5 — Cloud Burst Training

**Goal** Train on spot EC2
**Pass** Cost < \$25/month
**Tools** AWS CLI, DVC remote

### Phase 6 — Drift Monitoring + Auto‑Retrain

**Goal** Cron checks drift; retrain if 14‑day MASE > threshold
**Pass** `drift_monitor.json` & `drift_trigger.log` updated
**Tools** GitHub Actions, PyOD

### Phase 7 — Feature‑Aware Forecasting

**Goal** LightGBM regressors gated by anomaly flags
**Pass** Beats Holt‑Winters on **Score**
**Tools** LightGBM, MLflow

### Phase 8 — Foundation Models

**Goal** Benchmark ceiling (TabPFN, TimeGPT)
**Pass** Diebold‑Mariano p < 0.05
**Tools** TabPFN, TimeGPT, scipy

### Phase 9 — SaaS Layer + FinOps Telemetry *(UPGRADE PLANNED)*

**Goal** Monetise multi‑tenant; tag cost per job
**Pass** Stripe billing lives; `cost_report.csv` anomalies < 5 %
**Tools** Stripe, AWS Cost Explorer

### Phase 10 — Enterprise Audit Layer

**Goal** Deep lineage & snapshots
**Pass** LakeFS & Evidently dashboards active
**Tools** LakeFS, Evidently

## 🕦 4. Metrics Logic

* **MAE** – Mean Absolute Error
* **Bias** – Signed average error
* **Score** – Composite KPI = MAE + |Bias|
* **Target** – `Score ≤ 0.9 × baseline_naïve`
* **CI Rule** – `Score ≤ min(ensemble_naive, holt_winters)`
* **Anchor Rule** – `anchor_bias = atomic_forecast − aggregate_forecast`

### Additional Metrics

| Metric     | Use‑case               | Calculation                                         |
| ---------- | ---------------------- | --------------------------------------------------- |
| **CRPS**   | Distribution accuracy  | `properscoring.crps_ensemble`                       |
| **PICP**   | Interval coverage      | hits / total                                        |
| **ACE**    | Average coverage error | `abs(PICP − α)`                                     |
| **VOI\_€** | Value‑of‑Information   | Δ expected cost between current & improved forecast |

### 🧮 Decision Value Metrics in Ops

* **Decision Value Added (DVA)** – `% reduction in cost, stockouts, or emissions due to forecast‑driven actions.`
* **Forecast Value Coefficient (FVC)** – `(Cost_without_model − Cost_with_model) / Cost_without_model`

  * **Deployment Threshold** – Deploy only if `FVC ≥ 0.35`.

### 🔢 4b. Decision‑Kernel Integration *(PFOD)*

> *Source: Probabilistic Forecasts & Optimal Decisions* (Krzysztofowicz, 2024) — Ch. 7.1‑7.4, 12.1‑12.4, 13.1‑13.4

| Function             | Expression                                | Purpose                                  |                                   |
| -------------------- | ----------------------------------------- | ---------------------------------------- | --------------------------------- |
| **Critical Ratio**   | `CR = Cu / (Cu + Co)`                     | Balance underage vs overage cost         |                                   |
| **Optimal Quantity** | `Q* = F⁻¹(CR)`                            | Inverse CDF of demand distribution       |                                   |
| **Bayes Action**     | \`a\* = argminₐ ∫ L(a,θ) · p(θ            |  data) dθ\`                              | Minimises posterior expected loss |
| **VOI**              | `VOI = E_cost(current) − E_cost(perfect)` | Monetises benefit of perfect information |                                   |

**Endpoints**
*All kernel endpoints require **JWT bearer auth***

| Method & Path         | Payload                     | Response                 |
| --------------------- | --------------------------- | ------------------------ |
| `POST /recommend_qty` | `{mu, sigma, Cu, Co}`       | `{q_opt, expected_cost}` |
| `POST /voi`           | `{dist_params, cost_curve}` | `{voi_euro}`             |

---

## 🧠 5. Forecasting Principles

* CI descent must pass before propagating to lower levels
* Residuals + raw features → anomaly detection
* Errors recycled as learning signals
* Feedback loops tracked + linked to correction events

**Aggregation & Granularity**
L1/L2: Holt‑Winters, SES
L3/L4: Croston (SBA/Opt)

**Anomaly Overlay**
PyOD on residuals + raw; flags feed overrides + retrain

---

## 🩌 6. Operating Principles

1. No fluff. Only signal.
2. Forecasts are inputs, not commands.
3. Institutionalise feedback — every error becomes training signal.

### 6a — Process‑Filter Gate

| Gate                 | Yes/No Question                   | If **No** → Action |
| -------------------- | --------------------------------- | ------------------ |
| G1 Leverage Fit      | KPI ≥ 10 % in ≤ 30 d?             | Archive            |
| G2 Re‑Use Radius     | ≥ 2 domains?                      | Skim + Notes       |
| G3 Time‑to‑Prototype | ≤ 5 Pomodoros?                    | Defer              |
| G4 Metric Tie‑In     | Linked to Grafana?                | Define/Discard     |
| G5 Opportunity Cost  | Better than refining 80 % module? | Finish existing    |

---

## 🧪 7. Quick Build Loop

1. Charter → `/docs/charter.md`
2. Audit → `src/utils/data_audit.py`
3. EDA → `/notebooks/`
4. Model Select → `src/pipelines/model_selection.py`
5. Diagnostics → `src/evaluation/residuals.py`
6. Deploy → `src/pipelines/production.py`
7. Tests → `tests/test_contracts.py`

---

## 🔍 8. Model Selection Heuristics

| Data Pattern              | Model              | Why                       |
| ------------------------- | ------------------ | ------------------------- |
| Flat mean, no seasonality | MeanForecast       | Tough to beat             |
| Random walk               | Naïve              | Efficient‑markets model   |
| Stable seasonality        | SeasonalNaïve, ETS | Low tuning cost           |
| Trend + seasonality       | ETS Add/SARIMA     | Captures joint structure  |
| Multiple seasonalities    | TBATS / Prophet    | Flexible seasonal windows |
| External drivers          | ARIMAX / Dyn Reg   | Injects causality         |

---

## 🛱️ 9. Communication of Uncertainty

* Always return **prediction intervals**.
* Visualise horizon‑wise widening of intervals.
* Pair quantitative forecasts with **narrative overlays** for planners.

---

## 🔐 10. Governance Principles

| Area      | Practice                                     |
| --------- | -------------------------------------------- |
| Privacy   | Block cloud burst if PII detected            |
| Overrides | Require manager review if `GoalPressure = Y` |
| Lineage   | Log SHA‑256 snapshot of training data        |
| Data Ops  | Version both raw **and** overridden datasets |
| Feedback  | Dashboards must track model accuracy         |
| Detection | Watch level + variance shifts over time      |

---

## ⚠️ 11. Pitfalls Checklist

* Seasonal‑Naïve not beaten
* No calendar effects modelled
* Residuals autocorrelated (Ljung‑Box p ≤ 0.05)
* Fat tails left unmodelled
* `VOI_€` < 15 % of baseline ordering cost

---

## ⛓️ Constraint & Feedback Compass

### Quarterly System Constraint Map

* Explicitly map **Data → Forecast → Decision → Execution → Feedback**.
* Quantify friction, delay, and value loss at each node.
* **Rule:** Kill any initiative that optimises a non‑bottleneck.

### Real‑Time Compounding Feedback

* All overrides, errors, and planner interventions are **automatically** logged and recycled as:

  * new features,
  * test cases,
  * or protocol patches.
* Any override pattern seen **> 2×** triggers a protocol/code patch (not only documentation).

### Embedded Network Effects

* Track **number and depth** of external API integrations (suppliers, customers, partner systems).
* Make “# of systems that cannot operate without kernel API” a core health metric.
* Design for **network participation growth** (review quarterly).

### Anti‑Blind Spot Table (Quarterly Review)

| Blind Spot          | Scan Question     | Correction Action           |
| ------------------- | ----------------- | --------------------------- |
| Model as constraint | Is it *really*?   | System map check            |
| Feedback recycling  | Enforced in code? | Pipeline/test not checklist |
| Network effect      | Embedded APIs?    | KPI, growth target          |
| Regret/latency      | In Grafana?       | Wire to dashboard or kill   |

---

## 🔧 12. Kernel Extensions

| Horizon | Modules                                   |
| ------- | ----------------------------------------- |
| 0–6 m   | Real‑time anomalies, staffing triggers    |
| 6 m–2 y | S\&OP scenario generation, error learning |
| 2–10 y  | Monte‑Carlo macro simulators              |

---

## 🛡️ 13. Escalation & Override Flow

* If the **anomaly overlay triggers** (residual > 3σ **or** FVC < 0.35) → automatically **flag for human review**.
* All **overrides are logged and versioned**; each override is recycled as a learning signal for the next retrain cycle.
* If the overall **Score exceeds the baseline** for **two consecutive cycles**, the system auto‑falls back to the **Naïve forecast**, emits an alert, and mandates a formal **Root‑Cause Analysis (RCA)**.
  *Cooldown*: at least **one full forecasting cycle with Score ≤ baseline** before re‑enabling the model.
* After fallback, the system must deliver **one full clean cycle** (Score ≤ baseline) before the model can be re‑enabled.

## 🗂️ Glossary (Key Short‑Hands)

| Term            | Definition                                                              |
| --------------- | ----------------------------------------------------------------------- |
| anchor\_bias    | Difference between atomic and aggregate forecasts                       |
| recommend\_qty  | Endpoint for cost-optimal order quantity                                |
| VOI\_€          | € benefit of perfect information                                        |
| CR              | Critical ratio Cu / (Cu + Co)                                           |
| Q\*             | Optimal quantity = F⁻¹(CR)                                              |
| Bayes Action    | Action that minimises expected posterior loss                           |
| CRPS            | Continuous Ranked Probability Score                                     |
| PICP / ACE      | Coverage probability and associated error                               |
| FPR             | False Positive Rate from anomaly detection                              |
| CI descent      | Cross-impact consistency during hierarchical descent                    |
| Edge Smoke-Test | Offline test to validate container readiness without cloud dependencies |
