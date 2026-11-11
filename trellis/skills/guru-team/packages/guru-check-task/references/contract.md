# Original Check recovery and historical controls

This semantic Skill is standalone_only under MIGRATION-794. Current development
candidate_check, initial_check, finding_fix_rerun, planning_reentry,
resolved_reconciliation, scope revision and withdrawal profiles are retired.
Their old schemas remain pinned validation assets, never current runtime fallback.
Original guru-review-branch owns all nine adequacy dimensions, qualification,
Architecture, documents/consumers/compatibility review and Planning/scope routes.
Engineering self-checks are facts, never a Check pass.

Only already-completed original Planning rollback recovery and selected legacy
control maintenance remain. Read exact current Interface, original result and
source facts. For legacy controls load legacy-maintenance.md and use its named
command. No development Check result, pass or new external action is created.

## Recover an already completed planning rollback

`delivery_planning_stale_recovery` is a separate semantic profile of this same
Check owner. Its public input carries mode, task_ref, delivery_key and the
actual `original_check_input`. Read its schema and
`schemas/delivery-planning-stale-recovery-owner-1.0.schema.json` before invoking.
The private `--owner-result` is an envelope with `original_result`, optionally
`corrected_result`, and, for old unbound results, `original_delivery`. It is
not a downstream handoff.

For a pre-775 rollback, first retain the original target checkout's candidate,
HEAD, plans, full Check result, public input and actual original public source.
Choose a complete matching Guru provider outside that target. Its current
workflow/router, Check package, consumer contracts, dispatcher and managed
runtime must belong to that same complete provider. The target supplies its
compatible installed Task schema 2 / Delivery API 1.0, C4 and actual current
selection. Do not copy one package or invoke the target's old dispatcher.

`--root` is the existing target-checkout parameter. The public wrapper and its
help declare it. The launcher resolves the provider's own runtime; Check then
uses the specified target and its installed public API. Set
`PROVIDER_CHECK_PACKAGE` to this complete provider's actual Check package,
`TARGET_CHECKOUT` to the unchanged target, and the JSON locators below to
absolute regular files. Invoke the existing wrapper:

```bash
"$PROVIDER_CHECK_PACKAGE/scripts/invoke.sh" \
  --root "$TARGET_CHECKOUT" --input "$RECOVERY_INPUT" \
  --owner-result "$RECOVERY_OWNER_RESULT"
```

For a genuine semantic correction use that same provider's recorder, with the
same target and recovery input, before passing both full results to recovery:

```bash
"$PROVIDER_CHECK_PACKAGE/scripts/record-phase2-check.sh" \
  --root "$TARGET_CHECKOUT" --task "$TASK_REF" \
  --skill-input "$RECOVERY_INPUT" --input "$CORRECTION_AUTHORING" \
  --dry-run > "$CORRECTION_RECEIPT"
```

Validate and project the receipt as described below. These commands do not
install or update target tools. A missing compatible target public API or an
actual identity/selection error stops at its original diagnostic; never load a
provider-private Task implementation as fallback.

Recover this unchanged target first. The original Author/Clarify consumes the
actual handoff and enters current replanning. Only after the old result is no
longer reused may the original tools owner review and apply a complete target
tool update. Implementation then follows the matching current provider’s committed review chain. Updating tracked target tools before recovery changes the old
result's content/candidate; return that change to its affected original owner.
Do not replace an old token or relax content checks to continue it. This narrow
provider use adds no generic remote execution, alternate runtime, environment
identity override or recovery state.

Ordinary Check profiles still require their actual
current Planning result; this recovery profile does not call the ordinary
binding or checker after Planning was lawfully cleared.

The pinned original provider recorded the first `planning_stale` rework with `--skill-input` pointing
to the original public Check input. The original recorder derives the optional
`rollback_binding` in its existing schema-6.0 result from the actual public
Delivery and Planning result: key, Planning result ID, scope_ref, plan_ref,
candidate and the three Planning evidence AuthorityRefs. The binding has only
this same-owner recovery consumer. Do not author it, substitute current facts
for original facts, or create a second checkpoint. Initial invocation requires
that binding before rework. Non-planning outcomes retain the original shape.

Recovery performs these actions in order:

1. Read the complete original 6.0 result, original public input and actual
   current public Task/Delivery. Check C4/identity and exact current selection;
   with no context use the existing explicit-key path. Keep the same key.
2. Read the original binding. For a pre-775 result without it, obtain an actual
   retained original public query with `key` and `delivery`, including its
   Planning result and candidate. Alternatively read the exact original Git
   Task object with the installed public `common.delivery_schema.parse_task_v2`
   parser, then select this same key. Feed that original object as
   `original_delivery`; never assemble it from current values. Planning evidence
   alone without the original candidate is incomplete. The original Planning
   ID must equal `original_check_input.planning_accepted_result_id`.
3. Compare current scope/accepted_scope, plan, all three planning bytes,
   candidate, HEAD, reviewed content and paths with those original facts.
   Require planning phase and cleared planning/check/full_review/readiness
   result slots. A real change returns its concrete field/error to the affected
   original identity, Clarify, Planning or implementation/Check owner. Preserve
   edits. The current phase and empty slots alone do not establish recovery.
4. If the original semantic classification, action and route remain correct,
   invoke the original public wrapper with this recovery input/envelope. It
   validates and returns only the existing `planning_stale` handoff. It performs
   no rework, record_gate, candidate write or pass creation; repeated recovery
   leaves the public Task/Delivery unchanged.
5. If the handoff needs correction, personally judge the scope classification,
   concrete repair and route against current authority before recording a new
   result. Preserve the original file. Use the same 11-field authoring with
   `record-phase2-check.sh --root . --task "$TASK_REF" --skill-input
   "$RECOVERY_INPUT" --input "$CORRECTION_AUTHORING" --dry-run`. Validate its
   ordinary intermediate receipt. Its `result`, excluding only receipt result
   fields `artifact_path` and `dry_run`, is the new complete 6.0
   `corrected_result`. Pass both full results to recovery; do not send the
   correction through the ordinary checker or overwrite the original checkpoint.
   Correction still produces only this same rollback's `planning_stale`.

The recovery envelope's original and corrected results must be planning_stale;
a passed result cannot serve as either. The local reviewed-content identity is
freshly captured for dry-run correction without requiring the cleared Planning
slot. An original delivery_resolved_reconciliation retains its explicit
resolved-content algorithm for first rollback, recovery and correction; the
recovery profile does not turn that result into an ordinary content token. Recovery separately compares that new result with the original rollback
and actual current facts. The recorder rejects persisted recovery correction.

If an old result has no binding and no original public source, the wrapper
returns the existing zero-payload `blocked` exit and a stderr diagnostic naming
`owner_result.original_delivery` and original Planning/Clarify. The AI reports
the concrete missing source and stops this recovery. Original Planning/Clarify
must judge the actual current scope afresh; never reconstruct a missing pass,
read old Activation private state, change a digest or repeat the completed
rollback. Other ordinary missing/incomplete source and stale errors keep their
specific field and remediation, rather than becoming a fabricated handoff.

The original result remains available only for this bounded same-owner
recovery. The original owner retires it when its consumer finishes. Recovery proves planning handoff usability only; Author,
Wording, Architecture, Approval and current independent Review retain their own entry and
judgment. It establishes no Planning, Check, publication or Task Completion pass.
