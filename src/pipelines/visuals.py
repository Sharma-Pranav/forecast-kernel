import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def visual_debug(df: pd.DataFrame, forecasts: pd.DataFrame, forecastability: list, forecast_cols: list, output_path: str):
    uid_sample = df["unique_id"].unique()[:2]
    os.makedirs(os.path.join(output_path, "plots"), exist_ok=True)

    for uid in uid_sample:
        df_plot = df[df["unique_id"] == uid]
        plt.figure(figsize=(10, 4))
        plt.plot(df_plot["ds"], df_plot["y"], label="Actual", marker="o")
        for model in forecast_cols:
            fcast = forecasts[forecasts["unique_id"] == uid][["ds", model]]
            plt.plot(fcast["ds"], fcast[model], label=model, linestyle="--")
        plt.title(f"Forecasts for {uid}")
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(output_path, "plots", f"{uid}_forecast.png"))
        plt.close()

    fac_df = pd.DataFrame(forecastability)
    sns.scatterplot(data=fac_df, x="Entropy", y="CV2")
    plt.title("Forecastability Scatter: Entropy vs CV²")
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, "plots", "forecastability_scatter.png"))
    plt.close()
