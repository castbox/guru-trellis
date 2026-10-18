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

    def test_prepared_target_is_installer_idempotent_and_public_rollback_restores(self):
        plan = self.prepare()
        before = copy.deepcopy(plan)
        owner.project_agents_target(plan,self.module)
        agents = next(a for a in plan['actions'] if a['path']=='AGENTS.md')
        other = copy.deepcopy(plan)
        next(a for a in other['actions'] if a['path']=='AGENTS.md')['target'] = next(
            a for a in before['actions'] if a['path']=='AGENTS.md')['target']
        self.assertEqual(other,before)  # Source/operation/guard/receipt stay with their original owners.
        self.assertEqual((self.root/'AGENTS.md').read_bytes(),self.original)
        applied = self.sdk('applyMaintenance',plan)
        self.assertNotIn('error',applied,applied)
        self.assertEqual((self.root/'AGENTS.md').read_bytes(),base64.b64decode(agents['target']['content_base64']))
        self.assertEqual(self.module.ensure_agents_ai_first_principles(self.root)['action'],'unchanged')
        restored = self.sdk('rollbackMaintenance',{'recovery_ref':applied['result']['recovery_ref']})
        self.assertNotIn('error',restored,restored)
        self.assertEqual(restored['result']['status'],'rolled_back')
        self.assertEqual((self.root/'AGENTS.md').read_bytes(),self.original)

    def test_previous_two_writer_path_exposes_the_original_rollback_conflict(self):
        plan = self.prepare()
        applied = self.sdk('applyMaintenance',plan)
        self.assertNotIn('error',applied,applied)
        self.assertEqual(self.module.ensure_agents_ai_first_principles(self.root)['action'],'updated')
        restored = self.sdk('rollbackMaintenance',{'recovery_ref':applied['result']['recovery_ref']})
        self.assertEqual(restored['error']['code'],'later_work_conflict')


if __name__ == '__main__':
    unittest.main()
