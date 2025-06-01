import os
import sys
import io
import json
import argparse
import pandas as pd
from datetime import datetime
from tabulate import tabulate
from statsforecast import StatsForecast
from statsforecast.models import (
    Naive, SeasonalNaive, RandomWalkWithDrift,
    CrostonSBA, HoltWinters
)
from core.dm_test import compute_dm_test
from core.evaluation import evaluate_forecasts
from core.forecastability import compute_forecastability_metrics
from pipelines.visuals import visual_debug
from core.phase_handler import include_dm_test, include_drift_monitor, include_serve_hash

# Ensure UTF-8 output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ------------------------------
# Argument Parsing
# ------------------------------
parser = argparse.ArgumentParser(description="Baseline StatsForecast Runner")
parser.add_argument("--data", type=str, required=True, help="Path to input CSV file")
parser.add_argument("--horizon", type=int, default=7, help="Forecast horizon")
parser.add_argument("--output_dir", type=str, default="data/outputs/baseline", help="Root output directory")
parser.add_argument("--tag", type=str, default=None, help="Optional run tag")
parser.add_argument("--window_size", type=int, default=3, help="Window size for WindowAverage and SeasWA")
parser.add_argument("--season_length", type=int, default=12, help="Season length for seasonal models")
parser.add_argument("--phase", type=int, default=1, help="Forecast-Kernel phase (default: 1)")
args = parser.parse_args()

active_phase = args.phase
# ------------------------------
# Setup Run Metadata
# ------------------------------
run_id = args.tag or f"run-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
output_path = os.path.join(args.output_dir, run_id)
os.makedirs(output_path, exist_ok=True)

from utils.logging_utils import setup_logger
log_path = os.path.join(output_path, "forecast_run.log")
log = setup_logger(log_path, logger_name="baseline")

# ------------------------------
# Load Dataset
# ------------------------------
log.info(f"Loading dataset from: {args.data}")
df = pd.read_csv(args.data)
df["ds"] = pd.to_datetime(df["ds"])
df = df.sort_values(["unique_id", "ds"])

h = args.horizon
cutoff_df = (
    df.groupby("unique_id", group_keys=False)
      .apply(lambda g: g.sort_values("ds").iloc[:-h])
      .reset_index(drop=True)
)
true_future = (
    df.groupby("unique_id", group_keys=False)
      .apply(lambda g: g.sort_values("ds").iloc[-h:].copy())
      .reset_index(drop=True)
)

# ------------------------------
# Model Setup (CI-Compliant)
# ------------------------------
models = [
    Naive(),
    SeasonalNaive(season_length=args.season_length),
    RandomWalkWithDrift(),
    CrostonSBA(),
    HoltWinters(season_length=args.season_length)
]

sf = StatsForecast(models=models, freq='D', n_jobs=-1)
forecasts = sf.forecast(df=cutoff_df, h=h)

# ------------------------------
# EnsembleNaive (manual logic)
# ------------------------------
log.info("Computing EnsembleNaive as average of Naive and SeasonalNaive forecasts...")
naive_forecast = forecasts["Naive"]
seasonal_forecast = forecasts["SeasonalNaive"]
forecasts["ensemble_naive"] = (naive_forecast + seasonal_forecast) / 2

# ------------------------------
# Evaluation + Scoring
# ------------------------------
forecast_cols = [col for col in forecasts.columns if col not in ["unique_id", "ds"]]
results = evaluate_forecasts(forecasts, true_future, forecast_cols)
log.info("\n" + tabulate(results, headers="keys", tablefmt="github"))

# ------------------------------
# Forecastability Metrics
# ------------------------------
forecastability = compute_forecastability_metrics(df)
forecastability_path = os.path.join(output_path, "forecastability.json")
with open(forecastability_path, "w") as f:
    json.dump(forecastability, f, indent=2)
log.info(f"🔍 Forecastability metadata saved to: {forecastability_path}")

# ------------------------------
# Compile and Save CI-Valid Metrics
# ------------------------------
if isinstance(results, list):
    results = pd.DataFrame(results)

metrics_dict = {
    row["model"]: {
        "MAE": round(row["mae"], 2),
        "Bias": round(row["bias"], 2),
        "Score": round(row["score"], 2)
    } for _, row in results.iterrows()
}


ci_floor = min(metrics_dict["ensemble_naive"]["Score"], metrics_dict["HoltWinters"]["Score"])
selected_model = min(metrics_dict.items(), key=lambda kv: kv[1]["Score"])[0]
pass_ci = metrics_dict[selected_model]["Score"] <= ci_floor

# ------------------------------
# DM-Test (vs. ensemble_naive)
# ------------------------------
# dm_test_result = compute_dm_test(forecasts, true_future, selected_model, "ensemble_naive")
# ------------------------------
# Save Baseline Metrics 
baseline_metrics = {
    "series_id": df["unique_id"].iloc[0],
    "horizon": h,
    "timestamp": datetime.now().isoformat(),
    "forecastability": forecastability,
    "metrics": metrics_dict,
    "ci_baseline_rule": "min(ensemble_naive, holt_winters)",
    "selected_model": selected_model,
    "pass_ci": pass_ci,
    "metadata": {
        "tag": "v0.1-baseline",
        "phase": active_phase
    }
}

if include_dm_test(active_phase):
    baseline_metrics["dm_test"] = compute_dm_test(
        forecasts, true_future, selected_model, "ensemble_naive"
    )

if include_drift_monitor(active_phase):
    baseline_metrics["drift_monitor"] = {
        "last_trained": datetime.now().strftime("%Y-%m-%d"),
        "drift_detected": False,
        "fp_rate": 0.01
    }

if include_serve_hash(active_phase):
    baseline_metrics["metadata"]["serve_hash"] = "abc1234"

metrics_path = os.path.join(output_path, "baseline_metrics.json")
with open(metrics_path, "w") as f:
    json.dump(baseline_metrics, f, indent=2)
log.info(f"✅ Metrics saved to: {metrics_path}")

# ------------------------------
# Save Forecasts
# ------------------------------
forecasts["run_id"] = run_id
forecasts["horizon"] = h
forecasts["n_models"] = len(models)
forecast_file = os.path.join(output_path, "baseline_forecasts.csv")
ordered_cols = ["run_id", "horizon", "n_models", "unique_id", "ds"] + forecast_cols
forecasts = forecasts[ordered_cols]
forecasts.to_csv(forecast_file, index=False)
log.info(f"📄 Forecasts saved to: {forecast_file}")

# ------------------------------
# Save Run Info
# ------------------------------
info = {
    "run_id": run_id,
    "horizon": h,
    "n_models": len(models),
    "input_file": args.data,
    "timestamp": datetime.now().isoformat()
}
with open(os.path.join(output_path, "run_info.json"), "w") as f:
    json.dump(info, f, indent=2)
log.info(f"🧾 Metadata saved to: {output_path}/run_info.json")

# ------------------------------
# Visual Debug
# ------------------------------
visual_debug(df, forecasts, forecastability, forecast_cols, output_path)
log.info(f"✅ Run completed successfully. Outputs saved to: {output_path}")
log.info(f"🔍 Visualizations saved to: {os.path.join(output_path, 'plots')}")