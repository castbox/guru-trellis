# Guru Check Task Contract

## Ownership

`guru-check-task` is the sole semantic owner of the complete Phase 2 check. It
uses `judgment_mode=semantic`. Official Trellis workers and repository commands
provide ephemeral evidence; they do not own the Guru result and do not create a
handoff, assignment, liveness record, or raw review artifact.

Workflow and standalone mode use the same owner loop. Any real side-effect
authorization remains only in the current conversation and is never recorded.

## Public Entry

Public input schema 2.0 is a minimal route DTO:

- `initial_check` identifies the current implementation-complete entry;
- `finding_fix_rerun` carries only the finding references whose fixes require a
  complete current-scope rerun;
- `planning_reentry` identifies a refreshed planning route.

The caller does not submit semantic conclusions, findings, raw evidence, an AI
gate, or an exit. Eval cases likewise choose a staged semantic case outside the
public input and assert the actual exit only after the owner result returns.

## Semantic Loop

1. Reread the current task, approved plan, live authority, issue scope, diff,
   dirty paths, code, tests, docs, and applicable validation commands.
2. Perform early candidate hygiene over the committed task-base diff, staged,
   unstaged, untracked, and new files before expensive or external validation.
3. Classify each candidate on supported normal behavior. Only current-scope
   candidates receive P0-P3 findings; scope changes route to planning and
   excluded hostile or deliberately forged cases remain out of scope.
4. Review requirements, design, implementation, tests, Docs SSOT, cross-layer
   behavior, compatibility, deployment/operations, and verification
   completeness.
5. After a finding fix, perform one current complete semantic round. Do not
   persist each worker round or require historical HEAD equality.

AI-owned delta classification decides which conclusions actually changed.
Equivalent formatting, links, derived text, OS noise, and stale downstream
workflow projections do not trigger an unrelated full replay. Real semantic
changes, unknown dirty content, missing checks, or reproduced findings do.

## Private Result

New evidence uses schema `guru-phase2-check-3.0` in ignored runtime. It retains
only task and checked content identity, one composite
`reviewed_worktree_sha256` freshness token, reviewed path locators, validation
summaries and unverified items, Docs SSOT conclusion, nine-dimension semantic
result, scope decisions, findings, route, reason, and consumer.

It does not retain implementation handoffs, worker identity, raw output,
assignments, liveness, repository snapshots, per-file digests, artifact-digest
bundles, or authorization. The one composite token has a direct local consumer:
the checker invoked inside this Skill's public wrapper before typed-output
projection. A mismatch returns to this owner for AI delta classification; it is
not authorization, semantic approval, a public DTO field, cross-Skill authority,
or a digest chain. After the checked typed output passes its output schema, the
same producer wrapper deletes the checkpoint. Task Commit consumes only the
minimal `passed` DTO and live Git facts; it never reads or deletes Phase 2 private
state. Schema 2.0 and 2.1 artifacts are read only to detect one-time AI-first
re-entry; new execution does not regenerate their fields.

## Recorder And Validator

The recorder writes the completed semantic result and derives the one composite
worktree-content token. The validator recomputes that token before public output
projection and checks closed schema shape, task/planning linkage, reviewed dirty-path
coverage, checked HEAD or allowed task-commit ancestry, finding/scope linkage,
and exit/consumer invariants. It never decides scope, severity, sufficiency,
Docs SSOT, semantic pass, or route.

The ignored runtime result is distinct from the public DTO. `passed` projects
only `task_ref` and `checked_head` to `guru-create-task-commit`; finding and
planning routes project only their direct consumer references.

## Exits

- `passed`: all nine dimensions pass with no open finding or blocking
  unverified item.
- `implementation_required`: A current-scope finding returns to implementation.
- `planning_stale`: a current scope or authority change returns to planning.
- `blocked`: a concrete evidence or dependency gap prevents a reliable result.

Mapped re-entry is automatic. Unknown, multiple, stale, ambiguous, or
consumer-mismatched exits fail closed without a routine user prompt.
