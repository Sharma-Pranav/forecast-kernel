import os
import json
import argparse
import pandas as pd
from datetime import datetime
from core.evaluation import evaluate_forecasts
from utils.hash_utils import compute_file_hash

# ------------------------------
# Argument Parsing
# ------------------------------
parser = argparse.ArgumentParser(description="CI Runtime Drift Validator")
parser.add_argument("--run_dir", type=str, default="data/outputs/baseline/demo", help="Path to run output directory")
parser.add_argument("--data", type=str, default="data/raw/univariate_example.csv", help="Path to raw input CSV")
args = parser.parse_args()

# ------------------------------
# Load Baseline Artifacts
# ------------------------------
METRICS_PATH = os.path.join(args.run_dir, "baseline_metrics.json")
FORECASTS_PATH = os.path.join(args.run_dir, "baseline_forecasts.csv")

with open(METRICS_PATH) as f:
    baseline = json.load(f)

forecasts = pd.read_csv(FORECASTS_PATH)
true_df = pd.read_csv(args.data)
true_df["ds"] = pd.to_datetime(true_df["ds"])
true_df = true_df.sort_values(["unique_id", "ds"])

# ------------------------------
# Forecast Evaluation
# ------------------------------
h = baseline["horizon"]

# Suppress deprecation warnings by excluding grouping columns
cutoff_df = (
    true_df.groupby("unique_id", group_keys=False)
    .apply(lambda g: g.sort_values("ds").iloc[:-h], include_groups=False)
    .reset_index(drop=True)
)
true_future = (
    true_df.groupby("unique_id", group_keys=False)
    .apply(lambda g: g.sort_values("ds").iloc[-h:], include_groups=False)
    .reset_index(drop=True)
)

forecast_cols = [col for col in forecasts.columns if col not in ["unique_id", "ds", "run_id", "horizon", "n_models"]]

forecasts["ds"] = pd.to_datetime(forecasts["ds"])
true_future["ds"] = pd.to_datetime(true_future["ds"])

# Ensure unique_id exists in true_future
if "unique_id" not in true_future.columns:
    true_future["unique_id"] = forecasts["unique_id"].unique()[0]


results, _ = evaluate_forecasts(forecasts, true_future, forecast_cols, output_path=args.run_dir)

# ------------------------------
# CI Comparison Logic
# ------------------------------
score_drift = {
    row["model"]: round(row["score"] - baseline["metrics"][row["model"]]["Score"], 4)
    for _, row in results.iterrows()
    if row["model"] in baseline["metrics"]
}

hash_now = compute_file_hash(METRICS_PATH)
hash_match = hash_now == compute_file_hash(METRICS_PATH)

ci_result = {
    "run_id": baseline.get("series_id"),
    "timestamp": datetime.now().isoformat(),
    "passed": all(abs(v) < 0.1 for v in score_drift.values()),
    "hash_match": hash_match,
    "score_drift": score_drift
}

# Save results
with open(os.path.join(args.run_dir, "ci_results.json"), "w") as f:
    json.dump(ci_result, f, indent=2)

print(json.dumps(ci_result, indent=2))
