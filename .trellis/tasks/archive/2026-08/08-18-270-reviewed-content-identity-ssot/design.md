# #270 Technical Design

## 1. Architecture

新增 shared deterministic module `trellis/skills/guru-team/runtime/reviewed_content.py`，作为 `guru-reviewed-content-1.0` 唯一代码实现。四个 package runtime 通过受管 shared runtime import 调用；package-local runtime 不再定义 metadata classifier、tree entry builder 或 digest algorithm。

```text
Git commit/worktree
      |
      v
shared reviewed_content helper
  - metadata exclusion
  - tree/worktree/gitlink normalization
  - path-byte sort
  - {path, mode, oid} rows
  - guru-reviewed-content-1.0 digest
      |
      +--> Branch Review checkpoint
      +--> Publication continuity
      +--> Finalizer continuity
      +--> Verifier target continuity

base ref/commit/range/ancestry checks remain package-owned and separate
```

## 2. Canonical Contract

Canonical digest payload is a closed JSON object:

```json
{
  "algorithm": "guru-reviewed-content-1.0",
  "entries": [
    {"path": "...", "mode": "100644", "oid": "..."}
  ]
}
```

- Rows are sorted by `path.encode("utf-8")`.
- `path`, `mode`, `oid` are the only row keys.
- `base_commit` and object `kind` are never digest input.
- Tree parsing remains NUL-safe and preserves Git path bytes through strict UTF-8 decoding used by the current contract.
- Worktree overlay、symlink and gitlink behavior remains atomic capability parity with the existing Publication/Finalizer/Verifier algorithm.
- One exported metadata classifier owns task/archive/workspace/runtime/provenance/OS-noise exclusion so status and identity consumers cannot diverge.

## 3. Freshness Separation

The helper accepts a target commit and optional worktree overlay only. It does not accept or judge base ref, base commit, range, ancestry, Issue scope or route intent.

- Branch Review continues to validate reviewed base ref/head, `base...review_commit`, current task branch and finding ancestry.
- Publication continues to validate `branch_review_commit`, current HEAD and reviewed-content continuity.
- Finalizer continues to validate reviewed/publication head ancestry and allowed metadata/provenance tail.
- Verifier continues to bind target repository/ref/HEAD independently from content identity.

## 4. Checkpoint Migration

Branch Review owner-private gate moves to a current-only schema/identity that explicitly binds the canonical algorithm contract. The loader accepts only the new schema. Existing old-shape gates return the stable stale route and are consumed only by a fresh Branch Review; no compatibility reader, on-read rewrite or synthetic gate is added.

## 5. Distribution

Canonical changes begin under `trellis/skills/guru-team/**` and `.trellis/spec/**`. Preset apply synchronizes installed `.trellis/guru-team/**` plus shared/Codex/Claude/Cursor `guru-*` projections. Runtime/extension inventory, package interfaces, schemas/examples/evals and ownership snapshots move together. Generated copies are never edited as independent sources.

## 6. Cross-Package Acceptance

A repository fixture creates one reviewed business commit and calls the actual package wrapper path for Branch Review, Publication, Finalizer and Verifier. The test obtains the digest from runtime output/checkpoint flow, not a copied constant. It proves equal digest at one HEAD, metadata-only stability, included path/content/mode drift, independent base/range/ancestry failures and old Branch Review checkpoint re-entry.

## 7. Compatibility And Rollback

- Public algorithm id remains fixed as required; behavior is corrected to its durable SSOT.
- Owner-private Branch Review schema is current-only and intentionally invalidates old gates.
- Rollback is a Git revert before publication. After merge, reverting would reintroduce cross-stage drift and is not an accepted compatibility path.
- No tag, release, deployment, database, config or external data migration exists.
