import json
import pandas as pd
import pytest
from forecastkernel.core.aggregation import compute_anchor_bias, enforce_cascade_checks

def test_compute_anchor_bias() -> None:
    atomic = pd.DataFrame({
        "unique_id": ["A"],
        "ds": [pd.Timestamp("2023-01-01")],
        "model_a": [12.0],
    })
    anchor = pd.DataFrame({
        "unique_id": ["A"],
        "ds": [pd.Timestamp("2023-01-01")],
        "model_a": [10.0],
    })
    bias = compute_anchor_bias(atomic, anchor, "model_a")
    assert bias.iloc[0] == 2.0


def test_enforce_cascade_checks(tmp_path) -> None:
    parent = tmp_path / "parent"
    parent.mkdir()
    metrics = {
        "pass_ci": True,
        "drift_monitor": {"drift_detected": False}
    }
    (parent / "baseline_forecasts.csv").write_text("unique_id,ds,model_a\nA,2023-01-01,1\n")
    with open(parent / "baseline_metrics.json", "w") as f:
        json.dump(metrics, f)

    # Should not raise
    enforce_cascade_checks(str(parent))
