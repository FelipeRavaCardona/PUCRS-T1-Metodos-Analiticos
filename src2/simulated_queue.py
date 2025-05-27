class Queue:
    def __init__(self, name, servers, capacity, min_service, max_service, min_arrival=-1, max_arrival=-1):
        self.name = name
        self.servers = servers
        self.capacity = capacity
        self.min_arrival = min_arrival
        self.max_arrival = max_arrival
        self.min_service = min_service
        self.max_service = max_service

        self.losses = 0
        self.queue = 0
        self.in_service = 0

        self.end_time_next_service = [float('inf')] * servers

        

    def free_slots(self):
        return self.queue < self.servers + self.capacity

    def lose_customer(self):
        self.losses += 1

    def add_to_queue(self):
        if self.free_slots():
            self.queue += 1
        else:
            self.lose_customer()

    def free_servers(self):
        return self.servers - self.in_service
    
    def start_service(self, current_time, service_time):
        for i in range(self.servers):
            if self.end_time_next_service[i] == float('inf'):
                self.end_time_next_service[i] = current_time + service_time
                self.in_service += 1
                return

    def next_server(self):
        shortest_time = float('inf')
        index = -1
        for i in range(self.servers):
            if self.end_time_next_service[i] < shortest_time:
                shortest_time = self.end_time_next_service[i]
                index = i
        return index

    def __repr__(self):
        return self.name