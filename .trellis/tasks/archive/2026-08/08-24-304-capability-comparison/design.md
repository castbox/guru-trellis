# Design

## Boundary

变更只位于兼容性矩阵的语义比较层：

- `installed_capability_projection()` 继续采集完整 `distribution` 和 `skill_api`。
- 安装、package、projection 与 consistency validators 继续消费这些投影。
- `compare_capabilities()` 只从 capability preservation 维度排除这两个内部资产组。

## Comparison Contract

`compare_capabilities()` 保持两级判断：

1. `extension_identity` 去除版本绑定字段后仍进行比较。
2. observable capability groups 继续比较 `workflow`、`task_data` 和
   `docs_authority`。

`distribution` 与 `skill_api` 不进入 capability blocking differences。该调整不改变
projection 数据格式，也不影响其它 validator 对两组数据的检查。

## Projection Consistency Repair

`.trellis/spec/docs/requirements-design-test-ssot.md` 与
`.trellis/spec/architecture/baseline-usage.md` 是 Agent 使用的最小 projection，
不是新的业务 authority。修复只同步以下可重建字段：

- current version：`current-main-0.6.5-guru.40`；
- current status 与既有 canonical locators；
- `.40` authority 已声明的 source binding。

Requirements、Design、Test 与 Architecture 正文继续分别由 `docs/**/README.md`
指向的 `.40` 内容独占。projection repair 不进入 capability blocking comparison，
但继续由 consistency gate 独立验证。

## Test Design

在现有 `test_capability_comparison_ignores_version_only_changes` 附近保留同一组
fixture，并增加两个非阻断断言：

- 移除一个 installed package file/mode 条目。
- 清空 typed output schema id 投影。

现有 workflow marker loss 用例继续证明 observable capability loss 会阻断。

## Compatibility And Rollback

- 无 public API、schema、CLI 或 installed-file inventory 变更。
- 无数据迁移和运行时状态迁移。
- 回滚点为 `compare_capabilities()` 的 group tuple、对应测试断言和两份最小
  projection identity 行。
