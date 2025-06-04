"""CLI for validating output files against an audit log."""

import argparse
import json
import os
from utils.hash_utils import compute_file_hash

def validate_audit_hashes(audit_log_path: str, base_dir: str) -> bool:
    """Return ``True`` if all files match the hashes in ``audit_log_path``.

    Parameters
    ----------
    audit_log_path : str
        Path to ``audit_log.json`` created during the run.
    base_dir : str
        Directory containing the files to validate.

    Returns
    -------
    bool
        Whether all recorded hashes match the current file contents.
    """
    with open(audit_log_path, "r") as f:
        audit_log = json.load(f)

    mismatches = []
    for file_name, recorded_hash in audit_log["files"].items():
        full_path = os.path.join(base_dir, file_name)
        current_hash = compute_file_hash(full_path)
        if current_hash != recorded_hash:
            mismatches.append((file_name, recorded_hash, current_hash))

    if mismatches:
        print("⚠️ Hash Mismatches Found:")
        for fname, old, new in mismatches:
            print(f"- {fname}:\n  Expected: {old}\n  Found:    {new}")
        return False

    print("✅ All hashes match audit log.")
    return True

def main():
    """Entry point for the ``validate_hashes`` command.

    Returns
    -------
    None
    """

    parser = argparse.ArgumentParser(description="Validate CI Hashes from audit log.")
    parser.add_argument("--audit_log", type=str, required=True, help="Path to audit_log.json")
    parser.add_argument("--base_dir", type=str, required=True, help="Base directory containing the files")

    args = parser.parse_args()
    success = validate_audit_hashes(args.audit_log, args.base_dir)

    if not success:
        exit(1)

if __name__ == "__main__":
    main()

