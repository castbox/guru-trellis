from __future__ import annotations

import json
import unittest
from pathlib import Path


class RepresentativePackageContractTests(unittest.TestCase):
    def test_interface_points_to_this_test_evidence(self) -> None:
        package = Path(__file__).resolve().parents[1]
        interface = json.loads((package / "interface.json").read_text(encoding="utf-8"))

        self.assertEqual(interface["id"], "guru-example-action")
        self.assertIn("tests/test_contract.py", interface["tests"])


if __name__ == "__main__":
    unittest.main()
