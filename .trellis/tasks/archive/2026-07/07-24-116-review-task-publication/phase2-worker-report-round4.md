## 检查完成

### 审查身份与范围

- 角色：独立 `trellis-check` 阶段二检查代理，按 installed `guru-check-task` Skill 及其 `references/contract.md` 执行 semantic review。
- Task：`.trellis/tasks/07-24-116-review-task-publication`
- Issue：`castbox/guru-trellis#116`
- Worktree：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/116-review-task-publication`
- Branch：`codex/116-review-task-publication`
- 审查 HEAD / planning base：`bdc8f50bcd1e325aed331d4b01107b83ed8ee940`
- 工作树范围：69 个 modified tracked files，258 个 untracked files；本轮按真实未提交实现 diff、全部 task artifacts、curated specs、durable docs、canonical / installed / 四平台副本和测试链路审查。
- 写入边界：本轮除本 raw report 外未修改实现、规划、durable docs、gate artifact 或其它 task artifact；未调用 Phase 2 recorder/checker，未 commit、push、创建 PR、归档或 finalize。
- 问题资格边界：候选问题先按受支持正常路径判断。本报告未把恶意篡改、伪造 artifact、对抗性输入、非常规竞态或其它明确排除场景列为 finding。

### 前置条件与新鲜度

- Workspace Boundary：通过。Expected workspace 与 actual repo root 均为上述 issue #116 worktree；source checkout 为 `/Users/wumengye/Documents/GoProjects/guru-trellis`，source checkout clean，suspicious source artifacts 为 `[]`，task worktree dirty 与待审实现状态一致。
- Planning Approval：`approved`。规划证据绑定当前 HEAD `bdc8f50bcd1e325aed331d4b01107b83ed8ee940`，facts digest `28aff0...`，artifact digest `eb8b4...`；`ambiguity_review`、fixed-scope scanner、`explicit-post-planning-review` provenance 和三份规划文档 digest 均通过 validator。
- Agent Assignment：通过；8 个 assignment、168 个有效 status events，包含本轮独立 reviewer。
- Task structure：`task.py validate` 通过；`implement.jsonl` 9 个有效条目，`check.jsonl` 8 个 curated 条目。
- Live issue：已重新读取 GitHub issue #116；其 active publication semantic owner、两个 profile、三个 typed exits、target-owned authoring seed、caller 初始内容准备、publication 独占充分性/修订判断和真实 wrapper eval 范围与已批准规划一致。
- 官方依据：重新读取 Trellis 官方 `index.md`、`advanced/custom-workflow.md`、`advanced/custom-spec-template-marketplace.md`；当前实现继续遵守 Markdown 控制流程、脚本只执行确定性事实、公共 marketplace 只发布可复用合同的边界。

### 已检查文件

- Task planning / handoff / prior evidence：
  - `.trellis/tasks/07-24-116-review-task-publication/prd.md`
  - `.trellis/tasks/07-24-116-review-task-publication/design.md`
  - `.trellis/tasks/07-24-116-review-task-publication/implement.md`
  - `.trellis/tasks/07-24-116-review-task-publication/implementation-handoff.md`
  - `.trellis/tasks/07-24-116-review-task-publication/issue-scope-ledger.json`
  - `.trellis/tasks/07-24-116-review-task-publication/phase2-check.json`
  - `.trellis/tasks/07-24-116-review-task-publication/phase2-worker-report.md`
  - `.trellis/tasks/07-24-116-review-task-publication/phase2-worker-report-round2.md`
  - `.trellis/tasks/07-24-116-review-task-publication/phase2-worker-report-round3.md`
- Curated specs：
  - `.trellis/spec/workflow/quality-guidelines.md`
  - `.trellis/spec/workflow/skill-package-contract.md`
  - `.trellis/spec/workflow/workflow-contract.md`
  - `.trellis/spec/workflow/data-contracts.md`
  - `.trellis/spec/workflow/companion-scripts.md`
  - `.trellis/spec/preset/installer.md`
  - `.trellis/spec/preset/upstream-ownership.md`
  - `.trellis/spec/docs/public-docs.md`
- Canonical publication package：
  - `trellis/skills/guru-team/packages/guru-review-task-publication/**`
  - `trellis/skills/guru-team/adapters/eval/native_adapter.py`
  - `trellis/skills/guru-team/registry.json`
  - `trellis/skills/guru-team/consumers/stop/**`
  - `trellis/skills/guru-team/consumers/workflow/production/review-task-publication-return-to-task-work.schema.json`
- Canonical workflow / runtime / scripts：
  - `trellis/workflows/guru-team/workflow.md`
  - `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
  - `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
  - `trellis/workflows/guru-team/scripts/bash/record-task-publication-review.sh`
  - `trellis/workflows/guru-team/scripts/bash/check-task-publication-review.sh`
- Installed / platform package and routing copies：
  - `.trellis/guru-team/skills/packages/guru-review-task-publication/**`
  - `.agents/skills/guru-review-task-publication/**`
  - `.codex/skills/guru-review-task-publication/**`
  - `.claude/skills/guru-review-task-publication/**`
  - `.cursor/skills/guru-review-task-publication/**`
  - `.trellis/guru-team/scripts/python/guru_team_trellis.py`
  - `.trellis/guru-team/skills/adapters/eval/native_adapter.py`
  - `.trellis/guru-team/skills/registry.json`
  - `.trellis/guru-team/extension.json`
  - `.trellis/workflow.md`
  - `.agents/skills/trellis-continue/SKILL.md`
  - `.codex/skills/trellis-continue/SKILL.md`
  - `.codex/prompts/trellis-continue.md`
  - `.claude/commands/trellis/continue.md`
  - `.cursor/commands/trellis-continue.md`
- Branch Review producer：
  - canonical、installed、Agents、Codex、Claude、Cursor 的 `guru-review-branch` `SKILL.md`、`interface.json`、`references/contract.md` 与 tests。
- Preset / ownership / install：
  - `trellis/guru-team-extension.json`
  - `trellis/presets/guru-team/README.md`
  - `trellis/presets/guru-team/overlays/**`
  - `trellis/presets/guru-team/ownership/upstream-ownership.json`
  - `trellis/presets/guru-team/ownership/upstream-ownership.schema.json`
  - `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`
  - `trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`
  - `trellis/presets/guru-team/scripts/python/test_upstream_ownership.py`
  - `trellis/presets/guru-team/scripts/python/validate_upstream_ownership.py`
  - `trellis/presets/guru-team/scripts/python/verify_installed_closeout.py`
- Durable docs：
  - `README.md`
  - `trellis/workflows/guru-team/README.md`
  - `trellis/presets/guru-team/README.md`
  - `docs/requirements/README.md`
  - `docs/requirements/guru-team-trellis-flow.md`
  - `docs/requirements/requirement-main.md`
  - 本次变更覆盖的 `.trellis/spec/**` durable contract files。

### F-001 至 F-005 关闭复核

#### F-001：已关闭

- 两个 profile `publication_review` / `publication_review_stale` 均重建并校验 12 项 entry precondition bindings：runtime dependency、task workspace、task identity、Branch Review handoff、planning approval、Phase 2 check、issue scope ledger、Docs SSOT reconciliation、Branch Review evidence、publication content、review range / working tree、invocation freshness。
- stale profile 强制非空 `stale_reason`、`reentry_context` 和 `supersedes_publication_ref`；recorder 在替换前按 exact current prior artifact 复核 supersedes。
- non-stale profile 不允许携带 stale 字段或替换既有 artifact。
- public wrapper 在 owner checker 已通过后仍逐项复核 stale reason / context，并要求非空 owner supersedes。
- actual-wrapper stale evaluation 通过。

#### F-002：已关闭

- Schema 与 runtime 对 ready / return / blocked 三条 route 均使用 closed shapes，并对十个维度、findings、conclusions、gate decision、consumer 和 cross-reference 执行语义约束。
- `ready`：十维必须全 passed、所有 findings closed 且 closure evidence 非空、三个 conclusions 均 passed、gate passed、12 项 entry checks 全 passed。
- `return_to_task_work`：必须有 finding dimension，不允许 blocked dimension；至少一个 open `task_work` finding，全部 open findings 均为 `task_work` 且引用 finding dimensions；conclusions 只能为 passed / finding，gate 为 return。
- `blocked`：必须有 reason / remediation、blocked dimension、open `external_blocker` finding、blocked conclusion；不得混入 finding conclusion，gate 为 blocked。
- Runtime 额外拒绝 duplicate finding refs、无 evidence / closure、错误 finding-dimension binding、错误 consumer 或非精确维度集合。
- Source / installed contract tests 已覆盖三个合法 route 以及 ready 混入 blocked conclusion、return 全维 passed、blocked 只有 reason、duplicate ref、open finding 与非 passed dimension 不一致等负例。
- Shared actual-wrapper evaluation 覆盖 ready / return / blocked，而非仅序列化静态 output fixture。

#### F-003：已关闭

- `.trellis/guru-team/extension.json` skill package 安装结果：`status=ok`，11 packages，2100 managed files，removals / conflicts / sidecars 均为 0。
- Source 与 installed package validator 均通过：11 active Skills、42 exits、25 targets；唯一 planned target 为 `guru-finalize-task`。
- Ownership validator 通过：frozen 43、active 43、overlay 43、removed 0、reviewed-current payload 5。
- Dogfood overlay drift 检查通过；无 `.new`、`.bak`、`.orig` sidecar。
- Canonical、installed、Agents、Codex、Claude、Cursor publication package 逐字节一致（排除 `__pycache__`）；runtime / adapter 逐字节一致，shell scripts 保持 executable。

#### F-004：可执行路由已关闭；durable docs 子项由 F-006 重新阻塞

- Canonical 与 dogfood workflow 逐字节一致。
- Branch Review 的 source、installed 和四平台副本均把 `passed` 指向 active `guru-review-task-publication`。
- 五个 canonical continue overlays 及 dogfood copies 均要求 Branch Review passed 后进入 Phase 3.6，由 caller 先编写初始 publication content，再调用 active publication；仅 publication `ready` 指向 planned finalize。
- 测试中残留的 old planned-publication wording 只存在于 `assertNotIn` 等负向断言，不是正向 expected route。
- Global workflow 明确：Branch Review passed -> publication；mandatory publication invoke；ready -> planned finalize；return -> workflow router；blocked -> fail-closed stop。
- Production manifest 保持 3 Skills / 11 exits；Stage 0 保持 6 Skills / 24 exits；active closure 为 11 Skills / 42 exits。
- 但 durable `docs/requirements/requirement-main.md` 当前章节仍保留互相矛盾的现时态说明，见 F-006；因此不能把 F-004 的“全部 durable docs 同步”视为完全关闭。

#### F-005：已关闭

- Global workflow Phase 3.6 明确 caller 先根据 current reviewed evidence 编写 `pr-body.md` 与 `finish-summary-index.json`；该 entry preparation 不判断 semantic sufficiency、Issue closure、十维结论、finding route 或 readiness。
- 缺失 / malformed content 在 publication invocation 前 fail closed；publication 仍是充分性、finding、metadata revision 和 route 的唯一 semantic owner。
- Phase 3.7 明确两份文件已经 authored / reviewed / bound，禁止在 `ready` 后首次创建、重新生成或修改。
- 五个平台 continue 入口保持同样顺序和 owner 边界。
- 静态 tests 校验 content preparation / fail-close 位于 publication invoke 前，且 Phase 3.7 不首次创建内容。
- Shared actual-wrapper eval 在隔离 installed repo 中先 staging 当前 content，再调用真实 owner recorder、checker 和 public wrapper；不是只对 output fixture 做 schema serialization。

### 已修复问题

- 无。本轮 handoff 明确要求对实现保持只读，唯一允许写入为本 raw report；因此没有自修复实现或 durable docs。

### 未修复问题

#### F-006（P2，blocking）：current requirements SSOT 仍把已激活 publication 描述为 planned / missing

- 文件：`docs/requirements/requirement-main.md:520-522`
- 资格：`normal_required_behavior` / `explicit_requirement`
- 正常复现：
  1. 直接读取 current durable requirements 的 `## Post-commit Branch Review closed-loop Skill` 章节；
  2. 该章节以现时态声明：`passed` 只生成给 planned `guru-review-task-publication` 的三字段 seed，`#131` 不定义其 schema/profile/authoring fields，目标缺失时 fail closed；
  3. 同一文档 `:90-100` 已说明 Branch Review passed 后 active publication、target-owned authoring seed、caller initial content 和 publication 独占 semantic ownership；
  4. 实际 canonical / installed / platform route 也已经激活该 target。
- 当前 diff 还把紧随其后的 closure 从旧 10/39 更新为“#116 激活后 11 Skills / 42 exits”，却保留前一句 planned / target missing 现时态，因此同一 current section 内形成直接矛盾。
- 影响：
  - 违反 PRD AC18 的 Docs SSOT reconciliation；
  - AC19 的“完整验证后无 P0-P3 finding”不能成立；
  - durable requirements 读者可能错误理解 current Branch Review exit 与 active publication 的 package / schema / authoring ownership；
  - 当前 green tests 未覆盖这一段 current durable wording。
- 范围说明：无需篡改 artifact、hash、state 或 payload，也不依赖恶意 actor、竞态或非常规环境；仅按正常文档读取路径即可复现，因此属于 current acceptance finding。
- 必需修复：
  - 将 `:520-522` 改为清晰的历史时态（例如明确“#131 交付时”）或直接改为 #116 当前 active contract；
  - 增加针对该 current durable section 的定向测试 / scanner，能够区分 current SSOT、显式 historical / task archive 与负向测试断言；
  - 修复后重新运行 durable docs 定向检查及完整验证链路。
- 未自修复原因：本轮 reviewer 的显式写入边界禁止修改 implementation / durable docs。该 finding 必须返回 implementation，再经 Phase 2、task commit 与 Branch Review 闭环。

### 十维充分性判断

| 维度 | 结论 | 证据 |
| --- | --- | --- |
| Requirements | finding | F-001 至 F-005 的代码/route 主体已承接，但 F-006 违反 AC18 / AC19。 |
| Functional correctness | passed | 两 profile、三 exits、12 项 entry binding、stale replacement、route semantics 和真实 wrapper eval 均闭环。 |
| Code quality | passed | Semantic owner 保持在 Markdown Skill / AI Gate；Python / shell 只记录、校验或执行确定性事实。 |
| Compatibility | passed | Legacy reader、Stage 0、production manifest、planned finalize 和 frozen package ownership 均保持边界。 |
| Tests | passed | Full runtime / Skill / preset / publication / Branch Review / actual-wrapper / throwaway 均通过；F-006 同时暴露 durable wording scanner 需补强，但不影响本轮验证足以给出 return route。 |
| Docs SSOT | finding | `ssot_first` 主体已同步，但 F-006 使 current requirements SSOT 尚未完全 reconciled。 |
| Security / privacy | passed | 未发现 secret、credential、private data、签名 URL 或生产敏感数据写入；无恶意 actor 范围扩张。 |
| Deploy / operations | passed | 无 `.github`、Docker / Compose、Kubernetes / Helm、DB migration、`.env`、Makefile、Go module 或 package manifest 变更；无生产写操作。 |
| Agent recovery | passed | Assignment / status evidence 完整，本轮 reviewer 可被定位和恢复。 |
| Verification completeness | passed | 全量与 targeted 验证均完成；唯一无法执行的是未 push 分支的 exact remote branch marketplace，已明确作为当前限制而非失败。 |

### 验证结果

- Lint：通过
  - `git diff --check`
  - `bash -n` publication scripts 与 `verify-throwaway-install.sh`
  - 仓库未提供 Ruff / Flake8 / ShellCheck 配置；未虚构额外 lint 结论。
- TypeCheck：不适用
  - 仓库未提供 mypy、pyright 或等价 type-check 入口；
  - `python3 -m py_compile` 对 runtime、native adapter、ownership validator、installed closeout 通过，但不把它冒充 TypeCheck。
- Tests：通过
  - Source publication contract：16/16
  - Installed publication contract：16/16
  - Source Branch Review contract：8/8
  - Installed Branch Review contract：8/8
  - Source publication shared actual-wrapper eval：7/7
  - Installed publication shared actual-wrapper eval：7/7
  - Runtime full：570/570，13 skipped
  - Skill full：174/174
  - Preset apply：45/45
  - Upstream ownership unit tests：9/9
  - Preset 合计：54/54（45 + 9；ownership validator 另行执行，不拿 validator 替代 9 项 unit tests）
  - Source / installed skill-package validators：通过，11 Skills / 42 exits / 25 targets
  - Upstream ownership validator：通过，43 frozen / 43 active / 43 overlay / 0 removed / 5 reviewed-current payload
  - Dogfood overlay drift：通过
  - Agent assignment checker：通过
  - Task validation：通过
  - Throwaway install / update / reapply / no-developer fixture：通过，exit 0

#### 主要实际命令与终态

- `python3 trellis/skills/guru-team/packages/guru-review-task-publication/tests/test_contract.py`：16 tests，OK。
- `python3 .trellis/guru-team/skills/packages/guru-review-task-publication/tests/test_contract.py`：16 tests，OK。
- `python3 trellis/skills/guru-team/packages/guru-review-branch/tests/test_contract.py`：8 tests，OK。
- `python3 .trellis/guru-team/skills/packages/guru-review-branch/tests/test_contract.py`：8 tests，OK。
- 按 source / installed `guru-review-task-publication/evals/evals.json` 遍历 shared native adapter 的 7 个 cases：各 7/7 passed。
- `python3 trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`：570 tests passed，13 skipped。
- `python3 trellis/skills/guru-team/tests/test_skill_packages.py`：174 tests passed。
- `python3 trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`：45 tests passed。
- `python3 trellis/presets/guru-team/scripts/python/test_upstream_ownership.py`：9 tests passed。
- Source / installed `check-skill-packages`：均 passed，11 active / 42 exits / 25 targets。
- `python3 trellis/presets/guru-team/scripts/python/validate_upstream_ownership.py`：passed。
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`：passed。
- `TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1 ./trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`：exit 0。
- `git diff --check`：passed。

### Throwaway / marketplace / upgrade-update 证据

- 使用独立临时仓库运行：
  - `TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1 ./trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`
- 已覆盖：
  - clean init 与 local unpublished workflow sample；
  - public marketplace discovery；
  - initial workflow / preset install；
  - initial closeout：local / remote / PR heads 一致，PR ready；
  - `trellis update`；
  - workflow / preset reapply；
  - after-update closeout：local / remote / PR heads 一致，PR ready；
  - no-developer fixture 的 update / reapply / validation；
  - source / installed validators、ownership 和 overlay drift checkpoints；
  - 无 `.new` / `.bak` 冲突副本。
- 最终输出：`Verified public marketplace discovery plus local unpublished workflow sample ...`，exit 0。
- 当前限制：`codex/116-review-task-publication` 尚未 push；`git ls-remote` 未发现该 remote branch，因此无法用 exact remote branch ref 验证尚未发布的候选 bytes。该限制已如实记录，不把本地 sample 验证表述为 exact remote-branch verification，也不将未 push 事实误判为实现失败。

### Docs SSOT 证据交接

- Plan strategy：`ssot_first`
- Durable docs / specs：workflow、Skill package、data contracts、companion scripts、preset installer / ownership、public docs、README 与 requirements 主体已按 active publication 更新，并与 code / schema / tests 大体一致。
- Task artifacts：`prd.md`、`design.md`、`implement.md` 与 `implementation-handoff.md` 对 active publication、两个 profile、三个 exits、authoring order、stale route 和 frozen scope 保持一致。
- Code / test：canonical / installed / platform package、runtime、recorder/checker、workflow route 和 actual-wrapper eval 保持一致。
- Task-history-only：prior worker reports、historical `phase2-check.json`、task-local planning / handoff / ledger 属 task history，不作为 current durable product SSOT。
- Reconciliation 结论：`task_delta_merged=false`。原因不是缺少大范围 docs 写入，而是 F-006 指向的 current durable requirements 段落尚未完成语义合并；因此本轮不能确认 `ssot_first` 完成，也不能给出 no-update 结论。

### Frozen scope / 非影响范围

- `guru-finalize-task` 仍仅为 planned identity；未实现 #118。
- Finish-work / publish / archive 资产未修改；未实现 #119。
- 物理 finish overlays 保持现状；未实现 #132。
- #131 public output schemas / examples 保持冻结。
- Production manifest 保持 3 Skills / 11 exits。
- Stage 0 保持 6 Skills / 24 exits。
- 43-path overlay identity / inventory 保持冻结；仅 5 个 reviewed-current payload bytes 按计划更新。
- 未产生 GitHub mutation、生产写入、push、PR、archive 或 finalization。

### 证据交接

- 阶段二：已覆盖完整未提交实现 diff、8 个 curated specs、三份批准规划、implementation handoff、live issue、官方 Trellis docs、durable docs、canonical / installed / platform route、schema/runtime/scripts 和全验证链路。F-001、F-002、F-003、F-005 关闭；F-004 的 executable route 关闭，但 durable docs reconciliation 被新 F-006 阻塞。
- 当前 `phase2-check.json`：仍是历史 `schema_version=2.0`、`typed_exit=implementation_required` 证据，本轮没有调用 recorder/checker，也没有覆盖该 artifact。本报告可支撑主会话在 semantic Gate 后记录新的 `implementation_required`，不能支撑 `passed`。
- Docs SSOT：strategy 为 `ssot_first`；current durable docs 尚未完全一致，F-006 修复前不得声称 task delta 已 merge。
- Branch Review：尚未进入 post-commit Branch Review；当前没有 implementation commit，不能以本报告替代完整 `origin/<base>...HEAD` committed diff review，也不能供 Branch Review Gate 直接放行。
- 部署 / 安全：无 deploy surface、生产配置、数据库、容器、CI/CD 或 secret-handling 影响；验证过程无生产副作用。
- 开放风险：仅 F-006。它是 current-scope P2 finding，不是 speculative warning 或 excluded hardening。

### 结论

`implementation_required`

当前实现的 publication runtime、schema、route、preset、跨平台副本和实际 wrapper 链路已通过完整验证，F-001 至 F-005 的可执行行为已闭环；但 `docs/requirements/requirement-main.md:520-522` 仍在 current section 中以现时态把已激活 publication 描述为 planned / missing，与同文档当前 SSOT 和真实 route 直接矛盾。该 P2 finding 违反 AC18 / AC19，必须返回实现修复 durable docs 并补定向回归检查，之后重新执行完整 Phase 2。
