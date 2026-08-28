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
  Issue mutation 均未调用；executor preflight 接受 absent remote 或精确 reviewed head，并继续拒绝非空
  remote drift；fresh Draft/Ready adoption 与每个 post-bind transition 仍先于 provenance inference，
  payload/scope/plan/remote/HEAD drift 保持 fail closed。
- `T311-08`（R311-08/09）：四个 current input profiles、六个 exits、transaction/archive/terminal/Merge
  regression通过；首次 Publication 在没有 existing plan 时仍绑定 target repo 并在首次 preview 识别
  required tail；静态与 runtime fixture 的 verifier package/wrapper/command/artifact call count均为零。
- `T311-09`（R311-09/11）：canonical package tests、installed package tests、source/installed validators、
  contract/eval/registry/manifest checks、Shared/Codex/Claude/Cursor byte/mode parity通过；installed verifier
  test 在不含 canonical `trellis/**` 的 business fixture 中仍能从 package-local shared adapter 运行。
- `T311-10`（R311-11）：all-platform preset apply 和第二次 reapply idempotent；dogfood drift、ownership、
  recursive `.new`/`.bak`/unknown-sidecar scan全部通过。
- `T311-11`（R311-12）：经单独 GitHub mutation 授权后，现有真实 fixture 的 fresh reinstall 与
  business closeout 应覆盖 Publication `ready`、preview `reprepare_required`、execute、
  `reprepare_preview`、唯一 Draft PR、archive、Ready 与
  archive 后 `ready_for_merge`；terminal invoke 使用原始 `publication_ready` 输入与第二轮 gate 的精确
  retired locator，重复 invoke不产生新 mutation。
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

- `T311-01..10` 与 `T311-13` 已通过：canonical/installed Finalizer 各 `59/59`，
  canonical/installed verifier 各 `17/17`，routing `44/44`，ownership `7/7`，upgrade `36/36`，
  preset `81/81`；source/installed validator、all-platform apply/reapply、dogfood drift、平台
  byte-mode parity 与 recursive sidecar-zero 均通过。
- local fake-GitHub complete Finish integration 第 3 次且最后一次运行通过；同一对象、同一阶段不再
  运行第 4 次完整 integration，也不得用新的真实 throwaway repository 规避该上限。
- distinct fresh-final Branch Review 绑定
  `origin/main@d907fcc5e17f23b6499648e5e9a208457f2d6f8b...651defee871d4bb07683547df09d1e0ac62b4a49`
  的 7 commits / 85 paths；`BR-311-FIXTURE-001` 与 `BR-311-SOURCE-001..006` 全部闭环，
  P0-P3 open findings 为零。
- contribution 已由 expected `.40` serialized promotion 提升为 `.41` 的 `reviewed_promoted`；
  promotion-created diff 仍须 fresh 重新进入 Phase 2、task commit 与 independent Branch Review，不能
  把 promotion 本身冒充为已复核。
- `T311-11` 仍为 `unverified`：current `651defee` 尚未在现有真实 fixture 上完成 fresh reinstall、
  GitHub Publication/Finalizer、Ready 与 terminal flow；旧 candidate 的被阻断 closeout和本地
  fake-GitHub integration 都不能替代该证据。
- `T311-12` 保持边界声明：#267 release-wide matrix、tag-pinned smoke、tag 与 GitHub Release 均未运行。
  生产发布与错误文件重试也仍为 `unverified`；Issue #311 必须保持 OPEN，直至复跑证明最大根因已修复。
