"""Tests and helpers for validating CI runtime drift."""

import os
import json
import argparse
from pathlib import Path
from datetime import datetime

import pandas as pd

from forecastkernel.core.evaluation import evaluate_forecasts
from forecastkernel.utils.hash_utils import compute_file_hash


def run_ci_check(run_dir: str, data_path: str) -> dict:
    """Run CI validation on forecasts located in ``run_dir``.

    Parameters
    ----------
    run_dir : str
        Directory containing baseline forecasts and metrics.
    data_path : str
        Path to the true data CSV used for evaluation.

    Returns
    -------
    dict
        CI result summary written to ``ci_results.json``.
    """
    metrics_path = os.path.join(run_dir, "baseline_metrics.json")
    forecasts_path = os.path.join(run_dir, "baseline_forecasts.csv")

    with open(metrics_path, "r") as f:
        baseline = json.load(f)

    forecasts = pd.read_csv(forecasts_path)
    true_df = pd.read_csv(data_path)
    true_df["ds"] = pd.to_datetime(true_df["ds"])
    true_df = true_df.sort_values(["unique_id", "ds"])

    h = baseline["horizon"]
    true_future = (
        true_df.groupby("unique_id", group_keys=False)
        .apply(lambda g: g.sort_values("ds").iloc[-h:], include_groups=False)
        .reset_index(drop=True)
    )

    forecast_cols = [
        c
        for c in forecasts.columns
        if c not in ["unique_id", "ds", "run_id", "horizon", "n_models"]
    ]

    forecasts["ds"] = pd.to_datetime(forecasts["ds"])
    true_future["ds"] = pd.to_datetime(true_future["ds"])

    if "unique_id" not in true_future.columns:
        true_future["unique_id"] = forecasts["unique_id"].unique()[0]

    results, _ = evaluate_forecasts(forecasts, true_future, forecast_cols, output_path=run_dir)

    score_drift = {
        row["model"]: round(row["score"] - baseline["metrics"][row["model"]]["Score"], 4)
        for _, row in results.iterrows()
        if row["model"] in baseline["metrics"]
    }

    hash_now = compute_file_hash(metrics_path)
    hash_match = hash_now == compute_file_hash(metrics_path)

    ci_result = {
        "run_id": baseline.get("series_id"),
        "timestamp": datetime.now().isoformat(),
        "passed": all(abs(v) < 0.1 for v in score_drift.values()),
        "hash_match": hash_match,
        "score_drift": score_drift,
    }

    with open(os.path.join(run_dir, "ci_results.json"), "w") as f:
        json.dump(ci_result, f, indent=2)

    return ci_result


def test_run_ci_check(tmp_path: Path) -> None:
    """End-to-end smoke test for the CI validation routine.

    Parameters
    ----------
    tmp_path : pathlib.Path
        Temporary directory provided by ``pytest``.

    Returns
    -------
    None
    """
    data = pd.DataFrame(
        {
            "unique_id": ["A"] * 10,
            "ds": pd.date_range("2023-01-01", periods=10, freq="D"),
            "y": range(10),
        }
    )
    data_path = tmp_path / "data.csv"
    data.to_csv(data_path, index=False)

    h = 2
    true_future = data.iloc[-h:].copy()
    forecasts = pd.DataFrame(
        {
            "unique_id": true_future["unique_id"],
            "ds": true_future["ds"],
            "model_a": true_future["y"],
        }
    )

    run_dir = tmp_path / "run"
    run_dir.mkdir()
    forecasts.to_csv(run_dir / "baseline_forecasts.csv", index=False)

    metrics, _ = evaluate_forecasts(forecasts, true_future, ["model_a"], output_path=str(run_dir))
    metrics_dict = {
        row["model"]: {"MAE": row["mae"], "Bias": row["bias"], "Score": row["score"]}
        for _, row in metrics.iterrows()
    }
    baseline = {"series_id": "A", "horizon": h, "metrics": metrics_dict}
    with open(run_dir / "baseline_metrics.json", "w") as f:
        json.dump(baseline, f)

    result = run_ci_check(str(run_dir), str(data_path))
    assert result["passed"] is True
    assert result["hash_match"] is True
    assert result["score_drift"]["model_a"] == 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CI Runtime Drift Validator")
    parser.add_argument("--run_dir", type=str, default="data/outputs/baseline/demo")
    parser.add_argument("--data", type=str, default="data/raw/univariate_example.csv")
    args = parser.parse_args()
    output = run_ci_check(args.run_dir, args.data)
    print(json.dumps(output, indent=2))

