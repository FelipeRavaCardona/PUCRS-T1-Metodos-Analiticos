class Route:
    source: str
    target: str
    probability: float

    def __init__(self, source: str, target: str, probability: float):
        self.source = source
        self.target = target
        self.probability = probability

    def __repr__(self):
        return f"source: {self.source}, target: {self.target}, probability: {self.probability}"