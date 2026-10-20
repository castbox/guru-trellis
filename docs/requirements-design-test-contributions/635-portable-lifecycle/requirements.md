# 跨环境生命周期需求贡献

状态：`promoted`。适用来源是 Issue #635 的 R1–R5/V1–V8 与固定基线 `7a7b60743499653ffeb81f6b31e627a02c33f579`。完整 current 定义位于 [生命周期](../../requirements/current/task-delivery-lifecycle.md) 和 [Completion/Closure](../../requirements/current/completion-closure.md)。六个完整单元已由原 owner 最终整合并读回；proposed 目录保留已审候选历史。

`R635-01 / BEH635-STATE` 区分可恢复共享事实、当前必须重审的语义资格、仅本机资源责任和实际必要输入缺失。Task、Delivery、source、scope 与已发生副作用按明确共享对象识别；不复制原机 runtime，不从 phase、旧 prose 或 provider 状态单独推出归属或 pass。

`R635-02 / BEH635-REACTIVATE` 以准确历史证明共享 Finish，已进入目标历史的归档不因本机 seal、退出或 Cleanup pending 被否定。已有后继继续同一 incarnation；没有后继才公共增代。当前 Task2 与指定正式旧 schema1 分路，保留前驱历史；人工历史和未完成 closeout 不混用。

`R635-03 / BEH635-RECOVER` 从已提交且可获取的明确 source ref/commit 恢复同一活动 Task/Delivery；原 Publish、Merge、Closure 各自核对精确关联并只补剩余动作。Open Draft/Ready 的当前资格仍由原 owner 判断；MERGED 不证明整体完成。Closure 只保留跨 clone consumer 无法重新推导的最小动作输入。

`R635-04 / BEH635-RESOURCE` 按 common-dir 隔离本机资源；共享 remote ref 保留 repository/full ref/expected head 与 generation 检查。旧资源 pending 不阻止另一环境使用不同合法资源，也不授予清理原机或另一 Task 的权限。

`R635-05 / BEH635-MIGRATION` 保留公共模型与原 owner；公共入口及消费者成套迁移。至少证明一个独立 common-dir 原生样本和最多一个代表安装样本，分别报告实际 Agent、确定性、安装和 live 层次。没有完整 V1–V8 证据不能关闭整体范围。

替代边界仅是本机 receipt 参与共享资格、无法跨 clone 读取原动作集和无法明确恢复既有 Open PR 的片段。#636/#637/#638 的 Draft、候选适用性、最终整合及真实最终门禁继续有效。无双主、锁/租约、攻击或压力扩展。
