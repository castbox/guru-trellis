from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock


SKILLS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SKILLS))

from adapters.eval.owner_runtime import (
    compose_production_fixture_runtime,
    compose_review_branch_eval_runtime,
)
from adapters.eval.production_fixtures import production_task_fixture


class ActiveFixtureCompositionTests(unittest.TestCase):
    def test_planning_fixture_needs_no_retired_publication_owner(self) -> None:
        runtime = SimpleNamespace()
        with mock.patch(
            "adapters.eval.owner_runtime.load_package_owner_runtime",
            side_effect=AssertionError("retired owner must not load"),
        ):
            compose_production_fixture_runtime(Path("/unused"), runtime)

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            subprocess.run(["git", "init", "-q", "-b", "main", str(root)], check=True)
            for key, value in (("user.name", "Fixture"), ("user.email", "fixture@example.invalid")):
                subprocess.run(["git", "config", key, value], cwd=root, check=True)
            (root / ".trellis/guru-team").mkdir(parents=True)
            task, base_head = production_task_fixture(runtime, root)
            self.assertEqual(task.relative_to(root).as_posix(), ".trellis/tasks/current")
            self.assertEqual(json.loads((task / "task.json").read_text())["status"], "planning")
            self.assertEqual(len(base_head), 40)
            self.assertFalse(hasattr(runtime, "write_runtime_mappings"))

    def test_branch_fixture_uses_current_git_without_publication_owner(self) -> None:
        runtime = SimpleNamespace()
        with mock.patch(
            "adapters.eval.owner_runtime.load_package_owner_runtime",
            side_effect=AssertionError("retired owner must not load"),
        ):
            compose_review_branch_eval_runtime(Path("/unused"), runtime)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            subprocess.run(["git", "init", "-q", "-b", "main", str(root)], check=True)
            subprocess.run(["git", "config", "user.name", "Fixture"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.email", "fixture@example.invalid"], cwd=root, check=True)
            path = root / "review.json"
            runtime.write_json(path, {"review": "current"})
            self.assertEqual(runtime.read_json(path), {"review": "current"})
            subprocess.run(["git", "add", "review.json"], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "fixture"], cwd=root, check=True)
            self.assertEqual(len(runtime.current_head(root)), 40)
            self.assertEqual(runtime.diff_base_ref(root, "main"), "origin/main")
            self.assertEqual(runtime.git_status_paths(root), [])


if __name__ == "__main__":
    unittest.main()
