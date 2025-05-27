class Queue:
    def __init__(self, name, servers, capacity, min_arrival, max_arrival, min_service, max_service):
        self.name = name
        self.servers = servers
        self.capacity = capacity
        self.min_arrival = min_arrival
        self.max_arrival = max_arrival
        self.min_service = min_service
        self.max_service = max_service

        self.queue = []
        self.in_service = 0
    
    def is_full(self):
        return len(self.queue) + self.in_service >= self.capacity