import os
import pandas as pd
from forecastkernel.scripts.data_preflight import run_preflight

def test_preflight_run(tmp_path):
    df = pd.DataFrame({
        "ds": pd.date_range("2024-01-01", periods=3, freq="D"),
        "unique_id": ["A"] * 3,
        "y": [1.0, 2.0, 3.0],
    })
    csv_path = tmp_path / "sample.csv"
    df.to_csv(csv_path, index=False)
    report_path = tmp_path / "report.json"

    report = run_preflight(str(csv_path), str(report_path))

    assert report["pandera_pass"] is True
    assert report["row_count"] == 3
    assert os.path.exists(report_path)
