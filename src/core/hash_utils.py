import hashlib
import json

def generate_serve_hash(baseline_metrics: dict) -> str:
    """Generate a reproducible SHA256 hash from selected fields in baseline_metrics."""
    payload = {
        "series_id": baseline_metrics["series_id"],
        "selected_model": baseline_metrics["selected_model"],
        "metrics": baseline_metrics["metrics"].get(baseline_metrics["selected_model"], {}),
        "timestamp": baseline_metrics["timestamp"],
        "phase": baseline_metrics["metadata"]["phase"]
    }
    encoded = json.dumps(payload, sort_keys=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()[:8]  # short hash for readability
