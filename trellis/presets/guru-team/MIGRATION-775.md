# Check 规划回退交接与原结果恢复

本次直接演进原 Check `planning_stale` 合同。当前首次 Check 使用成套 matching
Check package、workflow/router、consumer schema、Author 来源说明、示例与声明平台
投影。已回退旧现场必须先按下节从完整外部 provider 恢复未变目标；不能先原地
更新其已跟踪工具。后续由原 tools owner 按独立审查的写集采用目标工具，保留
Task/session 和用户修改，处理实际 sidecar、验证 drift。源码变更不代表目标安装
或业务现场已采用。

## 已回退旧现场先恢复未变目标

原 owner 先保留目标 checkout 的 candidate、HEAD、三份规划字节、原 Check 6.0、
原 public input 及实际原公共来源。选择目标之外的完整 matching Guru provider；
该 provider 提供当前 workflow/router、Check package、consumer 合同、dispatcher 和
managed runtime。目标继续提供其已安装且兼容的 Task schema2 / Delivery API1.0、
C4 和真实当前选择。不得复制单个 package，也不使用目标旧 dispatcher 执行新入口。

从完整 provider 的公开 Check wrapper 传既有 `--root <目标checkout>`。launcher
选择 provider 自己的 runtime，Check 对指定目标调用其已安装公共 API。invoke
元数据与 help 声明该目标参数及 API 前置。原 Task/Delivery 身份和状态仍由目标
公共 API 拥有；无兼容 API、身份/选择失配或缺原来源时，按原诊断停止。不得从
provider 加载私有 Task 模型作为 fallback。完整命令由下文链接的 Check 合同拥有。

必须先恢复旧交接，再由原 Author/Clarify 消费实际输出进入当前重规划。在不再
复用旧结果后，原 tools owner 才按另外审查的写集成套更新目标。恢复不安装或
更新目标工具。后续 implementation 按实际 after 重建候选并重新 Check。
先更新已跟踪工具会改变原结果覆盖的内容和 candidate；该现场回受影响原 owner
判断真实变化，不补旧 token，也不放宽内容校验。本采用顺序不新增执行服务、
备用 runtime、身份环境覆盖、恢复状态或账本。

## 当前 producer、router 与 consumer

`planning_stale` exit、`reapprove_plan` / `clarify_requirements` route、原 Author
输入及既有命令保持。`reapprove_plan` 对所有范围内修复输出空 proposal_refs 和
非空 revision_actions，动作来自 AI 在原 reason 中写出的具体修复要求；保留
私有 current_scope 决策。真实 scope_change_required 不能使用该路线。
clarify_requirements 只携带真实 scope_change_required 的 proposal_refs，不附动作。
router 只向 Author 复制 task_ref/delivery_key/revision_actions，并添加固定 profile
与当前 mode。旧“非空 refs → Author 且没有 actions”路径退出，不保留双路由。

这是公开 producer/consumer 合同的显式不兼容演进，沿当前路径和 id 成套切换。
旧完整安装固定在原发行；已有旧结果先使用上节完整外部 provider 的原 Check
恢复入口。不能仅替换 producer、放宽 Author 必需字段，或拿旧不闭合输出直接
进入新 router。

## 新的首次回退

正常 recorder 仍接原 11 字段语义输入。首次 planning_stale 时必须提供原
`--skill-input`；recorder 从真实公共 Planning/Delivery 派生最小 rollback_binding，
写入原私有 6.0 结果。普通通过结果不增加此字段。完整输出验证后，首次 invoke
才执行一次既有 rework 到 planning 并清除四类结果槽。

新结果中的局部绑定仅服务原 Check 恢复，包括原 key/Planning result ID、scope、
plan、candidate 和三份规划 evidence。它不进入后继 DTO，不表示批准、授权或
跨阶段 freshness，不新增通用事务或账本。原 owner 在消费者完成后退休此结果，
或由后续正常 record 替换。

## 修复前已经回退的现场

原 owner 读取完整旧 6.0、原公开 Check input 和实际当前 Task/Delivery。
`delivery_planning_stale_recovery` 不要求已清除的 Planning pass，也不调用普通
Check binding/checker。旧 6.0 无 rollback_binding 时，必须持有实际原公共 query
的 key/delivery，其中保留匹配 Planning result、scope/plan/evidence 和 candidate。
也可从精确原 Git Task 对象经安装的公共 parse_task_v2 parser 读取并选同 key；
不能用当前对象拼原事实。只有 Planning 结果而无原 candidate 时，来源不完整。

私有 owner-result envelope 使用 original_result、可选 corrected_result 和上述
original_delivery。原输入 ID 必须匹配实际原 Planning。原 owner 核对当前身份、
选择、planning phase、清空结果槽、scope/accepted_scope、plan、三规划字节、
candidate、HEAD、内容和路径。相同则只返回现有 planning_stale DTO，不重放 rework、
record_gate，不改 candidate 或旧结果，不制造 pass。

旧交接分类或动作需纠正时，AI 先依据当前 authority 真实判断，再按原合同以
recovery input 和 11 字段 authoring 调用 recorder --dry-run，形成新完整 6.0，
作为 corrected_result 与原结果一并交回恢复入口。旧结果字节保留；纠正不写新的
持久 checkpoint，不调用普通 checker。完整命令与 receipt 投影由原
[Check 合同](../../skills/guru-team/packages/guru-check-task/references/contract.md#recover-an-already-completed-planning-rollback)
拥有。

缺原公共来源时，公开 wrapper 返回 blocked，并在 stderr 指明缺失
owner_result.original_delivery 及原 Planning/Clarify 入口。原 owner 必须明确说明
缺口，停止该恢复；原 Planning/Clarify 在当前真实范围重新判断。不能手改旧
artifact/digest、恢复不存在的 Planning pass、使用 Activation 私有 checkpoint，
或创建替代 Task/Delivery。真实身份、范围、规划、内容或后续阶段变化保留具体
stale 字段与受影响原 owner 路线，不把任意 planning 状态当作同次回退。

## 验证层次

定向验证采用实际 recorder/checker/invoke wrapper fixture；首次回退后在 Planning
已清除状态测试恢复和 dry-run 纠正，旧无绑定转换使用保留的原公共来源。
恢复 wrapper 位于目标之外的完整 source provider，通过 --root 使用目标已安装
公共 API，并观察目标工具、业务字节、原结果和 candidate 未写入。目标工具发生
真实变化时，旧恢复仍拒绝；该 fixture 不表示完整旧安装升级链已验证。
producer 输出经正式薄投影通过真实 Author schema；真实范围变化仍走 Clarify。
同时检查受影响回归、matching packages、installed/声明平台、drift 和 sidecar。
这些证据不表示业务仓生产效果、完整 native Agent 链或多平台 Release 矩阵已验证。
