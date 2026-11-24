class Catalog:
    def __init__(self, provider, clock):
        self.provider = provider
        self.clock = clock
    def get(self):
        return self.provider()
