#!/usr/bin/env python3
"""Focused tests for Guru Team preset installer behavior."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
import sys
from io import StringIO
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import apply_guru_team_trellis_preset as preset


class CodexDispatchModeInstallerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        (self.repo / ".trellis").mkdir()

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_missing_config_installs_sub_agent_default(self) -> None:
        payload = preset.ensure_codex_dispatch_mode(self.repo)

        self.assertEqual(payload["action"], "installed")
        text = (self.repo / ".trellis/config.yaml").read_text(encoding="utf-8")
        self.assertIn("codex:", text)
        self.assertIn("dispatch_mode: sub-agent", text)

    def test_commented_default_is_materialized_as_sub_agent(self) -> None:
        config = self.repo / ".trellis/config.yaml"
        config.write_text(
            "# codex:\n#   dispatch_mode: inline\n",
            encoding="utf-8",
        )

        payload = preset.ensure_codex_dispatch_mode(self.repo)

        self.assertEqual(payload["action"], "updated")
        self.assertEqual(payload["mode"], "sub-agent")
        text = config.read_text(encoding="utf-8")
        self.assertIn("codex:", text)
        self.assertIn("dispatch_mode: sub-agent", text)

    def test_explicit_inline_is_preserved(self) -> None:
        config = self.repo / ".trellis/config.yaml"
        config.write_text("codex:\n  dispatch_mode: inline\n", encoding="utf-8")

        payload = preset.ensure_codex_dispatch_mode(self.repo)

        self.assertEqual(payload["action"], "unchanged")
        self.assertEqual(payload["mode"], "inline")
        self.assertEqual(config.read_text(encoding="utf-8"), "codex:\n  dispatch_mode: inline\n")

    def test_invalid_value_is_replaced_with_sub_agent(self) -> None:
        config = self.repo / ".trellis/config.yaml"
        config.write_text("codex:\n  dispatch_mode: disabled\n", encoding="utf-8")

        payload = preset.ensure_codex_dispatch_mode(self.repo)

        self.assertEqual(payload["action"], "updated")
        self.assertEqual(payload["previous"], "disabled")
        self.assertIn("dispatch_mode: sub-agent", config.read_text(encoding="utf-8"))


class LanguageGuidanceInstallerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        (self.repo / ".trellis").mkdir()
        self.guru_root = preset.guru_root_from_script()
        self.workflow_src = self.guru_root / "trellis/workflows/guru-team"
        self.install_dst = self.repo / ".trellis/guru-team"

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_spec_index_english_language_rule_is_replaced_with_chinese(self) -> None:
        spec_index = self.repo / ".trellis/spec/backend/index.md"
        spec_index.parent.mkdir(parents=True)
        spec_index.write_text(
            "# Backend\n\n**Language**: All documentation must be written in **English**.\n",
            encoding="utf-8",
        )

        payload = preset.normalize_business_doc_language_guidance(self.repo)

        self.assertEqual(payload["replacement_count"], 1)
        self.assertEqual(payload["updated_paths"], [{"path": ".trellis/spec/backend/index.md", "replacements": 1}])
        self.assertIn(".trellis/spec/backend/index.md", payload["checked_paths"])
        text = spec_index.read_text(encoding="utf-8")
        self.assertIn("业务项目人类可读文档默认使用**中文**", text)
        self.assertNotIn("All documentation must be written in **English**", text)

    def test_workspace_indexes_english_language_rules_are_replaced_with_chinese(self) -> None:
        root_index = self.repo / ".trellis/workspace/index.md"
        user_index = self.repo / ".trellis/workspace/wumengye/index.md"
        user_index.parent.mkdir(parents=True)
        root_index.write_text(
            "**Language**: All documentation should be written in **English**.\n",
            encoding="utf-8",
        )
        user_index.write_text(
            "**Language**: All documentation must be written in **English**.\n",
            encoding="utf-8",
        )

        payload = preset.normalize_business_doc_language_guidance(self.repo)

        self.assertEqual(payload["replacement_count"], 2)
        self.assertEqual(
            payload["updated_paths"],
            [
                {"path": ".trellis/workspace/index.md", "replacements": 1},
                {"path": ".trellis/workspace/wumengye/index.md", "replacements": 1},
            ],
        )
        self.assertIn("业务项目人类可读文档默认使用**中文**", root_index.read_text(encoding="utf-8"))
        self.assertIn("业务项目人类可读文档默认使用**中文**", user_index.read_text(encoding="utf-8"))

    def test_bootstrap_guidelines_language_rule_is_replaced_with_chinese(self) -> None:
        bootstrap_prd = self.repo / ".trellis/tasks/00-bootstrap-guidelines/prd.md"
        bootstrap_prd.parent.mkdir(parents=True)
        bootstrap_prd.write_text(
            "# Bootstrap\n\n**Language**: All documentation must be written in **English**.\n",
            encoding="utf-8",
        )

        payload = preset.normalize_business_doc_language_guidance(self.repo)

        self.assertEqual(payload["replacement_count"], 1)
        self.assertEqual(
            payload["updated_paths"],
            [{"path": ".trellis/tasks/00-bootstrap-guidelines/prd.md", "replacements": 1}],
        )
        self.assertIn(".trellis/tasks/00-bootstrap-guidelines/**/*.md", payload["scope"])
        text = bootstrap_prd.read_text(encoding="utf-8")
        self.assertIn("业务项目人类可读文档默认使用**中文**", text)
        self.assertNotIn("All documentation must be written in **English**", text)

    def test_files_without_known_language_rule_remain_unchanged_and_docs_are_not_scanned(self) -> None:
        spec_index = self.repo / ".trellis/spec/backend/index.md"
        docs_file = self.repo / "docs/requirements/index.md"
        spec_index.parent.mkdir(parents=True)
        docs_file.parent.mkdir(parents=True)
        spec_text = "# Backend\n\nWrite examples with precise command names.\n"
        docs_text = "**Language**: All documentation must be written in **English**.\n"
        spec_index.write_text(spec_text, encoding="utf-8")
        docs_file.write_text(docs_text, encoding="utf-8")

        payload = preset.normalize_business_doc_language_guidance(self.repo)

        self.assertEqual(payload["action"], "checked")
        self.assertEqual(payload["replacement_count"], 0)
        self.assertEqual(payload["updated_paths"], [])
        self.assertIn(".trellis/spec/backend/index.md", payload["checked_paths"])
        self.assertNotIn("docs/requirements/index.md", payload["checked_paths"])
        self.assertEqual(spec_index.read_text(encoding="utf-8"), spec_text)
        self.assertEqual(docs_file.read_text(encoding="utf-8"), docs_text)

    def test_main_payload_reports_language_guidance(self) -> None:
        spec_index = self.repo / ".trellis/spec/backend/index.md"
        spec_index.parent.mkdir(parents=True)
        spec_index.write_text(
            "**Language**: All documentation must be written in **English**.\n",
            encoding="utf-8",
        )

        with mock.patch(
            "sys.argv",
            [
                "apply_guru_team_trellis_preset.py",
                "--repo",
                str(self.repo),
                "--platform",
                "codex",
            ],
        ):
            stdout = StringIO()
            with mock.patch("sys.stdout", stdout):
                exit_code = preset.main()

        payload = json.loads(stdout.getvalue())
        self.assertEqual(exit_code, 0)
        self.assertEqual(payload["language_guidance"]["replacement_count"], 1)
        self.assertEqual(payload["language_guidance"]["updated_paths"][0]["path"], ".trellis/spec/backend/index.md")
        self.assertIn(".trellis/spec/**/*.md", payload["language_guidance"]["scope"])


class PlatformOverlayInstallerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        (self.repo / ".trellis").mkdir()
        self.guru_root = preset.guru_root_from_script()
        self.workflow_src = self.guru_root / "trellis/workflows/guru-team"
        self.install_dst = self.repo / ".trellis/guru-team"

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def install(self, platforms: set[str] | None = None, all_platforms: bool = False) -> dict[str, object]:
        return preset.install_assets(self.workflow_src, self.install_dst, self.repo, platforms, all_platforms=all_platforms)

    def test_default_platforms_install_codex_cursor_and_shared_overlays(self) -> None:
        payload = self.install()

        self.assertEqual(payload["platforms"], ["codex", "cursor"])
        self.assertFalse(payload["all_platforms"])
        self.assertTrue((self.repo / ".agents/skills/trellis-start/SKILL.md").is_file())
        self.assertTrue((self.repo / ".trellis/agents/implement.md").is_file())
        self.assertIn("实现代理", (self.repo / ".trellis/agents/implement.md").read_text(encoding="utf-8"))
        self.assertTrue((self.repo / ".codex/prompts/trellis-start.md").is_file())
        self.assertTrue((self.repo / ".codex/agents/trellis-implement.toml").is_file())
        codex_implement = (self.repo / ".codex/agents/trellis-implement.toml").read_text(encoding="utf-8")
        self.assertIn("实现代理", codex_implement)
        self.assertIn('nickname_candidates = ["Implement Agent"', codex_implement)
        self.assertNotIn('nickname_candidates = ["实现代理"', codex_implement)
        self.assertTrue((self.repo / ".cursor/commands/trellis-continue.md").is_file())
        self.assertTrue((self.repo / ".cursor/agents/trellis-check.md").is_file())
        self.assertIn("阶段二检查代理", (self.repo / ".cursor/agents/trellis-check.md").read_text(encoding="utf-8"))
        self.assertFalse((self.repo / ".claude").exists())

    def test_repeated_default_apply_does_not_restore_unselected_claude_overlay(self) -> None:
        self.install()
        self.assertFalse((self.repo / ".claude").exists())

        second_payload = self.install()

        self.assertEqual(second_payload["platforms"], ["codex", "cursor"])
        self.assertFalse((self.repo / ".claude").exists())

    def test_explicit_claude_platform_installs_only_shared_and_claude_overlays(self) -> None:
        payload = self.install({"claude"})

        self.assertEqual(payload["platforms"], ["claude"])
        self.assertFalse(payload["all_platforms"])
        self.assertTrue((self.repo / ".agents/skills/trellis-start/SKILL.md").is_file())
        self.assertTrue((self.repo / ".trellis/agents/check.md").is_file())
        self.assertTrue((self.repo / ".claude/commands/trellis/continue.md").is_file())
        self.assertTrue((self.repo / ".claude/agents/trellis-implement.md").is_file())
        self.assertFalse((self.repo / ".codex").exists())
        self.assertFalse((self.repo / ".cursor").exists())

    def test_all_platforms_installs_historical_full_overlay_set(self) -> None:
        platforms, all_platforms = preset.selected_platforms(None, True)
        payload = self.install(platforms, all_platforms=all_platforms)

        self.assertTrue(all_platforms)
        self.assertEqual(payload["platforms"], ["claude", "codex", "cursor"])
        self.assertTrue((self.repo / ".agents/skills/trellis-start/SKILL.md").is_file())
        self.assertTrue((self.repo / ".trellis/agents/implement.md").is_file())
        self.assertTrue((self.repo / ".codex/prompts/trellis-start.md").is_file())
        self.assertTrue((self.repo / ".codex/agents/trellis-check.toml").is_file())
        self.assertTrue((self.repo / ".cursor/commands/trellis-continue.md").is_file())
        self.assertTrue((self.repo / ".cursor/agents/trellis-research.md").is_file())
        self.assertTrue((self.repo / ".claude/commands/trellis/continue.md").is_file())
        self.assertTrue((self.repo / ".claude/agents/trellis-research.md").is_file())

    def test_main_accepts_repeated_platform_arguments(self) -> None:
        with mock.patch(
            "sys.argv",
            [
                "apply_guru_team_trellis_preset.py",
                "--repo",
                str(self.repo),
                "--platform",
                "codex",
                "--platform",
                "cursor",
            ],
        ):
            with mock.patch("sys.stdout", new_callable=StringIO):
                exit_code = preset.main()

        self.assertEqual(exit_code, 0)
        self.assertTrue((self.repo / ".codex/prompts/trellis-start.md").is_file())
        self.assertTrue((self.repo / ".codex/agents/trellis-research.toml").is_file())
        self.assertTrue((self.repo / ".cursor/commands/trellis-continue.md").is_file())
        self.assertTrue((self.repo / ".cursor/agents/trellis-implement.md").is_file())
        self.assertFalse((self.repo / ".claude").exists())

    def test_known_trellis_agent_entries_are_replaced_with_chinese_overlays(self) -> None:
        existing = self.repo / ".codex/agents/trellis-check.toml"
        existing.parent.mkdir(parents=True)
        existing.write_text(
            'name = "trellis-check"\n'
            'description = "Workspace-write Trellis reviewer that self-fixes spec drift."\n'
            'sandbox_mode = "workspace-write"\n',
            encoding="utf-8",
        )

        payload = self.install({"codex"})

        self.assertIn(".codex/agents/trellis-check.toml", payload["replaced_overlays"])
        text = existing.read_text(encoding="utf-8")
        self.assertIn("阶段二检查代理", text)
        self.assertIn('nickname_candidates = ["Check Agent"', text)
        self.assertNotIn('nickname_candidates = ["阶段二检查代理"', text)

    def test_unknown_local_agent_edit_gets_new_copy(self) -> None:
        existing = self.repo / ".codex/agents/trellis-check.toml"
        existing.parent.mkdir(parents=True)
        existing.write_text(
            'name = "trellis-check"\n'
            'description = "Local custom reviewer without Trellis defaults."\n'
            'sandbox_mode = "workspace-write"\n',
            encoding="utf-8",
        )

        payload = self.install({"codex"})

        self.assertIn(".codex/agents/trellis-check.toml.new", payload["new_copies"])
        self.assertIn("Local custom reviewer", existing.read_text(encoding="utf-8"))
        self.assertTrue((self.repo / ".codex/agents/trellis-check.toml.new").is_file())

    def test_main_reports_explicit_all_platforms_only_for_all_platforms_flag(self) -> None:
        with mock.patch(
            "sys.argv",
            [
                "apply_guru_team_trellis_preset.py",
                "--repo",
                str(self.repo),
                "--platform",
                "codex",
                "--platform",
                "cursor",
                "--platform",
                "claude",
            ],
        ):
            stdout = StringIO()
            with mock.patch("sys.stdout", stdout):
                exit_code = preset.main()

        self.assertEqual(exit_code, 0)
        self.assertIn('"platforms": [', stdout.getvalue())
        self.assertIn('"all_platforms": false', stdout.getvalue())

    def test_main_rejects_platform_with_all_platforms(self) -> None:
        with mock.patch(
            "sys.argv",
            [
                "apply_guru_team_trellis_preset.py",
                "--repo",
                str(self.repo),
                "--platform",
                "codex",
                "--all-platforms",
            ],
        ):
            with self.assertRaises(SystemExit) as context:
                preset.main()

        self.assertNotEqual(context.exception.code, 0)

    def test_main_rejects_unknown_platform(self) -> None:
        with mock.patch(
            "sys.argv",
            [
                "apply_guru_team_trellis_preset.py",
                "--repo",
                str(self.repo),
                "--platform",
                "opencode",
            ],
        ):
            with self.assertRaises(SystemExit) as context:
                preset.main()

        self.assertNotEqual(context.exception.code, 0)


class ExtensionManifestInstallerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        (self.repo / ".trellis").mkdir()
        self.guru_root = preset.guru_root_from_script()
        self.workflow_src = self.guru_root / "trellis/workflows/guru-team"
        self.install_dst = self.repo / ".trellis/guru-team"

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_install_assets_writes_installed_extension_manifest(self) -> None:
        payload = preset.install_assets(self.workflow_src, self.install_dst, self.repo, {"codex", "cursor"})

        manifest_path = self.repo / ".trellis/guru-team/extension.json"
        self.assertTrue(manifest_path.is_file())
        installed = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(installed["extension"]["extension_id"], "guru-team")
        self.assertEqual(installed["extension"]["version"], payload["guru_team_extension"]["version"])
        self.assertEqual(installed["extension"]["version"], "0.6.5-guru.1")
        self.assertEqual(installed["extension"]["target_trellis_cli"], "0.6.5")
        self.assertEqual(payload["guru_team_extension"]["target_trellis_cli"], "0.6.5")
        self.assertEqual(payload["guru_team_extension"]["trellis_cli_compatibility"], "0.6.5")
        self.assertEqual(payload["guru_team_extension"]["tested_trellis_cli"], ["0.6.5"])
        self.assertEqual(installed["install"]["selected_platforms"], ["codex", "cursor"])
        self.assertIn("observed at apply time", installed["notes"])
        self.assertIn("not a claim", installed["notes"])
        self.assertEqual(payload["extension_manifest"], ".trellis/guru-team/extension.json")

    def test_main_version_prints_canonical_extension_version(self) -> None:
        with mock.patch("sys.argv", ["apply_guru_team_trellis_preset.py", "--version"]):
            stdout = StringIO()
            with mock.patch("sys.stdout", stdout):
                exit_code = preset.main()

        self.assertEqual(exit_code, 0)
        self.assertRegex(stdout.getvalue().strip(), r"^\d+\.\d+\.\d+")

    def test_source_provenance_reports_archive_without_git_metadata(self) -> None:
        with mock.patch.object(preset, "run_git") as run_git:
            run_git.return_value = mock.Mock(returncode=1, stdout="", stderr="not a git repo")

            provenance = preset.source_provenance(self.guru_root)

        self.assertEqual(provenance["tree_state"], "archive")
        self.assertIsNone(provenance["commit"])

    def test_source_provenance_reports_dirty_git_tree(self) -> None:
        def fake_git(args: list[str], cwd: Path) -> mock.Mock:
            command = " ".join(args)
            if command == "rev-parse --show-toplevel":
                return mock.Mock(returncode=0, stdout=str(self.guru_root), stderr="")
            if command == "remote get-url origin":
                return mock.Mock(returncode=0, stdout="https://github.com/castbox/guru-trellis.git\n", stderr="")
            if command == "rev-parse --abbrev-ref HEAD":
                return mock.Mock(returncode=0, stdout="main\n", stderr="")
            if command == "rev-parse HEAD":
                return mock.Mock(returncode=0, stdout="abc123\n", stderr="")
            if command == "describe --tags --exact-match HEAD":
                return mock.Mock(returncode=1, stdout="", stderr="")
            if command == "status --short":
                return mock.Mock(returncode=0, stdout=" M README.md\n", stderr="")
            return mock.Mock(returncode=1, stdout="", stderr="")

        with mock.patch.object(preset, "run_git", side_effect=fake_git):
            provenance = preset.source_provenance(self.guru_root)

        self.assertEqual(provenance["tree_state"], "dirty")
        self.assertTrue(provenance["is_mutable_ref"])
        self.assertEqual(provenance["source_ref"] if "source_ref" in provenance else provenance["ref"], "main")


if __name__ == "__main__":
    unittest.main()
