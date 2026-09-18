# #432 修复 historical predecessor validator

## Goal

修复 #410 Stage 2 发现的 historical existing-install validator 前序版本硬编码，使两个明确指定的 immutable predecessor 可以分别建立独立 target，并绑定同一个 exact candidate 完成 update、workflow preview/switch 与 preset reapply 验证。

## Requirements

- existing-install 前序 extension identity 必须从 `--before-tag` 导出的 immutable source tree 读取，不得保留 `0.6.5-guru.36` 或其他单一历史版本硬编码。
- 提供只运行一个选定平台 existing cell 的显式定向模式；不得把 #410 的定向验证扩张为累计六 cell release matrix。
- 定向结果必须包含精确 before tag、annotated tag object、peeled commit、前序 extension/CLI、candidate source identity 和 cell 结果。
- wrapper 必须显式转发 before tag、before CLI、platform、predecessor source/commit 和 candidate Fork source。
- official Trellis update 后、marketplace preview/force 前，active workflow 必须精确匹配该 update 路径的受管理身份：migration 使用 pinned candidate Trellis 的 native template，普通 update 使用 immutable predecessor workflow；未知或用户修改字节必须原样保留并 fail closed。
- `focused` 与 `full` 的既有入口和语义保持不变。
- 两个 predecessor target 必须由两次独立 invocation 和不同 work root 创建，不共享状态，也不泛化为支持任意历史版本。

## Acceptance Criteria

- validator 生产代码与测试中不再使用 `0.6.5-guru.36` 作为 existing-cell 固定身份。
- `v0.6.16-guru.1` 精确解析为 extension `0.6.16-guru.41`，`v0.6.15-guru.6` 精确解析为 extension `0.6.15-guru.40`。
- 定向模式只执行一个 `<platform>-existing` cell，并明确 `predecessor_upgrade_verified=true`、`full_matrix_verified=false`。
- 错误 tag、CLI、predecessor source/commit、installed manifest 或 candidate source drift 均 fail closed。
- update 后 active workflow 身份未知时必须在 `--create-new` / `--force` 前失败；两种合法 managed identity 均有回归覆盖。
- focused unit/contract tests、source/installed validators、projection parity、ownership、dogfood drift、diff/residue 检查通过。
- 修复经标准 task、Branch Review、Publication、Finalizer、PR merge 进入 `main`；随后 #410 必须从新的 `origin/main` 冻结全新 candidate 并从零重跑 Stage 2。

## Non-goals

- 不声明任意历史版本兼容。
- 不修改 npm package、Trellis upstream、全局 Python/npm、业务仓库或生产基础设施。
- 本 task 不创建 `v0.6.17-guru.1` tag/Release，也不关闭 #410。
