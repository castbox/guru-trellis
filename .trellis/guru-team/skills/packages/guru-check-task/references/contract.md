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
   Git-diff and untracked-text whitespace or blank-EOF findings are suppressed
   only when the bytes in the projection being checked (`HEAD`, index, or
   worktree) exactly match the same repo-relative path's valid schema-v2
   Trellis `.trellis/.template-hashes.json` entry. This covers tracked
   upstream-template migration deltas without letting exact worktree bytes
   exempt a different staged or committed candidate, and without treating the
   digest as semantic authority. Missing, invalid, unknown, or mismatched
   provenance does not exempt the file, and path, UTF-8, and JSON validation
   always remains active.
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

New evidence uses schema `guru-phase2-check-4.0` in ignored runtime. It retains
only task and checked content identity, one composite
`reviewed_content_sha256` freshness token, reviewed path locators, validation
summaries and unverified items, Docs SSOT conclusion, nine-dimension semantic
result, scope decisions, findings, route, reason, and consumer.

It does not retain implementation handoffs, worker identity, raw output,
assignments, liveness, repository snapshots, per-file digests, artifact-digest
bundles, or authorization. The one composite token has a direct local consumer:
the checker invoked inside this Skill's public wrapper before typed-output
projection. A mismatch returns to this owner for AI delta classification; it is
not authorization, semantic approval, a public DTO field, cross-Skill authority,
or a digest chain. After the checked typed output passes its output schema, the
producer retains the checkpoint only for `passed` and deletes it for the other
three exits. Task Commit rereads the retained checkpoint, current content
identity, and commit parent before its candidate and executor proceed, then
deletes the checkpoint after successful publication or successful same-plan
recovery. Failed attempts retain it. Only schema 4.0 is valid; any other artifact
shape is rejected and the owner must run again from the current public profile.

## Recorder And Validator

The recorder writes the completed semantic result and derives the one composite
worktree-content token. The validator recomputes that token before public output
projection and checks closed schema shape, task/planning linkage, reviewed dirty-path
coverage, the current content identity and commit-anchor ancestry, finding/scope linkage,
and exit/consumer invariants. It never decides scope, severity, sufficiency,
Docs SSOT, semantic pass, or route.

The ignored runtime result is distinct from the public DTO. `passed` projects
only `task_ref` and `phase2_commit_anchor` to `guru-create-task-commit`; finding and
planning routes project only their direct consumer references.

## Exits

- `passed`: all nine dimensions pass with no open finding or blocking
  unverified item.
- `implementation_required`: A current-scope finding returns to implementation.
- `planning_stale`: a current scope or authority change returns to planning.
- `blocked`: a concrete evidence or dependency gap prevents a reliable result.

Mapped re-entry is automatic. Unknown, multiple, stale, ambiguous, or
consumer-mismatched exits fail closed without a routine user prompt.
