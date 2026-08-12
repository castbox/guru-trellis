# 技术设计

## 1. 设计原则

本任务优化的是确定性 supporting I/O，不改变 semantic Skill 边界。实现顺序固定为：先计数复现，再按 owner 收敛，再验证 stale/mutation；没有 fresh baseline 证据的历史重复点不修改。

## 2. 架构边界

### 2.1 Package-local owner

六个 Phase 0 package 继续独立拥有自己的 runtime、schema、contract 和 tests。共享 runtime 仅保留 dispatcher、schema、I/O、安装验证和其它既有公共基础设施，不承载 Phase 0 业务判断或跨 package private state。

### 2.2 Invocation-local validation context

每个复用 live facts 的 package 引入局部 `ValidationContext`、`AuthoritySnapshot`，或引入具有相同不可变性、生命周期和绑定字段的值。它只存在于一次 public invocation 的进程内，包含该 owner 使用的规范化 authority facts 与调用计数，不写 tracked/ignored checkpoint。

```text
public invocation
  -> capture exact live authority once
  -> recorder/checker consume same immutable snapshot
  -> checker produces exact binding receipt
  -> serializer validates receipt + schema only
```

独立 CLI recorder/checker 仍可各自捕获 live authority，因为它们是独立 invocation；完整 workflow public invocation 必须走单进程共享路径，避免相邻重复读取。

### 2.3 Checker receipt

Receipt 是局部确定性结果，不是 semantic approval 或跨 Skill authority。Binding 字段固定为 package/schema id、result digest、直接 prerequisite identity digest、snapshot identity digest、validated operation/profile 和 receipt digest。Public serializer 只能消费同一 invocation 内的 receipt；任何字段不匹配即拒绝。

若现有 package 的 public invoke 已只做纯 schema/shape validation，则不为了形式新增 receipt。R1 基线决定采用显式 receipt 还是直接传递已验证对象。

## 3. 跨 Skill duplicate projection

Discovery 的 `context_ready` 输出向 Clarification 提供一个最小 duplicate snapshot projection，字段仅包含直接 consumer 必需的 query identity、checked-at/freshness identity、候选集合 facts 和 checker binding。候选 reason、完整 Discovery review、history evidence 和 private owner result 不跨边界。

Clarification 的 public input schema 显式接收该 projection，并按以下规则处理：

- current 且 target identity 一致：复用，不执行 search；
- policy stale、authority mutation、retarget 或显式 refresh route：拒绝旧 projection并定向返回 context refresh；
- 缺失或 identity mismatch：fail closed，不静默自行搜索后沿用旧 semantic decision。

这是现有 public API 的实质修改，必须更新 interface/schema/example/eval/consumer projection、版本/迁移说明和全部平台安装副本；不能仅在实现内部偷读上游状态。

## 4. Readiness 单快照

Readiness owner 在一次 invocation 中先构建 target authority snapshot，再用它完成 target normalization、clarity projection、wording projection 和 linkage validation。`live_issue_source` 不再由每个 projection 独立调用；comments 若属于 selected authority，同样只读取一次并投影给所有校验器。

Snapshot identity 分别绑定 target body/state/comments，避免把不同 authority 合并成一个粗粒度 hash。任一依赖改变，只失效使用该依赖的下游结果。

## 5. Workspace mutation boundary

Workspace plan recorder/checker 使用 exact checked result 收敛无状态重复校验，但 executor 在首次 branch/worktree/task/GitHub write 前必须重新执行一次 base/live authoritative recheck。测试直接断言该边界调用数为 1，并验证变化时零业务写入和 refresh/block route。

## 6. Call-count harness

在现有 fake Git/GitHub adapter 或 Phase 0 transcript harness 上增加结构化 counter。Counter 按规范化 operation id 记录，不依赖命令文本模糊匹配：

- `base.resolve`、`base.fetch`、`base.check`
- `issue.get`、`issue.comments.list`、`issue.search`
- `archive.scan`
- `prerequisite.project`、`prerequisite.validate`
- `public.serialize.live_calls`
- `workspace.mutation_boundary_recheck`

每个 transcript 输出 before/after counters 和 ceiling assertion。Test fixture 只模拟正常 operation、stale 和 mutation，不引入恶意篡改或并发压力。

## 7. 迁移与兼容

1. 先扩展 canonical schemas/interfaces，明确旧 input 的处理方式。
2. 同步 producer output 和 consumer input projection，保证唯一 consumer 可确定性验证。
3. 更新 package contract、examples、evals、tests 与 production transcript。
4. 运行 preset installer 同步 dogfood 和平台副本，处理全部 `.new` / `.bak`。
5. 通过 clean install 与 existing update/reapply 验证 managed provenance；不得依赖当前仓库历史 patch。

## 8. 失败与回滚

- Snapshot/receipt 缺失、stale、identity mismatch 或未知字段：fail closed 到现有 owner route。
- Live authority 在 capture 后、mutation 前变化：mutation-boundary recheck 拒绝并零业务写入。
- 计数超过 ceiling：测试失败，不以环境速度解释通过。
- 可按 package 独立回滚 canonical commit；public schema migration 必须整体回滚 producer/consumer，不保留半迁移状态。

## 9. 取舍

- 选择 invocation-local snapshot，而非 repository cache：减少 I/O 且不制造 freshness/cleanup 状态。
- 选择最小 public duplicate projection，而非跨 Skill private result：满足唯一 consumer 与 package isolation。
- 选择 operation counters，而非 wall-clock：结果稳定且能定位回归来源。
- 只优化 fresh baseline 可复现点：避免为历史架构制造无 consumer 的抽象。
