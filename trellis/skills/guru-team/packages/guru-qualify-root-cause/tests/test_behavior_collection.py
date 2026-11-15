"""Exercise fixture assembly and native command transport, not model judgment."""
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('behavior_collector', Path(__file__).with_name('run_behavior_validation.py'))
collector = importlib.util.module_from_spec(spec)
spec.loader.exec_module(collector)


class CollectionTests(unittest.TestCase):
    def collect(self, case_id, returncodes, **settings):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        output = Path(temporary.name)
        real_run = subprocess.run
        calls = []

        def native_transport(argv, **kwargs):
            if argv[0] != 'codex':
                return real_run(argv, **kwargs)
            calls.append((argv, kwargs['input']))
            kwargs['stderr'].write('transport fixture, no semantic result\n')
            return subprocess.CompletedProcess(argv, returncodes[len(calls)-1])

        with patch.object(collector.subprocess, 'run', side_effect=native_transport):
            result = collector.run_case(collector.SOURCE, output, case_id, **settings)
        return output/case_id, result, calls

    def test_material_assembly_and_native_failure_are_observed(self):
        case, report, calls = self.collect('shared-material', [23], model='test-model', reasoning_effort='medium')
        self.assertEqual(report['native_returncode'], 23)
        argv, prompt = calls[0]
        self.assertEqual(argv[argv.index('--model')+1], 'test-model')
        self.assertEqual(argv[argv.index('-c')+1], 'model_reasoning_effort="medium"')
        self.assertEqual(json.loads((case/'collection.json').read_text())['argv'], argv)
        root = case/'workspace'
        receipt = json.loads((root/'local-observation.json').read_text())
        self.assertEqual(receipt['returncode'], 0)
        observed = json.loads(receipt['stdout'])
        self.assertEqual(observed['backend_calls'], ['pear'])
        self.assertEqual(observed['values'], ['PEAR', 'PEAR'])
        self.assertEqual((root/'frozen/app/cache_proxy.py').read_bytes(), (root/'app/cache_proxy.py').read_bytes())
        self.assertTrue((root/'observed/inflight/app/vector_service.py').is_file())
        self.assertFalse((root/'app/vector_service.py').exists())
        self.assertFalse((root/'.trellis/guru-team/skills/packages/guru-qualify-root-cause/tests').exists())
        task = next((root/'.trellis/tasks').glob('*/task.json')).parent
        self.assertEqual(len(list((task/'deliveries').iterdir())), 1)
        self.assertNotIn('shared_dependency', prompt)
        self.assertNotIn('853', prompt)

    def test_ordinary_assembly_preserves_default_native_argv(self):
        case, report, calls = self.collect('shared-ordinary', [0])
        argv, _ = calls[0]
        self.assertEqual(argv, ['codex', 'exec', '--ephemeral', '--skip-git-repo-check',
                               '--sandbox', 'danger-full-access', '--cd', str(case/'workspace'),
                               '--json', '--output-last-message', str(case/'native-final.txt'), '-'])
        self.assertEqual(report['native_returncode'], 0)
        self.assertFalse((case/'workspace/observed/inflight').exists())
        self.assertEqual(json.loads((case/'workspace/local-observation.json').read_text())['returncode'], 0)

    def test_existing_followup_uses_same_settings_and_retains_failure(self):
        _, report, calls = self.collect('v4-async', [0, 17], model='test-model', reasoning_effort='medium')
        self.assertEqual(report['execution_returncode'], 17)
        self.assertEqual(report['execution_argv'], calls[1][0])
        for argv, _ in calls:
            self.assertEqual(argv[argv.index('--model')+1], 'test-model')
            self.assertEqual(argv[argv.index('-c')+1], 'model_reasoning_effort="medium"')


if __name__ == '__main__':
    unittest.main()
