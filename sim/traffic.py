TRAFFIC_CONDITIONS = {
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
    condition_name = condition.upper()

    if condition_name not in TRAFFIC_CONDITIONS:
        raise ValueError(f"Unknown traffic condition: {condition}")

    edge = graph.get_edge(source, destination)

    if edge is None:
        raise ValueError(f"No road exists from {source} to {destination}")

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
    for edges in graph.adjacency_list.values():
        for edge in edges:
            edge.reset_traffic()
