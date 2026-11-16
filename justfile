# Shared commands for every package. CI runs these same recipes, so a green
# `just check` locally means the same checks pass on the PR.

# Lint, type check and test all three packages.
check: engine api web

# Run from the engine's folder so `uv run` syncs only the engine and its dev tools.
[working-directory('packages/engine')]
engine:
    uv run ruff check
    uv run ruff format --check
    uv run mypy
    uv run pytest

[working-directory('apps/api')]
api:
    uv run ruff check
    uv run ruff format --check
    uv run mypy
    uv run pytest

[working-directory('apps/web')]
web:
    pnpm lint
    pnpm typecheck
    pnpm test
