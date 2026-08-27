# #311 Test contribution

- `T311-01`（R311-01/03/05）：self-hosted fixture 建立两个不同路径的 detached checkouts，source/apply
  来自 reviewed head，target 只产生 manifest tail，source 前后 clean 且 HEAD 不变。
- `T311-02`（R311-01/02/04/05）：installed business target 不含 `trellis/presets/guru-team/**`，仍从
  manifest canonical repo exact-OID fetch source，origin/HEAD/detached/clean 全部通过。
- `T311-03`（R311-02/10）：missing/malformed repo/ref/commit、短 OID、dirty、mutable、canonical locator
  mismatch、fetch/HEAD mismatch 在 apply 或 target mutation 前分别 fail closed。
- `T311-04`（R311-05/10）：source checkout dirty、apply entry missing、apply 修改 source 或写入 target
  额外 path 时阻断，错误不含 credential、token、raw remote payload 或绝对 secret locator。
- `T311-05`（R311-06/07）：self-hosted postimage 绑定 reviewed head；installed postimage 保持 immutable
  extension repo/ref/commit；source repo drift、business HEAD overwrite、extra field/path 与 managed-byte
  drift均失败。
- `T311-06`（R311-06）：tail direct parent、manifest-only changed path、field allowlist、single child、
  `reviewed_content_head` / `publication_head` 分离与 second-tail rejection通过。
- `T311-07`（R311-08）：initial installed `publication_ready` fixture 在无 plan、无 remote branch、无 PR、
  无 tail 时返回 `reprepare_required/provenance_metadata_tail`，并断言 push、PR create、archive、Ready、
  Issue mutation 均未调用；fresh Draft/Ready adoption 与每个 post-bind transition 仍先于 provenance
  inference，payload/scope/plan/remote/HEAD drift 保持 fail closed。
- `T311-08`（R311-08/09）：四个 current input profiles、六个 exits、transaction/archive/terminal/Merge
  regression通过；首次 Publication 在没有 existing plan 时仍绑定 target repo 并在首次 preview 识别
  required tail；静态与 runtime fixture 的 verifier package/wrapper/command/artifact call count均为零。
- `T311-09`（R311-09/11）：canonical package tests、installed package tests、source/installed validators、
  contract/eval/registry/manifest checks、Shared/Codex/Claude/Cursor byte/mode parity通过；installed verifier
  test 在不含 canonical `trellis/**` 的 business fixture 中仍能从 package-local shared adapter 运行。
- `T311-10`（R311-11）：all-platform preset apply 和第二次 reapply idempotent；dogfood drift、ownership、
  recursive `.new`/`.bak`/unknown-sidecar scan全部通过。
- `T311-11`（R311-12）：经单独 GitHub mutation授权的 disposable business closeout覆盖 Publication
  `ready`、preview `reprepare_required`、execute、`reprepare_preview`、唯一 Draft PR、archive、Ready与
  archive 后 `ready_for_merge`；重复 invoke不产生新 mutation。
- `T311-12`（R311-12）：任务报告明确列出未运行的 #267 release-wide multi-platform matrix、tag-pinned
  smoke、tag 与 GitHub Release，不把 focused proof表述为 release acceptance。
- `T311-13`（R311-13）：focused fixtures 分别制造 pre-matrix、确定 matrix cell/command 与 post-matrix
  failure，断言 wrapper/outer owner 在 cleanup 后仍保留 schema-valid bounded facts；unparseable output
  显式分类，failed + null 被 schema 拒绝，matrix 外 command 与 inventory/ownership/sidecar/capability
  postcheck 均形成确定性 `postcheck_failure`，secret markers/credential-bearing remote 不出现在 detail。
  该测试不执行完整 live matrix，也不对 `cdc55ca9` 进行第 4 次 throwaway。

证据层级遵循 current Validation Scope Ownership：focused package/runtime 与一个代表性 clean target
证明 #311 normal path；canonical/projection/reapply/drift证明 managed distribution；external closeout只有在
当前会话单独授权后执行。

## Current Phase 2 evidence

- `T311-01..10` 与 `T311-13` 当前 worktree candidate 已通过：canonical/installed Finalizer 各
  `58/58`，canonical/installed verifier 各 `17/17`，preset installer `81/81`，upgrade contract
  `36/36`，throwaway routing + ownership `51/51`。Finish family integration 的既有 clean candidate
  `6/6` 证据未被 verifier-only finding-fix 改写；fresh pre-commit rerun因当前 source 尚未形成 clean
  commit 正确停止于 `provenance_tail_source_not_clean`，必须在 finding-fix commit 后对 exact clean
  candidate 重跑，不得记为当前通过。
- source validator 通过 21 packages / 72 commands；installed validator 通过 21 packages / 72
  commands / 4263 managed files，且 conflicts/sidecars 为零。
- all-platform apply/reapply、dogfood drift、canonical/installed/Shared/Codex/Claude/Cursor byte-mode
  parity、recursive sidecar-zero、task validation、local-link、code-fence、whitespace、terminology 与
  cross-SSOT semantic review 均通过。
- caller inventory 与 verifier failure-evidence finding-fix 后已重新执行 fresh Architecture
  implementation-discovery/Phase 2，均返回 `baseline_current / architecture_impact / target_native /
  reviewed_candidate`，project check 为 `pass/blocking=true`；fresh RDT `task_impact_sync` 返回
  `ssot_current`，`guru-check-task:finding_fix_rerun` recorder、checker 与 public wrapper 均返回
  `passed`。四个历史 P1 finding 均为 `resolved`，没有 open P0-P3 finding；该结果仍不替代 T311-11
  的真实 representative closeout。
- `T311-11` 仍为 `unverified`：已授权的代表性 disposable business closeout 使用 candidate
  `ea30cac7878bf8f36338e6bfdc67869fbecca009` 完成 fixture task commit 与 independent Branch Review，
  但 Branch Review 发现 `BR-311-FIXTURE-001`（P1）：首次 Publication 在没有 existing plan 时读取未
  初始化的 `prospective_git`，在返回 `reprepare_required` 前稳定失败。后续 validation candidate
  `8138e3dd355f088ad6d4b43548243134f7bbe7d5` 又暴露首次无 remote branch/PR 时 state 为 `prepared`，
  provenance detector 只接受 `content_pushed`，preview 错误返回 `prepared`。source worktree 已分别修复
  target-repo binding 与 initial prepared-state inference，并通过 canonical/installed `58/58`、两种
  package validator、reapply/parity/sidecar checks。current candidate
  `a03f8ad1bf2bb98575df4a9376a88b480c7bfd5f` 的第 2 次 throwaway 诊断随后发现 source secondary
  caller inventory 仍登记旧 apply AST anchor `004063a10598...`；canonical inventory 已更新为唯一当前
  anchor `f16c2314ce2a...`，focused routing tests `44/44`、source `check-inventory`、JSON 与 whitespace
  checks 通过。该 source-only inventory 不属于 installed preset projection。随后形成的第 3 次
  candidate 证据如下；不能把旧 candidate 的 false green 或被阻断的 closeout 记为通过。
  第 3 次 current candidate `cdc55ca93bc28934bfaa1c4ba48aeef83baf3277` 已越过 caller inventory，
  default compatibility matrix 失败但只留下 stdout `188e4847...` / 78220 bytes、空 stderr、exit 2 与
  incomplete asset inventory；失败 cell/stage/command/error-tail 不可恢复。对该 candidate 禁止第 4 次
  throwaway。`T311-13` finding-fix 现已通过 focused pre-matrix/matrix-cell/post-matrix、stable helper
  command label、schema 5.0、outer parse/unparseable、2000-character bound、Authorization/env/signature
  URL/private-key credential redaction 测试；未运行完整 matrix，下一步必须先形成新 candidate object。
  `T311-12` 保持边界声明：#267 release-wide matrix、tag-pinned smoke、tag 与 GitHub Release 均未运行。
- contribution 仍是 `candidate_pending_review`；本摘要不是 independent committed full-diff review、
  serialized promotion、Publication 或 Acceptance/Finish 证据。
