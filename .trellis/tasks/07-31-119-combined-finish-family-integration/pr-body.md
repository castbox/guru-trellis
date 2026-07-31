## 变更摘要

- 将 `guru-finish-work` 设为 Guru Team 日常收尾入口，在 Codex、Claude、Cursor 三个平台新增薄入口，并继续由 canonical workflow mandatory invoke `guru-review-task-publication`、`guru-finalize-task`、`guru-verify-extension-installation`。
- 保持 PR #165 已有 13 个 Finish-family typed exits、唯一 consumers、mapped-exit 自动承接与最小 public DTO；平台入口和 workflow 不读取 producer private gate、checkpoint 或 transaction journal。
- 将 checker-passed #117 marketplace evidence 以进程内 private projection 贯通 finalizer preview、retry、normal archive transaction 与 active-completed recovery，在 archive mutation 前 fail closed。
- 为 `guru-finalize-task` 增加 `publication-ready-published` 与 `same-plan-published` 两个 real-wrapper terminal eval，并新增 combined integration suite 覆盖 route、public/private boundary、平台分发与兼容状态。
- 扩展 clean install、`trellis update`、workflow reselect、preset reapply、CLI upgrade dry-run、ownership 与 drift 验收；五个 legacy `trellis-finish-work` payload 保持不变，只移除 #119 blocker，并继续由 #132 负责物理删除。
- 同步 canonical source、dogfood copies、managed manifest、README 与 workflow/preset/spec Docs SSOT；修复 Branch Review 发现的六份 Guru entry EOF 多余空行。
- 修复正常 closeout 先完成 publication review、再由 content push 写入 plan-owned marketplace machine evidence 时的 freshness 顺序：仅接受 immutable plan 的 exact pending evidence 或 current checker-derived passed projection，并只更新枚举的 ledger artifact、entry、status-path、repository 与派生 working-tree bindings。

## 影响范围

- 涉及 canonical/dogfood workflow、Guru namespace overlays、preset installer 与 ownership inventory、shared runtime private projection、publication-ledger finalization augmentation、finalizer eval corpus、combined/runtime/preset/ownership tests，以及 15 个 durable Docs SSOT paths。
- 三个 Finish Skills 的 interface、schema、stable Skill id、external exit id、consumer projection 与 public output fields 均未变化；五个 legacy entry payload bytes 也未变化。
- 未修改 Trellis upstream、全局 npm 包或 `node_modules`，未新增 routine handoff、通用“确认继续”、无人消费 artifact、聚合 DTO 或 consumer 对 producer private state 的解析。
- 不涉及 GitHub Actions、Docker/Compose、Kubernetes、数据库 schema/migration、Makefile、生产配置、业务数据或服务部署；无需停机、配置迁移或数据迁移。

## 验证结果

- Fresh Phase 2 schema 2.1 记录 29 条 exact commands：runtime 553 passed / 13 declared skips，Skill packages 184 passed，preset 47 passed，ownership 14 passed，source 与 installed combined integration 各 6 passed，共 810 tests passed。
- 两次 `apply.sh --repo . --all-platforms` 均成功且第二次幂等；dogfood overlay drift、changed JSON、Python compile、Bash syntax、workspace boundary、frozen donor invariants 与 `git diff --check origin/main` 全部通过。
- Clean throwaway 验证覆盖 marketplace index、workflow install/preview/switch、preset install、`trellis update`、workflow reselect、preset reapply、多平台 discovery、managed hashes、`.new`/`.bak` contract 与 normal/extension closeout transaction。
- `trellis upgrade --dry-run --tag 0.6.5` 通过且未修改 host global installation；Issue #105 的 prepare、push、draft、archive、recovery、PR identity 与 failure matrix 完整回归通过。
- Publication-ledger 顺序回归覆盖 semantic ledger、唯一 reviewed preimage、pending/passed projection、允许的五类派生 binding，以及其它 ledger/artifact/entry/repository/status-path drift 的 fail-closed 负例。
- 当前分支尚未 push，因此不声明 exact unpublished feature-ref marketplace install 已完成；该项由 push 后的 `guru-verify-extension-installation` gate 使用真实 remote ref 验证。

## Review Gate

- Fresh-final Branch Review 覆盖 `origin/main@7ca1a0b96492cbb265bcd7715d14ac93c897fc98...95379d6b498edcd7f0362d10ba20009f84a55d41` 的 5 个 commits、73 个 changed paths 和完整当前 task/ledger/Docs SSOT evidence。
- `BR-119-01`（Guru entry EOF 空白）、`BR-119-02`（durable Finish route SSOT）和 `P2-publication-ledger-closeout-order` 均绑定当前 reviewed HEAD 并已 resolved。
- 独立 reviewer 确认无 open P0-P3 finding、scope proposal、public-I/O drift、compatibility regression 或 Docs SSOT conflict；Branch Review typed exit 为 `passed`，唯一 consumer 是 `guru-review-task-publication`。
- Exact remote feature-ref marketplace installation 仍是 push 后 observation，不是当前 Branch Review pass 声明；#132 仍是 legacy physical removal follow-up。

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
- `merged delta`：日常 `guru-finish-work` 入口、legacy compatibility 状态、private projection responsibility、exact pending/passed publication-ledger augmentation、installer/update/reapply 与 #132 边界已合并到 durable owners；已闭环 findings 不再留下冲突合同。
- `task history`：live GitHub discovery、donor 比对、命令日志、finding lifecycle 与 unpublished branch observation 仅保留在 task history/runtime evidence，不扩张 public DTO。
- `follow-up / limitation`：#132 继续负责 legacy overlay physical removal；exact remote feature-ref marketplace verification 必须在独立 push 授权后完成，当前 PR 文案不把该未执行项写成已验证。
