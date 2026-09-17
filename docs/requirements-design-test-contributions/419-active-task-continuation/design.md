# #419 Active-task continuation Design contribution

状态：`task_isolated_candidate`；expected current 为
`current-main-0.6.17-guru.53`。本文只承接 R419 的 stable design delta，不成为第二份 current
Design，也不声明实现、测试、review、promotion 或 release 已完成。

- `D419-01`：采用 `target_native`。上游 Trellis 提供结构化 continuation protocol 与薄入口；Guru
  workflow 独占 Guru continuation body。Detailed routes 只存在于唯一 block，breadcrumbs 只提示加载。
- `D419-02`：continuation 以 exact current task identity 为前置，先区分 adjacent DTO 与 lost DTO。
  Adjacent 走 Interface projection；lost deterministic result 回 producer；lost semantic result fresh
  重跑。Unknown/multiple/stale/unsupported state 进入 declared owner/stop，不猜 route。
- `D419-03`：Phase 1 recovery 按 task-created attach -> partial planning -> wording -> Planning
  Architecture -> Approval -> plan presentation/confirmation -> activation 有序判断最早 current owner。
  Lost `created` output 只走 `guru-create-task-workspace:recover_created_result` 的 read-only checker；
  Activation wrapper 只拥有 `initial|recovery`；两者先验证 current task/worktree/branch/mapping/status，
  `initial` 才可调用一次 official start 并 post-check `in_progress`，`recovery` 直接重物化 success，
  不重复 official start，也不保存确认。
- `D419-04`：Phase 2 current retained `passed` checkpoint 使用现有 checker 和
  `invoke-guru-check-task` 重投影原 DTO；不增加 input profile/schema/exit/checkpoint。缺失或 stale
  时执行 fresh Architecture phase2 + semantic check。
- `D419-05`：Task Commit 使用既有 private candidate、transaction stage 与 `recovery_resume` 证明同一
  published commit。Branch Review/Publication checkpoint 正常退休，lost output 分别触发 fresh
  Architecture + semantic owner。Continuation 只恢复到 existing Finalizer entry。
- `D419-06`：dialogue-local confirmation 与 typed-exit auto-consumption 分离。Executor 必须验证实际
  success 后才能返回 exit；payload/target/authority 改变使旧确认失效；failure 不产生 success exit。
- `D419-07`：Guru preset 只分发 Guru packages/runtime/schema/projections。Marketplace workflow 负责
  continuation bytes；upstream entries 与 native continuation 由 exact upstream candidate 提供。
  Guru task diff 与 managed inventory 不取得这些路径 ownership。
- `D419-08`：真实回归使用 canonical/installed workflow、真实 Git/task/worktree fixtures 与正式 wrappers，
  分开覆盖 adjacent consumption 和 cross-session recovery。Semantic owner 必须真实运行，测试不得
  预填 pass、手写 DTO、保留 retired checkpoint 或用关键词断言替代行为。
- `D419-09`：exact upstream 定向验证先绑定 candidate full SHA、ordered parents 与 tree，再运行 extractor、
  continuation mode、start/continue contract tests。Guru 验证运行 source/installed package runtime、eval、
  正式 wrappers 与真实 Git/task fixture；最后检查 projection parity、ownership、dogfood drift、当前工作树
  sidecar/residue hygiene 与 `git diff --check`。
- `D419-10`：#410 独占发布安装、更新、workflow switch 与 preset reapply 的 Release Gate。它必须在 #419
  合并后的最新 `main` 上重新冻结 Guru release candidate，并从零产生证据，不消费 #419 的部分结果。
- `D419-11`：ledger 使用 direct subtraction。Architecture/RDT serialized promotion 从 current successor
  删除 `guru-ledger-free-runtime@1.0.0` capability 与 `.53` 中对应的 current compatibility claims；immutable
  `.53`、accepted ADR、archive/release evidence 保持 historical，不增加 exemption、alias、adapter、fallback、
  dual-read 或 compatibility path。

Architecture decision candidate 见
[`ADR-011`](../../architecture/adr/011-active-task-continuation-authority.md)，状态保持 `draft`。
Exact-upstream 定向验证必须绑定 candidate 的 full SHA、ordered parents 与 tree；当前 source lock、
release mapping 和 shared `.53` 不由本 contribution 改写。
