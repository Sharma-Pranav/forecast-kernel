from pandera.pandas import Column, DataFrameSchema, Check
import pandera as pa  
import pandas as pd

# Define forecast input schema
forecast_input_schema = DataFrameSchema({
    "ds": Column(pa.DateTime),
    "unique_id": Column(pa.String),
    "y": Column(pa.Float, nullable=False),
})