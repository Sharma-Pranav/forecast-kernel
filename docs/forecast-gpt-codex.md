# 🗭 FORECAST‑GPT CODEX — Forecast‑Kernel v∞ (PyOD Extended Variant)

**Author**: Pranav Sharma  
**Variant**: Anomaly Overlay Logic  

---

## 🌌 Strategic Intent

Design a sovereign, scalable, and cost‑conscious forecasting system that runs locally or in the cloud, using ≤12 core tools. It supports reproducible logic, structure-aware aggregation descent, anomaly overlays, and phase-gated CI/CD.

---

## 🚩 1. North-Star Drivers

| Driver         | Win Definition                       | Guardrail                              |
|----------------|--------------------------------------|----------------------------------------|
| Sovereignty    | Swap any vendor in a weekend         | No closed SaaS allowed                 |
| Leverage       | Every artefact compounds velocity    | Max 12 primary tools                   |
| Scalable Uplift| 1 series → 10,000 FM without rewrite | Bootstrap ≤5 min · Ops ≤2 h/week · <\$25/month |

**🧹 Kill‑List**: Delete anything that hasn’t saved ≥1 hour or caught a bug in 90 days.

---

## 🧰 2. Tool Stack

- **Core**: `git`, `uv`, `pandas`, `statsmodels`, `StatsForecast`, `Pandera`, `MLflow`, `DVC`, `FastAPI`, `Docker`, `PyOD`  
- **Optional**: `Polars`, `DuckDB`, `RAPIDS`, `Prefect`

---

## 🧭 3. Phase Roadmap (0–10)

Each phase includes **GOAL**, **PASS IF**, and **BENEFIT** with explicit success criteria.

### Phase 0 — Bootstrap
**Goal**: Deterministic environment setup  
**Pass If**: `.venv` activates and prints "hello" in under 5 min using ≤3 commands  
**Benefit**: Cold-start to CI-ready in <300 s  
**Tools**: `git`, `uv`, `.venv`, `scripts/bootstrap.ps1`

### **Phase 0a — Data Pre-Flight** *(NEW)*  
Goal Catch schema drift before code runs  
Pass `preflight_report.json`; no column drift vs contract  
Benefit Fail-fast on bad data  
Tools `Pandera`, `Great Expectations`, `duckdb`


### Phase 1 — Baseline Forecast Battery
**Goal**: Establish benchmark accuracy and metrics  
**Pass If**: `baseline_metrics.json` saved; MAPE at least 5% better than Naïve  
**Tools**: Naïve, SeasonalNaïve, Drift, Holt-Winters, Croston, `ensemble_naive`

### **Phase 1c — Feature Registry Stub** *(NEW)*  
Goal One YAML maps raw → engineered features  
Pass `features.yaml` committed; all Phase 2+ code imports via keys  
Benefit Zero hidden renames, instant deprecations  
Tools `YAML`, `pandas`, `polars` (opt.)

### Phase 1b — Aggregation-Aware CI Descent
**Goal**: Cascade forecasts from L1 (Dept-Month) to L4 (SKU-Store-Day)  
**Pass If**: CI descent passes with `anchor_bias` logged  
**Benefit**: Reduced cost, better audit trail

### Phase 2 — Schema + MLflow + PyOD Anomaly Overlay
**Goal**: Drift diagnostics + governance  
**Pass If**: Schema validated, MLflow runs, False Positive Rate ≤ 0.05  
**Tools**: Pandera, MLflow, PyOD

### **Phase 2c — Back-Test Grid & Hyper-Search** *(NEW)*  
Goal Grid search core params w/ rolling-origin  
Pass `grid_metrics.parquet` in MLflow; ΔMAE ≥ 3 % vs baseline  
Benefit Quantify ROI before fancy models  
Tools `StatsForecast.grid`, `MLflow`, `joblib`

### Phase 3 — DVC Reproducibility + Audit Hardening
**Goal**: Full rollback + SHA tracking  
**Pass If**: `dvc repro`, `dvc push`, `audit_log.json` written

### Phase 4 — Serve & Visual Audit
**Goal**: Local API + anomaly-flag plots  
**Pass If**: `docker run` serves, delta audit shows <5% false spikes  
**Tools**: FastAPI, Docker

### Phase 4b — Edge Serve Smoke-Test 
Goal One-click container demo offline  
Pass `curl localhost/ping` ⇒ `{"status":"ok"}` < 10 s  
Benefit No internet? Still demo.  
Tools `docker-compose`, `FastAPI`, `Makefile`

### Phase 5 — Cloud Burst Training
**Goal**: Train on EC2 with auto-termination  
**Pass If**: Training completes, cost < \$25/month  
**Tools**: AWS CLI, S3, DVC Remote

### Phase 6 — Drift Monitoring
**Goal**: Auto-refresh + anomaly watch  
**Pass If**: `refresh.sh` + `drift_monitor.json` updated  
**Tools**: GitHub Actions, PyOD

### **Phase 6b — Auto-Retrain Trigger** *(NEW)*  
Goal Cron checks drift; retrain if 14-day MASE > threshold  
Pass `drift_trigger.log` shows decision · cost logged  
Benefit No stale model creep  
Tools GitHub Actions (cron), PyOD, shell

### Phase 7 — Feature-Aware Forecasting
**Goal**: Add LightGBM regressors with PyOD gating  
**Pass If**: Model beats Holt-Winters on Score  
**Tools**: LightGBM, MLflow, PyOD

### Phase 7b — Driver Attribution Audit
**Goal**: Quantify impact of anomaly drivers  
**Pass If**: ≥20% variance explained; error reduced ≥5%  
**Tools**: SHAP, delta attribution scripts

### Phase 8 — Foundation Models
**Goal**: Benchmark ceiling with pretrained models  
**Pass If**: Diebold-Mariano p < 0.05  
**Tools**: TabPFN, TimeGPT

### Phase 9 — SaaS Layer
**Goal**: Monetize with multi-tenant and explainability  
**Pass If**: Stripe billing works; per-client anomaly logs  
**Tools**: Stripe, FastAPI

### **Phase 9b — FinOps Telemetry** *(NEW)*  
Goal Cost tags on every cloud job  
Pass `cost_report.csv` daily; anomalies < 5 %  
Benefit Budget guard; pricing intel  
Tools AWS Cost Explorer API, `pandas`, `prefect`


### Phase 10 — Enterprise Audit Layer
**Goal**: Deep forensics + snapshot lineage  
**Pass If**: LakeFS + Evidently dashboards active  
**Tools**: LakeFS, Evidently AI

---

## 📏 4. Metrics Logic

- `MAE`: Mean Absolute Error (magnitude of error)  
- `Bias`: Signed average error (direction)  
- `Score`: Composite KPI defined as `Score = MAE + |Bias|`  
- `anomaly_flag`: Any residual or input anomaly detected  
- **CI Rule**: `Score ≤ min(ensemble_naive, holt_winters)`  
- **Anchor Rule**: `anchor_bias = atomic_forecast − aggregate_forecast` (required for L3/L4 descent)

**Metric add-ons**  
| Metric | Use-case | Calc |
|--------|----------|------|
| **CRPS** | Full-distribution accuracy | `properscoring.crps_ensemble` |
| **PICP** | Interval coverage % | hits / total |
| **ACE** | Avg coverage error vs target | `|PICP − α|` |
---

## 🧠 5. Forecasting Principles

- Descend through aggregation only after CI pass.  
- PyOD on residuals **and** inputs.  
- Every forecast error becomes a future feature.

### Aggregation & Granularity
- Start at high forecastability levels (L1), descend only post-CI pass  
- L1/L2: Holt-Winters, SES  
- L3/L4: Croston (SBA/Opt)

### Anomaly Overlay
- Apply PyOD to both residuals and feature inputs  
- Used for gating regressors, triggering overrides, and audit diagnostics

---

## 🧘 6. Operating Principles

1. No fluff. Only signal.  
2. Forecasts are inputs, not commands.  
3. Institutionalize feedback — each error becomes a feature.

---

## 🧪 7. Quick Build Loop

1. Charter → `/docs/charter.md`  
2. Audit → `src/utils/data_audit.py`  
3. EDA → `/notebooks/`  
4. Model Select → `src/pipelines/model_selection.py`  
5. Diagnostics → `src/evaluation/residuals.py`  
6. Deploy → `src/pipelines/production.py`
7. Unit + Contract Tests → `tests/test_contracts.py` (Pandera) in CI.
---

## 🔍 8. Model Selection Heuristics

| Data Pattern              | Model                | Why                          |
|---------------------------|----------------------|-------------------------------|
| Flat mean, no seasonality | MeanForecast         | Tough to beat                |
| Random walk               | Naïve                | Efficient markets model      |
| Stable seasonality        | SeasonalNaive, ETS   | Low tuning cost              |
| Trend + seasonality       | ETS Add/SARIMA       | Captures joint structure     |
| Multiple seasonalities    | TBATS / Prophet      | Flexible seasonal windows    |
| External drivers          | ARIMAX / Dyn Regr.   | Injects causality            |

---

## 📡 9. Communication of Uncertainty

- Always return prediction intervals — never just point forecasts  
- Show horizon-wise interval widening  
- For planning, include narrative overlays (e.g. `/docs/scenarios/`)

---

## 🔐 10. Governance Principles
| Area | Practice |
|------|----------|
| Privacy | **PII flag** blocks cloud burst |
| Overrides | `GoalPressure = Y` ⇒ manager review |
| Lineage | SHA-256 of training snapshot logged |
| Data Ops | Version raw + override data |
| Feedback | Dashboards track accuracy |
| Detection | Monitor level & variance shifts |
---

## ⚠️ 11. Pitfalls Checklist

- [ ] Seasonal-Naïve not beaten  
- [ ] Calendar effects absent  
- [ ] Residual autocorrelation (Ljung-Box p ≤ 0.05)  
- [ ] Fat tails unmodeled in residuals  

---

## 🔧 12. Kernel Extensions

| Horizon     | Modules                                      |
|-------------|----------------------------------------------|
| 0–6 months  | Real-time anomalies, staffing triggers       |
| 6m–2 years  | S&OP scenario generators                     |
| 2y–10 years | Monte-Carlo macro simulators                 |

---
