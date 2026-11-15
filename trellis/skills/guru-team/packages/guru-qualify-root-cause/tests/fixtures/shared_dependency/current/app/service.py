from app.cache_proxy import CacheProxyHelper


def lookup_twice(key, client):
    helper = CacheProxyHelper(lambda *event: None)
    return [helper.scalar(key, client), helper.scalar(key, client)]
