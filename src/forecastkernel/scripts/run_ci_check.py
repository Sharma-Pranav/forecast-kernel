"""Command line helper to validate CI audit log hashes."""

import argparse
import json
import os
import sys
from forecastkernel.utils.hash_utils import compute_file_hash

def validate_audit_hashes(
    audit_log_path: str, base_dir: str, force: bool = False
) -> bool:
    """Check recorded file hashes against the actual files.

    Parameters
    ----------
    audit_log_path : str
        Path to ``audit_log.json`` produced during the baseline run.
    base_dir : str
        Directory containing the files to validate.
    force : bool, optional
        If ``True`` return success even when mismatches are found.

    Returns
    -------
    bool
        ``True`` if all hashes match or ``force`` is ``True``.
    """
    with open(audit_log_path, "r") as f:
        audit_log = json.load(f)

    mismatches = []
    for file_name, recorded_hash in audit_log["files"].items():
        full_path = os.path.join(base_dir, file_name)
        if not os.path.exists(full_path):
            print(f"[❌] Missing file: {file_name}")
            mismatches.append((file_name, recorded_hash, "MISSING"))
            continue
        current_hash = compute_file_hash(full_path)
        if current_hash != recorded_hash:
            mismatches.append((file_name, recorded_hash, current_hash))

    if mismatches:
        print("⚠️ Hash Mismatches Found:")
        for fname, old, new in mismatches:
            print(f"- {fname}:\n  Expected: {old}\n  Found:    {new}")
        if force:
            print("[⚠] Mismatch overridden by --force.")
            return True
        return False

    print("✅ All hashes match audit log.")
    return True

def main() -> None:
    """Entry point for the ``run_ci_check`` command.

    Returns
    -------
    None
    """

    parser = argparse.ArgumentParser(description="Validate CI Hashes from audit log.")
    parser.add_argument("--audit_log", type=str, required=True, help="Path to audit_log.json")
    parser.add_argument("--base_dir", type=str, required=True, help="Base directory containing the files")
    parser.add_argument("--force", action="store_true", help="Override hash mismatch failure")
    args = parser.parse_args()

    success = validate_audit_hashes(args.audit_log, args.base_dir, args.force)

    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()

