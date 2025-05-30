import pandas as pd


def evaluate_forecasts(forecasts: pd.DataFrame, actuals: pd.DataFrame, forecast_cols: list) -> list:
    results = []
    for col in forecast_cols:
        merged = forecasts[["unique_id", "ds", col]].merge(actuals, on=["unique_id", "ds"])
        if not merged.empty:
            y_pred = merged[col]
            y_true = merged["y"]
            mae = abs(y_pred - y_true).mean()
            bias = (y_pred - y_true).mean()
            results.append({
                "model": col,
                "mae": round(mae, 2),
                "bias": round(bias, 2),
                "score": round(mae + abs(bias), 2)
            })
    return sorted(results, key=lambda x: x["score"])
