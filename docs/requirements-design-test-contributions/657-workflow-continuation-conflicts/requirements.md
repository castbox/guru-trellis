# 活动续接与迁移残余合同需求贡献

状态：promoted，完整定义已整合到 manifest 指定的 current 单元。适用来源为 Issue #657 F1–F6/R1–R7/V1–V12，固定前驱为 Git `319202beab79c7666ecdb855291bf117e43d407e`。完整拟写定义在 manifest 的三个 proposed targets；本文件说明变化，不代替完整单元。

- `R657-01 / BEH657-ADMISSION`：初始 Task 创建及原操作恢复使用精确 created；既有 Task 正式身份、binding/rebind、唯一 checkout 和阶段 owner 满足时，原创建 DTO 不可得不能阻塞写入。每批写前仍检查 live boundary。保留 Task/generation/source/history，不重开 Task 或空 Delivery，不放宽初始 validator。
- `R657-02 / BEH657-SELECTION`：Creation/Selection 的 created 只交明确 key/root。原 consumer fresh 读取公共阶段；planning 且符合适用 Author 入口才规划，其余活跃阶段回唯一 continuation。phase 不证明 gate，历史或 stopped 对象不冒充当前执行。
- `R657-03 / BEH657-SCOPE`：范围变更先 Clarify pre-Author scope_ready2.0，唯一 Author 写根需求，再 Clarify acceptance 发布 accepted_scope；只有 post-Author task_key 结果才交当前阶段合法返工或撤回。revised/no_change/withdrawal_required 与无 Delivery 分路均保持，不用旧 clear/profile 或空切片。
- `R657-04 / BEH657-CONTRACT`：Discovery/Review/verifier 当前身份与入口对齐，保留原验证约束。canonical、managed spec、平台和 installed 完整成套切换；历史 schema 不重解释，原在途操作由原 producer 恢复。

不变责任为 R531/R635 的公共身份、唯一 owner、跨环境共享事实及资源边界，以及最终 Check、独立 Review、Closure/Finish。#649、完整 Release 矩阵和业务现场升级不进入本批。当前没有新增公共 DTO、状态或脚本语义 router。
