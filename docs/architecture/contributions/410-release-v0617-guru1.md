# #410 Release v0.6.17-guru.1 Architecture contribution

## Identity And Authority Boundary

- contribution identity: `architecture-contribution-410-release-v0617-guru1-v1` / `candidate`.
- requirement authority: live Issue #410 and task `410-release-v0617-guru1`.
- source predecessor: `v0.6.16-guru.1` / immutable released history.
- change path: `target_native`; ADR required: `false`.

This contribution records the stable architecture boundary for the release
candidate. It does not record task HEAD, dynamic gate results, tag, Release,
Issue closure, time, or user authorization.

## Boundary And Decision

Issue #410 advances the current release-facing mapping to repository tag
`v0.6.17-guru.1` and Guru Team extension `0.6.17-guru.42`, while keeping the
Trellis CLI/core at `0.6.17` and the accepted Fork source lock unchanged.
The repository tag, extension revision, and CLI/source identity remain
independent version axes.

The preparation flow uses one task writer, serialized Architecture/RDT
promotion owners, and a fresh post-promotion review. After the preparation PR
is merged, a fresh `origin/main` commit/tree becomes the only exact candidate
for release gates, tag-pinned smoke, and GitHub Release.

## Required Concerns

| Concern | Applicability | #410 contract |
| --- | --- | --- |
| authority-binding | applicable | Bind current docs and package mapping to Issue #410 and the exact candidate. |
| boundary-and-decision | applicable | Use `target_native`; do not add a release lifecycle owner or public API. |
| owner-and-single-writer | applicable | Task worktree writes delivery; Architecture/RDT owners write shared current authority. |
| compatibility-and-exit | applicable | Preserve existing Skill IDs, exits, schemas, commands, and ownership. |
| evidence-and-freshness | applicable | Recompute Phase 2, commit, review, candidate, tag, smoke, and Release evidence per identity. |
| review-and-promotion | applicable | Promotion-created bytes require fresh Phase 2, task commit, and full Branch Review. |

## Explicit Boundaries

- No new Skill, typed exit, schema, compatibility adapter, or release state machine.
- No Trellis upstream, global npm, `node_modules`, business repository,
  production, database, or infrastructure changes.
- Historical release documents and immutable predecessor facts remain unchanged.
- This candidate contribution does not prove publication, tag creation,
  GitHub Release, or Issue closure.
