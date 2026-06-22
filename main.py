from models.graph import Graph
from models.node import Node
from algos.astar import astar
from algos.dijkstra import dijkstra
from sim.traffic import apply_bidirectional_traffic_condition
from utils.metrics import measure_route_search


def build_city():
    # Phase 1: Build a tiny city map.
    # Each node is a place, and each edge is a road between two places.

    graph = Graph()

    # The x and y numbers are simple map positions.
    # A* uses these positions to guess which road is closer to the destination.
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

    # Phase 4: Roads now have types.
    # The same distance can take different time depending on the road speed.
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
    # Print one algorithm's answer in a readable way.
    # The result dictionary comes from Dijkstra or A*.
    print(f"\n{label}")
    print("-" * 50)
    print(f"Route: {' -> '.join(result['path'])}")
    print(f"Travel time: {result['cost']:.2f} hr")
    print(f"Nodes explored: {result['nodes_explored']}")
    print(f"Execution time: {result['execution_time_ms']:.4f} ms")


def compare_algorithms(city_graph, start, goal, scenario):
    # Phase 2 and Phase 3: Run both path-finding algorithms on the same map.
    # This lets us compare route, travel time, explored nodes, and speed.
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

    # Show the city before any route search happens.
    city_graph.print_graph()

    start = "A"
    goal = "D"

    compare_algorithms(
        city_graph,
        start,
        goal,
        "Normal Traffic"
    )

    # Phase 5: Change the road conditions after the graph is already built.
    # An accident makes A-B much slower, so the best route should change.
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
