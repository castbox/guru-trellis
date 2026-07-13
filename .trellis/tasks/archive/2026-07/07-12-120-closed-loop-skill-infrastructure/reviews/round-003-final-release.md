# #120 Branch Review 第 3 轮最终放行审查原始报告

## 审查身份与结论

- 审查角色：独立 `最终放行审查代理`
- 技术代理：`/root/branch_review_120_final`
- 复用决策：`new-agent`
- 审查轮次：`round-003`
- 结论：`blocked`
- 问题数量：`1`（P0=`0`，P1=`0`，P2=`1`，P3=`0`）
- 门禁判断：当前报告不能作为 Branch Review Gate final pass evidence；必须回到 Phase 2 修复不真实的验证命令证据，再由本 finding owner 做问题闭环审查，随后重新派发另一名 fresh 最终放行审查代理。

## 审查绑定

- GitHub issue：`castbox/guru-trellis#120`，live 状态为 `OPEN`；已读取 issue body 与 2026-07-13 scope clarification comment。
- 基线：`origin/main`
- 合并基点：`f14f167294154abffc0ef6124e0428911350b25b`
- 审查范围：完整 `origin/main...HEAD`
- 审查 HEAD：`5a1fb0412b68ef75fe05816c0eb29e1b1d417945`
- 变更规模：55 files，6439 insertions，47 deletions。
- 提交：`ea5d5e4 feat(trellis): #120 建立闭环 Skill Canonical 分发基础设施` 与 `5a1fb04 fix(trellis): #120 收紧闭环 Skill 发现与测试证据校验`；两条提交均具有中文事实正文和 `Refs #120`，没有 close keyword，commit message validator 通过。
- 工作区边界：审查前 `check-workspace-boundary.sh` 已绑定当前 task worktree；当前非提交变更全部是 task-local planning/gate/review metadata，没有未提交 source/docs/schema/test/preset 变更。

## P0-P3 问题清单

### P0

无。

### P1

无。

### P2-1：Phase 2 报告记录的全量测试命令客观上不执行任何测试

- 位置：`.trellis/tasks/07-12-120-closed-loop-skill-infrastructure/phase2-check.json` 的 `validation_commands[]`。
- 合同：Branch Review 必须验证 fresh Phase 2 evidence 的真实性与完整性；缺失、不准确或无法复现的 Phase 2 检查证据必须作为 finding 返回 earlier phase，不能用 Branch Review 当场测试替代 Phase 2 owner/checker 的审查记录。
- 记录事实：`phase2-check.json` 声明命令 `python3 -m unittest discover` 的结果为 `474/474 passed`。
- 独立复现：在精确 reviewed worktree 和 HEAD 上运行该命令，实际输出为 `Ran 0 tests in 0.000s`、`NO TESTS RAN`，退出码为 `5`。
- 对照事实：显式运行规划所列真实 suite 时，`trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py` 与 `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py` 为 `420/420 passed`；`trellis/skills/guru-team/tests/test_skill_packages.py` 为 `54/54 passed`，合计确为 `474/474`。这说明当前实现回归通过，但不能使错误的 Phase 2 命令记录变成真实证据。
- 影响：passing Phase 2 artifact 对“执行过什么”作出客观错误声明。后续 gate、PR readiness 与审计者无法从该 artifact 复现所谓全量检查，因此不能把当前 Phase 2 evidence 视为完整、真实的 release input。
- 修复要求：由 Phase 2 owner/checker 回到 Phase 2，按实际执行的两个显式 unittest 命令重录 fresh `phase2-check.json`，保留 `420/420`、`54/54` 与合计 `474/474` 的真实对应关系，并重新运行 Phase 2 validator。不得仅把字符串机械替换为通过结果；AI checker 必须确认所记录命令就是实际执行命令。
- 状态：`unresolved`。

### P3

无。

## 前两轮问题生命周期

- Round 1 P1（active package discovery frontmatter/tests evidence）：Round 2 已通过 strict frontmatter、package-local real tests、schema、fixture、distribution 与负向矩阵闭合；本轮独立执行 skill suite `54/54`，未重新打开该 finding。
- Round 1 P2（缺少 `ssot_first` implementation handoff/check evidence）：`implementation-handoff.md` SHA-256 为 `1a379090b4653d356ab2141b9522a33c63e230917d24eaa184b490b0b8f48263`，已记录 durable primary inputs、docs sync、task delta merge、task-history-only、验证与 PR limitation；未重新打开该 finding。
- AC11 后续冲突：live issue comment、fresh planning approval 与当前规划把公共资产禁令和 task-local workspace-boundary evidence 窄例外分开；本轮未发现该例外被用于掩盖 source/package/docs 泄漏，未重新打开该 finding。
- Round 1 finding owner `/root/branch_review_120_round1` 已以 Round 2 `问题闭环审查代理`、`reuse-for-closure`、`findings_count=0` 完成显式闭环。该代理没有被复用为本轮最终 reviewer。

## 最终审查证据

- 读取 live GitHub issue #120 body/comment、官方 custom skills/workflow/spec marketplace 文档、根 `AGENTS.md`、fresh `prd.md`/`design.md`/`implement.md`、planning approval、implementation handoff、Phase 2 check/findings、agent assignment、issue scope ledger、Round 1/2 raw reports、rollup 与 durable docs/spec。
- 独立审查 `origin/main...HEAD` 完整 55 文件 diff、两个 commit message、canonical/dogfood runtime、registry/interface schema、fixture-only active package、preset installer、managed hash、platform shrink/removal、tests、public API、README 和 throwaway verifier。
- `check-planning-approval.sh` 通过；批准来源是 `explicit-post-planning-review`，规划 artifact digest 与当前 bytes 一致。
- `check-agent-assignment.sh` 在 Round 3 写入前通过；Round 1 raw report SHA-256 `b8664f70ed00d5ca433c5a29ec5b1d55fa01f7741d1da8a46e34a57afc9dd93e`、size `10101`，Round 2 raw report SHA-256 `44240a2a92229ca7f8d4e5c4dbaef0bcb94ef1d60ca619fd9c63e6dcff447127`、size `10544`，均与 assignment 记录一致。
- `check-skill-packages --mode source` 通过：production `reserved_ids=[guru-create-work-commit]`、`active_ids=[]`、invoke/exit marker 均为 0。
- `check-skill-packages --mode installed` 通过：selected platforms 为 Claude/Codex/Cursor，managed files=3，sidecar/removal/conflict 均为 0。
- `check-dogfood-overlay-drift.sh` 通过；canonical/dogfood Python runtime 与 workflow 逐字节一致；没有 production fixture platform copy 或未处理 `.new/.bak`。
- 显式 Python suite `420/420 + 54/54 = 474/474` 通过；`py_compile`、相关 `bash -n`、`git diff --check origin/main...HEAD` 与 task metadata diff check 通过。
- 当前分支用默认公共 `main` source 运行 throwaway verifier 时，在安装前按预期退出 2，并明确报告 public marketplace 不能代表 current branch；exact feature-ref verification 没有被本地/public sample 冒充。
- 未运行 `review-branch.sh`、`check-review-gate.sh`、`record-agent-assignment.sh` 或任何 `record-*` recorder；本代理只写本 raw report 和更新 `review.md`。

## Docs SSOT 判断

- 批准策略为 `ssot_first`，`docs_state=partial_docs`。Durable requirements、`.trellis/spec/workflow/skill-package-contract.md`、preset/workflow/docs specs、根 README、workflow README 和 preset README 已承接 canonical root、registry lifecycle、strict discovery/test evidence、marker、managed hash、platform distribution、update/reapply 与公共 API。
- `implementation-handoff.md` 具体记录 durable docs 是 primary input、task delta 已合并、task-history-only 边界和 current PR limitation；代码/schema/tests 与 durable contracts 未发现第二套 owner 或当前矛盾。
- 本轮 P2-1 针对 Phase 2 验证命令事实，不重新打开已闭环的 Docs SSOT handoff finding。

## 安全与部署影响

- 安全：审查了 package/installed/platform 目标的 lexical containment、逐组件 `lstat`、symlink 拒绝、unknown edit preserve + `.new`、known upgrade + `.bak`、manifest inventory 与 public asset 数据边界。公共 package、fixture、manifest、example、公开 docs 和变更代码未发现真实本机绝对路径、secret、private key、credential URL、`.env` 值、客户数据或签名 URL；Round 1 中真实 worktree path 仅保留在 immutable task-local workspace-boundary evidence。
- 部署：没有 Dockerfile、Docker Compose、GitHub Actions、Kubernetes/Kustomize、数据库 migration、Makefile 或服务运行时入口变化，不需要同步这些部署资产。存在 extension version `0.6.5-guru.4`、public schema、validator、preset installed asset、platform discovery 和 manifest 变化，属于 extension 发布/安装影响。
- Stable/canary：durable docs 继续把 `v0.6.5-guru.2` 作为已发布 stable；本分支 `.4` 在 merge/tag/exact remote verification 前没有被宣称为 stable。

## Issue Scope 与发布边界

- `issue-scope-ledger.json` 只包含 primary/close issue #120；`related_issues=[]`、`followup_issues=[]`。当前 diff 没有实现或关闭 `guru-create-work-commit`、#98、#115 或其它具体 skill issue。
- `acceptance_evidence` 仍为空，符合 publish transaction 前 pending 语义；本轮 finding 未关闭前不得补写 close-ready 结论或关闭 #120。
- Exact remote feature-ref marketplace verification 必须在 reviewed content push 后绑定 remote branch/ref/HEAD 执行并进入 publish evidence；本轮确认默认 public `main` sampling 会 fail closed，因此该门禁被正确保留到 push 后。

## 观察项

- `phase2-check.json.validation_commands` 当前把真实的多模块显式测试简写成不可执行的 discover 命令，说明 recorder 输入仍需要 AI checker 对命令逐字复核；这是本轮 P2 finding 的审计教训，不是脚本应自行推断或修复的语义。

## 后续候选

- Branch Review raw report 在 digest 绑定前增加通用去敏/阻断门禁仍是独立基础设施候选；它不属于 #120 当前 close scope，也不能用于改写 Round 1 immutable evidence。

## 最终结论

当前实现和显式回归未发现代码级缺陷，但 Phase 2 passing artifact 包含 1 个可复现的 P2 证据错误。Round 3 最终放行审查结论为 `blocked`，禁止进入 passing Branch Review Gate、finish-work、push、PR 或 issue close。
