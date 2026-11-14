# Existing Issue Readiness

`judgment_mode=semantic`. Use the original review method and all ten dimensions.
Read the complete live Issue title/body, effective discussions and review comments,
necessary prerequisite deliveries and code changes that affect prior conclusions.
Judge actual coverage, currency, independent delivery and remaining conditions.
A comment's presence, format, author, age or count never establishes readiness.
Clear historical comments can suffice; no comment alone is not a blocker.

## Input and local recording

`existing_issue_intake` carries mode, exact Issue, base_source, continuation_id
and the actual Sync source_exit (`baseline_ready` or `synced`). Copy a read
source's kind/selected_ref/commit unchanged. A genuine synchronized source uses
kind=synced_branch, normalized selected_base as selected_ref and decision_head
as commit. Keep the original full Sync stdout available call-locally if complete
Intake becomes necessary. It cannot be rebuilt from these three source fields.

`issue_review_return` keeps that exact Issue/source/continuation. Its separate
closed variants carry the actual local context_result, requirements_result or
wording_result summary with source_refs; Clarify also supplies source_selection.
Wording requirements_gap is its own variant and is not a wording pass. Project
the actual producer result_summary to the corresponding result field, preserving
all other identity/source fields. Add only profile=issue_review_return and map
exit_id to source_exit. Do not handwrite a producer result or copy its private
owner checkpoint. Reread changed authority and judge remaining coverage yourself.

Use the original record/check/invoke wrappers with --invocation -. The envelope
has schema_version=1.0, public_input, owner_context.change_request and owner_result;
no transition is required or manufactured for these two profiles. Supply current
Issue kind/repo/number/title/body/updated_at in change_request. The independent
issue-review-owner-1.0 schema requires public_input unchanged, typed_exit,
result_summary, source_refs, source_selection, ten original dimensions with actual
conclusions and ai_review_gate. `gap` is required for supplement exits. Record
returns the reviewed owner result. Check rereads Issue and emits a local receipt;
invoke consumes that exact receipt. Local digests bind adjacent bytes only.

## One result and consumer

- ready: coverage sufficient, still applicable and prerequisites met. The original
  task-intake router invokes Create Task with its own scope/resource gate.
- supplement_context: ask original Discovery to resolve the actual fact gap.
- supplement_requirements: ask original Clarify to resolve requirements, source
  roles, scope or delivery-unit questions and actual required choices.
- supplement_wording: ask original Wording to review or revise the indicated wording.
- full_intake_required: coverage insufficient or change impact cannot be bounded.
  Original Discovery -> Clarify -> Wording -> current_issue Readiness consumes
  the original actual Sync transition and Issue change_input.
- refresh_issue_baseline: the selected source really became unusable/inapplicable.
  Original Sync gets a dedicated Issue/continuation return identity. A read source
  preserves selected_ref and exact commit; synchronized source requires actual sync.
- blocked: name the unmet prerequisite, real unresolved choice or unavailable
  necessary evidence, and the condition/owner for recovery. Do not create a Task.

Choose the earliest necessary gap in context -> requirements -> wording order.
Each completed supplement returns here; do not automatically run remaining owners.
If investigation proves behavior unchanged, it can be ready immediately. After a
requirement change, request wording only where the previous wording coverage lost
applicability. Reuse unaffected coverage. Time, Agent/session changes and unrelated
HEAD movement are not refresh triggers. Missing call-local material returns to its
original producer; never invent receipts or create a durable coverage ledger.

No mutation follows merely from a local review. Only real choices and exact
Git/GitHub side effects use the original interaction boundary. `ready` itself
does not authorize creation. Unknown exits or mismatched identities stop.
