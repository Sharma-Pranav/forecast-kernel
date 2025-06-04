"""Break down residual errors into interpretable components."""

import numpy as np
import json
import os

def decompose_errors(residuals_df, forecast_cols):
    """Return bias, variance and noise components for each model.

    Parameters
    ----------
    residuals_df : pandas.DataFrame
        DataFrame of residuals with columns matching ``forecast_cols``.
    forecast_cols : list
        Names of forecast columns to analyse.

    Returns
    -------
    dict
        Mapping of model name to a dictionary of error breakdown statistics.
    """

    breakdown = {}
    for model in forecast_cols:
        resids = residuals_df[model].dropna()
        bias_error = np.mean(resids)
        variance_error = np.var(resids)
        noise = np.mean(np.abs(resids - bias_error))
        seasonality_miss = np.mean(np.abs(resids.diff(7)))

        breakdown[model] = {
            "Bias Error": round(float(bias_error), 4),
            "Variance Error": round(float(variance_error), 4),
            "Noise": round(float(noise), 4),
            "Seasonality Miss": round(float(seasonality_miss), 4)
        }
    return breakdown
