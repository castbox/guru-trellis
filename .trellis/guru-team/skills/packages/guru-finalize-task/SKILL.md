---
name: guru-finalize-task
description: Finalize a reviewed Trellis task through one semantic closeout loop, one deterministic transaction engine, and six typed exits.
---

# Guru Finalize Task

Use this Skill only after publication review is current, or when explicitly
resuming a previously prepared finalization.

1. Read `references/contract.md` completely.
2. Validate the selected public input profile and every owner precondition.
3. Run the side-effect-free preview or current-state discovery.
4. Perform the AI Review Gate and obtain current side-effect confirmation only
   when the contract requires it.
5. Record and check the private gate before any deterministic transition.
6. Emit exactly one declared typed exit.

In workflow mode, the caller automatically consumes
`verification_required`, `publication_review_stale`, `resume_finalization`, and
`reprepare_required`. These are machine routes, not user decisions. Ask again
only when the external side-effect plan or its authority changed.

For `provenance_tail_required`, the checked gate retains only the private
executor marker because `publication_head` does not exist yet. After the
executor has produced or reused the allowed tail and retired the old private
state, it returns the exact `branch_review_commit` and `publication_head` needed
by the next preview. Before returning either reprepare exit, Finalizer writes a
replacement owner-private transaction containing the exact reviewed title/body
and the new task/content/publication identity. `archive_month_changed` follows
the same authority-continuity rule. The next preview never recovers PR payload
from a deleted plan, a Closed PR, or an incomplete synthesized input.

`publication_review_stale` carries the exact `branch_review_commit` that the
Finalizer found stale, together with task identity and the stable reason. The
Publication owner uses that current Git anchor to distinguish a task-work
continuity finding from metadata-only re-review. Missing or mismatched current
identity fails closed; never infer or synthesize it. The wrapper emits the
stale route without mutating plan, publication, verification, or gate state.

For one current, unique action, prompt with `确认继续`. Any clear affirmative
reply applies to the displayed action in the current dialogue; no recorder or
checkpoint stores or binds that authorization. Never require the user to repeat
a SHA, digest, or fixed sentence. If the plan, HEAD, target, or scope changes,
present the change and obtain fresh confirmation.

`judgment_mode=semantic`. Scripts execute, record, and validate deterministic
facts; they never choose scope, readiness, user authorization, or semantic pass.
Unknown, missing, multiple, stale, or consumer-mismatched results stop fail
closed.
