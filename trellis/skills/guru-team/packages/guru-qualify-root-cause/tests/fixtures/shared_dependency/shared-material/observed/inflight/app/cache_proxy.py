from app.scalar_cache import ScalarCache


class CacheProxyHelper:
    def __init__(self, logger):
        self.logger = logger
        self.cache = ScalarCache()

    def scalar(self, key, client):
        self.logger('scalar', key)
        return self.cache.get_or_load(key, client.fetch_scalar)

    def vector(self, keys, client):
        return [self.cache.get_or_load(key, client.fetch_scalar) for key in keys]
