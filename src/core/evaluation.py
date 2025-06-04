"""Utilities for evaluating forecast accuracy and residuals."""

import os
import pandas as pd
from sklearn.metrics import mean_absolute_error

def evaluate_forecasts(
    forecasts: pd.DataFrame,
    true_future: pd.DataFrame,
    forecast_cols: list[str],
    output_path: str,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Compute MAE, bias and residuals for multiple forecast columns.

    Parameters
    ----------
    forecasts : pandas.DataFrame
        Forecast output for each model with ``unique_id`` and ``ds`` columns.
    true_future : pandas.DataFrame
        Actual observations to compare against.
    forecast_cols : list
        Names of columns in ``forecasts`` corresponding to model predictions.
    output_path : str
        Directory where intermediate outputs may be saved (unused).

    Returns
    -------
    tuple[pandas.DataFrame, pandas.DataFrame]
        A DataFrame of metrics per model and a DataFrame of residuals.
    """

    metrics = []
    residuals = []

    for model in forecast_cols:
        joined = forecasts[["unique_id", "ds", model]].merge(
            true_future, on=["unique_id", "ds"], how="left", suffixes=("", "_true")
        )

        y_true = joined["y"]
        y_pred = joined[model]
        mae = mean_absolute_error(y_true, y_pred)
        bias = (y_true - y_pred).mean()
        score = mae + abs(bias)

        metrics.append({
            "model": model,
            "mae": mae,
            "bias": bias,
            "score": score
        })

        residual_df = joined[["unique_id", "ds"]].copy()
        residual_df[model] = y_true - y_pred
        residuals.append(residual_df)

    residuals_df = pd.concat(residuals, axis=0).groupby(["unique_id", "ds"], as_index=False).first()
    return pd.DataFrame(metrics), residuals_df
