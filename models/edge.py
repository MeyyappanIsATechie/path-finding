ROAD_SPEEDS = {
    # Phase 4: Each road type has a speed.
    # Higher speed means the same distance takes less time.
    "HIGHWAY": 100,
    "ARTERIAL": 60,
    "LOCAL": 30
}

DEFAULT_TRAFFIC_STATUS = "NORMAL"


class Edge:
    # An Edge is one road from one place to another.
    # Example: A -> B is separate from B -> A, even if both represent the same street.
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

        # Phase 5: Traffic starts as normal.
        # Later, traffic can make this road slower or completely closed.
        self.traffic_status = DEFAULT_TRAFFIC_STATUS
        self.traffic_multiplier = 1
        self.is_closed = False

        if self.road_type not in ROAD_SPEEDS:
            raise ValueError(f"Unknown road type: {road_type}")

    @property
    def speed(self):
        # Look up the speed from the road type.
        return ROAD_SPEEDS[self.road_type]

    @property
    def travel_time(self):
        # Basic time formula: time = distance / speed.
        return self.distance / self.speed

    @property
    def cost(self):
        # Algorithms use "cost" to mean "how expensive this road is to use".
        # In this project, cost means travel time.
        if self.is_closed:
            return float("inf")

        return self.travel_time * self.traffic_multiplier

    def apply_traffic(self, status, multiplier=1, is_closed=False):
        # A multiplier makes a road slower.
        # Example: multiplier 4 means the road takes 4 times longer.
        self.traffic_status = status.upper()
        self.traffic_multiplier = multiplier
        self.is_closed = is_closed

    def reset_traffic(self):
        # Put the road back to its original normal condition.
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
