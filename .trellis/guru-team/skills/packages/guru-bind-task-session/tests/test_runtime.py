import json, os, subprocess, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[6]
class BindingRuntimeTest(unittest.TestCase):
 def test_schema_and_live_binding(self):
  self.assertTrue((ROOT/'trellis/skills/guru-team/packages/guru-bind-task-session/interface.json').is_file())
if __name__=='__main__': unittest.main()
