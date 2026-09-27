"""Old managed companion-script reapply coverage shared by the installer fixture."""

import hashlib
import json
import subprocess
from pathlib import Path
from unittest import mock

import apply_guru_team_trellis_preset as preset


class RetiredScriptReapplyTests:
    def test_retired_script_hashes_cover_managed_git_history(self) -> None:
        for relative, known_hashes in preset.LEGACY_MANAGED_ASSET_HASHES.items():
            if relative.parts[:2] != ("scripts", "bash"):
                continue
            source_path = f".trellis/guru-team/{relative.as_posix()}"
            revisions = subprocess.run(
                ["git", "log", "--all", "--format=%H", "--", source_path],
                cwd=self.guru_root,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.splitlines()
            self.assertTrue(revisions, source_path)
            for revision in revisions:
                old = subprocess.run(
                    ["git", "show", f"{revision}:{source_path}"],
                    cwd=self.guru_root,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                )
                if old.returncode == 0:
                    with self.subTest(path=source_path, revision=revision):
                        self.assertIn(hashlib.sha256(old.stdout).hexdigest(), known_hashes)

    def test_reapply_removes_known_retired_start_task_entry(self) -> None:
        self.install({"codex"})
        target = self.install_dst / "scripts/bash/start-task.sh"
        target.parent.mkdir(parents=True, exist_ok=True)
        legacy = b"#!/bin/sh\nexit 0\n"
        target.write_bytes(legacy)
        target.chmod(0o755)
        with mock.patch.dict(preset.LEGACY_MANAGED_ASSET_HASHES, {
            Path("scripts/bash/start-task.sh"): frozenset({hashlib.sha256(legacy).hexdigest()}),
        }):
            result = self.install({"codex"})

        self.assertFalse(target.exists())
        self.assertIn({
            "path": ".trellis/guru-team/scripts/bash/start-task.sh",
            "action": "removed_managed",
            "previous_managed_sha256": hashlib.sha256(legacy).hexdigest(),
        }, result["skill_packages"]["removals"])
        self.assertEqual(result["skill_packages"]["status"], "ok")

    def test_reapply_preserves_edited_retired_start_task_entry(self) -> None:
        self.install({"codex"})
        target = self.install_dst / "scripts/bash/start-task.sh"
        target.write_text("#!/bin/sh\n# local edit\n", encoding="utf-8")

        result = self.install({"codex"})

        self.assertTrue(target.is_file())
        self.assertEqual(result["skill_packages"]["status"], "conflict")
        self.assertTrue(target.with_name("start-task.sh.new").is_file())

    def test_reapply_uses_prior_managed_hash_for_retired_start_task(self) -> None:
        self.install({"codex"})
        target = self.install_dst / "scripts/bash/start-task.sh"
        legacy = b"#!/bin/sh\n# prior managed version\n"
        target.write_bytes(legacy)
        manifest_path = self.install_dst / "extension.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        relative = ".trellis/guru-team/scripts/bash/start-task.sh"
        manifest["install"]["managed_assets"].append(relative)
        manifest["install"]["managed_asset_hashes"][relative] = hashlib.sha256(legacy).hexdigest()
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

        result = self.install({"codex"})

        self.assertFalse(target.exists())
        self.assertEqual(result["skill_packages"]["status"], "ok")

    def test_reapply_retires_all_scripts_from_pre_interpreter_install(self) -> None:
        self.install({"codex"})
        old_commit = "1092865fce6a25cd414d810140e03132d88a35d5"
        manifest_path = self.install_dst / "extension.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        retired = [
            path for path in preset.LEGACY_MANAGED_ASSET_HASHES
            if path.parts[:2] == ("scripts", "bash")
        ]
        self.assertEqual(len(retired), 18)
        for relative in retired:
            old = subprocess.run(
                ["git", "show", f"{old_commit}:.trellis/guru-team/{relative.as_posix()}"],
                cwd=self.guru_root,
                check=True,
                stdout=subprocess.PIPE,
            ).stdout
            target = self.install_dst / relative
            target.write_bytes(old)
            installed_path = f".trellis/guru-team/{relative.as_posix()}"
            manifest["install"]["managed_assets"].append(installed_path)
            manifest["install"]["managed_asset_hashes"].pop(installed_path, None)
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

        result = self.install({"codex"})

        self.assertEqual(result["skill_packages"]["status"], "ok")
        self.assertTrue(all(not (self.install_dst / relative).exists() for relative in retired))

    def test_reapply_retires_older_scripts_without_manifest_hashes(self) -> None:
        retired = [
            path for path in preset.LEGACY_MANAGED_ASSET_HASHES
            if path.parts[:2] == ("scripts", "bash")
        ]
        for revision in ("0b46f0b0", "c89da4aa", "35bb6337"):
            with self.subTest(revision=revision):
                self.install({"codex"})
                manifest_path = self.install_dst / "extension.json"
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                for relative in retired:
                    old = subprocess.run(
                        ["git", "show", f"{revision}:.trellis/guru-team/{relative.as_posix()}"],
                        cwd=self.guru_root,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.DEVNULL,
                    )
                    if old.returncode != 0:
                        continue
                    target = self.install_dst / relative
                    target.write_bytes(old.stdout)
                    installed_path = f".trellis/guru-team/{relative.as_posix()}"
                    manifest["install"]["managed_assets"].append(installed_path)
                    manifest["install"]["managed_asset_hashes"].pop(installed_path, None)
                manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

                result = self.install({"codex"})

                self.assertEqual(result["skill_packages"]["status"], "ok")
                self.assertTrue(all(not (self.install_dst / relative).exists() for relative in retired))

    def test_reapply_preserves_edited_legacy_conflict_sidecar(self) -> None:
        self.install({"codex"})
        target = self.install_dst / "scripts/bash/start-task.sh"
        target.write_text("#!/bin/sh\n# local edit\n", encoding="utf-8")
        first = self.install({"codex"})
        self.assertEqual(first["skill_packages"]["status"], "conflict")
        sidecar = target.with_name("start-task.sh.new")
        sidecar.write_text("manual resolution in progress\n", encoding="utf-8")

        second = self.install({"codex"})

        self.assertEqual(second["skill_packages"]["status"], "conflict")
        self.assertEqual(sidecar.read_text(encoding="utf-8"), "manual resolution in progress\n")
