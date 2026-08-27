# ADR-007: Finalizer extension source and target reviewed checkout binding

状态：`proposed`。Owner：Issue #311。Predecessor：#191 provenance-tail decision。该 candidate 只有在
exact committed range 的 independent Branch Review 与 expected `.40` serialized promotion 通过后才
进入 shared-current authority。

## Context

`guru-finalize-task` 的 pre-PR provenance producer currently creates a detached checkout from the target
repository at `reviewed_content_head` and uses that checkout for two responsibilities:

1. applying and committing the target repository metadata tail;
2. supplying the canonical Guru Trellis preset implementation.

This works in a self-hosted Guru Trellis checkout because the target contains `trellis/presets/guru-team/**`.
It fails in a normal installed business repository because that source-only tree is not part of the installed
target and must not become a business repository dependency.

The target reviewed commit and the installed extension source commit are independent identities. #191's
`source.commit == reviewed_content_head` invariant describes the self-hosted case. Applying it to a business
target overwrites extension source meaning with an unrelated business commit.

## Decision

Finalizer provenance preparation uses two independent temporary checkouts:

- `target_reviewed_checkout` is created from the target repository at `reviewed_content_head`. It is the
  installer target, metadata-tail commit owner, and publication lineage owner.
- `extension_source_checkout` is a detached clean checkout that only supplies canonical preset implementation
  bytes.

Source selection has two modes and no fallback:

1. `self_hosted`: target and manifest source repository identities match. Extension source commit is the
   target `reviewed_content_head`.
2. `installed`: identities differ. Extension source repository/ref/commit comes from the clean immutable
   installed manifest; Finalizer configures canonical `origin`, fetches the exact full OID, checks out detached,
   and verifies HEAD and clean state.

Finalizer invokes the apply script from `extension_source_checkout` with `--repo target_reviewed_checkout`.
Post-apply validation binds two dimensions independently:

- target tail parent and publication lineage bind target `reviewed_content_head`;
- manifest source repo/ref/commit bind the selected extension source checkout.

The helper remains package-local to `guru-finalize-task`. Verifier workflow/profile/gate/artifact/transaction
code is not called or imported as lifecycle authority. Existing low-level Finalizer Git/repository primitives
remain reusable inside the package.

## Consequences

- release-installed business repositories no longer need the canonical source tree.
- self-hosted #191 behavior remains bound to the reviewed source commit.
- installed source provenance remains bound to immutable Guru Trellis identity instead of business HEAD.
- Finalizer public profiles, exits, transaction states, post-bind recovery ordering, Merge handoff, and
  side-effect boundaries remain unchanged.
- source-resolution failure stops before target apply, PR creation, archive, Ready, or Issue mutation.
- source and target temporary checkout cleanup stay independent and never touch caller or sibling worktrees.

## Rejected alternatives

- Read the canonical apply script from the business target: preserves the defect and makes source-only paths a
  target dependency.
- Resolve mutable `main`, PATH packages, global installs, or hidden local checkouts: breaks manifest-bound
  reproducibility and exact source identity.
- Call `guru-verify-extension-installation`: violates the established business Finalizer/verifier boundary and
  imports an unrelated lifecycle.
- Always bind `source.commit` to target reviewed HEAD: corrupts installed extension provenance.
- Always preserve the manifest commit: regresses self-hosted #191 behavior.
- Retain both old and new resolvers: creates dual-read authority with no exit.

## Verification and promotion

The Phase 2 candidate has focused self-hosted/installed binding tests, exact-OID and failure fixtures,
manifest-only tail validation, post-bind recovery regression, canonical/installed/platform parity,
reapply/drift/sidecar-zero, source/installed package validation and task/document checks. These prove the
implemented owner and checkout boundary on the current worktree candidate; they do not constitute an
independent committed-range review or promotion.

Acceptance still requires one separately authorized representative clean business closeout. The full #267
release matrix, tag-pinned smoke, tag, and GitHub Release remain outside this ADR and are unverified here.

Promotion requires a fresh #311 Phase 2 result, exact task commit, independent `origin/main...HEAD` Branch
Review with no open P0-P3 finding, and expected `.40` serialized Architecture/RDT promotion. A promotion-created
diff repeats Phase 2, task commit, and Branch Review before Publication or Finish.
