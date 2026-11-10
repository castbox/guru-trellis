# Task 载体诊断与同身份恢复

知识单元：`RDT-REQ-TASK-CARRIER-RECOVERY`；别名：R773 / BEH773。
状态：current；authority：`guru-trellis-rdt`；原 owner：
`guru-maintain-requirements-design-test-ssot`。来源为
[Issue #773](https://github.com/castbox/guru-trellis/issues/773) 的 R1/R2 与最小验收；
适用前驱为 Git `313d80215f65777fc70893a90c6d8dce8005d6dd` 中的
[`RDT-REQ-LIFECYCLE`](task-delivery-lifecycle.md)。本完整定义仅在原 RDT final_integration 实际晋升后生效；隔离 proposed 文件不改变共享 authority。

## 能力与适用边界

本能力服务正常缺失原 schema-2 active Task 的 AI 调用方。原 Task 及完整规划存在于
可获取的固定 Git 载体；恢复保持 TaskId/generation/source/scope、Delivery 和真实
历史。恢复者选择目标基线、注册 checkout 和精确写集后，沿原 Identity、Branch、
Ensure、Bind 及 Git/task.py writers 继续同一生命周期。

公共模型、阶段结果、通用跨环境接续和整体 Completion 仍由 lifecycle 单元与各原
packages 定义。本叶只展开载体与当前环境关联的差额。文件恢复、基线修改、C4/C5
关联和 session binding 是独立结果，不能合并表述为业务交付或 Task 完成。

## R773-01 / BEH773-DIAGNOSTIC：准确拒绝

公开 branch discovery 和 plan recorder 正常遇到缺失的规范 TaskRef 时，必须保持
拒绝。现有诊断结构须定位原 `task_not_found`、实际 TaskRef 和原 Identity/Branch
恢复处理。不能将缺前置变成无候选成功，也不能把这一已知生命周期条件误归为
`internal_error`。转换位于两入口共用的 Task 解析边界，不扩大为通用异常框架。

## R773-02 / BEH773-CARRIER：固定载体与精确写入

AI 先固定原完整 Git commit，再核唯一 TaskId/generation、source/scope、Delivery、
各 planning_root 的完整计划及真实 Publication/Delivery/full_review/readiness 缺口。
目标基线、当前 branch/registered checkout 和精确文件写集必须明确。原 Git 只恢复
已审路径；所选基线改变时由原 native task.py writer 更新。重读结果并保留本地并行
工作，不通过内部 Python、手编 common-dir JSON 或手改受管文件填补公开动作。

载体不可获取、身份/source 不唯一、schema 不受支持或记录矛盾时，停止依赖动作并
回原 Identity/source/migration owner。已明确的同目标恢复自动接续；真实目标、写集
或副作用变化沿原对话边界。授权只存在当前对话，不进入文件或公共输入输出。

## R773-03 / BEH773-ASSOCIATION：原身份在当前环境的关联

Identity 可读取恢复后的工作区 Task。普通未绑定 Branch 候选仍从 HEAD Git 树验证，
因此未跟踪恢复目录不足以成为普通候选。指引必须说明该前提差异；不能反复扫描
代替恢复，也不能隐含要求提交。

已有有效 C4/C5 直接复用。普通 HEAD 候选满足原合同则使用原 establishment；已核
工作区恢复但 HEAD 缺 Task 的首次/补缺关联，由原 Branch 的显式恢复 profile 承接。
只建立缺失 controls，匹配 controls 和既有 ownership 保留，矛盾停止。primary 与
linked checkout 均受支持；缺失权属采用 caller_owned，primary worktree 为
not_applicable。普通候选枚举/排序、Creation 和 Rebind 准入不改变。

Branch 实际成功后由 Ensure 重读唯一 checkout，再由接收聊天自身 Bind 处理自己的
pointer。保留已有同 Task Delivery selection；真正无 context 沿原 explicit-task
路径，不写 session。current/continuation 决定真实剩余义务，no_current_delivery
不自动创建空 Delivery。绑定不补造历史 gate 或 Publication/Delivery 归属。

## R773-04 / BEH773-ADOPTION：匹配采用与证据

新恢复能力须由完整 matching Branch/shared runtime、schemas/Interface/commands/
examples、原 owners 的指引及受管投影共同采用。已有 checkout 由原工具维护 owner
保留 Task/session 完成同步，处理实际冲突/sidecar；普通安装阻塞不授权手拷或迁移
无关历史。旧完整安装保留其原合同，不热解释新输入。

验收包括两个共用缺失入口的定向回归、原成功/只读覆盖、指引公开可执行性，
以及执行动作变化后的一条去敏代表载体恢复及历史缺口保留。证据须说明实际层次。
不重操作原 #223 业务事件，不扩大为 native Agent 全链、生产验收或完整多平台
安装/Upgrade/Release 矩阵。

## 关系

职责和接口：[D773](../../design/current/task-carrier-recovery.md)。验证策略：
[T773](../../test/current/task-carrier-recovery.md)。原公共生命周期完整定义仍读
[Task/Delivery 生命周期](task-delivery-lifecycle.md)；本叶不重定义阶段或终态。
