from app.cache_proxy import CacheProxyHelper


def lookup_vector(keys, client):
    helper = CacheProxyHelper()
    return helper.vector(keys, client)
