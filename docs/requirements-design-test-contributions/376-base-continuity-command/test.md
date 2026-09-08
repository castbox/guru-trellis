# #376 Base-continuity command Test contribution

- `T376-CONT-01`：Reconcile canonical/installed contract/runtime/eval 覆盖无关 base delta、真实 authority/
  task-content drift、expected-head executor、commit recovery 与零写入 negative cases。
- `T376-CONT-02`：Review Branch canonical/installed contract覆盖 current schema、prior/current identity 分离、
  ancestry/pair/tree freshness、bounded scope 与最小 public output。
- `T376-CONT-03`：source/installed integration 使用真实 Git repository 和真实 Publication recorder/checker/
  wrapper，覆盖 Finalizer mismatch -> reconciliation commit -> bounded continuity -> `ready`。
- `T376-CONT-04`：Publication package regression 保持当前 reviewed-content strictness；未审查 base merge、
  content/authority/scope drift 和 stale checkpoint 均不能进入 ready。
- `T376-CONT-05`：source package closure 从 registry/interface 派生 23 packages / 78 commands，并验证
  canonical/installed/platform projection、manifest、ownership、overlay drift、JSON/Python/shell 与 task artifacts。
- `T376-CONT-06`：Issue #108 的 39 个 `.bak` 及既存 installed drift 保持独立边界；本任务不修改、
  登记、删除或以 full reapply 吸收它们，也不执行完整多平台 Release/upgrade matrix。
- `T376-CONT-07`：promotion 保持 `.45` 正文与 release facts 不变，只写 predecessor lifecycle locator，
  并验证 `.45` Design manifest 的历史 command count 从错误的 81 收敛为真实的 77。
