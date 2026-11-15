"""Smoke test that proves the toolchain runs. Replace once the engine has real behavior."""


def test_package_is_importable() -> None:
    # Tests import the installed package (importlib mode plus the src/ layout), so a
    # successful import shows the package built and installed correctly.
    import agent_flow_engine  # noqa: F401 (unused on purpose: the import is the test)
