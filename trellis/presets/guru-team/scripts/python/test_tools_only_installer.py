"""Tools-only reuse of preset writer must preserve legacy Task documentation."""
import tempfile
import unittest
from pathlib import Path
import apply_guru_team_trellis_preset as preset

class ToolsOnlyLanguageTests(unittest.TestCase):
    def test_task_guidance_excluded_from_inventory_and_real_writer(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            task=root/'.trellis/tasks/00-bootstrap-guidelines/prd.md'
            spec=root/'.trellis/spec/index.md'
            task.parent.mkdir(parents=True);spec.parent.mkdir(parents=True)
            original=preset.ENGLISH_LANGUAGE_RULES[0]
            task.write_text(original);spec.write_text(original)
            paths=preset.managed_transaction_paths(root,root/'.trellis/guru-team',{'codex'},None,source_projections={},tools_only=True)
            self.assertNotIn(task.relative_to(root),paths)
            self.assertNotIn(spec.relative_to(root),paths)
            result=preset.normalize_business_doc_language_guidance(root,tools_only=True)
            self.assertEqual(task.read_text(),original)
            self.assertEqual(spec.read_text(),original)
            self.assertNotIn(task.relative_to(root).as_posix(),result['checked_paths'])
            # Ordinary full installation keeps its existing Task guidance behavior.
            preset.normalize_business_doc_language_guidance(root)
            self.assertNotEqual(task.read_text(),original)


class ToolsMaintenancePrerequisiteTests(unittest.TestCase):
    def test_actual_applied_operation_and_public_api_are_required_without_task_parser(self):
        from unittest import mock
        from delivery_installation import require_tools_maintenance_installation
        with tempfile.TemporaryDirectory() as temp:
            target=Path(temp)
            plan={'kind':'tools_install','operation_id':'same-operation','target_root':str(target)}
            maintenance={'source':{'dependency_mode':'local_candidate'},'plan':plan,'recovery_ref':'original-recovery'}
            applied={'operation_id':'same-operation','kind':'tools_install','status':'applied'}
            with mock.patch('runtime.maintenance_transport.call',side_effect=[{'operation_id':'same-operation'},applied]), mock.patch('delivery_installation.installed_capabilities',return_value=[]) as capabilities:
                result=require_tools_maintenance_installation(target,maintenance)
                self.assertEqual(result['task_inventory'],'preserved_unparsed')
                self.assertEqual(capabilities.call_args.args[2],[])
            with mock.patch('runtime.maintenance_transport.call',side_effect=[{'operation_id':'same-operation'},{**applied,'status':'pending'}]), mock.patch('delivery_installation.installed_capabilities') as capabilities:
                with self.assertRaises(SystemExit):require_tools_maintenance_installation(target,maintenance)
                capabilities.assert_not_called()

if __name__=='__main__':unittest.main()
