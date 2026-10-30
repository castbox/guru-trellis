# ADR-EXPLICIT-REVIEW-OBJECT：独立 final_plan 对象接入

状态：proposed；owner为原Architecture maintenance。来源[live #694](https://github.com/castbox/guru-trellis/issues/694)，适用before为`2dbaf308e6d5137bf640cfe546a078497c1c713a`。本文件是task-owned候选；目标为`docs/architecture/adr/explicit-review-object.md`，shared写入仍须原完整候选评审、Check和final_integration。

## 背景与决定

原R679及接收流程对有context的独立final_plan也要求Task/Delivery选择。完整对象足以定位一次性评审，持久选择没有后续执行consumer；同时普通执行仍需要自己的选择。两类对象关系必须区分。

只在原Architecture `delivery_task_impact_sync / planning / final_plan`接入允许完整显式对象经只读校验后评审。原TaskId/generation、C4/唯一注册checkout、公开关系/profile、非终态planning、scope/root及设计内容freshness保持；合法已有选择复用，其他选择、损坏绑定和真实冲突回原owner。显式对象不写成session选择，正式typed结果不代表选择已建立。

原Architecture AI仍独立决定impact/出口；authority-first与空任务历史方法不变。只有原允许的成功出口交相邻Approval，其接收者保自己的合法选择。Author/Wording/Approval/Activation/实施、candidate_assessment及其他Architecture stage保原绑定/选择与恢复writer。

## 替代范围与理由

本决定窄替代R679、D679及原Architecture/工作流中“所有Planning接收者一律先Bind/Selection”的final_plan部分；原模型、single-writer、其他stage条件及首失败/错误路由存续。ADR-024/035的身份与唯一owner分工保持。

拒绝全局current(key) fallback，因为它会改变未接受consumer；拒绝先自动写选择的wrapper，因为它不满足一次性只读目标；拒绝通用派发框架和新大DTO，因为现有输入已完整且仅此目的需要变化。原包本地purpose限定复用原事实校验，维护成本与影响面受限。

## 采用与验证边界

canonical Skill/workflow/派发及原完整RDT/Architecture单元同步收敛，再经matching preset分发。旧完整安装成套采用前保原合同，同key/root/实际义务续接；没有持久格式迁移、第二版本reader或OS协调机制。

验证沿原开发、定向package/installed/reapply、Check和独立完整Review。普通错误、真实选择冲突和无context合法入口必须保持。当前仍为设计，尚无新入口行为/安装/交付证明；source完成不代表已有业务安装采用。
