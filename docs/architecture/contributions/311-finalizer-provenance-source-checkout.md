# #311 Architecture contribution

## Candidate identity and authority boundary

- candidate identity：`architecture-contribution-311-finalizer-extension-source-target-binding-v2`。
- source authority：Issue #311、current `REQ-006`、`BEH-008`、`DES-001`、`DES-012` 与 #191
  clean provenance-tail contract。
- serialized promotion source authority：`docs/architecture/README.md` /
  `current-main-0.6.5-guru.40` / `active`；promoted current identity：
  `current-main-0.6.5-guru.41` / `active`。
- design constitution：`docs/architecture/00-foundation/design-constitution.md` /
  `guru-trellis-design-constitution-v1` / `current`。
- project change contract：`docs/architecture/06-governance/change-contract.md` /
  `guru-trellis-architecture-change-contract-v1` /
  `guru-trellis-architecture-change-concerns-v1`。
- change path：`target_native`；promotion state：`reviewed_promoted`。
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

The representative closeout also exposed a separate evidence-boundary defect: standalone verification can
enter the compatibility matrix, fail, and clean its temporary workspace while the outer owner retains only
aggregate stdout/stderr digests and sizes. The verifier remains its own lifecycle owner, but must project
bounded structured failure facts before cleanup. This does not alter ADR-007 or add any Finalizer dependency
on verifier state.

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
| `evidence-and-freshness` | `applicable` | Planning binds live Issue/code/task docs; verifier failure evidence retains stage/cell/command/bounded tail before cleanup; later stages bind focused tests, installed fixture, representative closeout, exact committed range, and current provider facts |
| `review-and-promotion` | `applicable` | Candidate remains task-owned until independent Branch Review; expected `.40` serialized promotion creates a successor and repeats Phase 2/commit/Branch Review |

## Owner transition and compatibility exit

- current owner failure：target checkout is incorrectly treated as extension source implementation owner.
- target owner：`guru-finalize-task` package-local runtime resolves mode and owns both temporary checkout
  lifecycles; installer remains the sole producer of manifest source provenance.
- task writer：`311-finalizer-provenance-source-checkout` worktree.
- shared-current writer：Architecture promotion owner bound to expected `.40`.
- standalone verification evidence owner：`guru-verify-extension-installation`; compatibility matrix runner
  supplies structured failure facts and the outer owner retains them before cleanup. Finalizer remains a zero
  consumer of that evidence.
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
- diagnostic addition：standalone verifier failures preserve bounded stage/cell/command/error facts through
  cleanup; successful matrix, capability, asset inventory and Finalizer contracts remain unchanged.

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
- initial `publication_ready` preview now classifies an exact existing PR first; when no PR and no remote branch
  exist, a tail-less installed `prepared` state maps to `reprepare_required/provenance_metadata_tail` before
  push, PR creation, archive, Ready, or Issue mutation. The matching executor preflight accepts an absent remote
  or the exact reviewed head and still rejects every non-empty mismatched remote head.
- compatibility matrix failures now emit one closed pre-matrix/matrix-cell/post-matrix terminal with the
  applicable cell, actual helper basename, exit code and 2000-character credential-safe tail. The standalone
  verifier parses it before temporary cleanup, preserves command hashes/sizes, and classifies malformed output
  as `unparseable_failure_output`; this remains verifier-private and adds no Finalizer edge.
- standalone verifier contract tests resolve the shared eval adapter from the current package root, so the same
  contract runs in canonical and installed layouts without requiring a business target to contain
  `trellis/skills/**`.
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
- Current candidate evidence：canonical/installed Finalizer 各 `59/59`（包括首次 Publication、无 existing
  plan 的 target-repo binding，以及无 remote branch/PR 的 prepared-state provenance regression），
  canonical/installed verifier 各 `17/17`，preset installer `81/81`，upgrade contract `36/36`，
  throwaway routing + ownership `51/51`；source/installed validators 分别验证 21 packages / 72 commands
  与 21 packages / 72 commands / 4263 managed files。clean candidate
  `b1d6fc00bed7c933b2b9613c5e6a8cfae604f9a5` reapply 后的本地完整 Finish integration 已越过
  provenance source、两段 reprepare 与 absent-remote preflight，并在 terminal public invoke 修正为
  原始 `publication_ready` 输入加第二轮 gate 精确 retired locator 后通过（`Ran 1 test in 378.336s,
  OK`）。该 harness 修复不改变 Finalizer public profile、terminal projection、transaction state 或
  Architecture owner。all-platform
  reapply、dogfood drift、canonical/installed/platform byte-mode parity、recursive sidecar-zero、task
  validation、local-link、code-fence、terminology/cross-SSOT semantic review 与 `git diff --check` 均通过。
- Phase 2 result：`pass` / `blocking=true`。完整 worktree candidate 只建立一个 package-local owner，
  删除 installed single-checkout 假设且不保留 fallback/dual-read；required concerns、before/after、
  one-writer、compatibility exit 与 current `.40` identity 均完整，没有新增或恶化 Architecture
  deviation。该结果不替代后续独立 committed full-diff review。
- Current finding-fix Architecture result：fresh implementation-discovery 与 Phase 2 均返回
  `baseline_current` / `architecture_impact` / `target_native` / `reviewed_candidate`。prepared-state、caller
  inventory 与 verifier failure-evidence 修复分别保持在 Finalizer owner、canonical caller inventory 与
  standalone verifier evidence owner 内，不新增 public I/O、transaction state、persistence、SDK/external
  integration、compatibility layer 或 shared-current writer；`guru-trellis-architecture-convergence@1` 为
  `pass` / `blocking=true`，无新或恶化 deviation、dual writer、owner expansion 或 closed
  `ARCH-GAP-006` recurrence。该结果绑定完整 current worktree candidate，仍不替代后续 independent
  committed full-diff Branch Review。
- Branch Review、Publication 与 Acceptance/Finish 必须使用各自 fresh candidate/range 重新执行
  project check，不复用 Planning 或本 Phase 2 result。

## Evidence and remaining gate

- test refs：Finalizer binding/tail/recovery tests、installer source tests、installed no-source-tree fixture、
  projection/reapply/drift/sidecar checks。
- runtime refs：canonical and installed Finalizer wrappers、package validators、source/target negative
  fixtures 与 current all-platform installed graph。
- external refs：Issue #311 and the separately authorized disposable GitHub closeout facts。
- current external status：`unverified`。已授权的代表性 disposable business closeout 使用旧
  candidate 执行到 independent Branch Review，并因 `BR-311-FIXTURE-001`（P1）阻断；source
  finding-fix 已通过 current focused regression。current candidate
  `a03f8ad1bf2bb98575df4a9376a88b480c7bfd5f` 的第 2 次 throwaway 诊断又发现 source secondary caller
  inventory 仍绑定旧 Finalizer apply AST anchor；canonical inventory 已收敛到唯一新 anchor
  `f16c2314ce2a...`，当轮 focused routing tests `44/44` 与 source caller inventory validation 通过。后续
  `4a50f88e` fresh-final review 又发现 installed closeout fake `git` 的 generated-shebang identity 因
  `b1d6fc00` 增加 `subprocess` 已演进为 `07004913deeb...`，inventory 仍保留
  `da71f59de8d1...`；`BR-311-SOURCE-006` 只刷新该确定性 inventory anchor，不改变 caller、routing、
  Architecture owner 或 ADR-007。current
  candidate `cdc55ca93bc28934bfaa1c4ba48aeef83baf3277` 的第 3 次且最后一次 throwaway 已进入 default
  matrix，但 outer verifier 只保留 stdout/stderr hash/size，失败 stage/cell/command/tail 随 cleanup
  丢失。`guru-qualify-normal-scenario:requirements_scope_set` 已将该正常路径缺陷资格化为
  `qualified_current`，用户接受 standalone verifier failure evidence 为当前 #311 scope。该扩展不改变
  ADR-007，却使全部 prior Phase 2/Architecture evidence stale；focused diagnostic fix 现已完成并通过
  matrix-stage/helper-label/schema/outer-parser/bounded credential-safe tests，对 `cdc55ca9` 仍禁止第 4 次
  完整 throwaway，须先形成不同 clean candidate。新 candidate 尚未在现有
  fixture 上完成 fresh Branch Review 与真实 Publication/Finalizer。本 Architecture result 不把旧 candidate
  false green、被阻断的 closeout、#267 release-wide matrix、tag-pinned smoke、tag 或 GitHub Release
  表述为已通过。

## Review and promotion state

- review：Architecture owner 与 distinct fresh-final Branch Review 已对
  `origin/main@d907fcc5e17f23b6499648e5e9a208457f2d6f8b...651defee871d4bb07683547df09d1e0ac62b4a49`
  的 7 commits / 85 paths 完成 independent review，project check 为 `pass / blocking=true`，
  `BR-311-FIXTURE-001` 与 `BR-311-SOURCE-001..006` 全部闭环，P0-P3 open findings 为零。
- ADR：`required=true`；`ADR-007` 已由 expected `.40` serialized promotion 接受，locator 为
  `docs/architecture/adr/007-finalizer-extension-source-target-binding.md`。
- promotion：`reviewed_promoted`；pre-promotion contribution SHA-256 为
  `a6e2835e2303c081c28296f9d635dabbb7bad2dffbe99466f2bd6d4e834058aa`；promoted identity 为
  `current-main-0.6.5-guru.41`。
- promotion-created diff 必须 fresh 重新进入 Phase 2、task commit 与 independent Branch Review。
  真实 fixture、Publication/Finalizer、生产发布与错误文件重试仍为 `unverified`，Issue #311 保持
  OPEN；#267 release-wide matrix、tag 与 GitHub Release 继续由独立 owner负责。
