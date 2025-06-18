from forecastkernel.utils.feature_registry import load_features, get_feature


def test_registry_loads() -> None:
    registry = load_features()
    assert "features" in registry
    assert "y" in registry["features"]


def test_get_feature() -> None:
    feat = get_feature("lag_7")
    assert feat is not None
    assert "transformation" in feat
