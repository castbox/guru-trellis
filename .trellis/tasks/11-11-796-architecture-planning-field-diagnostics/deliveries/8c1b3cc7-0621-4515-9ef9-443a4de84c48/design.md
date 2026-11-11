# #796 D1 规划字段诊断设计

## 1. 设计目标、需求承接与内容基线

本批承接 D1 PRD 的 D1-R1—R4、D1-S1—S3、AC1/AC2。
development baseline B 为 main@e30c7bb5d4c24bc075dc14cfcd04c1da00fcf78e，来源为本 Task 经原 Sync 固定的 main。Planning H0 同 B；最终实现 H 由原候选构造器读取实际 HEAD。PR 目标为本仓库 main，不能用 PR 目标替换固定 B。
独立 Architecture 实际候选结果为 baseline_current / no_architecture_impact，baseline_identity= guru-trellis-architecture，constitution_identity= guru-trellis-design-constitution-v1。本批不产生架构贡献或 ADR。

## 2. 当前系统、边界与目标差额

唯一生产实现位于 trellis/skills/guru-team/packages/guru-maintain-architecture-baseline。run 根据规划 profile 选择 Schema，_check_owner_result 先 validate_json，再消费两个 identity 作实际 authority 比较。
缺口在 semantic-result-delivery-1.0.schema.json 的规划结果分支：其声明字段类型但未在 baseline_current 条件下要求字段存在，直接读取触发 KeyError。
D1 无前序交付；复用原字段诊断器和 wrapper，目标差额为读取前拒绝遗漏结果。

## 3. 来源设计处置（唯一）

| 来源与条款 | 原承诺 | 处置与落点 | 理由及影响 |
| --- | --- | --- | --- |
| https://github.com/castbox/guru-trellis/issues/796 ，行为1 | 读取前检查两个 identity，给字段路径和指引，不默认补值 | retain：本设计第4—6节 | 修复首次结构偏差，不改为成功 |
| 同 Issue，行为2 | Schema 与实际要求一致，字段按真实分支，保留原门禁和其它出口 | retain：规划分支的 baseline_current 条件 required | 已成功输入无变化，不将字段推广到其它出口 |
| 同 Issue，行为3 | 原 owner fresh re-entry，不新增恢复或审核链 | retain：第7节 | 当前 Skill 已拥有恢复路径 |
| 同 Issue，最小验收 | 字段各自诊断及合法调用原出口，共享逻辑不重复完整矩阵 | retain：第8节 | 独立断言足以发现缺陷，复用适用正向覆盖 |

## 4. 模块、职责与设计取舍

- 修改 schemas/semantic-result-delivery-1.0.schema.json 的 planning oneOf 分支：增加 typed_exit=baseline_current 时要求 baseline_identity、constitution_identity 的条件约束。复用已有属性类型，不新建 schema、helper、DTO 或补值逻辑。
- tests/test_contract.py 在真实 invoke wrapper 夹具中补两个字段各自遗漏的行为断言，使用同一共享规划分支。采用已有候选成功、final_plan 成功及其它出口用例。
- runtime/invoke.py、共享 runtime/command.py 保持职责；Schema 足以在直接索引前给出明确结构错误，无需新增全局异常分类。
- 检查当前合同/示例的字段和原纠正说明；已有定义准确时保持正文。同步实际受影响的 installed/dogfood/声明平台投影由 guru-upgrade-tools 完整源 owner 执行。

## 5. 接口与数据

入口仍为 scripts/invoke.sh --invocation -，输入仍为 public_input 与 owner_result。
profile=delivery_task_impact_sync，schema_version=delivery-1.0，stage=planning，两种 planning_purpose 保持。
baseline_current 的 owner_result 缺 baseline_identity 或 constitution_identity 时，使用既有 schema_mismatch，field_path 指向对应 owner_result 字段，remediation 指向当前合同和重新调用原入口。
其它 typed exit 没有新增字段义务。字段值不匹配、freshness 和语义 gate 仍由原实现检查。本次不增加 public API，不把历史无效输入定义成新合法成功路径。

## 6. 状态、顺序、正常与失败流程

原 owner 完成当前评估并提交结果 → 原 Schema 按 typed_exit 校验结构 → 缺字段返回明确错误并停止该调用；完整输入继续原 identity/语义/出口检查 → 返回实际合法 typed exit。
字段结构校验没有通过时不进入直接读取；后续其它真实错误仍走原错误路径，不把所有 internal_error 解释成输入遗漏。本次不改变 Task/Delivery 状态协议。

## 7. 恢复、兼容、迁移与集成

保留原失败；原 owner fresh re-entry 重读 authority、完成评估、生成新完整 envelope，再调用原 wrapper。新成功不改写旧失败。
本次补齐原成功域本就需要的字段，已成功的合法调用与原出口不变；不新增兼容 reader、字段别名或版本迁移。历史 Schema 按其真实消费者保留，不追改不被当前入口选择的旧资产。
开发 checkout 工具同步使用 guru-upgrade-tools 的完整源及隔离 local_candidate；该模式的 formal_fork_source_lock 未验证边界需如实报告，不代替发布/升级矩阵。保留 Task、session 和其它 checkout 工具。

## 8. 验证设计

- V1 / AC1：正式 invoke wrapper 中分别省略 baseline_identity 与 constitution_identity，断言 schema_mismatch、准确 owner_result 字段路径及非成功出口；不能仅检查 Schema 声明。
- V2 / AC2：采用已有正常候选、final_plan 与其它合法出口用例；输入纠正后原 wrapper 返回实际出口。共享规划分支不重复完整组合矩阵。
- V3 / R4：按实际改动运行 package 定向回归、受管同步和 dogfood drift；检查 diff 无无关受管回退、无未处理 .new/.bak。
此前故障复现已确立因果；实施者无需重复回退实验。测试不证明业务 #813 的当前审核通过，不要求完整安装升级/Release 矩阵。

## 9. Canonical 引用、本轮差额与实际未决项

必要来源为原 package references/contract.md 的结果 authoring 与纠正合同、runtime/invoke.py 的 _check_owner_result、上述当前 Schema 及 tests/test_contract.py。
Architecture no-impact 结果不要求贡献或晋升；现有 RDT 语义/owner/成功行为不变，Docs SSOT 计划见 implement 第6节。
需求与候选无未决项；任何真实范围或机制扩张回原 owner。

