"""Objective terminal attribution and public recording after the AI review.

No pre-merge gate, remote merge, readiness judgment or Completion decision.
"""
from __future__ import annotations

import os
import subprocess

from owner import archived_fact_gap, gh_json, git, require_gh
from runtime.delivery_projection.adapter import DeliveryProjection
from runtime.io import CommandError
from runtime.schema import validate_json
from runtime.task_lifecycle import LifecycleContractError


def blocked(package, public, reason, remediation):
    output = {"exit_id": "merge_blocked", "repo_ref": public["repo_ref"],
              "pr_number": public["pr_number"], "reason_code": reason, "remediation": remediation}
    validate_json(output, package / "schemas/public-output-delivery-merge-blocked-1.0.schema.json", "stdout")
    return output


def publication_relation(projection, key, repo_ref, pr_number):
    """One existing public Publication, never a branch/title inference."""
    delivery = projection.resolve(key)
    record = projection.read_record()
    if key["task_id"] != record["id"] or delivery["profile"] != "pull_request":
        raise CommandError("stale_identity", "delivery_key", "Select this Task's published pull-request Delivery.", 3)
    matches = [row for row in record["deliveries"]
               if row["publication_result"] is not None
               and row["publication_result"]["repo_ref"].casefold() == repo_ref.casefold()
               and row["publication_result"]["pr_number"] == pr_number]
    if not matches:
        return delivery, None, "manual_merge_missing_publication"
    if len(matches) != 1:
        return delivery, None, "manual_merge_ambiguous_publication"
    if (matches[0]["id"], matches[0]["lifecycle_generation"]) != (key["delivery_id"], key["lifecycle_generation"]):
        return delivery, None, "manual_merge_publication_mismatch"
    return delivery, matches[0]["publication_result"], None


def ensure_commit(root, repo_ref, sha):
    """Fetch only a missing immutable object from the selected repository."""
    import re
    if not isinstance(sha, str) or not re.fullmatch(r"[0-9a-f]{40}", sha):
        raise CommandError("github_response_incomplete", "github.commit", "Read one full immutable commit SHA.")
    if subprocess.run(["git", "cat-file", "-e", sha + "^{commit}"], cwd=root,
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode:
        result = subprocess.run(["git", "fetch", "--no-tags", "https://github.com/" + repo_ref + ".git", sha],
                                cwd=root, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result.returncode:
            raise CommandError("stale_identity", "repository.commit", "Fetch the exact selected PR/merge commit before recovery.", 3)


def candidate_read_error(root, head, paths, error):
    """Diagnose an unsuccessful public read without reading any blob bodies.

    The public API uses invalid_git_fact for unavailable objects and unsupported
    modes alike. Only the former belongs to the history preparation owner.
    """
    environment = {key: value for key, value in os.environ.items()
                   if not key.upper().startswith("GIT_")}
    environment["GIT_NO_LAZY_FETCH"] = "1"
    args = ["git", "--literal-pathspecs", "ls-tree", "-t", "-z", head, "--"]
    fixed = sum(len(os.fsencode(arg)) + 1 for arg in args)
    batches, batch, used = [], [], fixed
    for path in paths:
        size = len(os.fsencode(path)) + 1
        if fixed + size > 64 * 1024:
            return CommandError("stale_identity", "repository", error.remediation, 3)
        if used + size > 64 * 1024:
            batches.append(batch)
            batch, used = [], fixed
        batch.append(path)
        used += size
    if batch:
        batches.append(batch)
    selected = set(paths)
    try:
        for batch in batches:
            result = subprocess.run([*args, *batch], cwd=root, env=environment,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            for row in result.stdout.split(b"\0"):
                if not row:
                    continue
                metadata, name = row.split(b"\t", 1)
                mode, kind, _oid = metadata.split()
                if (os.fsdecode(name) in selected
                        and (kind != b"blob" or mode not in (b"100644", b"100755"))):
                    return CommandError("stale_identity", "candidate.paths",
                                        "Use the file/mode candidate supported by the installed public API.", 3)
    except (OSError, subprocess.SubprocessError, ValueError):
        pass
    return CommandError("stale_identity", "repository", error.remediation, 3)


def commit_candidate(projection, publication, actual_head, *, git_root=None, content=None):
    """Use the installed public hash over immutable bytes/modes/deletions."""
    candidate = publication["candidate"]
    paths = candidate["paths"]
    source = projection.root if git_root is None else git_root
    if content is None:
        with projection._call(projection.api.delivery_store.GitCandidateContent,
                              source, no_lazy_fetch=True) as local:
            return commit_candidate(projection, publication, actual_head,
                                    git_root=source, content=local)
    try:
        content_ref = projection._call(content.content_ref, actual_head, paths)
    except LifecycleContractError as exc:
        if exc.code != "invalid_git_fact":
            raise
        raise candidate_read_error(source, actual_head, paths, exc) from exc
    return {**candidate, "kind": "git", "head_ref": actual_head, "content_ref": content_ref}


def terminal_facts(root, public, publication):
    repo, number = public["repo_ref"], public["pr_number"]
    require_gh(root)
    repository = gh_json(root, ["api", f"repos/{repo}"], "repository")
    if str(repository.get("full_name", "")).casefold() != repo.casefold():
        raise CommandError("stale_identity", "github.repository", "Read the exact selected repository.", 3)
    pr = gh_json(root, ["api", f"repos/{repo}/pulls/{number}"], "merged PR")
    if not pr.get("merged_at"):
        return None, "manual_merge_not_merged"
    try:
        head = pr["head"]["sha"]
        target = pr["base"]["ref"]
        merge = pr["merge_commit_sha"]
        base_repo, head_repo = pr["base"]["repo"]["full_name"], pr["head"]["repo"]["full_name"]
    except (KeyError, TypeError) as exc:
        raise CommandError("github_response_incomplete", "github.pr", "Read complete repo/base/head/merge identity.") from exc
    if (pr.get("number") != number or pr.get("state", "").upper() != "CLOSED"
            or base_repo.casefold() != repo.casefold() or head_repo.casefold() != repo.casefold()
            or target != publication["target_ref"]):
        return None, "manual_merge_pr_identity_mismatch"
    commit = gh_json(root, ["api", f"repos/{repo}/git/commits/{merge}"], "merge commit")
    try:
        parents = [row["sha"] for row in commit["parents"]]
    except (KeyError, TypeError) as exc:
        raise CommandError("github_response_incomplete", "github.merge_commit", "Read actual merge parents.") from exc
    if len(parents) != 2:
        return None, "unsupported_manual_merge_method"
    if commit.get("sha") != merge or parents[1] != head:
        return None, "manual_merge_commit_identity_mismatch"
    base = gh_json(root, ["api", f"repos/{repo}/git/ref/heads/{target}"], "target base")
    try:
        base_head = base["object"]["sha"]
    except (KeyError, TypeError) as exc:
        raise CommandError("github_response_incomplete", "github.base_ref", "Read the current selected target base.") from exc
    prepared = []
    for sha in (merge, head, base_head, publication["reviewed_head"]):
        if sha not in prepared:
            ensure_commit(root, repo, sha)
            prepared.append(sha)
    if git(root, "rev-list", "--parents", "-n", "1", merge).split() != [merge, *parents]:
        return None, "manual_merge_commit_identity_mismatch"
    if merge not in git(root, "rev-list", "--first-parent", base_head).splitlines():
        return None, "manual_merge_target_ancestry_mismatch"
    checks = gh_json(root, ["pr", "view", str(number), "--repo", repo, "--json",
                           "number,headRefOid,statusCheckRollup,reviewDecision"], "actual checks and reviews")
    if (checks.get("number") != number or checks.get("headRefOid") != head
            or "statusCheckRollup" not in checks
            or checks["statusCheckRollup"] is not None and not isinstance(checks["statusCheckRollup"], list)):
        raise CommandError("github_response_incomplete", "github.checks", "Read this actual merged head's checks, including an empty missing set.")
    # Unfiltered deltas are read even if candidate.paths would miss new paths.
    return {"repo_ref": repo, "pr_number": number, "head_sha": head, "merge_sha": merge,
            "target_ref": target, "checks": checks["statusCheckRollup"] or [],
            "publication_delta": git(root, "diff", "--name-status", publication["reviewed_head"], head, "--"),
            "pr_delta": git(root, "diff", "--name-status", parents[0], head, "--")}, None


def invoke(root, package, public, review):
    validate_json(public, package / "schemas/public-delivery-merged-recovery-input-1.0.schema.json", "input")
    validate_json(review, package / "schemas/manual-merged-review-1.0.schema.json", "review_input")
    try:
        projection = DeliveryProjection(root, public["task_ref"])
        delivery, publication, reason = publication_relation(projection, public["delivery_key"], public["repo_ref"], public["pr_number"])
        if reason:
            return blocked(package, public, reason, "Resolve the exact existing public Publication association through original Merge/Publish; do not create an identity.")
        facts, reason = terminal_facts(root, public, publication)
        if reason:
            return blocked(package, public, reason, "Original Merge requires an attributable actual two-parent MERGED PR on its recorded target base; no remote merge is performed.")
        reviewed_pr = {key: facts[key] for key in ("repo_ref", "pr_number", "head_sha", "merge_sha", "target_ref")}
        if (review["reviewed_delivery_key"] != public["delivery_key"]
                or review["publication_result_id"] != publication["result_id"]
                or review["reviewed_pr"] != reviewed_pr
                or review["observed_checks"] != facts["checks"]):
            raise CommandError("stale_identity", "review_input", "Reread actual association, head/content and CI facts and complete this recovery review.", 3)
        actual = commit_candidate(projection, publication, facts["head_sha"])
        impact = review["content_impact"]
        if impact["kind"] == "same_candidate" and (actual != publication["candidate"] or facts["publication_delta"]):
            raise CommandError("stale_identity", "content_impact", "Review the full actual candidate delta and affected original owners.", 3)
        if impact["kind"] == "equivalent_candidate" and actual["content_ref"] != publication["candidate"]["content_ref"]:
            raise CommandError("stale_identity", "content_impact", "Different candidate bytes require an explicit changed-candidate impact review.", 3)
        if review["ai_review_gate"]["status"] != "passed":
            return blocked(package, public, "manual_merge_review_blocked", review["ai_review_gate"]["summary"])
        fact = {"result_id": "delivery:" + facts["merge_sha"], "owner_id": projection.declaration()["owners"]["delivery"],
                "evidence": [{"locator": f"https://github.com/{public['repo_ref']}/pull/{public['pr_number']}", "revision": facts["merge_sha"]}],
                "profile": "pull_request", "candidate": actual, "repo_ref": public["repo_ref"], "pr_number": public["pr_number"],
                "reviewed_head": facts["head_sha"], "merge_commit": facts["merge_sha"], "target_ref": facts["target_ref"]}
        if delivery["delivery_result"] is not None and delivery["delivery_result"] != fact:
            return blocked(package, public, "manual_merge_existing_result_mismatch", "Recover this Delivery's original immutable result; never replace an already recorded success.")
        if delivery["delivery_result"] is None:
            if projection.task_dir.resolve().is_relative_to((root / ".trellis/tasks/archive").resolve()):
                raise archived_fact_gap()
            projection.apply({"api_version": "1.0", "operation": "record_delivery", "key": public["delivery_key"],
                              "owner_role": "delivery", "owner_id": fact["owner_id"], "expected_phase": delivery["phase"],
                              "historical_success": True, "result": fact})
        output = {"exit_id": "delivered", "task_ref": public["task_ref"],
                  "task_key": {key: public["delivery_key"][key] for key in ("task_id", "lifecycle_generation")}}
        validate_json(output, package / "schemas/public-output-delivery-delivered-1.0.schema.json", "stdout")
        return output
    except LifecycleContractError as exc:
        raise CommandError("stale_identity", exc.field_path, exc.remediation, 3) from exc
