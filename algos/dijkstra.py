import heapq


def reconstruct_path(parents, start_id, goal_id):
    # The algorithms remember "how we reached each place" in parents.
    # This walks backward from the goal to rebuild the final route.
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


def dijkstra(graph, start_id, goal_id):
    # Phase 2: Dijkstra checks the cheapest known route first.
    # It does not guess. It slowly expands outward until it reaches the goal.
    if graph.get_node(start_id) is None:
        raise ValueError(f"{start_id} does not exist")

    if graph.get_node(goal_id) is None:
        raise ValueError(f"{goal_id} does not exist")

    distances = {
        # At the beginning, every place looks unreachable.
        # infinity means "we do not know a route yet".
        node_id: float("inf")
        for node_id in graph.nodes
    }
    parents = {
        start_id: None
    }
    visited = set()
    priority_queue = []

    # The start point costs 0 because we are already there.
    distances[start_id] = 0
    heapq.heappush(priority_queue, (0, start_id))

    while priority_queue:
        # heapq gives us the place with the lowest travel time so far.
        current_distance, current_id = heapq.heappop(priority_queue)

        if current_id in visited:
            continue

        visited.add(current_id)

        if current_id == goal_id:
            break

        # Try every road leaving the current place.
        for edge in graph.get_neighbors(current_id):
            neighbor_id = edge.destination

            if neighbor_id in visited:
                continue

            new_distance = current_distance + edge.cost

            # If this route is better than the old one, remember it.
            if new_distance < distances[neighbor_id]:
                distances[neighbor_id] = new_distance
                parents[neighbor_id] = current_id
                heapq.heappush(
                    priority_queue,
                    (new_distance, neighbor_id)
                )

    path = reconstruct_path(
        parents,
        start_id,
        goal_id
    )

    return {
        "path": path,
        "cost": distances[goal_id],
        "nodes_explored": len(visited),
        "explored_order": list(visited)
    }
