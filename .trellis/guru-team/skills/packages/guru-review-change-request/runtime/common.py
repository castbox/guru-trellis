from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

from runtime.io import CommandError
from runtime.schema import validate_json


DIMENSIONS = (
    "requirement_completeness", "delivery_unit_consistency", "implementation_target_evidence",
    "claimed_behavior_current", "current_implementation_gap", "docs_code_tests_consistency",
    "archived_history_constraints", "duplicate_reuse_validity", "target_authority_current",
    "prerequisite_hash_linkage",
)
CATEGORIES = {"requirement_gap", "delivery_conflict", "wording_gap", "context_stale", "target_complete", "current_history_conflict", "duplicate_reuse_conflict", "prerequisite_mismatch"}
CONSUMERS = {
    "ready": {"kind": "skill", "id": "guru-create-task-workspace"},
    "clarify_requirements": {"kind": "skill", "id": "guru-clarify-requirements"},
    "review_wording": {"kind": "skill", "id": "guru-review-contract-wording"},
    "refresh_context": {"kind": "skill", "id": "guru-sync-base"},
    "blocked": {"kind": "stop", "id": "change-request-review-blocked"},
}
GATES = {"ready": "passed", "clarify_requirements": "reroute", "review_wording": "reroute", "refresh_context": "reroute", "blocked": "blocked"}


def parse(parser, argv):
    parser.add_argument("--json", action="store_true")
    try:
        return parser.parse_args(argv)
    except SystemExit as exc:
        raise CommandError("invalid_arguments", "arguments", "Use the exact command help contract.") from exc


def root(package_root, value=None):
    candidate = Path(value or ".").resolve()
    if not candidate.is_dir():
        raise CommandError("unsafe_path", "root", "Use a repository root.")
    return candidate


def load(repo, package_root, value, field):
    if value == "-":
        raw = sys.stdin.read()
    else:
        source = Path(str(value or ""))
        choices = [source] if source.is_absolute() else [repo / source, package_root / source]
        source = next((path for path in choices if path.is_file() and not path.is_symlink()), None)
        if source is None:
            raise CommandError("unsafe_path", field, "Use a regular JSON file below the repository or package.")
        raw = source.read_text(encoding="utf-8")
    try:
        value = json.loads(raw)
    except (TypeError, json.JSONDecodeError) as exc:
        raise CommandError("invalid_json", field, "Provide one valid JSON object.") from exc
    if not isinstance(value, dict):
        raise CommandError("invalid_json", field, "Provide one valid JSON object.")
    return value


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def validate_owner(package_root, payload, field="input"):
    validate_json(payload, package_root / "schemas/change-request-review.schema.json", field)
    return payload


def normalize_target(source, authored_target):
    if not isinstance(source, dict) or not isinstance(authored_target, dict):
        raise CommandError("schema_mismatch", "target", "Provide current source and target objects.")
    title = str(source.get("title") or "")
    body = str(source.get("body") or "")
    title_hash, body_hash = sha(title), sha(body)
    content_hash = digest({"title_sha256": title_hash, "body_sha256": body_hash})
    kind = authored_target.get("kind")
    repo = authored_target.get("repo")
    if not isinstance(repo, str) or re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo) is None:
        raise CommandError("schema_mismatch", "target.repo", "Use owner/repository.")
    common = {"kind": kind, "repo": repo, "issue_number": None, "url": None, "updated_at": None, "draft_id": None, "source_request_sha256": None, "caller_locator": None, "request_id": None, "title_sha256": title_hash, "body_sha256": body_hash, "side_effect_free": True}
    if kind == "existing_issue":
        number = source.get("number")
        url = f"https://github.com/{repo}/issues/{number}"
        if source.get("kind") != "issue" or source.get("repo") != repo or not isinstance(number, int) or authored_target.get("issue_number") != number or authored_target.get("url") != url or authored_target.get("updated_at") != source.get("updated_at"):
            raise CommandError("stale_identity", "target", "Reread the current issue authority.", 3)
        common.update({"issue_number": number, "url": url, "updated_at": source.get("updated_at"), "side_effect_free": False})
    elif kind in {"proposed_draft", "standalone_request"}:
        request_id = source.get("draft_id")
        authority = {"kind": "draft", "repo": repo, "issue_number": None, "url": None, "state": "draft", "updated_at": None, "body_sha256": body_hash}
        request_hash = digest(authority)
        if source.get("kind") != "draft" or not isinstance(request_id, str) or authored_target.get("source_request_sha256") != request_hash:
            raise CommandError("stale_identity", "target", "Reread the current draft authority.", 3)
        if kind == "proposed_draft":
            if authored_target.get("draft_id") != request_id:
                raise CommandError("stale_identity", "target.draft_id", "Use the current draft id.", 3)
            common.update({"draft_id": request_id, "source_request_sha256": request_hash})
        else:
            if authored_target.get("request_id") != request_id or not authored_target.get("caller_locator"):
                raise CommandError("stale_identity", "target.request_id", "Use the current standalone request identity.", 3)
            common.update({"request_id": request_id, "caller_locator": authored_target["caller_locator"], "source_request_sha256": request_hash})
    else:
        raise CommandError("schema_mismatch", "target.kind", "Use one declared target kind.")
    identity = {key: value for key, value in common.items() if key not in {"side_effect_free"} and value is not None}
    common["identity_sha256"] = digest(identity)
    common["content_sha256"] = content_hash
    for key in ("title_sha256", "body_sha256", "identity_sha256", "content_sha256"):
        if key in authored_target and authored_target[key] != common[key]:
            raise CommandError("stale_identity", f"target.{key}", "Rerun against current target content.", 3)
    return common


def live_issue_source(source):
    if not isinstance(source, dict) or source.get("kind") != "issue":
        return source
    repo, number = source.get("repo"), source.get("number")
    if not isinstance(repo, str) or not isinstance(number, int):
        raise CommandError("schema_mismatch", "change_request_input", "Use current issue repo and number.")
    proc = subprocess.run(["gh", "issue", "view", str(number), "--repo", repo, "--json", "number,url,state,title,body,updatedAt"], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode:
        raise CommandError("stale_identity", "change_request_input", proc.stderr.strip() or "Reread the current issue.", 3)
    try:
        live = json.loads(proc.stdout)
    except Exception as exc:
        raise CommandError("invalid_json", "change_request_input", "GitHub returned invalid JSON.") from exc
    expected_url = f"https://github.com/{repo}/issues/{number}"
    if str(live.get("state") or "").lower() != "open" or live.get("url") != expected_url or live.get("title") != source.get("title") or live.get("body") != source.get("body") or live.get("updatedAt") != source.get("updated_at"):
        raise CommandError("stale_identity", "change_request_input", "Issue content changed; refresh context.", 3)
    return source


def normalize_prerequisites(transition, target, source, package_root):
    stage = transition.get("stage") if isinstance(transition, dict) else None
    if stage not in {"context_current", "clarity_current", "wording_current"}:
        raise CommandError("schema_mismatch", "transition", "Provide a declared public prerequisite stage transition.")
    schema = package_root.parents[1] / "consumers/workflow/stage0/transitions" / (stage.replace("_", "-") + ".schema.json")
    validate_json(transition, schema, "transition")
    if stage == "context_current" and transition["authority_content_sha256"] != target["body_sha256"]:
        raise CommandError("stale_identity", "transition.authority_content_sha256", "Refresh context for the current body.", 3)
    result = {}
    fields = {"clarity": ("facts_sha256", "target_sha256", "disposition_sha256", "content_sha256", "scope_sha256"),
              "wording": ("facts_sha256", "scope_sha256", "scan_sha256", "target_content_sha256")}
    for name, keys in fields.items():
        present = name in transition
        result[name] = {"status": "current" if present else "missing",
                        **{key: transition[name][key] if present else None for key in keys}}
    if "clarity" in transition:
        clarity = transition["clarity"]
        if (transition["clarity_result_sha256"] != clarity["facts_sha256"]
                or (stage == "clarity_current" and transition["target_content_sha256"] != clarity["content_sha256"])):
            raise CommandError("schema_mismatch", "transition.clarity", "Use consistent public clarity facts and disposition identities.")
    if "wording" in transition:
        wording = transition["wording"]
        if transition["wording_facts_sha256"] != wording["facts_sha256"] or transition["target_content_sha256"] != wording["target_content_sha256"]:
            raise CommandError("schema_mismatch", "transition.wording", "Use consistent public wording facts and content identities.")
        if wording["target_content_sha256"] != target["content_sha256"]:
            raise CommandError("stale_identity", "transition.wording.target_content_sha256", "Refresh wording for the current title and body.", 3)
    return result


def invocation(package_root, argv, *, final=False):
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root")
    parser.add_argument("--invocation", required=True)
    args = parse(parser, argv)
    envelope = load(root(package_root, args.root), package_root, args.invocation, "invocation")
    schema = (package_root.parents[1] / "consumers/workflow/stage0/invocations/semantic-owner.schema.json"
              if final else package_root / "schemas/review-invocation.schema.json")
    validate_json(envelope, schema, "invocation")
    public, context, owner = envelope["public_input"], envelope["owner_context"], envelope["owner_result"]
    profile = public.get("profile")
    schemas = {"current_issue": "public-current-issue-input.schema.json", "proposed_draft": "public-proposed-draft-input.schema.json", "standalone_request": "public-standalone-request-input.schema.json"}
    if profile not in schemas:
        raise CommandError("schema_mismatch", "public_input.profile", "Use one declared source profile.")
    validate_json(public, package_root / "schemas" / schemas[profile], "public_input")
    if set(context) != {"change_request"} or not isinstance(context["change_request"], dict):
        raise CommandError("schema_mismatch", "owner_context", "Provide only the current change_request source.")
    source = context["change_request"]
    if source.get("kind") != ("issue" if profile == "current_issue" else "draft") or not isinstance(owner.get("target"), dict) or owner["target"].get("kind") != ("existing_issue" if profile == "current_issue" else profile):
        raise CommandError("schema_mismatch", "public_input.profile", "Match the public profile, source kind and reviewed target kind.")
    if not isinstance(source.get("title"), str) or not isinstance(source.get("body"), str):
        raise CommandError("schema_mismatch", "owner_context.change_request", "Provide the current title and body strings.")
    if "prerequisite_payloads" in owner:
        raise CommandError("schema_mismatch", "owner_result.prerequisite_payloads", "Consume the public transition, not authored prerequisite payloads.")
    target = normalize_target(source, owner["target"])
    transition = envelope.get("transition")
    prerequisites = normalize_prerequisites(transition, target, source, package_root)
    if owner.get("mode") != public["mode"]:
        raise CommandError("schema_mismatch", "owner_result.mode", "Match the reviewed invocation mode.")
    for key in ("mode", "target_locator", "continuation_id"):
        if transition[key] != public[key]:
            raise CommandError("stale_identity", "transition." + key, "Use the same current public handoff.", 3)
    expected_locator = target["url"] if profile == "current_issue" else source["draft_id"]
    if public["target_locator"] != expected_locator:
        raise CommandError("stale_identity", "public_input.target_locator", "Use the current source target locator.", 3)
    required_stage = {"ready": "wording_current", "clarify_requirements": "context_current", "review_wording": "clarity_current"}.get(owner.get("typed_exit"))
    if required_stage and transition["stage"] != required_stage:
        raise CommandError("schema_mismatch", "transition.stage", "Provide the original " + required_stage + " transition for the AI-selected exit.")
    return envelope, target, prerequisites


def linkage(target, prerequisites):
    value = {"target_identity_sha256": target["identity_sha256"], "target_content_sha256": target["content_sha256"], "clarity_facts_sha256": prerequisites["clarity"].get("facts_sha256"), "clarity_disposition_sha256": prerequisites["clarity"].get("disposition_sha256"), "wording_facts_sha256": prerequisites["wording"].get("facts_sha256")}
    value["linkage_sha256"] = digest(value)
    return value


def validate_semantics(authored, target, prerequisites, linked):
    exit_id = authored.get("typed_exit")
    semantic = authored.get("semantic_review") if isinstance(authored.get("semantic_review"), dict) else {}
    dimensions = semantic.get("dimensions") if isinstance(semantic.get("dimensions"), list) else []
    findings = semantic.get("findings") if isinstance(semantic.get("findings"), list) else []
    if [row.get("id") for row in dimensions if isinstance(row, dict)] != list(DIMENSIONS):
        raise CommandError("schema_mismatch", "semantic_review.dimensions", "Review all ten dimensions in declared order.")
    ids = [row.get("finding_id") for row in findings if isinstance(row, dict)]
    if len(ids) != len(findings) or len(ids) != len(set(ids)) or any(row.get("category") not in CATEGORIES for row in findings):
        raise CommandError("schema_mismatch", "semantic_review.findings", "Use unique findings with declared categories.")
    referenced = {item for row in dimensions for item in row.get("finding_ids", [])}
    if referenced != set(ids):
        raise CommandError("schema_mismatch", "semantic_review.findings", "Reference every finding from a reviewed dimension.")
    gate = semantic.get("ai_review_gate") if isinstance(semantic.get("ai_review_gate"), dict) else {}
    scope = semantic.get("scope_conclusion") if isinstance(semantic.get("scope_conclusion"), dict) else {}
    if exit_id not in CONSUMERS or authored.get("consumer") != CONSUMERS[exit_id] or gate.get("status") != GATES[exit_id] or gate.get("reviewed_linkage_sha256") != linked["linkage_sha256"] or gate.get("findings_count") != len(findings) or gate.get("scope_conclusion_sha256") != digest(scope):
        raise CommandError("schema_mismatch", "semantic_review.ai_review_gate", "Bind gate, exit, consumer, findings, and scope to current linkage.")
    if exit_id == "ready":
        if any(row.get("status") != "passed" for row in dimensions) or any(row.get("blocking") for row in findings) or any(row.get("status") != "current" for row in prerequisites.values()):
            raise CommandError("schema_mismatch", "typed_exit", "Ready requires current prerequisites and a passed finding-free gate.")
    elif not findings or not any(row.get("blocking") for row in findings) or not any(row.get("status") == "failed" for row in dimensions):
        raise CommandError("schema_mismatch", "typed_exit", "Non-ready exits require a blocking finding and failed dimension.")


def build_result(authored, target, prerequisites):
    linked = linkage(target, prerequisites)
    validate_semantics(authored, target, prerequisites, linked)
    result = {"schema_version": "2.0", "skill_id": "guru-review-change-request", "generated_at": authored.get("generated_at"), "mode": authored.get("mode"), "target": target, "prerequisites": prerequisites, "evidence_linkage": linked, "semantic_review": authored.get("semantic_review"), "typed_exit": authored.get("typed_exit"), "reason": authored.get("reason"), "affected_evidence": authored.get("affected_evidence"), "consumer": authored.get("consumer")}
    result["facts_sha256"] = digest(result)
    return result


def check_result(package_root, payload, target, prerequisites):
    validate_owner(package_root, payload)
    expected = build_result({key: copy.deepcopy(payload[key]) for key in ("generated_at", "mode", "semantic_review", "typed_exit", "reason", "affected_evidence", "consumer")}, target, prerequisites)
    if payload != expected:
        raise CommandError("stale_identity", "input", "Rerun review against current target and prerequisites.", 3)
    return payload


def validation_receipt(payload, transition):
    value = {"schema_version": "1.0", "skill_id": "guru-review-change-request", "operation": "check-change-request-review", "result_sha256": payload["facts_sha256"], "prerequisite_sha256": digest({"prerequisites": payload["prerequisites"], "transition": transition}), "snapshot_sha256": digest(payload["target"])}
    value["receipt_sha256"] = digest(value)
    return value


def check_receipt(payload, receipt, transition):
    if receipt != validation_receipt(payload, transition):
        raise CommandError("stale_identity", "validation_receipt", "Run the readiness checker for this exact result and prerequisites.", 3)
