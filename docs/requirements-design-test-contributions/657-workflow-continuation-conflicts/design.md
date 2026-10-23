# 活动续接与迁移残余合同设计贡献

状态：promoted；完整定义已由原 RDT owner 写入并读回 current 单元。固定来源为 Git `319202beab79c7666ecdb855291bf117e43d407e` 的 RDT-LIFECYCLE 三完整单元；目标是 manifest 指定的完整 resulting definitions。原 Architecture 独立候选和 final_plan 均选择 target_native，本次晋升已在正式 candidate_checked 后完成。

`D657-01 / CON657-ADMISSION`：global workflow 划分初始创建与既有活动续接。Identity/Establish/rebind/Ensure/Bind 只拥有当前 common-dir 身份和位置；原阶段 owner 判断实际写入资格。原 create-task recovery 精确 binding0/ledger1 边界保留，不服务通用恢复。

`D657-02 / CON657-SELECTION`：created wire、schema/exit 和唯一 consumer id 不变。consumer 读取公共 current selection/phase 并沿唯一 continuation 路由；只有 planning 满足相应 profile 前置时进 Author。普通 source/gate 缺失回原 owner，不重置 phase、不新增缓存或 state authority。

`D657-03 / CON657-SCOPE`：Clarify pre-Author→scope-only Author→Clarify acceptance→post-Author→原阶段 owner。两种 scope_ready2.0 closed shapes 及唯一 accept_scope writer 保持；post-Author 不回写根 PRD，原阶段合法 rework 后更新受影响 Delivery 规划。无 current Delivery 按义务 Creation/Completion，撤回不造空切片。

`D657-04 / CON657-DISTRIBUTION`：原 Discovery、Review、verifier 及 managed specs 统一 current 合同；通过 matching workflow/preset/platform 迁移，历史 pinned-old 与原 producer 的既成副作用恢复保持。完整细节只由 canonical packages/workflow 定义，RDT 不复制 schema。

Architecture 的窄替代与晋升由原 owner 负责，本贡献不改 constitution、GAP 或终态。实际 after 纳入新 candidate/begin_check 后才最终 Check/committed Review。
