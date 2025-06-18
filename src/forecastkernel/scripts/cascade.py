import argparse
import subprocess
import sys

from forecastkernel.core.aggregation import enforce_cascade_checks


def main() -> None:
    """Validate parent run then launch ``baseline_sf`` with ``--parent_run``."""
    parser = argparse.ArgumentParser(description="Cascade baseline run from parent outputs")
    parser.add_argument("--parent_run", type=str, required=True, help="Path to parent run directory")
    parser.add_argument(
        "baseline_args",
        nargs=argparse.REMAINDER,
        help="Additional args for baseline_sf (use '--' before these)"
    )
    args = parser.parse_args()

    enforce_cascade_checks(args.parent_run)

    extra_args = args.baseline_args
    if extra_args and extra_args[0] == "--":
        extra_args = extra_args[1:]

    cmd = [
        sys.executable,
        "-m",
        "forecastkernel.scripts.baseline_sf",
        "--parent_run",
        args.parent_run,
    ] + extra_args

    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
