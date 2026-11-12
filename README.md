# agent-flow-builder

A collaborative visual workflow builder for AI pipelines. You wire nodes (LLM call, MCP tool, branch, transform) together on a canvas, a Python engine runs the resulting graph, and the browser shows each node's status live as it runs.

## Why

Multi-step AI pipelines are usually glue code: prompts, tool calls and branching logic spread across scripts that are hard to see, share or change. This project makes the pipeline itself the thing you edit. The graph on screen is the program, and you watch it execute step by step.

It is also a learning project, built in small, reviewed pull requests with every decision written down.

## Status

Milestone 1 (foundation) is in progress. There are no product features yet. The plan is in [docs/plans/m1-foundation.md](docs/plans/m1-foundation.md), and work is tracked in the [M1: Foundation milestone](https://github.com/peleg11/agent-flow-builder/milestone/1).

## Layout

| Path | What it is |
| --- | --- |
| `apps/api` | FastAPI service: HTTP, server-sent events, persistence |
| `apps/web` | React + TypeScript + Vite frontend |
| `packages/engine` | Pure Python engine that runs the graph |
| `docs/adr` | Architecture decision records |
| `docs/plans` | Per-milestone plans |

The three code packages arrive in later M1 issues. Why the repo is laid out this way is recorded in [ADR-0001](docs/adr/0001-monorepo-layout.md).

## Running it

There is nothing to run yet. Once the packages land you will need:

- Python 3.12 or newer, with [uv](https://docs.astral.sh/uv/)
- Node.js with [pnpm](https://pnpm.io/)
- [just](https://just.systems/)

Then `just check` will run lint, type checks and tests for everything, the same as CI. This section is updated as each package is added.

## License

[MIT](LICENSE)
