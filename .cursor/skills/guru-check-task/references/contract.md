# Guru Check Task Contract

## Ownership

`guru-check-task` is the semantic owner of the complete Phase 2 check and the
single tracked `phase2-check.json`. Workflow and standalone mode use the same
ten preconditions and the same stage order: forward behavior, AI review gate,
conditional confirmation, recorder/checker, then one typed exit. Official
`trellis-check` workers return ephemeral evidence; they do not own Guru pass or
write an additional handoff/report artifact.

## Semantic Loop

1. Validate the current workspace, active task, approved planning, provenance,
   Docs SSOT plan, issue ledger, repository inputs and invocation freshness.
2. Read the complete scope, implementation terminal result, current diff,
   code, tests, docs/specs, repository-defined validation commands and any
   unresolved verification.
3. Run every applicable check. Record exact argv, exit code, output digests and
   a concrete result summary. Record a specific reason and impact for an
   intentionally omitted check.
4. Classify each candidate before severity. P0-P3 applies only to supported
   current-scope behavior. A scope-changing candidate routes to planning;
   follow-up and out-of-scope candidates do not block or authorize work.
5. Review nine adequacy dimensions: requirements, design, implementation,
   tests, Docs SSOT, cross-layer behavior, compatibility,
   deployment/operations and verification completeness.
6. Complete the AI gate. A current-scope finding returns
   `implementation_required`; changed planning/scope returns `planning_stale`;
   unavailable reliable evidence returns `blocked`.
7. After implementation changes, run one full new round over the complete
   scope and current repository. A latest-chunk-only rerun cannot pass.

Routine assignment, liveness, progress, completion and recovery bookkeeping is
not entry evidence. A real unfinished-to-replacement event may use the separate
gitignored recovery checkpoint, but that checkpoint does not become a Phase 2
dimension or tracked handoff.

## Artifact Boundary

New evidence uses `schema_version=2.1` and schema id
`guru-phase2-check-2.1`. It binds planning/provenance, Docs SSOT, the embedded
implementation evidence collection, repository snapshot, checks, scope
qualification, nine adequacy dimensions, findings, unresolved verification,
AI gate, route, consumer, full-round identity and `facts_sha256`.

`implementation_handoff` remains the public input id for compatibility, but it
is an embedded evidence collection assembled from terminal output and live
facts. It never requires `implementation-handoff.md`.

Recorder/checker code validates objective schema, paths, hashes, sizes, HEAD,
diff, dirty state, planning/ledger linkage, full-round identity and
exit/consumer invariants. It never decides scope, severity, sufficiency, Docs
SSOT consistency, semantic pass or route. Existing schema 2.0 artifacts remain
read-only compatible. Re-entry writes 2.1 and drops legacy assignment/recovery
fields and dimensions.

Post-commit consumers may accept the recorded HEAD as an ancestor only when
later committed paths are the reviewed task commit and no unreviewed
non-metadata dirty path exists. They do not re-record Phase 2 solely to match a
Git commit that contains its already reviewed changes.

## Exits

- `passed`: all nine dimensions pass, no open finding or blocking unverified
  item remains, and the consumer is `guru-create-task-commit`.
- `implementation_required`: one or more current-scope findings return to the
  implementation route.
- `planning_stale`: the checked discriminator routes to plan reapproval or
  requirement clarification.
- `blocked`: a concrete evidence/dependency blocker stops the workflow.

Mapped re-entry is automatic. Unknown, multiple, stale, ambiguous, unmapped or
consumer-mismatched exits fail closed without a routine user prompt.
