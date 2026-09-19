# #449 将 Skill tests 视为 package-private，停止分发到业务仓库

## Goal

Keep Skill package tests as canonical source-validation assets while stopping
their distribution into business repositories.

## Requirements

- Canonical `trellis/skills/guru-team/packages/*/tests/` remains available to
  source validation and package-local tests.
- Installed `.trellis/guru-team/skills/packages/*` contains only the public
  runtime/package projection and no package-private `tests/` trees.
- Shared and platform projections continue to exclude package-private tests.
- Reapply/update removes previously managed installed package test copies when
  their recorded managed bytes still match, and records each removal in
  `skill_packages.removals`.
- Local edits to historical test copies are preserved through the existing
  conflict/sidecar path rather than overwritten or silently deleted.
- Installed validation rejects package-private tests in the installed package
  corpus and reports source package tests separately from installed runtime and
  package validation.
- Package contract/spec, installer, manifest/provenance, projection parity,
  update/reapply, and regression tests describe the same boundary.

## Acceptance Criteria

- [ ] Source package tests remain present and source package validation passes.
- [ ] Fresh installation has no `tests/` below installed package roots or
  platform projections.
- [ ] Reapply removes an unchanged historical installed test copy and records
  its removal provenance; a locally edited copy produces a conflict/sidecar.
- [ ] Installed validator fails for an injected installed package test tree and
  passes for the corrected public projection.
- [ ] Manifest/projection parity and targeted installer tests pass without
  claiming package-private tests ran in installed validation.
- [ ] Task validation and `git diff --check` pass; unrelated business-repo
  code and Skill runtime semantics remain unchanged.

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.
