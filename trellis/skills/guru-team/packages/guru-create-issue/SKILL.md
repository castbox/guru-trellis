---
name: guru-create-issue
description: Use when the user asks to create, open, or file a GitHub Issue, including 新建 issue、创建 Issue、新增 Issue、提 Issue and contextual confirmation such as 同意新建 issue. Load the required upstream review before creating one reviewed Issue, or recover its exact result read-only.
---

# Create Issue

Before substantive output, read `.trellis/spec/workflow/clear-technical-writing.md`
in full and apply it within this entry's existing scope. Until that read succeeds,
use only short progress messages or concrete missing-dependency diagnostics.
State the current action or missing item; make no unverified claim. If the file
cannot be read, pause substantive output, then read it and resume the same
request when available. No additional approval is needed for that recovery.

## Intent Entry

Load this Skill when the user requests GitHub Issue creation in natural
language or explicitly names it. Recognize equivalent intent semantically;
the description examples are not an exhaustive keyword list. A contextual
confirmation such as “同意新建 issue” retains the actual proposal and scope
from the current conversation. Quoting these phrases to discuss this Skill
is not itself an Issue creation request.

Loading the Skill does not satisfy its creation preconditions. If the current
`guru-review-change-request:ready` transition for `proposed_draft` is missing,
return control to the current workflow's initial Intake or applicable active
scope owner to obtain the actual upstream review, then invoke this Skill
with that result. Do not fabricate a transition or bypass this owner with
`gh issue create` or a provider create call. Retain the user's Issue-only
scope; Issue creation does not authorize Task, branch or worktree creation.

## Reviewed Creation

Read `.trellis/spec/workflow/workflow-contract.md#interaction-budget` before
any confirmation, choice or clarification. This Skill retains its own action
plan, confirmation boundary and execution/recovery contract.

`judgment_mode=semantic`. Accept only a current
`guru-review-change-request:ready` transition whose `target.kind` is
`proposed_draft`. Before mutation reread the selected repository, title,
body, labels and duplicate disposition. At this Skill's AI review gate, capture
`reviewed_label_identity_sha256` by canonically digesting the reviewed target's
`identity_sha256` and the sorted, unique, case-folded reviewed label names:
`{"reviewed_target": target.identity_sha256, "labels": sorted_label_set}`.
Keep this review-time identity unchanged across creation and read-only recovery;
never derive it from a changed invocation draft. The runtime independently
recomputes it from `draft.labels`. The input carries the exact reviewed
target digests; any repo, title, body or label-identity drift returns
`refresh_review` before provider access. The current conversation must show
the exact GitHub Issue side effect. Do not create a Trellis task here.
Capture a UTC `reviewed_at` when the current duplicate decision is made and
reuse that same value on output-loss recovery; an older same-content Issue is
not this creation result. GitHub's `createdAt` readback has second precision:
creation waits until the next whole second after `reviewed_at`. The creation
call accepts only a current review no more than 60 seconds old; future or
older reviewed times require fresh review. Read-only output-loss recovery
reuses the original time without that creation freshness limit.

Record the reviewed plan, execute one Issue creation, then reread the live
Issue and verify its number, URL, state and full draft content. Creation adds
a stable, non-secret hidden Markdown comment derived from the reviewed target
identity and UTC review time. This marker is the creation-attempt identity;
the visible draft text is unchanged. Output loss
uses `recover-created-issue-result`: search from the reviewed time by draft
title, then require one live body (including that exact marker), state and
case-insensitive label identity
match with `createdAt` at or after the next whole second following
`reviewed_at`. This same lower bound applies to creation reread and recovery;
zero or multiple matches fail closed. Do
not retry mutation. `check-issue-creation-result` is read-only.

`created -> guru-sync-base -> fresh Intake`. `refresh_review ->
guru-sync-base`, `blocked -> issue-creation-blocked`. A created Issue is only
an Intake candidate; it never goes directly to task creation. The output
contains only repository, number and URL.

Read `.trellis/spec/workflow/companion-scripts.md#intermediate-command-stdout-10` for receipts and `result` projection.
Only the declared public invocation emits a formal exit; follow its consumer and positive-exit conditions.
