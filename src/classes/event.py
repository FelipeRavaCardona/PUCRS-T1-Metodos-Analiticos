from enum import Enum

class EventType(Enum):
    ARRIVAL = "arrival"
    EXIT = "exit"
    PASS = "pass"

class Event:
    time: float
    type: EventType
    queue_name: str
    target_name: str

    def __init__(self, time: float, event_type: EventType, queue_name: str, target_name: str = None):
        self.time = time
        self.type = event_type
        self.queue_name = queue_name
        self.target_name = target_name

    def __lt__(self, other):
        return self.time < other.time

    def __repr__(self):
        return f"name: {self.queue_name}, time: {self.time}, type: {self.type}, target: {self.target_name}"
