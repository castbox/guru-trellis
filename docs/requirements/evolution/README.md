# Guru Trellis Evolution Requirements SSOT

本目录是 Guru Trellis 下一阶段 target Requirements 的唯一文档集。它定义尚未实现的产品
目标、场景、功能/非功能要求和进入 Design 的条件，不声明 current runtime 已实现这些能力。

文档集类别：`post_release` target Requirements。Release authority、#304 隔离、planning
snapshot 状态与阶段边界只在
[`requirement-main.md` 第 0 章](./requirement-main.md#0-authority状态与阶段边界)和
[`第 10 章`](./requirement-main.md#10-进入-evolution-design-的条件)主定义；本 README 只提供
状态、locator 与读取导航。

| 状态 | Locator | 职责 |
| --- | --- | --- |
| `requirements_ready_for_design` | [`requirement-main.md`](./requirement-main.md) | Authority、产品总述、第一/二章入口组织、功能需求、核心能力、验收 fixture、闭环、目标追踪和 Design gate；`REQ-REV-129..132` 已同步并通过修订后的 fresh Requirements、Strict technical 与确定性全稿门禁 |
| `requirements_ready_for_design` | [`requirement-non-functional.md`](./requirement-non-functional.md) | 执行效率、安静性、上下文治理、可靠性、兼容/分发、安全和非功能范围豁免的唯一主定义；cache-friendly context 与 AI-owned progression 质量合同已通过 fresh exact-candidate 审核 |
| `requirements_trace_ready_for_design` | [`current-capability-inventory.md`](./current-capability-inventory.md) | `.40` current 可观察能力、上一版 Design inventory 逐项 successor、capability-loss 与 consistency/installation 独立门禁、target delta 及 intentionally-not-retained 差集；stable-authority/context successor trace 已通过 fresh closure |

读取顺序：`requirement-main.md` -> `requirement-non-functional.md` ->
`current-capability-inventory.md`。

入口组织的主定义见 `requirement-main.md` 第 1.6 节和第二章；shared-layer/host coverage
的主定义见 `current-capability-inventory.md` 第 1.2 节，stock semantic ownership 与
caller 边界见 `requirement-main.md` 第 3.7 节。
本轮无独立 UI、无服务端 API contract，也不新增或改变用户 CLI command contract。依据
`requirement-doc-standard` 第 5.1 节的 API/CLI 适用标准，API/CLI 均判定为整体不适用，不创建
对应 intent 主定义；外部 Trellis CLI 仅按主文档所述作为 provider test stimulus。

current runtime Requirements 仍从 [`../README.md`](../README.md) 的 active version 读取。
