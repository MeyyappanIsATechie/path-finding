from models.graph import Graph
from models.node import Node
from algos.astar import astar
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
        10,
        "ARTERIAL"
    )

    graph.add_bidirectional_edge(
        "A",
        "C",
        10,
        "LOCAL"
    )

    graph.add_bidirectional_edge(
        "B",
        "D",
        10,
        "HIGHWAY"
    )

    graph.add_bidirectional_edge(
        "C",
        "D",
        10,
        "LOCAL"
    )

    return graph


def main():

    city_graph = build_city()

    city_graph.print_graph()

    start = "A"
    goal = "D"

    dijkstra_result = measure_route_search(
        dijkstra,
        city_graph,
        start,
        goal
    )

    astar_result = measure_route_search(
        astar,
        city_graph,
        start,
        goal
    )

    print("\nDijkstra Result")
    print("-" * 50)
    print(f"Route: {' -> '.join(dijkstra_result['path'])}")
    print(f"Travel time: {dijkstra_result['cost']:.2f} hr")
    print(f"Nodes explored: {dijkstra_result['nodes_explored']}")
    print(f"Execution time: {dijkstra_result['execution_time_ms']:.4f} ms")

    print("\nA* Result")
    print("-" * 50)
    print(f"Route: {' -> '.join(astar_result['path'])}")
    print(f"Travel time: {astar_result['cost']:.2f} hr")
    print(f"Nodes explored: {astar_result['nodes_explored']}")
    print(f"Execution time: {astar_result['execution_time_ms']:.4f} ms")


if __name__ == "__main__":
    main()
