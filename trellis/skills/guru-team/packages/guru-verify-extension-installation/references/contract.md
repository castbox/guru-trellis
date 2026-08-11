# Extension Installation Verification Contract

## Ownership And Entry

`guru-verify-extension-installation` is a source-repository-owned,
standalone-only semantic Skill. Its single current public profile is
`source_repository_verification` in aggregate input 4.0. The caller explicitly
supplies `repo_ref=castbox/guru-trellis`, `remote=origin`, a requested ref, and
`caller_intent=verify-extension-installation`. Task, plan, Publication,
Finalizer, review, business repository, and credential-bearing locator fields
are forbidden.

Before any clone, install, temporary directory, artifact write, or Git/GitHub
mutation, the runtime proves canonical source assets exist, origin normalizes to
`castbox/guru-trellis`, the requested ref resolves to current HEAD, and the
source checkout is clean. Failure returns a stable invocation error with zero
executor calls and zero owner writes.

## Execution And Persistence

After preflight, the executor uses an isolated source checkout and clean
throwaway target for marketplace, preset, workflow, update/reapply, platform,
ownership, redaction, README, and zero-sidecar capabilities. It never clones or
scans a real business task ref. Owner state is ignored source-session runtime
only, is deleted after terminal consumption, and never appears under
`.trellis/tasks/**`.

## Semantic Gate And Exits

The AI owns capability selection, adequacy, findings, and the final route.
Explicit source verification always records `applicability.status=required`;
the current semantic input rejects `not_required` before recorder execution.
Deterministic commands only execute, record, and validate facts. Current exits
are `verified` and `blocked`, both returned directly to the standalone caller;
there is no Finalizer projection, `not_required`, or task-work route.

## Migration

Task-bearing 3.0 inputs, workflow profiles, `not_required`,
`return_to_task_work`, Finalizer projections, tracked
`marketplace-verification.json`, and their recovery contracts are retired.
Legacy schemas/examples, including private result 4.0, remain immutable
compatibility assets but are not in
the current graph. Old input fails closed with remediation to rerun current
Publication/Finalizer preparation rather than being auto-projected.
