"""CI helpers for validating hashed file outputs."""

import json
import os
from utils.hash_utils import compute_file_hash

def validate_file_hashes(audit_log_path: str, output_dir: str) -> dict:
    """Validate a set of files against hashes stored in an audit log.

    Parameters
    ----------
    audit_log_path : str
        Path to ``audit_log.json`` produced during the run.
    output_dir : str
        Directory containing the files to check.

    Returns
    -------
    dict
        Mapping of file names to mismatch information. Empty if all match.
    """

    with open(audit_log_path, "r") as f:
        audit_data = json.load(f)

    stored_hashes = audit_data.get("files", {})
    mismatches = {}

    for filename, expected_hash in stored_hashes.items():
        current_path = os.path.join(output_dir, filename)
        if not os.path.exists(current_path):
            mismatches[filename] = "Missing file"
            continue

        current_hash = compute_file_hash(current_path)
        if current_hash != expected_hash:
            mismatches[filename] = {
                "expected": expected_hash,
                "actual": current_hash
            }

    return mismatches

if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Validate CI File Hashes")
    parser.add_argument("--audit_log", type=str, required=True, help="Path to audit_log.json")
    parser.add_argument("--output_dir", type=str, required=True, help="Path to directory with files to validate")
    args = parser.parse_args()

    mismatches = validate_file_hashes(args.audit_log, args.output_dir)

    if mismatches:
        print("❌ Hash mismatches detected:")
        print(json.dumps(mismatches, indent=2))
    else:
        print("✅ All hashes match. CI validation passed.")
if __name__ == "__main__":
    import argparse
    import json
    import os

    parser = argparse.ArgumentParser(description="Validate CI File Hashes")
    parser.add_argument("--audit_log", type=str, help="Path to audit_log.json")
    parser.add_argument("--output_dir", type=str, help="Path to directory with files to validate")
    parser.add_argument("--run_dir", type=str, help="Base path to infer both audit_log and output_dir")
    parser.add_argument("--log_ci_results", action="store_true", help="Log validation result to ci_hash_results.json")

    args = parser.parse_args()

    # Support --run_dir shortcut
    if args.run_dir:
        args.audit_log = os.path.join(args.run_dir, "audit_log.json")
        args.output_dir = args.run_dir

    mismatches = validate_file_hashes(args.audit_log, args.output_dir)

    if mismatches:
        print("❌ Hash mismatches detected:")
        print(json.dumps(mismatches, indent=2))
    else:
        print("✅ All hashes match. CI validation passed.")

    if args.log_ci_results:
        result = {
            "timestamp": datetime.utcnow().isoformat(),
            "run_dir": args.run_dir or args.output_dir,
            "passed": not bool(mismatches),
            "mismatches": mismatches
        }
        with open(os.path.join(args.output_dir, "ci_hash_results.json"), "w") as f:
            json.dump(result, f, indent=2)

