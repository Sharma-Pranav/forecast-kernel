import pandas as pd
import pytest
from forecastkernel.schemas.input_schema import forecast_input_schema
import pandera as pa
def test_valid_input_passes():
    df = pd.DataFrame({
        "ds": ["2025-01-01", "2025-01-02"],
        "unique_id": ["A", "A"],
        "y": [10.0, 12.0]
    })
    df["ds"] = pd.to_datetime(df["ds"])
    forecast_input_schema.validate(df)

def test_missing_column_fails():
    df = pd.DataFrame({
        "unique_id": ["A", "A"],
        "y": [10.0, 12.0]
    })
    with pytest.raises(pa.errors.SchemaError):
        forecast_input_schema.validate(df)
