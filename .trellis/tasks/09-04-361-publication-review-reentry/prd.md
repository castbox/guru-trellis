# [Bug] Publication Review 保留 owner 错误分类并按变更范围执行精确重试

## Goal

Publication Review must preserve the owner failure that actually occurred and
route recovery according to the changed scope. A ledger/task-content defect
must return to Phase 2 and rebuild downstream reviewed identities; a PR title,
body, or publication-payload defect must remain a Publication-only retry.

## Requirements

- Preserve the stable owner `error_code`, bounded `field_path`, and a stable
  recovery classification in the public Publication error projection.
- Distinguish Issue Scope/authority contract, Publication content contract,
  stale or cross-identity, and runtime/dependency failures. Unknown or
  unmapped classifications fail closed as `internal_error`.
- Perform deterministic Publication preflight for the current PR title/body
  and all contract-required sections, including `影响范围`, `Review Gate`,
  `Docs SSOT`, validation, scope, and follow-up content.
- Keep task-content, publication-only, identity-refresh, and external/runtime
  recovery routes explicit and mutually consistent across workflow, Skill,
  schemas, owner runtime, facade, and projections.
- Do not repeat commit, PR, archive, Ready, or unrelated Branch Review
  mutations/evidence when only Publication content changed.
- Do not create a second Issue Scope Ledger authority, change required-check or
  merge policy, or handle hostile-input/TOCTOU scenarios.

## Acceptance Criteria

- [ ] A sole-disposition/`primary_issue` mismatch returns a stable Issue
  Scope/authority classification with the owner code and the precise field
  path, rather than `internal_error / owner`.
- [ ] Each missing required PR-body section returns a Publication-content
  classification and identifies the relevant payload field/section.
- [ ] Tracked task/code/test/durable-doc changes route through Phase 2,
  Task Commit, Branch Review, and then Publication with fresh identities.
- [ ] PR title/body/publication-only changes re-enter only Publication Review
  and do not create duplicate GitHub or task mutations.
- [ ] Stale, cross-SHA, unknown, and unmapped Publication inputs fail closed;
  old `branch_review_commit` and old ready results are not reused.
- [ ] Canonical, dogfood, installed, Shared, Codex, Claude, and Cursor
  projections are synchronized and pass drift checks.
- [ ] Targeted runtime/schema/contract tests cover every required section and
  every recovery class; the tests do not treat facade `ready` as semantic AI
  approval.
- [ ] The task changes only Issue #361 and records #247/#332/#223 as related
  boundaries, with no closure of adjacent Issues.

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.
