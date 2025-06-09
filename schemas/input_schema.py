import pandera as pa
from pandera import Column, DataFrameSchema, Check
import pandas as pd

# Define forecast input schema
forecast_input_schema = DataFrameSchema({
    "ts": Column(pa.DateTime),
    "unique_id": Column(pa.String),
    "y": Column(pa.Float, nullable=False),
})