---
name: guru-review-branch
description: Review a committed task branch through independent review, an internal closure-then-fresh-final loop, and four typed exits.
---

# Guru Review Branch

Use this Skill after `guru-create-task-commit:committed` and before publication.
Read [references/contract.md](references/contract.md) completely before acting.

Validate all 11 entry preconditions in workflow or standalone mode. Perform one
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
judgment. It retains `introduced_head` and produces `resolved_at_head` plus
concrete closure evidence. The AI workflow then automatically dispatches a
distinct fresh reviewer over the complete current `origin/<base>...HEAD` range.

Closure emits no public exit and writes no artifact. Only the distinct
`fresh_final_review` may reach the recorder and pass. After its AI Review Gate
exists, the recorder may write the compact `review-gate.json`; it does not
create assignment, liveness, rollup, or raw per-round reports. Only after
`check-review-gate` passes
may the public wrapper emit exactly one of `passed`,
`implementation_required`, `scope_confirmation_required`, or `blocked`.
`passed` targets the active `guru-review-task-publication` Skill through its
target-owned authoring seed. The workflow caller performs the publication
content authoring preparation required by the global Phase 3.6 order before
invoking that active owner.
This package is not self-contained or portable.

Public input schema 1.1 accepts only `initial_review` and
`fresh_final_review`. A legacy `finding_fix_review` intent is migrated by
completing closure internally and authoring a fresh-final invocation, never by
forwarding that legacy value to the recorder. Schema 2.0 gates and their
tracked reports remain read-only compatible for existing active tasks. New and
re-entered reviews write schema 2.1 only.
