"""Original owners read the archive and retain original-path attribution."""
from __future__ import annotations
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

PACKAGES = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PACKAGES.parent))
from runtime.io import CommandError
from runtime.schema import validate_json

OWNERS = ('guru-publish-task-delivery', 'guru-merge-task-delivery', 'guru-finish-task',
          'guru-approve-task-plan', 'guru-check-task', 'guru-review-branch')


class ArchiveControlTests(unittest.TestCase):
    def test_six_original_owners_inspect_freeze_retire_restore_archive_source(self):
        for name in OWNERS:
            with self.subTest(owner=name), tempfile.TemporaryDirectory() as temporary:
                package = PACKAGES / name
                spec = importlib.util.spec_from_file_location(name.replace('-', '_'), package/'runtime/legacy_maintenance.py')
                owner = importlib.util.module_from_spec(spec); spec.loader.exec_module(owner)
                root = Path(temporary)
                if hasattr(owner, 'ARTIFACT'):
                    gate = json.loads((package/'tests/fixtures/legacy-gate.json').read_text())
                    original_ref = gate[owner.IDENTITY_FIELD]
                    task_id = Path(original_ref).name
                    control = owner.CONTROL_ROOT + task_id + '/' + owner.ARTIFACT
                else:
                    task_id = 'selected'
                    original_ref = '.trellis/tasks/selected'
                    gate = {'public_input': {'task_id': task_id, 'lifecycle_generation': 0, 'task_ref': original_ref}}
                    control = owner.CONTROL_ROOT + 'selected.json'
                archive = '.trellis/tasks/archive/2026-10/' + task_id
                source = root/archive/'task.json'; source.parent.mkdir(parents=True)
                source.write_text(json.dumps({'id': task_id, 'status': 'completed'}))
                file = root/control; file.parent.mkdir(parents=True); file.write_text(json.dumps(gate))
                file.chmod(0o640)
                preimage = owner.raw(file)
                key = {'task_id': task_id, 'lifecycle_generation': 0}
                selected = {'root': str(root), 'key': key, 'task_ref': original_ref, 'source_task_ref': archive}
                def invoke(profile, **fields):
                    public = {'profile': profile, **selected, **fields}
                    validate_json(public, package/'schemas/legacy-maintenance-input-1.0.schema.json', 'input')
                    return owner.execute(package, public)
                inspected = invoke('legacy_control_inspection', control_refs=[control])
                frozen = invoke('legacy_control_freeze', controls=inspected['controls'], source=owner.raw(source), operation_id='archive-operation')
                retired = invoke('legacy_control_retirement', control_refs=[control], preserved_source_ref=archive+'/task.json', recovery_ref=frozen['recovery_ref'])
                self.assertEqual(retired['exit_id'], 'legacy_controls_retired')
                self.assertFalse(file.exists())
                self.assertFalse((root/original_ref).exists())
                owner.precheck_restore(frozen['recovery_ref'])
                owner.restore_controls(frozen['recovery_ref'])
                self.assertEqual(owner.raw(file), preimage)
                self.assertEqual(json.loads(source.read_text())['id'], task_id)

    def test_terminal_finish_remains_readable_and_is_not_retired(self):
        package = PACKAGES/'guru-finish-task'
        spec = importlib.util.spec_from_file_location('finish_archive_controls', package/'runtime/legacy_maintenance.py')
        owner = importlib.util.module_from_spec(spec); spec.loader.exec_module(owner)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); archive = '.trellis/tasks/archive/2026-10/selected'
            source = root/archive/'task.json'; source.parent.mkdir(parents=True)
            source.write_text(json.dumps({'id': 'selected'}))
            control = owner.CONTROL_ROOT+'terminal.json'; file = root/control
            file.parent.mkdir(parents=True)
            file.write_text(json.dumps({'stage': 'success', 'task_ref': '.trellis/tasks/selected'}))
            before = file.read_bytes()
            with self.assertRaises(CommandError) as raised:
                owner.inspect_controls(root, {'task_id': 'selected', 'lifecycle_generation': 0}, '.trellis/tasks/selected', [control], archive)
            self.assertEqual(raised.exception.code, 'terminal_result_preserved')
            self.assertEqual(file.read_bytes(), before)


if __name__ == '__main__': unittest.main()
