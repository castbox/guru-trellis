# #460 实施计划

## 交付切片

本任务只有一个可独立交付切片：校准 created-Issue result 嵌入版本，补齐同一生产路径的
fail-closed 与 installed 回归，并同步受管投影。完成后 Issue #460 的全部 accepted scope 结束；
#454 生命周期重构仍由 #454 owner 持有。

## 实施步骤

1. 修改 canonical plan schema：
   - 文件：`trellis/skills/guru-team/packages/guru-create-task-workspace/schemas/task-workspace-plan.schema.json`
   - 只把 `$defs.createdIssueResult.properties.schema_version.const` 改为 `3.0`。
   - 保持顶层 plan version、schema id、required 字段、variant、consumer 与 digest 结构不变。
2. 扩展 package contract 测试：
   - 使用 runtime/checker 产生完整 `created_issue` result 3.0。
   - 验证 fresh existing-Issue plan 接受该 result。
   - 验证嵌入 2.0、单侧 provenance、不完整 result、binding digest、result digest 与 live Issue mismatch
     均失败。
   - 保留并加强 stateful recovery create-count 断言，证明恢复没有第二次 Issue mutation。
   - 使用另一个真实 executor/checker 通过的 created-Issue result，验证其不能与当前外层
     target 组合，即使两侧 digest 都各自合法。
3. 收紧 runtime plan 校验：
   - 在 `runtime/common.py::validate_plan` 比较嵌入 provenance 与外层 target 的 repo、number、
     canonical URL、state、title/body digest 和 updated time。
   - identity 不一致沿用 `stale_identity`，不新增公共合同或兼容路径。
4. 扩展受管安装集成测试：
   - 在 preset 安装后的 package 上执行 reviewed draft create 或精确恢复。
   - 把 checker-passed result 3.0 交给 fresh existing-Issue Intake/plan。
   - 执行 workspace/task creation，并断言 `created`、planning task、runtime mappings 与单次 Issue create。
5. 运行 preset apply 同步 dogfood package：
   - `trellis/presets/guru-team/scripts/bash/apply.sh --repo .`
   - 检查命令产生的 `.new`、`.bak` 与非预期文件；任何非本任务改动都停止并审查。
6. 执行定向验证并修复本任务 finding，直到全部通过。

## 验证命令

以下命令在 task worktree 根目录执行：

```bash
python3 -m unittest discover -s trellis/skills/guru-team/packages/guru-create-task-workspace/tests -p 'test_*.py'
python3 trellis/presets/guru-team/scripts/python/test_workspace_invocation_integration.py
python3 trellis/presets/guru-team/scripts/python/test_verify_installed_task_workspace.py
bash .trellis/guru-team/scripts/bash/check-skill-packages.sh --root . --json --mode source
bash .trellis/guru-team/scripts/bash/check-skill-packages.sh --root . --json --mode installed
bash trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh --repo .
```

实现后再依据实际 changed paths 运行受影响 preset installer 测试。完整
`verify_trellis_compatibility_matrix.py` 与 Release Gate 多平台矩阵不在本任务验证集内。

## 检查清单

- [ ] schema diff 只有嵌入 result 常量从 2.0 到 3.0。
- [ ] package 正向回归使用 checker-passed 完整 result 3.0。
- [ ] 2.0 与所有 partial/mismatch case 仍 fail closed。
- [ ] checked provenance 与外层 target 的完整 Issue identity 不一致时 fail closed。
- [ ] recovery create mutation count 保持为一。
- [ ] fresh plan 后 workspace/task 创建成功。
- [ ] canonical 与 dogfood package 无 drift。
- [ ] 代表性 installed 路径通过。
- [ ] shared Docs SSOT 无需修改的结论经 Phase 2 live reread 保持成立。
- [ ] 没有引入 #454 内容、兼容层、无 consumer 状态或 3000 行文件触发项。

## 停止条件

出现下列任一事实时停止当前实施并返回对应 owner：

- 需要接受 legacy result 2.0 或引入双版本读取；
- 需要修改 Skill ID、schema ID、typed exit、consumer 或 workflow routing；
- 发现 current RDT/Data Contracts 并非 result 3.0 authority；
- 需要修改 `chengtuo-resume` 或业务 Issue；
- 需要扩大到完整 Release Gate 矩阵；
- preset apply 产生与本任务无关且无法隔离的修改。

## 副作用边界

Phase 1 只写 task planning artifacts。实现批准是修改 schema、测试与 dogfood 投影的前置条件。
commit、push、PR、merge、Issue closure、release 与资源清理均需要各自后续流程和独立确认。
