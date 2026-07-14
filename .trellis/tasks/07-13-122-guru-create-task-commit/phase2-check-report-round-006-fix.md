# #122 第六轮修复后独立 Phase 2 检查报告

## 身份、边界与结论摘要

- 逻辑角色：`阶段二检查代理`。
- 技术身份：`trellis_check_122_round6_fix`。
- 固定 worktree：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/122-guru-create-task-commit`。
- Task：`.trellis/tasks/07-13-122-guru-create-task-commit`。
- Base：`origin/main=6b9495a17dc953c7a54c105e39c23a786edcd8a7`。
- Pre-commit HEAD：`163e64168d5d9783c32665da92aebbb4397564a3`，检查前后未改变。
- Source checkout：`/Users/wumengye/Documents/GoProjects/guru-trellis`，检查前后均 clean，HEAD 与 `origin/main` 一致。
- 检查范围：完整 `origin/main...HEAD`、当前全部 dirty diff、Round 6 raw finding、规划、Docs SSOT、canonical/runtime/schema/interface/example/workflow/tests、五个 installed package roots、manifest、installer、throwaway/update/reapply、历史提交、安全与部署边界。
- 结论：`blocked`。发现 1 个 P1 当前范围 finding；现有 22/22、24/24、500/500 与 throwaway 全绿不能反证该 executor 竞争窗口。
- 操作边界：本代理只新增本 raw report；未修改实现、durable docs、旧 task artifact 或旧 raw report，未运行/写入 `phase2-check.json` recorder、assignment/review recorder、commit、push、PR 或 finish-work。

## 输入证据

- Live issue：`castbox/guru-trellis#122`，状态 `OPEN`；#122 是唯一 close candidate，#92、#120 仅 related。
- 规划：`prd.md`、`design.md`、`implement.md`；schema 1.2 planning approval 由 `check-planning-approval.sh` 验证为 `ok`。
- Round 6 finding：`reviews/round-006-final-release.md` 的 `F-06-01`、`F-06-02`、`F-06-03`。
- 实现交接：`implementation-handoff.md` 的 “Round 6 findings 实现交接”。
- Docs SSOT Plan：`partial_docs`、strategy=`ssot_first`；requirements、README、workflow/spec、package contract、runtime/schema/tests 与 installer/distribution 是 durable owner。
- 官方 Trellis 文档：`https://docs.trytrellis.app/index.md`、`advanced/custom-workflow.md`、`advanced/custom-spec-template-marketplace.md`。官方合同与本仓库 AGENTS.md 一致：Markdown 定义流程/判断，脚本只执行确定性事实；workflow marketplace 与 preset/canonical source 承担可恢复分发。
- 项目规范：`.trellis/spec/workflow/` 五份相关规范、preset/docs 规范、cross-layer/code-reuse guides，以及 `trellis-meta` 的 local workflow、generated files、platform map、skill/command 与 customization references。

## 完整 dirty paths

本报告写入前 `git status --porcelain=v1 --untracked-files=all` 为 55 个 tracked modified、16 个 untracked、0 staged，共 71 个路径；写入后仅新增本报告自身，预期为 72 个 dirty paths。完整集合如下：

```text
 M .agents/skills/guru-create-task-commit/examples/task-commit-plan.json
 M .agents/skills/guru-create-task-commit/interface.json
 M .agents/skills/guru-create-task-commit/references/contract.md
 M .agents/skills/guru-create-task-commit/schemas/task-commit-plan.schema.json
 M .agents/skills/guru-create-task-commit/tests/test_contract.py
 M .claude/skills/guru-create-task-commit/examples/task-commit-plan.json
 M .claude/skills/guru-create-task-commit/interface.json
 M .claude/skills/guru-create-task-commit/references/contract.md
 M .claude/skills/guru-create-task-commit/schemas/task-commit-plan.schema.json
 M .claude/skills/guru-create-task-commit/tests/test_contract.py
 M .codex/skills/guru-create-task-commit/examples/task-commit-plan.json
 M .codex/skills/guru-create-task-commit/interface.json
 M .codex/skills/guru-create-task-commit/references/contract.md
 M .codex/skills/guru-create-task-commit/schemas/task-commit-plan.schema.json
 M .codex/skills/guru-create-task-commit/tests/test_contract.py
 M .cursor/skills/guru-create-task-commit/examples/task-commit-plan.json
 M .cursor/skills/guru-create-task-commit/interface.json
 M .cursor/skills/guru-create-task-commit/references/contract.md
 M .cursor/skills/guru-create-task-commit/schemas/task-commit-plan.schema.json
 M .cursor/skills/guru-create-task-commit/tests/test_contract.py
 M .trellis/guru-team/extension.json
 M .trellis/guru-team/scripts/python/guru_team_trellis.py
 M .trellis/guru-team/skills/packages/guru-create-task-commit/examples/task-commit-plan.json
 M .trellis/guru-team/skills/packages/guru-create-task-commit/interface.json
 M .trellis/guru-team/skills/packages/guru-create-task-commit/references/contract.md
 M .trellis/guru-team/skills/packages/guru-create-task-commit/schemas/task-commit-plan.schema.json
 M .trellis/guru-team/skills/packages/guru-create-task-commit/tests/test_contract.py
 M .trellis/spec/workflow/companion-scripts.md
 M .trellis/spec/workflow/data-contracts.md
 M .trellis/spec/workflow/quality-guidelines.md
 M .trellis/spec/workflow/skill-package-contract.md
 M .trellis/spec/workflow/workflow-contract.md
 M .trellis/tasks/07-13-122-guru-create-task-commit/agent-assignment.json
 M .trellis/tasks/07-13-122-guru-create-task-commit/implementation-handoff.md
 M .trellis/tasks/07-13-122-guru-create-task-commit/phase2-check.json
 M .trellis/tasks/07-13-122-guru-create-task-commit/task-commit-plans/001.json
 M .trellis/tasks/07-13-122-guru-create-task-commit/task-commit-plans/002.json
 M .trellis/tasks/07-13-122-guru-create-task-commit/task-commit-plans/003.json
 M .trellis/tasks/07-13-122-guru-create-task-commit/task-commit-plans/004.json
 M .trellis/tasks/07-13-122-guru-create-task-commit/task-commit-plans/005.json
 M .trellis/workflow.md
 M README.md
 M docs/requirements/README.md
 M docs/requirements/guru-team-trellis-flow.md
 M docs/requirements/requirement-main.md
 M trellis/skills/guru-team/packages/guru-create-task-commit/examples/task-commit-plan.json
 M trellis/skills/guru-team/packages/guru-create-task-commit/interface.json
 M trellis/skills/guru-team/packages/guru-create-task-commit/references/contract.md
 M trellis/skills/guru-team/packages/guru-create-task-commit/schemas/task-commit-plan.schema.json
 M trellis/skills/guru-team/packages/guru-create-task-commit/tests/test_contract.py
 M trellis/skills/guru-team/tests/test_skill_packages.py
 M trellis/workflows/guru-team/README.md
 M trellis/workflows/guru-team/scripts/python/guru_team_trellis.py
 M trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py
 M trellis/workflows/guru-team/workflow.md
?? .trellis/tasks/07-13-122-guru-create-task-commit/phase2-check-report-round-001-fix.md
?? .trellis/tasks/07-13-122-guru-create-task-commit/phase2-check-report-round-002-fix.md
?? .trellis/tasks/07-13-122-guru-create-task-commit/phase2-check-report-round-003-fix.md
?? .trellis/tasks/07-13-122-guru-create-task-commit/phase2-check-report-round-004-fix.md
?? .trellis/tasks/07-13-122-guru-create-task-commit/phase2-check-report-round-006-fix.md
?? .trellis/tasks/07-13-122-guru-create-task-commit/phase2-findings-round-001-fix.json
?? .trellis/tasks/07-13-122-guru-create-task-commit/phase2-findings-round-002-fix.json
?? .trellis/tasks/07-13-122-guru-create-task-commit/review-findings-round-001.json
?? .trellis/tasks/07-13-122-guru-create-task-commit/review-findings-round-002.json
?? .trellis/tasks/07-13-122-guru-create-task-commit/review-gate.json
?? .trellis/tasks/07-13-122-guru-create-task-commit/review.md
?? .trellis/tasks/07-13-122-guru-create-task-commit/reviews/round-001-final-release.md
?? .trellis/tasks/07-13-122-guru-create-task-commit/reviews/round-002-finding-closure.md
?? .trellis/tasks/07-13-122-guru-create-task-commit/reviews/round-003-finding-closure.md
?? .trellis/tasks/07-13-122-guru-create-task-commit/reviews/round-004-finding-closure.md
?? .trellis/tasks/07-13-122-guru-create-task-commit/reviews/round-005-finding-closure.md
?? .trellis/tasks/07-13-122-guru-create-task-commit/reviews/round-006-final-release.md
```

## Findings

### PHASE2-R6-01（P1）：gitlink 可在 executor revalidation 后、exact stage 前被替换，仍提交未经审查的 C

- 位置：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:10504`、`:10511`、`:10572`、`:10583`、`:10590`。
- 事实：executor 入口调用 `validate_task_commit_candidate()`，当时会把当前 submodule HEAD 与 artifact 的 B 比较；但该调用返回后，到 `git add` 前不再比较 gitlink identity。`git add` 后只要求 staged **path set** 等于 `exact_stage_paths`，随后把已产生的 index tree 作为 expected tree。它没有要求 mode `160000` 的 staged blob/OID 仍等于 artifact `gitlink_head=B`。
- 独立复现：临时真实 superproject/submodule 建立 A/B/C 三个 revision；artifact 在 B 生成并通过 candidate validation。检查代理在 executor 入口 revalidation 返回后、首次 stage 前受控把 submodule 从 B 切到 C，模拟并行用户/进程恰好命中该窗口。executor 最终返回 `status=committed` / `exit=committed`，真实 commit gitlink 为 C：

```text
reviewed_revision=0f1c0fc0fc4945add6380c19a0ede5b4e8c8d5cf
switched_revision=ccf9e19d5694801ae5016603cd3b11b5bf95e738
committed_gitlink=ccf9e19d5694801ae5016603cd3b11b5bf95e738
committed_unreviewed_revision=true
```

- 影响：Round 6 的常规 “B candidate -> 执行前已切 C” 回归会通过，因为入口 validator 能发现 stale；但无法证明 artifact 到 exact index 的内容绑定。供应链 revision 可以在 executor 已宣称 revalidated 之后被替换，C 被 stage/commit 并给出虚假的 `committed` typed exit。这违反 #122 R3/R5/R7-R8、AC5-AC7，以及 `F-06-02` 要求的 executor revalidation 与 “C 不得被 stale plan stage/commit” 边界。
- 修复要求：exact stage 必须把 mode `160000` 的 artifact OID 绑定到 index，而不是只 stage path 并接受当时 worktree OID；至少在 commit 前验证 staged gitlink blob 等于 reviewed `gitlink_head`，且设计必须保证发生 B->C 竞争时 C 不被 stale plan stage/commit。新增永久回归，在 candidate/executor 入口验证通过后、exact stage 前切换 B->C，断言 exit blocked、HEAD/candidate/operation state 不变、index 未变为 C。普通文件/symlink/delete/rename 的既有路径合同必须继续通过。
- 处理：本代理不做语义修复；按阶段二检查边界记录 finding 并阻断。

## Round 6 三项 finding 独立闭环结果

### F-06-01：通过

- 7-state detector 覆盖 `MERGE_HEAD`、`CHERRY_PICK_HEAD`、`REVERT_HEAD`、`REBASE_HEAD`、`sequencer/`、`rebase-merge/`、`rebase-apply/`；只返回 stable id、Git path token 与 marker/directory kind。
- Candidate validation、executor 在任何 stage 前、紧邻 `git commit` 前均 fail closed。
- 永久测试用真实 conflicted cherry-pick 验证 candidate command/executor exit code 2 / blocked；marker bytes、HEAD、index、porcelain worktree status、candidate bytes 全部不变。
- Marker matrix 验证 7/7 状态均被识别且 detector 不改 inode；ordinary state 不误报。merge/revert/rebase/sequencer/am 边界与合同一致。

### F-06-02：部分关闭，受 PHASE2-R6-01 阻断

- Public schema/interface/example/runtime 已加入 mode `160000` conditional identity；`gitlink_head`、`gitlink_initialized`、`gitlink_dirty` 在安全 gitlink row 中强制为 commit/true/false。
- 旧 schema 1.0 ordinary plan 删除三个可选字段后仍通过；缺 identity 的 mode160000 row 被 schema 拒绝；完整 identity row 通过。
- 常规真实 A/B/C 回归成立：index=A、candidate=B 时通过；在 executor 调用前切 C 会 stale，validator/executor blocked，C 未 stage。dirty、deinitialized/root-mismatched、unborn 均 fail closed；deliberate gitlink delete 与普通文件/symlink/delete/rename/pathspec/Unicode 回归继续通过。
- 但 executor 内部 revalidation-to-stage 窗口仍可提交 C，故 finding 不能完整关闭。

### F-06-03：通过

- Canonical 与 dogfood workflow 已删除 task work subject/type/scope/body/footer 模板，字节一致。
- Global workflow 只保留 shared branch validator 引用、唯一 mandatory invoke、3 个 typed-exit consumers、finding repeat 与 fail-closed route。
- Metadata empty-body subject 和 merge payload 明确由非 task-work owner 保留。
- 永久 test 直接扫描 canonical/dogfood workflow，拒绝完整 template token、任何直接 `git commit`、`validate_commit_message(` 或 parser definition；五个平台 route-only entry 回归继续通过。

## R1-R10 / AC1-AC14

| 范围 | 结论 | 证据或阻断 |
| --- | --- | --- |
| R1 / AC1 | 通过 | reserved `guru-create-work-commit` 与 active `guru-create-task-commit`、public API/registry/interface 保持一致。 |
| R2 / AC2 / AC8 | 通过 | canonical/dogfood 各 1 invoke、3 exits；5 个历史 sequence/commit freshness 通过。 |
| R3 / R5 / AC5-AC6 | 阻断 | gitlink 的 artifact-to-exact-index content binding 存在 revalidation 后竞争窗口。 |
| R4 / AC3-AC4 | 通过 | standalone trigger、task-local artifact、candidate mode 与 empty branch range 行为仍通过。 |
| R6 | 通过 | AI/human owner 仍在 Markdown；operation state runtime 只检查客观 marker。 |
| R7-R8 / AC7 | 阻断 | shared parser、message/tree/post-result 合同通过，但 exact executor 可提交 reviewed B 之外的 C。 |
| R9 / AC9 | 通过 | workflow/platform route-only 与永久扫描完整。 |
| R10 / AC10-AC11 | 阻断 | package/install/update/throwaway 均通过，但永久测试没有覆盖并阻止 revalidation-to-stage gitlink mutation。 |
| AC12 | 按合同 pending | Remote exact feature-ref verifier 只能在 reviewed content push 后由 `trellis-finish-work` 执行。 |
| AC13 | 通过 | `close_issues=[122]`；#92、#120 仅 related；5 个 work commit 只使用 `Refs #122`。 |
| AC14 | 通过 | Public added-line 与 task plan scan 未发现 secret、credential URL、signed URL、客户数据或机器绝对路径。 |

## Docs SSOT

- Strategy 保持 `ssot_first`，durable docs 的 Round 6 operation/gitlink/route-only delta 已同步且 canonical/installed copies 一致。
- Preset installer、overlay guidelines、public-docs 规范与 preset README 的 no-byte-change 理由成立：本轮未改变 installer 算法、managed path、平台入口或公开安装命令。
- 当前 durable docs 声称 executor revalidation 能使 reviewed gitlink 变化 stale、C 不被 stale plan stage；PHASE2-R6-01 证明该声明只覆盖 executor 调用前变化，不覆盖入口 validation 返回后的可达窗口。因此 Docs SSOT 与真实 runtime 仍有当前范围不一致，不能通过 Phase 2。修复时必须先收敛 package/data/runtime contract，再改 runtime/schema/test/copies。
- Round 6 raw finding、代理身份、临时 probe SHA、单次命令输出、耗时与 sidecar 处理过程继续只属于 task history。

## 验证结果

| 检查 | 结果 |
| --- | --- |
| Planning / workspace / task | planning approval `ok`；workspace boundary `ok`；task validate 与 phase 2.2/3.4/3.5 context parse 通过。 |
| Targeted executor/candidate | 22/22，13.709s，`OK`。 |
| 六个 package roots | 各 4/4，共 24/24，全部 `OK`。 |
| Full suite | package/runtime/preset 500/500，130.393s，`OK`。 |
| 独立 gitlink 竞争探针 | 失败：reviewed B 在 executor revalidation 后切 C，executor commit C 并返回 committed。 |
| Source/installed validator | 均 passed；reserved=1、active=1、invoke=1、exit=3；dogfood 43 managed files、3 platforms、conflict/removal/sidecar=0。 |
| Canonical/installed equality | workflow/runtime byte-equal；canonical package 到 5 roots 的 8 个 managed files 由 validator/manifest 校验一致。 |
| Idempotent preset reapply | `installed=[]`、`updated_managed=[]`、`managed_backups=[]`、`new_copies=[]`；0 sidecar。 |
| Clean throwaway | exit 0；fresh workflow/preset install、initial/finding-fix commit、old-plan reject、`trellis update --force`、workflow/preset reapply、source/installed、drift、两次 installed closeout smoke、recursive sidecar 全通过。 |
| History | `check-task-commit-plan --range origin/main..HEAD` 对 5/5 work commits 返回 `errors=[]`；base 是 HEAD ancestor；分支 107 个 committed paths。 |
| Static | Python compile、相关 Bash syntax、全部 changed JSON parse、branch/dirty `git diff --check` 全部通过。 |
| Official extension boundary | 未修改 upstream/global npm/node_modules；canonical marketplace/preset 与 dogfood copy 边界符合官方文档。 |

## 安全、部署与工作区卫生

- Public committed+dirty added-line high-confidence scan：private key、AWS/GitHub/Slack token、credential URL、signed URL、`/Users/<name>`、`/home/<name>` 均为 0。
- 五个 task plans 的机器绝对路径与 high-confidence secret 命中均为 0。
- 107 个 branch/dirty union paths 未包含 GitHub Actions、Dockerfile/Compose、Kubernetes/Kustomize、Helm/chart、database migration 或 Makefile；无需应用部署、容器发布、配置或数据迁移。
- Canonical preset reapply 未产生 `.new/.bak`；recursive sidecar 为 0。
- Staged paths 为 0；pre-commit HEAD 保持 `163e64168d5d9783c32665da92aebbb4397564a3`；source checkout clean。

## 观察项

1. Remote exact feature-ref marketplace verifier 继续按合同 pending；它只能在 reviewed content push 后由 `trellis-finish-work` 生成，不能替代当前本地 finding。
2. Trellis CLI compatibility target 仍为 `0.6.5`；throwaway 显示 npm `0.6.7`，#122 未授权扩大兼容目标。
3. Sequence 001 的 pre-tree-evidence legacy result limitation 已由既有 review 披露，本轮没有伪造 post-hoc evidence，也不新增 finding。

## 最终结论

- `findings_count: 1`。
- 优先级：P0=0、P1=1、P2=0、P3=0。
- `F-06-01`: closed。
- `F-06-02`: open，被 `PHASE2-R6-01` 阻断。
- `F-06-03`: closed。
- Phase 2：`blocked`。
- 下一步必须返回 implementation，修复 artifact-to-index gitlink OID 绑定并增加竞争窗口永久回归；完成新的 fresh Phase 2 后才能创建下一 sequence work commit。不得复用旧 Phase 2、sequence 001-005、旧授权或现有 Branch Review Gate。
