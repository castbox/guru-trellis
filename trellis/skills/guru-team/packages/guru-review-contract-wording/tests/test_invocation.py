from __future__ import annotations

import copy
import hashlib
import json
import os
import subprocess
import tempfile
import sys
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE.parent / "guru-create-delivery/tests"))
from support import installed_fixture
sys.path.insert(0, str(PACKAGE.parents[1]))
from runtime.io import CommandError, project_intermediate_receipt
DIMENSIONS = (
    "complete_profile_scope", "all_hits_classified", "zero_unchecked_hits",
    "product_semantics_preserved", "retained_reasons_sufficient",
    "zero_hits_not_requirement_review",
)
PLANNING = (
    "no_requirement_weakening", "source_issue_semantics_preserved",
    "conditional_paths_have_conditions", "no_parallel_implementation_paths",
    "gates_have_machine_verifiable_conditions",
    "acceptance_criteria_are_deterministic", "external_quotes_are_labeled_non_contract",
)


class SingleReadDispatcherTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.envelope = json.loads((PACKAGE / "examples/review-scan-invocation.json").read_text())
        self.envelope["change_request"]["body"] = "Term definition: 建议."

    def tearDown(self):
        self.tmp.cleanup()

    def command(self, name, value=None, args=(), expected=0):
        proc = subprocess.run(
            [str(PACKAGE / "scripts" / name), "--root", str(self.root), *args],
            input=json.dumps(value, ensure_ascii=False) if value is not None else "",
            text=True, capture_output=True,
        )
        self.assertEqual(expected, proc.returncode, proc.stdout + proc.stderr)
        payload = json.loads(proc.stdout)
        if expected == 0 and name != "invoke.sh":
            return project_intermediate_receipt(payload, PACKAGE.parents[1] / "schemas")
        return payload

    def envelope_command(self, name, value, *args, expected=0):
        return self.command(name, value, ("--invocation", "-", *args), expected)

    def author(self, scan, exit_id="pass"):
        return {
            "generated_at": "2026-09-09T00:00:00Z", "revisions": [],
            "classifications": [
                {"hit_id": hit["hit_id"], "classification": "term_definition",
                 "reason": "The sentence defines the literal term, not an operative requirement."}
                for hit in scan["scan"]["hits"]
            ],
            "ai_review_gate": {
                "status": "blocked" if exit_id == "blocked" else "passed",
                "reviewer": "dispatcher-test", "summary": "Complete fixed scope reviewed.",
                "reviewed_scan_sha256": scan["scan"]["scan_sha256"],
                "checked_dimensions": {name: exit_id != "blocked" for name in DIMENSIONS},
            },
            "typed_exit": exit_id,
        }

    def recorded(self, exit_id="pass"):
        scan = self.envelope_command("record-contract-wording-review.sh", self.envelope, "--scan-only")
        env = copy.deepcopy(self.envelope)
        env["owner_result"] = self.author(scan, exit_id)
        if exit_id == "content_changed":
            env["owner_result"]["revisions"] = [{
                "revision_id": "draft-body-revision", "locator": "body:draft-wording-example",
                "before_sha256": hashlib.sha256(b"Previous draft body").hexdigest(),
                "after_sha256": hashlib.sha256(env["change_request"]["body"].encode()).hexdigest(),
                "reason": "Replaced the draft body with an explicit term definition.",
                "rescan_sha256": scan["scan"]["scan_sha256"],
            }]
        env["owner_result"] = self.envelope_command("record-contract-wording-review.sh", env)
        return env

    def test_complete_chain_is_fileless_and_checker_receipt_is_real(self):
        before = sorted(self.root.rglob("*"))
        for exit_id in ("pass", "blocked", "content_changed"):
            env = self.recorded(exit_id)
            checked = self.envelope_command("check-contract-wording-review.sh", env)
            transition = json.loads((PACKAGE / "examples/public-pass-output-2.0.json").read_text())["transition"]
            transition.update(stage="clarity_current", transition_id="clarity_current:" + "3" * 24)
            for key in ("wording", "wording_facts_sha256", "target_content_sha256"):
                transition.pop(key, None)
            public = json.loads((PACKAGE / "examples/public-change-request-input.json").read_text())
            public["continuation_id"] = transition["continuation_id"]
            output = self.envelope_command("invoke.sh", {
                "public_input": public, "transition": transition,
                "owner_result": env["owner_result"],
                "validation_receipt": checked["validation_receipt"],
            })
            self.assertEqual(exit_id, output["exit_id"])
            if exit_id == "pass":
                self.assertEqual("wording_current", output["transition"]["stage"])
        self.assertEqual(before, sorted(self.root.rglob("*")))

    def test_envelope_and_normal_input_errors(self):
        for flag, value in (("--input", "-"), ("--mode", "workflow"),
                            ("--profile", "change_request"), ("--task", "task"),
                            ("--path", "file.md"), ("--change-request-input", "source.json")):
            error = self.envelope_command("record-contract-wording-review.sh", self.envelope,
                                          flag, value, expected=2)
            self.assertEqual("conflicting_arguments", error["code"])
        for field in self.envelope:
            env = copy.deepcopy(self.envelope)
            del env[field]
            self.assertEqual("schema_mismatch", self.envelope_command(
                "record-contract-wording-review.sh", env, "--scan-only", expected=2)["code"])
        for extra in ({"extra": True}, {"owner_result": {"typed_exit": "pass"}}):
            env = dict(self.envelope, **extra)
            self.envelope_command("record-contract-wording-review.sh", env, "--scan-only", expected=2)
        scan = self.envelope_command("record-contract-wording-review.sh", self.envelope, "--scan-only")
        env = copy.deepcopy(self.envelope)
        env["owner_result"] = self.author(scan)
        env["owner_result"]["classifications"] = []
        self.envelope_command("record-contract-wording-review.sh", env, expected=2)
        env = self.recorded()
        env["mode"] = "standalone"
        self.assertEqual("stale_identity", self.envelope_command(
            "check-contract-wording-review.sh", env, expected=3)["code"])
        env = self.recorded()
        env["change_request"]["body"] += " Current update."
        self.assertEqual("stale_identity", self.envelope_command(
            "check-contract-wording-review.sh", env, expected=3)["code"])

    def test_legacy_change_request_files_and_double_stdin_migration(self):
        source = self.root / "source.json"
        source.write_text(json.dumps(self.envelope["change_request"]))
        args = ("--profile", "change_request", "--mode", "workflow", "--change-request-input", str(source))
        scan = self.command("record-contract-wording-review.sh", args=(*args, "--scan-only"))
        authored = self.root / "author.json"
        authored.write_text(json.dumps(self.author(scan)))
        owner = self.command("record-contract-wording-review.sh", args=(*args, "--input", str(authored)))
        result = self.root / "result.json"
        result.write_text(json.dumps(owner))
        self.command("check-contract-wording-review.sh", args=("--input", str(result), "--change-request-input", str(source)))
        error = self.command("record-contract-wording-review.sh", self.envelope["change_request"],
                             ("--mode", "workflow", "--profile", "change_request", "--input", "-", "--change-request-input", "-"), 2)
        self.assertEqual("conflicting_arguments", error["code"])

    def test_original_markdown_profiles_keep_fixed_scopes(self):
        (self.root / "contract.md").write_text("Exact contract.\n")
        args = ("--profile", "explicit_paths", "--mode", "standalone", "--path", "contract.md")
        scan = self.command("record-contract-wording-review.sh", args=(*args, "--scan-only"))
        owner = self.command("record-contract-wording-review.sh", self.author(scan), (*args, "--input", "-"))
        self.command("check-contract-wording-review.sh", owner, ("--path", "contract.md", "--input", "-"))
        (self.root / "contract.md").write_text("Updated contract.\n")
        self.command("check-contract-wording-review.sh", owner, ("--path", "contract.md", "--input", "-"), expected=3)

    def test_delivery_markdown_scope_uses_installed_locator_and_exact_key(self):
        fixture = installed_fixture(self)
        self.root = fixture.root.resolve()
        key = fixture.create()
        directory = fixture.projection.planning_directory(key)
        for name in ("prd.md", "design.md", "implement.md"):
            (directory / name).write_text("Exact contract.\n")
        selectors = ("--task", fixture.task_ref, "--delivery-key", json.dumps(key))
        args = ("--profile", "delivery_planning_artifacts", "--mode", "workflow", *selectors)
        scan = self.command("record-contract-wording-review.sh", args=(*args, "--scan-only"))
        self.assertEqual({item["path"] for item in scan["scope"]["items"]},
                         {(directory / name).relative_to(self.root.resolve()).as_posix() for name in ("prd.md", "design.md", "implement.md")})
        auth = self.author(scan)
        auth["ai_review_gate"]["planning_checked_dimensions"] = {name: True for name in PLANNING}
        owner = self.command("record-contract-wording-review.sh", auth, (*args, "--input", "-"))
        checked = self.command("check-contract-wording-review.sh", owner, (*selectors, "--input", "-"))
        public = json.loads((PACKAGE / "examples/public-delivery-planning-artifacts-input.json").read_text())
        public.update(task_ref=fixture.task_ref, delivery_key=key)
        output = self.envelope_command("invoke.sh", {"public_input": public, "owner_result": owner,
                                                       "validation_receipt": checked["validation_receipt"]})
        self.assertEqual(output["delivery_key"], key)
        self.assertEqual(output["exit_id"], "pass")
        self.assertEqual((fixture.task / "prd.md").read_text(), "整体scope\n")
        before = fixture.projection.resolve(key)
        (directory / "implement.md").write_text("Updated plan obligation.\n")
        self.command("check-contract-wording-review.sh", owner, (*selectors, "--input", "-"), expected=3)
        self.envelope_command("invoke.sh", {"public_input": public, "owner_result": owner,
                                            "validation_receipt": checked["validation_receipt"]}, expected=3)
        self.assertEqual(fixture.projection.resolve(key), before)

    def changed_markdown(self, profile):
        task_ref = ".trellis/tasks/wording-reentry"
        folder = self.root / task_ref if profile == "planning_artifacts" else self.root
        folder.mkdir(parents=True, exist_ok=True)
        files = ("prd.md", "design.md", "implement.md") if profile == "planning_artifacts" else ("contract.md",)
        for name in files:
            (folder / name).write_text("Original contract.\n")
        changed = folder / files[-1]
        before = hashlib.sha256(changed.read_bytes()).hexdigest()
        changed.write_text("Current contract.\n")
        mode = "workflow" if profile == "planning_artifacts" else "standalone"
        selectors = ("--task", task_ref) if profile == "planning_artifacts" else ("--path", "contract.md")
        args = ("--profile", profile, "--mode", mode, *selectors)
        scan = self.command("record-contract-wording-review.sh", args=(*args, "--scan-only"))
        auth = self.author(scan, "content_changed")
        locator = changed.relative_to(self.root).as_posix()
        auth["revisions"] = [{
            "revision_id": "current-wording-revision", "locator": locator,
            "before_sha256": before, "after_sha256": hashlib.sha256(changed.read_bytes()).hexdigest(),
            "reason": "Equivalent wording clarification completed in this invocation.",
            "rescan_sha256": scan["scan"]["scan_sha256"],
        }]
        if profile == "planning_artifacts":
            auth["ai_review_gate"]["planning_checked_dimensions"] = dict.fromkeys(PLANNING, True)
        owner = self.command("record-contract-wording-review.sh", auth, (*args, "--input", "-"))
        checked = self.command("check-contract-wording-review.sh", owner, (*selectors, "--input", "-"))
        public = json.loads((PACKAGE / ("examples/public-planning-artifacts-input.json" if profile == "planning_artifacts" else "examples/public-explicit-paths-input.json")).read_text())
        if profile == "planning_artifacts":
            public["task_locator"] = task_ref
        else:
            public["paths"] = ["contract.md"]
        invocation = {"public_input": public, "owner_result": owner,
                      "validation_receipt": checked["validation_receipt"]}
        return self.envelope_command("invoke.sh", invocation), locator

    def test_real_changed_planning_stdout_validates_author_reentry_without_private_reads(self):
        from runtime.schema import validate_json
        fixture = installed_fixture(self)
        self.root = fixture.root.resolve()
        key = fixture.create()
        folder = fixture.projection.planning_directory(key)
        for name in ("prd.md", "design.md", "implement.md"):
            (folder / name).write_text("Original contract.\n")
        changed = folder / "design.md"
        before = hashlib.sha256(changed.read_bytes()).hexdigest()
        changed.write_text("Current equivalent contract.\n")
        selectors = ("--task", fixture.task_ref, "--delivery-key", json.dumps(key))
        args = ("--profile", "delivery_planning_artifacts", "--mode", "workflow", *selectors)
        scan = self.command("record-contract-wording-review.sh", args=(*args, "--scan-only"))
        auth = self.author(scan, "content_changed")
        locator = changed.relative_to(self.root).as_posix()
        auth["revisions"] = [{"revision_id": "current-wording-revision", "locator": locator,
            "before_sha256": before, "after_sha256": hashlib.sha256(changed.read_bytes()).hexdigest(),
            "reason": "Equivalent wording clarified.", "rescan_sha256": scan["scan"]["scan_sha256"]}]
        auth["ai_review_gate"]["planning_checked_dimensions"] = dict.fromkeys(PLANNING, True)
        owner = self.command("record-contract-wording-review.sh", auth, (*args, "--input", "-"))
        checked = self.command("check-contract-wording-review.sh", owner, (*selectors, "--input", "-"))
        public = json.loads((PACKAGE / "examples/public-delivery-planning-artifacts-input.json").read_text())
        public.update(task_ref=fixture.task_ref, delivery_key=key)
        output = self.envelope_command("invoke.sh", {"public_input": public, "owner_result": owner,
                                                   "validation_receipt": checked["validation_receipt"]})
        author_input = {"profile": "delivery_wording_reentry", "mode": "workflow",
                        **{name: output[name] for name in ("task_ref", "delivery_key", "change_refs")}}
        validate_json(author_input, PACKAGE.parent / "guru-author-task-plan/schemas/public-delivery-wording-reentry-input.schema.json", "author_input")
        self.assertEqual([locator], author_input["change_refs"])
        self.assertEqual({"exit_id", "profile", "task_ref", "delivery_key", "change_refs"}, set(output))

    def test_changed_explicit_paths_preserves_nonplanning_output(self):
        output, _ = self.changed_markdown("explicit_paths")
        self.assertEqual({"exit_id", "profile", "continuation_id"}, set(output))
        self.assertEqual("explicit_paths", output["profile"])
        self.assertEqual("content_changed", output["exit_id"])

    def test_source_metadata_keeps_legacy_scan_behavior(self):
        for comments in ([], [{"id": "comment-1", "body": "Existing source metadata"}]):
            env = copy.deepcopy(self.envelope)
            env["change_request"]["selected_comments"] = comments
            source = self.root / "source.json"
            source.write_text(json.dumps(env["change_request"]))
            legacy = self.command("record-contract-wording-review.sh", args=(
                "--profile", "change_request", "--mode", "workflow",
                "--change-request-input", str(source), "--scan-only"))
            current = self.envelope_command("record-contract-wording-review.sh", env, "--scan-only")
            self.assertEqual(legacy, current)

    def test_scan_example_matches_declared_schema(self):
        from jsonschema import Draft202012Validator
        schema = json.loads((PACKAGE / "schemas/change-request-review-invocation.schema.json").read_text())
        example = json.loads((PACKAGE / "examples/review-scan-invocation.json").read_text())
        self.assertEqual([], list(Draft202012Validator(schema).iter_errors(example)))
        self.envelope_command("record-contract-wording-review.sh", example, "--scan-only")

    def test_checker_mixed_malformed_and_digest_inputs(self):
        env = self.recorded()
        for flag, value in (("--input", "-"), ("--task", "."),
                            ("--path", "contract.md"), ("--change-request-input", "-")):
            self.assertEqual("conflicting_arguments", self.envelope_command(
                "check-contract-wording-review.sh", env, flag, value, expected=2)["code"])
        for name in ("record-contract-wording-review.sh", "check-contract-wording-review.sh"):
            proc = subprocess.run([str(PACKAGE / "scripts" / name), "--root", str(self.root),
                                   "--invocation", "-"], input="{", text=True, capture_output=True)
            self.assertEqual(2, proc.returncode, proc.stderr)
            self.assertEqual("invalid_json", json.loads(proc.stdout)["code"])
            for value in ([], {**env, "unexpected": True}):
                self.envelope_command(name, value, expected=2)
        self.envelope_command("check-contract-wording-review.sh", env,
                              "--expected-facts-sha256", env["owner_result"]["facts_sha256"])
        self.assertEqual("stale_identity", self.envelope_command(
            "check-contract-wording-review.sh", env, "--expected-facts-sha256", "0" * 64, expected=3)["code"])
        env["owner_result"] = {}
        self.envelope_command("check-contract-wording-review.sh", env, expected=2)

    def test_issue_checker_really_rereads_authority(self):
        # Only GitHub transport is stubbed; every owner command uses its real dispatcher.
        from unittest import mock
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            gh = fixture / "gh"
            gh.write_text("#!/bin/sh\ncat \"$WORDING_LIVE_ISSUE\"\n")
            gh.chmod(0o755)
            self.envelope["change_request"].update(
                source_kind="issue", identity="https://github.com/example/repo/issues/388",
                updated_at="2026-09-09T00:00:00Z")
            source = self.envelope["change_request"]
            live = {"number": 388, "url": source["identity"], "state": "OPEN",
                    "title": source["title"], "body": source["body"], "updatedAt": source["updated_at"]}
            live_path = fixture / "live.json"
            live_path.write_text(json.dumps(live))
            with mock.patch.dict(os.environ, {"PATH": str(fixture) + os.pathsep + os.environ["PATH"],
                                              "WORDING_LIVE_ISSUE": str(live_path)}):
                env = self.recorded()
                checked = self.envelope_command("check-contract-wording-review.sh", env)
                self.assertEqual("passed", checked["status"])
                live["body"] = "Actual updated source"
                live_path.write_text(json.dumps(live))
                self.assertEqual("stale_identity", self.envelope_command(
                    "check-contract-wording-review.sh", env, expected=3)["code"])


if __name__ == "__main__":
    unittest.main()
