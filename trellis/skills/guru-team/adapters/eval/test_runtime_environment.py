"""Environment selection stays independent of business fixture residue."""
from pathlib import Path
import tempfile
import unittest

from adapters.eval.eval_support import runtime_residue
from runtime.bootstrap import active_pointer_path


class RuntimeEnvironmentTests(unittest.TestCase):
    def test_environment_is_preserved_and_other_runtime_files_remain_residue(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            selection = active_pointer_path(repo)
            selection.parent.mkdir(parents=True)
            selection.write_bytes(b"environment-owner fixture\n")
            before = selection.read_bytes()
            self.assertEqual([], runtime_residue(repo))
            leftover = repo / ".trellis/.runtime/guru-team/evals/owner-result.json"
            leftover.parent.mkdir(parents=True)
            leftover.write_bytes(b"unfinished owner fixture\n")
            self.assertEqual([leftover], runtime_residue(repo))
            self.assertEqual(before, selection.read_bytes())


if __name__ == "__main__":
    unittest.main()
