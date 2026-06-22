import heapq
from math import sqrt

from models.edge import ROAD_SPEEDS


MAX_ROAD_SPEED = max(ROAD_SPEEDS.values())


def euclidean_distance(node1, node2):
    # Straight-line distance between two map points.
    # Think "as the crow flies" distance.
    return sqrt(
        (node1.x - node2.x) ** 2
        + (node1.y - node2.y) ** 2
    )


def estimated_travel_time(node1, node2):
    # Phase 3 and Phase 4: A* needs a smart guess.
    # We divide straight-line distance by the fastest road speed so the guess
    # stays optimistic and does not overpromise.
    return euclidean_distance(node1, node2) / MAX_ROAD_SPEED


def reconstruct_path(parents, start_id, goal_id):
    # Rebuild the final route by following parent links backward.
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
    # Phase 3: A* is like Dijkstra, but it also asks:
    # "Which option seems closest to the goal?"
    start_node = graph.get_node(start_id)
    goal_node = graph.get_node(goal_id)

    if start_node is None:
        raise ValueError(f"{start_id} does not exist")

    if goal_node is None:
        raise ValueError(f"{goal_id} does not exist")

    costs = {
        # costs stores the real travel time from start to each place.
        node_id: float("inf")
        for node_id in graph.nodes
    }
    parents = {
        start_id: None
    }
    visited = set()
    priority_queue = []

    # Start with the estimated total travel time from start to goal.
    costs[start_id] = 0
    heapq.heappush(
        priority_queue,
        (estimated_travel_time(start_node, goal_node), start_id)
    )

    while priority_queue:
        # The queue sorts by estimated total cost:
        # real cost so far + guessed cost to the goal.
        _, current_id = heapq.heappop(priority_queue)

        if current_id in visited:
            continue

        visited.add(current_id)

        if current_id == goal_id:
            break

        # Check every road leaving the current place.
        for edge in graph.get_neighbors(current_id):
            neighbor_id = edge.destination

            if neighbor_id in visited:
                continue

            new_cost = costs[current_id] + edge.cost

            # If this is the best known way to reach the neighbor, keep it.
            if new_cost < costs[neighbor_id]:
                neighbor_node = graph.get_node(neighbor_id)
                costs[neighbor_id] = new_cost
                parents[neighbor_id] = current_id

                # A* chooses what to explore next using:
                # travel time so far + best guess for the remaining travel time.
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
