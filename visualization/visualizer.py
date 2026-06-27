import matplotlib.pyplot as plt


ROAD_COLORS = {
    "HIGHWAY": "#2563eb",
    "ARTERIAL": "#f97316",
    "LOCAL": "#64748b"
}

TRAFFIC_COLORS = {
    "NORMAL": "#475569",
    "CONGESTION": "#eab308",
    "ACCIDENT": "#dc2626",
    "CONSTRUCTION": "#9333ea",
    "CLOSED": "#111827"
}


def _path_edges(path):
    edges = set()

    for index in range(len(path) - 1):
        edges.add((path[index], path[index + 1]))
        edges.add((path[index + 1], path[index]))

    return edges


def _edge_key(source, destination):
    return tuple(sorted((source, destination)))


def _draw_edge(ax, graph, edge, drawn_edges, route_edges):
    key = _edge_key(edge.source, edge.destination)

    if key in drawn_edges:
        return

    drawn_edges.add(key)

    source = graph.get_node(edge.source)
    destination = graph.get_node(edge.destination)
    is_route_edge = (edge.source, edge.destination) in route_edges
    color = "#16a34a" if is_route_edge else TRAFFIC_COLORS.get(
        edge.traffic_status,
        ROAD_COLORS[edge.road_type]
    )
    line_width = 4 if is_route_edge else 2
    alpha = 1 if is_route_edge else 0.7
    style = "--" if edge.is_closed else "-"

    ax.plot(
        [source.x, destination.x],
        [source.y, destination.y],
        color=color,
        linewidth=line_width,
        alpha=alpha,
        linestyle=style,
        zorder=1
    )

    mid_x = (source.x + destination.x) / 2
    mid_y = (source.y + destination.y) / 2

    ax.text(
        mid_x,
        mid_y,
        f"{edge.road_type.title()}\n{edge.cost:.2f} hr",
        fontsize=8,
        ha="center",
        va="center",
        bbox={
            "boxstyle": "round,pad=0.2",
            "facecolor": "white",
            "edgecolor": "none",
            "alpha": 0.8
        },
        zorder=3
    )


def _draw_nodes(ax, graph, explored_nodes, path):
    path_nodes = set(path)

    for node_id, node in graph.nodes.items():
        if node_id in path_nodes:
            color = "#16a34a"
            size = 520
        elif node_id in explored_nodes:
            color = "#facc15"
            size = 420
        else:
            color = "#e2e8f0"
            size = 360

        ax.scatter(
            node.x,
            node.y,
            s=size,
            color=color,
            edgecolor="#0f172a",
            linewidth=1.5,
            zorder=4
        )
        ax.text(
            node.x,
            node.y,
            node_id,
            fontsize=11,
            fontweight="bold",
            ha="center",
            va="center",
            color="#0f172a",
            zorder=5
        )


def visualize_route(graph, result, title="Route Visualization", save_path=None, show=True):
    path = result.get("path", [])
    explored_nodes = set(result.get("explored_order", []))
    route_edges = _path_edges(path)
    drawn_edges = set()

    fig, ax = plt.subplots(figsize=(8, 6))
    fig.patch.set_facecolor("#f8fafc")
    ax.set_facecolor("#f8fafc")

    for edges in graph.adjacency_list.values():
        for edge in edges:
            _draw_edge(ax, graph, edge, drawn_edges, route_edges)

    _draw_nodes(ax, graph, explored_nodes, path)

    ax.set_title(title, fontsize=14, fontweight="bold", pad=14)
    ax.set_aspect("equal", adjustable="datalim")
    ax.grid(True, color="#cbd5e1", linewidth=0.8, alpha=0.7)
    ax.set_xlabel("X position")
    ax.set_ylabel("Y position")

    if save_path is not None:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")

    if show:
        plt.show()
    else:
        plt.close(fig)
