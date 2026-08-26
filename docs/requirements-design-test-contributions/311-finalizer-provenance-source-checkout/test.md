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
- `T311-07`（R311-08）：matching Draft/Ready transaction 在每个 post-bind transition 先于 provenance
  inference；payload/scope/plan/remote/HEAD drift 保持 fail closed。
- `T311-08`（R311-08/09）：四个 current input profiles、六个 exits、transaction/archive/terminal/Merge
  regression通过；静态与 runtime fixture 的 verifier package/wrapper/command/artifact call count均为零。
- `T311-09`（R311-09/11）：canonical package tests、installed package tests、source/installed validators、
  contract/eval/registry/manifest checks、Shared/Codex/Claude/Cursor byte/mode parity通过。
- `T311-10`（R311-11）：all-platform preset apply 和第二次 reapply idempotent；dogfood drift、ownership、
  recursive `.new`/`.bak`/unknown-sidecar scan全部通过。
- `T311-11`（R311-12）：经单独 GitHub mutation授权的 disposable business closeout覆盖 Publication
  `ready`、preview `reprepare_required`、execute、`reprepare_preview`、唯一 Draft PR、archive、Ready与
  archive 后 `ready_for_merge`；重复 invoke不产生新 mutation。
- `T311-12`（R311-12）：任务报告明确列出未运行的 #267 release-wide multi-platform matrix、tag-pinned
  smoke、tag 与 GitHub Release，不把 focused proof表述为 release acceptance。

证据层级遵循 current Validation Scope Ownership：focused package/runtime 与一个代表性 clean target
证明 #311 normal path；canonical/projection/reapply/drift证明 managed distribution；external closeout只有在
当前会话单独授权后执行。

## Current Phase 2 evidence

- `T311-01..10` 当前 worktree candidate 已通过：canonical/installed Finalizer 各 `56/56`，preset
  installer `81/81`，ownership `7/7`，upgrade contract `32/32`，Finish family integration `6/6`。
- source validator 通过 21 packages / 72 commands；installed validator 通过 21 packages / 72
  commands / 4263 managed files，且 conflicts/sidecars 为零。
- all-platform apply/reapply、dogfood drift、canonical/installed/Shared/Codex/Claude/Cursor byte-mode
  parity、recursive sidecar-zero、task validation、local-link、code-fence、whitespace、terminology 与
  cross-SSOT semantic review 均通过。
- `T311-11` 仍为 `unverified`：代表性 disposable business closeout 需要单独 GitHub mutation 授权。
  `T311-12` 保持边界声明：#267 release-wide matrix、tag-pinned smoke、tag 与 GitHub Release 均未运行。
- contribution 仍是 `candidate_pending_review`；本摘要不是 independent committed full-diff review、
  serialized promotion、Publication 或 Acceptance/Finish 证据。
