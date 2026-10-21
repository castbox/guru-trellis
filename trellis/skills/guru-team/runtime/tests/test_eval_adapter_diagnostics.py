"""Actual adapter subprocess failures keep their original diagnostic output."""
from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from runtime import eval_runner


class AdapterDiagnosticsTests(unittest.TestCase):
    def test_real_failure_and_invalid_response_keep_process_output(self):
        for returncode, stdout in ((4, 'partial original output'), (0, '{}')):
            with self.subTest(returncode=returncode), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                adapter = root / 'adapters/eval/failure.py'
                adapter.parent.mkdir(parents=True)
                adapter.write_text(f'#!{sys.executable}\nimport sys\n'
                    f'print({stdout!r})\nprint("original error detail", file=sys.stderr)\n'
                    f'raise SystemExit({returncode})\n')
                adapter.chmod(0o755)
                request = root / 'adapter-request.json'
                request.write_text(json.dumps({'schema_version': '1.0', 'corpus_sha256': 'a' * 64}))
                # The actual published response schema rejects the invalid object.
                (root / 'schemas').symlink_to(Path(__file__).resolve().parents[2] / 'schemas', target_is_directory=True)
                result = eval_runner.call_adapter(root, {'executable': 'failure.py', 'native_command': 'unused'}, request)
                self.assertEqual(result['capability_status'], 'execution_error')
                diagnostic = json.loads(Path(result['transcript_locator']).read_text())
                self.assertEqual(diagnostic['returncode'], returncode)
                self.assertEqual(diagnostic['stdout'], stdout + '\n')
                self.assertEqual(diagnostic['stderr'], 'original error detail\n')
                self.assertEqual('validation_error' in diagnostic, returncode == 0)


if __name__ == '__main__':
    unittest.main()
