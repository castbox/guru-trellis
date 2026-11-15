"""Generated from schema/vector-v2.json by local-gen 2.0; SDK 0.11.2."""
SDK_VERSION = '0.11.2'


class Client:
    def fetch_scalars(self, keys):
        return {key: key.upper() for key in keys}
