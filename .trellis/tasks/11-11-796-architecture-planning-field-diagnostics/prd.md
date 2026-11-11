# #796 Architecture 规划入口字段诊断整体需求

## 1. 来源与术语

| 来源 | 角色 | 本 Task 用途 |
| --- | --- | --- |
| https://github.com/castbox/guru-trellis/issues/796 ，目标与行为要求、最小验收、范围边界 | Direct Source 要求 | 完整交付本次修复 |
| 同 Issue 的已确认根因与证据边界 | 历史诊断证据 | 定位普通字段遗漏及错误包装，不作为实现通过 |

identity 指 baseline_current 结果中的 baseline_identity 与 constitution_identity。typed exit 是原正式入口返回的流程出口。

## 2. 背景与问题

Guru 0.7.0-guru.8 的 delivery_task_impact_sync / planning 支持 candidate_assessment 和 final_plan。两份现场 owner_result 遗漏 identity 后通过 semantic-result-delivery-1.0 Schema，随后 _check_owner_result 直接索引字段并抛出 KeyError；共享包装仅返回 internal_error，stderr 为空。当前 main 的对应逻辑相同。原本可由当前 owner 纠正的输入错误失去字段诊断并阻断规划。

## 3. 目标与非目标

完成两个 identity 字段的分支结构检查、现有错误合同下的明确诊断及合法输入回归。只修正当前 Architecture 规划合同与其实际消费者。
不处理 Reconcile、早期 Wording 的未定位错误，不修改业务 Task 审核状态，不重构全局异常框架或遥测，不新增恢复机制及审核链。

## 4. 真实调用方、场景与流程

- S1：原 Architecture owner 评估后经 scripts/invoke.sh --invocation - 提交 baseline_current；普通装配遗漏任一 identity，应在读取前收到对应 owner_result 字段诊断，不能得到成功出口。
- S2：原 owner 按当前 authority 和评估完成输入，经同一正式入口应返回原合法 typed exit。
- S3：其它合法 typed exit 保持自己的字段合同，不因本次 baseline_current 约束增加无关字段。

## 5. 行为要求

- R1：candidate_assessment 与 final_plan 在消费 baseline_current identity 前检查其结构；遗漏 baseline_identity 或 constitution_identity 返回明确字段路径与纠正指引，不归为 internal_error，不静默补值。
- R2：规划 Schema 与运行时实际要求一致；条件约束只施加于消费字段的分支。保留其它合法出口、身份、freshness 和 AI 语义门禁。
- R3：保留原失败，复用原 Skill fresh re-entry：重读当前 authority，完成当前评估，构造完整 envelope 并走原入口。纠正后成功不改写原失败。公开合同或示例有实际缺漏时修正。
- R4：受影响 canonical、dogfood 和声明平台投影沿既有安装 owner 同步，验证范围由实际改动决定。

## 6. 约束与依赖

Markdown 仍拥有语义流程，Schema/runtime 只校验确定性结构和一致性。复用既有 schema_mismatch/CommandError 及 wrapper，不增加公共 DTO、状态、默认值或并行成功路径。现有完整合法输入的成功语义保持；拒绝原本必然触发 KeyError 的不完整结果不是新增业务限制。

## 7. 可观察验收与验证方式

- AC1（R1/R2、S1）：经正式 invoke wrapper 分别遗漏两个 identity，观察对应字段诊断与非成功出口。按实际分支选取能检测缺陷的用例；共享逻辑不重复完整 purpose×字段矩阵。
- AC2（R2/R3、S2/S3）：完整合法调用保持原 typed exit；复用适用正常路径及受影响回归，只补实际缺口。合同/示例与投影按实际修改验证。
不要求重放业务 #813 全流程、完整多平台安装升级或 Release 矩阵。测试夹具成功不证明业务 Task 已恢复。

## 8. 实际未决项

需求及范围无未决项。具体 Schema 落点、定向测试与投影更新由本 Task 的原 Author/Architecture/实施 owners 完成。修复尚未实施，当前正文不预填验收通过。
