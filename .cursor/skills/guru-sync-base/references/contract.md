# `guru-sync-base` Contract

## Ownership And Modes

The global workflow owns caller-side tool-free route classification, mandatory
invocation, typed-exit consumers, transitions and fail-closed stops. This package
declares `judgment_mode=deterministic` and owns the complete step-local loop:

```text
forward_behavior -> recorder_validator -> typed_exit
```

The Skill accepts normalized mode/route inputs and performs no scope,
sufficiency, finding, revision, user-choice or route-intent judgment. Workflow
and standalone modes use identical Git and runtime preconditions. Workflow may
use `skipped` only for a caller-classified non-repository route. Standalone
requires caller-recognized explicit refresh/verify intent and never returns
`skipped`.

## Forward Behavior

Run the `sync_executor` wrapper with `--resolve-only`, `--mode`, repository
root, remote and optional explicit base. Resolution uses this strict order and
never consults current branch as a fallback:

1. explicit `--base`;
2. non-empty scalar `base_branch`;
3. first existing exact local or remote-tracking branch in configured
   `base_branch_candidates` order, defaulting to `dev`, `develop`, `main`,
   `master`;
4. remote default branch from `git ls-remote --symref <remote> HEAD` when no
   configured candidate exists.

Every entered branch value passes `git check-ref-format --branch`. Lower
priority sources are not evaluated after a source selects a branch.
Multiple existing candidates are not ambiguous: configured order is the
priority. If no source selects a branch, resolution returns `blocked`. Resolve-only emits
canonical JSON with source, selected base, remote, candidates, decision checkout
branch and HEAD, plus `resolution_sha256`, on stdout only.

## Digest-Bound Execution

Run `sync_executor --execute` with the same resolution inputs and exact expected
pre-sync resolution digest. The executor recomputes the complete resolution
object before its first fetch and rejects any mismatch. After synchronization,
it emits the full `post_sync_resolution` identity and
`post_sync_resolution_sha256`. Already-equal execution may keep the same digest;
fast-forward execution must produce a new digest bound to the synchronized HEAD.

The result validator receives the pre-sync digest, validates both resolution
identities, and returns only the post-sync digest to the next consumer. Every
later `prepare-task` invocation receives the same resolution inputs and the
preceding post-sync digest through `--expected-resolution-sha256`. Prepare
recomputes the source-preserving resolution before `gh auth status`,
issue/duplicate reads, or fetch, then repeats the shared guard immediately
before GitHub issue, worktree, and Trellis task mutations. Each guard returns
its post-sync digest for the next guard. Identity or digest drift blocks before
fetch and all later reads or mutations.

Execution performs only an explicit remote-tracking refspec fetch. An already
equal local base is unchanged. A behind local base can fast-forward only when it
is an ancestor of the fetched remote and the decision checkout is clean and
currently on the selected base; then it uses `git merge --ff-only`. It never
uses `git branch -f`, reset, checkout, stash, rebase, force, or implicit current
branch selection.

Success requires the checkout to remain clean and these full commit ids to be
equal after synchronization:

```text
decision checkout HEAD == local selected-base HEAD == remote-tracking HEAD
```

The executor emits a closed `guru-base-sync-result-1.0` object,
`post_sync_resolution_sha256`, and `facts_sha256` on stdout. This deterministic Skill has no selected-base AI
confirmation, post-execution AI Review Gate or conditional human confirmation.

## Objective Validation And Exits

Run `result_validator --result-json <executor-stdout-json>` with the expected
pre-sync digest. The validator checks objective schema identity, closed field
shape, facts digest, pre/post resolution identities, selected refs, clean state,
and live three-way equality. It never fetches or mutates Git.

- `synced`: the digest-bound executor and live Git validator passed; the typed
  result carries `post_sync_resolution_sha256` and workflow enters
  `guru-discover-change-context`.
- `skipped`: caller-side workflow route classification completed and
  `result_validator --mode workflow --record-skipped original-request-route`
  returned validated stdout facts.
- `blocked`: resolution, Git, digest or validator facts cannot prove the
  contract; stop at `base-sync-blocked`.

If the Skill later needs scope, sufficiency, finding, revision, user-choice or
route-intent judgment, its interface must migrate to `judgment_mode=semantic`;
the deterministic profile cannot absorb that behavior.

## Runtime Dependency

Both wrappers locate only the installed `run-skill-command` dispatcher and pass
a fixed validator id. The dispatcher proves interface schema 1.2, installed
manifest/runtime API, declared runtime command, managed package inventory and
selected discovery copy before execution. The package is not self-contained or
portable. Missing or drifted runtime and unresolved `.new`/`.bak` sidecars fail
before fetch and require complete Guru Team preset install/upgrade plus source
and installed Skill validation.
