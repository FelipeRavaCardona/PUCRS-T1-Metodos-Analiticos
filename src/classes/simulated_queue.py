from classes.route import Route

class Queue:
    name: str
    servers: int
    capacity: int
    min_arrival: float
    max_arrival: float
    min_service: float
    max_service: float

    routes: Route

    status: int
    losses: int
    times: list[float]

    def __init__(self, name: str, servers: int, capacity: int = float('inf'),
                 min_arrival: float = -1, max_arrival: float = -1,
                 min_service: float = 0, max_service: float = 0):
        self.name = name
        self.servers = servers
        self.capacity = capacity
        self.min_arrival = min_arrival
        self.max_arrival = max_arrival
        self.min_service = min_service
        self.max_service = max_service

        self.routes: list[Route] = []

        self.status = 0
        self.losses = 0

        if not isinstance(capacity, int) or capacity == float('inf'):
            self.times = [0.0] * (100000 + 1)
        else:
            self.times = [0.0] * (capacity + 1)

    def customer_in(self):
        self.status += 1

    def customer_out(self):
        self.status -= 1

    def customer_lost(self):
        self.losses += 1

    def __repr__(self):
        return f"name: {self.name}, losses: {self.losses}"