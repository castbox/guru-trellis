# #120 Branch Review 第 2 轮问题闭环审查原始报告

## 审查身份与结论

- 审查角色：`问题闭环审查代理`
- 代理复用：`/root/branch_review_120_round1`
- 复用决策：`reuse-for-closure`
- 审查轮次：`round-002`
- 结论：`closure-passed`
- 新问题数量：`0`（P0=`0`，P1=`0`，P2=`0`，P3=`0`）
- 闭环范围：round 1 的 P1/P2，以及后续 AC11 scope clarification。
- 身份边界：本代理在 round 1 发现问题后只能复用做 finding closure，不能再担任最终放行 reviewer；本报告不能单独形成 Branch Review Gate final pass。

## 审查绑定

- GitHub issue：`castbox/guru-trellis#120`，live 状态为 `OPEN`；已读取 2026-07-13 scope clarification comment。
- 基线：`origin/main`
- 合并基点：`f14f167294154abffc0ef6124e0428911350b25b`
- 审查范围：完整 `origin/main...HEAD`
- 审查 HEAD：`5a1fb0412b68ef75fe05816c0eb29e1b1d417945`
- 修复提交：`fix(trellis): #120 收紧闭环 Skill 发现与测试证据校验`
- Round 1 reviewed HEAD：`ea5d5e46686348b3006b9678eab7edfe735c31b3`
- Round 1 原始报告：`reviews/round-001-final-release.md`
- Round 1 immutable identity：SHA-256 `b8664f70ed00d5ca433c5a29ec5b1d55fa01f7741d1da8a46e34a57afc9dd93e`，size `10101`，mtime `2026-07-12T16:18:38.326684+00:00`；与 `agent-assignment.json.review_rounds[0]` 完全一致，本轮未修改其 bytes。

## 问题闭环

### Round 1 P1：active package discovery frontmatter 与 tests evidence 门禁缺失

- 原状态：`unresolved`。
- 当前状态：`resolved`。
- 代码证据：`skill_read_frontmatter()` 要求 `SKILL.md` 只有一个闭合 `---` frontmatter，只含 `name`/`description`；registry/interface/SKILL name 均绑定 stable skill id，description 非空并与 interface 精确一致。`tests[]` 被限制为 unique package-relative `tests/<file>`，并经过 safe-relative、tests root、存在性、regular-file 与逐组件 `lstat` 校验。
- Schema 证据：registry active `name` 复用 public skill id schema；interface `name` 使用 stable id pattern，`tests[]` 使用 unique path array 并拒绝 parent traversal。Canonical、fixture 与 dogfood installed schema/runtime bytes 一致。
- Fixture/分发证据：`guru-example-action` 新增真实 `tests/test_contract.py`；interface 指向该文件；installer distribution tests 证明 test evidence 进入 shared/Codex runtime copy 和 manifest `files[]`。Production registry 仍只有 `guru-create-work-commit` reserved，没有 fixture 或 active production package 泄漏。
- 独立复现：valid fixture 返回 `passed`；空 `SKILL.md`、虚构 `tests/does-not-exist.py`、frontmatter name drift、`tests/../outside.py`、symlink test evidence 均返回 structured `failed`，并给出对应 frontmatter/path/symlink error。
- 回归：`test_skill_packages.py` 覆盖 empty/fictitious、missing/unclosed/duplicate/extra frontmatter、name/description/whitespace drift、tests outside/missing/symlink/wrong type/duplicate/parent traversal。
- 闭环判断：round-1 P1 的两个独立复现均已由机器可验证合同阻断，且 package tests 随分发 inventory 管理；问题闭合。

### Round 1 P2：缺少可审计的 `ssot_first` implementation handoff/check evidence

- 原状态：`unresolved`。
- 当前状态：`resolved`。
- 实现交接：新增 `implementation-handoff.md`，明确 strategy=`ssot_first`、durable docs primary inputs、confirmed task delta、durable docs sync result、task delta merge、task-history-only 内容、代码/schema/tests/installer carryover、验证结果、follow-up 与 current PR limitation。
- Phase 2 复核：fresh `phase2-check.json` 将上述 handoff 以 SHA-256 `1a379090b4653d356ab2141b9522a33c63e230917d24eaa184b490b0b8f48263`、size `8921` 绑定为 checked artifact，并由独立 checker `/root/trellis_check_120_scope` 明确复核 `ssot_first`、Docs SSOT reconciliation、AC11 与完整 code/schema/test/install 范围，结论 P0-P3 为 0。
- 文档一致性：durable requirement、`.trellis/spec/workflow/skill-package-contract.md`、根 README、workflow README、preset README、schema、runtime 和 tests 对 strict frontmatter/test evidence 使用同一合同；未发现第二套 canonical owner。
- Freshness：planning docs、fresh planning approval、implementation handoff、phase2 findings、round-001 report 与 phase2 recorded digest/size 均匹配当前 bytes。`agent-assignment.json` 在 Phase 2 check 后因本轮 closure reviewer liveness snapshot 发生允许的 post-check mutable 更新；不是 source/docs/test drift，也未改变 Phase 2 checker completion 或 round-001 identity。
- 闭环判断：不再只有 `coverage.docs_ssot=true` 泛化断言，implementation owner 与 checker 的具体、可审计 evidence 已存在并互相绑定；问题闭合。

### 后续 AC11 scope clarification

- 触发：immutable round-001 report 的 workspace-boundary 字段包含真实 task worktree path，旧 AC11 又一概禁止 task artifact 的本机绝对路径。
- Live scope evidence：issue #120 comment 明确区分公共资产、去身份化负向 fixture 与 task-local workspace-boundary gate evidence；根因定性为“系统性风险、条件性显现”，并要求 round-001 immutable。
- Fresh planning：修订后的 `prd.md`、`design.md`、`implement.md` 由 schema 1.2 planning approval 重新绑定；`ambiguity_review.status=passed`、`unchecked_normative_hits=[]`，确认来源为 `explicit-post-planning-review`。
- 当前合同：production code、公共 package、fixture、manifest、example 和公开文档不得包含 secret、真实本机绝对路径、workspace journal 或业务私有状态；去身份化拒绝 fixture 不等于真实本机状态；task-local gate evidence 仅在绑定 reviewed workspace boundary 时允许记录真实 worktree path，且仍禁止 secret、客户数据、签名 URL、`.env`、workspace journal 和业务私有状态。
- Scope 边界：pre-bind raw report 通用 sanitizer/validator 是 Branch Review 基础设施独立 follow-up，不在 #120 canonical skill package close scope；当前 diff 未实现该能力，也未静默扩大脚本的 AI 判断职责。
- 安全扫描：公共 package、fixture、manifest、公开 docs 与变更代码未发现真实本机绝对路径、secret、private key、credential URL、`.env` 值、客户数据或签名 URL。Round-001 的 workspace path 保持 task-local immutable evidence，未改写。
- 闭环判断：live issue、fresh planning、Phase 2 check、immutable evidence 和当前 diff 对 AC11 只有一种解释；后续 scope clarification 闭合。

## P0-P3 结果

### P0

无新问题。

### P1

无新问题；round-1 P1 与 AC11 scope clarification 已闭合。

### P2

无新问题；round-1 P2 已闭合。

### P3

无新问题。

## 完整审查证据

- 读取 live issue body/comment、fresh planning approval、`implementation-handoff.md`、fresh `phase2-check.json`、`phase2-findings.json`、immutable round-001 report、`agent-assignment.json`、issue scope ledger、task planning 和 curated specs。
- 审查 `origin/main...HEAD` 完整 55 文件 diff，并重点审查 `ea5d5e4..5a1fb04` 的 runtime/schema/fixture/tests/durable docs/dogfood 修复。
- 官方 live custom skills docs 确认平台通过 `SKILL.md` YAML frontmatter 的 `name`/`description` 发现 skill；当前 plain two-field 合同是兼容官方 surface 的团队收紧合同，不修改 Trellis upstream。
- 独立运行 skill/preset/companion Python suites：474/474 通过。
- 独立临时 fixture 正负矩阵：1 个 valid 通过，5 个 invalid 场景按预期失败。
- `py_compile`、相关 `bash -n`、changed/current JSON parse、`git diff --check` 通过；canonical/dogfood runtime 与 schema byte comparison 通过；无 `.new/.bak`，无 production fixture platform copy。
- 未运行 `review-branch.sh`、`record-agent-assignment.sh`、`record-*` 或其它 Branch Review recorder；round-2 assignment/reuse/report digest 的确定性记录留给主会话在 raw report 写入后执行。

## 提交、关闭范围、安全与部署

- 两个 work commit 都使用中文 Conventional Commit subject/body 和 `Refs #120`，未使用 close keyword；本轮不 commit/push/PR/finish。
- `issue-scope-ledger.json` 仅有 #120 primary/close candidate，related/followup 为空；`guru-create-work-commit`、#98、#115 和其它具体 skill 未实现或关闭。
- 无 Docker、K8s、DB migration、Makefile 或服务运行时部署影响；存在 public schema、validator、preset installed asset、platform package inventory 与 extension release 影响。
- Stable/canary 文案仍将 `v0.6.5-guru.2` 作为已发布 stable，并明确 `.4` 在 merge/tag/远端验证前不是 stable。
- Exact remote feature-ref marketplace verification 仍须在 reviewed content push 后由 finish-work verifier 绑定 remote branch/ref/HEAD；本地 throwaway/public `main` sample 不能替代。

## 报告写入前文件状态

Round-002 raw report 创建及 `review.md` 更新前，`git status --short` 为：

```text
 M .trellis/tasks/07-12-120-closed-loop-skill-infrastructure/agent-assignment.json
 M .trellis/tasks/07-12-120-closed-loop-skill-infrastructure/design.md
 M .trellis/tasks/07-12-120-closed-loop-skill-infrastructure/implement.md
 M .trellis/tasks/07-12-120-closed-loop-skill-infrastructure/phase2-check.json
 M .trellis/tasks/07-12-120-closed-loop-skill-infrastructure/phase2-findings.json
 M .trellis/tasks/07-12-120-closed-loop-skill-infrastructure/planning-approval.json
 M .trellis/tasks/07-12-120-closed-loop-skill-infrastructure/prd.md
?? .trellis/tasks/07-12-120-closed-loop-skill-infrastructure/implementation-handoff.md
?? .trellis/tasks/07-12-120-closed-loop-skill-infrastructure/review.md
?? .trellis/tasks/07-12-120-closed-loop-skill-infrastructure/reviews/
```

该状态的文本快照 SHA-256 为 `587f5eeef29b262f30a63b57d9212b21902023dc87063b48b9f5bacafb9ff108`。其中 task-local fresh evidence 与 round-1 artifacts 均为主会话流程资产；本代理只新增本 raw report 并更新 rollup。

## 结论与下一步

Round 2 finding closure 通过，当前未解决问题数为 0。主会话应在本报告写入后记录 `logical_role=问题闭环审查代理`、`reuse_decision=reuse-for-closure` 和 report digest，再派发未参与实现、Phase 2、round 1 或 round 2 的 fresh `最终放行审查代理` 审查最新完整 diff。本代理不得被用于最终放行。
