# Forecast Kernel

This repository contains a small forecasting toolkit used for testing continuous integration pipelines. The `src` directory is organised into logical subpackages:

- **core** – statistical helpers and algorithms such as evaluation utilities, drift detection and error decomposition.
- **utils** – general helpers for hashing, logging and git integration.
- **pipelines** – plotting helpers for diagnostics.
- **models** – placeholder package for forecast model definitions.

Scripts under `scripts/` provide command line entry points for running baseline forecasts, validating hashes and visualising forecast deltas. Tests live in `tests/` and exercise the CI routines.

The project follows a lightweight structure to keep components modular and easy to reuse across experiments.
