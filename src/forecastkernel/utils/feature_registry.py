"""Feature registry loader for Forecast Kernel."""

from __future__ import annotations

import os
from typing import Any, Dict, Optional

import yaml

_FEATURES: Optional[Dict[str, Any]] = None


def _default_path() -> str:
    """Return the default path of ``features.yaml`` relative to project root."""
    project_root = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    )
    return os.path.join(project_root, "configs", "features.yaml")


def load_features(path: Optional[str] = None) -> Dict[str, Any]:
    """Load feature definitions from ``features.yaml``.

    Parameters
    ----------
    path : str, optional
        Custom path to a ``features.yaml`` file. Defaults to the project
        config location.

    Returns
    -------
    dict
        Parsed feature registry.
    """
    global _FEATURES
    if _FEATURES is None or path:
        registry_path = path or _default_path()
        with open(registry_path, "r") as f:
            _FEATURES = yaml.safe_load(f)
    return _FEATURES  # type: ignore[return-value]


def get_feature(name: str, path: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Retrieve a feature definition by key."""
    registry = load_features(path)
    features = registry.get("features", {}) if registry else {}
    return features.get(name)
