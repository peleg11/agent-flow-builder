# Architecture decision records

An ADR records one significant decision: the problem, what we chose, what else we considered, and what follows from it. They exist so that a later reader (including future us) can see why the code is the way it is without guessing.

## When to write one

Write an ADR when a decision is expensive to reverse or shapes how other code is written. For example: repo layout, a framework or significant dependency, a data model or protocol, or a cross-cutting rule. Small, local choices go in the PR description instead.

## How

1. Copy [template.md](template.md) to `NNNN-short-title.md`, using the next free number.
2. Fill in every section. Alternatives must say why each was rejected.
3. Open it in the same PR as the change it describes, or on its own if it comes first.

ADRs are not edited after they are accepted, except to fix typos. To change a decision, write a new ADR and set the old one's status to "Superseded by ADR-NNNN".

## Index

| ADR | Title | Status |
| --- | --- | --- |
| [0001](0001-monorepo-layout.md) | Monorepo layout and tooling | Accepted |
