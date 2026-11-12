# ADR-0001: Monorepo layout and tooling

- **Status:** Accepted
- **Date:** 2026-11-12

## Context

The project has three parts that change together: a Python engine that runs workflow graphs, a FastAPI service that exposes it over HTTP and server-sent events, and a React frontend. The frontend's types are generated from the API's OpenAPI schema, so an API change and its frontend change should land in the same pull request.

The project is built by one person with Claude Code, in small PRs. What matters most is that the layout is easy to understand and explain, that one command checks everything, and that the engine stays independent of HTTP and the database.

## Decision

One repository with plain folders:

- `packages/engine`: the Python engine, a standalone package with no HTTP or DB imports.
- `apps/api`: the FastAPI service, which depends on the engine.
- `apps/web`: the React + TypeScript frontend.

Tooling:

- **uv workspace** for Python. `apps/api` and `packages/engine` are workspace members that share one lockfile, and the API depends on the engine as a workspace package.
- **pnpm** for the frontend. There is only one JavaScript package today, so no pnpm workspace yet.
- **A root `justfile`** for shared commands, such as `just check` to run lint, type checks and tests across all three packages. CI calls the same recipes.

## Alternatives considered

**Turborepo or Nx.** Both add task caching and dependency-aware builds across packages. They are built mainly for JavaScript monorepos, and their Python support is weaker or comes through plugins. With three packages and one of them in JavaScript, the speed gain is small and the extra config and concepts are not. Rejected for now. If builds get slow, we can revisit.

**Separate repositories.** Each part would get its own CI and history. But a change to the API contract would need coordinated PRs across repos, and the generated frontend types would need a publishing step to share them. That costs more than it gives for a single developer. Rejected.

**One Python package for engine and API.** This is simpler at first, with one `pyproject.toml`. But the rule that the engine never imports HTTP or DB code would then depend on discipline alone. Separate packages make the dependency direction explicit (the API imports the engine, never the reverse) and let the engine be tested and type checked on its own. Rejected.

## Consequences

- One PR can change the engine, API and frontend together, and CI checks them together.
- Contributors need three tools: uv, pnpm and just. The README lists them.
- `just` is a thin layer of shell recipes, so there is no caching. Every `just check` runs everything. That is acceptable at this size.
- Python and JavaScript dependencies are locked separately (`uv.lock` and `pnpm-lock.yaml`), so dependency updates are configured per ecosystem.
- Keeping the engine free of HTTP and DB code is enforced by package boundaries and review. A lint rule for forbidden imports could come later if needed.
