import json,unittest
from pathlib import Path
class ContractTest(unittest.TestCase):
 def test_interface_declares_unique_routes(self):
  p=Path(__file__).resolve().parents[1]; i=json.loads((p/'interface.json').read_text()); exits=[x['id'] for x in i['external_exits']]; self.assertEqual(len(exits),len(set(exits))); self.assertEqual(i['judgment_mode'],'semantic')
if __name__=='__main__': unittest.main()
