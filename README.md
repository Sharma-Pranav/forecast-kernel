# Forecast Kernel

This repository contains a small forecasting toolkit used for testing continuous integration pipelines. The `src` directory is organised into logical subpackages:

- **core** – statistical helpers and algorithms such as evaluation utilities, drift detection and error decomposition.
- **utils** – general helpers for hashing, logging and git integration.
- **pipelines** – plotting helpers for diagnostics.
- **models** – placeholder package for forecast model definitions.

Scripts under `scripts/` provide command line entry points for running baseline forecasts, validating hashes and visualising forecast deltas. Tests live in `tests/` and exercise the CI routines.

The project follows a lightweight structure to keep components modular and easy to reuse across experiments.


Activate environment in ubuntu/macos: source .venv/bin/activate
Activate environment in windows (CMD): .venv\Scripts\activate.bat
Activate environment in windows (Powershell): .venv\Scripts\Activate.ps1


# Only once:
C:\Users\topra\AppData\Local\Programs\Python\Python310\python.exe -m venv .venv

# Install dependencies=
# Install Python 3.10 or higher

# if multiple dependiceies exist : 

# Only once:
C:\Users\topra\AppData\Local\Programs\Python\Python310\python.exe -m venv .venv
# Install uv if not present
iwr https://astro.build/install.ps1 -useb | iex
uv venv --python=3.10 .venv
python -m pip install --upgrade pip 
uv pip compile requirements.in -o requirements.txt
uv pip install -r requirements.txt
# Or
pip install -r requirements.txt
pip install -e .
$env:PYTHONPATH="."; pytest tests/test_schema.py

# Only once : 
# 1. Create venv using Python 3.10
C:\Users\topra\AppData\Local\Programs\Python\Python310\python.exe -m venv .venv

# 2. Activate
.venv\Scripts\Activate.ps1

# 3. Install dependencies via UV
uv pip install -r requirements.txt

# 4. Editable install via pip (NOT uv)
pip install -e .

# Each time you want to start work 
# 1. Activate venv
.venv\Scripts\Activate.ps1

# 2. (Optional) Pull latest packages
uv pip install -r requirements.txt

# 3. Re-confirm editable link (if structure changed)
pip install -e .



# Run MLflow UI 

mlflow ui --backend-store-uri file:./.mlflow_logs

# DVC (Data Version Control)
dvc init
dvc add data/outputs/baseline
dvc stage add -n forecast -d data/raw/univariate_example.csv -d src/forecastkernel/scripts/baseline_sf.py -o data/outputs/baseline/baseline_metrics.json -o data/outputs/baseline/baseline_forecasts.csv -o data/outputs/baseline/run_info.json -o data/outputs/baseline/audit_log.json --always-changed python src/forecastkernel/scripts/baseline_sf.py --data data/raw/univariate_example.csv

dvc push

