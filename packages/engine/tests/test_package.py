"""Smoke test that proves the toolchain runs. Replace once the engine has real behavior."""

import agent_flow_engine


def test_package_is_importable() -> None:
    assert agent_flow_engine.__name__ == "agent_flow_engine"
