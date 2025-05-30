# 🧭 Forecast-GPT Codex — Forecast-Kernel v∞

**Author**: Pranav Sharma

---

## 🌌 Strategic Intent

Design a sovereign, scalable, and cost-conscious forecasting system that runs locally or in the cloud, with ≤12 tools, reproducible logic, and phase-gated CI.

---

## 1. North-Star Drivers

| Driver          | Win Definition                       | Guardrail                                    |
| --------------- | ------------------------------------ | -------------------------------------------- |
| Sovereignty     | Swap any vendor in a weekend         | No closed SaaS                               |
| Leverage        | Every artefact compounds velocity    | ≤ 12 primary tools                           |
| Scalable Uplift | 1 series → 10,000 FM without rewrite | Bootstrap ≤ 5 min · Ops ≤ 2 h/wk · ≤ \$25/mo |

🧹 **Kill-List**: Delete anything that hasn't saved ≥ 1 hr or caught a bug in 90 days.

---

## 2. Tool Stack (Core System)

`git`, `uv`, `pandas`, `statsmodels`, `StatsForecast`, `Pandera`, `MLflow`, `DVC`, `FastAPI`, `Docker`  
**Optional**: `Polars`, `DuckDB`, `RAPIDS`, `Prefect`

---

## 3. Phase Roadmap (0–10)

Each phase builds cleanly into the next, ensuring continuity and compound value:

* Phase 0–2 establish repeatable, tracked baselines.
* Phase 3–6 enforce reproducibility, serving, and drift stability.
* Phase 7 leverages drift-controlled, baseline-aware series to apply regressors cleanly.
* Phase 8 uses those same foundations to benchmark against pretrained models.
* Phase 9–10 scale the system outward: first economically (SaaS) then institutionally (audit & trust).

### 🔹 Phase 0 — Bootstrap

**Goal**: Deterministic environment setup  
**Pass If**: `.venv` activates + prints hello  
**Tools**: `git`, `uv`, `.venv`, `scripts/bootstrap.ps1`  
**Kill If**: Setup takes > 5 minutes or uses > 3 commands  
**Benefit**: Cold-start to CI-ready in under 300s

### 🔹 Phase 1 — Baseline Forecast Battery

**Goal**: Run baseline forecast, track metrics  
**Pass If**: `baseline_metrics.json` saved via `scripts/baseline_sf.py`  
**Models**: Naive, SeasonalNaive, Drift, Holt-Winters, Croston, ensemble_naive  
**CI Rule**: Model must beat `min(ensemble_naive, holt_winters)` on Score  
**Kill If**: MAPE gain < 5% vs naive  
**Benefit**: Reliable control-arm for all future models

### 🔹 Phase 2 — Schema + MLflow

**Goal**: Enable early drift detection and experiment tracking  
**Pass If**:
* `Pandera` schema passes for input structure
* At least 1 `MLflow` experiment run recorded  
**Kill If**: > 3 false positives/month  
**Tools**: `Pandera`, `MLflow`, `configs/`, `src/registry.py`  
**Benefit**: Metrics lineage + failure tracing + reproducibility

### 🔹 Phase 3 — DVC Reproducibility

**Goal**: Enable full rollback and deterministic pipeline  
**Pass If**:
* `dvc repro` regenerates pipeline
* `dvc push` uploads artefacts
* Storage ≤ 500MB after 6 months  
**Kill If**: Large artefacts accumulate or pipelines break during `dvc repro`  
**Benefit**: Robust versioning + disaster recovery

### 🔹 Phase 4 — Serve Anywhere

**Goal**: Run the kernel as a local/offline API  
**Pass If**: `docker run … MODE=serve` returns predictions  
**Tools**: `FastAPI`, `Docker`, `src/serve/`, `Dockerfile`  
**Kill If**: Docker image > 1GB or no local inference  
**Benefit**: Full portability across dev/infra/client systems

### 🔹 Phase 5 — Cloud Burst Training

**Goal**: Push training to EC2 with on-demand sync  
**Pass If**:
* Train → push model → EC2 auto-terminates
* Uses spot instance under `$25/month`  
**Kill If**: AWS costs exceed \$25/mo or no savings vs local  
**Tools**: `aws`, `s3`, `dvc remote`, `train_cloud.sh`  
**Benefit**: Elastic compute, reproducibility, minimal ops debt

### 🔹 Phase 6 — Drift Monitoring

**Goal**: Hands-free model freshness checks  
**Pass If**:
* `refresh.sh` updates predictions
* GitHub Actions detect drift  
**Kill If**: >2 false positives/month  
**Tools**: `GitHub Actions`, `scripts/refresh.sh`, `tests/`  
**Benefit**: SLA-respecting forecasts without manual review

### 🔹 Phase 7 — Feature-Aware Forecasting (LightGBM)

**Goal**: Handle regressors and structured features  
**Pass If**:
* `features.py` generates features without leak
* `lightgbm_train.py` runs and logs to MLflow
* Model outperforms Holt-Winters on Score  
**Tools**: `LightGBM`, `pandas`, `features.py`, `mlflow`  
**Kill If**: Feature ETL cost > model uplift OR S3/compute costs explode  
**Benefit**: Enables promotion impact, scale-out, and feature experimentation

### 🔹 Phase 8 — Foundation Models (TabPFN/TimeGPT)

**Goal**: Leverage pretrained or zero-shot models for ceiling benchmarks  
**Pass If**: Model output is generated via TabPFN or TimeGPT API and Score is tracked  
**Tools**: `TabPFN`, `TimeGPT`, HuggingFace or API SDKs  
**Kill If**: Latency > 500ms (CPU p95) or no gain over LightGBM  
**Benefit**: Establishes power benchmark and foundation-aware fallback layer

### 🔹 Phase 9 — Monetizable SaaS Layer

**Goal**: Convert kernel into a multi-tenant offering with billing and RDS  
**Pass If**: ECS/Fargate deploys live model endpoint, Stripe bills clients, Postgres stores metrics  
**Tools**: `AWS Fargate`, `Stripe`, `Postgres`, `Docker Compose`  
**Kill If**: Ops > 8 h/wk or no paying user after pilot  
**Benefit**: Transition from project to product with economic sustainability

### 🔹 Phase 10 — Enterprise Hardening & Auditability

**Goal**: Enable enterprise readiness via lineage, audit, and rollback controls  
**Pass If**: LakeFS snapshots + Evidently dashboard are integrated into drift chain  
**Tools**: `LakeFS`, `Evidently`, `DVC`, `GitHub Actions`  
**Kill If**: Added complexity without external demand  
**Benefit**: Offers enterprise trust layer, de-risking vendor engagement

---

## 4. Metrics Logic

* `MAE`: Absolute error magnitude  
* `Bias`: Signed average error  
* `Score = MAE + |Bias|` → primary KPI across Phases 1, 7, and 8  
* **Rule**: Every new model must beat `ensemble_naive` or `holt_winters` on Score

---

## 5. Forecastability Classifier

| Metric           | Use Case            | Action                                                     |
| ---------------- | ------------------- | ---------------------------------------------------------- |
| ADI × CV²        | Intermittent demand | Use if ADI ≥ 1.32 → classify (Smooth, Lumpy…)              |
| Spectral Entropy | Continuous demand   | Use if ADI < 1.32 → lower entropy = better forecastability |

---

## 6. Sample Q&A

**Q: What’s the cleanest success for Phase 1?**  
A: `baseline_sf.py` runs and creates `baseline_metrics.json`. Score beats naive/holt_winters. Tagged as `v0.1-baseline`.

**Q: What does Phase 3 give me?**  
A: Full rollback, reproducible pipelines, and tracked artefacts. Enables disaster recovery and versioned experiments.

**Q: I have ADI = 1.5, CV² = 2.9. What model?**  
A: Classify as intermittent. Try Croston (SBA), then compare with SeasonalWindowAvg.

**Q: What breaks CI in Phase 2?**  
A: Missing Pandera schema, failed MLflow run, or >3 false positives/month.

**Q: When should I switch to DuckDB?**  
A: If parquet files > 500MB or columnar queries slow in Pandas.

**Q: Why FastAPI + Docker in Phase 4?**  
A: Enables local/offline deployment. Ensures model can run without cloud access.

**Q: What’s the kill signal for a tool?**  
A: If it adds complexity but hasn’t saved ≥ 1 hour or caught a bug in 90 days.

---

## 7. Execution SLA

* Ops time ≤ 2 h/wk  
* Storage cap ≤ 500MB after 6 months  
* GitHub Actions false positives ≤ 2/month  
* AWS cost ≤ \$25/month for Phase 0–6  
* Review kill-list every 90 days

---

## 9. Knowledge Layer — Embedded Forecasting Principles

### 📌 Demand Planning Excellence – Core Steps

* Clarify why forecasts are needed and link to business decisions.
* Focus on unconstrained demand. Include external drivers.
* Track accuracy, bias, and Score (MAE + |Bias|).
* Deploy robust models, minimize human intervention.
* Use FVA to validate overrides. Assign accountability.

### 📌 Demand vs. Sales Forecasting

* Demand Forecast: Customer need (unconstrained).
* Sales Forecast: Constrained by supply. Can mislead planning.

### 📌 Shortage-Censoring & Substitution

* Mark zero/low demand periods during stockouts.
* Attribute substitution orders to original SKUs.
* Estimate lost demand using external drivers.

### 📌 Forecasting Metrics

* MAE: Robust average error
* Bias: Directional tendency
* RMSE: Penalizes large errors
* MAPE: Risky with low-volume SKUs
* Score = MAE + |Bias|: Kernel standard

### 📌 Forecast Value Added (FVA)

* Track contribution at every step: model → planner → sales
* Filter noise; enable process improvement

### 📌 ABC-XYZ Review Targeting

* ABC = Economic value
* XYZ = Forecastability
* Focus review on A/X (high value, low error)

### 📌 Aggregation & Granularity

* Match forecast granularity to decision-making granularity
* Use top-down, bottom-up, or middle-out aggregation

### 📌 Forecast Horizon & Risk

* Risk Horizon = Lead Time + Review Cycle
* Forecasts should always exceed risk horizon

### 📌 One Number Mindset

* Align on shared inputs/events/assumptions
* Allow forecasts to vary by function (logistics, finance, etc.)

### 📌 Judgmental Forecasting

* Use when data is missing or blind spots exist
* Apply FVA to track value of human adjustments

### 📌 Driver-Based & ML Forecasting

* Include promotions, pricing, weather, seasonality
* Use LightGBM, TabPFN, and scenario planners
* Validate all with Score vs tuned moving average
