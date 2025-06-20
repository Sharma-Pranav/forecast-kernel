# Next Steps

This document tracks project phases from the codex and their current status.

## Completed Phases

- **Phase 0 – Environment Initialization**: deterministic setup with `.venv` and dependency lock.
- **Phase 0a – Data Pre‑Flight**: `data_preflight.py` validates inputs; outputs `preflight_report.json`.
- **Phase 1 – Baseline Forecast Generation**: `baseline_sf.py` produces forecasts and metrics.
- **Phase 1b – Aggregation‑Aware CI Descent**: cascade pipeline using `cascade.py` and anchor bias checks.
- **Phase 1c – Feature Registry Stub**: `features.yaml` defines engineered features.
- **Phase 2 – Drift Detection and Error Decomposition**: residual tests and drift alerts via `core/drift.py`.
- **Phase 3 – Audit Hardening**: hash logging and commit tracking with DVC integration.
- **Phase 4 – CI Runtime & Regeneration**: regeneration logic and visual delta audits in `visual_delta_audit.py`.
### Verification Steps

1. `scripts/bootstrap.ps1` created `.venv` and ran a hello check. *(Phase 0)*
2. `python -m forecastkernel.scripts.data_preflight --input data/raw/univariate_example.csv --output preflight_report.json` produced a passing report. *(Phase 0a)*
3. `python -m forecastkernel.scripts.baseline_sf --data data/raw/univariate_example.csv --horizon 14 --tag demo --phase 1` generated `baseline_metrics.json`. *(Phase 1)*
4. `python -m forecastkernel.scripts.cascade --parent_run data/outputs/baseline/demo -- --data data/raw/univariate_example.csv --horizon 14 --tag cascaded` recorded anchor bias. *(Phase 1b)*
5. `python - <<EOF` and `load_features()` displayed registry keys. *(Phase 1c)*
6. `pytest tests/test_drift_decomposition_dm.py -q` passed. *(Phase 2)*
7. `python -m forecastkernel.tests.test_ci_runtime --run_dir data/outputs/baseline/demo --data data/raw/univariate_example.csv` succeeded. *(Phase 3)*
8. `python -m forecastkernel.utils.ci_utils --audit_log data/outputs/baseline/demo/audit_log.json --output_dir data/outputs/baseline/demo` reported matching hashes. *(Phase 3)*
9. `python -m forecastkernel.scripts.baseline_sf --data data/raw/univariate_example.csv --horizon 14 --tag demo --phase 4 --regenerate` and `python -m forecastkernel.scripts.visual_delta_audit --output_path data/outputs/baseline/demo` produced delta plots. *(Phase 4)*


## Planned Features

The following roadmap items remain to be implemented:

- **Phase 2 – Anomaly Overlay with PyOD**: integrate PyOD models and log anomaly flags in MLflow. `[Standalone]`
- **Phase 2b – Back‑Test Grid & Hyper‑Search**: grid search baseline parameters, store results in MLflow. `[Standalone]`
- **Phase 2c – Decision‑Kernel Microservices**: expose `/recommend_qty` and `/voi` endpoints using PFOD formulas. `[Standalone]`
- **Phase 4 – Serve & Visual Audit**: expose forecasts through a FastAPI service and containerize with Docker. `[Standalone]`
- **Phase 4.5 – Scenario Framing Layer**: simulate macro and promo overrides.
- **Phase 4b – Edge Serve Smoke‑Test**: offline container demo using `docker-compose`.
- **Phase 5 – Cloud Burst Training**: run training jobs on EC2 with DVC remote storage. `[Standalone]`
- **Phase 6 – Drift Monitoring**: scheduled drift checks and automatic anomaly logging. `[Standalone]`
- **Phase 6b – Auto‑Retrain Trigger**: cron‑based retraining if drift thresholds are exceeded.
- **Phase 7 – Feature‑Aware Forecasting**: add LightGBM regressors gated by PyOD.
- **Phase 7b – Driver Attribution Audit**: explain anomalies via SHAP and attribution plots.
- **Phase 8 – Foundation Models**: benchmark large pre‑trained models such as TabPFN or TimeGPT. `[Standalone]`
- **Phase 9 – SaaS Layer + FinOps Telemetry**: multi‑tenant serving with usage cost tracking.
- **Phase 10 – Enterprise Audit Layer**: integrate LakeFS and Evidently dashboards for lineage. `[Standalone]`

