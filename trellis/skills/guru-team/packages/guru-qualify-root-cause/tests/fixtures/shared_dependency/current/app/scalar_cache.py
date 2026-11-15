class ScalarCache:
    def __init__(self):
        self.values = {}

    def get_or_load(self, key, load):
        if key not in self.values:
            self.values[key] = load(key)
        return self.values[key]
