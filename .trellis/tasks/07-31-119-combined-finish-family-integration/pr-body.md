## 变更摘要

- 将 `guru-finish-work` 设为 Guru Team 日常收尾入口，在 Codex、Claude、Cursor 三个平台新增薄入口，并继续由 canonical workflow mandatory invoke `guru-review-task-publication`、`guru-finalize-task`、`guru-verify-extension-installation`。
- 保持 PR #165 已有 13 个 Finish-family typed exits、唯一 consumers、mapped-exit 自动承接与最小 public DTO；平台入口和 workflow 不读取 producer private gate、checkpoint 或 transaction journal。
- 将 checker-passed #117 marketplace evidence 以进程内 private projection 贯通 finalizer preview、retry、normal archive transaction 与 active-completed recovery，在 archive mutation 前 fail closed。
- 为 `guru-finalize-task` 增加 `publication-ready-published` 与 `same-plan-published` 两个 real-wrapper terminal eval，并新增 combined integration suite 覆盖 route、public/private boundary、平台分发与兼容状态。
- 扩展 clean install、`trellis update`、workflow reselect、preset reapply、CLI upgrade dry-run、ownership 与 drift 验收；五个 legacy `trellis-finish-work` payload 保持不变，只移除 #119 blocker，并继续由 #132 负责物理删除。
- 同步 canonical source、dogfood copies、managed manifest、README 与 workflow/preset/spec Docs SSOT；修复 Branch Review 发现的六份 Guru entry EOF 多余空行。
- 修复正常 closeout 先完成 publication review、再由 content push 写入 plan-owned marketplace machine evidence 时的 freshness 顺序：仅接受 immutable plan 的 exact pending evidence 或 current checker-derived passed projection，并只更新枚举的 ledger artifact、entry、status-path、repository 与派生 working-tree bindings。
- 修复 GitHub PR HEAD 正常传播延迟：validator 保持单次客观读取，executor 在 local/remote 已一致且 PR identity 稳定时执行六次有界读取；短暂旧值收敛后自动继续，持续不一致、identity drift 或 remote divergence 仍 fail closed。
- 修复 compact schema 1.1 archived recovery 的工作树依赖：active pre-publication 仍检查 task-local publication owner artifact；archived/archive_pushed recovery 从 exact committed plan、gate、evidence/archive commit、finish summary 与 live Git/GitHub facts 恢复，不要求或重建已删除的 `pr-readiness.json`。

## 影响范围

- 涉及 canonical/dogfood workflow、Guru namespace overlays、preset installer 与 ownership inventory、shared runtime private projection、publication-ledger finalization augmentation、finalizer eval corpus、combined/runtime/preset/ownership tests，以及 15 个 durable Docs SSOT paths。
- 三个 Finish Skills 的 interface、schema、stable Skill id、external exit id、consumer projection 与 public output fields 均未变化；五个 legacy entry payload bytes 也未变化。
- 未修改 Trellis upstream、全局 npm 包或 `node_modules`，未新增 routine handoff、通用“确认继续”、无人消费 artifact、聚合 DTO 或 consumer 对 producer private state 的解析。
- 不涉及 GitHub Actions、Docker/Compose、Kubernetes、数据库 schema/migration、Makefile、生产配置、业务数据或服务部署；无需停机、配置迁移或数据迁移。

## 验证结果

- 当前 recovery Phase 2 schema 2.1 记录 15 条受影响验证：runtime 561 passed / 13 existing conditional skips，finalizer contract 6 passed，source integration 9 passed，installed integration 9 passed / 1 existing environment-dependent skip，preset 47 passed。
- Python compile、canonical/installed runtime parity、canonical/installed integration parity、dogfood overlay drift、workspace boundary、task validation、sidecar scan、frozen donor invariants 与 `git diff --check` 全部通过。
- 回归明确覆盖 PR HEAD 首次旧值后收敛、持续不一致 fail closed、compact archive 不含 `closeout-plan.json`/`pr-readiness.json` 的 same-plan recovery、active missing-readiness stale，以及不重复 PR/archive/evidence commit 或其它 side effect。
- 既有完整 #119 clean install、upgrade/update、workflow reselect、preset reapply、多平台与 Issue #105 transaction/recovery 验收保持有效；本 recovery 按授权未因 plan/digest 变化重放无关 Phase 2 或 Skill tests。
- 当前分支尚未 push，因此不声明 exact unpublished feature-ref marketplace install 已完成；该项由 push 后的 `guru-verify-extension-installation` gate 使用真实 remote ref 验证。

## Review Gate

- Distinct fresh-final Branch Review 覆盖 `origin/main@7ca1a0b96492cbb265bcd7715d14ac93c897fc98...72bf89a789d25598a95944dfe9af8735b4a92a10` 的完整 12 commits、74 net paths 和当前 task/ledger/Docs SSOT evidence。
- `F119-FRESH-001`（P1 archived plan working-tree dependency）和 `F119-FRESH-002`（P3 durable archived-readiness SSOT）保留原 `introduced_head=d8664c83...`，并在 `resolved_at_head=72bf89a7...` 取得独立 closure。
- 独立 reviewer 确认无 open P0-P3 finding、scope proposal、public-I/O drift、compatibility regression 或 Docs SSOT conflict；Branch Review typed exit 为 `passed`，唯一 consumer 是 `guru-review-task-publication`。
- Draft PR #166 仍是唯一 OPEN Draft，当前 remote/PR HEAD 仍为历史 `15d957b...`；这是独立 push/finalizer 授权前的预期 observation，不是 Branch Review pass 证据。#132 仍是 legacy physical removal follow-up。

## Issue 关闭范围

Closes #119

Closes #115

### 仅关联或后续范围

- Refs #105：既有 finish-work transaction/recovery owner，本 PR 只做完整回归，不重复关闭或改变语义。
- Refs #116：既有 publication review owner，本 PR 只消费其 public contract。
- Refs #117：既有 extension verification owner，本 PR 只消费 checker-passed result 并构建 private projection。
- Refs #118：既有 finalization owner，本 PR 只完成 combined integration，不重做内部 semantic behavior。
- Refs #132：继续独占 legacy overlay physical removal 与全仓 upstream overlay convergence，本 PR 不实现或关闭该范围。

## 安全说明

- 未引入或暴露 token、credential、private key、signed URL、`.env`、数据库 URL、客户数据或敏感 provider 输出。
- Marketplace evidence projection 只存在于 finalizer private runtime；#117 owner artifact 不被改写，projection 不进入 public DTO、PR body 运行态附件或 task handoff。
- Hash、digest 与 freshness 仅用于 honest-but-fallible 正常流程的一致性和 stale 检测；本 PR 不扩展恶意伪造、adversarial input、并发竞态、锁、TOCTOU、额外 fault injection、偶发 crash consistency 或跨 OS atomicity。
- 没有生产权限、网络服务入口、容器镜像、Kubernetes 资源、数据库、配置或部署副作用。

## Docs SSOT

- `strategy`：`ssot_first`。
- `durable docs`：canonical/dogfood workflow、root/workflow/preset README，以及 workflow、preset、ownership、public-docs 等 15 个 durable paths 已同步并由 Phase 2 绑定当前 SHA-256。
- `merged delta`：日常 `guru-finish-work` 入口、legacy compatibility、private projection、publication-ledger augmentation、PR HEAD 有界收敛、active-versus-archived evidence ownership、installer/update/reapply 与 #132 边界已合并到 durable owners；compact archive 不再依赖或重建 readiness artifact。
- `task history`：live GitHub discovery、donor 比对、命令日志、finding lifecycle 与 unpublished branch observation 仅保留在 task history/runtime evidence，不扩张 public DTO。
- `follow-up / limitation`：#132 继续负责 legacy overlay physical removal；exact remote feature-ref marketplace verification 必须在独立 push 授权后完成，当前 PR 文案不把该未执行项写成已验证。
