# Issue #118 standalone not-required remote/ref 绑定修复交接

## 1. 身份与结论

- Agent：`/root/issue118_ref_binding_fix`，fresh Trellis implementation agent。
- Task：`.trellis/tasks/07-26-118-guru-finalize-task`。
- Worktree：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/118-guru-finalize-task`。
- Branch：`feat/118-guru-finalize-task`。
- HEAD：`925007cb6f9b8101360db8fb93f92ef6b35a5b77` 加当前未提交 finding-fix delta。
- Finding：只处理 `P2-R6-STANDALONE-REF-BINDING-01`。
- 结论：implementation fix 与 required normal-path regressions 已完成；未发现本轮 blocker。
- 本 agent 未调用 Phase 2 recorder/checker，未执行 commit、push、PR、archive、Issue mutation、deploy 或 production write。

## 2. 实现

Finalizer-private checker 现在要求 task-bearing standalone #117 `not_required`
owner evidence 同时满足：

- `repository.remote == plan.git.remote`；
- `repository.ref == refs/heads/{plan.git.head_branch}`；
- 原有 task、normalized repo、reviewed/remote HEAD、marketplace required=false、
  verification ref 与 same-plan identity 继续成立。

该绑定同时位于：

- augmentation checker `check_extension_verification_for_finalization_augmentation`；
- downstream currentness helper
  `finalization_standalone_not_required_owner_is_current`。

原有 live currentness 行为未删除或绕过：非 eval staging 仍以 evidence 自己声明的
`remote/ref` 执行 `git ls-remote` 并要求 live resolved HEAD 等于 evidence
`remote_head`。新增 private-plan identity check 不把 SHA 相同视为 remote/ref provenance
相同。

Production eval 的 private `finalization-context.json` 增加 `remote` 与
`head_branch`，用于构造 synthetic immutable private plan。它们不进入 native public
request、Skill public input/output、schema、Interface 或跨 Skill DTO。

## 3. 本 agent 精确 changed paths

1. `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
2. `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
3. `trellis/skills/guru-team/adapters/eval/native_adapter.py`
4. `.trellis/guru-team/scripts/python/guru_team_trellis.py`
5. `.trellis/guru-team/skills/adapters/eval/native_adapter.py`
6. `.trellis/tasks/07-26-118-guru-finalize-task/implementation-handoff-ref-binding-fix.md`

除此之外未修改 package、public schema、Interface、durable docs、global workflow、
upstream Finish family、official `task.py`、preset overlay 或 main-owned task metadata。

## 4. Regression 结果

Focused runtime：

- exact `origin` + `refs/heads/main` + matching live HEAD：accepted；
- same task/repo/HEAD，`remote=secondary`：rejected；
- same task/repo/HEAD，`ref=refs/heads/other`：rejected；
- focused 2 tests：passed，exit 0；
- eval-context focused test：passed，exit 0。

Full suites：

- Runtime：617 passed，13 skipped，exit 0；
- Skill package / production eval：179 passed，exit 0；
- Preset installer：45 passed，exit 0；
- `git diff --check 925007cb...`：passed。

真实 two-wrapper production eval：

- Shared source `not-required-reentry-published`：passed，actual exit=`published`；
- Shared installed 同一 case：passed，actual exit=`published`；
- transcript 证明执行 installed #117 public wrapper，应用 declared
  `project_not_required` projection 与 no-overwrite authoring merge，再执行 #118 public
  wrapper；不是直接注入 finalizer verification facts。

## 5. Public/private boundary 证明

- #118 Interface SHA-256 保持
  `3cc7291ba7fe6f3f425134fc4f452546f04caff238f1f61c27a0352b5d1949a8`。
- #117 Interface SHA-256 保持
  `768d1dd1ecba21fe1f23406d33c8732049517d27ebb413c56bb9e389212b64f7`。
- #117 public `not_required` output 未新增 remote/ref/plan 字段。
- #118 public standalone input 仍只由 producer seed
  `repo_ref/resolved_head/verification_ref` 与 target authoring
  `profile/mode/task_ref` 组成。
- `remote/ref/head_branch` 只存在于 #117 private owner evidence、immutable private plan
  与 eval private staging context；public request 和 typed exit DTO 不携带这些 facts。
- Runtime canonical/installed bytes 相同，SHA-256：
  `3d9211630c33ce4cfda0bad57e8fb22dcdd4defe5f2e53f02cc34350855f0f6e`。
- Eval adapter canonical/installed bytes 相同，SHA-256：
  `834f07870bed612de06be6af243f7866a7cda4023a1655dd46200007a6418a02`。

## 6. Sync、drift 与 hygiene

- 首次 all-platform preset apply 只为本轮两个 managed target 生成 `.bak`。
- 逐个比对确认 backup 与 canonical 的唯一内容差异就是本轮 runtime/adapter
  delta，无用户独有内容；删除这两个可重建 sidecar。
- 第二次幂等 reapply：exit 0，`updated_managed=0`、`managed_backups=0`、
  `sidecars=[]`。
- Source/installed package validators：passed；installed inventory 为 2659 managed
  files、0 sidecar、0 removal、0 conflict。
- Dogfood overlay drift：passed。
- Global workflow、upstream Finish family、official `task.py`、preset overlays：本轮
  no-diff。
- Round 6 #117 contract 机械修复六份 byte-identical，SHA-256：
  `223ab8ae598c7c37be230806f9576fa91a0292d37ef08ec8c13b8e7625d8af66`。
- Issue worktree 与 source checkout `__pycache__`、`.pyc`、`.pyo`：0。
- Issue worktree `.new` / `.bak`：0。
- 本轮 `/tmp/guru118-ref-binding-eval.VYVz63` 已删除。
- Source checkout clean，HEAD=
  `7820a9eeec2a2a75fb52fba156a7211d9f9fb09c`。

## 7. 边界与未重跑项

- 保持 #117 public DTO 与 general checker，不新增 public profile/schema 字段。
- 保持 #118 same-plan recovery 与 owner-private plan/readiness/verification/PR/archive
  facts。
- 保持 #105 transaction semantics；未承接 #119/#132/global Finish integration。
- 未引入 hostile actor、forgery、concurrency、lock、TOCTOU、fault injection、crash
  consistency 或 cross-OS mechanism/test。
- 未重跑 Claude native：本轮未改变 Claude protocol/adapter，Round 6 的 invalid API key
  仅作为外部环境上下文，不计为本 agent 的通过证据。
- 未重跑 full throwaway：本轮未改 installer、workflow marketplace、platform package
  corpus 或 overlays；以 full preset suite、all-platform apply、source/installed
  validators、canonical/installed identity 与 drift gate 覆盖该 narrow fix。

下一步应由 fresh Phase 2 checker 对完整 effective diff 重新执行语义检查；本报告不替代
Phase 2 pass、finding closure、Branch Review 或 publication review。
