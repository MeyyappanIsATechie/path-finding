from models.node import Node
from models.edge import Edge


class Graph:
    # The Graph is the whole city map.
    # nodes stores places, and adjacency_list stores roads leaving each place.

    def __init__(self):
        self.nodes = {}
        self.adjacency_list = {}

    def add_node(self, node: Node):

        # Add a place to the city if it is not already there.
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

        # A road only makes sense if both places already exist.
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

        # Most roads can be driven both ways, so add one edge in each direction.
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

        # Return all roads that leave this place.
        return self.adjacency_list[node_id]

    def get_edge(self, source: str, destination: str):
        # Find one exact road, like A -> B.
        # Traffic simulation uses this to slow down or close a road.
        for edge in self.get_neighbors(source):
            if edge.destination == destination:
                return edge

        return None

    def get_node(self, node_id: str):

        # Return a place by its id, or None if it does not exist.
        return self.nodes.get(node_id)

    def print_graph(self):

        # Print every place and the roads leaving from it.
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
