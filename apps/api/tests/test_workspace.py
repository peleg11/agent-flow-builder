"""Proves the uv workspace wiring: the API environment has the engine installed."""


def test_engine_is_importable() -> None:
    import agent_flow_engine  # noqa: F401 (unused on purpose: the import is the test)
