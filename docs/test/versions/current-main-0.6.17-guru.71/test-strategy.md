# Reference-only 创建测试策略

版本：`current-main-0.6.17-guru.71`；状态：`active`；predecessor：`current-main-0.6.17-guru.70`。本版以薄继承保留[不可变前驱的完整合同](../current-main-0.6.17-guru.70/test-strategy.md)；未由本版显式替换的 requirement/design/test、owner、边界、NFR 和 trace 全部继续有效。前驱版本身份、旧 source pin、历史计数与验证结果仅表示当时快照，当前版本事实以下文为准。Architecture：`docs/architecture/README.md` / `current-main-0.6.17-guru.71` / `active`。

## T490-01

正式 create-task wrapper -> official writer -> result recovery -> identity wrapper 覆盖 exact_source/reference_only/no_issue，验证实际 source 与 TaskId/generation/TaskRef 和恢复前后 metadata bytes。

## T490-02

C6 正常支持两种 Issue disposition，仍不支持 follow_up/parent 创建；复用 session/branch/checkout/resource/source 既有回归。

## T490-03

current official metadata fixture 验证 reference-only/no_issue Closure no_mutation、零 provider call、exact-source closure/recovery；不支持旧 metadata 的诊断保持只读拒绝。

## T490-04

source checker 检查真实 Fork commit/tree/parents/live CI/build marker，official projection 检查实际脚本和模板 hash；canonical、installed 和声明平台保持一致。

## T490-05

一个代表性 Codex clean init 与当前候选 update/reapply、session binding、零 sidecar/drift；local marketplace sample 与 projection parity 必须显式记录，不能晋升为 remote/native-host 或完整发布矩阵。

每项 requirement/design 映射见[反向 trace](./traceability.md)。证据与待重跑门禁由[本版计划](./test-plan.md)区分。
