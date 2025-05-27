class Queue:
    def __init__(self, name, servers=1, capacity=float('inf'), min_arrival=None, max_arrival=None, min_service=None, max_service=None):
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

    def add_customer(self, customer):
        if not self.is_full():
            self.queue.append(customer)
            return True
        return False

    def start_service(self):
        if self.queue and self.in_service < self.servers:
            self.in_service += 1
            return self.queue.pop(0)
        return None

    def finish_service(self):
        if self.in_service > 0:
            self.in_service -= 1

    def __repr__(self):
        return f"<Queue {self.name}: {len(self.queue)} waiting, {self.in_service} in service>"
