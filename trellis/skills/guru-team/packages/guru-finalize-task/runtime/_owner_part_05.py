def cmd_finish_work(args: argparse.Namespace) -> dict[str, Any]:
    return _cmd_finish_work_impl(args)

FINALIZATION_CONSUMERS = {
    "base_reconciliation_required": {
        "kind": "skill",
        "id": "guru-reconcile-task-base",
    },
    "publication_review_stale": {
        "kind": "skill",
        "id": TASK_PUBLICATION_SKILL_ID,
    },
    "resume_finalization": {
        "kind": "skill",
        "id": FINALIZE_TASK_SKILL_ID,
    },
    "reprepare_required": {
        "kind": "skill",
        "id": FINALIZE_TASK_SKILL_ID,
    },
    "ready_for_merge": {
        "kind": "skill",
        "id": "guru-merge-task-pr",
    },
    "blocked": {
        "kind": "stop",
        "id": "task-finalization-blocked",
    },
}

FINALIZATION_EXECUTOR_OUTPUT_MARKER = {"materialization": "executor"}

FINALIZATION_GATE_SCHEMA_VERSION = "5.0"

FINALIZATION_REPREPARE_ARCHIVE_MONTH = "archive_month_changed"

FINALIZATION_REPREPARE_PROVENANCE_TAIL = "provenance_tail_required"

FINALIZATION_COMMITTED_RECOVERY_STATES = {"archived", "ready"}

FINALIZATION_RESUME_RECOVERY_STATES = {
    "content_pushed",
    "draft_bound",
    "projection_validated",
    "archive_moved",
    "archive_pushed",
    "archived",
}

def finalization_package_root(root: Path) -> Path:
    invoked = os.environ.get("GURU_TEAM_INVOKED_PACKAGE_ROOT", "")
    candidates = [
        Path(invoked) if invoked else None,
        root / "trellis/skills/guru-team/packages/guru-finalize-task",
        root / ".trellis/guru-team/skills/packages/guru-finalize-task",
    ]
    for candidate in candidates:
        if (
            isinstance(candidate, Path)
            and candidate.is_dir()
            and not candidate.is_symlink()
            and candidate.name == FINALIZE_TASK_SKILL_ID
        ):
            return candidate
    raise WorkflowError("The active task finalization package is unavailable.", exit_code=2)

def finalization_json_input(
    root: Path,
    value: str | None,
    label: str,
    *,
    allow_stdin: bool = False,
) -> tuple[dict[str, Any], str]:
    raw = str(value or "").strip()
    if allow_stdin and raw == "-":
        try:
            payload = json.load(sys.stdin)
        except (OSError, json.JSONDecodeError) as exc:
            raise WorkflowError(f"{label} stdin JSON is invalid.", exit_code=2) from exc
        if not isinstance(payload, dict):
            raise WorkflowError(f"{label} stdin must be an object.", exit_code=2)
        return payload, "<stdin>"
    relative = skill_safe_relative(raw)
    if relative is None:
        raise WorkflowError(
            f"{label} must be a safe repo- or package-relative JSON path.",
            exit_code=2,
        )
    package = finalization_package_root(root)
    package_candidate = package / relative
    path = package_candidate if package_candidate.is_file() else root / relative
    boundary = package if path == package_candidate else root
    errors: list[str] = []
    if skill_lstat_path(
        boundary,
        path,
        label,
        errors,
        kind="file",
    ) is None:
        raise WorkflowError(f"{label} is missing or unsafe.", exit_code=2)
    payload = skill_read_json(path, label, errors)
    if errors or not isinstance(payload, dict):
        raise WorkflowError(
            f"{label} is invalid.",
            exit_code=2,
            payload={"errors": errors},
        )
    locator = repo_relative(root, path) if path.is_relative_to(root) else relative.as_posix()
    return payload, locator

def finalization_interface(root: Path) -> dict[str, Any]:
    package = finalization_package_root(root)
    errors: list[str] = []
    interface = skill_read_json(package / "interface.json", "task finalization interface", errors)
    if errors or not isinstance(interface, dict) or interface.get("id") != FINALIZE_TASK_SKILL_ID:
        raise WorkflowError("Task finalization interface is unavailable.", exit_code=2)
    return interface

def finalization_public_input(
    root: Path,
    value: str | None,
) -> tuple[dict[str, Any], str]:
    payload, locator = finalization_json_input(root, value, "task finalization public input")
    package = finalization_package_root(root)
    interface = finalization_interface(root)
    profiles = interface["public_contracts"]["input"]["profiles"]
    profile = next(
        (
            item
            for item in profiles
            if isinstance(item, dict) and item.get("id") == payload.get("profile")
        ),
        None,
    )
    errors: list[str] = []
    schema = skill_read_schema(
        package / str((profile.get("schema") or {}).get("path") if isinstance(profile, dict) else ""),
        "task finalization public input schema",
        errors,
    )
    if isinstance(schema, dict):
        errors.extend(
            skill_json_schema_validation_errors(
                payload,
                schema,
                "task finalization public input",
            )
        )
    if errors or not isinstance(profile, dict) or not isinstance(schema, dict):
        raise WorkflowError(
            "Task finalization public input failed its declared profile.",
            exit_code=2,
            payload={"errors": errors},
        )
    return payload, locator

def finalization_semantic_review_input(
    root: Path,
    value: str | None,
) -> dict[str, Any]:
    payload, _ = finalization_json_input(
        root,
        value,
        "task finalization semantic review input",
        allow_stdin=True,
    )
    package = finalization_package_root(root)
    errors: list[str] = []
    schema = skill_read_schema(
        package / "schemas/semantic-review-input-3.0.schema.json",
        "task finalization semantic review input schema",
        errors,
    )
    if isinstance(schema, dict):
        errors.extend(
            skill_json_schema_validation_errors(
                payload,
                schema,
                "task finalization semantic review input",
            )
        )
    if errors or not isinstance(schema, dict):
        raise WorkflowError(
            "Task finalization semantic review input is invalid.",
            exit_code=2,
            payload={"errors": errors},
        )
    return payload

def finalization_task_dir(root: Path, public_input: dict[str, Any]) -> Path:
    task_ref = str(public_input.get("task_ref") or "")
    task_dir = resolve_finish_work_task_dir(root, task_ref)
    resolved_ref = repo_relative(root, task_dir)
    if resolved_ref == task_ref:
        return task_dir
    if task_dir_is_archived(root, task_dir):
        transaction_match = finalization_find_transaction_by_task_ref(
            root,
            task_ref,
        )
        if transaction_match is not None:
            transaction, _transaction_path = transaction_match
            if transaction.get("task_ref") == task_ref:
                return task_dir
        if finalization_current_terminal_gate(root, task_dir, task_ref) is not None:
            return task_dir
        if finalization_terminal_projection_gate(root, task_dir, public_input) is not None:
            return task_dir
    if resolved_ref != task_ref:
        raise WorkflowError(
            "Task finalization task_ref does not resolve to the exact task locator.",
            exit_code=2,
        )
    return task_dir

def finalization_transaction_path(root: Path, task_dir: Path) -> Path:
    return (
        runtime_root(root, load_config(root))
        / "finalization-transaction"
        / ai_first_task_checkpoint_key(task_dir)
        / FINALIZATION_TRANSACTION_ARTIFACT
    )

def finalization_transaction_schema(root: Path) -> dict[str, Any]:
    errors: list[str] = []
    schema = skill_read_schema(
        finalization_package_root(root)
        / "schemas/finalization-transaction.schema.json",
        "task finalization transaction",
        errors,
    )
    if errors or not isinstance(schema, dict):
        raise WorkflowError(
            "Task finalization transaction schema is unavailable.",
            exit_code=2,
            payload={"errors": errors},
        )
    return schema

def finalization_transaction_from_plan(
    plan: dict[str, Any],
    *,
    next_transition: str,
    pr: dict[str, Any] | None = None,
    pre_push_remote_head: str | None = None,
    mode: str = "ordinary_publication",
    adopted_pr: dict[str, Any] | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "schema_version": "3.0",
        "skill_id": FINALIZE_TASK_SKILL_ID,
        "mode": mode,
        "task_ref": plan["task"]["active_locator"],
        "repo_ref": plan["git"]["repo"],
        "base_branch": plan["git"]["base_branch"],
        "branch": plan["git"]["head_branch"],
        "branch_review_commit": plan["git"]["branch_review_commit"],
        "publication_head": (
            plan["git"].get("publication_head")
            or plan["git"]["branch_review_commit"]
        ),
        "plan_digest": plan["plan_digest"],
        "publication": {
            "title": plan["publish"]["title"],
            "body": plan["publish"]["body"],
        },
        "next_transition": next_transition,
    }
    if pr is not None:
        payload["pr"] = {
            "number": pr["number"],
            "url": pr["url"],
        }
    if pre_push_remote_head is not None:
        payload["pre_push_remote_head"] = pre_push_remote_head
    if adopted_pr is not None:
        payload["adopted_pr"] = copy.deepcopy(adopted_pr)
    return payload

def finalization_advance_transaction(
    plan: dict[str, Any],
    transaction: dict[str, Any],
    *,
    next_transition: str,
    pr: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return finalization_transaction_from_plan(
        plan,
        next_transition=next_transition,
        pr=pr if pr is not None else (
            transaction.get("pr") if isinstance(transaction.get("pr"), dict) else None
        ),
        mode=str(transaction.get("mode") or "ordinary_publication"),
        adopted_pr=(
            transaction.get("adopted_pr")
            if isinstance(transaction.get("adopted_pr"), dict)
            else None
        ),
    )


def finalization_reprepared_transaction(
    plan: dict[str, Any],
    previous_transaction: dict[str, Any] | None,
    *,
    pre_push_remote_head: str,
) -> dict[str, Any]:
    if (
        isinstance(previous_transaction, dict)
        and previous_transaction.get("mode") == "existing_pr_recovery"
    ):
        adopted_pr = previous_transaction.get("adopted_pr")
        pr = previous_transaction.get("pr")
        if not isinstance(adopted_pr, dict) or not isinstance(pr, dict):
            raise WorkflowError(
                "Existing PR recovery transaction is incomplete during reprepare.",
                exit_code=2,
            )
        return finalization_transaction_from_plan(
            plan,
            next_transition="push_content",
            pr=pr,
            pre_push_remote_head=pre_push_remote_head,
            mode="existing_pr_recovery",
            adopted_pr=adopted_pr,
        )
    return finalization_transaction_from_plan(
        plan,
        next_transition="push_content",
        pre_push_remote_head=pre_push_remote_head,
    )

def finalization_validate_transaction_plan(
    transaction: dict[str, Any],
    plan: dict[str, Any],
) -> None:
    expected = finalization_transaction_from_plan(
        plan,
        next_transition=str(transaction.get("next_transition") or "push_content"),
        pr=(transaction.get("pr") if isinstance(transaction.get("pr"), dict) else None),
        pre_push_remote_head=(
            str(transaction["pre_push_remote_head"])
            if transaction.get("next_transition") == "push_content"
            and isinstance(transaction.get("pre_push_remote_head"), str)
            else None
        ),
        mode=str(transaction.get("mode") or "ordinary_publication"),
        adopted_pr=(
            transaction.get("adopted_pr")
            if isinstance(transaction.get("adopted_pr"), dict)
            else None
        ),
    )
    if transaction != expected:
        raise WorkflowError(
            "Task finalization transaction no longer matches the rebuilt plan.",
            exit_code=2,
        )

def finalization_write_transaction(
    root: Path,
    task_dir: Path,
    payload: dict[str, Any],
) -> Path:
    errors = skill_json_schema_validation_errors(
        payload,
        finalization_transaction_schema(root),
        "task finalization transaction",
    )
    if errors:
        raise WorkflowError(
            "Task finalization transaction is invalid.",
            exit_code=2,
            payload={"errors": errors},
        )
    path = finalization_transaction_path(root, task_dir)
    write_json(path, payload)
    return path

def finalization_read_transaction(
    root: Path,
    task_dir: Path,
) -> dict[str, Any] | None:
    path = finalization_transaction_path(root, task_dir)
    if not path.exists():
        return None
    if not path.is_file() or path.is_symlink():
        raise WorkflowError(
            "Task finalization transaction is unsafe.", exit_code=2
        )
    payload = read_json(path)
    errors = skill_json_schema_validation_errors(
        payload,
        finalization_transaction_schema(root),
        "task finalization transaction",
    )
    if errors:
        raise WorkflowError(
            "Task finalization transaction is invalid.",
            exit_code=2,
            payload={"errors": errors},
        )
    return payload

def finalization_current_terminal_gate(
    root: Path,
    task_dir: Path,
    task_ref: str,
) -> dict[str, Any] | None:
    """Resolve the adjacent terminal gate without reviving transaction state."""
    if not task_dir_is_archived(root, task_dir):
        return None
    path = task_finalization_path(root, task_dir)
    if not path.exists():
        return None
    if not path.is_file() or path.is_symlink():
        raise WorkflowError(
            "Archived current Finalizer gate is missing or unsafe.", exit_code=2
        )
    gate = finalization_normalize_gate(root, read_json(path))
    identity = gate.get("identity") if isinstance(gate.get("identity"), dict) else {}
    plan_digest = str(identity.get("plan_digest") or "")
    plan_ref = str(identity.get("plan_ref") or "")
    if not plan_ref.startswith("finalization:"):
        return None
    errors = skill_json_schema_validation_errors(
        gate,
        finalization_gate_schema(root),
        "task finalization gate",
    )
    if (
        errors
        or identity.get("task_ref") != task_ref
        or re.fullmatch(r"[0-9a-f]{64}", plan_digest) is None
        or plan_ref != f"finalization:{plan_digest}"
        or re.fullmatch(
            r"[0-9a-f]{40}", str(identity.get("branch_review_commit") or "")
        )
        is None
        or gate.get("route")
        != {
            "typed_exit": "ready_for_merge",
            "consumer": FINALIZATION_CONSUMERS["ready_for_merge"],
            "output": FINALIZATION_EXECUTOR_OUTPUT_MARKER,
        }
    ):
        raise WorkflowError(
            "Archived current Finalizer gate does not bind the terminal transaction.",
            exit_code=2,
            payload={"errors": errors},
        )
    return gate


def finalization_terminal_projection_gate(
    root: Path,
    task_dir: Path,
    public_input: dict[str, Any],
) -> dict[str, Any] | None:
    """Project a retired gate from the committed terminal archive authority."""
    task_ref = str(public_input.get("task_ref") or "")
    archive_locator = repo_relative(root, task_dir)
    if (
        not task_dir_is_archived(root, task_dir)
        or task_finalization_path(root, task_dir).exists()
        or finalization_find_transaction_by_task_ref(root, task_ref) is not None
    ):
        return None
    task = task_json(task_dir)
    summary_path = task_dir / FINISH_SUMMARY_ARTIFACT
    if task.get("status") != "completed":
        return None
    if not summary_path.is_file() or summary_path.is_symlink():
        return None
    summary = read_json(summary_path)
    validate_finish_summary(summary)
    summary_task = summary.get("task") if isinstance(summary.get("task"), dict) else {}
    summary_git = summary.get("git") if isinstance(summary.get("git"), dict) else {}
    branch_review_commit = str(public_input.get("branch_review_commit") or "")
    commits = summary_git.get("commits") if isinstance(summary_git.get("commits"), list) else []
    if (
        summary_task.get("artifact_dir") != task_ref
        or summary_task.get("archive_dir") != archive_locator
        or re.fullmatch(r"[0-9a-f]{40}", branch_review_commit) is None
        or branch_review_commit not in commits
    ):
        return None
    archive_commit = finalization_terminal_archive_commit(
        root,
        task_ref,
        archive_locator,
        branch_review_commit,
    )
    terminal_digest = canonical_json_sha256(
        {
            "schema_version": "1.0",
            "task_ref": task_ref,
            "archive_locator": archive_locator,
            "branch_review_commit": branch_review_commit,
            "archive_commit": archive_commit,
            "finish_summary_sha256": canonical_json_sha256(summary),
        }
    )
    return {
        "schema_version": FINALIZATION_GATE_SCHEMA_VERSION,
        "skill_id": FINALIZE_TASK_SKILL_ID,
        "identity": {
            "task_ref": task_ref,
            "plan_ref": f"finalization:{terminal_digest}",
            "plan_digest": terminal_digest,
            "branch_review_commit": branch_review_commit,
        },
        "review": {
            "status": "passed",
            "summary": "The committed terminal archive remains the reviewed Ready authority.",
        },
        "route": {
            "typed_exit": "ready_for_merge",
            "consumer": copy.deepcopy(FINALIZATION_CONSUMERS["ready_for_merge"]),
            "output": copy.deepcopy(FINALIZATION_EXECUTOR_OUTPUT_MARKER),
        },
    }


def finalization_terminal_archive_commit(
    root: Path,
    task_ref: str,
    archive_locator: str,
    branch_review_commit: str,
) -> str:
    """Require current HEAD to be the exact reviewed archive metadata commit."""
    archive_commit = current_head(root)
    transaction_parent = closeout_commit_parent(root, archive_commit)
    parent_active_paths = closeout_commit_tracked_task_paths(
        root,
        transaction_parent,
        task_ref,
    )
    expected_archive_paths = {
        f"{archive_locator}/{relative}"
        for relative in CLOSEOUT_ARCHIVE_DURABLE_ARTIFACTS
    }
    archived_paths = closeout_commit_tracked_task_paths(
        root,
        archive_commit,
        archive_locator,
    )
    remaining_active_paths = closeout_commit_tracked_task_paths(
        root,
        archive_commit,
        task_ref,
    )
    committed_paths = closeout_commit_paths(root, archive_commit)
    expected_paths = parent_active_paths | expected_archive_paths
    reviewed_identity = reviewed_content_identity(
        root,
        branch_review_commit,
        include_worktree=False,
    )["sha256"]
    archive_identity = reviewed_content_identity(
        root,
        archive_commit,
        include_worktree=False,
    )["sha256"]
    if (
        not parent_active_paths
        or not is_ancestor(root, branch_review_commit, transaction_parent)
        or archived_paths != expected_archive_paths
        or remaining_active_paths
        or committed_paths != expected_paths
        or archive_identity != reviewed_identity
    ):
        raise WorkflowError(
            "Archived current Finalizer HEAD is not the exact reviewed archive metadata commit.",
            exit_code=2,
            payload={
                "archive_commit": archive_commit,
                "transaction_parent": transaction_parent,
                "expected_paths": sorted(expected_paths),
                "actual_paths": sorted(committed_paths),
            },
        )
    return archive_commit

def finalization_find_transaction_by_task_ref(
    root: Path,
    task_ref: str,
) -> tuple[dict[str, Any], Path] | None:
    owner_root = runtime_root(root, load_config(root)) / "finalization-transaction"
    if not owner_root.exists():
        return None
    if not owner_root.is_dir() or owner_root.is_symlink():
        raise WorkflowError("Task finalization transaction owner root is unsafe.", exit_code=2)
    matches: list[tuple[dict[str, Any], Path]] = []
    for owner_dir in sorted(owner_root.iterdir()):
        if not owner_dir.is_dir() or owner_dir.is_symlink():
            raise WorkflowError("Task finalization transaction owner entry is unsafe.", exit_code=2)
        path = owner_dir / FINALIZATION_TRANSACTION_ARTIFACT
        if not path.exists():
            continue
        if not path.is_file() or path.is_symlink():
            raise WorkflowError("Task finalization transaction is unsafe.", exit_code=2)
        payload = read_json(path)
        errors = skill_json_schema_validation_errors(
            payload,
            finalization_transaction_schema(root),
            "task finalization transaction",
        )
        if errors:
            raise WorkflowError(
                "Task finalization transaction is invalid.",
                exit_code=2,
                payload={"errors": errors},
            )
        if payload.get("task_ref") == task_ref:
            matches.append((payload, path))
    if len(matches) > 1:
        raise WorkflowError(
            "Task finalization found multiple transactions for one task.",
            exit_code=2,
        )
    return matches[0] if matches else None

def finalization_retire_current_state(root: Path, task_dir: Path) -> list[str]:
    retired: list[str] = []
    task_ref = repo_relative(root, task_dir)
    transaction_match = finalization_find_transaction_by_task_ref(root, task_ref)
    candidates = [
        (
            transaction_match[1]
            if transaction_match is not None
            else finalization_transaction_path(root, task_dir)
        ),
        task_finalization_path(root, task_dir),
        task_finalization_transition_path(root, task_dir),
    ]
    for path in candidates:
        if path.is_symlink():
            raise WorkflowError(
                "Task finalization terminal cleanup found unsafe owner state.",
                exit_code=2,
            )
        if path.is_dir():
            shutil.rmtree(path)
            retired.append(repo_relative(root, path))
        elif path.is_file():
            path.unlink()
            retired.append(repo_relative(root, path))
    return retired

def finalization_publication_owner_result(
    root: Path,
    task_dir: Path,
    public_input: dict[str, Any],
    verification: tuple[dict[str, Any], dict[str, Any]] | None = None,
) -> dict[str, Any]:
    del verification
    task_ref = repo_relative(root, task_dir)
    if public_input.get("task_ref") != task_ref:
        raise WorkflowError(
            "Task finalization publication handoff does not match the resolved task.",
            exit_code=2,
        )

    profile = str(public_input.get("profile") or "")
    branch_review_commit = str(public_input.get("branch_review_commit") or "")
    if profile == "publication_ready":
        task = task_json(task_dir)
        if task.get("status") != "in_progress":
            return {
                "owner_status": "stale",
                "branch_review_commit": branch_review_commit,
                "stale_reason": "publication_review_stale",
            }
        repository = task_publication_repository_binding(root, task_dir)
        unexpected = task_publication_unexpected_status_paths(
            repository["status_paths"],
        )
        if unexpected:
            raise WorkflowError(
                "Task finalization found dirty paths outside the reviewed-content boundary.",
                exit_code=2,
                payload={"unexpected_dirty_paths": unexpected},
            )
        task_context = load_task_runtime_identity(task_dir, load_config(root))
        old_base_head = str(task_context.get("base_head_sha") or "")
        base_branch = str(task_context.get("base_branch") or task.get("base_branch") or "")
        selected_base_ref = diff_base_ref(root, base_branch)
        new_base_head = run(["git", "rev-parse", selected_base_ref], cwd=root).stdout.strip()
        if old_base_head != new_base_head:
            task_head = current_head(root)
            if not is_ancestor(root, old_base_head, new_base_head):
                raise WorkflowError("Finalizer base evolution is not an ancestor delta.", exit_code=2)
            return {
                "owner_status": "base_reconciliation_required",
                "task_ref": task_ref,
                "task_head": task_head,
                "publication_head": task_head,
                "selected_base_ref": selected_base_ref,
                "old_base_head": old_base_head,
                "new_base_head": new_base_head,
                "branch_review_commit": branch_review_commit,
                "resume_target": "finalization_resume",
            }
    elif profile == "reprepare_preview":
        publication_head = str(public_input.get("publication_head") or "")
        reason_code = str(public_input.get("reason_code") or "")
        transaction = finalization_read_transaction(root, task_dir)
        if transaction is not None:
            plan_reviewed = str(transaction["branch_review_commit"])
            plan_publication = str(transaction["publication_head"])
            if (
                plan_reviewed != branch_review_commit
                or plan_publication != publication_head
            ):
                return {
                    "owner_status": "stale",
                    "branch_review_commit": branch_review_commit,
                    "stale_reason": "publication_review_stale",
                }
        try:
            target_repo = (
                transaction.get("repo_ref")
                if isinstance(transaction, dict)
                else infer_github_repo(root)
            )
            publication_identity = finalizer_publication_identity(
                root,
                branch_review_commit,
                target_repo,
            )
        except WorkflowError as exc:
            return {
                "owner_status": "stale",
                "branch_review_commit": branch_review_commit,
                "stale_reason": "publication_review_stale",
                "errors": [str(exc)],
            }
        if (
            publication_head != current_head(root)
            or publication_identity["publication_head"] != publication_head
            or (
                reason_code == FINALIZATION_REPREPARE_PROVENANCE_TAIL
                and publication_identity["metadata_tail"] is None
            )
        ):
            return {
                "owner_status": "stale",
                "branch_review_commit": branch_review_commit,
                "stale_reason": "publication_review_stale",
            }
    else:
        transaction = finalization_read_transaction(root, task_dir)
        if transaction is None:
            return {
                "owner_status": "stale",
                "branch_review_commit": branch_review_commit,
                "stale_reason": "publication_review_missing",
            }
        branch_review_commit = str(transaction["branch_review_commit"])
        supplied_commit = public_input.get("branch_review_commit")
        if (
            isinstance(supplied_commit, str)
            and supplied_commit != branch_review_commit
        ):
            return {
                "owner_status": "stale",
                "branch_review_commit": branch_review_commit,
                "stale_reason": "publication_review_stale",
            }
    try:
        reviewed_content_sha256 = reviewed_content_identity(
            root,
            branch_review_commit,
            include_worktree=False,
        )["sha256"]
        continuity_errors = review_branch_content_continuity_errors(
            root,
            task_dir,
            branch_review_commit,
            reviewed_content_sha256,
            current_head(root),
        )
    except WorkflowError as exc:
        continuity_errors = [str(exc)]
    if continuity_errors:
        return {
            "owner_status": "stale",
            "branch_review_commit": branch_review_commit,
            "stale_reason": "publication_review_stale",
            "errors": continuity_errors,
        }
    return {
        "status": "ok",
        "owner_status": "current",
        "typed_exit": "ready",
        "task_ref": task_ref,
        "branch_review_commit": branch_review_commit,
    }

def finalization_prepare_publication_ready(
    public_input: dict[str, Any],
    *,
    transaction: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    """Select exact Publication authority without inflating reprepare identity."""
    if public_input.get("profile") == "publication_ready":
        return public_input
    if transaction is not None:
        profile = public_input.get("profile")
        if (
            public_input.get("task_ref") != transaction.get("task_ref")
            or (
                profile == "reprepare_preview"
                and (
                    public_input.get("branch_review_commit")
                    != transaction.get("branch_review_commit")
                    or public_input.get("publication_head")
                    != transaction.get("publication_head")
                )
            )
        ):
            raise WorkflowError(
                "Task finalization reprepare input differs from its owner publication authority.",
                exit_code=2,
            )
        publication = transaction["publication"]
        return {
            "profile": "publication_ready",
            "mode": public_input["mode"],
            "task_ref": transaction["task_ref"],
            "branch_review_commit": transaction["branch_review_commit"],
            "pr_title": publication["title"],
            "pr_body": publication["body"],
        }
    if public_input.get("profile") != "reprepare_preview":
        return None
    raise WorkflowError(
        "Task finalization reprepare is missing its owner publication authority.",
        exit_code=2,
    )

def finalization_eval_preview_context(
    root: Path,
    public_input: dict[str, Any],
) -> dict[str, Any] | None:
    if os.environ.get("GURU_TEAM_EVAL_STAGING") != "1":
        return None
    path = root / ".trellis/.runtime/guru-team/evals/finalization-context.json"
    if not path.is_file() or path.is_symlink():
        return None
    payload = read_json(path)
    expected_keys = {
        "schema_version",
        "task_ref",
        "plan_ref",
        "plan_digest",
        "branch_review_commit",
        "publication_head",
        "archive_locator",
        "repo_ref",
        "remote",
        "head_branch",
        "pr_title",
        "pr_body",
        "publication_status",
        "publication_stale_reason",
        "transaction_state",
    }
    states = {
        "prepared",
        "content_pushed",
        "draft_bound",
        "projection_validated",
        "archive_moved",
        "archive_pushed",
        "archived",
        "ready",
        "publication_review_stale",
        "reprepare_required",
    }
    if (
        set(payload) != expected_keys
        or payload.get("schema_version") != "2.0"
        or payload.get("task_ref") != public_input.get("task_ref")
        or not re.fullmatch(r"finalization:[0-9a-f]{64}", str(payload.get("plan_ref") or ""))
        or payload.get("plan_ref") != f"finalization:{payload.get('plan_digest')}"
        or not re.fullmatch(r"[0-9a-f]{64}", str(payload.get("plan_digest") or ""))
        or not re.fullmatch(
            r"[0-9a-f]{40}", str(payload.get("branch_review_commit") or "")
        )
        or not re.fullmatch(
            r"[0-9a-f]{40}", str(payload.get("publication_head") or "")
        )
        or normalize_github_repository(payload.get("repo_ref")) != payload.get("repo_ref")
        or not isinstance(payload.get("pr_title"), str)
        or not payload.get("pr_title")
        or not isinstance(payload.get("pr_body"), str)
        or not payload.get("pr_body")
        or payload.get("publication_status") not in {"current", "stale"}
        or (
            payload.get("publication_status") == "current"
            and payload.get("publication_stale_reason") is not None
        )
        or (
            payload.get("publication_status") == "stale"
            and payload.get("publication_stale_reason")
            not in {
                "publication_review_missing",
                "publication_review_stale",
            }
        )
        or payload.get("transaction_state") not in states
        or (
            payload.get("transaction_state") == "reprepare_required"
            and (
                public_input.get("profile") != "reprepare_preview"
                or public_input.get("reason_code") not in {
                    FINALIZATION_REPREPARE_ARCHIVE_MONTH,
                    FINALIZATION_REPREPARE_PROVENANCE_TAIL,
                }
            )
        )
    ):
        raise WorkflowError(
            "Task finalization eval objective facts are invalid.",
            exit_code=2,
        )
    task_dir = finalization_task_dir(root, public_input)
    if payload["transaction_state"] == "ready":
        archive_relative = skill_safe_relative(str(payload["archive_locator"]))
        archive_dir = root / archive_relative if archive_relative is not None else None
        if (
            archive_relative is None
            or archive_relative.as_posix() != payload["archive_locator"]
            or archive_dir is None
            or not archive_dir.is_dir()
            or archive_dir.is_symlink()
        ):
            raise WorkflowError(
                "Task finalization eval terminal archive locator is unavailable.",
                exit_code=2,
            )
        task_dir = archive_dir
    plan = {
        "plan_digest": payload["plan_digest"],
        "git": {
            "repo": payload["repo_ref"],
            "remote": payload["remote"],
            "base_branch": "main",
            "head_branch": payload["head_branch"],
            "branch_review_commit": payload["branch_review_commit"],
            "reviewed_content_head": payload["branch_review_commit"],
            "publication_head": payload["publication_head"],
        },
        "publish": {
            "title": payload["pr_title"],
            "body": payload["pr_body"],
        },
        "review": {"changed_paths": []},
        "task": {
            "active_locator": payload["task_ref"],
            "archive_locator": payload["archive_locator"],
        },
    }
    return {
        "task_dir": task_dir,
        "task_context": None,
        "prepared": None,
        "plan": plan,
        "plan_ref": payload["plan_ref"],
        "transaction_state": payload["transaction_state"],
        "published_transition_complete": payload["transaction_state"] == "ready",
        "published_pr": (
            {
                "number": 118,
                "url": f"https://github.com/{payload['repo_ref']}/pull/118",
                "headRefOid": payload["publication_head"],
            }
            if payload["transaction_state"] == "ready"
            else None
        ),
        "publication": {"owner_status": "current"},
        "publication_status": payload["publication_status"],
        "publication_stale_reason": payload["publication_stale_reason"],
        "publication_branch_review_commit": payload["branch_review_commit"],
        "reprepare_reason_code": (
            public_input.get("reason_code")
            if payload["transaction_state"] == "reprepare_required"
            else None
        ),
        "verification": None,
    }

def finalization_archived_published_facts(
    root: Path,
    plan: dict[str, Any],
    transaction: dict[str, Any] | None = None,
) -> tuple[bool, dict[str, Any] | None]:
    transaction = transaction or resolve_committed_closeout_archive_transaction(
        root,
        plan,
    )
    if transaction is None:
        raise WorkflowError(
            "Archived task finalization is not the exact plan transaction.",
            exit_code=2,
        )
    summary_pr = transaction.get("summary_pr")
    if not isinstance(summary_pr, dict):
        raise WorkflowError(
            "Archived task finalization is missing its committed PR identity.",
            exit_code=2,
        )
    git = plan["git"]
    pr = resolve_closeout_pull_request(
        root,
        git["repo"],
        git["head_branch"],
        git["base_branch"],
        git["remote"],
    )
    if pr is None:
        raise WorkflowError(
            "Archived task finalization requires the bound pull request.",
            exit_code=2,
        )
    local_head = current_head(root)
    validate_closeout_remote_pull_request_identity(
        plan,
        pr,
        expected_draft=bool(pr["isDraft"]),
        bound_pr=summary_pr,
    )
    complete = (
        pr.get("isDraft") is False
        and closeout_remote_branch_head(root, plan) == local_head
        and pr.get("headRefOid") == local_head
    )
    return complete, pr if complete else None

def finalization_archived_owner_results(
    root: Path,
    plan: dict[str, Any],
    transaction: dict[str, Any],
    public_input: dict[str, Any],
) -> tuple[dict[str, Any], tuple[dict[str, Any], dict[str, Any]] | None]:
    del root, plan, transaction, public_input
    return {"owner_status": "current"}, None

def finalization_current_archived_context(
    root: Path,
    task_dir: Path,
    public_input: dict[str, Any],
    transaction: dict[str, Any],
) -> dict[str, Any]:
    task_ref = str(public_input.get("task_ref") or "")
    archive_locator = repo_relative(root, task_dir)
    next_transition = transaction.get("next_transition")
    if (
        transaction.get("task_ref") != task_ref
        or next_transition not in {"archive", "push_archive", "mark_ready"}
        or not isinstance(transaction.get("pr"), dict)
    ):
        raise WorkflowError(
            "Archived current Finalizer transaction is incomplete or obsolete.",
            exit_code=2,
        )
    task = task_json(task_dir)
    if task.get("status") != "completed":
        raise WorkflowError(
            "Archived current Finalizer task is not completed.",
            exit_code=2,
        )
    remote = str(publish_config(load_config(root)).get("remote") or "origin")
    repo = validate_github_remote_repository(
        root,
        remote,
        str(transaction["repo_ref"]),
    )
    pr = resolve_closeout_pull_request(
        root,
        repo,
        str(transaction["branch"]),
        str(transaction["base_branch"]),
        remote,
    )
    bound_pr = transaction["pr"]
    adopted_pr = transaction.get("adopted_pr")
    expected_draft = (
        bool(adopted_pr.get("initial_is_draft"))
        if next_transition != "mark_ready" and isinstance(adopted_pr, dict)
        else False
    )
    if (
        pr is None
        or pr.get("number") != bound_pr.get("number")
        or pr.get("url")
        != canonical_pull_request_url(repo, int(bound_pr["number"]), bound_pr.get("url"))
        or pr.get("isDraft") is not expected_draft
    ):
        raise WorkflowError(
            "Archived current Finalizer pull request is not the exact Ready transaction.",
            exit_code=2,
        )
    ready_head = str(pr.get("headRefOid") or "")
    local_head = current_head(root)
    remote_head = closeout_remote_branch_head(
        root,
        {"git": {"remote": remote, "head_branch": transaction["branch"]}},
    )
    if (
        re.fullmatch(r"[0-9a-f]{40}", ready_head) is None
        or local_head != remote_head
        or local_head != ready_head
    ):
        raise WorkflowError(
            "Archived current Finalizer local, remote and Ready PR heads differ.",
            exit_code=2,
        )
    summary_path = task_dir / FINISH_SUMMARY_ARTIFACT
    if not summary_path.is_file() or summary_path.is_symlink():
        raise WorkflowError(
            "Archived current Finalizer summary is missing or unsafe.",
            exit_code=2,
        )
    summary = read_json(summary_path)
    validate_finish_summary(summary)
    if (
        summary.get("task", {}).get("artifact_dir") != task_ref
        or summary.get("task", {}).get("archive_dir") != archive_locator
        or summary.get("github", {}).get("pr_url") != pr.get("url")
        or summary.get("index", {}).get("search_terms", {}).get("pr_refs")
        != [f"PR #{pr['number']}"]
    ):
        raise WorkflowError(
            "Archived current Finalizer summary does not bind the Ready PR transaction.",
            exit_code=2,
        )
    plan = {
        "plan_digest": transaction["plan_digest"],
        "git": {
            "repo": repo,
            "remote": remote,
            "base_branch": transaction["base_branch"],
            "head_branch": transaction["branch"],
            "branch_review_commit": transaction["branch_review_commit"],
            "reviewed_content_head": transaction["branch_review_commit"],
        "publication_head": local_head,
        },
        "publish": copy.deepcopy(transaction["publication"]),
        "review": {
            "changed_paths": [],
        },
        "task": {
            "active_locator": task_ref,
            "archive_locator": archive_locator,
        },
    }
    return {
        "task_dir": task_dir,
        "task_context": None,
        "prepared": None,
        "plan": plan,
        "plan_ref": f"finalization:{transaction['plan_digest']}",
        "transaction_state": "ready" if next_transition == "mark_ready" else "archived",
        "published_transition_complete": next_transition == "mark_ready",
        "published_pr": pr if next_transition == "mark_ready" else None,
        "publication": {"owner_status": "current"},
        "publication_status": "current",
        "publication_stale_reason": None,
        "publication_branch_review_commit": transaction["branch_review_commit"],
        "reprepare_reason_code": None,
        "verification": None,
        "publication_mode": str(transaction.get("mode") or "ordinary_publication"),
        "existing_pr_recovery": copy.deepcopy(transaction.get("adopted_pr")),
    }

def finalization_current_terminal_context(
    root: Path,
    task_dir: Path,
    public_input: dict[str, Any],
    gate: dict[str, Any],
) -> dict[str, Any]:
    """Rebuild the checked Ready context after a no-reentry Finalizer run."""
    identity = gate["identity"]
    task_ref = str(public_input.get("task_ref") or "")
    archive_locator = repo_relative(root, task_dir)
    task = task_json(task_dir)
    summary_path = task_dir / FINISH_SUMMARY_ARTIFACT
    if task.get("status") != "completed":
        raise WorkflowError(
            "Archived current Finalizer task is not completed.", exit_code=2
        )
    if not summary_path.is_file() or summary_path.is_symlink():
        raise WorkflowError(
            "Archived current Finalizer summary is missing or unsafe.", exit_code=2
        )
    summary = read_json(summary_path)
    validate_finish_summary(summary)
    summary_task = summary.get("task") if isinstance(summary.get("task"), dict) else {}
    summary_git = summary.get("git") if isinstance(summary.get("git"), dict) else {}
    summary_github = (
        summary.get("github") if isinstance(summary.get("github"), dict) else {}
    )
    summary_commits = (
        summary_git.get("commits") if isinstance(summary_git.get("commits"), list) else []
    )
    search_terms = (
        summary.get("index", {}).get("search_terms", {})
        if isinstance(summary.get("index"), dict)
        and isinstance(summary.get("index", {}).get("search_terms"), dict)
        else {}
    )
    branch = str(task.get("branch") or "")
    base_branch = str(task.get("base_branch") or "")
    if (
        identity.get("task_ref") != task_ref
        or public_input.get("branch_review_commit")
        != identity.get("branch_review_commit")
        or summary_task.get("artifact_dir") != task_ref
        or summary_task.get("archive_dir") != archive_locator
        or summary_git.get("branch") != branch
        or summary_git.get("base_branch") != base_branch
        or identity.get("branch_review_commit") not in summary_commits
    ):
        raise WorkflowError(
            "Archived current Finalizer summary does not bind the terminal gate.",
            exit_code=2,
        )
    archive_commit = finalization_terminal_archive_commit(
        root,
        task_ref,
        archive_locator,
        str(identity.get("branch_review_commit") or ""),
    )
    remote = str(publish_config(load_config(root)).get("remote") or "origin")
    repo = normalize_github_repository(infer_github_repo(root))
    repo = validate_github_remote_repository(root, remote, repo)
    pr = resolve_closeout_pull_request(
        root,
        repo,
        branch,
        base_branch,
        remote,
    )
    if pr is None:
        raise WorkflowError(
            "Archived current Finalizer requires the bound Ready pull request.",
            exit_code=2,
        )
    pr_url, pr_number = parse_canonical_pull_request_url(
        repo, summary_github.get("pr_url")
    )
    ready_head = str(pr.get("headRefOid") or "")
    local_head = current_head(root)
    archive_status = run_stdout(
        ["git", "status", "--porcelain", "--untracked-files=all", "--", archive_locator],
        cwd=root,
    )
    reviewed_is_ancestor = run(
        [
            "git",
            "merge-base",
            "--is-ancestor",
            str(identity.get("branch_review_commit") or ""),
            local_head,
        ],
        cwd=root,
        check=False,
    ).returncode == 0
    remote_head = closeout_remote_branch_head(
        root,
        {"git": {"remote": remote, "head_branch": branch}},
    )
    if (
        pr.get("number") != pr_number
        or pr.get("url") != pr_url
        or pr.get("isDraft") is not False
        or pr.get("title") != public_input.get("pr_title")
        or pr.get("body") != public_input.get("pr_body")
        or re.fullmatch(r"[0-9a-f]{40}", ready_head) is None
        or local_head != remote_head
        or local_head != ready_head
        or local_head != archive_commit
        or archive_status
        or not reviewed_is_ancestor
        or search_terms.get("pr_refs") != [f"PR #{pr_number}"]
    ):
        raise WorkflowError(
            "Archived current Finalizer live Ready facts do not match its terminal gate.",
            exit_code=2,
        )
    plan = {
        "plan_digest": identity["plan_digest"],
        "git": {
            "repo": repo,
            "remote": remote,
            "base_branch": base_branch,
            "head_branch": branch,
            "branch_review_commit": identity["branch_review_commit"],
            "reviewed_content_head": identity["branch_review_commit"],
            "publication_head": ready_head,
        },
        "publish": {
            "title": public_input["pr_title"],
            "body": public_input["pr_body"],
        },
        "review": {"changed_paths": []},
        "task": {
            "active_locator": task_ref,
            "archive_locator": archive_locator,
        },
    }
    return {
        "task_dir": task_dir,
        "task_context": None,
        "prepared": None,
        "plan": plan,
        "plan_ref": identity["plan_ref"],
        "transaction_state": "ready",
        "published_transition_complete": True,
        "published_pr": pr,
        "publication": {"owner_status": "current"},
        "publication_status": "current",
        "publication_stale_reason": None,
        "publication_branch_review_commit": identity["branch_review_commit"],
        "reprepare_reason_code": None,
        "verification": None,
        "publication_mode": "ordinary_publication",
        "existing_pr_recovery": None,
    }

def finalization_preview_context(
    root: Path,
    args: argparse.Namespace,
    public_input: dict[str, Any],
) -> dict[str, Any]:
    official_after_archive_hook_state(root)
    eval_context = finalization_eval_preview_context(root, public_input)
    if eval_context is not None:
        return eval_context
    task_dir = finalization_task_dir(root, public_input)
    archived = task_dir_is_archived(root, task_dir)
    config = load_config(root)
    reprepare_reason_code: str | None = None
    transaction_rebind_recovery: dict[str, Any] | None = None
    if archived:
        transaction_match = finalization_find_transaction_by_task_ref(
            root,
            str(public_input.get("task_ref") or ""),
        )
        if transaction_match is not None:
            return finalization_current_archived_context(
                root,
                task_dir,
                public_input,
                transaction_match[0],
            )
        terminal_gate = finalization_current_terminal_gate(
            root,
            task_dir,
            str(public_input.get("task_ref") or ""),
        )
        if terminal_gate is not None:
            return finalization_current_terminal_context(
                root,
                task_dir,
                public_input,
                terminal_gate,
            )
        terminal_projection_gate = finalization_terminal_projection_gate(
            root,
            task_dir,
            public_input,
        )
        if terminal_projection_gate is not None:
            return finalization_current_terminal_context(
                root,
                task_dir,
                public_input,
                terminal_projection_gate,
            )
        raise WorkflowError(
            "Archived current Finalizer recovery has no transaction or terminal authority.",
            exit_code=2,
        )
    else:
        current_transaction = finalization_read_transaction(root, task_dir)
        verification = None
        publication = finalization_publication_owner_result(
            root,
            task_dir,
            public_input,
            verification,
        )
        if publication.get("owner_status") == "base_reconciliation_required":
            return {
                "task_dir": task_dir,
                "task_context": None,
                "prepared": None,
                "plan": None,
                "plan_ref": None,
                "transaction_state": "base_reconciliation_required",
                "publication": publication,
                "publication_status": "current",
                "publication_stale_reason": None,
                "publication_branch_review_commit": publication["branch_review_commit"],
                "base_reconciliation": publication,
                "verification": None,
            }
        if publication.get("owner_status") == "stale":
            return {
                "task_dir": task_dir,
                "task_context": None,
                "prepared": None,
                "plan": None,
                "plan_ref": None,
                "transaction_state": "publication_review_stale",
                "publication": publication,
                "publication_status": "stale",
                "publication_stale_reason": publication["stale_reason"],
                "publication_branch_review_commit": publication.get(
                    "branch_review_commit"
                ),
                "verification": None,
            }
        published_transition_complete = False
        published_pr = None
        task_context = load_task_runtime_identity(task_dir, config)
        assert_workspace_boundary(root, config, task_context, task_dir)
        prepared = prepare_closeout(
            root,
            args,
            config,
            task_dir,
            task_context,
            publication_ready=finalization_prepare_publication_ready(
                public_input,
                transaction=current_transaction,
            ),
            current_finalizer=True,
        )
        plan = prepared["plan"]
        if current_transaction is not None:
            try:
                finalization_validate_transaction_plan(
                    current_transaction,
                    plan,
                )
            except WorkflowError:
                if (
                    current_transaction.get("mode") == "ordinary_publication"
                    and current_transaction.get("next_transition") == "push_content"
                    and current_transaction.get("pr") is None
                    and current_transaction.get("adopted_pr") is None
                ):
                    transaction_rebind_recovery = (
                        classify_provenance_tail_transaction_rebind(
                            root,
                            plan,
                            current_transaction,
                        )
                    )
                    if transaction_rebind_recovery is None:
                        if provenance_tail_transaction_reprepare_eligible(
                            root,
                            plan,
                            current_transaction,
                        ):
                            base_evolution = None
                        else:
                            raise
                        prepared["pre_pr_reprepare"] = {
                            "previous_transaction": copy.deepcopy(current_transaction),
                            "prior_state": "content_pushed",
                            "base_evolution": base_evolution,
                        }
                else:
                    raise
        if prepared.get("month_supersession") is not None:
            state = "reprepare_required"
            reprepare_reason_code = FINALIZATION_REPREPARE_ARCHIVE_MONTH
        elif prepared.get("pre_pr_reprepare") is not None:
            state = "reprepare_required"
            reprepare_reason_code = FINALIZATION_REPREPARE_PROVENANCE_TAIL
        else:
            state = resolve_closeout_pre_draft_state(
                root,
                task_dir,
                plan,
            )
            if (
                public_input.get("profile") == "reprepare_preview"
                and public_input.get("reason_code")
                == FINALIZATION_REPREPARE_PROVENANCE_TAIL
                and state == "content_pushed"
            ):
                remote_head = closeout_remote_branch_head(root, plan)
                publication_head = str(
                    plan["git"].get("publication_head")
                    or plan["git"]["branch_review_commit"]
                )
                if remote_head != publication_head:
                    if remote_head and is_ancestor(root, remote_head, publication_head):
                        state = "prepared"
                    else:
                        raise WorkflowError(
                            "Reprepared closeout remote HEAD is not the immutable publication ancestor.",
                            exit_code=2,
                            payload={
                                "remote_head": remote_head,
                                "publication_head": publication_head,
                            },
                        )
    existing_pr_recovery: dict[str, Any] | None = None
    if not archived and isinstance(plan, dict):
        if transaction_rebind_recovery is not None:
            state = "existing_pr_recovery"
            existing_pr_recovery = transaction_rebind_recovery
        else:
            state, existing_pr_recovery = finalization_existing_pr_recovery_context(
                root, plan, current_transaction, state
            )
    if (
        not archived
        and isinstance(prepared, dict)
        and state in {"prepared", "content_pushed"}
        and prepared.get("metadata_tail") is None
        and finalizer_pre_pr_provenance_tail_applies(
            root,
            plan,
            current_transaction,
        )
    ):
        state = "reprepare_required"
        reprepare_reason_code = FINALIZATION_REPREPARE_PROVENANCE_TAIL
    plan_ref = f"finalization:{plan['plan_digest']}"
    input_plan_ref = public_input.get("plan_ref")
    if (
        isinstance(input_plan_ref, str)
        and input_plan_ref != plan_ref
    ):
        raise WorkflowError(
            "Task finalization plan_ref does not match the current immutable plan.",
            exit_code=2,
        )
    return {
        "task_dir": task_dir,
        "task_context": task_context,
        "prepared": prepared,
        "plan": plan,
        "plan_ref": plan_ref,
        "transaction_state": state,
        "published_transition_complete": published_transition_complete,
        "published_pr": published_pr,
        "publication": publication,
        "publication_status": "current",
        "publication_stale_reason": None,
        "publication_branch_review_commit": plan["git"]["branch_review_commit"],
        "reprepare_reason_code": reprepare_reason_code,
        "verification": verification,
        "publication_mode": (
            "existing_pr_recovery"
            if existing_pr_recovery is not None
            else "ordinary_publication"
        ),
        "existing_pr_recovery": existing_pr_recovery,
    }

def cmd_preview_finalization(args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(Path(args.root or os.getcwd()))
    public_input, input_locator = finalization_public_input(root, args.input)
    context = finalization_preview_context(root, args, public_input)
    return finalization_preview_receipt(root, public_input, input_locator, context)


def finalization_confirmation_projection(
    public_input: dict[str, Any],
    context: dict[str, Any],
) -> dict[str, Any] | None:
    plan = context.get("plan")
    if not isinstance(plan, dict):
        return None
    publication_mode = str(
        context.get("publication_mode")
        or (
            "existing_pr_recovery"
            if isinstance(context.get("existing_pr_recovery"), dict)
            else "ordinary_publication"
        )
    )
    side_effects = (
        [
            "bind_existing_pr_transaction",
            "push_or_preserve_exact_publication_head",
            "converge_or_preserve_pr_metadata",
            "archive",
            "push_archive",
            "mark_or_preserve_ready",
            "verify_three_way_head",
        ]
        if publication_mode == "existing_pr_recovery"
        else [
            "push_exact_publication_head",
            "create_draft_pr",
            "archive",
            "push_archive",
            "mark_ready",
            "verify_three_way_head",
        ]
    )
    return {
        "schema_version": "1.0",
        "task_ref": str(public_input.get("task_ref") or plan["task"]["active_locator"]),
        "repo_ref": plan["git"]["repo"],
        "base_branch": plan["git"]["base_branch"],
        "head_branch": plan["git"]["head_branch"],
        "branch_review_commit": plan["git"]["branch_review_commit"],
        "pr_title": plan["publish"]["title"],
        "pr_body": plan["publish"]["body"],
        "publication_mode": publication_mode,
        "side_effects": side_effects,
    }


def finalization_confirmation_identity(
    public_input: dict[str, Any],
    context: dict[str, Any],
) -> str | None:
    projection = finalization_confirmation_projection(public_input, context)
    return canonical_json_sha256(projection) if projection is not None else None


def finalization_preview_receipt(
    root: Path,
    public_input: dict[str, Any],
    input_locator: str,
    context: dict[str, Any],
) -> dict[str, Any]:
    plan = context["plan"]
    if plan is None:
        receipt = {
            "schema_version": "1.0",
            "status": "ok",
            "side_effects": False,
            "input_locator": input_locator,
            "profile": public_input["profile"],
            "mode": public_input["mode"],
            "task_ref": public_input["task_ref"],
            "plan_ref": None,
            "finalization_plan": None,
            "finalization_plan_bytes_sha256": None,
            "finalization_plan_digest": None,
            "branch_review_commit": context.get(
                "publication_branch_review_commit"
            ),
            "transaction_state": context["transaction_state"],
            "publication_status": context["publication_status"],
            "publication_stale_reason": context["publication_stale_reason"],
            "expected_actions": [],
            "publication_mode": "ordinary_publication",
            "existing_pr_recovery": None,
            "confirmation_identity": None,
        }
    else:
        receipt = {
            "schema_version": "1.0",
            "status": "ok",
            "side_effects": False,
            "input_locator": input_locator,
            "profile": public_input["profile"],
            "mode": public_input["mode"],
            "task_ref": public_input["task_ref"],
            "plan_ref": context["plan_ref"],
            "finalization_plan": plan,
            "finalization_plan_bytes_sha256": hashlib.sha256(
                closeout_json_artifact_bytes(plan)
            ).hexdigest(),
            "finalization_plan_digest": plan["plan_digest"],
            "branch_review_commit": plan["git"]["branch_review_commit"],
            "transaction_state": context["transaction_state"],
            "publication_status": context["publication_status"],
            "publication_stale_reason": context["publication_stale_reason"],
            "publication_mode": context.get("publication_mode", "ordinary_publication"),
            "existing_pr_recovery": copy.deepcopy(context.get("existing_pr_recovery")),
            "expected_actions": (
                [
                    "bind_existing_pr_transaction",
                    "push_exact_publication_head"
                    if context.get("existing_pr_recovery", {}).get("push_required")
                    else "preserve_existing_remote_head",
                    "converge_pr_metadata"
                    if context.get("existing_pr_recovery", {}).get("metadata_update_required")
                    else "preserve_current_pr_metadata",
                    "archive",
                    "push_archive",
                    context.get("existing_pr_recovery", {}).get("ready_action"),
                    "verify_three_way_head",
                ]
                if context.get("existing_pr_recovery") is not None
                else list(CLOSEOUT_TRANSITIONS[1:])
            ),
            "confirmation_identity": finalization_confirmation_identity(
                public_input,
                context,
            ),
        }
    errors: list[str] = []
    schema = skill_read_schema(
        finalization_package_root(root) / "schemas/finalization-preview-1.0.schema.json",
        "task finalization preview receipt",
        errors,
    )
    if isinstance(schema, dict):
        errors.extend(
            skill_json_schema_validation_errors(
                receipt,
                schema,
                "task finalization preview receipt",
            )
        )
    if errors or not isinstance(schema, dict):
        raise WorkflowError(
            "Task finalization preview receipt is invalid.",
            exit_code=2,
            payload={"errors": errors},
        )
    return receipt

def finalization_output_contract(
    root: Path,
    exit_id: str,
) -> dict[str, Any]:
    package = finalization_package_root(root)
    interface = finalization_interface(root)
    schema, _ = stage0_output_contract(
        FINALIZE_TASK_SKILL_ID,
        package,
        interface,
        exit_id,
    )
    return schema

def finalization_reprepare_public_output(
    root: Path,
    *,
    task_ref: str,
    reason_code: str,
    branch_review_commit: str,
    publication_head: str,
) -> dict[str, Any]:
    payload = {
        "exit_id": "reprepare_required",
        "task_ref": task_ref,
        "reason_code": reason_code,
        "branch_review_commit": branch_review_commit,
        "publication_head": publication_head,
    }
    errors = skill_json_schema_validation_errors(
        payload,
        finalization_output_contract(root, "reprepare_required"),
        "task finalization reprepare_required output",
    )
    if errors:
        raise WorkflowError(
            "Task finalization reprepare output is invalid.",
            exit_code=2,
            payload={"errors": errors},
        )
    return payload

def finalization_route_branch_review_commit(
    context: dict[str, Any],
    exit_id: str,
) -> str | None:
    if exit_id == "publication_review_stale":
        value = context.get("publication_branch_review_commit")
        return str(value) if isinstance(value, str) else None
    plan = context.get("plan")
    if isinstance(plan, dict):
        return str(plan["git"]["branch_review_commit"])
    return None

def finalization_validate_route(
    root: Path,
    public_input: dict[str, Any],
    context: dict[str, Any],
    route: dict[str, Any],
    *,
    allow_pending_transition: bool = False,
) -> None:
    exit_id = str(route.get("typed_exit") or "")
    if route.get("consumer") != FINALIZATION_CONSUMERS.get(exit_id):
        raise WorkflowError(
            "Task finalization selected consumer does not match the typed exit.",
            exit_code=2,
        )
    output = route.get("output")
    if not isinstance(output, dict):
        raise WorkflowError("Task finalization route output must be an object.", exit_code=2)
    plan = context["plan"]
    state = context["transaction_state"]
    executor_materialized = output == FINALIZATION_EXECUTOR_OUTPUT_MARKER
    if executor_materialized and exit_id not in {"ready_for_merge", "reprepare_required"}:
        raise WorkflowError(
            "Only ready_for_merge or reprepare_required may defer public output to the deterministic executor.",
            exit_code=2,
        )
    if exit_id == "ready_for_merge" and not executor_materialized:
        raise WorkflowError(
            "The persisted ready_for_merge route must retain the exact private executor marker.",
            exit_code=2,
        )
    if (
        exit_id == "reprepare_required"
        and context.get("reprepare_reason_code") == FINALIZATION_REPREPARE_PROVENANCE_TAIL
        and not executor_materialized
    ):
        raise WorkflowError(
            "Provenance reprepare must retain the executor marker until publication_head exists.",
            exit_code=2,
        )
    if (
        exit_id == "reprepare_required"
        and context.get("reprepare_reason_code") == FINALIZATION_REPREPARE_ARCHIVE_MONTH
        and executor_materialized
    ):
        raise WorkflowError(
            "Archive-month reprepare must retain its complete current public output.",
            exit_code=2,
        )
    if executor_materialized and not (
        allow_pending_transition
        or (
            state in FINALIZATION_COMMITTED_RECOVERY_STATES
            and context.get("published_transition_complete") is True
        )
    ):
        raise WorkflowError(
            "The executor marker is not valid before its checked transition.",
            exit_code=2,
        )
    if not executor_materialized:
        schema = finalization_output_contract(root, exit_id)
        errors = skill_json_schema_validation_errors(
            output,
            schema,
            f"task finalization route output {exit_id}",
        )
        if errors:
            raise WorkflowError(
                "Task finalization route output is invalid.",
                exit_code=2,
                payload={"errors": errors},
            )
        if exit_id == "base_reconciliation_required":
            facts = context.get("base_reconciliation")
            if not isinstance(facts, dict) or output != {
                "exit_id": exit_id,
                **{
                    key: facts[key]
                    for key in (
                        "task_ref",
                        "task_head",
                        "publication_head",
                        "selected_base_ref",
                        "old_base_head",
                        "new_base_head",
                        "branch_review_commit",
                        "resume_target",
                    )
                },
            }:
                raise WorkflowError(
                    "base_reconciliation_required does not match the current base pair.",
                    exit_code=2,
                )
            return
        expected_task_ref = (
            plan["task"]["archive_locator"]
            if exit_id == "ready_for_merge"
            and plan is not None
            and state in FINALIZATION_COMMITTED_RECOVERY_STATES
            else public_input.get("task_ref")
        )
        for field, expected in (
            ("task_ref", expected_task_ref),
            ("plan_ref", context.get("plan_ref")),
            (
                "branch_review_commit",
                finalization_route_branch_review_commit(context, exit_id),
            ),
            (
                "publication_head",
                (
                    plan["git"].get("publication_head")
                    or plan["git"].get("branch_review_commit")
                )
                if plan is not None
                else None,
            ),
        ):
            if field in output and output.get(field) != expected:
                raise WorkflowError(
                    f"Task finalization route output {field} does not match current facts.",
                    exit_code=2,
                )
    publication_status = context.get("publication_status", "current")
    if context.get("transaction_state") == "base_reconciliation_required" and exit_id != "blocked":
        raise WorkflowError("Current base evolution requires reconciliation or a blocked route.", exit_code=2)
    if exit_id == "publication_review_stale":
        if (
            publication_status != "stale"
            or state != "publication_review_stale"
            or output.get("task_ref") != public_input.get("task_ref")
            or output.get("branch_review_commit")
            != context.get("publication_branch_review_commit")
            or output.get("stale_reason")
            != context.get("publication_stale_reason")
        ):
            raise WorkflowError(
                "publication_review_stale is not compatible with current owner facts.",
                exit_code=2,
            )
        return
    if publication_status == "stale" and exit_id != "blocked":
        raise WorkflowError(
            "Current stale publication facts require an AI-authored stale or blocked route.",
            exit_code=2,
        )
    if plan is None:
        return
    if exit_id == "resume_finalization":
        if state not in FINALIZATION_RESUME_RECOVERY_STATES:
            raise WorkflowError(
                "resume_finalization is not compatible with a legal same-plan recovery state.",
                exit_code=2,
            )
    if exit_id == "reprepare_required" and state != "reprepare_required":
        raise WorkflowError(
            "reprepare_required is not compatible with the current transaction state.",
            exit_code=2,
        )
    if exit_id == "reprepare_required" and context.get("reprepare_reason_code") not in {
        FINALIZATION_REPREPARE_ARCHIVE_MONTH,
        FINALIZATION_REPREPARE_PROVENANCE_TAIL,
    }:
        raise WorkflowError(
            "reprepare_required reason does not match the current recovery state.",
            exit_code=2,
        )
    if (
        exit_id == "reprepare_required"
        and not executor_materialized
        and output.get("reason_code") != context.get("reprepare_reason_code")
    ):
        raise WorkflowError(
            "reprepare_required reason does not match the current recovery state.",
            exit_code=2,
        )
    if exit_id == "ready_for_merge" and state not in FINALIZATION_COMMITTED_RECOVERY_STATES:
        if not allow_pending_transition or not executor_materialized:
            raise WorkflowError(
                "ready_for_merge requires the exact private marker before its executor transition.",
                exit_code=2,
            )
    if (
        exit_id == "ready_for_merge"
        and state in FINALIZATION_COMMITTED_RECOVERY_STATES
        and context.get("published_transition_complete") is not True
        and not allow_pending_transition
    ):
        raise WorkflowError(
            "ready_for_merge requires the exact archive transaction and ready pull request.",
            exit_code=2,
        )

def finalization_gate_schema(root: Path) -> dict[str, Any]:
    errors: list[str] = []
    schema = skill_read_schema(
        finalization_package_root(root) / "schemas/task-finalization-gate-5.0.schema.json",
        "task finalization gate schema",
        errors,
    )
    if errors or not isinstance(schema, dict):
        raise WorkflowError("Task finalization gate schema is unavailable.", exit_code=2)
    return schema

def finalization_normalize_gate(root: Path, payload: Any) -> dict[str, Any]:
    del root
    if not isinstance(payload, dict):
        raise WorkflowError("Task finalization gate must be an object.", exit_code=2)
    return payload

def cmd_record_finalization_gate(args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(Path(args.root or os.getcwd()))
    public_input, _ = finalization_public_input(root, args.input)
    reviewed = finalization_semantic_review_input(root, args.review_input)
    context = finalization_preview_context(root, args, public_input)
    return finalization_record_gate_result(
        root,
        public_input,
        reviewed,
        context,
        dry_run=bool(getattr(args, "dry_run", False)),
        include_private=False,
    )


def finalization_record_gate_result(
    root: Path,
    public_input: dict[str, Any],
    reviewed: dict[str, Any],
    context: dict[str, Any],
    *,
    dry_run: bool,
    include_private: bool,
) -> dict[str, Any]:
    finalization_validate_route(
        root,
        public_input,
        context,
        reviewed["route"],
        allow_pending_transition=True,
    )
    plan = context["plan"]
    gate = {
        "schema_version": FINALIZATION_GATE_SCHEMA_VERSION,
        "skill_id": FINALIZE_TASK_SKILL_ID,
        "identity": {
            "task_ref": public_input["task_ref"],
            "plan_ref": context["plan_ref"] if plan is not None else None,
            "plan_digest": plan["plan_digest"] if plan is not None else None,
            "branch_review_commit": finalization_route_branch_review_commit(
                context,
                str(reviewed["route"]["typed_exit"]),
            ),
        },
        "review": copy.deepcopy(reviewed["review"]),
        "route": copy.deepcopy(reviewed["route"]),
    }
    errors = skill_json_schema_validation_errors(
        gate,
        finalization_gate_schema(root),
        "task finalization gate",
    )
    if errors:
        raise WorkflowError(
            "Task finalization recorder produced an invalid gate.",
            exit_code=2,
            payload={"errors": errors},
        )
    task_dir = context["task_dir"]
    artifact_path = task_finalization_path(root, task_dir)
    committed_recovery = (
        context["transaction_state"] in FINALIZATION_COMMITTED_RECOVERY_STATES
    )
    if not dry_run and not committed_recovery:
        write_json(artifact_path, gate)
    result = {
        "status": "ok",
        "artifact_path": str(artifact_path),
        "typed_exit": gate["route"]["typed_exit"],
        "plan_ref": context["plan_ref"],
        "plan_digest": plan["plan_digest"] if plan is not None else None,
        "dry_run": dry_run,
    }
    if include_private:
        result["gate"] = gate
        result["gate_path"] = artifact_path
    return result

def finalization_gate_input(
    root: Path,
    public_input: dict[str, Any],
    value: str | None,
) -> tuple[dict[str, Any], Path]:
    task_dir = finalization_task_dir(root, public_input)
    expected = task_finalization_path(root, task_dir)
    if task_dir_is_archived(root, task_dir):
        transaction_match = finalization_find_transaction_by_task_ref(
            root,
            str(public_input.get("task_ref") or ""),
        )
        # A completed terminal recovery retires the owner gate and transaction.
        # Keep the caller's exact locator binding, but allow the archived
        # committed-terminal projection to rebuild the checked marker when the
        # normal owner artifact was intentionally retired.
        owner_result_missing_after_terminal_cleanup = False
        if value:
            relative = skill_safe_relative(str(value).strip())
            supplied = root / relative if relative is not None else None
            if supplied is None or supplied.resolve() != expected.resolve():
                raise WorkflowError(
                    "Task finalization gate must use the exact owner-private artifact.",
                    exit_code=2,
                )
            if expected.exists() or expected.is_symlink():
                supplied = stage0_owner_path(root, value, "arguments.owner_result")
            else:
                owner_result_missing_after_terminal_cleanup = True
        if transaction_match is not None:
            if not expected.is_file() or expected.is_symlink():
                raise WorkflowError(
                    "Archived current Finalizer is missing its owner-private gate.",
                    exit_code=2,
                )
            return finalization_normalize_gate(root, read_json(expected)), expected
        terminal_gate = finalization_current_terminal_gate(
            root,
            task_dir,
            str(public_input.get("task_ref") or ""),
        )
        if terminal_gate is not None:
            if value and not owner_result_missing_after_terminal_cleanup:
                supplied = stage0_owner_path(root, value, "arguments.owner_result")
                if supplied.resolve() != expected.resolve():
                    raise WorkflowError(
                        "Task finalization gate must use the exact owner-private artifact.",
                        exit_code=2,
                    )
            return terminal_gate, expected
        terminal_projection_gate = finalization_terminal_projection_gate(
            root,
            task_dir,
            public_input,
        )
        if terminal_projection_gate is not None:
            if not value or not owner_result_missing_after_terminal_cleanup:
                raise WorkflowError(
                    "Retired terminal projection requires its exact owner-private locator.",
                    exit_code=2,
                )
            return terminal_projection_gate, expected
        raise WorkflowError(
            "Archived current Finalizer gate is unavailable.",
            exit_code=2,
        )
    transition = task_finalization_transition_path(root, task_dir)
    path = (
        stage0_owner_path(root, value, "arguments.owner_result")
        if value
        else (
            transition
            if transition.is_file() and not transition.is_symlink()
            else expected
        )
    )
    if path.resolve() not in {expected.resolve(), transition.resolve()}:
        raise WorkflowError(
            "Task finalization gate must use the exact owner-private artifact.",
            exit_code=2,
        )
    if path.resolve() == transition.resolve() and (
        not expected.is_file() or expected.is_symlink()
    ):
        raise WorkflowError(
            "Task finalization transition gate requires its predecessor checkpoint.",
            exit_code=2,
        )
    return finalization_normalize_gate(root, read_json(path)), path

def check_finalization_gate_result(
    root: Path,
    args: argparse.Namespace,
    public_input: dict[str, Any],
    gate: dict[str, Any],
    gate_path: Path,
    *,
    allow_pending_transition: bool = False,
) -> tuple[dict[str, Any], dict[str, Any]]:
    preview_args = copy.copy(args)
    preview_args._finalization_checked_gate = gate
    context = finalization_preview_context(root, preview_args, public_input)
    return check_finalization_gate_context(
        root,
        public_input,
        gate,
        gate_path,
        context,
        allow_pending_transition=allow_pending_transition,
    )


def check_finalization_gate_context(
    root: Path,
    public_input: dict[str, Any],
    gate: dict[str, Any],
    gate_path: Path,
    context: dict[str, Any],
    *,
    allow_pending_transition: bool = False,
) -> tuple[dict[str, Any], dict[str, Any]]:
    errors = skill_json_schema_validation_errors(
        gate,
        finalization_gate_schema(root),
        "task finalization gate",
    )
    transition_gate = task_finalization_transition_path(root, context["task_dir"])
    if (
        gate_path.resolve() == transition_gate.resolve()
    ):
        errors.append(
            "task finalization transition gate is outside base-evolution supersession"
        )
    committed_recovery = (
        context["transaction_state"] in FINALIZATION_COMMITTED_RECOVERY_STATES
    )
    plan = context["plan"]
    expected_identity = {
        "task_ref": (
            plan["task"]["active_locator"]
            if committed_recovery and plan is not None
            else public_input["task_ref"]
        ),
        "plan_ref": context["plan_ref"] if plan is not None else None,
        "plan_digest": plan["plan_digest"] if plan is not None else None,
        "branch_review_commit": finalization_route_branch_review_commit(
            context,
            str((gate.get("route") or {}).get("typed_exit") or ""),
        ),
    }
    if gate.get("identity") != expected_identity:
        errors.append("task finalization gate objective identity mismatch")
    try:
        finalization_validate_route(
            root,
            public_input,
            context,
            gate.get("route") or {},
            allow_pending_transition=allow_pending_transition,
        )
    except WorkflowError as exc:
        errors.append(str(exc))
    if errors:
        raise WorkflowError(
            "Task finalization gate failed objective checks.",
            exit_code=2,
            payload={"artifact_path": str(gate_path), "errors": errors},
        )
    return gate, context

def cmd_check_finalization_gate(args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(Path(args.root or os.getcwd()))
    public_input, _ = finalization_public_input(root, args.input)
    gate, gate_path = finalization_gate_input(root, public_input, args.gate)
    checked, context = check_finalization_gate_result(
        root,
        args,
        public_input,
        gate,
        gate_path,
        allow_pending_transition=True,
    )
    return {
        "status": "ok",
        "artifact_path": str(gate_path),
        "typed_exit": checked["route"]["typed_exit"],
        "task_ref": public_input["task_ref"],
        "plan_ref": context["plan_ref"],
        "plan_digest": (
            context["plan"]["plan_digest"]
            if context["plan"] is not None
            else None
        ),
        "transaction_state": context["transaction_state"],
    }

def finalization_gate_with_ready_for_merge_output(
    root: Path,
    task_dir: Path,
    gate: dict[str, Any],
    plan: dict[str, Any],
    pr: dict[str, Any],
) -> dict[str, Any]:
    if (
        gate.get("route", {}).get("typed_exit") != "ready_for_merge"
        or gate.get("route", {}).get("output")
        != FINALIZATION_EXECUTOR_OUTPUT_MARKER
    ):
        raise WorkflowError(
            "Task finalization gate did not retain the exact private ready_for_merge marker.",
            exit_code=2,
        )
    if repo_relative(root, task_dir) != plan["task"]["archive_locator"]:
        raise WorkflowError(
            "Task finalization ready_for_merge output requires the exact archived task locator.",
            exit_code=2,
        )
    updated = copy.deepcopy(gate)
    updated["route"]["output"] = {
        "exit_id": "ready_for_merge",
        "repo_ref": plan["git"]["repo"],
        "pr_number": pr["number"],
        "pr_url": canonical_pull_request_url(
            plan["git"]["repo"],
            pr["number"],
            pr["url"],
        ),
        "expected_head_sha": pr["headRefOid"],
        "expected_base_branch": plan["git"]["base_branch"],
        "expected_head_branch": plan["git"]["head_branch"],
        "publication_body_sha256": hashlib.sha256(
            plan["publish"]["body"].encode("utf-8")
        ).hexdigest(),
    }
    errors = skill_json_schema_validation_errors(
        updated["route"]["output"],
        finalization_output_contract(root, "ready_for_merge"),
        "task finalization ready_for_merge output",
    )
    if errors:
        raise WorkflowError(
            "Task finalization ready_for_merge output is invalid.",
            exit_code=2,
            payload={"errors": errors},
        )
    return updated
