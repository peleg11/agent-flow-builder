# CLAUDE.md

Guidelines for any Claude Code session working in this repo. Read this first, then read the GitHub issue you were given.

## Project

A collaborative visual workflow builder for AI pipelines. Users wire nodes (LLM call, MCP tool, branch, transform) on a canvas. A Python engine runs the resulting DAG and streams live status back to the browser.

## Layout

- `apps/api`: FastAPI service (HTTP, SSE, persistence)
- `apps/web`: React + TypeScript + Vite frontend
- `packages/engine`: pure Python DAG engine. No HTTP or DB imports, ever.
- `docs/adr`: architecture decision records
- `docs/plans`: per-milestone plans

<!-- EDIT: update this list as the layout changes -->

## Commands

- `just check`: lint, type check and tests for everything (the same thing CI runs)
- Per package commands live in each package's README

<!-- EDIT: fill in once the justfile exists -->

## Workflow

- Work from a GitHub issue. If the task isn't covered by one, stop and say so.
- Never commit to `main`. One branch and one PR per issue.
- One concept per PR, about 300 changed lines or fewer. If it's growing, split it and open follow-up issues.
- Stay in scope. Anything extra you notice becomes a new issue, not part of this PR.
- Commit messages follow Conventional Commits (`feat:`, `fix:`, `test:`, `docs:`, `refactor:`, `chore:`).
- Fill in every field of the PR template. "Closes #N" goes in the description.
- Add a dependency only with a one-line justification in the PR. Significant ones need an ADR.

## Explain the work

I need to be able to explain every line in this repo. For each PR:

- End with a short walkthrough: what each changed file does, why this approach, and what the alternatives were.
- Name trade-offs and uncertainties plainly instead of guessing or hiding them.
- Prefer the simple, boring approach and say why when you pick it.

## Architecture rules

- Pydantic models are the API contract. The frontend's types are generated from the OpenAPI schema and never hand-edited.
- Dependencies point inward: `apps/api` imports `packages/engine`, never the reverse.
- The engine takes its dependencies (clock, node executors, event sink) as parameters so it can be tested in isolation.
- Business logic does not live in route handlers or React components.

## Python

- Full type hints. `mypy --strict` must pass.
- `ruff` for lint and format. No ignoring a rule without a comment explaining why.
- Async all the way down in the API. No blocking calls on the event loop.
- No bare `except`, no mutable default arguments, no global mutable state.
- Small functions with one job. Names say what a thing is or does.

## TypeScript

- `strict` mode. No `any`. No `!` non-null assertions without a comment explaining why.
- Small components. Logic goes in hooks, state goes in Jotai atoms next to the feature that uses them.
- Parse and validate data at the boundary. Don't trust API or user input.

## Testing

- Test behavior, not implementation details.
- Every bug fix starts with a failing test that reproduces it.
- Unit tests for the engine and pure logic. Integration tests for the API against a real Postgres (testcontainers). Playwright for key user journeys.
- Don't mock our own domain code. Mock only at the edges (network, clock, LLM providers).
- A PR that changes behavior without a test needs a stated reason.

## Clean code

- Comments explain why, not what. Delete dead code instead of commenting it out.
- No `TODO` without an issue number.
- No secrets in the repo. Config comes from environment variables, with a documented `.env.example`.
- Prefer deleting code over adding it.

## Definition of done

- `just check` passes locally.
- Tests added or updated.
- Docs or ADR updated if a decision changed.
- PR template complete, including the walkthrough.

<!-- EDIT: add your own rules below. Your personal style, naming conventions, folder habits, review pet peeves. -->

## Keeping these rules current

- When I correct you or state a coding preference, propose adding it as a rule in its own `docs:` PR. Never slip rule changes into feature work.
- Write each rule with its reason, so it can be judged and revisited later.
- Keep this file under about 200 lines. If it grows past that, tighten wording or move detail into a package README or an ADR.
- Never weaken or remove a rule without asking me first. If a rule gets in the way, say so instead of working around it.
