# 实施计划

1. 定位 canonical workspace boundary helper、Phase 2 implementation coordinator 及所有 task-local write 入口，确认当前调用链和安装投影。
2. 抽取或补强统一的 live task/worktree identity validator；保持既有公共 Skill ID、typed exits 和 task-free 路径兼容。
3. 将 validator 接入实现 dispatch 前和每次源码、测试、task artifact 写入前；校验失败零写入并返回既有 fail-closed 路由。
4. 增加 Issue #327 要求的临时仓库/linked worktree 回归矩阵，并保留 dirty main 内容。
5. 同步 canonical workflow/preset/spec 与 `.agents`、`.codex`、`.claude`、`.cursor` 等声明投影，执行 drift 检查。
6. 运行 package targeted tests、安装副本验证、Trellis check、完整 diff review；不执行无关 Release Gate 或自动清理。
