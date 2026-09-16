"""Real archived owner wrappers; semantic fixture inputs are NOT native AI proof."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

import jsonschema


SKILLS = Path(__file__).resolve().parents[1]
REPO = SKILLS.parents[2]
PACKAGES = SKILLS / "packages"
MERGE = "guru-merge-task-pr"
BRANCH = "guru-review-branch"
PUBLICATION = "guru-review-task-publication"
FINALIZER = "guru-finalize-task"
ARCHITECTURE = "guru-maintain-architecture-baseline"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def archive_fixture():
    # Reuse the normal Workspace producer and real archive executor test setup.
    directory = PACKAGES / FINALIZER / "tests"
    previous_path = sys.path[:]
    previous_support = sys.modules.pop("support", None)
    try:
        sys.path.insert(0, str(directory))
        spec = importlib.util.spec_from_file_location(
            "archived_integration_mapping_fixture", directory / "test_archive_mappings.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.ArchiveMappingTests(), module.GTT
    finally:
        sys.path[:] = previous_path
        sys.modules.pop("support", None)
        if previous_support is not None:
            sys.modules["support"] = previous_support


class ArchivedReviewIntegrationTest(unittest.TestCase):
    def setUp(self):
        self.fixture, self.owner = archive_fixture()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.root = self.fixture.root
        self.parent = self.fixture.producer.parent
        self.inputs = self.root / ".trellis/.runtime/guru-team/archived-integration-inputs"
        self.inputs.mkdir(parents=True)
        self.bin = self.parent / "archived-bin"
        self.bin.mkdir()
        self.real_git = shutil.which("git")
        self.env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}

        # Install only in the disposable task fixture, before H and archive A.
        shutil.copy2(REPO / "trellis/workflows/guru-team/workflow.md", self.root / ".trellis/workflow.md")
        for relative in ("docs/architecture/README.md", "docs/architecture/00-foundation/design-constitution.md",
                         "docs/architecture/06-governance/change-contract.md", "docs/requirements/README.md",
                         "docs/design/README.md"):
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("# Isolated fixture authority\n\nThe seed text is unchanged; closeout moves task metadata only.\n", encoding="utf-8")
        self.run_command([
            sys.executable, "-B", str(REPO / "trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py"),
            "--repo", str(self.root), "--platform", "codex", "--json",
        ], cwd=REPO)
        summary = self.fixture.task_dir / self.owner.FINISH_SUMMARY_ARTIFACT
        summary.unlink()
        self.git("add", "-A")
        self.git("commit", "-qm", "Install current source assets in isolated fixture")
        self.original_tip = self.git("rev-parse", "HEAD")
        old = self.fixture.plan
        self.fixture.head = self.original_tip
        self.fixture.plan = self.owner.build_finalization_plan(
            self.root, self.fixture.task_dir, self.fixture.context,
            self.owner.task_json(self.fixture.task_dir), repo="example/repo", remote="origin",
            base_branch="main", head_branch="feat/027-workspace",
            branch_review_commit=self.original_tip, title=old["publish"]["title"],
            body=old["publish"]["body"] + "\nExact trailing payload bytes.  \n",
            review_facts={"changed_paths": [self.fixture.active + "/task.json"]},
        )
        self.owner.write_json(summary, self.owner.closeout_summary_for_pr(self.fixture.plan, self.fixture.pr))
        self.fixture.archive()
        self.fixture.assert_converged()
        self.task_ref = self.fixture.plan["task"]["archive_locator"]
        self.head = self.git("rev-parse", "HEAD")
        self.base = self.git("rev-parse", "refs/remotes/origin/main")
        self.git("push", "-q", "origin", "feat/027-workspace")
        self.git("remote", "set-url", "origin", "https://github.com/example/repo.git")
        self.git("config", f"url.{self.fixture.producer.remote}.insteadOf", "https://github.com/example/repo.git")
        self.pr = {
            **self.fixture.pr, "state": "OPEN", "isDraft": False,
            "headRefName": "feat/027-workspace", "baseRefName": "main", "headRefOid": self.head,
            "headRepository": {"nameWithOwner": "example/repo"}, "isCrossRepository": False,
            "headRepositoryOwner": {"login": "example"},
            "title": self.fixture.plan["publish"]["title"], "body": self.fixture.plan["publish"]["body"],
            "mergeable": "MERGEABLE", "mergeStateStatus": "CLEAN", "reviewDecision": "APPROVED",
            "statusCheckRollup": [], "mergedAt": None, "mergeCommit": None,
        }
        self.provider_base = self.base
        self.provider_path = self.write("provider.json", {})
        self.provider_log = self.inputs / "provider.log"
        self.write_provider()
        # Only known read requests reach the transport fixture; everything else fails.
        self.executable("gh", '''import json, os, sys
from pathlib import Path
a = sys.argv[1:]
p = json.loads(Path(os.environ["ARCHIVED_PROVIDER"]).read_text())
with Path(os.environ["ARCHIVED_PROVIDER_LOG"]).open("a") as log:
    log.write(json.dumps(["gh", *a]) + "\\n")
if a == ["--version"]: print("gh version fixture"); sys.exit(0)
if a == ["auth", "status"]: sys.exit(0)
if a[:2] == ["api", "repos/example/repo"]:
    result = {"full_name": "example/repo", "default_branch": "main", "allow_merge_commit": True, "allow_squash_merge": False, "allow_rebase_merge": False}
elif a[:2] == ["api", "repos/example/repo/git/ref/heads/main"]:
    result = {"ref": "refs/heads/main", "object": {"sha": p["base"], "type": "commit"}}
elif a[:3] == ["pr", "view", "27"] and "--repo" in a and a[a.index("--repo")+1] == "example/repo": result = p["pr"]
elif a[:2] == ["pr", "list"] and "--repo" in a and a[a.index("--repo")+1] == "example/repo": result = [p["pr"]]
elif a[:3] == ["pr", "checks", "27"] and "--repo" in a and a[a.index("--repo")+1] == "example/repo": result = []
else: print("Unsupported fixture request", file=sys.stderr); sys.exit(91)
print(json.dumps(result))
''')
        self.executable("git", '''import json, os, sys
from pathlib import Path
a = sys.argv[1:]
with Path(os.environ["ARCHIVED_PROVIDER_LOG"]).open("a") as log:
    log.write(json.dumps(["git", *a]) + "\\n")
if a in (["remote", "get-url", "origin"], ["remote", "get-url", "--all", "origin"], ["remote", "get-url", "--push", "--all", "origin"]):
    print("https://github.com/example/repo.git"); sys.exit(0)
if a and a[0] in {"push", "fetch", "commit", "add", "update-ref", "checkout", "switch", "merge", "reset", "rebase", "stash"}:
    print("Read-only fixture forbids mutation", file=sys.stderr); sys.exit(92)
os.execv(os.environ["ARCHIVED_REAL_GIT"], [os.environ["ARCHIVED_REAL_GIT"], *a])
''')
        self.env.update({"PATH": str(self.bin) + os.pathsep + os.environ["PATH"],
                         "ARCHIVED_PROVIDER": str(self.provider_path),
                         "ARCHIVED_PROVIDER_LOG": str(self.provider_log),
                         "ARCHIVED_REAL_GIT": self.real_git})
        self.installed = self.root / ".trellis/guru-team/skills/packages"
        self.before = self.state()

    def run_command(self, argv, *, ok=True, cwd=None):
        result = subprocess.run(argv, cwd=cwd or self.root, env=self.env, text=True, capture_output=True)
        detail = (result.stdout + result.stderr)[-8000:]
        if ok:
            self.assertEqual(0, result.returncode, detail)
        else:
            self.assertNotEqual(0, result.returncode, detail)
        return result

    def git(self, *argv):
        return self.run_command([self.real_git, *argv]).stdout.strip()

    def write(self, name, value):
        path = self.inputs / name
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return path

    def executable(self, name, source):
        path = self.bin / name
        path.write_text(f"#!{sys.executable}\n" + source, encoding="utf-8")
        path.chmod(0o755)

    def write_provider(self):
        self.write("provider.json", {"pr": self.pr, "base": self.provider_base})

    def state(self):
        files = [*self.fixture.mapping_paths, *self.fixture.workspace_paths]
        for root in (self.fixture.source, self.root):
            files.extend(p for p in (root / ".trellis/tasks").rglob("*") if p.is_file())
        return {"files": {str(p): p.read_bytes() for p in files},
                "refs": self.git("show-ref"), "head": self.git("rev-parse", "HEAD"),
                "status": self.git("status", "--porcelain"),
                "remote": self.git("ls-remote", "origin"),
                "provider": self.provider_path.read_bytes()}

    def assert_read_only_calls(self):
        for line in self.provider_log.read_text(encoding="utf-8").splitlines():
            call = json.loads(line)
            if call[0] == "git":
                self.assertNotIn(call[1], {"push", "fetch", "commit", "add", "update-ref", "checkout",
                                         "switch", "merge", "reset", "rebase", "stash"}, call)
            elif call[1] == "pr":
                self.assertIn(call[2], {"view", "list", "checks"}, call)
            elif call[1] == "api":
                self.assertNotIn("--method", call)
                self.assertNotIn("-X", call)
            else:
                self.assertIn(call[1:], [["--version"], ["auth", "status"]])

    def wrapper(self, package, name, *args, ok=True):
        if package == FINALIZER:
            args = tuple(arg.relative_to(self.root).as_posix() if isinstance(arg, Path) else arg for arg in args)
        process = self.run_command([str(self.installed / package / "scripts" / name),
                                    "--root", str(self.root), *map(str, args), "--json"], ok=ok)
        payload = json.loads(process.stdout or process.stderr)
        self.assertIsInstance(payload, dict)
        return payload

    def project(self, producer, output):
        contracts = read(self.installed / producer / "interface.json")["public_contracts"]
        out = next(row for row in contracts["outputs"] if row["exit_id"] == output["exit_id"])
        jsonschema.validate(output, read(self.installed / producer / out["schema"]["path"]))
        projection, = [row for row in contracts["projections"] if row["exit_id"] == output["exit_id"]]
        self.assertEqual("select", projection["operation"])
        target = next(row for row in contracts["consumer_inputs"] if row["id"] == projection["consumer_input_id"])
        contract = target["contract"]
        consumer = target["consumer"]["id"]
        authored = read(self.installed / consumer / contract["authoring_example"]["path"])
        public = {**authored, **{row["target"]: output[row["source"]] for row in projection["mappings"]}}
        interface = read(self.installed / consumer / "interface.json")
        profile = next(row for row in interface["public_contracts"]["input"]["profiles"] if row["id"] == contract["profile_id"])
        jsonschema.validate(public, read(self.installed / consumer / profile["schema"]["path"]))
        return public

    def merge_request(self):
        public = {"schema_version": "2.0", "mode": "workflow", "profile": "archived_review_request",
                  "task_ref": self.task_ref, "repo_ref": "example/repo", "pr_number": 27,
                  "expected_head_sha": self.head}
        return self.wrapper(MERGE, "invoke.sh", "--input", self.write("request.json", public),
                            "--review-input", self.installed / MERGE / "examples/archived-review-semantic-input.json")

    def branch_review(self, public, *, ok=True):
        example = read(self.installed / BRANCH / "examples/review-gate.json")
        semantic = {key: example[key] for key in ("candidate_classifications", "semantic_review", "verification_evidence")}
        semantic["semantic_review"]["ai_review_gate"]["status"] = "archived_review_passed"
        semantic["verification_evidence"]["evidence"] = ["Deterministic integration fixture input, not native semantic proof."]
        public_path = self.write("branch.json", public)
        recorded = self.wrapper(BRANCH, "review-branch.sh", "--task", self.task_ref,
                                "--skill-input", public_path, "--semantic-review-file", self.write("branch-semantic.json", semantic),
                                "--typed-exit", "archived_review_passed", ok=ok)
        if not ok:
            return recorded
        self.wrapper(BRANCH, "check-review-gate.sh", "--task", self.task_ref)
        result = self.wrapper(BRANCH, "invoke.sh", "--input", public_path)
        self.assertFalse(self.checkpoint("review-gate.json").exists())
        return result

    def checkpoint(self, name):
        return self.root / ".trellis/.runtime/guru-team/owner-checkpoints" / Path(self.task_ref).name / name

    def publication(self, public, *, ok=True):
        example = read(self.installed / PUBLICATION / "examples/pr-readiness.json")
        semantic = {**public, **{key: example[key] for key in (
            "candidate_classifications", "dimensions", "findings", "conclusions", "route")},
            "pr_payload": {key: self.fixture.plan["publish"][key] for key in ("title", "body")}}
        semantic["route"] = {"typed_exit": "archived_ready"}
        result = self.wrapper(PUBLICATION, "invoke.sh", "--input", self.write("publication.json", public),
                              "--semantic-result", self.write("publication-semantic.json", semantic), ok=ok)
        if ok:
            self.assertFalse(self.checkpoint("pr-readiness.json").exists())
        return result

    def finalizer(self, public, *, ok=True):
        result = self.wrapper(FINALIZER, "invoke.sh", "--input", self.write("finalizer.json", public),
                              "--review-input", self.installed / FINALIZER / "examples/semantic-review-input.json", ok=ok)
        if ok:
            self.assertFalse(self.checkpoint("task-finalization-gate.json").exists())
        return result

    def architecture(self, output):
        stage = {"review_refresh_required": "branch_review", "archived_review_passed": "publication",
                 "archived_ready": "acceptance_finish"}[output["exit_id"]]
        public = read(self.installed / ARCHITECTURE / "examples/public-input-impact.json")
        public.update(source_exit=output["exit_id"], stage=stage, task_locator=self.task_ref,
                      freshness_identity=f"fixture:{stage}:{self.base}:{self.head}")
        if stage == "branch_review":
            public["committed_range"] = {"base_ref": "origin/main", "base_head": self.base, "review_head": self.head}
        owner = {key: public[key] for key in ("schema_version", "profile", "mode", "continuation_id",
                 "stage", "task_locator", "baseline", "constitution", "project_contract", "freshness_identity")}
        owner.update(
            input_sha256=hashlib.sha256(json.dumps(public, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
            ai_review_gate={"status": "passed", "reviewed_scope": f"Fixture {stage} {self.base}...{self.head}",
                            "evidence_summary": "Deterministic fixture owner input, not native AI evidence.",
                            "findings": [], "conclusion": "The fixture retains its seed behavior and authority."},
            typed_exit="baseline_current", consumer={"kind": "workflow", "id": "guru-architecture-baseline-current-router"},
            baseline_identity=public["baseline"]["identity"], constitution_identity=public["constitution"]["identity"],
            impact_kind="no_architecture_impact", impact_reason="The isolated seed behavior is unchanged.", promotion_state="no_change",
        )
        result = self.run_command([str(self.installed / ARCHITECTURE / "scripts/invoke.sh"),
                                   "--input", str(self.write(f"architecture-{stage}.json", public)),
                                   "--owner-result", str(self.write(f"architecture-{stage}-semantic.json", owner)), "--json"])
        actual = json.loads(result.stdout)
        self.assertEqual("baseline_current", actual["exit_id"])
        self.assertEqual(stage, actual["stage"])
        return actual

    def to_publication(self):
        request = self.merge_request()
        self.assertEqual("review_refresh_required", request["exit_id"])
        self.assertEqual({"exit_id", "task_ref", "branch_review_commit", "pr_payload_snapshot_sha256"}, set(request))
        snapshot = hashlib.sha256(json.dumps({k: self.pr[k] for k in ("title", "body")},
                                             ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        self.assertEqual(snapshot, request["pr_payload_snapshot_sha256"])
        self.architecture(request)
        reviewed = self.branch_review(self.project(MERGE, request))
        self.assertEqual("archived_review_passed", reviewed["exit_id"])
        self.assertEqual(self.base, reviewed["reviewed_base_head"])
        self.architecture(reviewed)
        return self.project(BRANCH, reviewed)

    def test_real_archived_chain_preserves_h_a_and_all_business_state(self):
        public = self.to_publication()
        published = self.publication(public)
        self.assertEqual("archived_ready", published["exit_id"])
        self.assertEqual(self.pr["body"], published["pr_body"])
        self.assertEqual(self.pr["title"], published["pr_title"])
        self.architecture(published)
        final_input = self.project(PUBLICATION, published)
        preview = self.wrapper(FINALIZER, "preview-finalization.sh", "--input", self.write("final-preview.json", final_input))
        self.assertEqual(self.original_tip, preview["original_review_commit"])
        self.assertEqual(self.head, preview["branch_review_commit"])
        self.assertNotEqual(self.head, self.original_tip)
        summary = read(self.root / self.task_ref / "finish-summary.json")
        self.assertIn(self.original_tip, summary["git"]["commits"])
        self.assertNotIn(self.head, summary["git"]["commits"])
        self.git("merge-base", "--is-ancestor", self.original_tip, self.git("rev-parse", "HEAD^"))
        ready = self.finalizer(final_input)
        self.assertEqual("ready_for_merge", ready["exit_id"])
        merge_input = self.project(FINALIZER, ready)
        # Target-owned message authoring is fixture input, never a producer DTO.
        message = merge_input["reviewed_merge_message"]
        message["subject"] = message["subject"].replace("#176", "#27")
        message["body"] = message["body"].replace("#176", "#27").replace("codex/180-eval", "feat/027-workspace")
        self.wrapper(MERGE, "preview-task-pr-merge.sh", "--input", self.write("merge-preview.json", merge_input))
        self.assertEqual(self.before, self.state())
        self.assertFalse(list((self.root / ".trellis/.runtime/guru-team").rglob("finalization-transaction.json")))
        self.assertFalse(list((self.root / ".trellis/.runtime/guru-team").rglob("archived-review-gate.json")))
        self.assert_read_only_calls()

    def test_existing_payload_and_ready_state_drift_blocks_snapshot_consumers(self):
        request = self.merge_request()
        self.architecture(request)
        public = self.project(MERGE, request)
        original = dict(self.pr)
        for field, value in (("title", "Changed title"), ("body", "Changed body\n"),
                             ("headRefOid", self.base), ("state", "CLOSED"), ("isDraft", True)):
            with self.subTest(field=field):
                self.pr = {**original, field: value}
                self.write_provider()
                before = self.state()
                failure = self.branch_review(public, ok=False)
                self.assertEqual("stale_identity", failure["code"])
                self.assertEqual(before, self.state())
        self.assert_read_only_calls()

    def test_base_and_payload_drift_block_publication_and_finalizer(self):
        public = self.to_publication()
        published = self.publication(public)
        self.architecture(published)
        final_input = self.project(PUBLICATION, published)
        # A real existing ancestor advances B without changing A or any artifact.
        self.provider_base = self.original_tip
        self.git("update-ref", "refs/remotes/origin/main", self.provider_base)
        self.write_provider()
        before = self.state()
        self.assertEqual("publication_stale", self.publication(public, ok=False)["code"])
        self.assertEqual("finalization_stale", self.finalizer(final_input, ok=False)["code"])
        self.assertEqual(before, self.state())
        self.provider_base = self.base
        self.git("update-ref", "refs/remotes/origin/main", self.base)
        original = dict(self.pr)
        for field in ("title", "body"):
            with self.subTest(field=field):
                self.pr = {**original, field: original[field] + " changed"}
                self.write_provider()
                before = self.state()
                self.assertEqual("publication_stale", self.publication(public, ok=False)["code"])
                self.assertEqual("finalization_stale", self.finalizer(final_input, ok=False)["code"])
                self.assertEqual(before, self.state())
        self.assert_read_only_calls()


if __name__ == "__main__":
    unittest.main()
