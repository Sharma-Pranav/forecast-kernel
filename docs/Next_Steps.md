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

## Planned Features

The following roadmap items remain to be implemented:

- **Phase 2 – Anomaly Overlay with PyOD**: integrate PyOD models and log anomaly flags in MLflow. `[Standalone]`
- **Phase 2b – Decision‑Kernel Microservices**: expose `/recommend_qty` and `/voi` endpoints using PFOD formulas. `[Standalone]`
- **Phase 2c – Back‑Test Grid & Hyper‑Search**: grid search baseline parameters, store results in MLflow. `[Standalone]`
- **Phase 4 – Serve & Visual Audit**: expose forecasts through a FastAPI service and containerize with Docker. `[Standalone]`
- **Phase 4b – Edge Serve Smoke‑Test**: offline container demo using `docker-compose`.
- **Phase 5 – Cloud Burst Training**: run training jobs on EC2 with DVC remote storage. `[Standalone]`
- **Phase 6 – Drift Monitoring**: scheduled drift checks and automatic anomaly logging. `[Standalone]`
- **Phase 6b – Auto‑Retrain Trigger**: cron‑based retraining if drift thresholds are exceeded.
- **Phase 7 – Feature‑Aware Forecasting**: add LightGBM regressors gated by PyOD.
- **Phase 7b – Driver Attribution Audit**: explain anomalies via SHAP and attribution plots.
- **Phase 8 – Foundation Models**: benchmark large pre‑trained models such as TabPFN or TimeGPT. `[Standalone]`
- **Phase 9 – SaaS Layer**: multi‑tenant serving with billing via Stripe.
- **Phase 9b – FinOps Telemetry**: track cloud costs for each job.
- **Phase 10 – Enterprise Audit Layer**: integrate LakeFS and Evidently dashboards for lineage. `[Standalone]`

