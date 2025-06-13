"""Aggregation helpers for cascade enforcement and anchor bias."""

from __future__ import annotations

import json
import os
import pandas as pd


def compute_anchor_bias(
    atomic_forecasts: pd.DataFrame,
    anchor_forecasts: pd.DataFrame,
    model: str,
) -> pd.Series:
    """Return the bias between atomic and aggregate forecasts.

    Parameters
    ----------
    atomic_forecasts : pandas.DataFrame
        Forecasts at the granular level containing ``unique_id`` and ``ds``.
    anchor_forecasts : pandas.DataFrame
        Forecasts from the upstream aggregation level with the same columns.
    model : str
        Column name of the forecast to compare.

    Returns
    -------
    pandas.Series
        Series of ``atomic_forecast - aggregate_forecast`` aligned on
        ``unique_id`` and ``ds``.
    """
    atomic = atomic_forecasts[["unique_id", "ds", model]].copy()
    anchor = anchor_forecasts[["unique_id", "ds", model]].copy()

    joined = atomic.merge(anchor, on=["unique_id", "ds"], how="left", suffixes=("", "_anchor"))
    if joined[f"{model}_anchor"].isna().any():
        raise ValueError("Anchor forecasts missing for some timestamps.")

    return joined[model] - joined[f"{model}_anchor"]


def enforce_cascade_checks(parent_dir: str) -> None:
    """Validate upstream run before cascading to a granular level.

    Parameters
    ----------
    parent_dir : str
        Directory containing the upstream run outputs.

    Raises
    ------
    ValueError
        If any cascade criterion is violated.
    """
    metrics_path = os.path.join(parent_dir, "baseline_metrics.json")
    if not os.path.exists(metrics_path):
        raise FileNotFoundError("Missing baseline_metrics.json in parent run.")
    with open(metrics_path, "r") as f:
        parent_metrics = json.load(f)

    if not parent_metrics.get("pass_ci", False):
        raise ValueError("❌ Upstream CI failed. Cascade blocked.")

    drift = parent_metrics.get("drift_monitor", {})
    if drift.get("drift_detected", False):
        raise ValueError("❌ Drift unresolved in parent run. Cascade blocked.")

    forecast_path = os.path.join(parent_dir, "baseline_forecasts.csv")
    if not os.path.exists(forecast_path):
        raise FileNotFoundError("Missing anchor forecasts for cascade.")

