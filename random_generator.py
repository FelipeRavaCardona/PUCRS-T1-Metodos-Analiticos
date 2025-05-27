class RandomGenerator:
    def __init__(self, seed, A, C, M):
        self.a = A
        self.c = C
        self.m = M
        self.seed = seed

    def generate(self):
        x = self.seed
        while True:
            x = (self.a * x + self.c) % self.m
            yield x / self.m