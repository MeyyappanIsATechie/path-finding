from models.node import Node
from models.edge import Edge


class Graph:

    def __init__(self):
        self.nodes = {}
        self.adjacency_list = {}

    def add_node(self, node: Node):

        if node.id not in self.nodes:
            self.nodes[node.id] = node
            self.adjacency_list[node.id] = []

    def add_edge(
        self,
        source: str,
        destination: str,
        distance: float,
        road_type: str = "LOCAL"
    ):

        if source not in self.nodes:
            raise ValueError(f"{source} does not exist")

        if destination not in self.nodes:
            raise ValueError(f"{destination} does not exist")

        edge = Edge(
            source,
            destination,
            distance,
            road_type
        )

        self.adjacency_list[source].append(edge)

    def add_bidirectional_edge(
        self,
        node1: str,
        node2: str,
        distance: float,
        road_type: str = "LOCAL"
    ):

        self.add_edge(
            node1,
            node2,
            distance,
            road_type
        )

        self.add_edge(
            node2,
            node1,
            distance,
            road_type
        )

    def get_neighbors(self, node_id: str):

        return self.adjacency_list[node_id]

    def get_edge(self, source: str, destination: str):
        for edge in self.get_neighbors(source):
            if edge.destination == destination:
                return edge

        return None

    def get_node(self, node_id: str):

        return self.nodes.get(node_id)

    def print_graph(self):

        print("\nCity Road Network")
        print("-" * 50)

        for node_id, edges in self.adjacency_list.items():

            print(f"{node_id} -> ", end="")

            neighbors = []

            for edge in edges:
                neighbors.append(
                    f"{edge.destination} "
                    f"({edge.road_type}, "
                    f"{edge.traffic_status}, "
                    f"{edge.cost:.2f} hr)"
                )

            print(", ".join(neighbors))
