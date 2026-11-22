---
name: guru-create-issue
description: Create one reviewed Issue, reread its content and review comment, and recover the same objects.
---

# Create Issue

Before substantive output, read `.trellis/spec/workflow/clear-technical-writing.md`
in full. If it is unavailable, report the exact missing path and resume after
reading it. Read `.trellis/spec/workflow/workflow-contract.md#interaction-budget`
before any confirmation, choice or clarification.

## Intent and content

Load this Skill when the user asks to create a GitHub Issue or explicitly
invokes this Skill. A reply confirming a concrete Issue retains the original
preview and scope. Quoting a trigger phrase to discuss this Skill is outside
this entry.

Start with the direct entry for an Issue-only request. If the original workflow
supplies an actual `ready` result for a proposed draft or the current request
requires complete Intake, use the complete Intake entry.

For either entry, read the full shared content and comment rules from
`.trellis/guru-team/skills/packages/guru-clarify-requirements/references/issue-content.md`
and `.trellis/guru-team/skills/packages/guru-clarify-requirements/references/issue-review-comment.md`.
Review the complete title, body and acceptance criteria against the effective
request and necessary sources. Apply the shared responsibility and acceptance
rules. Review the exact comment against the reviews actually completed. Keep
the current requested scope and applicable evidence across returns.

## Issue-only direct entry

`judgment_mode=semantic`. Verify the target repository with the repo-bound
GitHub CLI. Read the draft, the effective request, and the related sources
that could change the scope or acceptance. Check live duplicate candidates in
that repository. Use the relevant terms and exact identifiers under
`.trellis/spec/workflow/semantic-retrieval.md`. Review candidates that could
change the disposition. When you decide to create a new Issue, capture the
actual UTC time as `reviewed_at`.

If the materials are sufficient, express the established scope and acceptance
in the exact title and body. Decide whether the complete Issue and comment meet
the shared content rules. Clarify owns unresolved intent, scope and acceptance.
Readiness owns unresolved independent delivery and start prerequisites. If a
material gap remains, return the affected question to the original owner with
the still applicable evidence. If the necessary coverage cannot be bounded,
or the original owner requires it, enter the existing complete Intake chain.
Keep the Issue-only scope. Continue only after the applicable review is
sufficient.

After the semantic review and a `create_new` disposition, prepare the input
from a stable conversation-local `draft_id`, the complete reviewed draft,
its exact review comment and the captured `reviewed_at`. Use the
[preparation input example](examples/prepare-input-1.0.json) as the shape and
replace all its values with actual facts.

```bash
pkg=.trellis/guru-team/skills/packages/guru-create-issue
"$pkg/scripts/prepare-issue-creation.sh" --input - < /path/to/reviewed-preparation.json
```

Preparation is read-only. It returns one intermediate receipt with
`formal_exit: false` and the complete `issue_creation_direct` input in
`result`. Preview the exact repository, full title and body, labels and
review comment for one concrete write confirmation. After confirmation pass
the receipt's unchanged `result` to `"$pkg/scripts/invoke.sh" --input -`.
Keep the original receipt and payload in the current call for this action and
its recovery. If a stdin carrier needs a temporary file, keep it outside the
repository and remove it after the consumer finishes.

`direct_review_refresh` returns to this same entry using the original draft
and the reported reason. If `reviewed_time_not_current`, refresh the live
duplicate search and check for relevant changes since review. If the evidence
and visible write remain applicable, retain the completed content review and
its confirmation. If the search still supports `create_new`, prepare the same
draft with the newly observed UTC time. If the disposition changes, complete
the corresponding review before any write. If `reviewed_draft_stale`,
reconcile the pending input against the original reviewed draft or refresh
the affected review. For a changed visible write, present the revised preview
and obtain confirmation.

Both direct refresh reasons mean this invocation stopped before GitHub
access. If an earlier attempt may already have written, use the original
attempt through the shared recovery path.

## Complete Intake entry

`judgment_mode=semantic`. Use `issue_creation` with a current actual
`guru-review-change-request:ready` transition whose `target.kind` is
`proposed_draft`. If that input is required, obtain it through initial Intake
or the applicable active scope owner. Check the exact repository, title,
body, labels and duplicate disposition before mutation. At this Skill's
semantic gate, capture `reviewed_label_identity_sha256` by canonically
digesting `{"reviewed_target": target.identity_sha256, "labels": sorted_label_set}`.
Use sorted, unique, case-folded reviewed label names. Keep this identity
fixed through creation and recovery. Capture the UTC `reviewed_at` when you
decide the duplicate disposition. The
[complete creation input example](examples/public-create-input.json) shows the
draft and comment fields. A stale draft or time returns `refresh_review` to
Sync and fresh Intake.

## Shared execution and recovery

Preview the exact Issue and comment, and obtain confirmation for that write.
From the repository root, pass the reviewed input on stdin to
`.trellis/guru-team/skills/packages/guru-create-issue/scripts/invoke.sh --input -`.
Only this wrapper emits a formal exit. The intermediate receipt contract
is in `.trellis/spec/workflow/companion-scripts.md#intermediate-command-stdout-10`.

Creation requires a current duplicate decision timestamp no more than
60 seconds old. It starts at or after the next whole second following
`reviewed_at` to match GitHub's `createdAt` precision. Waiting for confirmation
may exceed the freshness window. Follow the selected entry's refresh exit
when the wrapper reports it before GitHub access.

The wrapper creates one Issue, then rereads and compares the live Issue
identity and content with the reviewed draft. The executor appends a hidden
attempt marker to the Issue body. After a successful readback, it publishes the
exact review comment and gets that comment by ID. It verifies the comment
body and its parent Issue before returning `created`.

For an argument or JSON error before provider access, correct the named
field and retry the original command. If the writer output is lost or the
provider effect is unknown, retain the actual failure and keep the original
payload and `reviewed_at`. Resolve the tool failure, then invoke the same
wrapper with `action=recover_created_issue_result`. Supply all other
fields from the original execution. Recovery finds the same Issue using the
exact attempt marker, content and next-second lower bound. It then locates the
same comment. When a complete live comment listing shows the comment is absent,
recovery may perform only that remaining comment write. A missing or ambiguous
Issue, ambiguous comment, or mismatched original payload stops recovery.
The original `check-issue-creation-result` command remains read-only.
For an in-flight operation from a pinned pre-comment provider, use its
original recovery contract in MIGRATION-819.

`created` returns the live repository, Issue number and URL. The Issue-only
request ends after comment readback. If the user also requests to start work,
the workflow invokes the original Sync and existing Issue Readiness using the
formal Issue and live comment. Applicable evidence may be reused when its
source and scope still match. That entry makes its own readiness judgment.
`blocked` stops at `issue-creation-blocked`.
