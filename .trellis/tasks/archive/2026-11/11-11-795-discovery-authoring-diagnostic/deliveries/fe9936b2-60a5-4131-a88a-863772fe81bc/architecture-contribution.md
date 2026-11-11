# #795 Discovery authoring 结构诊断与恢复边界

Identity：`architecture-contribution-795-discovery-authoring-diagnostic-v1`；状态：`reviewed_candidate`；Task=`11-11-795-discovery-authoring-diagnostic` / generation=`0` / Delivery=`fe9936b2-60a5-4131-a88a-863772fe81bc`。来源为 [Issue #795](https://github.com/castbox/guru-trellis/issues/795)、整体 root PRD 和本 Delivery PRD。change path：`target_native`。适用 baseline=`guru-trellis-architecture`，constitution=`guru-trellis-design-constitution-v1/current`，change contract=`guru-trellis-architecture-change-contract-v1`。本文是 Planning 的隔离 Architecture 拟写，不是 Check、Review、Promotion 或完成结果。

## Before / After

Before：`guru-discover-change-context` 的 Git-object record 路径在完整 owner-result schema 校验前读取 `history_review.deep_reads[*].source`。正常 authoring 把 `source` 写成 `source_kind` 时触发未捕获 `KeyError`，再由共享 dispatcher 返回 `internal_error/runtime`。Interface、合同和示例同时混用当前 Git-object 4.0、同步来源 3.0 及旧 interface/example 版本，普通纠正后重跑原 record/check/invoke 的边界也不够明确。

After：Discovery 在读取 reviewed Git evidence 前，先以现有 4.0 owner-result schema 校验当前 authoring 结构，并使用既有 `schema_mismatch`、`field_path` 和 `remediation`。Git evidence、history、candidate、freshness 与最终 result identity 校验随后保持不变。当前 Interface、合同和示例唯一导航 Git-object authoring 到 pre_task 4.0、context_request 2.0、owner-result 4.0；同步来源 owner-result 3.0 保留为明确兼容资产。恢复文本说明首次失败保留，原 owner 可用完整正确输入重跑原链；真实未知异常继续走向 `internal_error` 维护 owner。

## Concerns

| Concern | 本批判断 |
| --- | --- |
| authority-binding | applicable：Planning 绑定 `guru-maintain-architecture-baseline:planning:3.0`、`candidate_assessment`、current baseline/constitution/change contract；真实 candidate 来自 Delivery PRD 与独立 Architecture 输出。 |
| constitution-binding | applicable：复用既有 schema 与错误 taxonomy，不新增错误框架、别名、public DTO、缓存或第二 authority；符合最小必要复杂度、职责内聚与单向收敛。 |
| boundary-and-decision | applicable：需求/行为 authority 为本 Issue 与 root/Delivery PRD；本轮改变 Discovery record 内部校验顺序、当前版本导航和恢复说明。决策引用 `ARCH-DOM-038`、`ARCH-DOM-039`、`ARCH-INT-001`；无需新 ADR。 |
| owner-and-single-writer | applicable：Discovery 继续拥有 context evidence；共享 `validate_json` 只提供结构化诊断；Author 写规划，Architecture/RDT owner 在最终整合时维护各自正文，installer 维护投影。 |
| compatibility-and-exit | applicable：owner-result 3.0 是同步来源的既有兼容合同，必须保留；当前 Git-object 使用 4.0。无 dual-write、无新 fallback；旧 3.0 保留有明确 consumer 和版本身份。 |
| gap-and-deviation | applicable：本批只关闭“Git-object evidence 校验早于结构校验”的当前实现偏移，并修正当前导航冲突；不关闭或新增无关 Architecture GAP。 |
| parallel-scope | applicable：允许本 Task 修改 Discovery package、相应 workflow specs、tests 和隔离 Task/Delivery 文档；禁止同时修改无关 current、其他 Task 和共享安装版本轴。 |
| evidence-and-freshness | applicable：before 由固定基线和公开 record 复现；after 需同入口覆盖字段诊断、observation 诊断、纠正后实际 `context_ready`、版本导航与投影一致性。测试与安装结果分别报告，计划或静态检查不证明完成。 |
| review-and-promotion | applicable：Planning candidate/final、独立 Phase 2 Architecture、完整候选 Check、最终整合、TaskCommit 和完整 committed Branch Review 各保留原职责。本贡献在每个后续阶段独立评估，不预填 pass。 |

## Project Check

采用 `guru-trellis-architecture-convergence:repository:1`，entrypoint 为 `docs/architecture/06-governance/change-contract.md`，check id/version=`guru-trellis-architecture-convergence/1`，result contract=`guru-project-architecture-check-result-2.0`。审查当前 stage/authority binding、九 concern 完整性、before/after、单一 writer、parallel 边界、受管投影和 review/promotion freshness；关联 `ARCH-GOV-006..009`、`ARCH-GAP-006/008` 与当前 DeliveryKey。AI 依据实际证据判断 applicability 和 blocking，脚本只校验公开结构。

## Target

完整 proposed resulting definitions 位于：

- `architecture/proposed/docs/architecture/01-current/system.md`，新增 `ARCH-CUR-077` 完整单元；
- `architecture/proposed/docs/architecture/03-domains/ownership.md`，新增 `ARCH-DOM-061` 完整单元；
- `architecture/proposed/docs/architecture/04-integrations/distribution.md`，新增 `ARCH-INT-064` 完整单元。

三份拟写均以固定 B=`e30c7bb5d4c24bc075dc14cfcd04c1da00fcf78e` 的完整目标文件为 preimage，只插入上述当前单元；其他单元与关系保持。仅为实际受影响的单元补写版本区分、结构诊断顺序、恢复边界和投影责任；不更新共享 README 导航、ARCH-GAP 生命周期或新增 ADR。原 Architecture/RDT writer 在 candidate Check 后 final integration 读取实际写入并晋升。
