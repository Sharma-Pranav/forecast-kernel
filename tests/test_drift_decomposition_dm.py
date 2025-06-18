import pandas as pd
import numpy as np

from forecastkernel.core.drift import detect_residual_drift
from forecastkernel.core.decomposition import decompose_errors
from forecastkernel.core.dm_test import compute_dm_test


def test_detect_residual_drift_detects_change() -> None:
    df = pd.DataFrame({
        "ds": pd.date_range("2024-01-01", periods=40, freq="D"),
        "model_a": list(np.zeros(26)) + list(np.ones(14) * 5)
    })
    result = detect_residual_drift(df, "model_a", window_size=14)
    assert bool(result["drift_detected"]) is True
    assert 0 <= result["p_value"] < 0.05


def test_detect_residual_drift_insufficient_history() -> None:
    df = pd.DataFrame({
        "ds": pd.date_range("2024-01-01", periods=20, freq="D"),
        "model_a": np.random.randn(20)
    })
    result = detect_residual_drift(df, "model_a", window_size=14)
    assert result == {"drift_detected": False, "p_value": 1.0}


def test_decompose_errors_basic() -> None:
    df = pd.DataFrame({"model_a": range(14)})
    breakdown = decompose_errors(df, ["model_a"])
    expected = {
        "model_a": {
            "Bias Error": 6.5,
            "Variance Error": 16.25,
            "Noise": 3.5,
            "Seasonality Miss": 7.0,
        }
    }
    assert breakdown == expected


def test_compute_dm_test_expected_values() -> None:
    forecasts = pd.DataFrame({
        "model_1": [10, 12, 8],
        "model_2": [9, 11, 10],
    })
    actuals = pd.DataFrame({"y": [10, 10, 10]})
    result = compute_dm_test(forecasts, actuals, "model_1", "model_2")
    assert result["vs"] == "model_2"
    assert abs(result["dm_stat"] - 0.756) < 1e-3
    assert abs(result["p_value"] - 0.529) < 1e-3

