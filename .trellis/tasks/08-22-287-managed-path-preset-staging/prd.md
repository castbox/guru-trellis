# #287 重构 Guru Team preset staging，避免全仓库物理复制导致磁盘占用线性增长

## Goal

Implement canonical managed-path preset staging while preserving #286 lifecycle, transaction, sidecar, installed validation, update/reapply/drift, and atomic recovery semantics.

## Requirements

- Replace the current `shutil.copytree(repo, staging_repo)` transaction input with a canonical managed-path inventory. Only preset-owned source files, managed target preimages, transaction metadata, and declared conflict/recovery sidecars may be materialized in the controlled #286 temporary root.
- Reuse the #286 temporary root, registered prefix, stale reaper, explicit caller workdir, normal cleanup, and diagnostic-retention contract. Do not add another reaper, broad temporary-directory scan, or whole-repository fallback.
- Preserve user-modification protection, `.new`/`.bak`/unknown-sidecar handling, installed manifest/content/mode/provenance validation, per-target activation and recovery, preimage binding, repeated reapply idempotency, official update followed by reapply, and source-repository non-mutation.
- Add deterministic managed inventory and space-preflight/observability facts: selected strategy, controlled root, managed file count/bytes, estimated peak bytes and safety margin, available space, staged/backup/sidecar bytes, and cleanup disposition. Fail before large writes when the managed transaction cannot fit.
- Keep public workflow/preset/template/asset identities stable unless a versioned migration is required. Update canonical, dogfood, installed, Shared/Codex/Claude/Cursor, preset and marketplace projections through the existing installer and drift checks.
- Do not modify Trellis upstream, business repositories, or the release/tag surface. #267 remains the owner of the complete multi-platform exact-candidate matrix.

## Acceptance Criteria

- [ ] A representative fixture with nested repository content, dependencies, build output, and untracked files proves staged file count and physical bytes are determined by managed surface rather than total repository size.
- [ ] Unmanaged content is neither traversed for copying nor materialized; there is no silent whole-repository fallback, and source bytes/modes/content remain unchanged.
- [ ] Initial apply, unchanged reapply, user-modified/conflict, `.new`, `.bak`, unknown sidecar, mode migration, preimage drift, partial activation/recovery, repeated reapply, and update/reapply paths preserve current protected semantics.
- [ ] Installed inventory/content/mode/provenance validation remains required before activation; failure recovery processes only the managed action plan.
- [ ] Space preflight fails closed before large writes and reports estimate, available space, strategy, and cleanup disposition.
- [ ] #286 success/failure/signal/stale-next-run lifecycle tests continue to pass with no second reaper or unregistered prefix.
- [ ] Canonical, dogfood, installed, Shared/Codex/Claude/Cursor, preset, marketplace, update/reapply, and overlay-drift projections are synchronized and validated.
- [ ] Targeted Python tests plus one representative clean/isolated fixture pass; no tag or Release is created.

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.
