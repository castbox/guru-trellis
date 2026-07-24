# Issue #131 Branch Review Round 5 问题发现原始报告

## 角色重入说明

- 逻辑角色：`问题发现审查代理`，round 5。
- Technical agent：`/root/issue_131_branch_review_final`。
- Reuse decision：assignment 已记录 round 4 → round 5 `decision=reuse`。
- Re-entry purpose：将同一 technical agent 在 fresh final review 中独立发现的
  `F-131-BR4-01` 重录为 finding owner evidence，使 qualified finding owner 使用
  lifecycle 接受的 `问题发现审查代理` 角色。
- 本报告不是新的语义审查，不新增或改写 finding，不改变 severity、资格化、HEAD、
  range、验证或 typed exit。
- Round 4 完整原始报告仍为：
  `reviews/04-final-release.md`，SHA-256
  `7701f3157748a3550a6dca780341461d952aad210e2a924fda61722c1f8a56f2`。
  本报告只引用它，不替代、覆盖或篡改它。
- 本 agent 后续可以按已记录 policy 仅作为 `问题闭环审查代理` 复核本 finding；
  不得再次担任后续最终放行审查代理。

## 固定审查范围

- Task：`.trellis/tasks/07-23-131-guru-review-branch`。
- Base：`origin/main`。
- Base HEAD / merge base：
  `ea132e350c4b6861fc955f17e590651a46e890ab`。
- Reviewed HEAD：`38a0e8dd2314b086378e0674f4bd377dc5e6f694`。
- 完整范围：
  `origin/main...38a0e8dd2314b086378e0674f4bd377dc5e6f694`。
- 完整 diff：315 files changed，33022 insertions，933 deletions。
- Workspace boundary：expected workspace 与 actual repo root 均为当前 task
  worktree；source checkout clean；suspicious source artifacts 为 0。

本轮只写本 raw report。未修改实现、测试、规划、durable docs、Round 4 报告、
`review.md`、`review-gate.json`、`agent-assignment.json`、`phase2-check.json` 或
task commit evidence；未 commit、push、创建或修改 PR。

## Qualified Finding Owner Evidence

### `F-131-BR4-01` — P2：全局 workflow 仍复制 Branch Review step-local 内部合同

- Scenario class：`normal_required_behavior`。
- Disposition：`qualified_finding`。
- Severity：P2。
- Owner round：5。
- Source discovery：round 4 fresh final review。
- Affected paths：
  - `trellis/workflows/guru-team/workflow.md`
  - `.trellis/workflow.md`

### Requirement refs

- `prd.md:11-17`：`guru-review-branch` 是完整分支审查唯一 step-local SSOT；
  全局 workflow 只保留 mandatory invocation、四个 exits、consumer 与 stop。
- `prd.md:196-199` / `prd.md:268-269`：R11 与 AC13 要求 workflow 不再复制
  Branch Review 内部合同。
- `implement.md:121-137`：Phase 3.5 收敛 checkpoint 要求 workflow 不含
  step-local Branch Review checklist。
- `.trellis/spec/workflow/workflow-contract.md:20-25`：workflow prose 不得复制
  package 的 step-local closed loop。
- `.trellis/spec/workflow/workflow-contract.md:945-961`：reviewer prompt、
  qualification、severity、finding closure、final-review freshness、artifact
  construction 与 recovery 都属于 `guru-review-branch`，不得复制到 workflow。

### Canonical / dogfood 精确重复段

Canonical 与 dogfood workflow byte-identical，以下重复同时存在于两侧：

- `workflow.md:250-260`：直接给出
  `review-branch.sh --pass` 与 `check-review-gate.sh` 的可执行 recorder/checker
  路径。
- `workflow.md:302-366`：继续展开 Branch Review reviewer role、independence、
  raw report、liveness/recovery、finding owner、fresh final review、
  post-commit Phase 2 audit、artifact 与 recorder/checker 规则。
- 其中 `workflow.md:359-366` 精确复制完整 diff scope、独立 reviewer、Docs SSOT、
  post-commit audit、review report/gate artifact 与 recorder 参数语义。
- 与此同时，Phase 3.5 主段 `workflow.md:1170-1201` 已正确使用
  `guru-review-branch` mandatory invocation 与四个 exact exits；前述旧段因此形成
  第二个行为 SSOT，而不是 Phase 3.5 所需的 typed routing。

### 资格化与影响

普通 main session 按当前 workflow prose 执行即可进入该路径；复现不依赖恶意伪造、
artifact 攻击、TOCTOU、并发压力或非常规 failure injection。因此它属于
`normal_required_behavior`，不是 out-of-scope 加固建议。

旧直调示例和重复 reviewer/closure/recorder 规则继续把全局 workflow 作为第二个
Branch Review 行为权威，并可能引导调用方绕过 active package mandatory invocation
直接进入 recorder。Issue #131 的核心 SSOT migration 与 AC13 因此没有完整交付；
durable contract 虽然正确，canonical/dogfood workflow 仍与其不一致，
`ssot_first` reconciliation 不能通过。

P2 severity 保持不变：该缺口影响公共 workflow 的正常运行权威和新安装/dogfood
副本，但本报告没有证据把它升级为 P0/P1，也没有理由降级为 P3、observation 或
follow-up。

### Required closure

1. 删除或改写全局 workflow 中 Branch Review 专属 helper 直调示例。
2. 删除 step-local reviewer、qualification、closure、final-review、artifact 与
   recorder 细节，只保留真正跨 Skill 的全局 sub-agent 原则和 Phase 3.5 typed route。
3. 同步 canonical 与 dogfood workflow。
4. 重新执行完整 Phase 2 并创建 fresh task commit。
5. 由本 finding owner 或合法 replacement 完成问题闭环审查。
6. 再派发一个未参与此前发现/闭环的全新 technical agent 执行 fresh final review。

## 历史 Findings 与本轮计数

- Phase 2 `F-131-01..05`：closed。
- Round 1 `F-131-BR-01..04`：closed。
- Round 2 `F-131-BR2-01`：closed。
- 本轮没有重新打开历史 finding。
- Round 5 owner findings：
  - P0：0
  - P1：0
  - P2：1
  - P3：0
- 唯一 finding：`F-131-BR4-01`。
- Scope proposals：0。

## 验证证据

本轮按指令不重跑长套件。验证结论原样引用 Round 4 完整报告及其 SHA：

- `git diff --check` passed；
- focused 74/74；
- package contract 8/8；
- Skill package 167/167；
- runtime 566 passed、13 skipped；
- preset 45/45；
- ownership 6/6；
- source/installed shared eval 各 7/7；
- source/installed validators、10/39/23、1903-file inventory、dogfood drift、
  parity、sensitive scan、sidecar scan 均 passed。

这些 green checks不改变 `F-131-BR4-01` 的 semantic finding。Exact remote
feature-ref marketplace install、外部 lint/typecheck 工具和本轮未重跑 full
throwaway 的限制也保持 Round 4 原结论。

## 结论

Round 5 是 round 4 → 5 lifecycle role re-entry，不是第二个 finding，也不替代
Round 4 fresh final review。`F-131-BR4-01` 继续保持
`normal_required_behavior`、P2、open，当前 HEAD 不能放行。

New finding count：1。建议 typed exit：`implementation_required`。本报告不能支持
`guru-review-branch:passed` 或 passing Branch Review Gate。
