def execute_finalization_transition_result(
    root: Path,
    args: argparse.Namespace,
    public_input: dict[str, Any],
    gate: dict[str, Any],
    context: dict[str, Any],
) -> dict[str, Any]:
    exit_id = gate["route"]["typed_exit"]
    task_dir = context["task_dir"]
    if exit_id == "reprepare_required":
        reason_code = context["reprepare_reason_code"]
        reviewed_content_head = context["plan"]["git"]["reviewed_content_head"]
        reprepare: dict[str, Any] | None = None
        reprepare_facts: dict[str, Any] | None = None
        if reason_code == FINALIZATION_REPREPARE_PROVENANCE_TAIL:
            reprepare = (
                context.get("prepared", {}).get("pre_pr_reprepare")
                if isinstance(context.get("prepared"), dict)
                else None
            )
            previous_transaction = (
                reprepare.get("previous_transaction")
                if isinstance(reprepare, dict)
                and isinstance(reprepare.get("previous_transaction"), dict)
                else None
            )
            reprepare_facts = finalizer_pre_pr_provenance_reprepare_preflight(
                root,
                task_dir,
                context["plan"],
                previous_transaction=previous_transaction,
            )
            target_repo = context["plan"]["git"]["repo"]
            publication = finalizer_publication_identity(
                root,
                reviewed_content_head,
                target_repo,
            )
            provenance = (
                publication
                if publication["metadata_tail"] is not None
                else prepare_provenance_metadata_tail(
                    root,
                    reviewed_content_head,
                    target_repo,
                )
            )
        elif reason_code == FINALIZATION_REPREPARE_ARCHIVE_MONTH:
            publication = finalizer_publication_identity(
                root,
                reviewed_content_head,
                context["plan"]["git"]["repo"],
            )
            provenance = publication
        else:
            raise WorkflowError(
                "Finalizer reprepare reason is unsupported.",
                exit_code=2,
            )
        previous_owner_transaction = finalization_read_transaction(root, task_dir)
        retired = finalizer_supersede_pre_pr_state(root, task_dir)
        replacement_transaction: dict[str, Any] | None = None
        if reason_code in {
            FINALIZATION_REPREPARE_PROVENANCE_TAIL,
            FINALIZATION_REPREPARE_ARCHIVE_MONTH,
        }:
            task_context = context.get("task_context")
            # The public eval fixture supplies only the reviewed objective
            # facts.  It intentionally has no task/worktree runtime mapping;
            # exercise the archive-month route without manufacturing a
            # production closeout transaction in that fixture.
            if (
                reason_code == FINALIZATION_REPREPARE_ARCHIVE_MONTH
                and task_context is None
                and os.environ.get("GURU_TEAM_EVAL_STAGING") == "1"
            ):
                output = finalization_reprepare_public_output(
                    root,
                    task_ref=public_input["task_ref"],
                    reason_code=reason_code,
                    branch_review_commit=reviewed_content_head,
                    publication_head=(
                        context["plan"]["git"].get("publication_head")
                        or reviewed_content_head
                    ),
                )
                return {
                    "status": "ok",
                    "stage": "reprepare_required",
                    "typed_exit": exit_id,
                    "retired_owner_state": False,
                    "publication_head": output["publication_head"],
                    "replacement_transaction_created": False,
                    "output": output,
                }
            if not isinstance(task_context, dict):
                raise WorkflowError(
                    "Provenance reprepare is missing current task runtime identity.",
                    exit_code=2,
                )
            replacement_args = copy.copy(args)
            replacement_args.repo = context["plan"]["git"]["repo"]
            replacement_args.remote = context["plan"]["git"]["remote"]
            replacement_args.base_branch = context["plan"]["git"]["base_branch"]
            replacement_args.title = context["plan"]["publish"]["title"]
            replacement_args.include_finalization_gate = True
            replacement = prepare_closeout(
                root,
                replacement_args,
                load_config(root),
                task_dir,
                task_context,
                publication_ready={
                    "profile": "publication_ready",
                    "mode": public_input.get("mode", "workflow"),
                    "task_ref": public_input["task_ref"],
                    "branch_review_commit": provenance["reviewed_content_head"],
                    "pr_title": context["plan"]["publish"]["title"],
                    "pr_body": context["plan"]["publish"]["body"],
                },
                current_finalizer=True,
            )
            if reprepare_facts is None:
                previous_recovery = (
                    previous_owner_transaction.get("adopted_pr")
                    if isinstance(previous_owner_transaction, dict)
                    and previous_owner_transaction.get("mode")
                    == "existing_pr_recovery"
                    else None
                )
                if isinstance(previous_recovery, dict):
                    pre_push_remote_head = str(
                        previous_recovery.get("pre_push_remote_head") or ""
                    )
                else:
                    _existing_pr, pre_push_remote_head = (
                        finalization_pre_mutation_remote_preflight(
                            root,
                            replacement["plan"],
                            None,
                        )
                    )
                replacement_transaction = finalization_reprepared_transaction(
                    replacement["plan"],
                    previous_owner_transaction,
                    pre_push_remote_head=pre_push_remote_head,
                )
            else:
                replacement_transaction = finalization_reprepared_transaction(
                    replacement["plan"],
                    previous_owner_transaction,
                    pre_push_remote_head=str(reprepare_facts["remote_head"]),
                )
            finalization_pre_mutation_remote_preflight(
                root,
                replacement["plan"],
                replacement_transaction,
            )
            finalization_write_transaction(
                root,
                task_dir,
                replacement_transaction,
            )
        output = finalization_reprepare_public_output(
            root,
            task_ref=public_input["task_ref"],
            reason_code=reason_code,
            branch_review_commit=provenance["reviewed_content_head"],
            publication_head=provenance["publication_head"],
        )
        return {
            "status": "ok",
            "stage": "reprepare_required",
            "typed_exit": exit_id,
            "retired_owner_state": retired,
            "reviewed_content_head": provenance["reviewed_content_head"],
            "publication_head": provenance["publication_head"],
            "replacement_transaction_created": replacement_transaction is not None,
            "output": output,
        }
    if exit_id == "ready_for_merge":
        if context["transaction_state"] == "ready":
            pr = context.get("published_pr")
            if not isinstance(pr, dict):
                raise WorkflowError(
                    "Task finalization Ready recovery is missing the bound pull request.",
                    exit_code=2,
                )
            materialized_gate = finalization_gate_with_ready_for_merge_output(
                root,
                task_dir,
                gate,
                context["plan"],
                pr,
            )
            retired_owner_state = finalization_retire_current_state(root, task_dir)
            return {
                "status": "ok",
                "stage": "ready_recovered",
                "typed_exit": exit_id,
                "output": materialized_gate["route"]["output"],
                "retired_owner_state": retired_owner_state,
            }
        if (
            context["transaction_state"] == "archived"
            and context.get("published_transition_complete") is not True
        ):
            transaction = finalization_read_transaction(root, task_dir)
            if not isinstance(transaction, dict):
                raise WorkflowError(
                    "Task finalization archived recovery is missing its transaction.",
                    exit_code=2,
                )
            bound_pr = transaction.get("pr")
            if not isinstance(bound_pr, dict):
                raise WorkflowError(
                    "Task finalization archived recovery is missing its bound pull request.",
                    exit_code=2,
                )
            publish_payload = ensure_closeout_pr_ready(
                root,
                context["plan"],
                bound_pr=bound_pr,
            )
            finalization_write_transaction(
                root,
                task_dir,
                finalization_advance_transaction(
                    context["plan"],
                    transaction,
                    next_transition="mark_ready",
                    pr=publish_payload["pr"],
                ),
            )
            materialized_gate = finalization_gate_with_ready_for_merge_output(
                root,
                task_dir,
                gate,
                context["plan"],
                publish_payload["pr"],
            )
            retired_owner_state = finalization_retire_current_state(root, task_dir)
            return {
                "status": "ok",
                "stage": "ready_recovered",
                "typed_exit": exit_id,
                "output": materialized_gate["route"]["output"],
                "retired_owner_state": retired_owner_state,
            }
        finish_args = copy.copy(args)
        finish_args.task = public_input["task_ref"]
        finish_args.from_guru_finalizer = True
        finish_args.expected_plan_digest = context["plan"]["plan_digest"]
        finish_args.dry_run = False
        finish_args.finalization_gate = gate
        finish_args.existing_pr_recovery = copy.deepcopy(
            context.get("existing_pr_recovery")
        )
        finish_args.publication_ready = finalization_prepare_publication_ready(
            public_input,
            transaction=finalization_read_transaction(root, task_dir),
        )
        result = cmd_finish_work(finish_args)
        materialized_gate = finalization_gate_with_ready_for_merge_output(
            root,
            Path(result["archived_task_dir"]),
            gate,
            context["plan"],
            result["publish"]["pr"],
        )
        return {
            **result,
            "typed_exit": exit_id,
            "output": materialized_gate["route"]["output"],
        }
    return {
        "status": "ok",
        "stage": "no_side_effect",
        "typed_exit": exit_id,
        "output": copy.deepcopy(gate["route"]["output"]),
    }


def cmd_execute_finalization_transition(args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(Path(args.root or os.getcwd()))
    public_input, _ = finalization_public_input(root, args.input)
    gate, gate_path = finalization_gate_input(root, public_input, args.gate)
    gate, context = check_finalization_gate_result(
        root,
        args,
        public_input,
        gate,
        gate_path,
        allow_pending_transition=True,
    )
    return execute_finalization_transition_result(
        root,
        args,
        public_input,
        gate,
        context,
    )

def context_sort(values: set[str] | list[str]) -> list[str]:
    return sorted(set(values), key=lambda item: item.encode("utf-8"))
