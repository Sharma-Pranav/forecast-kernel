"""Plotting utilities for visual diagnostics and drift checks."""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def visual_debug(
    df: pd.DataFrame,
    forecasts: pd.DataFrame,
    forecastability: dict,
    forecast_cols: list,
    output_path: str,
    residuals_df: pd.DataFrame = None,
):
    """Generate a suite of diagnostic plots for a forecast run.

    Parameters
    ----------
    df : pandas.DataFrame
        Original time series data.
    forecasts : pandas.DataFrame
        Forecast results for each model.
    forecastability : dict
        Metrics describing overall forecastability.
    forecast_cols : list
        Names of forecast columns to visualise.
    output_path : str
        Directory where plots will be written.
    residuals_df : pandas.DataFrame, optional
        Residuals for each model, used for drift diagnostics.

    Returns
    -------
    None
    """

    plots_dir = os.path.join(output_path, "plots")
    os.makedirs(plots_dir, exist_ok=True)

    forecast_dir = os.path.join(plots_dir, "forecasts")
    forecastability_dir = os.path.join(plots_dir, "forecastability")
    residuals_dir = os.path.join(plots_dir, "residuals")

    os.makedirs(forecast_dir, exist_ok=True)
    os.makedirs(forecastability_dir, exist_ok=True)
    os.makedirs(residuals_dir, exist_ok=True)

    # Forecasts
    uid_sample = df["unique_id"].unique()[:2]
    for uid in uid_sample:
        df_plot = df[df["unique_id"] == uid]
        plt.figure(figsize=(14, 6))
        plt.plot(df_plot["ds"], df_plot["y"], label="Actual", marker="o")
        for model in forecast_cols:
            fcast = forecasts[forecasts["unique_id"] == uid][["ds", model]]
            plt.plot(fcast["ds"], fcast[model], label=model, linestyle="--")
        plt.title(f"Forecasts for {uid}")
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(forecast_dir, f"{uid}_forecast.png"))
        plt.close()

    # Forecastability Scatter
    fac_df = pd.DataFrame([forecastability])
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=fac_df, x="SpectralEntropy", y="CV2")
    plt.title("Forecastability Scatter: Entropy vs CV²")
    plt.tight_layout()
    plt.savefig(os.path.join(forecastability_dir, "forecastability_scatter.png"))
    plt.close()

    # Residual Visuals
    if residuals_df is not None:
        for model in forecast_cols:
            resids = residuals_df[[model, "ds"]].dropna().sort_values("ds")
            plt.figure(figsize=(12, 4))
            plt.plot(resids["ds"], resids[model], label="Residuals")
            plt.axhline(0, linestyle="--", color="gray")
            plt.title(f"Residual Time Series - {model}")
            plt.tight_layout()
            plt.savefig(os.path.join(residuals_dir, f"{model}_residuals.png"))
            plt.close()

            if len(resids) > 28:
                recent = resids[model].iloc[-14:]
                prior = resids[model].iloc[:-14]
                plt.figure(figsize=(8, 4))
                sns.histplot(prior, kde=True, label="Prior", color="blue", alpha=0.6)
                sns.histplot(recent, kde=True, label="Recent", color="red", alpha=0.6)
                plt.title(f"Residual Histogram Comparison - {model}")
                plt.legend()
                plt.tight_layout()
                plt.savefig(os.path.join(residuals_dir, f"{model}_resid_hist.png"))
                plt.close()


def plot_residual_drift(
    residuals_df: pd.DataFrame, model: str, output_path: str, window: int = 30
):
    """Plot residuals over time for a selected model.

    Parameters
    ----------
    residuals_df : pandas.DataFrame
        DataFrame containing residuals with ``ds`` and model columns.
    model : str
        Name of the model column to plot.
    output_path : str
        Directory for saving the plot.
    window : int, optional
        Smoothing window for highlight (unused currently).

    Returns
    -------
    None
    """
    df_plot = residuals_df[["ds", "unique_id", model]].copy()
    df_plot = df_plot.sort_values(["unique_id", "ds"])

    os.makedirs(os.path.join(output_path, "drift"), exist_ok=True)

    for uid in df_plot["unique_id"].unique():
        series = df_plot[df_plot["unique_id"] == uid]
        plt.figure(figsize=(14, 6))
        plt.plot(series["ds"], series[model], label="Residuals", marker="o")
        plt.axhline(0, color="black", linestyle="--", linewidth=0.8)
        plt.title(f"Residuals Over Time - {uid}")
        plt.tight_layout()
        plt.savefig(os.path.join(output_path, "drift", f"{uid}_residuals.png"))
        plt.close()

def plot_residual_histograms(
    residuals_df: pd.DataFrame, model: str, output_path: str, window: int = 30
):
    """Compare distribution of past and recent residuals.

    Parameters
    ----------
    residuals_df : pandas.DataFrame
        Residual data for a single model.
    model : str
        Column name of the residuals to compare.
    output_path : str
        Directory for saving the plot.
    window : int, optional
        Number of recent observations to treat as "recent".

    Returns
    -------
    None
    """
    residuals_df = residuals_df.sort_values("ds")
    recent = residuals_df[model].iloc[-window:]
    past = residuals_df[model].iloc[:-window]

    plt.figure(figsize=(14, 6))
    sns.histplot(past, label="Past", color="gray", kde=True)
    sns.histplot(recent, label="Recent", color="orange", kde=True)
    plt.legend()
    plt.title(f"Residual Distribution Shift - {model}")
    plt.tight_layout()
    drift_dir = os.path.join(output_path, "drift")
    os.makedirs(drift_dir, exist_ok=True)
    plt.savefig(os.path.join(drift_dir, f"{model}_residual_histogram.png"))
    plt.close()


def plot_forecast_deltas(
    true_df,
    original_forecasts,
    regenerated_forecasts,
    drift_scores,
    forecast_cols,
    output_path,
):
    """Visualise differences between original and regenerated forecasts.

    Parameters
    ----------
    true_df : pandas.DataFrame
        Actual observations for the forecast period.
    original_forecasts : pandas.DataFrame
        Forecasts from the original run.
    regenerated_forecasts : pandas.DataFrame
        Newly generated forecasts to compare.
    drift_scores : dict
        Mapping of model name to drift score.
    forecast_cols : list
        Names of forecast columns to visualise.
    output_path : str
        Base directory for saving comparison plots.

    Returns
    -------
    None
    """
    delta_path = os.path.join(output_path, "plots", "delta_audit")
    os.makedirs(delta_path, exist_ok=True)

    sample_ids = true_df["unique_id"].unique()[:3]

    for uid in sample_ids:
        actual = true_df[true_df["unique_id"] == uid].sort_values("ds")
        orig = original_forecasts[original_forecasts["unique_id"] == uid].sort_values("ds")
        regen = regenerated_forecasts[regenerated_forecasts["unique_id"] == uid].sort_values("ds")

        for model in forecast_cols:
            if model not in orig.columns or model not in regen.columns:
                continue

            plt.figure(figsize=(12, 6))
            plt.plot(actual["ds"], actual["y"], label="Actual", color="black", linewidth=1.5)
            plt.plot(orig["ds"], orig[model], label="Original", linestyle="--", color="blue")
            plt.plot(regen["ds"], regen[model], label="Regenerated", linestyle=":", color="red")
            drift_val = drift_scores.get(model, 0.0)
            plt.title(f"{uid} | {model} Drift: {drift_val:+.2%}")
            plt.legend()
            plt.tight_layout()
            fname = f"{uid}_{model}_delta.png"
            plt.savefig(os.path.join(delta_path, fname))
            plt.close()

