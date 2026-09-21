# #460 技术设计

## 当前合同

`guru-task-workspace-plan-2.0` 是 workspace mutation 前的闭合 plan。其
`target.created_issue_result` 在 created-Issue recovery 路径中承载完整
`guru-task-workspace-result-3.0` `created_issue` variant。Data Contracts 已经明确该
关系，runtime、checker 与 result schema 也都使用 `3.0`。

原始缺陷位于
`trellis/skills/guru-team/packages/guru-create-task-workspace/schemas/task-workspace-plan.schema.json`
的 `$defs.createdIssueResult.properties.schema_version`。该常量仍为 `2.0`，与同一
package 的 producer contract 冲突。

合并当前 `main` 后的完整 Branch Review 还发现一个同 scope 的一致性缺口：
`runtime/common.py::validate_plan` 虽然重算外层 result、内层 `created_issue` 和 binding
digest，却没有比较内层 provenance 与外层 `plan.target` 的 Issue identity。两个分别合法、
但属于不同 Issue 的 checked result 和 target 因此可能被错误组合。

## 设计决策

### 1. 直接修改嵌入版本常量

把 `$defs.createdIssueResult.properties.schema_version.const` 从 `2.0` 改为 `3.0`。
plan 顶层 `$defs`、`$id` 与 `properties.schema_version.const` 均保持不变。

这是 current producer/consumer 的合同校准，不是新版本兼容层。实现不接受嵌入
result 2.0，不增加 `oneOf` 双版本，不增加转换器，也不复制
`task-workspace-result.schema.json` 之外的新 result owner。

### 2. 保留完整 provenance 校验

现有 `createdIssueResult` 对象结构、required 字段、closed object、variant、route、
consumer 与 digest 字段不变。`runtime/plan_input.py`、`runtime/common.py`、
`runtime/check.py` 和 `runtime/recover.py` 的现有 semantic/deterministic ownership 不迁移。

在现有 `validate_plan` 中增加单一直接校验：把嵌入 `created_issue` 的 `repo`、`number`、
`canonical_url`、`state`、`title_sha256`、`body_sha256`、`updated_at` 映射到外层 target 的
对应字段并要求完全相等。失败继续使用现有 `stale_identity`；不新增 schema、wrapper、
compatibility path 或持久状态。

测试只构造生产 recorder/checker 能产生的完整 result，并验证：

- result 3.0 能够进入 fresh existing-Issue plan；
- result 2.0 在 schema 边界被拒绝；
- 缺一侧 provenance、字段缺失、binding/result digest 漂移、live Issue 漂移仍被拒绝；
- 两个各自 checker-passed、但 Issue identity 不同的 target/result 组合被拒绝；
- reviewed draft recovery 不执行第二次 create mutation。

### 3. 端到端回归位置

package contract 测试负责精确 schema 与 fail-closed 行为。
`test_workspace_invocation_integration.py` 负责受管安装后的 public invocation 链路，新增
created-Issue result 3.0 经 fresh plan 到 workspace/task creation 的回归。
如 installed verifier 已提供相同生产调用链，则复用该 helper，不建立第二套 fixture
协议。

### 4. Canonical、dogfood 与 installed 投影

canonical source 位于 `trellis/skills/guru-team/packages/guru-create-task-workspace/`。
修改 canonical 与测试后，执行 Guru preset apply，把 package 同步到
`.trellis/guru-team/skills/packages/guru-create-task-workspace/`。随后执行 dogfood drift
检查。代表性临时安装通过现有 preset 测试或 installed verifier 构建，不手工维护第三份
source。

## Subtraction-First 结论

- 当前 supported consumer 是 fresh existing-Issue plan recorder/schema validation。
- 当前 producer 是 `guru-task-workspace-result-3.0` created-Issue checker output。
- 直接演进影响是旧的错误嵌入值 2.0 被继续拒绝；不存在合法的 result 2.0 producer。
- 不保留 legacy path，不增加 compatibility exception。
- #454 是旧 package 的未来删除 owner；本任务不修改其 target authority。

## Architecture 影响判断候选

本任务不改变 Skill ownership、public Skill graph、typed exits、consumer、workflow routing、
Architecture decision、GAP lifecycle 或 shared-current owner。它使 schema 投影重新符合现有
Data Contracts 与 `minimum-necessary-complexity`、`debt-one-way-convergence`。规划阶段预期
route 为 `no_architecture_impact`，仍由 Architecture owner 通过正式 invocation 独立确认。

## Docs SSOT Plan

- 策略：`no_docs_update_needed`。
- Requirements/Design/Test current authority 已声明 `guru-create-task-workspace` 的恢复能力与
  provenance 边界；Data Contracts 已明确嵌入完整 result 3.0。
- 不修改 shared RDT、Architecture、workflow README 或 package contract 文本，因为本任务不改变
  已有语义，只修正落后实现投影。
- task-local `prd.md`、`design.md`、`implement.md` 记录 Issue #460 的范围、设计与验证计划，随
  task 历史归档。
- Phase 2 必须重新读取上述 durable locators；若实现发现 durable authority 与代码真实行为存在
  新冲突，停止编辑并返回 Docs SSOT/Architecture owner。

## 风险与控制

- 风险：只改 schema 会漏掉生产调用链。控制：增加 result 3.0 到 fresh plan，再到 workspace/task
  mutation 的集成回归。
- 风险：fixture 手工构造放宽完整 provenance。控制：复用 runtime finalize/checker 输出，并保留
  digest 与 live Issue mismatch 负例。
- 风险：canonical 修复但 dogfood 仍旧。控制：preset apply 后执行 source/installed package 检查与
  dogfood drift 检查。
- 风险：把普通 Issue 扩张成 Release Gate。控制：只运行 package、受影响 preset、代表性 installed
  路径；完整矩阵保持未验证。
