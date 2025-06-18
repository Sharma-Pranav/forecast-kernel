import argparse
import json
from datetime import datetime

import duckdb
import pandas as pd

from forecastkernel.schemas.input_schema import forecast_input_schema
from forecastkernel.utils.logging_utils import setup_logger


def run_preflight(input_path: str, report_path: str) -> dict:
    """Run basic validation checks on the raw input data.

    Parameters
    ----------
    input_path : str
        Path to the CSV file containing the time series data.
    report_path : str
        Destination path for the JSON validation report.

    Returns
    -------
    dict
        Dictionary summarising validation results and dataset metadata.
    """
    log = setup_logger(None, "preflight")
    log.info("Loading dataset via duckdb ...")
    con = duckdb.connect()
    df = con.execute(f"SELECT * FROM read_csv_auto('{input_path}')").fetch_df()

    report = {
        "timestamp": datetime.utcnow().isoformat(),
        "input_file": input_path,
        "row_count": len(df),
        "columns": list(df.columns),
    }

    try:
        forecast_input_schema.validate(df)
        report["pandera_pass"] = True
    except Exception as exc:  # broad exception -> fail-fast
        log.exception("Pandera validation failed")
        report["pandera_pass"] = False
        report["pandera_error"] = str(exc)

    try:
        import great_expectations as ge  # type: ignore

        ge_df = ge.from_pandas(df)
        ge_df.expect_column_values_to_not_be_null("ds")
        ge_df.expect_column_values_to_not_be_null("unique_id")
        ge_df.expect_column_values_to_not_be_null("y")
        ge_result = ge_df.validate()
        report["great_expectations_pass"] = ge_result["success"]
        report["great_expectations_results"] = ge_result["statistics"]
    except ImportError:
        log.warning("Great Expectations not installed; skipping checks")
        report["great_expectations_pass"] = None
    except Exception as exc:  # catch any ge errors
        log.exception("Great Expectations validation failed")
        report["great_expectations_pass"] = False
        report["great_expectations_error"] = str(exc)

    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)

    log.info(f"Preflight report saved to {report_path}")
    if report.get("pandera_pass") is not True or report.get("great_expectations_pass") is False:
        raise ValueError("Data preflight checks failed")

    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Phase 0a Data Pre-Flight")
    parser.add_argument("--input", type=str, required=True, help="Path to raw CSV file")
    parser.add_argument("--output", type=str, default="preflight_report.json", help="Path for JSON report")
    args = parser.parse_args()
    run_preflight(args.input, args.output)


if __name__ == "__main__":
    main()
