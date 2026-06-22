from models.graph import Graph
from models.node import Node
from algos.astar import astar
from algos.dijkstra import dijkstra
from sim.traffic import apply_bidirectional_traffic_condition
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


def print_route_result(label, result):
    print(f"\n{label}")
    print("-" * 50)
    print(f"Route: {' -> '.join(result['path'])}")
    print(f"Travel time: {result['cost']:.2f} hr")
    print(f"Nodes explored: {result['nodes_explored']}")
    print(f"Execution time: {result['execution_time_ms']:.4f} ms")


def compare_algorithms(city_graph, start, goal, scenario):
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

    print(f"\n{scenario}")
    print("=" * 50)
    print_route_result("Dijkstra Result", dijkstra_result)
    print_route_result("A* Result", astar_result)


def main():

    city_graph = build_city()

    city_graph.print_graph()

    start = "A"
    goal = "D"

    compare_algorithms(
        city_graph,
        start,
        goal,
        "Normal Traffic"
    )

    apply_bidirectional_traffic_condition(
        city_graph,
        "A",
        "B",
        "ACCIDENT"
    )

    city_graph.print_graph()

    compare_algorithms(
        city_graph,
        start,
        goal,
        "Accident on A-B"
    )


if __name__ == "__main__":
    main()
