from __future__ import annotations
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

PACKAGE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PACKAGE.parents[1]));sys.path.insert(0,str(PACKAGE/'runtime'))
import tools_owner as owner

class ToolsRecoveryTests(unittest.TestCase):
    def fixture(self,directory):
        root=Path(directory)/'target';root.mkdir();(root/'asset').write_text('old')
        old=owner.legacy_owner(PACKAGE);recovery=Path(directory)/'recovery'
        cp={'root':str(root),'source':'unused','source_ref':'unused','public':{'dependency_mode':'local_candidate'},
            'plan':{'upstream_source':{}},'phase':'complete','old_version':'old-guru',
            'controls':{},'peer_pointers':{},'upstream_ref':str(recovery/'public.json')}
        cp['preimages']=old.snapshot(root,recovery,{'asset'}, {})
        (root/'asset').write_text('new');cp['baseline']=old.current_baseline(root,cp)
        Path(cp['upstream_ref']).write_text('{}')
        return root,recovery,cp,old

    def test_incompatible_public_rollback_leaves_guru_half_unrestored(self):
        with tempfile.TemporaryDirectory() as d:
            root,recovery,cp,old=self.fixture(d)
            with patch.object(owner,'check_source'),patch.object(owner,'call',side_effect=ValueError('incompatible_restore')):
                with self.assertRaisesRegex(ValueError,'incompatible_restore'):owner.rollback(PACKAGE,root,recovery,cp)
            self.assertEqual((root/'asset').read_text(),'new')
            self.assertEqual((recovery/cp['preimages']['repo:asset']['backup']).read_text(),'old')

    def test_later_owned_edit_blocks_before_public_rollback(self):
        with tempfile.TemporaryDirectory() as d:
            root,recovery,cp,old=self.fixture(d);(root/'asset').write_text('later business-owned tool edit')
            with patch.object(owner,'check_source'),patch.object(owner,'call') as public:
                result=owner.rollback(PACKAGE,root,recovery,cp)
            self.assertEqual(result['exit_id'],'blocked');public.assert_not_called()
            self.assertEqual((root/'asset').read_text(),'later business-owned tool edit')

    def test_restore_uses_original_preimage_after_public_rollback(self):
        with tempfile.TemporaryDirectory() as d:
            root,recovery,cp,old=self.fixture(d)
            with patch.object(owner,'check_source'),patch.object(owner,'unchanged_peers'),patch.object(owner,'old_native_smoke'),patch.object(owner,'call',return_value={'status':'rolled_back'}):
                result=owner.rollback(PACKAGE,root,recovery,cp)
            self.assertEqual(result,{'exit_id':'rolled_back','installed_version':'old-guru'})
            self.assertEqual((root/'asset').read_text(),'old')
            self.assertEqual((recovery/cp['preimages']['repo:asset']['backup']).read_text(),'old')

    def test_resume_does_not_refresh_original_preimages_on_later_edits(self):
        with tempfile.TemporaryDirectory() as d:
            root,recovery,cp,old=self.fixture(d);before=json.dumps(cp['preimages'],sort_keys=True)
            (root/'asset').write_text('later work')
            with patch.object(owner,'check_source'):
                result=owner.resume(PACKAGE,root,recovery,cp)
            self.assertEqual(result['exit_id'],'blocked')
            self.assertEqual(json.dumps(cp['preimages'],sort_keys=True),before)

    def test_rollback_restores_or_removes_current_selection_and_preserves_legacy(self):
        for current_before in (None, b'{"schema_version":"3.0","hints":{}}\n'):
            with self.subTest(current_before=current_before), tempfile.TemporaryDirectory() as d:
                root,recovery,cp,old=self.fixture(d)
                legacy=root/'.trellis/.runtime/guru-team/python/active.json'
                current=legacy.with_name('selection-v3.json')
                legacy.parent.mkdir(parents=True)
                legacy.write_bytes(b'original legacy selection\n')
                if current_before is not None:
                    current.write_bytes(current_before)
                    current.chmod(0o640)
                selection_rows=old.snapshot(root,recovery/'selection',
                    {str(legacy.relative_to(root)),str(current.relative_to(root))},{})
                for row in selection_rows.values():
                    row['backup']='selection/'+row['backup']
                cp['preimages'].update(selection_rows)
                current.write_bytes(b'new current selection\n')
                cp['baseline']=old.current_baseline(root,cp)
                with patch.object(owner,'check_source'),patch.object(owner,'unchanged_peers'),patch.object(owner,'old_native_smoke'),patch.object(owner,'call',return_value={'status':'rolled_back'}):
                    result=owner.rollback(PACKAGE,root,recovery,cp)
                self.assertEqual('rolled_back',result['exit_id'])
                self.assertEqual(b'original legacy selection\n',legacy.read_bytes())
                if current_before is None:
                    self.assertFalse(current.exists())
                else:
                    self.assertEqual(current_before,current.read_bytes())
                    self.assertEqual(0o640,current.stat().st_mode & 0o777)
