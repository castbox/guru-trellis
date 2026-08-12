# #157 Phase 0 单快照与调用预算

## 目标

在当前 package-local Guru Team 架构上，减少 Phase 0 正常路径中无状态相邻的重复 Git、GitHub 和 prerequisite validation 调用，同时保持每个 semantic Skill 的判断所有权、真实 authority freshness 和 workspace mutation-boundary recheck 不变。

## 当前事实

- GitHub Issue #157 是本任务唯一关闭目标；#98 仅为历史 umbrella，不在关闭范围内，#132 已关闭。
- 前置 Issue #156 已关闭，当前基线为 `main@c6f0ea2496077b4e2df4418da657b172c8a19c94`。
- #195 / PR #210 后，Phase 0 行为分别由 `guru-sync-base`、`guru-discover-change-context`、`guru-clarify-requirements`、`guru-review-contract-wording`、`guru-review-change-request`、`guru-create-task-workspace` package-local runtime 所有。
- canonical source 位于 `trellis/skills/guru-team/**`；`.trellis/guru-team/**` 与平台 Skills 是安装副本，不是语义源头。
- 当前代码中 wording 和 readiness 的 record/check 会重建 live issue authority；各 public invoke 还会再次校验 owner result。clarification 的合同仍要求自行执行 duplicate search。具体调用次数必须由 fresh fake harness 基线确定，不能沿用旧共享 runtime 的历史数字。
- workspace 创建前的 fresh base/live recheck 属于正确性边界，必须保留且每次 mutation transaction 只执行合同要求的一次。

## 需求

### R1 当前调用图与确定性基线

扩展 fake Git/GitHub harness，逐个记录以下调用类别并形成优化前、优化后的稳定计数：base resolve/fetch/check、issue get、comments list、issue search、archive scan、prerequisite projection/validation、public serialization 前后 live calls。

基线必须覆盖 existing open issue、空/非空 duplicate、retain/select/retarget、authority mutation refresh、wording changed、base unchanged/changed、draft create/rebind、workspace mutation 前 unchanged/changed，以及 standalone/workflow 两种调用。

### R2 invocation-local immutable snapshot

每个受影响 package 只能在同一 invocation、exact authority identity 和无中间 mutation 的范围内复用 immutable snapshot。Snapshot 必须分别标识 base identity、target issue body/state/comments、duplicate candidate set、clarification authority、wording scope 和 readiness prerequisites。

Snapshot 不得成为跨 invocation 或跨 authoritative mutation 的长期缓存，不得进入另一 Skill 的 private runtime，也不得替代 semantic review。

### R3 checker-bound validation receipt

对仍存在重复 live validation 的 package，在 checker 完成一次 authoritative validation 后生成 invocation-local、exact-result/exact-prerequisites 绑定的确定性 receipt，或生成具有相同绑定字段与拒绝行为的已验证对象。Public serializer 只验证 result bytes、binding 和 output schema；没有 mutation boundary 时不得再次发起 Git/GitHub live scan。

旧 receipt 在 result、prerequisite、base、issue body/comments/state、duplicate target 或其它所依赖 authority identity 变化后必须被拒绝。

### R4 duplicate search 单 owner 复用

正常 `discover -> clarify` 路径由 context discovery 唯一执行初始 duplicate search。Clarification 通过明确、最小、checker-passed 的 public producer-output -> consumer-input projection 消费 candidate facts，不读取 Discovery private result/checkpoint，也不新增 `guru-search-duplicates` wrapper Skill。

只有明确 stale policy、target/authority mutation、用户明确要求或 #156 transition route 才能 refresh duplicate search；refresh 必须使旧 semantic decision 失效并按 owner route 重入。

### R5 readiness 单 authority snapshot

同一次 readiness validation 对同一 target issue body 最多读取一次、comments 最多读取一次。Clarity、wording 和 target projection 必须在一个 invocation-local authority snapshot 上验证，不能各自独立重读同一 authority。

### R6 dependency-aware invalidation

实现并测试最小 dependency graph。只有依赖 identity 变化的下游结果失效；base HEAD、issue body/comments/state、duplicate retarget、draft rebind、load-bearing clarification 或 wording content 的真实变化仍 fail closed 或定向重入。仅 representation 改变且 exact authority identity 未变时，不得触发完整 semantic chain。

### R7 分发一致性

所有实质变更先落 canonical package、schema、contract、tests，再经 preset installer 同步 dogfood 和声明平台副本。不得恢复共享 `guru_team_trellis.py`、聚合 checker、compatibility fallback 或跨 package private-state 读取。

## 性能预算

以下是最高允许 ceiling；设计阶段的 baseline test 仅可收紧，不得放宽：

1. current context snapshot 下，一条 `discover -> clarify` 链的 issue duplicate search 总数等于 1。
2. Public wrapper 消费 exact checker-passed result/receipt 时，新增 live Git/GitHub 调用等于 0。
3. 一次 readiness invocation 对同一 target issue body 的获取次数不超过 1，comments list 次数不超过 1。
4. workspace executor 在首次业务写入前执行且只执行 1 次 authoritative base/live mutation-boundary recheck。
5. 任一依赖 authority identity 改变后，旧 snapshot/receipt 的接受次数等于 0。

## 验收标准

- AC1：提交可重复运行的 before/after call-count tests；结果按调用类别断言，不以 wall-clock 作为唯一证据。
- AC2：六个 Phase 0 package 的 current call graph 均被测试覆盖；仅修改能在 fresh baseline 复现重复调用的 owner。
- AC3：R2-R6 的 happy path 与 stale/mutation 负路径全部通过 package-local tests 和 public-only 跨 Skill integration。
- AC4：AI semantic gate、clarity/wording/readiness ownership、typed exits 和正常 failure routes 与当前合同一致。
- AC5：workspace mutation-boundary recheck 保留且 call-count ceiling 通过。
- AC6：canonical source、installed package、dogfood 和 Codex/Claude/Cursor/shared projection 字节或受管 provenance 一致。
- AC7：clean throwaway install、existing repo update/reapply、workflow marketplace preview/switch、preset reapply 和完整 Phase 0 transcript 通过，无未处理 `.new` / `.bak`。
- AC8：`git diff --check`、受影响 package 的 Python compile/unit/integration tests、source/installed contract validation 和 dogfood overlay drift check 通过。
- AC9：独立 Phase 2 check 证明优化没有削弱 semantic gate、freshness、normal stale/re-entry 或 public I/O 最小化合同。

## 非目标

- 不新增只包装 duplicate search、issue read 或 checker 的公共 Skill。
- 不改变 AI 对 scope、clarity、wording、readiness 或 workspace plan 的 semantic ownership。
- 不删除或用旧 snapshot 替代 mutation-boundary recheck。
- 不恢复共享 monolith、跨 Skill private artifact 读取或长期语义缓存。
- 不处理恶意伪造、对抗性输入、并发压力、锁、TOCTOU、额外 fault injection、crash consistency 或跨 OS 原子性。
- 不重新实现 #132 的 workflow thinning，也不关闭 #98 或 #132。

## Docs SSOT Plan

- `trellis/skills/guru-team/packages/*/references/contract.md`：各 package 的 snapshot、receipt、freshness、duplicate reuse 和 mutation boundary 所有权。
- `.trellis/spec/workflow/skill-package-contract.md`：跨 Skill 最小 public projection 与 private state 总体规则；仅在实现形成新的通用合同后更新。
- `.trellis/spec/workflow/companion-scripts.md`：recorder/checker/serializer 的确定性边界与 call-count harness 规则。
- `.trellis/spec/workflow/data-contracts.md`：新增或迁移 schema/receipt/snapshot 字段时的唯一数据合同。
- `trellis/presets/guru-team/README.md`、`trellis/workflows/guru-team/README.md`：仅在安装、验证命令或公开行为发生用户可见变化时更新。
- canonical 变更同步到 `.trellis/guru-team/**`、`.agents/skills/**`、`.codex/skills/**` 及声明平台副本；不把安装副本写成 SSOT。

## 未决问题

无。具体受影响 package 和收紧后的 ceiling 由 R1 的 fresh deterministic baseline 决定，不需要新增产品选择。
