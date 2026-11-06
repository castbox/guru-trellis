"""Native context/trace projection integration for the original eval transports."""
from __future__ import annotations
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from adapters.eval import native_adapter
from adapters.eval.eval_support import qualification_trace_helper_source
SKILLS=Path(__file__).resolve().parents[2]
REPO=SKILLS.parents[2]


def request(root, skill, case_id):
    package=SKILLS/'packages'/skill
    case=next(c for c in json.loads((package/'evals/evals.json').read_text())['evals'] if c['id']==case_id)
    work=root/'execution/workdir';work.mkdir(parents=True)
    for relative in case['files']:
        target=work/relative;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(package/relative,target)
    interface=json.loads((package/'interface.json').read_text())
    return {**{k:case[k] for k in ('prompt','files','model_id','native_execution_mode','native_execution_adapter')},
        'schema_version':'1.0','skill_id':skill,'case_id':case_id,'package_root':str(package),
        'workdir':str(work),'runtime_target':str(REPO/'.trellis/guru-team/scripts/bash/run-skill-command.sh'),
        'interface':{'public_invocation':interface['public_contracts']['invocation']}}


class NativeConstraintTransportTests(unittest.TestCase):
    def test_persistence_changes_only_selected_codex_semantic_argv(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            selected = [('guru-author-task-plan', 'native-implementation-plan-premise'),
                ('guru-check-task', 'native-implementation-code-drift')]
            for skill, case in selected:
                req = {'skill_id': skill, 'case_id': case, 'workdir': temp,
                    'native_execution_mode': 'semantic_authoring', 'native_execution_adapter': 'codex',
                    'model_id': 'original-model'}
                argv, output = native_adapter.native_argv('codex', 'codex', req, 'original context',
                    root / 'context', root / 'request', root / 'projection')
                other = dict(req, case_id='another-existing-case')
                original, original_output = native_adapter.native_argv('codex', 'codex', other,
                    'original context', root / 'context', root / 'request', root / 'projection')
                self.assertEqual(original, [*argv[:2], '--ephemeral', *argv[2:]])
                self.assertEqual(output, original_output)
                for delta in ({'skill_id': 'guru-clarify-requirements'},
                              {'native_execution_mode': 'post_owner'},
                              {'native_execution_adapter': 'claude'}):
                    with self.subTest(case=case, delta=delta):
                        self.assertFalse(native_adapter.persisted_r5_observation({**req, **delta}, 'codex'))
                self.assertFalse(native_adapter.persisted_r5_observation(req, 'claude'))

    def test_host_wrapper_observation_preserves_duplicate_requests_and_both_streams(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            package = root / 'guru-author-task-plan'
            wrapper = package / 'scripts/invoke.sh'
            wrapper.parent.mkdir(parents=True)
            wrapper.write_text('#!/bin/sh\n')
            wrapper.chmod(0o755)
            request_fifo, response_fifo = root / 'request', root / 'response'
            private = root / 'private-control'
            private.mkdir()
            sink = private / 'worker-invocations.jsonl'
            payload = {'arguments': ['--qualifier', 'normal-scenario'], 'stdin': ' {"a":1}\n'}
            raw = json.dumps(payload, indent=2).encode()
            outcomes = [subprocess.CompletedProcess([], code, '原stdout\r\n', 'original stderr\n')
                for code in (0, 0, 7)]
            stop = threading.Event()
            with patch.object(native_adapter.subprocess, 'run', side_effect=outcomes) as run:
                thread = native_adapter.start_qualification_runtime_boundary(request_fifo, response_fifo,
                    stop, root, package, {}, {}, wrapper_observation_path=sink)
                try:
                    for expected in outcomes:
                        with request_fifo.open('wb') as handle:
                            handle.write(raw)
                        with response_fifo.open() as handle:
                            actual = json.load(handle)
                        self.assertEqual(actual, {'returncode': expected.returncode,
                            'stdout': expected.stdout, 'stderr': expected.stderr})
                    thread.join(timeout=2)
                    self.assertFalse(thread.is_alive())
                finally:
                    stop.set()
                    thread.join(timeout=2)
            self.assertEqual(run.call_count, 3)
            rows = [json.loads(line) for line in sink.read_text().splitlines()]
            self.assertEqual(len(rows), 3)
            for row, expected, call in zip(rows, outcomes, run.call_args_list):
                self.assertEqual(bytes.fromhex(row['request_bytes_hex']), raw)
                self.assertEqual(row['stdin'], payload['stdin'])
                self.assertEqual(call.kwargs['input'], payload['stdin'])
                self.assertEqual(row['wrapper'], {'argv': call.args[0], 'executed': True,
                    'returncode': expected.returncode, 'stdout': expected.stdout, 'stderr': expected.stderr})
                self.assertEqual(row['response']['returncode'], expected.returncode)
            self.assertEqual(thread.observation_errors, [])

    def test_wrapper_observation_distinguishes_no_launch_from_nonzero_exit(self):
        for raw, launch in ((b'{', False),
                (json.dumps({'arguments': ['--invocation', '-'], 'stdin': '{}'}).encode(), True)):
            with self.subTest(launch=launch), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                package = root / 'guru-maintain-architecture-baseline'
                wrapper = package / 'scripts/invoke.sh'
                wrapper.parent.mkdir(parents=True)
                wrapper.write_text('#!/bin/sh\n')
                wrapper.chmod(0o755)
                sink = root / 'host-private.jsonl'
                stop = threading.Event()
                with patch.object(native_adapter.subprocess, 'run', side_effect=OSError('wrapper unavailable')) as run:
                    thread = native_adapter.start_qualification_runtime_boundary(root / 'request', root / 'response',
                        stop, root, package, {}, {}, wrapper_observation_path=sink)
                    try:
                        with (root / 'request').open('wb') as handle:
                            handle.write(raw)
                        with (root / 'response').open() as handle:
                            response = json.load(handle)
                    finally:
                        stop.set()
                        thread.join(timeout=2)
                row = json.loads(sink.read_text())
                self.assertEqual(row['response'], response)
                self.assertEqual(response['returncode'], 2)
                self.assertEqual(run.call_count, int(launch))
                if launch:
                    self.assertFalse(row['wrapper']['executed'])
                    self.assertNotIn('returncode', row['wrapper'])
                else:
                    self.assertIsNone(row['wrapper'])

    def test_task_free_model_projection_has_actual_contracts_and_qualifier_targets(self):
        with tempfile.TemporaryDirectory() as temp:
            req=request(Path(temp),'guru-execute-task-free-change','native-owner-qualification-pair')
            values=native_adapter.build_context(req,'codex')
            try:
                protocol=json.loads(values[4].read_text())
                module=native_adapter.additional_authoring_module(req['skill_id'])
                package=Path(protocol['projection_root'])
                for path in module.PUBLIC_READS:self.assertTrue((package/path).is_file(),path)
                repo=Path(protocol['repository_projection_root'])
                facts=json.loads((repo/module.FACTS).read_text())
                self.assertTrue(all((repo/path).is_file() for path in facts['required_reads']))
                self.assertIsNone(protocol['architecture_context'])
                self.assertIn('--qualifier normal-scenario',values[0])
                self.assertIn('--qualifier root-cause',values[0])
                self.assertIn('intentionally has no .git',values[0])
                self.assertIn('command inspect',values[0])
                self.assertTrue(protocol['task_free_observation_receipts_path'])
                self.assertIn('.trellis/guru-team/skills/consumers/workflow/production/root-cause-qualification-invocation.schema.json',facts['required_reads'])
                self.assertIn(str(repo/module.FACTS),values[0])
                self.assertTrue(protocol['writable_preimages'])
                native=json.loads(values[5].read_text())
                self.assertNotIn('expected_exit',native)
                self.assertNotIn('assertions',native)
            finally:values[9].set();values[8].join(timeout=2)

    def test_implementation_private_commands_do_not_add_a_public_flow(self):
        for skill,case in [('guru-author-task-plan','native-implementation-plan-premise'),
                           ('guru-clarify-requirements','native-implementation-authority-conflict'),
                           ('guru-check-task','native-implementation-code-drift')]:
            with self.subTest(case=case),tempfile.TemporaryDirectory() as temp:
                req=request(Path(temp),skill,case)
                values=native_adapter.build_context(req,'codex')
                try:
                    protocol=json.loads(values[4].read_text())
                    self.assertTrue(protocol['implementation_commands'])
                    self.assertIsNone(protocol['architecture_context'])
                    self.assertIsNone(protocol['native_authoring_flow'])
                    self.assertIn('COMMAND_FORWARDING_ALLOWED = True',Path(protocol['helper_path']).read_text())
                    module=native_adapter.additional_authoring_module(skill,case)
                    package=Path(protocol['projection_root'])
                    for path in module.public_reads(package):self.assertTrue((package/path).is_file(),path)
                    facts=json.loads((Path(protocol['repository_projection_root'])/module.FACTS).read_text())
                    self.assertTrue(facts['owner_mutated_paths'])
                    self.assertIn('command --skill-id',values[0])
                finally:values[9].set();values[8].join(timeout=2)
        self.assertIn('COMMAND_FORWARDING_ALLOWED = False',qualification_trace_helper_source())

if __name__=='__main__':unittest.main()
