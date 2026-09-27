---
name: guru-create-issue
description: Create one reviewed proposed GitHub Issue, or recover its exact result read-only.
---

# Create Issue

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
