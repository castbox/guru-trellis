# 阶段二检查原始报告

## 1. 检查身份与范围

- 检查角色：`trellis-check` 阶段二独立检查代理。
- Issue：`castbox/guru-trellis#131`。
- Task：`.trellis/tasks/07-23-131-guru-review-branch`。
- Worktree：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/131-guru-review-branch`。
- Branch：`codex/131-guru-review-branch`。
- Intake base：`main` @ `ea132e350c4b6861fc955f17e590651a46e890ab`。
- 检查 HEAD：`ea132e350c4b6861fc955f17e590651a46e890ab`，检查对象为该 HEAD 上的完整未提交实现 diff。
- Planning approval：`approved`，来源为 `explicit-post-planning-review`；检查开始时确定性 approval validator 通过。
- Docs SSOT strategy：`ssot_first`。
- `check.jsonl` 仅含 seed row，因此按检查协议回退到 task planning artifacts 与 `implement.jsonl` 的 11 个 curated spec。

检查覆盖了：

- `prd.md`、`design.md`、`implement.md`、`implementation-handoff.md`。
- `.trellis/spec/workflow/**`、`.trellis/spec/preset/**`、`.trellis/spec/docs/public-docs.md` 与相关 guide。
- `guru-review-branch` canonical package、installed package、Codex/Claude/Cursor platform package。
- production runtime、recorder/checker/public projection、native eval adapter、schema、migration manifest、registry。
- workflow、continue entry、preset overlay、ownership inventory、installer、公开文档与测试。
- 官方 Trellis `index.md`、custom workflow 与 custom spec template marketplace 文档。

禁止改动的现有 Phase 2 reviewer 路径在检查结束前保持零 diff：

- `.trellis/agents/check.md`
- `trellis/presets/guru-team/overlays/.trellis/agents/check.md`
- `.agents/skills/trellis-check/**`
- `.codex/agents/trellis-check.toml`
- `.claude/agents/trellis-check.md`
- `.cursor/agents/trellis-check.md`

## 2. 候选问题资格判定

| ID | 正常路径可复现 | 需求依据 | 处置 | 严重级别 |
| --- | --- | --- | --- | --- |
| C-001 | 是；规划文档发生正常修订后，planning approval validator 已判 stale，但 public invocation 仍返回 `passed` | PRD R3、R9；design §5、§8.3 | `qualified_finding` | P1 |
| C-002 | 是；正常缺少 task commit handoff，或正常 evidence stale 时，13 项入口闭环与声明的 `blocked` 路由均不成立 | PRD R3、R7、R9；design §5、§10.1、§11.2 | `qualified_finding` | P1 |
| C-003 | 是；AI 正常误写 `owner_round` 与 `closure_evidence` 时，recorder、checker 与 public invocation 均接受 | PRD R6、R9；design §6.3、§8.2 | `qualified_finding` | P2 |

下列项目未升级为 finding：

- 当前 feature branch 未推送，故不能用精确远端 feature ref 执行 marketplace 安装；这是当前授权边界内的验证限制，不是实现缺陷。已使用公开 marketplace discovery 加本地未发布 workflow sample 完成 throwaway 验证。
- npm 已有 Trellis CLI `0.6.8`，但本 task 明确批准和测试的 baseline 是 `0.6.5`；不把未授权的新版兼容扩展为当前 scope。
- 需要恶意伪造、手工攻击 artifact、TOCTOU 或并发压力才能构造的场景均为 `out_of_scope`，未用于 finding。

## 3. 未修复问题

### F-131-01 — P1：Public invocation 未重新验证 planning freshness

复现目录：

`/tmp/guru-review-branch-eval.vkdCkb/current/workflow-passed/execution/owner-repo`

复现过程：

1. 使用真实 eval 生成的通过态仓库执行 package public invocation，得到 `passed`。
2. 对 `.trellis/tasks/current/prd.md` 增加一次正常规划修订。
3. 执行 `check-planning-approval.sh --json --task .trellis/tasks/current`，退出码为 2，并报告 `contract_wording_scope_stale`、`prd` SHA/size mismatch、reviewed artifacts 已过期、requirement authority stale。
4. 再次执行精确 public wrapper，退出码仍为 0，结果仍为 `{"exit_id":"passed", ...}`。

根因：

- `production_owner_result()` 只调用 `cmd_check_review_gate()`。
- `review-gate` artifact 没有绑定 planning、Phase 2、ledger 与 task commit evidence 的当前 digest。
- `cmd_check_review_gate()` 没有重新执行设计声明的 13 项 entry preconditions。

影响：

- 已通过 gate 可在 planning 内容正常变化后继续投影为 `passed`，违反 fail-closed freshness 与 public invocation contract。

建议修复：

- 在 owner-result/public invocation checker 路径中重新验证全部 entry preconditions，或使 review gate 对这些上游 evidence 建立可确定性重验的 freshness binding。
- 增加“先通过、再正常修改 planning、随后调用 public invocation 必须非 `passed`”的真实负例测试。

### F-131-02 — P1：13 项入口闭环和声明的 stale `blocked` 路由未实现

复现 A：缺少 task commit handoff

复现目录：

`/tmp/guru-review-branch-eval.vkdCkb/current/standalone-passed/execution/owner-repo`

将当前 task 的 `.trellis/tasks/current/task-commit-plans/001.json` 移出 task 后，执行 `review-branch.sh --pass ... --dry-run` 仍退出 0，并构造 passing gate。`cmd_review_branch()` 未检查 current `guru-create-task-commit` evidence。

复现 B：stale evidence 不能形成声明的 `blocked` typed exit

复现目录：

`/tmp/guru-review-branch-eval.vkdCkb/current/blocked-stale/execution/owner-repo`

对 `prd.md` 做正常修订使 planning approval stale 后，执行 package `review-branch.sh ... --typed-exit blocked --dry-run`。命令在写 owner result 前退出 2，只输出 planning stale 错误。由于 package contract 又要求 checker-passed owner artifact 才能由 wrapper 发出 typed exit，因此该正常 stale 场景得到的是 invocation error，而不是接口声明的 `blocked` DTO。

现有 eval 的覆盖缺口：

- 名为 `blocked-stale` 的 corpus case 在 native adapter 中先创建 fresh planning、Phase 2、commit、assignment 与 report，再人工记录 semantic `typed_exit=blocked`。
- 因此 7/7 eval 通过没有验证“上游 evidence 实际 stale 时返回 `blocked`”这一命名场景。

影响：

- 核心入口安全合同缺少 task commit evidence。
- 声明的 `blocked` closed-loop route 对真实 stale evidence 不可达，consumer 无法按稳定 typed exit 恢复。

建议修复：

- 在 entry checker 中验证 current task commit handoff 的 identity/freshness。
- 明确区分“合法 semantic blocked owner result”与“entry evidence stale”的 recorder/checker 顺序，使 stale 正常路径可产生接口承诺的稳定结果，或修订接口并提供兼容合同。
- 将 `blocked-stale` eval 改为真实制造上游 stale，而不是只预填 `typed_exit=blocked`。

### F-131-03 — P2：Finding closure 未绑定到 assignment/report 客观证据

复现目录：

`/tmp/guru-review-branch-eval.vkdCkb/current/finding-fix-passed/execution/owner-repo`

该真实生成仓库的 assignment 只有 round 1、2、3 及对应报告。对 owner input 做一次正常 AI authoring error：

- `owner_round` 从 `1` 改为不存在的 `99`。
- `closure_evidence` 从 `reviews/round-002-closure.md` 改为不存在的 `reviews/nonexistent-closure.md`。

随后执行实际 package recorder、checker 与 public wrapper：

- recorder：退出 0；
- checker：退出 0，`typed_exit=passed`；
- public wrapper：退出 0，返回 `passed`。

根因：

- `review_branch_semantic_payload` 与 v2 schema 仅验证整数/非空字符串形状。
- `validate_review_gate()` 未将每个 semantic finding 的 `owner_round`、`closure_evidence` 与 `agent-assignment.json.review_rounds[]`、真实 raw report path/digest 交叉校验。
- 通用 final-review checker 只能证明“存在某个 closure round”，不能证明“该 finding 的 closure evidence 属于已登记且当前的 review round”。

影响：

- 正常 AI 写错 round 或报告路径时，finding 仍可被记录为已闭环并最终 `passed`，不满足 finding lifecycle evidence binding。

建议修复：

- recorder/checker 对每个 finding 的 round 和 closure report 做 assignment membership、路径存在性、报告 identity/digest 与 closure status 绑定。
- 增加不存在 round、不存在报告、报告 digest stale 的正常负例测试。

## 4. 已修复问题

- 无。
- 三项 finding 均涉及 runtime/schema/eval/test 的行为合同，不属于可由阶段二 reviewer 机械自修的小问题；为避免 reviewer 扩大实现范围，本轮未修改实现文件。
- 仅新增本 task-local 原始检查报告。

## 5. 验证结果

| 验证项 | 结果 |
| --- | --- |
| `python3 trellis/skills/guru-team/packages/guru-review-branch/tests/test_contract.py` | 通过，8 tests |
| `run-skill-evals.sh ... --skill guru-review-branch --adapter shared` | 通过，7/7；但 `blocked-stale` 存在 F-131-02 所述语义覆盖缺口 |
| source package validator | 通过，active 10 / exits 39 / targets 23，planned #116 |
| installed package validator | 通过，active 10 / exits 39 / targets 23，1903 managed files，0 sidecar/removal/conflict |
| `python3 trellis/skills/guru-team/tests/test_skill_packages.py` | 通过，166 tests |
| `python3 trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py` | 通过，557 tests，13 skipped |
| `python3 trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py` | 通过，45 tests |
| `python3 trellis/presets/guru-team/scripts/python/test_upstream_ownership.py` | 通过，6 tests |
| `check-dogfood-overlay-drift.sh` | 通过，43 active ownership entries、10 active/1 planned skills、48 assets |
| `validate_upstream_ownership.py --repo . --json` | 通过 |
| `task.py validate .trellis/tasks/07-23-131-guru-review-branch` | 通过，implement 11 / check 0 |
| repo JSON parse | 通过，2629 files |
| Bash `-n` syntax | 通过，295 files |
| Python compile（临时 `PYTHONPYCACHEPREFIX`） | 通过，70 files |
| `git diff --check` | 通过 |
| canonical/installed/shared/Codex/Claude/Cursor package tree diff | 通过，零差异 |
| 禁止路径 diff | 通过，零差异 |
| sidecar scan | 通过，零结果 |
| throwaway install/update/reapply | 通过；公开 marketplace discovery + 本地未发布 workflow sample，覆盖 0.6.5 `update --force` 与 preset 重应用 |

Lint 说明：

- 仓库未提供统一 lint 命令；已完成 `git diff --check`、JSON parse、Bash syntax、Python compile、package validators 与完整相关测试。
- 当前环境未安装 `ruff`、`shellcheck`。

TypeCheck 说明：

- 仓库未配置可执行的类型检查门禁，当前环境也无 `mypy`、`pyright`；本项记为“不适用”。
- Python compile 与 557 个 runtime tests 已通过，但不能替代上述语义 finding。

## 6. Docs SSOT reconciliation

- Plan strategy：`ssot_first`。
- Durable docs 已覆盖 `README.md`、`docs/requirements/**`、`.trellis/spec/workflow/**`、`.trellis/spec/preset/**`、`.trellis/spec/docs/public-docs.md`、workflow/preset README。
- Canonical、dogfood 安装副本、platform package 与 overlay 的结构和字节一致性验证通过；task handoff 声明 task delta 已合并。
- 但 durable docs、planning 与 implementation handoff 当前宣称“13 项 entry preconditions、freshness、finding closure 已闭环”，与 F-131-01 至 F-131-03 的真实 runtime 行为不一致。因此 current-scope Docs SSOT reconciliation 不成立，是阶段二放行阻塞项。
- 本 task 没有 CI/CD、container、Kubernetes、database migration、Makefile 或业务 service 变更。
- 远端精确 feature-ref marketplace 验证因当前分支未推送而未执行；不把公开 `main` 当作当前实现。完整 publication 前仍需在已授权 push 后复验精确 ref。

## 7. 证据交接与结论

- 本报告覆盖完整未提交实现 diff、task artifacts、curated specs、官方 Trellis 扩展文档、durable docs、canonical/installed/platform copies、runtime、schema、config、installer 与 tests。
- 自动化测试全部通过，但存在 2 个 P1、1 个 P2 的正常路径可复现 finding；这些问题说明现有测试未覆盖关键 semantic contract。
- 本报告不能支撑 passing `phase2-check.json`。
- 建议 `guru-check-task` typed exit：`implementation_required`。
- 应由 implement owner 修复 runtime/schema/eval/test 与 Docs SSOT，再重新执行完整 Phase 2 check。

