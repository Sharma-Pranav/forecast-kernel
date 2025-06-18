# Forecast-Kernel CLI Reference

This short guide describes the main command line utilities included in the repository.

## baseline_sf.py
Runs the StatsForecast baseline pipeline and writes metrics and plots.

```bash
python -m forecastkernel.scripts.baseline_sf \
  --data path/to/input.csv \
  --horizon 14 --tag demo
```

See `--help` for all options including `--regenerate` to reuse existing forecasts.

## cascade.py
Validates a parent run then launches `baseline_sf` with its forecasts as the anchor.

```bash
python -m forecastkernel.scripts.cascade \
  --parent_run data/outputs/baseline/parent -- \
  --data path/to/new.csv
```

## data_preflight.py
Performs schema and optional Great Expectations checks on raw data.

```bash
python -m forecastkernel.scripts.data_preflight \
  --input path/to/raw.csv \
  --output preflight_report.json
```

## run_ci_check.py
Validates file hashes stored in an audit log.

```bash
python -m forecastkernel.scripts.run_ci_check \
  --audit_log data/outputs/baseline/audit_log.json \
  --base_dir data/outputs/baseline
```

## check_storage.py
Reports the disk usage of `data` directories and fails if over 500MB.

```bash
python -m forecastkernel.scripts.check_storage
```

---
Refer to `Basic_Commands.txt` for a full end-to-end example workflow.
