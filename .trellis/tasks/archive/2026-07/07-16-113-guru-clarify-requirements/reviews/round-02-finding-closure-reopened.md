# 第 2 轮问题闭环审查报告（阻塞）

## 审查身份

- 逻辑角色：`问题闭环审查代理`
- 技术身份：`/root/issue_113_finding_closure_review`
- 审查来源：`independent-agent`
- 复用决策：`new-agent`
- 审查类型：`closure`
- 审查 HEAD：`d77fda1f6a16d064b5db37ff23be9dfe4fa8649a`
- Intake base：`96ba63b8c0fab175f6b02997c8799b36bec64e20`
- 完整 diff：`96ba63b8c0fab175f6b02997c8799b36bec64e20...d77fda1f6a16d064b5db37ff23be9dfe4fa8649a`
- Finding 修订 diff：`2bf9317d2fa838aff40f250f770e6e51f4439aab..d77fda1f6a16d064b5db37ff23be9dfe4fa8649a`
- 结论：`blocked`
- Findings 数量：`1`

## 审查范围

审查覆盖完整 112 个 base-to-HEAD committed paths 和 66 个 finding 修订提交路径，包括：

- Live GitHub issue `#113` 与用户决策评论 `issuecomment-4990373622`
- 最新 source checkout `AGENTS.md` 第 2.1 节 honest-but-fallible 边界
- `prd.md`、`design.md`、`implement.md`
- `planning-approval.json`、`phase2-check.json`、`issue-scope-ledger.json`
- 第 1 轮原始 finding report
- Canonical package、schema、runtime、workflow、registry、manifest
- Dogfood、Agents、Codex、Cursor、Claude copies
- Preset installer、ownership pin、update/reapply、throwaway
- Durable specs、requirements docs、public README
- 测试、安全、部署、CI/CD、容器、K8s、migration、Makefile 影响

## 原 Findings 生命周期

### F-001：out_of_scope

用户通过 live GitHub 评论明确排除调用方恶意伪造 pre-task/standalone draft/context artifact 的场景；最新 `AGENTS.md` 2.1 同样要求仅靠手工伪造 hash、artifact 或 state 的案例不得进入 P0-P3。

正常 correctness 未被削弱：live issue authority、active-task ledger/planning/context snapshot stale、unknown mutation/action mismatch、confirmed payload、mutation result 与 live body/comment 一致性仍执行校验，且 `needs_context`、stale authority、active-task file drift 仍有正反测试。

状态：`out_of_scope`，不阻塞，不列 follow-up。

### F-002：resolved

`guru_team_trellis.py:19461-19511` 维护逐轮 `current_open`，要求 `question_id` 来自本轮 opened 或既有 open set，拒绝 close-before-open、reopen-after-close，并固定 `open_questions = opened - closed`。

`test_question_state_requires_exact_open_minus_closed` 证明空 lifecycle 的 partial answer返回 `clarification_question_not_opened`。

状态：`resolved`。

### F-003：resolved

`guru_team_trellis.py:19689-19741` 将 mutation 绑定 exact action、confirmation 和 payload body；`:20067-20120` 再将 mutation content 与 live issue body/comment 绑定。Unknown action 返回结构化 `mutation_action_binding_mismatch`，CLI exit 2，未泄露绝对路径且无 traceback。

状态：`resolved`。

### F-004：reopened

原 finding 的两个直接症状已经修复：

- Active-task Scope Change Gate 现在 mandatory invoke `guru-clarify-requirements`，旧复制分类步骤已删除。
- `clear` 唯一 consumer 已统一为 `guru-requirements-clear-router`，initial、standalone、accepted-current 和 non-current resume targets 已形成 closed mapping。

但 active-task 非 current 分类仍存在新的正常路径缺口，见当前 P1。F-004 因闭环不完整重新打开。

### F-005：resolved

Schema 与 runtime 均要求 repository-answerable `answered` 至少包含一个 checked `evidence_ref`；空 evidence 返回 `answered_repository_question_requires_evidence`。

状态：`resolved`。

### F-006：resolved

Ownership facts pin 已更新为 `active_skill_count=4`、`managed_asset_count=37`、`facts_sha256=9cd93021139c5e8f0b0400a6460521f321f8230cfe086a1bcf8ae51f840c1681`。Fresh ownership tests `6/6`、registry discovery `71/71`、source/installed package gates 均通过。

状态：`resolved`。

## 当前 Finding

### P1 [F-004R] Active-task 非 current 分类可无确认、无决策落盘直接恢复 progression

- 路径：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:19681`、`:19774`
- 测试路径：`trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py:16885`
- 合同：`prd.md:67`、`prd.md:73`、`prd.md:116`，以及 live issue `#113` 的 Artifact 与 Active-task Scope Change Gate

正常复现：

1. Active task 收到一个未确认的 scope expansion。
2. AI 将 proposal 分类为 `related`、`followup` 或 `out_of_scope`。
3. 保持 `clarification_rounds=[]`、`human_confirmation.status=not_required`、`source_actions=[none]`、`mutation_results=[]`。
4. `active_task_evidence` 只绑定未记录该分类的既有 ledger 和 planning 文件。
5. Validator 接受 `clear`，router 恢复 `guru-resume-implementation`。

当前测试 `test_active_task_binds_existing_files_and_reentry_owners` 把上述三个 decision 构造成通过用例并断言 `structural_errors=[]`。测试中的 ledger 内容仅为 `{}`，planning 仅为占位标题，证明 validator 没有要求 decision 已写入 task authority。

Runtime 只在 `accepted_current` 时强制 exact confirmation、`active_task_scope_update`、GitHub-visible authority 和 planning-review resume；非 current 分类没有等价 gate。该问题无需伪造 artifact/hash，也不依赖恶意调用方，是受支持 active-task 正常路径中的 correctness bug。

影响：

- 用户未明确分类时，AI 可在没有可审计确认的情况下排除或延后需求。
- Final decision trail 只存在 stdout，未写入当前 task 的 ledger/planning/review evidence。
- GitHub-visible authority 与 `issue-scope-ledger.json` 可保持旧内容，却继续 implementation/check/commit/review。
- 跨 session 会丢失 close/ref/followup/out-of-scope 决策，破坏后续 PR close scope 审计。
- `new_task` 路径也未强制把当前 task 的分类决定留下 task-local trail。

修复后必须增加正反测试：

- `unconfirmed_expansion + related/followup/out_of_scope` 无用户决策证据必须拒绝。
- 非 current final classification 未绑定当前 task decision trail 和所需 GitHub-visible authority必须拒绝。
- `new_task` 必须保留当前 task 的分类 trail，同时继续由 `#112` 执行新 issue/task intake。
- 完成 mutation 后必须走 `refresh_context`，fresh re-entry 后才能恢复 exact interrupted progression。

状态：`open`，阻塞 Branch Review Gate。

## 验证结果

- Package：`6/6 passed`
- Focused clarification：`16/16 passed`
- Full runtime：`484/484 passed`
- Registry/distribution：`71/71 passed`
- Preset apply：`39/39 passed`
- Ownership：`6/6 passed`
- Source/installed package gate：通过，managed files `168`
- Sidecar/conflict/removal：`0/0/0`
- Canonical/dogfood/Agents/Codex/Cursor/Claude tracked package bytes 与 mode：一致
- Canonical/dogfood runtime 与 workflow：一致
- Dogfood overlay drift：通过
- Clean throwaway public sample：initial、preview/switch、update/reapply、两轮 closeout、all-platform 通过
- `task.py validate`：`implement.jsonl 14`、`check.jsonl 11`，通过
- Post-commit Phase 2 audit：`allow_committed_head=True`，`errors=[]`
- `git diff --check`：通过
- Secret pattern scan：无命中
- CI/CD、容器、K8s/Kustomize、migration、Makefile、服务配置/部署路径：无变更

未验证项：分支尚未 push，因此 remote current-branch marketplace ref 未验证。Verifier 已正确 fail-closed；显式 public marketplace sample 加 local unpublished workflow 验证通过。该项保留给 publish gate，不是本轮 finding。

## Docs SSOT 判断

Docs strategy 为 `ssot_first`。Durable specs、requirements docs、workflow、preset 与 public README 已同步 question lifecycle、repository evidence、exact confirmed mutation payload、caller-aware clear router、active-task mandatory invocation 和 ownership/update/throwaway 边界。

Docs SSOT reconciliation 最终为 `failed`：PRD R4/R9 和 live issue 要求 active-task final decision trail 进入 GitHub-visible authority及当前 task ledger/planning/review evidence，runtime 与现有通过测试却允许非 current decision 仅停留在 stdout。

这是当前代码/测试与已批准 Docs SSOT 的阻塞不一致，不能降级为观察项。

## Scope、安全与部署

`issue-scope-ledger.json` 当前为 `close_issues=[#113]`、related `#55/#98/#109/#111/#114/#101/#112/#127`、`followup_issues=[]`。分类本身与 live issue 一致，但 `acceptance_evidence` 尚为空，且当前存在 P1，因此 `#113` 不能进入 close/readiness。

未发现 secret、credential、private key、token 或敏感原始数据。无部署、配置、数据库、容器、Kubernetes、CI/CD 或 Makefile 影响。本轮阻塞属于 workflow correctness 与审计连续性，不是恶意伪造安全场景。

## 观察项

- 单独运行 pre-commit 语义的 `check-phase2-check` 会因 HEAD 已提交而报 HEAD/dirty mismatch；Branch Review 使用的 `allow_committed_head=True` post-commit audit 已 fresh 通过，此现象不是 finding。
- 测试产生的 ignored `__pycache__` 不属于 tracked/managed payload；tracked package byte/mode equality 已单独通过。
- 工作区非 clean 路径均为主会话维护的 task review/commit metadata；审查代理未编辑任何文件。

## 后续候选

无。当前 P1 属于 `#113` 明确 active-task scope-change acceptance，必须在本任务内修复，不得移入 follow-up。

## 结论

`F-001` 按用户决策为 `out_of_scope`；`F-002`、`F-003`、`F-005`、`F-006` 已关闭。F-004 的 mandatory invocation 与 caller-aware router 已修复，但 active-task 非 current 分类仍可无确认、无持久化 decision trail 直接恢复 progression，因此重新打开为 1 个 P1。

- `reviewed_head=d77fda1f6a16d064b5db37ff23be9dfe4fa8649a`
- `findings_count=1`
- `reuse_decision=new-agent`
- `final_result=blocked`

必须返回实现与完整 Phase 2，创建新的 finding-fix commit；在该 P1 关闭前不得派发最终放行审查代理，不得记录 passing Branch Review Gate，不得 push、创建 PR 或关闭 issue。
