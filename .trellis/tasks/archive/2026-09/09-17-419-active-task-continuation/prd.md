# #419 Guru active task continuation 恢复合同

合同版本：`2026-09-17-r7`。本任务处于 `in_progress`；实现、验证、提交与发布状态以当前 live task、Git 与 runtime gate 为准，不在本文持久化。

## 1. 目标与权威

修复 Guru Team active task 在中断、上下文压缩或新会话后的粗粒度错误路由，使当前 AI 只从当前 workflow 的唯一 continuation 合同进入合法 owner，并在 public DTO 丢失时回原 producer 恢复或 fresh 重算。

需求权威：[`castbox/guru-trellis#419`](https://github.com/castbox/guru-trellis/issues/419)，状态 `OPEN`，正文合同 `2026-09-17-r7`。

直接上游依赖：`castbox/Trellis#6` 合同 `2026-09-17-r3` 已关闭，PR #7 已合并。唯一可接受的本任务集成候选为：

```text
43fffc170927c85d9f7fc106cc5a059e80d4530b
```

该 merge commit 的 parents 为 `db4ca1dfbb5abaf9be62b2a01b70dda3f80df0f0` 与 `df12903220ce22b2c84782968ed5c93406b5738b`，tree 为 `02fc0922f535200f67de7f6ba7920e3c763d7e95`。本任务不得复用旧 candidate、旧测试证据、旧 planning 结论或旧 continuation 假设。

## 2. 已核实事实

- 当前任务 identity 为 `.trellis/tasks/09-17-419-active-task-continuation`，branch 为 `codex/419-active-task-continuation`，worktree 为本任务 worktree，status 为 `in_progress`。
- 当前任务基线 HEAD 为 `f5ebf9f92b0f174b48f6c8ed04038eb32a5f054e`；worktree 包含本任务实现、测试、文档、task artifact 与同步后的安装投影改动。
- 上游 candidate 已重新 fetch，并验证为 `upstream/main` 可达的 PR #7 merge commit；不能用 PR head 或其他 revision 代替。
- 上游 candidate 已提供结构化 `[trellis-continuation]` 提取、`get_context.py --mode continuation`、workflow-neutral `trellis-start` / `trellis-continue` 与 native continuation 定向回归。
- Guru canonical workflow 已增加唯一 `[trellis-continuation]` 区块；Phase Index 与 `[workflow-state:*]` 仅保留 broad breadcrumb。
- 当前 `guru-create-task-commit` 已通过 package-owned candidate/receipt 支持同一 commit 的 stdout-loss recovery；不得另建全局 commit resolver。
- 当前 `guru-check-task` 的 `passed` checkpoint 只服务 Task Commit，并由 Task Commit 成功消费后退休；缺失时不得从 Git 或旧文本重建 pass。
- Guru preset 的 ownership contract 明确禁止安装、patch、删除或 managed-upgrade upstream-owned `trellis-*` entries、hooks、agents 与 `trellis-meta`。

## 3. 必须实现的行为

### R419-01 唯一 continuation authority

Guru canonical workflow 必须包含且仅包含一个非空 `[trellis-continuation]` 区块。该区块完整分发：

- `planning` 与 `planning-inline`：同一 Phase 1 recovery matrix；
- `in_progress` 与 `in_progress-inline`：同一 Phase 2 至 Finalizer 前 recovery matrix；
- `completed`：进入 canonical `guru-finish-work`；
- invalid identity 或 invalid task state：停止在 `invalid-task-state`。

Phase Index 与 active-task breadcrumbs 只能提供 broad lifecycle guidance，不得复制第二份具体 route table。

### R419-02 Phase 1 recovery

Continuation 必须覆盖：task-created attach 丢失、三份 planning 文件尚未全部完成、planning wording stale、Planning Architecture stale、`guru-approve-task-plan` output 丢失、plan presentation 后 dialogue-local confirmation 丢失、activation 尚未完成，以及 activation mutation 成功但 output 丢失。

恢复必须保持原 owner：补齐规划回 planning author；wording、Architecture、Approval fresh 重跑；旧确认重新取得；activation output-loss 由 activation owner读取 current task state重新物化成功结果，不重复 activation。

### R419-03 Phase 2 至 Finalizer 前 recovery

- 相邻调用仍持有 current public DTO 时，直接交给唯一 consumer。
- DTO 丢失时，确定性 mutation/output-loss 由原 producer 的正式 recovery/rematerialization 恢复；semantic result 必须 fresh 重跑原 owner。
- Phase 2 缺失/stale 回 fresh Architecture + `guru-check-task`。
- Task Commit mutation/output-loss 只走现有 `guru-create-task-commit` recovery，不创建重复/空/amend commit。
- Branch Review DTO 丢失或 checkpoint 已退休时，对当前完整 committed range fresh 重跑 Architecture Branch Review 与 `guru-review-branch`。
- Publication DTO 丢失或 checkpoint 已退休时，fresh 重跑 Publication Architecture 与 `guru-review-task-publication`。
- 本任务只恢复到现有 `guru-finalize-task` 正式入口，不进入 archived/Merge/Finalizer transaction recovery。

### R419-04 自然语言与确认语义

SessionStart、UserPromptSubmit、显式 `trellis-start`、显式 `trellis-continue`、自然语言“继续”与无待确认计划时的“确认继续”，在 exact active task 上必须加载同一 continuation 区块。

当前对话存在唯一、完整且 current 的副作用计划时，“确认继续”只授权该计划。原 executor 成功后返回正式 typed exit，workflow 自动消费 mapped transitions，直到新的独立副作用、真实选择或 fail-closed stop。失败不得生成成功 exit。确认信息只存在于当前对话，不得持久化。

### R419-05 ownership 与分发

- 只修改 Guru-owned workflow、Guru Skill packages/runtime/tests、Guru specs/docs、preset validator/tests 与 Guru-owned projections。
- 不修改或新增 upstream-owned start/continue/hooks/platform entries/`trellis-meta` overlay。
- 如现有 producer 缺少正常 output-loss recovery，只在该 producer 内增加最小 recovery profile/command/schema；不得建立 global lifecycle state store、semantic resolver 或第二 authority。
- Canonical 修改后必须通过 preset apply 同步 dogfood 与选择的平台 Guru-owned copies。

### R419-06 exact-upstream 定向验证与发布边界

必须绑定 exact upstream candidate `43fffc170927c85d9f7fc106cc5a059e80d4530b`，但 #419 只执行 continuation 缺陷直接需要的定向验证：

1. candidate commit、tree、ordered parents 与 source lock identity 精确匹配；
2. upstream continuation extractor、`get_context.py --mode continuation`、`trellis-start` 与 `trellis-continue` 薄入口合同通过；
3. Guru continuation、adjacent DTO consumption 与 producer-owned recovery 通过 current package/runtime/eval 和真实 Git/task fixture 验证；
4. current source、installed、dogfood 与声明平台 Guru-owned projection 一致；
5. upstream ownership、dogfood drift、当前工作树 `.new` / `.bak` 与 bytecode residue hygiene、`git diff --check` 通过；
6. 不修改 upstream-owned start/continue/hooks/platform/`trellis-meta`。

#419 不执行或要求 throwaway、clean install、existing-install update、固定 predecessor、多平台 workflow-switch 或 release-grade preset-reapply matrix。完整发布兼容性验证由 #410 独占；#410 必须在 #419 合并后的最新 `main` 上重新冻结 Guru release candidate，并独立执行其 live Release Gate，不能复用 #419 中任何已开始、失败、中断或未完整完成的结果。

## 4. 验收标准

- [ ] Guru workflow 唯一非空 continuation 区块覆盖六类 state 与 invalid stop。
- [ ] task-created、partial planning、wording、Planning Architecture、Approval、confirmation 与 activation output-loss 均由原 owner 合法恢复。
- [ ] Phase 2、Task Commit、Branch Review、Publication 的 adjacent DTO 与 lost DTO 路径被明确区分。
- [ ] 不从 task status、Git、文件存在、旧摘要、旧 checkpoint 缺失或旧确认推断 semantic pass。
- [ ] Task Commit output-loss 不产生第二 commit、空 commit、amend 或同内容 commit。
- [ ] 自然语言与显式入口在 exact active task 上收敛到同一 current owner；无 exact task 时不从 project inventory 选择。
- [ ] 当前副作用确认只授权展示计划，成功 typed exit 自动继续，新的副作用/选择/stop 再暂停。
- [ ] Exact candidate 的 extractor、`trellis-start` 与 `trellis-continue` 定向合同测试通过。
- [ ] Guru continuation 与 owner-preserving recovery 通过 current source/installed runtime、eval 和真实 Git/task fixture 验证。
- [ ] Source、installed、dogfood 和声明平台 Guru-owned projection 一致。
- [ ] Upstream ownership、dogfood drift、当前工作树 sidecar/residue hygiene 与 `git diff --check` 通过。
- [ ] 真实 canonical/installed workflow、真实 Git fixture 与正式 wrappers 覆盖 adjacent consumption 和 cross-session recovery；测试不预填 semantic pass、不手写 DTO、不用关键词断言代替行为。

## 5. 非目标

- 不实现 Phase 0 exact identity 建立前的恢复，也不从 project inventory 选 task。
- 不实现 #398 的完整 lifecycle graph、Acceptance、Completion、Closure、official Finish 或 migration API。
- 不修改 archived task、Finalizer transaction、Merge 或 #418 已拥有的 archived recovery。
- 不在 Guru 仓库 patch upstream-owned start/continue/hooks/platform/`trellis-meta`。
- 不增加长期 continuation checkpoint、全局 task-stage store、授权 artifact、锁、TOCTOU、攻击模型或对抗性测试。
- 不执行 throwaway、clean install、existing-install update、固定 predecessor、跨平台 workflow-switch 或 release-grade preset-reapply matrix；#410 在 #419 合并后重新冻结自己的 Guru release candidate，并从零生成 Release Gate evidence。

## 6. Open Questions

无。live Issue r7、上游 r3 candidate 与当前 repository authority 已关闭本任务的产品、scope 和定向验收选择；发布兼容性验证由 #410 独立拥有。
