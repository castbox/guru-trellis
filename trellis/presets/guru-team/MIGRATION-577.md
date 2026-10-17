# #577：人工旧归档恢复

本迁移在原 `guru-maintain-legacy-task` 增加独立 `archive_resume` profile。
原 convert、history_closeout、resume、rollback 及其 typed exits 保持原义。
当前输入、独立 schema、调用和完整语义步骤由该 package 的 Interface 与
`references/contract.md` 独占。完整 Plan2、工具更新和正式 Reactivate 仍归原 owner。

## 数据与当前身份

新输入显式选择 archive task_ref、original_task_ref 与 active_ref。公共 CLI/Core
独占归档/活动关系、受支持格式、generation、转换、session/binding 和恢复回退。
Guru 提供已审查投影与恢复意图，并消费公共 returned resumed_task。原归档可读且
仅作历史，当前执行只使用活动记录。创建/历史 identity reservation 仍保留归档占位；
当前 Identity 与 Bind 共用目标 installed 官方 active resolver，不复制公共识别算法。
首次绑定前，Identity 只用公共 schema parser 验证活动记录并保留原 active 占用检查，
交原 C4 建立绑定；绑定后仍由官方 resolver 核验选定 checkout，C3/Bind 门禁不变。

原六个私有 owner 的 inspection/freeze/retirement 输入新增可选 source_task_ref。
该字段指向物理归档，task_ref 仍标识原活动控制归属；未提供时使用原 task_ref。
这些 owner 分别冻结和恢复自身资产，不共享或复制私有状态解释。恢复 coordinator
验证原 archive 与公共保存的原始 source 后，才调用各原 owner 精确退役。
正式 Finish 及合法人工 Cleanup 仍走 Reactivate。未完成 Closure/Finish/Finalizer
回原事务或既定人工处置，不按人工历史归档恢复，也不制造 seal 或完成结果。

## 依赖与采用边界

原 transport 接受 API1.0 的基础 tools_install/task_conversion/legacy_closeout
及 additive task_resume，并转发 prepareArchivedTaskResume。归档恢复准备必须具备
实际 task_resume 能力。实际 package digest 继续覆盖 bytes/modes；source_locked
仍严格核对正式 source lock、构建和 mode，不更改 Fork pin 或静默安装依赖。

本次匹配候选来自 Trellis PR #52。其 CLI/Core 标签均为 0.7.0-castbox.4；标签不
证明源或构建一致。仅 local_candidate 用于隔离开发。CLI 的 cli_adapter.py 与
task.py 两份 Python template 在实际打包安装后为0644，source dist为0755；严格
source_locked 校验保留这个缺口。正式配对来源采用和真实业务恢复由各原 owner
另行处理，不能把本地能力验证描述成正式安装或发布。

## 分发与验证

canonical source、受管 runtime、平台发现 package 和 spec 必须一起 reapply。
不修改上游 template、hook、全局安装或 node_modules。官方 update 后按原 marketplace
选择和 preset reapply 恢复；处理实际 sidecars 后检查 source/installed 与 drift。

目标恢复须实际执行 installed Identity、C3/C4、Bind、native continuation 及下一
Guru 语义 owner。历史交付由原 Publish/Merge 核验，当前 scope 补差归 Clarify；补验收
不创建空 Delivery。一个代表性隔离旧安装证明本范围，完整 Release 矩阵仍属专门 owner。
实际测试和未验证边界由本任务唯一 RDT Test 记录，不在本文件预写通过结论。

对原 tools owner 使用的历史来源解析，只有 receipt 明确记录 tree_state=dirty
时，其真实 provenance commit 才可在整体 extension/core metadata 不同的情况下
提供逐路径历史候选。仍需可读 Git 对象、原逐路径字节检查及未知 preimage 的
显式 preserve/replace；不以 HEAD 或 target hash 代替历史。clean mismatch、
缺对象及正式 source_locked 合同均不放宽。
