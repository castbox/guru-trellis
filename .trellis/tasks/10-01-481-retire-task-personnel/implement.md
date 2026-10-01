# #481 实施与验证

## 实施顺序

1. 清点活动源、schema、运行时、示例/测试、workflow/skill、配置、README/spec、overlay 和平台投影的任务人员依赖；把 GitHub 平台 assignee、Git author、资源 owner 与历史诊断区分出来。
2. 更新 Guru create-task public schema/例子/CLI 与 runtime；移除 `task.json.delivery_target` 写入及其创建后读取，逐个检查其他 consumer 是否真正需要该字段。按上游 current task schema 处理任务元数据，并验证 Issue/no-Issue 创建及旧 public input 拒绝。
3. 收敛 TaskId 唯一性、当前 task inventory、旧 archive 严格只读定位和 Reactivate/Finish 拒绝边界；覆盖结构化 source 优先、fallback 冲突、重复与线索缺失。
4. 回归 #454 的 session bind/switch/rebind/retirement、branch bind/rebind/retirement、checkout、资源归属；同步 brainstorm 及 #292 边界文案。
5. 将精确候选写入 canonical source lock、manifest/README/spec 与 installed provenance；按上游 Fork 模板更新受管的 `trellis-brainstorm` 和官方 task/session 脚本，经 preset/overlay 正式机制更新 dogfood 和声明平台，不修改历史归档。变更后的 RDT 与 Architecture 先写 task-owned contribution，再由各自 owner 审查推广共享 current。
6. 运行受影响 package/runtime 定向测试、旧档案/新任务 fixture、source validator、canonical/dogfood/installed 及实际平台加载、代表性 clean throwaway、reapply/drift、sidecar/update 定向检查；记录未跑的完整 Release 矩阵。
7. Phase 2 semantic review 之后，分别提交精确 commit 计划、完整 base-to-HEAD Branch Review、Delivery PR 计划和后续 merge/Closure/Finish 计划，任何 Git/GitHub 写入均另取确认。

## 预期修改范围

`trellis/skills/guru-team/packages/`、`trellis/skills/guru-team/runtime/task_lifecycle/`、`trellis/presets/guru-team/`、`trellis/workflows/guru-team/`、各平台安装投影、根/安装 README、manifest 与 `.trellis/spec/` 的受影响 current authority。历史 `.trellis/tasks/archive/**` 保持原字节。

## Docs SSOT Plan

- 先在 `docs/requirements-design-test-contributions/481-retire-task-personnel/` 写 task-owned Requirements、Design、Test 与 traceability；当前 `.69` 三层权威仅由 RDT owner 在完整审查后推广。
- `docs/architecture/contributions/481-retire-task-personnel.md` 保存 task-owned Architecture before/after、owner 和兼容退出；当前 `.69` Architecture 仅由 Architecture owner 在独立 Branch Review 后推广。
- `.trellis/spec/workflow/`、canonical package/installer README、根 README 和 source/extension manifest 随实现同步更新，明确新 Fork 版本、严格旧格式拒绝和安装边界。对旧 README、归档、历史版本目录只标示其历史性，不做溯源修改。
- #292 的 Phase 1 author 文档和完整 Release Gate 文档不属于本次修改；其矩阵证据在 #481 中标为未验证的独立边界。

## 验收门禁

每项测试记录精确命令、exit 和当前候选身份。测试通过不替代 AI 对 #481 全范围、#454 保留合同、#292 排除项和未验证安装/升级边界的判断。
