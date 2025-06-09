# 🗭 Forecast-GPT Codex — Forecast-Kernel v∞ (Aggregation Layer Enhanced)

**Author**: Pranav Sharma

---

## 🌌 Strategic Intent

Design a sovereign, scalable, and cost-conscious forecasting system that runs locally or in the cloud, with ≤12 tools, reproducible logic, **structure-aware aggregation descent**, and phase-gated CI.

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
**Models**: Naive, SeasonalNaive, Drift, Holt-Winters, Croston, ensemble\_naive
**CI Rule**: Model must beat `min(ensemble_naive, holt_winters)` on Score
**Kill If**: MAPE gain < 5% vs naive
**Benefit**: Reliable control-arm for all future models

### 🔹 Phase 1b — Aggregation-Aware CI Descent

**Goal**: Cascade forecasts from stable aggregates (L1: Dept-Month) to granular series (L4: SKU-Store-Day) based on CI pass, drift stability, and anchor validation.
**Pass If**:

* `baseline_metrics.json` shows `pass_ci: true` for L1
* L2 inherits drift monitor and passes CI
* Anchor bias is logged for L3/L4

**Reject If**:

* CI fails at any upstream level
* Anchor forecast not logged in `error_breakdown.json`

**Benefit**: Reduces ops cost, ensures audit integrity, stabilizes atomic forecasts.

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

...

## 4. Metrics Logic

* `MAE`: Absolute error magnitude
* `Bias`: Signed average error
* `Score = MAE + |Bias|` → primary KPI across Phases 1, 7, and 8
* **CI Rule**: `Score <= min(ensemble_naive, holt_winters)`
* **Anchor Rule**: `anchor_bias = atomic_forecast - aggregate_forecast` → Required for L3/L4 activation and logged in `error_breakdown.json`

...

## 9. Knowledge Layer — Embedded Forecasting Principles

### 📌 Aggregation & Granularity

* Match forecast granularity to decision-making granularity
* Start at highest-forecastability level (lowest entropy)
* Cascade downward only after upstream CI pass and anchor registration
* Forecast Class Mapping:

  * L1/L2 → Holt-Winters, SES
  * L3/L4 → Croston (SBA/Opt), Intermittent-specific

---

## Appendix: Aggregation Protocol

See `docs/aggregation_protocol.md` for:

* CI descent logic
* Rejection rules
* Anchor formula
* Fail-safe thresholds

Version: `aggregation-v1`

---
