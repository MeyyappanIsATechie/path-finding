class Edge:
    def __init__(
        self,
        source: str,
        destination: str,
        distance: float,
        road_type: str = "LOCAL"
    ):
        self.source = source
        self.destination = destination
        self.distance = distance
        self.road_type = road_type

    def __repr__(self):
        return (
            f"Edge("
            f"{self.source} -> {self.destination}, "
            f"distance={self.distance}"
            f")"
        )