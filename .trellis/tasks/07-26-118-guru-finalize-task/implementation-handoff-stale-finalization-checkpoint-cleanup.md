# #118 stale finalization checkpoint cleanup handoff

## 结论

这是一个受支持 normal path 中的 task-work correctness 修复，不是新的 finalization
transition，也不改变 `guru-finalize-task` 的 runtime、public contract 或 durable Docs
SSOT。旧 `closeout-plan.json` 与 `task-finalization-gate.json` 占用了 active task 中由
finalizer 独占的 reserved checkpoint names，但它们绑定的是已经过期的 pre-commit
identity，无法合法承接 current publication entry。

本轮 task-work 因此删除这两个 tracked active checkpoints，释放 reserved names，让后续
finalization 在所有 task-work gates 重新通过后，以 current publication evidence 重新执行
side-effect-free preview、生成新的 immutable plan，并取得新的 exact digest confirmation。

## Live finding

当前 task-work HEAD 是：

`362f8cd62c62621e892b46e68763ae4323460871`

被删除的旧 plan/gate 则绑定：

- reviewed work HEAD：`d420a6842eca05bd0bf7472bdf06e3b519bace5f`
- closeout plan digest：
  `59ce5a04a6e9470d7d5e99ab76f8821af0b1ae8cc0448f0ded08b205021d88f6`
- old route：`verification_required`

对 current `publication_ready` input 执行真实 side-effect-free preview 时，runtime
fail closed：

`Persisted closeout plan does not own newly added task artifacts.`

Exact `unexpected_task_files` 为：

1. `implementation-handoff-live-wrapper-namespace-fix.md`
2. `phase2-check-live-wrapper-namespace-fix-exact-stream-full-round.md`
3. `phase2-check-live-wrapper-namespace-fix-full-round.md`
4. `phase2-command-evidence-live-wrapper-namespace-fix-exact-stream-full-round.json`
5. `phase2-command-evidence-live-wrapper-namespace-fix-full-round.json`
6. `reviews/round-016-final-release.md`
7. `task-commit-plans/008.json`

这些都是旧 plan 之后在正常 task workflow 中形成的 task-work evidence。旧 plan 的 immutable
projection 不能吸收它们；same-month recovery 也不能把一个已经拥有 finalizer gate 的旧
checkpoint 当作 legacy takeover 输入。因此继续保留旧 active checkpoint names 只会让
current preview 重复阻断。

## 为什么不能临时删除或绕过 #116

临时移走旧文件、preview 后再恢复，不是合法恢复路线：

- `guru-finalize-task` 的 publication entry 必须重新运行 #116
  `guru-review-task-publication` owner checker，并消费 current `ready` DTO；
- checkpoint 缺失不会替代、放宽或伪造 #116 的 task、reviewed HEAD 与 opaque
  `publication_ref` binding；
- 恢复旧 checkpoint 会重新引入 `d420a684...` identity；formal execution 重建的 plan
  bytes/digest 将与 preview 或 current publication evidence 不一致，并在任何副作用前
  fail closed；
- 因此 reserved names 必须作为当前 task-work 的 tracked cleanup 被正式移除，随后完整
  重跑 task-work 与 publication gates，而不是对 finalizer runtime state 做临时文件操作。

## 历史与 Docs SSOT

旧 checkpoint 的 exact bytes 已由 Git commit
`362f8cd62c62621e892b46e68763ae4323460871` 保存。删除 active copies 不抹除历史证据，
也不需要把 private checkpoint body 复制到新的公共 DTO、runtime cache 或 durable docs。

本 remediation 的 Docs SSOT strategy 是 `no_docs_update_needed`：

- durable finalizer contract 对 immutable plan、owner-private state、#116 owner checker、
  same-plan recovery 与 fail-closed preview 的语义无需修改；
- 不修改 runtime、schemas、examples、tests、workflow、preset、overlay、README 或平台分发；
- 本文件只记录当前 task 的 implementation handoff 与 recovery provenance。

## Scope boundary

- 只关闭 #118。
- #115 保持 umbrella/related，不在本 task 关闭。
- #119 继续拥有 Finish family workflow/platform integration、combined acceptance 与 #115
  closure。
- #132 继续拥有 upstream overlay cleanup。
- 不改变、重新执行或重新关闭 #105 的 transaction semantics。

## Required follow-up gates

本 cleanup 不是发布授权。后续必须按完整顺序重新完成：

1. Phase 2 全量 semantic check，覆盖本次 deletion/addition 与 current metadata tail。
2. 新 task commit，并对 exact commit plan/digest 取得 mandatory human confirmation。
3. 使用不同于实现者的独立 agent 执行完整 Branch Review，关闭全部 current-scope P0-P3
   findings。
4. 重新执行 publication review，取得绑定新 HEAD 的 #116 `ready` output。
5. 使用 current publication DTO 重新运行 side-effect-free finalization preview。
6. 展示新的 immutable closeout plan、exact digest、repo/Issue/HEAD 与全部外部副作用，并
   等待独立 mandatory human confirmation。
7. 只有该确认完成后，才能进入 content push、#117 verification routing、唯一 Draft PR、
   archive transaction、三方 HEAD equality、draft-to-ready 与只关闭 #118 的正式
   closeout。

在上述新 confirmation 前，禁止 push、PR 创建/更新、archive、Ready、merge 或 Issue
mutation。
