# #122 第二轮问题闭环审查报告

## 身份与边界

- 逻辑角色：`问题闭环审查代理`。
- 技术身份：`trellis_final_review_122_01`。
- 复用决策：`reuse_decision: reuse-for-closure`。
- Reviewed HEAD：`03e813c5af37dec98c2c77114bc877c774256074`。
- Parent：`afcab19397a6ebc7cbd571722ba01950b670e620`。
- 审查范围：只复核 Round 1 raw report 的三个 finding；不执行最终放行审查。
- 操作边界：未修改实现、durable docs、规划、Phase 2 evidence、Round 1 raw report 或 review rollup；未运行 recorder/gate validator，未 commit、push、创建 PR 或执行 finish-work。

## 输入与范围

- Round 1 finding 来源：`reviews/round-001-final-release.md`。
- Finding-fix commit：`03e813c5`，31 个 committed paths。
- Commit evidence：提交中的 `task-commit-plans/002.json` planned bytes、working-tree committed result、raw commit object 与实际 path/tree。
- Fresh Phase 2：`phase2-check-report-round-001-fix.md`、`phase2-findings-round-001-fix.json`、`phase2-check.json`。
- 实现：canonical/dogfood runtime、canonical/installed/shared/Claude/Codex/Cursor package、public schema、contract 与 tests。
- Durable SSOT：`.trellis/spec/workflow/companion-scripts.md`、`.trellis/spec/workflow/data-contracts.md`。
- 闭环外 task metadata 保持未提交，不计入 commit 002 的 finding-fix implementation path set。

## 提交 002 证据

- Sequence：`002`；pre-commit HEAD 为 `afcab19397a6ebc7cbd571722ba01950b670e620`。
- Actual commit/working result SHA：`03e813c5af37dec98c2c77114bc877c774256074`。
- Raw message SHA-256：planned、result 与 commit object 均为 `9e37f6fd54b34d026a3d2e8a948b38053ac238dd8c6629a85a85e17f974e70fc`。
- Exact stage、result committed paths 与 actual diff 均为 31 paths，集合相等。
- Plan 对 40 个 dirty paths 分类：31 个 `task-reviewed`（含 candidate self），10 个 `unrelated-preserved`；result 记录 `unrelated_preserved=true`。
- Expected/actual tree 均为 `3ee42799b9b33a78f3276624a598149d7da582c3`；31 个 path 的 blob/mode evidence 全部 `matches=true`，`hook_mutation=false`。
- 当前真实 committed result 通过 `task_commit_result_validation_errors()`，返回空 errors。

## 三项问题闭环

### F-01（P1）同路径 hook 内容与模式变更

结论：已关闭。

- Runtime 在 exact staging 后、hook 前执行 `git write-tree`，绑定完整 expected tree。
- 每个 exact path 使用 tree identity 记录 expected/actual blob 与 mode；post-commit 要求完整 tree 与逐路径 evidence 一致。
- 同路径 content+restage 与 mode+restage 均产生真实 commit 后被标记 `blocked`，记录 `hook_mutation=true` 和 mismatch evidence，不误报 `committed`。
- Benign exit-0 hook 正常 `committed`；exit-1 且没有 index/worktree/unrelated mutation 的 hook 记录 `failure_stage=commit`、`head_changed=false`、`tree_evidence.matches=true`、`hook_mutation=false`，不会把计划内 staged path 本身误报为 mutation。

### F-02（P2）字面量精确索引与树身份

结论：已关闭。

- `task_commit_index_identity()` 和 `task_commit_tree_path_identity()` 均使用 `git --literal-pathspecs`、`-z`、exact decoded path comparison。
- Index 查询只接受 0 或 1 条 record，并要求 stage 为 `0`；多 record、非 exact record、unmerged stage 直接 `WorkflowError` fail closed。
- Literal `src/[0]*.txt` 与 decoy `src/0foo.txt` 并存时，tracked/staged/delete identity 均返回 literal path blob，不再取 decoy。
- 真实 merge conflict 的 metacharacter path 产生多 stage records，定向测试确认 fail closed。

### F-03（P2）封闭四状态结果 schema 与后置条件

结论：未关闭。

已完成部分：

- `result` 已由 closed `oneOf` 承载 planned/revision-required/blocked/committed 四态；status/exit 基本配对和 additional properties 已收紧。
- 正常 committed result 要求 parent/message/path/tree evidence；真实 plan 002 result 通过 schema/runtime。
- Committed tree tamper 会同时被 public schema 与 runtime 拒绝。

仍开放缺口：

- `blockedResult.allOf` 在 `failure_stage=pre-commit` 时只强制 `hook_mutation=false`，未要求 `tree_evidence=null`。构造 `tree_evidence.matches=false`、`hook_mutation=false` 的 pre-commit blocked result，public schema 与 runtime 均返回 `errors=[]`。
- `failure_stage=commit` 或 `postcondition` 时允许 `tree_evidence=null`；同时允许 `head_changed=false`、空 commit/message/path evidence。两种构造也被 schema/runtime 接受。
- Runtime `task_commit_result_validation_errors()` 在 `10160-10177` 对 pre-commit 无条件把 expected hook mutation 设为 false；对 commit/postcondition 的 `tree_evidence=null` 计算为无 mutation，没有校验 failure stage 与 tree/head/commit evidence 的可达关系。

该缺口直接不满足本轮明确要求的“tree mismatch/hook false 被 schema/runtime 拒绝”，也不满足 durable SSOT 的“每个 blocked branch 记录可审计 tree/hook facts，并在写入前拒绝跨字段矛盾”。

## 新发现

### C-01（P2）blocked 失败阶段条件不完整，矛盾树与 HEAD 证据仍可通过 schema

- 文件：`trellis/skills/guru-team/packages/guru-create-task-commit/schemas/task-commit-plan.schema.json:185`。
- Runtime：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:10160`。
- 复现 1：`failure_stage=pre-commit` + mismatched tree + `hook_mutation=false` -> schema/runtime errors 均为空。
- 复现 2：`failure_stage=commit` 或 `postcondition` + `tree_evidence=null` + `head_changed=false` -> schema/runtime errors 均为空。
- 影响：tampered/伪造 blocked evidence 可隐藏 tree mutation或声称不可达的 postcondition 状态，公共 artifact 不能按 F-03 要求 fail closed。
- 修复要求：按 failure stage 收紧 closed schema 与 runtime reachability：pre-commit 必须没有 expected tree 时 `tree_evidence=null`；commit 必须包含 index-source tree evidence并与 head 未变/commit evidence为空的事实一致；postcondition 必须 head changed、commit/parent/message/path evidence完整且 tree source 为 commit。任何 tree mismatch 必须与 `hook_mutation=true` 一致。补齐三阶段 cross-product negative matrix。

## 命令与结果

| 命令/检查 | 结果 |
| --- | --- |
| `TaskCommitCandidateExecutorTest` | 17 tests，7.167s，`OK`。 |
| canonical package standalone | 4 tests，0.100s，`OK`。 |
| 五个关键 named tests | failing hook no mutation、content mutation、mode mutation、literal decoy、unmerged literal 全部 `OK`。 |
| Canonical/dogfood/platform byte comparison | 6 个 package roots 各 8 files 一致；canonical/dogfood runtime 一致。 |
| `py_compile`、schema JSON parse、commit 002 `git diff --check` | 全部通过。 |
| Fresh Phase 2 full suite evidence | 495/495、clean throwaway、update/reapply、drift、source/installed validation 均记录通过；闭环代理未重复运行 recorder/validator。 |
| 真实 plan 002 result validation | `errors=[]`。 |
| Committed tree tamper | schema oneOf 与 runtime cross-field validation 均拒绝。 |
| Pre-commit mismatched tree/hook false tamper | 错误地接受，`errors=[]`。 |
| Commit/postcondition null-tree tamper | 错误地接受，`errors=[]`。 |

## 文档 SSOT、安全与部署

- Docs strategy 仍为 `ssot_first`；package contract、companion script spec 与 data contract 已描述 expected/actual tree、literal path、blocked evidence 和 cross-field rejection。
- F-01/F-02 runtime 与 docs 一致；C-01 表明 F-03 schema/runtime 尚未完全承接 data contract 的“每个 blocked branch”与“拒绝跨字段矛盾”。
- Finding-fix commit 未修改 GitHub Actions、Dockerfile/Compose、Kubernetes/Kustomize、Helm、migration、Makefile、应用 service、worker、queue 或 runtime config；无需应用部署或数据迁移。
- 公共 finding-fix diff 未发现 secret、客户数据、`.env` 内容、签名 URL、本机绝对路径或 workspace journal。
- Executor 仍不 push、不 amend/rebase/reset/force/stash；message temp file 权限和清理边界未退化。

## 观察项

1. Remote exact feature-ref marketplace verification 仍按合同等待 reviewed content push；这是 publish gate 的 pending evidence，不是本轮 closure finding。
2. 现有 package negative matrix覆盖 commit-stage mismatched tree/hook false，但没有覆盖 pre-commit mismatch 或 commit/postcondition null tree，因此测试通过不能关闭 C-01。

## 后续候选

无。C-01 属于 Round 1 F-03 的当前 post-result schema/runtime closure 范围，不能移出本 issue。

## 结论

- Round 1 F-01：closed。
- Round 1 F-02：closed。
- Round 1 F-03：open。
- `findings_count: 1`（P2=1）。
- 结论：`blocked`。
- 本报告只代表问题闭环审查，不代表最终放行；当前也不能作为 closure pass evidence。
- 下一步必须修复 C-01、完成 fresh Phase 2 与新的 task work commit，再由同一 finding owner 复核该 finding；全部 finding 关闭后仍需全新最终放行代理。
