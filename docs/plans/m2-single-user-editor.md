# M2: Single-user editor

Goal: one person can build a workflow graph on a canvas, configure its nodes, save it, and load it again. The API stores workflows in Postgres and validates every graph with the engine. Nothing runs yet; running graphs is M3.

Issues live in the [M2: Single-user editor](https://github.com/peleg11/agent-flow-builder/milestone/2) milestone. Each issue is one PR (about 300 changed lines or fewer, not counting generated files and lockfiles), and each UI PR brings its own Playwright test (#26).

## Issues

In order. An issue can start once everything it depends on is merged.

| # | Issue | Depends on |
| --- | --- | --- |
| [#26](https://github.com/peleg11/agent-flow-builder/issues/26) | Rules from M2 planning: trusting our own API, PR size, e2e with UI | nothing |
| [#27](https://github.com/peleg11/agent-flow-builder/issues/27) | M2 plan and persistence ADRs (this file, ADR-0002, ADR-0003) | nothing |
| [#28](https://github.com/peleg11/agent-flow-builder/issues/28) | Engine graph model and validation | nothing |
| [#29](https://github.com/peleg11/agent-flow-builder/issues/29) | Postgres wiring for the API | #27 |
| [#30](https://github.com/peleg11/agent-flow-builder/issues/30) | Workflow API contract | #28 |
| [#31](https://github.com/peleg11/agent-flow-builder/issues/31) | Create and get a workflow | #29, #30 |
| [#32](https://github.com/peleg11/agent-flow-builder/issues/32) | List, update and delete workflows | #31 |
| [#33](https://github.com/peleg11/agent-flow-builder/issues/33) | Generated API types and typed client | #31 |
| [#34](https://github.com/peleg11/agent-flow-builder/issues/34) | Playwright setup | nothing |
| [#35](https://github.com/peleg11/agent-flow-builder/issues/35) | Canvas with local editor state | #34 |
| [#36](https://github.com/peleg11/agent-flow-builder/issues/36) | Node config panel | #33, #35 |
| [#37](https://github.com/peleg11/agent-flow-builder/issues/37) | Workflow list, routing and full-stack e2e | #32, #33, #34 |
| [#38](https://github.com/peleg11/agent-flow-builder/issues/38) | Save and load in the editor | #36, #37 |

Three chains can run in parallel at the start: the backend (#27, #29), the engine and contract (#28, #30), and the frontend tooling (#34, #35). They meet at #31 and again at #36.

## Decisions

- [ADR-0002](../adr/0002-persistence.md): Postgres, SQLAlchemy 2.0 async, Alembic, testcontainers.
- [ADR-0003](../adr/0003-graph-storage.md): a workflow's graph is one JSONB column.

## Roadmap

- **M1: Foundation.** Done. See [m1-foundation.md](m1-foundation.md).
- **M2: Single-user editor.** This milestone.
- **M3: DAG engine.** Topological scheduling, retries, cancellation, run history.
- **M4: Multiplayer with Yjs.** Open question: pycrdt in Python or a small Node relay. Needs a spike and an ADR.
- **M5: Live run view.** Run status streamed over SSE, plus per-node logs.
- **M6: Deployed demo and docs.** Fly.io or Render gets an ADR. E2E tests no longer wait for M6: each UI PR brings its own Playwright test (#26).
