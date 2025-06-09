"""Helpers to gate optional features based on project phase."""


def include_dm_test(phase: int) -> bool:
    """Enable DM test output for phase ≥ 2.

    Parameters
    ----------
    phase : int
        Current project phase.

    Returns
    -------
    bool
        ``True`` if DM test metrics should be generated.
    """
    return phase >= 2

def include_drift_monitor(phase: int) -> bool:
    """Enable drift monitor for phase ≥ 2.

    Parameters
    ----------
    phase : int
        Current project phase.

    Returns
    -------
    bool
        ``True`` if drift monitoring plots should be produced.
    """
    return phase >= 2

def include_serve_hash(phase: int) -> bool:
    """Enable model serving hash for phase ≥ 2.

    Parameters
    ----------
    phase : int
        Current project phase.

    Returns
    -------
    bool
        ``True`` if a serve hash should be included in metrics.
    """
    return phase >= 2

