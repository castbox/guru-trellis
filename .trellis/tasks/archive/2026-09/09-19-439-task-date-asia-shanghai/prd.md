# 需求：统一 Trellis task 日期生成的 Asia/Shanghai 时区语义

## 背景

官方 task store、共享路径工具和 Guru workspace executor 当前分别使用未显式指定时区的本地时间生成 task 日期身份。进程运行在 UTC、Asia/Shanghai 或跨午夜窗口时，可能得到不同的目录前缀、`createdAt` 或归档月份。

## 目标

- 所有 task 日期身份按 `Asia/Shanghai` 计算，不依赖进程本地 `TZ`。
- 官方 task store 与 workspace executor 使用同一日期语义。
- 保留 UTC instant 时间戳和 session binding 语义，不通过日期推断当前 task。

## 范围

- `.trellis/tasks/<MM-DD>-<slug>` 日期前缀。
- `task.json.createdAt` 的业务日期。
- task archive 的 `YYYY-MM` 目录。
- `guru-create-task-workspace` canonical 与 dogfood runtime 的 task 路径预检。
- TZ 环境和 Asia/Shanghai 午夜边界回归测试。

## 验收标准

1. `TZ=UTC` 与 `TZ=Asia/Shanghai` 在同一业务时刻产生相同的上海日期身份。
2. 业务时刻从 `2026-09-19 15:59:59+08:00` 跨到 `2026-09-20 00:00:00+08:00` 时，所有路径同步切换为 `09-20` / `2026-09-20`。
3. task store 与 workspace executor 对同一时刻计算相同的目录前缀。
4. UTC 审计时间戳仍为 UTC，不被业务日期 helper 改写。
5. session binding/current-task 校验行为没有变化。
