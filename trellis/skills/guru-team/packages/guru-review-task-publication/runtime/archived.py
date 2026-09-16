"""Read-only completed-archive Publication review, loaded in the owner namespace."""

ARCHIVED_PUBLICATION_FIELDS = {
    "profile", "mode", "task_ref", "branch_review_commit",
    "reviewed_base_head", "pr_payload_snapshot_sha256",
}
ARCHIVED_SEMANTIC_FIELDS = {
    "pr_payload", "candidate_classifications", "dimensions", "findings",
    "conclusions", "route",
}


def archived_publication_error(field: str, *, stale: bool = True) -> None:
    raise WorkflowError(
        "Archived Publication evidence is missing, mismatched, or stale.",
        exit_code=2,
        payload={
            "error_code": "publication_stale" if stale else "publication_input_invalid",
            "field_path": field,
            "remediation": "Stop this read-only round and obtain current owner evidence.",
        },
    )


def archived_publication_preflight(root: Path, task_dir: Path, invocation: dict[str, Any]) -> dict[str, Any]:
    """Validate archive identity and live payload without active preparation or repair."""
    from urllib.parse import quote

    config = load_config(root)
    task_ref = repo_relative(root, task_dir)
    task = task_json(task_dir)
    if (not task_dir_is_archived(root, task_dir)
            or task.get("status") != "completed"
            or invocation.get("task_ref") != task_ref):
        archived_publication_error("input.task_ref")
    context = load_task_runtime_identity(task_dir, config, allow_rebuild=False)
    assert_workspace_boundary(root, config, context, task_dir)
    head = invocation.get("branch_review_commit")
    base_head = invocation.get("reviewed_base_head")
    if current_head(root) != head or git_status_paths(root, fail_closed=True):
        archived_publication_error("input.branch_review_commit")
    if current_branch(root) != task.get("branch"):
        archived_publication_error("input.task_ref")
    # Require every retained archive file to be exactly committed, including ignored files.
    tracked = run_stdout(["git", "ls-tree", "-r", "--name-only", head, "--", task_ref], cwd=root).splitlines()
    actual = sorted(repo_relative(root, path) for path in task_dir.rglob("*") if path.is_file())
    if sorted(tracked) != actual or not actual:
        archived_publication_error("input.task_ref")
    for name in actual:
        if (root / name).is_symlink() or (root / name).read_bytes() != closeout_commit_blob_bytes(root, head, name):
            archived_publication_error("input.task_ref")
    summary_path = task_dir / FINISH_SUMMARY_ARTIFACT
    if not summary_path.is_file():
        archived_publication_error("input.task_ref")
    summary = read_json(summary_path)
    if (summary.get("task", {}).get("archive_dir") != task_ref
            or summary.get("task", {}).get("status") != "completed"
            or summary.get("git", {}).get("branch") != task.get("branch")
            or summary.get("git", {}).get("base_branch") != task.get("base_branch")):
        archived_publication_error("input.task_ref")
    base_branch = normalize_ref(task["base_branch"]).removeprefix("origin/")
    base_ref = diff_base_ref(root, task["base_branch"])
    local_base = run_stdout(["git", "rev-parse", "--verify", f"{base_ref}^{{commit}}"], cwd=root)
    if local_base != base_head or not is_ancestor(root, base_head, head):
        archived_publication_error("input.reviewed_base_head")
    repo = normalize_github_repository(str(config.get("github_repo") or "") or infer_github_repo(root))
    remote = str(publish_config(config).get("remote") or "origin")
    validate_github_remote_repository(root, remote, repo)
    live_base = gh_json(
        ["api", f"repos/{repo}/git/ref/heads/{quote(base_branch, safe='')}"],
        cwd=root, required_fields=("ref", "object"), operation="base_ref_read",
    )
    if (not isinstance(live_base, dict)
            or live_base.get("ref") != f"refs/heads/{base_branch}"
            or live_base.get("object", {}).get("sha") != base_head):
        archived_publication_error("input.reviewed_base_head")
    plan = {"git": {"remote": remote, "head_branch": task["branch"]}}
    if closeout_remote_branch_head(root, plan) != head:
        archived_publication_error("input.branch_review_commit")
    pr = resolve_closeout_pull_request(root, repo, task["branch"], base_branch, remote)
    if (pr is None or pr["isDraft"] or pr["headRefOid"] != head
            or summary.get("github", {}).get("pr_url") != pr["url"]):
        archived_publication_error("input.branch_review_commit")
    payload = {"title": pr["title"], "body": pr["body"]}
    snapshot = canonical_json_sha256(payload)
    if snapshot != invocation.get("pr_payload_snapshot_sha256"):
        archived_publication_error("input.pr_payload_snapshot_sha256")
    if invocation.get("pr_payload") != payload:
        archived_publication_error("publication.pr_payload")
    return payload


def archived_publication_check_errors(root: Path, task_dir: Path, payload: dict[str, Any]) -> list[str]:
    schema = read_json(Path(__file__).resolve().parents[1] / "schemas/archived-pr-readiness.schema.json")
    errors = skill_json_schema_validation_errors(payload, schema, "archived publication readiness")
    if errors:
        return errors
    errors.extend(task_publication_semantic_errors(payload, branch_review_commit=payload["branch_review_commit"], archived=True))
    classifications = payload["candidate_classifications"]
    refs = [item["candidate_ref"] for item in classifications]
    if len(refs) != len(set(refs)) or any(item["candidate_ref"] not in refs for item in payload["findings"]):
        errors.append("publication findings must bind unique current classified candidates")
    if not errors:
        archived_publication_preflight(root, task_dir, payload)
    return sorted(set(errors))


def record_archived_publication(root: Path, task_dir: Path, args: argparse.Namespace, authored: dict[str, Any], context: Any = None) -> dict[str, Any]:
    if (set(authored) != ARCHIVED_PUBLICATION_FIELDS | ARCHIVED_SEMANTIC_FIELDS
            or authored.get("branch_review_commit") != args.branch_review_commit):
        archived_publication_error("input", stale=False)
    payload = {"schema_version": "1.0", "skill_id": TASK_PUBLICATION_SKILL_ID, **copy.deepcopy(authored)}
    errors = archived_publication_check_errors(root, task_dir, payload)
    if errors:
        archived_publication_error("publication.owner_result", stale=False)
    path = task_publication_path(root, task_dir)
    if not args.dry_run:
        write_json(path, payload)
    if context is not None:
        context.checked_owner_result = copy.deepcopy(payload)
    return {**payload, "artifact_path": str(path), "dry_run": bool(args.dry_run)}


def check_archived_publication(root: Path, task_dir: Path, args: argparse.Namespace, payload: dict[str, Any], context: Any = None) -> dict[str, Any]:
    errors = archived_publication_check_errors(root, task_dir, payload)
    typed_exit = payload.get("route", {}).get("typed_exit")
    if getattr(args, "expected_exit", None) and args.expected_exit != typed_exit:
        errors.append("archived publication expected exit mismatch")
    if errors:
        archived_publication_error("publication.owner_result", stale=False)
    if context is not None:
        context.checked_owner_result = copy.deepcopy(payload)
    return {"status": "ok", "artifact_path": str(task_publication_path(root, task_dir)),
            "task_dir": str(task_dir), "task_ref": payload["task_ref"],
            "branch_review_commit": payload["branch_review_commit"],
            "typed_exit": typed_exit, "owner_result": payload}
