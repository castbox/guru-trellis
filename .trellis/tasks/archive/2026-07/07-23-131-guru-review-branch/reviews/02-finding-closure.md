# Issue #131 Branch Review 问题闭环原始报告

## 审查身份与固定范围

- 逻辑角色：`问题闭环审查代理`，round 2。
- Technical agent：`/root/issue_131_branch_review_discovery`。
- Continuity：复用 round 1 finding owner，已记录
  `reuse-for-closure`，`from_round=1`、`to_round=2`。
- 禁止角色：本代理不是、也不能担任最终放行审查代理。
- Task：`.trellis/tasks/07-23-131-guru-review-branch`。
- Base：`origin/main`。
- Reviewed HEAD：`0fdbb708f91296847b5812c3c1b9dd80b6e488a2`。
- 完整范围：
  `origin/main...0fdbb708f91296847b5812c3c1b9dd80b6e488a2`。
- Merge base：`ea132e350c4b6861fc955f17e590651a46e890ab`。
- 完整 diff：312 files changed，32197 insertions，933 deletions。
- Finding-fix commit：
  `0fdbb708 fix(workflow): #131 闭环分支审查问题`；
  parent 为 `cdf0fa47d3d6f508851b9c0e91260276d9fde8f5`。
- Workspace boundary：`status=ok`；expected workspace 与 actual repo root
  均为当前 task worktree；source checkout clean；suspicious source artifacts 为 0。
- 审查开始时仅存在 main-session 已登记的 task metadata tail：
  `agent-assignment.json` 与 `task-commit-plans/002.json`。

本轮仅写本 raw report；未修改实现、测试、规划、Phase 2、
`review.md`、`review-gate.json`、assignment、task commit plan，未 commit、push 或
创建 PR。

## 当前权威与证据重读

本轮重新读取而未复用旧 pass 结论：

- live GitHub Issue `castbox/guru-trellis#131` 正文与 accepted-current comment；
- approved `prd.md`、`design.md`、`implement.md`；
- schema 2.0 `planning-approval.json`，其 `typed_exit=approved`，三份 planning
  SHA-256 仍精确匹配；
- current `phase2-check.json`，其 `typed_exit=passed`；
- `implementation-handoff.md`、四份 Phase 2 raw report、issue scope ledger、
  current task commit evidence；
- round 1
  `reviews/01-problem-discovery.md` 与旧 `review.md` / `review-gate.json`；
- `guru-review-branch` canonical package、installed package、四平台 mirrors、
  runtime、schema、eval adapter、tests；
- relevant workflow/data/package/preset durable contracts；
- 完整新 committed range，而非只审查 finding-fix commit。

Qualification 继续遵循 Issue #131：只有
`normal_required_behavior`、`explicit_nonstandard_requirement`、
`approved_nonstandard_expansion` 且真实违反当前合同时才赋 P0-P3；未确认扩张、
威胁模型、恶意伪造、TOCTOU、额外 fault injection、crash consistency 与跨 OS
atomicity 不进入 current finding。

## Round 1 四项 finding closure

### F-131-BR-01 — 已关闭

- 原 finding：合法 `decision=replace` replacement closure 被 v2 finding lifecycle
  拒绝。
- 修复路径：
  `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`。
- Closure evidence：
  - semantic lifecycle 现复用既有
    `finding_round_has_replacement_closure()`；
  - source `finding-fix-passed` real-wrapper fixture 包含完整
    `failed -> replacement-started -> completed` chain、
    `reuse_decisions[].decision=replace`、closure round
    `reuse_decision=replace`；
  - 真实 public wrapper 返回 `exit_id=passed`；
  - 直接执行 lifecycle，完整链返回 `[]`；移除 replacement reviewer 的
    `completed` event 后，返回缺少 replacement linkage 与 current bound closure
    evidence。
- 结论：原 P1 正常恢复阻断已真实关闭。

### F-131-BR-02 — 已关闭

- 原 finding：entry 把所有 `.trellis/tasks/` / `.trellis/.runtime/` dirty 路径
  当作允许的 current review metadata。
- 修复路径：
  `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`。
- Closure evidence：
  - allowlist 已收敛为 current task 的 assignment/rollup/gate、assignment-registered
    direct `reviews/*.md`、唯一绑定 current HEAD 的 committed task plan，以及
    invocation-declared regular Guru runtime input；
  - 在 fresh source `workflow-passed` owner repo 中重跑 round 1 原复现：
    新增 `.trellis/tasks/unrelated/ordinary-note.md` 后，真实 installed wrapper
    不再返回 `passed`，而返回最小 `{"exit_id":"blocked"}`；
  - focused regression 同时拒绝 current-task ordinary file、unregistered report、
    undeclared runtime input，并接受精确 owner metadata/direct runtime input。
- 结论：原 P2 目录级过宽放行已真实关闭。

### F-131-BR-03 — 已关闭

- 原 finding：current-scope candidate 经证据证明无缺陷后无法记录为
  `rejected_candidate`。
- 修复路径：
  runtime semantic normalizer、review gate schema、package contract/example、
  eval adapter及各分发副本。
- Closure evidence：
  - 直接重跑 round 1 的
    `normal_required_behavior` no-defect payload，当前
    `review_branch_semantic_payload()` 成功返回无 `severity`、无
    `finding_ref` 的 `rejected_candidate`；
  - focused regression 覆盖三个 current-scope scenario；
  - 向 rejection 添加 `severity` 或 `finding_ref` 仍被拒绝；
  - source/installed production corpus 都实际承载 current-scope rejections。
- 结论：原 P2 qualification evidence 表达缺口已真实关闭。

### F-131-BR-04 — 已关闭

- 原 finding：完整 committed diff 未通过计划要求的 `git diff --check`。
- Closure evidence：

  ```text
  git diff --check origin/main...0fdbb708f91296847b5812c3c1b9dd80b6e488a2
  ```

  返回 exit code 0、无输出。旧
  `phase2-worker-report.md:200` EOF 多余空行已从新 commit 删除。
- 结论：原 P3 已在精确新 committed range 关闭。

## 新 candidate 资格化

| Candidate | Affected behavior | Scenario | Disposition | Severity |
| --- | --- | --- | --- | --- |
| `C-131-BR2-01` | replacement lifecycle 可用任意合法 replacement round 为另一个、未链接的 `closure_evidence` report 背书 | `normal_required_behavior` | `qualified_finding` | P2 |
| `C-131-BR2-02` | exact remote feature-ref marketplace install 尚不可执行 | `out_of_scope` / publication limitation | `followup_candidate` | 无 |
| `C-131-BR2-03` | hostile tamper、恶意绕过、TOCTOU、额外并发/原子性加固 | `out_of_scope` | `rejected_candidate` | 无 |

## 新 P0-P3 Finding

### F-131-BR2-01 — P2：replacement closure helper 未绑定当前 `closure_evidence` round

- Scenario class：`normal_required_behavior`。
- Requirement refs：
  - PRD R6：每个 finding owner 必须有 fresh closure evidence；
  - PRD R9 / Design 7.2：finding lifecycle 必须记录并验证 closure evidence；
  - package contract：每个 qualified finding binds closure evidence，missing、
    digest mismatch 或 lifecycle mismatch 必须 block。
- Affected path：
  `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:12855-12883`。
- Qualification reason：
  当前实现对正在遍历的 `closure_evidence` report 完成 path、role、round 与 digest
  校验后，调用
  `finding_round_has_replacement_closure(assignment_payload, rounds, owner, final_round)`
  检查 owner 在 final 前是否存在 **任意** 合法 replacement closure。调用没有传入
  当前 `closure_number`，随后只要任意链有效便设置 `matched_closure=True`。因此合法链
  不必对应 semantic finding 实际引用的 raw report。
- 正常路径复现：
  1. 使用 current source `finding-fix-passed` 真实 owner repo；
  2. 保留 round 1 finding owner 与 round 2 完整、合法 replacement closure；
  3. 加入一个具有真实 task-local raw report及当前 digest、但没有从 round 1
     linkage 的另一 closure round 3；fresh final reviewer 移到 round 4；
  4. 把 `F-001.closure_evidence` 指向 round 3，而不是合法 round 2；
  5. 执行真实 validators，结果为：

  ```text
  validate_agent_assignment_payload = []
  final_review_round_errors = []
  review_branch_finding_lifecycle_errors = []
  ```

  该场景只需要正常多 finding/multi-closure round 与普通引用错误，不需要恶意伪造、
  手工虚假 digest、攻击 artifact、TOCTOU 或并发压力。额外 report 是真实 regular
  task-local file，digest 由当前 runtime计算。
- Impact：
  Gate 可以接受与 finding 无 linkage 的 raw report 作为该 finding 的
  `closure_evidence`。虽然同一 owner 的另一个合法 replacement closure 实际存在，
  public route不会因此在完全无 closure 时误通过，但 per-finding audit/evidence
  binding 与“current bound closure evidence”声明不真实，后续人工审查会读取错误的
  closure report。
- Severity：
  P2。它破坏 Branch Review 核心 lifecycle evidence correctness，但复现中仍存在
  一个真实合法 closure，因此没有升级为使未修 finding直接通过的 P1。
- 建议修复：
  replacement helper 必须验证当前正在处理的 exact closure round，例如接收
  `expected_closure_round`，或返回匹配的 closure round identities并要求包含当前
  `closure_number`；增加“两条 closure round，semantic 引用未链接那条”的负例，
  要求 lifecycle 返回错误。

## 验证结果

| 验证项 | 本轮结果 |
| --- | --- |
| `git diff --check origin/main...0fdbb708...` | passed |
| Focused finding closure tests | 5/5 passed |
| `guru-review-branch/tests/test_contract.py` | 8/8 passed |
| Source shared real-wrapper eval | 7/7 passed |
| Installed shared real-wrapper eval | 7/7 passed |
| `test_skill_packages.py` | 167/167 passed |
| `test_guru_team_trellis.py` | 565 passed，13 skipped |
| Preset installer tests | 45/45 passed |
| Upstream ownership tests | 6/6 passed |
| Dogfood overlay drift | passed；43 frozen，10 active Skills，1 planned |
| Canonical/installed/Codex/Claude/Cursor package parity | passed |
| Canonical/installed runtime与adapter parity | passed |
| Forbidden upstream reviewer diff | 0 |
| Python compile（3个本轮相关 Python文件） | passed，使用外部临时 cache |
| Public package secret / local absolute path scan | 0 |
| Recursive `.new` / `.bak` / `.orig` scan | 0 |

Lint：

- 完整 committed-range `git diff --check`、Python compile、repo package/runtime/
  preset/ownership validators均通过；
- 环境未安装 `ruff` / `shellcheck`，仓库没有声明统一 lint command。

TypeCheck：

- 环境未安装 `mypy` / `pyright`，仓库未声明 executable type-check gate；不适用。

测试全部通过没有覆盖 `F-131-BR2-01` 的多 closure 错误引用组合，不能替代该
semantic finding。

## Docs SSOT、分发、部署与安全

- Docs strategy：`ssot_first`。
- 原四项 finding对应的 package contract、schema、runtime、tests、eval与 mirrors
  已同步；durable docs继续正确要求 exact closure evidence。
- `F-131-BR2-01` 是 runtime未完全承接现有 durable contract，不是新增产品需求，
  不需要 scope confirmation。
- Canonical、installed、`.agents`、`.codex`、`.claude`、`.cursor` package tree
  一致；upstream reviewer资产无 diff。
- 本 range 没有 CI/CD、container、Kubernetes、database migration、Makefile 或业务
  service deployment变更。`production-minimal-handoff.json` 是 Skill migration
  manifest，不是数据库 migration。
- Public package未发现 secret、credential、客户数据或本机绝对路径。Task-history
  artifacts中的 workspace路径不属于公共 package。
- 当前 branch未push，exact remote feature-ref marketplace install继续作为 publication
  前限制；默认门禁不得以 public `main` 冒充当前 feature ref。

## 结论

- Round 1 findings：
  - `F-131-BR-01`：closed
  - `F-131-BR-02`：closed
  - `F-131-BR-03`：closed
  - `F-131-BR-04`：closed
- Round 2 new findings：1
  - P0：0
  - P1：0
  - P2：1
  - P3：0
- Scope proposals：0。
- 建议 typed exit：`implementation_required`。
- 本报告不能支持 fresh final review或 Branch Review Gate `passed`。
- `F-131-BR2-01` 修复后必须重新执行完整 Phase 2、fresh finding-fix commit，并由
  本 round finding owner或合法 replacement形成新的 closure evidence。只有所有
  findings关闭后，才能 dispatch从未参与 round 1/2及后续 closure的全新最终放行审查代理。
