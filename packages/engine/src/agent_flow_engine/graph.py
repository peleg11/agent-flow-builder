"""The workflow graph model and the checks that make it a valid DAG."""

from collections import Counter
from collections.abc import Container
from dataclasses import dataclass
from typing import Literal

type NodeId = str


@dataclass(frozen=True)
class Node:
    id: NodeId
    type: str


@dataclass(frozen=True)
class Edge:
    source: NodeId
    target: NodeId


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
    node_ids: tuple[NodeId, ...]


def validate_graph(graph: Graph) -> list[GraphProblem]:
    """Return every problem in the graph. An empty list means it is a valid DAG.

    Each edge gets at most one problem: a missing node, else a self-loop. Repeated edges count once.
    """
    node_ids = [node.id for node in graph.nodes]
    problems = _duplicate_node_problems(node_ids)
    adjacency: dict[NodeId, list[NodeId]] = {node_id: [] for node_id in node_ids}
    for edge in dict.fromkeys(graph.edges):
        problem = _missing_node_problem(edge, adjacency) or _self_loop_problem(edge)
        if problem:
            problems.append(problem)
        else:
            adjacency[edge.source].append(edge.target)
    problems.extend(_cycle_problems(adjacency))
    return problems


def _duplicate_node_problems(node_ids: list[NodeId]) -> list[GraphProblem]:
    return [
        GraphProblem("duplicate_node_id", f"{count} nodes share the id {node_id}", (node_id,))
        for node_id, count in Counter(node_ids).items()
        if count > 1
    ]


def _missing_node_problem(edge: Edge, node_ids: Container[NodeId]) -> GraphProblem | None:
    ends = tuple(dict.fromkeys((edge.source, edge.target)))
    missing = [end for end in ends if end not in node_ids]
    if not missing:
        return None
    message = f"Edge {edge.source} -> {edge.target} points to missing node {', '.join(missing)}"
    return GraphProblem("missing_node", message, ends)


def _self_loop_problem(edge: Edge) -> GraphProblem | None:
    if edge.source != edge.target:
        return None
    return GraphProblem("self_loop", f"Node {edge.source} has an edge to itself", (edge.source,))


def _cycle_problems(adjacency: dict[NodeId, list[NodeId]]) -> list[GraphProblem]:
    """One problem per strongly connected component with more than one node.

    A node is on a cycle exactly when its component has other nodes (self-loops are reported
    separately), so this lists every node on every cycle, whatever order the edges came in.
    """
    groups: dict[NodeId, list[NodeId]] = {}
    for node, root in _component_roots(adjacency).items():
        groups.setdefault(root, []).append(node)
    return [
        GraphProblem("cycle", f"Nodes {', '.join(group)} form a cycle", tuple(group))
        for group in groups.values()
        if len(group) > 1
    ]


def _component_roots(adjacency: dict[NodeId, list[NodeId]]) -> dict[NodeId, NodeId]:
    """Kosaraju's algorithm: map each node, in adjacency order, to its component's root.

    Both passes use explicit stacks, not recursion, so a long chain of nodes cannot hit
    Python's recursion limit.
    """
    reverse: dict[NodeId, list[NodeId]] = {node: [] for node in adjacency}
    for source, targets in adjacency.items():
        for target in targets:
            reverse[target].append(source)
    root_of: dict[NodeId, NodeId] = {}
    for root in reversed(_post_order(adjacency)):
        if root in root_of:
            continue
        root_of[root] = root
        to_visit = [root]
        while to_visit:
            for source in reverse[to_visit.pop()]:
                if source not in root_of:
                    root_of[source] = root
                    to_visit.append(source)
    return {node: root_of[node] for node in adjacency}


def _post_order(adjacency: dict[NodeId, list[NodeId]]) -> list[NodeId]:
    """Every node, each listed after all the nodes reachable from it (depth-first)."""
    visited: set[NodeId] = set()
    order: list[NodeId] = []
    for start in adjacency:
        if start in visited:
            continue
        visited.add(start)
        stack = [(start, iter(adjacency[start]))]
        while stack:
            node, targets = stack[-1]
            target = next(targets, None)
            if target is None:
                stack.pop()
                order.append(node)
            elif target not in visited:
                visited.add(target)
                stack.append((target, iter(adjacency[target])))
    return order
