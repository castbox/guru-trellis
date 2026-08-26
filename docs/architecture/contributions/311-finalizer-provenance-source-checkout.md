# #311 Architecture contribution

## Candidate identity and authority boundary

- candidate identity：`architecture-contribution-311-finalizer-extension-source-target-binding-v1`。
- source authority：Issue #311、current `REQ-006`、`BEH-008`、`DES-001`、`DES-012` 与 #191
  clean provenance-tail contract。
- current Architecture authority：`docs/architecture/README.md` /
  `current-main-0.6.5-guru.40` / `active`。
- design constitution：`docs/architecture/00-foundation/design-constitution.md` /
  `guru-trellis-design-constitution-v1` / `current`。
- project change contract：`docs/architecture/06-governance/change-contract.md` /
  `guru-trellis-architecture-change-contract-v1` /
  `guru-trellis-architecture-change-concerns-v1`。
- change path：`target_native`；promotion state：`reviewed_candidate`。
- expected current identity：`current-main-0.6.5-guru.40`。shared current 只由 Architecture promotion
  owner 在 independent committed full-diff review 后更新。

## Boundary and decision

Current Finalizer provenance preparation creates one detached checkout from the target business repository
at `reviewed_content_head`, then treats that target checkout as the owner of both business mutation and
canonical Guru Trellis installer implementation. A release-installed business repository does not contain
the source-only `trellis/presets/guru-team/**` tree, so the supported pre-PR reprepare path stops before the
metadata tail.

Target boundary uses two independent checkout identities:

1. `target_reviewed_checkout` belongs to the business repository at `reviewed_content_head`; it is the only
   checkout passed through installer `--repo`, the only checkout that receives the manifest diff, and the
   only checkout that creates the metadata-tail commit.
2. `extension_source_checkout` belongs to the canonical extension repository at one exact immutable source
   commit; it only supplies the canonical preset implementation and remains clean.

The binding has two closed modes:

- `self_hosted` binds extension source to target `reviewed_content_head`, preserving #191 behavior.
- `installed` binds extension source to the clean immutable `repo/ref/commit` in the target reviewed
  manifest; it never rewrites source provenance to the business repository HEAD.

The decision is recorded by ADR candidate
[`ADR-007`](../adr/007-finalizer-extension-source-target-binding.md). Finalizer owns one package-local source
binding/checkout helper. It does not call verifier lifecycle code, create a shared resolver API, search hidden
local checkouts, or retain a legacy single-checkout fallback.

## Required concern review

| Concern | Applicability | #311 contract |
| --- | --- | --- |
| `authority-binding` | `applicable` | Binds Architecture 2.0, `.40`, the current constitution/change contract, Issue #311, target reviewed identity, and installed manifest source identity |
| `constitution-binding` | `applicable` | Hits `concept-semantic-completeness`, `cohesion-change-isolation`, `minimum-necessary-complexity`, and `debt-one-way-convergence` without copying principle prose |
| `boundary-and-decision` | `applicable` | `target_native` separates target mutation ownership from extension implementation ownership and defines two closed source modes |
| `owner-and-single-writer` | `applicable` | Finalizer runtime owns binding and tail production; installer owns manifest source provenance; task worktree writes the candidate; promotion owner writes shared current |
| `compatibility-and-exit` | `applicable` | Public Finalizer profiles, exits, transaction states, Merge handoff, and post-bind ordering remain unchanged; the old single-checkout assumption is deleted |
| `gap-and-deviation` | `applicable` | Closes the #311 installed reprepare gap; does not modify `ARCH-GAP-001..006` or absorb #267 |
| `parallel-scope` | `applicable` | Task edits stay in #311 canonical/package/projection/docs scope; business repository #29 and shared current remain outside this worktree |
| `evidence-and-freshness` | `applicable` | Planning binds live Issue/code/task docs; later stages bind focused tests, installed fixture, representative closeout, exact committed range, and current provider facts |
| `review-and-promotion` | `applicable` | Candidate remains task-owned until independent Branch Review; expected `.40` serialized promotion creates a successor and repeats Phase 2/commit/Branch Review |

## Owner transition and compatibility exit

- current owner failure：target checkout is incorrectly treated as extension source implementation owner.
- target owner：`guru-finalize-task` package-local runtime resolves mode and owns both temporary checkout
  lifecycles; installer remains the sole producer of manifest source provenance.
- task writer：`311-finalizer-provenance-source-checkout` worktree.
- shared-current writer：Architecture promotion owner bound to expected `.40`.
- compatibility required：yes, for self-hosted #191 semantics and existing public Finalizer graph.
- compatibility exit：the current single-checkout assumption and `source.commit == business HEAD` rule are
  removed from installed mode; no fallback, dual-read, or verifier re-entry remains.
- legacy deletion condition：all canonical, installed, platform, reapply, drift, self-hosted, installed, and
  representative closeout checks pass with zero active call site using the single-checkout assumption.

## Before and after

- before：target business checkout at reviewed head is also searched for canonical installer source;
  provenance validation applies the self-hosted source-commit rule to every repository.
- after：`prepare_provenance_metadata_tail()` resolves one closed `self_hosted|installed` binding, creates
  distinct extension-source and target-reviewed checkouts, runs the source checkout's canonical apply entry
  with `--repo` bound to the target checkout, and validates target lineage and extension provenance
  independently before creating one manifest-only tail child.
- preserved：reviewed/publication two-head model, manifest-only allowlist, single tail, FF-only publication,
  post-bind recovery precedence, Finalizer public graph, Issue scope, archive, Ready, Merge handoff, and
  verifier isolation.

## Implemented candidate

- canonical runtime now owns manifest parsing, canonical GitHub repository normalization, closed mode
  resolution, exact-OID installed fetch, detached/clean checkout validation, binding-aware postimage checks,
  and independent cleanup for both checkout roots.
- self-hosted mode keeps the mutable/dirty installed-manifest preimage accepted by #191, but binds the source
  checkout and postimage to the reviewed target HEAD. Installed mode requires clean immutable full-OID
  manifest provenance and preserves that extension identity across apply.
- apply executable bytes come only from `extension_source_checkout`; target content and metadata-tail commit
  remain owned only by `target_reviewed_checkout`. Direct parent, manifest-only path, allowlist, one-tail and
  publication-head checks remain unchanged.
- matching post-bind transaction recovery still short-circuits before source resolution. Static package
  assertions and focused runtime tests confirm no verifier import, call, artifact, command or typed-exit
  dependency was introduced.
- canonical package, dogfood installed package, Shared/Codex/Claude/Cursor discovery projections, owning
  specs and operator docs are synchronized from the canonical preset source. No shared Architecture current
  file is modified by this task candidate.

## Project check

- descriptor：`guru-trellis-architecture-convergence:repository:1` /
  `guru-trellis-architecture-convergence@1`。
- refs：`ARCH-GOV-006..008`、`ADR-005`、`ARCH-GAP-006`。
- Planning evidence：live Issue #311、current Finalizer/installer source、task `prd.md` / `design.md` /
  `implement.md`、本 contribution 与 ADR-007 candidate。
- Planning result：`pass`。当前计划固定一个 `target_native` path、一个 Finalizer binding owner、一个
  task writer、一个 promotion owner，并保留 self-hosted compatibility exit；没有新增 legacy
  authority、dual writer、public route 或 closed GAP regression。
- Phase 2 evidence：canonical/installed Finalizer 各 `56/56`，preset installer `81/81`，ownership
  `7/7`，upgrade contract `32/32`，Finish family integration `6/6`；source/installed validators 分别
  验证 21 packages / 72 commands 与 21 packages / 72 commands / 4263 managed files。all-platform
  reapply、dogfood drift、canonical/installed/platform byte-mode parity、recursive sidecar-zero、task
  validation、local-link、code-fence、terminology/cross-SSOT semantic review 与 `git diff --check` 均通过。
- Phase 2 result：`pass` / `blocking=true`。完整 worktree candidate 只建立一个 package-local owner，
  删除 installed single-checkout 假设且不保留 fallback/dual-read；required concerns、before/after、
  one-writer、compatibility exit 与 current `.40` identity 均完整，没有新增或恶化 Architecture
  deviation。该结果不替代后续独立 committed full-diff review。
- Branch Review、Publication 与 Acceptance/Finish 必须使用各自 fresh candidate/range 重新执行
  project check，不复用 Planning 或本 Phase 2 result。

## Evidence and remaining gate

- test refs：Finalizer binding/tail/recovery tests、installer source tests、installed no-source-tree fixture、
  projection/reapply/drift/sidecar checks。
- runtime refs：canonical and installed Finalizer wrappers、package validators、source/target negative
  fixtures 与 current all-platform installed graph。
- external refs：Issue #311 and the separately authorized disposable GitHub closeout facts。
- current external status：`unverified`。代表性 disposable business closeout 仍需单独 GitHub mutation
  授权；本 Phase 2 Architecture result 不把它、#267 release-wide matrix、tag-pinned smoke、tag 或
  GitHub Release 表述为已通过。

## Review and promotion state

- review：`pending`；independent committed range 尚未形成。
- ADR：`required=true`；locator 为
  `docs/architecture/adr/007-finalizer-extension-source-target-binding.md`。
- promotion：`required`；promoted identity 为空。
- contribution 在 implementation discovery、Phase 2 finding、committed full-diff review 或 current
  authority变化后必须更新并重新进入 Architecture owner。
