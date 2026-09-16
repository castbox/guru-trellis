ARCHIVED_REVIEW_REFRESH_PROFILE = "archived_review_refresh"


def archived_review_original_tip(root: Path, commits: Any) -> str:
    """The summary producer uses rev-list; ancestry, not list position, owns H."""
    if not isinstance(commits, list) or not commits:
        raise WorkflowError("Archived review requires the original nonempty commit set.", exit_code=2)
    for commit in commits:
        if (
            not isinstance(commit, str)
            or re.fullmatch(r"[0-9a-f]{40}", commit) is None
            or run(["git", "cat-file", "-e", f"{commit}^{{commit}}"], cwd=root, check=False).returncode
        ):
            raise WorkflowError("Archived review original commit object is unavailable.", exit_code=2)
    tips = [tip for tip in set(commits) if all(is_ancestor(root, other, tip) for other in commits)]
    if len(tips) != 1:
        raise WorkflowError("Archived review has no unique original review tip H.", exit_code=2)
    return tips[0]


def archived_review_refresh_context(
    root: Path, public_input: dict[str, Any]
) -> dict[str, Any]:
    task_ref = public_input["task_ref"]
    task_dir = finalization_task_dir(root, public_input)
    if repo_relative(root, task_dir) != task_ref or not task_dir_is_archived(root, task_dir):
        raise WorkflowError("Archived review requires the exact archived task locator.", exit_code=2)
    if git_status_paths(root):
        raise WorkflowError("Archived review requires a clean committed checkout.", exit_code=2)
    archive_head = current_head(root)
    if archive_head != public_input["branch_review_commit"]:
        raise WorkflowError("Archived review A no longer matches current HEAD.", exit_code=2)
    task = task_json(task_dir)
    if task.get("status") != "completed":
        raise WorkflowError("Archived review requires a completed task.", exit_code=2)
    try:
        summary = json.loads(closeout_commit_blob_bytes(root, archive_head, f"{task_ref}/{FINISH_SUMMARY_ARTIFACT}"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise WorkflowError("Archived review committed summary is invalid JSON.", exit_code=2) from exc
    validate_finish_summary(summary)
    active = summary["task"]["artifact_dir"]
    if (
        re.fullmatch(r"\.trellis/tasks/[^/]+", active) is None
        or summary["task"]["archive_dir"] != task_ref
        or Path(active).name != task_dir.name
        or (root / active).exists()
        or summary["git"]["branch"] != task.get("branch")
        or summary["git"]["base_branch"] != task.get("base_branch")
    ):
        raise WorkflowError("Archived review task and committed summary identity differ.", exit_code=2)
    if (
        finalization_transaction_path(root, task_dir).exists()
        or finalization_find_transaction_by_task_ref(root, active) is not None
        or task_finalization_transition_path(root, task_dir).exists()
    ):
        raise WorkflowError("Archived review requires completed closeout; resume the existing Finalizer transaction first.", exit_code=2)
    original_tip = archived_review_original_tip(root, summary["git"]["commits"])
    finalization_terminal_archive_commit(root, active, task_ref, original_tip)
    parent = closeout_commit_parent(root, archive_head)
    for name in CLOSEOUT_ARCHIVE_DURABLE_ARTIFACTS:
        after_path = f"{task_ref}/{name}"
        after = closeout_commit_blob_bytes(root, archive_head, after_path)
        mode, kind, _ = closeout_commit_tree_entry(root, archive_head, after_path)
        file = task_dir / name
        if kind != "blob" or mode not in {"100644", "100755"} or not file.is_file() or file.is_symlink() or file.read_bytes() != after:
            raise WorkflowError("Archived review requires complete current archive blobs.", exit_code=2)
        if name == FINISH_SUMMARY_ARTIFACT:
            continue
        before_path = f"{active}/{name}"
        before = closeout_commit_blob_bytes(root, parent, before_path)
        before_mode, before_kind, _ = closeout_commit_tree_entry(root, parent, before_path)
        if before_kind != "blob" or before_mode != mode:
            raise WorkflowError("Archived review archive mode continuity failed.", exit_code=2)
        if name == "task.json":
            validate_closeout_task_json_archive_change(before, after)
        elif before != after:
            raise WorkflowError("Archived review archive blob continuity failed.", exit_code=2)
    config = load_config(root)
    task_context = load_task_runtime_identity(task_dir, config, allow_rebuild=False)
    assert_workspace_boundary(root, config, task_context, task_dir)
    plan = {
        "task": {"active_locator": active, "archive_locator": task_ref},
        "git": {
            "repo": task_context["source_repo"]["repo"],
            "remote": str(publish_config(config).get("remote") or "origin"),
            "head_branch": task["branch"], "base_branch": task["base_branch"],
            "branch_review_commit": archive_head, "publication_head": archive_head,
        },
        "publish": {"title": public_input["pr_title"], "body": public_input["pr_body"]},
    }
    if closeout_task_mapping_updates(root, task_dir, plan):
        raise WorkflowError("Archived review requires converged mappings; use existing Finalizer recovery first.", exit_code=2)
    git = plan["git"]
    repo = validate_github_remote_repository(root, git["remote"], git["repo"])
    base_ref = diff_base_ref(root, task["base_branch"])
    base = public_input["reviewed_base_head"]
    local_base = run_stdout(["git", "rev-parse", "--verify", f"{base_ref}^{{commit}}"], cwd=root)
    live_base = gh_json(
        ["api", f"repos/{repo}/git/ref/heads/{task['base_branch']}"], cwd=root,
        required_fields=("object",), operation="base_ref_read",
    )
    if (
        not isinstance(live_base, dict)
        or not isinstance(live_base.get("object"), dict)
        or live_base["object"].get("sha") != base
        or local_base != base
        or not is_ancestor(root, base, archive_head)
    ):
        raise WorkflowError("Archived review B is stale or unavailable; repeat Branch Review against the current base.", exit_code=2)
    pr = resolve_closeout_pull_request(root, repo, task["branch"], task["base_branch"], git["remote"])
    url, number = parse_canonical_pull_request_url(repo, summary["github"]["pr_url"])
    if (
        pr is None or pr.get("number") != number or pr.get("url") != url
        or pr.get("isDraft") is not False or pr.get("headRefOid") != archive_head
        or pr.get("title") != public_input["pr_title"] or pr.get("body") != public_input["pr_body"]
        or closeout_remote_branch_head(root, plan) != archive_head
        or summary["index"]["search_terms"]["pr_refs"] != [f"PR #{number}"]
    ):
        raise WorkflowError("Archived review requires the exact Open Ready PR, A and Publication payload bytes.", exit_code=2)
    # This local gate identity is not a new archive transaction or public handoff.
    plan["plan_digest"] = canonical_json_sha256({"input": public_input, "original_tip": original_tip, "repo": repo, "pr_number": number})
    return {
        "task_dir": task_dir, "task_context": task_context, "plan": plan,
        "plan_ref": f"finalization:{plan['plan_digest']}",
        "transaction_state": ARCHIVED_REVIEW_REFRESH_PROFILE,
        "publication_status": "current", "publication_stale_reason": None,
        "publication_branch_review_commit": archive_head, "published_pr": pr,
        "original_review_commit": original_tip, "reviewed_base_head": base,
    }


def archived_review_refresh_preview(root: Path, public_input: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    result = {
        "schema_version": "1.0", "status": "ok", "side_effects": False,
        "profile": ARCHIVED_REVIEW_REFRESH_PROFILE, "task_ref": public_input["task_ref"],
        "branch_review_commit": public_input["branch_review_commit"],
        "reviewed_base_head": public_input["reviewed_base_head"],
        "original_review_commit": context["original_review_commit"],
    }
    schema = read_json(finalization_package_root(root) / "schemas/archived-review-refresh-preview-1.0.schema.json")
    if skill_json_schema_validation_errors(result, schema, "archived review preview"):
        raise WorkflowError("Archived review preview is invalid.", exit_code=2)
    return result


def invoke_archived_review_refresh(root: Path, args: argparse.Namespace, public_input: dict[str, Any]) -> dict[str, Any]:
    if getattr(args, "confirmed_preview_sha256", None):
        raise WorkflowError("Archived review is read-only and accepts no mutation confirmation.", exit_code=2)
    reviewed = finalization_semantic_review_input(root, args.review_input)
    context = archived_review_refresh_context(root, public_input)
    recorded = finalization_record_gate_result(root, public_input, reviewed, context, dry_run=False, include_private=True)
    gate, path = recorded["gate"], recorded["gate_path"]
    gate, current = check_finalization_gate_result(root, args, public_input, gate, path, allow_pending_transition=True)
    output = (
        finalization_gate_with_ready_for_merge_output(root, current["task_dir"], gate, current["plan"], current["published_pr"])["route"]["output"]
        if gate["route"]["typed_exit"] == "ready_for_merge"
        else copy.deepcopy(gate["route"]["output"])
    )
    path.unlink(missing_ok=True)
    return output
