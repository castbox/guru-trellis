# Guru Team Trellis 已实现扩展总览

本文按重要性说明本仓库已经在官方 Trellis 之上建设的扩展。内容基于本 repo 全量
GitHub issue / PR 历史，包括已 closed issue、已 merged PR、已 closed 未合并 PR，
并在后续维护中追加当前 active issue 已形成的长期能力。

重点不是重新写一份抽象流程，而是把历史迭代已经沉淀出的 Trellis 扩展能力分类，并说明
每类能力的职责边界、实现资产和历史来源。

## 1. P0：Workflow 主合同与日常入口

`guru-team` workflow 是本仓库最核心的扩展。它通过官方 Trellis workflow marketplace
机制安装到目标仓库，并把 Guru Team 的任务流程定义为 Markdown 合同，而不是依赖脚本
或 hook 分叉。

历史来源：

- Issue #1 / PR #4：中台知识门禁与 Repo Docs SSOT。
- Issue #64：Phase 1 `Docs SSOT Plan` planning 合同，明确 docs 状态、同步策略和 task artifact delta merge 责任。
- Issue #65：Phase 2 implementation/check 消费 `Docs SSOT Plan`，把 docs 同步执行和一致性复核纳入实现 handoff 与 `trellis-check`。
- Issue #66：Phase 3 / Branch Review / finish-work / PR body 只验证 Phase 2 Docs SSOT reconciliation 已完成，不首次执行 docs merge。
- Issue #2 / PR #3：对齐 Trellis auto-bootstrap start model。

Canonical 资产：

- `trellis/index.json`
- `trellis/workflows/guru-team/workflow.md`
- `trellis/workflows/guru-team/README.md`
- 本仓库 dogfood 运行副本 `.trellis/workflow.md`

已实现能力：

| 能力 | 说明 |
| --- | --- |
| 固定 marketplace id | `trellis/index.json` 暴露 `guru-team` workflow，稳定安装使用 `trellis init --workflow guru-team --workflow-source gh:castbox/guru-trellis/trellis#vX.Y.Z`，latest/canary 才使用不带 `#ref` 的 source。 |
| Phase 0 intake | 文件变更类任务先进入 issue intake、duplicate search、base branch 选择和 worktree preflight；默认 planner 不写 task artifact。 |
| Intake clarity / scope evolution | AI 读取 issue body/comment 或自然语言请求后，必须判断是否需要 `trellis-brainstorm`；澄清结果应回写 issue comment/body 或 proposed issue body。任务中新增需求或引用其他 issue 时，先确认纳入当前 task、related，还是 follow-up/new issue，并同步 `issue-scope-ledger.json`。 |
| 业务项目中文文档默认规则 | 业务项目 `.trellis/spec/**`、`.trellis/tasks/**`（含 `reviews/*.md` raw reports 与 `review.md` rollup）、`docs/**` durable docs、`00-bootstrap-guidelines` 生成或补齐的 docs SSOT，以及 workflow artifact human-readable 字段默认中文；literal token 可保留英文。 |
| Phase 1 planning | Trellis task 创建后写中文 `prd.md` / `design.md` / `implement.md`，并定位同一个 `Docs SSOT Plan`；主会话必须显式展示三份 task-local 规划文档链接并等待用户 post-planning 确认；Phase 0 handoff 确认不能替代 planning approval。 |
| Phase 2 execute/check | 默认 sub-agent mode 下实现由 `trellis-implement` / channel `implement` 完成并输出 handoff，随后 `trellis-check` / channel `check` 基于真实 diff、task artifacts、spec、docs/overlay/config/test 和验证命令完成完整检查；实现/check 都必须消费 Phase 1 `Docs SSOT Plan`，按 `ssot_first` / `delta_first` / `bootstrap_or_repair_docs` / `no_docs_update_needed` 策略说明 docs 同步结果并复核 durable docs / task artifacts / code / test 一致性；不用主会话自检或少量命令通过替代完整检查。 |
| Phase 3 review/finish/publish | commit 后由独立 review sub-agent 审查完整 `origin/<base>...HEAD` diff；每轮保留 task-local 中文 `reviews/*.md` raw report，最终中文 `review.md` 作为 rollup 汇总并链接 raw reports，再经过 Branch Review Gate；final reviewer 只验证 Phase 2 已按 `Docs SSOT Plan` 完成 reconciliation，current-scope Docs SSOT 不一致必须 finding；之后由 `trellis-finish-work` archive task、基于 AI-authored index 生成 task-local `finish-summary.json`、提交 metadata、发布非 draft PR，并以精确 metadata tail 回写 PR URL。 |
| Auto-bootstrap 日常入口 | 用户日常直接描述任务、贴 issue URL 或说 issue number；`trellis-start` 是 fallback / explicit orientation，不是每个任务的必需入口。 |

边界：

- Workflow 行为写在 Markdown 合同中，不通过修改 Trellis 上游源码、全局 npm 包、
  `node_modules` 或 hook hack 实现分叉。
- `trellis-continue` 只推进到 Branch Review Gate，不 push、不创建 PR、不调用
  `finish-work`。
- `trellis-finish-work` 是正常 closeout 与 PR publish 的唯一用户入口。

## 2. P0：Intake / worktree / no_task 副作用边界

这类扩展解决的是“AI 何时可以造成副作用”。历史问题集中在 freeform 请求、duplicate
issue、worktree、branch、task 创建和当前 checkout 直改上。

历史来源：

- Issue #6 / PR #14：`prepare-task` 默认路径改为无副作用 planner。
- Issue #15 / PR #16：`no_task` 当前 checkout 直接修改必须显式审批。
- Issue #26 / PR #28：worktree 创建后继承或初始化 Trellis developer identity。
- Issue #51：`prepare-task` slug / branch / worktree / task 命名质量门禁。
- Issue #60：workspace boundary 机器事实层，阻断 task artifact、review metadata 和
  recorder/validator 路径误写 source checkout；#76 在该事实层上实现 sub-agent liveness
  与 source checkout progress/boundary violation 判定。
- Issue #55：intake clarity / brainstorming、issue evidence update、任务中 scope change 留痕。

已实现能力：

| 能力 | 说明 |
| --- | --- |
| Side-effect-free prepare | `prepare-task.sh --json` 默认只输出 stdout JSON，不创建 GitHub issue、worktree、branch、Trellis task，也不写 handoff。 |
| Duplicate / proposed issue review | freeform 请求先输出 proposed issue、duplicate candidates、base branch、branch name、workspace path 和后续命令，由 AI 展示给用户确认。 |
| Intake clarity gate | 读取 issue body/comment 或自然语言请求后，AI 判断需求是否足以进入 planning；模糊时先用 `trellis-brainstorm` 澄清，并把澄清结果写入 issue comment/body 或 reviewed proposed issue body。 |
| Confirmed issue creation | 创建 GitHub issue 必须使用 `--create-issue-confirmed --issue-title ... --issue-body-file ...`，标题和正文来自 AI/human 已审阅内容。 |
| Worktree executor boundary | `--create-worktree` / `--create-task` 只在 intake plan review 和用户确认后使用，并把 handoff 写入选定 workspace。 |
| Workspace boundary guard | worktree mode 下 `local runtime workspace mapping` 是 task artifact 写入边界；`check-workspace-boundary.sh --json --task <task>` 输出 expected workspace、actual repo root、source checkout status、task worktree status 和 source checkout 可疑同名 artifact/review metadata，并让 recorder/validator 在错误 cwd 或错误 artifact path 下 fail closed。 |
| Base freshness | executor 路径创建 worktree 前刷新 base branch，只允许安全 fast-forward，本地 base 分叉或 freshness 不明时 fail closed。 |
| Naming quality gate | planner 输出 `naming_quality`；中文、非 ASCII 或低信息自动 slug（如 `issue-52`、`52-issue-52`、纯编号、仅通用词）不得静默进入 create 路径，agent 必须在读完 issue 后显式传入语义英文 `--short-name` / `--workspace-slug` / `--task-slug`，需要特殊分支名时才传 `--branch`。未显式传 `--branch` 时，branch 格式为 `<branch-type>/<slug>`，类型只能是 `feat` / `fix` / `refactor` / `perf` / `test` / `docs` / `style` / `build` / `ci` / `chore` / `revert`，未知语义 fallback 为 `chore`。 |
| Developer identity | 新 worktree 优先复制 source checkout 的 gitignored `.trellis/.developer`；缺失但有 `--assignee` 时初始化；两者都没有则阻塞并给恢复命令。 |
| no_task direct edit override | 当前 checkout 直改必须由用户明确批准跳过 issue、Trellis task、worktree 和 branch；批准不包含 commit、push、PR 或 issue close。 |
| Scope-change gate | task 进行中新增需求、引用其他 issue 或发现新 bug 时，AI 先询问/确认是当前 close scope、related context，还是 follow-up/new issue；结论同步到 GitHub issue 证据和 `issue-scope-ledger.json`。 |

实现资产：

- `trellis/workflows/guru-team/scripts/bash/prepare-task.sh`
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
- `trellis/workflows/guru-team/schemas/task-start-context.schema.json`
- `trellis/workflows/guru-team/workflow.md`
- `.agents/skills/trellis-start/SKILL.md`
- `.codex/prompts/trellis-start.md`

## 3. P0：Planning / check / Branch Review Gate 证据链

这类扩展解决的是“通过 gate 必须留下什么证据，以及脚本不能冒充 reviewer”。

历史来源：

- Issue #5 / PR #12：Branch Review Gate 前必须先执行 AI review prompt。
- Issue #8 / PR #25：增加 planning approval 与 phase2 check 可审计证据。
- Issue #52：`prd.md` / `design.md` / `implement.md` 生成后必须展示三份文档链接并等待用户显式 post-planning 确认；旧 `source=workflow` 或 Phase 0 handoff 确认 fail closed。
- Issue #83：展示三份规划文档前必须完成 planning artifact ambiguity review，并在 `planning-approval.json` schema 1.2 记录结构化 `ambiguity_review` evidence；脚本只做 recorder / validator，不替 AI 判断语义充分性。
- Issue #93：`record-planning-approval` / `check-planning-approval` 必须对 `prd.md`、`design.md`、`implement.md` 执行 v2 受控词表正文扫描，记录 `hits[]` 和 `unchecked_normative_hits[]`，并阻塞未分类命中或 `contract_violation` 命中。
- Issue #20 / PR #22：Branch Review Gate 建立 task-local final `review.md` 人类入口和
  `review-gate.json` digest 基线。
- Issue #70：多轮 Branch Review 每轮保留 task-local `reviews/*.md` raw report，最终
  `review.md` 只做 rollup 并链接 raw reports；`agent-assignment.json.review_rounds[]` 和
  `review-gate.json.verification_evidence.review_reports[]` 追溯 raw report digest。#61
  顶层 artifact 表默认仍只列 final `review.md`。
- Issue #78：`reviews/*.md` raw reports 和 `review.md` rollup 继承 #57 中文
  human-readable artifact 规则；标题、小节、字段/标签、发现、观察、后续候选、
  部署/安全判断、Docs SSOT 判断和结论默认中文，literal token 可保留英文。
- PR #21：`#20` 的早期 closed 未合并实现，由 PR #22 替代。
- Issue #62：sub-agent wait timeout / stale / unfinished termination 策略，避免把等待窗口
  timeout 或未闭环部分输出当作 pass evidence。

已实现能力：

| 能力 | Artifact / 脚本 | 说明 |
| --- | --- | --- |
| Planning start gate | `planning-approval.json`、`record-planning-approval.sh`、`check-planning-approval.sh` | 记录三份 planning artifact 的 hash / size / mtime、reviewer、`review_prompt_presented_at`、`approved_at`、HEAD、dirty paths、`user_confirmation.source=explicit-post-planning-review` 和 schema 1.2 `ambiguity_review` evidence；validator 以三份规划文档内容 digest 是否仍匹配为 freshness 判定，并校验 `ambiguity_review` 状态、reviewer/summary、v2 受控词表、固定 `scan_scope`、全部正文扫描 `hits[]`、空 `unchecked_normative_hits[]` 和七个审查维度；HEAD / dirty paths drift 不单独阻塞；`task.py start` 只是状态写入，Phase 0 handoff 确认、旧 schema、旧 `source=workflow`、缺失 ambiguity evidence、未分类命中或 `contract_violation` 命中不能通过 gate。 |
| Phase 2 check gate | `phase2-check.json`、`record-phase2-check.sh`、`check-phase2-check.sh` | commit 前记录完整 `trellis-check` AI check 覆盖范围、验证命令、findings 和当时的 `dirty_paths`；`trellis-check` 必须按 `Docs SSOT Plan` 策略复核 durable docs、task artifacts、code/schema/config/deploy/test 和测试覆盖一致性，确认 `delta_first` 已 merge、`ssot_first` 以 durable docs 为主输入、`bootstrap_or_repair_docs` 有最小修复或 follow-up / PR 限制、`no_docs_update_needed` 理由仍成立；`phase2-check.json` 是 Guru Team evidence artifact，不是 Trellis 原生步骤本身，命令和脚本通过只是 evidence 的一部分。 |
| AI review prompt | workflow / overlay 文案 | Branch Review Gate 前必须由独立 review sub-agent 审查 `origin/<base>...HEAD` 完整 diff；review sub-agent 不继续实现、不替 implement/check 代理补工作。 |
| Raw reports + rollup 必填 | `reviews/*.md`、`review.md` | 每轮 AI/human review 判断都必须写 task-local 中文 raw Markdown report；顶层 `review.md` 是最终中文 rollup，建议使用 `审查轮次`、`问题生命周期`、`最终审查`、`证据`、`观察项`、`后续候选`、`结论` 等小节，汇总审查轮次、问题闭环生命周期、关键证据、最终结论，并链接所有 raw reports。#61 顶层 artifact 表默认仍只列 final `review.md`，raw reports 通过 rollup 和 gate digest 追溯；literal command/path/JSON/HEAD/API/code token 可保留英文。 |
| Finding 全阻断 | workflow、`review-branch.sh`、`review-gate.json` | Branch Review Gate 中任意 finding 都阻断，包括 P3；`observation` 与 `followup_candidate` 可记录但不是放行 finding 的替代品。 |
| 闭环后 Fresh 最终放行审查 | `agent-assignment.json`、`review-branch --agent-assignment` | 任何发现过 findings 的 agent 必须先作为同一 `问题闭环审查代理` 确认其 finding 已闭环并记录 0 findings；若原 agent 失败/中断且无法继续，必须记录 predecessor failed/unfinished、`replacement-started`、`reuse_decisions[] decision=replace from_round/to_round` 和替代闭环 round。之后最终 pass 必须由新的 fresh `最终放行审查代理` 完整审查当前 HEAD diff 并记录 0 findings，且 final agent 不能是 finding owner 或替代闭环 reviewer。 |
| Sub-agent liveness 状态机 | `agent-assignment.json`、`record-subagent-liveness-event.sh`、`check-subagent-liveness.sh`、`check-agent-assignment.sh`、`review-branch --agent-assignment` | `agent-assignment.json` 是唯一 task-local assignment/status/liveness/review ledger，schema 1.1 包含 `agents[]`、`status_events[]` 和 `liveness[agent_id].last_scan_snapshot`；checker 每次按需单次采样 task/source checkout 与 progress event digest，输出 `progress_observed`、`workspace_boundary_violation_progress`、`status_request_required`、`continue_waiting_no_repeat_ping`、`stale_allowed` 或 `blocked_missing_evidence`。`progress_scan_interval=120s` 是扫描间隔，`max_progress_silence=180s` 从 `progress_anchor_at` 起算；`status-requested` 不刷新 anchor 或延长 deadline。stale cutover 必须结构化记录 `terminated-unfinished termination_reason=stale_cutover termination_source_event_id=<stale-assessed.event_id>` 和 `replacement-started replacement_reason=max_progress_silence_exceeded`，failed/stale/unfinished/replacement partial output 只有在恢复链到达 `completed` 后才能进入 Phase 2 / Branch Review pass evidence。旧 `record-agent-assignment.sh --status-event` 路径 fail closed。 |
| Workspace boundary snapshot | `check-workspace-boundary.sh`、recorder/validator boundary helper | 在记录 planning、phase2、assignment、review gate 或 sub-agent status evidence 前确认 actual repo root 等于 local runtime workspace mapping，并拒绝 source checkout / 非当前 task worktree 的 `--review-report`、`--agent-assignment`、`--review-round-report`、`--checked-artifact` 等路径；脚本只输出事实，不判断 stale、不迁移 patch、不清理 source checkout。 |
| Review gate recorder | `review-branch.sh`、`check-review-gate.sh`、`review-gate.json` | 固化 review result、final `review.md` digest、raw `review_reports[]` digest、base/head、evidence、findings、observations、follow-up candidates；脚本不是 reviewer，且独立 review sub-agent 不调用这些 recorder/validator 扩展脚本作为审查过程。脚本可客观拦截 `Review Rounds`、`Findings Lifecycle`、`Evidence Handoff`、`Deployment / safety impact`、`Follow-up Candidates` 等英文模板标题痕迹，但不判断中文审查语义充分性。 |
| Independent review source | `--review-source independent-agent` | 通过 gate 不能来自 `self-review` 或 `*-main-session`。 |
| Sub-agent assignment ledger | `agent-assignment.json`、`record-agent-assignment.sh`、`check-agent-assignment.sh`、`review-branch --agent-assignment` | 记录中文 `logical_role`、技术 `agent_id`、展示用 `platform_nickname`、HEAD、review round、raw report path/sha256/size/modified_at 和复用/更换判断；脚本只做客观校验，不决定复用。UI 展示面优先使用中文 subagent 名称，平台只给随机/自动昵称时记录原始值。 |
| 默认 sub-agent mode 执行边界 | workflow / overlay / agent definitions | 默认 mode 下必须有 `trellis-implement`、`trellis-check` 和 Branch Review review sub-agent 三段真实 sub-agent evidence；review sub-agent 每轮输出中文 `reviews/*.md` raw report，最终形成中文 `review.md` rollup。main session 只协调和记录，不能用主会话实现、自检、自审或 recorder/validator 成功替代。inline/self-exemption 必须有 artifact evidence，否则 fail closed。 |
| Post-commit audit / metadata tail 规则 | `review-branch.sh`、`finish-work.sh` / gate 校验 | Branch Review Gate 接受 Phase 2 后提交的非 metadata task paths，但这些 paths 必须已被 commit 前 `phase2-check.json.dirty_paths` 覆盖；review gate 通过后到 finish-work 之间仍只允许 Trellis metadata tail，新的非 metadata 变更会使 evidence stale。 |

覆盖范围：

- docs、code、tests、Trellis artifacts
- preset overlay、companion scripts、schema、config
- CI/CD、container、Kubernetes/Kustomize/Helm、DB migration、Makefile
- Issue Scope Ledger、publish readiness、部署影响和安全风险

## 4. P0：Finish / publish / PR readiness

这类扩展解决的是“PR 何时发布、由谁判断 PR body 是否足够，以及 dry-run 是否真的无副作用”。

历史来源：

- Issue #18 / PR #19：PR publish 只能发生在 finish-work 之后。
- Issue #17 / PR #23：PR body 质量标准，禁止低信息量默认摘要。
- Issue #7 / PR #24：publish 前必须有 AI-reviewed body file 或 readiness artifact。
- Issue #27 / PR #29：`finish-work --dry-run` 成为真正无副作用 readiness preview，同时修正
  Codex 默认 dispatch 为 `sub-agent`。

已实现能力：

| 能力 | 说明 |
| --- | --- |
| Publish after finish | `publish-pr` 是兼容性阻断入口；正常发布与恢复只由 `finish-work.sh --from-trellis-finish-work` 执行 reviewed content push、draft PR、final projection、archive transaction 与 draft-to-ready。 |
| Recovery/debug 明确化 | 同一 `trellis-finish-work` 从 committed plan/readiness、active/archive locator、Git/remote 与唯一 PR identity 恢复；不暴露 publish recovery flag，也不生成 initial empty-URL summary 或 URL tail commit。 |
| Reviewed body source | closeout 必须传入当前 task-local `pr-body.md`；`--body-artifact` 与 generated fallback 不进入 finish-work 事务。 |
| PR body 质量门禁 | 变更摘要、影响范围、验证结果、Review Gate、Issue 关闭范围、安全说明必须具体，禁止“当前 Trellis task”“详见 artifact”等低信息量短语作为主要摘要。 |
| Issue close 语义 | `Closes #xx` 只能来自 task-level `issue-scope-ledger.json` 的 `close_issues`，`related_issues` / `followup_issues` 不得被关闭。 |
| Final archive projection | finish-work 在 active task 中生成最终 summary，并由 official archive move 原样迁移；archive 后不重写 body/readiness/summary。 |
| Dry-run readiness preview | `finish-work --dry-run --from-trellis-finish-work --finish-summary-index-file <task>/finish-summary-index.json` 运行与 formal 相同的 prepare/validate，输出 immutable plan/digest，不移动或写入文件、不 commit、不 push、不创建 PR。 |
| Codex default dispatch | 缺省或非法 `codex.dispatch_mode` 回落到 `sub-agent`，显式 `inline` 保留为调试/降级模式。 |

实现资产：

- `trellis/workflows/guru-team/scripts/bash/finish-work.sh`
- `trellis/workflows/guru-team/scripts/bash/publish-pr.sh`
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
- `trellis/presets/guru-team/overlays/**/trellis-finish-work*`
- `.trellis/spec/workflow/workflow-contract.md`
- `.trellis/spec/workflow/companion-scripts.md`

## 5. P1：Preset installer 与平台 overlay

Preset installer 把 workflow 之外的 Guru Team companion assets 和平台入口安装到目标仓库。
它不运行 `trellis init`，不修改官方 Trellis 生成脚本，也不改上游源码。

历史来源：

- Issue #9 / PR #13：保持 dogfood installed overlays 与 canonical preset overlays 同步。
- Issue #11 / PR #30：preset installer 只安装所选平台 overlay。
- Issue #31：Guru Team extension version manifest 与 installed provenance。
- Issue #33：Guru Team extension version 与 repo 级 release tag `vX.Y.Z` 对齐。

Canonical 资产：

- `trellis/presets/guru-team/scripts/bash/apply.sh`
- `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`
- `trellis/presets/guru-team/README.md`
- `trellis/presets/guru-team/overlays/`

已实现能力：

| 能力 | 说明 |
| --- | --- |
| Managed assets 安装 | 安装 `.trellis/guru-team/config.yml`、schema、bash scripts、Python helper。 |
| 幂等更新 | 同内容跳过；Guru-managed 文件升级 active 文件并保留 `.bak`；未知本地改动写 `.new`。 |
| 配置保护 | 已有 `.trellis/guru-team/config.yml` 不为补 key 被覆盖；`middle_platform_knowledge.mode` 缺失时按 `optional_warn`。 |
| Codex dispatch 默认 | 物化 `.trellis/config.yaml` 的 `codex.dispatch_mode: sub-agent` 默认，显式 `inline` 保留。 |
| Subagent UI 中文展示名 | 安装 `.trellis/agents`、`.codex/agents`、`.cursor/agents`、`.claude/agents`；保留 `trellis-implement` / `trellis-check` / `trellis-research` / `implement` / `check` 技术标识。Cursor / Claude / channel runtime 用中文 `description` 和标题作为展示名来源；Codex 当前限制 `nickname_candidates` 为 ASCII，因此只用中文 `description` 和 assignment 角色表达中文 UI 语义。 |
| Subagent 执行边界 | workflow、continue overlay、agent definitions | 默认 sub-agent mode 下 main session 必须 dispatch implement/check/review sub-agent 并等待 evidence；`trellis-implement` 输出实现 handoff，并包含 `Docs SSOT Plan` strategy、docs 同步结果、task delta merge / task history-only 内容、no-update 或 follow-up / PR 限制；`trellis-check` 输出 Phase 2 evidence 并按 plan strategy 复核 durable docs / task artifacts / code / test 一致性；Branch Review sub-agent 输出可被 gate 消费的中文 `reviews/*.md` raw reports 与最终中文 `review.md` rollup。 |
| 平台可选安装 | 默认安装 shared + Codex + Cursor；支持重复 `--platform codex|cursor|claude`；支持 `--all-platforms`。 |
| 未选择平台不恢复 | 默认 Codex + Cursor 安装不创建 `.claude/`；重复 apply 不会恢复未选择平台目录。 |
| Extension version/provenance | `trellis/guru-team-extension.json` 是 Guru Team extension canonical version；installer 写入 `.trellis/guru-team/extension.json` 记录安装版本、source ref/commit、source tree state 和 selected platforms。 |
| Release tag contract | Guru Team extension release tag 使用 repo 级 `vX.Y.Z`，并与 `trellis/guru-team-extension.json.version` 一致；tag-pinned stable marketplace source 使用 `gh:castbox/guru-trellis/trellis#vX.Y.Z`。 |
| Dogfood drift check | canonical overlay 与本仓库安装副本可通过 `check-dogfood-overlay-drift.sh` 比对。 |
| 业务项目语言归一化 | preset installer 确定性替换 `.trellis/spec/**` 和 `00-bootstrap-guidelines` 中已知 Trellis 英文文档语言规则，不扫描 `.trellis/workspace/**`、普通 task 历史或翻译业务 `docs/**`。 |
| Finish summary 合同 | `finish-summary.schema.json` 是正常 finish 与 #100 backfill 的共同 SSOT；Guru Team 不调用 `add_session.py`，shared/Codex/Cursor context 不打开、枚举或输出 `.trellis/workspace/**`，preset 写入 `session_auto_commit: false` 与 workspace ignore。recorder 对 raw paths 排序去重并过滤受保护前缀；任一必需 Git path snapshot 命令失败时两个 path 数组清空，只记录固定 unavailable fact。`pr-readiness.json.publish_inputs` 在首次 PR create 前提交并绑定 repo/base/head/title/body digest/draft/reviewed source，recovery 在 query/create 前验证 Git blob、snapshot/body digest、gate 与 current/remote HEAD。 |

平台 overlay 当前覆盖：

| 平台/层 | 文件 |
| --- | --- |
| Shared skills | `.agents/skills/trellis-start`、`trellis-continue`、`trellis-finish-work` |
| Channel runtime | `.trellis/agents/implement.md`、`.trellis/agents/check.md` |
| Codex | `.codex/agents/trellis-*.toml`、`.codex/prompts/*` 与 `.codex/skills/*` |
| Cursor | `.cursor/agents/trellis-*.md`、`.cursor/commands/trellis-continue.md`、`.cursor/commands/trellis-finish-work.md` |
| Claude | `.claude/agents/trellis-*.md`、`.claude/commands/trellis/continue.md`、`.claude/commands/trellis/finish-work.md` |

## 6. P1：安装、升级与开箱验证

公共 workflow skill 基础设施由 `trellis/skills/guru-team/` 单点定义。
Production registry 的 `reserved` 项只占用公共 id，不能安装或被 mandatory
route 引用；`active` 项必须携带完整 package/interface/schema/validator/test
和 workflow marker 证据。global workflow 只拥有 mandatory invocation、跨
skill transition 和 typed exit consumer/stop，step-local 正文只属于 skill。

Preset 负责把 active package 安装到 `.trellis/guru-team/skills/`、shared
root 和已选择的平台 root，并用 previous managed hash 区分 missing、
unchanged、known managed upgrade 与 unknown local edit。unknown/invalid
provenance 必须保留原文件、生成 `.new` 并 fail closed；known upgrade 先生成
`.bak`。`check-skill-packages --mode source|installed` 只校验机器事实，不得
替代 AI Gate。`trellis update` 后必须重放 workflow 和 preset、处理 sidecar，
再通过 source/installed/drift 检查。

这类扩展证明 `guru-team` 不是 dogfood 仓库里的局部 patch，而是可以安装、升级、抽样验证的
团队扩展。

历史来源：

- Issue #10：README 安装命令必须非交互且可开箱验证。
- Issue #9 / PR #13：dogfood overlay 同步。
- Issue #11 / PR #30：平台选择安装验证。
- Issue #27 / PR #29：finish-work dry-run readiness 和 Codex default dispatch 让新装项目不在 closeout 阶段卡死。
- Issue #31：安装/升级后用户和 AI 可直接查看 Guru Team extension version 与来源 provenance。

已实现验证能力：

| 能力 | 入口 | 说明 |
| --- | --- | --- |
| Non-interactive install | `README.md` | 默认命令使用 `trellis init -y ... --workflow guru-team --workflow-source gh:castbox/guru-trellis/trellis#vX.Y.Z`，不进入交互式 spec template picker。 |
| AI install / upgrade prompt | `README.md` | 提供可复制到目标业务仓库 AI session 的安装、升级、spec bootstrap prompt。 |
| Throwaway install | `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh` | 创建临时 Git repo，运行非交互 `trellis init`、应用 preset、检查 workflow、脚本、平台选择和 `check-env --json`。 |
| Extension version check | `.trellis/guru-team/scripts/bash/version.sh --json` | 读取 installed manifest，输出 Guru Team extension version、workflow template id、source ref/commit、source tree state 和 selected platforms。 |
| Existing workflow preview/switch | `trellis workflow --marketplace ... --template guru-team --create-new` / 无 `--create-new` | 验证已有项目可以预览并切换 active workflow。 |
| Dogfood overlay drift | `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh` | 比对 canonical overlay 与本仓库安装副本，防止 dogfood 文件漂移。 |
| Installer unit tests | `trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py` | 覆盖平台选择、Codex dispatch 默认、unknown platform fail closed 等 installer 行为。 |
| Workflow helper tests | `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py` | 覆盖 intake side-effect boundary、planning/phase2 gate、review/publish/finish 边界等行为。 |

维护规则：

- README 命令必须真实可执行，不依赖本机隐藏状态。
- 修改 `trellis/presets/guru-team/overlays/` 后，要重新 apply 到本仓库并运行 dogfood drift
  check。
- 修改 workflow/preset/overlay/脚本后，需要说明 throwaway install 或 upgrade/update
  验证覆盖了什么，未覆盖什么。

## 7. P2：Docs、spec 与 knowledge 协同

这类扩展不直接创建 task 或发布 PR，但决定长期维护质量。

历史来源：

- Issue #1 / PR #4：Middle-platform Knowledge Gate 与 Repo Docs SSOT。
- Issue #10：README install / upgrade prompt 需要包含 spec bootstrap 边界。
- Issue #9：overlay 与 dogfood 副本同步属于公共 docs / spec 可维护性问题。

已实现能力：

| 能力 | 说明 |
| --- | --- |
| Middle-platform Knowledge Gate | 当任务涉及 Guru Team 中台 SDK / framework 时，AI 检查当前平台是否可用 `guru-knowledge-center` MCP，并将 citation 写入 task artifact。 |
| Configurable knowledge mode | `middle_platform_knowledge.mode` 支持 `off`、`optional_warn`、`required`；缺失时按 `optional_warn`。 |
| Docs SSOT Plan | Phase 1 必须创建或更新同一个 planning 合同，推荐由 `design.md` 承载权威计划，`prd.md` 记录 docs 状态 / 需求影响，`implement.md` 记录 checklist / checkpoint。计划记录 `complete_docs`、`partial_docs`、`stale_docs`、`no_docs` 之一，以及 `ssot_first`、`delta_first`、`bootstrap_or_repair_docs`、`no_docs_update_needed` 之一。 |
| Repo Docs SSOT reconciliation | Planning 阶段识别 durable docs；Phase 2 完成 durable docs 更新/merge/repair/no-update 复核并在 handoff/check 中留痕；Phase 3 只验证结果，finish-work/archive 不首次执行 docs merge。 |
| Spec bootstrap 边界 | 安装后发现 `00-bootstrap-guidelines` 时只报告并询问，不把 spec bootstrap 作为安装副作用静默完成。 |
| Bootstrap/docs 中文规则 | 用户确认 bootstrap 后，生成或刷新 `.trellis/spec/**` 与 `docs/**` SSOT 主文档时按业务项目中文默认规则写作。 |
| Spec update 判断 | 每个任务 closeout 前判断是否需要更新 `.trellis/spec/`，但不把 active task 或私有业务 PRD 放入公共 template / marketplace。 |
| Public docs 规范 | `.trellis/spec/docs/public-docs.md` 约束 README 安装/升级 prompt、Git 发布预检、安全和 SSOT 一致性。 |

## 8. 历史覆盖矩阵

| Issue | 状态 | 对应 PR | 已沉淀扩展 |
| --- | --- | --- | --- |
| #1 | closed | #4 merged | Middle-platform Knowledge Gate；Repo Docs SSOT reconciliation。 |
| #2 | closed | #3 merged | Auto-bootstrap 日常入口；`trellis-start` fallback 定位。 |
| #5 | closed | #12 merged | Branch Review Gate 前先执行 AI review prompt；脚本只是 recorder / validator。 |
| #6 | closed | #14 merged | `prepare-task` 默认无副作用 planner；confirmed issue creation。 |
| #7 | closed | #24 merged | publish 前必须有 AI-reviewed PR body / readiness artifact。 |
| #8 | closed | #25 merged | `planning-approval.json` 与 `phase2-check.json` 可审计 gate。 |
| #9 | closed | #13 merged | canonical overlay 与 dogfood installed copy 同步；drift check。 |
| #10 | closed | 已体现在 README / verification | 非交互安装命令、AI install/upgrade prompt、开箱验证要求。 |
| #11 | closed | #30 merged | preset installer 支持 platform overlay selection。 |
| #15 | closed | #16 merged | `no_task` 当前 checkout 直改必须显式审批。 |
| #17 | closed | #23 merged | PR body 自解释质量标准与低信息量摘要阻塞。 |
| #18 | closed | #19 merged | PR publish 只能发生在 finish-work 后。 |
| #20 | closed | #22 merged | Branch Review Gate 建立 task-local final `review.md` 人类入口和 gate digest 基线；#21 为 closed 未合并尝试，#70 在其上扩展 raw reports + rollup。 |
| #26 | closed | #28 merged | worktree 创建后继承或初始化 Trellis developer identity。 |
| #27 | closed | #29 merged | `finish-work --dry-run` 真正无副作用；Codex 默认 `sub-agent` dispatch。 |
| #31 | closed | #32 merged | Guru Team extension canonical manifest、installed provenance、`check-env` / `version.sh` 可观测入口。 |
| #33 | open | 当前任务 | Guru Team extension version 对齐 `0.6.5`；repo release tag 使用 `v0.6.5`；稳定 marketplace source 使用 `#v0.6.5`。 |
| #52 | open | 当前任务 | 显式 post-planning 审核门禁：三份规划文档链接展示后用户确认，`planning-approval.json` 使用 `explicit-post-planning-review` source，Phase 0 handoff 确认 fail closed。 |
| #43 | open | 当前任务 | Trellis sub-agent 中文逻辑角色、UI 展示名中文化、`agent-assignment.json`、reviewer 复用/更换记录和 gate digest 集成。 |
| #72 | open | 当前任务 | 默认 sub-agent mode 下强制 implement、Phase 2 check 和 Branch Review 均由 sub-agent 执行；main session 只协调，脚本只 recorder/validator。 |
| #55 | open | 当前任务 | issue intake clarity / brainstorming、issue body/comment/new issue 留痕、任务中 scope-change gate。 |
| #57 | open | 当前任务 | 业务项目 Trellis 文档语言默认中文；installer 归一化已知英文模板语言规则；bootstrap docs SSOT 中文规则。 |
| #60 | open | 当前任务 | workspace boundary guard：新增 `check-workspace-boundary` 事实快照、recorder/validator cwd 与 task-local path fail-closed 校验、source checkout 可疑 task artifact 检测、workflow/overlay/docs 绝对 worktree 路径规则；为 #76 的 source/task 双侧 liveness checker 提供事实层。 |
| #76 | open | 当前任务 | sub-agent liveness、progress/stale 判定与 replacement cutover 状态机：单一 `agent-assignment.json` 1.1 artifact、required recorder/checker、status request 前置审计、stale cutover 结构化 termination/replacement cause、completed-only recovery gate；不新增 heartbeat 文件、daemon、sidecar、long-command wrapper 或后台 liveness 进程。 |
| #70 | open | 当前任务 | Branch Review 每轮保留 `reviews/*.md` raw report；最终 `review.md` 是 rollup 并链接 raw reports；`agent-assignment.json.review_rounds[]` 与 `review-gate.json.verification_evidence.review_reports[]` 记录 raw digest；#61 顶层 artifact 表默认仍只列 final `review.md`。 |
| #78 | open | 当前任务 | Branch Review raw reports / `review.md` 继承 #57 中文 artifact 规则；workflow / overlay / docs / spec / validator 防止英文模板标题复发。 |
| #83 | open | #93 的 baseline | Planning artifact ambiguity review gate：展示三份 planning docs 前完成 AI 语义审查，`planning-approval.json` schema 1.2 记录 passed `ambiguity_review`、受控词表和七个审查维度；recorder/validator 只校验结构化 evidence。 |
| #93 | open | 当前任务 | Planning ambiguity scanner hardening：v2 受控词表、固定扫描 `prd.md` / `design.md` / `implement.md`、记录全部 `hits[]`、阻塞未分类命中和 `contract_violation`，并保持脚本不替代 AI 语义审查。 |

## 9. 当前扩展边界

已经实现的边界：

- 本仓库维护 `guru-team` 可复用 workflow 与 preset，不 fork 官方 Trellis。
- 脚本可以执行事实动作、校验 JSON/hash/HEAD/diff/dirty state，但不替代 AI 判断。
- Platform overlay 是 harness 适配层，不是新的 workflow source。
- Subagent 技术 `name` 是调度 API，不为了中文 UI 展示改名；中文展示名通过 description、标题和 `agent-assignment.json.logical_role` 表达。Codex 当前 `nickname_candidates` 只能是 ASCII，不能用它承载中文展示名。
- Task artifact 是任务证据，不是 durable docs 的替代品。
- PR publish 必须经过 finish-work 与 review/readiness evidence，不能由普通 `publish-pr` 直接触发。

尚未在本目录展开的内容：

- 每个 companion script 的完整 CLI 参数合同。
- 每个 platform overlay 的逐文件行为差异。
- Throwaway install 在不同 Trellis CLI 版本上的兼容性矩阵。
- 完整 upgrade/update 漂移测试记录。


## Push 后远端 Marketplace 门禁

修改 marketplace/preset/overlay/schema/public API 的发布路径会在 branch push 后、`gh pr create` 前执行远端分支 `init`、preview、switch 和 preset reapply，记录 task-local `marketplace-verification.json`。缺失、失败、HEAD 不匹配或 stale artifact 会阻止创建 PR；该门禁不创建 tag，AI 仍负责 PR readiness 判断。
