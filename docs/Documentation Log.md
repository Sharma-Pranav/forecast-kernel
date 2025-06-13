# Forecast Kernel: Phase 0 to 4 Breakdown

## Overview

This document captures the step-by-step progression of building and validating a CI-compliant forecasting pipeline using the Forecast-Kernel structure. It spans phases 0 to 4 with full file mapping, purposes, and logic rationale.

---

## Phase 0: Environment Initialization

**Goal:** Prepare deterministic environment for forecasting pipeline.

### Key Actions

* Set up virtual environment (`.venv`) and dependencies.
* Directory scaffolding:

  * `data/raw/` — input files
  * `data/outputs/` — model outputs
  * `scripts/`, `src/core/`, `tests/` — logic, pipelines, tests

### Key Files

* `pyproject.toml` — dependency management
* `README.md` — project overview and usage

---

## Phase 0a: Data Pre-Flight

**Goal:** Validate raw inputs for schema drift before running models.

### Key Actions

* Added `data_preflight.py` using DuckDB and Pandera for validation.
* Runs optional Great Expectations checks when available.
* Produces a `preflight_report.json` summarising pass/fail.

### Key Files

* `scripts/data_preflight.py`
* `preflight_report.json`

---

## Phase 1: Baseline Forecast Generation

**Goal:** Build deterministic forecasts with clear scoring and evaluation.

### Key Actions

* Implemented `baseline_sf.py` to train and score:

  * Models: Naive, SeasonalNaive, RWD, CrostonSBA, HoltWinters
  * Ensemble logic: `ensemble_naive = avg(Naive, SeasonalNaive)`
* Evaluation metrics: MAE, Bias, Score
* Saved outputs: forecasts, metrics, info

### Key Files

* `scripts/baseline_sf.py`
* `core/evaluation.py`, `core/forecastability.py`
* Outputs:

  * `baseline_forecasts.csv`
  * `baseline_metrics.json`
  * `run_info.json`

---

## Phase 2: Drift Detection and Error Decomposition

**Goal:** Monitor model stability over time.

### Key Actions

* Residual audit via KS test
* Drift alert logging + visual plots
* Error decomposition into bias, variance, noise

### Key Files

* `core/drift.py`, `core/decomposition.py`
* `visuals.py` with residual visualizations
* Outputs:

  * `drift_monitor.json`
  * `error_breakdown.json`

---

## Phase 3: Audit Hardening

**Goal:** Establish audit-grade traceability for CI.

### Key Actions

* SHA-256 hashing of key files
* Git commit tracking
* Metadata expansion in `baseline_metrics.json`
* Hash mismatch alerts

### Key Files

* `utils/hash_utils.py`
* `utils/git_utils.py`
* `utils/ci_utils.py` (hash check logic)
* Outputs:

  * `audit_log.json`

---

## Phase 4: CI Runtime & Regeneration

**Goal:** Ensure re-executability and CI drift tolerance.

### Key Actions

* `--regenerate` flag for fast inference
* CI test harness to recompute and compare metrics
* Forecast hash parity + optional fail conditions
* Visual delta audit (before vs after plots)

### Key Files

* `tests/test_ci_runtime.py`
* `scripts/visual_delta_audit.py`
* `ci_utils.py` (result logging)
* Outputs:

  * `ci_results.json`
  * Delta plots in `plots/delta_audit/`

---

## Final Prompt to Run Full CI Pipeline

```bash
# Regenerate forecasts
python scripts/baseline_sf.py --data data/raw/univariate_example.csv --horizon 14 --tag demo --phase 4 --regenerate

# Run CI test harness
python tests/test_ci_runtime.py --run_dir data/outputs/baseline/demo --data data/raw/univariate_example.csv

# Validate audit hashes
python src/utils/ci_utils.py --audit_log data/outputs/baseline/demo/audit_log.json --output_dir data/outputs/baseline/demo --log_ci_results

# Delta visual audit
python scripts/visual_delta_audit.py --output_path data/outputs/baseline/demo
```

---

## Outcome

You now have a fully auditable, CI-compliant, and reproducible forecasting system with full pipeline integrity from training to audit to regeneration.
