# Forecast Kernel

Forecast Kernel is a lightweight sandbox for forecasting experiments. It ships
baseline models, evaluation helpers and simple command line utilities. The code
lives under `src/forecastkernel`:

- `core` – evaluation metrics, drift detection and error decomposition
- `utils` – hashing, logging and git helpers
- `pipelines` – diagnostic plotting utilities
- `models` – placeholder model definitions
- `scripts` – runnable utilities for baseline forecasts and CI checks

Tests reside in `tests/`.

## Quickstart

### 1. Create a Python 3.10 environment

Using `pip`:

```bash
python -m venv .venv
source .venv/bin/activate         # Unix/macOS
.venv\Scripts\Activate.ps1         # Windows
pip install -r requirements.txt
pip install -e .
```

Using [`uv`](https://github.com/astral-sh/uv) for faster installs:

```bash
pip install uv                     # if uv is not installed
uv venv --python=3.10 .venv
source .venv/bin/activate          # or .venv\Scripts\Activate.ps1 on Windows
uv pip install -r requirements.txt
uv pip compile requirements.in -o requirements.txt  # update lock file
pip install -e .
```

### 2. Activate for development

When you start a new shell session, reactivate the environment:

```bash
source .venv/bin/activate          # Unix/macOS
.venv\Scripts\Activate.ps1          # Windows
```

### 3. Verify the installation

Run a quick hello script and the test suite:

```bash
python -m forecastkernel.scripts.hello
pytest
```

### 4. Run the baseline pipeline

The main runner consumes a CSV with columns `ds`, `unique_id` and `y`:

```bash
python -m forecastkernel.scripts.baseline_sf \
  --data data/raw/univariate_example.csv \
  --horizon 14 --tag demo
```

Results are written to `data/outputs/baseline`.

## Data versioning with DVC

Data outputs are tracked with [DVC](https://dvc.org/):

```bash
dvc add data/outputs/baseline
dvc push
```

To use an S3 remote:

```bash
dvc remote add s3remote s3://your-bucket-name
dvc remote default s3remote
dvc push
```

## MLflow UI

Start the experiment tracker locally with:

```bash
mlflow ui --backend-store-uri file:./.mlflow_logs
```

---

This project is intended for experimentation and CI testing only.
