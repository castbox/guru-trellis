# D1 Issue 审核评论与 Intake 分流需求

## 1. 整体来源与术语

整体 authority 是 ../../prd.md 的 R1–R7、SC01–12、AC1–5；accepted_scope revision 为 sha256:6ef8d4ba97be878afad8539c03db604f195400b2127c25bcb5f042d31a2a4f20。公共 DeliveryKey 为 819-issue-review-intake/gen0/f108d161-d60d-4c89-91bf-d96004ef86a6。当前 planning_root 即本目录。

唯一 Direct Source 是 https://github.com/castbox/guru-trellis/issues/819 的完整当前正文。整体 PRD 第5节保留完整内容；本批实际读取它及 live Issue。原 workflow 和五个原审核/创建 package 是现状证据；#692 归档和 current/local-fix-intake 是事实复用与旧完整链来源。没有额外引入来源；评论是 AI 复核证据，不能提供自动放行 authority。

## 2. 整体与本批目标、非目标

D1 共同交付最小审核评论生产与已有 Issue 的前置 Readiness，并使三类局部补审合法返回原判断点。它覆盖整体全部 R1–R7 和 AC1–4 的实现/验证责任，保留 AC5 的原完整交付收尾。只有评论或只有分流都不能独立满足本项，故本批采用 full。

不新增复核 Skill、第二审核节点、固定评论模板/资格/label/有效期、hash 链、账本、评测系统或额外安装矩阵。不批量补旧 Issue。不涉及 #822、发布版本、业务后端/数据库/支付。当前仅规划，不实施或外部写入。

## 3. 本批起点、前序结果、依赖与剩余责任

开发基线 B 和 Planning H0 均为 4f2adef1f7b099f78bb8429e8b8facd66dce3bfc，B 来源为明确固定 origin/main；PR target=main。Task 内没有前序 Delivery。#818 已交付的内容方法和 #692 的适用事实复用只作为现有能力，不能计为本批成果。

现状：selector→Sync→Discovery→Clarify→Wording→Readiness；Create Issue created 亦回 Sync。Readiness 公共输入要求实际当前前序 transition；Discovery/Clarify/Wording 的正向出口没有面向本次已有 Issue Readiness 的独立局部返回合同。Create executor 已有同对象标记与找回，Clarify 已有受控 source_actions/GitHub 读回；需要在原职责内适配。

本批后仍须实际实现、工程检查、原 RDT/Architecture 整合/readback、TaskCommit 后一次独立完整 Review、Delivery readiness/发布/合并、整体 Completion/Closure/Finish。本轮不把规划通过描述为任何一项工程或整体完成。

Create Task的现有consumer采用当前profile2.0和共享creation3.0：审核来源与Task集成branch分开，完整来源身份按原合同承接。D1-R6/R7的公共合同适配必须保留这项已存在能力；具体投影、例子及条件由design第3、5、7节单写，不改Task/gen0/D1、固定B或整体范围。

## 4. 本批调用方、场景与流程

| ID | caller / 前置 / 触发 | 行为与观察 |
| --- | --- | --- |
| D1-SC01 | 原 Create；完整草稿已审且正式 readback 一致 | 发布真实最小评论，读回后完成创建；不确定时找回原 Issue 和评论。 |
| D1-SC02 | 原 Clarify；主动复审且本次写入范围明确 | 发布或更新准确局部/完整覆盖；只读审核零评论 mutation。 |
| D1-SC03 | 已有 Issue→Sync；原 Readiness 读取 live 当前依据 | 充分→ready；仅事实→Discovery；需求/单元→Clarify；仅措辞→Wording；不足→必要全链；真实前置缺失→blocked。 |
| D1-SC04 | 各局部步骤实际完成 | 返回同 Issue/同次 Readiness。事实不变时可直接 ready；需求变化只补受影响措辞；多缺口每次处理最早必要依赖。 |
| D1-SC05 | 基线真实失效或阻塞条件恢复 | 原 Sync 或受影响 owner 后回原 Readiness；时间、换 Agent 和无关 HEAD 不自行使覆盖失效。 |
| D1-SC06 | 未指定 Issue 的讨论、草稿、创建与开工 | 标准完整调查/草稿审核；只讨论/草稿停止，只创建在评论读回后停止；开工以正式 Issue/评论→Sync→已有 Issue 复核。 |
| D1-SC07 | 合法 standalone_request/no_issue | 保留完整链与原 Task 创建，不要求不存在的评论。 |

## 5. 完整行为、条件与约束

- D1-R1（整体 R1）：共享一个评论正文规则，说明实际审核对象、范围、结论、影响开工的未决条件；基线只在相关时写。Create 保留草稿完整审核和正式 readback；Clarify 不把局部审核写成全覆盖，也不因只读请求自动发布。
- D1-R2（整体 R2）：原 workflow 在 Sync 后为已有 Issue 显式调用原 Readiness 新入口。它读取完整 live Issue、有效讨论/评论、必要前置和影响代码变化，亲自判断充分性及当前适用性。评论存在不构成通过。
- D1-R3（整体 R3）：原 Discovery/Clarify/Wording 增加明确局部 profile/返回。局部前置可由仍适用覆盖和当前事实满足，不伪造旧完整前序。其结果只回原 Readiness；它重新判断尚有必要的后续步骤，不能把局部调用变成剩余全链。
- D1-R4（整体 R4）：依据不足或影响不可界定才走必要完整链；无评论本身不阻塞。必要前置/选择/证据阻塞明确条件，恢复后仅刷新受影响部分。只有选定基线真实失效回 Sync。
- D1-R5（整体 R5–6）：无 Issue 讨论仍按标准完整方法，创建前仍有完整草稿审核；用户意图决定讨论/草稿/仅创建的终点。要求开工的创建结果用正式 Issue 与实际评论重新复核，不复制草稿 pass。no_issue 和 Task 后续门禁保持。
- D1-R6（整体 R7）：新公共 profile、逐出口 schema、唯一 consumer 和薄 projection 同批迁移；AI 决定路由，脚本校验事实。已成功对象沿原恢复，不另建重复对象。公开包不携带 Task/会话状态，不记录授权，不制造完整审核历史或派生 digest 跨 Skill authority。
- D1-R7（整体 R7）：canonical 原 owner 修改后由原安装 owner 同步 dogfood/声明平台，验证 reapply、drift、sidecar、mode 及用户/Task/session 保留。源码和真实采用分别提供证据。实际 schema/字段/迁移落点在 design 第3节唯一处置及第5–7节展开。

## 6. 本批验收、验证方式与未决项

| ID | 对应 | 入口、输入和预期观察 |
| --- | --- | --- |
| D1-AC1 | R1；SC01–02 | 原实际 Create/Clarify 发布/更新及 live readback；范围准确，未知结果恢复原评论而非重复，纯只读不写。 |
| D1-AC2 | R2–4；SC03–05 | 从实际已有 Issue 开工入口观察六类分叉、各局部返回、多缺口顺序、完整链和必要阻塞恢复；原 Task 门禁保持。 |
| D1-AC3 | R5；SC06–07 | 实际讨论→创建→开工及各终点；no_issue 原完整链。 |
| D1-AC4 | R6–7 | 生产 public wrappers/graph/consumer、受影响包和现有真实分发/reapply；确认 canonical/installed/platform、mode、sidecar 和状态保留。 |
| D1-AC5 | 整体 AC5 | 原完整 Review/readiness、所有 satisfying Delivery 和 Task 整体收尾；本轮不执行。 |

没有未解决产品选择。机制细节必须在 design/implement 可编码粒度完成后才可 plan_ready。上述真实 Agent/外部验收尚未执行；本轮不能以机械检查或样例替代。

## 7. Canonical 引用与本轮差额

RDT authority：docs/{requirements,design,test}/README.md，guru-trellis-rdt/active。当前完整 local-fix-intake 单元的 R692-02 / BEH692-REUSE、D692-01 / CON692-OWNERS、T692-01 / SC692-ROUTE/REUSE 要从固定全链演进为按当前 Issue覆盖分流；原事实复用和正常诊断职责保留。issue-content 三层单元保留内容方法，补评论提供/消费关系；不改旧任务历史。

Architecture：docs/architecture/README.md、00-foundation/design-constitution.md、06-governance/change-contract.md。独立 candidate assessment 决定本批真实影响和贡献，不由 Author 预填结果。采用 Markdown workflow/Skills、公共 profile 与确定性 runtime，不改上游 CLI/hook/node_modules。后续必要知识贡献与原 owner 整合由唯一 Docs Plan 安排，当前不修改共享 authority。
