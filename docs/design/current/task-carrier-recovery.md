# Task 载体恢复的职责与接口

知识单元：`RDT-DES-TASK-CARRIER-RECOVERY`；别名：D773 / CON773。
状态：current；authority：`guru-trellis-rdt`；原 owner：
`guru-maintain-requirements-design-test-ssot`。来源为 [R773](../../requirements/current/task-carrier-recovery.md)
及 #773 D1 已审方案。适用前驱为 Git `313d80215f65777fc70893a90c6d8dce8005d6dd`
的 [`RDT-DES-LIFECYCLE`](task-delivery-lifecycle.md)。本完整定义仅在原 RDT final_integration 实际晋升后生效；隔离 proposed 文件不改变共享 authority。
Architecture 关系与 `ADR-TASK-RECOVERY-ASSOCIATION` 由原 Architecture owner 维护。

## D773-01 / CON773-DIAGNOSTIC：共用解析边界

Branch package 的 discovery/plan recorder 在枚举候选前解析 Task。原共用边界将
`LifecycleContractError` 转为既有 `CommandError`，保留原 error code 和 field_path；
正常缺失使用 `stale_identity`、退出码3，`remediation` 含 `task_not_found` 及原
Identity/Branch 恢复指引。错误 DTO 和拒绝语义保持，未知内部异常不假称已知前置。

准确 schema、命令和输出由
`trellis/skills/guru-team/packages/guru-establish-task-branch-binding/` 单写。本设计
只定义诊断责任，不建立新 error framework、空候选 fallback 或流程判断脚本。

## D773-02 / CON773-RESTORE：各原 writer 的顺序

1. Markdown 原 owner 固定完整 Git carrier，核原 TaskId/generation/source/scope、
   Delivery、完整规划和历史缺口，选定目标基线、当前注册 checkout/branch 与写集。
2. Git `restore --source <fixed-commit> --worktree -- <reviewed-paths>` 恢复已审文件。
   基线改变时由原 `task.py set-base-branch <TaskRef> <base>` 单写字段。
3. 原 Identity 解析恢复后的 workspace Task。该结果不保证未绑定 HEAD 候选成立。
4. 原 Branch 审查并建立/复用 C4/C5，Ensure 重读唯一 checkout。
5. 接收聊天自身 Bind 处理当前 pointer，再读 native current 与 workflow continuation。

每步仅表达自己的事实；来源/身份歧义、公开动作缺失或普通控制冲突回原 owner。
原 Branch `references/task-carrier-recovery.md` 拥有完整可执行例、语义 Gate、真实
副作用边界和停止/恢复顺序。其他三个 Skill 保留自身前置及结果含义并引用它，
global workflow 不复制 step-local 正文。

## D773-03 / CON773-C4C5：显式工作区准入

普通 `delivery_active_task` discovery/record/establish/recover 保持。未绑定候选仍
校验 HEAD 树，已绑定同分支按原工作区规则校验。新 `delivery_restored_checkout`
只服务已审原载体恢复后的显式当前 checkout 关联，入口仍为原 Branch invoke。
输入为 profile/mode、TaskId/TaskRef/generation、branch_name、expected_head；root
是调用期注册 checkout。完整 schema 仍由原 package 单写。

executor 核 schema-2 active 身份、TaskId/generation、注册及实际 branch/HEAD、
同 common-dir 和控制冲突。C4/C5 已存在项须同 key/branch/revision；匹配复用，
只补缺项，另一 Task 占用或 unresolved incarnation 停止。两项均缺时原 revision0；
一项存在时复用其 revision。primary 不受 Creation 的非 primary/non-base 限制。
新 branch 权属 caller_owned，新 primary worktree 权属 not_applicable，linked
为 caller_owned；既有 ownership 原样保留。

原 C4 经 `OwnershipPort` 调 C5，复用原 snapshot/write/readback/rollback 事务，
不复制 ledger representation 或新建 store。动作不写 Task/Delivery 内容、gate、
session、授权或跨 owner recovery state。成功保原 `binding_established` TaskKey
及 Ensure consumer；身份问题和控制问题分别保原 invalid_task_state/blocked。

stdout 丢失先用原 discovery 读实际 already_established/binding_ref，再以原
recover action 核 exact revision/branch/HEAD 只读恢复。同一结果不重新分配身份或
覆盖控制，普通失败沿原事务处理。这里没有锁、crash consistency 或重试账本。

该明确输入分支填补“工作区 Identity 成立但初次 C4/C5 关联无法公开执行”的实际
缺口。仅补文字不能完成该动作，强制 commit 增加副作用，放宽普通 HEAD 候选扩大
所有调用的准入。复用原事务限制维护成本；代价是一个有当前 consumer 和验收的
profile/schema 分支。当公共模型提供等价动作或原 C4/C5 authority 改变时，由原
Branch/Architecture 重评并显式迁移，不预留通用恢复策略。

## D773-04 / CON773-DISTRIBUTION：同一公共能力的采用

新 profile schema1.0 与 aggregate2.0 是同一原 owner 的 additive 公开演进；既有
active profile、typed outputs 和 consumers 保持。完整 package/shared runtime、
Interface/schema/commands/examples 和原 Skill 指引由原 installer/tools owner
成套投影；迁移边界由 `trellis/presets/guru-team/MIGRATION-773.md` 定义。

旧安装固定原合同或匹配升级，不能局部替换或把新恢复调用重解释成旧 action。
Task/session 与本地内容保留，实际 sidecar 归原 owner。源码一致只证明分发，
installed、native Agent、远端和业务效果按实际观察分别判断。

## 关系与状态

测试 [T773](../../test/current/task-carrier-recovery.md) 覆盖上述四项责任。Task/Delivery
阶段及通用既成副作用恢复仍由 [lifecycle](task-delivery-lifecycle.md) 定义。本单元
不声明当前实现、安装或生产结果；原 RDT final_integration 在候选审核后写入并读回
实际完整定义，后续最终质量链覆盖 after。
