"""CLI for generating delta plots comparing forecast versions."""

import os
import argparse
import pandas as pd
import json
from pipelines.visuals import plot_forecast_deltas

parser = argparse.ArgumentParser(description="Visual Delta Audit for Forecast Regeneration")
parser.add_argument("--output_path", type=str, required=True, help="Path to output directory with regenerated forecasts")
parser.add_argument("--original_forecasts", type=str, default=None, help="Optional: path to original forecasts CSV")
args = parser.parse_args()

baseline_path = os.path.join(args.output_path, "baseline_metrics.json")
forecasts_path = args.original_forecasts or os.path.join(args.output_path, "baseline_forecasts.csv")
regen_path = forecasts_path  # both default to same if original not provided

# Load
with open(baseline_path) as f:
    baseline = json.load(f)

true_df = pd.read_csv(baseline.get("input_file", "data/raw/univariate_example.csv"))
true_df["ds"] = pd.to_datetime(true_df["ds"])

original_forecasts = pd.read_csv(forecasts_path)
regenerated_forecasts = pd.read_csv(regen_path)

original_forecasts["ds"] = pd.to_datetime(original_forecasts["ds"])
regenerated_forecasts["ds"] = pd.to_datetime(regenerated_forecasts["ds"])

forecast_cols = [col for col in regenerated_forecasts.columns if col not in ["unique_id", "ds", "run_id", "horizon", "n_models"]]

drift_scores = {
    model: baseline["metrics"][model]["Score"] - baseline["metrics"]["ensemble_naive"]["Score"]
    for model in forecast_cols if model in baseline["metrics"]
}

# Plot
plot_forecast_deltas(
    true_df=true_df,
    original_forecasts=original_forecasts,
    regenerated_forecasts=regenerated_forecasts,
    drift_scores=drift_scores,
    forecast_cols=forecast_cols,
    output_path=args.output_path
)
print(f"Visual delta audit completed. Results saved to {args.output_path}")
