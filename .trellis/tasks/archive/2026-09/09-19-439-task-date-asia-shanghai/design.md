# 设计：统一 task 日期生成的 Asia/Shanghai 时区语义

## 方案

在共享 task path 工具中定义唯一的 `ZoneInfo("Asia/Shanghai")` 日期 helper，分别提供业务日期的 `MM-DD`、`YYYY-MM-DD` 和 `YYYY-MM` 格式化结果。官方 task store 复用该 helper；workspace executor 通过同一 canonical helper 计算预检路径，并同步到安装副本。

只替换 task identity 相关的本地日期读取。`datetime.now(timezone.utc)`、GitHub 时间戳解析和生成 UTC 审计时间的代码保持不变。

## 边界

- 只使用日期 helper 计算 task identity；不从日期猜测 session 或 active task。
- `ZoneInfo` 不可用时让运行时显式失败，不回退到系统时区。
- archive 月份也属于 task 日期身份，必须与创建日期采用同一时区。

## 验证

- 共享 helper 的固定 instant 单元测试。
- 子进程 `TZ=UTC` / `TZ=Asia/Shanghai` 的 task store 与 workspace executor 回归测试。
- 上海午夜前后目录前缀、`createdAt` 与 archive 月份的边界测试。
- canonical/dogfood 文件同步与 Python 编译检查。
