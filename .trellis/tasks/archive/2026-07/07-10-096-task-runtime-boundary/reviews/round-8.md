# Round 8 问题发现审查报告

## 审查身份

- 角色：Issue #96 新 HEAD 的问题发现审查代理。
- 技术身份：`019f4c1a-ea3d-78a2-8125-a55ae761c236`（Hypatia the 2nd）。
- 执行环境：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/096-task-runtime-boundary`。
- 审查方式：独立、只读复核完整累计 diff；不回退或修改实现、task metadata、既有 raw reports，不运行 installer、preset apply、mutation、recorder 或 Git mutation。
- 写入边界：只写本报告 `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/096-task-runtime-boundary/.trellis/tasks/07-10-096-task-runtime-boundary/reviews/round-8.md`。

## Reviewed HEAD 与 Diff

- Base：`origin/main` = `59d6c0caf404c4c927fe8aada92811d1ced907d5`。
- Reviewed HEAD：`4bbac759ab67e5975b56bc63f96c9e373282a6d5`。
- Reviewed diff：`origin/main...4bbac759ab67e5975b56bc63f96c9e373282a6d5`。
- 提交范围：完整七提交，依次为 `a84e572`、`90a2d45`、`f05cd66`、`9c54278`、`f48abcf`、`30f4f4a`、`4bbac75`。
- 审查开始及恢复时存在的非本代理工作树状态：`agent-assignment.json`、`review.md` 已修改，`reviews/round-6.md`、`reviews/round-7.md` 未跟踪；均未由本代理回退、覆盖或纳入本报告写入。

## 审查范围

- Live GitHub Issue #96 的任务启动上下文、本机运行态、workspace boundary、共享配置只读、普通 task 写入 allowlist、旧 handoff 公共 API 删除、installer cleanup、开箱安装与 upgrade/update 验收合同。
- Umbrella Issue #53 与 follow-up #97、#98、#99、#100 的 close/ref/followup 边界。
- `prd.md`、`design.md`、`implement.md`、`planning-approval.json`、`implementation-handoff.md`、`phase2-check.json`、`issue-scope-ledger.json`、`task-start-context.json` 与既有 raw review evidence。
- Canonical/dogfood workflow、helper、schema、config、extension manifest、preset installer、README、requirements、durable specs 与五平台 continue overlays。
- 新增跨 agent closure validator：`reuse_decisions[] decision=new-agent` 关系、链式 finding owner、same-agent `reuse-for-closure`、failure replacement、closure/finding owner 禁止 final、fresh final/current HEAD/zero findings。
- Phase 2 `247+30`、定向 8 项、临时 all-platform preset apply、active-reference mutation、dogfood drift、`.new/.bak`、Docs SSOT、安全、部署与远端 marketplace pending 证据。

## 已消费证据与只读核对

- 使用 GitHub API 读取 live Issue #96；issue 仍为 open，明确只关闭 #96，不关闭 #53，#97/#98/#99/#100 保持 follow-up。
- `git log`、`git diff --stat`、`git diff --name-only`、定向 `sed`/`rg`/`jq` 覆盖七提交和全部关键资产。
- Canonical 与 dogfood Python helper、workflow byte equal；五平台 continue canonical overlay 与 dogfood 文案均表达不同 fresh closure agent、精确关系、链式 finding owner 和 fresh final 规则。
- 活跃运行合同已移除固定 tracked `.trellis/guru-team/handoff.json`、`handoff_path`、`load_handoff`；旧 `intake-handoff.schema.json` 仅作为 installer obsolete-cleanup fixture 保留。`.trellis/.runtime/**` 无 tracked 实例。
- `task-start-context.schema.json` 使用字段白名单；当前 task context 为 repo-relative/portable 数据，不含绝对 worktree、完整 preflight、`existing_worktrees`、developer path 或 runtime path。
- Phase 2 artifact 记录 core `247`、preset `30`、closure 定向 `8`、compile/syntax/JSON/task/boundary/equality/drift/mutation/diff-check 与临时 all-platform preset apply 均通过，临时安装无 `.new/.bak`。本轮按只读约束消费这些证据，未重跑会写 repo 的命令。
- `issue-scope-ledger.json` 的 AC9 仍为结构化 `remote_marketplace_verification: pending`；pending 明确不满足 publish。发布流程要求 push reviewed content 后运行真实远端 verifier，再只提交 verifier artifact 与 ledger 两个 metadata tail 文件；本轮未把 pending 误判为 passed。
- Docs SSOT 已同步 canonical workflow、durable specs、README、requirements、preset README 与五平台 overlays；未发现 Issue #96 其余当前范围的文档漂移。

## Findings

### P1：Branch Review Gate 没有机器验证 closure 与 final reviewer 的 fresh 技术身份

- 位置：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:4161`、`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:4243`。
- 合同要求：workflow、durable specs、preset README 和五平台 continue overlays 均要求跨 agent closure 使用“different fresh”问题闭环代理，最终放行也必须是 fresh new agent；任何 finding owner 或 closure agent 不得 final。
- 当前实现：`finding_round_has_new_agent_closure()` 只要求 closure `agent_id != finding_agent`，未拒绝该 closure agent 已在更早 review round 出现；final freshness 只通过 `finding_owner_agents` 和 `closure_agents` 排除发现过 finding 或做过 closure 的代理，未拒绝一个更早以零 finding 普通 reviewer 身份出现过的相同 `agent_id` 再作为 final。
- 只读负向复现：调用 `final_review_round_errors(..., expected_head="head-final")` 时，以下两种 payload 均错误返回 `[]`：
  1. `agent-c` 先在 round 1 以问题发现审查代理记录零 finding，随后在 round 3 被标为 `new-agent` closure 来闭环 `agent-a` 的 round 2 finding；
  2. `agent-b` 先在 round 1 记录零 finding，随后同一 `agent_id` 在 round 2 被标为 fresh `最终放行审查代理`。
- 影响：只要 recorder 写出 `reuse_decision: new-agent`，已有 review agent 可冒充 fresh closure/final reviewer，Branch Review Gate 会错误接受不满足独立性合同的审查链。该缺陷直接削弱最终放行门禁，阻塞 Gate 与 finish/publish。
- 建议修复：在 final validator 中基于严格早期 round 集合验证 closure agent 在 `to_round` 之前未出现，final agent 在 final round 之前未出现在任何 review round；补充 closure/final 复用既有零 finding agent 的负向测试。若“fresh”还要求 assignment 级新分配，应同时把 `agents[]` 的 assigned order/event 关系纳入校验并在合同中明确。

### P1：`new-agent` closure 关系没有精确绑定 closure round 的 reuse 语义，且 round 字段未做严格整数校验

- 位置：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:4161`、`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:3830`。
- 合同要求：不同代理闭环必须由 closure round 自身的 `reuse_decision: new-agent` 与 `reuse_decisions[] decision=new-agent` 共同证明，并精确匹配 `from_round`、`to_round`、closure `agent_id`、role、reviewed HEAD 和非空 reason。
- 当前实现：`finding_round_has_new_agent_closure()` 没有检查 closure round 自身的 `reuse_decision`；只要另有匹配 decision，closure round 即使写成 `reuse` 仍会通过。`validate_agent_assignment_payload()` 也未验证 `reuse_decisions[].from_round/to_round` 的存在性与严格正整数类型；Python 中 `True == 1`，因此布尔 `from_round: true` 可匹配 round 1。
- 只读负向复现：以下 payload 调用 `final_review_round_errors()` 均错误返回 `[]`：
  1. closure round 的 `reuse_decision` 为 `reuse`，对应 `reuse_decisions[]` 却为 `decision: new-agent`；
  2. `reuse_decisions[].from_round` 为布尔值 `true`，仍被当作 round 1 精确关系接受。
- 测试缺口：现有 `test_final_review_round_errors_rejects_new_agent_closure_without_explicit_relation` 覆盖缺字段、错误 agent 和错误 round，但未覆盖 closure round/decision 语义不一致、布尔/非严格整数、role/head/reason 各字段的独立负向矩阵。
- 影响：手工编辑、合并冲突或非 recorder 生产的 task metadata 可以构造内部自相矛盾的 closure 关系并通过 Branch Review Gate；这违反“精确匹配、fail closed”的 gate artifact 合同，阻塞 Gate 与 finish/publish。
- 建议修复：要求 closure round `reuse_decision == "new-agent"`；对 `from_round/to_round` 使用 `is_strict_int()` 并要求正整数，再验证对应 source/target round 唯一存在、顺序正确；补齐 reuse mismatch、bool/string/null、role/head/reason mismatch 的负向测试。

## Finding 统计

- P0：0
- P1：2
- P2：0
- P3：0
- 总计：2 个阻塞 finding。

## Docs SSOT

- Issue #96 主合同的 canonical workflow、durable specs、README、requirements、preset README 和五平台 continue overlays 已同步。
- 当前问题不是文案缺失，而是文案明确声明的 fresh/精确 closure 与 final 合同未由 validator 完整执行；因此属于当前 scope 的实现 finding，不能降级为 observation。
- 修复 validator 后必须同步对应测试；若机器合同表述发生变化，再同步 canonical workflow/spec/preset/overlay 并重新 apply/drift 验证。

## 安全

- 本轮未发现 task-start-context 或 tracked runtime 中新增绝对路径、secret、token、`.env`、数据库 URL、签名 URL或客户数据泄露。
- 两个 finding 属于流程完整性与发布门禁安全：不 fresh 或内部不一致的 review metadata 可被错误接受，可能使未经合同要求的独立审查链进入 publish。

## 部署影响

- 七提交不修改业务运行服务、CI/CD、容器、K8s/Kustomize、数据库 migration 或 Makefile；无生产数据迁移和服务部署动作。
- 影响面是 Guru Team workflow/preset/companion validator 与多平台入口。修复后需重新执行 core/preset/定向 tests、all-platform preset apply、dogfood drift、mutation、静态检查与临时安装证据。

## Issue Scope

- `close_issues` 仅应包含 #96。
- #53 保持 related/open umbrella；#97、#98、#99、#100 保持 follow-up，不得使用 close 语义。
- 远端 marketplace AC9 继续保持真实 push 前 `pending`；不得在修复和重新审查前执行最终 publish，也不得创建稳定 release tag。

## 结论

- **不通过。** 当前 Reviewed HEAD `4bbac759ab67e5975b56bc63f96c9e373282a6d5` 存在 2 个 P1 finding，Branch Review Gate、finish-work 与 publish 必须阻塞。
- 请由实现代理修复 validator 与负向测试，重新完成 Phase 2；随后由新的问题闭环审查代理明确闭环本报告 findings。闭环通过后，才可调度全新的 final reviewer。
