"""Real legacy root blobs relocate without forcing a duplicate commit."""
import base64
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
SKILLS = PACKAGE.parents[1]
sys.path.insert(0, str(SKILLS))
from runtime.delivery_projection.adapter import DeliveryProjection, authority_ref
from runtime.task_lifecycle import BranchBindingStore, TaskLifecycleKey, inspect_repository
from runtime.delivery_projection.tests.upstream_fixture import public_task


class SourceMigrationTests(unittest.TestCase):
    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.repo, capture_output=True, text=True, check=True).stdout.strip()

    def write(self, name, value):
        path = self.repo / ".trellis/.runtime/inputs" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value))
        return str(path)

    def wrapper(self, skill, wrapper, *args, success=True):
        r = subprocess.run(["bash", str(SKILLS / "packages" / skill / "scripts" / wrapper), "--root", str(self.repo), *args], capture_output=True, text=True)
        value = json.loads(r.stdout or r.stderr)
        self.assertEqual(success, r.returncode == 0, value)
        return value.get("result", value)

    def setUp(self):
        source = os.environ.get("TRELLIS_DELIVERY_API_COMMON")
        if not source:
            self.skipTest("Set the fixed installed candidate common path.")
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.repo = Path(temporary.name).resolve()
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.name", "Migration Test")
        self.git("config", "user.email", "migration@example.invalid")
        shutil.copytree(source, self.repo / ".trellis/scripts/common", ignore=shutil.ignore_patterns("__pycache__"))
        (self.repo / ".gitignore").write_text(".trellis/.runtime/\n")
        (self.repo / "app.txt").write_text("base\n")
        self.task_ref = ".trellis/tasks/source-task"
        task = self.repo / self.task_ref
        task.mkdir(parents=True)
        self.key = {"task_id": "source-task", "lifecycle_generation": 0, "delivery_id": "c13a62ec-4ce7-4406-ab7c-fa1537a07658"}
        metadata = public_task({"id": "source-task"})
        legacy = {k: v for k, v in metadata.items() if k not in {"accepted_scope", "deliveries", "completion_results", "closure_results"}}
        legacy.update(schema_version="1.0", status="in_progress")
        (task / "task.json").write_text(json.dumps(legacy))
        self.names = ("prd.md", "design.md", "implement.md", "implement.jsonl", "check.jsonl")
        (self.repo / "docs").mkdir()
        (self.repo / "docs/requirements.md").write_text("R1: actual target\n")
        for name in self.names:
            (task / name).write_text("R1: original plan [requirements](../../../docs/requirements.md#R1)\n" if name.endswith(".md") else "")
        owners = {role: "guru-test-" + role for role in ("task_scope", "creation", "planning", "implementation", "check", "full_review", "readiness", "publication", "delivery", "completion", "closure")}
        owners["implementation"] = "guru-delivery-implementation-projection"
        (self.repo / ".trellis/workflow.md").write_text("[trellis-runtime-contract]\n" + json.dumps({"task_schema": "2.0", "delivery_api": "1.0", "profiles": ["local_commit"], "owners": owners}) + "\n[/trellis-runtime-contract]\n")
        self.git("add", ".")
        self.git("commit", "-qm", "legacy base")
        self.git("switch", "-qc", "feature/source")
        (self.repo / "app.txt").write_text("feature\n")
        self.git("commit", "-qam", "original committed candidate")
        self.head = self.git("rev-parse", "HEAD")
        metadata["accepted_scope"] = authority_ref(task / "prd.md", self.repo)
        (task / "task.json").write_text(json.dumps(metadata))
        self.projection = DeliveryProjection(self.repo, self.task_ref)
        self.projection.apply({"api_version": "1.0", "operation": "create_delivery", "key": self.key, "owner_role": "creation", "owner_id": owners["creation"], "scope_ref": {"authority": metadata["accepted_scope"], "anchors": ["R1"]}, "profile": "local_commit"})
        planning = self.projection.planning_directory(self.key)
        planning.mkdir(parents=True, exist_ok=True)
        files = []
        for name in self.names:
            shutil.copy2(task / name, planning / name)
            files.append({"target": {"kind": "project", "workspace": "current", "path": (planning / name).relative_to(self.repo).as_posix()}, "owner": "artifact", "action": "write", "target_content_base64": base64.b64encode((task / name).read_bytes()).decode(), "target_mode": 0o644})
        self.plan = {"schema_version": "2.0", "tasks": [{"workspace": "current", "task_ref": self.task_ref, "disposition": "convert_active", "record": self.projection.read_record()}], "files": files}
        delivery = self.projection.resolve(self.key)
        self.projection.apply({"api_version": "1.0", "operation": "record_gate", "key": self.key, "owner_role": "planning", "owner_id": owners["planning"], "expected_phase": "planning", "result": {"result_id": "planning:source", "owner_role": "planning", "owner_id": owners["planning"], "outcome": "accepted", "scope_ref": delivery["scope_ref"], "plan_ref": authority_ref(planning / "implement.md", self.repo), "candidate": None, "predecessor_result_id": None, "obligations": [], "evidence": [metadata["accepted_scope"]]}})
        BranchBindingStore(inspect_repository(self.repo)).establish(TaskLifecycleKey("source-task", 0), "feature/source")
        self.projection.begin_check(self.key, self.projection.candidate(["app.txt"], head_ref=self.head, base_ref=self.git("rev-parse", "main")))
        module_path = SKILLS / "packages/guru-check-task/runtime/common.py"
        spec = importlib.util.spec_from_file_location("migration_check_common", module_path)
        common = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(common)
        owner = json.loads((SKILLS / "packages/guru-check-task/examples/phase2-check.json").read_text())
        owner.update(task_ref=self.task_ref, phase2_capture_commit=self.head, reviewed_content_sha256=common.content_identity(self.repo), reviewed_paths=["app.txt"], candidate_classifications=[])
        checked = self.wrapper("guru-check-task", "invoke.sh", "--input", self.write("check.json", {"profile": "delivery_initial_check", "mode": "workflow", "source_exit": "implementation_complete", "task_ref": self.task_ref, "delivery_key": self.key, "planning_accepted_result_id": "planning:source"}), "--owner-result", self.write("check-owner.json", owner))
        self.public = {"profile": "delivery_committed_reentry", "mode": "workflow", "task_ref": self.task_ref, "delivery_key": self.key, "check_result_id": checked["check_result_id"]}
        self.review = {"status": "passed", "summary": "Original owner reviewed actual Plan2 mapping.", "evidence": ["Original committed root planning blobs and current scope."]}

    def migrate(self, planning_projection=None):
        value = {"profile": "delivery_source_migration", "task_ref": self.task_ref, "delivery_key": self.key, "source_commit": self.head, "planning_sources": {name: self.task_ref + "/" + name for name in self.names}, "plan_file": self.write("plan.json", self.plan), "workspace": "current"}
        if planning_projection is not None:
            value["planning_projection"] = planning_projection
        args = ("--input", self.write("migration.json", value), "--owner-result", self.write("review.json", self.review))
        preview = self.wrapper(PACKAGE.name, "migrate-delivery-source.sh", *args, "--preview")
        self.assertEqual("preview", preview["status"])
        self.assertEqual([".trellis/.runtime/guru-team/task-commit-sources/" + self.key["delivery_id"] + "/source.json"], preview["write_paths"])
        return self.wrapper(PACKAGE.name, "migrate-delivery-source.sh", *args)

    def reentry(self, success=True):
        return self.wrapper(PACKAGE.name, "invoke.sh", "--input", self.write("reentry.json", self.public), "--owner-result", self.write("review.json", self.review), success=success)

    def test_real_missing_delivery_paths_retain_original_clean_head(self):
        self.assertEqual("stale_identity", self.reentry(False)["code"])
        self.assertEqual("source_bound", self.migrate()["status"])
        self.assertEqual("source_bound", self.migrate()["status"])
        self.assertEqual("committed", self.reentry()["exit_id"])
        self.assertEqual(self.head, self.git("rev-parse", "HEAD"))
        self.assertEqual("", self.git("diff", "--cached", "--name-only"))
        # This is the first full independent Review, not Check or continuity.
        package = SKILLS / "packages/guru-review-branch"
        fixture = json.loads((package / "examples/review-gate.json").read_text())
        semantic = {key: fixture[key] for key in ("candidate_classifications", "semantic_review", "verification_evidence", "delivery_review")}
        semantic["candidate_classifications"] = []
        semantic["semantic_review"]["qualified_findings"] = []
        public = {"profile": "delivery_branch_review", "mode": "workflow", "task_ref": self.task_ref, "delivery_key": self.key, "check_result_id": self.public["check_result_id"], "base_ref": "main", "branch_review_commit": self.head, "review_intent": "initial_review"}
        self.wrapper(package.name, "review-branch.sh", "--task", self.task_ref, "--skill-input", self.write("branch.json", public), "--semantic-review-file", self.write("branch-review.json", semantic), "--typed-exit", "passed")
        reviewed = self.wrapper(package.name, "invoke.sh", "--input", self.write("branch.json", public))
        self.assertEqual("passed", reviewed["exit_id"])
        self.assertEqual(self.head, self.git("rev-parse", "HEAD"))

    def test_normal_plan_change_cannot_reuse_source_association(self):
        self.migrate()
        (self.projection.planning_directory(self.key) / "check.jsonl").write_text("{\"file\":\"app.txt\"}\n")
        self.assertEqual("stale_identity", self.reentry(False)["code"])

    def test_projected_destinations_retain_clean_head_and_reject_real_change(self):
        # The actual artifact writer supplies projected content to Plan2.
        planning = self.projection.planning_directory(self.key)
        for row in self.plan["files"]:
            path = self.repo / row["target"]["path"]
            if path.suffix == ".md":
                projected = path.read_bytes().replace(b"../../../docs/", b"../../../../../docs/")
                path.write_bytes(projected)
                row["target_content_base64"] = base64.b64encode(projected).decode()
        self.assertEqual("source_bound", self.migrate("markdown_relative_links_v1")["status"])
        self.assertEqual("committed", self.reentry()["exit_id"])
        self.assertEqual(self.head, self.git("rev-parse", "HEAD"))
        self.assertEqual("", self.git("diff", "--cached", "--name-only"))
        (planning / "design.md").write_text((planning / "design.md").read_text() + "New design obligation\n")
        self.assertEqual("stale_identity", self.reentry(False)["code"])

    def test_projected_mode_does_not_upgrade_existing_raw_association(self):
        self.migrate()
        value = {"profile": "delivery_source_migration", "task_ref": self.task_ref, "delivery_key": self.key, "source_commit": self.head, "planning_sources": {name: self.task_ref + "/" + name for name in self.names}, "plan_file": self.write("plan.json", self.plan), "workspace": "current", "planning_projection": "markdown_relative_links_v1"}
        result = self.wrapper(PACKAGE.name, "migrate-delivery-source.sh", "--input", self.write("changed-mode.json", value), "--owner-result", self.write("review.json", self.review), success=False)
        self.assertEqual("stale_identity", result["code"])


class MarkdownProjectionTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.repo = Path(temporary.name).resolve()
        (self.repo / "docs").mkdir()
        (self.repo / "docs/reference.md").write_text("Actual target")
        sys.path.insert(0, str(PACKAGE / "runtime"))
        self.addCleanup(lambda: sys.path.remove(str(PACKAGE / "runtime")))
        from migration import project_planning_links
        self.project = project_planning_links
        self.source = ".trellis/tasks/example/design.md"
        self.target = self.repo / ".trellis/tasks/example/deliveries/d1/design.md"

    def test_preserves_non_destinations_code_and_suffixes(self):
        raw = b'[actual](../../../docs/reference.md?view=1#R1 "title")\r\n![image](<../../../docs/reference.md>)\n`[literal](missing.md)`\n``[also literal](missing.md)``\n```markdown\n[literal](missing.md)\n```\n[web](https://example.invalid/a) [local](#R1)\n'
        expected = raw.replace(b"../../../docs/reference.md", b"../../../../../docs/reference.md")
        self.assertEqual(expected, self.project(self.repo, self.source, self.target, raw))
        self.assertEqual(raw, self.project(self.repo, self.source.replace(".md", ".jsonl"), self.target, raw))

    def test_normal_missing_target_and_unsupported_syntax_return_to_owner(self):
        from runtime.io import CommandError
        for raw in (b"[missing](../../../docs/missing.md)", b"[nested](../../../docs/ref(1).md)", b"[reference]: ../../../docs/reference.md"):
            with self.assertRaises(CommandError) as caught:
                self.project(self.repo, self.source, self.target, raw)
            self.assertEqual("planning_projection", caught.exception.field_path)
