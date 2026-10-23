"""Opt-in real paired-package proof against an original-writer old fixture.

GURU_TOOLS_NATIVE_FIXTURE is fixture.json with root,peer,source,context_id.
GURU_MAINTENANCE_CANDIDATE is an independently installed matching candidate.json.
The harness creating the old fixture must invoke its real CLI/preset writers.
No transport, installer, validation, or runtime call below is mocked.
"""
from __future__ import annotations
import base64
import hashlib
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
SOURCE = PACKAGE.parents[4]


def tree(directory):
    if not directory.exists():
        return {}
    return {p.relative_to(directory).as_posix(): [p.stat().st_mode & 0o777, hashlib.sha256(p.read_bytes()).hexdigest()]
            for p in directory.rglob('*') if p.is_file() and '__pycache__' not in p.parts and '.git' not in p.relative_to(directory).parts}


@unittest.skipUnless(os.environ.get('GURU_TOOLS_NATIVE_FIXTURE') and os.environ.get('GURU_MAINTENANCE_CANDIDATE'),
                     'Requires original-writer legacy fixture and matching installed public maintenance pair')
class NativeToolsInstallationTests(unittest.TestCase):
    def test_real_wrapper_target_native_and_reapply_preserve_old_data_and_peer(self):
        fixture = json.loads(Path(os.environ['GURU_TOOLS_NATIVE_FIXTURE']).read_text())
        candidate_path = Path(os.environ['GURU_MAINTENANCE_CANDIDATE']).resolve()
        candidate = json.loads(candidate_path.read_text())
        root, peer = Path(fixture['root']).resolve(), Path(fixture['peer']).resolve()
        env = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1', 'TRELLIS_CONTEXT_ID': fixture.get('context_id', 'codex_guru566')}
        def command(args, cwd=root, expected=0):
            result = subprocess.run(args, cwd=cwd, text=True, capture_output=True, env=env)
            self.assertEqual(result.returncode, expected, result.stderr[-1000:] + result.stdout[-1000:])
            return result.stdout
        common = Path(command(['git','rev-parse','--path-format=absolute','--git-common-dir']).strip())
        preserved = {str(path): tree(path) for path in (root / '.trellis/tasks', root / '.trellis/.runtime/sessions', common / 'trellis', peer)}
        source_ref = command(['git','rev-parse','HEAD'], SOURCE).strip()
        descriptor = {'cli_package_root': str(candidate_path.parent / 'installed/node_modules/@mindfoldhq/trellis'),
                      'dependency_mode': 'local_candidate', 'expected_candidate': candidate['candidate']}
        with tempfile.TemporaryDirectory(prefix='guru-tools-native-input-') as directory:
            inputs = Path(directory)
            def write(name, value):
                path = inputs / name; path.write_text(json.dumps(value)); return path
            public = write('input.json', {'profile':'install','source_ref':source_ref,'dependency_mode':'local_candidate','checkout':str(root)})
            dependency = write('source.json', descriptor)
            def invoke(script, profile, plan=None, source=None):
                argv = ['bash', str(PACKAGE / 'scripts' / script), '--root', str(root), '--input', str(profile)]
                if plan: argv += ['--plan', str(plan)]
                if source: argv += ['--upstream-source', str(source)]
                return json.loads(command(argv, SOURCE))
            preview = invoke('preview.sh', public, source=dependency)['result']
            request = {'upstream_source':descriptor, 'tools_input':{'root':str(root),'workflow':{
                'action':'install','template_id':'guru-team','provider':'local-canonical:'+source_ref,
                'content':(SOURCE/'trellis/workflows/guru-team/workflow.md').read_text(),'ownership':'custom'},
                'file_decisions':[{'path':row['path'],'source':row['source'],'action':'preserve'}
                                  for row in preview['public_tools']['files'] if row['path'] != 'AGENTS.md' and row['status']=='conflict' and not row['required']]},
                'selected_platforms':preview['public_tools']['configured_platforms'], 'guru_decisions':[]}
            agents = next(row for row in preview['public_tools']['files'] if row['path']=='AGENTS.md')
            request['tools_input']['file_decisions'].append({'path':'AGENTS.md','source':agents['source'],
                'action':'custom','content':(root/'AGENTS.md').read_text()})
            prepared = invoke('prepare.sh', public, write('prepare.json', request))['result']['plan']
            frozen = write('plan.json', prepared)
            upgraded = invoke('invoke.sh', public, frozen)
            self.assertEqual(upgraded['exit_id'], 'tools_upgraded', upgraded)
            self.assertEqual(upgraded['unverified'], ['formal_fork_source_lock'])
            # Same-candidate output-loss recovery uses the original operation.
            resume = write('resume.json', {'profile':'resume','recovery_ref':upgraded['recovery_ref']})
            self.assertEqual(invoke('invoke.sh', resume), upgraded)
            for path, before in preserved.items(): self.assertEqual(tree(Path(path)), before)
            runtime = root / '.trellis/guru-team/runtime'
            resolved = command(['bash',str(runtime/'resolve-python.sh'),str(root),str(runtime),'-c','import sys; print(sys.executable)']).strip()
            self.assertTrue(Path(resolved).is_file())
            self.assertTrue((root/'.trellis/.runtime/guru-team/python/active.json').is_file())
            result = subprocess.run(['/usr/bin/python3' if os.name!='nt' else 'python', str(root/'.trellis/scripts/get_context.py'),'--mode','continuation'],cwd=root,text=True,capture_output=True,env=env)
            self.assertNotEqual(result.returncode,0)
            self.assertIn('maintenance_required',result.stdout+result.stderr)
            # Real preset reapply through the same supported tools-only boundary.
            # It reuses the actual operation proof and cannot parse old Tasks.
            import sys
            sys.path.insert(0,str(PACKAGE.parents[1]));sys.path.insert(0,str(PACKAGE/'runtime'))
            import tools_owner
            original=tools_owner.legacy_owner(PACKAGE)
            module=original.installer(SOURCE)
            recovery=tools_owner.recovery_path(root,upgraded['recovery_ref'],original)
            checkpoint=json.loads((recovery/'checkpoint.json').read_text())
            result=module.install_assets(SOURCE/'trellis/workflows/guru-team',root/'.trellis/guru-team',root,
                set(prepared['selected_platforms']),python=resolved,checkout_local=True,tools_only=True,
                tools_maintenance={'source':descriptor,'plan':prepared['upstream_plan'],'recovery_ref':checkpoint['upstream_ref']})
            self.assertEqual(result['skill_installed_validation']['returncode'],0)
            for path,before in preserved.items():self.assertEqual(tree(Path(path)),before)
            fixture['tools_result']=upgraded;fixture['public_plan']=prepared['upstream_plan'];fixture['upstream_source']=descriptor
            Path(os.environ['GURU_TOOLS_NATIVE_FIXTURE']).write_text(json.dumps(fixture,indent=2)+'\n')
            # A real later edit blocks both recovery paths without being adopted.
            agents_path = root/'AGENTS.md'
            installed_agents = agents_path.read_bytes()
            installed_mode = agents_path.stat().st_mode & 0o777
            agents_path.write_bytes(installed_agents+b'\nLater project instruction.\n')
            rollback = write('rollback.json', {'profile':'rollback','recovery_ref':upgraded['recovery_ref']})
            for profile in (resume,rollback):
                self.assertEqual(invoke('invoke.sh',profile)['exit_id'],'blocked')
                self.assertEqual(agents_path.read_bytes(),installed_agents+b'\nLater project instruction.\n')
            # The fixture user undoes that edit before the original rollback.
            agents_path.write_bytes(installed_agents)
            agents_path.chmod(installed_mode)
            restored = invoke('invoke.sh',rollback)
            self.assertEqual(restored['exit_id'],'rolled_back',restored)
            for action in prepared['upstream_plan']['actions']:
                if action.get('kind','file') != 'file': continue
                path = Path(action['root'])/action['path']
                before = action['source']
                if before is None:
                    self.assertFalse(path.exists(),str(path))
                else:
                    self.assertEqual(path.read_bytes(),base64.b64decode(before['content_base64']),str(path))
                    self.assertEqual(path.stat().st_mode & 0o777,before['mode'],str(path))
            for path,before in preserved.items(): self.assertEqual(tree(Path(path)),before)
            fixture['combination_validation']={'resume':'passed','later_edit_resume_rollback':'blocked_preserved',
                'rollback':restored,'public_preimages':'bytes_modes_restored'}
            Path(os.environ['GURU_TOOLS_NATIVE_FIXTURE']).write_text(json.dumps(fixture,indent=2)+'\n')
