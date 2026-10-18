"""Original gate retirement preserves the selected legacy source and later work."""
from __future__ import annotations
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE.parents[1]))
from runtime.io import CommandError
spec = importlib.util.spec_from_file_location(PACKAGE.name.replace('-', '_') + '_legacy', PACKAGE/'runtime/legacy_maintenance.py')
owner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(owner)

class LegacyGateTests(unittest.TestCase):
    def fixture(self, root):
        gate = json.loads((PACKAGE/'tests/fixtures/legacy-gate.json').read_text())
        task_ref = gate[owner.IDENTITY_FIELD]
        task = root/task_ref
        task.mkdir(parents=True)
        # Actual old schema leaves generation absent; no new incarnation is manufactured.
        (task/'task.json').write_text(json.dumps({'id': task.name, 'name': task.name, 'status': 'in_progress'}))
        key = {'task_id':task.name, 'lifecycle_generation':0}
        control = owner.CONTROL_ROOT + task.name + '/' + owner.ARTIFACT
        path = root/control
        path.parent.mkdir(parents=True)
        path.write_bytes((PACKAGE/'tests/fixtures/legacy-gate.json').read_bytes())
        path.chmod(0o640)
        return task_ref, key, control, path

    def freeze(self, root):
        task_ref,key,control,path = self.fixture(root)
        rows = owner.inspect_controls(root,key,task_ref,[control])
        source = owner.raw(root/task_ref/'task.json')
        checkpoint = owner.freeze_controls(root,key,task_ref,rows,source,'original-operation')
        return task_ref,key,control,path,source,checkpoint

    def test_original_public_invoke_retires_after_readable_archive_then_restores(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root/'.git').mkdir()
            task_ref,key,control,path,source,checkpoint = self.freeze(root)
            original=owner.raw(path)
            archive=root/'.trellis/tasks/archive/2026-10'/key['task_id']/'task.json'
            archive.parent.mkdir(parents=True)
            (root/task_ref/'task.json').replace(archive)
            (root/task_ref).rmdir()
            public={'profile':'legacy_control_retirement','root':str(root),'key':key,'task_ref':task_ref,'control_refs':[control],'preserved_source_ref':archive.relative_to(root).as_posix(),'recovery_ref':checkpoint}
            input_path=root/'call.json';input_path.write_text(json.dumps(public))
            script="import sys,json; from pathlib import Path; sys.path.insert(0,sys.argv[1]); import invoke; print(json.dumps(invoke.run(Path(sys.argv[1]).parent,{},['--root',sys.argv[2],'--input',sys.argv[3]])))"
            result=subprocess.run([sys.executable,'-c',script,str(PACKAGE/'runtime'),str(root),str(input_path)],env={**os.environ,'PYTHONPATH':str(PACKAGE.parents[1])},text=True,capture_output=True)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertEqual(json.loads(result.stdout),{'exit_id':'legacy_controls_retired','owner_id':PACKAGE.name,'key':key})
            self.assertFalse(path.exists())
            self.assertEqual(owner.raw(archive),source)
            # Same operation resumes without reading the removed active Task tree.
            owner.execute(PACKAGE,public)
            owner.precheck_restore(checkpoint)
            owner.restore_controls(checkpoint)
            self.assertEqual(owner.raw(path),original)

    def test_conversion_retirement_requires_physical_source_before_any_gate_write(self):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary)
            task_ref,key,control,path,source,checkpoint=self.freeze(root)
            public={'profile':'legacy_control_retirement','root':str(root),'key':key,'task_ref':task_ref,'control_refs':[control],'preserved_source_ref':task_ref+'/migration/source-task.json','recovery_ref':checkpoint}
            original=owner.raw(path)
            with self.assertRaises(CommandError):owner.execute(PACKAGE,public)
            self.assertEqual(owner.raw(path),original)
            preserved=root/public['preserved_source_ref'];preserved.parent.mkdir()
            preserved.write_bytes((root/task_ref/'task.json').read_bytes());preserved.chmod(source['mode'])
            owner.execute(PACKAGE,public)
            self.assertFalse(path.exists())

    def test_new_gate_work_after_inspection_is_preserved(self):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary)
            task_ref,key,control,path,source,checkpoint=self.freeze(root)
            # An ordinary repeated old-owner write changes formatting after the pause.
            path.write_text(json.dumps(json.loads(path.read_text()),indent=4)+'\n')
            with self.assertRaises(CommandError):owner.precheck_restore(checkpoint)
            self.assertTrue(path.exists())
            with self.assertRaises(CommandError):owner.inspect_controls(root,{**key,'lifecycle_generation':1},task_ref,[control])

    def test_actual_shell_helper_freeze_restore_and_formal_retirement(self):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary);subprocess.run(['git','init','-q','-b','main',str(root)],check=True);task_ref,key,control,path=self.fixture(root);original=owner.raw(path)
            def port(public,formal=False):
                script=PACKAGE/'scripts'/('invoke.sh' if formal else 'legacy-maintenance.sh')
                result=subprocess.run(['bash',str(script),'--root',str(root),'--input','-'],input=json.dumps(public),text=True,capture_output=True)
                self.assertEqual(result.returncode,0,result.stdout+result.stderr)
                output=json.loads(result.stdout)
                return output.get('result',output)
            inspected=port({'profile':'legacy_control_inspection','root':str(root),'key':key,'task_ref':task_ref,'control_refs':[control]})
            source=owner.raw(root/task_ref/'task.json')
            frozen=port({'profile':'legacy_control_freeze','root':str(root),'key':key,'task_ref':task_ref,'controls':inspected['controls'],'source':source,'operation_id':'actual-shell-operation'})
            port({'profile':'legacy_control_restore_check','root':str(root),'recovery_ref':frozen['recovery_ref']})
            archive=root/'.trellis/tasks/archive/2026-10'/key['task_id']/'task.json';archive.parent.mkdir(parents=True);(root/task_ref/'task.json').replace(archive)
            retired=port({'profile':'legacy_control_retirement','root':str(root),'key':key,'task_ref':task_ref,'control_refs':[control],'preserved_source_ref':archive.relative_to(root).as_posix(),'recovery_ref':frozen['recovery_ref']},True)
            self.assertEqual(retired['exit_id'],'legacy_controls_retired');self.assertFalse(path.exists())
            port({'profile':'legacy_control_restore_check','root':str(root),'recovery_ref':frozen['recovery_ref']})
            port({'profile':'legacy_control_restore','root':str(root),'recovery_ref':frozen['recovery_ref']})
            self.assertEqual(owner.raw(path),original)

if __name__=='__main__':unittest.main()
