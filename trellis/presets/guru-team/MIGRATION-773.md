# Task 分支诊断与工作区载体恢复的匹配采用

本迁移承接 #773 R1/R2。原 Branch owner 新增显式工作区恢复准入，并在
discovery/plan recorder 共用的 Task 解析边界保留准确诊断。采用须包含同一
Guru source 的完整 Branch package、共享 lifecycle runtime、Interface、schemas、
commands、examples、四个原 owner 的 Skill 正文及受影响受管投影。

## 公开合同差额

- `delivery_active_task` 的 establish/recover、字段和既有 typed outputs/consumers
  保持。普通未绑定候选仍按 HEAD Git 树验证，枚举和排序不改变。
- 新增独立 `delivery_restored_checkout` 输入及
  `guru-establish-task-branch-binding-input-delivery-restored-checkout-1.0` schema。
  输入为 profile/mode、TaskId/TaskRef/generation、branch_name 和 expected_head；
  root 为当前注册 checkout。没有 action、授权、恢复历史或新 output 字段。
- aggregate identity 从 `guru-establish-task-branch-binding-input-delivery-1.0`
  演进为 `guru-establish-task-branch-binding-input-delivery-2.0`，明确 union 两个
  profile。原 active-task profile schema 保持原义，不把历史输入重解释成恢复。
- discovery 和 plan recorder 的正常缺失 Task 仍被拒绝。错误使用既有
  `stale_identity`、退出码3，保留原 `task_not_found`、实际 TaskRef field_path
  和 Identity/Branch 恢复指引；不再将此已知前置错误归为 `internal_error`。
  错误 DTO 形状不变，内部未知故障仍保留其原错误语义。

新 profile 仅补原 C4/C5 缺失控制，复用匹配控制并拒绝矛盾。现有权属不改；
缺失权属采用 caller_owned，primary worktree 为 not_applicable，linked 为
caller_owned。不继承 Creation 的 non-primary/non-base 限制，不放宽普通候选，
不要求隐含 commit。Task/Delivery schema、身份、历史 gate 和公共阶段不迁移。

## 采用、原操作与恢复

已有安装继续使用其完整旧合同，或通过原 `guru-upgrade-tools` 从完整匹配源
升级工具并保留 Task/session。旧安装不能只复制新调用 payload，也不能只替换
一个 dispatcher、schema 或 Skill 文件。源码更新不证明安装已采用；普通 apply
的历史 inventory 阻塞不授权手拷文件、绕过门禁或转换无关历史 Task。

升级前检查所选 checkout 和真实共享路径中的未完操作；它们仍归原 owner 和
原 recovery identity。保留原已执行动作与当前本地内容，不用新 schema 续命旧
gate。新建立结果输出丢失时，原 discovery 提供实际 binding_ref，再以原 recover
action 只读回同 revision/branch/HEAD；不会产生新 Task、Delivery、结果账本或授权记录。

同身份载体恢复的完整顺序和停止条件由原 Branch
`references/task-carrier-recovery.md` 单写。Identity 只核工作区身份，Ensure 只核
当前 checkout，接收聊天 Bind 只处理自己的 pointer；历史 Publication/Delivery/
full_review/readiness 缺口保持。各自成功不构成 Task Completion 或 Issue closure。

## 验证边界

采用后验证共用缺失诊断、原成功/只读恢复、新动作的一条去敏代表恢复及历史缺口
保留，以及受影响 package/runtime、canonical/installed/dogfood/声明投影、drift、
sidecar 和执行位。原工具 owner 验证真实 Task/session 保持和实际冲突处理。

本说明不是测试报告，也不证明安装、native Agent 全链或业务恢复已经通过。
本项不重建 #223 聊天、不重操作业务仓库，不运行完整多平台安装/Upgrade/Release
矩阵。实际结果必须说明执行入口、观察层次及尚未验证范围。
