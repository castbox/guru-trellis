from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[5]
SCRIPT = REPO / "trellis/presets/guru-team/scripts/python/verify_installed_parallel_finish.py"


def load_module():
    spec = importlib.util.spec_from_file_location("verify_installed_parallel_finish", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load parallel Finish verifier")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class InstalledParallelFinishTests(unittest.TestCase):
    def test_real_git_fixture_preserves_isolation_and_reachability(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as directory:
            result = module.run_fixture(REPO, Path(directory) / "fixture")
        self.assertEqual(result["status"], "passed")
        self.assertEqual(result["metadata_intersection"], [])
        for token in ("a", "b"):
            case = result[token]
            self.assertEqual(case["phase0"]["step_count"], 6)
            self.assertEqual(case["planning"], "passed")
            self.assertEqual(case["phase2_check"], "passed")
            self.assertEqual(case["branch_review"], "passed")
            self.assertEqual(case["publication_review"], "passed")
        self.assertTrue(result["a"]["provider_failure_recovered"])
        self.assertEqual(result["b"]["github_pr_call_count"], 0)
        self.assertFalse(result["b"]["workspace_journal_tracked"])
        self.assertTrue(result["cleanup_failure_recovered"])
        self.assertFalse(result["a"]["real_github_verified"])
        self.assertEqual(
            [row["order"] for row in result["merge_orders"]],
            [["a", "b"], ["b", "a"]],
        )
        self.assertTrue(result["protected_commits_reachable_after_cleanup"])


if __name__ == "__main__":
    unittest.main()
