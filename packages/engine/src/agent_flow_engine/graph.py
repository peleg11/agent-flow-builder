"""The workflow graph model and the checks that make it a valid DAG."""

from collections import Counter
from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class Node:
    id: str
    type: str


@dataclass(frozen=True)
class Edge:
    source: str
    target: str


@dataclass(frozen=True)
class Graph:
    nodes: tuple[Node, ...] = ()
    edges: tuple[Edge, ...] = ()


ProblemCode = Literal["duplicate_node_id", "missing_node", "self_loop", "cycle"]


@dataclass(frozen=True)
class GraphProblem:
    """One reason a graph is invalid. Same shape as the API's GraphProblem (ADR-0003)."""

    code: ProblemCode
    message: str
    node_ids: tuple[str, ...]


def validate_graph(graph: Graph) -> list[GraphProblem]:
    """Return every problem in the graph. An empty list means it is a valid DAG."""
    node_ids = [node.id for node in graph.nodes]
    problems = _duplicate_node_problems(node_ids)
    adjacency: dict[str, list[str]] = {node_id: [] for node_id in node_ids}
    for edge in graph.edges:
        missing = [end for end in (edge.source, edge.target) if end not in adjacency]
        if missing:
            problems.append(_missing_node_problem(edge, missing))
        elif edge.source == edge.target:
            problems.append(
                GraphProblem(
                    "self_loop", f"Node {edge.source} has an edge to itself", (edge.source,)
                )
            )
        else:
            adjacency[edge.source].append(edge.target)
    problems.extend(
        GraphProblem("cycle", f"Nodes {' -> '.join([*cycle, cycle[0]])} form a cycle", tuple(cycle))
        for cycle in _find_cycles(adjacency)
    )
    return problems


def _duplicate_node_problems(node_ids: list[str]) -> list[GraphProblem]:
    return [
        GraphProblem("duplicate_node_id", f"{count} nodes share the id {node_id}", (node_id,))
        for node_id, count in Counter(node_ids).items()
        if count > 1
    ]


def _missing_node_problem(edge: Edge, missing: list[str]) -> GraphProblem:
    return GraphProblem(
        "missing_node",
        f"Edge {edge.source} -> {edge.target} points to missing node {', '.join(missing)}",
        (edge.source, edge.target),
    )


def _find_cycles(adjacency: dict[str, list[str]]) -> list[list[str]]:
    """Depth-first search that returns the path of every back edge it meets.

    Iterative rather than recursive so a long chain of nodes cannot hit Python's recursion
    limit. Each cycle is found once per back edge, so cycles that share nodes can each show up.
    """
    finished: set[str] = set()
    cycles: list[list[str]] = []
    for start in adjacency:
        if start in finished:
            continue
        path = [start]
        on_path = {start}
        pending_targets = [iter(adjacency[start])]
        while pending_targets:
            target = next(pending_targets[-1], None)
            if target is None:
                done = path.pop()
                on_path.remove(done)
                finished.add(done)
                pending_targets.pop()
            elif target in on_path:
                cycles.append(path[path.index(target) :])
            elif target not in finished:
                path.append(target)
                on_path.add(target)
                pending_targets.append(iter(adjacency[target]))
    return cycles
