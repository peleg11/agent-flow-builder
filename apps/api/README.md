# agent-flow-api

The FastAPI service for agent-flow-builder. It will handle HTTP, server-sent events and persistence, and call into [`packages/engine`](../../packages/engine) to run workflow graphs. For now it serves one endpoint: `GET /health`.

The dependency points one way only: this package imports the engine, never the reverse. See [ADR-0001](../../docs/adr/0001-monorepo-layout.md).

## Layout

| File | What it does |
| --- | --- |
| `src/agent_flow_api/main.py` | `create_app(settings)` builds the app. The module-level `app` is what `fastapi dev` serves. |
| `src/agent_flow_api/health.py` | `GET /health`, which returns `{"status": "ok"}` while the process is up. |
| `src/agent_flow_api/settings.py` | Configuration from environment variables, using pydantic-settings. |

## Configuration

Settings are read from environment variables prefixed with `AGENT_FLOW_API_`, and from a `.env` file in the folder you start the server in. [`.env.example`](.env.example) lists every variable with its default. To change one locally, copy it to `.env`, which git ignores.

## Commands

Run these from `apps/api`. You need [uv](https://docs.astral.sh/uv/). This package and the engine are members of one uv workspace, so they share the lockfile (`uv.lock`) and the virtual environment (`.venv`) at the repo root.

| Command | What it does |
| --- | --- |
| `uv run fastapi dev` | Serve the API with auto-reload at http://127.0.0.1:8000 (try `/health` or `/docs`) |
| `uv run ruff check` | Lint |
| `uv run ruff format` | Format (add `--check` to only verify) |
| `uv run mypy` | Type check with `--strict` |
| `uv run pytest` | Run the tests |

`fastapi dev` finds the app through `[tool.fastapi] entrypoint` in `pyproject.toml`. It reads that file from the current folder, so run the command from `apps/api`. All tool settings live in `pyproject.toml`.
