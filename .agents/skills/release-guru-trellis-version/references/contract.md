# Release Guru Trellis Version Contract

## Ownership And Boundary

`release-guru-trellis-version` is a repository-private semantic orchestration
Skill for official `castbox/guru-trellis` releases. Its shared definition lives
under `.agents/skills/` and its Codex, Claude, and Cursor copies are
project-local discovery projections. It is not a public `guru-*` Skill and MUST
NOT enter the Guru Team registry, extension manifest, package tree,
marketplace, preset, overlay, ownership inventory, or a business-repository
installation.

This Skill defines no public interface, schema, runtime, script, checkpoint, or
typed exit. It composes the current owners and consumes only their declared,
fresh results. It never copies, replaces, shortens, or weakens an owner's
semantic gate, freshness check, confirmation boundary, mutation, or
fail-closed route.

## Invocation Input And Fresh Authority

Resolve exactly these six inputs for every invocation:

- repository;
- current release Issue;
- target repository tag;
- target extension revision;
- official Trellis CLI version;
- predecessor tag.

Before either stage, fresh-read the live Issue body, comments, and state;
`origin/main`; local branch and worktree state; tags and GitHub Releases;
version surfaces; and the current contracts of every invoked owner. Reject a
missing or ambiguous input, multiple version mapping, stale fact, cross-SHA
candidate, unprovable lineage, or live identity mismatch. Recovery repeats the
live reads and may use only an owner-private checkpoint that its owner still
accepts as fresh.

## Two-Stage Lifecycle

### Stage 1: Preparation Task And PR

Route preparation through standard intake and the existing global workflow:

1. Planning records stable `prd.md`, `design.md`, `implement.md`, and the Docs
   SSOT plan.
2. Phase 2 changes final delivery content and performs the scoped semantic
   check.
3. `guru-create-task-commit` exclusively owns every task commit preview,
   confirmation, and commit mutation.
4. After the final delivery-content commit, invoke `guru-review-branch` once
   for one independent full `origin/<base>...HEAD` Branch Review.
5. Only a fresh passed Branch Review enters
   `guru-review-task-publication`, which generates and semantically reviews the
   Chinese PR title and body from the live Issue, exact diff, current
   validation, and reviewed-content identity.
6. Only Publication's current minimal result enters `guru-finalize-task`.
   Finalizer exclusively owns its push, PR creation, archive, and Ready
   transaction. Only `guru-finalize-task:ready_for_merge` may enter
   `guru-merge-task-pr`, which exclusively owns expected-head merge and closure
   verification.

The honest path is exactly:

```text
stable_plan -> final_delivery_content -> guru-create-task-commit -> final_delivery_content_commit -> guru-review-branch_once -> guru-review-task-publication -> guru-finalize-task
```

Owner-private lifecycle metadata and the existing Finalizer metadata tail
excluded by `guru-reviewed-content-1.0` do not change reviewed delivery
identity and MUST NOT create a release-status commit, self-reference loop, or
second Branch Review. Any non-allowlisted tracked change returns to task work.

### Stage 2: Post-Merge Exact Candidate

After the preparation PR is merged, discard the preparation branch HEAD,
Branch Review, Publication result, and all earlier release evidence. Fresh-fetch
`origin/main`, prove its live merge/base lineage, and freeze one exact candidate
commit and tree. Every release check and later mutation must bind that same
candidate identity; the preparation reviewed HEAD is never substituted for it.

Before any tag mutation, perform the release Issue's scoped minimum gate. Run
it from the clean candidate checkout with `HEAD` equal to `candidate_commit`,
and bind every command and result to `predecessor_tag` and `candidate_commit`:

| Gate | Stable repository locator and executable entrypoint |
| --- | --- |
| candidate lineage and predecessor-to-candidate full diff | `git rev-parse HEAD`, `git rev-parse "${predecessor_tag}^{commit}"`, `git merge-base --is-ancestor "${predecessor_tag}^{commit}" "${candidate_commit}^{commit}"`, `git diff --find-renames --find-copies "${predecessor_tag}^{commit}" "${candidate_commit}^{commit}" --`, and `git diff --name-status "${predecessor_tag}^{commit}" "${candidate_commit}^{commit}" --` |
| version-axis mapping and public release text | Fresh-read `README.md`, `trellis/guru-team-extension.json`, `.trellis/spec/docs/public-docs.md`, `trellis/workflows/guru-team/README.md`, and `trellis/presets/guru-team/README.md` from the candidate tree; run `git show "${candidate_commit}:trellis/guru-team-extension.json" \| python3 -m json.tool` and `git show "${candidate_commit}:README.md"` and compare the target repository tag, extension revision, and official Trellis CLI version with the six invocation inputs. |
| source and installed validators | `./trellis/workflows/guru-team/scripts/bash/check-skill-packages.sh --root . --mode source --json` and `./.trellis/guru-team/scripts/bash/check-skill-packages.sh --root . --mode installed --json` |
| Shared/Codex/Claude/Cursor parity | Run the source validator once for each stable projection root: `for root in .agents/skills .codex/skills .claude/skills .cursor/skills; do ./trellis/workflows/guru-team/scripts/bash/check-skill-packages.sh --root . --mode source --platform-root "$root" --json; done`, then byte-compare the release Skill's `SKILL.md` and `references/contract.md` across those four roots. |
| ownership, preset, and dogfood drift | `./trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json`, `./trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms`, and `./trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh --repo .`; inspect and reject any unexpected mutation from reapply. |
| install/update/reapply checks | Run the existing single-repository compatibility profile against the exact candidate: `GURU_TEAM_THROWAWAY_SINGLE_REPO_COMPATIBILITY=1 TRELLIS_WORKFLOW_SOURCE="gh:castbox/guru-trellis/trellis#${candidate_commit}" ./trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`. This one clean Shared/Codex/Claude/Cursor install plus existing-project update/reapply flow is the ordinary Issue's targeted proof, not the verifier's default cumulative multi-platform Release Gate matrix. |
| secret scan | Derive the exact changed-file set with `git diff --name-only --diff-filter=ACMRT "${predecessor_tag}^{commit}" "${candidate_commit}^{commit}" --` and run the current environment's real secret-scanning capability over those candidate file bytes. A missing scanner, incomplete file set, alert, or unavailable result is `SKIP` or `FAIL`, not a pass. |
| residue check; residue and diff hygiene | `git status --short`, `git diff --check`, and `find . \( -type d -name '__pycache__' -o -type f \( -name '*.pyc' -o -name '*.pyo' -o -name '*.new' -o -name '*.bak' \) \) -print`; any unexpected output is blocking. |

After these deterministic results are current, independently review the full
diff, version mapping, command outputs, secret-scan result, residue result, and
unverified boundaries. This Skill MUST NOT replace these targeted locators with
an ad hoc command set and MUST NOT expand the task into the cumulative
multi-platform Release Gate matrix owned by a dedicated Release Gate Issue.

Immediately before the GitHub Release mutation, generate the Release title and
body from the live Issue, exact candidate diff, current validation evidence,
and candidate identity, then perform semantic review. Do not create a
task-local body handoff.

## Reviewed-Content Freshness

Use the existing `guru-reviewed-content-1.0` owner contract. Changes to actual
delivery bytes, durable README or Docs authority, configuration, schema,
scripts, or tests make every affected Phase 2, Branch Review, Publication,
Finalizer, or exact-candidate gate stale and require its owner to rerun.

Changes confined to `.trellis/tasks/**`, `.trellis/workspace/**`,
`.trellis/.runtime/**`, `.trellis/guru-team/extension.json`, or `.DS_Store`
remain lifecycle/provenance metadata only when the current owner contract
allows them. They do not refresh, repair, or prove a gate. Metadata commits are
never used to record or recover release progress.

## Forbidden Persistence

MUST NOT create task-local `release-notes*.md`, a PR or Release body handoff,
or a dynamic checkbox checklist in `implement.md`. `implement.md` remains a
stable implementation plan.

MUST NOT write tracked lifecycle state containing HEAD, timestamps, phase
progress, Gate pass/fail, finding closure, candidate status, tag status, smoke
status, GitHub Release status, or user authorization. Authorization exists only
in the current dialogue and is never reused, serialized, hashed, or persisted.

## Independent Mutation Confirmations

Each mutation is a separate boundary. Immediately before that one action,
fresh-read its authority, display the exact repository/object/ref/SHA, command,
files or remote objects affected, and expected result, then obtain confirmation
that authorizes only that displayed action:

| Mutation | Exclusive owner or boundary |
| --- | --- |
| task commit | `guru-create-task-commit` |
| branch push | `guru-finalize-task` exact transaction boundary |
| PR creation | `guru-finalize-task` exact transaction boundary |
| Finalizer archive and Ready mutations | `guru-finalize-task` |
| preparation PR merge | `guru-merge-task-pr` |
| annotated tag creation/push | post-merge tag boundary |
| tag-pinned smoke | post-tag smoke boundary |
| GitHub Release creation | post-smoke Release boundary |
| release Issue closure | Issue closure boundary |
| branch/worktree/task cleanup | cleanup boundary |

Confirmation for one row cannot authorize, pre-authorize, or be reused for any
other row. In this repository-private release route, branch push, PR creation,
and the Finalizer archive/Ready mutation MUST each be displayed in a separate
confirmation request and MUST each receive its own current-dialogue answer
immediately before that row executes. An atomic or bundled Finalizer preview or
answer MUST NOT authorize actions from more than one table row, even when the
underlying owner can execute them as one transaction. Keep `guru-finalize-task`
as the unchanged semantic and mutation owner, use only its existing public I/O
and same-owner recovery, and add no public Finalizer field, exit, consumer, or
owner; this private orchestrator only imposes the stricter per-row interaction
boundary before allowing the owner to continue. A failed action does not
authorize a retry. Tag, smoke, Release, Issue closure, merge, and cleanup remain
independently reviewable even when the same user performs them consecutively.

## Fail-Closed Stops

Stop in the current owner before later publication or release side effects on
stale evidence, cross-SHA evidence, `FAIL`, `SKIP`, identity mismatch,
unsupported input, or an unknown, multiple, ambiguous, consumer-mismatched, or
unmapped exit. Do not guess a route and do not create a metadata commit to mark
the stop or resume point.

This contract never itself runs a real commit, push, PR, merge, tag, smoke,
GitHub Release, Issue closure, or cleanup mutation. Those actions remain with
their named owner or explicit post-merge boundary and require the independent
current-dialogue confirmation above.
