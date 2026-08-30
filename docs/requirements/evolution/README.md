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
| `requirements_ready_for_design` | [`requirement-main.md`](./requirement-main.md) | Authority、产品总述、入口组织、52 UC、84 功能需求、核心能力、50 个验收 fixture、闭环、目标追踪和 Design gate；`REQ-REV-133..142` 已把 #311/#312 定义为 selected-base current 前置，将 PR #317 exact installed platform-set preservation 折入现有 capability/fixture，并将 PR #318 归类为 fact-only caller-inventory/provenance correction；current authority fresh 重绑到 `origin/main@5650df47…`，fresh Requirements semantic、Strict technical 与确定性闭包审核已通过，P1/P2/P3 finding 和 high-risk open question 均为 0 |
| `requirements_ready_for_design` | [`requirement-non-functional.md`](./requirement-non-functional.md) | 34 项执行效率、上下文治理、可靠性、兼容/分发、安全、platform preservation 和范围豁免的唯一主定义；`EVO-NFR-034` 的正反向质量门槛已纳入同一 fresh exact-candidate 审核 |
| `requirements_trace_ready_for_design` | [`current-capability-inventory.md`](./current-capability-inventory.md) | selected-base `.42` current 可观察能力、23 个 `CUR-CAP-*`、13 个 `TARGET-DELTA-*` 与 50 个 normal-path fixture 的 successor/差集；#311 已折入 `CUR-CAP-013/014/017/018/019`，#312 已折入 `CUR-CAP-012`，PR #317 平台保真折入 `CUR-CAP-013/014/017`；`.42` fact-only additions、`a41b8a34...9f560ec1` 与 `736ef333...5650df47` delta 不新增能力，`9f560ec1...736ef333` 是 material advance；Requirements-stage trace closure 与 fresh review 已通过，pre-`REQ-REV-142` Design review 仍 stale，但 current exact candidate 的 fresh Design review 与确定性闭包已通过 |

读取顺序：`requirement-main.md` -> `requirement-non-functional.md` ->
`current-capability-inventory.md`。

入口组织的主定义见 `requirement-main.md` 第 1.6 节和第二章；shared-layer/host coverage
的主定义见 `current-capability-inventory.md` 第 1.2 节，stock semantic ownership 与
caller 边界见 `requirement-main.md` 第 3.7 节。
本轮无独立 UI、无服务端 API contract，也不新增或改变用户 CLI command contract。依据
`requirement-doc-standard` 第 5.1 节的 API/CLI 适用标准，API/CLI 均判定为整体不适用，不创建
对应 intent 主定义；外部 Trellis CLI 仅按主文档所述作为 provider test stimulus。

current runtime Requirements 仍从 [`../README.md`](../README.md) 的 active version 读取。
