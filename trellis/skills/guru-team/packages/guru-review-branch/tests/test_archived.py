"""Deterministic wrapper fixtures, not evidence of an AI semantic review."""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import test_contract
from jsonschema import Draft202012Validator


class ArchivedContractTest(unittest.TestCase):
    def test_closed_examples_and_target_owned_projection(self):
        package = test_contract.PACKAGE
        interface = json.loads((package / "interface.json").read_text())
        skills = package.parents[1]
        Draft202012Validator(json.loads((skills / "schemas/skill-interface-1.4.schema.json").read_text())).validate(interface)
        for name in ("public-archived-review-input", "public-archived-review-passed-output"):
            schema = json.loads((package / "schemas" / (name + ".schema.json")).read_text())
            value = json.loads((package / "examples" / (name + ".json")).read_text())
            Draft202012Validator.check_schema(schema)
            Draft202012Validator(schema).validate(value)
            self.assertEqual(set(value), set(schema["required"]))
        output = json.loads((package / "examples/public-archived-review-passed-output.json").read_text())
        projection = next(p for p in interface["public_contracts"]["projections"] if p["exit_id"] == "archived_review_passed")
        projected = {m["target"]: output[m["source"]] for m in projection["mappings"]}
        target = package.parent / "guru-review-task-publication"
        target_interface = json.loads((target / "interface.json").read_text())
        profile = next(p for p in target_interface["public_contracts"]["input"]["profiles"] if p["id"] == "archived_publication_review")
        authored = json.loads((target / "examples/public-archived-publication-review-authoring.json").read_text())
        Draft202012Validator(json.loads((target / profile["schema"]["path"]).read_text())).validate({**projected, **authored})


class ArchivedReviewTest(unittest.TestCase):
    git = test_contract.BranchReviewWrapperLifecycleTest.git
    write = test_contract.BranchReviewWrapperLifecycleTest.write
    run_wrapper = test_contract.BranchReviewWrapperLifecycleTest.run_wrapper
    auth = test_contract.BranchReviewWrapperLifecycleTest.auth

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.parent = Path(self.tmp.name).resolve()
        self.repo = self.parent / "repo"
        self.inputs = self.parent / "inputs"
        self.inputs.mkdir()
        subprocess.run(["git", "init", "-q", "-b", "main", str(self.repo)], check=True)
        self.git("config", "user.name", "Test")
        self.git("config", "user.email", "test@example.invalid")
        (self.repo / ".gitignore").write_text(".trellis/.runtime/\n")
        (self.repo / "app.txt").write_text("base\n")
        self.git("add", ".")
        self.git("commit", "-qm", "base")
        self.base = self.git("rev-parse", "HEAD")
        self.git("switch", "-qc", "feat/archive")
        self.task_ref = ".trellis/tasks/archive/2026-09/09-16-example"
        archive = self.repo / self.task_ref
        archive.mkdir(parents=True)
        metadata = {"id": "example", "status": "completed", "branch": "feat/archive", "base_branch": "main"}
        summary = {
            "task": {"slug": archive.name, "status": "completed", "archive_dir": self.task_ref, "artifact_dir": ".trellis/tasks/09-16-example"},
            "git": {"branch": "feat/archive", "base_branch": "main", "commits": [self.base]},
            "github": {"pr_url": "https://github.com/example/repo/pull/12"},
        }
        (archive / "task.json").write_text(json.dumps(metadata))
        (archive / "finish-summary.json").write_text(json.dumps(summary))
        for name in ("prd.md", "design.md", "implement.md"):
            (archive / name).write_text("Archived planning\n")
        (self.repo / "app.txt").write_text("feature\n")
        if getattr(self, "config_text", None) is not None:
            config = self.repo / ".trellis/guru-team/config.yml"
            config.parent.mkdir(parents=True)
            config.write_text(self.config_text)
        self.git("add", ".")
        self.git("commit", "-qm", "completed archive fixture")
        self.head = self.git("rev-parse", "HEAD")
        self.git("update-ref", "refs/remotes/origin/main", self.base)
        remote = self.parent / "remote.git"
        subprocess.run(["git", "init", "--bare", "-q", str(remote)], check=True)
        self.git("remote", "add", "origin", "https://github.com/example/repo.git")
        self.git("config", f"url.{remote}.insteadOf", "https://github.com/example/repo.git")
        self.git("push", "-q", "origin", "feat/archive")
        # get-url expands insteadOf; expose the unchanged GitHub URL only for that read.
        self.bin = self.parent / "bin"
        self.bin.mkdir()
        import shutil
        real_git = shutil.which("git")
        (self.bin / "git").write_text(
            '#!/bin/sh\nif [ "$1 $2 $3" = "remote get-url origin" ]; then printf "%s\\n" "https://github.com/example/repo.git"; else exec '
            + str(real_git) + ' "$@"; fi\n'
        )
        (self.bin / "git").chmod(0o755)
        runtime = self.repo / ".trellis/.runtime/guru-team"
        mapping = {"schema_version": "1.0", "task_slug": "example", "workspace_slug": "example", "workspace_path": str(self.repo), "task_artifact_dir": self.task_ref}
        workspace = {"schema_version": "1.0", "workspace_slug": "example", "workspace_path": str(self.repo), "source_checkout": str(self.repo), "branch_name": "feat/archive"}
        for group, value in (("tasks", mapping), ("workspaces", workspace)):
            target = runtime / group / "example.json"
            target.parent.mkdir(parents=True)
            target.write_text(json.dumps(value))
        self.pr = {"number": 12, "url": "https://github.com/example/repo/pull/12", "state": "OPEN", "isDraft": False, "headRefName": "feat/archive", "baseRefName": "main", "headRefOid": self.head, "headRepository": {"nameWithOwner": "example/repo"}, "isCrossRepository": False, "title": "Current title", "body": "Current body\n"}
        self.provider_base = self.base
        self.provider_files()
        (self.bin / "gh").write_text(
            '#!/bin/sh\nprintf "%s\\n" "$*" >> "' + str(self.parent / "gh.log") + '"\n'
            'case "$1 $2" in\n'
            '  "auth status") exit 0;;\n'
            '  "api repos/example/repo") printf "%s\\n" \'{"full_name":"example/repo"}\';;\n'
            '  "api repos/example/repo/git/ref/heads/main") cat "' + str(self.inputs / "base.json") + '";;\n'
            '  "pr list") cat "' + str(self.inputs / "pr.json") + '";;\n'
            '  *) exit 1;;\nesac\n'
        )
        (self.bin / "gh").chmod(0o755)
        self.env = patch.dict(os.environ, {"PATH": str(self.bin) + os.pathsep + os.environ["PATH"]})
        self.env.start()
        self.public = {"profile": "archived_review", "mode": "workflow", "task_ref": self.task_ref, "branch_review_commit": self.head, "pr_payload_snapshot_sha256": self.snapshot()}
        self.public_file = self.write("public.json", self.public)

    def tearDown(self):
        self.env.stop()
        self.tmp.cleanup()

    def snapshot(self):
        value = {key: self.pr[key] for key in ("title", "body")}
        return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

    def provider_files(self):
        self.write("pr.json", [self.pr])
        self.write("base.json", {"ref": "refs/heads/main", "object": {"sha": self.provider_base, "type": "commit"}})

    def record(self, exit_id="archived_review_passed", semantic=None, ok=True):
        return self.run_wrapper("review-branch.sh", "--task", self.task_ref, "--skill-input", self.public_file, "--semantic-review-file", self.write("semantic.json", semantic or self.auth(exit_id)), "--typed-exit", exit_id, ok=ok)

    def check(self, ok=True):
        return self.run_wrapper("check-review-gate.sh", "--task", self.task_ref, ok=ok)

    def invoke(self, ok=True):
        return self.run_wrapper("invoke.sh", "--task", self.task_ref, "--input", self.public_file, ok=ok)

    def checkpoint(self):
        return self.repo / ".trellis/.runtime/guru-team/owner-checkpoints/09-16-example/review-gate.json"

    def test_record_check_project_retires_without_content_or_ref_mutation(self):
        before = self.git("show-ref")
        tree = self.git("rev-parse", "HEAD^{tree}")
        self.record()
        self.assertEqual("archived_review_passed", self.check()["typed_exit"])
        self.assertEqual({
            "exit_id": "archived_review_passed", "task_ref": self.task_ref,
            "branch_review_commit": self.head, "reviewed_base_head": self.base,
            "pr_payload_snapshot_sha256": self.snapshot(),
        }, self.invoke())
        self.assertFalse(self.checkpoint().exists())
        self.assertEqual(before, self.git("show-ref"))
        self.assertEqual(tree, self.git("rev-parse", "HEAD^{tree}"))
        self.assertEqual("", self.git("status", "--porcelain"))
        self.assertEqual("stale_identity", self.invoke(ok=False)["code"])

    def test_title_body_and_ready_state_drift_preserve_checkpoint(self):
        self.record()
        original = dict(self.pr)
        for key, value in (("title", "Revised title"), ("body", "Changed body"), ("isDraft", True), ("state", "CLOSED"), ("headRefOid", self.base)):
            with self.subTest(key=key):
                self.pr = {**original, key: value}
                self.provider_files()
                self.assertEqual("stale_identity", self.check(ok=False)["code"])
                self.assertTrue(self.checkpoint().exists())

    def test_live_or_local_base_advance_invalidates_review(self):
        self.record()
        self.provider_base = self.head
        self.provider_files()
        self.assertEqual("reviewed_base_head", self.check(ok=False)["field_path"])
        self.git("update-ref", "refs/remotes/origin/main", self.head)
        self.assertEqual("archived_review", self.check(ok=False)["field_path"])

    def test_dirty_archived_metadata_is_not_excluded(self):
        self.record()
        (self.repo / self.task_ref / "prd.md").write_text("Changed scope\n")
        self.assertEqual("worktree", self.check(ok=False)["field_path"])

    def test_open_finding_remains_truthful_blocked_and_retires(self):
        semantic = self.auth("blocked")
        semantic["semantic_review"]["qualified_findings"] = [{
            "candidate_ref": "candidate-no-defect", "disposition": "qualified_finding",
            "affected_behavior": "Current documented behavior is absent.", "path": "app.txt",
            "evidence_refs": ["diff:app.txt"], "finding_ref": "finding:missing-behavior",
            "severity": "P2", "introduced_head": self.head, "fix_head": None,
            "closure_head": None, "status": "open", "closure_evidence": [],
        }]
        semantic["candidate_classifications"][0]["decision"] = "qualified_current"
        self.record("blocked", semantic)
        self.assertEqual("open", json.loads(self.checkpoint().read_text())["semantic_review"]["qualified_findings"][0]["status"])
        self.assertEqual({"exit_id": "blocked"}, self.invoke())
        self.assertFalse(self.checkpoint().exists())

    def test_archived_profile_rejects_task_work_route(self):
        self.assertEqual("schema_mismatch", self.record("implementation_required", ok=False)["code"])
        self.assertFalse(self.checkpoint().exists())

    def test_standalone_uses_same_readonly_entry_and_retirement(self):
        self.public["mode"] = "standalone"
        self.write("public.json", self.public)
        self.record()
        self.assertEqual("archived_review_passed", self.invoke()["exit_id"])
        self.assertFalse(self.checkpoint().exists())


class ArchivedConfigDefaultsTest(unittest.TestCase):
    def test_empty_runtime_root_and_publish_remote_preserve_readonly_state(self):
        for empty in ('""', "''", ""):
            with self.subTest(empty=empty):
                fixture = ArchivedReviewTest()
                fixture.config_text = f"runtime_root: {empty}\npublish:\n  remote: {empty}\n"
                fixture.setUp()
                try:
                    paths = [
                        fixture.repo / ".trellis/guru-team/config.yml",
                        fixture.repo / ".trellis/.runtime/guru-team/tasks/example.json",
                        fixture.repo / ".trellis/.runtime/guru-team/workspaces/example.json",
                        fixture.inputs / "pr.json",
                        *sorted((fixture.repo / fixture.task_ref).iterdir()),
                    ]
                    before = {path: path.read_bytes() for path in paths}
                    remote_refs = fixture.git("ls-remote", "--heads", "origin")
                    fixture.test_record_check_project_retires_without_content_or_ref_mutation()
                    self.assertEqual(before, {path: path.read_bytes() for path in paths})
                    self.assertEqual(remote_refs, fixture.git("ls-remote", "--heads", "origin"))
                finally:
                    fixture.tearDown()


if __name__ == "__main__":
    unittest.main()
