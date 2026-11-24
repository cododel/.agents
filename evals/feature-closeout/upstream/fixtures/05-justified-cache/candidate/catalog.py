from copy import deepcopy

class Catalog:
    def __init__(self, provider, clock):
        self.provider = provider
        self.clock = clock
        self.cached = None
        self.fetched_at = None
    def get(self):
        if self.fetched_at is not None and self.clock() - self.fetched_at < 60:
            return deepcopy(self.cached)
        value = self.provider()
        self.cached = deepcopy(value)
        self.fetched_at = self.clock()
        return deepcopy(value)
