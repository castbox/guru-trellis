"""Transaction-focused tests for the Guru Team preset installer."""

from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import test_apply_guru_team_trellis_preset as parent

preset = parent.preset
_RUNTIME_RESULT = parent._RUNTIME_RESULT
STAGE0_SKILL_IDS = parent.STAGE0_SKILL_IDS
install_canonical_workflow = parent.install_canonical_workflow

class PresetTransactionInstallerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        (self.repo / ".trellis").mkdir()
        install_canonical_workflow(self.repo)
        self.guru_root = preset.guru_root_from_script()
        self.workflow_src = self.guru_root / "trellis/workflows/guru-team"
        self.install_dst = self.repo / ".trellis/guru-team"
        fresh = preset.install_assets(
            self.workflow_src,
            self.install_dst,
            self.repo,
            {"codex", "cursor", "claude"},
            all_platforms=True,
        )
        self.assertEqual(fresh["skill_packages"]["status"], "ok")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def install_current(self) -> dict[str, object]:
        return preset.install_assets(
            self.workflow_src,
            self.install_dst,
            self.repo,
            {"codex", "cursor", "claude"},
            all_platforms=True,
        )

    def managed_graph_snapshot(self) -> dict[str, tuple[bytes, int]]:
        extension_path = self.install_dst / "extension.json"
        extension = json.loads(extension_path.read_text(encoding="utf-8"))
        managed_paths = set(extension["install"]["managed_assets"])
        managed_paths.update(record["path"] for record in extension["skill_packages"]["files"])
        managed_paths.add(".trellis/guru-team/extension.json")
        snapshot: dict[str, tuple[bytes, int]] = {}
        for relative in sorted(managed_paths):
            path = self.repo / relative
            self.assertTrue(path.is_file(), relative)
            snapshot[relative] = (path.read_bytes(), path.stat().st_mode & 0o777)
        return snapshot

    def assert_stage0_contract_state(
        self,
        interface_schema_id: str,
        interface_version: str,
    ) -> None:
        registry = json.loads((self.install_dst / "skills/registry.json").read_text(encoding="utf-8"))
        entries = {str(entry["id"]): entry for entry in registry["skills"]}
        for skill_id in STAGE0_SKILL_IDS:
            self.assertEqual(entries[skill_id]["interface_schema_id"], interface_schema_id)
            for root in (
                self.install_dst / "skills/packages",
                self.repo / ".agents/skills",
                self.repo / ".codex/skills",
                self.repo / ".cursor/skills",
                self.repo / ".claude/skills",
            ):
                interface = json.loads((root / skill_id / "interface.json").read_text(encoding="utf-8"))
                self.assertEqual(interface["schema_version"], interface_version)

    def test_transaction_staging_excludes_existing_developer_identity(self) -> None:
        developer_identity = self.repo / ".trellis/.developer/identity.json"
        developer_identity.parent.mkdir(parents=True)
        identity_bytes = b'{"name":"fixture-maintainer"}\n'
        developer_identity.write_bytes(identity_bytes)

        with tempfile.TemporaryDirectory() as temporary:
            staging_repo = Path(temporary) / "repo"
            inventory = preset.managed_transaction_paths(
                self.repo,
                self.install_dst,
                {"codex", "cursor", "claude"},
                True,
                json.loads((self.install_dst / "extension.json").read_text(encoding="utf-8")),
            )
            staging_repo.mkdir(parents=True)
            preset.materialize_managed_preimage(self.repo, staging_repo, inventory)

            self.assertFalse((staging_repo / ".trellis/.developer").exists())
            self.assertTrue((staging_repo / ".trellis/guru-team/extension.json").is_file())

        self.assertEqual(developer_identity.read_bytes(), identity_bytes)

    def test_managed_transaction_does_not_materialize_unmanaged_repository_content(self) -> None:
        manifest = json.loads((self.install_dst / "extension.json").read_text(encoding="utf-8"))
        baseline_inventory = preset.managed_transaction_paths(
            self.repo,
            self.install_dst,
            {"codex", "cursor", "claude"},
            True,
            manifest,
        )
        unmanaged = self.repo / "build-output" / "nested-repository" / "dependency.bin"
        unmanaged.parent.mkdir(parents=True)
        unmanaged.write_bytes(b"x" * (1024 * 1024))
        (self.repo / "untracked-large.bin").write_bytes(b"y" * (1024 * 1024))
        inventory = preset.managed_transaction_paths(
            self.repo,
            self.install_dst,
            {"codex", "cursor", "claude"},
            True,
            manifest,
        )
        self.assertEqual(inventory, baseline_inventory)
        self.assertNotIn(Path("build-output/nested-repository/dependency.bin"), inventory)
        self.assertNotIn(Path("untracked-large.bin"), inventory)
        with tempfile.TemporaryDirectory() as temporary:
            temporary_root = Path(temporary)
            staging_repo = temporary_root / "repo"
            source_projections = preset.managed_source_projections(
                self.repo,
                self.install_dst,
                {"codex", "cursor", "claude"},
            )
            preflight = preset.preflight_managed_transaction(
                temporary_root,
                self.repo,
                inventory,
                source_projections,
            )
            staging_repo.mkdir()
            preimage = preset.materialize_managed_preimage(self.repo, staging_repo, inventory)
            self.assertEqual(preimage["bytes"], preflight["managed_bytes"])
            self.assertFalse((staging_repo / "build-output").exists())
            self.assertFalse((staging_repo / "untracked-large.bin").exists())
            self.assertEqual(preimage["file_count"], len(inventory))

    def test_space_preflight_counts_target_projections_and_fails_before_materialization(self) -> None:
        source_projections = preset.managed_source_projections(
            self.repo,
            self.install_dst,
            {"codex", "cursor", "claude"},
        )
        projected_source_bytes = sum(
            source.stat().st_size for source in source_projections.values()
        )
        unique_source_bytes = sum(
            source.stat().st_size for source in set(source_projections.values())
        )
        self.assertGreater(projected_source_bytes, unique_source_bytes)

        with (
            mock.patch.object(
                preset.shutil,
                "disk_usage",
                return_value=mock.Mock(free=0),
            ),
            mock.patch.object(preset, "materialize_managed_preimage") as materialize,
        ):
            with self.assertRaises(SystemExit) as raised:
                self.install_current()

        materialize.assert_not_called()
        payload = json.loads(str(raised.exception))
        self.assertEqual(payload["code"], "insufficient_managed_staging_space")
        self.assertEqual(payload["strategy"], "managed_paths")
        self.assertEqual(payload["available_bytes"], 0)
        self.assertEqual(payload["source_bytes"], projected_source_bytes)
        self.assertEqual(payload["source_projection_count"], len(source_projections))
        self.assertGreater(payload["estimated_peak_bytes"], payload["source_bytes"])
        self.assertEqual(payload["cleanup"], "temporary_lifecycle")

    def test_reapply_does_not_use_whole_repository_copy(self) -> None:
        with mock.patch.object(shutil, "copytree", side_effect=AssertionError("whole-repo copy")):
            result = self.install_current()
        self.assertEqual(result["skill_packages"]["status"], "ok")
        self.assertEqual(result["managed_transaction"]["strategy"], "managed_paths")

    def test_current_reapply_remains_valid(self) -> None:
        with mock.patch.object(
            preset,
            "ensure_managed_python_runtime",
            return_value=_RUNTIME_RESULT,
        ) as runtime:
            completed = self.install_current()

        self.assertEqual(completed["skill_packages"]["status"], "ok")
        self.assertEqual(
            [call.kwargs["activate"] for call in runtime.call_args_list],
            [False, True],
        )
        self.assertEqual(completed["skill_packages"]["sidecars"], [])
        self.assertEqual(completed["skill_installed_validation"]["returncode"], 0)
        self.assert_stage0_contract_state("guru-team-skill-interface-1.4", "1.4")
        self.assertTrue(
            (self.install_dst / "skills/schemas/skill-interface-1.5.schema.json").is_file()
        )
        self.assertTrue(
            (self.install_dst / "skills/schemas/skill-interface-1.6.schema.json").is_file()
        )

    def test_installs_only_declared_runtime_kernel_files(self) -> None:
        completed = self.install_current()

        self.assertEqual(completed["skill_packages"]["status"], "ok")
        runtime_root = self.install_dst / "runtime"
        installed = {
            path.relative_to(runtime_root)
            for path in runtime_root.rglob("*")
            if path.is_file()
        }
        self.assertEqual(installed, set(preset.SKILL_RUNTIME_KERNEL_PATHS))
        for relative in preset.SKILL_RUNTIME_KERNEL_PATHS:
            source = self.guru_root / "trellis/skills/guru-team/runtime" / relative
            target = runtime_root / relative
            self.assertEqual(target.read_bytes(), source.read_bytes())
            self.assertEqual(bool(target.stat().st_mode & 0o100), bool(source.stat().st_mode & 0o100))
        self.assertFalse((runtime_root / "tests").exists())
        self.assertFalse((runtime_root / "__pycache__").exists())
        self.assertFalse(any(path.suffix in {".pyc", ".pyo"} for path in installed))
        self.assertTrue(
            (self.install_dst / "skills/schemas/skill-registry-1.4.schema.json").is_file()
        )
        self.assertTrue((self.install_dst / "skills/contracts/production-current.json").is_file())
        self.assertTrue((self.install_dst / "skills/contracts/production-current-2.0.json").is_file())
        self.assertTrue((self.install_dst / "skills/contracts/production-current-3.0.json").is_file())
        self.assertTrue((self.install_dst / "skills/contracts/production-current-4.0.json").is_file())
        self.assertTrue((self.install_dst / "skills/schemas/production-contract-manifest.schema.json").is_file())
        self.assertTrue((self.install_dst / "skills/schemas/production-contract-manifest-2.0.schema.json").is_file())
        self.assertTrue((self.install_dst / "skills/schemas/production-contract-manifest-3.0.schema.json").is_file())
        self.assertTrue((self.install_dst / "skills/schemas/production-contract-manifest-4.0.schema.json").is_file())
        self.assertEqual(
            (self.install_dst / "skills/contracts/production-current.json").read_bytes(),
            (self.install_dst / "skills/contracts/production-current-4.0.json").read_bytes(),
        )
        for legacy in ("production-current-2.0.json", "production-current-3.0.json"):
            self.assertEqual(
                (self.install_dst / "skills/contracts" / legacy).read_bytes(),
                (self.guru_root / "trellis/skills/guru-team/contracts" / legacy).read_bytes(),
            )
        self.assertEqual(
            {
                path.name
                for path in (self.install_dst / "skills/schemas").iterdir()
                if path.is_file()
            },
            set(preset.CURRENT_SKILL_SHARED_SCHEMAS),
        )

    def test_unknown_local_edit_conflict_preserves_current_graph(self) -> None:
        target = self.install_dst / "skills/packages/guru-sync-base/SKILL.md"
        target.write_text(target.read_text(encoding="utf-8") + "\nlocal current edit\n", encoding="utf-8")
        before = self.managed_graph_snapshot()
        extension_before = (self.install_dst / "extension.json").read_bytes()

        with mock.patch.object(
            preset,
            "ensure_managed_python_runtime",
            return_value=_RUNTIME_RESULT,
        ) as runtime:
            result = self.install_current()

        self.assertEqual(result["skill_packages"]["status"], "conflict")
        self.assertEqual(
            [call.kwargs["activate"] for call in runtime.call_args_list],
            [False],
        )
        self.assertNotEqual(result["skill_installed_validation"]["returncode"], 0)
        self.assertEqual(self.managed_graph_snapshot(), before)
        self.assertEqual((self.install_dst / "extension.json").read_bytes(), extension_before)
        self.assert_stage0_contract_state("guru-team-skill-interface-1.4", "1.4")
        sidecar = target.with_name("SKILL.md.new")
        self.assertEqual(
            sidecar.read_bytes(),
            (self.guru_root / "trellis/skills/guru-team/packages/guru-sync-base/SKILL.md").read_bytes(),
        )

    def test_reapply_after_unknown_edit_sidecar_handling_recovers_current_install(self) -> None:
        target = self.install_dst / "skills/packages/guru-sync-base/SKILL.md"
        target.write_text(target.read_text(encoding="utf-8") + "\nlocal current edit\n", encoding="utf-8")
        conflicted = self.install_current()
        self.assertEqual(conflicted["skill_packages"]["status"], "conflict")
        sidecar = target.with_name("SKILL.md.new")
        target.write_bytes(sidecar.read_bytes())
        sidecar.unlink()

        recovered = self.install_current()
        self.assertEqual(recovered["skill_packages"]["status"], "ok")
        self.assert_stage0_contract_state("guru-team-skill-interface-1.4", "1.4")
        self.assertEqual(recovered["skill_installed_validation"]["returncode"], 0)

    def test_forced_installed_validation_failure_preserves_current_graph(self) -> None:
        before = self.managed_graph_snapshot()
        original_validator = preset.run_skill_package_validator

        def forced_validation(
            repo: Path,
            guru_root: Path,
            mode: str,
            python: Path | None = None,
        ) -> dict[str, object]:
            if mode == "source":
                return original_validator(repo, guru_root, mode, python)
            return {
                "status": "failed",
                "mode": "installed",
                "facts": {},
                "errors": ["forced installed validation failure"],
                "returncode": 2,
            }

        with mock.patch.object(preset, "run_skill_package_validator", side_effect=forced_validation):
            with mock.patch.object(
                preset,
                "ensure_managed_python_runtime",
                return_value=_RUNTIME_RESULT,
            ) as runtime:
                result = self.install_current()

        self.assertEqual(result["skill_installed_validation"]["errors"], ["forced installed validation failure"])
        self.assertEqual(
            [call.kwargs["activate"] for call in runtime.call_args_list],
            [False],
        )
        self.assertEqual(self.managed_graph_snapshot(), before)
        self.assert_stage0_contract_state("guru-team-skill-interface-1.4", "1.4")


if __name__ == "__main__":
    unittest.main()
