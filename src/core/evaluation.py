# import pandas as pd


# def evaluate_forecasts(forecasts: pd.DataFrame, actuals: pd.DataFrame, forecast_cols: list) -> list:
#     results = []
#     for col in forecast_cols:
#         merged = forecasts[["unique_id", "ds", col]].merge(actuals, on=["unique_id", "ds"])
#         if not merged.empty:
#             y_pred = merged[col]
#             y_true = merged["y"]
#             mae = abs(y_pred - y_true).mean()
#             bias = (y_pred - y_true).mean()
#             results.append({
#                 "model": col,
#                 "mae": round(mae, 2),
#                 "bias": round(bias, 2),
#                 "score": round(mae + abs(bias), 2)
#             })
#     return sorted(results, key=lambda x: x["score"])
import os
import pandas as pd
from sklearn.metrics import mean_absolute_error

def evaluate_forecasts(forecasts: pd.DataFrame, true_future: pd.DataFrame, forecast_cols: list, output_path: str):
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
