# #122 Round 1 finding-fix 阶段二独立检查报告

## 检查身份与边界

- 逻辑角色：`阶段二检查代理`。
- 技术身份：`trellis_check_122_round1_fix`。
- 显示名：`Check-Agent-122-Round1-Fix`。
- 工作目录：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/122-guru-create-task-commit`。
- 实际 `pwd` 与 `git rev-parse --show-toplevel` 均等于上述 worktree；source checkout
  `/Users/wumengye/Documents/GoProjects/guru-trellis` 保持 clean。
- Reviewed HEAD：`afcab19397a6ebc7cbd571722ba01950b670e620`。
- Base：`origin/main`，`6b9495a17dc953c7a54c105e39c23a786edcd8a7`。
- Branch：`feat/122-guru-create-task-commit`。
- 检查模式：按 `trellis-before-dev`、`trellis-check`、`trellis-meta` 执行，bug
  修复后的知识固化按 `trellis-break-loop` 执行；未调用 Phase 2 recorder、Branch
  Review recorder/validator，未 commit、push、创建 PR 或执行 finish-work。

## 输入与 dirty path

检查输入包括：

- live GitHub issue `castbox/guru-trellis#122`，检查时状态为 `OPEN`；
- `prd.md`、`design.md`、`implement.md`、`implementation-handoff.md` 的 Round 1 delta；
- `issue-scope-ledger.json`、`planning-approval.json`、既有
  `phase2-check.json` / `phase2-findings.json`；
- Round 1 raw report `reviews/round-001-final-release.md`、failed
  `review-gate.json`、`review-findings-round-001.json` 与 `review.md`；
- `.trellis/spec/docs/**`、`.trellis/spec/preset/**`、
  `.trellis/spec/workflow/**` 与 shared thinking guides；
- `origin/main...HEAD` 的 102 个 committed paths，以及 HEAD 后的 37 个 dirty paths；
- canonical workflow/package/runtime/schema/tests、preset installer、dogfood runtime、
  installed package 与 shared/Claude/Codex/Cursor copies；
- 2026-07-13 live Trellis 官方 `index.md`、`custom-workflow.md`、
  `custom-skills.md`、`custom-spec-template-marketplace.md`。

检查开始时的 37 个 exact dirty paths 分组如下：

| 分组 | 数量 | 路径 |
| --- | ---: | --- |
| canonical finding-fix 与 durable SSOT | 8 | `trellis/skills/guru-team/packages/guru-create-task-commit/{interface.json,references/contract.md,schemas/task-commit-plan.schema.json,tests/test_contract.py}`、`trellis/workflows/guru-team/scripts/python/{guru_team_trellis.py,test_guru_team_trellis.py}`、`.trellis/spec/workflow/{companion-scripts.md,data-contracts.md}` |
| dogfood/installed/platform managed copies | 22 | `.trellis/guru-team/extension.json`、dogfood runtime、dogfood package 4 files，以及 `.agents` / `.claude` / `.codex` / `.cursor` 下各 4 个 package files |
| task history metadata | 3 | `agent-assignment.json`、`implementation-handoff.md`、`task-commit-plans/001.json` |
| Round 1 review metadata | 4 | `review-findings-round-001.json`、`review-gate.json`、`review.md`、`reviews/round-001-final-release.md` |

本报告是检查结束时新增的第 38 个 dirty path。所有路径均属于 #122 finding-fix、
Phase 2 或既有 Round 1 review evidence；没有发现 unrelated/ambiguous path。

## Round 1 三项 finding 独立复核

### F-01 P1：同路径 hook content/mode mutation

结论：已关闭。

- Executor exact staging 后先执行 `git write-tree` 绑定完整 pre-hook index tree，并
  记录 exact paths 的 expected blob/mode；commit 后读取真实 commit tree 与 actual
  blob/mode。
- content+restage 与 mode+restage 两条真实 hook 回归均返回 `blocked`，
  `head_changed=true`、`hook_mutation=true`、`tree_evidence.matches=false`，且保留
  Git 现场。
- no-hook 与 benign exit-0 hook 仍返回 `committed`，tree evidence 完全匹配。
- 本轮额外发现并修复：仅 exit 1、完全不修改 index/worktree 的 hook 原先会因计划内
  路径仍 staged 而误报 `hook_mutation=true`。现在 mutation 只由 tree drift、
  unrelated drift、unexpected staged/dirty path 或 planned-path unstaged drift 推导；
  新回归记录 `hook_mutation=false` 且 expected/actual tree 相等。

### F-02 P2：literal exact path identity

结论：已关闭。

- Index、HEAD tree、expected tree、actual tree 的 path-bearing 查询均使用
  `git --literal-pathspecs` 与 `-z`，只接受 0 条或唯一 path bytes 完全相等的 record。
- `src/[0]*.txt` 与 decoy `src/0foo.txt` 并存时，tracked/staged/worktree-delete/
  staged-delete 均绑定 literal path 的真实 identity，没有绑定 decoy。
- 新增真实 merge-conflict 回归：包含 pathspec metacharacter 的 unmerged path 产生
  多 stage index records，`task_commit_index_identity()` 明确抛出 `WorkflowError`，
  不取第一条或误绑定。

### F-03 P2：closed four-state result schema 与 post-result evidence

结论：已关闭。

- Public schema 使用 closed `oneOf`：`planned` 无 exit；`revision-required`、
  `blocked`、`committed` 只能与同名 exit 配对，各状态禁止 undeclared fields。
- `committed` 强制 commit/parent/message/path/preservation/hook/tree/blob/mode evidence；
  `blocked` 强制 failure stage、pre/current HEAD、head-changed、parent/message/path、
  preservation、hook、unexpected staged/dirty、planned unstaged、tree 与 errors evidence。
- Runtime 在 atomic write 前执行 public Draft 2020-12 schema 与跨字段 validator；
  status/exit mismatch、缺失 evidence、committed hook mutation、tree mismatch 冒充
  committed 均被拒绝。
- 本轮额外发现并修复：blocked result 可构造
  `tree_evidence.matches=false` / `hook_mutation=false` 的矛盾组合。Schema conditional
  与 runtime cross-field validation 现均拒绝该组合；同路径 mutation tamper 回归通过。

## R / AC / Docs SSOT 覆盖

| 范围 | 独立结论 |
| --- | --- |
| R1 / AC1 | `guru-create-work-commit` 保持 reserved tombstone；`guru-create-task-commit` active，extension public API 与 replacement reason 一致。 |
| R2 / AC2 / AC8 | canonical/dogfood workflow 各 1 个 mandatory invoke、3 个唯一 typed-exit consumer；finding-fix 必须回到完整 Phase 2 和 fresh sequence。 |
| R3-R6 / AC3-AC6 | workflow/standalone preconditions 一致；candidate 绑定 task/ledger/planning/Phase 2/HEAD/full snapshot；AI 独占分类、message、review 与 confirmation 判断；executor 只 exact stage。 |
| R7-R8 / AC7 | candidate mode 复用唯一 `validate_commit_message()`；parent/raw message/path/unrelated/hook/tree postconditions 与 terminal result 已覆盖，三个 Round 1 finding 均关闭。 |
| R9 / AC9 | step-local SSOT 位于 canonical package `references/contract.md`；workflow/continue entries 只保留 mandatory invocation、re-entry 与 typed-exit route。 |
| R10 / AC10-AC11 | production registry、managed-hash installer、dogfood/platform distribution、source/installed validators、update/reapply/throwaway 与测试全部通过。 |
| AC12 | local clean throwaway 通过；remote exact feature-ref 因 branch 尚未 push，仍为 finish-work push 后必做 evidence，当前不满足 publish。 |
| AC13 | `close_issues=[122]`；#92、#120 仅在 `related_issues`，不得使用 close keyword。 |
| AC14 | public package/schema/example/manifest/README 未发现 secret、客户数据、`.env` 内容、签名 URL、本机绝对路径或 workspace journal。 |

Docs strategy 为 `ssot_first`。Design 第 14 节的 14 个 durable evidence paths 全部位于
`origin/main` 到当前 working tree 的变更集合；active/reserved id、mandatory route、
artifact/executor、typed exits、finding-fix re-entry、installer/update/reapply 已进入
durable owner。本轮新发现的 hook evidence 精度问题先写入 canonical package contract、
`.trellis/spec/workflow/companion-scripts.md` 与 `data-contracts.md`，再修改 runtime/
schema/tests 并 apply dogfood。Round 1 raw report、临时复现 repo、单次 hash 与 `.bak`
处理过程仍是 task history，没有进入公共 package。

官方文档复核结论：`workflow.md` 是 phase/routing 的 Markdown 控制面；skill 是可复用
workflow module；external skill 需要平台目录分发；spec marketplace 不承载 active task、
workspace 或平台 prompt。当前 workflow/package/preset/spec ownership 与这些边界一致，
没有修改 Trellis upstream、全局 npm 或 `node_modules`。

## 本轮修复与 break-loop 结论

本轮发现 2 个 P2 evidence 缺陷，均在本检查内机械修复：

1. 无修改失败 hook 被误报 mutation：根因是把“计划内 staged path 的存在”当作状态
   差异，属于跨层 evidence contract 与失败路径测试覆盖缺口。
2. blocked tree/hook 字段可相互矛盾：根因是 schema shape validation 与 runtime
   cross-field semantics 未完全连接，属于 data contract 边界缺口。

预防机制已经落地：明确 unexpected dirty / planned unstaged evidence 字段、按 failure
stage 推导 mutation、schema conditional、runtime cross-field validation、benign/failing/
mutating hook 三分回归。另补 unmerged literal path 的真实 Git 冲突回归。没有创建
follow-up issue；这些都属于 #122 当前范围。

## 验证命令与结果

| 命令/检查 | 最终结果 |
| --- | --- |
| `TaskCommitCandidateExecutorTest` | 17 tests，7.611s，`OK`；覆盖 no-hook、benign hook、unchanged failing hook、same-path content/mode mutation、literal decoy、delete、unmerged。 |
| canonical package standalone | 4 tests，`OK`；四状态正负 schema matrix 通过。 |
| package/runtime/preset full suite | 495 tests，128.219s，`OK`。 |
| clean throwaway verifier | exit 0；initial/finding-fix commits、fresh sequence、old-plan reject、unrelated preservation、`trellis update --force`、workflow preview/switch/reapply、preset reapply、source/installed validators、drift、closeout smoke、recursive sidecar scan全部通过。 |
| source / installed package validators | passed；reserved=1、active=1、invoke=1、exits=3；Claude/Codex/Cursor managed files=43，conflict/removal/sidecar=0。 |
| canonical preset apply | 最终幂等，`updated_managed=[]`、`managed_backups=[]`；首次同步本轮 contract/schema/runtime/test delta 产生 16 个 known-managed `.bak`，逐个核对旧/新 hash 后清理并重建 provenance。 |
| canonical/dogfood/platform equality | 6 个 package roots 各 8 files 字节一致；canonical/dogfood runtime 与 workflow 字节一致。 |
| dogfood overlay drift | passed。 |
| planning/workspace/task/context | workspace boundary、schema 1.2 planning approval、task validation、phase 2.2/3.4/3.5 parsing 全部通过。 |
| Bash/Python/JSON/diff | 全量相关 Bash `bash -n`、canonical/dogfood Python `py_compile`、32 个 changed JSON parse、`git diff --check` 全部通过。 |
| mode/sidecar | 四个 executor wrappers executable；recursive `.new/.bak` 为 0。 |
| scope/security/deployment | close=122、related=92/120；public asset security scan passed；broad `git add` absent；deployment asset changes=0。 |

Throwaway 使用 `TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1` 验证公开 marketplace
discovery，再覆盖当前未发布 canonical workflow sample；它不是 remote exact feature-ref
证据。`feat/122-guru-create-task-commit` push 后仍必须由 finish-work verifier 读取该
exact ref，成功前不得创建 ready PR 或关闭 #122。

## 安全、部署与兼容性

- Executor 不 push，不 amend/rebase/reset/force/stash；message temp file 为 `0600` 并
  在 `finally` 删除。
- 未修改 GitHub Actions、Dockerfile/Compose、Kubernetes/Kustomize、Helm、数据库
  migration、Makefile、应用 service、worker、queue 或 runtime config；无需应用部署、
  数据迁移或部署资产同步。
- 变更影响 Trellis workflow/preset/local Git executor 的安装与升级；clean install、
  known-managed update、manifest rebuild、update/workflow/preset reapply 已验证。
- Compatibility target 保持官方 Trellis CLI `0.6.5`；本任务不扩展到本机可见的更新
  版本。

## 最终状态与结论

- Round 1 finding：3 个，全部关闭。
- 本轮新 finding：2 个 P2，全部修复并重跑完整检查。
- 开放 finding：`0`（P0=0、P1=0、P2=0、P3=0）。
- 结论：`pass`，可由主会话记录 fresh `phase2-check.json`，然后准备新的
  `task-commit-plans/002.json`；本报告本身不是 recorder artifact，也不授权 commit。
- 当前 HEAD：`afcab19397a6ebc7cbd571722ba01950b670e620`，未被检查过程修改。
- Final working tree：本报告写入后 38 个 dirty paths，均属于 #122 finding-fix/
  Phase 2/Round 1 metadata；staged paths 为空。
- Source checkout：clean；未发现 suspicious source artifact。
- 未执行 commit、push、PR、finish-work、issue close 或 Branch Review。
