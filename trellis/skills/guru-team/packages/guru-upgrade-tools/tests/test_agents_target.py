"""Actual public tools writer and Guru block composition share one target."""
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


class AgentsInputTests(unittest.TestCase):
    def test_missing_capability_and_explicit_decision_stop_preparation(self):
        module = owner.legacy_owner(PACKAGE).installer(SOURCE)
        capability = {'tools_custom_instruction': {'path':'AGENTS.md','action':'custom'}}
        with self.assertRaisesRegex(ValueError,'lacks tools_custom_instruction'):
            owner.compose_agents_input({},module,{})
        for decisions in ([],[{'path':'AGENTS.md','action':'preserve'}],
                          [{'path':'AGENTS.md','action':'replace'}],
                          [{'path':'AGENTS.md','action':'custom','content':'base'}]*2):
            with self.assertRaisesRegex(ValueError,'exactly one explicit'):
                owner.compose_agents_input({'file_decisions':decisions},module,capability)


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
        agents.write_text(agents.read_text()+'\nProject instructions outside the Guru block.\n')
        agents.chmod(0o640)
        self.original = agents.read_bytes()

    def sdk(self, method, payload):
        proc = subprocess.run(['node','--input-type=module','-e',BRIDGE],cwd=self.root,
                              input=json.dumps({'cli':str(self.cli),'method':method,'input':payload,
                                                'state':str(self.directory/'recovery')}),
                              text=True,capture_output=True,check=True)
        return json.loads(proc.stdout)

    def prepare(self, custom=True, config_decision=False):
        raw = {'content_base64':base64.b64encode(self.original).decode(),
               'sha256':hashlib.sha256(self.original).hexdigest(),'mode':0o640}
        tools = {'root':str(self.root),
            'workflow':{'action':'install','template_id':'guru-team','ownership':'custom',
                        'provider':'local-canonical:test',
                        'content':(SOURCE/'trellis/workflows/guru-team/workflow.md').read_text()},
            'file_decisions':[{'path':'AGENTS.md','source':raw,'action':'preserve'}]}
        if config_decision:
            data = (self.root/'.trellis/config.yaml').read_bytes()
            tools['file_decisions'].append({'path':'.trellis/config.yaml','action':'preserve','source':{
                'content_base64':base64.b64encode(data).decode(),'sha256':hashlib.sha256(data).hexdigest(),'mode':0o644}})
        if custom:
            tools['file_decisions'][0].update(action='custom',content=self.original.decode())
            original_input = copy.deepcopy(tools)
            contract = self.sdk('getMaintenanceContract',None)['result']
            caller_input = tools
            tools = owner.compose_agents_input(caller_input,self.module,contract)
            self.assertEqual(caller_input,original_input)
            self.assertEqual(tools['file_decisions'][0]['source'],raw)
        result = self.sdk('prepareToolsInstallation',tools)
        self.assertNotIn('error',result,result)
        return result['result']

    def test_prepared_target_is_installer_idempotent_and_public_rollback_restores(self):
        plan = self.prepare()
        before = copy.deepcopy(plan)
        owner.validate_agents_target(plan,self.module)
        self.assertEqual(plan,before)
        agents = next(a for a in plan['actions'] if a['path']=='AGENTS.md')
        self.assertEqual((self.root/'AGENTS.md').read_bytes(),self.original)
        applied = self.sdk('applyMaintenance',plan)
        self.assertNotIn('error',applied,applied)
        self.assertEqual((self.root/'AGENTS.md').read_bytes(),base64.b64decode(agents['target']['content_base64']))
        self.assertEqual((self.root/'AGENTS.md').stat().st_mode & 0o777,0o640)
        self.assertIn(b'Project instructions outside the Guru block.',(self.root/'AGENTS.md').read_bytes())
        self.assertEqual(self.module.ensure_agents_ai_first_principles(self.root)['action'],'unchanged')
        for method in ('recoverMaintenance','resumeMaintenance'):
            recovered = self.sdk(method,{'recovery_ref':applied['result']['recovery_ref']})
            self.assertNotIn('error',recovered,recovered)
        restored = self.sdk('rollbackMaintenance',{'recovery_ref':applied['result']['recovery_ref']})
        self.assertNotIn('error',restored,restored)
        self.assertEqual(restored['result']['status'],'rolled_back')
        self.assertEqual((self.root/'AGENTS.md').stat().st_mode & 0o777,0o640)
        self.assertEqual((self.root/'AGENTS.md').read_bytes(),self.original)

    def test_later_project_edit_blocks_public_resume_and_rollback(self):
        applied = self.sdk('applyMaintenance',self.prepare())['result']
        agents = self.root/'AGENTS.md'
        agents.write_text(agents.read_text()+'\nLater project work.\n')
        edited = agents.read_bytes()
        for method in ('resumeMaintenance','rollbackMaintenance'):
            result = self.sdk(method,{'recovery_ref':applied['recovery_ref']})
            self.assertEqual(result['error']['code'],'later_work_conflict')
            self.assertEqual(agents.read_bytes(),edited)

    def test_update_skip_with_old_block_is_diagnosed_without_writing(self):
        config = self.root/'.trellis/config.yaml'
        config.write_text(config.read_text()+'\nupdate:\n  skip:\n    - AGENTS.md\n')
        plan = self.prepare(config_decision=True)
        with self.assertRaisesRegex(ValueError,'update.skip'):
            owner.validate_agents_target(plan,self.module)
        self.assertEqual((self.root/'AGENTS.md').read_bytes(),self.original)

    def test_previous_two_writer_path_exposes_the_original_rollback_conflict(self):
        plan = self.prepare(custom=False)
        applied = self.sdk('applyMaintenance',plan)
        self.assertNotIn('error',applied,applied)
        self.assertEqual(self.module.ensure_agents_ai_first_principles(self.root)['action'],'updated')
        restored = self.sdk('rollbackMaintenance',{'recovery_ref':applied['result']['recovery_ref']})
        self.assertEqual(restored['error']['code'],'later_work_conflict')


if __name__ == '__main__':
    unittest.main()
