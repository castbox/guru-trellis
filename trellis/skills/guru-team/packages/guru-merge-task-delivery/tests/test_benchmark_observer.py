"""Measurement correctness against real Git protocols and root selection."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from benchmark_observer import protocol, summarize
from benchmark_profile import observe_hashes, selected_function
from benchmark_git_objects import instrument_wrapper, profile_runtime_root


class ObserverTests(unittest.TestCase):
    def test_real_git_protocols_at_distinct_roots(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / 'observations'
            output.mkdir()
            realgit = shutil.which('git')
            for ordinal, protocol_flag in enumerate(('--batch', '--batch-check', '--batch-command')):
                repo = root / str(ordinal)
                repo.mkdir()
                subprocess.run([realgit, 'init', '-q', str(repo)], check=True)
                oid = subprocess.run([realgit, '-C', str(repo), 'hash-object', '-w', '--stdin'],
                                     input=b'abc', capture_output=True, check=True).stdout.decode().strip()
                data = ((f'info {oid}\ncontents {oid}\nflush\n') if protocol_flag == '--batch-command'
                        else oid + '\n')
                request = root / 'stdin'
                request.write_text(data)
                with request.open('rb') as stream:
                    result = subprocess.run([sys.executable, str(Path(__file__).with_name('benchmark_observer.py')),
                        str(output), realgit, '-C', str(repo), 'cat-file', protocol_flag, *(['--buffer'] if protocol_flag == '--batch-command' else [])], stdin=stream,
                        env={**os.environ, 'GURU_BENCH_SAMPLE': str(ordinal)}, capture_output=True)
                self.assertEqual(result.returncode, 0, result.stderr)
            volume = summarize(output, realgit)
            self.assertEqual(volume['requested_objects'], 2)
            self.assertEqual(volume['successful_content_bytes'], 6)
            self.assertEqual(volume['unique_content_bytes'], 3)
            self.assertEqual(volume['metadata_requests'], 2)
            self.assertEqual(volume['control_requests'], {'flush': 1})
            self.assertEqual(volume['uncaptured_batch_commands'], 0)
            self.assertEqual(volume['unavailable_at_post_probe'], [])
            self.assertEqual({row['sample'] for row in volume['commands']}, {'0', '1', '2'})
            self.assertEqual({row['actual_root'] for row in volume['commands']},
                             {str((root / str(i)).resolve()) for i in range(3)})

    def test_profile_runtime_source_and_installed_layouts(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for base, relative in ((root / 'canonical', 'packages/skill'),
                                   (root / 'installed', 'skills/packages/skill')):
                package = base / relative
                package.mkdir(parents=True)
                (base / 'runtime').mkdir()
                (base / 'runtime/command.py').write_text('')
                self.assertEqual(profile_runtime_root(package), base)

    def test_non_json_profile_failure_retains_process_facts(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'runtime').mkdir()
            (root / 'runtime/command.py').write_text('')
            flow = SimpleNamespace()
            case = SimpleNamespace(flow=flow, repo=root, assertEqual=self.assertEqual)
            args = SimpleNamespace(measurement='profile', output=root)
            instrument_wrapper(case, args, root)
            failure = subprocess.CompletedProcess([], 17, '', 'ordinary import failure\n')
            with patch('subprocess.run', return_value=failure):
                with self.assertRaisesRegex(RuntimeError, 'non-JSON, exit=17'):
                    flow.wrapper('skill', 'invoke.sh')
            process = json.loads((root / 'profile-0.process.json').read_text())
            self.assertEqual(process['exit_code'], 17)
            self.assertEqual((root / 'profile-0.stderr').read_text(), 'ordinary import failure\n')

    def test_scalar_metadata_and_body(self):
        self.assertEqual(protocol(['cat-file', '-e', 'abc'], [])[1], {'abc': 1})
        self.assertEqual(protocol(['cat-file', 'blob', 'abc'], [])[0], {'abc': 1})
        self.assertTrue(selected_function('/common/delivery_store.py', 'GitCandidateContent.content_ref'))
        self.assertTrue(selected_function('/common/delivery_store.py', '_ContentObservation.content_ref'))
        self.assertFalse(selected_function('/elsewhere.py', 'GitCandidateContent.content_ref'))
        self.assertFalse(selected_function('/common/delivery_store.py', 'content_ref'))

    def test_hash_and_file_observation_delegates_real_implementation(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'delivery_store.py'
            path.write_text('from pathlib import Path\nimport hashlib\n'
                            'def _candidate_content_ref(path):\n'
                            ' with path.open("rb") as stream:\n'
                            '  digest=hashlib.sha256()\n'
                            '  digest.update(stream.read())\n'
                            '  return digest.hexdigest()\n')
            spec = importlib.util.spec_from_file_location('observer_fixture', path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            data = Path(directory) / 'data'
            data.write_bytes(b'abc')
            import io
            original_sha, original_open = hashlib.sha256, io.open
            try:
                counts = observe_hashes()
                self.assertEqual(module._candidate_content_ref(data), original_sha(b'abc').hexdigest())
                self.assertEqual(sum(v for (metric, _), v in counts.items() if metric == 'sha256_input_bytes'), 3)
                self.assertEqual(sum(v for (metric, _), v in counts.items() if metric == 'filesystem_read_bytes'), 3)
            finally:
                hashlib.sha256, io.open = original_sha, original_open


if __name__ == '__main__':
    unittest.main()
