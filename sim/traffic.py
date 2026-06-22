TRAFFIC_CONDITIONS = {
    # Phase 5: Traffic changes the cost of roads.
    # multiplier 1 means normal time, 2 means twice as slow, and so on.
    "NORMAL": {
        "multiplier": 1,
        "is_closed": False
    },
    "CONGESTION": {
        "multiplier": 1.75,
        "is_closed": False
    },
    "ACCIDENT": {
        "multiplier": 4,
        "is_closed": False
    },
    "CONSTRUCTION": {
        "multiplier": 2.5,
        "is_closed": False
    },
    "CLOSED": {
        "multiplier": 1,
        "is_closed": True
    }
}


def apply_traffic_condition(graph, source, destination, condition):
    # Apply traffic to one direction of a road, such as A -> B.
    condition_name = condition.upper()

    if condition_name not in TRAFFIC_CONDITIONS:
        raise ValueError(f"Unknown traffic condition: {condition}")

    edge = graph.get_edge(source, destination)

    if edge is None:
        raise ValueError(f"No road exists from {source} to {destination}")

    # Copy the chosen traffic settings onto the edge.
    traffic = TRAFFIC_CONDITIONS[condition_name]
    edge.apply_traffic(
        condition_name,
        traffic["multiplier"],
        traffic["is_closed"]
    )


def apply_bidirectional_traffic_condition(
    graph,
    node1,
    node2,
    condition
):
    # Apply the same traffic both ways.
    # This is useful for a two-way road where both directions are affected.
    apply_traffic_condition(
        graph,
        node1,
        node2,
        condition
    )
    apply_traffic_condition(
        graph,
        node2,
        node1,
        condition
    )


def reset_traffic(graph):
    # Put every road in the city back to normal traffic.
    for edges in graph.adjacency_list.values():
        for edge in edges:
            edge.reset_traffic()
