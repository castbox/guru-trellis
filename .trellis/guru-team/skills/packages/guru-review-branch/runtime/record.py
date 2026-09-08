from __future__ import annotations

import argparse
import copy
from datetime import datetime, timezone
from pathlib import Path

from common import (
    ancestor,
    content_identity,
    digest,
    dirty_paths,
    git,
    load,
    parse,
    rel,
    root,
    store_checkpoint,
    task,
    tree_identity,
    validate_gate,
)
from runtime.io import CommandError
from runtime.reviewed_content import REVIEWED_CONTENT_ALGORITHM
from runtime.schema import validate_json


def run(package_root: Path, command: dict, argv: list[str]) -> dict:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root")
    parser.add_argument("--task")
    parser.add_argument("--skill-input", required=True)
    parser.add_argument("--semantic-review-file", required=True)
    parser.add_argument(
        "--typed-exit",
        required=True,
        choices=(
            "passed",
            "continuity_passed",
            "implementation_required",
            "scope_confirmation_required",
            "blocked",
        ),
    )
    args = parse(parser, argv)
    repo = root(package_root, args.root)
    task_dir = task(repo, args.task)
    public = load(repo, package_root, args.skill_input, "skill_input")
    auth = load(repo, package_root, args.semantic_review_file, "semantic_review_file")
    head = git(repo, "rev-parse", "HEAD")
    profile = public.get("profile")
    schema = {
        "branch_review": "public-branch-review-input.schema.json",
        "base_continuity": "public-base-continuity-input-2.0.schema.json",
    }.get(profile)
    if schema is None:
        raise CommandError(
            "schema_mismatch", "input.profile", "Use one declared Branch Review profile."
        )
    validate_json(public, package_root / "schemas" / schema, "skill_input")
    task_ref = rel(repo, task_dir)
    if public["task_ref"] != task_ref:
        raise CommandError(
            "stale_identity", "task", "Record the review for the exact task owner.", 3
        )
    if profile == "branch_review" and public.get("branch_review_commit") != head:
        raise CommandError(
            "stale_identity", "branch_review_commit", "Review current HEAD.", 3
        )
    base_ref = public["new_base_head"] if profile == "base_continuity" else public["base_ref"]
    base_head = git(repo, "rev-parse", base_ref)
    if profile == "branch_review" and not ancestor(repo, base_head, head):
        raise CommandError(
            "stale_identity", "base_ref", "Review base must precede current task content.", 3
        )
    if profile == "base_continuity":
        checks = (
            (public["task_head"] == head, "task_head", "Review current reconciled HEAD."),
            (
                ancestor(repo, public["old_base_head"], public["new_base_head"]),
                "old_base_head",
                "Review one exact ancestor base pair.",
            ),
            (
                public["branch_review_commit"] != head
                and ancestor(repo, public["branch_review_commit"], head),
                "branch_review_commit",
                "Use one prior full-review commit in current history.",
            ),
            (
                ancestor(repo, public["new_base_head"], head),
                "new_base_head",
                "Current reconciled HEAD must contain the reviewed base.",
            ),
            (
                tree_identity(repo, head) == public["candidate_tree_sha256"],
                "candidate_tree_sha256",
                "Current committed tree must match the integration candidate.",
            ),
        )
        for valid, field, remediation in checks:
            if not valid:
                raise CommandError("stale_identity", field, remediation, 3)
    if dirty_paths(repo, public["task_ref"]):
        raise CommandError(
            "stale_identity",
            "worktree",
            "Commit or remove all non-review overlays before branch review.",
            3,
        )
    semantic = auth.get("semantic_review", auth)
    gate = semantic.get("ai_review_gate", {})
    findings = semantic.get("qualified_findings", [])
    proposals = semantic.get("scope_proposals", [])
    if gate.get("status") != args.typed_exit:
        raise CommandError(
            "schema_mismatch", "ai_review_gate.status", "Bind the exact typed exit."
        )
    if args.typed_exit in {"passed", "continuity_passed"} and (
        any(item.get("status") == "open" for item in findings) or proposals
    ):
        raise CommandError(
            "schema_mismatch", "typed_exit", "Pass requires no open findings or scope proposals."
        )
    if (profile == "base_continuity") != (args.typed_exit == "continuity_passed"):
        raise CommandError(
            "schema_mismatch",
            "typed_exit",
            "Base continuity must use its dedicated pass exit; full review must not use it.",
        )
    if args.typed_exit == "implementation_required" and not any(
        item.get("status") == "open" for item in findings
    ):
        raise CommandError(
            "schema_mismatch",
            "typed_exit",
            "Implementation route requires an open finding.",
        )
    if args.typed_exit == "scope_confirmation_required" and (
        not proposals or any(item.get("status") == "open" for item in findings)
    ):
        raise CommandError(
            "schema_mismatch",
            "typed_exit",
            "Scope route requires proposals and no open findings.",
        )
    if (
        args.typed_exit == "passed"
        and any(item.get("status") == "resolved" for item in findings)
        and public.get("review_intent") != "fresh_final_review"
    ):
        raise CommandError(
            "schema_mismatch",
            "review_intent",
            "Resolved findings require fresh_final_review.",
        )
    pair = (
        None
        if profile == "branch_review"
        else {
            **{
                key: public[key]
                for key in (
                "task_head",
                "old_base_head",
                "new_base_head",
                "candidate_tree_sha256",
                "relevant_paths",
                "resume_target",
                )
            },
            "prior_branch_review_commit": public["branch_review_commit"],
        }
    )
    value = {
        "schema_version": "7.0",
        "skill_id": "guru-review-branch",
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "task_dir": task_ref,
        "mode": public["mode"],
        "profile": profile,
        "review_intent": public["review_intent"],
        "typed_exit": args.typed_exit,
        "review_commit": head,
        "reviewed_content_algorithm": REVIEWED_CONTENT_ALGORITHM,
        "reviewed_content_sha256": content_identity(repo, head),
        "base_ref": base_ref,
        "base_head": base_head,
        "integration_pair": pair,
        "candidate_classifications": copy.deepcopy(auth.get("candidate_classifications")),
        "semantic_review": semantic,
        "verification_evidence": auth.get("verification_evidence"),
    }
    value["facts_sha256"] = digest(
        {
            key: copy.deepcopy(item)
            for key, item in value.items()
            if key not in {"generated_at", "facts_sha256"}
        }
    )
    validate_gate(package_root, repo, value)
    _, duplicate = store_checkpoint(repo, task_dir, value)
    return {
        "status": "duplicate" if duplicate else "recorded",
        "task_ref": task_ref,
        "typed_exit": args.typed_exit,
        "checkpoint_id": "review-gate",
    }
