"""Real supported interpreters: tools-local installation then ordinary activation."""
from __future__ import annotations
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from runtime import bootstrap

ASSETS = Path(__file__).resolve().parents[1]
UPGRADE = ASSETS.parent/'packages/guru-upgrade-installation/runtime'


class EffectivePythonPointerTests(unittest.TestCase):
    def test_two_real_interpreters_primary_linked_and_full_owner_backup_restore(self):
        second = os.environ.get('GURU_RUNTIME_SECOND_PYTHON')
        if not second:
            self.skipTest('Provide a second supported CPython interpreter for the actual identity transition')
        first = Path(sys.executable)
        second = Path(second)
        first_id = bootstrap.runtime_identity(ASSETS, first)[0]
        second_id = bootstrap.runtime_identity(ASSETS, second)[0]
        self.assertNotEqual(first_id, second_id, 'Use distinct supported interpreter identities')
        sys.path.insert(0,str(UPGRADE))
        try:
            spec = importlib.util.spec_from_file_location('effective_pointer_upgrade_owner',UPGRADE/'owner.py')
            owner = importlib.util.module_from_spec(spec);spec.loader.exec_module(owner)
            import files
            with tempfile.TemporaryDirectory() as temporary:
                directory=Path(temporary);primary=directory/'primary';peer=directory/'peer'
                primary.mkdir()
                def git(*args):
                    subprocess.run(['git','-C',str(primary),*args],check=True,capture_output=True)
                git('init','-b','main')
                git('-c','user.name=Test','-c','user.email=t@example.invalid','commit','--allow-empty','-m','initial')
                git('worktree','add','-b','dev',str(peer))
                common=bootstrap.active_pointer_path(primary,for_write=True)
                bootstrap.bootstrap(primary,ASSETS,first)
                common_before=common.read_bytes()
                self.assertNotIn('python_effective',owner.controls(primary,{'controls':[]}))
                self.assertNotIn('python_effective',owner.controls(peer,{'controls':[]}))
                for index,target in enumerate((primary,peer)):
                    other=peer if target==primary else primary
                    bootstrap.bootstrap(target,ASSETS,first,checkout_local=True)
                    pointer=bootstrap.active_pointer_path(target)
                    pointer.chmod(0o640)
                    before=pointer.read_bytes()
                    other_pointer=bootstrap.active_pointer_path(other)
                    other_before=other_pointer.read_bytes()
                    controls=owner.controls(target,{'controls':[]})
                    self.assertEqual(controls['python_effective'],pointer)
                    recovery=directory/f'recovery-{index}';recovery.mkdir()
                    checkpoint={'controls':{k:str(v) for k,v in controls.items()},'preimages':files.snapshot(target,recovery,set(),controls)}
                    control_before=files.control_token(checkpoint)
                    # The ordinary bootstrap path must update the effective local override.
                    result=bootstrap.bootstrap(target,ASSETS,second)
                    self.assertEqual(result['runtime_identity'],second_id)
                    self.assertEqual(bootstrap.active_pointer_path(target,for_write=True),pointer)
                    self.assertEqual(bootstrap.validate_active(target,ASSETS)['runtime_identity'],second_id)
                    native=subprocess.run(['bash',str(ASSETS/'resolve-python.sh'),str(target),str(ASSETS),'-c','import sys;print(str(sys.version_info.major)+"."+str(sys.version_info.minor))'],text=True,capture_output=True)
                    self.assertEqual(native.returncode,0,native.stderr)
                    expected=subprocess.check_output([str(second),'-c','import sys;print(str(sys.version_info.major)+"."+str(sys.version_info.minor))'],text=True)
                    self.assertEqual(native.stdout,expected)
                    self.assertEqual(common.read_bytes(),common_before)
                    self.assertEqual(other_pointer.read_bytes(),other_before)
                    self.assertEqual(files.control_token(checkpoint),control_before)
                    # Exercise the original full-upgrade snapshot/restorer, including mode.
                    files.restore(target,recovery,checkpoint)
                    self.assertEqual(pointer.read_bytes(),before)
                    self.assertEqual(pointer.stat().st_mode & 0o777,0o640)
                    self.assertEqual(bootstrap.validate_active(target,ASSETS)['runtime_identity'],first_id)
                    self.assertEqual(common.read_bytes(),common_before)
                    self.assertEqual(other_pointer.read_bytes(),other_before)
        finally:
            sys.path.remove(str(UPGRADE))


if __name__=='__main__':unittest.main()
