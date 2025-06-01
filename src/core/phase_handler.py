def include_dm_test(phase: int) -> bool:
    """Enable DM test output for phase ≥ 2."""
    return phase >= 2

def include_drift_monitor(phase: int) -> bool:
    """Enable drift monitor for phase ≥ 2."""
    return phase >= 2

def include_serve_hash(phase: int) -> bool:
    """Enable model serving hash for phase ≥ 2."""
    return phase >= 2
