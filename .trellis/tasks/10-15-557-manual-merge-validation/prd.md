# #557 独立公开链验证夹具

状态：正式 Task 整体需求；各阶段审查及外部结果由其原 owner 产生。

来源：本次 #557 implement 第7步的独立验证。正式 Task 使用 no_issue；本夹具不拥有 #557 Closure。

## 整体范围

交付一个可读的 JSON 夹具 validation/manual-merge-557.json：scenario=manual-merged-delivery-recovery，version=1，task=557-manual-merge-validation，expected_delivery_fact=delivered，completion_owner=guru-review-task-completion，completion_requires 按候选文件列出的三个事实责任。

V557-01：夹具作为实际内容走正式 Creation、独立 Delivery、Author/Architecture/Wording/Approval、Activation、Check、TaskCommit、独立完整Review、Readiness、Publish。
V557-02：同一真实 GitHub PR 用普通 two-parent merge，不添加 Guru trailers，不生成 Guru Merge gate；仅专用验证基线承接。
V557-03：原 Merge 用既有 public Publication 与实际 PR/head/merge/base/content 恢复 delivered。query2 只读回该事实；原 Completion 判断夹具内容与本 Task 全部范围、真实证据。

交付前检查夹具 UTF-8 JSON 和明确字段；真实合入内容、恢复与 Completion 仅能在外部动作后观察，由 Completion 保留证据责任。没有运行 CI 的普通真实状态按 missing 记录；本 Task 不要求添加 CI，也不把 missing 宣称 green。

只包含夹具及正式 Task/Delivery 的必要规划/公开记录；本地完整 matching 安装和 docs authority 由 gitignore 保留在本地。当前候选素材不包含任何 owner pass。源 #557、本验证 Task 和真实业务现场各自保持责任边界。

## 来源选择

current-request:557-live-validation 的 Prepared fixture and original public-chain validation scope 是需求来源；README.md 的独立公开链验证基线约束隔离、安装与软件/业务验证边界。整体 accepted_scope 由原 Clarify 的公开 accept_scope 记录。
