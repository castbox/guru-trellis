# D1 实施与验证计划

## 1. 输入与引用

读取本 Task 整体范围、本批 PRD 和 design 第3节的唯一来源设计处置。按 §1 采用候选架构和固定 B。读取写作规范、Author 正文合同及适用模板、共用 review-sufficiency 和 quality-guidelines 的 Test And Validation Value 与 Validation Scope Ownership。读取命中的 RDT 正文和 Architecture 域。D1 为首批。

## 2. 有依赖顺序的步骤与文件责任

1. I1 原 RDT 与 Architecture owner 在本批的隔离提案中准备受影响单元。Architecture 使用 design §9 的完整提案。RDT 准备行为验证和审核充分性三层差额，保留现有关系。
2. I2 实施负责人更新 canonical Clarify contract、Author planning-body、共用 review-sufficiency 和 Author 去敏示例。补最小 distribution fixture 的该新增示例投影。原读取链直接消费这些方法。
3. I3 对同一候选先执行 V1，再执行 V5 和 V6。各原负责人分别读取真实结果和适用边界。保留原失败和未执行范围。
4. I4 原 RDT 和 Architecture owner 整合本批经过工程验证的差额并回读。走原 TaskCommit 和实际 committed Review、Delivery Review、交付。D2 单独建立后继计划及候选。

## 3. 验证入口、输入与预期观察

- V1。使用 #735 的既有 provider 装配与原生命令，输入使用预先冻结的中性来源、组件事实和候选。先观察 Clarify/Author。另用相同素材及完整候选 provider，从干净原生进程执行原 Approval 的独立候选审核方法。原审核者先读方法和来源，公开实际问题后才单独打开候选，并解释交回技术 owner 的理由。记录两次原始输出和读取顺序，由独立评价者判断 AC6。该只读观察无正式 Task 审批前置或结果。在本次对话或本批验证正文保留判断和证据边界。
- V5。以匹配 `0.7.0-castbox.6` 的已验证模板脚本和受管 Python 执行 `test_planning_body_distribution.py` 和 `test_review_sufficiency_distribution.py`，再跑相关 package 合同检查。核对安装/reapply、用户文件和 sidecar。
- V6。用 `guru-upgrade-tools` 的 `preview.sh`、`prepare.sh`、`invoke.sh` 同步同一 worktree。使用工作区的 `get_context.py`、原 installed validation、`check-upstream-ownership.sh` 与 `check-dogfood-overlay-drift.sh`。证明当次采用、完整性和保留 Task/session。使用 local_candidate 保留 formal source lock 的未验证边界。

## 4. 停止条件与适用回退点

来源或范围变化返回 Clarify。机制冲突由原 Architecture 处理。Agent 或 provider 装配失败保留原输出，只修实际装配问题。受管冲突通过原工具 owner 的同操作恢复处理，保留用户文件。未得到必要证据时停在对应验收边界。独立工作可继续。没有产品数据或业务发布回退。

## 5. Delivery Policy（唯一）

`partial`。独立交付 D1 的 JQ-R1/R2、适用的 R5/R6、V1/V5/V6 和原知识整合。D2 承担 JQ-R3/R4、适用的 R5/R6 及 V2–V6。整体 Completion 要求两个 Delivery 的实际结果和仍适用的证据。

## 6. Docs SSOT Plan（唯一）

`delta_first`。由 `guru-maintain-requirements-design-test-ssot` 在本批 `rdt-proposal/` 保存必要完整 proposed 单元，适用范围见 PRD 第7节。由 `guru-maintain-architecture-baseline` 承接 design §9 的领域提案。通过工程验证后在本地 TaskCommit 前由两位原维护 owner 整合并回读。Committed Review 使用实际 before/after 及可适用证据。既有历史原样保留。
