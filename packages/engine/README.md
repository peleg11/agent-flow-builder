# agent-flow-engine

The pure Python engine that runs workflow graphs (DAGs) built in agent-flow-builder. Later milestones add the graph model, the scheduler and node execution. It has no logic yet.

## The one rule: no HTTP or database code

This package never imports HTTP or database code: no FastAPI, no HTTP clients, no ORMs, no database drivers.

The engine receives everything it needs from outside as parameters: a clock, node executors and an event sink. `apps/api` handles HTTP and persistence and calls into the engine. The dependency points one way only: the API imports the engine, never the reverse.

Why: an engine with no I/O can be tested in isolation, quickly and deterministically, and it can be reused outside the web service. See [ADR-0001](../../docs/adr/0001-monorepo-layout.md).

## Commands

Run these from `packages/engine`. You need [uv](https://docs.astral.sh/uv/), which installs Python 3.12 on its own if it is missing.

| Command | What it does |
| --- | --- |
| `uv run ruff check` | Lint |
| `uv run ruff format` | Format (add `--check` to only verify) |
| `uv run mypy` | Type check with `--strict` |
| `uv run pytest` | Run the tests |

All tool settings live in `pyproject.toml`.
