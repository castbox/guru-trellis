# D1：按各自适用条件调用 qualifier

## 1. 整体来源与术语

整体 authority 是 Task [prd.md](../../prd.md)，公共 accepted_scope revision 为 `sha256:e38267c6d918f2104d8e7c8654215d32d9d09bc41a195c2d9e266bca8f22432b`。本批 scope_ref 选择 R1—R6、AC1—AC4；实际 planning_root 为 `deliveries/55d0c98b-a483-4ee3-b8ff-7ad547ef3ee9`。

| 来源 | 章节 | 角色与用途 |
| --- | --- | --- |
| [Issue #793](https://github.com/castbox/guru-trellis/issues/793) | 当前完整正文，无评论 | Direct Source 的要求，保留条件触发、原出口、采用刷新及分发边界。 |
| Task `prd.md` | 第1—8节 | 已接受整体范围；本批全部覆盖。 |
| 三 qualifier 的 `references/contract.md` | Ownership、Closed profiles、Gate/exits、Re-entry | 现行实现和兼容约束，定位本批迁移差额。 |
| `trellis/workflows/guru-team/workflow.md` | Mandatory qualification profiles、Root-cause qualification routing、Phase 2 Implementation | 现行全局调用和 consumer 权威。 |

术语沿整体 PRD。触发判断属于原阶段 AI owner；未调用不是一个伪造的 qualifier `classified` 结果。结论采用不等于本阶段自动通过。

## 2. 整体与本批目标、非目标

本批完整交付 #793：让原 caller 在加载 qualifier 全文前读到各自条件，先判断适用性；条件满足才显式加载并运行原 stable Skill。保持正常范围、机制 authority、因果判断三项原职责及真实非通过返回。

整体 R1—R6 均属于 D1，不留隐含 D2。已有空候选跳过与 root 不变机制采用继续有效，不能改成每阶段固定调用三个。本批排除整体 PRD 第3节的全部非目标，尤其不合并 Check/Branch Review，不修改发布入口或归档时序。

## 3. 本批起点、前序结果、依赖与剩余责任

首次 D1，无前序 Delivery。开发起点 B 为 `e30c7bb5d4c24bc075dc14cfcd04c1da00fcf78e`，当前 PR 目标为 main；development B、实现 H 与 PR target 分开处理。Task generation 0，所选 Delivery 处于 planning，尚无 planning/check/full_review/readiness 结果。

#713 的公开录入、验证和恢复能力已在本次 Intake 使用；保留其适用生产合同，不以其历史 pass 代替本批验收。真实具体缺口交原 owner，只阻塞依赖工作。#736、#792、#794 没有整项前置关系。

本批全部实现与验证、Docs SSOT 责任闭合后方可形成最终 Check 和独立 committed Review。发布前需原 readiness；本执行段发布 PR 后在 merge 前停止。实际 Delivery 结果及整体 Completion/Closure/Finish 尚未发生，不能预写完成。

## 4. 本批调用方、场景与流程

实际 caller 包括 task-free、Clarify、change-request readiness、Author、Planning Approval、implementation coordinator、Reconcile、Check、Branch Review 和 Delivery Review。十类全局 profile 与现有 `author_candidate_set` 各按其真实边界核对；不把 Author 的候选准入漏在全局表之外。

| 场景 | 前置与触发 | 行为与观察 |
| --- | --- | --- |
| D1-S1 不适用 | 当前普通功能或已清楚受接受范围覆盖的工作，没有某 qualifier 的触发条件 | 原 caller 读取简洁条件并自行判断该项不触发，不加载其全文、装配输入或空调用；继续本阶段独立判断。 |
| D1-S2 有适用候选 | 原 caller 从真实 authority、候选和变化确认某 qualifier 条件满足 | 显式加载该 stable Skill；仅给其实际适用非空候选；消费真实出口，无统一三连调用要求。 |
| D1-S3 非通过 | 被调用 owner 返回拒绝、机制修订、诊断、范围选择或 blocked | 由原唯一 consumer 承接；排除项不升级成新测试/实现或必需 follow-up；机制修订和诊断不假记为通过。 |
| D1-S4 仍适用 | 对象、authority、机制、条件、因果证据未实质变化，结论可得 | 原 caller 采用仍适用结论，阶段变化不重跑；本阶段仍审当前工作。 |
| D1-S5 刷新恢复 | 上述适用事实实质改变或必要结论丢失 | 原 owner 恢复或重判受影响部分；不复制旧输出、不造通过、不扩大全部阶段矩阵。 |
| D1-S6 分发 | canonical 合同完成实际变更 | 沿原安装 owner 同步 dogfood/受影响平台，检查真实投影和必要 drift。 |

## 5. 完整行为、条件与约束

- D1-R1（整体 R1/R2）：每个 qualifier 自己拥有清楚、可在全文加载前取得的条件；原 caller 根据真实 authority、候选和变化判断，条件与完整合同一致。规划须说明实际哪些调用省略、哪些保留；未触发不执行空判定。
- D1-R2（整体 R2/R3）：不能新增一个资格判定 Skill、固定问卷或逐候选证明 artifact。三项判断按完整职责区分，OS/内核/进程/FD 不是全部条件的替代。真实故障、保护或重大取舍不靠重命名跳过；真实 scope/authority 选择回原入口。
- D1-R3（整体 R3/R5）：触发时使用原 stable Skill、真实非空输入、完整 semantic Gate 和原出口。拒绝、机制修订、diagnosis、scope 与 blocked 的实际意义、consumer 和停止保持；脚本只验事实。
- D1-R4（整体 R4）：新建或实质改变的事故/保护机制仍进入 root；不变机制采用仍适用结论。阶段/caller 改变本身不重做相同判断；authority、机制、条件、因果证据实质变化才刷新命中判断，丢失必要结论由原 owner 恢复/重判。
- D1-R5（整体 R5/R6）：共同修改实际 caller、workflow mandatory 条件、原 Skill、输入/出口消费、示例和诊断。真实公共 API 差额写明确迁移合同，支持在途恢复；不重构未受影响算法，不合并三个 owner。
- D1-R6（整体 R6）：canonical、dogfood 与实际受影响平台由原安装 owner 同步，至少保留 Claude Code、Codex 的一致适用合同。Markdown/原 AI 作语义判断；不增加授权持久化、审计账本或无 consumer 字段。

来源未约定具体代码结构。现行合同的职责、非通过出口和在途恢复作为约束保留；本轮条件及兼容改变将在 design 第3节唯一处置。不能把待实施行为写成已通过，也不要求事故重放、费用阈值或全矩阵。

## 6. 本批验收、验证方式与未决项

| 验收 | 要求/场景 | 入口、输入与预期观察 |
| --- | --- | --- |
| D1-AC1 | D1-R1/R2；S1/S2 | 对真实改变 caller 的普通未触发与真实触发场景，观察实际加载/调用和原 consumer；两种路径都满足各自条件。 |
| D1-AC2 | D1-R3；S3 | 复用原 public wrapper/consumer 的可核验非通过覆盖，只补真实改变的承接缺口。不得伪造上游 classified 结果来满足 root 前置。 |
| D1-AC3 | D1-R4；S4/S5 | 未变机制采用结论、实质变化刷新受影响判断、结论丢失原 owner 恢复/重判；当前阶段判断仍执行。 |
| D1-AC4 | D1-R5/R6；S6 | 原分发 owner 同步实际投影；package/runtime、公共 graph/投影及必要 dogfood drift 定向验证通过，真实兼容差额有迁移说明。 |

当前需求无必要未决产品问题。具体条件、适用对象、直接 consumer 和迁移方案由本批 Author 提出并经独立 Architecture、Wording、Approval；未完成该链前不实现。验证按 `quality-guidelines.md#test-and-validation-value` 采用仍适用证据，补实际缺口，区分静态、确定性调用和真实 Agent 行为证据，不新增案例数量门槛或通用评测框架。

## 7. Canonical 引用与本轮差额

| 权威/证据 | 已读位置与用途 | 本轮差额 |
| --- | --- | --- |
| 整体 requirement | Task PRD R1—R6、AC1—AC4；Issue #793 当前完整正文 | 本批完整承接。 |
| 既有 R/D/T | `docs/requirements-design-test-contributions/382-root-cause-qualification/{requirements,design,test}.md`，已晋升历史职责及验证边界 | root 前置与未触发/采用/刷新条件须按实际改变维护；历史观察保持原样。 |
| 设计/行为合同 | 三 qualifier `references/contract.md`；Author `references/authoring.md`；workflow Mandatory qualification profiles | 原 caller 固定调用及上游结果前置需要与条件调用一起收敛。 |
| 测试 | root `tests/test_runtime.py` goals、非通过、stale/public wrapper；`tests/test_contract.py` schema/consumer | 采用仍适用覆盖，补实际 caller 的条件和承接缺口。测试存在不等于本批运行通过。 |
| Architecture | ADR-008 Decision；ADR-020 Decision | 保留三 owner 职责及 root 不变机制采用；调用适用性差额由原 Architecture/RDT owner 判断并维护完整当前单元。 |

必要共享知识目标和晋升策略由 solution planning 的唯一 Docs SSOT Plan 确定；本阶段不造空贡献、不修改共享导航。本节不将历史贡献或较新版本号当成当前实现通过。
