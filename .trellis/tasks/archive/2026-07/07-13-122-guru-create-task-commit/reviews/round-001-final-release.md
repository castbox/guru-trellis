# #122 最终放行审查报告（Round 001）

## 审查身份与边界

- 逻辑角色：`最终放行审查代理`。
- 技术身份：`trellis_final_review_122_01`。
- 复用决策：`reuse_decision=new-agent`。
- 审查模式：Branch Review，只读审查；未修改实现、durable docs、规划、Phase 2 evidence，未调用 Guru Team recorder/gate validator，未 commit、push、创建 PR 或执行 finish-work。
- Reviewed HEAD：`afcab19397a6ebc7cbd571722ba01950b670e620`。
- Base：`origin/main`，`6b9495a17dc953c7a54c105e39c23a786edcd8a7`。
- Diff：`origin/main...HEAD`，102 个 committed paths，9195 insertions / 128 deletions。
- Workspace boundary：actual repository root 与 task worktree 一致；source checkout clean；无 suspicious source artifact。
- Working tree：审查开始时只有主会话维护的 `agent-assignment.json` 与 executor post-result `task-commit-plans/001.json` 变化；二者分别按 committed bytes 和 working-tree result 审查，不混入 committed implementation diff。

## 输入证据

- 需求与规划：`prd.md`、`design.md`、`implement.md`，以及 design 第 14 节 `Docs SSOT Plan`。
- 实现与检查：`implementation-handoff.md`、`phase2-check-report.md`、`phase2-check.json`、`phase2-findings.json`。
- Scope 与身份：`issue-scope-ledger.json`、`planning-approval.json`、`agent-assignment.json`、live GitHub issue #122。
- Task commit：提交中的 `task-commit-plans/001.json` 1908 行 planned bytes、working-tree committed result、raw commit object、actual committed path set。
- 官方边界：Trellis `index.md`、`advanced/custom-workflow.md`、`advanced/custom-skills.md`、`advanced/custom-spec-template-marketplace.md`，以及本仓库 `trellis-meta` architecture/customization references。
- 完整 committed diff：canonical workflow/package/runtime/registry、preset/installer/overlay/manifest、dogfood/platform copies、requirements/spec/README、tests、throwaway verifier 与 task evidence 共 102 paths。

## 逐层审查

### R1-R10 与 AC1-AC14

| 范围 | 结论 |
| --- | --- |
| R1 / AC1 | 通过。`guru-create-work-commit` 保留 reserved tombstone，`guru-create-task-commit` active；extension 为 `0.6.5-guru.5`，官方 CLI baseline 保持 `0.6.5`。 |
| R2 / AC2 / AC8 | 通过。canonical/dogfood workflow 各只有一个 mandatory invoke、三个唯一 typed-exit consumer；finding-fix 明确返回完整 Phase 2 并使用新 sequence。 |
| R3-R4 / AC3-AC5 | 部分通过。task/ledger/planning/Phase 2/HEAD/snapshot/message/authorization 的 pre-commit validator 完整；但 post-result public schema 未绑定要求字段，见 F-03。 |
| R5 / AC6 | 阻塞。executor 使用 literal exact staging，但 snapshot 的 index identity 查询仍解释 pathspec metacharacter，见 F-02。 |
| R6 | 通过。AI Review、conditional confirmation 与 route judgment 位于 Markdown skill contract；runtime 只消费已记录事实。 |
| R7-R8 / AC7 | 阻塞。共享 parser、parent/raw message/path/unrelated/index 检查存在，但同一路径 hook 内容改写未被检测，见 F-01；result schema 也不能证明 typed exit/evidence，见 F-03。 |
| R9 / AC9 | 通过。step-local 正文位于 canonical package reference；workflow/continue entries 只做 invocation、route 与 re-entry。 |
| R10 / AC10-AC11 | 分发和现有测试通过，但测试矩阵未覆盖 F-01/F-02/F-03，因此不能以 489/489 替代语义放行。 |
| AC12 | 如实 pending。local throwaway evidence 存在；remote current feature-ref verifier 明确延后到 reviewed content push 后，当前 evidence 不满足 publish。 |
| AC13 | 通过。ledger 只把 #122 放入 `close_issues`；#92、#120 仅为 `related_issues`；work commit 只使用 `Refs #122`。 |
| AC14 | 通过。公共 package/schema/example/manifest/docs 未发现 secret、客户数据、`.env` 内容、签名 URL、本机绝对路径或 workspace journal。 |

### Workflow、Skill 与脚本边界

- 官方文档确认 workflow Markdown 是流程控制面、skill 是可复用扩展点、平台 skill roots 需要由 preset 分发；当前 canonical ownership 与该边界一致。
- Global workflow 只保留 Phase 3.4 mandatory invocation、typed-exit consumers、finding-fix repeat route 和 fail-closed stop；没有第二条 direct task work commit 路径。
- Canonical package、installed canonical、shared、Codex、Cursor、Claude 各 8 个 package files 字节一致；canonical/dogfood workflow、runtime、registry、wrapper 字节一致。
- Candidate validator 复用 `validate_commit_message()`；sequence/history、stale evidence、NUL status、rename source/destination、candidate restage、exact stage set 和 unrelated staged blocking 已实现。
- 当前三个 finding 都位于确定性事实层，不要求脚本做语义判断；修复仍应保持 AI gate 先于 validator/executor。

## Phase 2 Finding 复核

| Finding | 独立复核 |
| --- | --- |
| F-01 broad `git add -A` | 已修复。executor 使用 `git --literal-pathspecs add -- <exact paths>`。 |
| F-02 非 NUL path parsing | 已修复。status/path sets 使用 NUL-delimited bytes，Unicode/space/rename 主路径可用。 |
| F-03 sequence/history freshness | 已修复。强制 next-unused contiguous sequence，并拒绝 candidate 已存在于 pre-commit HEAD。 |
| F-04 stage/index failure 未回写 blocked | 已修复。unexpected staged 与 executor failure 会写 `blocked` result 并保留 Git 现场。 |
| F-05 staged-old candidate bytes | 已修复。candidate self path 在 commit 前无条件 restage 当前 validated bytes。 |

上述 5 个历史 finding 均 closed；本轮发现的是此前测试未覆盖的不同缺陷。

## Docs SSOT

- Strategy：`ssot_first`。
- Design 第 14 节列出的 14 个 durable evidence paths 均有 committed 语义变更。
- Requirements、flow、workflow/preset/docs specs 对 active/reserved id、mandatory route、artifact、candidate validator、exact executor、typed exits、re-entry、installer/update/reapply 的 owner 分层一致。
- `.trellis/spec/workflow/data-contracts.md:344` 明确 schema 绑定 freshness/result，post-result 记录真实 commit/message/path/preservation/hook evidence；F-03 表明实现 schema 尚未满足该 SSOT。
- `.trellis/spec/workflow/companion-scripts.md:76` 与 package contract 要求 snapshot/executor/hook checks；F-01/F-02 表明 objective implementation 尚未完全承接。
- Task-history-only planning/liveness/single-run evidence 未进入公共 package。

## 验证命令

| 命令/检查 | 结果 |
| --- | --- |
| `python3 -m unittest ...TaskCommitCandidateExecutorTest` | 11 tests，4.541s，OK。 |
| canonical package `unittest discover` | 3 tests，OK。 |
| package/runtime/preset full suite | 489 tests，124.753s，OK；本轮在 reviewed HEAD 重跑。 |
| source `check-skill-packages` | passed；reserved=1、active=1、invoke=1、exits=3。 |
| installed `check-skill-packages` | passed；Claude/Codex/Cursor、managed files=43、sidecar/removal/conflict=0。 |
| dogfood overlay drift | passed。 |
| changed Bash `bash -n`、Python `py_compile`、JSON parse、`git diff --check` | 全部通过。 |
| wrapper executable、recursive `.new/.bak` scan | 全部通过；sidecar=0。 |
| canonical/installed/platform byte comparison | 全部一致。 |
| commit object audit | parent、raw message SHA-256、102 planned/result/actual path sets 全部一致。 |
| Phase 2 clean throwaway evidence | 同一实现内容下已通过 initial/finding-fix、old-plan reject、update/workflow/preset reapply、validators、closeout smoke、sidecar scan；本轮完整阅读 verifier diff，未重复远端 feature-ref 测试。 |
| 独立 hook mutation regression | executor 错误返回 `committed`；commit 内容为 `hook-mutated`，result 写 `hook_mutation=false`。 |
| 独立 literal pathspec regression | `task_commit_index_identity("src/[0]*.txt")` 返回匹配 decoy `src/0foo.txt` 的 blob，而非 literal file blob。 |
| 独立 result schema negative | `committed` 缺全部 postcondition fields、以及 `status=blocked/exit=committed` 均得到 schema errors `[]`。 |

## 部署、安全与兼容性

- 未修改 GitHub Actions、Dockerfile/Compose、Kubernetes/Kustomize、数据库 migration、Makefile、应用 service、worker、queue 或 runtime config；无需应用部署或数据迁移。
- 变更影响 Trellis workflow/preset installation 与本地 Git commit executor；clean install/update/reapply/managed hash/drift 证据存在。
- Executor 不 push，不 amend/rebase/reset/force/stash；message temp file 使用 `0600` 并在 finally 删除。
- F-01 是提交完整性问题：受信任或被篡改的 local pre-commit hook 可让真实 commit bytes 脱离 AI-reviewed snapshot 而仍被错误标记为 `committed`。
- Compatibility target 仍为 Trellis CLI `0.6.5`；本 issue 不扩大到本机更新版本。

## Findings

### F-01（P1）同一路径 hook 改写可绕过 reviewed snapshot 并错误返回 committed

- 位置：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:10125`。
- 证据：executor 在 hook 执行后只比较 parent、message bytes、committed path set、unrelated 状态、extra dirty path 与 remaining staged path；`10140-10150` 没有把 commit tree/blob 与 hook 前 validated exact index/content identity 对比。
- 独立复现：candidate 审查 `src/task.txt=reviewed-change`；pre-commit hook 改为 `hook-mutated` 并 `git add src/task.txt`。executor 返回 `status=committed`，真实 commit 包含 `hook-mutated`，working result 写 `hook_mutation=false`。
- 影响：AI Review 和 dirty snapshot 绑定的实际内容可以在最后一次 validation 后被替换，核心闭环产生虚假的 postcondition pass。
- 修复要求：commit 前绑定 exact staged tree/blob identities（例如预期 tree），commit 后比较真实 tree/blob；任何同路径内容/mode mutation 必须写 `blocked`。新增 same-path worktree/index/mode hook regressions。

### F-02（P2）index identity 查询未使用 literal pathspec，metacharacter 路径绑定错误 blob

- 位置：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:9644`。
- 证据：`git ls-files -s -z -- <path>` 缺少 `--literal-pathspecs`，并在 `9654-9658` 取第一条匹配结果。
- 独立复现：仓库同时存在 literal `src/[0]*.txt` 与 decoy `src/0foo.txt` 时，runtime 为 literal path 返回 decoy blob `8f96...`，真实 literal blob 是 `0ba4...`。
- 影响：dirty snapshot 的 `index_blob` 不是目标路径的客观 identity；删除、staged 和 pathspec metacharacter evidence 可错误绑定其它文件，违反 R3/R5 与 AC11 的 literal path 回归要求。
- 修复要求：所有带 path 参数的 Git identity 查询使用 `git --literal-pathspecs ...`，并要求零或唯一 exact NUL record；新增 tracked/staged/deleted metacharacter path 与 decoy collision tests。

### F-03（P2）public result schema 不约束 typed exit 配对或 post-commit evidence

- 位置：`trellis/skills/guru-team/packages/guru-create-task-commit/schemas/task-commit-plan.schema.json:99`。
- 证据：`result.additionalProperties=true` 且只 required `status`/`exit`；schema 接受 `{"status":"committed","exit":"committed"}` 而缺少 commit SHA、parent、message digest、committed paths、preservation/hook facts，也接受 `status=blocked` 与 `exit=committed` 的冲突组合。
- 影响：public schema 未按 data-contract SSOT 绑定真实 post-result fields 和唯一 typed-exit 语义；损坏或伪造 result 仍是 schema-valid artifact，downstream 无法用公共合同 fail closed。
- 修复要求：对 planned/revision-required/blocked/committed 使用条件 schema 或 `oneOf`，关闭额外字段并为各状态声明 required/const 配对；committed 必须要求并校验 commit/parent/message/path/preservation/hook evidence，增加负向 schema tests 与 post-result validator。

## 观察项

1. `remote current feature-ref marketplace verifier` 仍为 pending 是预期状态，不是本轮 finding；在 reviewed content push 后通过前不得 ready PR 或关闭 #122。
2. 现有 489 tests 和 clean throwaway 都通过，但没有覆盖同路径 hook content mutation、tracked metacharacter decoy collision 或 invalid result-state schema，因此不能反证本轮 findings。

## 后续候选

无。三个问题都属于 #122 当前 artifact/executor/postcondition/test scope，不能降级为 follow-up candidate。

## 结论

- `findings_count=3`（P1=1，P2=2，P0/P3=0）。
- 当前结论：`blocked`。
- 本报告不可作为最终放行证据；它可作为 finding discovery evidence，必须返回 implementation，完成修复与新的完整 Phase 2，使用 fresh `task-commit-plans/002.json` 创建 finding-fix work commit，再由 finding owner closure review 和全新最终放行代理复核。
- Reviewed HEAD：`afcab19397a6ebc7cbd571722ba01950b670e620`。
- `reuse_decision=new-agent`。
