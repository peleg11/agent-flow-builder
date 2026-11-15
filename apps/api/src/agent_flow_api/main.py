"""Builds the FastAPI app. `app` is the object `fastapi dev` serves."""

from fastapi import FastAPI

from agent_flow_api import health
from agent_flow_api.settings import Settings


def create_app(settings: Settings) -> FastAPI:
    # Settings come in as a parameter so tests can build an app with any configuration.
    app = FastAPI(title="agent-flow-builder API", debug=settings.debug)
    app.include_router(health.router)
    return app


app = create_app(Settings())
