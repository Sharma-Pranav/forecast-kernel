"""Residual drift detection utilities."""

from scipy.stats import ks_2samp
import pandas as pd

def detect_residual_drift(
    residuals_df: pd.DataFrame, model: str, window_size: int = 14
):
    """Detect distribution shift in residuals using a KS test.

    Parameters
    ----------
    residuals_df : pandas.DataFrame
        DataFrame containing residuals with a ``ds`` column and per-model
        residual columns.
    model : str
        Column name of the residual series to test.
    window_size : int, optional
        Number of recent observations to compare against the prior history.

    Returns
    -------
    dict
        ``{"drift_detected": bool, "p_value": float}`` indicating whether a
        significant shift was detected and the associated p-value.
    """

    residuals_df = residuals_df.sort_values("ds")
    recent = residuals_df[model].iloc[-window_size:]
    past = residuals_df[model].iloc[:-window_size]
    if len(past) < window_size:
        return {"drift_detected": False, "p_value": 1.0}
    
    stat, p = ks_2samp(past, recent)
    return {"drift_detected": p < 0.05, "p_value": round(p, 4)}

