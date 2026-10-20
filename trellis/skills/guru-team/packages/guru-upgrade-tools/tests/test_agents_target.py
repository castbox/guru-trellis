"""The public tools writer and Guru installer retain separate file ownership."""
from __future__ import annotations

import base64
import copy
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
SOURCE = PACKAGE.parents[4]
sys.path.insert(0, str(PACKAGE.parents[1]))
sys.path.insert(0, str(PACKAGE / "runtime"))
import tools_owner as owner

BRIDGE = r"""
import fs from 'node:fs';
import {pathToFileURL} from 'node:url';
const x=JSON.parse(fs.readFileSync(0,'utf8'));
const manifest=JSON.parse(fs.readFileSync(x.cli+'/package.json','utf8'));
const sdk=await import(pathToFileURL(x.cli+'/'+manifest.main));
try {
 const result=x.method==='applyMaintenance'
   ? await sdk.maintenance.applyMaintenance(x.input,{state_dir:x.state})
   : await sdk.maintenance[x.method](x.input);
 console.log(JSON.stringify({result}));
} catch(error) { console.log(JSON.stringify({error:{code:error.code,message:error.message}})); }
"""


@unittest.skipUnless(os.environ.get('GURU_UPSTREAM_DELIVERY_CLI'),
                     'Requires the reviewed real CLI/Core public maintenance pair')
class AgentsTargetTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='guru-agents-target-')
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name).resolve()
        self.root = self.directory / 'project'
        self.root.mkdir()
        self.fork = Path(os.environ['GURU_UPSTREAM_DELIVERY_CLI']).resolve()
        self.cli = next(p for p in self.fork.parents if (p/'package.json').is_file()
                        and json.loads((p/'package.json').read_text()).get('name') == '@mindfoldhq/trellis')
        for args in [('init','-q'), ('config','user.name','Fixture'), ('config','user.email','fixture@example.invalid')]:
            subprocess.run(['git',*args],cwd=self.root,check=True,capture_output=True)
        subprocess.run(['node',str(self.fork),'init','--codex','--yes'],cwd=self.root,check=True,capture_output=True)
        self.module = owner.legacy_owner(PACKAGE).installer(SOURCE)
        agents = self.root/'AGENTS.md'
        agents.write_text(agents.read_text()+'\n'+self.module.AGENTS_AI_FIRST_START_MARKER+
                          '\nExisting Guru policy from the predecessor.\n'+self.module.AGENTS_AI_FIRST_END_MARKER+'\n')
        self.original = agents.read_bytes()

    def sdk(self, method, payload):
        proc = subprocess.run(['node','--input-type=module','-e',BRIDGE],cwd=self.root,
                              input=json.dumps({'cli':str(self.cli),'method':method,'input':payload,
                                                'state':str(self.directory/'recovery')}),
                              text=True,capture_output=True,check=True)
        return json.loads(proc.stdout)

    def prepare(self):
        raw = {'content_base64':base64.b64encode(self.original).decode(),
               'sha256':hashlib.sha256(self.original).hexdigest(),'mode':0o644}
        result = self.sdk('prepareToolsInstallation',{'root':str(self.root),
            'workflow':{'action':'install','template_id':'guru-team','ownership':'custom',
                        'provider':'local-canonical:test',
                        'content':(SOURCE/'trellis/workflows/guru-team/workflow.md').read_text()},
            'file_decisions':[{'path':'AGENTS.md','source':raw,'action':'preserve'}]})
        self.assertNotIn('error',result,result)
        return result['result']

    def test_preserved_agents_has_one_writer_and_recovery_restores_original(self):
        plan = self.prepare()
        before = copy.deepcopy(plan)
        source = owner.delegate_agents_preservation(plan)
        self.assertEqual(source, {'sha256':hashlib.sha256(self.original).hexdigest(),'mode':0o644})
        before['actions'] = [row for row in before['actions'] if row['path'] != 'AGENTS.md']
        self.assertEqual(plan,before)  # No replacement bytes, guard or receipt are rewritten.
        self.assertEqual((self.root/'AGENTS.md').read_bytes(),self.original)
        old = owner.legacy_owner(PACKAGE)
        recovery = self.directory/'guru-recovery'
        checkpoint = {'controls':{}, 'preimages':old.snapshot(self.root,recovery,{'AGENTS.md'}, {})}
        applied = self.sdk('applyMaintenance',plan)
        self.assertNotIn('error',applied,applied)
        self.assertEqual((self.root/'AGENTS.md').read_bytes(),self.original)
        self.assertEqual(self.module.ensure_agents_ai_first_principles(self.root)['action'],'updated')
        self.assertEqual(self.module.ensure_agents_ai_first_principles(self.root)['action'],'unchanged')
        for method in ('recoverMaintenance','resumeMaintenance'):
            resumed = self.sdk(method,{'recovery_ref':applied['result']['recovery_ref']})
            self.assertNotIn('error',resumed,resumed)
            self.assertEqual(resumed['result']['status'],'applied')
        restored = self.sdk('rollbackMaintenance',{'recovery_ref':applied['result']['recovery_ref']})
        self.assertNotIn('error',restored,restored)
        self.assertEqual(restored['result']['status'],'rolled_back')
        old.restore(self.root,recovery,checkpoint)
        self.assertEqual((self.root/'AGENTS.md').read_bytes(),self.original)

    def test_prepared_preservation_detects_a_later_project_instruction_edit(self):
        plan = self.prepare()
        private = {'agents_source':owner.delegate_agents_preservation(plan)}
        old = owner.legacy_owner(PACKAGE)
        owner.validate_agents_source(self.root,private,old)
        (self.root/'AGENTS.md').write_bytes(self.original+b'\nA later project instruction.\n')
        with self.assertRaisesRegex(ValueError,'changed since preparation'):
            owner.validate_agents_source(self.root,private,old)

    def test_core_replacement_is_not_silently_reinterpreted_as_preservation(self):
        plan = self.prepare()
        agents = next(row for row in plan['actions'] if row['path']=='AGENTS.md')
        agents['target'] = None
        with self.assertRaisesRegex(ValueError,'explicit AGENTS.md preserve'):
            owner.delegate_agents_preservation(plan)

    def test_previous_two_writer_path_exposes_the_original_rollback_conflict(self):
        plan = self.prepare()
        applied = self.sdk('applyMaintenance',plan)
        self.assertNotIn('error',applied,applied)
        self.assertEqual(self.module.ensure_agents_ai_first_principles(self.root)['action'],'updated')
        restored = self.sdk('rollbackMaintenance',{'recovery_ref':applied['result']['recovery_ref']})
        self.assertEqual(restored['error']['code'],'later_work_conflict')


if __name__ == '__main__':
    unittest.main()
