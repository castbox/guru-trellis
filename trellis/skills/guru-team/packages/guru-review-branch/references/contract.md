# guru-review-branch contract

## Public entry

The only profile is `branch_review`. It contains exactly `profile`, `mode`,
`task_ref`, `base_ref`, `committed_head`, and `review_intent`.
`guru-create-task-commit:committed` supplies the last committed identity seed;
the caller AI freshly authors `profile`, `mode`, and one of
`initial_review|finding_fix_review|fresh_final_review`.

Workflow and standalone modes both require, in order:

1. runtime dependency;
2. workspace boundary;
3. task identity;
4. commit handoff;
5. planning approval;
6. Phase 2 check;
7. issue scope ledger;
8. Docs SSOT outcome;
9. complete review range;
10. clean or review-metadata-only working tree;
11. reviewer assignment and recovery;
12. raw review evidence;
13. invocation freshness.

The runtime reads all private evidence from the resolved active task. The public
input never embeds planning, Phase 2, ledger, Docs SSOT, assignment, report,
finding, range, hash, or digest bodies.

## Semantic stages

### Forward behavior

Create an independent-review handoff covering the exact task, current full
range, requirements, approved planning, Docs SSOT result, Phase 2 result,
deployment/safety surfaces, and the public-package/private-runtime boundary.
Dispatch the official unchanged check/review agent. Preserve each raw report in
`reviews/*.md`, plus assignment/liveness/recovery evidence.

### Qualification before severity

For every candidate, record affected behavior/path/evidence and bind its
requirement, approved planning rule, necessary correctness/compatibility
invariant, or explicitly confirmed expansion. Then select exactly one scenario:

- `normal_required_behavior`
- `explicit_nonstandard_requirement`
- `approved_nonstandard_expansion`
- `unconfirmed_nonstandard_proposal`
- `out_of_scope`

Only the first three may become `qualified_finding` and receive P0-P3. An
unconfirmed proposal becomes `scope_proposal`, has no severity, and requires
dedicated clarification. Out-of-scope candidates become observation,
follow-up, or rejection. Ordinary continuation, planning approval, or reviewer
severity is not expansion confirmation. A risk created only by an unnecessary
mechanism should first be resolved by removing or replacing that mechanism.

### Finding closure and final review

Each qualified finding binds requirement refs, scope basis, scenario class,
qualification reason, severity, owner round, reviewed HEAD, status, and closure
evidence. The implementation owner repairs it, then a complete Phase 2 and task
commit run occur before a closure round. Same-agent closure needs explicit
continuity evidence; replacement needs a complete recovery chain.

When all findings are closed, a fresh final reviewer that did not perform
closure reviews the complete final range. The final round is last, current,
zero-finding, and linked from `review.md`. Missing reports, digest mismatch,
round gaps, stale HEAD, unfinished replacement, open closure findings, or
reviewer reuse block.

### Recorder, checker, and exit

The AI owns the semantic Gate. `review-branch` records it into the existing
artifacts; `check-review-gate` validates only objective structure, identity,
range, HEAD, hashes, report retention, lifecycle, freshness, and exact exit.
No second Branch Review pass artifact is allowed.

Return exactly one:

- `passed`: minimal planned publication seed;
- `implementation_required`: current finding refs;
- `scope_confirmation_required`: exact proposal refs;
- `blocked`: routing identity only.

Unknown, multiple, stale, or unmapped results fail closed.

## Upstream and runtime boundaries

Never modify or overlay upstream `trellis-check` Skill/Agent files. The package
owns the reviewer prompt and qualification contract. Public wrappers are
dispatcher-only and never import `guru_team_trellis.py`, eval assets, or private
review artifacts. `expected_exit` is only a runner assertion after actual
wrapper output.
