# #460 修复 created_issue_result 3.0 plan schema 冲突

## 需求权威

- GitHub Issue：`https://github.com/castbox/guru-trellis/issues/460`
- 当前数据合同：`.trellis/spec/workflow/data-contracts.md` 的 `Task Workspace Plan And Result`
- 当前能力边界：`CUR-CAP-006`，由 `guru-create-task-workspace` 持有 task workspace 创建与恢复能力

## 问题

`guru-create-task-workspace` 的 runtime 与 result schema 已输出
`guru-task-workspace-result-3.0`。plan schema 内嵌的
`createdIssueResult.schema_version` 却固定为 `2.0`。因此 reviewed draft 已经创建
Issue 后，fresh existing-Issue Intake 无法把 checker-passed result 3.0 作为完整
provenance 写入 plan，workspace 与 Trellis task 创建在 schema 校验阶段被阻断。

## 目标

在 #454 退役旧 `task_workspace` 模型前，使当前已发布路径能够消费自己产生的
created-Issue result 3.0，并继续执行 fresh Intake、workspace 创建和 task 创建。

## 功能要求

1. `guru-task-workspace-plan` 顶层 `schema_version` 必须保持 `2.0`。
2. plan 内嵌 `createdIssueResult.schema_version` 必须只接受 `3.0`。
3. 内嵌对象必须继续满足完整 `created_issue` variant 合同，包括 passed executor、
   passed checker、`refresh_review` route、固定 consumer、result facts digest 与 created
   issue binding digest。
4. fresh existing-Issue plan 必须继续校验 live Issue 的 repo、number、canonical URL、
   open state、title/body identity、updated time 与完整 Intake identity。
5. reviewed draft 创建成功后发生可恢复中断时，恢复必须绑定同一个 Issue，create
   mutation 次数必须保持为一。
6. checker-passed result 3.0 被 fresh plan 接受后，后续 branch、worktree、runtime
   mappings 与 planning task 创建必须成功。

## Fail-Closed 要求

- 缺失 provenance、只提供 binding、只提供 result、不完整 result、binding digest 不匹配、
  result facts digest 不匹配或 live Issue identity 不匹配时，plan 必须拒绝输入。
- 内嵌 result `schema_version = "2.0"` 必须保持无效。
- 修复不得放宽 freshness、digest、live Issue 或 complete Intake 校验。

## 范围边界

- 只修改 `guru-create-task-workspace` 的 plan schema、定向测试与受管投影。
- 不新增 Skill ID、command ID、schema ID、typed exit、consumer、adapter、fallback、
  dual-read 或 dual-write。
- 不实现 #454 的 `guru-create-issue`、`guru-create-task` 或 lifecycle substrate。
- 不修改 `chengtuo-resume`，不创建或关闭业务 Issue。
- 不执行完整 Release Gate 多平台矩阵；该矩阵由专项 Release Gate owner 持有。

## 验收标准

- [ ] 实际 runtime 产生且 checker-passed 的完整 `created_issue` result 3.0 通过 plan schema。
- [ ] plan 顶层版本仍为 `2.0`，嵌入版本 `2.0` 被 schema 拒绝。
- [ ] 缺失、不完整、digest mismatch 与 live Issue mismatch 的 provenance 回归全部 fail closed。
- [ ] reviewed draft 新建与精确恢复路径都产生 checker-passed result 3.0。
- [ ] 恢复路径证明只存在一次 Issue create mutation。
- [ ] created-Issue -> fresh Intake -> workspace/task creation 的定向回归通过。
- [ ] canonical 与 dogfood package 投影字节一致，preset drift 检查通过。
- [ ] 代表性 installed preset 回归证明安装后的 package 接受 result 3.0 并创建 task workspace。
- [ ] `guru-create-task-workspace` package contract/runtime 测试与受影响 preset 测试通过。

## 完成边界

本任务完成只证明 Issue #460 的当前 package 路径恢复一致性。它不证明 #454 已完成，
不证明完整 Trellis upgrade/update 矩阵通过，也不证明新版本已经发布。
