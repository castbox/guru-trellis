# ADR-011: Active-task continuation authority

状态：`draft`，尚未 accepted、promoted 或 current。来源：Issue #419
`2026-09-17-r6` 与 task-isolated
[Architecture contribution](../contributions/419-active-task-continuation.md)。
Expected current 为 `current-main-0.6.17-guru.53`；任何 successor 只能由现有
Architecture promotion owner 在 independent committed review 后建立。

## Context

`task.json.status=planning|in_progress` 只表达 coarse lifecycle，无法识别 Phase 1
内部 owner，也无法区分 Phase 2、Task Commit、Branch Review 与 Publication 的相邻边界。
Public DTO 是 call-local handoff，成功 checkpoint 可能在消费后退休。新会话若根据 status、
clean Git、commit message、旧摘要或缺失 checkpoint 推断 pass，会形成第二 lifecycle
authority，并可能重复 mutation 或跳过 semantic owner。

上游 Trellis 已提供结构化 `[trellis-continuation]` 协议、确定性提取与 workflow-neutral
start/continue loading。Guru Team 只需要定义自己的 active-task semantics；preset 不应取得
上游入口、hook、平台投影或 meta ownership。

## Proposed Decision

1. Guru marketplace workflow 的唯一非空 `[trellis-continuation]` 区块独占 detailed
   active-task continuation。Phase Index、workflow-state、hooks 与平台 entries 只提供 facts
   和 broad breadcrumbs。
2. Current adjacent public DTO 直接进入 Interface 声明的唯一 consumer。DTO 丢失时，
   deterministic mutation/output loss 回原 producer 的正式 recovery/rematerialization；
   semantic result fresh 重跑原 owner。
3. Phase 1 activation 采用 workflow-owned `initial|recovery`。`initial` 只执行一次 official
   status transition；`recovery` 只在 exact task pair 已 current 且已 `in_progress` 时返回同一
   success，不重复 mutation。
4. Phase 2 output loss 只通过既有 checker -> `invoke-guru-check-task` 重投影 current retained
   `passed` checkpoint，不新增 public recovery profile、schema 或 exit。Task Commit 复用现有
   same-candidate `recovery_resume`。
5. Branch Review 和 Publication output 丢失时 fresh 重跑，因为其成功 checkpoint 正常退休。
   continuation 只恢复到现有 Finalizer 入口。
6. “确认继续”只授权当前对话中唯一、完整、仍 current 的已展示副作用。正式成功 typed exit
   自动消费 mapped transitions；新的副作用、真实选择或 stop 再暂停。授权不持久化。
7. Upstream Trellis 继续独占 extractor、start/continue、hooks、generated platform entries 与
   `trellis-meta`。Guru preset reapply 不修改 upstream bytes 或 active workflow。

## Rejected Alternatives

- 从 status/artifact/commit message 建立 global resolver：会复制 semantic route authority。
- 新增长期 continuation state store 或跨 Skill digest chain：没有唯一直接 consumer，并会阻止
  checkpoint 正常退休。
- 为 Phase 2 新增 public recovery profile：既有 checker-to-invoker 已可在 current checkpoint
  上重物化，新增 profile 会制造第二 API。
- 从 Git shape 重建 `committed`、Branch Review `passed` 或 Publication `ready`：不能证明原
  semantic judgment 或 exact producer transaction。
- 通过 Guru overlay patch start/continue/hooks/meta：违反 upstream ownership，并在 update/reapply
  后产生漂移。

## Consequences And Adoption Gate

该候选保持现有 Skill/exit owner、Phase 2 checkpoint、Task Commit candidate 和 Finalizer
边界；新增的是 workflow continuation semantics 与 producer-owned activation recovery。
旧对话确认、旧 semantic pass 和已退休 checkpoint 不可复用，跨会话可能需要 fresh review，
这是保持 authority 正确性的预期代价。

采纳必须绑定 upstream candidate
`43fffc170927c85d9f7fc106cc5a059e80d4530b`，ordered parents
`db4ca1dfbb5abaf9be62b2a01b70dda3f80df0f0`,
`df12903220ce22b2c84782968ed5c93406b5738b`，tree
`02fc0922f535200f67de7f6ba7920e3c763d7e95`，并通过 clean install、existing update、
native/Guru 双向 switch、preset reapply、ownership/parity、零 sidecar 与零 bytecode residue
证明。本文不声明这些 gate 已通过。

只有 independent committed full-diff review 与 expected-current-bound serialized promotion
完成后，本 ADR 才能改为 `accepted`。普通 task、本文创建或文件存在本身都不构成接受。
