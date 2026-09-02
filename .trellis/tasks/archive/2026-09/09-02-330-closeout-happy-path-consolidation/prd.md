# #330 收敛 Commit、Publication、Finalizer、Merge 正常路径

## Goal

在不削弱 Guru Team 现有语义审查、副作用确认、freshness、expected-head、恢复和 fail-closed 行为的前提下，把 Commit、Publication、Finalizer、Merge 四个阶段各自收敛为一个文档化、兼容、低调用次数的 Happy Path，使 Agent 只需读取 Skill 合同、完成该阶段语义判断、执行一次只读 prepare/preview，并在需要确认的阶段执行一次确认后事务调用。

本任务的用户价值是减少正常 closeout 中由 Agent 手工阅读 runtime/schema/examples、拼装中间 JSON、重复调用 recorder/checker/invoke 和终态后继续调查造成的墙钟浪费，同时保留出错时的精确阻塞、恢复与兼容入口。

## Background And Confirmed Facts

- Live authority 是 `castbox/guru-trellis#330`，当前为 Open；本 task 唯一关闭目标是 #330。
- `related_issues` 为 #106、#108、#311；完整 release-wide 多平台 exact-candidate 验证仍由 `followup_issues` 中的 #267 承担。
- 2026-09-02 会话 `codex://threads/01a061d2-3d05-7170-94ee-c2a32f6d2aaa` 证明四阶段的主要耗时来自 Agent 编排而非底层命令执行：Commit 约 14 条命令，Publication 约 35 条命令，Finalizer 约 23 条命令，Merge 还出现约 19.8 分钟的自定义 CI 轮询。
- 该会话中 Merge 已返回 terminal `closure_mismatch`，之后仍继续读取 PR、Issue、remote ref 和 CI；PR 合入非默认分支 `dev`，GitHub 未按 `Closes #118` 自动关闭 Issue，属于明确 closure follow-up，而不是继续当前 Merge Skill 的理由。
- 当前四个 package 已分别拥有 recorder/checker/executor/public invoke 组件与稳定 typed exits，但推荐调用面仍要求 Agent 编排多个低层入口。
- #180、#191、#218、#311 已建立 Finalizer/Merge 的最小状态、provenance reprepare、mutation output-loss recovery 和 terminal recovery 正确性合同。本任务复用并收敛这些机制，不重新设计其业务语义。
- 官方 Trellis 扩展面要求 workflow 行为由 Markdown workflow/Skill 表达，spec marketplace 只承载可复用工程约定；不得修改 Trellis 上游源码、全局 npm 包或 `node_modules`。
- 当前仓库的 canonical source 位于 `trellis/skills/guru-team/**`、`trellis/workflows/guru-team/**` 和 `trellis/presets/guru-team/**`；`.trellis/guru-team/**`、`.agents/skills/**`、`.codex/skills/**` 是受管安装/发现副本。

## Requirements

### R1. 可重复的基线与阶段调用预算

- 为 Commit、Publication、Finalizer、Merge 建立同一 fixture 可重复运行的旧路径基线，结构化记录 normalized operation、command invocation、Git/GitHub/Trellis live read、mutation、recovery 和 terminal 后调用。
- 基线必须区分 Agent 编排时间、deterministic command 时间、GitHub API 时间和外部 CI 等待；wall-clock 只作观察，不能替代 operation counter。
- 将 #118 慢路径去敏后固化为 transcript/fixture，保留非默认分支 closure mismatch、terminal 后继续调用和重复 CI watcher 三项关键事实。
- 任何优化必须先由 fresh baseline 证明存在重复调用；未复现的路径不得为了形式统一而改造。

### R2. 四个 stage-local Happy Path facade

- Commit、Publication、Finalizer、Merge 各自提供一个唯一、文档化、推荐的 Happy Path facade；不得新增跨四阶段的总控脚本或隐藏 semantic route 的 monolith。
- facade 内部只能复用本阶段现有 recorder/checker/executor/projection 能力，并维持该 Skill 的 `judgment_mode`、entry contract、typed exits 和唯一 consumer。
- Agent 正常调用只读取 `SKILL.md`/contract 与公开输入输出，不读取 `runtime/*.py`、schema、examples、evals 或 tests；实现级文件只用于 facade 失败后的有界诊断。
- 旧 record/check/execute/invoke 命令在迁移期间保留为兼容、测试和恢复入口；不得静默删除或改变 stable Skill ID、command ID、schema ID 或 typed-exit 语义。

### R3. Commit Happy Path

- 一次 prepare 完成 task/Phase 2/Git facts 读取、AI 已完成的路径分类输入校验、提交信息规范化和候选检查。
- 取得当前精确 commit action 确认后，一次事务调用完成 mutation-boundary freshness、isolated index、hooks、commit、tree/index/worktree 后置校验、`git update-ref`、live index 刷新、结果投影和候选清理。
- 正常路径不得要求 Agent 依次调用 prepare、message check、create 和 invoke。
- dirty/staged drift、unrelated preservation、hook failure、active Git operation、stdout loss 和已成功 ref mutation recovery 与当前合同行为等价。

### R4. Publication Happy Path

- Publication 的语义审查仍由 AI 覆盖当前八个发布维度；facade 只记录并验证已完成的结论，不选择 finding、revision action 或 route。
- 在 `branch_review_commit`、reviewed-content identity 和发布新增事实未变化时，Publication 不重跑完整实现/设计审查，只验证直接依赖的 evidence binding。
- 无 metadata finding 的正常路径最多一次只读 preview 和一次 facade invoke；metadata-only revision 只重审直接受影响维度，content/durable drift 仍返回现有 task-work route。
- `primary_issue` 与 `close_issues` 的 ledger disposition mismatch 必须在进入 Publication 前或 facade preflight 中确定性阻塞。

### R5. Finalizer Happy Path

- 一次 preview 生成当前精确 Finalizer side-effect plan；用户确认后一次 facade invoke 自动完成现有 deterministic transition 与 mapped recovery/reprepare loop。
- `provenance_tail_required`、同 scope `reprepare_required`、stdout loss recovery、已有 PR adoption 四类不产生新语义选择的 current-plan route 在同一已确认事务中自动承接。
- scope、authority、PR payload、publication identity 或副作用集合发生实质变化时，旧确认失效并返回现有稳定 exit，不得自动跨越新的确认边界。
- Agent 不再读取 Finalizer runtime 手工重建第二轮 input、review JSON 或 plan locator；终态直接返回现有 typed exit 与最小 remediation。

### R6. Merge Happy Path 与 terminal stop

- 用户确认 exact repo/PR/base/head/expected-head/method/close scope 后，只调用一次 Merge facade。
- facade 内部最多执行一次合并前完整 live snapshot、expected-head mutation 和一次合并后完整 live snapshot；同一 snapshot 内的事实由调用内 checked object 复用。
- `merged`、`closure_mismatch` 和其它现有 terminal exit 返回后，当前 Merge Skill 立即停止，不再执行 Phase 0、base sync、PR branch update、本地 base 同步、额外 CI 等待、Issue mutation 或资源清理。
- 默认分支自动关闭、非默认分支 closure follow-up、`expected_close_issues=[]` refs-only 和 mutation 已成功但输出丢失恢复必须有明确回归。
- Merge Skill 不直接关闭 Issue；任何后续人工 Issue closure 是独立副作用并需要新的当前确认。

### R7. 单一 expected-head-bound CI watcher

- Finalizer 自身耗时与 PR Ready 后的外部 CI 等待分开记录。
- 当 Merge gate 遇到 required checks pending 时，只运行一个 deterministic、可恢复、repo/PR/expected-head-bound watcher。
- watcher 返回稳定的 pending/success/failure/head-changed 结果；不得先运行 `gh run watch` 再启动 Agent while-loop，也不得观察其它 head 的 run。
- watcher 不拥有 merge readiness 语义判断，不执行 merge mutation，也不改变 Finalizer/Merge 的独立确认边界。

### R8. 兼容迁移与分发一致性

- 新 Happy Path 先与旧路径在相同 fixture 上证明 typed exit、public DTO、deterministic blocker、mutation 次数、副作用顺序、恢复和临时文件生命周期等价，再切换 workflow/Skill/platform 默认推荐入口。
- 若需要扩展 public contract，使用新 schema/interface version 和显式 producer/consumer migration；旧 installed preset 继续可调用旧兼容入口。
- canonical 变更先落 package/workflow/spec，再通过 preset apply 同步 dogfood 与声明平台投影；全部 `.new`/`.bak` 必须处理，dogfood drift 必须为零。
- 本 task 至少执行一个代表性 clean installed/throwaway Happy Path；完整 release-wide 多平台 exact-candidate matrix 仍由 #267 承担。

## Hard Acceptance Criteria

- [ ] AC1: Commit、Publication、Finalizer、Merge 的 semantic ownership、确认边界、freshness、expected-head、dirty/mismatch、recovery 与 fail-closed 行为未削弱。
- [ ] AC2: 每个阶段存在唯一文档化 Happy Path；Agent 正常路径不读取 runtime/schema/examples/evals/tests。
- [ ] AC3: Commit 正常路径最多一次 prepare 和一次确认后事务调用，且 path/message/hook/ref/recovery 行为与旧路径等价。
- [ ] AC4: 无 metadata finding 的 Publication 正常路径最多一次 preview 和一次 facade invoke；metadata-only 与 content/durable drift route 保持正确。
- [ ] AC5: Finalizer 无新语义选择的 mapped reprepare/recovery 在同一已确认事务中自动承接；plan 实质变化仍重新取得确认。
- [ ] AC6: Merge 确认后只调用一个 facade，最多一次 pre-merge 完整 snapshot 与一次 post-merge 完整 snapshot。
- [ ] AC7: CI 只运行一个 repo/PR/expected-head-bound watcher；外部 CI 时间与 Guru Team 编排时间分别报告。
- [ ] AC8: terminal typed exit 返回后该 Skill 的 operation counter 不再增加；workflow 只进入该 exit 的唯一 consumer/stop target。
- [ ] AC9: 默认分支、非默认分支、refs-only、closure mismatch/follow-up、checks pending/success/failure 和 stdout-loss recovery 回归全部通过。
- [ ] AC10: 同一 fixture 新旧路径的 typed exit、public DTO、semantic/deterministic boundary、Git/GitHub/Trellis mutation 与临时状态生命周期等价。
- [ ] AC11: 正常路径 command invocation 相对 fresh baseline 至少下降 50%，重复完整事实读取至少下降 70%；若未达到，不能声明结构性收敛完成。
- [ ] AC12: 旧入口保持兼容；canonical、dogfood、installed projection、preset reapply、drift checks 和一个代表性 clean installed/throwaway Happy Path 通过。
- [ ] AC13: 独立 current-HEAD Branch Review 覆盖完整 `origin/main...HEAD` 且无未关闭 P0-P3 finding。

## Non-Blocking Performance Targets

以下目标在固定 fixture 或 5-10 次代表性运行上观察，wall-clock 受模型、GitHub API、网络和 CI 影响，不是单次运行的唯一成败判据：

- Commit 确认后墙钟中位数小于 30 秒。
- 无 metadata finding 的 Publication 墙钟中位数小于 60 秒。
- Merge 确认至 terminal typed exit 的墙钟中位数小于 90 秒。
- Agent/Guru Team 编排耗时相对基线下降 60%。

若上述目标未完全达到，但 AC1-AC13、行为等价和 operation-count 收敛均通过，则任务在如实记录实测值、未达原因与外部瓶颈后满足完成条件；单次 GitHub/网络/CI 延迟不直接判定失败。若 command invocation、重复事实读取或 Agent 正常调用面没有达到 AC11，则属于硬验收未完成，Issue 不得关闭。

## Regression Scenarios

- Commit：正常成功、hook failure、dirty/staged drift、unrelated preservation、active Git operation、stdout loss recovery。
- Publication：正常 ready、metadata-only revision、content/durable drift return、external blocker、ledger disposition mismatch。
- Finalizer：正常 ready、provenance tail、same-scope reprepare、publication stale、已有 PR adoption、stdout loss recovery。
- Merge：checks pending/success/failure、head/base drift、policy mismatch、mergeability blocker、默认分支自动关闭、非默认分支 follow-up、refs-only、mutation output loss。
- Workflow：terminal exit 后零当前 Skill 额外调用；旧 installed preset 使用兼容入口；新 Happy Path 在代表性 clean installed repo 中可运行。

## Out Of Scope

- 删除或降低 Phase 2、Branch Review、Publication、Finalizer、Merge 的 AI semantic review。
- 合并 Commit、Finalizer、Merge 的独立副作用确认，或持久化授权信息。
- 用 Python/shell 判断 scope、finding、readiness、route、Issue closure disposition 或 PR publication adequacy。
- 在 Merge Skill 中手工关闭 Issue、同步本地 base、更新 PR branch、清理 task/worktree/branch 或等待无关 CI。
- 无迁移合同地删除旧 command/schema/typed exit 或破坏旧 installed preset。
- 恶意 actor、故意伪造/篡改、对抗性输入、锁、TOCTOU、分布式并发压力、跨 OS 原子性和额外 fault injection。
- 替代 #267 的完整 release-wide 多平台 exact-candidate matrix。

## Open Questions

无。Issue 正文、当前 package contracts、历史会话证据和 repository authority 已足以形成实施方案。
