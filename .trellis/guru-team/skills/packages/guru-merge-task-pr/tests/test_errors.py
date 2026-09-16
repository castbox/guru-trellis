from __future__ import annotations

import ast
import contextlib
import hashlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE.parents[1]))
from runtime import command

spec = importlib.util.spec_from_file_location("merge_errors_owner", PACKAGE / "runtime/owner.py")
assert spec and spec.loader
OWNER = importlib.util.module_from_spec(spec)
spec.loader.exec_module(OWNER)


class MergeErrorWrapperTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        checkout = next(parent for parent in PACKAGE.parents if (parent / ".git").exists())
        cls.pointers = {}
        for flag in ("--git-common-dir", "--absolute-git-dir"):
            result = subprocess.run(
                ["git", "rev-parse", "--path-format=absolute", flag],
                cwd=checkout, text=True, capture_output=True, check=True,
            )
            path = Path(result.stdout.strip()) / "guru-team/python/active.json"
            cls.pointers[path] = path.read_bytes() if path.exists() else None

    @classmethod
    def tearDownClass(cls) -> None:
        for path, before in cls.pointers.items():
            after = path.read_bytes() if path.exists() else None
            if before != after:
                raise AssertionError("Wrapper tests changed the checkout managed-runtime pointer.")

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / ".trellis").mkdir()
        self.bin = self.root / "bin"
        self.bin.mkdir()
        self.log = self.root / "calls"
        self.env = {
            **os.environ, "PATH": str(self.bin) + os.pathsep + os.environ["PATH"],
            "MERGE_FIXTURE": str(self.root), "MERGE_FAILURE": "",
        }
        self.env.pop("GURU_TEAM_PYTHON_CACHE_ROOT", None)
        gh = self.bin / "gh"
        gh.write_text('''#!/bin/sh
set -eu
printf '%s %s\n' "$1" "${2:-}" >> "$MERGE_FIXTURE/calls"
case "$1 ${2:-}" in
  "auth status")
    if [ "$MERGE_FAILURE" = auth ]; then
      printf '%s\n' 'authentication unavailable fixture-private-value' >&2
      exit 1
    fi
    exit 0 ;;
  "pr merge")
    printf '%s\n' 'HTTP 403 permission denied fixture-private-value' >&2
    exit 1 ;;
esac
case "$MERGE_FAILURE" in
  repo) printf '%s\n' 'Could not resolve to a Repository fixture-private-value' >&2; exit 1 ;;
  permission) printf '%s\n' 'HTTP 403 forbidden fixture-private-value' >&2; exit 1 ;;
  api) printf '%s\n' 'HTTP 503 unavailable fixture-private-value' >&2; exit 1 ;;
  response) printf '%s\n' 'incomplete fixture-private-value'; exit 0 ;;
esac
case "$1 ${2:-}" in
  "pr view") cat "$MERGE_FIXTURE/pr.json" ;;
  "api repos/example/repo") cat "$MERGE_FIXTURE/policy.json" ;;
  "api repos/example/repo/git/ref/heads/main") cat "$MERGE_FIXTURE/base.json" ;;
  *) exit 99 ;;
esac
''', encoding="utf-8")
        gh.chmod(0o755)
        self.public = {
            "schema_version": "2.0", "profile": "ready_for_merge", "mode": "workflow",
            "repo_ref": "example/repo", "pr_number": 418,
            "pr_url": "https://github.com/example/repo/pull/418",
            "expected_head_sha": "1" * 40,
            "expected_base_branch": "main", "expected_head_branch": "fix/418",
            "publication_body_sha256": hashlib.sha256(b"Refs #418\n").hexdigest(),
            "reviewed_merge_message": OWNER.build_reviewed_merge_message(
                pull_request=418, summary="\u4fee\u590d Merge \u8bca\u65ad",
                head_branch="fix/418", base_branch="main",
            ),
        }
        self.pr = {
            "number": 418, "url": self.public["pr_url"], "state": "OPEN", "isDraft": False,
            "baseRefName": "main", "headRefName": "fix/418", "headRefOid": "1" * 40,
            "mergeable": "MERGEABLE", "mergeStateStatus": "CLEAN",
            "reviewDecision": "APPROVED", "statusCheckRollup": [], "body": "Refs #418\n",
            "mergedAt": None, "mergeCommit": None,
        }
        self.write("pr.json", self.pr)
        self.write("policy.json", {
            "full_name": "example/repo", "allow_merge_commit": True,
            "allow_squash_merge": False, "allow_rebase_merge": False,
        })
        self.write("base.json", {"ref": "refs/heads/main", "object": {"sha": "2" * 40}})
        self.input = self.write("input.json", self.public)
        self.review = self.write("review.json", {
            "semantic_review": {"dimensions": [
                {"id": name, "status": "passed", "summary": "Current fixture dimension reviewed."}
                for name in OWNER.TASK_PR_MERGE_DIMENSIONS
            ]},
            "route": {"typed_exit": "merged", "merge_method": "merge"},
        })

    def write(self, name: str, payload: dict) -> Path:
        path = self.root / name
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def wrapper(self, operation: str, *, input_path: Path | None = None) -> tuple[subprocess.CompletedProcess, dict]:
        name = "invoke.sh" if operation == "invoke" else f"{operation}-task-pr-merge.sh"
        argv = [str(PACKAGE / "scripts" / name), "--root", str(self.root),
                "--input", str(input_path or self.input), "--json"]
        if operation in {"record", "invoke"}:
            argv += ["--review-input", str(self.review)]
        proc = subprocess.run(argv, text=True, capture_output=True, env=self.env, check=False)
        self.assertNotIn("fixture-private-value", proc.stdout + proc.stderr)
        self.assertNotIn("Traceback", proc.stdout + proc.stderr)
        self.assertEqual(proc.stderr, "")
        return proc, json.loads(proc.stdout)

    def assert_error(self, operation: str, code: str, field: str, **kwargs) -> dict:
        proc, payload = self.wrapper(operation, **kwargs)
        self.assertEqual(proc.returncode, 2, proc.stdout)
        self.assertEqual(set(payload), {"code", "field_path", "remediation"})
        self.assertEqual(payload["code"], code)
        self.assertEqual(payload["field_path"], field)
        self.assertTrue(payload["remediation"])
        return payload

    def record_current_gate(self) -> Path:
        proc, payload = self.wrapper("record")
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertEqual(payload["status"], "recorded")
        return self.root / payload["gate"]

    def test_missing_current_input_all_original_wrappers(self) -> None:
        for operation in ("preview", "record", "check", "execute", "invoke"):
            with self.subTest(operation=operation):
                self.assert_error(operation, "invalid_arguments", "input", input_path=self.root / "missing.json")
        self.assertFalse(self.log.exists())
        self.assertEqual(list((self.root / ".trellis").iterdir()), [])

    def test_invalid_json_and_identity_are_diagnostic_without_echoing_input(self) -> None:
        self.input.write_text('{"body":"fixture-private-value"', encoding="utf-8")
        self.assert_error("preview", "invalid_arguments", "input")
        self.write("input.json", {**self.public, "pr_url": "https://github.com/example/repo/pull/419"})
        self.assert_error("preview", "invalid_arguments", "pr_url")
        self.assertFalse(self.log.exists())

    def test_provider_errors_keep_codes_in_preview_record_and_invoke(self) -> None:
        cases = [
            ("auth", "github_auth_failed", "github.auth"),
            ("repo", "github_repo_access_denied", "github.repo_access_denied"),
            ("permission", "github_permission_denied", "github.permission_denied"),
            ("api", "github_api_unavailable", "github.api_unavailable"),
            ("response", "github_response_incomplete", "github.response"),
        ]
        for failure, code, field in cases:
            self.env["MERGE_FAILURE"] = failure
            for operation in ("preview", "record", "invoke"):
                with self.subTest(failure=failure, operation=operation):
                    self.assert_error(operation, code, field)

    def test_provider_errors_propagate_through_checked_gate(self) -> None:
        self.record_current_gate()
        self.env["MERGE_FAILURE"] = "api"
        for operation in ("check", "execute", "invoke"):
            with self.subTest(operation=operation):
                self.assert_error(operation, "github_api_unavailable", "github.api_unavailable")
        self.assertNotIn("pr merge", self.log.read_text())

    def test_normal_head_advance_makes_produced_gate_explicitly_stale(self) -> None:
        self.record_current_gate()
        self.write("pr.json", {**self.pr, "headRefOid": "3" * 40})
        for operation in ("check", "execute", "invoke"):
            with self.subTest(operation=operation):
                self.assert_error(operation, "stale_identity", "gate.facts_sha256")
        self.assertNotIn("pr merge", self.log.read_text())

    def test_missing_merge_gate_does_not_request_branch_review_checkpoint(self) -> None:
        for operation in ("check", "execute"):
            error = self.assert_error(operation, "stale_identity", "gate")
            self.assertIn("Merge semantic review", error["remediation"])
            self.assertNotIn("Branch Review", error["remediation"])
        self.assertFalse(self.log.exists())

    def test_ready_preview_and_current_gate_need_no_branch_review_checkpoint(self) -> None:
        self.assertEqual(list((self.root / ".trellis").iterdir()), [])
        proc, preview = self.wrapper("preview")
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertEqual(preview["objective_blockers"], [])
        self.record_current_gate()
        proc, checked = self.wrapper("check")
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertEqual(checked["typed_exit"], "ready_to_merge")
        self.assertFalse(list((self.root / ".trellis").rglob("review-gate.json")))

    def test_publication_body_change_has_owner_specific_recovery(self) -> None:
        self.write("pr.json", {**self.pr, "body": "Updated ordinary PR description."})
        error = self.assert_error("preview", "stale_identity", "publication_body_sha256")
        self.assertIn("Publication owner", error["remediation"])
        self.assertNotIn("pr merge", self.log.read_text())

    def test_execute_provider_failure_retires_body_file(self) -> None:
        gate = self.record_current_gate()
        self.assert_error("execute", "github_permission_denied", "github.permission_denied")
        self.assertTrue(gate.exists())
        self.assertEqual(self.log.read_text().splitlines().count("pr merge"), 1)
        self.assertFalse(list((self.root / ".trellis").rglob("merge-body.md")))

    def test_all_known_errors_have_source_authored_fields(self) -> None:
        tree = ast.parse((PACKAGE / "runtime/owner.py").read_text())
        calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call)
                 and isinstance(node.func, ast.Name) and node.func.id == "WorkflowError"]
        self.assertTrue(calls)
        for node in calls:
            fields = {item.arg for item in node.keywords}
            self.assertTrue({"code", "field_path"} <= fields, f"line {node.lineno}")
            if not isinstance(node.args[0], ast.Constant):
                self.assertIn("remediation", fields, f"Dynamic diagnostic at line {node.lineno}")

    def test_missing_cli_preserves_provider_code(self) -> None:
        with mock.patch.object(OWNER.shutil, "which", return_value=None):
            with self.assertRaises(OWNER.WorkflowError) as raised:
                OWNER.require_gh_auth(self.root)
        self.assertEqual(raised.exception.code, "github_cli_missing")
        self.assertEqual(raised.exception.field_path, "github.cli")

    def test_unexpected_bug_still_uses_dispatcher_generic_fallback(self) -> None:
        output = io.StringIO()
        with mock.patch.object(command, "_load_entrypoint", side_effect=RuntimeError("fixture-private-value")):
            with contextlib.redirect_stdout(output):
                status = command.main(PACKAGE, ["preview-task-pr-merge", "--input", str(self.input)])
        self.assertEqual(status, 2)
        self.assertEqual(json.loads(output.getvalue()), {
            "code": "internal_error", "field_path": "runtime",
            "remediation": "Inspect the package runtime and retry.",
        })


if __name__ == "__main__":
    unittest.main()
