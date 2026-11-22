# ADR-0003: Store a workflow's graph as one JSONB column

- **Status:** Accepted
- **Date:** 2026-11-22

## Context

A workflow is a name plus a graph: nodes (id, type, position, config) and edges between them. Each node type has its own config shape, and the API's Pydantic models (#30) are the only definition of that shape.

How the graph is used decides how to store it:

- The editor always loads the whole graph and saves the whole graph (`PUT /workflows/{id}` is a full replace).
- The engine validates and later runs the whole graph at once.
- In M4, Yjs treats the graph as one shared document, so the server stores and loads it as a unit.
- Nothing in M2 or M3 needs to query inside graphs across workflows.

## Decision

The `workflows` table has a `graph` column of type JSONB that holds the whole graph: its nodes and its edges. There are no separate node or edge tables.

The graph includes each node's canvas position, because the editor needs it and M4's Yjs document will hold it too. The canvas viewport (zoom and pan) is not stored.

The API validates the graph with Pydantic and the engine before writing it, so the database only ever holds graphs that parsed and passed validation. An invalid graph gets a 422 response with a list of `GraphProblem` (`code`, `message`, `node_ids`), defined in the API contract, so the editor can point at the broken nodes. The database does not enforce the graph's structure itself.

## Alternatives considered

**Separate `nodes` and `edges` tables.** Foreign keys would stop an edge from pointing at a missing node, and queries across workflows would be plain SQL. But every save would become a diff or a delete-and-reinsert of many rows inside a transaction, every load a join, and each node type's config would still need JSON or one table per type. The engine already checks for missing nodes, cycles and duplicates, and it has to anyway, because a cycle is not something foreign keys can prevent. Rejected: more code and more queries for guarantees we already get elsewhere.

**JSON stored as text, or Postgres's plain `json` type.** Same shape as the decision, but neither can be indexed or queried efficiently, and `json` keeps whitespace and duplicate keys. JSONB costs nothing extra here. Rejected.

**Storing the Yjs document (binary) as the source of truth.** This would fit M4 directly. But M4's design is still an open question (pycrdt or a Node relay), and a binary blob cannot be validated, read or queried by the API. Rejected for now. M4's ADR decides how the Yjs state and this column relate.

## Consequences

- Load and save are one row read and one row write, and the column maps directly to the Pydantic graph model.
- Queries across workflows, such as "every workflow that uses tool X", are harder. They need JSONB operators (`@>`, `jsonb_path_query`) and possibly a GIN index. That is fine for occasional queries, but if such queries become a core feature, revisit this ADR.
- Referential integrity inside a graph depends on the API validating every write. A row written by hand or by a buggy migration could hold an invalid graph.
- Rejecting invalid graphs means a half-finished graph (for example one with a cycle) cannot be saved. In M3, "valid to save" and "valid to run" may diverge (for example a node with incomplete config), so revisit this rule then.
- The graph has no schema version field. Changing its shape later means an Alembic data migration that rewrites the JSON in every row.
- `PUT` replaces the whole graph, so a run in M3 cannot point back to the graph it executed. M3's runs must store their own copy of the graph, and M3 decides what deleting a workflow does to its runs. In M2, `DELETE` is a hard delete.
- Concurrent edits to the same workflow overwrite each other (last write wins). That is acceptable for the single-user editor in M2. M4's multiplayer work has to solve it.
