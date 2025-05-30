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
    HistoricAverage, WindowAverage, SeasonalWindowAverage,
    CrostonClassic, CrostonOptimized, CrostonSBA,
    Theta, SimpleExponentialSmoothing, HoltWinters
)

from core.evaluation import evaluate_forecasts
from core.forecastability import compute_forecastability_metrics
from pipelines.visuals import visual_debug

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
args = parser.parse_args()

# ------------------------------
# Setup Run Metadata
# ------------------------------
run_id = args.tag or f"run-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
output_path = os.path.join(args.output_dir, run_id)
os.makedirs(output_path, exist_ok=True)
log_path = os.path.join(output_path, "forecast_run.log")

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
# Model Setup
# ------------------------------
models = [
    Naive(),
    SeasonalNaive(season_length=args.season_length),
    RandomWalkWithDrift(),
    HistoricAverage(),
    WindowAverage(window_size=args.window_size),
    SeasonalWindowAverage(window_size=args.window_size, season_length=args.season_length),
    CrostonClassic(),
    CrostonOptimized(),
    CrostonSBA(),
    Theta(),
    SimpleExponentialSmoothing(alpha=0.2),
    HoltWinters(season_length=args.season_length)
]

sf = StatsForecast(models=models, freq='D', n_jobs=-1)
forecasts = sf.forecast(df=cutoff_df, h=h)

# ------------------------------
# Evaluation + Ensemble
# ------------------------------
ensemble_preds = forecasts.drop(columns=["unique_id", "ds"]).mean(axis=1)
forecasts["EnsembleMean"] = ensemble_preds
forecast_cols = [col for col in forecasts.columns if col not in ["unique_id", "ds"]]

results = evaluate_forecasts(forecasts, true_future, forecast_cols)
log.info("\n" + tabulate(results, headers="keys", tablefmt="github"))

# ------------------------------
# Save Outputs
# ------------------------------
metrics_path = os.path.join(output_path, "baseline_metrics.json")
with open(metrics_path, "w") as f:
    json.dump(results, f, indent=2)
log.info(f"✅ Metrics saved to: {metrics_path}")

forecasts["run_id"] = run_id
forecasts["horizon"] = h
forecasts["n_models"] = len(models)
forecast_file = os.path.join(output_path, "baseline_forecasts.csv")
ordered_cols = ["run_id", "horizon", "n_models", "unique_id", "ds"] + forecast_cols + ["EnsembleMean"]
forecasts = forecasts[ordered_cols]
forecasts.to_csv(forecast_file, index=False)
log.info(f"📄 Forecasts saved to: {forecast_file}")

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
# Forecastability Metrics
# ------------------------------
forecastability = compute_forecastability_metrics(df)
forecastability_path = os.path.join(output_path, "forecastability.json")
with open(forecastability_path, "w") as f:
    json.dump(forecastability, f, indent=2)
log.info(f"🔍 Forecastability metadata saved to: {forecastability_path}")

# ------------------------------
# Visual Debug
# ------------------------------
visual_debug(df, forecasts, forecastability, forecast_cols, output_path)
