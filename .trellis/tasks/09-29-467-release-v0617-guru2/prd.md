# #467 v0.6.17-guru.2 preparation

## Scope and authority

The source is live `castbox/guru-trellis#467`. This task delivers only Stage 1
preparation: version surfaces, validation contract, and Architecture/RDT
contribution and promotion. Stage 2 candidate validation and Stage 3 tag,
smoke, Release, and Issue closure remain owned by the open Issue after this
task's reference-only Delivery, Completion, Closure, Finish, and Cleanup.
The preparation PR must say `Refs #467` and must not close the Issue.

The six release inputs are repository `castbox/guru-trellis`, Issue `#467`, tag
`v0.6.17-guru.2`, extension `0.6.17-guru.43`, CLI/core `0.6.17`, and predecessor
`v0.6.17-guru.1`. Keep the fixed Fork source at
`castbox/Trellis@8336e78b8fafe2a4bc4ea3d01815a61cf4f08983`.
`main@8abf52ed40eb04280c72c4e20d8be1354c94baeb` is an Intake baseline,
not the eventual release candidate.

## Preparation requirements

1. Update the canonical extension manifest, root README, workflow and preset
   READMEs, public Docs, and affected current projections so all four version
   axes are explicit and consistent. Historical versioned authority and prior
   Release text remain immutable history.
2. Describe cumulative scope from predecessor to the eventual exact candidate.
   Include #459/PR #461, #434/#454 lifecycle capabilities and all other merged
   changes, but treat the final full diff as authority. Do not recast completed
   capabilities as planned or reuse earlier slice validation as release proof.
3. Preserve the repository-private release Skill outside the public extension,
   marketplace, preset, and business-repository install.
4. Correct the observed normal Intake failure: unrelated legacy task residue in
   registered worktrees, historical branch artifacts, and obsolete resource
   ledgers must not block creation of a distinct TaskId. Exact target
   TaskId/TaskRef/resource conflicts must still fail closed.
5. Complete pre-promotion Phase 2 and Task Commit, full Branch Review, then
   serialized Architecture/RDT promotion. Promotion-created delivery bytes
   require fresh Phase 2, Task Commit and a second full Branch Review.
6. Deliver with a Chinese reference-only preparation PR, merge it, then run
   whole-preparation Completion, no-mutation Closure, Finish and Cleanup.
7. In the targeted predecessor-to-candidate existing-install upgrade, remove
   managed Skills, commands, package files and projections retired since
   `v0.6.17-guru.1`. Verify the predecessor's retired Skill IDs are absent
   after update and preset reapply. Preserve a locally modified retired file
   as an explicit conflict; do not silently delete user content.

## Acceptance and boundaries

- Source, installed, Shared/Codex/Claude/Cursor, preset reapply and drift
  checks pass for the Stage 1 candidate. Task and runtime fixes have focused
  tests; the complete current diff receives two applicable independent reviews.
- Stage 1 completion means preparation is merged and archived, not that the
  version is published. The release Issue remains open until exact-candidate
  gates, annotated tag, tag-pinned smoke and GitHub Release succeed.
- Stage 2 must use fresh `origin/main` after Finish bookkeeping. It must prove
  predecessor lineage/full diff, version mapping, source/installed/projection
  parity, ownership/reapply/drift, focused clean install/update, one targeted
  predecessor existing-install upgrade with retired-asset removal, fixed Fork
  build and CLI identity, changed-file secret scan, and clean residue.
- Full multi-platform Release matrix, marketplace, business-repository
  production install, npm publication, and infrastructure/database changes are
  outside this Issue's verification claim.

## Docs SSOT plan

Use task-local Architecture and Requirements/Design/Test contributions for the
current release mapping and observed Intake normal-path correction. Promote
them only after a passed pre-promotion full Branch Review. Update current
public locator projections after promotion, preserving historical versions.
`README.md`, the two distribution READMEs, and `.trellis/spec/docs/public-docs.md`
are the release-facing Docs authority. No task-local release notes, dynamic
progress checklist, tracked release-state artifact, or authorization record.
