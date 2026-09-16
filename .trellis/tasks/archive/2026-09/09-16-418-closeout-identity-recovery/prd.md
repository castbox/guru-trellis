# #418 归档身份收敛与 Merge 恢复

状态：source实现与新基线上的installed fixture验证已完成，任务HEAD为78651e20且已同步投影。正式门禁结果以各owner当前输出为准；不声明独立committed review、promotion或发布完成。

## 1. 目标与来源

修复正常 Finalizer 归档后的 runtime locator 漂移，并使 closeout/stale/re-entry 失败具有明确诊断和保留原门禁的恢复路径。

唯一需求来源：[Issue #418](https://github.com/castbox/guru-trellis/issues/418)，正文更新时间 `2026-09-16T08:32:10Z`。基线为 `main@57e8b5df10aedc4f218a4685e819d25a44aa8928`。

## 2. 已核实事实

- Finalizer `runtime/_owner_part_04.py:1649` 的 `execute_archive_metadata_transaction` 执行 archive move/commit/push，但该函数没有同步 task mapping。
- Finalizer `runtime/_owner_part_01.py` 的 `load_task_runtime_identity` 要求 mapping 的 `task_artifact_dir` 与当前任务目录一致；已有但过期的 mapping 不属于 missing-mapping rebuild。
- Merge `runtime/owner.py:1110` 的 preview 只读取 public input 与 live GitHub facts，不直接读取 Branch Review checkpoint。
- Merge 自有 `WorkflowError` 不是共享 `CommandError`，`runtime/check.py` 直接调用 owner；共享 dispatcher 的兜底异常处理会丢失具体错误。
- 只读复现正式 `preview-task-pr-merge.sh --root . --input /tmp/guru-418-missing-merge-input.json --json`，退出码 2，返回 `internal_error/runtime/Inspect the package runtime and retry.`。这证明缺失输入的诊断传播缺陷，不证明原下游故障的具体触发原因。
- Branch Review 当前合同在成功投影后退休 checkpoint；旧 schema gate 被原 owner 判为 stale，不应成为 Merge 的额外私有输入。
- 对本任务尚未生成 checkpoint 的状态调用正式 `check-review-gate.sh`，退出码 3，返回与 Issue 相同的 `stale_identity/checkpoint/Rerecord the current Branch Review gate.`。该字符串本身不能区分缺失与旧 schema。

## 3. 需求与验收

| ID | 必须满足的行为 | 验收 |
| --- | --- | --- |
| R418-01 | 正常归档后，同一 task 的源与目标 runtime 映射不残留 active locator | 正常 producer 生成的映射与归档后 boundary 检查 |
| R418-02 | archived task、checkout、branch、Finalizer、PR 唯一对应 | 正式调用链联接测试；未知或冲突身份仍阻塞 |
| R418-03 | 已知 stale/缺失/不一致错误不折叠为无诊断 internal_error | 正式 wrapper 的错误码、字段与脱敏 remediation |
| R418-04 | 旧 Branch Review 被拒绝后提供完整标准恢复路径 | 重新审查和正式记录、重建 Merge input、再次 preview；不手写 pass |
| R418-05 | 保留 Branch Review、Publication、Finalizer 与 Merge 门禁及副作用边界 | 无提前 merge/PR mutation，无跨 owner private-state 消费 |
| R418-06 | 覆盖 active-to-archived、mapping reconciliation、stale review、fresh re-entry、preview | 对应正常生产入口回归 |
| R418-07 | canonical、dogfood、installed、声明平台投影一致 | 定向 package/install/reapply/drift 验证 |

## 4. 排除范围

只读恢复要求：业务 task 保持 completed；归档历史、PR/head/title/body 与 Issue 状态不变。旧 handoff 缺失时先捕获当前 PR 快照并进行真实新审查，不能把快照 digest 当旧批准。新复审锚点 A 与原 closeout 锚点 H 分离；必要的 private recorder/checker状态只服务当前owner，完成后退休。完整恢复路径以 design.md 的 D418-03 为唯一设计定义。

不修改业务仓库代码，不手工编辑业务 runtime，不修改 upstream/global Python/npm，不绕过 fail-closed。不处理 #419 active continuation、#421 Intake owner、未来完整 lifecycle 重构、攻击模型、锁、TOCTOU、额外 fault injection 或跨 OS 加固。不新增全局台账、授权 artifact 或长期双读兼容。

## 5. 原下游对照边界

Issue 未提供原下游 repo/task/PR locator、installed extension identity、实际 preview argv 与输入 shape。当前源码中 Merge 不读取 Branch Review checkpoint，因此两者同时失败不能证明因果关系。

当前已从正式入口独立复现错误传播问题，并由原 checker 证明相同 stale 文案的缺失来源。原实例用于后续对照，不作为这些已确认缺陷的实现前提。不得声称两条原始错误已经证明存在因果关系，或原业务故障已经修复。业务取证只保留脱敏结构、版本身份与错误码，不复制业务数据、凭据、PR 敏感正文或原始日志。
