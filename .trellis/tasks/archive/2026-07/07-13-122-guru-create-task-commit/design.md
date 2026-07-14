# #122 技术设计

## 1. 设计目标

本设计把 task work commit 建模为一个可重复进入的 closed-loop skill。Markdown
package 负责 AI 判断，companion runtime 负责 objective validation 与 exact Git
side effect。实现必须复用 #120 分发基础设施和 #92 parser，不建立平行 SSOT。

## 2. SSOT 与 owner

| 层 | SSOT | Owner | 禁止行为 |
| --- | --- | --- | --- |
| Global workflow | `trellis/workflows/guru-team/workflow.md` | phase 顺序、mandatory invocation、typed-exit route | 复制 step-local 正文 |
| Canonical skill | `trellis/skills/guru-team/packages/guru-create-task-commit/` | entry、forward behavior、AI Gate、human policy、re-entry、exit | 携带 active task 状态 |
| Commit parser | `validate_commit_message()` | subject/body objective syntax | 判断 message 语义充分性 |
| Candidate validator | `check-commit-messages --candidate-artifact` | artifact/schema/evidence/snapshot/message objective facts | 判断 scope 分类是否正确 |
| Exact executor | `create-task-commit` | exact stage、commit、postcondition、result record | 生成业务语义或改写历史 |
| Preset installer | `trellis/presets/guru-team/` | managed-hash distribution、platform selection、provenance | 覆盖 unknown local edit |
| Dogfood copies | `.trellis/guru-team/skills/` 与 platform roots | runtime discovery | 反向成为 canonical source |

## 3. Public id migration

Production registry 同时保留两项：

1. `guru-create-work-commit` 保持 `reserved`，作为 compatibility tombstone；
   reason 指向 active `guru-create-task-commit`。
2. `guru-create-task-commit` 使用 `active` lifecycle，package path 为
   `packages/guru-create-task-commit`，route id 为 `phase-3-task-commit`。

旧 reserved id 从未安装、从未进入 production marker。保留 tombstone 能阻止未来把
旧 id 赋给另一种语义，同时不要求目标仓库迁移运行文件。

## 4. Canonical package

```text
trellis/skills/guru-team/packages/guru-create-task-commit/
├── SKILL.md
├── interface.json
├── references/
│   └── contract.md
├── schemas/
│   └── task-commit-plan.schema.json
├── examples/
│   └── task-commit-plan.json
├── scripts/
│   ├── check-task-commit-plan.sh
│   └── create-task-commit.sh
└── tests/
    └── test_contract.py
```

`SKILL.md` 只包含 trigger、必读文件、闭环顺序、命令入口、typed exits 与
fail-closed 提示。`references/contract.md` 承载 step-local 完整合同。Package scripts
是 thin wrappers，调用 installed companion runtime；不复制 parser 或 Git 状态机。

## 5. Interface 与 workflow route

Workflow/standalone mode 声明同一 precondition id 集合：

- `workspace_boundary`
- `task_identity`
- `planning_approval`
- `phase2_check`
- `issue_scope_ledger`
- `pre_commit_head`
- `dirty_snapshot`
- `commit_authorization`

Production workflow 使用一组 unfenced markers：

```markdown
<!-- guru-skill-invoke: {"skill":"guru-create-task-commit","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-create-task-commit","exit":"committed","consumer":{"kind":"workflow","id":"branch-review-or-finding-closure"}} -->
<!-- guru-skill-exit: {"skill":"guru-create-task-commit","exit":"revision-required","consumer":{"kind":"skill","id":"guru-create-task-commit"}} -->
<!-- guru-skill-exit: {"skill":"guru-create-task-commit","exit":"blocked","consumer":{"kind":"stop","id":"task-commit-blocked"}} -->
```

Phase 3.4 文本只声明调用时点、finding-fix repeat condition 与 exit routing。
Candidate、AI Gate、confirmation、executor、postcondition 全部由 package owner。

## 6. Runtime data flow

```text
Phase 2 passed evidence
  -> AI reads full Git/task evidence
  -> AI classifies every dirty path
  -> AI writes task-commit-plans/<sequence>.json
  -> AI Review Gate
  -> check-commit-messages --candidate-artifact
  -> conditional user confirmation or fail-closed re-entry
  -> create-task-commit exact executor
  -> raw commit/postcondition validation
  -> artifact result update
  -> exactly one typed exit
```

Branch Review finding 产生非 metadata task work 时，route 返回 implementation 与
Phase 2。新的 Phase 2 pass 产生新的 candidate sequence；旧 artifact 因 pre-commit
`HEAD`、Phase 2 digest 与 dirty snapshot 不匹配而无法执行。

## 7. `task-commit-plan` artifact

Schema id 使用
`https://github.com/castbox/guru-trellis/schemas/guru-task-commit-plan-1.0.json`。
Runtime artifact 位于 task directory 的 `task-commit-plans/<sequence>.json`，
`sequence` 是三位递增十进制编号。

顶层结构：

| 字段 | 合同 |
| --- | --- |
| `schema_version` | 固定 `1.0` |
| `skill_id` | 固定 `guru-create-task-commit` |
| `sequence` | 与文件名一致 |
| `task` | task id、repo-relative task dir、status、branch |
| `issue` | primary issue number 与 ledger digest |
| `git` | base branch/ref、pre-commit `HEAD` |
| `evidence` | planning approval、Phase 2 check、ledger、task.json 的 path/digest/size |
| `dirty_snapshot` | staged/unstaged/untracked/delete/rename facts、entry digests、snapshot digest |
| `path_classifications` | dirty path 全覆盖、唯一 category、AI reason |
| `exact_stage_paths` | `task-reviewed` path 加 candidate artifact path |
| `message` | subject、body、exact bytes、SHA-256 |
| `ai_review` | status、reviewer、summary、evidence |
| `authorization` | authorized flag、source、evidence |
| `freshness` | captured time、artifact plan digest |
| `result` | `planned` / `revision-required` / `blocked` / `committed` 与 postcondition facts |

Artifact 不存储 dirty file content。Tracked/untracked content identity 使用 Git object
id、SHA-256、delete marker、rename source/destination 与 mode facts。Candidate artifact
自身不进入 snapshot content digest；validator 通过 repo-relative self path 与 plan
digest 单独绑定，避免 self-hash recursion。`path_classifications` 必须覆盖 snapshot
中的 path 及 candidate self path；self path 使用固定 `skill-artifact` coverage source。

每次 artifact 在 commit 前以 `result.status=planned` 进入 exact stage paths。Commit
成功后 executor 把同一 working-tree artifact 更新为 `committed`；该 post-commit
task metadata delta 由后续 finding-fix work commit 或 finish-work metadata commit
收纳。Git history 保留提交时的 planned bytes，当前 task artifact 保留真实 result。

## 8. Dirty snapshot 与 Phase 2 binding

Companion runtime 使用 NUL-delimited Git commands 收集完整状态，path identity 使用
exact repo-relative bytes 解码后的字符串。Snapshot 必须保留 rename source、
destination 与 similarity facts；最终 committed path set comparison 使用
`--no-renames` 归一为 delete 加 add path set。实现必须覆盖 path 包含空格、Unicode
与 pathspec metacharacter 的测试。

Candidate validation 必须证明：

- `phase2-check.json.head == git.pre_commit_head`；
- `task-reviewed` path 被 Phase 2 `dirty_paths` 覆盖；
- Phase 2 checked artifact digests 仍匹配；
- planning docs 仍通过 `check-planning-approval`；
- ledger primary issue 与 candidate message refs 一致；
- 当前 snapshot 与 artifact snapshot 一致；
- `unreviewed-blocking` 或 `ambiguous-blocking` 出现时不可执行；
- candidate artifact 是唯一被 Phase 2 后创建且可进入 stage plan 的 task metadata。

现有 `check-phase2-check` 必须增加窄例外：忽略当前 candidate artifact 本身的
post-Phase-2 dirty entry，但仍验证 artifact 外 dirty set 与 recorded `dirty_paths`。
该例外不能扩展到 source、docs、spec、test、schema、config、preset 或 overlay。

## 9. AI Review 与 confirmation

AI 负责：

- 判断 path 分类、exact stage scope、type/scope、中文描述、body 语义；
- 检查 issue refs、部署/升级/安全边界与 diff 一致；
- 判断并行工作冲突、evidence owner、危险 Git 操作；
- 决定 `passed`、`revision-required` 或 `blocked`。

Script 只验证 artifact 声明是否存在、结构是否合规、digest 是否 fresh，以及
`ai_review.status=passed` 与 authorization flag 是否为执行前置事实。Script 不推断 AI
Review 是否真实充分。

当 authorization 缺失、path 冲突、危险 Git 操作、hook 计划或 task/issue owner 冲突
出现时，Skill 必须暂停并获得用户确认，或返回 `blocked`。单独 message candidate
不触发暂停。

## 10. Candidate validator

`check-commit-messages` 增加与 range mode 互斥的
`--candidate-artifact <task-local-path>`。Candidate mode 必须：

1. 执行 workspace/task boundary；
2. schema-validate artifact；
3. 验证 evidence、plan digest、self path、sequence 与 freshness；
4. 调用现有 `validate_commit_message(subject, body, primary_issue)`；
5. 验证 exact message bytes digest、stage plan 与 dirty snapshot；
6. 返回 `candidate_validation` facts。

Range mode继续审查 branch history。Candidate mode 不能因
`checked_commits=[]` 成功；没有 candidate validation facts 必须返回非零。

## 11. Exact executor

新增 managed wrapper `scripts/bash/create-task-commit.sh` 与 Python subcommand
`create-task-commit`。Executor 顺序固定：

1. 复用 candidate validator；
2. 拒绝 artifact 外 staged path；
3. 使用 literal pathspec 只 stage exact paths；
4. 重新读取 index，并要求 staged path set 与计划一致；
5. 以权限 `0600` temporary message file 执行
   `git commit --cleanup=verbatim -F <file>`；
6. 读取 raw commit object，并验证 parent、message bytes、path set 与统一 parser；
7. 对比 `unrelated-preserved` pre/post snapshot；
8. 检查 hook mutation 与 remaining staged set；
9. 原子写回 artifact result；
10. 返回 `committed` 或 `blocked` facts。

Executor 不执行 push、amend、rebase、reset、force、stash 或 history rewrite。Commit
失败或 postcondition 失败时保留 Git 现场，artifact 记录 objective error，Skill 返回
`blocked`，由 AI/用户决定后续动作。

## 12. Workflow 与 platform convergence

必须删除：

- Phase 2 planned work commit message review；
- Phase 3.4 主会话 draft/stage/direct commit 细节；
- Branch Review 中重复 work message template；
- continue prompt/command/skill 内部 commit 编排。

Continue entries 只需声明：在 Phase 2 pass 后加载并调用
`guru-create-task-commit`，按 typed exit route，`committed` 后进入 Branch Review。
Contract tests 对 canonical workflow、dogfood workflow 与 selected platform entries
执行固定范围扫描，拒绝 step-local template 与直接 task work commit 文案回流。

## 13. Distribution 与 upgrade

Preset 执行顺序沿用 #120：source validation、canonical install、platform copy、
managed-hash state machine、manifest provenance、installed validation。

本任务增加：

- active package tree；
- `create-task-commit.sh` managed executable；
- extension public API 的 skill id、artifact schema、executor command；
- shared/Codex/Cursor/Claude dogfood copies；
- throwaway 对 initial commit 与 revision commit 的真实 Git 验证。

Extension version 从 `0.6.5-guru.4` 增加到 `0.6.5-guru.5`。该版本仍以官方
Trellis CLI `0.6.5` 为 compatibility target；本任务不升级官方 CLI baseline。

Unknown local skill edit 必须保留原 bytes 并生成 `.new`。Known managed upgrade
必须生成 `.bak`，由实现阶段逐项核对后处理。最终 source/installed/drift 与 recursive
sidecar scan 必须通过。

## 14. Docs SSOT Plan

- docs state：`partial_docs`。
- evidence paths：
  - `docs/requirements/README.md`
  - `docs/requirements/requirement-main.md`
  - `docs/requirements/guru-team-trellis-flow.md`
  - `.trellis/spec/workflow/workflow-contract.md`
  - `.trellis/spec/workflow/skill-package-contract.md`
  - `.trellis/spec/workflow/companion-scripts.md`
  - `.trellis/spec/workflow/data-contracts.md`
  - `.trellis/spec/workflow/quality-guidelines.md`
  - `.trellis/spec/preset/installer.md`
  - `.trellis/spec/preset/overlay-guidelines.md`
  - `.trellis/spec/docs/public-docs.md`
  - `README.md`
  - `trellis/workflows/guru-team/README.md`
  - `trellis/presets/guru-team/README.md`
- strategy：`ssot_first`。
- reason：本任务改变长期 workflow phase owner、公共 skill/API、task artifact、
  deterministic executor、安装与升级合同。Durable docs 必须先成为实现输入。
- affected durable docs：上列 evidence paths 全部进入语义复核；包含 active skill、
  commit flow、artifact/executor 或安装清单的文件必须修改。经复核不需改字节的文件
  必须在 implementation handoff 记录 no-change 理由。
- task artifact delta：R1-R10、artifact fields、candidate/executor state machine、
  typed exits、ID tombstone、test matrix 必须合并到 durable docs/spec。
- merge checkpoint：任何 runtime/schema/installer 代码编辑前完成 durable docs 首轮；
  final Phase 2 check 前再次核对 durable docs、task artifacts、code/schema/test 与
  installed copies 一致。
- task-history-only：Phase 0 handoff、planning approval、agent liveness、单次 command
  output、review rounds、PR readiness 与本机执行时间只保留在 task artifacts。

## 15. Tests 与门禁

### Unit/package tests

- production registry reserved+active lifecycle；
- package frontmatter/interface/schema/example/test evidence；
- mandatory invoke 与三条 typed-exit mapping；
- standalone trigger phrases；
- candidate positive/negative matrix；
- dirty snapshot path encoding、delete、rename、staged/unstaged/untracked；
- exact stage、message bytes、postcondition、hook mutation、unrelated preservation；
- initial/finding-fix multi-sequence freshness；
- workflow/platform duplicate-contract rejection。

### Installer/dogfood

- shared/Codex/Cursor/Claude discovery；
- missing、unchanged、known upgrade、unknown edit、platform shrink；
- executable mode、manifest hash/inventory、source/installed validation；
- canonical apply、dogfood drift、zero unresolved `.new`/`.bak`。

### Throwaway/update

- clean `trellis init`、workflow preview/switch、preset apply；
- installed skill initial commit；
- simulated finding-fix 后 fresh Phase 2 + new artifact + revision commit；
- `trellis update --force`、workflow reapply、preset reapply；
- runtime entrypoints、source/installed validation、final sidecar scan。

### Publish

- local throwaway 在 Phase 2 完成；
- remote feature-ref verifier 只能在 reviewed content push 后执行；
- remote evidence 未通过时 finish-work 不创建 ready PR。

## 16. 安全、兼容与回滚

- Public package 与 example 使用去身份化 repo-relative data；不写 task/private state。
- Message temporary file 必须在 `finally` 中删除，不打印 message 外的 file content。
- Executor 遇到 failure 不执行自动 rollback；这避免 reset/stash 覆盖并行工作。
- Existing `check-commit-messages` range mode、`format-merge-commit`、metadata commit
  与 merge commit 行为保持兼容。
- 回滚 active skill 时必须先移除 production route，再把 id 改为 reserved，并通过
  preset managed-removal contract 清理 known installed copies；不得直接删除 registry
  id 或留下 unknown platform copy。

## 17. 中台知识门禁

`not_applicable`。本任务修改 Guru Team Trellis extension，自身不消费 `go-guru`、
`proto-guru`、Unity3D Guru SDK 或 Flutter Guru SDK/API。

## 18. 需求追踪

| 需求 | 设计承接 | 实现计划承接 | 验收 |
| --- | --- | --- | --- |
| R1 | 第 3 节 | 第 2、6 节 | AC1、AC10 |
| R2 | 第 5、6、12 节 | 第 4 节 | AC2、AC8、AC9 |
| R3 | 第 5、8 节 | 第 3、5 节 | AC4、AC5 |
| R4 | 第 7 节 | 第 2、3 节 | AC4、AC7 |
| R5 | 第 7、8、11 节 | 第 3 节 | AC6、AC7 |
| R6 | 第 9 节 | 第 3、5 节 | AC6 |
| R7 | 第 10、11 节 | 第 3 节 | AC4-AC7 |
| R8 | 第 6、11 节 | 第 3、5 节 | AC7、AC8 |
| R9 | 第 12、14 节 | 第 2、4 节 | AC9 |
| R10 | 第 13、15 节 | 第 4、6、7 节 | AC10-AC14 |
