import pytest

from agent_flow_api.settings import Settings


def test_debug_is_off_by_default(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("AGENT_FLOW_API_DEBUG", raising=False)

    assert Settings(_env_file=None).debug is False


def test_debug_is_read_from_the_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AGENT_FLOW_API_DEBUG", "true")

    assert Settings(_env_file=None).debug is True
