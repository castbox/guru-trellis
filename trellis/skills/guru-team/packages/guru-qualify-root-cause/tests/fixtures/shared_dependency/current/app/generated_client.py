"""Generated from schema/scalar-v1.json by local-gen 1.0; SDK 0.11.1."""
SDK_VERSION = '0.11.1'


class Client:
    def __init__(self):
        self.calls = []

    def fetch_scalar(self, key):
        self.calls.append(key)
        return key.upper()
