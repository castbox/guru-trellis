from __future__ import annotations

import copy
import hashlib
import subprocess

from common import ancestor, git
from runtime.io import CommandError
from runtime.schema import validate_json


PROFILE = "delivery_promotion_reference_alignment"


def facts(package_root, repo, public):
    """Bind the original public result and all Git bytes; AI judges their meaning."""
    validate_json(
        public,
        package_root / "schemas/public-delivery-promotion-reference-alignment-input-1.0.schema.json",
        "input",
    )
    prior = public["prior_review"]
    base = public["prior_reviewed_base_head"]
    reviewed = prior["branch_review_commit"]
    final = public["branch_review_commit"]
    if (prior["task_ref"] != public["task_ref"]
            or prior["delivery_key"] != public["delivery_key"]
            or base != public["base_ref"]):
        raise CommandError(
            "stale_identity", "prior_review",
            "Recover the actual original full Review result and its fixed content base.", 3,
        )
    if (git(repo, "rev-parse", "HEAD") != final
            or git(repo, "rev-parse", base + "^{commit}") != base
            or reviewed == final or not ancestor(repo, base, reviewed)
            or not ancestor(repo, reviewed, final)):
        raise CommandError(
            "stale_identity", "prior_review.branch_review_commit",
            "Use the original reviewed Git object and current descendant candidate; otherwise run full Review.", 3,
        )
    delta = subprocess.run(
        ["git", "diff", "--no-ext-diff", "--no-textconv", "--binary",
         "--full-index", "--no-renames", reviewed, final, "--"],
        cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    if delta.returncode:
        raise CommandError(
            "stale_identity", "promotion_alignment", "Read the complete original-to-final Git delta.", 3,
        )
    return {
        "prior_review": copy.deepcopy(prior),
        "prior_reviewed_base_head": base,
        "delta_sha256": hashlib.sha256(delta.stdout).hexdigest(),
    }


def validate_facts(package_root, repo, gate):
    public = {
        "profile": PROFILE, "mode": gate["mode"], "task_ref": gate["task_dir"],
        "delivery_key": gate["delivery_key"], "base_ref": gate["base_ref"],
        "branch_review_commit": gate["review_commit"], "check_result_id": gate["check_result_id"],
        **{key: gate["promotion_alignment"][key]
           for key in ("prior_review", "prior_reviewed_base_head")},
    }
    if facts(package_root, repo, public) != gate["promotion_alignment"]:
        raise CommandError(
            "stale_identity", "promotion_alignment", "Review the current complete alignment delta again.", 3,
        )
