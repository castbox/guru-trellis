# `guru-sync-base` Contract

GitHub platform facts follow the single CLI-only, repo-bound contract in
`.trellis/spec/workflow/workflow-contract.md`; this Skill keeps `git` ownership
of fetch, revision and transport facts.

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

The caller invokes only the public `scripts/invoke.sh --invocation -` wrapper.
Inside that one authoritative invocation, the runtime first executes the
`sync_executor` component in resolve-only mode with the reviewed mode,
repository root, remote and optional explicit base. Resolution uses this strict
order and never consults current branch as a fallback:

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
priority. Current branch and worktree availability never participate in this
selection stage. If no source selects a branch, resolution returns `blocked`.

After selection is complete, runtime reads `git worktree list --porcelain -z`
and binds only the unique registered worktree in the same Git common-dir whose
branch field is exactly `refs/heads/<selected-base>`. The invocation checkout
may be detached. The bound authority must be an exact repository root, remain
symbolically attached to the selected branch, have registered HEAD == checkout
HEAD == local selected-base ref, and be clean. Missing, ambiguous, dirty, or
identity-mismatched authority returns stable `blocked`; runtime never reselects
a lower-priority base and never creates, checks out, or switches a worktree.
Resolve-only emits canonical JSON with source, selected base, remote,
candidates, authority checkout branch and HEAD as the existing
`decision_checkout`, plus `resolution_sha256`, on stdout only. The authority
path remains invocation-local routing state and is not added to the closed
result schema.

## Digest-Bound Execution

Within the same public invocation, the runtime executes the `sync_executor`
component with the same resolution inputs and exact expected pre-sync
resolution digest. The executor recomputes the complete resolution object and
authority binding before its first fetch and rejects any mismatch. Fetch and
any fast-forward run with the authority checkout as their working directory.
After synchronization, it
emits the full `post_sync_resolution` identity and
`post_sync_resolution_sha256`. Already-equal execution may keep the same digest;
fast-forward execution must produce a new digest bound to the synchronized HEAD.

The internal result validator receives the pre-sync digest, validates both
resolution identities, and projects the complete eight-field `base_current`
provenance to Discovery. Compatibility-only `prepare-task` requires that exact
reviewed provenance through `--reviewed-base-provenance '<JSON>'`; optional
`--base-branch` is only an equality assertion. Missing provenance returns
`missing_reviewed_base_provenance` before `gh auth status`, GitHub reads or
fetch. Changed provenance or live base facts return a stable blocking
diagnostic and never start semantic re-intake. `prepare-task` is query-only and
has no GitHub issue, worktree or Trellis task mutation path.

Execution performs only an explicit remote-tracking refspec fetch. An already
equal local base is unchanged. A behind local base can fast-forward only when it
is an ancestor of the fetched remote and the authority checkout is clean and
currently on the selected base; then it uses `git merge --ff-only`. It never
uses `git branch -f`, reset, checkout, stash, rebase, force, or implicit current
branch selection.

Success requires the checkout to remain clean and these full commit ids to be
equal after synchronization:

```text
decision checkout HEAD == local selected-base HEAD == remote-tracking HEAD
```

Here `decision checkout` is the selected-base authority checkout, not the
possibly detached invocation checkout.

The executor emits a closed `guru-base-sync-result-1.0` object,
`post_sync_resolution_sha256`, and `facts_sha256` on stdout. This deterministic Skill has no selected-base AI
confirmation, post-execution AI Review Gate or conditional human confirmation.

## Objective Validation And Exits

The public wrapper internally runs `result_validator` against executor stdout
and the expected pre-sync digest. The validator checks objective schema
identity, closed field shape, facts digest, pre/post resolution identities,
selected refs, clean state, and live three-way equality. It never fetches or
mutates Git. Its internal return may carry the resolved authority locator to the
public wrapper, but that field never enters `guru-base-sync-result-1.0`.

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

All package wrappers locate only the installed `run-skill-command` dispatcher
and pass a fixed validator id. The dispatcher proves interface schema 1.4, installed
manifest/runtime API, declared runtime command, managed package inventory and
selected discovery copy before execution. The package is not self-contained or
portable. Missing or drifted runtime and unresolved `.new`/`.bak` sidecars fail
before fetch and require complete Guru Team preset install/upgrade plus source
and installed Skill validation.

## Interface 1.4 Public Handoff

The public wrapper is `scripts/invoke.sh` and its validator id is
`public_invocation`. Normal workflow invocation is the closed call-local
`scripts/invoke.sh --invocation -` envelope; the declared scalar arguments
remain the compatibility CLI. Direct compatibility entry supplies repository
root and route explicitly; a typed re-entry may omit them, in which case the
owner derives the current repository (`.`) and the only valid re-entry route
(`repo_change`). Runtime
performs the formal resolver, executor, and checker sequence, derives live Git
facts, and serializes one per-exit DTO. The optional `--base-branch` value is the
caller-owned explicit selected-base scalar when present; when omitted, the
wrapper passes the unspecified state to the same shared resolver, which retains
configured scalar/candidate/remote-default fallback ownership. The
private `guru-base-sync-result-1.0` stdout artifact is not projected to consumers.
The existing `handoff_repo_locator` and `transition.repo_locator` fields point
to the authority checkout so Discovery reads only the validator-passed base.
