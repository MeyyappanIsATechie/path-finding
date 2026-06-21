import heapq


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


def dijkstra(graph, start_id, goal_id):
    if graph.get_node(start_id) is None:
        raise ValueError(f"{start_id} does not exist")

    if graph.get_node(goal_id) is None:
        raise ValueError(f"{goal_id} does not exist")

    distances = {
        node_id: float("inf")
        for node_id in graph.nodes
    }
    parents = {
        start_id: None
    }
    visited = set()
    priority_queue = []

    distances[start_id] = 0
    heapq.heappush(priority_queue, (0, start_id))

    while priority_queue:
        current_distance, current_id = heapq.heappop(priority_queue)

        if current_id in visited:
            continue

        visited.add(current_id)

        if current_id == goal_id:
            break

        for edge in graph.get_neighbors(current_id):
            neighbor_id = edge.destination

            if neighbor_id in visited:
                continue

            new_distance = current_distance + edge.cost

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
