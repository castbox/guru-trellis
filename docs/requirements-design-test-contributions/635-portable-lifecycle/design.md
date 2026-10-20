# 跨环境生命周期设计贡献

状态：`promoted`。完整 current 职责定义位于 [生命周期](../../design/current/task-delivery-lifecycle.md) 和 [Completion/Closure](../../design/current/completion-closure.md)。接口字面、schema 和恢复行为由各 canonical package 单写，本贡献不建立第二模型。

`D635-01 / CON635-SHARED-FINISH`：Reactivate 的原语义 owner 审查准确 Git archive、Task/source/scope、该版本终态关系及 bookkeeping PR/target；确定性 adapter 读取事实。Task2 复用公共 reopen；指定正式 schema1 复用 matching formal maintenance。先检查实际后继，再决定是否建立下一代。旧 seal 与 Cleanup 只交原资源 owner。

`D635-02 / CON635-CLOSURE`：原 Closure 单写最小 task-local carrier，并把其 AuthorityRef 关联到公共 Closure evidence。Finish reader 通过原 authority resolver 返回原 snapshot2.0。独立共享恢复 profile 零 provider close；carrier 只提供必要输入，不能证明动作完成或恢复授权。实际 current source、Completion、ResultRef、scope 与 provider 状态仍须核对。

`D635-03 / CON635-PUBLICATION`：两个闭合 remote Draft/Ready profile 显式选择既有 PR 和共享 source commit；复用原 Publish transaction executor，区分 PR remote head 和本地 binding。已完成动作只读回，剩余动作沿原 writer。真实当前 readiness 不从历史 Ready 或 phase 继承；MERGED 仍沿原 Merge recovery。

`D635-04 / CON635-ENVIRONMENT`：原 Identity/Establish/Ensure/Bind 恢复当前 common-dir 的合法执行资源。原各语义 owner 负责当前判断；可核验工程事实按候选适用性合同采用。资源 ownership、generation 和 remote expected-head 保持原 writer，未知归属保守保留。

`D635-05 / CON635-DISTRIBUTION`：matching provider、canonical packages、workflow、spec、声明平台与完整 preset 由原安装 owners 成套更新。source lock 采用、installed 行为和原生完整链分别验证。旧完整安装保留 pinned 行为；未完成旧事务不重解释，真实缺输入只阻塞其 consumer。

本次具体 provider 为已合并 Trellis PR #56 的 `e9fb95fd2eb0fb8441153e77384a9dfd3ea3358f`；准确可用身份由 canonical source lock 单写。该 provider 修复共享/较早后继快照检查，未扩大公共 I/O。旧 PR #55 的身份保留历史意义。
