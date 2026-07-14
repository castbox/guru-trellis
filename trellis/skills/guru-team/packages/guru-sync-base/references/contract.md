# `guru-sync-base` Contract

## Ownership And Modes

The global workflow owns the mandatory invocation and typed-exit consumers.
This package owns the complete step-local loop:

```text
resolve-only -> AI selected-base review -> conditional conflict confirmation
-> digest-bound execute -> mandatory post-execution AI Review Gate
-> objective result validation + result cleanup
-> standalone resolution cleanup | workflow resolution lease transfer
-> typed exit
```

Workflow and standalone modes use identical preconditions. Workflow may use
`skipped` only after tool-free classification proves that the original request
requires no repository or network action. Standalone requires an explicit
refresh/verify request and never returns `skipped`.

## Forward Behavior

Run the `sync_executor` wrapper with `--resolve-only`, `--mode`, repository
root, remote and optional explicit base. The deterministic resolver uses this
order and never consults current branch as a fallback:

1. explicit `--base`;
2. non-empty scalar `base_branch`, or a deduplicated one-value
   `base_branch_candidates` compatibility value;
3. remote default branch from `git ls-remote --symref <remote> HEAD`;
4. exactly one configured fallback candidate with an exact local or
   remote-tracking ref.

Every branch passes `git check-ref-format --branch`. Zero or multiple fallback
candidates return objective blocked evidence. Resolve-only produces canonical
JSON with source, selected base, remote, candidates, decision checkout branch
and HEAD, plus `resolution_sha256`. Any temporary evidence file is outside the
repository and contains no repository absolute path.

## AI Selected-Base Review

Before fetch, the AI reviews:

- whether the invocation intent is repo-changing or an allowed workflow skip;
- whether the resolution source matches the user request and repo config;
- whether the selected base conflicts with an explicit user base clue;
- whether proceeding stays inside the requested repository and declared task boundary.

Only a conflict between user intent and invocation/selected base triggers
human confirmation. A zero/multiple resolution, stale digest, dirty checkout,
or unsafe Git state is not a choice prompt; it returns `blocked`. The user may
start a new invocation with an explicit base.

## Digest-Bound Execution

After review, run `sync_executor --execute` with the exact resolution file and
expected digest. The executor rereads the raw bytes, verifies their digest,
recomputes resolution, and compares the complete object before its first fetch.
It rejects repository-internal or symlink-backed evidence.

Every later `prepare-task` invocation must receive that same external file via
`--resolution-file` and digest via `--expected-resolution-sha256`. Prepare
revalidates canonical raw bytes and recomputes the source-preserving resolution
identity before `gh auth status`, issue/duplicate reads, or fetch. It repeats
the shared guard independently and immediately before GitHub issue, worktree,
and Trellis task mutations. `--base-branch` is only an equality assertion; it
must never turn config, remote-default, or fallback provenance into explicit
provenance. Identity or digest drift blocks before fetch and all later reads or
mutations.

Execution performs only an explicit remote-tracking refspec fetch. An already
equal local base is unchanged. A behind local base can fast-forward only when
it is an ancestor of the fetched remote and the decision checkout is clean and
currently on the selected base; then it uses `git merge --ff-only`. It never
uses `git branch -f`, reset, checkout, stash, rebase, force, or implicit current
branch selection.

Success requires the checkout to remain clean and these full commit ids to be
equal after synchronization:

```text
decision checkout HEAD == local selected-base HEAD == remote-tracking HEAD
```

The executor emits a closed `guru-base-sync-result-1.0` object and
`facts_sha256`, and may write the exact result to a repository-external
temporary file.

## Mandatory Post-Execution AI Review Gate

The AI reviews the result tool output, not a script's return code as semantic
proof. It checks invocation scope, selected-base evidence, actual fetch/
fast-forward side effects, before/after Git facts, and whether any unexpected
effect occurred. The script does not decide scope, sufficiency, semantic pass,
human-confirmation need, or route.

## Objective Validation And Exits

Run `result_validator --evidence-file <external-result>` after the AI Review
Gate. The validator reads only objective facts: component/symlink boundary,
schema identity, closed field shape, facts digest, selected refs, clean state,
and live three-way equality. It never fetches or mutates Git.
After consuming a valid external result-evidence path, it removes that exact
file on validation pass or failure and confirms there is no result residue.

- `synced`: AI Review Gate passed and the result validator passed. Standalone
  first releases resolution evidence. Workflow transfers the exact external
  resolution file/raw bytes/digest as an active lease to
  `guru-discover-change-context`.
- `skipped`: workflow-only AI route review passed and
  `result_validator --mode workflow --record-skipped <route-id>` returned
  stdout-only facts; workflow returns to `original-request-route`.
- `blocked`: resolution, Git, AI review, confirmation, or validator evidence
  cannot prove the contract; stop at `base-sync-blocked`.

Workflow passes that same lease to every later `prepare-task` planner/executor
guard. The unique consumer calls
`sync_executor --release-resolution-evidence --resolution-file <external> \
--expected-resolution-sha256 <digest>` on task-created, blocked, aborted, or
superseded terminal routes. A user-confirmation-pending route is non-terminal
and keeps the lease active. Standalone and every non-`synced` terminal route
release resolution before return. Release revalidates the safe external path,
canonical raw bytes, and expected digest, deletes only the exact file, confirms
absence, and returns structured `already_released` for a repeated safe-path
release.

No result or lease path/digest is written to the repo root, task artifacts,
repo runtime, package, installed runtime, shared cache, README example, or
review evidence. A missing/released lease cannot continue prepare; start a new
explicit Skill invocation instead.

## Runtime Dependency

Both wrappers locate only the installed `run-skill-command` dispatcher and pass
a fixed validator id. The dispatcher proves interface schema 1.1, installed
manifest/runtime API, declared runtime command, managed package inventory and
selected discovery copy before execution. The package is not self-contained or
portable. Missing or drifted runtime and unresolved `.new`/`.bak` sidecars fail
before fetch and require complete Guru Team preset install/upgrade plus source
and installed Skill validation.
