def classify_unbound_equal_head_recovery(
    root: Path,
    plan: dict[str, Any],
    transaction: dict[str, Any],
) -> dict[str, Any] | None:
    """Adopt only one exact ordinary transaction whose publication is already pushed."""
    if (
        transaction.get("mode") != "ordinary_publication"
        or transaction.get("next_transition") != "push_content"
        or transaction.get("pr") is not None
        or transaction.get("adopted_pr") is not None
    ):
        return None
    finalization_validate_transaction_plan(transaction, plan)
    git = plan["git"]
    candidate = resolve_closeout_pull_request(
        root,
        git["repo"],
        git["head_branch"],
        git["base_branch"],
        git["remote"],
    )
    if candidate is None:
        terminal_prs = resolve_closeout_terminal_pull_requests(
            root,
            git["repo"],
            git["head_branch"],
            git["base_branch"],
            git["remote"],
        )
        if terminal_prs:
            raise WorkflowError(
                "Unbound equal-HEAD recovery found a Closed or Merged pull request for the immutable head/base.",
                exit_code=2,
                payload={
                    "reason_code": "pre_finalizer_terminal_pr_exists",
                    "pull_requests": terminal_prs,
                },
            )
        return None
    remote_head = closeout_remote_branch_head(root, plan)
    publication_head = str(
        git.get("publication_head") or git.get("branch_review_commit") or ""
    )
    if remote_head != str(candidate.get("headRefOid") or ""):
        return classify_existing_pr_recovery(
            root,
            plan,
            candidate,
            remote_head,
            allow_equal=True,
        )
    if remote_head != publication_head:
        raise WorkflowError(
            "Unbound ordinary recovery requires identical remote, PR, and Publication HEADs.",
            exit_code=2,
            payload={
                "reason_code": "existing_pr_unbound_equal_head_required",
                "remote_head": remote_head,
                "pr_head": candidate.get("headRefOid"),
                "publication_head": publication_head,
            },
        )
    return classify_existing_pr_recovery(
        root,
        plan,
        candidate,
        remote_head,
        allow_equal=True,
    )

def finalization_validate_recovery_metadata_decision(
    publication: dict[str, Any],
    metadata_comparison: Any,
    metadata_update_required: Any,
) -> dict[str, Any]:
    """Validate the persisted original metadata snapshot and convergence decision."""
    if (
        not isinstance(metadata_comparison, dict)
        or set(metadata_comparison)
        != {"live_title", "live_body", "title_matches", "body_matches"}
        or not isinstance(metadata_comparison.get("live_title"), str)
        or not isinstance(metadata_comparison.get("live_body"), str)
        or not isinstance(metadata_comparison.get("title_matches"), bool)
        or not isinstance(metadata_comparison.get("body_matches"), bool)
        or not isinstance(metadata_update_required, bool)
    ):
        raise WorkflowError(
            "Existing PR recovery transaction metadata decision is incomplete.",
            exit_code=2,
            payload={"reason_code": "existing_pr_transaction_drift"},
        )
    expected_comparison = {
        "live_title": metadata_comparison["live_title"],
        "live_body": metadata_comparison["live_body"],
        "title_matches": (
            metadata_comparison["live_title"] == publication.get("title")
        ),
        "body_matches": (
            metadata_comparison["live_body"] == publication.get("body")
        ),
    }
    expected_update_required = not (
        expected_comparison["title_matches"]
        and expected_comparison["body_matches"]
    )
    if (
        metadata_comparison != expected_comparison
        or metadata_update_required is not expected_update_required
    ):
        raise WorkflowError(
            "Existing PR recovery transaction metadata decision is inconsistent.",
            exit_code=2,
            payload={"reason_code": "existing_pr_transaction_drift"},
        )
    return copy.deepcopy(metadata_comparison)

def finalization_convert_unbound_equal_head_transaction(
    plan: dict[str, Any],
    transaction: dict[str, Any],
    pr: dict[str, Any],
    recovery: dict[str, Any],
) -> dict[str, Any]:
    """Convert one exact ordinary owner transaction into its bound recovery shape."""
    finalization_validate_transaction_plan(transaction, plan)
    publication_head = str(
        plan["git"].get("publication_head")
        or plan["git"].get("branch_review_commit")
        or ""
    )
    if (
        transaction.get("mode") != "ordinary_publication"
        or transaction.get("next_transition") != "push_content"
        or transaction.get("pr") is not None
        or transaction.get("adopted_pr") is not None
        or recovery.get("mode") != "existing_pr_recovery"
        or recovery.get("ancestry") != "equal"
        or recovery.get("push_required") is not False
        or recovery.get("publication_head") != publication_head
        or recovery.get("pre_push_remote_head") != publication_head
        or recovery.get("pr")
        != {"number": pr.get("number"), "url": pr.get("url")}
        or not isinstance(recovery.get("initial_is_draft"), bool)
    ):
        raise WorkflowError(
            "Unbound equal-HEAD recovery no longer matches its exact ordinary transaction.",
            exit_code=2,
            payload={"reason_code": "existing_pr_recovery_drift"},
        )
    metadata_comparison = finalization_validate_recovery_metadata_decision(
        transaction["publication"],
        recovery.get("metadata_comparison"),
        recovery.get("metadata_update_required"),
    )
    adopted_pr = {
        "number": pr["number"],
        "url": pr["url"],
        "initial_is_draft": bool(recovery["initial_is_draft"]),
        "pre_push_remote_head": publication_head,
        "metadata_update_required": bool(
            recovery["metadata_update_required"]
        ),
        "metadata_comparison": metadata_comparison,
    }
    return finalization_transaction_from_plan(
        plan,
        next_transition="bind_pr",
        pr=pr,
        mode="existing_pr_recovery",
        adopted_pr=adopted_pr,
    )

def finalization_adopt_unbound_equal_head_transaction(
    root: Path,
    task_dir: Path,
    plan: dict[str, Any],
    transaction: dict[str, Any],
    recovery_preview: dict[str, Any],
) -> dict[str, Any]:
    """Reread exact live facts, convert once, and persist before external mutation."""
    current_recovery = classify_unbound_equal_head_recovery(
        root,
        plan,
        transaction,
    )
    if current_recovery is None or current_recovery != recovery_preview:
        raise WorkflowError(
            "Unbound equal-HEAD recovery facts changed after semantic preview.",
            exit_code=2,
            payload={"reason_code": "existing_pr_recovery_drift"},
        )
    converted = finalization_convert_unbound_equal_head_transaction(
        plan,
        transaction,
        current_recovery["pr"],
        current_recovery,
    )
    finalization_write_transaction(root, task_dir, converted)
    return converted

def finalization_convert_provenance_tail_transaction(
    plan: dict[str, Any],
    transaction: dict[str, Any],
    pr: dict[str, Any],
    recovery: dict[str, Any],
) -> dict[str, Any]:
    """Project one legal predecessor transaction into current strict recovery."""
    publication_head = str(
        plan["git"].get("publication_head")
        or plan["git"].get("branch_review_commit")
        or ""
    )
    pre_push_remote_head = str(recovery.get("pre_push_remote_head") or "")
    if (
        transaction.get("mode") != "ordinary_publication"
        or transaction.get("next_transition") != "push_content"
        or transaction.get("pr") is not None
        or transaction.get("adopted_pr") is not None
        or recovery.get("mode") != "existing_pr_recovery"
        or recovery.get("ancestry") != "strict_ancestor"
        or recovery.get("push_required") is not True
        or recovery.get("publication_head") != publication_head
        or re.fullmatch(r"[0-9a-f]{40}", pre_push_remote_head) is None
        or recovery.get("pr")
        != {"number": pr.get("number"), "url": pr.get("url")}
        or not isinstance(recovery.get("initial_is_draft"), bool)
    ):
        raise WorkflowError(
            "Provenance-tail recovery no longer matches its predecessor transaction.",
            exit_code=2,
            payload={"reason_code": "existing_pr_recovery_drift"},
        )
    metadata_comparison = finalization_validate_recovery_metadata_decision(
        {
            "title": plan["publish"]["title"],
            "body": plan["publish"]["body"],
        },
        recovery.get("metadata_comparison"),
        recovery.get("metadata_update_required"),
    )
    adopted_pr = {
        "number": pr["number"],
        "url": pr["url"],
        "initial_is_draft": bool(recovery["initial_is_draft"]),
        "pre_push_remote_head": pre_push_remote_head,
        "metadata_update_required": bool(recovery["metadata_update_required"]),
        "metadata_comparison": metadata_comparison,
    }
    return finalization_transaction_from_plan(
        plan,
        next_transition="push_content",
        pr=pr,
        pre_push_remote_head=pre_push_remote_head,
        mode="existing_pr_recovery",
        adopted_pr=adopted_pr,
    )

def finalization_adopt_provenance_tail_transaction(
    root: Path,
    task_dir: Path,
    plan: dict[str, Any],
    transaction: dict[str, Any],
    recovery_preview: dict[str, Any],
) -> dict[str, Any]:
    """Reread, bind, and persist strict recovery before its publication push."""
    current_recovery = classify_provenance_tail_transaction_rebind(
        root,
        plan,
        transaction,
    )
    if current_recovery is None or current_recovery != recovery_preview:
        raise WorkflowError(
            "Provenance-tail recovery facts changed after semantic preview.",
            exit_code=2,
            payload={"reason_code": "existing_pr_recovery_drift"},
        )
    converted = finalization_convert_provenance_tail_transaction(
        plan,
        transaction,
        current_recovery["pr"],
        current_recovery,
    )
    finalization_write_transaction(root, task_dir, converted)
    return converted

def finalization_existing_pr_recovery_context(
    root: Path,
    plan: dict[str, Any],
    current_transaction: dict[str, Any] | None,
    state: str,
) -> tuple[str, dict[str, Any] | None]:
    """Classify recovery without overriding an owning reprepare decision."""
    if state == "reprepare_required":
        return state, None
    if current_transaction is None:
        candidate = resolve_closeout_pull_request(
            root,
            plan["git"]["repo"],
            plan["git"]["head_branch"],
            plan["git"]["base_branch"],
            plan["git"]["remote"],
        )
        if candidate is None:
            return state, None
        return "existing_pr_recovery", classify_existing_pr_recovery(
            root, plan, candidate
        )
    if current_transaction.get("mode") == "ordinary_publication":
        recovery = classify_unbound_equal_head_recovery(
            root,
            plan,
            current_transaction,
        )
        if recovery is None:
            return state, None
        return "existing_pr_recovery", recovery
    if current_transaction.get("mode") != "existing_pr_recovery":
        return state, None
    candidate, remote_head = finalization_pre_mutation_remote_preflight(
        root, plan, current_transaction
    )
    if candidate is None:
        raise WorkflowError(
            "Existing PR recovery transaction lost its bound PR.", exit_code=2
        )
    recovery = current_transaction["adopted_pr"]
    publication_head = str(current_transaction["publication_head"])
    metadata_comparison = {
        "live_title": candidate.get("title"),
        "live_body": candidate.get("body"),
        "title_matches": candidate.get("title") == plan["publish"]["title"],
        "body_matches": candidate.get("body") == plan["publish"]["body"],
    }
    return state, {
        "mode": "existing_pr_recovery",
        "pr": {"number": candidate["number"], "url": candidate["url"]},
        "initial_state": "draft" if recovery["initial_is_draft"] else "ready",
        "initial_is_draft": bool(recovery["initial_is_draft"]),
        "pre_push_remote_head": recovery["pre_push_remote_head"],
        "publication_head": publication_head,
        "ancestry": (
            "equal"
            if recovery["pre_push_remote_head"] == publication_head
            else "strict_ancestor"
        ),
        "push_required": remote_head != publication_head,
        "metadata_update_required": not (
            metadata_comparison["title_matches"]
            and metadata_comparison["body_matches"]
        ),
        "metadata_comparison": metadata_comparison,
        "ready_action": (
            "mark_ready" if recovery["initial_is_draft"] else "preserve_ready"
        ),
    }

def finalization_post_bind_existing_pr_recovery(
    transaction: dict[str, Any] | None,
    plan: dict[str, Any],
) -> bool:
    """Return whether one exact transaction owns the post-bind recovery stage."""
    if (
        not isinstance(transaction, dict)
        or transaction.get("mode") != "existing_pr_recovery"
        or transaction.get("next_transition")
        not in {"archive", "push_archive", "mark_ready"}
    ):
        return False
    finalization_validate_transaction_plan(transaction, plan)
    if not isinstance(transaction.get("pr"), dict) or not isinstance(
        transaction.get("adopted_pr"), dict
    ):
        raise WorkflowError(
            "Post-bind existing PR recovery transaction is incomplete.",
            exit_code=2,
        )
    return True

def finalizer_pre_pr_provenance_tail_applies(
    root: Path,
    plan: dict[str, Any],
    transaction: dict[str, Any] | None,
) -> bool:
    """Keep pre-PR provenance inference behind an exact post-bind transaction."""
    if finalization_post_bind_existing_pr_recovery(transaction, plan):
        return False
    return finalizer_pre_pr_provenance_tail_required(root, plan)

def finalization_pre_mutation_remote_preflight(
    root: Path,
    plan: dict[str, Any],
    transaction: dict[str, Any] | None,
    *,
    existing_pr_recovery: dict[str, Any] | None = None,
) -> tuple[dict[str, Any] | None, str]:
    """Require an unowned remote or the exact Finalizer-owned recovery state."""
    git = plan["git"]
    existing_pr = resolve_closeout_pull_request(
        root,
        git["repo"],
        git["head_branch"],
        git["base_branch"],
        git["remote"],
    )
    remote_head = closeout_remote_branch_head(root, plan)
    if transaction is None:
        if existing_pr_recovery is not None:
            current_recovery = classify_existing_pr_recovery(
                root, plan, existing_pr, remote_head
            )
            if current_recovery is None or current_recovery != existing_pr_recovery:
                raise WorkflowError(
                    "Existing PR recovery facts changed after semantic preview.",
                    exit_code=2,
                    payload={"reason_code": "existing_pr_recovery_drift"},
                )
            return existing_pr, remote_head
        reviewed_head = str(git["branch_review_commit"])
        remote_is_historical_baseline = bool(
            remote_head
            and remote_head != reviewed_head
            and is_ancestor(root, remote_head, reviewed_head)
        )
        if (
            existing_pr is not None
            or (remote_head and not remote_is_historical_baseline)
        ):
            raise WorkflowError(
                "Task finalization requires an unpublished branch and no Open PR before its first remote mutation.",
                exit_code=2,
                payload={
                    "reason_code": "pre_finalizer_remote_state_exists",
                    "remote_head": remote_head,
                    "pull_request": (
                        existing_pr.get("number") if existing_pr is not None else None
                    ),
                },
            )
        terminal_prs = resolve_closeout_terminal_pull_requests(
            root,
            git["repo"],
            git["head_branch"],
            git["base_branch"],
            git["remote"],
        )
        if terminal_prs:
            raise WorkflowError(
                "Task finalization found a Closed or Merged pull request for the immutable head/base before its first remote mutation.",
                exit_code=2,
                payload={
                    "reason_code": "pre_finalizer_terminal_pr_exists",
                    "pull_requests": terminal_prs,
                },
            )
        return None, remote_head

    identity_mismatches = [
        field
        for field, matches in (
            ("repo_ref", transaction.get("repo_ref") == git.get("repo")),
            ("base_branch", transaction.get("base_branch") == git.get("base_branch")),
            ("branch", transaction.get("branch") == git.get("head_branch")),
            (
                "branch_review_commit",
                transaction.get("branch_review_commit")
                == git.get("branch_review_commit"),
            ),
            (
                "publication_head",
                transaction.get("publication_head")
                == (git.get("publication_head") or git.get("branch_review_commit")),
            ),
        )
        if not matches
    ]
    if identity_mismatches:
        raise WorkflowError(
            "Task finalization owner transaction identity differs from the current plan: "
            + ", ".join(identity_mismatches),
            exit_code=2,
            payload={
                "reason_code": "finalizer_transaction_identity_drift",
                "mismatch_fields": identity_mismatches,
            },
        )
    allowed_heads = {
        str(transaction["branch_review_commit"]),
        str(transaction["publication_head"]),
    }
    if transaction.get("next_transition") == "push_content":
        allowed_heads.add(str(transaction.get("pre_push_remote_head") or ""))
    if remote_head not in allowed_heads:
        raise WorkflowError(
            "Task finalization remote branch drifted outside its owner transaction.",
            exit_code=2,
            payload={
                "reason_code": "finalizer_remote_head_drift",
                "remote_head": remote_head,
                "allowed_heads": sorted(allowed_heads),
            },
        )
    bound_pr = transaction.get("pr")
    recovery = transaction.get("adopted_pr")
    if existing_pr is None:
        if bound_pr is not None:
            raise WorkflowError(
                "Task finalization transaction-bound PR is no longer Open.",
                exit_code=2,
                payload={"reason_code": "finalizer_bound_pr_missing"},
            )
        return None, remote_head
    if not isinstance(bound_pr, dict):
        raise WorkflowError(
            "Task finalization found an Open PR before Finalizer bound it.",
            exit_code=2,
            payload={
                "reason_code": "pre_finalizer_pull_request_exists",
                "pull_request": existing_pr.get("number"),
            },
        )
    if transaction.get("mode") == "existing_pr_recovery":
        if not isinstance(recovery, dict) or (
            recovery.get("number") != bound_pr.get("number")
            or recovery.get("url") != bound_pr.get("url")
        ):
            raise WorkflowError(
                "Existing PR recovery transaction identity is incomplete.",
                exit_code=2,
                payload={"reason_code": "existing_pr_transaction_drift"},
            )
        if remote_head != existing_pr.get("headRefOid"):
            raise WorkflowError(
                "Existing PR recovery remote and PR HEADs diverged.",
                exit_code=2,
                payload={"reason_code": "existing_pr_remote_head_mismatch"},
            )
        validate_closeout_remote_pull_request_binding(
            plan,
            existing_pr,
            expected_draft=bool(recovery["initial_is_draft"]),
            expected_head=remote_head,
            bound_pr=bound_pr,
        )
        if (
            transaction.get("next_transition") == "bind_pr"
            and recovery.get("pre_push_remote_head")
            == transaction.get("publication_head")
        ):
            metadata_comparison = finalization_validate_recovery_metadata_decision(
                transaction["publication"],
                recovery.get("metadata_comparison"),
                recovery.get("metadata_update_required"),
            )
            live_metadata = {
                "title": existing_pr.get("title"),
                "body": existing_pr.get("body"),
            }
            original_metadata = {
                "title": metadata_comparison["live_title"],
                "body": metadata_comparison["live_body"],
            }
            converged_metadata = {
                "title": transaction["publication"]["title"],
                "body": transaction["publication"]["body"],
            }
            if live_metadata != original_metadata and not (
                recovery["metadata_update_required"]
                and live_metadata == converged_metadata
            ):
                raise WorkflowError(
                    "Equal-HEAD recovery PR metadata differs from both its original binding and exact Publication convergence.",
                    exit_code=2,
                    payload={"reason_code": "existing_pr_recovery_drift"},
                )
        if transaction.get("next_transition") not in {"push_content", "bind_pr"}:
            validate_closeout_remote_pull_request_identity(
                plan,
                existing_pr,
                expected_draft=bool(recovery["initial_is_draft"]),
                expected_head=remote_head,
                bound_pr=bound_pr,
            )
    else:
        validate_closeout_remote_pull_request_identity(
            plan,
            existing_pr,
            expected_draft=True,
            expected_head=remote_head,
            bound_pr=bound_pr,
        )
    return existing_pr, remote_head

def closeout_task_dir_from_plan(root: Path, plan: dict[str, Any]) -> Path:
    active = root / plan["task"]["active_locator"]
    archived = root / plan["task"]["archive_locator"]
    if active.is_dir() and not archived.exists():
        return active
    if archived.is_dir() and not active.exists():
        return archived
    raise WorkflowError(
        "Closeout PR identity requires exactly one active or archived task locator.",
        exit_code=2,
    )

def validate_closeout_remote_pull_request_binding(
    plan: dict[str, Any],
    pr: dict[str, Any],
    *,
    expected_draft: bool,
    expected_head: str | None = None,
    bound_pr: dict[str, Any] | None = None,
) -> None:
    expected_repo = normalize_github_repository(plan["git"]["repo"])
    actual_repo, is_target = closeout_pull_request_head_repository(pr, expected_repo)
    if not is_target or actual_repo != expected_repo:
        raise WorkflowError("Closeout pull request head repository differs from immutable readiness.", exit_code=2)
    number = pr.get("number")
    if not isinstance(number, int):
        raise WorkflowError("Closeout pull request number is invalid.", exit_code=2)
    canonical_url = canonical_pull_request_url(plan["git"]["repo"], number, pr.get("url"))
    if pr.get("url") != canonical_url:
        raise WorkflowError("Closeout pull request URL is not canonical.", exit_code=2)
    if (
        pr.get("headRefName") != plan["git"]["head_branch"]
        or pr.get("baseRefName") != plan["git"]["base_branch"]
    ):
        raise WorkflowError("Closeout pull request head/base differs from the immutable plan.", exit_code=2)
    if pr.get("isDraft") is not expected_draft:
        state = "draft" if expected_draft else "ready"
        raise WorkflowError(f"Closeout pull request is not in expected {state} state.", exit_code=2)
    if expected_head is not None and pr.get("headRefOid") != expected_head:
        raise WorkflowError("Closeout pull request HEAD differs from the expected immutable stage HEAD.", exit_code=2)
    if bound_pr is not None:
        bound_number = bound_pr.get("number")
        if not isinstance(bound_number, int):
            raise WorkflowError("Bound closeout pull request number is invalid.", exit_code=2)
        bound_url = canonical_pull_request_url(plan["git"]["repo"], bound_number, bound_pr.get("url"))
        if number != bound_number or canonical_url != bound_url:
            raise WorkflowError("Closeout pull request number/URL differs from the bound remote identity.", exit_code=2)

def validate_closeout_remote_pull_request_identity(
    plan: dict[str, Any],
    pr: dict[str, Any],
    *,
    expected_draft: bool,
    expected_head: str | None = None,
    bound_pr: dict[str, Any] | None = None,
) -> None:
    validate_closeout_remote_pull_request_binding(
        plan,
        pr,
        expected_draft=expected_draft,
        expected_head=expected_head,
        bound_pr=bound_pr,
    )
    if pr.get("title") != plan["publish"]["title"]:
        raise WorkflowError("Closeout pull request title differs from immutable readiness.", exit_code=2)
    body = pr.get("body")
    if not isinstance(body, str):
        raise WorkflowError("Closeout pull request body identity is invalid.", exit_code=2)
    if body != plan["publish"]["body"]:
        raise WorkflowError("Closeout pull request body differs from immutable readiness.", exit_code=2)

def closeout_immutable_pr_body(plan: dict[str, Any]) -> str:
    body = plan.get("publish", {}).get("body")
    if not isinstance(body, str) or not body:
        raise WorkflowError("Closeout immutable plan PR body is missing.", exit_code=2)
    return body

def validate_closeout_pull_request_identity(
    root: Path,
    task_dir: Path,
    plan: dict[str, Any],
    pr: dict[str, Any],
    *,
    expected_draft: bool,
    require_summary: bool,
    expected_head: str | None = None,
    bound_pr: dict[str, Any] | None = None,
) -> None:
    validate_closeout_remote_pull_request_identity(
        plan,
        pr,
        expected_draft=expected_draft,
        expected_head=expected_head,
        bound_pr=bound_pr,
    )
    number = pr["number"]
    canonical_url = canonical_pull_request_url(plan["git"]["repo"], number, pr.get("url"))

    expected_body = closeout_immutable_pr_body(plan)
    if pr.get("body") != expected_body:
        raise WorkflowError("Closeout pull request body differs from immutable readiness.", exit_code=2)

    summary_path = task_dir / FINISH_SUMMARY_ARTIFACT
    if require_summary and not summary_path.is_file():
        raise WorkflowError("Closeout final summary is missing for PR identity validation.", exit_code=2)
    if summary_path.is_file():
        summary = read_and_validate_closeout_final_summary(summary_path, plan)
        expected_ref = f"PR #{number}"
        if (
            summary.get("github", {}).get("pr_url") != canonical_url
            or summary.get("index", {}).get("search_terms", {}).get("pr_refs") != [expected_ref]
        ):
            raise WorkflowError(
                "Closeout final summary does not reference the same immutable pull request.",
                exit_code=2,
            )

def ensure_closeout_draft_pr(root: Path, plan: dict[str, Any], body: str) -> dict[str, Any]:
    git = plan["git"]
    task_dir = closeout_task_dir_from_plan(root, plan)
    expected_body = closeout_immutable_pr_body(plan)
    if body != expected_body:
        raise WorkflowError("Closeout requested PR body differs from the immutable plan.", exit_code=2)
    existing = resolve_closeout_pull_request(
        root, git["repo"], git["head_branch"], git["base_branch"], git["remote"]
    )
    if existing is not None:
        expected_head = current_head(root)
        validate_closeout_remote_pull_request_binding(
            plan,
            existing,
            expected_draft=True,
            expected_head=expected_head,
        )
        if (
            existing.get("title") != plan["publish"]["title"]
            or existing.get("body") != expected_body
        ):
            update_pull_request_metadata(
                root,
                git["repo"],
                existing["number"],
                plan["publish"]["title"],
                expected_body,
            )
            rebound = resolve_closeout_pull_request(
                root,
                git["repo"],
                git["head_branch"],
                git["base_branch"],
                git["remote"],
            )
            if rebound is None:
                raise WorkflowError(
                    "Updated draft PR could not be rebound to one immutable identity.",
                    exit_code=2,
                )
            validate_closeout_pull_request_identity(
                root,
                task_dir,
                plan,
                rebound,
                expected_draft=True,
                require_summary=False,
                expected_head=expected_head,
                bound_pr=existing,
            )
            return rebound
        validate_closeout_pull_request_identity(
            root,
            task_dir,
            plan,
            existing,
            expected_draft=True,
            require_summary=False,
            expected_head=expected_head,
        )
        return existing
    pr_url = create_pull_request(
        root, git["repo"], git["base_branch"], git["head_branch"],
        plan["publish"]["title"], body, True,
    )
    number = parse_pull_request_number(pr_url)
    if number is None:
        raise WorkflowError("Could not parse draft PR identity.", exit_code=2)
    created = resolve_closeout_pull_request(
        root, git["repo"], git["head_branch"], git["base_branch"], git["remote"]
    )
    if created is None or created.get("number") != number:
        raise WorkflowError("Created draft PR could not be rebound to one immutable identity.", exit_code=2)
    validate_closeout_pull_request_identity(
        root,
        task_dir,
        plan,
        created,
        expected_draft=True,
        require_summary=False,
        expected_head=current_head(root),
    )
    return created

def ensure_closeout_bound_pr(
    root: Path,
    plan: dict[str, Any],
    body: str,
    transaction: dict[str, Any] | None,
) -> dict[str, Any]:
    if not isinstance(transaction, dict) or transaction.get("mode") != "existing_pr_recovery":
        return ensure_closeout_draft_pr(root, plan, body)
    recovery = transaction.get("adopted_pr")
    bound_pr = transaction.get("pr")
    if not isinstance(recovery, dict) or not isinstance(bound_pr, dict):
        raise WorkflowError("Existing PR recovery transaction is incomplete.", exit_code=2)
    git = plan["git"]
    existing = resolve_closeout_pull_request(
        root, git["repo"], git["head_branch"], git["base_branch"], git["remote"]
    )
    if existing is None:
        raise WorkflowError(
            "Existing PR recovery candidate is no longer Open.",
            exit_code=2,
            payload={"reason_code": "finalizer_bound_pr_missing"},
        )
    expected_head = current_head(root)
    validate_closeout_remote_pull_request_binding(
        plan,
        existing,
        expected_draft=bool(recovery["initial_is_draft"]),
        expected_head=expected_head,
        bound_pr=bound_pr,
    )
    if (
        existing.get("title") != plan["publish"]["title"]
        or existing.get("body") != body
    ):
        update_pull_request_metadata(
            root,
            git["repo"],
            existing["number"],
            plan["publish"]["title"],
            body,
        )
        rebound = resolve_closeout_pull_request(
            root, git["repo"], git["head_branch"], git["base_branch"], git["remote"]
        )
        if rebound is None:
            raise WorkflowError("Updated recovery PR could not be rebound.", exit_code=2)
        existing = rebound
    validate_closeout_pull_request_identity(
        root,
        closeout_task_dir_from_plan(root, plan),
        plan,
        existing,
        expected_draft=bool(recovery["initial_is_draft"]),
        require_summary=False,
        expected_head=expected_head,
        bound_pr=bound_pr,
    )
    return existing


def finalization_expected_pr_draft_state(
    transaction: dict[str, Any] | None,
    *,
    current_finalizer: bool,
) -> bool:
    if (
        current_finalizer
        and isinstance(transaction, dict)
        and transaction.get("mode") == "existing_pr_recovery"
    ):
        recovery = transaction.get("adopted_pr")
        if not isinstance(recovery, dict) or not isinstance(
            recovery.get("initial_is_draft"), bool
        ):
            raise WorkflowError(
                "Existing PR recovery transaction is missing its initial Draft/Ready state.",
                exit_code=2,
            )
        return bool(recovery["initial_is_draft"])
    return True


def build_final_archive_projection(
    root: Path,
    task_dir: Path,
    prepared: dict[str, Any],
    pr: dict[str, Any],
    *,
    expected_draft: bool = True,
) -> tuple[Path, dict[str, Any]]:
    plan = prepared["plan"]
    branch_review_commit = str(plan["git"]["branch_review_commit"])
    anchor_identity = reviewed_content_identity(
        root,
        branch_review_commit,
        include_worktree=False,
    )["sha256"]
    continuity_errors = review_branch_content_continuity_errors(
        root,
        task_dir,
        branch_review_commit,
        anchor_identity,
        current_head(root),
    )
    if continuity_errors:
        raise WorkflowError(
            "Final projection content changed after Publication review.",
            exit_code=2,
            payload={"errors": continuity_errors},
        )
    validate_closeout_pull_request_identity(
        root,
        task_dir,
        plan,
        pr,
        expected_draft=expected_draft,
        require_summary=False,
        expected_head=current_head(root),
    )
    summary = closeout_summary_for_pr(plan, pr)
    if summary["index"]["search_terms"]["pr_refs"] != [f"PR #{pr['number']}"]:
        raise WorkflowError("Final projection must contain one canonical PR ref.", exit_code=2)
    required_artifacts = set(summary["artifacts"].values())
    missing = sorted(name for name in required_artifacts if not (task_dir / name).is_file())
    if missing:
        raise WorkflowError("Final archive projection is missing task artifacts.", exit_code=2, payload={"missing": missing})
    validate_closeout_final_summary(plan, summary)
    path = task_dir / FINISH_SUMMARY_ARTIFACT
    write_json(path, summary)
    read_and_validate_closeout_final_summary(path, plan)
    return path, summary

def closeout_commit_paths(root: Path, commit: str) -> set[str]:
    return set(
        run_stdout(
            ["git", "diff-tree", "--no-commit-id", "--name-only", "--no-renames", "-r", commit],
            cwd=root,
        ).splitlines()
    )

def closeout_archive_transaction_paths(plan: dict[str, Any]) -> set[str]:
    projection = plan["projection"]
    active = plan["task"]["active_locator"]
    archived = plan["task"]["archive_locator"]
    return {
        *(f"{active}/{path}" for path in projection["tracked_move_paths"]),
        *(f"{archived}/{path}" for path in closeout_archive_retained_paths(plan)),
    }

def validate_closeout_archive_git_paths(
    paths: set[str], plan: dict[str, Any], *, stage: str
) -> None:
    expected = closeout_archive_transaction_paths(plan)
    if paths != expected:
        raise WorkflowError(
            f"Closeout {stage} paths do not equal the immutable tracked/untracked archive transaction.",
            exit_code=2,
            payload={
                "stage": stage,
                "expected_paths": sorted(expected),
                "actual_paths": sorted(paths),
                "missing_paths": sorted(expected - paths),
                "extra_paths": sorted(paths - expected),
            },
        )

def closeout_commit_parent(root: Path, commit: str) -> str:
    return run_stdout(["git", "rev-parse", f"{commit}^"], cwd=root)

def closeout_commit_tracked_task_paths(
    root: Path, commit: str, active_locator: str
) -> set[str]:
    return set(
        run_stdout(
            ["git", "ls-tree", "-r", "--name-only", commit, "--", active_locator],
            cwd=root,
        ).splitlines()
    )

def validate_closeout_active_projection(
    root: Path,
    task_dir: Path,
    plan: dict[str, Any],
) -> None:
    if repo_relative(root, task_dir) != plan["task"]["active_locator"] or not task_dir.is_dir():
        raise WorkflowError("Closeout active projection locator is invalid.", exit_code=2)
    actual_files = sorted(path.relative_to(task_dir).as_posix() for path in task_dir.rglob("*") if path.is_file())
    expected_files = plan["projection"]["move_paths"]
    if actual_files != expected_files:
        raise WorkflowError(
            "Closeout active projection does not match the complete planned move set.",
            exit_code=2,
            payload={"expected_files": expected_files, "actual_files": actual_files},
        )
    read_and_validate_closeout_final_summary(task_dir / FINISH_SUMMARY_ARTIFACT, plan)

def closeout_commit_tree_entry(root: Path, commit: str, path: str) -> tuple[str, str, str]:
    proc = run(["git", "ls-tree", commit, "--", path], cwd=root, check=False)
    rows = [line for line in proc.stdout.splitlines() if line]
    if proc.returncode != 0 or len(rows) != 1:
        raise WorkflowError(
            "Closeout transaction parent is missing one exact tracked move path.",
            exit_code=2,
            payload={"commit": commit, "path": path, "stage": "pre-archive-continuity"},
        )
    metadata, separator, actual_path = rows[0].partition("\t")
    fields = metadata.split()
    if separator != "\t" or actual_path != path or len(fields) != 3:
        raise WorkflowError(
            "Closeout evidence tree entry is ambiguous.",
            exit_code=2,
            payload={"commit": commit, "path": path, "stage": "pre-archive-continuity"},
        )
    return fields[0], fields[1], fields[2]

def closeout_untracked_paths(root: Path) -> set[str]:
    proc = run(
        ["git", "ls-files", "--others", "--exclude-standard", "-z"],
        cwd=root,
        check=False,
    )
    if proc.returncode != 0:
        raise WorkflowError("Could not enumerate pre-archive untracked paths.", exit_code=2)
    return {path for path in proc.stdout.split("\0") if path}

def closeout_projection_content_is_current(
    plan: dict[str, Any],
    relative: str,
    content: bytes,
    mode: str | None = None,
) -> bool:
    projection = plan.get("projection", {})
    if "reviewed_tracked_bindings" in projection:
        binding = closeout_reviewed_tracked_binding_map(plan).get(relative)
        return bool(
            binding is not None
            and mode == binding.get("mode")
            and hashlib.sha256(content).hexdigest() == binding.get("sha256")
        )
    input_key = {"task.json": "task"}.get(relative)
    if input_key is None:
        return False
    record = plan.get("inputs", {}).get(input_key)
    if not isinstance(record, dict):
        return False
    actual = hashlib.sha256(content).hexdigest()
    return actual == record.get("sha256")

def validate_closeout_pre_move_continuity(
    root: Path,
    task_dir: Path,
    plan: dict[str, Any],
    transaction_parent: str,
    *,
    expected_summary_pr: dict[str, Any] | None = None,
) -> None:
    """Validate every local archive input before official task.py can mutate it."""
    assert_closeout_archive_month_current(plan)
    hook_state = official_after_archive_hook_state(root)
    hook_input = plan.get("inputs", {}).get("official_after_archive_hooks")
    if (
        not isinstance(hook_input, dict)
        or hook_input.get("path") != ".trellis/config.yaml"
        or hook_input.get("sha256") != canonical_json_sha256(hook_state)
    ):
        raise WorkflowError(
            "Official after_archive hook state drifted from the immutable finalization plan.",
            exit_code=2,
            payload={"stage": "after-archive-hook-preflight", "hook_executed": False},
        )

    active_locator = plan["task"]["active_locator"]
    for relative in plan["projection"]["move_paths"]:
        target = task_dir / relative
        try:
            working_mode = os.lstat(target).st_mode
        except OSError as exc:
            raise WorkflowError(
                "Closeout pre-archive move path is missing or unreadable.",
                exit_code=2,
                payload={"path": relative, "stage": "pre-archive-continuity"},
            ) from exc
        if not stat.S_ISREG(working_mode):
            raise WorkflowError(
                "Closeout pre-archive move paths must be regular files; symlinks and special modes are rejected.",
                exit_code=2,
                payload={"path": relative, "stage": "pre-archive-continuity"},
            )

    closeout_summary_runtime_pr_facts_from_bytes(
        plan,
        (task_dir / FINISH_SUMMARY_ARTIFACT).read_bytes(),
        expected_pr=expected_summary_pr,
    )

    binding_map = closeout_reviewed_tracked_binding_map(plan)
    observed_binding_paths: set[str] = set()
    for relative in plan["projection"]["tracked_move_paths"]:
        repo_path = f"{active_locator}/{relative}"
        git_mode, object_type, _object_id = closeout_commit_tree_entry(
            root, transaction_parent, repo_path
        )
        if object_type != "blob" or git_mode not in {"100644", "100755"}:
            raise WorkflowError(
                "Closeout tracked move paths must be regular Git blobs, not symlinks, submodules, or special modes.",
                exit_code=2,
                payload={
                    "path": relative,
                    "git_mode": git_mode,
                    "object_type": object_type,
                    "stage": "pre-archive-continuity",
                },
            )
        target = task_dir / relative
        working_mode = os.lstat(target).st_mode
        expected_working_mode = "100755" if working_mode & 0o111 else "100644"
        before = closeout_commit_blob_bytes(root, transaction_parent, repo_path)
        current_bytes = target.read_bytes()
        differs_from_parent = (
            current_bytes != before or expected_working_mode != git_mode
        )
        binding = binding_map.get(relative)
        if binding is not None:
            observed_binding_paths.add(relative)
        if (
            (binding is not None or differs_from_parent)
            and not closeout_projection_content_is_current(
                plan,
                relative,
                current_bytes,
                expected_working_mode,
            )
        ):
            raise WorkflowError(
                "Closeout tracked output differs from its transaction-parent blob and reviewed binding before archive.",
                exit_code=2,
                payload={
                    "path": relative,
                    "expected_mode": git_mode,
                    "actual_mode": expected_working_mode,
                    "stage": "pre-archive-continuity",
                },
            )
    expected_binding_paths = set(binding_map)
    if observed_binding_paths != expected_binding_paths:
        raise WorkflowError(
            "Closeout reviewed tracked bindings do not exactly cover the metadata tail.",
            exit_code=2,
            payload={
                "expected_paths": sorted(expected_binding_paths),
                "actual_paths": sorted(observed_binding_paths),
                "stage": "pre-archive-continuity",
            },
        )

    expected_outputs = {
        f"{active_locator}/{relative}"
        for relative in plan["projection"]["untracked_archive_outputs"]
    }
    dirty = set(git_status_paths(root))
    staged = set(
        run_stdout(
            ["git", "diff", "--cached", "--name-only", "--no-renames"], cwd=root
        ).splitlines()
    )
    untracked = closeout_untracked_paths(root)
    allowed_dirty = {
        f"{active_locator}/{relative}"
        for relative in plan["projection"]["move_paths"]
    }
    dirty_is_valid = dirty.issubset(allowed_dirty)
    if not dirty_is_valid or staged or untracked != expected_outputs:
        raise WorkflowError(
            "Closeout pre-archive dirty/staged/untracked paths do not match the immutable final outputs.",
            exit_code=2,
            payload={
                "stage": "pre-archive-continuity",
                "next_transition": "archive-move",
                "expected_paths": sorted(expected_outputs),
                "dirty_paths": sorted(dirty),
                "staged_paths": sorted(staged),
                "untracked_paths": sorted(untracked),
            },
        )

def compact_closeout_archive(archived: Path, plan: dict[str, Any]) -> None:
    """Remove task-local intermediates that have no long-term archive consumer."""
    parents: set[Path] = set()
    for relative in closeout_archive_pruned_paths(plan):
        target = archived / relative
        try:
            mode = os.lstat(target).st_mode
        except FileNotFoundError:
            continue
        except OSError as exc:
            raise WorkflowError(
                "Compact archive artifact could not be inspected.",
                exit_code=2,
                payload={"path": relative, "stage": "archive-compaction"},
            ) from exc
        if not stat.S_ISREG(mode):
            raise WorkflowError(
                "Compact archive may remove only regular task-local files.",
                exit_code=2,
                payload={"path": relative, "stage": "archive-compaction"},
            )
        target.unlink()
        parents.update(target.parents)
    for parent in sorted(
        (path for path in parents if path != archived and archived in path.parents),
        key=lambda path: len(path.parts),
        reverse=True,
    ):
        try:
            parent.rmdir()
        except OSError:
            pass

def validate_closeout_archive_move_layout(root: Path, archived: Path, plan: dict[str, Any]) -> None:
    active = root / plan["task"]["active_locator"]
    expected_archived = root / plan["task"]["archive_locator"]
    if (
        active.exists()
        or closeout_lexical_path(archived) != closeout_lexical_path(expected_archived)
        or archived.is_symlink()
        or not archived.is_dir()
    ):
        raise WorkflowError(
            "Archived closeout must have no active locator and one complete planned archive locator.",
            exit_code=2,
        )
    actual_files = sorted(path.relative_to(archived).as_posix() for path in archived.rglob("*") if path.is_file())
    expected_files = closeout_archive_retained_paths(plan)
    if actual_files != expected_files:
        raise WorkflowError(
            "Archived closeout files do not match the complete prevalidated move set.",
            exit_code=2,
            payload={"expected_files": expected_files, "actual_files": actual_files},
        )

def closeout_commit_blob_bytes(root: Path, commit: str, path: str) -> bytes:
    proc = subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        raise WorkflowError(
            "Closeout could not read an immutable Git blob.",
            exit_code=2,
            payload={"commit": commit, "path": path},
        )
    return proc.stdout

def closeout_optional_commit_blob_bytes(root: Path, commit: str, path: str) -> bytes | None:
    proc = subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    return proc.stdout if proc.returncode == 0 else None

def validate_closeout_task_json_archive_change(before: bytes, after: bytes) -> None:
    try:
        before_payload = json.loads(before.decode("utf-8"))
        after_payload = json.loads(after.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise WorkflowError("Closeout task.json archive blobs are invalid JSON.", exit_code=2) from exc
    if not isinstance(before_payload, dict) or not isinstance(after_payload, dict):
        raise WorkflowError("Closeout task.json archive blobs must be objects.", exit_code=2)
    expected = copy.deepcopy(before_payload)
    expected["status"] = "completed"
    completed_at = after_payload.get("completedAt")
    if not isinstance(completed_at, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", completed_at):
        raise WorkflowError("Archived task.json completedAt is not an official date value.", exit_code=2)
    expected["completedAt"] = completed_at
    if after_payload != expected:
        raise WorkflowError(
            "Archived task.json contains changes beyond the official status/completedAt transition.",
            exit_code=2,
        )

def closeout_task_json_reviewed_pre_move_bytes(
    transaction_parent: bytes,
    archived: bytes,
) -> bytes:
    """Reverse only the two fields that official task archive overwrites."""
    try:
        parent_payload = json.loads(transaction_parent.decode("utf-8"))
        archived_payload = json.loads(archived.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise WorkflowError("Closeout task.json archive blobs are invalid JSON.", exit_code=2) from exc
    if not isinstance(parent_payload, dict) or not isinstance(archived_payload, dict):
        raise WorkflowError("Closeout task.json archive blobs must be objects.", exit_code=2)

    reviewed_payload = copy.deepcopy(archived_payload)
    for field in ("status", "completedAt"):
        if field in parent_payload:
            reviewed_payload[field] = parent_payload[field]
        else:
            reviewed_payload.pop(field, None)
    # Official task_store.write_json uses this exact encoding without a trailing newline.
    return json.dumps(reviewed_payload, indent=2, ensure_ascii=False).encode("utf-8")

def validate_closeout_archive_blob_continuity(
    root: Path,
    archived: Path,
    plan: dict[str, Any],
    transaction_parent: str,
    *,
    archive_commit: str | None = None,
    expected_summary_pr: dict[str, Any] | None = None,
) -> dict[str, Any]:
    active_locator = plan["task"]["active_locator"]
    archive_locator = plan["task"]["archive_locator"]
    retained_paths = set(closeout_archive_retained_paths(plan))
    for relative in plan["projection"]["tracked_move_paths"]:
        if relative not in retained_paths:
            if archive_commit is None:
                if (archived / relative).exists():
                    raise WorkflowError(
                        "Pruned closeout artifact remains in the compact archive.",
                        exit_code=2,
                        payload={"path": relative},
                    )
            elif closeout_optional_commit_blob_bytes(
                root, archive_commit, f"{archive_locator}/{relative}"
            ) is not None:
                raise WorkflowError(
                    "Pruned closeout artifact remains in the committed compact archive.",
                    exit_code=2,
                    payload={"path": relative},
                )
            continue
        before = closeout_commit_blob_bytes(
            root,
            transaction_parent,
            f"{active_locator}/{relative}",
        )
        parent_mode, parent_type, _parent_oid = closeout_commit_tree_entry(
            root,
            transaction_parent,
            f"{active_locator}/{relative}",
        )
        if parent_type != "blob" or parent_mode not in {"100644", "100755"}:
            raise WorkflowError(
                "Archived tracked output parent is not a regular Git blob.",
                exit_code=2,
                payload={"path": relative},
            )
        if archive_commit is None:
            target = archived / relative
            if not target.is_file():
                raise WorkflowError(
                    "Archived tracked output is missing during content validation.",
                    exit_code=2,
                    payload={"path": relative},
                )
            after = target.read_bytes()
            working_mode = os.lstat(target).st_mode
            after_mode = "100755" if working_mode & 0o111 else "100644"
        else:
            archive_path = f"{archive_locator}/{relative}"
            after = closeout_commit_blob_bytes(root, archive_commit, archive_path)
            after_mode, after_type, _after_oid = closeout_commit_tree_entry(
                root,
                archive_commit,
                archive_path,
            )
            if after_type != "blob" or after_mode not in {"100644", "100755"}:
                raise WorkflowError(
                    "Archived tracked output is not a regular Git blob.",
                    exit_code=2,
                    payload={"path": relative},
                )
        if relative == "task.json":
            binding = closeout_reviewed_tracked_binding_map(plan).get(relative)
            reviewed_before = before
            if binding is not None:
                reviewed_before = closeout_task_json_reviewed_pre_move_bytes(before, after)
                if hashlib.sha256(reviewed_before).hexdigest() != binding.get("sha256"):
                    raise WorkflowError(
                        "Archived task.json does not derive from its reviewed pre-move binding.",
                        exit_code=2,
                        payload={"path": relative},
                    )
            validate_closeout_task_json_archive_change(reviewed_before, after)
            expected_mode = binding.get("mode") if binding is not None else parent_mode
            if after_mode != expected_mode:
                raise WorkflowError(
                    "Archived task.json mode differs from its reviewed pre-move mode.",
                    exit_code=2,
                    payload={"path": relative},
                )
        elif (
            (before != after or parent_mode != after_mode)
            and not closeout_projection_content_is_current(
                plan,
                relative,
                after,
                after_mode,
            )
        ):
            raise WorkflowError(
                "Archived tracked output differs from its transaction-parent blob and reviewed binding.",
                exit_code=2,
                payload={"path": relative},
            )
    if archive_commit is None:
        summary_path = archived / FINISH_SUMMARY_ARTIFACT
        try:
            summary_bytes = summary_path.read_bytes()
        except OSError as exc:
            raise WorkflowError("Archived final summary is missing during continuity validation.", exit_code=2) from exc
    else:
        summary_bytes = closeout_commit_blob_bytes(
            root,
            archive_commit,
            f"{archive_locator}/{FINISH_SUMMARY_ARTIFACT}",
        )
    return closeout_summary_runtime_pr_facts_from_bytes(
        plan,
        summary_bytes,
        expected_pr=expected_summary_pr,
    )

def validate_closeout_archive_commit_tree(
    root: Path, plan: dict[str, Any], archive_commit: str
) -> None:
    active_locator = plan["task"]["active_locator"]
    archive_locator = plan["task"]["archive_locator"]
    active_paths = closeout_commit_tracked_task_paths(root, archive_commit, active_locator)
    archived_paths = closeout_commit_tracked_task_paths(root, archive_commit, archive_locator)
    expected_archived_paths = {
        f"{archive_locator}/{relative}"
        for relative in closeout_archive_retained_paths(plan)
    }
    if active_paths or archived_paths != expected_archived_paths:
        raise WorkflowError(
            "Closeout archive commit tree does not contain the exact completed task move.",
            exit_code=2,
            payload={
                "commit": archive_commit,
                "unexpected_active_paths": sorted(active_paths),
                "expected_archive_paths": sorted(expected_archived_paths),
                "actual_archive_paths": sorted(archived_paths),
            },
        )

def resolve_committed_closeout_archive_transaction(
    root: Path, plan: dict[str, Any]
) -> dict[str, Any] | None:
    archive_commit = current_head(root)
    committed_paths = closeout_commit_paths(root, archive_commit)
    if committed_paths != closeout_archive_transaction_paths(plan):
        return None
    validate_closeout_archive_git_paths(committed_paths, plan, stage="archive-committed-head")
    transaction_parent = closeout_commit_parent(root, archive_commit)
    try:
        validate_closeout_reviewed_content(
            root,
            plan,
            transaction_parent,
            include_worktree=False,
        )
        validate_closeout_reviewed_content(
            root,
            plan,
            archive_commit,
            include_worktree=False,
        )
    except WorkflowError:
        return None
    validate_closeout_archive_commit_tree(root, plan, archive_commit)
    summary_pr = validate_closeout_archive_blob_continuity(
        root,
        root / plan["task"]["archive_locator"],
        plan,
        transaction_parent,
        archive_commit=archive_commit,
    )
    return {
        "commit": archive_commit,
        "parent": transaction_parent,
        "paths": sorted(committed_paths),
        "summary_pr": summary_pr,
    }

def assert_archived_current_transaction_boundary(
    root: Path,
    config: dict[str, Any],
    task_dir: Path,
    transaction: dict[str, Any],
    expected_plan_digest: str,
) -> dict[str, Any]:
    archive_locator = repo_relative(root, task_dir)
    active_locator = str(transaction["task_ref"])
    if (
        transaction.get("plan_digest") != expected_plan_digest
        or Path(active_locator).name != task_dir.name
        or not task_dir_is_archived(root, task_dir)
        or (root / active_locator).exists()
    ):
        raise WorkflowError(
            "Archived finalization transaction identity is stale.",
            exit_code=2,
        )
    archive_head = current_head(root)
    if closeout_commit_parent(root, archive_head) != transaction["publication_head"]:
        raise WorkflowError(
            "Archived finalization transaction is not the exact publication child.",
            exit_code=2,
        )
    try:
        task = json.loads(
            closeout_commit_blob_bytes(
                root,
                archive_head,
                f"{archive_locator}/task.json",
            ).decode("utf-8")
        )
        summary = json.loads(
            closeout_commit_blob_bytes(
                root,
                archive_head,
                f"{archive_locator}/{FINISH_SUMMARY_ARTIFACT}",
            ).decode("utf-8")
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise WorkflowError(
            "Archived finalization committed evidence is invalid.",
            exit_code=2,
        ) from exc
    if not isinstance(task, dict) or task.get("status") != "completed" or not isinstance(summary, dict):
        raise WorkflowError(
            "Archived finalization transaction is missing durable task evidence.",
            exit_code=2,
        )
    summary_task = summary.get("task") if isinstance(summary.get("task"), dict) else {}
    summary_git = summary.get("git") if isinstance(summary.get("git"), dict) else {}
    summary_github = summary.get("github") if isinstance(summary.get("github"), dict) else {}
    if (
        summary_task.get("artifact_dir") != active_locator
        or summary_task.get("archive_dir") != archive_locator
        or summary_git.get("branch") != transaction.get("branch")
        or summary_git.get("base_branch") != transaction.get("base_branch")
        or current_branch(root) != transaction.get("branch")
    ):
        raise WorkflowError(
            "Archived finalization summary does not match the transaction.",
            exit_code=2,
        )
    configured_repo = normalize_github_repository(config.get("github_repo"))
    if configured_repo and configured_repo != transaction.get("repo_ref"):
        raise WorkflowError(
            "Archived finalization repository does not match configuration.",
            exit_code=2,
        )
    remote = str(publish_config(config).get("remote") or "origin")
    validate_github_remote_repository(root, remote, str(transaction["repo_ref"]))
    pr_url = summary_github.get("pr_url")
    canonical_url, pr_number = parse_canonical_pull_request_url(
        str(transaction["repo_ref"]),
        pr_url,
    )
    plan = {
        "plan_digest": transaction["plan_digest"],
        "task": {
            "active_locator": active_locator,
            "archive_locator": archive_locator,
        },
        "git": {
            "repo": transaction["repo_ref"],
            "remote": remote,
            "base_branch": transaction["base_branch"],
            "head_branch": transaction["branch"],
            "branch_review_commit": transaction["branch_review_commit"],
            "reviewed_content_head": transaction["branch_review_commit"],
            "publication_head": transaction["publication_head"],
        },
        "review": {
            "changed_paths": [],
        },
        "publish": {
            "title": transaction["publication"]["title"],
            "body": transaction["publication"]["body"],
            "draft": True,
            "draft_to_ready": True,
            "match": {
                "repo": transaction["repo_ref"],
                "head": transaction["branch"],
                "base": transaction["base_branch"],
            },
        },
    }
    archive_commit = {
        "commit": archive_head,
        "parent": transaction["publication_head"],
        "paths": sorted(closeout_commit_paths(root, archive_head)),
        "summary_pr": {"number": pr_number, "url": canonical_url},
    }
    return {"plan": plan, "archive_commit": archive_commit}

def restore_current_archive_move_for_reentry(
    root: Path,
    archived: Path,
    transaction: dict[str, Any],
) -> Path:
    active = root / str(transaction["task_ref"])
    if (
        current_head(root) != transaction["publication_head"]
        or active.exists()
        or not archived.is_dir()
        or archived.is_symlink()
    ):
        raise WorkflowError(
            "Current archive-move recovery identity is invalid.",
            exit_code=2,
        )
    run_stdout(["git", "reset", "--mixed", "--quiet", "HEAD"], cwd=root)
    active.parent.mkdir(parents=True, exist_ok=True)
    archived.rename(active)
    run_stdout(
        [
            "git",
            "restore",
            f"--source={transaction['publication_head']}",
            "--worktree",
            "--",
            str(transaction["task_ref"]),
        ],
        cwd=root,
    )
    task_path = active / "task.json"
    if not task_path.is_file() or task_path.is_symlink():
        raise WorkflowError(
            "Current archive-move recovery is missing task identity.",
            exit_code=2,
        )
    task = read_json(task_path)
    if task.get("status") not in {"in_progress", "completed"}:
        raise WorkflowError(
            "Current archive-move recovery requires completed move metadata.",
            exit_code=2,
        )
    if task.get("status") == "completed":
        task["status"] = "in_progress"
        task.pop("completedAt", None)
        write_json(task_path, task)
    return active

def execute_archive_metadata_transaction(
    root: Path,
    task_dir: Path,
    plan: dict[str, Any],
    *,
    bound_pr: dict[str, Any] | None = None,
) -> tuple[Path, dict[str, Any]]:
    archive_script = root / ".trellis/scripts/task.py"
    if not archive_script.is_file():
        raise WorkflowError(f"Trellis task.py not found: {archive_script}")
    transaction_parent = current_head(root)
    validate_closeout_reviewed_content(
        root,
        plan,
        transaction_parent,
        include_worktree=True,
    )
    validate_closeout_active_projection(
        root,
        task_dir,
        plan,
    )
    assert_closeout_archive_path_preflight(root, plan["task"]["archive_locator"])
    validate_closeout_pre_move_continuity(
        root,
        task_dir,
        plan,
        transaction_parent,
        expected_summary_pr=bound_pr,
    )
    proc = run(
        [sys.executable, "./.trellis/scripts/task.py", "archive", task_dir.name, "--no-commit"],
        cwd=root,
        check=False,
    )
    if proc.returncode != 0:
        raise WorkflowError("task.py archive move failed.", exit_code=2, payload={"stderr": proc.stderr.strip(), "stdout": proc.stdout.strip()})
    archived = root / plan["task"]["archive_locator"]
    compact_closeout_archive(archived, plan)
    validate_closeout_archive_move_layout(root, archived, plan)
    validate_closeout_archive_blob_continuity(
        root,
        archived,
        plan,
        transaction_parent,
        expected_summary_pr=bound_pr,
    )
    active_locator = plan["task"]["active_locator"]
    archive_locator = plan["task"]["archive_locator"]
    dirty = set(git_status_paths(root))
    validate_closeout_archive_git_paths(dirty, plan, stage="archive-move-dirty")
    run_stdout(["git", "add", "-A", "--", active_locator, archive_locator], cwd=root)
    staged = set(run_stdout(["git", "diff", "--cached", "--name-only", "--no-renames"], cwd=root).splitlines())
    validate_closeout_archive_git_paths(staged, plan, stage="archive-staged")
    run_stdout(["git", "commit", "-m", format_metadata_commit_subject()], cwd=root)
    archive_commit = current_head(root)
    committed = closeout_commit_paths(root, archive_commit)
    validate_closeout_archive_git_paths(committed, plan, stage="archive-commit")
    if committed != staged:
        raise WorkflowError("Archive metadata commit differs from its staged transaction.", exit_code=2, payload={"staged": sorted(staged), "committed": sorted(committed)})
    if closeout_commit_parent(root, archive_commit) != transaction_parent:
        raise WorkflowError("Archive metadata commit parent is not the validated transaction parent.", exit_code=2)
    validate_closeout_archive_blob_continuity(
        root,
        archived,
        plan,
        transaction_parent,
        archive_commit=archive_commit,
        expected_summary_pr=bound_pr,
    )
    if git_status_paths(root):
        raise WorkflowError("Archive metadata commit left repository paths dirty.", exit_code=2)
    run_stdout(["git", "push", plan["git"]["remote"], plan["git"]["head_branch"]], cwd=root)
    return archived, {"commit": archive_commit, "parent": transaction_parent, "paths": sorted(committed)}

def ensure_closeout_pr_ready(
    root: Path, plan: dict[str, Any], *, bound_pr: dict[str, Any] | None = None
) -> dict[str, Any]:
    git = plan["git"]
    pr = resolve_closeout_pull_request(
        root, git["repo"], git["head_branch"], git["base_branch"], git["remote"]
    )
    if pr is None:
        raise WorkflowError("Closeout draft PR is missing.", exit_code=2)
    local_head = current_head(root)
    validate_closeout_remote_pull_request_identity(
        plan,
        pr,
        expected_draft=bool(pr["isDraft"]),
        bound_pr=bound_pr,
    )
    remote_head = closeout_remote_branch_head(root, plan)
    if local_head != remote_head:
        raise WorkflowError(
            "Closeout local/remote/PR HEAD identity mismatch.",
            exit_code=2,
            payload={"local_head": local_head, "remote_head": remote_head, "pr_head": pr["headRefOid"]},
        )
    initial_pr = pr
    for attempt in range(CLOSEOUT_PR_HEAD_READ_ATTEMPTS):
        if pr["headRefOid"] == local_head:
            break
        if attempt + 1 == CLOSEOUT_PR_HEAD_READ_ATTEMPTS:
            raise WorkflowError(
                "Closeout local/remote/PR HEAD identity mismatch.",
                exit_code=2,
                payload={
                    "local_head": local_head,
                    "remote_head": remote_head,
                    "pr_head": pr["headRefOid"],
                },
            )
        time.sleep(CLOSEOUT_PR_HEAD_READ_DELAY_SECONDS)
        reread = resolve_closeout_pull_request(
            root,
            git["repo"],
            git["head_branch"],
            git["base_branch"],
            git["remote"],
        )
        if reread is None:
            raise WorkflowError(
                "Closeout pull request disappeared while waiting for HEAD convergence.",
                exit_code=2,
            )
        validate_closeout_remote_pull_request_identity(
            plan,
            reread,
            expected_draft=bool(initial_pr["isDraft"]),
            bound_pr=bound_pr or initial_pr,
        )
        remote_head = closeout_remote_branch_head(root, plan)
        if remote_head != local_head:
            raise WorkflowError(
                "Closeout local/remote/PR HEAD identity mismatch.",
                exit_code=2,
                payload={
                    "local_head": local_head,
                    "remote_head": remote_head,
                    "pr_head": reread["headRefOid"],
                },
            )
        pr = reread
    validate_closeout_remote_pull_request_identity(
        plan,
        pr,
        expected_draft=bool(initial_pr["isDraft"]),
        expected_head=local_head,
        bound_pr=bound_pr or initial_pr,
    )
    if pr["isDraft"]:
        try:
            run_gh_command(
                ["pr", "ready", "--repo", git["repo"], str(pr["number"])],
                root,
                repo=git["repo"],
                operation="pull_request_ready",
            )
        except WorkflowError as exc:
            raise WorkflowError(
                "Draft-to-ready transition failed.",
                exit_code=2,
                payload={**exc.payload, "stage": "draft-to-ready"},
            ) from exc
        confirmed = resolve_closeout_pull_request(
            root, git["repo"], git["head_branch"], git["base_branch"], git["remote"]
        )
        if confirmed is None or confirmed.get("isDraft") is not False or confirmed.get("headRefOid") != local_head:
            raise WorkflowError("Draft-to-ready transition could not be confirmed.", exit_code=2, payload={"stage": "draft-to-ready-confirmation"})
        validate_closeout_remote_pull_request_identity(
            plan,
            confirmed,
            expected_draft=False,
            expected_head=local_head,
            bound_pr=bound_pr or pr,
        )
        pr = confirmed
    return {"pr": pr, "local_head": local_head, "remote_head": remote_head, "status": "ready"}

def resume_archive_metadata_transaction(
    root: Path,
    task_dir: Path,
    plan: dict[str, Any],
    *,
    bound_pr: dict[str, Any] | None = None,
) -> dict[str, Any]:
    compact_closeout_archive(task_dir, plan)
    validate_closeout_archive_move_layout(root, task_dir, plan)
    dirty = set(git_status_paths(root))
    if dirty:
        validate_closeout_archive_git_paths(dirty, plan, stage="archive-recovery-dirty")
        transaction_parent = current_head(root)
        validate_closeout_reviewed_content(
            root,
            plan,
            transaction_parent,
            include_worktree=True,
        )
        validate_closeout_archive_blob_continuity(
            root,
            task_dir,
            plan,
            transaction_parent,
            expected_summary_pr=bound_pr,
        )
        active = plan["task"]["active_locator"]
        archived = plan["task"]["archive_locator"]
        staged = set(run_stdout(["git", "diff", "--cached", "--name-only", "--no-renames"], cwd=root).splitlines())
        if not staged:
            pathspecs = (
                [f"{active}/{relative}" for relative in plan["projection"]["tracked_move_paths"]]
                + [
                    f"{archived}/{relative}"
                    for relative in closeout_archive_retained_paths(plan)
                ]
            )
            run_stdout(["git", "add", "-A", "--", *pathspecs], cwd=root)
            staged = set(run_stdout(["git", "diff", "--cached", "--name-only", "--no-renames"], cwd=root).splitlines())
        validate_closeout_archive_git_paths(staged, plan, stage="archive-recovery-staged")
        run_stdout(["git", "commit", "-m", format_metadata_commit_subject()], cwd=root)
        archive_commit = current_head(root)
        archive_paths = closeout_commit_paths(root, archive_commit)
        validate_closeout_archive_git_paths(archive_paths, plan, stage="archive-recovery-commit")
        if closeout_commit_parent(root, archive_commit) != transaction_parent:
            raise WorkflowError("Recovered archive commit does not match the exact parent/path transaction.", exit_code=2)
        validate_closeout_archive_blob_continuity(
            root,
            task_dir,
            plan,
            transaction_parent,
            archive_commit=archive_commit,
            expected_summary_pr=bound_pr,
        )
    else:
        archive_commit = current_head(root)
        last_paths = closeout_commit_paths(root, archive_commit)
        transaction_parent = closeout_commit_parent(root, archive_commit)
        validate_closeout_archive_git_paths(last_paths, plan, stage="archive-recovery-head")
        validate_closeout_reviewed_content(
            root,
            plan,
            transaction_parent,
            include_worktree=False,
        )
        validate_closeout_archive_blob_continuity(
            root,
            task_dir,
            plan,
            transaction_parent,
            archive_commit=archive_commit,
            expected_summary_pr=bound_pr,
        )
    local_head = current_head(root)
    remote_proc = run(
        ["git", "ls-remote", "--heads", plan["git"]["remote"], plan["git"]["head_branch"]],
        cwd=root,
        check=False,
    )
    rows = [line.split() for line in remote_proc.stdout.splitlines() if line.strip()]
    remote_head = rows[0][0] if len(rows) == 1 else ""
    if remote_proc.returncode != 0 or remote_head != local_head:
        run_stdout(["git", "push", plan["git"]["remote"], plan["git"]["head_branch"]], cwd=root)
    return {
        "commit": archive_commit,
        "parent": transaction_parent,
        "paths": sorted(closeout_commit_paths(root, archive_commit)),
    }

def resume_archived_closeout(
    root: Path,
    args: argparse.Namespace,
    task_dir: Path,
    *,
    committed_plan: dict[str, Any] | None = None,
    committed_archive: dict[str, Any] | None = None,
    finalization_transaction: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if committed_plan is None:
        raise WorkflowError(
            "Archived current Finalizer recovery requires transaction-bound plan authority.",
            exit_code=2,
        )
    plan = committed_plan
    expected = str(getattr(args, "expected_plan_digest", "") or "")
    if expected != plan["plan_digest"]:
        raise WorkflowError("Formal closeout expected digest does not match the archived plan.", exit_code=2, payload={"expected": expected, "actual": plan["plan_digest"]})
    git = plan["git"]
    require_gh_auth(root)
    archive_commit = committed_archive or resolve_committed_closeout_archive_transaction(root, plan)
    finalizer_recovery = (
        archive_commit is not None
        and isinstance(getattr(args, "finalization_gate", None), dict)
    )
    if finalizer_recovery:
        local_head = current_head(root)
        remote_head = closeout_remote_branch_head(root, plan)
        if remote_head != local_head:
            raise WorkflowError(
                "Archived finalization recovery requires the pushed archive HEAD before Ready.",
                exit_code=2,
                payload={"local_head": local_head, "remote_head": remote_head},
            )
    bound_pr: dict[str, Any] | None = None
    if archive_commit is not None:
        summary_pr = archive_commit.get("summary_pr")
        if not isinstance(summary_pr, dict):
            commit = str(archive_commit.get("commit") or "")
            summary_bytes = closeout_commit_blob_bytes(
                root,
                commit,
                f"{plan['task']['archive_locator']}/{FINISH_SUMMARY_ARTIFACT}",
            )
            summary_pr = closeout_summary_runtime_pr_facts_from_bytes(plan, summary_bytes)
        bound_pr = summary_pr
    pr = resolve_closeout_pull_request(
        root, git["repo"], git["head_branch"], git["base_branch"], git["remote"]
    )
    if pr is None:
        raise WorkflowError("Archived closeout recovery requires the bound pull request.", exit_code=2)
    expected_draft = True if finalizer_recovery else bool(pr["isDraft"])
    if (
        finalizer_recovery
        and isinstance(finalization_transaction, dict)
        and finalization_transaction.get("mode") == "existing_pr_recovery"
    ):
        adopted_pr = finalization_transaction.get("adopted_pr")
        if not isinstance(adopted_pr, dict) or not isinstance(
            adopted_pr.get("initial_is_draft"), bool
        ):
            raise WorkflowError(
                "Archived existing PR recovery transaction is incomplete.",
                exit_code=2,
                payload={"reason_code": "existing_pr_transaction_drift"},
            )
        expected_draft = bool(adopted_pr["initial_is_draft"])
    validate_closeout_remote_pull_request_identity(
        plan,
        pr,
        expected_draft=expected_draft,
        bound_pr=bound_pr,
    )
    if archive_commit is None:
        archive_commit = resume_archive_metadata_transaction(
            root,
            task_dir,
            plan,
            bound_pr=pr,
        )
    else:
        if not finalizer_recovery:
            push_closeout_branch_if_needed(root, plan)
    result = ensure_closeout_pr_ready(root, plan, bound_pr=bound_pr or pr)
    return {
        "status": "ok",
        "stage": "ready",
        "task_dir": str(task_dir),
        "archived_task_dir": str(task_dir),
        "plan_digest": plan["plan_digest"],
        "archive_commit": archive_commit,
        "publish": result,
    }

def execute_closeout_content_push(
    root: Path,
    task_dir: Path,
    task_context: dict[str, Any],
    prepared: dict[str, Any],
) -> dict[str, Any]:
    """Push reviewed content before continuing directly to Draft PR binding."""
    plan = prepared["plan"]
    validate_closeout_reviewed_content(
        root,
        plan,
        current_head(root),
        include_worktree=True,
    )
    publication_head = str(
        plan["git"].get("publication_head") or plan["git"]["branch_review_commit"]
    )
    if current_head(root) != publication_head:
        raise WorkflowError(
            "Closeout exact publication push requires local HEAD at publication_head.",
            exit_code=2,
        )
    run_stdout(
        [
            "git",
            "push",
            "-u",
            plan["git"]["remote"],
            f"{publication_head}:refs/heads/{plan['git']['head_branch']}",
        ],
        cwd=root,
    )
    validate_publish_identity_and_remote_head(
        root,
        prepared["task"],
        task_context,
        plan["git"]["repo"],
        plan["git"]["base_branch"],
        plan["git"]["head_branch"],
        plan["git"]["remote"],
    )
    return {
        "status": "ok",
        "stage": "content_pushed",
        "entry_state": "prepared",
        "task_dir": str(task_dir),
        "finalization_plan_digest": plan["plan_digest"],
        "plan_ref": f"finalization:{plan['plan_digest']}",
        "branch_review_commit": plan["git"]["branch_review_commit"],
    }

def _cmd_finish_work_impl(args: argparse.Namespace) -> dict[str, Any]:
    validate_finish_work_invocation(args)
    root = repo_root(Path(args.root or os.getcwd()))
    config = load_config(root)
    task_dir = resolve_finish_work_task_dir(root, args.task)
    if task_dir_is_archived(root, task_dir):
        if args.dry_run:
            raise WorkflowError("Archived closeout recovery does not have a new dry-run phase.", exit_code=2)
        current_match = finalization_find_transaction_by_task_ref(
            root,
            f".trellis/tasks/{task_dir.name}",
        )
        if current_match is not None:
            transaction, _transaction_path = current_match
            if current_head(root) == transaction["publication_head"]:
                active_task_dir = restore_current_archive_move_for_reentry(
                    root,
                    task_dir,
                    transaction,
                )
                resumed_args = copy.copy(args)
                resumed_args.task = str(active_task_dir)
                return cmd_finish_work(resumed_args)
            boundary = assert_archived_current_transaction_boundary(
                root,
                config,
                task_dir,
                transaction,
                str(getattr(args, "expected_plan_digest", "") or ""),
            )
            result = resume_archived_closeout(
                root,
                args,
                task_dir,
                committed_plan=boundary["plan"],
                committed_archive=boundary["archive_commit"],
                finalization_transaction=transaction,
            )
            result["retired_owner_state"] = finalization_retire_current_state(
                root,
                root / str(transaction["task_ref"]),
            )
            return result
        raise WorkflowError(
            "Archived current Finalizer recovery is missing its transaction.",
            exit_code=2,
        )
    task_context = load_task_runtime_identity(task_dir, config)
    assert_workspace_boundary(root, config, task_context, task_dir)
    current_finalizer = bool(getattr(args, "from_guru_finalizer", False))
    prepared = prepare_closeout(
        root,
        args,
        config,
        task_dir,
        task_context,
        publication_ready=getattr(args, "publication_ready", None),
        current_finalizer=current_finalizer,
    )
    plan = prepared["plan"]
    if args.dry_run:
        return {
            "status": "dry-run",
            "dry_run_side_effects": False,
            "task_dir": str(task_dir),
            "finalization_plan": plan,
            "finalization_plan_digest": plan["plan_digest"],
            "expected_actions": list(CLOSEOUT_TRANSITIONS[1:]),
        }

    expected_digest = str(getattr(args, "expected_plan_digest", "") or "")
    if expected_digest != plan["plan_digest"]:
        raise WorkflowError(
            "Formal closeout expected digest does not match the rebuilt plan.",
            exit_code=2,
            payload={"expected": expected_digest, "actual": plan["plan_digest"], "failed_stage": "plan-digest-handshake"},
        )
    assert_closeout_archive_month_current(plan)
    require_gh_auth(root)
    if current_finalizer:
        transaction = finalization_read_transaction(root, task_dir)
        prior_transaction = transaction
        recovery_preview = getattr(args, "existing_pr_recovery", None)
        if (
            isinstance(transaction, dict)
            and transaction.get("mode") == "ordinary_publication"
            and isinstance(recovery_preview, dict)
        ):
            if recovery_preview.get("ancestry") == "strict_ancestor":
                transaction = finalization_adopt_provenance_tail_transaction(
                    root,
                    task_dir,
                    plan,
                    transaction,
                    recovery_preview,
                )
            else:
                transaction = finalization_adopt_unbound_equal_head_transaction(
                    root,
                    task_dir,
                    plan,
                    transaction,
                    recovery_preview,
                )
            prior_transaction = transaction
        recovered_pr, pre_push_remote_head = finalization_pre_mutation_remote_preflight(
            root,
            plan,
            prior_transaction,
            existing_pr_recovery=(
                recovery_preview
                if transaction is None and isinstance(recovery_preview, dict)
                else None
            ),
        )
        if transaction is None:
            if isinstance(recovery_preview, dict):
                if recovered_pr is None:
                    raise WorkflowError(
                        "Existing PR recovery preview lost its bound PR.", exit_code=2
                    )
                adopted_pr = {
                    "number": recovered_pr["number"],
                    "url": recovered_pr["url"],
                    "initial_is_draft": bool(recovery_preview["initial_is_draft"]),
                    "pre_push_remote_head": pre_push_remote_head,
                }
                needs_push = pre_push_remote_head != str(
                    plan["git"].get("publication_head")
                    or plan["git"]["branch_review_commit"]
                )
                transaction = finalization_transaction_from_plan(
                    plan,
                    next_transition="push_content" if needs_push else "bind_pr",
                    pr=recovered_pr,
                    pre_push_remote_head=pre_push_remote_head if needs_push else None,
                    mode="existing_pr_recovery",
                    adopted_pr=adopted_pr,
                )
            else:
                transaction = finalization_transaction_from_plan(
                    plan,
                    next_transition=("bind_pr" if recovered_pr else "push_content"),
                    pr=recovered_pr,
                    pre_push_remote_head=(
                        None if recovered_pr is not None else pre_push_remote_head
                    ),
                )
            finalization_write_transaction(root, task_dir, transaction)
        else:
            if transaction.get("plan_digest") != plan["plan_digest"]:
                replacement = finalization_transaction_from_plan(
                    plan,
                    next_transition=str(transaction["next_transition"]),
                    pr=(
                        transaction["pr"]
                        if isinstance(transaction.get("pr"), dict)
                        else None
                    ),
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
                prior_identity = {
                    key: value
                    for key, value in transaction.items()
                    if key != "plan_digest"
                }
                replacement_identity = {
                    key: value
                    for key, value in replacement.items()
                    if key != "plan_digest"
                }
                if prior_identity != replacement_identity:
                    raise WorkflowError(
                        "Task finalization transaction cannot bind a changed plan identity.",
                        exit_code=2,
                    )
                transaction = replacement
                finalization_write_transaction(root, task_dir, transaction)
            else:
                finalization_validate_transaction_plan(transaction, plan)
        summary_path = task_dir / FINISH_SUMMARY_ARTIFACT
        if summary_path.exists():
            if not summary_path.is_file() or summary_path.is_symlink():
                raise WorkflowError(
                    "Task finalization summary recovery path is unsafe.",
                    exit_code=2,
                )
            try:
                read_and_validate_closeout_final_summary(summary_path, plan)
            except WorkflowError:
                summary_path.unlink()
    entry_state = resolve_closeout_pre_draft_state(root, task_dir, plan)
    if entry_state == "prepared":
        if current_finalizer:
            finalization_pre_mutation_remote_preflight(
                root,
                plan,
                transaction,
            )
        execute_closeout_content_push(
            root,
            task_dir,
            task_context,
            prepared,
        )
        entry_state = "content_pushed"
        if current_finalizer:
            transaction = finalization_advance_transaction(
                plan,
                transaction,
                next_transition="bind_pr",
            )
            finalization_write_transaction(root, task_dir, transaction)

    if entry_state == "content_pushed":
        validate_publish_identity_and_remote_head(
            root, prepared["task"], task_context, plan["git"]["repo"],
            plan["git"]["base_branch"], plan["git"]["head_branch"], plan["git"]["remote"],
        )

    validate_closeout_reviewed_content(
        root,
        plan,
        current_head(root),
        include_worktree=True,
    )

    if current_finalizer:
        finalization_pre_mutation_remote_preflight(
            root,
            plan,
            transaction,
        )
    pr = ensure_closeout_bound_pr(root, plan, prepared["body"], transaction if current_finalizer else None)
    if current_finalizer:
        transaction = finalization_advance_transaction(
            plan,
            transaction,
            next_transition="archive",
            pr=pr,
        )
        finalization_write_transaction(root, task_dir, transaction)
    finish_summary_path = task_dir / FINISH_SUMMARY_ARTIFACT
    expected_draft = finalization_expected_pr_draft_state(
        transaction,
        current_finalizer=current_finalizer,
    )
    if finish_summary_path.is_file():
        validate_closeout_active_projection(
            root,
            task_dir,
            plan,
        )
        validate_closeout_pull_request_identity(
            root,
            task_dir,
            plan,
            pr,
            expected_draft=expected_draft,
            require_summary=True,
            expected_head=current_head(root),
        )
    else:
        finish_summary_path, _summary = build_final_archive_projection(
            root,
            task_dir,
            prepared,
            pr,
            expected_draft=expected_draft,
        )
    finalization_gate = getattr(args, "finalization_gate", None)
    if isinstance(finalization_gate, dict):
        if (
            finalization_gate.get("route", {}).get("typed_exit") != "ready_for_merge"
            or finalization_gate.get("route", {}).get("output")
            != FINALIZATION_EXECUTOR_OUTPUT_MARKER
        ):
            raise WorkflowError(
                "Task finalization requires the exact private published marker before archive.",
                exit_code=2,
            )
    archived_task_dir, archive_commit = execute_archive_metadata_transaction(
        root,
        task_dir,
        plan,
        bound_pr=pr,
    )
    publish_payload = ensure_closeout_pr_ready(root, plan, bound_pr=pr)
    retired_owner_state: list[str] = []
    if current_finalizer:
        finalization_write_transaction(
            root,
            archived_task_dir,
            finalization_advance_transaction(
                plan,
                transaction,
                next_transition="mark_ready",
                pr=publish_payload["pr"],
            ),
        )
    return {
        "status": "ok",
        "stage": "ready",
        "task_dir": str(task_dir),
        "archived_task_dir": str(archived_task_dir),
        "finalization_plan_digest": plan["plan_digest"],
        "entry_state": entry_state,
        "finish_summary": str(archived_task_dir / finish_summary_path.name),
        "archive_commit": archive_commit,
        "publish": publish_payload,
        "retired_owner_state": retired_owner_state,
    }
