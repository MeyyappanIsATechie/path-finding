ROAD_SPEEDS = {
    "HIGHWAY": 100,
    "ARTERIAL": 60,
    "LOCAL": 30
}


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
        self.road_type = road_type.upper()

        if self.road_type not in ROAD_SPEEDS:
            raise ValueError(f"Unknown road type: {road_type}")

    @property
    def speed(self):
        return ROAD_SPEEDS[self.road_type]

    @property
    def travel_time(self):
        return self.distance / self.speed

    @property
    def cost(self):
        return self.travel_time

    def __repr__(self):
        return (
            f"Edge("
            f"{self.source} -> {self.destination}, "
            f"distance={self.distance}, "
            f"road_type={self.road_type}, "
            f"travel_time={self.travel_time:.2f}"
            f")"
        )
