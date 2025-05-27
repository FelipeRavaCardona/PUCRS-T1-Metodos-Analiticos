from random_generator import RandomGenerator
from simulated_queue import Queue

class Networking:
    def __init__(self, target, probability):
        self.target = target
        self.probability = probability

    def __repr__(self):
        return f"Networking(target={self.target}, probability={self.probability})"

class QueueNetwork:
    def __init__(self, seed, first_arrival, random_numbers_amount=100000):
        self.used = 0
        self.random_numbers_amount = random_numbers_amount
        self.current_time = 0.0
        self.next_arrival = first_arrival
        self.queues = []
        self.network = {}
        self.generator = RandomGenerator(seed)

    def next_random(self):
        return next(self.generator.generate())
    
    def next_uniform(self, min_value, max_value):
        return min_value + (max_value - min_value) * self.next_random()
    
    def next_external_arrival(self):
        self.next_arrival = self.current_time + self.next_uniform(self.queues[0].min_arrival, self.queues[0].max_arrival)              

    def __repr__(self):
        return f"QueueNetwork(queues={self.queues}, network={self.network})"