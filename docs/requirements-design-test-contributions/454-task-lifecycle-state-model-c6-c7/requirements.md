# #454 C6/C7 Task Creation And Phase C Validation Requirements Contribution

状态：`reviewed_promoted`。Expected predecessor RDT/Architecture 为 `current-main-0.6.17-guru.63`；
serialized successor 为 `.64/active`。本文件只定义 C6 task creation substrate/activation inputs 和 C7 inactive
subtraction/validation acceptance，不替代 C1-C5 已提升 authority，也不提前实施 D443、D436、E434 或 #434 graph。

- `R454-C6C7-01`：未来 task creation 只接受 reviewed `existing_issue | standalone_request`；proposed draft
  由独立 Issue owner 创建并 live reread 后重入 Sync/fresh Intake。task source、accepted scope、Completion 与 Closure
  各有独立 authority；no-Issue path 不创建虚构 Issue、关闭语义或 `primary_issue`。
- `R454-C6C7-02`：adopt invocation checkout 在 mutation 前验证 common-dir repository、registration、branch-bound、
  non-base branch、cleanliness、task/branch exclusivity 与 reviewed `decision_head`。base authority 变化回 fresh
  review；base 未变而 invocation HEAD 不等于 decision head 时阻断，不静默改为 provision 或接受领先提交。
- `R454-C6C7-03`：provision linked worktree 将调用期审查的 live pre-state 绑定到 C3
  `CheckoutAcquisitionPlan.provision_disposition` 的 `new_branch | existing_branch | existing_checkout`：分别创建
  branch 与 linked worktree、在 existing branch 上创建 linked worktree、复用 exact registered linked checkout。
  adopt route 不带 provision disposition。既有资源保持 caller-owned，Guru 实际创建的资源才标 Guru-owned。
  call-local `checkout_root` 不进入 tracked task、
  session、branch association、ledger locator authority或跨 Skill handoff。
- `R454-C6C7-04`：两种 route 建立同一 TaskId/generation 0/可变 TaskRef、初始 branch association revision 0
  与匹配的 C5 resource ledger。task create/rename/archive 的 official primitive 保持单一 framework owner，
  C6 不复制 TaskId/session store，也不读写旧 task/workspace mappings。
- `R454-C6C7-05`：context key 有效时仅经 official-backed C5 adapter 写入 path-free session；缺失时返回
  `explicit_task_mode` 且 lifecycle 成立。session write failure 不回滚 task creation；output loss 只能只读重建
  同一个 result，不重复 Issue、task、branch、worktree、binding 或 ledger mutation。
- `R454-C6C7-06`：Planning approval 不触发 status mutation；未来 `guru-activate-task` 独占
  `planning -> in_progress`，result loss 只读恢复，不重复激活。C6 提供可供 E434 组合的 shared runtime/schema、
  direct-consumer requirements 与 activation inputs，不把 planned identity 冒充已可调用 Skill。
- `R454-C6C7-07`：六个 C6 owner ID 仅为 planned stable identity。planned row 不带 package/interface/route/I/O，
  canonical `planned_skill_ids` 不改变 active inventory、selector 或 graph；E434 形成完整 package 并原子激活前，
  planned ID 无 canonical package tree、installed/platform projection 或 mandatory workflow edge。
- `R454-C6C7-08`：C7 只证明 Phase C 新 substrate 对 mappings、`worktree_path`、`source_checkout`、legacy session
  path 字段零读写；production predecessor 和其 readers/writers 保留到 E434 原子替换。不引入 dual-read/write、
  长期 alias、第二套 ownership/session store 或同义 checkout locator。
- `R454-C6C7-09`：C6/C7 focused validation 及 structural/inventory/ownership/sidecar/drift/line-limit/secret checks
  分别形成真实结果。代表性 clean throwaway 只在 accepted scope 要求时运行，不证明 planned package 已安装；
  完整多平台 Release matrix 留给 #410。完成 Docs candidate 不等于 runtime、Phase 2 或 production validation pass。

这些要求已进入 `.64` 的非激活 current acceptance；完整 E434 package、status mutation、production graph 和
Release matrix 仍需各自 owner 的后续实现与验证。
