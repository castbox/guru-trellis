---
name: guru-create-task
description: Create an independently reviewed Trellis task in the exact acquired checkout, or recover its result without repeating mutation.
---

# Create Task

Before substantive output, read `.trellis/spec/workflow/clear-technical-writing.md`
in full and apply it within this entry's existing scope. Until that read succeeds,
use only short progress messages or concrete missing-dependency diagnostics.
State the current action or missing item; make no unverified claim. If the file
cannot be read, pause substantive output, then read it and resume the same
request when available. No additional approval is needed for that recovery.

Read `.trellis/spec/workflow/workflow-contract.md#interaction-budget` before
any confirmation, choice or clarification. This Skill retains its own action
plan, confirmation boundary and execution/recovery contract.

`judgment_mode=semantic`. Consume only `guru-review-change-request:ready`
with a current complete-chain `target.kind=existing_issue | standalone_request`
or the independent existing-Issue ready result, after actual Sync and Readiness. Never create or select a GitHub Issue here. For an
existing Issue, reread its live identity and accepted scope; for a standalone
request preserve `source.kind=no_issue` without invented closure semantics.
Issue creation input accepts `exact_source | reference_only` and preserves the
reviewed disposition through official creation and result recovery.
`reference_only` does not grant source-Issue closure; `follow_up | parent` remain
unsupported creation inputs.

The current input is `schemas/public-delivery-task-creation-input-2.0.schema.json`.
Before authoring `creation`, read both installed contracts from the repository root:
`.trellis/guru-team/skills/packages/guru-create-task/schemas/public-delivery-task-creation-input-2.0.schema.json`
and `.trellis/guru-team/skills/contracts/task-lifecycle/task-creation-input-3.0.schema.json`.
When entering through a platform discovery copy, resolve the profile schema's
cross-package references from its directory in the shared installation.
Its `allOf` constraints apply together with the
profile's local properties. For `source_profile=existing_issue`, copy the reviewed Issue identity as
`reviewed_source={kind:"issue",repo_ref,number,disposition}`. The disposition is
`exact_source` or `reference_only`; `relation` is not an input field. Read
`examples/public-create-issue-input.json` for that normal shape. For
`source_profile=standalone_request`, use `reviewed_source={kind:"no_issue"}` and
`examples/public-create-input.json`. In both cases `delivery_target` has the
reviewed `repo_ref` and `branch_ref`. Replace sample facts with the actual
upstream ready/acquisition output and current Task date; examples supply no
semantic review or creation authority.

Project the actual upstream base into `reviewed_base_source={kind,selected_ref,commit}`.
For `ready.transition.base.kind=git_object`, copy those three values unchanged.
Its selected_ref locates the adopted source; do not resolve a later ref value or
compare local main with that fixed commit. The exact object must be available
as a commit in the same repository and equal acquisition.decision_head.
For an actual synchronized base, set kind=synced_branch, normalize its
selected_base into selected_ref, and copy decision_head into commit. Do not
invent synchronized provenance for a read result. Before new creation, the
synchronized source branch must match selected_base_ref and its local HEAD
must equal commit. Result recovery validates the original source/acquisition;
later branch advancement does not invalidate an already completed result.

Choose `selected_base_ref` independently as the reviewed Task integration
branch. It supplies official task.py --base-branch and non-base/non-target
checkout eligibility. `delivery_target` retains its future delivery role.
A fixed-object read does not choose either branch or require primary clean.
The current input removes reviewed_base_head; see
[MIGRATION-813](../../../../presets/guru-team/MIGRATION-813.md) for the matching
consumer cutover and fixed-old-provider result recovery.

Review the exact TaskId, date-prefixed TaskRef, title, ordinary scope, selected
base and delivery target. Choose one checkout acquisition route:
`adopt_invocation_checkout` for the unique clean registered linked invocation
checkout on a non-base, non-delivery branch at the reviewed decision HEAD,
or `provision_linked_worktree` with
an explicit `new_branch | existing_branch | existing_checkout` disposition.
New Task creation never adopts the primary checkout, including when it already
has a non-base branch. Read live topology, HEAD/ref, dirty/untracked contents
and the current conversation binding before choosing the location. Preserve
existing content and other worktrees; never switch or detach the primary HEAD
to prepare this Task. With no suitable linked location, review the exact path,
branch, source ref/HEAD and creation side effects before acquiring it.
`record-task-plan` and `create-task` reject primary adoption before mutation.
This create-only precondition does not govern read-only recovery of an already
created primary Task; old-Task migration, base Sync and Cleanup retain their
existing owners and clean-checkout requirements.

For a newly provisioned directory (`new_branch` or `existing_branch`), read
live Git topology and the confirmed primary repository's
`.trellis/guru-team/config.yml` before selecting the path. Confirm the primary
with actual toplevel, gitdir and common-dir facts; neither the porcelain first
row nor the common-dir parent alone establishes it. Use the existing
`guru-select-workflow-mode/scripts/check-env.sh --root <invocation-checkout>
--worktree-name <reviewed-name>` public query from the shared installation.
Its `worktree_root` is absolute: empty configuration uses
`<primary-parent>/<primary-name>-worktrees`, relative configuration resolves
from primary, and absolute configuration is used directly. Resolve a real
configuration or anchor conflict through its diagnostic; never overwrite
another checkout's configuration or substitute the current desktop directory.

When the AI generates the new location, set acquisition
`path_source=configured`, `worktree_name` to one reviewed directory name, and
`checkout_root` to the query's absolute `checkout_root` target. Use `--checkout-root <plan>`
with `--worktree-name` to precheck that exact plan. The creation runtime repeats
the configured target comparison before any branch, worktree or Task creation;
a mismatch requires this owner to correct and rereview the plan, never silent
relocation. A caller's genuine explicit location uses `path_source=explicit`
and the original absolute `checkout_root` contract. An absolute value authored
by the AI does not establish explicit caller intent.

Existing published inputs that omit the new fields retain their absolute-path
meaning under [MIGRATION-760](../../../../presets/guru-team/MIGRATION-760.md).
Current AI-generated plans use `configured`. Adopted invocation checkouts,
`existing_checkout`, and result recovery retain their original identity and
location checks; the generation root is not an allowlist for existing or
explicit locations. Recovery finds the verified original binding and location,
even after configuration changes, without relocation or another acquisition.

Review the actual branch and absolute call-local checkout path, plus the five
cleanup ownership projections. Show the exact task and Git side effects in
the current dialogue before invoking the executor.
The reviewed TaskRef must use the current Asia/Shanghai task date. If the date
changes before or during official creation, return `refresh_review` and review
a new TaskRef; do not create a task under a different date. Read-only result
recovery retains the original TaskRef across dates.

Use the `delivery_task_creation` profile. Public input schema `guru-create-task-input-delivery-2.0` retains the removal of retired task
`creator` and `assignee` fields. Rereview an old request and omit those fields;
the closed Delivery schema rejects them before acquisition. The reviewed delivery
target remains call-local and is never added to official `task.json`. The
official creator receives the slug body without its date prefix.

Use `record-task-plan` for objective preconditions, `create-task` for the
official Fixed Fork `task.py create --schema-version 2.0 --no-start` followed by TaskId/source
materialization and C4/C5 control-state establishment, then
`check-task-creation-result`. Task retains overall scope and completion responsibility without a development
status. `created` enters the current workflow and `guru-create-delivery` before
any D1 Planning. A context key binds through the public schema-3 Task session
with no selected Delivery; without one continue in explicit-task mode. Session failure after
creation does not erase a durable task. If output was lost, use only
`recover-created-task-result`; it rereads the task, branch binding and
resource ownership without creating a second task or checkout. It reads the
current session route first: the same task remains unchanged, a missing record
may retry the official attach, and a different or invalid current route blocks
without overwriting it. Return to `guru-bind-task-session` for an explicit
task switch or rebind. Recovery returns `created` only after the same binding,
a completed missing-record attach, or explicit-task mode is current.

Return exactly one exit: `created -> guru-task-created`, `refresh_review ->
guru-sync-base` for changed base authority or a stale creation date, `blocked ->
task-creation-blocked`, or `invalid_task_state -> invalid-task-state`.
An unchanged base with invocation branch HEAD mismatch is blocked; a changed
acquisition route requires a new semantic review. Never use task/workspace
mappings, `task.json.branch` or checkout paths as durable identity.

Metadata, occupied-identity and base/acquisition failures may carry one optional `diagnostic`
with `field_path` and `remediation`. The declared stop consumer uses these
call-local facts to explain the exact failing record and its disposition; they
are not task identity or a persisted inventory. Preserve the reason code and
stop. For unsupported old/mixed records, use `guru-upgrade-installation` for
reviewed per-record migration or manual disposition; never silently skip,
convert, or delete the record. Old minimal blocked/invalid outputs remain valid.

Read `.trellis/spec/workflow/companion-scripts.md#intermediate-command-stdout-10` for receipts and `result` projection.
Only the declared public invocation emits a formal exit; follow its consumer and positive-exit conditions.

## Existing-Issue ready projection

For the independent Issue ready result, copy issue into reviewed_source's
kind=issue/repo_ref/number; this owner reviews disposition as exact_source or
reference_only. Copy all three base_source fields unchanged into
creation.reviewed_base_source. Do not reconstruct readiness_current. Independently
review creation.selected_base_ref as the Task integration branch and delivery_target
as the future delivery repository/branch. Neither comes from source selected_ref.
Current public profile 2.0 and shared Creation 3.0 remain selected. Preserve
acquisition.decision_head=reviewed_base_source.commit, original checkout/resource
conditions and same-result recovery. For synced_branch preserve normalized source
branch equality; only a new creation additionally checks its current branch HEAD.
A fixed git_object source does not require primary clean or latest same-name ref.
