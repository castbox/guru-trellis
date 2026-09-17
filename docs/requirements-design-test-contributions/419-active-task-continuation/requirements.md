# #419 Active-task continuation Requirements contribution

状态：`task_isolated_candidate`，未 review/promote，不是 shared current。本文继承 active
`current-main-0.6.17-guru.53` Requirements authority，只记录 Issue #419
`2026-09-17-r7` 的 task-local delta；不得覆盖或改写 `.53`。

- `R419-01`：Guru canonical workflow 必须且只能包含一个非空
  `[trellis-continuation]` 区块，完整分发 `planning`、`planning-inline`、
  `in_progress`、`in_progress-inline`、`completed` 与 invalid task state。Phase Index、
  workflow-state、hooks、entries 和 task status 不得保留第二张 detailed route table。
- `R419-02`：Phase 1 continuation 必须保持 task-created attachment、planning author、wording、
  Planning Architecture、Approval、plan presentation/confirmation 与 activation 的原 owner。
  Activation 必须区分 `initial|recovery`；两种模式都必须在任何 mutation 前绑定 exact current
  task/worktree/branch/mapping/status，`initial` 只执行一次 transition，已成功 transition 使用
  `recovery` 零重复 mutation。
- `R419-03`：current adjacent public DTO 必须直接交给唯一 consumer。DTO 丢失时，
  deterministic output loss 只由原 producer 正式恢复；semantic output 必须 fresh 重跑原 owner。
  Status、Git shape、旧摘要、旧确认或 checkpoint 缺失不得重建 pass。
- `R419-04`：Phase 2 只能通过既有 checker -> public invoker 重投影 current retained
  `passed` checkpoint，不新增 public recovery profile。Task Commit 只能复用现有 same-candidate
  `recovery_resume`，不得重复 candidate/commit、创建空 commit 或 amend。Branch Review 与
  Publication output 丢失时分别 fresh 重跑。
- `R419-05`：SessionStart、UserPromptSubmit、显式 start/continue、自然语言“继续”与无 pending
  plan 时的“确认继续”，在 exact active task 上必须加载同一 continuation。存在 current side-effect
  plan 时，确认只授权该计划；成功 typed exit 自动续接到新副作用、真实选择或 stop。确认不持久化。
- `R419-06`：upstream extractor/start/continue/hooks/platform/meta 保持 upstream-owned；Guru preset
  不安装、patch、删除或 managed-upgrade 这些路径或 active workflow。选择 Guru
  workflow 但 preset 缺失时必须明确阻塞依赖不完整。
- `R419-07`：定向集成证据必须绑定 immutable candidate
  `43fffc170927c85d9f7fc106cc5a059e80d4530b`、ordered parents
  `db4ca1dfbb5abaf9be62b2a01b70dda3f80df0f0` /
  `df12903220ce22b2c84782968ed5c93406b5738b` 与 tree
  `02fc0922f535200f67de7f6ba7920e3c763d7e95`，覆盖 upstream extractor、continuation mode、
  workflow-neutral start/continue、Guru continuation 与 producer-owned recovery；使用 source/installed
  runtime、eval 和真实 Git/task fixture，并验证 Guru-owned projection parity、upstream ownership、dogfood
  drift、当前工作树 sidecar/residue hygiene 与 `git diff --check`。
- `R419-08`：本任务已批准的 ledger subtraction 必须由 task-local successor delta 明确删除 current
  `guru-ledger-free-runtime@1.0.0` capability/compatibility 声明。Promotion 后的 current successor 不得继承
  `.53` 的 `ARCH-CUR-027` capability、`R247-10`、matching non-functional projection requirement 或
  `RDEC-024` current claim；immutable `.53`、accepted ADR 与 archive/release evidence 仅保留历史事实，
  不得形成 exemption、alias、adapter、fallback、dual-read 或兼容层。

本 contribution 不实现 Phase 0 exact identity 建立前恢复、#398 全 lifecycle、Finalizer transaction、
Merge、archived recovery 或 #410 Release Gate。安装、更新、workflow switch 与 preset reapply 的发布证据
由 #410 在 #419 合并后的 fresh Guru release candidate 上独立建立，不得复用 #419 的部分结果。任何
shared-current successor 必须由 RDT owner 在 independent review 后 serialized promotion，并对
promotion-created diff fresh 重跑下游 gates。
