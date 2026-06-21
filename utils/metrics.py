from time import perf_counter


def measure_route_search(search_function, graph, start_id, goal_id):
    start_time = perf_counter()

    result = search_function(
        graph,
        start_id,
        goal_id
    )

    end_time = perf_counter()
    result["execution_time_ms"] = (end_time - start_time) * 1000

    return result
