from itertools import pairwise

from agent_flow_engine.graph import Edge, Graph, GraphProblem, Node, validate_graph


def graph(node_ids: str, edges: str = "") -> Graph:
    """Build a graph from short strings: graph("a b c", "a>b b>c")."""
    nodes = tuple(Node(node_id, "llm") for node_id in node_ids.split())
    return Graph(nodes, tuple(Edge(*pair.split(">")) for pair in edges.split()))


def test_empty_graph_is_valid() -> None:
    assert validate_graph(Graph()) == []


def test_diamond_graph_is_valid() -> None:
    assert validate_graph(graph("a b c d", "a>b a>c b>d c>d")) == []


def test_duplicate_node_id_is_reported_once_per_id() -> None:
    assert validate_graph(graph("a b a a")) == [
        GraphProblem("duplicate_node_id", "3 nodes share the id a", ("a",))
    ]


def test_edge_to_missing_node_is_reported() -> None:
    assert validate_graph(graph("a", "a>ghost")) == [
        GraphProblem("missing_node", "Edge a -> ghost points to missing node ghost", ("a", "ghost"))
    ]


def test_self_loop_is_reported_and_not_also_as_a_cycle() -> None:
    assert validate_graph(graph("a", "a>a")) == [
        GraphProblem("self_loop", "Node a has an edge to itself", ("a",))
    ]


def test_cycle_is_reported_with_its_nodes_in_order() -> None:
    assert validate_graph(graph("start a b c", "start>a a>b b>c c>a")) == [
        GraphProblem("cycle", "Nodes a -> b -> c -> a form a cycle", ("a", "b", "c"))
    ]


def test_every_problem_is_reported_together() -> None:
    codes = [p.code for p in validate_graph(graph("a a b", "a>a a>ghost a>b b>a"))]
    assert codes == ["duplicate_node_id", "self_loop", "missing_node", "cycle"]


def test_long_chain_does_not_hit_the_recursion_limit() -> None:
    ids = [f"n{i}" for i in range(5000)]
    edges = " ".join(f"{a}>{b}" for a, b in pairwise(ids))
    assert validate_graph(graph(" ".join(ids), edges)) == []
