# #454 C6/C7 Task Creation And Phase C Validation Test Contribution

状态：`candidate_unreviewed`。下列为待运行的 focused acceptance 和证明边界，**不是**通过记录。

- `T454-C6C7-01`（R01）：reviewed existing Issue 与 standalone 两条 create path；draft Issue 创建后 live
  reread、Sync/fresh Intake，create 本身零 Issue mutation；no-Issue 不产生伪 Issue/Closure identity。
- `T454-C6C7-02`（R02）：registered clean branch-bound invocation checkout 被 adopt且不创建第二 worktree；
  detached/foreign/base/dirty/other-task branch拒绝；base drift 返回 refresh，base unchanged + HEAD mismatch
  返回 blocked而非自动 provision。
- `T454-C6C7-03`（R03/04）：C3 `provision_disposition` 三值与 adopt primary/linked 的五种 ownership 投影：
  `new_branch` 创建 Guru-owned branch/worktree；`existing_branch` 保留 caller-owned branch 并创建 Guru-owned
  worktree；`existing_checkout` 精确复用 caller-owned registered linked checkout；adopt 不带 disposition。
  变化的 live pre-state 拒绝旧 plan。TaskId/generation 0/TaskRef、branch revision 0 与 ledger
  epoch/revision/branch 同步；call-local path 不持久化。
- `T454-C6C7-04`（R05/06）：context key 有/无与 session write failure；无 key 返回 explicit-task mode；
  task result loss 只读恢复且不重复资源 mutation；activation input 的 planning/status freshness、approval 不
  直接激活及 activation output loss 不重复 status mutation。planned owner 尚无 package 时仅验证 shared input，
  不声称完整 activation Skill 测试。
- `T454-C6C7-05`（R07）：active package/exit/command 清单不变，六个 planned IDs 只含 ID/state 与非路由说明并列于
  `planned_skill_ids`，无 planned package tree/interface、selector、workflow edge、installed/platform projection；
  E434 package tree/typed exit/parity/consumer 测试仍 deferred。
- `T454-C6C7-06`（R08）：static scope 明确只覆盖 Phase C 新代码，证明对 task/workspace mapping、
  `worktree_path`、`source_checkout`、legacy session path 零读写；现有 production predecessor 继续存在，
  E434 才证明其全局退休。不得把 predecessor 搜索命中误记为新 substrate 回归。
- `T454-C6C7-07`（R09）：fixed Fork exact source build 与 focused task/session/generated tests；lifecycle
  kernel/checkout/branch/session/ledger/creation/activation-input runtime/schema contract；source preparation、
  upstream ownership、dogfood overlay drift、recursive sidecar、managed Python routing、task validator、
  format/lint/type、secret scan、touched non-generated file 3000-line report 和 `git diff --check` 各自记录
  exact command/result。clean throwaway 仅在当前 accepted scope要求时运行，且仅证明 official primitives。

每项执行证据必须绑定本轮 candidate；未运行写 `unverified`，失败写失败，不能沿用 C5 focused `113/113`。
完整多平台 installer/upgrade/workflow-switch/Release matrix 归 #410。Phase 2 semantic check、Task Commit、
完整 Branch Review、Docs serialized promotion、Publication 与 production graph activation 仍为独立 gate。
