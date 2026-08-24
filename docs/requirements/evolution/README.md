# Guru Trellis Evolution Requirements SSOT

本目录是 Guru Trellis 下一阶段 target Requirements 的唯一文档集。它定义尚未实现的产品
目标、场景、功能/非功能要求和进入 Design 的条件，不声明 current runtime 已实现这些能力。

阶段边界：本目录整体为 `post_release` target authority。重构前稳定版
`v0.6.15-guru.1` / extension `0.6.5-guru.37` / Trellis `0.6.15` 冻结并验证 current 旧 graph；
本目录不进入该 Release candidate 的 capability gate、前置依赖或完成声明。只有该稳定版发布
闭环后，后续 Evolution Design、推进方案与新实施 Issue 链才能消费本目录。

| 状态 | Locator | 职责 |
| --- | --- | --- |
| `requirements_draft` | [`requirement-main.md`](./requirement-main.md) | Authority、产品总述、第一/二章入口组织、功能需求、核心能力、验收 fixture、闭环、目标追踪和 Design gate |
| `requirements_draft` | [`requirement-non-functional.md`](./requirement-non-functional.md) | 执行效率、安静性、上下文治理、可靠性、兼容/分发、安全和非功能范围豁免的唯一主定义 |
| `requirements_trace_draft` | [`current-capability-inventory.md`](./current-capability-inventory.md) | `.40` current 可观察能力、上一版 Design inventory 逐项 successor、target delta 与 intentionally-not-retained 差集 |

读取顺序：`requirement-main.md` -> `requirement-non-functional.md` ->
`current-capability-inventory.md`。

入口形态是 Shared/Codex/Claude/Cursor conversational workflow；本轮无独立 UI、无服务端
API contract，也不新增或改变用户 CLI command contract。API/CLI 均按需求标准判定为整体
不适用，不创建对应 intent 主定义。

Authority、现有 Issue 链边界与阶段放行规则只在
[`requirement-main.md` 第 0 章](./requirement-main.md#0-authority状态与阶段边界)定义；本
README 不复制其正文。

current runtime Requirements 仍从 [`../README.md`](../README.md) 的 active version 读取。
