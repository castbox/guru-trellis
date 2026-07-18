from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path
from unittest import mock


PACKAGE_ROOT = Path(__file__).resolve().parents[1]


def load_runtime():
    candidates = []
    for ancestor in [PACKAGE_ROOT, *PACKAGE_ROOT.parents]:
        candidates.extend([
            ancestor / "trellis/workflows/guru-team/scripts/python/guru_team_trellis.py",
            ancestor / ".trellis/guru-team/scripts/python/guru_team_trellis.py",
        ])
    runtime_path = next((path for path in candidates if path.is_file()), None)
    if runtime_path is None:
        raise RuntimeError("Compatible Guru Team runtime not found for package tests.")
    spec = importlib.util.spec_from_file_location("change_request_review_runtime", runtime_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Compatible Guru Team runtime could not be loaded.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


GTT = load_runtime()


class ChangeRequestReviewPackageContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.io_tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.io_root = Path(self.io_tmp.name)
        subprocess.run(["git", "init", "-q", "-b", "main", str(self.root)], check=True)
        self.git("config", "user.name", "Change Request Review Test")
        self.git("config", "user.email", "change-request-review@example.invalid")
        self.source = self.root / "draft.json"
        self.source.write_text(json.dumps({
            "kind": "draft",
            "draft_id": "draft-27",
            "title": "Add a readiness review Skill",
            "body": "Deliver one current and independently testable change.",
            "selected_comments": [],
        }), encoding="utf-8")
        self.caller_locator = "request:example-27"
        self.issue_source = self.root / "issue.json"
        self.issue_source.write_text(json.dumps({
            "kind": "issue",
            "repo": "example/guru-extension",
            "number": 27,
            "selected_comments": [],
        }), encoding="utf-8")
        self.issue_live = {
            "number": 27,
            "title": "Add a readiness review Skill",
            "body": "Deliver one current and independently testable change.",
            "url": "https://github.com/example/guru-extension/issues/27",
            "state": "OPEN",
            "updatedAt": "2026-01-01T00:00:00Z",
            "comments": [],
        }
        self.issue_live_path = self.io_root / "live-issue.json"
        self.issue_live_path.write_text(
            json.dumps(self.issue_live),
            encoding="utf-8",
        )
        self.fake_bin = self.io_root / "bin"
        self.fake_bin.mkdir()
        fake_gh = self.fake_bin / "gh"
        fake_gh.write_text(
            "#!/bin/sh\n"
            "if [ \"${1:-}\" = auth ]; then exit 0; fi\n"
            "if [ \"${1:-}\" = issue ] && [ \"${2:-}\" = view ]; then\n"
            "  /bin/cat \"$GURU_TEST_ISSUE_JSON\"\n"
            "  exit 0\n"
            "fi\n"
            "exit 2\n",
            encoding="utf-8",
        )
        fake_gh.chmod(0o755)
        for relative, content in (
            ("docs/requirements.md", "# Readiness requirements\n"),
            ("trellis/runtime.py", "READINESS_RUNTIME = 'deterministic'\n"),
            ("tests/test_runtime.py", "def test_readiness_runtime():\n    assert True\n"),
        ):
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        for skill_id, schema_name in (
            ("guru-sync-base", "base-sync-result.schema.json"),
            ("guru-discover-change-context", "context-discovery.schema.json"),
            ("guru-clarify-requirements", "requirements-clarification.schema.json"),
            ("guru-review-contract-wording", "contract-wording-review.schema.json"),
            ("guru-review-change-request", "change-request-review.schema.json"),
        ):
            source_schema = PACKAGE_ROOT.parent / skill_id / "schemas" / schema_name
            installed_schema = (
                self.root
                / ".trellis/guru-team/skills/packages"
                / skill_id
                / "schemas"
                / schema_name
            )
            installed_schema.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_schema, installed_schema)
        self.git("add", ".")
        self.git("commit", "-q", "-m", "test: seed current review repository")
        self.git("remote", "add", "origin", "https://github.com/example/guru-extension.git")
        self.git("update-ref", "refs/remotes/origin/main", self.git("rev-parse", "HEAD"))
        self.raw_target = self.raw_draft_target("proposed_draft")
        self.target, self.scope, self.contents = GTT.change_request_review_normalize_target(
            self.root,
            self.raw_target,
            self.source.name,
            "standalone",
        )

    def tearDown(self) -> None:
        self.io_tmp.cleanup()
        self.tmp.cleanup()

    def git(self, *args: str) -> str:
        return subprocess.run(
            ["git", *args],
            cwd=self.root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        ).stdout.strip()

    def write_external_json(self, name: str, payload: object) -> Path:
        path = self.io_root / name
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return path

    def raw_draft_target(
        self,
        kind: str,
        *,
        source_path: Path | None = None,
        caller_locator: str | None = None,
    ) -> dict[str, object]:
        reviewed_source = source_path or self.source
        source = json.loads(reviewed_source.read_text(encoding="utf-8"))
        scope, _ = GTT.contract_wording_build_scope(
            self.root,
            "change_request",
            "standalone",
            change_request_input=str(reviewed_source),
        )
        title_sha, body_sha, _ = GTT.change_request_review_scope_hashes(scope)
        common = {
            "kind": kind,
            "repo": "example/guru-extension",
            "source_request_sha256": GTT.context_digest(
                GTT.change_request_review_request_authority_projection(
                    "example/guru-extension",
                    source,
                    body_sha,
                )
            ),
            "title_sha256": title_sha,
            "body_sha256": body_sha,
            "side_effect_free": True,
        }
        if kind == "proposed_draft":
            return {**common, "draft_id": source["draft_id"]}
        return {
            **common,
            "caller_locator": caller_locator or self.caller_locator,
            "request_id": source["draft_id"],
        }

    def issue_environment(self):
        return mock.patch.dict(os.environ, {
            "PATH": f"{self.fake_bin}{os.pathsep}{os.environ.get('PATH', '')}",
            "GURU_TEST_ISSUE_JSON": str(self.issue_live_path),
        })

    def source_for_target(
        self,
        kind: str,
        source_path: Path | None = None,
    ) -> Path:
        return self.issue_source if kind == "existing_issue" else source_path or self.source

    def raw_issue_target(self) -> dict[str, object]:
        scope, _ = GTT.contract_wording_build_scope(
            self.root,
            "change_request",
            "standalone",
            change_request_input=str(self.issue_source),
        )
        title_sha, body_sha, _ = GTT.change_request_review_scope_hashes(scope)
        return {
            "kind": "existing_issue",
            "repo": "example/guru-extension",
            "issue_number": 27,
            "url": self.issue_live["url"],
            "updated_at": self.issue_live["updatedAt"],
            "title_sha256": title_sha,
            "body_sha256": body_sha,
        }

    def raw_target_for_kind(
        self,
        kind: str,
        *,
        source_path: Path | None = None,
        caller_locator: str | None = None,
    ) -> dict[str, object]:
        return (
            self.raw_issue_target()
            if kind == "existing_issue"
            else self.raw_draft_target(
                kind,
                source_path=source_path,
                caller_locator=caller_locator,
            )
        )

    def current_prerequisites(self) -> dict[str, dict[str, object]]:
        return {
            "context": {
                "status": "current",
                "schema_id": "guru-context-discovery-1.0",
                "typed_exit": "context_ready",
                "payload_sha256": "1" * 64,
                "snapshot_sha256": "2" * 64,
                "base_sync_facts_sha256": "3" * 64,
                "base_head": "4" * 40,
                "live_target_sha256": "5" * 64,
                "query_sha256": "6" * 64,
                "current_state_sha256": "7" * 64,
                "history_sha256": "8" * 64,
                "duplicate_sha256": "9" * 64,
                "error_codes": [],
            },
            "clarity": {
                "status": "current",
                "schema_id": "guru-requirements-clarification-1.0",
                "typed_exit": "clear",
                "payload_sha256": "a" * 64,
                "facts_sha256": "b" * 64,
                "target_sha256": self.target["identity_sha256"],
                "content_sha256": self.target["content_sha256"],
                "scope_sha256": self.scope["scope_sha256"],
                "error_codes": [],
            },
            "wording": {
                "status": "current",
                "schema_id": "guru-contract-wording-review-1.0",
                "profile": "change_request",
                "typed_exit": "pass",
                "payload_sha256": "c" * 64,
                "facts_sha256": "d" * 64,
                "scope_sha256": self.scope["scope_sha256"],
                "scan_sha256": "e" * 64,
                "target_content_sha256": self.target["content_sha256"],
                "error_codes": [],
            },
        }

    def base_sync_result(self) -> dict[str, object]:
        head = self.git("rev-parse", "HEAD")
        resolution = GTT.resolution_identity(
            source="explicit",
            selected_base="main",
            remote="origin",
            candidates=["main"],
            decision_branch="main",
            decision_head=head,
            decision_clean=True,
        )
        resolution_sha256 = GTT.canonical_json_sha256(resolution)
        result: dict[str, object] = {
            "schema_version": "1.0",
            "skill_id": "guru-sync-base",
            "status": "synced",
            "resolution": {
                "source": "explicit",
                "selected_base": "main",
                "remote": "origin",
                "candidates": ["main"],
                "resolution_sha256": resolution_sha256,
            },
            "post_sync_resolution": resolution,
            "post_sync_resolution_sha256": resolution_sha256,
            "decision_checkout": {
                "branch": "main",
                "head_before": head,
                "head_after": head,
                "clean_before": True,
                "clean_after": True,
            },
            "git": {
                "local_ref": "refs/heads/main",
                "remote_ref": "refs/remotes/origin/main",
                "local_head_before": head,
                "local_head_after": head,
                "remote_head_after": head,
                "fetch_performed": True,
                "fast_forwarded": False,
            },
            "fresh": True,
        }
        result["facts_sha256"] = GTT.canonical_json_sha256(result)
        return result

    def context_payload(
        self,
        *,
        target_kind: str = "proposed_draft",
        source_path: Path | None = None,
        body: str | None = None,
        current_marker: str = "initial",
        history_reason: str = "Current evidence is sufficient for this review.",
        duplicate_query: str = "repo:example/guru-extension is:issue is:open readiness review",
    ) -> dict[str, object]:
        package = PACKAGE_ROOT.parent / "guru-discover-change-context"
        payload = json.loads(
            (package / "examples/context-discovery.json").read_text(encoding="utf-8")
        )
        reviewed_source = self.source_for_target(target_kind, source_path)
        source = json.loads(reviewed_source.read_text(encoding="utf-8"))
        source_body = self.issue_live["body"] if target_kind == "existing_issue" else source["body"]
        reviewed_body = body if body is not None else source_body
        body_sha256 = hashlib.sha256(reviewed_body.encode("utf-8")).hexdigest()
        sync_result = self.base_sync_result()
        head = sync_result["decision_checkout"]["head_after"]
        payload["generated_at"] = "2026-01-01T00:00:00Z"
        payload["mode"] = "standalone"
        payload["repository"] = {
            "repo": "example/guru-extension",
            "selected_base": "main",
            "decision_branch": "main",
        }
        payload["base_evidence"] = {
            "schema_id": "guru-base-sync-result-1.0",
            "sync_result": sync_result,
            "remote": "origin",
            "base_head": head,
            "decision_head": head,
            "local_head": head,
            "remote_head": head,
            "post_sync_resolution_sha256": sync_result["post_sync_resolution_sha256"],
            "clean": True,
        }
        change_input = {
            "issue_refs": ["#27"] if target_kind == "existing_issue" else [],
            "pr_refs": [],
            "branches": [],
            "paths": ["docs/requirements.md"],
            "commands": ["record-change-request-review"],
            "config_keys": [],
            "schema_fields": ["source_request_sha256"],
            "symbols": ["guru-review-change-request"],
            "terms": ["readiness review"],
            "queries": ["review one independently deliverable change request"],
        }
        payload["change_input"] = change_input
        payload["canonical_query"] = GTT.canonicalize_context_query(
            self.root,
            change_input,
        )
        if target_kind == "existing_issue":
            issue_facts = {
                "repo": "example/guru-extension",
                "number": 27,
                "url": self.issue_live["url"],
                "state": str(self.issue_live["state"]).casefold(),
                "updated_at": self.issue_live["updatedAt"],
                "body_sha256": body_sha256,
            }
            payload["live_change"] = {
                "kind": "issue",
                "identity": issue_facts["url"],
                "state": issue_facts["state"],
                "updated_at": issue_facts["updated_at"],
                "body_sha256": body_sha256,
                "facts_sha256": GTT.context_digest(issue_facts),
                "issue_binding": None,
            }
        else:
            live_projection = {
                "kind": "draft",
                "identity": f"draft:{body_sha256}",
                "state": "draft",
                "updated_at": "2026-01-01T00:00:00Z",
                "body_sha256": body_sha256,
            }
            payload["live_change"] = {
                **live_projection,
                "facts_sha256": GTT.context_digest(live_projection),
                "issue_binding": None,
            }
        payload["duplicate_search"] = {
            "query": duplicate_query,
            "checked_at": "2026-01-01T00:00:00Z",
            "scope": "open_issues",
            "candidates": [],
        }
        payload["current_state"] = {
            "sequence_trace": list(GTT.CONTEXT_SEQUENCE_TRACE),
            "docs": [{
                "path": "docs/requirements.md",
                "blob_or_content_sha256": self.git("rev-parse", "HEAD:docs/requirements.md"),
                "purpose": "Review the durable readiness requirement.",
                "observation": "The durable requirement keeps semantic and deterministic ownership separate.",
                "query_clues": ["readiness requirement"],
            }],
            "code_contracts": [{
                "path": "trellis/runtime.py",
                "blob_or_content_sha256": self.git("rev-parse", "HEAD:trellis/runtime.py"),
                "purpose": "Review the deterministic runtime boundary.",
                "observation": "The runtime only validates objective facts.",
                "query_clues": ["deterministic runtime"],
            }],
            "tests": [{
                "path": "tests/test_runtime.py",
                "blob_or_content_sha256": self.git("rev-parse", "HEAD:tests/test_runtime.py"),
                "purpose": "Review the production linkage coverage.",
                "observation": "The test exercises the installed runtime commands.",
                "query_clues": ["production linkage"],
            }],
            "observations": [f"Current state marker: {current_marker}."],
        }
        payload["history_preview"] = GTT.build_context_history_preview(
            self.root,
            payload["canonical_query"],
        )
        payload["history_review"] = {
            "selected_candidates": [],
            "excluded_candidates": [],
            "deep_reads": [],
        }
        payload["mem_review"] = {
            "status": "not_needed",
            "reason": history_reason,
            "load_bearing_question": None,
            "exhausted_sources": {
                "task_artifacts": False,
                "current_docs_code_tests": False,
                "github": False,
                "git_history": False,
            },
            "summary": None,
        }
        payload["snapshot_identity"] = GTT.context_snapshot_identity(payload)
        return payload

    def record_and_check_context(
        self,
        payload: dict[str, object],
        label: str,
    ) -> dict[str, object]:
        authored_path = self.write_external_json(f"{label}-context-authored.json", payload)
        recorded = GTT.cmd_record_context_discovery(Namespace(
            root=str(self.root),
            mode="standalone",
            input=str(authored_path),
            task=None,
            expected_snapshot_sha256=None,
        ))
        recorded_path = self.write_external_json(f"{label}-context-recorded.json", recorded)
        checked = GTT.cmd_check_context_discovery(Namespace(
            root=str(self.root),
            input=str(recorded_path),
            task=None,
            expected_snapshot_sha256=recorded["snapshot_identity"]["snapshot_sha256"],
        ))
        self.assertEqual(checked["typed_exit"], "context_ready")
        return recorded

    def record_and_check_clarity(
        self,
        context_payload: dict[str, object],
        label: str,
        *,
        body: str | None = None,
        target_kind: str = "proposed_draft",
        source_path: Path | None = None,
        caller_locator: str | None = None,
        invocation_kind: str | None = None,
    ) -> dict[str, object]:
        package = PACKAGE_ROOT.parent / "guru-clarify-requirements"
        payload = json.loads(
            (package / "examples/requirements-clarification.json").read_text(encoding="utf-8")
        )
        reviewed_source = self.source_for_target(target_kind, source_path)
        source = json.loads(reviewed_source.read_text(encoding="utf-8"))
        source_body = self.issue_live["body"] if target_kind == "existing_issue" else source["body"]
        reviewed_body = body if body is not None else source_body
        body_sha256 = hashlib.sha256(reviewed_body.encode("utf-8")).hexdigest()
        if target_kind == "existing_issue":
            authority = {
                "kind": "issue",
                "repo": "example/guru-extension",
                "issue_number": 27,
                "url": self.issue_live["url"],
                "state": str(self.issue_live["state"]).casefold(),
                "updated_at": self.issue_live["updatedAt"],
                "body_sha256": body_sha256,
            }
        else:
            authority = {
                "kind": "draft",
                "repo": "example/guru-extension",
                "issue_number": None,
                "url": None,
                "state": "draft",
                "updated_at": None,
                "body_sha256": body_sha256,
            }
        payload["mode"] = "standalone"
        selected_invocation = invocation_kind or {
                "existing_issue": "initial_issue",
                "standalone_request": "standalone_review",
            }.get(target_kind, "proposed_draft")
        payload["invocation_context"] = {
            "kind": selected_invocation,
            "caller": caller_locator or self.caller_locator,
            "task_locator": None,
            "resume_target": (
                "guru-standalone-caller"
                if selected_invocation == "standalone_review"
                else "guru-review-contract-wording"
            ),
        }
        payload["review_target"] = {
            **authority,
            "facts_sha256": GTT.context_digest(authority),
        }
        snapshot_sha256 = context_payload["snapshot_identity"]["snapshot_sha256"]
        payload["context_evidence"] = {
            "status": "current",
            "schema_id": "guru-context-discovery-1.0",
            "snapshot_sha256": snapshot_sha256,
            "evidence_refs": [f"guru-context-discovery-1.0:{snapshot_sha256}"],
            "missing_reason": None,
        }
        authored_path = self.write_external_json(f"{label}-clarity-authored.json", payload)
        recorded = GTT.cmd_record_requirements_clarification(Namespace(
            root=str(self.root),
            mode="standalone",
            input=str(authored_path),
            task=None,
        ))
        recorded_path = self.write_external_json(f"{label}-clarity-recorded.json", recorded)
        checked = GTT.cmd_check_requirements_clarification(Namespace(
            root=str(self.root),
            input=str(recorded_path),
            task=None,
            expected_result_sha256=recorded["content_identity"]["result_sha256"],
        ))
        self.assertEqual(checked["typed_exit"], "clear")
        return recorded

    def record_and_check_active_task_clarity(
        self,
        context_payload: dict[str, object],
        label: str,
        *,
        target_kind: str,
    ) -> dict[str, object]:
        task = self.root / ".trellis/tasks" / f"active-{label}"
        task.mkdir(parents=True)
        locator = task.relative_to(self.root).as_posix()
        (task / "task.json").write_text(
            '{"status":"in_progress","branch":"main"}\n',
            encoding="utf-8",
        )
        for name, content in (
            ("prd.md", "# Active scope requirements\n\nClassify the current request.\n"),
            ("design.md", "# Active scope design\n\nBind current task evidence.\n"),
            ("implement.md", "# Active scope implementation\n\nValidate the recorded decision.\n"),
        ):
            (task / name).write_text(content, encoding="utf-8")

        wording_scope, wording_contents = GTT.contract_wording_build_scope(
            self.root,
            "planning_artifacts",
            "workflow",
            task_dir=task,
        )
        wording_scan = GTT.scan_contract_wording(wording_scope, wording_contents)
        wording_evidence = GTT.contract_wording_derive_result(
            "planning_artifacts",
            "workflow",
            wording_scope,
            wording_scan,
            {
                "generated_at": "2026-01-01T00:00:00Z",
                "semantic_review": {
                    "revisions": [],
                    "classifications": [{
                        "hit_id": hit["hit_id"],
                        "classification": "term_definition",
                        "reason": "The active-task planning term is explicit.",
                    } for hit in wording_scan["hits"]],
                    "ai_review_gate": {
                        "status": "passed",
                        "reviewer": "production-package-test-ai",
                        "summary": "The active-task planning wording was reviewed.",
                        "reviewed_scan_sha256": wording_scan["scan_sha256"],
                        "checked_dimensions": {
                            name: True for name in GTT.CONTRACT_WORDING_REVIEW_DIMENSIONS
                        },
                        "planning_checked_dimensions": {
                            name: True
                            for name in GTT.CONTRACT_WORDING_PLANNING_REVIEW_DIMENSIONS
                        },
                    },
                },
                "human_confirmation": {
                    "status": "not_required",
                    "confirmed_by": None,
                    "confirmed_at": None,
                    "reason": "The fixture requires no content mutation.",
                },
                "typed_exit": "pass",
            },
        )
        GTT.write_json(task / GTT.CONTRACT_WORDING_EVIDENCE_ARTIFACT, wording_evidence)
        planning_approval = GTT.build_planning_approval_payload(
            self.root,
            task,
            reviewer="production-package-test-ai",
            approval_summary="The complete active-task planning contract was reviewed.",
            user_confirmation="The three displayed planning documents were confirmed.",
            artifacts=[],
            contract_wording_evidence=GTT.CONTRACT_WORDING_EVIDENCE_ARTIFACT,
            review_prompt_presented_at="2026-01-01T00:00:00Z",
        )
        GTT.write_json(task / GTT.PLANNING_APPROVAL_ARTIFACT, planning_approval)

        snapshot_sha256 = context_payload["snapshot_identity"]["snapshot_sha256"]
        (task / "context-discovery.json").write_text(json.dumps({
            "generated_at": "2026-01-01T00:00:00Z",
            "snapshot_identity": {"snapshot_sha256": snapshot_sha256},
        }) + "\n", encoding="utf-8")
        ledger = {
            "primary_issue": {"number": 27},
            "close_issues": [{"number": 27}],
            "related_issues": [],
            "followup_issues": [],
            "scope_decisions": [],
        }
        GTT.write_json(task / "issue-scope-ledger.json", ledger)

        package = PACKAGE_ROOT.parent / "guru-clarify-requirements"
        payload = json.loads(
            (package / "examples/requirements-clarification.json").read_text(
                encoding="utf-8"
            )
        )
        reviewed_source = self.source_for_target(target_kind)
        source = json.loads(reviewed_source.read_text(encoding="utf-8"))
        source_body = (
            self.issue_live["body"]
            if target_kind == "existing_issue"
            else source["body"]
        )
        body_sha256 = hashlib.sha256(source_body.encode("utf-8")).hexdigest()
        if target_kind == "existing_issue":
            authority = {
                "kind": "issue",
                "repo": "example/guru-extension",
                "issue_number": 27,
                "url": self.issue_live["url"],
                "state": str(self.issue_live["state"]).casefold(),
                "updated_at": self.issue_live["updatedAt"],
                "body_sha256": body_sha256,
            }
        else:
            authority = {
                "kind": "draft",
                "repo": "example/guru-extension",
                "issue_number": None,
                "url": None,
                "state": "draft",
                "updated_at": None,
                "body_sha256": body_sha256,
            }
        payload["mode"] = "workflow"
        payload["invocation_context"] = {
            "kind": "active_task_scope_change",
            "caller": "active task",
            "task_locator": locator,
            "resume_target": "guru-resume-implementation",
        }
        payload["review_target"] = {
            **authority,
            "facts_sha256": GTT.context_digest(authority),
        }
        payload["context_evidence"] = {
            "status": "current",
            "schema_id": "guru-context-discovery-1.0",
            "snapshot_sha256": snapshot_sha256,
            "evidence_refs": [f"guru-context-discovery-1.0:{snapshot_sha256}"],
            "missing_reason": None,
        }
        payload["scope_proposals"] = [{
            "proposal_id": "remove_optional_guard",
            "scenario": "Remove an optional implementation guard.",
            "trigger_evidence": ["the mechanism created the reported risk"],
            "proposed_contracts": ["retain the original requirement boundary"],
            "cost": "Remove the optional mechanism.",
            "alternatives": ["Replace it with a simpler mechanism."],
            "consequence_if_omitted": "The implementation creates avoidable scope.",
            "origin_requirement_status": "unconfirmed_expansion",
            "optional_mechanism_origin": True,
            "decision": "mechanism_removed",
            "proposal_digest": "0" * 64,
            "confirmation_ref": None,
        }]
        planning = [{
            "path": f"{locator}/{name}",
            "content_sha256": hashlib.sha256((task / name).read_bytes()).hexdigest(),
        } for name in ("prd.md", "design.md", "implement.md")]
        payload["active_task_evidence"] = {
            "task_locator": locator,
            "github_authority_facts_sha256": payload["review_target"]["facts_sha256"],
            "ledger": {
                "path": f"{locator}/issue-scope-ledger.json",
                "content_sha256": hashlib.sha256(
                    (task / "issue-scope-ledger.json").read_bytes()
                ).hexdigest(),
            },
            "planning_documents": planning,
            "stale_downstream_evidence": {
                "planning_approval_sha256": hashlib.sha256(
                    (task / GTT.PLANNING_APPROVAL_ARTIFACT).read_bytes()
                ).hexdigest(),
                "phase2_check_sha256": None,
                "branch_review_sha256": None,
            },
            "review_evidence": {"status": "not_started", "artifact": None},
            "decision_trail": None,
            "reentry_owners": sorted(GTT.REQUIREMENTS_CLARIFICATION_REENTRY_OWNERS),
        }
        authored_path = self.write_external_json(f"{label}-clarity-authored.json", payload)
        recorded = GTT.cmd_record_requirements_clarification(Namespace(
            root=str(self.root),
            mode="workflow",
            input=str(authored_path),
            task=locator,
        ))
        recorded_path = self.write_external_json(f"{label}-clarity-recorded.json", recorded)
        checked = GTT.cmd_check_requirements_clarification(Namespace(
            root=str(self.root),
            input=str(recorded_path),
            task=locator,
            expected_result_sha256=recorded["content_identity"]["result_sha256"],
        ))
        self.assertEqual(checked["typed_exit"], "clear")
        shutil.rmtree(task)
        return recorded

    def record_and_check_wording(
        self,
        label: str,
        *,
        target_kind: str = "proposed_draft",
        source_path: Path | None = None,
    ) -> dict[str, object]:
        reviewed_source = source_path or self.source_for_target(target_kind)
        scope, contents = GTT.contract_wording_build_scope(
            self.root,
            "change_request",
            "standalone",
            change_request_input=str(reviewed_source),
        )
        scan = GTT.scan_contract_wording(scope, contents)
        authored = {
            "generated_at": "2026-01-01T00:00:00Z",
            "semantic_review": {
                "revisions": [],
                "classifications": [{
                    "hit_id": hit["hit_id"],
                    "classification": "term_definition",
                    "reason": "The semantic review retained this explicit contract term.",
                } for hit in scan["hits"]],
                "ai_review_gate": {
                    "status": "passed",
                    "reviewer": "production-package-test-ai",
                    "summary": "The current change-request wording was reviewed.",
                    "reviewed_scan_sha256": scan["scan_sha256"],
                    "checked_dimensions": {
                        name: True for name in GTT.CONTRACT_WORDING_REVIEW_DIMENSIONS
                    },
                },
            },
            "human_confirmation": {
                "status": "not_required",
                "confirmed_by": None,
                "confirmed_at": None,
                "reason": "No wording mutation is required.",
            },
            "typed_exit": "pass",
        }
        authored_path = self.write_external_json(f"{label}-wording-authored.json", authored)
        recorded = GTT.cmd_record_contract_wording_review(Namespace(
            root=str(self.root),
            mode="standalone",
            profile="change_request",
            input=str(authored_path),
            task=None,
            path=[],
            change_request_input=str(reviewed_source),
            scan_only=False,
            replace_stale=False,
            supersede_reentry_facts_sha256=None,
        ))
        recorded_path = self.write_external_json(f"{label}-wording-recorded.json", recorded)
        checked = GTT.cmd_check_contract_wording_review(Namespace(
            root=str(self.root),
            input=str(recorded_path),
            task=None,
            path=[],
            change_request_input=str(reviewed_source),
            expected_facts_sha256=recorded["facts_sha256"],
        ))
        self.assertEqual(checked["typed_exit"], "pass")
        return recorded

    def production_prerequisites(
        self,
        label: str,
        *,
        target_kind: str = "proposed_draft",
        source_path: Path | None = None,
        caller_locator: str | None = None,
        context_body: str | None = None,
        clarity_body: str | None = None,
        current_marker: str = "initial",
        history_reason: str = "Current evidence is sufficient for this review.",
        duplicate_query: str = "repo:example/guru-extension is:issue is:open readiness review",
    ) -> dict[str, dict[str, object]]:
        context = self.record_and_check_context(
            self.context_payload(
                target_kind=target_kind,
                source_path=source_path,
                body=context_body,
                current_marker=current_marker,
                history_reason=history_reason,
                duplicate_query=duplicate_query,
            ),
            label,
        )
        clarity = self.record_and_check_clarity(
            context,
            label,
            body=clarity_body,
            target_kind=target_kind,
            source_path=source_path,
            caller_locator=caller_locator,
        )
        wording = self.record_and_check_wording(
            label,
            target_kind=target_kind,
            source_path=self.source_for_target(target_kind, source_path),
        )
        return {"context": context, "clarity": clarity, "wording": wording}

    def semantic_review(
        self,
        linkage: dict[str, object],
        typed_exit: str,
        *,
        gate_override: object = ...,
        target: dict[str, object] | None = None,
    ) -> dict[str, object]:
        reviewed_target = target or self.target
        non_ready = typed_exit != "ready"
        finding = {
            "finding_id": "finding-1",
            "category": {
                "clarify_requirements": "requirement_gap",
                "review_wording": "wording_gap",
                "refresh_context": "context_stale",
                "blocked": "target_complete",
            }.get(typed_exit, "requirement_gap"),
            "summary": "The AI found evidence that prevents readiness.",
            "blocking": True,
            "evidence_refs": ["target"],
            "affected_hashes": [reviewed_target["content_sha256"]],
            "route_basis": "The recorded exit follows the reviewed finding.",
        }
        dimensions = []
        for index, dimension_id in enumerate(GTT.CHANGE_REQUEST_REVIEW_DIMENSIONS):
            dimensions.append({
                "id": dimension_id,
                "status": "failed" if non_ready and index == 0 else "passed",
                "summary": "The AI reviewed this dimension against current evidence.",
                "evidence_refs": ["target"],
                "affected_hashes": [reviewed_target["content_sha256"]],
                "finding_ids": ["finding-1"] if non_ready and index == 0 else [],
            })
        scope_conclusion = {
            "requirement_scope_basis": "The request and prerequisite evidence define the scope.",
            "delivery_unit_id": "example-change-27",
            "close_issues": [],
            "related_issues": [],
            "followup_issues": [],
            "duplicate_reuse_decision": "The reviewed duplicate facts do not replace this unit.",
            "implementation_target": "The fictional Guru extension package.",
            "current_gap": "The readiness contract remains to be delivered.",
            "archived_constraints": [],
            "risk_boundary": ["Normal honest workflow operation only."],
            "excluded_scope": ["Workspace creation is downstream."],
        }
        gate = {
            "status": GTT.CHANGE_REQUEST_REVIEW_GATE_BY_EXIT[typed_exit],
            "reviewer": "package-test-ai",
            "reviewed_linkage_sha256": linkage["linkage_sha256"],
            "summary": "The AI completed the semantic readiness review.",
            "findings_count": 1 if non_ready else 0,
            "scope_conclusion_sha256": GTT.context_digest(scope_conclusion),
        }
        if gate_override is not ...:
            gate = gate_override
        return {
            "dimensions": dimensions,
            "findings": [finding] if non_ready else [],
            "scope_conclusion": scope_conclusion,
            "ai_review_gate": gate,
        }

    def result(
        self,
        typed_exit: str,
        prerequisites: dict[str, dict[str, object]] | None = None,
        *,
        gate_override: object = ...,
    ) -> tuple[dict[str, object], dict[str, dict[str, object]], dict[str, object]]:
        projections = prerequisites or self.current_prerequisites()
        linkage = GTT.change_request_review_linkage(self.target, projections)
        confirmation = {
            "status": "required" if typed_exit == "clarify_requirements" else "not_required",
            "reason": "A new product decision is routed to its owner." if typed_exit == "clarify_requirements" else "No new product decision is required.",
            "proposal_sha256": "f" * 64 if typed_exit == "clarify_requirements" else None,
        }
        authored = {
            "generated_at": "2026-01-01T00:00:00Z",
            "mode": "standalone",
            "target": self.raw_target,
            "prerequisite_payloads": {"context": None, "clarity": None, "wording": None},
            "semantic_review": self.semantic_review(
                linkage,
                typed_exit,
                gate_override=gate_override,
            ),
            "human_confirmation": confirmation,
            "typed_exit": typed_exit,
            "reason": "The AI-authored review selected exactly one declared route.",
            "affected_evidence": [{
                "ref": "target",
                "sha256": self.target["content_sha256"],
                "summary": "The reviewed change request content.",
            }],
            "consumer": GTT.CHANGE_REQUEST_REVIEW_CONSUMERS[typed_exit],
        }
        return (
            GTT.change_request_review_derive_result(
                self.target,
                projections,
                linkage,
                authored,
            ),
            projections,
            linkage,
        )

    def review_authored(
        self,
        target_kind: str,
        prerequisite_payloads: dict[str, dict[str, object]],
        typed_exit: str,
        *,
        source_path: Path | None = None,
        caller_locator: str | None = None,
    ) -> tuple[dict[str, object], dict[str, object]]:
        reviewed_source = self.source_for_target(target_kind, source_path)
        raw_target = self.raw_target_for_kind(
            target_kind,
            source_path=reviewed_source,
            caller_locator=caller_locator,
        )
        target, scope, contents = GTT.change_request_review_normalize_target(
            self.root,
            raw_target,
            str(reviewed_source),
            "standalone",
        )
        projections = GTT.change_request_review_prerequisite_projections(
            self.root,
            prerequisite_payloads,
            target,
            scope,
            contents,
        )
        linkage = GTT.change_request_review_linkage(target, projections)
        authored = {
            "generated_at": "2026-01-01T00:00:00Z",
            "mode": "standalone",
            "target": raw_target,
            "prerequisite_payloads": prerequisite_payloads,
            "semantic_review": self.semantic_review(
                linkage,
                typed_exit,
                target=target,
            ),
            "human_confirmation": {
                "status": "required" if typed_exit == "clarify_requirements" else "not_required",
                "reason": "A new product decision is routed to its owner." if typed_exit == "clarify_requirements" else "No new product decision is required.",
                "proposal_sha256": "f" * 64 if typed_exit == "clarify_requirements" else None,
            },
            "typed_exit": typed_exit,
            "reason": "The AI-authored review selected one declared route.",
            "affected_evidence": [{
                "ref": "target",
                "sha256": target["content_sha256"],
                "summary": "The reviewed change-request title and body.",
            }],
            "consumer": GTT.CHANGE_REQUEST_REVIEW_CONSUMERS[typed_exit],
        }
        return authored, target

    def ready_authored(
        self,
        target_kind: str,
        prerequisite_payloads: dict[str, dict[str, object]],
        *,
        source_path: Path | None = None,
        caller_locator: str | None = None,
    ) -> tuple[dict[str, object], dict[str, object]]:
        return self.review_authored(
            target_kind,
            prerequisite_payloads,
            "ready",
            source_path=source_path,
            caller_locator=caller_locator,
        )

    def record_review(
        self,
        target_kind: str,
        prerequisite_payloads: dict[str, dict[str, object]],
        typed_exit: str,
        label: str,
        *,
        source_path: Path | None = None,
        caller_locator: str | None = None,
    ) -> tuple[dict[str, object], dict[str, object]]:
        authored, target = self.review_authored(
            target_kind,
            prerequisite_payloads,
            typed_exit,
            source_path=source_path,
            caller_locator=caller_locator,
        )
        authored_path = self.write_external_json(f"{label}-review-authored.json", authored)
        recorded = GTT.cmd_record_change_request_review(Namespace(
            root=str(self.root),
            mode="standalone",
            input=str(authored_path),
            change_request_input=str(self.source_for_target(target_kind, source_path)),
        ))
        return recorded, target

    def record_and_check_ready(
        self,
        target_kind: str,
        prerequisite_payloads: dict[str, dict[str, object]],
        label: str,
        *,
        source_path: Path | None = None,
        caller_locator: str | None = None,
    ) -> tuple[dict[str, object], dict[str, object]]:
        recorded, target = self.record_review(
            target_kind,
            prerequisite_payloads,
            "ready",
            label,
            source_path=source_path,
            caller_locator=caller_locator,
        )
        recorded_path = self.write_external_json(f"{label}-review-recorded.json", recorded)
        prerequisites_path = self.write_external_json(
            f"{label}-review-prerequisites.json",
            prerequisite_payloads,
        )
        checked = GTT.cmd_check_change_request_review(Namespace(
            root=str(self.root),
            input=str(recorded_path),
            prerequisites_input=str(prerequisites_path),
            change_request_input=str(self.source_for_target(target_kind, source_path)),
            expected_facts_sha256=recorded["facts_sha256"],
        ))
        self.assertEqual(checked["typed_exit"], "ready")
        self.assertEqual(checked["target_identity_sha256"], target["identity_sha256"])
        return recorded, target

    def checker_error_codes(
        self,
        recorded: dict[str, object],
        prerequisite_payloads: dict[str, dict[str, object]],
        label: str,
        *,
        expected_facts_sha256: str | None = None,
        source_path: Path | None = None,
    ) -> list[str]:
        recorded_path = self.write_external_json(f"{label}-recorded.json", recorded)
        prerequisites_path = self.write_external_json(
            f"{label}-prerequisites.json",
            prerequisite_payloads,
        )
        with self.assertRaises(GTT.WorkflowError) as raised:
            GTT.cmd_check_change_request_review(Namespace(
                root=str(self.root),
                input=str(recorded_path),
                prerequisites_input=str(prerequisites_path),
                change_request_input=str(source_path or self.source),
                expected_facts_sha256=(
                    expected_facts_sha256
                    if expected_facts_sha256 is not None
                    else recorded["facts_sha256"]
                ),
            ))
        return raised.exception.payload["error_codes"]

    def structural_errors(
        self,
        result: dict[str, object],
        prerequisites: dict[str, dict[str, object]],
        linkage: dict[str, object],
    ) -> list[str]:
        return GTT.change_request_review_structural_errors(
            self.root,
            result,
            self.target,
            prerequisites,
            linkage,
        )

    def test_interface_declares_semantic_profile_and_five_unique_consumers(self) -> None:
        interface = json.loads((PACKAGE_ROOT / "interface.json").read_text(encoding="utf-8"))
        self.assertEqual(interface["id"], "guru-review-change-request")
        self.assertEqual(interface["judgment_mode"], "semantic")
        self.assertEqual(
            interface["ordered_stages"],
            ["forward_behavior", "ai_review_gate", "conditional_human_confirmation", "recorder_validator", "typed_exit"],
        )
        self.assertEqual(
            interface["modes"]["workflow"]["entry_precondition_ids"],
            interface["modes"]["standalone"]["entry_precondition_ids"],
        )
        exits = interface["external_exits"]
        self.assertEqual([row["id"] for row in exits], list(GTT.CHANGE_REQUEST_REVIEW_CONSUMERS))
        self.assertEqual({row["id"]: row["consumer"] for row in exits}, GTT.CHANGE_REQUEST_REVIEW_CONSUMERS)
        self.assertEqual(len({json.dumps(row["consumer"], sort_keys=True) for row in exits}), 5)

    def test_contract_owns_semantics_and_keeps_scripts_deterministic(self) -> None:
        skill = " ".join((PACKAGE_ROOT / "SKILL.md").read_text(encoding="utf-8").split())
        contract = " ".join((PACKAGE_ROOT / "references/contract.md").read_text(encoding="utf-8").split())
        for phrase in ("AI Review Gate", "stdout-only", "not self-contained or portable"):
            self.assertIn(phrase, skill)
        for phrase in (
            "existing_issue", "proposed_draft", "standalone_request",
            "ten fixed dimensions", "issue-review.json", "guru-create-task-workspace",
            "scripts never map an error code to an exit", "normal honest",
        ):
            self.assertIn(phrase, contract)

    def test_wrappers_are_dispatcher_only_executable_and_package_copy_fails_closed(self) -> None:
        wrappers = {
            "record-change-request-review.sh": "change_request_review_recorder",
            "check-change-request-review.sh": "change_request_review_checker",
        }
        for name, validator in wrappers.items():
            path = PACKAGE_ROOT / "scripts" / name
            content = path.read_text(encoding="utf-8")
            self.assertTrue(path.stat().st_mode & 0o100)
            self.assertIn("run-skill-command.sh", content)
            self.assertIn(f"--validator {validator}", content)
            self.assertNotIn("guru_team_trellis.py", content)
        with tempfile.TemporaryDirectory() as temp:
            copied = Path(temp) / "guru-review-change-request"
            shutil.copytree(PACKAGE_ROOT, copied)
            for name in wrappers:
                process = subprocess.run(
                    [str(copied / "scripts" / name), "--help"],
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=False,
                )
                self.assertEqual(process.returncode, 2, process)
                self.assertIn("not self-contained or portable", process.stderr)

    @unittest.skipIf(importlib.util.find_spec("jsonschema") is None, "jsonschema unavailable")
    def test_schema_and_deidentified_example_are_closed(self) -> None:
        from jsonschema import Draft202012Validator

        schema = json.loads((PACKAGE_ROOT / "schemas/change-request-review.schema.json").read_text(encoding="utf-8"))
        example = json.loads((PACKAGE_ROOT / "examples/issue-review.json").read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema, format_checker=Draft202012Validator.FORMAT_CHECKER)
        self.assertEqual(list(validator.iter_errors(example)), [])
        unexpected = copy.deepcopy(example)
        unexpected["unexpected"] = True
        self.assertNotEqual(list(validator.iter_errors(unexpected)), [])
        serialized = json.dumps(example)
        self.assertNotIn("/Users/", serialized)
        self.assertNotIn(".trellis/tasks/", serialized)
        self.assertNotIn(".trellis/workspace/", serialized)

    def test_all_three_target_variants_normalize_and_reject_stale_normalized_target(self) -> None:
        for kind in ("proposed_draft", "standalone_request"):
            with self.subTest(kind=kind):
                target, _, _ = GTT.change_request_review_normalize_target(
                    self.root,
                    self.raw_draft_target(kind),
                    self.source.name,
                    "standalone",
                )
                self.assertEqual(target["kind"], kind)
                self.assertTrue(target["side_effect_free"])

        with mock.patch.object(GTT, "require_gh_auth"), mock.patch.object(GTT, "issue_view", return_value=self.issue_live):
            scope, _ = GTT.contract_wording_build_scope(
                self.root,
                "change_request",
                "standalone",
                change_request_input=self.issue_source.name,
            )
            title_sha, body_sha, _ = GTT.change_request_review_scope_hashes(scope)
            issue_target, _, _ = GTT.change_request_review_normalize_target(
                self.root,
                {
                    "kind": "existing_issue", "repo": "example/guru-extension",
                    "issue_number": 27,
                    "url": "https://github.com/example/guru-extension/issues/27",
                    "updated_at": "2026-01-01T00:00:00Z",
                    "title_sha256": title_sha, "body_sha256": body_sha,
                },
                self.issue_source.name,
                "standalone",
            )
        self.assertEqual(issue_target["kind"], "existing_issue")
        self.assertFalse(issue_target["side_effect_free"])

        stale = copy.deepcopy(self.target)
        stale["caller_locator"] = "unexpected"
        with self.assertRaises(GTT.WorkflowError) as raised:
            GTT.change_request_review_normalize_target(
                self.root, stale, self.source.name, "standalone"
            )
        self.assertIn("normalized_target_mismatch", str(raised.exception.payload))

    def test_draft_source_request_digest_binds_current_authority_projection(self) -> None:
        source = json.loads(self.source.read_text(encoding="utf-8"))
        projection = GTT.change_request_review_request_authority_projection(
            "example/guru-extension",
            source,
            self.raw_target["body_sha256"],
        )
        self.assertEqual(projection, {
            "kind": "draft",
            "repo": "example/guru-extension",
            "issue_number": None,
            "url": None,
            "state": "draft",
            "updated_at": None,
            "body_sha256": self.raw_target["body_sha256"],
        })
        self.assertEqual(
            self.raw_target["source_request_sha256"],
            GTT.context_digest(projection),
        )
        for kind in ("proposed_draft", "standalone_request"):
            with self.subTest(kind=kind):
                stale = self.raw_draft_target(kind)
                stale["source_request_sha256"] = "0" * 64
                with self.assertRaises(GTT.WorkflowError) as raised:
                    GTT.change_request_review_normalize_target(
                        self.root,
                        stale,
                        str(self.source),
                        "standalone",
                    )
                self.assertIn(
                    "change_request_review_source_request_mismatch",
                    raised.exception.payload["error_codes"],
                )

    def test_production_prerequisites_record_check_to_ready_for_draft_variants(self) -> None:
        for kind in ("proposed_draft", "standalone_request"):
            with self.subTest(kind=kind):
                prerequisites = self.production_prerequisites(
                    f"production-{kind}",
                    target_kind=kind,
                )
                recorded, target = self.record_and_check_ready(
                    kind,
                    prerequisites,
                    f"production-{kind}",
                )
                self.assertEqual(recorded["target"], target)
                self.assertTrue(all(
                    projection["status"] == "current"
                    for projection in recorded["prerequisites"].values()
                ))

    def test_production_existing_issue_record_check_chain_reaches_ready(self) -> None:
        with self.issue_environment():
            prerequisites = self.production_prerequisites(
                "production-existing-issue",
                target_kind="existing_issue",
            )
            recorded, target = self.record_and_check_ready(
                "existing_issue",
                prerequisites,
                "production-existing-issue",
            )
        self.assertEqual(target["kind"], "existing_issue")
        self.assertEqual(target["issue_number"], 27)
        self.assertEqual(target["updated_at"], self.issue_live["updatedAt"])
        self.assertEqual(recorded["target"], target)
        self.assertTrue(all(
            projection["status"] == "current"
            for projection in recorded["prerequisites"].values()
        ))

    def test_production_record_and_check_reject_reused_draft_identity_prerequisites(self) -> None:
        alternate_source = self.io_root / "alternate-draft.json"
        alternate_source.write_text(json.dumps({
            "kind": "draft",
            "draft_id": "draft-28",
            "title": "Add a readiness review Skill",
            "body": "Deliver one current and independently testable change.",
            "selected_comments": [],
        }), encoding="utf-8")
        cases = (
            (
                "proposed-draft-id",
                "proposed_draft",
                alternate_source,
                self.caller_locator,
            ),
            (
                "standalone-request-id",
                "standalone_request",
                alternate_source,
                self.caller_locator,
            ),
            (
                "standalone-caller-locator",
                "standalone_request",
                self.source,
                "request:alternate-27",
            ),
        )
        identity_error = "change_request_review_target_identity_linkage_mismatch"
        for label, target_kind, target_source, target_caller in cases:
            with self.subTest(case=label):
                original = self.production_prerequisites(
                    f"{label}-original",
                    target_kind=target_kind,
                    source_path=self.source,
                    caller_locator=self.caller_locator,
                )
                current = self.production_prerequisites(
                    f"{label}-current",
                    target_kind=target_kind,
                    source_path=target_source,
                    caller_locator=target_caller,
                )
                recorded, target = self.record_and_check_ready(
                    target_kind,
                    current,
                    f"{label}-current",
                    source_path=target_source,
                    caller_locator=target_caller,
                )

                authored, authored_target = self.ready_authored(
                    target_kind,
                    original,
                    source_path=target_source,
                    caller_locator=target_caller,
                )
                self.assertEqual(authored_target, target)
                normalized, scope, contents = GTT.change_request_review_normalize_target(
                    self.root,
                    authored["target"],
                    str(target_source),
                    "standalone",
                )
                projections = GTT.change_request_review_prerequisite_projections(
                    self.root,
                    original,
                    normalized,
                    scope,
                    contents,
                )
                for projection in projections.values():
                    self.assertEqual(projection["status"], "invalid")
                    self.assertIn(identity_error, projection["error_codes"])

                authored_path = self.write_external_json(
                    f"{label}-reused-prerequisites-authored.json",
                    authored,
                )
                with self.assertRaises(GTT.WorkflowError) as raised:
                    GTT.cmd_record_change_request_review(Namespace(
                        root=str(self.root),
                        mode="standalone",
                        input=str(authored_path),
                        change_request_input=str(target_source),
                    ))
                self.assertIn(identity_error, raised.exception.payload["error_codes"])
                self.assertIn(
                    "change_request_review_ready_requires_current_prerequisites",
                    raised.exception.payload["error_codes"],
                )

                errors = self.checker_error_codes(
                    recorded,
                    original,
                    f"{label}-checker-reused-prerequisites",
                    source_path=target_source,
                )
                self.assertIn(identity_error, errors)
                self.assertIn("change_request_review_prerequisites_stale", errors)
                self.assertIn("change_request_review_linkage_stale", errors)
                self.assertIn(
                    "change_request_review_ready_requires_current_prerequisites",
                    errors,
                )

    def test_production_record_and_check_reject_none_identity_projection_combinations(self) -> None:
        identity_error = "change_request_review_target_identity_linkage_mismatch"
        cases = (
            ("issue-proposed", "existing_issue", "proposed_draft"),
            ("issue-standalone", "existing_issue", "standalone_review"),
            ("issue-active-task", "existing_issue", "active_task_scope_change"),
            ("proposed-initial", "proposed_draft", "initial_issue"),
            ("proposed-active-task", "proposed_draft", "active_task_scope_change"),
            ("standalone-initial", "standalone_request", "initial_issue"),
            ("standalone-active-task", "standalone_request", "active_task_scope_change"),
        )
        with self.issue_environment():
            current_by_target: dict[
                str,
                tuple[
                    dict[str, dict[str, object]],
                    dict[str, object],
                    dict[str, object],
                ],
            ] = {}
            for target_kind in (
                "existing_issue",
                "proposed_draft",
                "standalone_request",
            ):
                prerequisites = self.production_prerequisites(
                    f"none-projection-current-{target_kind}",
                    target_kind=target_kind,
                )
                recorded, target = self.record_and_check_ready(
                    target_kind,
                    prerequisites,
                    f"none-projection-current-{target_kind}",
                )
                current_by_target[target_kind] = prerequisites, recorded, target

            for label, target_kind, invocation_kind in cases:
                with self.subTest(case=label):
                    current, recorded, target = current_by_target[target_kind]
                    if invocation_kind == "active_task_scope_change":
                        clarity = self.record_and_check_active_task_clarity(
                            current["context"],
                            label,
                            target_kind=target_kind,
                        )
                    else:
                        clarity = self.record_and_check_clarity(
                            current["context"],
                            label,
                            target_kind=target_kind,
                            invocation_kind=invocation_kind,
                        )
                    mismatched = {
                        "context": current["context"],
                        "clarity": clarity,
                        "wording": current["wording"],
                    }
                    self.assertIsNone(
                        GTT.change_request_review_prerequisite_target_identity_projection(
                            mismatched
                        )
                    )

                    reviewed_source = self.source_for_target(target_kind)
                    authored, authored_target = self.ready_authored(
                        target_kind,
                        mismatched,
                    )
                    self.assertEqual(authored_target, target)
                    normalized, scope, contents = GTT.change_request_review_normalize_target(
                        self.root,
                        authored["target"],
                        str(reviewed_source),
                        "standalone",
                    )
                    self.assertEqual(
                        GTT.change_request_review_context_projection(
                            self.root, mismatched["context"]
                        )["status"],
                        "current",
                    )
                    clarity_projection = GTT.change_request_review_clarity_projection(
                        self.root, mismatched["clarity"]
                    )
                    if invocation_kind == "active_task_scope_change":
                        self.assertEqual(clarity_projection["status"], "invalid")
                        self.assertIn(
                            "active_task_scope_change_requires_task",
                            clarity_projection["error_codes"],
                        )
                    else:
                        self.assertEqual(clarity_projection["status"], "current")
                    self.assertEqual(
                        GTT.change_request_review_wording_projection(
                            self.root,
                            mismatched["wording"],
                            scope,
                            contents,
                        )["status"],
                        "current",
                    )
                    projections = GTT.change_request_review_prerequisite_projections(
                        self.root,
                        mismatched,
                        normalized,
                        scope,
                        contents,
                    )
                    for projection in projections.values():
                        self.assertEqual(projection["status"], "invalid")
                        self.assertIn(identity_error, projection["error_codes"])

                    authored_path = self.write_external_json(
                        f"{label}-none-projection-authored.json",
                        authored,
                    )
                    with self.assertRaises(GTT.WorkflowError) as raised:
                        GTT.cmd_record_change_request_review(Namespace(
                            root=str(self.root),
                            mode="standalone",
                            input=str(authored_path),
                            change_request_input=str(reviewed_source),
                        ))
                    self.assertIn(
                        identity_error,
                        raised.exception.payload["error_codes"],
                    )
                    self.assertIn(
                        "change_request_review_ready_requires_current_prerequisites",
                        raised.exception.payload["error_codes"],
                    )

                    errors = self.checker_error_codes(
                        recorded,
                        mismatched,
                        f"{label}-none-projection-checker",
                        source_path=reviewed_source,
                    )
                    self.assertIn(identity_error, errors)
                    self.assertIn("change_request_review_prerequisites_stale", errors)
                    self.assertIn("change_request_review_linkage_stale", errors)
                    self.assertIn(
                        "change_request_review_ready_requires_current_prerequisites",
                        errors,
                    )

    def test_production_ready_rejects_wrong_exits_and_target_content_mismatch(self) -> None:
        prerequisites = self.production_prerequisites("production-mismatch")
        wrong_exits = {
            "context": "blocked",
            "clarity": "blocked",
            "wording": "blocked",
        }
        for prerequisite, wrong_exit in wrong_exits.items():
            with self.subTest(prerequisite=prerequisite):
                mismatched = copy.deepcopy(prerequisites)
                mismatched[prerequisite]["typed_exit"] = wrong_exit
                authored, _ = self.ready_authored("proposed_draft", mismatched)
                authored_path = self.write_external_json(
                    f"wrong-{prerequisite}-exit.json",
                    authored,
                )
                with self.assertRaises(GTT.WorkflowError) as raised:
                    GTT.cmd_record_change_request_review(Namespace(
                        root=str(self.root),
                        mode="standalone",
                        input=str(authored_path),
                        change_request_input=str(self.source),
                    ))
                self.assertIn(
                    "change_request_review_ready_requires_current_prerequisites",
                    raised.exception.payload["error_codes"],
                )

        context_mismatch = copy.deepcopy(prerequisites)
        context_mismatch["context"] = self.record_and_check_context(
            self.context_payload(body="A different current request body."),
            "context-target-mismatch",
        )
        clarity_mismatch = copy.deepcopy(prerequisites)
        clarity_mismatch["clarity"] = self.record_and_check_clarity(
            prerequisites["context"],
            "clarity-target-mismatch",
            body="A different current request body.",
        )
        for label, mismatched in (
            ("context", context_mismatch),
            ("clarity", clarity_mismatch),
        ):
            with self.subTest(target_content_mismatch=label):
                authored, _ = self.ready_authored("proposed_draft", mismatched)
                authored_path = self.write_external_json(
                    f"{label}-target-content-mismatch.json",
                    authored,
                )
                with self.assertRaises(GTT.WorkflowError) as raised:
                    GTT.cmd_record_change_request_review(Namespace(
                        root=str(self.root),
                        mode="standalone",
                        input=str(authored_path),
                        change_request_input=str(self.source),
                    ))
                self.assertIn(
                    "change_request_review_ready_requires_current_prerequisites",
                    raised.exception.payload["error_codes"],
                )

    def test_production_checker_rejects_consumer_and_context_projection_drift(self) -> None:
        prerequisites = self.production_prerequisites("production-drift")
        recorded, _ = self.record_and_check_ready(
            "proposed_draft",
            prerequisites,
            "production-drift",
        )
        consumer_mismatch = copy.deepcopy(recorded)
        consumer_mismatch["consumer"] = {
            "kind": "stop",
            "id": "wrong-consumer",
        }
        unsigned = copy.deepcopy(consumer_mismatch)
        unsigned.pop("facts_sha256")
        consumer_mismatch["facts_sha256"] = GTT.context_digest(unsigned)
        consumer_path = self.write_external_json(
            "consumer-mismatch-recorded.json",
            consumer_mismatch,
        )
        prerequisites_path = self.write_external_json(
            "consumer-mismatch-prerequisites.json",
            prerequisites,
        )
        with self.assertRaises(GTT.WorkflowError) as raised:
            GTT.cmd_check_change_request_review(Namespace(
                root=str(self.root),
                input=str(consumer_path),
                prerequisites_input=str(prerequisites_path),
                change_request_input=str(self.source),
                expected_facts_sha256=consumer_mismatch["facts_sha256"],
            ))
        self.assertIn(
            "change_request_review_consumer_mismatch",
            raised.exception.payload["error_codes"],
        )

        recorded_path = self.write_external_json("drift-recorded.json", recorded)
        drift_contexts = {
            "current": self.context_payload(current_marker="changed"),
            "history": self.context_payload(history_reason="A different current history conclusion."),
            "duplicate": self.context_payload(duplicate_query="repo:example/guru-extension is:issue is:open alternate query"),
        }
        for label, authored_context in drift_contexts.items():
            with self.subTest(drift=label):
                current = copy.deepcopy(prerequisites)
                current["context"] = self.record_and_check_context(
                    authored_context,
                    f"{label}-drift",
                )
                current_path = self.write_external_json(
                    f"{label}-drift-prerequisites.json",
                    current,
                )
                with self.assertRaises(GTT.WorkflowError) as raised:
                    GTT.cmd_check_change_request_review(Namespace(
                        root=str(self.root),
                        input=str(recorded_path),
                        prerequisites_input=str(current_path),
                        change_request_input=str(self.source),
                        expected_facts_sha256=recorded["facts_sha256"],
                    ))
                self.assertIn(
                    "change_request_review_prerequisites_stale",
                    raised.exception.payload["error_codes"],
                )
                self.assertIn(
                    "change_request_review_linkage_stale",
                    raised.exception.payload["error_codes"],
                )

    def test_production_checker_rejects_current_base_drift(self) -> None:
        prerequisites = self.production_prerequisites("production-base-drift")
        recorded, _ = self.record_and_check_ready(
            "proposed_draft",
            prerequisites,
            "production-base-drift",
        )
        self.git("commit", "--allow-empty", "-q", "-m", "test: advance current base")
        self.git("update-ref", "refs/remotes/origin/main", self.git("rev-parse", "HEAD"))
        current = copy.deepcopy(prerequisites)
        current["context"] = self.record_and_check_context(
            self.context_payload(current_marker="advanced-base"),
            "advanced-base",
        )
        recorded_path = self.write_external_json("base-drift-recorded.json", recorded)
        current_path = self.write_external_json("base-drift-prerequisites.json", current)
        with self.assertRaises(GTT.WorkflowError) as raised:
            GTT.cmd_check_change_request_review(Namespace(
                root=str(self.root),
                input=str(recorded_path),
                prerequisites_input=str(current_path),
                change_request_input=str(self.source),
                expected_facts_sha256=recorded["facts_sha256"],
            ))
        self.assertIn(
            "change_request_review_prerequisites_stale",
            raised.exception.payload["error_codes"],
        )
        self.assertIn(
            "change_request_review_linkage_stale",
            raised.exception.payload["error_codes"],
        )

    def test_production_checker_rejects_clarity_and_wording_stale_hashes(self) -> None:
        prerequisites = self.production_prerequisites("production-prerequisite-freshness")
        recorded, _ = self.record_and_check_ready(
            "proposed_draft",
            prerequisites,
            "production-prerequisite-freshness",
        )

        stale_clarity = copy.deepcopy(prerequisites)
        stale_clarity["clarity"] = self.record_and_check_clarity(
            prerequisites["context"],
            "stale-clarity-content",
            body="A different independently reviewed request body.",
        )
        clarity_hash_mismatch = copy.deepcopy(prerequisites)
        clarity_hash_mismatch["clarity"]["content_identity"]["result_sha256"] = "0" * 64

        alternate_source = self.root / "alternate-draft.json"
        alternate_source.write_text(json.dumps({
            "kind": "draft",
            "draft_id": "alternate-draft-27",
            "title": "Add a readiness review Skill",
            "body": "A separately reviewed wording body.",
            "selected_comments": [],
        }), encoding="utf-8")
        stale_wording = copy.deepcopy(prerequisites)
        stale_wording["wording"] = self.record_and_check_wording(
            "stale-wording-content",
            source_path=alternate_source,
        )
        alternate_source.unlink()

        wording_facts_mismatch = copy.deepcopy(prerequisites)
        wording_facts_mismatch["wording"]["facts_sha256"] = "0" * 64
        wording_scan_mismatch = copy.deepcopy(prerequisites)
        wording_scan_mismatch["wording"]["scan"]["scan_sha256"] = "0" * 64

        cases = {
            "clarity-content-stale": (stale_clarity, True),
            "clarity-facts-mismatch": (clarity_hash_mismatch, True),
            "wording-content-stale": (stale_wording, True),
            "wording-facts-mismatch": (wording_facts_mismatch, True),
            "wording-scan-mismatch": (wording_scan_mismatch, False),
        }
        for label, (current, linkage_changes) in cases.items():
            with self.subTest(case=label):
                errors = self.checker_error_codes(recorded, current, label)
                self.assertIn("change_request_review_prerequisites_stale", errors)
                if linkage_changes:
                    self.assertIn("change_request_review_linkage_stale", errors)
                else:
                    self.assertNotIn("change_request_review_linkage_stale", errors)
                self.assertIn(
                    "change_request_review_ready_requires_current_prerequisites",
                    errors,
                )

    def test_production_checker_enforces_finding_reference_and_hash_closure(self) -> None:
        prerequisites = self.production_prerequisites("production-finding-closure")
        recorded, _ = self.record_review(
            "proposed_draft",
            prerequisites,
            "refresh_context",
            "production-finding-closure",
        )
        mutations = {
            "finding-id": (
                lambda payload: payload["semantic_review"]["dimensions"][0].update(
                    {"finding_ids": ["missing-finding"]}
                ),
                "change_request_review_finding_reference_invalid",
            ),
            "evidence-ref": (
                lambda payload: payload["semantic_review"]["findings"][0].update(
                    {"evidence_refs": ["unbound-evidence"]}
                ),
                "change_request_review_evidence_reference_invalid",
            ),
            "affected-hash": (
                lambda payload: payload["semantic_review"]["findings"][0].update(
                    {"affected_hashes": ["0" * 64]}
                ),
                "change_request_review_affected_hash_invalid",
            ),
        }
        for label, (mutate, expected_error) in mutations.items():
            with self.subTest(case=label):
                invalid = copy.deepcopy(recorded)
                mutate(invalid)
                unsigned = copy.deepcopy(invalid)
                unsigned.pop("facts_sha256")
                invalid["facts_sha256"] = GTT.context_digest(unsigned)
                errors = self.checker_error_codes(
                    invalid,
                    prerequisites,
                    f"finding-closure-{label}",
                )
                self.assertIn(expected_error, errors)

    def test_production_checker_rejects_result_and_expected_facts_mismatch(self) -> None:
        prerequisites = self.production_prerequisites("production-facts-freshness")
        recorded, _ = self.record_and_check_ready(
            "proposed_draft",
            prerequisites,
            "production-facts-freshness",
        )

        digest_mismatch = copy.deepcopy(recorded)
        digest_mismatch["reason"] = "The result bytes changed after recording."
        errors = self.checker_error_codes(
            digest_mismatch,
            prerequisites,
            "result-facts-mismatch",
        )
        self.assertIn("change_request_review_facts_digest_mismatch", errors)

        errors = self.checker_error_codes(
            recorded,
            prerequisites,
            "expected-facts-mismatch",
            expected_facts_sha256="0" * 64,
        )
        self.assertIn("expected_change_request_review_facts_mismatch", errors)

    def test_five_ai_authored_exits_preserve_exact_consumers(self) -> None:
        for typed_exit in GTT.CHANGE_REQUEST_REVIEW_CONSUMERS:
            with self.subTest(typed_exit=typed_exit):
                result, prerequisites, linkage = self.result(typed_exit)
                self.assertEqual(self.structural_errors(result, prerequisites, linkage), [])
                self.assertEqual(result["typed_exit"], typed_exit)
                self.assertEqual(result["consumer"], GTT.CHANGE_REQUEST_REVIEW_CONSUMERS[typed_exit])

        result, prerequisites, linkage = self.result("review_wording")
        result["consumer"] = {"kind": "stop", "id": "wrong-consumer"}
        result["facts_sha256"] = GTT.context_digest({
            key: value for key, value in result.items() if key != "facts_sha256"
        })
        self.assertIn("change_request_review_consumer_mismatch", self.structural_errors(result, prerequisites, linkage))

    def test_missing_or_stale_prerequisites_cannot_become_ready(self) -> None:
        for kind in ("context", "clarity", "wording"):
            with self.subTest(kind=kind):
                prerequisites = self.current_prerequisites()
                prerequisites[kind] = GTT.change_request_review_missing_projection(kind)
                result, expected, linkage = self.result("ready", prerequisites)
                self.assertIn(
                    "change_request_review_ready_requires_current_prerequisites",
                    self.structural_errors(result, expected, linkage),
                )

        result, prerequisites, linkage = self.result("refresh_context")
        current = copy.deepcopy(prerequisites)
        current["context"]["history_sha256"] = "0" * 64
        current_linkage = GTT.change_request_review_linkage(self.target, current)
        errors = self.structural_errors(result, current, current_linkage)
        self.assertIn("change_request_review_prerequisites_stale", errors)
        self.assertIn("change_request_review_linkage_stale", errors)

    def test_empty_ai_gate_and_dimension_loss_fail_closed(self) -> None:
        result, prerequisites, linkage = self.result("ready", gate_override={})
        errors = self.structural_errors(result, prerequisites, linkage)
        self.assertIn("change_request_review_schema_validation_failed", errors)
        self.assertIn("change_request_review_gate_linkage_mismatch", errors)

        result, prerequisites, linkage = self.result("ready")
        result["semantic_review"]["dimensions"].pop()
        result["facts_sha256"] = GTT.context_digest({
            key: value for key, value in result.items() if key != "facts_sha256"
        })
        errors = self.structural_errors(result, prerequisites, linkage)
        self.assertIn("change_request_review_schema_validation_failed", errors)
        self.assertIn("change_request_review_dimensions_invalid", errors)

        result, prerequisites, linkage = self.result("refresh_context")
        result["semantic_review"]["findings"] = []
        for dimension in result["semantic_review"]["dimensions"]:
            dimension["status"] = "passed"
            dimension["finding_ids"] = []
        result["semantic_review"]["ai_review_gate"]["findings_count"] = 0
        result["affected_evidence"] = []
        result["facts_sha256"] = GTT.context_digest({
            key: value for key, value in result.items() if key != "facts_sha256"
        })
        errors = self.structural_errors(result, prerequisites, linkage)
        self.assertIn("change_request_review_non_ready_requires_finding", errors)
        self.assertIn("change_request_review_non_ready_requires_failed_dimension", errors)
        self.assertIn("change_request_review_non_ready_requires_blocking_finding", errors)
        self.assertIn("change_request_review_non_ready_requires_affected_evidence", errors)

    def test_record_and_check_are_stdout_only_and_checker_accepts_normalized_target(self) -> None:
        prerequisite_payloads = {"context": None, "clarity": None, "wording": None}
        projections = GTT.change_request_review_prerequisite_projections(
            self.root,
            prerequisite_payloads,
            self.target,
            self.scope,
            self.contents,
        )
        linkage = GTT.change_request_review_linkage(self.target, projections)
        authored = {
            "generated_at": "2026-01-01T00:00:00Z",
            "mode": "standalone",
            "target": self.raw_target,
            "prerequisite_payloads": prerequisite_payloads,
            "semantic_review": self.semantic_review(linkage, "review_wording"),
            "human_confirmation": {
                "status": "not_required",
                "reason": "The wording owner does not require a new product decision.",
                "proposal_sha256": None,
            },
            "typed_exit": "review_wording",
            "reason": "Current wording evidence is missing.",
            "affected_evidence": [{
                "ref": "prerequisites.wording",
                "sha256": self.target["content_sha256"],
                "summary": "The missing wording projection for the reviewed target.",
            }],
            "consumer": GTT.CHANGE_REQUEST_REVIEW_CONSUMERS["review_wording"],
        }
        authored_path = self.root / "authored.json"
        prerequisites_path = self.root / "prerequisites.json"
        authored_path.write_text(json.dumps(authored), encoding="utf-8")
        prerequisites_path.write_text(json.dumps(prerequisite_payloads), encoding="utf-8")
        runtime_path = Path(GTT.__file__)
        before = {path.relative_to(self.root) for path in self.root.rglob("*")}
        record = subprocess.run(
            [
                "python3", str(runtime_path), "record-change-request-review",
                "--root", str(self.root), "--json", "--mode", "standalone",
                "--input", authored_path.name,
                "--change-request-input", self.source.name,
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(record.returncode, 0, record.stderr)
        recorded = json.loads(record.stdout)
        self.assertEqual(recorded["typed_exit"], "review_wording")
        self.assertEqual(before, {path.relative_to(self.root) for path in self.root.rglob("*")})
        self.assertFalse((self.root / "issue-review.json").exists())

        recorded_path = self.root / "recorded.json"
        recorded_path.write_text(json.dumps(recorded), encoding="utf-8")
        before_check = {path.relative_to(self.root) for path in self.root.rglob("*")}
        check = subprocess.run(
            [
                "python3", str(runtime_path), "check-change-request-review",
                "--root", str(self.root), "--json",
                "--input", recorded_path.name,
                "--prerequisites-input", prerequisites_path.name,
                "--change-request-input", self.source.name,
                "--expected-facts-sha256", recorded["facts_sha256"],
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(check.returncode, 0, check.stderr)
        checked = json.loads(check.stdout)
        self.assertEqual(checked["typed_exit"], "review_wording")
        self.assertEqual(before_check, {path.relative_to(self.root) for path in self.root.rglob("*")})


if __name__ == "__main__":
    unittest.main()
