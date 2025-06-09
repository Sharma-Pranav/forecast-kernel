import pandas as pd
import pytest
from schemas.input_schema import forecast_input_schema

def test_valid_input_passes():
    df = pd.DataFrame({
        "ts": ["2025-01-01", "2025-01-02"],
        "unique_id": ["A", "A"],
        "y": [10.0, 12.0]
    })
    df["ts"] = pd.to_datetime(df["ts"])
    forecast_input_schema.validate(df)

def test_missing_column_fails():
    df = pd.DataFrame({
        "unique_id": ["A", "A"],
        "y": [10.0, 12.0]
    })
    with pytest.raises(pa.errors.SchemaError):
        forecast_input_schema.validate(df)
