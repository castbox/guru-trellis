"""Frozen local observation: scalar caller, SDK 0.11.1, no network."""
import json
from app.generated_client import Client, SDK_VERSION
from app.service import lookup_twice

client = Client()
values = lookup_twice('pear', client)
assert values == ['PEAR', 'PEAR']
assert client.calls == ['pear']
print(json.dumps({'sdk': SDK_VERSION, 'input': 'pear', 'values': values,
                  'backend_calls': client.calls, 'transport': 'local pure Python'}))
