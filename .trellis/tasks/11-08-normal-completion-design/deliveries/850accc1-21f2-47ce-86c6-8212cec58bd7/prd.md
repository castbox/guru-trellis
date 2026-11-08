# 正常完成路径与协调成本：D1 需求

## 1. 整体来源与术语

本批为 Task `normal-completion-design` 的首个完整 Delivery，key 为 `850accc1-21f2-47ce-86c6-8212cec58bd7`、generation 0。公共 accepted_scope 和 scope_ref 指向根 `prd.md`，revision `sha256:8e408b05aa32b31ecdc8bd43b31f8a6526558d5f3a7b7f9d9d81a00cfc64fcda`，选中 NC-R1—R7、NC-AC1—AC4。planning_root 为本目录。

| 来源 | 章节 | 角色与用途 |
| --- | --- | --- |
| `../../prd.md` | 全文 | 整体要求、术语、场景及边界，本批完整承担 |
| `/tmp/codex-architecture-three-layers-20261108/proposal.md` | §1、§3、§7、§8 | 原始要求与约定的三处 canonical 落点；本批正文已承接，不以临时路径存在为后续运行前提 |
| Architecture、Root Cause、Author 的原 canonical contracts | 根 PRD 来源表指定章节 | 既有行为与兼容约束，完整来源设计处置由 design 第3节单写 |

正常完成指支持的调用方取得承诺的可观察结果。额外协调指增加共享写、串行依赖、等待阶段或独立维护状态；不按机制名称分类。

## 2. 整体与本批目标、非目标

本批完整增强唯一采用机制审核方法及原 Root Cause、Author 必要消费点。先推导直接完成路径，主动尝试删除或缩小协调，再共同核正确性和最终完成成本。

不新增 Skill、阶段、审批角色、公共字段、评分或问卷，不改 runtime、installer、业务代码或依赖。backend 基线、业务投影和生产整改另仓承接。当前工作只实施本地规范与定向验证，不承担安装采用或生产效果。

## 3. 本批起点、前序结果、依赖与剩余责任

尚无前序 Delivery。当前 canonical 已有正常路径、成本和替代比较，但默认准入、主动淘汰和最终完成成本的要求仍需明确。根 PRD 已接受；本批尚未完成独立 Architecture、规划批准或实现验证，文件存在不代表通过。

本批依赖原 owner、qualification、知识贡献及晋升合同。完整本地实现和风险匹配验证为本批目标；后续 commit、发布、目标安装采用和业务效果保持各自职责，不能由本地源码成功替代。整体 Completion 仍须原完整范围审核，不能以单次 Delivery 进度代替。

## 4. 本批调用方、场景与流程

| 场景 | 调用方、前置与触发 | 处理与观察 |
| --- | --- | --- |
| NC-S1 | Author 从接受行为形成候选 | 先推导最终结果的直接路径，再尝试删除、收窄协调或复用已有原子能力；形成有依据候选 |
| NC-S2 | Architecture/独立审核审新机制、扩用或无 helper diff 的复用 | 自行尝试简单替代并判断可行性，不只审作者论证自洽；原方案已最小时说明依据 |
| NC-S3 | Protection 资格成立但候选增加等待或共享写 | 原 Architecture 继续判断最小范围和完成成本，资格不自动变为方案批准 |
| NC-S4 | 原审核审已有机制 | 区分必要、已证缺陷和证据不足；分别保留、有界整改或补证，不危险删除或默认批准未知复用 |

所有场景使用原阶段和 typed exits，不新建准入层。

## 5. 完整行为、条件与约束

- **NC-R1**：从业务、数据、权限和外部约束推导直接可行路径；异步方案比较到最终结果可消费，不能仅凭受理返回较快成立。
- **NC-R2**：新增、修改、扩用或复用额外协调默认不准入，先说明更简单方案为何不能满足已接受要求。用途、旧实现、技术测试和可靠性标签不是充分依据。
- **NC-R3**：Author 主动尝试删除、缩小一致性范围、已有原子能力或更直接职责。审核方独立判断，不强迫虚构可行替代；原方案已最小时说明依据。
- **NC-R4**：正确性及完成成本共同成立，核 I/O、共享写竞争、串行、排队和恢复前提及跨用户/资源/实例作用域。功能正确不能豁免可避免成本；不普遍要求性能压测。
- **NC-R5**：必要性已证机制可按范围保留；缺陷已证交原 scope/Architecture owner 承接消费者适配；证据不足不危险删除、不当作成功复用、不扩大机制，无关工作继续。
- **NC-R6**：唯一方法正文保留在 Architecture Adopted-mechanism review，Root Cause/Author 仅消费。现有有效消费者不复制新清单。
- **NC-R7**：命中案例同时核拒绝无依据成本与保留必要机制。源码、分发、安装采用和业务效果分别报告，不扩完整安装或业务矩阵。

必要权限、资金、幂等及恢复约束保持。规范性来源设计只在 design 第3节处置；没有 API、字段和运行单元变化，因此不产生数据迁移或部署步骤。

## 6. 本批验收、验证方式与未决项

| AC | 要求与入口/输入 | 预期观察 |
| --- | --- | --- |
| NC-AC1 | R1—R4/S1—S3；用方法审共享写、持锁慢调用、整批等待 | 覆盖最终完成路径，拒绝无依据额外成本，Protection 不替代取舍 |
| NC-AC2 | R3/R5/S2/S4；最小方案、必要短事务、证据不足案例 | 不虚构替代，不按名称禁用，不直接删除或批准未知机制 |
| NC-AC3 | R6；canonical diff 和真实引用消费者 | 唯一正文及必要消费，无新阶段、公共状态或重复清单 |
| NC-AC4 | R7；命中文档、引用及 package 分发入口的定向检查 | 如实报告检查及未验证安装/业务效果，不追加完整矩阵 |

没有待决产品问题。具体方案依赖原 independent Architecture candidate_assessment；本需求不预填其结论。验证层级沿 Test And Validation Value，由 Planning 展开当前风险匹配安排。

## 7. Canonical 引用与本轮差额

`docs/requirements/current/knowledge-maintenance.md` 的 R-MECH-01—05、同名 design 的 D-MECH-01—03、同名 test 的 T-MECH 保持完整有效单元。本轮需补正常最终完成、主动尝试简单替代、协调默认不准入、Protection/Architecture 分工及当前定向验证边界；旧专项 native 观察和历史要求不扩为本批固定次数验收。

Architecture 读取 `docs/architecture/README.md`、foundation/current、`03-domains/ownership.md` 与 `03-domains/review-sufficiency.md` 的实际命中规则；原 owner 判断并准备真实差额。RDT/Architecture 各自隔离贡献，候选审核后才由原 final_integration 晋升 shared current。无需改共享导航或全局版本。canonical 三处正文和知识说明各有原 owner，不能将私有业务规则写入公共 Guru。
