---
name: guru-review-branch
description: Review a committed task branch through independent review, qualification-first findings, closure, fresh final review, and four typed exits.
---

# Guru Review Branch

Use this Skill after `guru-create-task-commit:committed` and before publication.
Read [references/contract.md](references/contract.md) completely before acting.

Validate all 13 entry preconditions in workflow or standalone mode. Dispatch an
official unchanged check/review agent with the package-owned review prompt,
retain its task-local raw report, and qualify every candidate before assigning severity.
Scripts never decide scope, scenario class, qualification, severity,
review sufficiency, pass, or route.

Current-scope qualified findings return `implementation_required`; fixes must
pass `guru-check-task`, a fresh task commit, and this Skill again. An
unconfirmed nonstandard proposal returns `scope_confirmation_required` and
cannot become a finding. After every finding has closure evidence, dispatch a
fresh final reviewer that did not perform closure and covers the complete
current `origin/<base>...HEAD` range.

Only after the AI Review Gate exists may the existing `review-branch` recorder
write `review.md`/`review-gate.json`, and only after `check-review-gate` passes
may the public wrapper emit exactly one of `passed`,
`implementation_required`, `scope_confirmation_required`, or `blocked`.
`passed` targets the planned `guru-review-task-publication` Skill and therefore
fails closed at the missing-Skill boundary until that package is activated.
This package is not self-contained or portable.
