# #481 Task Personnel Retirement Test Strategy

State: task-owned Phase 2 candidate; passing commands alone do not constitute the semantic gate.

- `T481-01`: Real source-lock validator checks exact Git HEAD, ordered parents, tree, clean tracked state, remote, package manager, CLI/core versions, built templates and matching successful CI run.
- `T481-02`: Issue-backed and no-Issue task creation use the current upstream CLI without personnel fields; public schema rejects both old fields and generated task JSON passes the official schema.
- `T481-03`: Existing personnel-bearing archives reserve TaskIds without blocking unrelated current tasks. Explicit TaskId and exact Issue clues return only a rejection diagnosis; conflict, duplicate, missing and non-exact source cases remain distinct.
- `T481-04`: #454 session bind/switch/rebind/Finish retirement, branch establish/rebind/retirement, checkout resolution and caller/guru resource ownership regressions pass for schema-valid current tasks.
- `T481-05`: Task-free brainstorm reaches requirements clarification without task mutation, while Guru task creation and activation remain separate owners.
- `T481-06`: Canonical/dogfood/installed equality, declared platform loading, preset reapply/drift, sidecar and mode checks use one representative clean installation from the selected Fork build. Full multi-platform Release/upgrade matrix remains with its separate owner.
- `T481-07`: Scan current workflow, skills, scripts, schema, examples, config and README for personnel behavior, distinguishing historical migration prose and independent platform/resource owners.

## Candidate Evidence

- Exact Fork source validation: `castbox/Trellis@64fe9a15a68df1add3a2a7fd182f3d84e6eba4ac`, tree `a964088ffa3f8df0deafc8f042f91911e3e8ecbe`, CLI/core `0.7.0-castbox.1`, successful CI run `36755826713`.
- Current package/runtime: task lifecycle 152/152; create-task against that Fork 13/13; Reactivate 25/25; Finish 56/56; session 8/8 with one skipped environment case; checkout 4/4; branch 3/3; installer 101/101; compatibility contract 73/73.
- Installed sample: one Codex clean focused install passed native projection loading, initial preset apply, two reapply operations, same-candidate update, template-hash preservation and session binding. Dogfood drift passed and no `.new`/`.bak` remained.
- Historical pre-434 task-workspace transcript requires a removed package and is not a current install gate; running it against this candidate yields three missing-package errors. The complete multi-platform Release/upgrade matrix, predecessor-upgrade matrix, public remote marketplace and production installs remain unverified.
