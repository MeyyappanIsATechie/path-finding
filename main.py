from models.graph import Graph
from models.node import Node
from algos.dijkstra import dijkstra
from utils.metrics import measure_route_search


def build_city():

    graph = Graph()

    graph.add_node(
        Node("A", 0, 0)
    )

    graph.add_node(
        Node("B", 10, 0)
    )

    graph.add_node(
        Node("C", 0, 10)
    )

    graph.add_node(
        Node("D", 10, 10)
    )

    graph.add_bidirectional_edge(
        "A",
        "B",
        4
    )

    graph.add_bidirectional_edge(
        "A",
        "C",
        2
    )

    graph.add_bidirectional_edge(
        "B",
        "D",
        5
    )

    graph.add_bidirectional_edge(
        "C",
        "D",
        8
    )

    return graph


def main():

    city_graph = build_city()

    city_graph.print_graph()

    start = "A"
    goal = "D"

    result = measure_route_search(
        dijkstra,
        city_graph,
        start,
        goal
    )

    print("\nDijkstra Result")
    print("-" * 50)
    print(f"Route: {' -> '.join(result['path'])}")
    print(f"Path cost: {result['cost']}")
    print(f"Nodes explored: {result['nodes_explored']}")
    print(f"Execution time: {result['execution_time_ms']:.4f} ms")


if __name__ == "__main__":
    main()
