# #658：tools-only AGENTS.md 内容合同修复

## 1. 来源与术语

| 来源 | 角色与用途 |
| --- | --- |
| https://github.com/castbox/guru-trellis/issues/658 全文及验收1–9 | Direct Source：整体范围与验收 |
| https://github.com/castbox/guru-trellis/issues/566 工具安装与恢复 | 既有单checkout、工具/数据隔离及恢复兼容约束 |
| https://github.com/castbox/Trellis/issues/57 | 必要公共维护能力依赖；具体接口归Fork |
| https://github.com/castbox/guru-trellis/issues/656 版本与来源 | 新Fork来源采用前的发布依赖协调 |
| trellis/skills/guru-team/packages/guru-upgrade-tools/references/contract.md | 当前准备、执行、恢复与回滚职责及待修复机制 |

tools-only仅维护选定checkout工具；公共维护操作归Fork CLI/Core，Guru管理自身受管资产与规则块。安装、业务任务迁移、Task Completion和正式发布分别判断。

## 2. 背景与问题

Guru在公共prepare返回后修改AGENTS.md target，公共执行重新生成候选时拒绝该内容。先执行公共维护再由preset更新规则块，又会使公共恢复与回滚误判为later_work_conflict。正常升级需要一致的最终内容合同。

原业务dev失败操作停在公开写入前。历史快照不是当前安装证明；处置前须回读原checkpoint、公开恢复记录与目标内容。现有测试是回归起点，具体helper不是必须保留的设计。

## 3. 目标与非目标

更新Guru规则，保留项目正文与权限；使准备、公共执行、preset重应用、恢复和回滚一致；完成原失败操作处置及真实目标核验。

不迁移Task、规划、归档或workspace/session，不修改其它checkout/common指针，不承担正式发布或完整多平台矩阵，不修改已发布tag/npm，不新增通用扩展框架、锁、攻击防护或非常规故障协议。

## 4. 真实调用方、场景与流程

| 场景 | 前置、动作与可观察结果 |
| --- | --- |
| S1 升级 | Guru维护owner从固定完整匹配来源准备最终内容，审查工具写集并执行公共维护/preset；目标自身installed/native可用 |
| S2 重应用 | 已正确安装再次更新或重应用，不重复Guru块或改变项目正文 |
| S3 恢复 | 同操作正常中断且来源未变，使用原recovery_ref继续，最终内容与正常完成一致 |
| S4 回滚 | 兼容且无后续编辑时恢复原始字节与权限；有真实后续编辑时阻止覆盖 |
| S5 旧失败处置 | 读取原业务dev操作实际写入，依原合同退出/回退；需要新操作时重新准备，不改旧checkpoint强续 |

## 5. 行为要求

- R1：最终内容由受支持公共准备接口接受，不事后改冻结计划规避校验。保留既有preserve/replace等语义，准备与审核明确实际内容变更。
- R2：Guru更新AI-first标记块；块外项目自定义正文保持。上游模板内容沿已审查处置，不以默认模板覆盖项目全文。
- R3：公共执行、preset、同操作恢复及回滚使用一致内容与权限合同；正确规则块的preset重应用幂等。
- R4：回滚保留原兼容性与后续工作保护，不吸收后续编辑为新恢复基线。
- R5：工具更新保持Task、规划、归档、workspace/session及其它checkout/common指针字节、权限不变。
- R6：原失败操作先核验实际状态，保留来源绑定；新源码不直接接管旧checkpoint，需要新操作时先合法处置原操作。
- R7：同步canonical Skill、安装说明和受影响分发副本，消除强制旧机制的合同。公共API变化提供明确兼容或迁移合同。
- R8：分别报告API、完整安装、原生入口、真实目标与发布证据；旧冲突诊断测试通过不算修复通过。

## 6. 约束与依赖

以main为基线。Fork #57交付前可进行必要规划与本地适配；固定来源集成及整体完成须等待依赖交付。采用新Fork来源前由#656发布owner收敛来源约束及受影响验证，已发布制品保持不变。

业务目标实际工具写集在执行前单独回读与展示，不扩为业务任务维护。恢复/回滚沿原owner，不增加checkpoint编辑或临时补偿写入桥。

## 7. 可观察验收与验证方式

| AC | 要求/场景 | 入口与预期 |
| --- | --- | --- |
| AC01 | R1/R3，S1 | 真实匹配CLI/Core接受准备候选并写入相同内容；测试入口可适配最终方案，行为断言保留 |
| AC02 | R2/R3，S1/S2 | 旧Guru块和块外正文样本更新正确，原权限保持，重应用无额外变化 |
| AC03 | R3/R4，S3/S4 | 完整公共维护/preset组合的正常恢复与回滚恢复原字节/权限；真实后续编辑阻止覆盖 |
| AC04 | R5，S1–S5 | 操作前后业务数据及非目标指针快照一致，不转换Task/session |
| AC05 | R6，S5 | 回读并合法处置原操作，用固定修复来源重新准备并验证业务dev自身installed/native |
| AC06 | R7 | canonical/dogfood/声明平台投影、重应用、漂移及sidecar定向验证；合同与实现一致 |
| AC07 | R8 | 完成证据按真实层级报告；完整发布矩阵另由对应owner承担 |

## 8. 实际未决项

需求与范围没有待用户选择项。Fork源码交付、成功CI及source lock更新是执行前置；业务原操作处置与真实安装是整体完成前必要工作，不能由本地候选测试替代。具体适配机制由Delivery方案与独立Architecture判断。
