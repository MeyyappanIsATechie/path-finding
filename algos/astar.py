import heapq
from math import sqrt

from models.edge import ROAD_SPEEDS


MAX_ROAD_SPEED = max(ROAD_SPEEDS.values())


def euclidean_distance(node1, node2):
    return sqrt(
        (node1.x - node2.x) ** 2
        + (node1.y - node2.y) ** 2
    )


def estimated_travel_time(node1, node2):
    return euclidean_distance(node1, node2) / MAX_ROAD_SPEED


def reconstruct_path(parents, start_id, goal_id):
    path = []
    current = goal_id

    while current is not None:
        path.append(current)

        if current == start_id:
            break

        current = parents.get(current)

    path.reverse()

    if not path or path[0] != start_id:
        return []

    return path


def astar(graph, start_id, goal_id):
    start_node = graph.get_node(start_id)
    goal_node = graph.get_node(goal_id)

    if start_node is None:
        raise ValueError(f"{start_id} does not exist")

    if goal_node is None:
        raise ValueError(f"{goal_id} does not exist")

    costs = {
        node_id: float("inf")
        for node_id in graph.nodes
    }
    parents = {
        start_id: None
    }
    visited = set()
    priority_queue = []

    costs[start_id] = 0
    heapq.heappush(
        priority_queue,
        (estimated_travel_time(start_node, goal_node), start_id)
    )

    while priority_queue:
        _, current_id = heapq.heappop(priority_queue)

        if current_id in visited:
            continue

        visited.add(current_id)

        if current_id == goal_id:
            break

        for edge in graph.get_neighbors(current_id):
            neighbor_id = edge.destination

            if neighbor_id in visited:
                continue

            new_cost = costs[current_id] + edge.cost

            if new_cost < costs[neighbor_id]:
                neighbor_node = graph.get_node(neighbor_id)
                costs[neighbor_id] = new_cost
                parents[neighbor_id] = current_id

                estimated_total_cost = (
                    new_cost
                    + estimated_travel_time(neighbor_node, goal_node)
                )
                heapq.heappush(
                    priority_queue,
                    (estimated_total_cost, neighbor_id)
                )

    path = reconstruct_path(
        parents,
        start_id,
        goal_id
    )

    return {
        "path": path,
        "cost": costs[goal_id],
        "nodes_explored": len(visited),
        "explored_order": list(visited)
    }
