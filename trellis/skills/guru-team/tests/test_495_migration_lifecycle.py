"""Opt-in, source-loaded migration acceptance against a real legacy installation.

Run with TRELLIS_495_LEGACY_REPO and TRELLIS_FIXED_FORK_SOURCE. Only manifest-
declared reusable assets are copied; business tasks and historical data below
are deidentified representatives of the observed full/minimal legacy shapes.
No operation mutates the legacy source repository or publishes Git resources.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


REPO = Path(__file__).resolve().parents[4]
PACKAGES = REPO / "trellis/skills/guru-team/packages"
PROFILE = "guru0.6-family"


def json_identity(value: object) -> str:
    """Author a call-local identity; the public owner independently checks it."""
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def digest(path: Path) -> str | None:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run(root: Path, arguments: list[str], *, payload: dict | None = None,
        environment: dict | None = None) -> subprocess.CompletedProcess[str]:
    env = {key: value for key, value in os.environ.items()
           if key not in {"CODEX_THREAD_ID", "TRELLIS_CONTEXT_ID", "PYTHONPATH"}}
    env.update({"PYTHONDONTWRITEBYTECODE": "1", "TRELLIS_CONTEXT_ID": "migration-495"})
    env.update(environment or {})
    return subprocess.run(arguments, cwd=root, env=env, text=True,
                          input=json.dumps(payload) if payload is not None else None,
                          capture_output=True, check=False)


def git(root: Path, *arguments: str) -> str:
    result = run(root, ["git", *arguments])
    if result.returncode:
        raise AssertionError(result.stderr)
    return result.stdout.strip()


def legacy_task(task_id: str, status: str, *, minimal: bool = False) -> dict:
    """Same field shapes as the observed .41 tasks, without business content."""
    record = {
        "id": task_id, "name": task_id, "title": "脱敏迁移接续样本",
        "status": status, "branch": "task/legacy", "base_branch": "main",
        "creator": "legacy-user", "assignee": "legacy-user", "scope": "fixture",
    }
    if not minimal:
        record.update({
            "description": "TAPD business reference retained as description.",
            "dev_type": "backend", "package": None, "priority": "P2",
            "createdAt": "2026-09-08", "completedAt": None,
            "worktree_path": "/retired-fixture/old-checkout", "commit": None,
            "pr_url": None, "subtasks": [], "children": [], "parent": None,
            "relatedFiles": [], "notes": "Business notes retained.",
            "meta": {"business_reference": "TAPD-fixture"},
        })
    return record


def reviewed_projection(record: dict, source: dict) -> dict:
    """AI-reviewed fixture projection; production writers perform conversion."""
    value = {
        "description": "", "dev_type": None, "package": None, "priority": "P2",
        "createdAt": "", "completedAt": None, "worktree_path": None,
        "commit": None, "pr_url": None, "children": [], "parent": None,
        "relatedFiles": [], "notes": "", "meta": {},
    }
    value.update({key: item for key, item in record.items()
                  if key not in {"creator", "assignee", "subtasks"}})
    value.update({"lifecycle_generation": 0, "source": source})
    return value


class MigrationLifecycleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        legacy = os.environ.get("TRELLIS_495_LEGACY_REPO")
        fork = os.environ.get("TRELLIS_FIXED_FORK_SOURCE")
        if not legacy or not fork:
            raise unittest.SkipTest("Explicit legacy repository and Fork candidate are required; no migration proof.")
        cls.legacy = Path(legacy).resolve()
        cls.fork = Path(fork).resolve()
        cls.cli = cls.fork / "packages/cli/bin/trellis.js"
        cls.manifest = json.loads((cls.legacy / ".trellis/guru-team/extension.json").read_text())
        if ((cls.legacy / ".trellis/.version").read_text().strip() != "0.6.16"
                or cls.manifest["extension"]["version"] != "0.6.16-guru.41"):
            raise AssertionError("This acceptance requires the exact .41 legacy representative; other families have grouped acceptance.")

    def setUp(self) -> None:
        self.temporary = Path(tempfile.mkdtemp(prefix="guru-495-lifecycle-"))
        if os.environ.get("TRELLIS_495_KEEP_FIXTURES") != "1":
            self.addCleanup(shutil.rmtree, self.temporary)
        else:
            print(f"Retained isolated fixture: {self.temporary}")
        self.root = self.temporary / "repo"
        self.root.mkdir()
        self.source_status = git(self.legacy, "status", "--porcelain=v1", "--untracked-files=all")
        self.source_head = git(self.legacy, "rev-parse", "HEAD")
        self.copy_legacy_assets()
        git(self.root, "init", "-q", "-b", "main")
        git(self.root, "config", "user.name", "Migration Fixture")
        git(self.root, "config", "user.email", "migration@example.invalid")
        git(self.root, "remote", "add", "origin", "https://github.com/castbox/guru-trellis.git")
        self.write("business.txt", "committed business baseline\n")
        self.write("unrelated.txt", "unrelated baseline\n")
        self.write(".gitignore", ".trellis/.runtime/\n__pycache__/\n")
        self.write(".trellis/config.yaml", "task_auto_commit: false\nfixture_setting: preserved\n")
        self.configuration_before = (self.root / ".trellis/config.yaml").read_text()
        self.write(".trellis/spec/business/example.md", "# User-owned business convention\n")
        self.write(".codex/local-notes.md", "# User-owned platform customization\n")
        self.write("AGENTS.md", "# Business instructions\nPreserve this user-owned paragraph.\n")
        self.write_architecture_foundation()
        # Synthetic historical bytes prove preservation without reading real traces.
        self.write(".trellis/.developer", "historical-fixture\n")
        self.write(".trellis/workspace/fixture/journal-1.md", "# Immutable historical journal\n")
        self.write(".trellis/agent-traces/fixture.jsonl", '{"event":"historical-fixture"}\n')
        write_json(self.root / ".trellis/tasks/archive/2026-09/retired/task.json",
                   {"id": "retired", "creator": "historical-fixture", "status": "completed"})
        git(self.root, "add", ".")
        git(self.root, "commit", "-qm", "legacy reusable assets and business baseline")
        self.base_head = git(self.root, "rev-parse", "HEAD")
        git(self.root, "update-ref", "refs/remotes/origin/main", self.base_head)
        git(self.root, "switch", "-qc", "task/legacy")
        self.addCleanup(self.check_source_unchanged)

    def check_source_unchanged(self) -> None:
        self.assertEqual(git(self.legacy, "rev-parse", "HEAD"), self.source_head)
        self.assertEqual(git(self.legacy, "status", "--porcelain=v1", "--untracked-files=all"), self.source_status)

    def copy_legacy_assets(self) -> None:
        hashes = json.loads((self.legacy / ".trellis/.template-hashes.json").read_text())
        paths = set(hashes["hashes"])
        paths.update(self.manifest["install"]["managed_assets"])
        paths.update(self.manifest["install"]["managed_asset_hashes"])
        paths.update(row["path"] for key in ("skill_packages", "overlays")
                     for row in self.manifest[key]["files"])
        paths.update({".trellis/.version", ".trellis/.template-hashes.json", ".trellis/workflow.md"})
        for relative in sorted(paths):
            path = Path(relative)
            if path.is_absolute() or ".." in path.parts or ".env" in path.parts:
                raise AssertionError("Unexpected managed asset locator in legacy fixture.")
            if any(part in {"workspace", "agent-traces", "tasks", ".runtime"} for part in path.parts):
                continue
            source = self.legacy / path
            if source.is_file() and not source.is_symlink():
                target = self.root / path
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)

    def write(self, relative: str, text: str) -> None:
        target = self.root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    def write_architecture_foundation(self) -> None:
        """A real small business baseline, independent of Guru's own baseline."""
        self.write("docs/architecture/README.md", """# Fixture Architecture Baseline
Identity: fixture-business-current-v1; status: active.
The application stores a single business document in business.txt.
Its owner is the business task; Trellis owns development metadata only.
Current and target application behavior are identical during tool migration.
Rule FIXTURE-ARCH-001: preserve application documents and their existing owner.
No task may treat installation evidence as business acceptance.
Constitution: 00-foundation/design-constitution.md.
Change contract: 06-governance/change-contract.md.
""")
        self.write("docs/architecture/00-foundation/design-constitution.md", """# Fixture Design Constitution
Identity: fixture-constitution-v1; status: current.
Use applicable mature practices; retain complete business concepts and facts;
keep application and tool ownership separate; use only necessary mechanisms;
retire old runtime authority through an explicit single migration boundary.
""")
        self.write("docs/architecture/06-governance/change-contract.md", """# Fixture Architecture Change Contract
Identity: fixture-change-contract-v1; status: current.
Required concerns: fixture-concerns-v1.
Review authority, application/tool boundary, owners, compatibility exit,
scope, before/after evidence, and required promotion.
A task which only resumes unchanged business work has no Architecture impact.
Changing business storage or its owner requires an isolated contribution and
independent review before shared baseline promotion.
""")

    def commit_task(self, status: str, *, minimal: bool = False) -> dict:
        self.task_id = "legacy-task.non-uuid"
        self.task_ref = ".trellis/tasks/09-08-legacy-task"
        record = legacy_task(self.task_id, status, minimal=minimal)
        write_json(self.root / self.task_ref / "task.json", record)
        # A valid old task remains at its original ref with a distinct stable
        # id (as after an ordinary rename). It occupies identity but has no
        # current source/binding; migration explicitly defers its continuation.
        self.deferred_ref = ".trellis/tasks/09-09-renamed-deferred-work"
        self.deferred_id = "deferred-old-task"
        deferred = legacy_task(self.deferred_id, "planning")
        deferred.update({"branch": None, "worktree_path": None})
        write_json(self.root / self.deferred_ref / "task.json", deferred)
        self.deferred_before = (self.root / self.deferred_ref / "task.json").read_bytes()
        for name, text in {
            "prd.md": "# Fixture request\nPreserve existing business work and resume this task after installation maintenance.\nThe unrelated deferred task keeps its original bytes and stable identity.\nAcceptance: current creation, identity resolution and session continuation remain usable in mixed inventory; business behavior is unchanged.\n",
            "design.md": "# Fixture design\nUse the existing branch, checkout and session owners; migration changes tooling only.\nBusiness storage remains business.txt with the same owner and behavior, per docs/architecture/README.md.\nKnown old inventory reserves identity without entering current lifecycle candidates.\n",
            "implement.md": "# Fixture implementation\nRun actual normal-scenario and solution-mechanism qualification, current Architecture Planning review, then Planning approval.\nVerify mixed-inventory owner re-entry, native session reads, semantic configuration preservation, and business/history byte preservation.\nNo production operation or remote delivery.\n",
        }.items():
            self.write(f"{self.task_ref}/{name}", text)
        git(self.root, "add", self.task_ref, self.deferred_ref)
        git(self.root, "commit", "-qm", "committed legacy task")
        if status == "in_progress":
            self.write("business.txt", "committed business implementation\n")
            git(self.root, "add", "business.txt")
            git(self.root, "commit", "-qm", "existing business work")
            self.write("business.txt", "committed business implementation\nordinary uncommitted work\n")
            self.write("unrelated.txt", "unrelated dirty work\n")
            self.write("untracked-note.txt", "unrelated untracked work\n")
        self.pre_migration_head = git(self.root, "rev-parse", "HEAD")
        return record

    def public(self, skill_id: str, payload: dict, *, owner: dict | None = None,
               extra: list[str] | None = None, script: str = "invoke.sh",
               environment: dict | None = None) -> dict:
        package = (PACKAGES / skill_id if skill_id == "guru-upgrade-installation"
                   else self.root / ".codex/skills" / skill_id)
        arguments = ["bash", str(package / "scripts" / script), "--root", str(self.root), "--input", "-"]
        if owner is not None:
            arguments.extend(["--owner-result", json.dumps(owner)])
        arguments.extend(extra or [])
        process = run(self.root, arguments, payload=payload, environment=environment)
        self.assertEqual(process.returncode, 0, f"{skill_id}: {process.stdout}\n{process.stderr}")
        return json.loads(process.stdout)

    def preserved_snapshot(self) -> dict:
        paths = ["business.txt", "unrelated.txt", "untracked-note.txt", ".trellis/.developer",
                 ".trellis/workspace/fixture/journal-1.md", ".trellis/agent-traces/fixture.jsonl",
                 ".trellis/tasks/archive/2026-09/retired/task.json", ".trellis/spec/business/example.md",
                 ".codex/local-notes.md", ".gitignore", self.deferred_ref + "/task.json",
                 "docs/architecture/README.md", "docs/architecture/00-foundation/design-constitution.md",
                 "docs/architecture/06-governance/change-contract.md"]
        paths.extend(f"{self.task_ref}/{name}" for name in ("prd.md", "design.md", "implement.md"))
        return {path: (digest(self.root / path), (self.root / path).stat().st_mode & 0o777)
                for path in paths if (self.root / path).exists()}

    def upgrade(self, record: dict, source: dict, *, preserve_edit: str | None = None) -> dict:
        projection = reviewed_projection(record, source)
        core_plan = {"schema_version": "1.0", "target_version": "0.7.0-castbox.3",
                     "tasks": [{"task_ref": self.task_ref,
                                "expected_sha256": digest(self.root / self.task_ref / "task.json"),
                                "record": projection}], "file_decisions": [],
                     "deferred_tasks": [{"task_ref": self.deferred_ref,
                                         "expected_sha256": digest(self.root / self.deferred_ref / "task.json")}]}
        core_path = self.temporary / "core-plan.json"
        write_json(core_path, core_plan)
        preview = run(self.root, ["node", str(self.cli), "migrate", "--from", "0.6.16",
                                 "--plan", str(core_path), "--dry-run"])
        self.assertEqual(preview.returncode, 0, preview.stdout + preview.stderr)
        core_preview = json.loads(preview.stdout)
        # The fixture copied only versioned reusable assets. Its intentionally
        # user-owned configuration/workflow is handled by their explicit owner.
        core_plan["file_decisions"] = [
            {"path": path, "action": ("remove" if path in {
                f".{platform}/skills/trellis-meta/references/local-architecture/workspace-memory.md"
                for platform in ("agents", "claude", "cursor")
            } | {".trellis/scripts/add_session.py", ".trellis/scripts/common/developer.py",
                 ".trellis/scripts/get_developer.py", ".trellis/scripts/init_developer.py"}
             else "replace"), "expected_sha256": digest(self.root / path)}
            for path in core_preview["conflicts"]
        ]
        write_json(core_path, core_plan)
        reviewed_preview = run(self.root, ["node", str(self.cli), "migrate", "--from", "0.6.16",
                                          "--plan", str(core_path), "--dry-run"])
        self.assertEqual(reviewed_preview.returncode, 0, reviewed_preview.stdout + reviewed_preview.stderr)
        public_input = {"profile": "initial_upgrade", "source_profile": PROFILE,
                        "target_source_ref": git(REPO, "rev-parse", "HEAD")}
        plan = {"core_plan": core_plan, "dependency_mode": "local_candidate", "selected_platforms": ["codex"],
                "guru_decisions": [], "controls": [],
                "workflow": {"provider_ref": public_input["target_source_ref"],
                             "action": "replace", "expected_sha256": digest(self.root / ".trellis/workflow.md")}}
        if preserve_edit:
            plan["guru_decisions"] = [{"path": preserve_edit, "action": "preserve",
                                       "expected_sha256": digest(self.root / preserve_edit)}]
        plan_path = self.temporary / "reviewed-plan.json"
        write_json(plan_path, plan)
        before_preview = self.preserved_snapshot()
        before_status = git(self.root, "status", "--porcelain=v1", "--untracked-files=all")
        facts = self.public("guru-upgrade-installation", public_input, script="preview.sh",
                            extra=["--fork", str(self.cli), "--plan", str(plan_path)])
        self.assertEqual(facts.get("status"), "preview", facts)
        self.assertEqual({row["id"] for row in facts["tasks"]}, {self.task_id, self.deferred_id})
        self.assertEqual(self.preserved_snapshot(), before_preview)
        self.assertEqual(git(self.root, "status", "--porcelain=v1", "--untracked-files=all"), before_status)
        result = self.public("guru-upgrade-installation", public_input,
                             extra=["--fork", str(self.cli), "--plan", str(plan_path)])
        if result["exit_id"] == "upgraded":
            self.assertIn("formal_fork_source_lock", result["unverified"])
            self.assert_live_installed()
            self.assertEqual(result["installed_version"], "0.7.0-guru.3")
            self.assertEqual((self.root / ".trellis/.version").read_text().strip(), "0.7.0-castbox.3")
            self.assertIn("Preserve this user-owned paragraph.\n", (self.root / "AGENTS.md").read_text())
            self.assert_configuration_preserved()
            self.assertEqual((self.root / self.deferred_ref / "task.json").read_bytes(), self.deferred_before)
            self.assertEqual([path.relative_to(self.root).as_posix() for suffix in ("*.new", "*.bak")
                              for path in self.root.rglob(suffix) if ".git" not in path.parts], [])
        return result

    def assert_configuration_preserved(self) -> None:
        # Official owners may add required settings such as codex.dispatch_mode.
        # Existing valid values remain; configuration is not a historical file.
        current = (self.root / ".trellis/config.yaml").read_text()
        for line in self.configuration_before.splitlines():
            self.assertIn(line, current)
        process = self.native(["-c",
            "import json,sys;from pathlib import Path;sys.path.insert(0,'.trellis/scripts');"
            "from common.config import _load_config,get_task_auto_commit;values=_load_config(Path.cwd());"
            "values['task_auto_commit']=get_task_auto_commit(Path.cwd());print(json.dumps(values))"])
        self.assertEqual(process.returncode, 0, process.stderr)
        values = json.loads(process.stdout)
        self.assertIs(values["task_auto_commit"], False)
        self.assertEqual(values["fixture_setting"], "preserved")

    def native(self, arguments: list[str], *, environment: dict | None = None,
               source_owned: bool = False) -> subprocess.CompletedProcess[str]:
        # Partial preset conflicts have no activated target runtime yet. This
        # explicit source-owned checkpoint executes the installed official task
        # script through the already bootstrapped source runner, without any
        # PATH interpreter or simulated metadata writer.
        runner_root = REPO if source_owned else self.root
        runtime = REPO / "trellis/skills/guru-team/runtime" if source_owned else self.root / ".trellis/guru-team/runtime"
        return run(self.root, ["bash", str(runtime / "resolve-python.sh"),
                              str(runner_root), str(runtime), *arguments], environment=environment)

    def assert_native_session(self, task_id: str, task_ref: str, *, context: str = "migration-495") -> None:
        process = self.native([".trellis/scripts/task.py", "current", "--json", "--source"],
                              environment={"TRELLIS_CONTEXT_ID": context})
        self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
        result = json.loads(process.stdout)
        self.assertNotIn("error", result, result)
        self.assertFalse(result["stale"], result)
        self.assertEqual(result["current_task"]["id"], task_id)
        self.assertEqual(result["current_task"]["dir"], task_ref)
        self.assertEqual((self.root / self.deferred_ref / "task.json").read_bytes(), self.deferred_before)

    def fresh_planning_approval(self) -> dict:
        # These are AI-authored judgments for the concrete deidentified fixture,
        # not a recorder's inference from schema validation or an old gate.
        # Every run invokes the actual installed owners with current identities.
        planning_paths = [f"{self.task_ref}/{name}" for name in ("prd.md", "design.md", "implement.md")]
        planning_identity = json_identity([
            {"path": path, "content_sha256": digest(self.root / path)}
            for path in sorted(planning_paths)
        ])
        for skill_id, candidate, observation, consumer_id in (
            ("guru-qualify-normal-scenario", "fixture-mixed-continuation",
             "Before migration the old full/minimal record cannot enter current owners; the supported migration must preserve this task and the explicitly deferred unrelated record.",
             "guru-normal-scenario-classified-router"),
            ("guru-qualify-solution-mechanism", "fixture-current-owner-reentry",
             "Task identity remains in task.json and the existing branch/checkout/session stores; ordinary metadata and private recovery files do not provide OS/process authority.",
             "guru-solution-mechanism-classified-router"),
        ):
            public = {
                "profile": "planning_scenario_set", "mode": "standalone", "caller": "guru-approve-task-plan",
                "target_locator": self.task_ref,
                "target": {"repo_locator": ".", "task_ref": self.task_ref,
                           "planning_paths": planning_paths, "planning_identity": planning_identity},
                "candidate_refs": [candidate],
                "candidate_locators": [{"candidate_ref": candidate,
                                        "locators": ["path:" + path for path in planning_paths] + ["path:docs/architecture/README.md"]}],
            }
            semantic = {
                "schema_version": "1.0", "skill_id": skill_id, "public_input": public,
                "candidate_results": [{
                    "candidate_ref": candidate, "decision": "qualified_current",
                    "reason": "The fixture's current requirement explicitly preserves unchanged business work and uses the existing application-level owners.",
                    "witness": {
                        "requirement_refs": ["path:" + self.task_ref + "/prd.md"],
                        "supported_entry_refs": ["guru-upgrade-installation", "guru-bind-task-session"],
                        "existing_caller_refs": ["guru-approve-task-plan"],
                        "honest_action_sequence": ["Convert the selected old task, explicitly defer unrelated old inventory, and call existing owners with the retained identity.",
                                                   "Read this unchanged business plan and the fixture Architecture authority before current development re-entry."],
                        "defect_observation": observation, "excluded_assumptions": [],
                    },
                }],
                "ai_review_gate": {"status": "passed", "reviewed_candidate_refs": [candidate],
                                   "summary": "Reviewed the exact fixture authority, supported migration/re-entry graph and ordinary action sequence; no attack, locks or scope expansion."},
                "typed_exit": "classified", "consumer": {"kind": "workflow", "id": consumer_id},
            }
            qualified = self.invoke_envelope(skill_id, {"schema_version": "1.0", "semantic_result": semantic})
            self.assertEqual(qualified["exit_id"], "classified", qualified)
        architecture = self.fixture_architecture_review(planning_identity)
        self.assertEqual(architecture["exit_id"], "baseline_current", architecture)
        self.assertEqual(architecture["impact_kind"], "no_architecture_impact")
        self.fixture_wording_review()
        author = {
            "mode": "standalone", "authority_refs": [self.task_ref + "/prd.md", "docs/architecture/README.md"],
            "delivery_policy": {
                "task_scope": ["fixture-continuation"], "delivery_slice": ["fixture-continuation"],
                "remaining_work": [], "remaining_work_owner": "fixture task",
                "independent_delivery_conditions": ["Existing task and work remain usable through current owners."],
                "validation_boundaries": ["Isolated local candidate only; formal source lock is unverified."],
            },
            "docs_ssot_plan": {"strategy": "no_docs_update_needed", "durable_paths": [],
                               "summary": "The fixture adds no product contract; its existing three plans define this bounded re-entry."},
            "semantic_review": {
                "status": "passed",
                "summary": "Reviewed retained fixture plans and current qualified scenarios/mechanisms; consumed fresh Architecture baseline_current fixture-business-current-v1/no_change. Business ownership is unchanged; deferred bytes and existing work remain separate from current candidates.",
                "checked_dimensions": {
                    "requirement_authority": True, "scope_boundary": True,
                    "design_adequacy": True, "implementation_plan": True,
                    "acceptance_verifiability": True, "docs_ssot": True,
                    "provenance": True, "unusual_scenarios": True,
                },
                "findings": [], "revision_actions": [], "scope_proposals": [], "blocking_reasons": [],
            },
            "typed_exit": "approved", "reason": "Fresh fixture Planning review before current development/check re-entry.",
            "consumer": {"kind": "workflow", "id": "phase-1-task-activation"},
        }
        relative = ".trellis/.runtime/guru-team/fixture/planning-author.json"
        write_json(self.root / relative, author)
        package = self.root / ".codex/skills/guru-approve-task-plan"
        runtime_package = self.root / ".trellis/guru-team/skills/packages/guru-approve-task-plan"
        common = ["--root", str(self.root), "--task", self.task_ref, "--json"]
        recorded = run(self.root, ["bash", str(runtime_package / "scripts/record-planning-approval.sh"),
                                  *common, "--input", relative])
        self.assertEqual(recorded.returncode, 0, recorded.stdout + recorded.stderr)
        checked = run(self.root, ["bash", str(runtime_package / "scripts/check-planning-approval.sh"),
                                 *common, "--require-exit", "approved"])
        self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
        checkpoint = Path(json.loads(checked.stdout)["artifact_path"])
        public_path = self.root / ".trellis/.runtime/guru-team/fixture/planning-public.json"
        write_json(public_path, {"profile": "initial_review", "mode": "standalone",
                                 "task_ref": self.task_ref, "source_exit": "planning_ready"})
        invoked = run(self.root, ["bash", str(package / "scripts/invoke.sh"),
                                 "--root", str(self.root), "--input", str(public_path),
                                 "--owner-result", str(checkpoint)])
        self.assertEqual(invoked.returncode, 0, invoked.stdout + invoked.stderr)
        output = json.loads(invoked.stdout)
        self.assertEqual(output["exit_id"], "approved")
        self.assertEqual(output["task_ref"], self.task_ref)
        self.assertTrue(output["planning_result_id"].startswith("planning:"))
        self.assertFalse(checkpoint.exists())
        return output

    def fixture_wording_review(self) -> None:
        package = self.root / ".trellis/guru-team/skills/packages/guru-review-contract-wording"
        selectors = ["--root", str(self.root), "--task", self.task_ref]
        scope = ["--profile", "planning_artifacts", "--mode", "standalone", *selectors]

        def command(name: str, arguments: list[str], payload: dict | None = None) -> dict:
            result = run(self.root, ["bash", str(package / "scripts" / name), *arguments], payload=payload)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            return json.loads(result.stdout)

        scan = command("record-contract-wording-review.sh", [*scope, "--scan-only"])
        self.assertEqual(scan["scan"]["hits"], [])
        dimensions = ("complete_profile_scope", "all_hits_classified", "zero_unchecked_hits",
                      "product_semantics_preserved", "retained_reasons_sufficient", "zero_hits_not_requirement_review")
        planning = ("no_requirement_weakening", "source_issue_semantics_preserved", "conditional_paths_have_conditions",
                    "no_parallel_implementation_paths", "gates_have_machine_verifiable_conditions",
                    "acceptance_criteria_are_deterministic", "external_quotes_are_labeled_non_contract")
        # AI review of these exact English fixture plans: unchanged business
        # behavior, one owner per operation, explicit deferred-byte checks, and
        # concrete current-owner/session/config acceptance. A zero scanner count
        # is only a vocabulary fact and does not supply semantic approval.
        author = {
            "generated_at": datetime.now(ZoneInfo("UTC")).isoformat(), "revisions": [], "classifications": [],
            "typed_exit": "pass",
            "ai_review_gate": {"status": "passed", "reviewer": "fixture-current-owner",
                               "summary": "Reviewed all three retained business plans: unchanged requirement and owner, explicit mixed-inventory and byte/config checks, one current continuation path, no external normative quotation.",
                               "reviewed_scan_sha256": scan["scan"]["scan_sha256"],
                               "checked_dimensions": {name: True for name in dimensions},
                               "planning_checked_dimensions": {name: True for name in planning}},
        }
        owner = command("record-contract-wording-review.sh", [*scope, "--input", "-"], author)
        checked = command("check-contract-wording-review.sh", [*selectors, "--input", "-"], owner)
        self.assertEqual(checked["typed_exit"], "pass", checked)
        output = self.invoke_envelope("guru-review-contract-wording", {
            "public_input": {"profile": "planning_artifacts", "mode": "standalone",
                             "source_exit": "start", "continuation_id": "fixture-current-planning",
                             "task_locator": self.task_ref, "planning_artifacts": ["prd.md", "design.md", "implement.md"]},
            "owner_result": owner, "validation_receipt": checked["validation_receipt"],
        })
        self.assertEqual(output["exit_id"], "pass", output)

    def invoke_envelope(self, skill_id: str, envelope: dict) -> dict:
        wrapper = self.root / ".codex/skills" / skill_id / "scripts/invoke.sh"
        process = run(self.root, ["bash", str(wrapper), "--invocation", "-"], payload=envelope)
        self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
        return json.loads(process.stdout)

    def fixture_architecture_review(self, planning_identity: str) -> dict:
        public = json.loads((self.root / ".trellis/guru-team/skills/packages/guru-maintain-architecture-baseline/examples/public-input-impact.json").read_text())
        public.update({"mode": "standalone", "continuation_id": "fixture-current-planning", "task_locator": self.task_ref,
                       "freshness_identity": planning_identity,
                       "requirement_authority": self.task_ref + "/prd.md", "behavior_authority": self.task_ref + "/design.md"})
        public["baseline"].update({"identity": "fixture-business-current-v1", "status": "active"})
        public["constitution"]["identity"] = "fixture-constitution-v1"
        public["project_contract"].update({"change_contract_identity": "fixture-change-contract-v1",
                                           "required_concern_set_identity": "fixture-concerns-v1"})
        # Read the actual project authorities, rather than attaching missing
        # arbitrary locators to a shape-valid Architecture result.
        for locator in (public["baseline"]["locator"], public["constitution"]["authority_locator"],
                        public["project_contract"]["change_contract_locator"], public["requirement_authority"],
                        public["behavior_authority"]):
            self.assertTrue((self.root / locator).read_text().strip())
        owner = {key: public[key] for key in ("profile", "mode", "continuation_id", "stage", "task_locator", "baseline",
                                              "constitution", "project_contract", "freshness_identity")}
        owner.update({
            "schema_version": "2.0", "input_sha256": json_identity(public),
            "baseline_identity": public["baseline"]["identity"], "constitution_identity": public["constitution"]["identity"],
            "impact_kind": "no_architecture_impact", "promotion_state": "no_change",
            "impact_reason": "This business task only resumes its unchanged document work after tooling maintenance. Application storage, ownership, behavior, and the fixture's current Architecture decisions remain identical; migration itself belongs to the separate installation task.",
            "ai_review_gate": {"status": "passed", "reviewed_scope": "Retained business plans, fixture application baseline/constitution/change contract, and existing task owners.",
                               "evidence_summary": "The fixture has one unchanged application document store and owner. Core/Guru metadata conversion is explicit and does not change application interfaces, storage, decisions, GAPs or shared current Architecture.",
                               "findings": [], "conclusion": "Current business planning may re-enter with no Architecture impact; no contribution or promotion burden is introduced."},
            "typed_exit": "baseline_current", "consumer": {"kind": "workflow", "id": "guru-architecture-baseline-current-router"},
        })
        return self.invoke_envelope("guru-maintain-architecture-baseline", {"schema_version": "1.0", "public_input": public, "owner_result": owner})

    def reenter_current_owners(self, status: str) -> dict:
        identity = self.public("guru-establish-task-identity", {
            "profile": "active_task", "mode": "standalone", "task_id": self.task_id,
            "task_ref": self.task_ref, "lifecycle_generation": 0,
        })
        self.assertEqual(identity["exit_id"], "identity_established", identity)
        binding = self.public("guru-establish-task-branch-binding", {
            "profile": "active_task", "mode": "standalone", "action": "establish",
            "task_id": self.task_id, "task_ref": self.task_ref,
            "lifecycle_generation": 0, "expected_status": status,
        })
        self.assertEqual(binding["exit_id"], "binding_established", binding)
        checkout = self.public("guru-ensure-task-checkout", {
            "profile": "active_task", "mode": "standalone",
            "task_id": self.task_id, "lifecycle_generation": 0,
        })
        self.assertEqual(checkout["exit_id"], "checkout_resolved", checkout)
        self.assertEqual(Path(checkout["checkout_path"]).resolve(), self.root.resolve())
        public = {"profile": "rebind_missing_session", "mode": "standalone",
                  "task_id": self.task_id, "lifecycle_generation": 0,
                  "continuation_id": "migration-fixture"}
        owner = {**public, "route": "rebind", "resume_target": "phase-1",
                 "ai_review_gate": {"status": "passed",
                                    "summary": "Reviewed the migrated identity, unique checkout and fresh Planning re-entry."}}
        result = self.public("guru-bind-task-session", public, owner=owner)
        self.assertEqual(result["exit_id"], "session_rebound", result)
        self.assertEqual(result["resume_target"], "phase-1")
        session_path = self.root / ".git/trellis/sessions/migration-495.json"
        self.assertEqual(json.loads(session_path.read_text()),
                         {"schema_version": 2, "task_id": self.task_id, "lifecycle_generation": 0})
        resumed = {**public, "profile": "resume_current_task"}
        owner = {**owner, **resumed, "route": "resume"}
        before = session_path.read_bytes()
        self.assertEqual(self.public("guru-bind-task-session", resumed, owner=owner)["exit_id"], "session_resumed")
        self.assertEqual(session_path.read_bytes(), before)
        self.assert_native_session(self.task_id, self.task_ref)
        return checkout

    def live_installed(self) -> subprocess.CompletedProcess[str]:
        runtime = self.root / ".trellis/guru-team/runtime"
        return run(self.root, ["bash", str(runtime / "resolve-python.sh"), str(self.root), str(runtime),
                               "-m", "runtime.validate", "--root", str(self.root), "--mode", "installed", "--json"],
                   environment={"PYTHONPATH": str(self.root / ".trellis/guru-team")})

    def assert_live_installed(self) -> None:
        validation = self.live_installed()
        self.assertEqual(validation.returncode, 0, validation.stdout + validation.stderr)
        self.assertEqual(json.loads(validation.stdout)["status"], "passed")

    def test_nonempty_retired_directories_preserved_and_live_failure_requires_resume(self) -> None:
        old = self.commit_task("planning")
        local_paths = [".agents/skills/guru-finalize-task/local-notes.md",
                       ".codex/skills/guru-finalize-task/local-notes.md",
                       ".trellis/guru-team/skills/packages/guru-check-task/tests/local-notes.md"]
        for relative in local_paths:
            self.write(relative, "Ordinary project-local guidance retained during upgrade.\n")
        before = {relative: (self.root / relative).read_bytes() for relative in local_paths}
        result = self.upgrade(old, {"kind": "no_issue"})
        self.assertEqual(result["exit_id"], "resume_required", result)
        for relative, content in before.items():
            self.assertEqual((self.root / relative).read_bytes(), content)
        # Staging succeeded but the actual target still contains retained local
        # content in retired/private directories, so success is not published.
        validation = self.live_installed()
        self.assertNotEqual(validation.returncode, 0)
        errors = json.loads(validation.stdout)["errors"]
        self.assertTrue(any("unknown workflow skill copy" in error for error in errors))
        self.assertTrue(any("package-private tests directory" in error for error in errors))
        recovery = self.root / ".git/guru-team/install-upgrade" / result["recovery_ref"]
        checkpoint = json.loads((recovery / "checkpoint.json").read_text())
        self.assertEqual(checkpoint["phase"], "preset")
        self.assertEqual(json.loads((self.root / ".trellis/guru-team/extension.json").read_text())["skill_packages"]["status"], "ok")
        # Resolve the local content, then consume the original public recovery.
        for relative in local_paths:
            (self.root / relative).unlink()
        resumed = self.public("guru-upgrade-installation", {
            "profile": "resume", "recovery_ref": result["recovery_ref"],
        })
        self.assertEqual(resumed["exit_id"], "upgraded", resumed)
        self.assert_live_installed()
        for relative in local_paths:
            self.assertFalse((self.root / relative).parent.exists())

    def test_full_planning_task_reenters_current_owners_without_schema_commit(self) -> None:
        old = self.commit_task("planning")
        before = self.preserved_snapshot()
        output = self.upgrade(old, {"kind": "no_issue"})
        self.assertEqual(output["exit_id"], "upgraded", output)
        self.reenter_current_owners("planning")
        self.fresh_planning_approval()
        self.assertEqual(git(self.root, "rev-parse", "HEAD"), self.pre_migration_head)
        self.assertEqual(self.preserved_snapshot(), before)
        current = json.loads((self.root / self.task_ref / "task.json").read_text())
        self.assertEqual(current["id"], old["id"])
        self.assertEqual(current["meta"], old["meta"])
        self.assertEqual(current["description"], old["description"])
        self.assertEqual(current["source"], {"kind": "no_issue"})
        self.assertNotIn("creator", current)
        self.assertNotIn("assignee", current)
        self.assertIn(" M " + self.task_ref + "/task.json", git(self.root, "status", "--porcelain=v1"))

    def test_minimal_in_progress_retains_commit_dirty_and_untracked_work(self) -> None:
        old = self.commit_task("in_progress", minimal=True)
        before = self.preserved_snapshot()
        source = {"kind": "issue", "repo_ref": "castbox/guru-trellis", "number": 495,
                  "disposition": "reference_only"}
        output = self.upgrade(old, source)
        self.assertEqual(output["exit_id"], "upgraded", output)
        self.reenter_current_owners("in_progress")
        self.fresh_planning_approval()
        resumed = {"profile": "resume_current_task", "mode": "standalone",
                   "task_id": self.task_id, "lifecycle_generation": 0,
                   "continuation_id": "fresh-review-dev-check"}
        owner = {**resumed, "route": "resume", "resume_target": "phase-2",
                 "ai_review_gate": {"status": "passed",
                                    "summary": "Fresh current Planning approved the unchanged bounded fixture; resume current development/check."}}
        self.assertEqual(self.public("guru-bind-task-session", resumed, owner=owner)["resume_target"], "phase-2")
        self.assertEqual(git(self.root, "rev-parse", "HEAD"), self.pre_migration_head)
        self.assertEqual(self.preserved_snapshot(), before)
        current = json.loads((self.root / self.task_ref / "task.json").read_text())
        self.assertEqual(current["createdAt"], "")
        self.assertEqual(current["children"], [])
        self.assertEqual(current["priority"], "P2")
        self.assertEqual(current["status"], "in_progress")
        self.assertEqual(current["source"], source)
        business_status = git(self.root, "status", "--porcelain=v1", "--", "business.txt", "unrelated.txt", "untracked-note.txt")
        self.assertEqual(business_status, "M business.txt\n M unrelated.txt\n?? untracked-note.txt")

    def test_upgraded_installation_creates_new_task_through_current_creator(self) -> None:
        old = self.commit_task("planning")
        source = {"kind": "issue", "repo_ref": "castbox/guru-trellis", "number": 495,
                  "disposition": "exact_source"}
        output = self.upgrade(old, source)
        self.assertEqual(output["exit_id"], "upgraded", output)
        self.reenter_current_owners("planning")
        self.assertEqual(json.loads((self.root / self.task_ref / "task.json").read_text())["source"], source)
        # An isolated fixture commit makes the ordinary clean acquisition path
        # real. This is not a Guru/Fork work commit or a prerequisite for resume.
        git(self.root, "add", ".")
        git(self.root, "commit", "-qm", "isolated completed installation baseline")
        head = git(self.root, "rev-parse", "HEAD")
        git(self.root, "branch", "fixture-new-base", head)
        git(self.root, "switch", "-qc", "task/new-current")
        prefix = datetime.now(ZoneInfo("Asia/Shanghai")).strftime("%m-%d")
        new_id = "new-current-task"
        new_ref = f".trellis/tasks/{prefix}-{new_id}"
        payload = {
            "profile": "task_creation", "action": "create_task",
            "creation": {
                "task_id": new_id, "task_ref": new_ref, "source_profile": "standalone_request",
                "reviewed_source": {"kind": "no_issue"}, "accepted_scope_identity": "scope:fixture-new-current",
                "delivery_target": {"repo_ref": "castbox/guru-trellis", "branch_ref": "fixture-new-base"},
                "selected_base_ref": "fixture-new-base", "reviewed_base_head": head,
            },
            "acquisition": {
                "route": "adopt_invocation_checkout", "branch_ref": "task/new-current",
                "decision_head": head, "transaction_id": "acquisition:fixture-new-current",
                "result_id": "checkout:fixture-new-current", "invocation_checkout": str(self.root),
            },
            "task": {"title": "新版正式 creator 样本", "description": "Current task creation after migration.",
                     "scope": "isolated new task fixture"},
        }
        created = self.public("guru-create-task", payload,
                              environment={"TRELLIS_CONTEXT_ID": "migration-495-new"})
        self.assertEqual(created["exit_id"], "created", created)
        task = json.loads((self.root / new_ref / "task.json").read_text())
        self.assertEqual((task["id"], task["lifecycle_generation"], task["source"]),
                         (new_id, 0, {"kind": "no_issue"}))
        self.assertNotIn("creator", task)
        self.assertNotIn("assignee", task)
        checkout = self.public("guru-ensure-task-checkout", {
            "profile": "active_task", "mode": "standalone", "task_id": new_id, "lifecycle_generation": 0,
        })
        self.assertEqual(checkout["exit_id"], "checkout_resolved", checkout)
        self.assertEqual(checkout["task_ref"], new_ref)
        identity = self.public("guru-establish-task-identity", {
            "profile": "active_task", "mode": "standalone", "task_id": new_id,
            "task_ref": new_ref, "lifecycle_generation": 0,
        })
        self.assertEqual(identity["exit_id"], "identity_established", identity)
        self.assert_native_session(new_id, new_ref, context="migration-495-new")
        unsupported = self.public("guru-establish-task-identity", {
            "profile": "active_task", "mode": "standalone", "task_id": self.deferred_id,
            "task_ref": self.deferred_ref, "lifecycle_generation": 0,
        })
        self.assertEqual(unsupported, {"exit_id": "blocked", "reason_code": "unsupported_legacy_task"})
        before_collision = git(self.root, "status", "--porcelain=v1", "--untracked-files=all")
        for reserved_id in (self.deferred_id, self.deferred_id.upper()):
            collision = self.native([".trellis/scripts/task.py", "create", "Identity already reserved",
                                     "--description", "A current creator must reject the old reserved identity.",
                                     "--task-id", reserved_id, "--slug", "old-id-reuse",
                                     "--source-json", '{"kind":"no_issue"}', "--no-start"])
            self.assertNotEqual(collision.returncode, 0, collision.stdout + collision.stderr)
            self.assertIn("task_id_collision", collision.stderr, collision.stdout + collision.stderr)
        self.assertEqual(git(self.root, "status", "--porcelain=v1", "--untracked-files=all"), before_collision)
        self.assertEqual((self.root / self.deferred_ref / "task.json").read_bytes(), self.deferred_before)

    def partial_with_preserved_edit(self) -> tuple[dict, Path]:
        old = self.commit_task("planning")
        edited = ".codex/skills/guru-check-task/SKILL.md"
        path = self.root / edited
        path.write_text(path.read_text() + "\n# Ordinary project-local guidance\n")
        partial = self.upgrade(old, {"kind": "no_issue"}, preserve_edit=edited)
        self.assertEqual(partial["exit_id"], "resume_required", partial)
        converted = json.loads((self.root / self.task_ref / "task.json").read_text())
        self.assertEqual(converted["lifecycle_generation"], 0)
        return partial, path

    def test_partial_resume_does_not_absorb_new_task_work_into_rollback(self) -> None:
        partial, path = self.partial_with_preserved_edit()
        metadata = self.native([".trellis/scripts/task.py", "set-meta", self.task_ref,
                                "post_upgrade_business_work", "normal-new-task-metadata"], source_owned=True)
        self.assertEqual(metadata.returncode, 0, metadata.stdout + metadata.stderr)
        # The owned fixture's conflicting file is now explicitly resolved to
        # the canonical installation; no checkpoint or gate is fabricated.
        path.unlink()
        path.with_name(path.name + ".new").unlink(missing_ok=True)
        resumed = self.public("guru-upgrade-installation", {
            "profile": "resume", "recovery_ref": partial["recovery_ref"],
        })
        self.assertEqual(resumed["exit_id"], "upgraded", resumed)
        task_path = self.root / self.task_ref / "task.json"
        before_rollback = task_path.read_bytes()
        self.assertEqual(json.loads(before_rollback)["meta"]["post_upgrade_business_work"], "normal-new-task-metadata")
        blocked = self.public("guru-upgrade-installation", {
            "profile": "rollback", "recovery_ref": resumed["recovery_ref"],
        })
        self.assertEqual(blocked, {"exit_id": "blocked", "reason": "task_work_since_core_migration"})
        self.assertEqual(task_path.read_bytes(), before_rollback)
        self.assertEqual((self.root / self.deferred_ref / "task.json").read_bytes(), self.deferred_before)

    def test_partial_rejected_resume_preserves_new_deferred_business_notes(self) -> None:
        partial, _ = self.partial_with_preserved_edit()
        path = self.root / self.deferred_ref / "task.json"
        # Ordinary editing of the still-old business task's notes; no checkpoint,
        # decision hash, source identity, or review evidence is altered.
        record = json.loads(path.read_text())
        record["notes"] = "Ordinary deferred business notes added during partial installation."
        write_json(path, record)
        before_rollback = path.read_bytes()
        resumed = self.public("guru-upgrade-installation", {
            "profile": "resume", "recovery_ref": partial["recovery_ref"],
        })
        self.assertEqual(resumed["exit_id"], "resume_required", resumed)
        blocked = self.public("guru-upgrade-installation", {
            "profile": "rollback", "recovery_ref": partial["recovery_ref"],
        })
        self.assertEqual(blocked, {"exit_id": "blocked", "reason": "task_work_since_core_migration"})
        self.assertEqual(path.read_bytes(), before_rollback)

    def test_partial_resolution_without_new_work_rolls_back_exact_legacy_state(self) -> None:
        old = self.commit_task("planning")
        edited = ".codex/skills/guru-check-task/SKILL.md"
        path = self.root / edited
        path.write_text(path.read_text() + "\n# Ordinary project-local guidance\n")

        def repository_bytes_and_modes() -> dict:
            process = run(self.root, ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"])
            self.assertEqual(process.returncode, 0, process.stderr)
            return {relative: (digest(self.root / relative), (self.root / relative).stat().st_mode & 0o777)
                    for relative in process.stdout.split("\0") if relative and (self.root / relative).is_file()}

        before = repository_bytes_and_modes()
        before_status = git(self.root, "status", "--porcelain=v1", "--untracked-files=all")
        head = git(self.root, "rev-parse", "HEAD")
        partial = self.upgrade(old, {"kind": "no_issue"}, preserve_edit=edited)
        self.assertEqual(partial["exit_id"], "resume_required", partial)
        path.unlink()
        path.with_name(path.name + ".new").unlink(missing_ok=True)
        resumed = self.public("guru-upgrade-installation", {
            "profile": "resume", "recovery_ref": partial["recovery_ref"],
        })
        self.assertEqual(resumed["exit_id"], "upgraded", resumed)
        self.assert_live_installed()
        rolled_back = self.public("guru-upgrade-installation", {
            "profile": "rollback", "recovery_ref": resumed["recovery_ref"],
        })
        self.assertEqual(rolled_back, {"exit_id": "rolled_back", "installed_version": "0.6.16-guru.41"})
        self.assertEqual(repository_bytes_and_modes(), before)
        self.assertEqual(git(self.root, "status", "--porcelain=v1", "--untracked-files=all"), before_status)
        self.assertEqual(git(self.root, "rev-parse", "HEAD"), head)
        self.assertEqual((self.root / ".trellis/.version").read_text().strip(), "0.6.16")
        self.assertEqual(json.loads((self.root / self.task_ref / "task.json").read_text()), old)
        self.assertFalse((self.root / ".git/guru-team/install-upgrade" / resumed["recovery_ref"]).exists())
        # Execute the restored old native CLI against its restored old task
        # store; no current lifecycle adapter substitutes for this smoke.
        smoke = self.native([".trellis/scripts/task.py", "list"], source_owned=True)
        self.assertEqual(smoke.returncode, 0, smoke.stdout + smoke.stderr)
        self.assertIn("legacy-task", smoke.stdout)
        self.assertEqual(repository_bytes_and_modes(), before)


if __name__ == "__main__":
    unittest.main()
