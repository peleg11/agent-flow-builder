# ADR-0002: Persistence with Postgres and SQLAlchemy

- **Status:** Accepted
- **Date:** 2026-11-22

## Context

M2 saves workflows, and later milestones add run history (M3) and multiplayer state (M4). The API needs a database, a way to talk to it, a way to change its schema over time, and a way to test against it.

Constraints from `CLAUDE.md`: the API is async all the way down, with no blocking calls on the event loop; `mypy --strict` must pass; and integration tests run against a real Postgres, not a mock or a stand-in. ADR-0003 stores each workflow's graph as JSON, so the database needs good JSON support.

## Decision

- **Postgres** is the database, in development, tests, CI and production.
- **SQLAlchemy 2.0 with its async extension** talks to it, through the **psycopg 3** driver in async mode (`postgresql+psycopg://`). Models use the typed `Mapped[...]` style so mypy checks them. The engine and session factory are created in the app's lifespan, not at import time, and routes get a session through a FastAPI dependency.
- **Alembic** owns the schema. Every schema change is a migration in the repo. The app never creates tables itself (no `metadata.create_all`).
- **testcontainers** starts a throwaway Postgres for integration tests, and the test fixture runs the Alembic migrations against it, so tests use the same schema as production.
- Local development uses Postgres from a `docker-compose.yml`.
- One pinned Postgres major version is used everywhere: docker-compose, testcontainers and CI. #29 picks the number.

SQLAlchemy models are storage only. Pydantic models stay the API contract, and a service layer converts between them.

Schema conventions:

- Ids are UUIDs, with `gen_random_uuid()` as the database default.
- Timestamps are `timestamptz`, stored in UTC.
- The app sets `updated_at` (SQLAlchemy `onupdate`). No database triggers, so no logic hides in the database.

## Alternatives considered

**SQLite.** Zero setup and no Docker. But its JSON support is weaker than Postgres's JSONB (no GIN indexes, fewer operators), async access goes through a thread pool, and it differs from Postgres in types and locking. Tests would pass on SQLite and then behave differently in production, which is exactly what the "real Postgres" testing rule exists to prevent. Rejected.

**SQLModel.** One class serves as both the Pydantic model and the table, which saves code at first. But it ties the API contract to the storage schema, so a column change becomes an API change and the reverse. Its async support and typing lag behind SQLAlchemy 2.0, and it adds a layer on top of SQLAlchemy that we would have to understand anyway. Rejected: we want the contract and the storage to change independently.

**asyncpg as the driver.** The most common async driver with SQLAlchemy, and faster in benchmarks. But it is async-only, and its prepared-statement cache breaks behind connection poolers such as PgBouncer, which managed Postgres hosts often put in front of the database (relevant for M6). psycopg 3 does both sync and async, and works behind poolers with less configuration. The speed difference does not matter at our size. Switching later is mostly a URL and dependency change, because SQLAlchemy hides the driver. Rejected.

**A raw driver (psycopg or asyncpg) with no ORM.** Fewest moving parts and full control of SQL. But rows come back untyped, so `mypy --strict` gets nothing out of query results, and we would write our own mapping and session handling. Alembic also works best with SQLAlchemy models to compare against. Rejected: the saved code is small, and the lost type checking is large.

**A document database such as MongoDB.** Fits "store the whole graph as one document". But runs, users and permissions in later milestones are relational, and Postgres's JSONB already gives document storage where we need it. Rejected: one database is simpler than two.

**Mocking the database in tests, or an in-memory fake.** Faster tests with no Docker. But a fake does not catch migration errors, constraint violations or JSONB behavior, and `CLAUDE.md` says to mock only at the edges. Rejected.

## Consequences

- `just check` and the `api` CI job need Docker, because testcontainers starts Postgres. GitHub's Ubuntu runners include Docker. Locally, Docker Desktop (or another runtime) must be running, and the README will say so. Without Docker, `just check` fails with a clear message. Integration tests are never skipped, so a green local run still means a green CI run.
- Integration tests are slower than unit tests: starting a container takes a few seconds. Starting one container per test session, not per test, keeps this small.
- Contributors need to know SQLAlchemy 2.0's async session rules, for example that lazy loading does not work in async code. Relationships must be loaded explicitly.
- Every schema change needs a migration, which is more ceremony but keeps every environment on the same schema.
- Three new runtime dependencies (`sqlalchemy`, `psycopg[binary]`, `alembic`) and one dev dependency (`testcontainers`), added in #29.
