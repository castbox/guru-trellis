# 第 3 轮问题闭环审查报告（阻塞）

## 审查身份

- 逻辑角色：`问题闭环审查代理`
- 技术身份：`/root/issue_113_round3_closure_review`
- 审查来源：`independent-agent`
- 复用决策：`new-agent`
- 审查类型：`closure`
- 审查 HEAD：`a9242def2a9173b72c0bacc186601fba74ddfbd8`
- Intake base：`96ba63b8c0fab175f6b02997c8799b36bec64e20`
- 完整 diff：`96ba63b8c0fab175f6b02997c8799b36bec64e20...a9242def2a9173b72c0bacc186601fba74ddfbd8`
- Finding 修订 diff：`d77fda1f6a16d064b5db37ff23be9dfe4fa8649a..a9242def2a9173b72c0bacc186601fba74ddfbd8`
- 结论：`blocked`
- Findings 数量：`1`

## 审查范围

本轮独立审查覆盖固定 base-to-HEAD 的 113 个 committed paths，以及 Round 2 finding 修订提交的 54 个 paths。审查内容包括：

- Live GitHub issue `#113` 与用户范围决策评论 `issuecomment-4990373622`
- `prd.md`、`design.md`、`implement.md`、schema 1.2 `planning-approval.json`
- implementation/check handoff、Round 8 `phase2-check.json`、`issue-scope-ledger.json`、Docs SSOT Plan
- Round 1、Round 2 原始审查报告及完整 finding 生命周期
- Canonical package、interface、contract、schema、example、wrapper、runtime、workflow、registry、extension manifest
- Dogfood runtime/workflow/package 与 Agents、Codex、Cursor、Claude discovery copies
- Preset installer、ownership pin、update/reapply、throwaway 与 all-platform 证据
- 完整测试、安全、部署、CI/CD、容器、Kubernetes/Kustomize、migration、Makefile 影响
- `a9242def` 的 post-commit Phase 2 audit 语义和当前仅 task metadata tail 的工作树状态

## 问题生命周期

### F-001：out_of_scope

Live 评论 `https://github.com/castbox/guru-trellis/issues/113#issuecomment-4990373622` 明确排除调用方恶意伪造 pre-task/standalone draft/context artifact 的场景；评论正文 SHA-256 为 `ef8b1239738ead871cd562639f0f7854111432d2917ae7113bfe401ceeed362f`，`updated_at=2026-07-16T09:39:51Z`。

本轮不把恶意伪造、手工篡改、hostile/adversarial input、anti-forgery、embedded body/locator 或相应负例纳入 finding、观察项或后续候选。正常 stale/mismatch、recorder/executor 错误 payload 与 supported workflow correctness 仍在审查范围内。

状态：`out_of_scope`，不阻塞。

### F-002：resolved

Runtime 逐轮维护 `current_open`，要求每轮 `question_id` 已打开或本轮打开，拒绝 close-before-open、reopen-after-close，并固定 `open_questions = opened - closed`。`partial` 不能关闭问题，空 lifecycle 不能隐藏 partial answer。Full runtime 与 package tests fresh 通过，未见回归。

状态：`resolved`。

### F-003：resolved

GitHub comment/body mutation 仍要求 mutation result 绑定已确认 action、action digest、payload body、canonical payload digest 与 live reread content；unknown action、content mismatch 和缺少 exact action confirmation 均 fail closed。未见 confirmed payload/live mutation 一致性回归。

状态：`resolved`。

### F-004：resolved

Active-task Scope Change Gate mandatory invoke `guru-clarify-requirements`；`clear` 统一进入 `guru-requirements-clear-router`，initial、standalone、accepted-current 与 non-current resume targets 均为 closed mapping。Workflow 不再复制 step-local 分类和确认流程。

状态：`resolved`。

### F-004R：resolved

Round 2 的 P1 已按正常路径关闭：

- `accepted_current`、`related`、`followup`、`new_task`、`out_of_scope` 五类 classification 无论 origin 均要求 proposal-digest-bound exact 用户决策证据；
- active-task `clear/new_task` 拒绝空 `scope_proposals[]`、`pending` 或非 terminal 集合；
- 五类 classification 必须绑定 live GitHub comment/body authority、唯一 task-local structured trail 与 exact ledger match；
- authority mutation 只能先返回 `refresh_context`，fresh re-entry 强制 `authority.updated_at <= context.generated_at`，并把 task update preimage、trail `context_before_task_update_sha256` 与当前 context digest 绑定；
- non-current classification 恢复 exact interrupted progression，`accepted_current` 进入 planning review，`new_task` 保留当前 task trail并只交付 side-effect-free draft。

针对 `related/followup/out_of_scope/new_task/accepted_current` 的正反 tests 与独立 replay 均证明：缺 confirmation、缺 trail、ledger 不含 exact trail、authority stale 或时序不完整会失败。

状态：`resolved`。本轮新 finding 属于独立的 source-action confirmation 缺口，不否定上述 classification/trail 闭环。

### F-005：resolved

Schema 与 runtime 继续要求 repository-answerable `answered` 至少绑定一个 checked evidence ref；空 evidence 返回 `answered_repository_question_requires_evidence`。未见回归。

状态：`resolved`。

### F-006：resolved

Ownership facts 继续固定为 `active_skill_count=4`、`managed_asset_count=37`、`facts_sha256=9cd93021139c5e8f0b0400a6460521f321f8230cfe086a1bcf8ae51f840c1681`。Fresh registry/distribution `71/71` 与 preset/ownership `45/45` 通过；canonical、dogfood 和五个 discovery destinations 共 40 组 package file/mode 比较无差异。

状态：`resolved`。

## 后续正常路径回归闭环

### 空 proposal、`action=none` 与空 mutation 绕过：closed

Active-task `clear/new_task` 必须存在非空且全部 terminal 的 proposal set；`new_task` 必须至少包含一个 `decision=new_task`。五类 classification 还必须存在唯一 validated `active_task_scope_update`，因此不能用 `none` action 与空 mutations 绕过。`none` 只在合法 mechanism-only 路径保留。

### Planning approval、planning docs 与 review evidence placeholder：closed

Active-task terminal re-entry 复用 shared schema 1.2 planning approval validator，验证 explicit post-planning confirmation、passed ambiguity review、受控词扫描、空 `unchecked_normative_hits[]`、七个审查维度与三份 planning artifact 的 path/hash/size。占位 planning 文件和最小 approval JSON 在 fresh test 中返回 `active_task_planning_approval_invalid` 与 binding mismatch。

### Mechanism-only 与 mixed clear freshness：closed

七类 terminal decision 已分离为五类 classification 与两类 mechanism disposition。`mechanism_removed/replaced` 要求 optional origin、null confirmation、无 trail/authority mutation；mixed payload 的 confirmation/trail 只投影 classification 子集。无论 mechanism-only 还是 mixed，terminal re-entry 都执行相同 active-task planning/review/context live freshness；stale context 会失败。

### Existing review evidence：closed

`review-gate.json` 存在时，结构与 live checker 均只接受 `review_evidence.status=stale` 且 exact 绑定 artifact path/content digest；`current` 同时触发 structural/live failure。文件不存在时只接受 `not_started`、null artifact 和 null Branch Review digest。

### Authority、context 与 task update 顺序：closed

Live authority content、URL 和 `updated_at` 均重新读取；context snapshot identity 必须 current，`generated_at` 不早于 authority `updated_at`；trail 与 `active_task_scope_update.preimage_sha256` 必须等于 task update 前 context digest。Comment/body stale、context predates authority、task-update digest mismatch 均有负例。

## Findings

### P0

无。

### P1 [F-007] `active_task_scope_update` 可在未绑定 action digest 的情况下写入 task authority

- 需求合同：`.trellis/tasks/07-16-113-guru-clarify-requirements/prd.md:5`、`:68`、`:70`
- 设计与 durable contract：`.trellis/tasks/07-16-113-guru-clarify-requirements/design.md:188`、`.trellis/spec/workflow/data-contracts.md:248`、`.trellis/spec/workflow/quality-guidelines.md:79`
- Runtime：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:19640`、`:19686`、`:19761`、`:19929`
- 当前通过样例：`trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py:16999`、`:17073`

PRD R4 明确要求任何 source-of-truth mutation 前展示 exact target、payload、scope delta、affected contracts 与 executor command，并取得 action-digest-bound 用户确认；planning approval、普通继续或其它确认不能替代。`active_task_scope_update` 正是当前 task-local ledger/planning/review authority write。

当前 runtime 只在 `confirmed_actions` 非空时校验 `human_confirmation.action_digest`，并且只对存在于 `mutation_results[]` 的 action 强制 `mutation_requires_exact_action_confirmation`。Active-task re-entry 则要求一个 `status=validated` 的 `active_task_scope_update`，但该 task-local write 没有 mutation result，也没有等价的 confirmed-action gate。

Fresh 正常路径 replay 结果：

```json
{
  "decision": "related",
  "action_kind": "active_task_scope_update",
  "action_status": "validated",
  "action_digest": "69ac0fbb24cfdf9205671d7a727863bbfdbd31810fc946626df1e0c5f7caa7fe",
  "confirmation_kind": "exact_scope_proposal",
  "confirmation_action_digest": null,
  "confirmed_actions": [],
  "proposal_confirmed": true,
  "structural_errors": [],
  "live_errors": []
}
```

该场景不需要伪造或手工篡改：用户只确认 classification proposal 后，AI 正常刷新 GitHub authority/context，再修改 task-local ledger/planning/review evidence并把 action 标记为 `validated`，checker 即允许 `clear` 恢复 implementation。Proposal confirmation证明“如何分类”，但没有证明用户看过并确认实际 task mutation 的 exact target/payload/command。Schema 1.2 planning approval也不能替代该 action confirmation，因为 PRD R4 已明确排除这种替代。

影响：五类 classification 虽已具备用户决策、GitHub authority 与持久 trail，但当前 task 的 source-of-truth mutation 仍能在未绑定其 action digest 时完成，违反 #113 正向闭环第 7 步和 AC4/AC7 的 mutation boundary；现有通过测试把该遗漏固化为合法路径。

修复必须让每个五类 classification 的 `active_task_scope_update` 在写入前被同一 exact confirmation 明确覆盖，例如要求该 action id 出现在 `confirmed_actions[]`、`confirmation_kind=exact_source_action_and_scope` 且 `action_digest` exact 匹配，并增加五类 classification 对“proposal 已确认但 task action 未确认”的负例。实现应保持 mechanism-only 无 action/confirmation 的既定合同。

状态：`open`，阻塞 Branch Review Gate。

### P2

无。

### P3

无。

## 验证证据

- Workspace boundary：`status=ok`，expected/actual root 均为当前 task worktree；source checkout clean，无 suspicious source artifacts。
- Live GitHub：issue `#113` 为 OPEN，正文与用户决策评论已 fresh 读取；F-001 评论 SHA-256、URL 与时间匹配 task ledger。
- 完整 diff：`113 files changed, 28211 insertions(+), 198 deletions(-)`；`git diff --check 96ba63b...a9242def` 通过。
- Full runtime：`495/495 passed`。
- Registry/distribution：`71/71 passed`。
- Preset + ownership：`45/45 passed`，其中 apply `39/39`、ownership `6/6`。
- Clarification package：`6/6 passed`。
- F-004R 聚焦 tests：non-current persisted trail、active `new_task` trail、五类 exact user evidence均通过。
- 独立 action-confirmation replay：上列正常路径 structural/live 均错误地返回空 errors，形成当前 P1。
- Canonical distribution：canonical package 8 files 对 dogfood、Agents、Codex、Cursor、Claude 五个 destinations 共 40 组 byte/mode 比较全部一致；canonical/dogfood runtime 与 workflow 字节一致。
- Phase 2：已审阅 Round 8 `27/27` focused、`6/6` package、`495/495` runtime、`71/71` registry、`39/39` preset、`6/6` ownership、`46/46` normal-state replay、managed files `168`、AST/Bash/JSON/JSONL `19/17/38/2`、clean throwaway/update/reapply/two-closeout/all-platform 证据。
- Post-commit audit：`a9242def` 的 54 个 paths 全部属于 `phase2-check.json.dirty_paths`、4 个 `checked_artifacts` 或允许的 Phase 2/task-commit metadata self-tail；`uncovered_nonmetadata=[]`。Phase 2 记录 HEAD 为 `d77fda1...` 是预提交审查语义，不应在 commit 后重录。
- Task commit：`a9242def` parent 为 `d77fda1...`，candidate sequence `003` 的 expected/actual tree 一致，`hook_mutation=false`。
- 官方 Trellis 文档：current `custom-workflow.md` 仍明确 `.trellis/workflow.md` 拥有 phase/skill routing，workflow 行为通过 Markdown 定义而不是 fork hook/runtime；本次 canonical workflow/package/preset 分层未偏离该扩展面。
- Secret scan：无 token、private key、credential 或数据库 URL 命中。
- Sidecar：未发现 `.new` / `.bak`。

## Docs SSOT 判断

Docs strategy 为 `ssot_first`。Durable requirements、workflow specs、package contract、public README、canonical workflow 与 task planning 已同步 F-004R 的五类 confirmation、trail、mechanism-only/mixed、review stale 与 authority/context/task 顺序；这些部分一致。

Docs SSOT reconciliation 最终为 `failed`：PRD R4 与 durable quality/data contract要求 active-task action 覆盖 exact action confirmation，但 runtime 和当前通过样例允许 `active_task_scope_update` 在 `confirmed_actions=[]`、`action_digest=null` 时完成。该 current-scope code/test 与 Docs SSOT 不一致是 P1 finding，不能降级为观察项。

## 测试判断

全量 runtime、package、registry、preset 与 ownership tests 均通过，distribution、installer 和多数正常状态矩阵覆盖充分。测试缺口不是“没有跑测试”，而是当前 `make_active_task_classification` helper 把未 action-confirmed 的 task update 构造成正例，导致所有五类 classification 继承错误前提。

必须补充 action confirmation 的正反矩阵，并确认 recorder/checker 在 proposal 已确认但 action 未确认时 fail closed；mechanism-only 路径继续保持无 action、无 confirmation、无 trail 的合法终态。

## 安全与部署

本轮 P1 是 honest-but-fallible 正常 workflow 的 confirmation/correctness 缺口，不涉及恶意 actor、伪造、篡改或对抗性输入。F-001 继续保持 out-of-scope。

完整 diff 未修改 CI/CD workflow、Dockerfile/Compose、Kubernetes/Kustomize、数据库 migration、Makefile、服务、后台任务、队列、runtime config 或部署资产；新增能力仅是 repo-local Trellis Markdown/package/companion runtime/preset 分发，不改变应用部署形态。无需同步部署资产。

未发现 secret、credential、private key、token、签名 URL、`.env`、数据库 URL、客户数据或敏感原始记录。

## Issue 范围

`issue-scope-ledger.json` 当前记录 `close_issues=[#113]`，related 为 `#55/#98/#109/#111/#114/#101/#112/#127`，`followup_issues=[]`。该分类与 live issue 依赖/阻塞关系一致；F-001 的 out-of-scope structured trail exact 绑定用户评论、planning documents、approval、stale review/Phase 2 与 re-entry owners。

由于当前仍有 1 个 P1，`#113` 尚未满足全部 acceptance，`close_issues[].acceptance_evidence` 为空是当前未进入 publish readiness 的真实状态；不得创建 `Closes #113` 的 ready PR、关闭 issue 或进入 finish-work。

## 观察项

- 分支尚未 push，remote current-branch marketplace ref 未验证；现有 verifier 正确 fail closed，publish 后 remote verification 属于既定 finish-work 门禁，本身不是本轮 finding。
- 当前 tracked/untracked 变化仅为主会话维护的 task commit/review metadata tail；index 为空，无 source/config/script/schema/preset/overlay 非 metadata drift。
- 普通 `check-phase2-check` 在 commit 后报告 HEAD/dirty mismatch 是预期现象；Branch Review 使用 post-commit audit 语义，且本轮人工核对 `uncovered_nonmetadata=[]`。

## 后续候选

无。当前 P1 属于 `#113` 已批准的 exact action confirmation 与 active-task mutation acceptance，必须在本任务内修复，不能移入 follow-up。

## 结论

Round 2 的 F-004R 以及空 proposal、placeholder planning、mechanism-only/mixed freshness、review current/stale、authority/context/task 时序等后续正常路径回归已关闭；F-002、F-003、F-005、F-006 未回归。F-001 按用户决策固定为 `out_of_scope`。

本轮发现 1 个新的 P1：五类 classification 的 proposal 虽已 exact 确认，但实际 `active_task_scope_update` task authority mutation 没有被 action digest confirmation 覆盖，structural/live checker 仍接受并恢复 progression。因此本轮成为新的 finding owner，Branch Review Gate 继续阻塞；必须返回 implementation、完整 Phase 2 与 finding-fix commit，之后再执行新的问题闭环审查。不得派发最终放行审查代理，不得记录 passing gate，不得 push、创建 PR、关闭 issue 或调用 finish-work。

- `reviewed_head=a9242def2a9173b72c0bacc186601fba74ddfbd8`
- `findings_count=1`
- `reuse_decision=new-agent`
- `final_result=blocked`
