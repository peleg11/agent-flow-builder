# M1: Foundation

Goal: a public repo with three empty-but-wired packages, strict tooling, CI on every PR, and documented decisions. No product features yet.

Order matters. Each issue is one PR (about 300 changed lines or fewer). Issue 7 comes last because branch protection needs CI checks that have already run once.

## Kickoff (about 10 minutes, on your side)

1. Create a public GitHub repo with a README, clone it, open it in VS Code, and start Claude Code.
2. Make sure the GitHub CLI works: `gh auth status`. Install it from cli.github.com if needed.
3. Create the project board in the GitHub UI: Projects tab, New project, Board template. (Creating boards from the CLI needs an extra token scope, so the UI is simpler.)
4. Save this file as `docs/plans/m1-foundation.md`. Do not commit it yet (issue 1 does that).
5. Paste this into Claude Code:

```
Read docs/plans/m1-foundation.md. Create a GitHub milestone named "M1: Foundation".
Create the labels docs, engine, api, web, ci if they don't exist. Then create the 7 issues
under "Issues" using gh issue create, with the milestone, one matching label each, and the
body exactly as written. Do not write code and do not commit anything.
When done, list each issue number and URL.
```

## Issues

### 1. Docs foundation and ADR-0001
**Label:** docs

**Goal:** the repo explains itself and has a place for decisions.

**Scope:**
- `README.md`: what the project is, why it exists, current status, and how to run things (stub is fine).
- `docs/plans/m1-foundation.md`: commit this file.
- `docs/adr/README.md`, an ADR template (title, status, context, decision, alternatives, consequences), and `docs/adr/0001-monorepo-layout.md`.
- `.gitignore`, `.editorconfig`, and an MIT `LICENSE` (confirm with me before committing the license).

**ADR-0001 must cover:** plain folders (`apps/api`, `apps/web`, `packages/engine`), pnpm for the frontend, uv workspace for Python, a `justfile` for shared commands. Alternatives considered: Turborepo or Nx, separate repos, one Python package. State why each was rejected.

**Acceptance criteria:**
- An ADR exists with all sections filled in.
- The README has no placeholder text.

**Not in this PR:** any tooling config, code, or CI.

### 2. CLAUDE.md and GitHub templates
**Label:** docs

**Goal:** every future session and PR starts from the same rules and structure.

**Scope:**
- Add the `CLAUDE.md` I provide to the repo root. Do not rewrite it.
- Append a "Keeping these rules current" section: propose new rules as separate `docs:` PRs, write each with its reason, keep the file under about 200 lines, never weaken a rule without asking.
- `.github/pull_request_template.md` with: What, Why, How to test, Walkthrough (each changed file, why this approach, alternatives), What I learned, "Closes #".
- `.github/ISSUE_TEMPLATE/task.md` with: Goal, Scope, Acceptance criteria, Not in this PR.

**Acceptance criteria:**
- A fresh Claude Code session in the repo can accurately summarize the rules in `CLAUDE.md`.
- Opening a new PR shows the template.

**Not in this PR:** tooling, code, CI.

### 3. Engine package skeleton
**Label:** engine

**Goal:** a strictly checked Python package that has no logic yet.

**Scope:**
- `packages/engine` as a uv project with a `src/` layout, Python 3.12 or newer.
- `ruff` (lint and format), `mypy --strict`, `pytest` configured in `pyproject.toml`.
- One trivial passing test, to prove the toolchain runs.
- Package README: purpose, and the rule that it never imports HTTP or DB code.

**Acceptance criteria:**
- `uv run ruff check`, `uv run mypy`, and `uv run pytest` all pass from `packages/engine`.
- No real domain logic exists.

**Not in this PR:** DAG code, API, CI.

### 4. API skeleton
**Label:** api

**Goal:** a FastAPI service with one endpoint, wired to the engine package.

**Scope:**
- `apps/api` as a uv project, added to a uv workspace together with `packages/engine`.
- FastAPI app with `GET /health` returning `{"status": "ok"}`.
- Settings via `pydantic-settings`, plus a documented `.env.example`.
- Same tooling as the engine (ruff, strict mypy, pytest).
- Tests: `/health` returns 200, and the API can import the engine package (proves the workspace wiring).

**Acceptance criteria:**
- All three checks pass from `apps/api`.
- `uv run fastapi dev` serves `/health` locally.

**Not in this PR:** database, routes beyond `/health`, auth.

### 5. Web skeleton
**Label:** web

**Goal:** a strictly checked React app that renders one thing.

**Scope:**
- `apps/web` with Vite, React, TypeScript (`strict`), pnpm.
- ESLint and Prettier, with no `any` allowed by lint rules.
- Vitest and Testing Library, with one component test.
- App renders a placeholder heading.

**Acceptance criteria:**
- `pnpm lint`, `pnpm typecheck`, `pnpm test`, and `pnpm build` all pass from `apps/web`.

**Not in this PR:** React Flow, Jotai, API calls, styling system.

### 6. CI and local `just check`
**Label:** ci

**Goal:** the same checks run locally and on every PR and push to `main`.

**Scope:**
- Root `justfile` with `just check` (runs lint, type check and tests for all three packages) plus per-package recipes.
- `.github/workflows/ci.yml` with separate jobs for engine, api and web, dependency caching, triggers on `pull_request` and on pushes to `main`.
- Job names stay stable and descriptive, because branch protection will refer to them.
- Document in the README how to run `just check`.

**Acceptance criteria:**
- CI passes on this PR.
- Proof it works: a throwaway PR (closed, not merged) with a deliberately failing test turns CI red. Link it in this PR's description.

**Not in this PR:** deploy workflows, e2e tests, Dependabot.

### 7. Repo settings, CodeRabbit, Dependabot
**Label:** ci

**Goal:** `main` is protected and reviews and dependency updates are automatic.

**Scope (mostly settings, one tiny PR):**
- Branch protection on `main`: require a pull request, require the CI status checks from issue 6, no required approvals (GitHub does not let you approve your own PR), block force pushes.
- Merge settings: squash merge only, auto-delete branches after merge.
- Install the CodeRabbit GitHub App on this repo.
- PR adding `.github/dependabot.yml` for pip (uv), npm and GitHub Actions, weekly.
- Add a short "Review process" section to the README: CI, CodeRabbit, `/code-review` locally, then merge.

**Acceptance criteria:**
- Pushing directly to `main` is rejected.
- A PR cannot merge while CI is red.
- CodeRabbit posts a summary on the next PR.

**Not in this PR:** Claude-in-CI review (needs an API key and separate billing; revisit later).
