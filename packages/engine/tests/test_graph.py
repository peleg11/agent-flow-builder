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


def test_edge_to_missing_target_is_reported() -> None:
    assert validate_graph(graph("a", "a>ghost")) == [
        GraphProblem("missing_node", "Edge a -> ghost points to missing node ghost", ("a", "ghost"))
    ]


def test_edge_from_missing_source_is_reported() -> None:
    assert validate_graph(graph("b", "ghost>b")) == [
        GraphProblem("missing_node", "Edge ghost -> b points to missing node ghost", ("ghost", "b"))
    ]


def test_self_loop_on_missing_node_names_it_once() -> None:
    assert validate_graph(graph("", "x>x")) == [
        GraphProblem("missing_node", "Edge x -> x points to missing node x", ("x",))
    ]


def test_repeated_edge_is_reported_once() -> None:
    codes = [p.code for p in validate_graph(graph("a", "a>a a>a a>ghost a>ghost"))]
    assert codes == ["self_loop", "missing_node"]


def test_self_loop_is_reported_and_not_also_as_a_cycle() -> None:
    assert validate_graph(graph("a", "a>a")) == [
        GraphProblem("self_loop", "Node a has an edge to itself", ("a",))
    ]


def test_cycle_is_reported_with_only_its_nodes() -> None:
    assert validate_graph(graph("start a b c end", "start>a a>b b>c c>a c>end")) == [
        GraphProblem("cycle", "Nodes a, b, c form a cycle", ("a", "b", "c"))
    ]


def test_every_node_on_overlapping_cycles_is_reported_whatever_the_edge_order() -> None:
    expected = [GraphProblem("cycle", "Nodes a, b, c form a cycle", ("a", "b", "c"))]
    assert validate_graph(graph("a b c", "a>b b>a a>c c>b")) == expected
    assert validate_graph(graph("a b c", "a>c c>b a>b b>a")) == expected


def test_separate_cycles_are_reported_separately() -> None:
    codes_and_nodes = [
        (p.code, p.node_ids) for p in validate_graph(graph("a b c d", "a>b b>a c>d d>c"))
    ]
    assert codes_and_nodes == [("cycle", ("a", "b")), ("cycle", ("c", "d"))]


def test_every_problem_is_reported_together() -> None:
    codes = [p.code for p in validate_graph(graph("a a b", "a>a a>ghost a>b b>a"))]
    assert codes == ["duplicate_node_id", "self_loop", "missing_node", "cycle"]


def test_long_graph_does_not_hit_the_recursion_limit() -> None:
    ids = [f"n{i}" for i in range(5000)]
    chain = " ".join(f"{a}>{b}" for a, b in pairwise(ids))
    assert validate_graph(graph(" ".join(ids), chain)) == []
    ring = validate_graph(graph(" ".join(ids), f"{chain} n4999>n0"))
    assert [p.node_ids for p in ring] == [tuple(ids)]
