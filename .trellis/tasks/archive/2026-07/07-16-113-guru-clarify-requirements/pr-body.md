## 变更摘要

- 新增公共 semantic closed-loop Skill `guru-clarify-requirements`，统一承接 initial intake、active-task scope change 与显式 standalone clarification review。
- 建立 evidence-first 分类、单问题 clarification loop、repository-answerable question 先取证、partial answer 不得关闭问题，以及 current content/scope digest freshness 合同。
- 定义 `none`、`issue_comment`、`issue_body_edit`、`proposed_draft_update`、`new_issue_draft`、`active_task_scope_update` 六类 action plan；任何 source-of-truth mutation 前必须取得 action-digest-bound exact confirmation，mutation 后重新绑定 live authority。
- 为 active-task scope change 固化五类 scope classification、七类 terminal proposal decision、task-local structured decision trail、authority -> context -> task update 时序，以及 fresh planning/Phase 2/review re-entry。
- 接入 canonical registry、workflow mandatory invocation、shared runtime、extension manifest、preset installer与 Agents/Codex/Cursor/Claude 平台副本，并同步 durable requirements、spec 和三份 public README。

## 影响范围

- Skill package：新增 `guru-clarify-requirements` 的 `SKILL.md`、interface、contract、schema、example、recorder/checker wrappers 与 package tests。
- Workflow/runtime：`guru-discover-change-context` 的 `context_ready` 进入新 Skill；shared runtime新增 requirements clarification recorder、validator、typed-exit 与 active-task decision-trail 校验。
- Schema/contract：定义 clarification round closed shape、question lifecycle、scope proposals、confirmed actions、live mutation facts、freshness与 caller-aware resume invariants。
- 分发/升级：canonical、dogfood、registry、extension manifest、preset managed inventory及 Agents/Codex/Cursor/Claude discovery copies同步；clean install、`trellis update`、workflow re-selection与preset reapply已覆盖。
- Docs SSOT：更新 `docs/requirements/**`、`.trellis/spec/**`、README、workflow README 与 preset README；task artifacts只保留规划、finding lifecycle与审查证据。

## 验证结果

- Clarification focused runtime `28/28`、package contract `6/6`、shared runtime `496/496`、registry/distribution `71/71`、preset installer `39/39`、upstream ownership `6/6` 全部通过。
- Python AST `19`、Bash syntax `17`、JSON `40`、JSONL `2` 全部通过；固定 diff range 的 `git diff --check` 通过。
- Source/installed package validation通过，`managed_file_count=168`；sidecar、removal、conflict均为 `0`。
- Canonical package 8个文件对dogfood及四个平台共40组byte/mode一致，canonical/dogfood workflow与runtime字节一致。
- Clean throwaway覆盖public marketplace discovery、initial install、五个 typed exits、standalone、preview/switch、`trellis update`、workflow re-selection、preset reapply、two-closeout、all-platform与零sidecar。
- Reviewed HEAD push后的remote exact feature-ref marketplace验证由 `trellis-finish-work` 在创建PR前执行；失败会阻塞发布。

## Review Gate

- Branch Review Gate已绑定HEAD `908eec2ee6bdf8190a6da52af1b925d890e75954`，覆盖固定base `96ba63b8c0fab175f6b02997c8799b36bec64e20` 到HEAD的完整115-path diff与五个task work commits。
- 七轮独立审查中，F-002至F-008已按finding owner/closure/fresh final reviewer链全部关闭；F-001按用户明确决定和GitHub-visible comment保持 `out_of_scope`。
- 最终开放 findings 为 `P0=0, P1=0, P2=0, P3=0`，审查覆盖需求、设计、代码、测试、spec sync、cross-layer、Docs SSOT、安装升级、安全与部署影响。

## Issue 关闭范围

Closes #113

### 仅引用

- Refs #55：closed历史行为来源，不重复关闭。
- Refs #98：Intake Skill family umbrella，本PR不关闭。
- Refs #109：Skill-first architecture prerequisite，已独立关闭。
- Refs #111：上游context discovery producer，已独立关闭。
- Refs #114：`clear` 的下游wording review owner，由独立task实现。
- Refs #101：clarity passing evidence consumer，由独立task实现。
- Refs #112：task workspace与intake integration consumer，由独立task实现。
- Refs #127：scope qualification与upstream ownership架构来源。

## Docs SSOT

- `strategy`：`ssot_first`；`docs_state`：`partial_docs`。
- `durable docs`：已更新Guru Team流程需求、workflow/preset/docs specs、canonical package contract、仓库README、workflow README与preset README。
- `merged delta`：已回写evidence-first classification、single-question loop、exact confirmation、active-task scope proposal/decision trail、fresh re-entry、typed exits、script boundary、分发和验证矩阵。
- `task history`：Phase 0 snapshot、规划过程、F-001范围决策、sub-agent liveness、Phase 2与七轮Branch Review仅保留为task evidence。
- `follow-up / limitation`：下游 #114/#101/#112 保持独立交付；本PR不提前实现其behavior。

## 安全说明

- 本任务按AI与用户诚实协作的正常运行边界实现；F-001所述恶意伪造pre-task/standalone artifact场景明确不属于当前威胁模型，未引入仅服务该场景的embedded body/locator或负例测试。
- 正常流程的hash、digest、freshness、live reread与fail-closed仍用于版本绑定、stale/mismatch检测和阻止错误接续；secret/credential redaction与GitHub mutation权限边界保持不变。
- 变更不包含token、secret、private key、签名URL、`.env`、数据库URL、客户数据或敏感原始记录。
- 未修改GitHub Actions、Dockerfile/Compose、Kubernetes/Kustomize/Helm、数据库migration/seed/backfill、Makefile、服务、后台任务、队列或业务runtime config；无需业务部署、数据库迁移或额外rollback资产。
- 回滚使用Git revert，并从上一extension ref重新应用workflow/preset。
