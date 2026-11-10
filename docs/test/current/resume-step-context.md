# 正常续接与实际出口查询测试定义

知识单元：`RDT-TST-RESUME-CONTEXT`。别名：minimal current DTO、exit discovery、context unavailable、selector preservation。语义 owner：`guru-maintain-requirements-design-test-ssot`。状态：current，表示测试规范已整合，不表示下列测试全部通过。适用前驱为 Git `26630149070e2988ad08102679931468b3535ef8`；来源和完整拟写见[贡献追踪](../../requirements-design-test-contributions/resume-step-context/traceability.md)。晋升依据为本 D1 candidate_checked 后、Architecture 实际晋升之后的原 RDT final_integration。source/package、installed、原生 Agent 和实际效果分别取证。

## 策略与验收关系

需求为[RDT-REQ-RESUME-CONTEXT](../../requirements/current/resume-step-context.md) RSC-R1～R5，设计为[RDT-DES-RESUME-CONTEXT](../../design/current/resume-step-context.md) RSC-D1～D5；既有[生命周期测试](task-delivery-lifecycle.md)保留原阶段验证职责。长期测试由原 package/runtime 的正式测试入口承接；调用真实 invoke、parser 和 discovery CLI，不能由 fixture 直接返回待测投影或把字符串自比较当路由验证。fixtures 只准备合法前置和局部正常声明差错，不构造恶意伪造、生产损坏、额外并发或崩溃压力。

| 稳定测试身份 | 对应要求／设计 | 正常输入和实际入口 | 必须观察及证明边界 |
| --- | --- | --- | --- |
| RSC-T1 | R1／D1 | 原 Ensure 新 current profile；合法 Task 有/无 Delivery，上游带大 results/candidate 树 | 原身份、binding、ownership、checkout 校验实际执行；成功仅含 Task 四字段及存在时 Delivery 三字段，同 Task/generation；无 Delivery 省略，结果树和 candidate paths 不泄入公共输出。不证明阶段语义通过。 |
| RSC-T2 | R2/R5／D2/D5 | 真实 context 无绑定、无 key、普通 stale、ownership/checkout/关系失配及原读取/API 错误；原 invoke | 两种缺失分开；原 code/field_path/remediation 和恢复 owner 保持；不按非零统一判无 Task。比较查询前后 Task/Delivery/session/Git/业务状态；原 launcher ignored cache 刷新单列。测试受控 context 不是生产绑定证据。 |
| RSC-T3 | R3/R4／D3/D4 | 原 discovery CLI 查询 Skill、workflow、stop consumer，以及动态 selector | 返回唯一原 consumer 与实际可解析的 output/input/projection/入口或 target 定位；selector 未提前求值；caller 可完整加载原合同，无下一步执行副作用。source 与 installed 各核真实路径。 |
| RSC-T4 | R3／D3 | 局部 fixture 中未知 exit、缺 marker、多重映射、Interface 不一致 | 实际解析/CLI 明确非零失败，不任选 consumer；生产安装保持。保留旧全局校验，不以新查询窄检查放宽原规则。 |
| RSC-T5 | R4/R5／D1/D3/D4/D5 | 原显式 Ensure profile、无 exit discovery、help、相关 contract graph、canonical/dogfood drift 及一次原 owner 代表性安装投影 | 旧输入、输出、错误、consumer 兼容；新字段、出口及相邻投影成套可用；原适用合同完整读取；Task/session、并行修改、mode/sidecar 保持。机械和安装结果不证明 Agent 效果或完整 Release 矩阵。 |
| RSC-T6 | R5／D4/D5 | 冻结 bound/unbound 原生 prompt；控制组与实验组同模型/输入/环境及共同 `26630149` 旅程方法，实验组仅增加两项查询差额 | 先比较实际答案、身份和出口正确性，再记录首次失败、非通过、不利观察、重复查询、装配错误、读取量及人工介入；准备 context/fixture、待测查询、cache 成本分列。每组10分钟；首次原始结果另存，不覆盖历史。 |

## 执行、停止与结果归属

先完成 T1/T2 对应原 Ensure `tests/test_contract.py` 的真实行为及 T3/T4 对应 discovery/parser 的命中回归，再执行 T5 的 contract graph、分发及一次代表性安装，最后由原协调 owner 执行 T6。具体命令沿原 package tests、`test_skill_packages.py`、`test_delivery_contract_graph.py` 及必要 runtime tests；准确路径由实际代码 owner 确认，不新增平行测试实现。

已有工程结果仅在输入、依赖、版本、工具链、环境、参数和预期仍匹配且原结果可核验时采用。失败停止其对应验收，保留原诊断，由实际实现或工具 owner 修复；实际身份冲突交原恢复 owner。没有新影响时不重复充分验证，不要求惯例回退红绿。

原 RDT 隔离拟写时未执行实现测试、安装或原生对照，T1～T6 当时均待验证；该历史观察保留在原贡献 `test.md`。后续实现及 native 已由其执行 owners 推进，原 candidate Check 已由 Nash 返回 candidate_checked；本次知识晋升不重跑工程测试，也不把该出口或主会话的完成说明换算为各项独立通过。实际覆盖、首次结果、失败和未验证边界由原命令、外部 evidence 及后续正式质量结果确定。最终 after 候选仍须重绑并经最终 Check。长期场景在本单元维护，本文不新建证据账本。

旧 `43d8/unbound` 退出0及214.97秒保留为历史观察和已发生成本，不作为本轮控制组或节省比例依据。无 context 设施只证明 unavailable/explicit 边界；显式测试绑定单列。原生设施缺失保持缺证，不能以 package 通过替代。执行者只读取冻结 prompt 和正常入口资料，不读取独立比较 protocol。上游启动读取未被本项消除，命令更少、文档更短或查询通过均不能证明真实产品缺陷下降。
