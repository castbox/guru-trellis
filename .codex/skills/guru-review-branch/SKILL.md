---
name: guru-review-branch
description: Review a committed task branch or bounded base delta through independent semantic review and five typed exits.
---

# Guru Review Branch

Use this Skill after `guru-create-task-commit:committed` and before publication.
Read [references/contract.md](references/contract.md) completely before acting.

Before searching the range, Docs, tests, fixtures, consumers, or relevant
history, read `.trellis/spec/workflow/semantic-retrieval.md` and apply it in
candidate qualification. A negative finding or impact conclusion cannot rely
on a single-language zero result, and no query process enters the gate or DTO.

Validate all eight entry preconditions in workflow or standalone mode. Perform one
independent semantic review of the complete current range and qualify every
candidate before assigning severity.
Scripts never decide scope, scenario class, qualification, severity,
review sufficiency, pass, or route.
When current-scope evidence disproves a candidate, preserve it as
`rejected_candidate` without severity or finding-only fields.

Current-scope qualified findings return `implementation_required`; fixes must
pass the applicable checks, a fresh task commit, and this Skill again. An
unconfirmed nonstandard proposal returns `scope_confirmation_required` and
cannot become a finding. After a fix commit, the finding owner or a real
unfinished-agent replacement performs closure as an internal transient
judgment. It retains `introduced_head`, binds the fixing `fix_head`, and
produces a later `closure_head` plus concrete closure evidence. The AI workflow
then automatically dispatches a distinct fresh reviewer over the complete
current `origin/<base>...HEAD` range.

Closure emits no public exit and writes no artifact. Only the distinct
`fresh_final_review` may reach the recorder and pass. After its AI Review Gate
exists, the recorder may write the compact `review-gate.json`; it does not
create assignment, liveness, rollup, or raw per-round reports. Only after
`check-review-gate` passes
may the public wrapper emit exactly one of `passed`,
`continuity_passed`, `implementation_required`,
`scope_confirmation_required`, or `blocked`.
`passed` targets the active `guru-review-task-publication` Skill through its
target-owned authoring seed. The workflow caller performs the publication
content authoring preparation required by the global Phase 3.6 order before
invoking that active owner.
This package is not self-contained or portable.

Aggregate public input schema 3.0 dispatches two profiles: `branch_review`
schema 2.0 accepts only `initial_review` and `fresh_final_review`, while
`base_continuity` schema 1.0 accepts only `base_continuity`. The owner-private
gate is current-only schema 4.0 and records profile-specific identity plus
`review_commit` and `reviewed_content_sha256`. Aggregate input schema 2.0 and
gate schema 3.0 remain legacy compatibility inventory, not current runtime
authority. Any other current gate shape or input field fails closed through
the normal invalid-input path. The commit is used for range and finding
ancestry; the reviewed-content identity alone owns content freshness.
