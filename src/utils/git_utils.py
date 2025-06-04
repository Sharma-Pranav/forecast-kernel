"""Git helper utilities."""

import subprocess

def get_git_commit_hash() -> str:
    """Return the current commit hash or ``"unknown"`` if unavailable.

    Returns
    -------
    str
        The git commit hash for ``HEAD`` or ``"unknown"`` if not in a git repo.
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return "unknown"

