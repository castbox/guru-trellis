"""Real public Intake chain for an uncommitted draft and a fixed Git tree."""
from __future__ import annotations

import copy
import hashlib
import json
import os
import sys
import subprocess
import tempfile
import unittest
from pathlib import Path

SKILLS = Path(__file__).resolve().parents[3]
PACKAGES = SKILLS / "packages"


def sha(data):
    return hashlib.sha256(data.encode() if isinstance(data, str) else data).hexdigest()


def digest(value):
    return sha(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")))


class ReadBaselineChainTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="guru-read-baseline-")
        self.addCleanup(self.tmp.cleanup)
        self.environment = dict(os.environ)
        provider = Path(self.tmp.name) / "provider"
        provider.mkdir()
        gh = provider / "gh"
        gh.write_text("#!" + sys.executable + "\nimport json,sys\nif sys.argv[1:3] != ['issue','list']: raise SystemExit(2)\nprint(json.dumps([]))\n")
        gh.chmod(0o755)
        self.environment["PATH"] = str(provider) + os.pathsep + self.environment["PATH"]
        self.root = Path(self.tmp.name) / "repository"
        self.git("init", "-b", "main", str(self.root), cwd=Path(self.tmp.name))
        self.git("config", "user.email", "fixture@example.invalid")
        self.git("config", "user.name", "Fixture")
        self.files = {"docs/requirements.md": "固定来源需求。\n", "src/runtime.py": "VALUE = 1\n", "tests/test_runtime.py": "assert 1 == 1\n"}
        for relative, content in self.files.items():
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
        self.git("add", ".")
        self.git("commit", "-m", "fixed baseline")
        self.commit = self.git("rev-parse", "HEAD")
        self.git("remote", "add", "origin", "https://github.com/example/guru-extension.git")
        self.worktree = Path(self.tmp.name) / "external-worktree"
        self.git("worktree", "add", "-b", "external-draft", str(self.worktree))
        self.body = "目标：读取固定来源。\n约束：保留草案。\n验收：返回当前结果。\n"
        self.title = "固定来源草案"
        self.draft_id = "draft:" + sha(self.body)
        self.draft = self.worktree / "draft.md"
        self.draft.write_text(self.body)
        (self.root / "unrelated.txt").write_text("unrelated dirty baseline checkout\n")
        # Different execution-tree content must never substitute for baseline blobs.
        (self.worktree / "docs/requirements.md").write_text("工作区文档与基线不同。\n")
        self.clues = {key: [] for key in ("issue_refs", "pr_refs", "branches", "paths", "commands", "config_keys", "schema_fields", "symbols", "terms", "queries")}
        self.clues["paths"] = ["docs/requirements.md"]
        self.clues["terms"] = ["固定来源"]

    def git(self, *args, cwd=None):
        result = subprocess.run(["git", *args], cwd=cwd or self.root, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout.strip()

    def call(self, skill, wrapper, data=None, args=(), expected=0):
        command = [str(PACKAGES / skill / "scripts" / wrapper), *args]
        result = subprocess.run(command, input=json.dumps(data, ensure_ascii=False) if data is not None else None,
                                text=True, capture_output=True, env=self.environment)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        output = json.loads(result.stdout)
        if "exit_id" in output:
            self.validate_consumer(skill, output)
        return output["result"] if output.get("formal_exit") is False else output

    def validate_consumer(self, skill, output):
        from runtime.schema import validate_json
        package=PACKAGES/skill
        contracts=json.loads((package/"interface.json").read_text())["public_contracts"]
        declaration=next(row for row in contracts["outputs"] if row["exit_id"]==output["exit_id"])
        validate_json(output, package/declaration["schema"]["path"], "actual_stdout")
        projection=next(row for row in contracts["projections"] if row["exit_id"]==output["exit_id"])
        consumer=next(row for row in contracts["consumer_inputs"] if row["id"]==projection["consumer_input_id"])
        contract=consumer.get("contract",{})
        if contract.get("kind")=="json_schema":
            value=output if projection["operation"]=="direct" else {row["target"]:output[row["source"]] for row in projection.get("mappings",[]) if row["source"] in output}
            path=package/contract["path"]
            validate_json(value,path if path.is_file() else SKILLS/contract["path"],"actual_consumer")

    def invoke(self, skill, envelope, expected=0):
        return self.call(skill, "invoke.sh", envelope, ("--invocation", "-"), expected)

    def baseline(self, ref="refs/heads/main", commit=None):
        public = {"source_exit": "start", "mode": "workflow", "route": "repo_change", "operation": "read",
                  "repo_root": str(self.worktree), "base_ref": ref}
        if commit is not None:
            public["base_commit"] = commit
        return self.invoke("guru-sync-base", {"schema_version": "1.0", "public_input": public})

    def projection(self, skill, output):
        interface = json.loads((PACKAGES / skill / "interface.json").read_text())
        contract = interface["public_contracts"]
        projection = next(row for row in contract["projections"] if row["exit_id"] == output["exit_id"])
        self.assertEqual(projection["operation"], "rename")
        return {row["target"]: copy.deepcopy(output[row["source"]]) for row in projection["mappings"] if row["source"] in output}

    def context(self, baseline, public=None):
        transition = baseline["transition"]
        public = public or {**self.projection("guru-sync-base", baseline), "change_input": self.clues,
                            "clarify_profile": "standard_intake", "candidate_file": str(self.draft)}
        package = PACKAGES / "guru-discover-change-context"
        # This is the current owner's semantic authoring seed. Every upstream
        # transition below comes only from an actual public invoke result.
        owner = json.loads((package / "examples/change-context-owner-result-3.0.json").read_text())
        owner["repository"] = {"repo": "example/guru-extension", "source_kind": "git_object",
                               "selected_ref": transition["base"]["selected_ref"], "commit": self.commit}
        owner["live_change"] = {"kind": "draft", "identity": self.draft_id, "state": "draft",
                                "updated_at": "2026-01-01T00:00:00Z", "body_sha256": sha(self.body),
                                "facts_sha256": digest({"body": self.body}), "issue_binding": None}
        searched=subprocess.run(["gh","issue","list","--repo","example/guru-extension","--state","open","--search","fixed baseline","--json","number,url,state,updatedAt"],text=True,capture_output=True,env=self.environment,check=True)
        owner["duplicate_search"]["candidates"] = json.loads(searched.stdout)
        for section, relative in zip(("docs", "code_contracts", "tests"), self.files):
            observed = self.call("guru-discover-change-context", "read-change-context-source.sh",
                                 args=("--source-transition", json.dumps(transition), "--path", relative))
            self.assertEqual(observed["content"], self.files[relative])
            self.assertEqual(observed["commit"], self.commit)
            owner["current_state"][section] = [{"path": relative, "blob_or_content_sha256": observed["blob"],
                                               "purpose": "Read selected source", "observation": "The fixed source is available.", "query_clues": ["固定来源"]}]
        envelope = {"schema_version": "1.0", "public_input": public, "transition": transition, "owner_context": {}, "owner_result": owner}
        envelope["owner_result"] = self.call("guru-discover-change-context", "record-context-discovery.sh", envelope,
                                             ("--root", str(self.worktree), "--invocation", "-"))
        checked = self.call("guru-discover-change-context", "check-context-discovery.sh", envelope,
                            ("--root", str(self.worktree), "--invocation", "-"))
        self.assertEqual(checked["typed_exit"], "context_ready")
        return self.invoke("guru-discover-change-context", envelope), envelope

    def clarify(self, context, needs_context=False):
        package = PACKAGES / "guru-clarify-requirements"
        owner = json.loads((package / "examples/requirements-clarification.json").read_text())
        owner.pop("content_identity")
        owner["mode"] = "workflow"
        owner["review_target"].update(body_sha256=sha(self.body), updated_at=None)
        owner["review_target"].pop("facts_sha256")
        owner["context_evidence"]["evidence_refs"] = [context["transition"]["context_result_sha256"]]
        disposition = owner["target_disposition"]
        disposition.pop("disposition_digest")
        snapshot = context["duplicate_snapshot"]
        disposition.update(duplicate_query=snapshot["query"], duplicate_checked_at=snapshot["checked_at"],
                           duplicate_facts_sha256=snapshot["facts_sha256"], duplicate_candidates=[])
        for action in owner["source_actions"]:
            action.pop("payload_sha256", None)
            action.pop("action_digest", None)
        if needs_context:
            owner.update(typed_exit="needs_context", consumer={"kind": "skill", "id": "guru-discover-change-context"})
            owner["context_evidence"].update(status="missing", missing_reason="Reread the fixed evidence for this question.")
        recorded = self.call("guru-clarify-requirements", "record-requirements-clarification.sh", owner,
                             ("--mode", "workflow", "--input", "-"))
        checked = self.call("guru-clarify-requirements", "check-requirements-clarification.sh", recorded, ("--input", "-"))
        self.assertEqual(checked["typed_exit"], owner["typed_exit"])
        public = self.projection("guru-discover-change-context", context)
        return self.invoke("guru-clarify-requirements", {"schema_version": "1.0", "public_input": public,
                                                         "transition": context["transition"], "owner_context": {}, "owner_result": recorded})

    def wording(self, clear):
        source = {"source_kind": "draft", "identity": self.draft_id, "title": self.title, "body": self.body, "updated_at": None}
        envelope = {"profile": "change_request", "mode": "workflow", "change_request": source, "owner_result": {}}
        scanned = self.call("guru-review-contract-wording", "record-contract-wording-review.sh", envelope,
                            ("--root", str(self.worktree), "--invocation", "-", "--scan-only"))
        envelope["owner_result"] = {"generated_at": "2026-01-01T00:00:00Z", "typed_exit": "pass", "revisions": [],
            "classifications": [{"hit_id": hit["hit_id"], "classification": "term_definition", "reason": "The term preserves the declared meaning."} for hit in scanned["scan"]["hits"]],
            "ai_review_gate": {"status": "passed", "reviewer": "test-owner", "summary": "The fixed title/body scope is clear.",
                "checked_dimensions": {key: True for key in ("complete_profile_scope", "all_hits_classified", "zero_unchecked_hits", "product_semantics_preserved", "retained_reasons_sufficient", "zero_hits_not_requirement_review")}}}
        recorded = self.call("guru-review-contract-wording", "record-contract-wording-review.sh", envelope,
                             ("--root", str(self.worktree), "--invocation", "-"))
        envelope["owner_result"] = recorded
        checked = self.call("guru-review-contract-wording", "check-contract-wording-review.sh", envelope,
                            ("--root", str(self.worktree), "--invocation", "-"))
        public = {"profile": "change_request", "source_exit": "clear", "mode": "workflow", "target_locator": self.draft_id, "continuation_id": "stage0-current"}
        return self.invoke("guru-review-contract-wording", {"schema_version": "1.0", "public_input": public,
            "transition": clear["transition"], "owner_context": {}, "owner_result": recorded, "validation_receipt": checked["validation_receipt"]})

    def readiness(self, wording):
        seed = json.loads((PACKAGES / "guru-review-change-request/examples/issue-review.json").read_text())
        owner = {key: seed[key] for key in ("generated_at", "semantic_review", "reason")}
        authority = {"kind": "draft", "repo": "example/guru-extension", "issue_number": None, "url": None, "state": "draft", "updated_at": None, "body_sha256": sha(self.body)}
        owner.update(mode="workflow", typed_exit="ready", consumer={"kind": "workflow", "id": "guru-task-intake-router"},
                     target={"kind": "proposed_draft", "repo": "example/guru-extension", "draft_id": self.draft_id, "source_request_sha256": digest(authority)})
        owner["affected_evidence"] = [{"ref": "transition.context_result_sha256", "sha256": wording["transition"]["context_result_sha256"], "summary": "Current fixed source."}]
        gate = owner["semantic_review"]["ai_review_gate"]
        owner["semantic_review"]["ai_review_gate"] = {key: gate[key] for key in ("status", "reviewer", "summary")}
        for row in owner["semantic_review"]["dimensions"]:
            row.update(evidence_refs=["transition.context_result_sha256"], affected_hashes=[wording["transition"]["context_result_sha256"]])
        envelope = {"schema_version": "1.0", "public_input": {"profile": "proposed_draft", "source_exit": "pass", "mode": "workflow", "target_locator": self.draft_id, "continuation_id": "stage0-current"},
                    "transition": wording["transition"], "owner_context": {"change_request": {"kind": "draft", "draft_id": self.draft_id, "title": self.title, "body": self.body}}, "owner_result": owner}
        envelope["owner_result"] = self.call("guru-review-change-request", "record-change-request-review.sh", envelope, ("--root", str(self.worktree), "--invocation", "-"))
        checked = self.call("guru-review-change-request", "check-change-request-review.sh", envelope, ("--root", str(self.worktree), "--invocation", "-"))
        envelope["validation_receipt"] = checked["validation_receipt"]
        return self.invoke("guru-review-change-request", envelope), envelope

    def test_fixed_tree_and_untracked_draft_reach_readiness_and_issue_plan(self):
        before = self.git("status", "--porcelain=v1", cwd=self.worktree)
        baseline = self.baseline(commit=self.commit)
        self.assertEqual(baseline["exit_id"], "baseline_ready")
        self.assertNotIn("decision_head", baseline["transition"]["base"])
        context, _ = self.context(baseline)
        # Exercise the original needs_context return instead of inventing a base.
        returning = self.clarify(context, needs_context=True)
        request = self.projection("guru-clarify-requirements", returning)
        request["change_input"] = self.clues
        context, _ = self.context(returning, request)
        ready, envelope = self.readiness(self.wording(self.clarify(context)))
        self.assertEqual(ready["exit_id"], "ready")
        self.assertEqual(ready["transition"]["base"], baseline["transition"]["base"])
        target = ready["transition"]["target"]
        data = {"profile": "issue_creation", "action": "create_issue", "ready_target_kind": "proposed_draft", "reviewed_target": target,
                "reviewed_label_identity_sha256": digest({"reviewed_target": target["identity_sha256"], "labels": []}),
                "draft": {"repo_ref": "example/guru-extension", "title": self.title, "body": self.body, "labels": [], "duplicate_disposition": "create_new"}, "reviewed_at": "2026-01-01T00:00:00Z"}
        plan = self.command("guru-create-issue", "record-issue-creation-plan", data)
        self.assertEqual(plan["status"], "ready")
        self.assertEqual(self.git("rev-parse", "HEAD"), self.commit)
        self.assertEqual(self.git("status", "--porcelain=v1", cwd=self.worktree), before)
        self.assertEqual(self.draft.read_text(), self.body)
        self.draft.write_text(self.body + "新增条件。\n")
        failed = self.invoke("guru-review-change-request", envelope, expected=3)
        self.assertEqual(failed["code"], "stale_identity")

    def command(self, skill, command, data):
        # The production launcher dispatches the package's declared command.
        result = subprocess.run([str(SKILLS / "runtime/launch.sh"), str(PACKAGES / skill), command, "--input", "-"], input=json.dumps(data), text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return json.loads(result.stdout)["result"]

    def test_ref_without_checkout_and_later_ref_advance_keep_adopted_commit(self):
        self.git("branch", "never-checked-out")
        baseline = self.baseline("refs/heads/never-checked-out", self.commit)
        self.assertEqual(baseline["exit_id"], "baseline_ready")
        # Ordinary branch work advances the ref after the baseline was adopted.
        self.git("checkout", "never-checked-out")
        (self.root / "later.txt").write_text("later\n")
        self.git("add", "later.txt")
        self.git("commit", "-m", "later work")
        context, _ = self.context(baseline)
        self.assertEqual(context["transition"]["base"]["commit"], self.commit)
        self.assertNotEqual(self.git("rev-parse", "HEAD"), self.commit)
        mismatch = self.invoke("guru-sync-base", {"schema_version": "1.0", "public_input": {"source_exit": "start", "mode": "workflow", "operation": "read", "repo_root": str(self.worktree), "base_ref": "refs/heads/never-checked-out", "base_commit": self.commit}}, expected=3)
        self.assertEqual(mismatch["field_path"], "base_commit")

    def test_fixed_archive_preview_uses_baseline_without_target_installation(self):
        index={"problem":"Fixed history", "outcome":"Original recorded result", "changed_behavior":["Fixed history is available"],
               "affected_surfaces":[{"kind":"docs","name":"history","paths":["docs/requirements.md"],"change":"Original source"}],
               "contract_changes":[], "search_terms":{key:[] for key in ("issue_refs","pr_refs","branches","paths","commands","config_keys","schema_fields","symbols")},
               "retrieval_text":"fixed history"}
        index["search_terms"]["phrases"]=["fixed history", "original source", "recorded result"]
        relative=".trellis/tasks/archive/2026-01/fixture/finish-summary.json"
        path=self.root/relative;path.parent.mkdir(parents=True);path.write_text(json.dumps({"index":index}))
        self.git("add",relative);self.git("commit","-m","historical fixture outside the tested writer boundary")
        self.commit=self.git("rev-parse","HEAD")
        draft_copy=self.worktree/relative;draft_copy.parent.mkdir(parents=True);draft_copy.write_text(json.dumps({"index":{**index,"problem":"Uncommitted history edit"}}))
        baseline=self.baseline(commit=self.commit)
        result=self.call("guru-discover-change-context","preview-change-context-history.sh",args=("--root",str(self.worktree),"--source-transition",json.dumps(baseline["transition"]),"--query-json",json.dumps({"terms":["fixed history"]})))
        self.assertEqual(result["manifest"][0]["status"],"valid")
        self.assertEqual(result["candidates"][0]["index_projection"]["problem"],"Fixed history")
        self.assertFalse((self.worktree/".trellis/guru-team").exists())

    def test_read_reuses_config_selection_without_a_base_checkout(self):
        self.git("branch","configured-base")
        config=self.worktree/".trellis/guru-team/config.yml";config.parent.mkdir(parents=True);config.write_text("base_branch: configured-base\n")
        output=self.invoke("guru-sync-base",{"schema_version":"1.0","public_input":{"source_exit":"start","mode":"workflow","operation":"read","repo_root":str(self.worktree)}})
        self.assertEqual(output["transition"]["base"]["source"],"config")
        self.assertEqual(output["transition"]["base"]["selected_ref"],"refs/heads/configured-base")
        self.assertEqual(output["transition"]["base"]["commit"],self.commit)

    def test_actual_sync_still_rejects_dirty_authority(self):
        output = self.invoke("guru-sync-base", {"schema_version": "1.0", "public_input": {"source_exit": "start", "mode": "workflow", "operation": "sync", "repo_root": str(self.worktree), "base_branch": "main"}})
        self.assertEqual(output, {"exit_id": "blocked"})


if __name__ == "__main__":
    unittest.main()
