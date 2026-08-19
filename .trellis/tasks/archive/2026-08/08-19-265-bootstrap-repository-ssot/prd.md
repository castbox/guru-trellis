# #265 编排 Bootstrap 双 SSOT 与 Spec 投影

## 目标

在当前 Trellis 0.6.5 / Guru source-dogfood surface 上新增并激活
`guru-bootstrap-repository-ssot` semantic Skill，为 `new_repository`、
`existing_repository` 和 `repair` 提供一次性、可重入的仓库基线编排。Skill
调用官方 `trellis-spec-bootstrap`、#263 Requirements/Design/Test SSOT 和
#264 Architecture Baseline，但只消费各自最小 schema-validated typed output；
由自身负责跨 SSOT 对齐、激活判断和 `.trellis/spec` 概要投影。

## 范围

- 新增 Interface 1.4-compatible public package、profile-specific schemas、四个 typed exits、唯一 consumers/projections、runtime wrapper、contract tests/evals 和声明平台副本。
- 将 canonical registry、global workflow mandatory invocation、preset inventory、dogfood/installed copies 与 README 导航同步到同一公共 API。
- 明确 upstream、#263、#264 的调用边界；不得复制子 Skill 流程、读取 private checkpoint 或把 Bootstrap 变成每个业务 task 的总控 wrapper。
- `.trellis/spec` 只投影 canonical locator、版本/status、适用范围、读取/更新规则、traceability 入口和 freshness/route 摘要，不复制需求、设计、测试、架构正文或 active task。
- 共享 tracked docs/spec 写入、upstream bootstrap task finish/archive 和并行 writer 冲突均由 Bootstrap owner 的语义门禁与确认控制；installer/upgrade/update/reapply 只能报告状态。

## 非目标

不重写 #263/#264 内部语义，不实现 #260/#267 的完整矩阵或 release，不修改 Trellis upstream/global npm/node_modules，不创建 repair Issue，不做 Git delivery/PR/merge/cleanup，不引入 shared ledger、锁、TOCTOU 或攻击模型。

## 验收标准

- [ ] 三个必需 profile 均能通过 workflow 与 standalone mode 复用同一 preconditions、freshness、semantic gate、confirmation 和 typed exits。
- [ ] `completed`、`baseline_incomplete`、`repair_required`、`blocked` 各有唯一 consumer；incomplete/repair 不误报完成、不自动 archive bootstrap task。
- [ ] #263/#264 只接收最小 canonical locator/version/status/freshness projection，Bootstrap 完成跨版本、行为、设计、测试和架构约束对齐判断。
- [ ] canonical/dogfood/installed/declared-platform、preset reapply/drift、`.new/.bak`、executable mode、README command 和一个 clean current-version throwaway 通过；完整多平台矩阵明确留给 #260/#267。
- [ ] 既有 task、Docs SSOT、base reconciliation、Planning、Phase 2、Branch Review、commit/publication/Finish 能力保持可用，公共包不包含业务私有正文。

## Docs SSOT Plan

公共 Skill 行为 SSOT 仅在 `trellis/skills/guru-team/packages/guru-bootstrap-repository-ssot/`；全局路由仅在 `trellis/workflows/guru-team/workflow.md` 声明 mandatory invocation 和 typed consumers。preset README、registry/interface、平台副本和 dogfood copy 只承接安装、导航和 projection contract。目标业务仓库的真实 Requirements/Design/Test、Architecture Baseline 与 `.trellis/spec` 正文仍由 #263/#264 及 Bootstrap runtime 按其 owner boundary 管理。
