#!/usr/bin/env python3
"""Focused tests for Guru Team preset installer behavior."""

from __future__ import annotations

import json
import hashlib
import importlib.util
import copy
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
import sys
from io import StringIO
from unittest import mock

GURU_FINISH_ENTRIES = (
    ".codex/prompts/guru-finish-work.md",
    ".claude/commands/guru/finish-work.md",
    ".cursor/commands/guru-finish-work.md",
)

sys.path.insert(0, str(Path(__file__).resolve().parent))
import apply_guru_team_trellis_preset as preset


_RUNTIME_RESULT = {
    "status": "ok",
    "action": "reused",
    "runtime_identity": "0123456789abcdef01234567",
    "interpreter": sys.executable,
}
_ensure_managed_python_runtime = preset.ensure_managed_python_runtime
_runtime_patchers: list[mock._patch] = []


def setUpModule() -> None:
    _runtime_patchers.extend([
        mock.patch.object(
            preset,
            "ensure_managed_python_runtime",
            return_value=_RUNTIME_RESULT,
        ),
    ])
    for patcher in _runtime_patchers:
        patcher.start()


def tearDownModule() -> None:
    for patcher in reversed(_runtime_patchers):
        patcher.stop()


class ManagedPythonBootstrapBoundaryTest(unittest.TestCase):
    def test_helper_returns_success_payload(self) -> None:
        completed = subprocess.CompletedProcess(
            ["bootstrap"],
            0,
            json.dumps(_RUNTIME_RESULT),
            "",
        )
        with mock.patch.object(preset.subprocess, "run", return_value=completed):
            with tempfile.TemporaryDirectory() as tmp:
                result = _ensure_managed_python_runtime(
                    Path(tmp),
                    preset.guru_root_from_script(),
                )
        self.assertEqual(result, _RUNTIME_RESULT)

    def test_helper_preserves_stable_failure_json_without_traceback(self) -> None:
        failure = {
            "code": "runtime_dependency_missing",
            "field_path": "runtime",
            "dependency": "jsonschema",
            "runtime_identity": "0123456789abcdef01234567",
            "remediation": "trellis/presets/guru-team/scripts/bash/apply.sh --repo .",
            "detail": "network unavailable",
        }
        completed = subprocess.CompletedProcess(
            ["bootstrap"],
            2,
            json.dumps(failure),
            "",
        )
        with mock.patch.object(preset.subprocess, "run", return_value=completed):
            with tempfile.TemporaryDirectory() as tmp:
                with self.assertRaises(SystemExit) as raised:
                    _ensure_managed_python_runtime(
                        Path(tmp),
                        preset.guru_root_from_script(),
                    )
        payload = json.loads(str(raised.exception))
        self.assertEqual(set(payload), {"code", "field_path", "dependency", "runtime_identity", "remediation"})
        self.assertEqual(payload["runtime_identity"], failure["runtime_identity"])
        self.assertNotIn("detail", payload)

STAGE0_SKILL_IDS = (
    "guru-sync-base",
    "guru-discover-change-context",
    "guru-clarify-requirements",
    "guru-review-contract-wording",
    "guru-review-change-request",
    "guru-create-task-workspace",
)


def assert_thin_guru_finish_entry(testcase: unittest.TestCase, path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    testcase.assertIn("<!-- guru-team-overlay: v1 -->", text, path)
    testcase.assertIn("`.trellis/workflow.md`", text, path)
    for skill_id in (
        "guru-review-task-publication",
        "guru-finalize-task",
        "guru-merge-task-pr",
    ):
        testcase.assertIn(skill_id, text, path)
    for exit_id in (
        "ready",
        "return_to_task_work",
        "publication_review_stale",
        "resume_finalization",
        "reprepare_required",
        "ready_for_merge",
        "merged",
        "merge_blocked",
        "closure_mismatch",
        "blocked",
    ):
        testcase.assertIn(exit_id, text, path)
    testcase.assertIn("not user choices", text, path)
    testcase.assertIn("Do not add a routine confirmation", text, path)
    for forbidden in (
        "guru-verify-extension-installation",
        "verification_required",
        "not_required",
        "finish-work.sh",
        "--expected-plan-digest",
        "closeout_plan_digest",
        "artifact schema field",
    ):
        testcase.assertNotIn(forbidden, text, path)


def install_canonical_workflow(repo: Path) -> None:
    source = preset.guru_root_from_script() / "trellis/workflows/guru-team/workflow.md"
    target = repo / ".trellis/workflow.md"
    target.write_bytes(source.read_bytes())


class CanonicalWorkflowBaseEvolutionTest(unittest.TestCase):
    def test_current_pair_consumes_recorded_output_before_checkpoint_retirement(self) -> None:
        source = preset.guru_root_from_script() / "trellis/workflows/guru-team/workflow.md"
        text = source.read_text(encoding="utf-8")
        self.assertIn(
            "`current_pair` consumes and routes the recorded exact typed output, then deletes\n"
            "its one-use checkpoint.",
            text,
        )
        self.assertIn(
            "It must never resume from the guard's `resume_target`\n"
            "alone because that would discard a previously recorded non-`reconciled` exit.",
            text,
        )
        self.assertNotIn(
            "Unchanged or\nalready-current pairs resume the closed `resume_target`",
            text,
        )
        self.assertNotIn("An unchanged/current pair resumes activation", text)
        self.assertIn(
            "An unchanged pair resumes activation; a\n"
            "current pair consumes and routes its recorded exact typed output",
            text,
        )

    def test_installed_workflow_is_exact_canonical_projection(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = Path(raw)
            (repo / ".trellis").mkdir()
            install_canonical_workflow(repo)
            source = preset.guru_root_from_script() / "trellis/workflows/guru-team/workflow.md"
            self.assertEqual(source.read_bytes(), (repo / ".trellis/workflow.md").read_bytes())

    def test_base_reconciliation_eval_staging_uses_current_task_identity(self) -> None:
        adapter = (
            preset.guru_root_from_script()
            / "trellis/skills/guru-team/adapters/eval/native_adapter.py"
        ).read_text(encoding="utf-8")
        self.assertIn('"task_artifact_dir": task_ref', adapter)
        self.assertIn('"workspace_path": str(fixture.resolve())', adapter)
        self.assertIn('"branch_name": "eval/base-reconciliation"', adapter)
        self.assertIn('hashlib.sha256(task_ref.encode()).hexdigest()[:12]', adapter)
        self.assertNotIn(
            'owner-checkpoints/current"\n        / "guru-reconcile-task-base',
            adapter,
        )

    def test_eval_adapters_use_checkout_local_managed_python(self) -> None:
        root = preset.guru_root_from_script()
        for adapter_id in ("shared", "codex", "claude", "cursor"):
            with self.subTest(adapter=adapter_id):
                adapter = (
                    root / f"trellis/skills/guru-team/adapters/eval/{adapter_id}.sh"
                ).read_text(encoding="utf-8")
                self.assertIn('REPO_ROOT="$(cd "$SCRIPT_DIR/../../../../.." && pwd)"', adapter)
                self.assertIn('$SCRIPT_DIR/../../runtime/resolve-python.sh', adapter)
                self.assertIn('$SCRIPT_DIR/../../../runtime/resolve-python.sh', adapter)
                self.assertIn('exec "$RUNTIME_ASSETS/resolve-python.sh"', adapter)
                self.assertNotIn("exec python3", adapter)

        native_adapter_path = (
            root / "trellis/skills/guru-team/adapters/eval/native_adapter.py"
        )
        native_adapter = native_adapter_path.read_text(encoding="utf-8")
        shared_eval_path = (
            root / "trellis/skills/guru-team/adapters/eval/guru-team-shared-eval"
        )
        shared_eval = shared_eval_path.read_text(encoding="utf-8")

        self.assertFalse(native_adapter.startswith("#!"))
        self.assertFalse(shared_eval.startswith("#!"))
        self.assertTrue(os.access(shared_eval_path, os.X_OK))
        self.assertIn(
            'return [sys.executable, command, "--request"',
            native_adapter,
        )
        self.assertIn(
            'source_repo / "trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py"',
            native_adapter,
        )
        self.assertIn(
            '[sys.executable, str(apply_script), "--repo", str(fixture), "--all-platforms"]',
            native_adapter,
        )
        self.assertNotIn(
            '[str(apply_script), "--repo", str(fixture), "--all-platforms"]',
            native_adapter,
        )

    def test_verifier_shell_second_hops_use_checkout_local_managed_python(self) -> None:
        root = preset.guru_root_from_script()
        for script_name in ("finish-work.sh", "prepare-task.sh"):
            with self.subTest(script=script_name):
                script = (
                    root
                    / f"trellis/workflows/guru-team/scripts/bash/{script_name}"
                ).read_text(encoding="utf-8")
                self.assertIn(
                    '$SCRIPT_DIR/../../../../skills/guru-team/runtime/resolve-python.sh',
                    script,
                )
                self.assertIn(
                    '$REPO_ROOT/.trellis/guru-team/runtime',
                    script,
                )
                self.assertIn('exec "$RUNTIME_ASSETS/resolve-python.sh"', script)
                self.assertNotIn("python3", script)

    def test_dogfood_spec_matches_finalizer_six_exit_contract(self) -> None:
        root = preset.guru_root_from_script()
        spec = (root / ".trellis/spec/workflow/index.md").read_text(encoding="utf-8")
        interface = json.loads(
            (root / "trellis/skills/guru-team/packages/guru-finalize-task/interface.json").read_text(
                encoding="utf-8"
            )
        )

        self.assertEqual(6, len(interface["external_exits"]))
        self.assertIn("six public exits", spec)
        self.assertIn("six external\nexits", spec)
        self.assertNotIn("five public exits", spec)
        self.assertNotIn("five external\nsix exits", spec)


class Phase0TranscriptOwnerBindingTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        guru_root = preset.guru_root_from_script()
        module_path = (
            guru_root
            / "trellis/presets/guru-team/scripts/python/verify_installed_phase0_transcript.py"
        )
        spec = importlib.util.spec_from_file_location(
            "guru_phase0_transcript_verifier_test", module_path
        )
        assert spec is not None and spec.loader is not None
        cls.verifier = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.verifier)

    @staticmethod
    def clarity_owner() -> dict[str, object]:
        return {
            "mode": "workflow",
            "invocation_context": {"kind": "initial_issue"},
            "review_target": {
                "kind": "issue",
                "url": "https://github.com/example/guru-extension/issues/145",
            },
        }

    def test_rejects_clear_transcript_owner_mode_mismatch(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "owner mode"):
            self.verifier.assert_owner_binding(
                "guru-clarify-requirements",
                {"profile": "initial_change_request", "mode": "workflow"},
                {**self.clarity_owner(), "mode": "standalone"},
            )

    def test_rejects_clear_transcript_owner_profile_mismatch(self) -> None:
        owner = self.clarity_owner()
        owner["invocation_context"] = {"kind": "standalone_review"}
        with self.assertRaisesRegex(RuntimeError, "owner profile"):
            self.verifier.assert_owner_binding(
                "guru-clarify-requirements",
                {
                    "profile": "initial_change_request",
                    "mode": "workflow",
                    "target_locator": "https://github.com/example/guru-extension/issues/145",
                },
                owner,
            )

    def test_rejects_clear_transcript_owner_live_target_mismatch(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "owner profile"):
            self.verifier.assert_owner_binding(
                "guru-clarify-requirements",
                {
                    "profile": "initial_change_request",
                    "mode": "workflow",
                    "target_locator": "https://github.com/example/guru-extension/issues/146",
                },
                self.clarity_owner(),
            )

    def test_rejects_forbidden_private_runtime_material_recursively(self) -> None:
        cases = (
            ".trellis/.runtime/guru-team/evals/owner-result.json",
            ".trellis/.runtime/guru-team/phase0-transcript/change-request.json",
            ".trellis/.runtime/guru-team/checkpoints/owner-plan.json",
            ".trellis/.runtime/guru-team/checkpoints/current-transition.json",
        )
        for relative in cases:
            with self.subTest(relative=relative), tempfile.TemporaryDirectory() as raw:
                root = Path(raw)
                target = root / relative
                target.parent.mkdir(parents=True)
                target.write_text("{}\n", encoding="utf-8")
                with self.assertRaisesRegex(RuntimeError, "forbidden private runtime"):
                    self.verifier.assert_forbidden_runtime_absent(root)

    def test_allows_only_workspace_and_task_runtime_mappings(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            for relative in (
                ".trellis/.runtime/guru-team/workspaces/145-phase0.json",
                ".trellis/.runtime/guru-team/tasks/145-phase0.json",
            ):
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("{}\n", encoding="utf-8")
            self.verifier.assert_forbidden_runtime_absent(root)

    def test_finalizes_clarification_owner_identity_before_recording(self) -> None:
        owner = {
            "review_target": {"kind": "issue", "url": "https://example.invalid/145"},
            "target_disposition": {"disposition": "keep_current_open_issue"},
            "context_evidence": {"status": "current"},
            "confirmed_facts": [],
            "repository_answerable_questions": [],
            "clarification_rounds": [],
            "open_questions": [],
            "scope_proposals": [],
            "source_actions": [{
                "action_id": "no_source_change",
                "kind": "none",
                "target": None,
                "payload": None,
                "preimage_sha256": None,
                "payload_sha256": "0" * 64,
                "action_digest": "0" * 64,
            }],
            "affected_contracts": ["requirements"],
            "reason": "Current evidence is sufficient.",
            "content_identity": {},
        }

        finalized = self.verifier.finalize_clarification_owner(owner)
        unsigned = copy.deepcopy(finalized)
        unsigned.pop("content_identity")
        action = finalized["source_actions"][0]
        action_projection = {
            key: action[key]
            for key in (
                "action_id", "kind", "target", "payload", "preimage_sha256",
                "payload_sha256",
            )
        }

        self.assertIsNone(action["payload_sha256"])
        self.assertEqual(
            action["action_digest"], self.verifier.digest(action_projection)
        )
        self.assertEqual(
            finalized["content_identity"]["result_sha256"],
            self.verifier.digest(unsigned),
        )

    def test_projects_clarification_semantic_typed_outputs(self) -> None:
        identity = {
            key: value * 64
            for key, value in (
                ("result_sha256", "1"),
                ("target_sha256", "2"),
                ("disposition_sha256", "3"),
                ("content_sha256", "4"),
                ("scope_sha256", "5"),
            )
        }
        owner = {
            "typed_exit": "clear",
            "invocation_context": {"resume_target": "guru-review-contract-wording"},
            "content_identity": identity,
            "target_disposition": {
                "disposition_digest": "6" * 64,
                "duplicate_facts_sha256": "7" * 64,
            },
        }
        public_input = {"mode": "workflow", "continuation_id": "stage0-current"}
        transition = {
            "schema_version": "1.0",
            "transition_id": "context_current:old",
            "stage": "context_current",
            "mode": "workflow",
            "repo_locator": ".",
            "base": {
                "selected_base": "main",
                "post_sync_resolution_sha256": "8" * 64,
            },
            "target_locator": "https://github.com/example/repo/issues/145",
            "continuation_id": "stage0-current",
            "context_result_sha256": "9" * 64,
            "authority_content_sha256": "a" * 64,
        }

        clear = self.verifier.clarification_typed_output(
            owner, public_input, transition
        )
        needs = self.verifier.clarification_typed_output(
            {**owner, "typed_exit": "needs_context"}, public_input, transition
        )

        self.assertEqual(clear["exit_id"], "clear")
        self.assertEqual(clear["transition"]["stage"], "clarity_current")
        self.assertNotIn("authority_content_sha256", clear["transition"])
        self.assertEqual(needs["exit_id"], "needs_context")
        self.assertEqual(needs["transition"]["stage"], "base_current")
        refresh = self.verifier.clarification_typed_output(
            {**owner, "typed_exit": "refresh_context"}, public_input, transition
        )
        self.assertNotIn("handoff_base_branch", refresh)
        transition["base"]["source"] = "explicit"
        explicit_refresh = self.verifier.clarification_typed_output(
            {**owner, "typed_exit": "refresh_context"}, public_input, transition
        )
        self.assertEqual(explicit_refresh["handoff_base_branch"], "main")

    def test_projects_live_issue_for_wording_recorder(self) -> None:
        source = self.verifier.wording_change_request_source({
            "number": 145,
            "url": "https://github.com/example/repo/issues/145",
            "state": "OPEN",
            "title": "Current title",
            "body": "Current body",
            "updatedAt": "2026-08-12T00:00:00Z",
        })

        self.assertEqual(source, {
            "source_kind": "issue",
            "identity": "https://github.com/example/repo/issues/145",
            "title": "Current title",
            "body": "Current body",
            "updated_at": "2026-08-12T00:00:00Z",
        })

    def test_projects_readiness_reentry_to_required_owner_stage(self) -> None:
        wording = {
            "transition_id": "wording_current:old",
            "stage": "wording_current",
            "context_result_sha256": "1" * 64,
            "clarity_result_sha256": "2" * 64,
            "target_content_sha256": "3" * 64,
            "clarity": {"facts_sha256": "2" * 64},
            "target_disposition": {"disposition_sha256": "4" * 64},
            "wording_facts_sha256": "5" * 64,
            "wording": {"facts_sha256": "5" * 64},
        }

        clarity = self.verifier.readiness_reentry_transition(
            wording, "review_wording"
        )

        self.assertEqual(clarity["stage"], "clarity_current")
        self.assertIn("clarity", clarity)
        self.assertNotIn("wording", clarity)

    def test_failed_transcript_command_reports_json_stdout(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            script = Path(raw) / "fail.py"
            script.write_text(
                "#!/usr/bin/env python3\n"
                "print('{\"code\":\"schema_mismatch\"}')\n"
                "raise SystemExit(2)\n",
                encoding="utf-8",
            )
            script.chmod(0o755)

            with self.assertRaisesRegex(RuntimeError, "schema_mismatch"):
                self.verifier.run([script], cwd=Path(raw))


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


class AgentsAiFirstPrinciplesInstallerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        (self.repo / ".trellis").mkdir()

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_missing_agents_file_is_created(self) -> None:
        payload = preset.ensure_agents_ai_first_principles(self.repo)

        self.assertEqual(payload["action"], "installed")
        self.assertEqual(payload["path"], "AGENTS.md")
        text = (self.repo / "AGENTS.md").read_text(encoding="utf-8")
        self.assertEqual(text, preset.AGENTS_AI_FIRST_BLOCK)
        for principle in (
            "AI-first，不模拟人类审批流",
            "只保留不可重新推导且有直接 consumer 的最小结果",
            "任何阶段都不持久化用户授权信息或授权过程",
            "Digest 不是 workflow authority",
            "交互只服务真实选择和副作用",
            "语义门禁与持久化解耦",
        ):
            self.assertIn(principle, text)

    def test_existing_content_is_preserved_and_reapply_is_idempotent(self) -> None:
        path = self.repo / "AGENTS.md"
        original = b"# Local instructions\r\n\r\nKeep this byte-for-byte.\r\n"
        path.write_bytes(original)

        first = preset.ensure_agents_ai_first_principles(self.repo)
        first_bytes = path.read_bytes()
        second = preset.ensure_agents_ai_first_principles(self.repo)

        self.assertEqual(first["action"], "updated")
        self.assertEqual(second["action"], "unchanged")
        self.assertTrue(first_bytes.startswith(original))
        self.assertEqual(path.read_bytes(), first_bytes)
        self.assertEqual(first_bytes.count(preset.AGENTS_AI_FIRST_START_MARKER.encode()), 1)
        self.assertEqual(first_bytes.count(preset.AGENTS_AI_FIRST_END_MARKER.encode()), 1)

    def test_single_old_block_is_refreshed_without_touching_surrounding_bytes(self) -> None:
        path = self.repo / "AGENTS.md"
        prefix = b"# Local prefix\r\n"
        suffix = b"Local suffix remains.\r\n"
        old_block = (
            f"{preset.AGENTS_AI_FIRST_START_MARKER}\nold principles\n"
            f"{preset.AGENTS_AI_FIRST_END_MARKER}\n"
        ).encode("utf-8")
        path.write_bytes(prefix + old_block + suffix)

        payload = preset.ensure_agents_ai_first_principles(self.repo)

        self.assertEqual(payload["action"], "updated")
        self.assertEqual(path.read_bytes(), prefix + preset.AGENTS_AI_FIRST_BLOCK.encode("utf-8") + suffix)

    def test_malformed_or_duplicate_markers_fail_closed(self) -> None:
        path = self.repo / "AGENTS.md"
        cases = (
            f"{preset.AGENTS_AI_FIRST_START_MARKER}\nmissing end\n",
            (
                f"{preset.AGENTS_AI_FIRST_START_MARKER}\n"
                f"{preset.AGENTS_AI_FIRST_START_MARKER}\n"
                f"{preset.AGENTS_AI_FIRST_END_MARKER}\n"
            ),
            f"prefix {preset.AGENTS_AI_FIRST_START_MARKER}\n{preset.AGENTS_AI_FIRST_END_MARKER}\n",
            f"{preset.AGENTS_AI_FIRST_END_MARKER}\n{preset.AGENTS_AI_FIRST_START_MARKER}\n",
        )
        for content in cases:
            with self.subTest(content=content):
                original = content.encode("utf-8")
                path.write_bytes(original)
                with self.assertRaises(SystemExit):
                    preset.ensure_agents_ai_first_principles(self.repo)
                self.assertEqual(path.read_bytes(), original)


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
        self.assertEqual(payload["agents_principles"]["action"], "installed")
        self.assertEqual(payload["agents_principles"]["path"], "AGENTS.md")
        self.assertEqual(
            (self.repo / "AGENTS.md").read_text(encoding="utf-8"),
            preset.AGENTS_AI_FIRST_BLOCK,
        )
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

    def test_legacy_finalizer_wrappers_import_shared_runtime_from_canonical_and_installed_roots(self) -> None:
        self.install({"codex", "cursor"})
        env = os.environ.copy()
        env.pop("PYTHONPATH", None)
        wrappers = (
            "check-workspace-boundary.sh",
            "check-agent-recovery.sh",
            "record-agent-recovery.sh",
        )
        roots = (
            self.workflow_src / "scripts/bash",
            self.install_dst / "scripts/bash",
        )
        for root in roots:
            for wrapper in wrappers:
                with self.subTest(root=root, wrapper=wrapper):
                    process = subprocess.run(
                        [str(root / wrapper), "--help"],
                        cwd=self.repo,
                        env=env,
                        text=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        check=False,
                    )
                    self.assertEqual(process.returncode, 0, process.stderr)
                    self.assertIn("usage:", process.stdout)
                    self.assertNotIn("ModuleNotFoundError", process.stderr)

    def test_managed_spec_unknown_collision_is_preserved_with_new_sidecar(self) -> None:
        source_relative, target_relative = preset.MANAGED_SPEC_PATHS[0]
        target = self.repo / target_relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("# Local semantic contract\n", encoding="utf-8")

        result = preset.copy_managed_spec(
            self.guru_root / source_relative, target, self.repo, None
        )

        self.assertEqual(result["action"], "conflict")
        self.assertEqual(target.read_text(encoding="utf-8"), "# Local semantic contract\n")
        self.assertEqual(
            target.with_name(f"{target.name}.new").read_bytes(),
            (self.guru_root / source_relative).read_bytes(),
        )

    def test_managed_spec_declared_managed_upgrade_uses_backup(self) -> None:
        source_relative, target_relative = preset.MANAGED_SPEC_PATHS[0]
        target = self.repo / target_relative
        target.parent.mkdir(parents=True, exist_ok=True)
        old = b"# Prior managed semantic contract\n"
        target.write_bytes(old)
        previous = {
            "install": {
                "managed_assets": [target_relative.as_posix()],
                "managed_asset_hashes": {
                    target_relative.as_posix(): hashlib.sha256(old).hexdigest(),
                },
            }
        }

        result = preset.copy_managed_spec(
            self.guru_root / source_relative, target, self.repo, previous
        )

        self.assertEqual(result["action"], "updated_managed")
        self.assertEqual(target.read_bytes(), (self.guru_root / source_relative).read_bytes())
        self.assertEqual(target.with_name(f"{target.name}.bak").read_bytes(), old)

    def test_managed_spec_user_edit_is_preserved_on_reapply(self) -> None:
        first = self.install({"codex", "cursor"})
        self.assertEqual(first["skill_packages"]["status"], "ok")
        _, target_relative = preset.MANAGED_SPEC_PATHS[0]
        target = self.repo / target_relative
        local = target.read_bytes() + b"\n# Local semantic extension\n"
        target.write_bytes(local)
        manifest_before = (self.install_dst / "extension.json").read_bytes()

        second = self.install({"codex", "cursor"})

        sidecar = target.with_name(f"{target.name}.new")
        self.assertEqual(second["skill_packages"]["status"], "conflict")
        self.assertEqual(target.read_bytes(), local)
        self.assertEqual(
            sidecar.read_bytes(),
            (self.guru_root / preset.MANAGED_SPEC_PATHS[0][0]).read_bytes(),
        )
        self.assertEqual((self.install_dst / "extension.json").read_bytes(), manifest_before)
        self.assertEqual(
            [item["reason"] for item in second["skill_packages"]["conflicts"]],
            ["unknown_local_spec_edit"],
        )

    def test_managed_spec_equal_legacy_manifest_reapply_backfills_hash(self) -> None:
        first = self.install({"codex", "cursor"})
        self.assertEqual(first["skill_packages"]["status"], "ok")
        source_relative, target_relative = preset.MANAGED_SPEC_PATHS[0]
        target = self.repo / target_relative
        canonical = (self.guru_root / source_relative).read_bytes()
        self.assertEqual(target.read_bytes(), canonical)
        manifest_path = self.install_dst / "extension.json"
        legacy = json.loads(manifest_path.read_text(encoding="utf-8"))
        legacy["install"].pop("managed_asset_hashes")
        manifest_path.write_text(
            json.dumps(legacy, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

        second = self.install({"codex", "cursor"})

        self.assertEqual(second["skill_packages"]["status"], "ok")
        self.assertEqual(second["skill_installed_validation"]["status"], "passed")
        self.assertIn(target_relative.as_posix(), second["unchanged"])
        installed = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(
            installed["install"]["managed_asset_hashes"],
            {
                target.as_posix(): hashlib.sha256(
                    (self.guru_root / source).read_bytes()
                ).hexdigest()
                for source, target in preset.MANAGED_SPEC_PATHS
            },
        )
        self.assertEqual(
            sorted(
                path.relative_to(self.repo).as_posix()
                for path in self.repo.rglob("*")
                if path.is_file() and path.suffix in {".new", ".bak"}
            ),
            [],
        )

    def test_legacy_runtime_absence_is_a_clean_initial_install(self) -> None:
        removals, conflicts, sidecars = preset.remove_legacy_managed_assets(
            self.repo, self.install_dst
        )

        self.assertEqual(removals, [])
        self.assertEqual(conflicts, [])
        self.assertEqual(sidecars, [])

    def test_stale_managed_kernel_file_is_removed_by_previous_hash(self) -> None:
        target = self.install_dst / "runtime/retired.py"
        target.parent.mkdir(parents=True)
        target.write_text("retired kernel\n", encoding="utf-8")
        digest = hashlib.sha256(target.read_bytes()).hexdigest()

        removal, conflict, sidecar = preset.remove_stale_skill_path(
            self.repo,
            ".trellis/guru-team/runtime/retired.py",
            {".trellis/guru-team/runtime/retired.py": digest},
            True,
        )

        self.assertEqual(removal, {
            "path": ".trellis/guru-team/runtime/retired.py",
            "action": "removed_managed",
            "previous_managed_sha256": digest,
        })
        self.assertIsNone(conflict)
        self.assertIsNone(sidecar)
        self.assertFalse(target.exists())

    def test_stale_edited_kernel_file_is_preserved_and_blocks(self) -> None:
        target = self.install_dst / "runtime/retired.py"
        target.parent.mkdir(parents=True)
        target.write_text("local edit\n", encoding="utf-8")

        removal, conflict, sidecar = preset.remove_stale_skill_path(
            self.repo,
            ".trellis/guru-team/runtime/retired.py",
            {".trellis/guru-team/runtime/retired.py": "0" * 64},
            True,
        )

        self.assertIsNone(removal)
        self.assertEqual(conflict["reason"], "stale_unknown_local_edit")
        self.assertEqual(sidecar, ".trellis/guru-team/runtime/retired.py.new")
        self.assertEqual(target.read_text(encoding="utf-8"), "local edit\n")
        self.assertTrue(target.with_name("retired.py.new").is_file())

    def test_known_dot_five_legacy_runtime_is_removed(self) -> None:
        target = self.install_dst / "scripts/python/guru_team_trellis.py"
        target.parent.mkdir(parents=True)
        legacy = subprocess.run(
            [
                "git",
                "show",
                "v0.6.5-guru.5:trellis/workflows/guru-team/scripts/python/guru_team_trellis.py",
            ],
            cwd=self.guru_root,
            check=True,
            stdout=subprocess.PIPE,
        ).stdout
        target.write_bytes(legacy)

        removals, conflicts, sidecars = preset.remove_legacy_managed_assets(
            self.repo, self.install_dst
        )

        self.assertFalse(target.exists())
        self.assertEqual(conflicts, [])
        self.assertEqual(sidecars, [])
        self.assertEqual(removals, [{
            "path": ".trellis/guru-team/scripts/python/guru_team_trellis.py",
            "action": "removed_managed",
            "previous_managed_sha256": hashlib.sha256(legacy).hexdigest(),
        }])

    def test_unknown_legacy_runtime_is_preserved_and_blocks_with_sidecar(self) -> None:
        target = self.install_dst / "scripts/python/guru_team_trellis.py"
        target.parent.mkdir(parents=True)
        target.write_text("local runtime edit\n", encoding="utf-8")

        removals, conflicts, sidecars = preset.remove_legacy_managed_assets(
            self.repo, self.install_dst
        )

        sidecar = target.with_name("guru_team_trellis.py.new")
        self.assertEqual(removals, [])
        self.assertEqual(target.read_text(encoding="utf-8"), "local runtime edit\n")
        self.assertTrue(sidecar.is_file())
        self.assertEqual(sidecars, [
            ".trellis/guru-team/scripts/python/guru_team_trellis.py.new"
        ])
        self.assertEqual(conflicts[0]["reason"], "legacy_unknown_local_edit")
        self.assertIn("package-local", sidecar.read_text(encoding="utf-8"))

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
        registry = json.loads(
            (
                guru_root
                / "trellis/skills/guru-team/registry.json"
            ).read_text(encoding="utf-8")
        )
        active_package_count = sum(
            entry.get("state") == "active"
            for entry in registry["skills"]
        )
        group_order: list[str] = []
        for path in fresh_paths:
            group = next(
                label
                for prefix, label in (
                    (".trellis/guru-team/runtime/", "installed"),
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
                *(
                    ["shared", "codex", "claude", "cursor"]
                    * active_package_count
                ),
            ],
        )

    def test_default_platforms_install_codex_cursor_and_shared_overlays(self) -> None:
        payload = self.install()

        self.assertEqual(payload["platforms"], ["codex", "cursor"])
        self.assertFalse(payload["all_platforms"])
        self.assertIn(Path("scripts/bash/check-workspace-boundary.sh"), preset.MANAGED_ASSET_PATHS)
        self.assertIn(Path("scripts/bash/discover-skill-contract.sh"), preset.MANAGED_ASSET_PATHS)
        self.assertIn(Path("scripts/bash/discover-skill-evals.sh"), preset.MANAGED_ASSET_PATHS)
        self.assertIn(Path("scripts/bash/run-skill-evals.sh"), preset.MANAGED_ASSET_PATHS)
        self.assertIn(Path("scripts/bash/run-skill-command.sh"), preset.MANAGED_ASSET_PATHS)
        self.assertIn(Path("scripts/bash/preview-finalization.sh"), preset.MANAGED_ASSET_PATHS)
        self.assertIn(Path("scripts/bash/record-finalization-gate.sh"), preset.MANAGED_ASSET_PATHS)
        self.assertIn(Path("scripts/bash/check-finalization-gate.sh"), preset.MANAGED_ASSET_PATHS)
        self.assertIn(Path("scripts/bash/execute-finalization-transition.sh"), preset.MANAGED_ASSET_PATHS)
        self.assertIn(Path("scripts/bash/preview-task-pr-merge.sh"), preset.MANAGED_ASSET_PATHS)
        self.assertIn(Path("scripts/bash/record-task-pr-merge.sh"), preset.MANAGED_ASSET_PATHS)
        self.assertIn(Path("scripts/bash/check-task-pr-merge.sh"), preset.MANAGED_ASSET_PATHS)
        self.assertIn(Path("scripts/bash/execute-task-pr-merge.sh"), preset.MANAGED_ASSET_PATHS)
        self.assertIn(Path("scripts/bash/invoke-task-pr-merge.sh"), preset.MANAGED_ASSET_PATHS)
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
        self.assertIn(Path("scripts/bash/record-agent-recovery.sh"), preset.MANAGED_ASSET_PATHS)
        self.assertIn(Path("scripts/bash/check-agent-recovery.sh"), preset.MANAGED_ASSET_PATHS)
        self.assertNotIn(Path("scripts/bash/record-agent-assignment.sh"), preset.MANAGED_ASSET_PATHS)
        self.assertNotIn(Path("scripts/bash/check-agent-assignment.sh"), preset.MANAGED_ASSET_PATHS)
        self.assertNotIn(Path("scripts/bash/record-subagent-liveness-event.sh"), preset.MANAGED_ASSET_PATHS)
        self.assertNotIn(Path("scripts/bash/check-subagent-liveness.sh"), preset.MANAGED_ASSET_PATHS)
        self.assertIn(Path("scripts/bash/check-commit-messages.sh"), preset.MANAGED_ASSET_PATHS)
        self.assertIn(Path("scripts/bash/format-merge-commit.sh"), preset.MANAGED_ASSET_PATHS)
        self.assertIn(Path("schemas/finish-summary.schema.json"), preset.MANAGED_ASSET_PATHS)
        self.assertTrue((self.repo / ".trellis/guru-team/scripts/bash/check-workspace-boundary.sh").is_file())
        self.assertTrue((self.repo / ".trellis/guru-team/scripts/bash/discover-skill-contract.sh").is_file())
        self.assertTrue(os.access(self.repo / ".trellis/guru-team/scripts/bash/discover-skill-contract.sh", os.X_OK))
        self.assertTrue(os.access(self.repo / ".trellis/guru-team/scripts/bash/discover-skill-evals.sh", os.X_OK))
        self.assertTrue(os.access(self.repo / ".trellis/guru-team/scripts/bash/run-skill-evals.sh", os.X_OK))
        self.assertTrue(
            os.access(
                self.repo
                / ".trellis/guru-team/scripts/bash/record-task-publication-review.sh",
                os.X_OK,
            )
        )
        self.assertTrue(
            os.access(
                self.repo
                / ".trellis/guru-team/scripts/bash/check-task-publication-review.sh",
                os.X_OK,
            )
        )
        self.assertTrue((self.repo / ".trellis/guru-team/scripts/bash/run-skill-command.sh").is_file())
        self.assertTrue(os.access(self.repo / ".trellis/guru-team/scripts/bash/run-skill-command.sh", os.X_OK))
        for name in (
            "preview-finalization.sh",
            "record-finalization-gate.sh",
            "check-finalization-gate.sh",
            "execute-finalization-transition.sh",
            "preview-task-pr-merge.sh",
            "record-task-pr-merge.sh",
            "check-task-pr-merge.sh",
            "execute-task-pr-merge.sh",
            "invoke-task-pr-merge.sh",
        ):
            self.assertTrue((self.repo / ".trellis/guru-team/scripts/bash" / name).is_file())
            self.assertTrue(os.access(self.repo / ".trellis/guru-team/scripts/bash" / name, os.X_OK))
        self.assertTrue(os.access(self.repo / ".trellis/guru-team/scripts/bash/sync-base.sh", os.X_OK))
        self.assertTrue(os.access(self.repo / ".trellis/guru-team/scripts/bash/check-base-sync.sh", os.X_OK))
        self.assertTrue(os.access(self.repo / ".trellis/guru-team/scripts/bash/preview-change-context-history.sh", os.X_OK))
        self.assertTrue(os.access(self.repo / ".trellis/guru-team/scripts/bash/record-context-discovery.sh", os.X_OK))
        self.assertTrue(os.access(self.repo / ".trellis/guru-team/scripts/bash/check-context-discovery.sh", os.X_OK))
        self.assertTrue((self.repo / ".trellis/guru-team/scripts/bash/resolve-human-artifacts.sh").is_file())
        self.assertTrue(os.access(self.repo / ".trellis/guru-team/scripts/bash/resolve-human-artifacts.sh", os.X_OK))
        self.assertTrue((self.repo / ".trellis/guru-team/scripts/bash/record-agent-recovery.sh").is_file())
        self.assertTrue(os.access(self.repo / ".trellis/guru-team/scripts/bash/record-agent-recovery.sh", os.X_OK))
        self.assertTrue((self.repo / ".trellis/guru-team/scripts/bash/check-agent-recovery.sh").is_file())
        self.assertTrue(os.access(self.repo / ".trellis/guru-team/scripts/bash/check-agent-recovery.sh", os.X_OK))
        for obsolete in (
            "record-agent-assignment.sh",
            "check-agent-assignment.sh",
            "record-subagent-liveness-event.sh",
            "check-subagent-liveness.sh",
        ):
            self.assertFalse((self.repo / ".trellis/guru-team/scripts/bash" / obsolete).exists())
        self.assertTrue((self.repo / ".trellis/guru-team/scripts/bash/check-commit-messages.sh").is_file())
        self.assertTrue(os.access(self.repo / ".trellis/guru-team/scripts/bash/check-commit-messages.sh", os.X_OK))
        self.assertTrue((self.repo / ".trellis/guru-team/scripts/bash/format-merge-commit.sh").is_file())
        self.assertTrue(os.access(self.repo / ".trellis/guru-team/scripts/bash/format-merge-commit.sh", os.X_OK))
        self.assertTrue((self.repo / ".trellis/guru-team/schemas/finish-summary.schema.json").is_file())
        self.assertIn("session_auto_commit: false", (self.repo / ".trellis/config.yaml").read_text(encoding="utf-8"))
        self.assertIn(".trellis/workspace/", (self.repo / ".gitignore").read_text(encoding="utf-8"))
        self.assertEqual(payload["replaced_overlays"], [])
        self.assertFalse((self.repo / ".agents/skills/trellis-start/SKILL.md").exists())
        self.assertFalse((self.repo / ".trellis/agents/implement.md").exists())
        self.assertFalse((self.repo / ".codex/prompts/trellis-start.md").exists())
        self.assertFalse((self.repo / ".cursor/commands/trellis-continue.md").exists())
        self.assertTrue((self.repo / ".agents/skills/guru-create-task-workspace/SKILL.md").is_file())
        self.assertTrue((self.repo / ".codex/skills/guru-create-task-workspace/SKILL.md").is_file())
        self.assertTrue((self.repo / ".cursor/skills/guru-create-task-workspace/SKILL.md").is_file())
        self.assertTrue((self.repo / ".codex/prompts/guru-finish-work.md").is_file())
        self.assertTrue((self.repo / ".cursor/commands/guru-finish-work.md").is_file())
        assert_thin_guru_finish_entry(self, self.repo / ".codex/prompts/guru-finish-work.md")
        assert_thin_guru_finish_entry(self, self.repo / ".cursor/commands/guru-finish-work.md")
        self.assertFalse((self.repo / ".claude").exists())

    def test_repeated_default_apply_does_not_restore_unselected_claude_overlay(self) -> None:
        self.install()
        self.assertFalse((self.repo / ".claude").exists())

        second_payload = self.install()

        self.assertEqual(second_payload["platforms"], ["codex", "cursor"])
        self.assertEqual(second_payload["new_copies"], [])
        for relative in (
            ".codex/prompts/guru-finish-work.md",
            ".cursor/commands/guru-finish-work.md",
        ):
            self.assertEqual(
                (self.repo / relative).read_bytes(),
                (self.guru_root / "trellis/presets/guru-team/overlays" / relative).read_bytes(),
            )
        self.assertFalse((self.repo / ".claude").exists())

    def test_non_current_installed_manifest_fails_before_reapply(self) -> None:
        self.install()
        manifest_path = self.install_dst / "extension.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["schema_version"] = "not-current"
        manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        before = manifest_path.read_bytes()

        with self.assertRaisesRegex(SystemExit, "does not match the current contract"):
            self.install()

        self.assertEqual(manifest_path.read_bytes(), before)

    def test_default_reapply_does_not_restore_removed_unselected_claude_guru_entry(self) -> None:
        self.install({"claude", "codex", "cursor"})
        claude_entry = self.repo / ".claude/commands/guru/finish-work.md"
        claude_entry.unlink()

        self.install()

        self.assertFalse(claude_entry.exists())

    def test_unknown_local_guru_finish_edit_gets_new_copy(self) -> None:
        target = self.repo / ".codex/prompts/guru-finish-work.md"
        target.parent.mkdir(parents=True)
        target.write_text("# Local custom finish command\n", encoding="utf-8")

        payload = self.install({"codex"})

        sidecar = target.with_name("guru-finish-work.md.new")
        self.assertIn(".codex/prompts/guru-finish-work.md.new", payload["new_copies"])
        self.assertEqual(target.read_text(encoding="utf-8"), "# Local custom finish command\n")
        self.assertEqual(
            sidecar.read_bytes(),
            (self.guru_root / "trellis/presets/guru-team/overlays/.codex/prompts/guru-finish-work.md").read_bytes(),
        )

    def test_marker_preserving_selected_overlay_edit_is_not_overwritten(self) -> None:
        self.install({"codex"})
        target = self.repo / ".codex/prompts/guru-finish-work.md"
        local_bytes = target.read_bytes() + b"\n# Local project finish customization\n"
        target.write_bytes(local_bytes)
        manifest_before = (self.install_dst / "extension.json").read_bytes()

        payload = self.install({"codex"})

        sidecar = target.with_name("guru-finish-work.md.new")
        self.assertEqual(payload["overlays"]["status"], "conflict")
        self.assertEqual(
            [item["reason"] for item in payload["overlays"]["conflicts"]],
            ["unknown_local_edit"],
        )
        self.assertIn(".codex/prompts/guru-finish-work.md.new", payload["new_copies"])
        self.assertEqual(target.read_bytes(), local_bytes)
        self.assertEqual(
            sidecar.read_bytes(),
            (
                self.guru_root
                / "trellis/presets/guru-team/overlays/.codex/prompts/guru-finish-work.md"
            ).read_bytes(),
        )
        self.assertFalse(target.with_name("guru-finish-work.md.bak").exists())
        self.assertEqual((self.install_dst / "extension.json").read_bytes(), manifest_before)

    def test_explicit_claude_platform_installs_only_shared_and_claude_overlays(self) -> None:
        payload = self.install({"claude"})

        self.assertEqual(payload["platforms"], ["claude"])
        self.assertFalse(payload["all_platforms"])
        self.assertTrue((self.repo / ".agents/skills/guru-create-task-workspace/SKILL.md").is_file())
        self.assertTrue((self.repo / ".claude/skills/guru-create-task-workspace/SKILL.md").is_file())
        installed_finish_integration = (
            self.repo
            / ".trellis/guru-team/skills/tests/test_finish_family_integration.py"
        )
        self.assertTrue(installed_finish_integration.is_file())
        self.assertEqual(
            installed_finish_integration.read_bytes(),
            (
                self.guru_root
                / "trellis/skills/guru-team/tests/test_finish_family_integration.py"
            ).read_bytes(),
        )
        self.assertTrue((self.repo / ".claude/commands/guru/finish-work.md").is_file())
        assert_thin_guru_finish_entry(self, self.repo / ".claude/commands/guru/finish-work.md")
        self.assertFalse((self.repo / ".claude/commands/trellis/continue.md").exists())
        self.assertFalse((self.repo / ".claude/agents/trellis-check.md").exists())
        self.assertFalse((self.repo / ".agents/skills/trellis-meta").exists())
        self.assertFalse((self.repo / ".codex").exists())
        self.assertFalse((self.repo / ".cursor").exists())

    def test_all_platforms_installs_only_guru_owned_overlays(self) -> None:
        platforms, all_platforms = preset.selected_platforms(None, True)
        payload = self.install(platforms, all_platforms=all_platforms)

        self.assertTrue(all_platforms)
        self.assertEqual(payload["platforms"], ["claude", "codex", "cursor"])
        ownership_facts = payload["upstream_ownership_validation"]
        self.assertEqual(ownership_facts["schema_version"], "3.0")
        self.assertEqual(ownership_facts["overlay_count"], 3)
        self.assertEqual(ownership_facts["active_skill_count"], 21)
        self.assertEqual(ownership_facts["managed_claim_count"], 9)
        self.assertEqual(payload["replaced_overlays"], [])
        overlay_root = self.guru_root / "trellis/presets/guru-team/overlays"
        guru_entry_bytes = []
        for relative in GURU_FINISH_ENTRIES:
            canonical = overlay_root / relative
            installed = self.repo / relative
            assert_thin_guru_finish_entry(self, canonical)
            assert_thin_guru_finish_entry(self, installed)
            self.assertFalse(canonical.is_symlink())
            self.assertFalse(installed.is_symlink())
            self.assertEqual(canonical.stat().st_mode & 0o777, 0o644)
            self.assertEqual(installed.stat().st_mode & 0o777, 0o644)
            self.assertEqual(installed.read_bytes(), canonical.read_bytes())
            guru_entry_bytes.append(canonical.read_bytes())
        self.assertEqual(len(set(guru_entry_bytes)), 1)
        installed_manifest = json.loads(
            (self.repo / ".trellis/guru-team/extension.json").read_text(encoding="utf-8")
        )
        managed_assets = installed_manifest["install"]["managed_assets"]
        installed_integration_path = (
            ".trellis/guru-team/skills/tests/test_finish_family_integration.py"
        )
        self.assertEqual(installed_manifest["install"]["selected_platforms"], ["claude", "codex", "cursor"])
        self.assertTrue(installed_manifest["install"]["all_platforms"])
        self.assertEqual(
            len(managed_assets),
            len(preset.MANAGED_ASSET_PATHS)
            + len(preset.MANAGED_SPEC_PATHS)
            + len(GURU_FINISH_ENTRIES)
            + 1,
        )
        self.assertEqual(managed_assets, sorted(set(managed_assets)))
        self.assertNotIn(installed_integration_path, managed_assets)
        self.assertEqual(
            [path for path in managed_assets if not (self.repo / path).is_file()],
            [],
        )
        managed_specs = {
            target.as_posix(): source
            for source, target in preset.MANAGED_SPEC_PATHS
        }
        self.assertEqual(
            set(managed_specs),
            {
                ".trellis/spec/workflow/companion-scripts.md",
                ".trellis/spec/workflow/data-contracts.md",
                ".trellis/spec/workflow/quality-guidelines.md",
                ".trellis/spec/workflow/requirements-design-test-ssot.md",
                ".trellis/spec/workflow/semantic-retrieval.md",
                ".trellis/spec/workflow/skill-package-contract.md",
                ".trellis/spec/workflow/workflow-contract.md",
            },
        )
        for target, source in managed_specs.items():
            self.assertIn(target, managed_assets)
            self.assertEqual(
                (self.repo / target).read_bytes(),
                (self.guru_root / source).read_bytes(),
            )
        integration_records = [
            record
            for record in installed_manifest["skill_packages"]["files"]
            if record["path"] == installed_integration_path
        ]
        self.assertEqual(len(integration_records), 1)
        self.assertEqual(
            integration_records[0]["source"],
            "trellis/skills/guru-team/tests/test_finish_family_integration.py",
        )
        self.assertEqual(
            integration_records[0]["sha256"],
            hashlib.sha256(
                (
                    self.guru_root
                    / "trellis/skills/guru-team/tests/test_finish_family_integration.py"
                ).read_bytes()
            ).hexdigest(),
        )

    def test_review_branch_current_gate_schema_closes_every_platform_interface_reference(self) -> None:
        platforms, all_platforms = preset.selected_platforms(None, True)
        payload = self.install(platforms, all_platforms=all_platforms)

        self.assertEqual(payload["skill_packages"]["status"], "ok")
        canonical_root = (
            self.guru_root
            / "trellis/skills/guru-team/packages/guru-review-branch"
        )
        schema_relative = Path("schemas/review-gate-6.0.schema.json")
        canonical_bytes = (canonical_root / schema_relative).read_bytes()
        package_roots = (
            self.repo / ".trellis/guru-team/skills/packages/guru-review-branch",
            self.repo / ".agents/skills/guru-review-branch",
            self.repo / ".codex/skills/guru-review-branch",
            self.repo / ".claude/skills/guru-review-branch",
            self.repo / ".cursor/skills/guru-review-branch",
        )
        legacy_schema_paths = (
            Path("schemas/review-gate.schema.json"),
            Path("schemas/review-gate-4.0.schema.json"),
            Path("schemas/review-gate-5.0.schema.json"),
        )
        for package_root in package_roots:
            with self.subTest(package_root=package_root):
                interface = json.loads(
                    (package_root / "interface.json").read_text(encoding="utf-8")
                )
                referenced = {
                    Path(str(item["path"]))
                    for item in interface["schemas"]
                    if str(item["id"]) == "review_gate_schema"
                }
                self.assertEqual(referenced, {schema_relative})
                self.assertEqual(
                    (package_root / schema_relative).read_bytes(), canonical_bytes
                )
                self.assertEqual(
                    (package_root / schema_relative).stat().st_mode & 0o777,
                    0o644,
                )
                for legacy_relative in legacy_schema_paths:
                    self.assertEqual(
                        (package_root / legacy_relative).read_bytes(),
                        (canonical_root / legacy_relative).read_bytes(),
                    )

    def test_all_platforms_to_subset_removes_clean_managed_overlay(self) -> None:
        platforms, all_platforms = preset.selected_platforms(None, True)
        self.install(platforms, all_platforms=all_platforms)
        claude_entry = self.repo / ".claude/commands/guru/finish-work.md"
        self.assertTrue(claude_entry.is_file())

        payload = self.install({"codex", "cursor"})

        self.assertEqual(payload["overlays"]["status"], "ok")
        self.assertFalse(claude_entry.exists())
        self.assertEqual(
            payload["overlays"]["removals"],
            [
                {
                    "path": ".claude/commands/guru/finish-work.md",
                    "action": "removed_managed",
                    "previous_managed_sha256": hashlib.sha256(
                        (
                            self.guru_root
                            / "trellis/presets/guru-team/overlays/.claude/commands/guru/finish-work.md"
                        ).read_bytes()
                    ).hexdigest(),
                }
            ],
        )
        installed_manifest = json.loads(
            (self.install_dst / "extension.json").read_text(encoding="utf-8")
        )
        self.assertEqual(installed_manifest["overlays"]["selected_platforms"], ["codex", "cursor"])
        self.assertNotIn(
            ".claude/commands/guru/finish-work.md",
            installed_manifest["install"]["managed_assets"],
        )

    def test_all_platforms_to_subset_preserves_edited_overlay_and_blocks_activation(self) -> None:
        platforms, all_platforms = preset.selected_platforms(None, True)
        self.install(platforms, all_platforms=all_platforms)
        claude_entry = self.repo / ".claude/commands/guru/finish-work.md"
        local_bytes = claude_entry.read_bytes() + b"\n# Claude project customization\n"
        claude_entry.write_bytes(local_bytes)
        manifest_before = (self.install_dst / "extension.json").read_bytes()

        payload = self.install({"codex", "cursor"})

        sidecar = claude_entry.with_name("finish-work.md.new")
        self.assertEqual(payload["overlays"]["status"], "conflict")
        self.assertEqual(
            [item["reason"] for item in payload["overlays"]["conflicts"]],
            ["stale_unknown_local_edit"],
        )
        self.assertEqual(claude_entry.read_bytes(), local_bytes)
        self.assertEqual(sidecar.read_bytes(), preset.GURU_OVERLAY_REMOVAL_SIDECAR)
        self.assertIn(".claude/commands/guru/finish-work.md.new", payload["new_copies"])
        self.assertEqual((self.install_dst / "extension.json").read_bytes(), manifest_before)

    def test_known_overlay_hash_upgrade_uses_backup_and_recovers(self) -> None:
        self.install({"codex"})
        target = self.repo / ".codex/prompts/guru-finish-work.md"
        old_bytes = b"<!-- guru-team-overlay: v0 -->\n# Previous managed finish entry\n"
        target.write_bytes(old_bytes)
        manifest_path = self.install_dst / "extension.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        record = manifest["overlays"]["files"][0]
        record["sha256"] = hashlib.sha256(old_bytes).hexdigest()
        manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

        upgraded = self.install({"codex"})

        backup = target.with_name("guru-finish-work.md.bak")
        self.assertEqual(upgraded["overlays"]["status"], "conflict")
        self.assertEqual(upgraded["overlays"]["conflicts"], [])
        self.assertEqual(upgraded["overlays"]["sidecars"], [
            ".codex/prompts/guru-finish-work.md.bak"
        ])
        self.assertEqual(backup.read_bytes(), old_bytes)
        self.assertEqual(
            target.read_bytes(),
            (
                self.guru_root
                / "trellis/presets/guru-team/overlays/.codex/prompts/guru-finish-work.md"
            ).read_bytes(),
        )
        self.assertNotEqual(upgraded["skill_installed_validation"]["returncode"], 0)
        self.assertEqual(upgraded["skill_activation_validation"]["returncode"], 0)

        backup.unlink()
        recovered = self.install({"codex"})

        self.assertEqual(recovered["overlays"]["status"], "ok")
        self.assertEqual(recovered["overlays"]["sidecars"], [])
        installed_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(installed_manifest["overlays"]["status"], "ok")

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
        self.assertTrue((self.repo / ".codex/prompts/guru-finish-work.md").is_file())
        self.assertTrue((self.repo / ".cursor/commands/guru-finish-work.md").is_file())
        self.assertTrue((self.repo / ".codex/skills/guru-create-task-workspace/SKILL.md").is_file())
        self.assertTrue((self.repo / ".cursor/skills/guru-create-task-workspace/SKILL.md").is_file())
        self.assertFalse((self.repo / ".codex/prompts/trellis-start.md").exists())
        self.assertFalse((self.repo / ".cursor/commands/trellis-continue.md").exists())
        self.assertFalse((self.repo / ".claude").exists())

    def test_throwaway_verifier_cleans_preview_and_scans_sidecars_after_reapply(self) -> None:
        verifier = (
            self.guru_root
            / "trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh"
        ).read_text(encoding="utf-8")

        current_private_schema = (
            'assert "guru-extension-installation-verification-result-5.0" '
            'in api["skill_contracts"]["private_artifact_schema_ids"]'
        )
        retired_private_schema = current_private_schema.replace("5.0", "4.0")
        self.assertIn(current_private_schema, verifier)
        self.assertNotIn(retired_private_schema, verifier)
        self.assertNotIn("test_issue_174_controlled_replay_is_one_chained_session", verifier)
        self.assertNotIn("GURU_ISSUE_174_REPLAY_REPORT", verifier)
        self.assertIn(
            'assert managed_specs.issubset(set(assets))',
            verifier,
        )
        self.assertNotIn(
            'assert (target / ".trellis/spec/workflow/semantic-retrieval.md").is_file()',
            verifier,
        )
        grading_path = (
            self.guru_root
            / "trellis/presets/guru-team/tests/semantic-retrieval-grading.json"
        )
        grading = json.loads(grading_path.read_text(encoding="utf-8"))
        self.assertEqual(grading["schema_version"], "1.0")
        self.assertEqual(
            {(item["case_id"], item["assertion_id"]) for item in grading["results"]},
            {
                ("clear-route", "bilingual-history-decision"),
                ("clear-route", "single-language-negative-blocked"),
                ("context-ready-route", "bilingual-current-evidence"),
                ("context-ready-route", "exact-literal-preserved"),
            },
        )
        self.assertTrue(all(item["passed"] for item in grading["results"]))
        self.assertEqual(
            verifier.count('--semantic-grading "$SEMANTIC_RETRIEVAL_GRADING"'),
            4,
        )

        preview_assert = verifier.index('test -f "$TARGET/.trellis/workflow.md.new"')
        preview_remove = verifier.index('rm -f "$TARGET/.trellis/workflow.md.new"', preview_assert)
        initial_switch = verifier.index(
            'trellis workflow --marketplace "$WORKFLOW_SOURCE" --template guru-team --force',
            preview_remove,
        )
        update = verifier.index("trellis update --dry-run 2>&1", initial_switch)
        workflow_reapply = verifier.index(
            'trellis workflow --marketplace "$WORKFLOW_SOURCE" --template guru-team --force',
            update,
        )
        preset_reapply = verifier.index(
            'source_python "$REPO_ROOT/trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py"',
            workflow_reapply,
        )
        final_scan = verifier.index('FINAL_SIDECARS="$(find "$TARGET"', preset_reapply)
        initial_ownership = verifier.index('ownership_checkpoint "initial-init-before-preset-apply"')
        initial_apply = verifier.index(
            'source_python "$REPO_ROOT/trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py"',
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
        self.assertIn("Unexpected .new/.bak sidecars after preview, switch, update, and preset reapply", verifier)
        self.assertIn('"id":"guru-requirements-clear-router"', verifier)
        self.assertNotIn(
            '"exit":"clear","consumer":{"kind":"workflow","id":"guru-review-contract-wording"}',
            verifier,
        )
        self.assertIn('verify_requirements_clarification_exits "initial"', verifier)
        self.assertIn('verify_requirements_clarification_exits "after-update"', verifier)
        self.assertIn('--mode installed', verifier)
        self.assertIn('--skill guru-clarify-requirements', verifier)
        self.assertIn('"clear", "needs_context", "refresh_context", "retarget_context", "new_task", "blocked"', verifier)
        self.assertNotIn("derive_requirements_clarification_result", verifier)
        self.assertIn('verify_contract_wording_standalone_profiles "initial"', verifier)
        self.assertIn('verify_contract_wording_standalone_profiles "after-update"', verifier)
        self.assertIn('verify_change_request_review_package "initial"', verifier)
        self.assertIn('verify_change_request_review_package "after-update"', verifier)
        self.assertIn('"planned_skill_ids"] == []', verifier)
        self.assertIn('test -f "$TARGET/.trellis/guru-team/skills/packages/guru-create-task-workspace/SKILL.md"', verifier)
        self.assertIn('test -x "$TARGET/.trellis/guru-team/skills/packages/guru-create-task-workspace/scripts/record-task-workspace-plan.sh"', verifier)
        self.assertIn('test ! -e "$TARGET/.claude/skills/guru-create-task-workspace/scripts/create-task-workspace.sh"', verifier)
        self.assertIn('test ! -e "$TARGET/.codex/skills/guru-create-task-workspace/scripts/create-task-workspace.sh"', verifier)
        self.assertIn('test ! -e "$TARGET/.cursor/skills/guru-create-task-workspace/scripts/check-task-workspace-result.sh"', verifier)
        self.assertIn('fail_if_python_cache "throwaway target" "$TARGET"', verifier)
        self.assertIn('record_planning_contract_wording "$TASK_REL"', verifier)
        self.assertIn('record_and_check_planning_approval "$TASK_REL" "initial"', verifier)
        self.assertIn(
            'record_and_check_planning_approval "$POST_UPDATE_TASK_REL" "after-update"',
            verifier,
        )
        self.assertIn('--task "$task_rel" --input "$input" >"$result"', verifier)
        self.assertIn('recorded["schema_version"] == "5.0"', verifier)
        self.assertNotIn("--ambiguity-reviewer", verifier)
        self.assertNotIn("--normative-hit", verifier)
        self.assertIn("verify_installed_closeout.py", verifier)
        self.assertIn("--case initial", verifier)
        self.assertIn("--case after-update", verifier)
        self.assertIn('verify_closeout_package_boundaries "fresh-install"', verifier)
        self.assertIn(
            'verify_closeout_package_boundaries "after-update-reapply"', verifier
        )
        for skill_id in (
            "guru-review-task-publication",
            "guru-verify-extension-installation",
            "guru-finalize-task",
            "guru-merge-task-pr",
        ):
            self.assertIn(f'    "{skill_id}",', verifier)
        self.assertIn('private_dirs = [projection / name for name in ("runtime", "tests", "errors")]', verifier)
        self.assertIn('if path.name != "invoke.sh"', verifier)
        self.assertIn(
            'for artifact in interface["public_contracts"]["private_artifacts"]',
            verifier,
        )
        self.assertIn('payload["after_archive_hook_preflight"] is True', verifier)
        self.assertIn('payload["merge_exit"] == "merged"', verifier)
        self.assertIn('payload["pr_head"] == payload["merge_commit"]', verifier)
        self.assertIn('payload["verifier_artifacts"] == 0', verifier)
        self.assertIn("verify_installed_task_workspace.py", verifier)
        self.assertIn("installed-task-workspace-initial", verifier)
        self.assertIn("installed-task-workspace-after-update", verifier)
        self.assertIn("--checkpoint initial", verifier)
        self.assertIn("--checkpoint after-update", verifier)
        self.assertIn("--existing-developer-identity", verifier)
        self.assertIn('payload["developer_identity_preserved"] is True', verifier)
        self.assertIn('payload["task_creator"] == "fixture-maintainer"', verifier)
        self.assertEqual(verifier.count("verify_installed_phase0_transcript.py"), 2)
        self.assertEqual(
            verifier.count(
                'verify_installed_phase0_transcript.py" --installed-repo "$TARGET" '
                '--work-root "$WORK_DIR/installed-phase0-transcript-'
            ),
            2,
        )
        self.assertEqual(
            verifier.count(
                '--checkpoint initial-install --semantic-grading '
                '"$SEMANTIC_RETRIEVAL_GRADING"'
            ),
            1,
        )
        self.assertEqual(
            verifier.count(
                '--checkpoint update-reapply --semantic-grading '
                '"$SEMANTIC_RETRIEVAL_GRADING"'
            ),
            1,
        )
        self.assertIn("installed-phase0-transcript-initial", verifier)
        self.assertIn("installed-phase0-transcript-after-update", verifier)
        self.assertIn('payload["exit_family_count"] == 23', verifier)
        self.assertIn('len(payload["six_step_transcript"]) == 6', verifier)
        self.assertIn('row["edge_id"] for row in payload["reentry_transcripts"]', verifier)
        self.assertIn(
            'row["source"] for row in payload["refresh_provenance_transcripts"]',
            verifier,
        )
        self.assertIn('"legacy_typed_output_schema_ids"', verifier)
        self.assertIn(
            'len(api["skill_contracts"]["legacy_typed_output_schema_ids"]) == 5',
            verifier,
        )
        self.assertIn("build_discovery_invocation", verifier)
        self.assertIn("DISCOVERY_STANDALONE_BASE_JSON", verifier)
        self.assertIn("DISCOVERY_WORKFLOW_BASE_JSON", verifier)
        self.assertNotIn("DISCOVERY_PUBLIC_INPUT_REL", verifier)
        self.assertNotIn("DISCOVERY_RECOVERY_PUBLIC_INPUT_REL", verifier)
        self.assertIn("PHASE0_REVIEWED_BASE_PROVENANCE", verifier)
        self.assertIn(
            '--reviewed-base-provenance "$PHASE0_REVIEWED_BASE_PROVENANCE"',
            verifier,
        )
        self.assertIn('trellis init -y --claude --codex --cursor', verifier)
        self.assertIn(
            'skills["selected_platforms"] == ["claude", "codex", "cursor"]',
            verifier,
        )
        self.assertIn(
            f"assert len(assets) == {len(preset.MANAGED_ASSET_PATHS) + len(preset.MANAGED_SPEC_PATHS) + len(GURU_FINISH_ENTRIES) + 1}",
            verifier,
        )
        self.assertIn('ownership["schema_version"] == "3.0"', verifier)
        self.assertIn('test -f "$TARGET/.codex/prompts/guru-finish-work.md"', verifier)
        self.assertIn('test -f "$TARGET/.claude/commands/guru/finish-work.md"', verifier)
        self.assertIn('test -f "$TARGET/.cursor/commands/guru-finish-work.md"', verifier)
        self.assertIn(
            'installed_python "$TARGET" "$TARGET/.trellis/guru-team/skills/tests/test_finish_family_integration.py" -q',
            verifier,
        )
        self.assertIn('verify_finish_family_integration "initial"', verifier)
        self.assertIn(
            'verify_finish_family_integration "after-update-reapply"', verifier
        )
        self.assertIn(
            '"$REPO_ROOT/trellis/workflows/guru-team/scripts/bash/run-skill-evals.sh"',
            verifier,
        )
        self.assertIn(
            '--root "$REPO_ROOT" \\\n'
            '    --mode source \\\n'
            '    --skill guru-verify-extension-installation',
            verifier,
        )
        self.assertNotIn("record_throwaway_completed_agent", verifier)
        self.assertIn('! grep -q "record-subagent-liveness-event.sh"', verifier)
        self.assertIn("record-agent-recovery.sh", verifier)
        self.assertNotIn("TASK_COMMIT_RUNTIME_DIR", verifier)
        self.assertIn("prepare_task_commit_candidate initial_commit", verifier)
        self.assertIn("scripts/prepare-task-commit.sh", verifier)
        self.assertNotIn("/rules/" + "branches/", verifier)
        self.assertNotIn("create_task_commit_plan", verifier)
        self.assertIn('test -f "$TARGET/.trellis/guru-team/skills/adapters/eval/native_adapter.py"', verifier)
        for adapter_id in ("shared", "codex", "claude", "cursor"):
            self.assertIn(
                f'test -x "$TARGET/.trellis/guru-team/skills/adapters/eval/{adapter_id}.sh"',
                verifier,
            )
        self.assertIn("SkillPackageIntegrationTests", verifier)
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
        self.assertNotIn("importlib", installed_workspace)
        self.assertNotIn("guru_team_trellis.py", installed_workspace)
        self.assertIn('wrappers / "create-task-workspace.sh"', installed_workspace)
        self.assertIn('wrappers / "check-task-workspace-result.sh"', installed_workspace)
        self.assertIn('wrappers / "invoke.sh"', installed_workspace)
        self.assertIn("--existing-developer-identity", installed_workspace)
        self.assertIn('task_data.get("creator") != "fixture-maintainer"', installed_workspace)
        installed_phase0 = (
            self.guru_root
            / "trellis/presets/guru-team/scripts/python/verify_installed_phase0_transcript.py"
        ).read_text(encoding="utf-8")
        self.assertNotIn("importlib", installed_phase0)
        self.assertNotIn("guru_team_trellis.py", installed_phase0)
        self.assertIn('"--invocation",', installed_phase0)
        self.assertIn('"-",', installed_phase0)
        self.assertIn('parser.add_argument("--semantic-grading", required=True)', installed_phase0)
        self.assertIn('"--semantic-grading",\n                    semantic_grading,', installed_phase0)
        self.assertNotIn('"passed": True', installed_phase0)
        self.assertIn("actual_exit != expected_exit", installed_phase0)
        self.assertIn('len(actual_pairs) != 23', installed_phase0)
        self.assertIn("create-task-workspace.sh", installed_phase0)
        self.assertIn("check-task-workspace-result.sh", installed_phase0)
        self.assertIn('"gh",', installed_phase0)
        self.assertIn('issue["facts_sha256"] = context_digest(issue)', installed_phase0)
        self.assertIn('"history_preview": preview', installed_phase0)
        wording_owner_source = installed_phase0[
            installed_phase0.index("def wording_owner_for_issue("):
            installed_phase0.index("def readiness_owner_for_issue(")
        ]
        self.assertNotIn('"semantic_review": {', wording_owner_source)
        self.assertIn("def checked_readiness_owner_for_issue(", installed_phase0)
        self.assertIn("readiness-change-request.json", installed_phase0)
        self.assertIn("wording-change-request.json", installed_phase0)
        self.assertIn('"--query-json",', installed_phase0)
        self.assertIn(
            "json.dumps(change_input, ensure_ascii=False, sort_keys=True)",
            installed_phase0,
        )
        for retired_flag in (
            '"--issue-ref",',
            '"--path",',
            '"--command",',
            '"--term",',
            '"--query",',
            '"--symbol",',
        ):
            self.assertNotIn(retired_flag, installed_phase0)
        self.assertNotIn("owner_eval_payload", installed_phase0)
        self.assertNotIn("cleanup_seed_workspace", installed_phase0)
        self.assertNotIn("bind_workspace_plan_to_transition", installed_phase0)
        self.assertNotIn("phase0-transcript/change-request.json", installed_phase0)
        self.assertIn("stage_transcript_owner_repo", installed_phase0)
        self.assertIn("project_installed_output", installed_phase0)
        self.assertIn("def reentry_transcripts(", installed_phase0)
        self.assertIn("def refresh_provenance_transcripts(", installed_phase0)
        self.assertIn("workspace_plan_for_transition", installed_phase0)
        self.assertIn("assert_forbidden_runtime_absent", installed_phase0)
        chain_source = installed_phase0[
            installed_phase0.index("def six_step_transcript("):
            installed_phase0.index("def parse_args()")
        ]
        self.assertNotIn("records", chain_source)
        self.assertNotIn("HAPPY_CASES", chain_source)
        self.assertNotIn("evals", chain_source)
        installed_closeout = (
            self.guru_root
            / "trellis/presets/guru-team/scripts/python/verify_installed_closeout.py"
        ).read_text(encoding="utf-8")
        self.assertIn(
            'root / ".trellis/guru-team/skills/packages/guru-finalize-task"',
            installed_closeout,
        )
        self.assertNotIn("rules/" + "branches/", installed_closeout)
        for wrapper_name in (
            "preview-finalization",
            "record-finalization-gate",
            "check-finalization-gate",
            "execute-finalization-transition",
            "invoke",
        ):
            self.assertIn(f'"{wrapper_name}"', installed_closeout)
        for wrapper_name in (
            "preview-task-pr-merge",
            "record-task-pr-merge",
            "check-task-pr-merge",
            "execute-task-pr-merge",
        ):
            self.assertIn(f'"{wrapper_name}"', installed_closeout)
        self.assertNotIn(
            '.trellis/guru-team/scripts/bash/finish-work.sh', installed_closeout
        )
        self.assertNotIn("guru_team_trellis.py", installed_closeout)
        self.assertNotIn("class InstalledRuntimeFacade", installed_closeout)
        self.assertNotIn("load_installed_package_runtime", installed_closeout)
        self.assertNotIn('"runtime/owner.py"', installed_closeout)
        self.assertIn("class InstalledPackageClient", installed_closeout)
        self.assertIn('process_env["PYTHONDONTWRITEBYTECODE"] = "1"', installed_closeout)
        self.assertIn('["git", "reset", "--mixed", "HEAD"]', installed_closeout)
        for wrapper_name in (
            "record-planning-approval.sh",
            "check-planning-approval.sh",
            "record-phase2-check.sh",
            "check-phase2-check.sh",
            "prepare-task-commit.sh",
            "create-task-commit.sh",
            "review-branch.sh",
            "check-review-gate.sh",
        ):
            self.assertIn(f'"{wrapper_name}"', installed_closeout)
        self.assertIn('owners["guru-approve-task-plan"]', installed_closeout)
        self.assertIn('owners["guru-check-task"]', installed_closeout)
        self.assertIn('owners["guru-create-task-commit"]', installed_closeout)
        self.assertIn('owners["guru-review-branch"]', installed_closeout)
        self.assertIn('owners["guru-review-task-publication"]', installed_closeout)
        self.assertNotIn(
            'list(root.rglob("marketplace-verification.json"))',
            installed_closeout,
        )
        self.assertIn('root / ".trellis/tasks"', installed_closeout)
        self.assertIn('root / ".trellis/.runtime/guru-team"', installed_closeout)
        self.assertIn(
            '".trellis/guru-team/skills/packages/guru-review-task-publication"',
            installed_closeout,
        )
        self.assertIn('args[:2] == ["remote", "get-url"]', installed_closeout)
        self.assertIn('args[:2] == ["pr", "ready"]', installed_closeout)
        self.assertIn('value("--match-head-commit")', installed_closeout)
        self.assertIn('merged_payload.get("exit_id") != expected_merge_exit', installed_closeout)
        self.assertIn('expected_merge_exit = "closure_mismatch" if closure_mismatch else "merged"', installed_closeout)
        self.assertIn("installed Merge terminal recovery repeated the merge mutation", installed_closeout)
        self.assertIn("installed Finalizer terminal recovery repeated a GitHub mutation", installed_closeout)
        self.assertIn('after_archive:', installed_closeout)
        self.assertIn('after-archive-hook-preflight', installed_closeout)
        self.assertIn('hook_executed', installed_closeout)
        self.assertIn('installed-after-archive-hook-', installed_closeout)
        self.assertIn('ledger = {\n        "schema_version": "2.0",', installed_closeout)
        self.assertIn(
            'semantic_review.write_text(\n        json.dumps(\n            {\n                "schema_version": "3.0",',
            installed_closeout,
        )
        self.assertNotIn("verification_required", installed_closeout)
        self.assertIn('root.rglob("marketplace-verification.json")', installed_closeout)
        self.assertNotIn("copytree", installed_closeout)
        self.assertIn(
            '"branch_review_commit": branch_check["review_commit"]',
            installed_closeout,
        )

    def test_dogfood_drift_checks_ownership_before_payload_bytes(self) -> None:
        checker = (
            self.guru_root
            / "trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh"
        ).read_text(encoding="utf-8")

        ownership_gate = checker.index('"$OWNERSHIP_CHECK" --repo "$REPO_ROOT" --json')
        payload_loop = checker.index('while IFS= read -r source; do')
        self.assertLess(ownership_gate, payload_loop)
        self.assertIn("Missing executable ownership validator", checker)
        self.assertIn("current Guru-owned claims", checker)
        self.assertIn("three canonical Guru Team finish overlays", checker)

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
            preset.copy_repo_to_staging(self.repo, staging_repo)

            self.assertFalse((staging_repo / ".trellis/.developer").exists())
            self.assertTrue((staging_repo / ".trellis/guru-team/extension.json").is_file())

        self.assertEqual(developer_identity.read_bytes(), identity_bytes)

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
        self.assertEqual(installed["schema_version"], preset.INSTALLED_EXTENSION_SCHEMA_VERSION)
        self.assertEqual(set(installed), preset.INSTALLED_EXTENSION_KEYS)
        self.assertEqual(installed["extension"]["extension_id"], "guru-team")
        self.assertEqual(installed["extension"]["version"], payload["guru_team_extension"]["version"])
        self.assertEqual(installed["extension"]["version"], "0.6.5-guru.35")
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
        self.assertNotIn("agent-assignment.json", public_api["artifact_contracts"])
        self.assertNotIn("reviews/*.md", public_api["artifact_contracts"])
        self.assertNotIn("review.md", public_api["artifact_contracts"])
        self.assertIn("record-agent-recovery", public_api["companion_scripts"])
        self.assertIn("check-agent-recovery", public_api["companion_scripts"])
        self.assertNotIn("record-agent-assignment", public_api["companion_scripts"])
        self.assertNotIn("check-agent-assignment", public_api["companion_scripts"])
        self.assertNotIn("record-subagent-liveness-event", public_api["companion_scripts"])
        self.assertNotIn("check-subagent-liveness", public_api["companion_scripts"])
        self.assertIn("check-commit-messages", public_api["companion_scripts"])
        self.assertIn("create-task-commit", public_api["companion_scripts"])
        self.assertIn("discover-skill-contract", public_api["companion_scripts"])
        self.assertIn("discover-skill-evals", public_api["companion_scripts"])
        self.assertIn("run-skill-evals", public_api["companion_scripts"])
        self.assertIn("run-skill-command", public_api["companion_scripts"])
        self.assertIn("record-planning-approval", public_api["companion_scripts"])
        self.assertIn("check-planning-approval", public_api["companion_scripts"])
        self.assertIn("record-task-publication-review", public_api["companion_scripts"])
        self.assertIn("check-task-publication-review", public_api["companion_scripts"])
        self.assertIn("execute-extension-verification", public_api["companion_scripts"])
        self.assertIn("record-extension-verification", public_api["companion_scripts"])
        self.assertIn("check-extension-verification", public_api["companion_scripts"])
        self.assertIn("invoke-extension-verification", public_api["companion_scripts"])
        for command_id in (
            "guard-task-base-pair",
            "execute-base-candidate",
            "record-base-reconciliation",
            "check-base-reconciliation",
            "invoke-guru-reconcile-task-base",
        ):
            self.assertIn(command_id, public_api["companion_scripts"])
        self.assertIn(
            "guru-planning-approval-3.0",
            public_api["skill_contracts"]["artifact_schema_ids"],
        )
        self.assertIn(
            "guru-phase2-check-4.0",
            public_api["skill_contracts"]["artifact_schema_ids"],
        )
        self.assertEqual(public_api["skill_contracts"]["registry_schema_id"], "guru-team-skill-registry-1.4")
        self.assertEqual(
            set(public_api["skill_contracts"]),
            {
                "canonical_root",
                "installed_root",
                "registry_schema_id",
                "interface_schema_id",
                "interface_schema_ids",
                "public_input_schema_ids",
                "typed_output_schema_ids",
                "legacy_typed_output_schema_ids",
                "private_artifact_schema_ids",
                "artifact_schema_ids",
                "active_skill_ids",
                "planned_skill_ids",
                "registry_lifecycle",
                "contract_manifests",
                "workflow_markers",
            },
        )
        for field, expected_count in (
            ("public_input_schema_ids", 57),
            ("typed_output_schema_ids", 78),
            ("private_artifact_schema_ids", 18),
        ):
            self.assertEqual(
                public_api["skill_contracts"][field],
                canonical["public_api"]["skill_contracts"][field],
            )
            self.assertEqual(len(public_api["skill_contracts"][field]), expected_count)
        public_input_schema_ids = public_api["skill_contracts"]["public_input_schema_ids"]
        self.assertIn("guru-normal-scenario-input-aggregate-1.0", public_input_schema_ids)
        self.assertIn(
            "guru-normal-scenario-input-implementation-discovery-1.0",
            public_input_schema_ids,
        )
        self.assertIn(
            "guru-stage0-clarify-requirements-input-initial-change-request-2.0",
            public_input_schema_ids,
        )
        self.assertNotIn(
            "guru-stage0-clarify-requirements-input-initial-change-request-1.0",
            public_input_schema_ids,
        )
        typed_output_schema_ids = public_api["skill_contracts"]["typed_output_schema_ids"]
        self.assertIn("guru-normal-scenario-output-classified-1.0", typed_output_schema_ids)
        self.assertIn(
            "guru-normal-scenario-output-scope-confirmation-required-1.0",
            typed_output_schema_ids,
        )
        self.assertIn(
            "guru-stage0-discover-change-context-output-context-ready-3.0",
            typed_output_schema_ids,
        )
        self.assertNotIn(
            "guru-stage0-discover-change-context-output-context-ready-2.0",
            typed_output_schema_ids,
        )
        discovery_interface = json.loads(
            (
                self.guru_root
                / "trellis/skills/guru-team/packages/guru-discover-change-context/interface.json"
            ).read_text(encoding="utf-8")
        )
        artifact_by_path = {
            artifact["path"]: artifact["id"] for artifact in discovery_interface["artifacts"]
        }
        self.assertEqual(
            artifact_by_path["examples/public-context-ready-output-3.0.json"],
            "public_output_context_ready_example_3_0",
        )
        self.assertEqual(public_api["skill_evals"]["schema_id"], "guru-team-skill-evals-1.0")
        self.assertEqual(
            public_api["skill_evals"]["schema_ids"],
            ["guru-team-skill-evals-1.0", "guru-team-skill-evals-2.0"],
        )
        self.assertEqual(
            public_api["skill_evals"]["production_schema_id"],
            "guru-team-skill-evals-2.0",
        )
        self.assertEqual(
            public_api["skill_contracts"]["contract_manifests"],
            [
                {
                    "id": "production-current-v4",
                    "schema_id": "guru-team-production-contract-manifest-4.0",
                    "path": "contracts/production-current-4.0.json",
                }
            ],
        )
        self.assertEqual(
            public_api["skill_evals"]["adapter_request_schema_ids"],
            [
                "guru-team-skill-eval-adapter-request-1.0",
                "guru-team-skill-eval-adapter-request-2.0",
                "guru-team-skill-eval-adapter-request-3.0",
            ],
        )
        self.assertEqual(
            public_api["skill_evals"]["adapter_response_schema_ids"],
            [
                "guru-team-skill-eval-adapter-response-1.0",
                "guru-team-skill-eval-adapter-response-2.0",
                "guru-team-skill-eval-adapter-response-3.0",
            ],
        )
        self.assertEqual(
            public_api["skill_evals"]["run_schema_ids"],
            [
                "guru-team-skill-eval-run-1.0",
                "guru-team-skill-eval-run-2.0",
                "guru-team-skill-eval-run-3.0",
                "guru-team-skill-eval-run-4.0",
            ],
        )
        self.assertEqual(
            public_api["skill_evals"]["control_map_schema_id"],
            "guru-team-skill-eval-control-map-1.0",
        )
        self.assertEqual(
            public_api["skill_evals"]["control_map_schema_path"],
            "schemas/skill-eval-control-map-1.0.schema.json",
        )
        self.assertEqual(public_api["skill_evals"]["adapter_ids"], ["shared", "codex", "claude", "cursor"])
        for relative in (
            "contracts/production-current.json",
            "contracts/production-current-2.0.json",
            "contracts/production-current-3.0.json",
            "contracts/production-current-4.0.json",
            "schemas/production-contract-manifest-4.0.schema.json",
            "schemas/skill-evals-2.0.schema.json",
            "schemas/skill-evals.schema.json",
            "schemas/skill-eval-adapter-request-3.0.schema.json",
            "schemas/skill-eval-adapter-request-2.0.schema.json",
            "schemas/skill-eval-adapter-request.schema.json",
            "schemas/skill-eval-adapter-response-3.0.schema.json",
            "schemas/skill-eval-adapter-response-2.0.schema.json",
            "schemas/skill-eval-adapter-response.schema.json",
            "schemas/skill-eval-control-map-1.0.schema.json",
            "schemas/skill-eval-native-trace.schema.json",
            "schemas/skill-eval-run-4.0.schema.json",
            "schemas/skill-eval-run-3.0.schema.json",
            "schemas/skill-eval-run.schema.json",
            "adapters/eval/shared.json",
            "adapters/eval/codex.json",
            "adapters/eval/claude.json",
            "adapters/eval/cursor.json",
        ):
            self.assertTrue((self.repo / ".trellis/guru-team/skills" / relative).is_file(), relative)
        installed_contracts = self.repo / ".trellis/guru-team/skills/contracts"
        self.assertEqual(
            (installed_contracts / "production-current.json").read_bytes(),
            (installed_contracts / "production-current-4.0.json").read_bytes(),
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
        self.assertNotIn("task-commit-plans/*.json", public_api["artifact_contracts"])
        self.assertEqual(
            public_api["skill_contracts"]["active_skill_ids"],
            [
                "guru-approve-task-plan",
                "guru-bootstrap-repository-ssot",
                "guru-check-task",
                "guru-clarify-requirements",
                "guru-create-task-commit",
                "guru-create-task-workspace",
                "guru-discover-change-context",
                "guru-execute-task-free-change",
                "guru-finalize-task",
                "guru-maintain-architecture-baseline",
                "guru-maintain-requirements-design-test-ssot",
                "guru-merge-task-pr",
                "guru-qualify-normal-scenario",
                "guru-reconcile-task-base",
                "guru-review-branch",
                "guru-review-change-request",
                "guru-review-contract-wording",
                "guru-review-task-publication",
                "guru-select-workflow-mode",
                "guru-sync-base",
                "guru-verify-extension-installation",
            ],
        )
        self.assertEqual(
            public_api["skill_contracts"]["planned_skill_ids"],
            [],
        )
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
        self.assertIn(
            "guru-task-publication-readiness-4.0",
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
        installed_wording = self.repo / ".trellis/guru-team/skills/packages/guru-review-contract-wording"
        self.assertEqual(
            (installed_wording / schema_relative).read_bytes(),
            canonical_schema_bytes,
        )
        for package_root in (
            self.repo / ".agents/skills/guru-review-contract-wording",
            self.repo / ".codex/skills/guru-review-contract-wording",
            self.repo / ".cursor/skills/guru-review-contract-wording",
        ):
            self.assertFalse((package_root / schema_relative).exists())
        readiness_schema_relative = Path("schemas/change-request-review.schema.json")
        readiness_canonical_root = (
            self.guru_root
            / "trellis/skills/guru-team/packages/guru-review-change-request"
        )
        readiness_schema_bytes = (readiness_canonical_root / readiness_schema_relative).read_bytes()
        installed_readiness = self.repo / ".trellis/guru-team/skills/packages/guru-review-change-request"
        self.assertEqual(
            (installed_readiness / readiness_schema_relative).read_bytes(),
            readiness_schema_bytes,
        )
        for package_root in (
            self.repo / ".agents/skills/guru-review-change-request",
            self.repo / ".codex/skills/guru-review-change-request",
            self.repo / ".cursor/skills/guru-review-change-request",
        ):
            self.assertFalse((package_root / readiness_schema_relative).exists())
        self.assertEqual(public_api["skill_contracts"]["interface_schema_id"], "guru-team-skill-interface-1.4")
        self.assertEqual(
            public_api["skill_contracts"]["interface_schema_ids"],
            [
                "guru-team-skill-interface-1.4",
                "guru-team-skill-interface-1.5",
                "guru-team-skill-interface-1.6",
            ],
        )
        self.assertIn("format-merge-commit", public_api["companion_scripts"])
        self.assertIn("check-skill-packages", public_api["companion_scripts"])
        self.assertEqual(public_api["skill_contracts"]["canonical_root"], "trellis/skills/guru-team/")
        self.assertEqual(payload["guru_team_extension"]["target_trellis_cli"], "0.6.5")
        self.assertEqual(payload["guru_team_extension"]["tested_trellis_cli"], ["0.6.5"])
        self.assertEqual(installed["install"]["selected_platforms"], ["codex", "cursor"])
        self.assertEqual(
            installed["install"]["managed_asset_hashes"],
            {
                target.as_posix(): hashlib.sha256(
                    (self.guru_root / source).read_bytes()
                ).hexdigest()
                for source, target in preset.MANAGED_SPEC_PATHS
            },
        )
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
        source_commit = "a" * 40

        def fake_git(args: list[str], cwd: Path) -> mock.Mock:
            command = " ".join(args)
            if command == "rev-parse --show-toplevel":
                return mock.Mock(returncode=0, stdout=str(self.guru_root), stderr="")
            if command == "remote get-url origin":
                return mock.Mock(returncode=0, stdout="https://github.com/castbox/guru-trellis.git\n", stderr="")
            if command == "rev-parse --abbrev-ref HEAD":
                return mock.Mock(returncode=0, stdout="main\n", stderr="")
            if command == "rev-parse HEAD":
                return mock.Mock(returncode=0, stdout=f"{source_commit}\n", stderr="")
            if command == "describe --tags --exact-match HEAD":
                return mock.Mock(returncode=1, stdout="", stderr="")
            if command == "status --short":
                return mock.Mock(returncode=0, stdout=" M README.md\n", stderr="")
            return mock.Mock(returncode=1, stdout="", stderr="")

        with mock.patch.object(preset, "run_git", side_effect=fake_git):
            provenance = preset.source_provenance(self.guru_root)

        self.assertEqual(provenance["tree_state"], "dirty")
        self.assertFalse(provenance["is_mutable_ref"])
        self.assertEqual(provenance["ref"], source_commit)
        self.assertEqual(provenance["commit"], source_commit)


if __name__ == "__main__":
    unittest.main()
