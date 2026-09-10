"""Regression coverage for documented preparation and stale same-version builds."""
from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

import test_verify_trellis_upgrade_contract as upgrade_tests

ROOT = Path(__file__).resolve().parents[5]


class ForkPreparationTests(unittest.TestCase):
    def test_readme_stops_on_each_preparation_failure(self):
        snippet = (ROOT / "README.md").read_text().split("```bash\n", 1)[1].split("```", 1)[0]
        lock = json.loads((ROOT / "trellis/presets/guru-team/source/trellis-source.json").read_text())
        for failure in ("status", "dirty", "fetch", "checkout", "sha", "install", "build", ""):
            with self.subTest(failure=failure), tempfile.TemporaryDirectory(prefix="fork-prepare-") as tmp:
                work = Path(tmp)
                fork, commands = work / "fork", work / "bin"
                fork.mkdir()
                commands.mkdir()
                node_marker = work / "node-ran"
                bodies = {
                    "git": '''#!/bin/sh
case "$*" in
  *"status --porcelain"*)
    [ "$FAILURE" != status ] || exit 9
    [ "$FAILURE" != dirty ] || echo " M ordinary-local-edit"
    ;;
  *fetch*) [ "$FAILURE" != fetch ] || exit 9 ;;
  *checkout*) [ "$FAILURE" != checkout ] || exit 9 ;;
  *"rev-parse HEAD"*)
    if [ "$FAILURE" = sha ]; then echo wrong; else echo "$EXPECTED_SHA"; fi
    ;;
esac
exit 0
''',
                    "pnpm": '''#!/bin/sh
[ "$FAILURE" != "$1" ] || exit 7
if [ "$1" = build ]; then mkdir -p packages/cli/dist; fi
exit 0
''',
                    "node": '#!/bin/sh\nprintf ran > "$NODE_MARKER"\n',
                }
                for name, body in bodies.items():
                    path = commands / name
                    path.write_text(body)
                    path.chmod(0o755)
                result = subprocess.run(["bash", "-c", snippet], capture_output=True, text=True, env={
                    **os.environ, "PATH": str(commands) + os.pathsep + os.environ["PATH"],
                    "GURU_SOURCE": str(ROOT), "FORK_SOURCE": str(fork),
                    "TARGET_REPO": str(work / "target"), "EXPECTED_SHA": lock["commit"],
                    "FAILURE": failure, "NODE_MARKER": str(node_marker),
                })
                origin = fork / "packages/cli/dist/.guru-source-commit"
                if failure:
                    self.assertNotEqual(result.returncode, 0)
                    self.assertFalse(node_marker.exists())
                    self.assertFalse(origin.exists())
                else:
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertTrue(node_marker.exists())
                    self.assertEqual(origin.read_text().strip(), lock["commit"])

    def test_same_version_checkout_without_rebuild_is_rejected(self):
        matrix = upgrade_tests.load_matrix_helper()
        with tempfile.TemporaryDirectory(prefix="stale-build-") as tmp:
            repo, fork = upgrade_tests.VerifyTrellisUpgradeContractTests().fork_fixture(Path(tmp))
            matrix.validate_fork_source(repo, fork)
            source = fork / "packages/cli/src/cli/index.ts"
            source.parent.mkdir(parents=True)
            source.write_text('console.log("changed behavior, unchanged release version");\n')
            subprocess.run(["git", "add", "."], cwd=fork, check=True)
            subprocess.run(["git", "-c", "core.hooksPath=/dev/null", "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "same-version behavior change"], cwd=fork, check=True)
            lock_path = repo / "trellis/presets/guru-team/source/trellis-source.json"
            lock = json.loads(lock_path.read_text())
            lock["commit"] = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=fork, text=True).strip()
            lock_path.write_text(json.dumps(lock))
            # A normal checkout/lock advance left the prior successful build.
            with self.assertRaisesRegex(matrix.MatrixError, "stale fork build origin"):
                matrix.validate_fork_source(repo, fork)


if __name__ == "__main__":
    unittest.main()
