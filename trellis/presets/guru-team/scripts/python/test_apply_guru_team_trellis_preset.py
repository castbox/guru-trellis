#!/usr/bin/env python3
"""Focused tests for Guru Team preset installer behavior."""

from __future__ import annotations

import json
import os
import re
import subprocess
import tempfile
import importlib.util
import types
import unittest
from pathlib import Path
import sys
from io import StringIO
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import apply_guru_team_trellis_preset as preset


STALE_PLANNING_HINTS = (
    "Task `design.md` - Technical design (if exists)",
    "Task `implement.md` - Execution plan (if exists)",
    "design.md` if present",
    "implement.md` if present",
    "design.md if present",
    "implement.md if present",
    "optional `design.md` / `implement.md`",
    "technical design and implementation plan when present",
)


def assert_required_planning_context(testcase: unittest.TestCase, text: str) -> None:
    testcase.assertIn("Task `design.md` - required Guru Team technical design", text)
    testcase.assertIn("Task `implement.md` - required Guru Team execution plan", text)
    for stale_hint in STALE_PLANNING_HINTS:
        testcase.assertNotIn(stale_hint, text)


def install_canonical_workflow(repo: Path) -> None:
    source = preset.guru_root_from_script() / "trellis/workflows/guru-team/workflow.md"
    target = repo / ".trellis/workflow.md"
    target.write_bytes(source.read_bytes())


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


class FinishSummaryPresetPolicyTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        (self.repo / ".trellis").mkdir()

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_session_auto_commit_missing_true_false_and_invalid_values(self) -> None:
        config = self.repo / ".trellis/config.yaml"
        cases = [
            ("# config\n", None, "updated"),
            ("session_auto_commit: true\n", "true", "updated"),
            ("session_auto_commit: false\n", "false", "unchanged"),
            ("session_auto_commit: sometimes\n", "sometimes", "updated"),
        ]
        for content, previous, action in cases:
            with self.subTest(content=content):
                config.write_text(content, encoding="utf-8")
                payload = preset.ensure_session_auto_commit_false(self.repo)
                self.assertEqual(payload["action"], action)
                self.assertEqual(payload["previous"], previous)
                text = config.read_text(encoding="utf-8")
                self.assertEqual(sum(line == "session_auto_commit: false" for line in text.splitlines()), 1)

    def test_duplicate_active_session_auto_commit_keys_fail_closed(self) -> None:
        config = self.repo / ".trellis/config.yaml"
        config.write_text("session_auto_commit: true\nsession_auto_commit: false\n", encoding="utf-8")
        with self.assertRaises(SystemExit):
            preset.ensure_session_auto_commit_false(self.repo)

    def test_workspace_ignore_is_idempotent_and_does_not_write_workspace(self) -> None:
        first = preset.ensure_workspace_gitignore(self.repo)
        second = preset.ensure_workspace_gitignore(self.repo)
        self.assertEqual(first["action"], "installed")
        self.assertEqual(second["action"], "unchanged")
        text = (self.repo / ".gitignore").read_text(encoding="utf-8")
        self.assertEqual(text.splitlines().count(".trellis/workspace/"), 1)
        self.assertFalse((self.repo / ".trellis/workspace").exists())


class LanguageGuidanceInstallerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        (self.repo / ".trellis").mkdir()
        install_canonical_workflow(self.repo)
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

    def test_workspace_indexes_are_not_scanned_or_rewritten(self) -> None:
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

        self.assertEqual(payload["replacement_count"], 0)
        self.assertEqual(payload["updated_paths"], [])
        self.assertNotIn(".trellis/workspace/index.md", payload["checked_paths"])
        self.assertIn("All documentation should be written in **English**", root_index.read_text(encoding="utf-8"))
        self.assertIn("All documentation must be written in **English**", user_index.read_text(encoding="utf-8"))

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
        install_canonical_workflow(self.repo)
        self.guru_root = preset.guru_root_from_script()
        self.workflow_src = self.guru_root / "trellis/workflows/guru-team"
        self.install_dst = self.repo / ".trellis/guru-team"

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_upstream_ownership_failure_precedes_every_target_mutation(self) -> None:
        before = {
            path.relative_to(self.repo).as_posix(): path.read_bytes()
            for path in self.repo.rglob("*")
            if path.is_file()
        }
        with mock.patch.object(
            preset,
            "run_upstream_ownership_validator",
            side_effect=SystemExit("fixture ownership failure"),
        ):
            with self.assertRaisesRegex(SystemExit, "fixture ownership failure"):
                preset.install_assets(
                    self.workflow_src,
                    self.install_dst,
                    self.repo,
                    {"codex", "cursor"},
                )
        after = {
            path.relative_to(self.repo).as_posix(): path.read_bytes()
            for path in self.repo.rglob("*")
            if path.is_file()
        }
        self.assertEqual(after, before)
        self.assertFalse(self.install_dst.exists())

    def install(self, platforms: set[str] | None = None, all_platforms: bool = False) -> dict[str, object]:
        return preset.install_assets(self.workflow_src, self.install_dst, self.repo, platforms, all_platforms=all_platforms)

    def test_skill_manifest_file_order_is_stable_across_hash_seeds_and_reapply(self) -> None:
        module_path = Path(preset.__file__).resolve()
        guru_root = preset.guru_root_from_script()
        script = """
import importlib.util
import json
import sys
from pathlib import Path

module_path = Path(sys.argv[1])
repo = Path(sys.argv[2])
guru_root = Path(sys.argv[3])
spec = importlib.util.spec_from_file_location("guru_preset_seeded", module_path)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)
repo.mkdir(parents=True, exist_ok=True)
dst = repo / ".trellis/guru-team"
manifest_path = repo / "previous-extension.json"
previous = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else None
result = module.install_skill_packages(
    repo,
    guru_root,
    dst,
    {"claude", "codex", "cursor"},
    previous,
)
manifest_path.write_text(
    json.dumps({"skill_packages": result}, ensure_ascii=False, indent=2) + "\\n",
    encoding="utf-8",
)
sys.stdout.write(json.dumps(result["files"], ensure_ascii=False, separators=(",", ":")))
"""

        outputs: list[tuple[bytes, bytes]] = []
        for first_seed, second_seed in (("1", "2"), ("777", "999")):
            repo = self.repo / f"seed-{first_seed}"
            seeded: list[bytes] = []
            for seed in (first_seed, second_seed):
                process = subprocess.run(
                    [sys.executable, "-c", script, str(module_path), str(repo), str(guru_root)],
                    check=True,
                    capture_output=True,
                    env={**os.environ, "PYTHONHASHSEED": seed},
                )
                seeded.append(process.stdout)
            outputs.append((seeded[0], seeded[1]))

        self.assertEqual(outputs[0][0], outputs[1][0])
        self.assertEqual(outputs[0][1], outputs[1][1])
        fresh_paths = [record["path"] for record in json.loads(outputs[0][0])]
        reapplied_paths = [record["path"] for record in json.loads(outputs[0][1])]
        self.assertEqual(fresh_paths, reapplied_paths)
        group_order: list[str] = []
        for path in fresh_paths:
            group = next(
                label
                for prefix, label in (
                    (".trellis/guru-team/skills/", "installed"),
                    (".agents/skills/", "shared"),
                    (".codex/skills/", "codex"),
                    (".claude/skills/", "claude"),
                    (".cursor/skills/", "cursor"),
                )
                if path.startswith(prefix)
            )
            if not group_order or group_order[-1] != group:
                group_order.append(group)
        self.assertEqual(
            group_order,
            [
                "installed",
                "shared",
                "codex",
                "claude",
                "cursor",
                "shared",
                "codex",
                "claude",
                "cursor",
                "shared",
                "codex",
                "claude",
                "cursor",
                "shared",
                "codex",
                "claude",
                "cursor",
                "shared",
                "codex",
                "claude",
                "cursor",
                "shared",
                "codex",
                "claude",
                "cursor",
                "shared",
                "codex",
                "claude",
                "cursor",
                "shared",
                "codex",
                "claude",
                "cursor",
            ],
        )

    def test_default_platforms_install_codex_cursor_and_shared_overlays(self) -> None:
        payload = self.install()

        self.assertEqual(payload["platforms"], ["codex", "cursor"])
        self.assertFalse(payload["all_platforms"])
        self.assertIn(Path("scripts/bash/check-workspace-boundary.sh"), preset.MANAGED_ASSET_PATHS)
        self.assertIn(Path("scripts/bash/run-skill-command.sh"), preset.MANAGED_ASSET_PATHS)
        self.assertIn(Path("scripts/bash/sync-base.sh"), preset.MANAGED_ASSET_PATHS)
        self.assertIn(Path("scripts/bash/check-base-sync.sh"), preset.MANAGED_ASSET_PATHS)
        self.assertIn(Path("scripts/bash/preview-change-context-history.sh"), preset.MANAGED_ASSET_PATHS)
        self.assertIn(Path("scripts/bash/record-context-discovery.sh"), preset.MANAGED_ASSET_PATHS)
        self.assertIn(Path("scripts/bash/check-context-discovery.sh"), preset.MANAGED_ASSET_PATHS)
        self.assertIn(Path("scripts/bash/record-requirements-clarification.sh"), preset.MANAGED_ASSET_PATHS)
        self.assertIn(Path("scripts/bash/check-requirements-clarification.sh"), preset.MANAGED_ASSET_PATHS)
        self.assertIn(Path("scripts/bash/record-contract-wording-review.sh"), preset.MANAGED_ASSET_PATHS)
        self.assertIn(Path("scripts/bash/check-contract-wording-review.sh"), preset.MANAGED_ASSET_PATHS)
        self.assertIn(Path("scripts/bash/record-change-request-review.sh"), preset.MANAGED_ASSET_PATHS)
        self.assertIn(Path("scripts/bash/check-change-request-review.sh"), preset.MANAGED_ASSET_PATHS)
        self.assertIn(Path("scripts/bash/resolve-human-artifacts.sh"), preset.MANAGED_ASSET_PATHS)
        self.assertIn(Path("scripts/bash/record-subagent-liveness-event.sh"), preset.MANAGED_ASSET_PATHS)
        self.assertIn(Path("scripts/bash/check-subagent-liveness.sh"), preset.MANAGED_ASSET_PATHS)
        self.assertIn(Path("scripts/bash/check-commit-messages.sh"), preset.MANAGED_ASSET_PATHS)
        self.assertIn(Path("scripts/bash/format-merge-commit.sh"), preset.MANAGED_ASSET_PATHS)
        self.assertIn(Path("scripts/bash/backfill-finish-summary.sh"), preset.MANAGED_ASSET_PATHS)
        self.assertIn(Path("schemas/finish-summary.schema.json"), preset.MANAGED_ASSET_PATHS)
        self.assertTrue((self.repo / ".trellis/guru-team/scripts/bash/check-workspace-boundary.sh").is_file())
        self.assertTrue((self.repo / ".trellis/guru-team/scripts/bash/run-skill-command.sh").is_file())
        self.assertTrue(os.access(self.repo / ".trellis/guru-team/scripts/bash/run-skill-command.sh", os.X_OK))
        self.assertTrue(os.access(self.repo / ".trellis/guru-team/scripts/bash/sync-base.sh", os.X_OK))
        self.assertTrue(os.access(self.repo / ".trellis/guru-team/scripts/bash/check-base-sync.sh", os.X_OK))
        self.assertTrue(os.access(self.repo / ".trellis/guru-team/scripts/bash/preview-change-context-history.sh", os.X_OK))
        self.assertTrue(os.access(self.repo / ".trellis/guru-team/scripts/bash/record-context-discovery.sh", os.X_OK))
        self.assertTrue(os.access(self.repo / ".trellis/guru-team/scripts/bash/check-context-discovery.sh", os.X_OK))
        self.assertTrue((self.repo / ".trellis/guru-team/scripts/bash/resolve-human-artifacts.sh").is_file())
        self.assertTrue(os.access(self.repo / ".trellis/guru-team/scripts/bash/resolve-human-artifacts.sh", os.X_OK))
        self.assertTrue((self.repo / ".trellis/guru-team/scripts/bash/record-subagent-liveness-event.sh").is_file())
        self.assertTrue(os.access(self.repo / ".trellis/guru-team/scripts/bash/record-subagent-liveness-event.sh", os.X_OK))
        self.assertTrue((self.repo / ".trellis/guru-team/scripts/bash/check-subagent-liveness.sh").is_file())
        self.assertTrue(os.access(self.repo / ".trellis/guru-team/scripts/bash/check-subagent-liveness.sh", os.X_OK))
        self.assertTrue((self.repo / ".trellis/guru-team/scripts/bash/check-commit-messages.sh").is_file())
        self.assertTrue(os.access(self.repo / ".trellis/guru-team/scripts/bash/check-commit-messages.sh", os.X_OK))
        self.assertTrue((self.repo / ".trellis/guru-team/scripts/bash/format-merge-commit.sh").is_file())
        self.assertTrue(os.access(self.repo / ".trellis/guru-team/scripts/bash/format-merge-commit.sh", os.X_OK))
        self.assertTrue((self.repo / ".trellis/guru-team/scripts/bash/backfill-finish-summary.sh").is_file())
        self.assertTrue(os.access(self.repo / ".trellis/guru-team/scripts/bash/backfill-finish-summary.sh", os.X_OK))
        self.assertTrue((self.repo / ".trellis/guru-team/schemas/finish-summary.schema.json").is_file())
        self.assertIn("session_auto_commit: false", (self.repo / ".trellis/config.yaml").read_text(encoding="utf-8"))
        self.assertIn(".trellis/workspace/", (self.repo / ".gitignore").read_text(encoding="utf-8"))
        self.assertTrue((self.repo / ".agents/skills/trellis-start/SKILL.md").is_file())
        self.assertTrue((self.repo / ".agents/skills/trellis-brainstorm/SKILL.md").is_file())
        brainstorm = (self.repo / ".agents/skills/trellis-brainstorm/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("explicit post-planning confirmation", brainstorm)
        self.assertNotIn("Lightweight tasks may have only", brainstorm)
        self.assertTrue((self.repo / ".agents/skills/trellis-before-dev/SKILL.md").is_file())
        before_dev = (self.repo / ".agents/skills/trellis-before-dev/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("required `design.md`", before_dev)
        self.assertNotIn("design.md` if present", before_dev)
        self.assertTrue((self.repo / ".agents/skills/trellis-check/SKILL.md").is_file())
        check_skill = (self.repo / ".agents/skills/trellis-check/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("required `design.md`", check_skill)
        self.assertNotIn("design.md` if present", check_skill)
        self.assertTrue((self.repo / ".trellis/agents/implement.md").is_file())
        self.assertIn("实现代理", (self.repo / ".trellis/agents/implement.md").read_text(encoding="utf-8"))
        self.assertTrue((self.repo / ".codex/prompts/trellis-start.md").is_file())
        self.assertTrue((self.repo / ".codex/agents/trellis-implement.toml").is_file())
        self.assertTrue((self.repo / ".codex/hooks/session-start.py").is_file())
        codex_implement = (self.repo / ".codex/agents/trellis-implement.toml").read_text(encoding="utf-8")
        self.assertIn("实现代理", codex_implement)
        self.assertIn('nickname_candidates = ["Implement Agent"', codex_implement)
        self.assertNotIn('nickname_candidates = ["实现代理"', codex_implement)
        codex_hook = (self.repo / ".codex/hooks/session-start.py").read_text(encoding="utf-8")
        self.assertIn("post-planning confirmation", codex_hook)
        self.assertNotIn("PRD-only", codex_hook)
        self.assertNotIn("Missing optional artifacts", codex_hook)
        self.assertNotIn("design.md if present", codex_hook)
        codex_meta = (
            self.repo / ".agents/skills/trellis-meta/references/local-architecture/task-system.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Guru Team requires this document before implementation", codex_meta)
        self.assertNotIn("Lightweight tasks may be PRD-only", codex_meta)
        codex_context = (
            self.repo / ".agents/skills/trellis-meta/references/local-architecture/context-injection.md"
        ).read_text(encoding="utf-8")
        self.assertIn("required `design.md`", codex_context)
        self.assertNotIn("design.md if present", codex_context)
        codex_change_workflow = (
            self.repo / ".agents/skills/trellis-meta/references/customize-local/change-workflow.md"
        ).read_text(encoding="utf-8")
        self.assertIn("explicit post-planning confirmation", codex_change_workflow)
        self.assertNotIn("lightweight task with `prd.md` complete", codex_change_workflow)
        codex_change_context = (
            self.repo / ".agents/skills/trellis-meta/references/customize-local/change-context-loading.md"
        ).read_text(encoding="utf-8")
        self.assertIn("required `design.md`", codex_change_context)
        self.assertNotIn("design.md` if present", codex_change_context)
        codex_agents_doc = (
            self.repo / ".agents/skills/trellis-meta/references/platform-files/agents.md"
        ).read_text(encoding="utf-8")
        self.assertIn("required `prd.md`, `design.md`, `implement.md`", codex_agents_doc)
        self.assertNotIn("optional `design.md` / `implement.md`", codex_agents_doc)
        self.assertTrue((self.repo / ".cursor/commands/trellis-continue.md").is_file())
        self.assertTrue((self.repo / ".cursor/agents/trellis-check.md").is_file())
        cursor_check_agent = (self.repo / ".cursor/agents/trellis-check.md").read_text(encoding="utf-8")
        self.assertIn("阶段二检查代理", cursor_check_agent)
        assert_required_planning_context(self, cursor_check_agent)
        self.assertTrue((self.repo / ".cursor/skills/trellis-brainstorm/SKILL.md").is_file())
        cursor_brainstorm = (self.repo / ".cursor/skills/trellis-brainstorm/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("explicit post-planning confirmation", cursor_brainstorm)
        self.assertNotIn("Lightweight tasks may have only", cursor_brainstorm)
        self.assertTrue((self.repo / ".cursor/skills/trellis-before-dev/SKILL.md").is_file())
        cursor_before_dev = (self.repo / ".cursor/skills/trellis-before-dev/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("required `design.md`", cursor_before_dev)
        self.assertNotIn("design.md` if present", cursor_before_dev)
        self.assertTrue((self.repo / ".cursor/skills/trellis-check/SKILL.md").is_file())
        cursor_check_skill = (self.repo / ".cursor/skills/trellis-check/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("required `design.md`", cursor_check_skill)
        self.assertNotIn("design.md` if present", cursor_check_skill)
        self.assertTrue((self.repo / ".cursor/hooks/session-start.py").is_file())
        cursor_hook = (self.repo / ".cursor/hooks/session-start.py").read_text(encoding="utf-8")
        self.assertIn("post-planning confirmation", cursor_hook)
        self.assertNotIn("PRD-only", cursor_hook)
        self.assertNotIn("Missing optional artifacts", cursor_hook)
        self.assertNotIn("design.md if present", cursor_hook)
        self.assertTrue((self.repo / ".cursor/hooks/inject-subagent-context.py").is_file())
        cursor_context_hook = (self.repo / ".cursor/hooks/inject-subagent-context.py").read_text(encoding="utf-8")
        self.assertIn("required design.md", cursor_context_hook)
        self.assertNotIn("design.md if present", cursor_context_hook)
        cursor_meta = (
            self.repo / ".cursor/skills/trellis-meta/references/local-architecture/task-system.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Guru Team requires this document before implementation", cursor_meta)
        self.assertNotIn("Lightweight tasks may be PRD-only", cursor_meta)
        cursor_context = (
            self.repo / ".cursor/skills/trellis-meta/references/local-architecture/context-injection.md"
        ).read_text(encoding="utf-8")
        self.assertIn("required `design.md`", cursor_context)
        self.assertNotIn("design.md if present", cursor_context)
        cursor_change_workflow = (
            self.repo / ".cursor/skills/trellis-meta/references/customize-local/change-workflow.md"
        ).read_text(encoding="utf-8")
        self.assertIn("explicit post-planning confirmation", cursor_change_workflow)
        self.assertNotIn("lightweight task with `prd.md` complete", cursor_change_workflow)
        cursor_change_context = (
            self.repo / ".cursor/skills/trellis-meta/references/customize-local/change-context-loading.md"
        ).read_text(encoding="utf-8")
        self.assertIn("required `design.md`", cursor_change_context)
        self.assertNotIn("design.md` if present", cursor_change_context)
        cursor_agents_doc = (
            self.repo / ".cursor/skills/trellis-meta/references/platform-files/agents.md"
        ).read_text(encoding="utf-8")
        self.assertIn("required `prd.md`, `design.md`, `implement.md`", cursor_agents_doc)
        self.assertNotIn("optional `design.md` / `implement.md`", cursor_agents_doc)
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
        self.assertTrue((self.repo / ".agents/skills/trellis-brainstorm/SKILL.md").is_file())
        self.assertTrue((self.repo / ".agents/skills/trellis-before-dev/SKILL.md").is_file())
        self.assertTrue((self.repo / ".agents/skills/trellis-check/SKILL.md").is_file())
        self.assertTrue((self.repo / ".trellis/agents/check.md").is_file())
        self.assertTrue((self.repo / ".claude/commands/trellis/continue.md").is_file())
        self.assertTrue((self.repo / ".claude/agents/trellis-implement.md").is_file())
        self.assertTrue((self.repo / ".claude/agents/trellis-check.md").is_file())
        claude_check_agent = (self.repo / ".claude/agents/trellis-check.md").read_text(encoding="utf-8")
        self.assertIn("阶段二检查代理", claude_check_agent)
        assert_required_planning_context(self, claude_check_agent)
        self.assertFalse((self.repo / ".agents/skills/trellis-meta").exists())
        self.assertFalse((self.repo / ".codex").exists())
        self.assertFalse((self.repo / ".cursor").exists())

    def test_all_platforms_installs_historical_full_overlay_set(self) -> None:
        platforms, all_platforms = preset.selected_platforms(None, True)
        payload = self.install(platforms, all_platforms=all_platforms)

        self.assertTrue(all_platforms)
        self.assertEqual(payload["platforms"], ["claude", "codex", "cursor"])
        self.assertTrue((self.repo / ".agents/skills/trellis-start/SKILL.md").is_file())
        self.assertTrue((self.repo / ".agents/skills/trellis-brainstorm/SKILL.md").is_file())
        self.assertTrue((self.repo / ".agents/skills/trellis-before-dev/SKILL.md").is_file())
        self.assertTrue((self.repo / ".agents/skills/trellis-check/SKILL.md").is_file())
        self.assertTrue((self.repo / ".trellis/agents/implement.md").is_file())
        self.assertTrue((self.repo / ".codex/prompts/trellis-start.md").is_file())
        self.assertTrue((self.repo / ".codex/agents/trellis-check.toml").is_file())
        self.assertTrue((self.repo / ".codex/hooks/session-start.py").is_file())
        self.assertTrue((self.repo / ".agents/skills/trellis-meta/references/customize-local/change-workflow.md").is_file())
        self.assertTrue((self.repo / ".agents/skills/trellis-meta/references/customize-local/change-context-loading.md").is_file())
        self.assertTrue((self.repo / ".agents/skills/trellis-meta/references/local-architecture/context-injection.md").is_file())
        self.assertTrue((self.repo / ".agents/skills/trellis-meta/references/platform-files/agents.md").is_file())
        self.assertTrue((self.repo / ".agents/skills/trellis-meta/references/local-architecture/task-system.md").is_file())
        self.assertTrue((self.repo / ".cursor/commands/trellis-continue.md").is_file())
        self.assertTrue((self.repo / ".cursor/agents/trellis-research.md").is_file())
        self.assertTrue((self.repo / ".cursor/agents/trellis-check.md").is_file())
        assert_required_planning_context(
            self,
            (self.repo / ".cursor/agents/trellis-check.md").read_text(encoding="utf-8"),
        )
        self.assertTrue((self.repo / ".cursor/hooks/session-start.py").is_file())
        self.assertTrue((self.repo / ".cursor/hooks/inject-subagent-context.py").is_file())
        self.assertTrue((self.repo / ".cursor/skills/trellis-brainstorm/SKILL.md").is_file())
        self.assertTrue((self.repo / ".cursor/skills/trellis-before-dev/SKILL.md").is_file())
        self.assertTrue((self.repo / ".cursor/skills/trellis-check/SKILL.md").is_file())
        self.assertTrue((self.repo / ".cursor/skills/trellis-meta/references/customize-local/change-workflow.md").is_file())
        self.assertTrue((self.repo / ".cursor/skills/trellis-meta/references/customize-local/change-context-loading.md").is_file())
        self.assertTrue((self.repo / ".cursor/skills/trellis-meta/references/local-architecture/context-injection.md").is_file())
        self.assertTrue((self.repo / ".cursor/skills/trellis-meta/references/platform-files/agents.md").is_file())
        self.assertTrue((self.repo / ".cursor/skills/trellis-meta/references/local-architecture/task-system.md").is_file())
        self.assertTrue((self.repo / ".claude/commands/trellis/continue.md").is_file())
        self.assertTrue((self.repo / ".claude/agents/trellis-research.md").is_file())
        self.assertTrue((self.repo / ".claude/agents/trellis-check.md").is_file())
        assert_required_planning_context(
            self,
            (self.repo / ".claude/agents/trellis-check.md").read_text(encoding="utf-8"),
        )
        installed_manifest = json.loads(
            (self.repo / ".trellis/guru-team/extension.json").read_text(encoding="utf-8")
        )
        managed_assets = installed_manifest["install"]["managed_assets"]
        self.assertEqual(installed_manifest["install"]["selected_platforms"], ["claude", "codex", "cursor"])
        self.assertTrue(installed_manifest["install"]["all_platforms"])
        self.assertEqual(len(managed_assets), 88)
        self.assertEqual(managed_assets, sorted(set(managed_assets)))
        self.assertEqual(
            [path for path in managed_assets if not (self.repo / path).is_file()],
            [],
        )

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
        self.assertTrue((self.repo / ".codex/hooks/session-start.py").is_file())
        self.assertTrue((self.repo / ".cursor/commands/trellis-continue.md").is_file())
        self.assertTrue((self.repo / ".cursor/agents/trellis-implement.md").is_file())
        self.assertTrue((self.repo / ".cursor/hooks/session-start.py").is_file())
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

    def test_generated_markdown_check_agents_replace_optional_context_hints(self) -> None:
        stale_agent = (
            "---\n"
            "name: trellis-check\n"
            "---\n"
            "# Trellis workflow check agent\n\n"
            "Read check.jsonl, then task artifacts.\n\n"
            "## Context\n"
            "- Task `prd.md` - Requirements document\n"
            "- Task `design.md` - Technical design (if exists)\n"
            "- Task `implement.md` - Execution plan (if exists)\n\n"
            "- Does it follow the technical design and implementation plan when present\n"
        )
        claude_check = self.repo / ".claude/agents/trellis-check.md"
        cursor_check = self.repo / ".cursor/agents/trellis-check.md"
        claude_check.parent.mkdir(parents=True)
        cursor_check.parent.mkdir(parents=True)
        claude_check.write_text(stale_agent, encoding="utf-8")
        cursor_check.write_text(stale_agent, encoding="utf-8")

        payload = self.install({"claude", "cursor"})

        self.assertIn(".claude/agents/trellis-check.md", payload["replaced_overlays"])
        self.assertIn(".cursor/agents/trellis-check.md", payload["replaced_overlays"])
        assert_required_planning_context(self, claude_check.read_text(encoding="utf-8"))
        assert_required_planning_context(self, cursor_check.read_text(encoding="utf-8"))

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

    def test_generated_session_start_hooks_are_replaced_with_planning_gate_overlays(self) -> None:
        codex_hook = self.repo / ".codex/hooks/session-start.py"
        cursor_hook = self.repo / ".cursor/hooks/session-start.py"
        codex_hook.parent.mkdir(parents=True)
        cursor_hook.parent.mkdir(parents=True)
        stale_hook = (
            "#!/usr/bin/env python3\n"
            "\"\"\"Trellis Session Start Hook\"\"\"\n"
            "def _get_task_status(trellis_dir, hook_input):\n"
            "    return 'Lightweight task can ask for start review with PRD-only'\n"
        )
        codex_hook.write_text(stale_hook, encoding="utf-8")
        cursor_hook.write_text(stale_hook, encoding="utf-8")

        payload = self.install({"codex", "cursor"})

        self.assertIn(".codex/hooks/session-start.py", payload["replaced_overlays"])
        self.assertIn(".cursor/hooks/session-start.py", payload["replaced_overlays"])
        self.assertIn("post-planning confirmation", codex_hook.read_text(encoding="utf-8"))
        self.assertIn("post-planning confirmation", cursor_hook.read_text(encoding="utf-8"))
        self.assertNotIn("PRD-only", codex_hook.read_text(encoding="utf-8"))
        self.assertNotIn("PRD-only", cursor_hook.read_text(encoding="utf-8"))

    def test_no_workspace_session_start_overlays_never_access_or_disclose_journal_sentinel(self) -> None:
        workspace_dir = self.repo / ".trellis/workspace/private"
        workspace_dir.mkdir(parents=True)
        sentinel = workspace_dir / "secret-journal-name.md"
        sentinel.write_text("SECRET_JOURNAL_CONTENT\nsecond line\n", encoding="utf-8")

        self.install({"codex", "cursor"})
        for name, relative in [
            ("codex", ".codex/hooks/session-start.py"),
            ("cursor", ".cursor/hooks/session-start.py"),
        ]:
            with self.subTest(platform=name):
                hook_path = self.repo / relative
                source = hook_path.read_text(encoding="utf-8")
                self.assertNotIn("get_active_journal_file", source)
                self.assertNotIn("count_lines", source)
                self.assertNotIn("Journal:", source)

                spec = importlib.util.spec_from_file_location(f"guru_{name}_session_start", hook_path)
                self.assertIsNotNone(spec)
                self.assertIsNotNone(spec.loader)
                module = importlib.util.module_from_spec(spec)
                with mock.patch.object(sys, "dont_write_bytecode", True):
                    spec.loader.exec_module(module)

                original_read_text = Path.read_text
                original_iterdir = Path.iterdir

                def guarded_read_text(path: Path, *args: object, **kwargs: object) -> str:
                    if ".trellis/workspace" in path.as_posix():
                        raise AssertionError(f"workspace read attempted: {path}")
                    return original_read_text(path, *args, **kwargs)

                def guarded_iterdir(path: Path):
                    if ".trellis/workspace" in path.as_posix():
                        raise AssertionError(f"workspace enumeration attempted: {path}")
                    return original_iterdir(path)

                with (
                    mock.patch.object(module, "_resolve_active_task", return_value=types.SimpleNamespace(task_path=None)),
                    mock.patch.object(Path, "read_text", guarded_read_text),
                    mock.patch.object(Path, "iterdir", guarded_iterdir),
                ):
                    output = module._build_compact_current_state(self.repo / ".trellis", {}, [])

                self.assertNotIn("secret-journal-name.md", output)
                self.assertNotIn("SECRET_JOURNAL_CONTENT", output)
                self.assertNotIn("2 / 2000", output)

    def test_shared_start_uses_fixed_no_workspace_context_commands(self) -> None:
        workspace_dir = self.repo / ".trellis/workspace/private"
        workspace_dir.mkdir(parents=True)
        (workspace_dir / "shared-start-secret.md").write_text(
            "SHARED_START_SECRET_CONTENT\n",
            encoding="utf-8",
        )
        self.install({"codex"})
        skill = (
            self.repo / ".agents/skills/trellis-start/SKILL.md"
        ).read_text(encoding="utf-8")

        command_block = re.search(
            r"load the fixed Guru Team no-workspace context set:\n\n```bash\n(.*?)\n```",
            skill,
            re.DOTALL,
        )
        self.assertIsNotNone(command_block)
        self.assertLess(
            skill.index("mandatory invoke `guru-sync-base`"),
            command_block.start(),
        )
        commands = [line.strip() for line in command_block.group(1).splitlines() if line.strip()]
        self.assertEqual(commands, [
            "python3 ./.trellis/scripts/get_context.py --mode phase",
            "python3 ./.trellis/scripts/get_context.py --mode packages",
            "python3 ./.trellis/scripts/task.py current --source",
            "git branch --show-current",
            "git status --short --branch",
        ])
        self.assertNotRegex(skill, r"(?m)^python3 \.\/\.trellis/scripts/get_context\.py$")
        self.assertIn("Do not open, enumerate, read", skill)
        self.assertNotIn("shared-start-secret.md", skill)
        self.assertNotIn("SHARED_START_SECRET_CONTENT", skill)

    def test_throwaway_verifier_cleans_preview_and_scans_sidecars_after_reapply(self) -> None:
        verifier = (
            self.guru_root
            / "trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh"
        ).read_text(encoding="utf-8")

        preview_assert = verifier.index('test -f "$TARGET/.trellis/workflow.md.new"')
        preview_remove = verifier.index('rm -f "$TARGET/.trellis/workflow.md.new"', preview_assert)
        initial_switch = verifier.index(
            'trellis workflow --marketplace "$WORKFLOW_SOURCE" --template guru-team --force',
            preview_remove,
        )
        update = verifier.index("trellis update --force", initial_switch)
        workflow_reapply = verifier.index(
            'trellis workflow --marketplace "$WORKFLOW_SOURCE" --template guru-team --force',
            update,
        )
        preset_reapply = verifier.index(
            '"$REPO_ROOT/trellis/presets/guru-team/scripts/bash/apply.sh"',
            workflow_reapply,
        )
        final_scan = verifier.index('FINAL_SIDECARS="$(find "$TARGET"', preset_reapply)
        initial_ownership = verifier.index('ownership_checkpoint "initial-init-before-preset-apply"')
        initial_apply = verifier.index(
            '"$REPO_ROOT/trellis/presets/guru-team/scripts/bash/apply.sh"',
            initial_ownership,
        )
        post_update_ownership = verifier.index(
            'ownership_checkpoint "post-update-before-workflow-and-preset-reapply"',
            update,
        )
        post_reapply_ownership = verifier.index(
            'ownership_checkpoint "post-preset-reapply-before-final-checks"',
            preset_reapply,
        )

        self.assertLess(preview_assert, preview_remove)
        self.assertLess(preview_remove, initial_switch)
        self.assertLess(initial_switch, update)
        self.assertLess(update, workflow_reapply)
        self.assertLess(workflow_reapply, preset_reapply)
        self.assertLess(preset_reapply, final_scan)
        self.assertLess(initial_ownership, initial_apply)
        self.assertLess(update, post_update_ownership)
        self.assertLess(post_update_ownership, workflow_reapply)
        self.assertLess(preset_reapply, post_reapply_ownership)
        self.assertLess(post_reapply_ownership, final_scan)
        self.assertEqual(verifier.count('ownership_checkpoint "'), 3)
        self.assertIn('WORKSPACE_SENTINEL="$TARGET/.trellis/workspace/private/shared-start-secret-journal.md"', verifier)
        self.assertIn('event not in {"open", "os.listdir", "os.scandir"}', verifier)
        self.assertIn("os._exit(91)", verifier)
        self.assertIn('"$CURRENT_TASK_STATUS" -ne 0 && "$CURRENT_TASK_STATUS" -ne 1', verifier)
        self.assertIn("get_context.py --mode phase", verifier)
        self.assertIn("get_context.py --mode packages", verifier)
        self.assertIn("task.py current --source", verifier)
        self.assertIn("Unexpected .new/.bak sidecars after preview, switch, update, and preset reapply", verifier)
        self.assertIn('"id":"guru-requirements-clear-router"', verifier)
        self.assertNotIn(
            '"exit":"clear","consumer":{"kind":"workflow","id":"guru-review-contract-wording"}',
            verifier,
        )
        self.assertIn('"resume_target": "guru-review-contract-wording"', verifier)
        self.assertIn('verify_contract_wording_standalone_profiles "initial"', verifier)
        self.assertIn('verify_contract_wording_standalone_profiles "after-update"', verifier)
        self.assertIn('verify_change_request_review_package "initial"', verifier)
        self.assertIn('verify_change_request_review_package "after-update"', verifier)
        self.assertIn('"planned_skill_ids"] == []', verifier)
        self.assertIn('test -f "$TARGET/.trellis/guru-team/skills/packages/guru-create-task-workspace/SKILL.md"', verifier)
        self.assertIn('test -x "$TARGET/.agents/skills/guru-create-task-workspace/scripts/record-task-workspace-plan.sh"', verifier)
        self.assertIn('test -x "$TARGET/.codex/skills/guru-create-task-workspace/scripts/create-task-workspace.sh"', verifier)
        self.assertIn('test -x "$TARGET/.cursor/skills/guru-create-task-workspace/scripts/check-task-workspace-result.sh"', verifier)
        self.assertIn('fail_if_python_cache "throwaway target" "$TARGET"', verifier)
        self.assertIn('record_planning_contract_wording "$TASK_REL"', verifier)
        self.assertIn('record_and_check_planning_approval "$TASK_REL" "initial"', verifier)
        self.assertIn(
            'record_and_check_planning_approval "$POST_UPDATE_TASK_REL" "after-update"',
            verifier,
        )
        self.assertIn('--task "$task_rel" --input "$input" >"$result"', verifier)
        self.assertIn('payload["schema_version"] == "2.0"', verifier)
        self.assertNotIn("--ambiguity-reviewer", verifier)
        self.assertNotIn("--normative-hit", verifier)
        self.assertIn("verify_installed_closeout.py", verifier)
        self.assertIn("--case initial", verifier)
        self.assertIn("--case after-update", verifier)
        self.assertIn('payload["after_archive_hook_preflight"] is True', verifier)
        self.assertIn("verify_installed_task_workspace.py", verifier)
        self.assertIn("installed-task-workspace-initial", verifier)
        self.assertIn("installed-task-workspace-after-update", verifier)
        self.assertIn("--existing-developer-identity", verifier)
        self.assertIn('payload["developer_identity_preserved"] is True', verifier)
        self.assertIn('payload["task_creator"] == "fixture-maintainer"', verifier)
        self.assertIn('trellis init -y --claude --codex --cursor', verifier)
        self.assertIn(
            'skills["selected_platforms"] == ["claude", "codex", "cursor"]',
            verifier,
        )
        self.assertIn("assert len(assets) == 88", verifier)
        self.assertNotIn('trellis init -y -u', verifier)
        self.assertIn('DEVELOPER_IDENTITY_DIGEST_BEFORE="$(file_sha256', verifier)
        self.assertIn('assert_official_state_absent "$ABSENCE_TARGET" "initial preset apply"', verifier)
        self.assertIn('assert_official_state_absent "$ABSENCE_TARGET" "trellis update"', verifier)
        self.assertIn('assert_official_state_absent "$ABSENCE_TARGET" "workflow reapply"', verifier)
        self.assertIn('assert_official_state_absent "$ABSENCE_TARGET" "preset reapply"', verifier)
        installed_workspace = (
            self.guru_root
            / "trellis/presets/guru-team/scripts/python/verify_installed_task_workspace.py"
        ).read_text(encoding="utf-8")
        self.assertIn("runtime.cmd_create_task_workspace", installed_workspace)
        self.assertIn("runtime.cmd_check_task_workspace_result", installed_workspace)
        self.assertIn("TASK_WORKSPACE_ARTIFACT_NAMES", installed_workspace)
        self.assertIn("--existing-developer-identity", installed_workspace)
        self.assertIn('task_data.get("creator") != "fixture-maintainer"', installed_workspace)
        installed_closeout = (
            self.guru_root
            / "trellis/presets/guru-team/scripts/python/verify_installed_closeout.py"
        ).read_text(encoding="utf-8")
        self.assertIn('.trellis/guru-team/scripts/bash/finish-work.sh', installed_closeout)
        self.assertIn('.trellis/guru-team/scripts/python/guru_team_trellis.py', installed_closeout)
        self.assertIn('args[:2] == ["remote", "get-url"]', installed_closeout)
        self.assertIn('args[:2] == ["pr", "ready"]', installed_closeout)
        self.assertIn('after_archive:', installed_closeout)
        self.assertIn('after-archive-hook-preflight', installed_closeout)
        self.assertIn('hook_executed', installed_closeout)
        self.assertIn('installed-after-archive-hook-', installed_closeout)
        self.assertNotIn("copytree", installed_closeout)

    def test_dogfood_drift_checks_ownership_before_payload_bytes(self) -> None:
        checker = (
            self.guru_root
            / "trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh"
        ).read_text(encoding="utf-8")

        ownership_gate = checker.index('"$OWNERSHIP_CHECK" --repo "$REPO_ROOT" --json')
        payload_loop = checker.index('while IFS= read -r source; do')
        self.assertLess(ownership_gate, payload_loop)
        self.assertIn("Missing executable ownership validator", checker)

    def test_generated_trellis_meta_task_system_docs_are_replaced_with_guru_team_overlay(self) -> None:
        shared_meta = self.repo / ".agents/skills/trellis-meta/references/local-architecture/task-system.md"
        cursor_meta = self.repo / ".cursor/skills/trellis-meta/references/local-architecture/task-system.md"
        stale_meta = (
            "# Local Task System\n\n"
            "The Trellis task system is stored under `.trellis/tasks/`.\n\n"
            "| `prd.md` | Requirements. Lightweight tasks may be PRD-only. |\n"
        )
        shared_meta.parent.mkdir(parents=True)
        cursor_meta.parent.mkdir(parents=True)
        shared_meta.write_text(stale_meta, encoding="utf-8")
        cursor_meta.write_text(stale_meta, encoding="utf-8")

        payload = self.install({"codex", "cursor"})

        self.assertIn(
            ".agents/skills/trellis-meta/references/local-architecture/task-system.md",
            payload["replaced_overlays"],
        )
        self.assertIn(
            ".cursor/skills/trellis-meta/references/local-architecture/task-system.md",
            payload["replaced_overlays"],
        )
        self.assertIn("Guru Team requires this document before implementation", shared_meta.read_text(encoding="utf-8"))
        self.assertIn("Guru Team requires this document before implementation", cursor_meta.read_text(encoding="utf-8"))
        self.assertNotIn("Lightweight tasks may be PRD-only", shared_meta.read_text(encoding="utf-8"))
        self.assertNotIn("Lightweight tasks may be PRD-only", cursor_meta.read_text(encoding="utf-8"))

    def test_generated_brainstorm_and_trellis_meta_reference_docs_are_replaced(self) -> None:
        shared_brainstorm = self.repo / ".agents/skills/trellis-brainstorm/SKILL.md"
        cursor_brainstorm = self.repo / ".cursor/skills/trellis-brainstorm/SKILL.md"
        shared_before_dev = self.repo / ".agents/skills/trellis-before-dev/SKILL.md"
        cursor_before_dev = self.repo / ".cursor/skills/trellis-before-dev/SKILL.md"
        shared_check_skill = self.repo / ".agents/skills/trellis-check/SKILL.md"
        cursor_check_skill = self.repo / ".cursor/skills/trellis-check/SKILL.md"
        shared_change_workflow = self.repo / ".agents/skills/trellis-meta/references/customize-local/change-workflow.md"
        cursor_change_workflow = self.repo / ".cursor/skills/trellis-meta/references/customize-local/change-workflow.md"
        shared_change_context = self.repo / ".agents/skills/trellis-meta/references/customize-local/change-context-loading.md"
        cursor_change_context = self.repo / ".cursor/skills/trellis-meta/references/customize-local/change-context-loading.md"
        shared_context = self.repo / ".agents/skills/trellis-meta/references/local-architecture/context-injection.md"
        cursor_context = self.repo / ".cursor/skills/trellis-meta/references/local-architecture/context-injection.md"
        shared_agents_doc = self.repo / ".agents/skills/trellis-meta/references/platform-files/agents.md"
        cursor_agents_doc = self.repo / ".cursor/skills/trellis-meta/references/platform-files/agents.md"
        cursor_context_hook = self.repo / ".cursor/hooks/inject-subagent-context.py"
        stale_brainstorm = (
            "# Trellis Brainstorm\n\n"
            "## PRD Convergence Pass\n\n"
            "Lightweight tasks may have only `prd.md`.\n"
        )
        stale_before_dev = (
            "# Read the relevant development guidelines\n\n"
            "Trellis before-dev reads task artifacts.\n"
            "- `prd.md` for requirements and acceptance criteria\n"
            "- `design.md` if present for technical design\n"
            "- `implement.md` if present for execution order and validation plan\n"
        )
        stale_check_skill = (
            "# Code Quality Check\n\n"
            "Trellis check reads task artifacts.\n"
            "- `prd.md`\n"
            "- `design.md` if present\n"
            "- `implement.md` if present\n"
        )
        stale_change_workflow = (
            "# Change Local Workflow\n\n"
            "Edit `.trellis/workflow.md`.\n\n"
            "| `planning` | lightweight task with `prd.md` complete | ask for start review, then run `task.py start` |\n"
        )
        stale_change_context = (
            "# Change Context Loading\n\n"
            "Trellis context loading reads `.trellis/workflow.md` and `.trellis/tasks/`.\n\n"
            "5. `design.md` if present\n6. `implement.md` if present\n"
        )
        stale_context = (
            "# Local Context Injection System\n\n"
            "Trellis context injection reads `.trellis/workflow.md` and `.trellis/tasks/`.\n\n"
            "In both modes, JSONL files in the task directory are the manifest for spec/research context. "
            "Task artifacts are read separately in this order: `prd.md` -> `design.md if present` -> `implement.md if present`.\n"
        )
        stale_agents_doc = (
            "# Agents\n\n"
            "| `trellis-implement` | Implement against `prd.md`, optional `design.md` / `implement.md`, `implement.jsonl`, and related spec/research. |\n"
        )
        stale_context_hook = (
            "#!/usr/bin/env python3\n"
            "\"\"\"Multi-Platform Sub-Agent Context Injection Hook\"\"\"\n"
            "# Trellis active task resolver points to the current task directory.\n"
            "implement_jsonl = 'implement.jsonl'\n"
            "check_jsonl = 'check.jsonl'\n"
            "READ_ORDER = 'design.md if present and implement.md if present'\n"
        )
        for path, text in [
            (shared_brainstorm, stale_brainstorm),
            (cursor_brainstorm, stale_brainstorm),
            (shared_before_dev, stale_before_dev),
            (cursor_before_dev, stale_before_dev),
            (shared_check_skill, stale_check_skill),
            (cursor_check_skill, stale_check_skill),
            (shared_change_workflow, stale_change_workflow),
            (cursor_change_workflow, stale_change_workflow),
            (shared_change_context, stale_change_context),
            (cursor_change_context, stale_change_context),
            (shared_context, stale_context),
            (cursor_context, stale_context),
            (shared_agents_doc, stale_agents_doc),
            (cursor_agents_doc, stale_agents_doc),
            (cursor_context_hook, stale_context_hook),
        ]:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")

        payload = self.install({"codex", "cursor"})

        for relative in [
            ".agents/skills/trellis-brainstorm/SKILL.md",
            ".cursor/skills/trellis-brainstorm/SKILL.md",
            ".agents/skills/trellis-before-dev/SKILL.md",
            ".cursor/skills/trellis-before-dev/SKILL.md",
            ".agents/skills/trellis-check/SKILL.md",
            ".cursor/skills/trellis-check/SKILL.md",
            ".agents/skills/trellis-meta/references/customize-local/change-workflow.md",
            ".cursor/skills/trellis-meta/references/customize-local/change-workflow.md",
            ".agents/skills/trellis-meta/references/customize-local/change-context-loading.md",
            ".cursor/skills/trellis-meta/references/customize-local/change-context-loading.md",
            ".agents/skills/trellis-meta/references/local-architecture/context-injection.md",
            ".cursor/skills/trellis-meta/references/local-architecture/context-injection.md",
            ".agents/skills/trellis-meta/references/platform-files/agents.md",
            ".cursor/skills/trellis-meta/references/platform-files/agents.md",
            ".cursor/hooks/inject-subagent-context.py",
        ]:
            self.assertIn(relative, payload["replaced_overlays"])

        self.assertIn("explicit post-planning confirmation", shared_brainstorm.read_text(encoding="utf-8"))
        self.assertIn("explicit post-planning confirmation", cursor_brainstorm.read_text(encoding="utf-8"))
        self.assertIn("required `design.md`", shared_before_dev.read_text(encoding="utf-8"))
        self.assertIn("required `design.md`", cursor_before_dev.read_text(encoding="utf-8"))
        self.assertIn("required `design.md`", shared_check_skill.read_text(encoding="utf-8"))
        self.assertIn("required `design.md`", cursor_check_skill.read_text(encoding="utf-8"))
        self.assertIn("explicit post-planning confirmation", shared_change_workflow.read_text(encoding="utf-8"))
        self.assertIn("explicit post-planning confirmation", cursor_change_workflow.read_text(encoding="utf-8"))
        self.assertIn("required `design.md`", shared_change_context.read_text(encoding="utf-8"))
        self.assertIn("required `design.md`", cursor_change_context.read_text(encoding="utf-8"))
        self.assertIn("required `design.md`", shared_context.read_text(encoding="utf-8"))
        self.assertIn("required `design.md`", cursor_context.read_text(encoding="utf-8"))
        self.assertIn("required `prd.md`, `design.md`, `implement.md`", shared_agents_doc.read_text(encoding="utf-8"))
        self.assertIn("required `prd.md`, `design.md`, `implement.md`", cursor_agents_doc.read_text(encoding="utf-8"))
        self.assertIn("required design.md", cursor_context_hook.read_text(encoding="utf-8"))
        self.assertNotIn("Lightweight tasks may have only", shared_brainstorm.read_text(encoding="utf-8"))
        self.assertNotIn("design.md` if present", shared_before_dev.read_text(encoding="utf-8"))
        self.assertNotIn("design.md` if present", shared_check_skill.read_text(encoding="utf-8"))
        self.assertNotIn("lightweight task with `prd.md` complete", shared_change_workflow.read_text(encoding="utf-8"))
        self.assertNotIn("design.md` if present", shared_change_context.read_text(encoding="utf-8"))
        self.assertNotIn("design.md if present", shared_context.read_text(encoding="utf-8"))
        self.assertNotIn("optional `design.md` / `implement.md`", shared_agents_doc.read_text(encoding="utf-8"))
        self.assertNotIn("design.md if present", cursor_context_hook.read_text(encoding="utf-8"))

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
        self.assertIn('"upstream_ownership_validation": {', stdout.getvalue())

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
        install_canonical_workflow(self.repo)
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
        self.assertEqual(installed["extension"]["version"], "0.6.5-guru.16")
        self.assertEqual(installed["extension"]["target_trellis_cli"], "0.6.5")
        public_api = installed["extension"]["public_api"]
        canonical = json.loads(
            (self.guru_root / "trellis/guru-team-extension.json").read_text(encoding="utf-8")
        )
        self.assertIn(
            "contract-wording-review.json",
            canonical["public_api"]["artifact_contracts"],
        )
        self.assertIn("contract-wording-review.json", public_api["artifact_contracts"])
        self.assertIn("issue-review.json", public_api["artifact_contracts"])
        self.assertIn("agent-assignment.json", public_api["artifact_contracts"])
        self.assertIn("reviews/*.md", public_api["artifact_contracts"])
        self.assertIn("record-subagent-liveness-event", public_api["companion_scripts"])
        self.assertIn("check-subagent-liveness", public_api["companion_scripts"])
        self.assertIn("check-commit-messages", public_api["companion_scripts"])
        self.assertIn("create-task-commit", public_api["companion_scripts"])
        self.assertIn("run-skill-command", public_api["companion_scripts"])
        self.assertIn("record-planning-approval", public_api["companion_scripts"])
        self.assertIn("check-planning-approval", public_api["companion_scripts"])
        self.assertIn(
            "guru-planning-approval-2.0",
            public_api["skill_contracts"]["artifact_schema_ids"],
        )
        self.assertIn("sync-base", public_api["companion_scripts"])
        self.assertIn("check-base-sync", public_api["companion_scripts"])
        self.assertIn("preview-change-context-history", public_api["companion_scripts"])
        self.assertIn("record-context-discovery", public_api["companion_scripts"])
        self.assertIn("check-context-discovery", public_api["companion_scripts"])
        self.assertIn("record-requirements-clarification", public_api["companion_scripts"])
        self.assertIn("check-requirements-clarification", public_api["companion_scripts"])
        self.assertIn("record-contract-wording-review", public_api["companion_scripts"])
        self.assertIn("check-contract-wording-review", public_api["companion_scripts"])
        self.assertIn("record-change-request-review", public_api["companion_scripts"])
        self.assertIn("check-change-request-review", public_api["companion_scripts"])
        self.assertEqual(
            public_api["skill_runtime"],
            {
                "api_version": "1.0",
                "dispatcher": "run-skill-command",
                "manifest_path": ".trellis/guru-team/extension.json",
            },
        )
        self.assertIn("task-commit-plans/*.json", public_api["artifact_contracts"])
        self.assertEqual(
            public_api["skill_contracts"]["active_skill_ids"],
            [
                "guru-approve-task-plan",
                "guru-clarify-requirements",
                "guru-create-task-commit",
                "guru-create-task-workspace",
                "guru-discover-change-context",
                "guru-review-change-request",
                "guru-review-contract-wording",
                "guru-sync-base",
            ],
        )
        self.assertEqual(public_api["skill_contracts"]["planned_skill_ids"], [])
        self.assertIn(
            "guru-base-sync-result-1.0",
            public_api["skill_contracts"]["artifact_schema_ids"],
        )
        self.assertIn(
            "guru-requirements-clarification-2.0",
            public_api["skill_contracts"]["artifact_schema_ids"],
        )
        self.assertIn(
            "guru-contract-wording-review-1.0",
            public_api["skill_contracts"]["artifact_schema_ids"],
        )
        self.assertIn(
            "guru-change-request-review-1.0",
            public_api["skill_contracts"]["artifact_schema_ids"],
        )
        schema_relative = Path("schemas/contract-wording-review.schema.json")
        canonical_schema_path = (
            self.guru_root
            / "trellis/skills/guru-team/packages/guru-review-contract-wording"
            / schema_relative
        )
        canonical_schema_bytes = canonical_schema_path.read_bytes()
        canonical_schema = json.loads(canonical_schema_bytes)
        planning_dimensions = canonical_schema["$defs"]["planningCheckedDimensions"]
        self.assertFalse(planning_dimensions["additionalProperties"])
        self.assertEqual(
            set(planning_dimensions["required"]),
            {
                "no_requirement_weakening",
                "source_issue_semantics_preserved",
                "conditional_paths_have_conditions",
                "no_parallel_implementation_paths",
                "gates_have_machine_verifiable_conditions",
                "acceptance_criteria_are_deterministic",
                "external_quotes_are_labeled_non_contract",
            },
        )
        for package_root in (
            self.repo / ".trellis/guru-team/skills/packages/guru-review-contract-wording",
            self.repo / ".agents/skills/guru-review-contract-wording",
            self.repo / ".codex/skills/guru-review-contract-wording",
            self.repo / ".cursor/skills/guru-review-contract-wording",
        ):
            self.assertEqual(
                (package_root / schema_relative).read_bytes(),
                canonical_schema_bytes,
            )
        readiness_schema_relative = Path("schemas/change-request-review.schema.json")
        readiness_canonical_root = (
            self.guru_root
            / "trellis/skills/guru-team/packages/guru-review-change-request"
        )
        readiness_schema_bytes = (readiness_canonical_root / readiness_schema_relative).read_bytes()
        for package_root in (
            self.repo / ".trellis/guru-team/skills/packages/guru-review-change-request",
            self.repo / ".agents/skills/guru-review-change-request",
            self.repo / ".codex/skills/guru-review-change-request",
            self.repo / ".cursor/skills/guru-review-change-request",
        ):
            self.assertEqual(
                (package_root / readiness_schema_relative).read_bytes(),
                readiness_schema_bytes,
            )
        self.assertEqual(public_api["skill_contracts"]["interface_schema_id"], "guru-team-skill-interface-1.2")
        self.assertEqual(public_api["skill_contracts"]["reserved_skill_ids"], ["guru-create-work-commit"])
        self.assertIn("format-merge-commit", public_api["companion_scripts"])
        self.assertIn("backfill-finish-summary", public_api["companion_scripts"])
        self.assertIn("check-skill-packages", public_api["companion_scripts"])
        self.assertEqual(public_api["skill_contracts"]["canonical_root"], "trellis/skills/guru-team/")
        self.assertEqual(payload["guru_team_extension"]["target_trellis_cli"], "0.6.5")
        self.assertEqual(payload["guru_team_extension"]["trellis_cli_compatibility"], "0.6.5")
        self.assertEqual(payload["guru_team_extension"]["tested_trellis_cli"], ["0.6.5"])
        self.assertEqual(installed["install"]["selected_platforms"], ["codex", "cursor"])
        self.assertIn("observed at apply time", installed["notes"])
        self.assertIn("not a claim", installed["notes"])
        self.assertEqual(payload["extension_manifest"], ".trellis/guru-team/extension.json")
        self.assertEqual(payload["runtime_gitignore"]["rule"], ".trellis/.runtime/")
        self.assertIn(".trellis/.runtime/", (self.repo / ".gitignore").read_text(encoding="utf-8"))

    def test_runtime_gitignore_is_idempotent(self) -> None:
        first = preset.ensure_runtime_gitignore(self.repo)
        second = preset.ensure_runtime_gitignore(self.repo)
        self.assertEqual(first["action"], "installed")
        self.assertEqual(second["action"], "unchanged")
        self.assertEqual((self.repo / ".gitignore").read_text().count(".trellis/.runtime/"), 1)

    def test_install_removes_unmodified_obsolete_schema(self) -> None:
        obsolete = self.install_dst / "schemas/intake-handoff.schema.json"
        obsolete.parent.mkdir(parents=True)
        fixture = Path(__file__).resolve().parent / "fixtures/intake-handoff.schema.json"
        obsolete.write_bytes(fixture.read_bytes())

        payload = preset.install_assets(self.workflow_src, self.install_dst, self.repo, {"codex"})

        self.assertFalse(obsolete.exists())
        self.assertIn(".trellis/guru-team/schemas/intake-handoff.schema.json", payload["removed_obsolete"])

    def test_install_preserves_modified_obsolete_schema_as_conflict(self) -> None:
        obsolete = self.install_dst / "schemas/intake-handoff.schema.json"
        obsolete.parent.mkdir(parents=True)
        obsolete.write_text('{"user_modified": true}\n', encoding="utf-8")

        payload = preset.install_assets(self.workflow_src, self.install_dst, self.repo, {"codex"})

        self.assertTrue(obsolete.exists())
        self.assertIn(".trellis/guru-team/schemas/intake-handoff.schema.json", payload["obsolete_conflicts"])

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
