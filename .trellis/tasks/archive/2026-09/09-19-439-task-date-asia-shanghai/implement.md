# 实现计划

1. 在 `.trellis/scripts/common/paths.py` 增加 Asia/Shanghai 业务日期 helper，并保留现有公开函数的返回格式。
2. 修改 task store 的创建日期、完成归档日期和 archive destination 月份计算。
3. 修改 `guru-create-task-workspace` 的 canonical 与 dogfood executor，复用统一 helper 或等价的明确时区函数。
4. 更新相关测试，覆盖 UTC、Asia/Shanghai、固定 instant 与上海午夜边界。
5. 执行 targeted tests、Python 编译、`git diff --check`，并检查 canonical/dogfood 漂移。

不修改 session binding、Issue #438 资源、GitHub 状态或发布流程。
