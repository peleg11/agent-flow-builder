"""Service configuration, read from environment variables. See .env.example."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Every field has a default so the app can be built at import time with no env set,
    # which is what `fastapi dev` and the tests do.
    model_config = SettingsConfigDict(env_prefix="AGENT_FLOW_API_", env_file=".env")

    # FastAPI's debug mode: tracebacks in error responses. Never enable in production.
    debug: bool = False
