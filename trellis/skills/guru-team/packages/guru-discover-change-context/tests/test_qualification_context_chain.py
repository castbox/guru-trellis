"""Qualification -> Clarify -> Sync/Discovery -> clear, through real wrappers.

The fixture establishes Task/Delivery before this boundary. A repo-bound gh
substitute is the external boundary; semantic payloads exercise transport and
factual validation, not real Agent judgment or remote GitHub effects.
"""
from __future__ import annotations
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

SKILLS = Path(__file__).resolve().parents[3]
PACKAGES = SKILLS / "packages"
sys.path.insert(0, str(SKILLS))
from runtime.schema import validate_json
from runtime.discovery import select_authoring_profile

spec = importlib.util.spec_from_file_location("qualification_identity_fixture", SKILLS / "runtime/tests/test_qualification_identity.py")
identity_fixture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(identity_fixture)


def sha(value):
    return hashlib.sha256(value.encode() if isinstance(value, str) else value).hexdigest()


def digest(value):
    return sha(json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")))


class QualificationContextChainTests(unittest.TestCase):
    def setUp(self):
        self.no_issue = self._testMethodName.endswith("no_issue")
        no_issue = self.no_issue
        class Fixture(identity_fixture.QualificationIdentityTest):
            def owner(inner, skill, public, **kwargs):
                if skill == "guru-create-task" and not no_issue:
                    public = copy.deepcopy(public)
                    public["creation"].update(source_profile="existing_issue", reviewed_source={
                        "kind": "issue", "repo_ref": "castbox/guru-trellis", "number": 811,
                        "disposition": "exact_source"})
                return super().owner(skill, public, **kwargs)
        self.fixture = Fixture("test_three_public_wrappers_accept_real_explicit_identity_and_keep_continuation")
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.root = self.fixture.root
        self.installed = self.root / ".trellis/guru-team/skills/packages"
        self.fixture.fixture.git("remote", "add", "origin", "https://github.com/castbox/guru-trellis.git")
        self.commit = self.fixture.head
        self.authority = self.fixture.ref + "/prd.md" if self.no_issue else "https://github.com/castbox/guru-trellis/issues/811"
        self.state = self.root.parent / "github-state.json"
        self.state.write_text(json.dumps({"body": "Current source requirements.\n", "updated_at": "2026-01-01T00:00:00Z", "writes": 0}))
        provider = self.root.parent / "provider"
        provider.mkdir()
        gh = provider / "gh"
        gh.write_text("#!" + sys.executable + "\n" + """import json,os,pathlib,sys
p=pathlib.Path(os.environ['GURU_TEST_GH_STATE']); state=json.loads(p.read_text());args=sys.argv[1:]
if args[:2]==['issue','list']:
 print(json.dumps([dict(number=812,url="https://github.com/castbox/guru-trellis/issues/812",state="OPEN",updatedAt="2026-01-01T00:00:00Z")]))
elif args[:2]==['api','repos/castbox/guru-trellis/issues/811/comments'] and '--method' in args and args[args.index('--method')+1]=='POST':
 payload=json.load(sys.stdin);state.update(comment_body=payload['body'],updated_at='2026-01-03T00:00:00Z',writes=state['writes']+1);p.write_text(json.dumps(state));print(json.dumps(dict(body=state['comment_body'],url='https://github.com/castbox/guru-trellis/issues/811#issuecomment-1',updated_at=state['updated_at'])))
elif args[:2]==['api','repos/castbox/guru-trellis/issues/comments/1']:
 print(json.dumps(dict(body=state['comment_body'],url='https://github.com/castbox/guru-trellis/issues/811#issuecomment-1',updated_at=state['updated_at'])))
elif args[:2]==['api','repos/castbox/guru-trellis/issues/811']:
 if '--method' in args and args[args.index('--method')+1]=='PATCH':
  payload=json.load(sys.stdin);state.update(body=payload['body'],updated_at='2026-01-02T00:00:00Z',writes=state['writes']+1);p.write_text(json.dumps(state))
 print(json.dumps(dict(state,number=811,url='https://github.com/castbox/guru-trellis/issues/811',state='open')))
else: raise SystemExit(2)
""")
        gh.chmod(0o755)
        self.environment = dict(os.environ, PATH=str(provider) + os.pathsep + os.environ["PATH"], GURU_TEST_GH_STATE=str(self.state))
        self.clues = {key: [] for key in ("issue_refs", "pr_refs", "branches", "paths", "commands", "config_keys", "schema_fields", "symbols", "terms", "queries")}
        self.clues["issue_refs"] = [] if self.no_issue else ["#811"]
        self.clues["paths"] = [self.authority] if self.no_issue else ["README.md"]

    def gh(self, *args, body=None):
        process = subprocess.run(["gh", *args], cwd=self.root, input=json.dumps(body) if body is not None else None,
                                 text=True, capture_output=True, env=self.environment)
        self.assertEqual(process.returncode, 0, process.stderr)
        return json.loads(process.stdout)

    def call(self, skill, wrapper, payload, args=("--invocation", "-"), expected=0):
        process = subprocess.run(["bash", str(self.installed / skill / "scripts" / wrapper), *args], cwd=self.root,
                                 input=json.dumps(payload, ensure_ascii=False), text=True, capture_output=True, env=self.environment)
        self.assertEqual(process.returncode, expected, process.stdout + process.stderr)
        result = json.loads(process.stdout)
        if result.get("formal_exit") is False:
            return result["result"]
        return result

    def invoke(self, skill, payload, expected=0):
        return self.call(skill, "invoke.sh", payload, expected=expected)

    def projection(self, skill, output):
        contracts = json.loads((self.installed / skill / "interface.json").read_text())["public_contracts"]
        declared = next(row for row in contracts["outputs"] if row["exit_id"] == output["exit_id"])
        validate_json(output, self.installed / skill / declared["schema"]["path"], "actual_stdout")
        projection = next(row for row in contracts["projections"] if row["exit_id"] == output["exit_id"])
        value = copy.deepcopy(output) if projection["operation"] == "direct" else {
            row["target"]: copy.deepcopy(output[row["source"]]) for row in projection["mappings"] if row["source"] in output}
        consumer = next(row for row in contracts["consumer_inputs"] if row["id"] == projection["consumer_input_id"])
        if consumer["contract"]["kind"] == "skill_input_authoring_seed":
            selected = select_authoring_profile(consumer["contract"], output)
            self.assertEqual(set(value), set(selected["seed_fields"]))
            self.assertFalse(set(value) & set(selected["authoring_fields"]))
            self.assertIn("change_input", selected["authoring_fields"])
        if consumer["contract"]["kind"] == "json_schema":
            validate_json(value, self.root / ".trellis/guru-team/skills" / consumer["contract"]["path"], "actual_consumer")
        return value

    def qualify(self, name, confirmed=False, task_bound=True, candidate=None):
        semantic = self.fixture.semantic(name)
        if not task_bound:
            public = semantic["public_input"]
            public.update(profile="requirements_scope_set", caller="guru-clarify-requirements", target_locator=self.authority,
                target={"repo_locator":".", "authority_kind":"issue", "authority_locator":self.authority, "authority_identity":"issue-current", "scope_locator":"path:README.md"})
        if candidate is not None:
            semantic["public_input"]["candidate_refs"]=[candidate]
            semantic["public_input"]["candidate_locators"]=[{"candidate_ref":candidate,"locators":["path:README.md"]}]
            semantic["candidate_results"][0]["candidate_ref"]=candidate
            semantic["ai_review_gate"]["reviewed_candidate_refs"]=[candidate]
        semantic["candidate_results"][0]["decision"] = "qualified_current" if confirmed else "scope_confirmation_required"
        semantic["typed_exit"] = "classified" if confirmed else "scope_confirmation_required"
        semantic["consumer"] = {"kind": "workflow", "id": "guru-" + ("normal-scenario" if name == "normal-scenario" else "solution-mechanism") + "-classified-router"} if confirmed else {"kind": "skill", "id": "guru-clarify-requirements"}
        return self.invoke("guru-qualify-" + name, {"schema_version": "1.0", "semantic_result": semantic})

    def baseline(self, public=None):
        return self.invoke("guru-sync-base", {"schema_version": "1.0", "public_input": public or {
            "source_exit": "start", "mode": "workflow", "route": "repo_change", "operation": "read",
            "repo_root": str(self.root), "base_ref": self.commit}})

    def review_target(self):
        if self.no_issue:
            return {"kind":"draft", "repo":"castbox/guru-trellis", "issue_number":None, "url":None, "state":"draft", "updated_at":None, "body_sha256":sha((self.root/self.authority).read_bytes())}
        live = self.gh("api", "repos/castbox/guru-trellis/issues/811")
        return {"kind": "issue", "repo": "castbox/guru-trellis", "issue_number": 811, "url": self.authority,
                "state": "open", "updated_at": live["updated_at"], "body_sha256": sha(live["body"])}

    def clarify(self, public, transition, exit_id="clear", mutation=False, expected=0):
        owner = json.loads((PACKAGES / "guru-clarify-requirements/examples/requirements-clarification.json").read_text())
        owner.pop("content_identity")
        owner.update(schema_version="5.0", mode=public["mode"], typed_exit=exit_id, review_target=self.review_target(), target_disposition=None,
                     invocation_context={"kind": public["profile"], "caller": "guru-qualify-normal-scenario" if public["profile"].startswith("normal") else "guru-qualify-solution-mechanism",
                        "task_locator": public.get("task_ref"), **{k:public[k] for k in ("target_locator", "continuation_id", "resume_target", "candidate_refs", "task_ref", "delivery_key") if k in public}},
                     consumer={"kind": "skill", "id": "guru-discover-change-context"} if exit_id == "needs_context" else
                        {"kind": "skill", "id": "guru-sync-base"} if exit_id == "refresh_context" else {"kind": "workflow", "id": "guru-requirements-clear-router"})
        owner["context_evidence"].update(status="missing" if exit_id == "needs_context" else "current",
            missing_reason="Obtain current confirmation context." if exit_id == "needs_context" else None,
            evidence_refs=[transition["transition_id"]])
        for action in owner["source_actions"]:
            action.pop("action_digest", None); action.pop("payload_sha256", None)
        if mutation:
            snapshot = public["authority_duplicate_snapshot"]
            owner["target_disposition"] = {"disposition": "keep_current_open_issue", "duplicate_query": snapshot["query"],
                "duplicate_checked_at": snapshot["checked_at"], "duplicate_candidates": [{**row,"identity":f"#{row['number']}","state":"open","decision":"rejected","reason":"The related Issue does not replace this source."} for row in snapshot["candidates"]], "duplicate_facts_sha256": snapshot["facts_sha256"],
                "selected_issue": None, "original_target_role": "primary", "decision_summary": "The current source remains the authority."}
            payload = {"body": "Current source requirements.\nConfirmed source scope for " + public["profile"] + ".\n"}
            kind = "issue_comment" if mutation == "comment" else "issue_body_edit"
            if kind == "issue_comment":
                self.gh("api", "repos/castbox/guru-trellis/issues/811/comments", "--method", "POST", "--input", "-", body=payload)
                reread = self.gh("api", "repos/castbox/guru-trellis/issues/comments/1")
            else:
                reread = self.gh("api", "repos/castbox/guru-trellis/issues/811", "--method", "PATCH", "--input", "-", body=payload)
            action = {"action_id": "source-edit", "kind": kind, "target": {"repo": "castbox/guru-trellis", "issue_number": 811},
                      "payload": payload, "preimage_sha256": owner["review_target"]["body_sha256"], "payload_sha256": digest(payload),
                      "status": "validated", "mutation_evidence": {"source": "ai-reviewed-gh"}}
            action["action_digest"] = digest({k:action[k] for k in ("action_id", "kind", "target", "payload", "preimage_sha256", "payload_sha256")})
            owner["source_actions"] = [action]
            owner["mutation_results"] = [{"action_id": action["action_id"], "kind": action["kind"], "status": "succeeded", "url": reread["url"],
                "state": "open", "updated_at": reread["updated_at"], "content_sha256": sha(reread["body"]), "action_digest": action["action_digest"], "facts_sha256": sha(json.dumps(reread))}]
            owner["clarification_rounds"] = [{"round_id": "r1", "question_id": "q1", "atomic_group_id": None, "atomic_group_reason": None,
                "category": "scope_risk_decision", "question": "Which source scope applies?", "answer_summary": "The source now states the selected scope.",
                "answer_status": "complete", "authority_impact": "load_bearing", "authority_action_ids": [action["action_id"]],
                "affected_contracts": ["source scope"], "opened_question_ids": ["q1"], "closed_question_ids": ["q1"]}]
        recorded = self.call("guru-clarify-requirements", "record-requirements-clarification.sh", owner, ("--mode", public["mode"], "--input", "-"))
        checked = self.call("guru-clarify-requirements", "check-requirements-clarification.sh", recorded, ("--input", "-"))
        self.assertEqual(checked["typed_exit"], exit_id)
        return self.invoke("guru-clarify-requirements", {"schema_version": "1.0", "public_input": public, "transition": transition, "owner_context": {}, "owner_result": recorded}, expected=expected)

    def discover(self, handoff, transition):
        public = {**self.projection("guru-clarify-requirements" if handoff["exit_id"] == "needs_context" else "guru-sync-base", handoff), "change_input": self.clues}
        owner = json.loads((PACKAGES / "guru-discover-change-context/examples/change-context-owner-result-4.0.json").read_text())
        owner["repository"] = {"repo": "castbox/guru-trellis", "source_kind": "git_object", "selected_ref": transition["base"]["selected_ref"], "commit": self.commit}
        target = self.review_target()
        facts = {"repo": target["repo"], "number": 811, "url": target["url"], "state": "open", "updated_at": target["updated_at"], "body_sha256": target["body_sha256"]}
        owner["live_change"] = {"kind": "issue", "identity": self.authority, "state": "open", "updated_at": target["updated_at"],
                                "body_sha256": target["body_sha256"], "facts_sha256": sha(json.dumps(facts, sort_keys=True, ensure_ascii=False, separators=(",", ":")) + "\n"), "issue_binding": None}
        if self.no_issue:
            owner["live_change"] = {"kind":"draft", "identity":"draft:" + target["body_sha256"], "state":"draft", "updated_at":"2026-01-01T00:00:00Z", "body_sha256":target["body_sha256"], "facts_sha256":target["body_sha256"], "issue_binding":None}
        candidates = self.gh("issue", "list", "--repo", "castbox/guru-trellis", "--state", "open", "--json", "number,url,state,updatedAt")
        normalized = []
        for candidate in candidates:
            source = {"repo":"castbox/guru-trellis", "number":candidate["number"], "identity":f"#{candidate['number']}", "url":candidate["url"], "state":"open", "updated_at":candidate["updatedAt"]}
            normalized.append({**source, "facts_sha256":sha(json.dumps(source, sort_keys=True, ensure_ascii=False, separators=(",", ":")) + "\n"), "reason":"The related source was reviewed as a duplicate candidate.", "observation":"The source search returned this open Issue."})
        owner["duplicate_search"].update(query="repo:castbox/guru-trellis is:issue is:open source scope", checked_at=target["updated_at"] or "2026-01-01T00:00:00Z", candidates=normalized)
        for section in ("docs", "code_contracts", "tests"):
            observed = self.call("guru-discover-change-context", "read-change-context-source.sh", None,
                ("--source-transition", json.dumps(transition), "--path", "README.md"))
            owner["current_state"][section] = [{"path": "README.md", "blob_or_content_sha256": observed["blob"], "purpose": "Read fixed source", "observation": "Fixture requirements establish the tested context boundary.", "query_clues": ["source scope"]}]
        envelope = {"schema_version": "1.0", "public_input": public, "transition": transition, "owner_context": {}, "owner_result": owner}
        envelope["owner_result"] = self.call("guru-discover-change-context", "record-context-discovery.sh", envelope, ("--root", str(self.root), "--invocation", "-"))
        checked = self.call("guru-discover-change-context", "check-context-discovery.sh", envelope, ("--root", str(self.root), "--invocation", "-"))
        self.assertEqual(checked["typed_exit"], "context_ready")
        return self.invoke("guru-discover-change-context", envelope)

    def context(self, qualifier):
        public = self.projection("guru-qualify-" + ("normal-scenario" if qualifier["handoff_profile"].startswith("normal") else "solution-mechanism"), qualifier)
        base = self.baseline()
        needs = self.clarify(public, base["transition"], "needs_context")
        return self.discover(needs, needs["transition"])

    def consume(self, name, clear, qualifier):
        returned = self.projection("guru-clarify-requirements", clear)
        for field in ("mode", "target_locator", "continuation_id", "candidate_refs", "task_ref", "delivery_key", "resume_target"):
            self.assertEqual(returned[field], qualifier[field], field)
        self.assertEqual(returned["resume_target"], "guru-resume-implementation")
        # The original implementation caller rereads the authority and refreshes
        # the affected qualifier admission; no private producer state is read.
        if self.no_issue:
            self.assertTrue((self.root/self.authority).read_text())
        else:
            self.assertIn("body", self.gh("api", "repos/castbox/guru-trellis/issues/811"))
        refreshed = self.qualify(name, confirmed=True)
        self.assertEqual((refreshed["exit_id"], refreshed["profile"], refreshed["resume_target"]),
                         ("classified", "implementation_discovery", returned["resume_target"]))

    def test_both_profiles_missing_current_and_ordinary_stale_context(self):
        for name in ("normal-scenario", "solution-mechanism"):
            with self.subTest(profile=name):
                qualifier = self.qualify(name)
                context = self.context(qualifier)
                self.assertEqual(context["transition"]["target_locator"], self.fixture.ref)
                self.assertEqual(context["transition"]["authority_locator"], self.authority)
                public = self.projection("guru-discover-change-context", context)
                clear = self.clarify(public, context["transition"])
                self.consume(name, clear, qualifier)
                # An existing current context also supports the original qualifier input.
                bootstrap = self.projection("guru-qualify-" + name, qualifier)
                self.consume(name, self.clarify(bootstrap, context["transition"]), qualifier)
                self.gh("api", "repos/castbox/guru-trellis/issues/811", "--method", "PATCH", "--input", "-", body={"body": "Ordinary source revision for " + name})
                rejected = self.clarify(public, context["transition"], expected=3)
                self.assertEqual((rejected["code"], rejected["field_path"]), ("stale_identity", "transition.authority_content_sha256"))
                renewed = self.context(qualifier)
                self.assertNotEqual(renewed["authority_duplicate_snapshot"]["authority_content_sha256"], context["authority_duplicate_snapshot"]["authority_content_sha256"])
                self.consume(name, self.clarify(self.projection("guru-discover-change-context", renewed), renewed["transition"]), qualifier)

    def test_both_profiles_mutation_refresh_preserves_object_and_reads_new_snapshot(self):
        for name in ("normal-scenario", "solution-mechanism"):
            with self.subTest(profile=name):
                qualifier = self.qualify(name)
                context = self.context(qualifier)
                snapshot = context["authority_duplicate_snapshot"]
                self.assertEqual(snapshot["target_locator"], self.authority)
                self.assertNotEqual(snapshot["target_locator"], self.fixture.ref)
                public = self.projection("guru-discover-change-context", context)
                writes = self.gh("api", "repos/castbox/guru-trellis/issues/811")["writes"]
                refresh = self.clarify(public, context["transition"], "refresh_context", mutation=True)
                sync_input = self.projection("guru-clarify-requirements", refresh)
                self.assertEqual((sync_input["operation"], sync_input["base_ref"]), ("read", self.commit))
                base = self.baseline(sync_input)
                self.assertEqual((base["handoff_profile"], base["handoff_continuation_id"]), ("context_request", qualifier["continuation_id"]))
                renewed = self.discover(base, base["transition"])
                self.assertNotEqual(snapshot["authority_content_sha256"], renewed["authority_duplicate_snapshot"]["authority_content_sha256"])
                clear = self.clarify(self.projection("guru-discover-change-context", renewed), renewed["transition"])
                self.consume(name, clear, qualifier)
                self.assertEqual(self.gh("api", "repos/castbox/guru-trellis/issues/811")["writes"], writes + 1)


    def test_confirmation_comment_refreshes_without_changing_issue_body(self):
        qualifier = self.qualify("normal-scenario")
        context = self.context(qualifier)
        before = self.gh("api", "repos/castbox/guru-trellis/issues/811")
        refresh = self.clarify(self.projection("guru-discover-change-context", context), context["transition"], "refresh_context", mutation="comment")
        after = self.gh("api", "repos/castbox/guru-trellis/issues/811")
        self.assertEqual(refresh["exit_id"], "refresh_context")
        self.assertEqual(after["body"], before["body"])
        self.assertEqual(after["writes"], before["writes"] + 1)
        for key in ("target_locator", "candidate_refs", "continuation_id", "resume_target", "task_ref", "delivery_key"):
            self.assertEqual(refresh["return_identity"][key], qualifier[key])

    def test_legal_non_task_and_other_candidate_context_stays_separate(self):
        for name in ("normal-scenario", "solution-mechanism"):
            qualifier = self.qualify(name, task_bound=False)
            self.assertNotIn("task_ref", qualifier)
            context = self.context(qualifier)
            clear = self.clarify(self.projection("guru-discover-change-context", context), context["transition"])
            returned = self.projection("guru-clarify-requirements", clear)
            self.assertNotIn("delivery_key", returned)
            self.assertEqual(returned["resume_target"], "guru-clarify-requirements")
            other = self.qualify(name, task_bound=False, candidate="another-current-candidate")
            public = self.projection("guru-qualify-" + name, other)
            rejected = self.clarify(public, context["transition"], expected=3)
            self.assertEqual(rejected["code"], "stale_identity")

    def test_legal_task_without_issue_uses_current_accepted_scope_no_issue(self):
        for name in ("normal-scenario", "solution-mechanism"):
            qualifier = self.qualify(name)
            context = self.context(qualifier)
            self.assertEqual(context["transition"]["authority_locator"], self.fixture.ref + "/prd.md")
            self.assertEqual(context["authority_duplicate_snapshot"]["target_locator"], self.fixture.ref + "/prd.md")
            self.assertNotEqual(context["handoff_target_locator"], context["transition"]["authority_locator"])
            self.consume(name, self.clarify(self.projection("guru-discover-change-context", context), context["transition"]), qualifier)


if __name__ == "__main__":
    unittest.main()
