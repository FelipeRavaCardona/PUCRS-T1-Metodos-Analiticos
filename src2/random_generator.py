class RandomGenerator:
    def __init__(self, seed):
        self.a = 1140671485
        self.c = 12820163
        self.m = 2124325123
        self.seed = seed

    def generate(self):
        x = self.seed
        while True:
            x = (self.a * x + self.c) % self.m
            yield x / self.m