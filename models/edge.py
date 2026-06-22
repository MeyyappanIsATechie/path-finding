ROAD_SPEEDS = {
    "HIGHWAY": 100,
    "ARTERIAL": 60,
    "LOCAL": 30
}

DEFAULT_TRAFFIC_STATUS = "NORMAL"


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
        self.traffic_status = DEFAULT_TRAFFIC_STATUS
        self.traffic_multiplier = 1
        self.is_closed = False

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
        if self.is_closed:
            return float("inf")

        return self.travel_time * self.traffic_multiplier

    def apply_traffic(self, status, multiplier=1, is_closed=False):
        self.traffic_status = status.upper()
        self.traffic_multiplier = multiplier
        self.is_closed = is_closed

    def reset_traffic(self):
        self.apply_traffic(DEFAULT_TRAFFIC_STATUS)

    def __repr__(self):
        return (
            f"Edge("
            f"{self.source} -> {self.destination}, "
            f"distance={self.distance}, "
            f"road_type={self.road_type}, "
            f"traffic={self.traffic_status}, "
            f"cost={self.cost:.2f}"
            f")"
        )
