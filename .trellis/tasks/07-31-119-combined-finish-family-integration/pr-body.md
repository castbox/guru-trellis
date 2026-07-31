## 变更摘要

- 将 `guru-finish-work` 设为 Guru Team 日常收尾入口，在 Codex、Claude、Cursor 三个平台新增薄入口，并继续由 canonical workflow mandatory invoke `guru-review-task-publication`、`guru-finalize-task`、`guru-verify-extension-installation`。
- 保持 PR #165 已有 13 个 Finish-family typed exits、唯一 consumers、mapped-exit 自动承接与最小 public DTO；平台入口和 workflow 不读取 producer private gate、checkpoint 或 transaction journal。
- 将 checker-passed #117 marketplace evidence 以进程内 private projection 贯通 finalizer preview、retry、normal archive transaction 与 active-completed recovery，在 archive mutation 前 fail closed。
- 为 `guru-finalize-task` 增加 `publication-ready-published` 与 `same-plan-published` 两个 real-wrapper terminal eval，并新增 combined integration suite 覆盖 route、public/private boundary、平台分发与兼容状态。
- 扩展 clean install、`trellis update`、workflow reselect、preset reapply、CLI upgrade dry-run、ownership 与 drift 验收；五个 legacy `trellis-finish-work` payload 保持不变，只移除 #119 blocker，并继续由 #132 负责物理删除。
- 同步 canonical source、dogfood copies、managed manifest、README 与 workflow/preset/spec Docs SSOT；修复 Branch Review 发现的六份 Guru entry EOF 多余空行。

## 影响范围

- 涉及 canonical/dogfood workflow、Guru namespace overlays、preset installer 与 ownership inventory、shared runtime private projection、finalizer eval corpus、combined/runtime/preset/ownership tests，以及 15 个 durable Docs SSOT paths。
- 三个 Finish Skills 的 interface、schema、stable Skill id、external exit id、consumer projection 与 public output fields 均未变化；五个 legacy entry payload bytes 也未变化。
- 未修改 Trellis upstream、全局 npm 包或 `node_modules`，未新增 routine handoff、通用“确认继续”、无人消费 artifact、聚合 DTO 或 consumer 对 producer private state 的解析。
- 不涉及 GitHub Actions、Docker/Compose、Kubernetes、数据库 schema/migration、Makefile、生产配置、业务数据或服务部署；无需停机、配置迁移或数据迁移。

## 验证结果

- Fresh Phase 2 schema 2.1 记录 50 条 exact commands：runtime 551 passed / 13 declared skips，Skill packages 184 passed，preset 47 passed，ownership 14 passed，source 与 installed combined integration 各 6 passed，共 808 tests passed。
- 两次 `apply.sh --repo . --all-platforms` 均成功且第二次幂等；dogfood overlay drift、changed JSON、Python compile、Bash syntax、workspace boundary、frozen donor invariants 与 `git diff --check origin/main` 全部通过。
- Clean throwaway 验证覆盖 marketplace index、workflow install/preview/switch、preset install、`trellis update`、workflow reselect、preset reapply、多平台 discovery、managed hashes、`.new`/`.bak` contract 与 normal/extension closeout transaction。
- `trellis upgrade --dry-run --tag 0.6.5` 通过且未修改 host global installation；Issue #105 的 prepare、push、draft、archive、recovery、PR identity 与 failure matrix 完整回归通过。
- 当前分支尚未 push，因此不声明 exact unpublished feature-ref marketplace install 已完成；该项由 push 后的 `guru-verify-extension-installation` gate 使用真实 remote ref 验证。

## Review Gate

- 既有 Branch Review 覆盖 `origin/main...c8c84ab21fc80cd2e72017e293f2aba38e00150c` 两提交范围与 70 个 changed paths，并发现 `BR-119-01`（六份 Guru entry EOF 多余空行，P2）。
- 当前 finding-fix candidate 已修复 `BR-119-01`、same-month augmented-plan owner projection、real `cmd_finish_work` prepare/apply projection threading，以及 Phase 2 schema 2.1/2.0 Docs SSOT 冲突。
- 独立 final pre-recorder review 复核完整 working-tree candidate 与 50 条命令证据后确认 P0=0、P1=0、P2=0、P3=0；canonical Branch Review Gate 将在单独授权的 task commit 后重跑，未在本轮提前声明 publication ready。

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
- `merged delta`：日常 `guru-finish-work` 入口、legacy compatibility 状态、private projection responsibility、installer/update/reapply 与 #132 边界已合并到 durable owners；BR-119-01 不改变长期语义。
- `task history`：live GitHub discovery、donor 比对、命令日志、finding lifecycle 与 unpublished branch observation 仅保留在 task history/runtime evidence。
- `follow-up / limitation`：#132 继续负责 legacy overlay physical removal；exact remote feature-ref marketplace verification 必须在独立 push 授权后完成，当前 PR 文案不把该未执行项写成已验证。
