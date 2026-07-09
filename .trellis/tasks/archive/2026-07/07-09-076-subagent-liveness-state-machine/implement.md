# #76 实施计划

## 执行原则

- 先完成规划 review，用户确认后才进入实现。
- 不直接在 source checkout 修改；所有实现发生在 worktree `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/076-subagent-liveness-state-machine`。
- issue #76 正文是需求 / 设计 SSOT；旧 comment 中的 heartbeat、task-local heartbeat、旧 180s observation window、long-command wrapper 口径不得进入实现。
- Workflow / prompt / skill 承担 AI 判断流程；Python / Bash 只做 deterministic recorder/checker/validator/executor。
- 不新增 `{TASK_DIR}/agent-progress.jsonl`，不实现 subagent 周期 heartbeat，不实现 daemon/sidecar/long-command wrapper/background liveness 进程。
- checker 是按需启动、单次采样、立即退出的短生命周期命令。

## Phase 1 完成条件

- [x] Phase 0 intake/preflight 完成。
- [x] 创建 worktree、branch、Trellis task。
- [x] 读取 live issue #76 正文和评论。
- [x] 读取 Trellis workflow / trellis-meta / repo docs/spec / existing companion script 现状。
- [ ] 用户 review 并确认 `prd.md`、`design.md`、`implement.md`。
- [ ] 记录 `planning-approval.json` 并通过 `check-planning-approval.sh --json`。
- [ ] `task.py start` 后再进入实现。

## 实施步骤

### 0. 现有实现盘点与替代边界

1. 在写代码前再次读取并标注当前实现入口：
   - `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py` 中的 `AGENT_ASSIGNMENT_SCHEMA_VERSION`、`ALLOWED_AGENT_STATUS_EVENTS`、`ALLOWED_AGENT_STATUS_DECISIONS`、`append_agent_status_event()`、`validate_agent_assignment_payload()`、`status_event_completion_errors()`、`cmd_record_agent_assignment()`、`cmd_check_agent_assignment()`、`cmd_review_branch()`。
   - Bash wrappers：`record-agent-assignment.sh`、`check-agent-assignment.sh`、`review-branch.sh`、`check-review-gate.sh`、`check-workspace-boundary.sh`。
   - Workflow / overlay 中的旧 `record-agent-assignment.sh --status-event` 示例和 “stale 默认至少 5 分钟” 文案。
   - Durable docs 中 `Sub-agent status ledger`、`Workspace boundary snapshot`、`agent-assignment.json`、`status_events[]`、Phase 2 / Branch Review Gate 描述。

2. 明确替代关系：
   - 不新增第二个 task-local status/liveness artifact。
   - 不让 `record-agent-assignment.sh --status-event` 和 `record-subagent-liveness-event.sh` 分别维护两套 event enum / validator / stale cause。
   - `record-subagent-liveness-event.sh` 是 active liveness/status event canonical writer。
   - `record-agent-assignment.sh` 保留 review round / reuse decision；assignment 兼容入口必须改为 thin shim 调用新 `assigned` core；旧 `--status-event` 必须 fail closed 并提示改用 `record-subagent-liveness-event.sh`。
   - `check-agent-assignment.sh`、`review-branch.sh`、`check-review-gate.sh` 必须复用新 liveness validation helper；不得让旧 gate 继续只按 `supersedes_agent_id` / old coarse events 放行。

3. 对现有粗粒度 status 语义做迁移决策：
   - 旧 `wait-timeout` / `continue-waiting` 不再是 active event；由 checker decision 和 `next_wait_ms` 替代。
   - 旧 `progress-observed` 不再是 active event；由 `explicit-message-observed` / `tool-activity-observed` / `command-output-observed` / `platform-progress-observed` / `status-response-observed` 和机器 snapshot progress 替代。
   - 旧无结构化 cause 的 `stale-assessed` 不得作为新 stale cutover evidence；新 `stale-assessed` 必须来自 `last_decision == stale_allowed` 和 snapshot/digest freshness 校验。
   - 旧 `replacement-started.supersedes_agent_id` 被新 `predecessor_agent_id`、`predecessor_event_id`、`replacement_reason` 取代；legacy archived entries 可读，但 active gates 需要新字段。

### 1. Contract / docs source 更新

1. 更新 canonical workflow：
   - `trellis/workflows/guru-team/workflow.md`
   - 明确 `progress_scan_interval=120s` 与 `max_progress_silence=180s` 的不同语义。
   - 明确主会话 liveness loop：record non-machine-readable progress -> checker -> decision -> wait/status request/stale/replacement。
   - 明确 `status_request_required` 是发送 status request 的唯一授权。
   - 明确 `stale_allowed` 是记录 `stale-assessed` 的唯一授权。
   - 明确 deadline 已过后补发 `status-requested` 不延长 `max_progress_silence_deadline_at`。
   - 明确 `stale-assessed` 后同一 handling turn 必须 cutover 到 replacement，且 `replacement_reason=max_progress_silence_exceeded`。
   - 明确 unfinished/failed/stale partial output 不能作为 Phase 2 check / Branch Review Gate pass evidence。

2. 同步 dogfood workflow：
   - `.trellis/workflow.md`

3. 更新 durable specs：
   - `.trellis/spec/workflow/workflow-contract.md`
   - `.trellis/spec/workflow/data-contracts.md`
   - `.trellis/spec/workflow/companion-scripts.md`
   - `.trellis/spec/workflow/quality-guidelines.md`
   - `.trellis/spec/preset/installer.md`
   - `.trellis/spec/preset/overlay-guidelines.md`

4. 更新 durable requirements docs：
   - `docs/requirements/README.md`
   - `docs/requirements/requirement-main.md`
   - `docs/requirements/guru-team-trellis-flow.md`

5. 更新 public README / workflow README / preset README：
   - `README.md`
   - `trellis/workflows/guru-team/README.md`
   - `trellis/presets/guru-team/README.md`

### 2. Recorder / checker 脚本实现

1. 新增 Bash wrappers：
   - `trellis/workflows/guru-team/scripts/bash/record-subagent-liveness-event.sh`
   - `trellis/workflows/guru-team/scripts/bash/check-subagent-liveness.sh`

2. 在 `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py` 新增子命令：
   - `record-subagent-liveness-event`
   - `check-subagent-liveness`

3. 实现 artifact normalize：
   - 老 `agent-assignment.json` 缺少 `liveness` 时补 `{}`。
   - 老 artifact 缺少 `status_events` 时补 `[]`。
   - 保留现有 `agents[]`、`review_rounds[]`、`reuse_decisions[]` 行为。
   - 将 schema additive 升级到 `1.1`，但不得破坏 archive 中旧 `1.0` artifact 的只读校验/迁移能力。

4. 实现 snapshot 采集：
   - task worktree `HEAD`
   - task worktree `git status --porcelain`，排除 `{TASK_DIR}/agent-assignment.json`
   - task worktree `git diff --stat`，排除 `{TASK_DIR}/agent-assignment.json`
   - task worktree 非 `.git` max mtime，排除 `{TASK_DIR}/agent-assignment.json`
   - source checkout `HEAD`
   - source checkout `git status --porcelain`
   - source checkout `git diff --stat`
   - source checkout 非 `.git` max mtime
   - progress events count/digest/newest event id

5. 实现 event recorder：
   - `assigned`
   - progress events: `explicit-message-observed`、`tool-activity-observed`、`command-output-observed`、`platform-progress-observed`、`status-response-observed`
   - `workspace-boundary-violation`
   - `status-requested`
   - `status-request-failed`
   - `stale-assessed`
   - `resume-same-agent`
   - `replacement-started`
   - `terminated-unfinished`
   - `completed`
   - `failed`

6. 实现 event validator：
   - 通用字段非空 / 枚举 / ISO-8601 UTC / HEAD / evidence。
   - event-specific 参数必须提供或必须省略。
   - `resume-same-agent` 前置证据只能是同 agent 的 `failed` 或 `terminated-unfinished manual_or_platform_terminated_unfinished`。
   - `replacement-started` 前置证据和 `replacement_reason` 必须匹配。
   - stale cutover 必须有 `stale-assessed -> terminated-unfinished stale_cutover -> replacement-started` 链路。
   - `terminated-unfinished` 必须结构化区分 `stale_cutover` 与 `manual_or_platform_terminated_unfinished`。
   - `stale-assessed` 前必须验证 `last_decision == stale_allowed` 且当前 snapshot / progress digest 未变化。
   - legacy coarse status events 仅作为旧 artifact 可读兼容，不得作为新的 progress/stale/pass evidence。

7. 实现 checker decision engine：
   - 固定优先级：blocked -> source progress -> task/status event progress -> status request required -> continue waiting -> stale allowed。
   - 输出唯一 decision JSON。
   - 输出 `max_progress_silence_deadline_at` 与 `next_wait_ms`。
   - `status_request_required` / `stale_allowed` / `blocked_missing_evidence` 的 `next_wait_ms=0`。
   - `continue_waiting_no_repeat_ping` 不睡过 deadline。
   - progress 类 decision 用刷新后的 anchor 重新计算。
   - deadline 已过但无 pending request 时仍先输出 `status_request_required`。
   - `status-requested` 不延长 deadline。

### 3. Gate 集成

1. 更新 `check-agent-assignment.sh` / Python validator：
   - 识别 `liveness` schema。
   - 校验新的 `status_events[]` 枚举与字段。
   - 校验 unclosed stale/unfinished/replacement chain。
   - 确保 `stale-assessed` 后没有 `resume-same-agent`。
   - 确保 stale replacement chain 到达 replacement `completed` 才能进入 pass evidence。
   - 确保 `failed` / manual unfinished 后有 same-agent resume 或 replacement，并且后续 `completed` 才能进入 pass evidence。
   - 替换现有 `status_event_completion_errors()` 的旧 `supersedes_agent_id` 链路判断，使该函数调用同一新 liveness chain validator；不能保留一条旧 gate pass 路径。
   - 对 review finding owner replacement，继续校验既有 `reuse_decisions[] decision=replace from_round/to_round`，并额外校验新 `replacement-started` / terminal chain 与 review round replacement 互相一致。

2. 更新 `record-phase2-check.sh` / `review-branch.sh` 相关校验：
   - Phase 2 check pass 不能使用 unfinished/failed/stale partial output。
   - Branch Review Gate pass 必须 fail closed 于未闭环 `terminated-unfinished`、stale cutover 缺 replacement completed、replacement failed 未恢复等状态。
   - 现有 review-round closure/fresh final reviewer 逻辑保持兼容。

3. 保持脚本边界：
   - recorder/checker 只校验 objective artifact completeness。
   - AI review 仍决定实现是否满足需求、review 是否通过、issue 是否可关闭。

### 4. Overlay / prompt / subagent 文案

1. 更新 continue entries：
   - canonical overlay `.agents/skills/trellis-continue/SKILL.md`
   - `.codex/prompts/trellis-continue.md`
   - `.codex/skills/trellis-continue/SKILL.md`
   - Cursor / Claude equivalents

2. 更新 implement/check/review subagent prompts：
   - 不要求定时 heartbeat。
   - 收到 status request 后要求通过平台可见消息回复当前状态。
   - unfinished handoff 必须包含 predecessor output、当前 diff、task artifacts、剩余工作、gate blockers。
   - failed / unfinished / stale partial output 不能声明 pass。
   - review subagent 入口若由 `trellis-check` / Branch Review Gate prompt 复用承载，也必须同步同一 liveness、partial-output 和 pass-evidence 规则；不得只更新 implement/check 执行代理。
   - 删除或替换所有 `record-agent-assignment.sh --status-event` 的 active status 示例，统一改为 `record-subagent-liveness-event.sh` / `check-subagent-liveness.sh` 流程；保留 `record-agent-assignment.sh` 仅用于 review round / reuse decision 的文案。
   - 删除或替换所有 “stale 默认至少 5 分钟” 文案，统一改为 `progress_scan_interval=120s`、`max_progress_silence=180s` 和 checker decision 语义。

3. 更新 `.trellis/agents/implement.md` / `.trellis/agents/check.md` channel runtime agent definitions 和平台-specific agent definitions。

4. 应用 preset 到 dogfood：
   - `trellis/presets/guru-team/scripts/bash/apply.sh --repo .`
   - 处理 `.new` / `.bak`
   - `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`

### 5. Preset installer / managed assets

1. 更新 `MANAGED_ASSET_PATHS`，加入新增 Bash scripts。
2. 确认 installer 对新脚本设置 executable bit。
3. 更新 installer tests：
   - 新脚本被复制到 `.trellis/guru-team/scripts/bash/`
   - 新脚本 executable
   - config preservation 不受影响
   - overlay drift 不受影响
4. 更新 `trellis/presets/guru-team/README.md` installed-file list。

### 6. 测试补齐

#### Unit tests: recorder

- [ ] `assigned` 创建 `agents[]` 并初始化 liveness baseline；`assigned_at=observed_at`、`assigned_head=current HEAD`、`reason=evidence`。
- [ ] progress events 写入后 checker 能识别 progress digest 更新。
- [ ] `status-requested` 设置 pending request 但不刷新 anchor。
- [ ] `status-request-failed` 不设置 pending request，后续 checker 不得输出 `stale_allowed`。
- [ ] `completed` / `failed` 清除 pending request。
- [ ] `stale-assessed` 只有 `last_decision == stale_allowed` 且 snapshot/digest 未变化时才能写入。
- [ ] `stale-assessed` 写入前新增 progress event/task change/source change 时 recorder 拒绝并要求重跑 checker。
- [ ] `terminated-unfinished` 缺 `termination_reason` 失败。
- [ ] `stale_cutover` 缺或错 `termination_source_event_id` 失败。
- [ ] `manual_or_platform_terminated_unfinished` 带 `termination_source_event_id` 失败。
- [ ] `resume-same-agent` 引用 `stale-assessed` 或 stale cutover 失败。
- [ ] `replacement-started` 缺 `predecessor_event_id` / `replacement_reason` 失败。
- [ ] `replacement-started.replacement_reason` 与 predecessor event 不匹配失败。
- [ ] `record-agent-assignment.sh --status-event` 必须 fail closed，不能独立写旧 coarse status event，错误信息必须提示使用 `record-subagent-liveness-event.sh`。
- [ ] 旧 `wait-timeout` / `continue-waiting` / 粗粒度 `progress-observed` 不能作为新 checker progress source、`stale-assessed` 前置证据或 gate pass evidence。
- [ ] 旧 `replacement-started.supersedes_agent_id` 不能绕过新 `predecessor_event_id` / `replacement_reason` / `termination_source_event_id` 校验。

#### Unit tests: checker

- [ ] task worktree `HEAD` 变化 -> `progress_observed`。
- [ ] task worktree dirty status 变化 -> `progress_observed`。
- [ ] task worktree diff stat 变化 -> `progress_observed`。
- [ ] task worktree mtime 变化 -> `progress_observed`。
- [ ] source checkout `HEAD` 变化 -> `workspace_boundary_violation_progress`。
- [ ] source checkout dirty status 变化 -> `workspace_boundary_violation_progress`。
- [ ] source checkout diff stat 变化 -> `workspace_boundary_violation_progress`。
- [ ] source checkout mtime 变化 -> `workspace_boundary_violation_progress`。
- [ ] recorded `explicit-message-observed` / `tool-activity-observed` / `command-output-observed` / `platform-progress-observed` / `status-response-observed` -> `progress_observed`。
- [ ] 已有 pending status request 后出现任一新 progress -> 刷新 `progress_anchor_at`、清除 `pending_status_request_at`，新的无 progress 周期才进入下一次 `status_request_required`。
- [ ] 无新 progress 且无 pending request -> `status_request_required`。
- [ ] 无新 progress 且 pending request 未过 deadline -> `continue_waiting_no_repeat_ping`。
- [ ] 无新 progress 且 pending request 已过 deadline -> `stale_allowed`。
- [ ] 无 pending request 且 deadline 已过 -> 仍输出 `status_request_required`；记录 `status-requested` 后立即重跑才可 `stale_allowed`。
- [ ] `next_wait_ms` 不超过剩余 deadline，默认首次 status request 后不超过 60000ms。
- [ ] 既有 dirty diff / 旧 event 不重复刷新 anchor。
- [ ] 迟到 progress event observed_at 早于当前 anchor 不回拨 anchor。
- [ ] recorder 的 control/bookkeeping event 和 `agent-assignment.json` mtime/diff/digest 不误判为 progress。
- [ ] artifact/schema/snapshot/source repo 缺失 -> `blocked_missing_evidence`。

#### Gate tests

- [ ] 只有 `stale-assessed`、缺 `terminated-unfinished -> replacement-started`，Phase 2 check / Branch Review Gate fail closed。
- [ ] stale cutover replacement 未 `completed`，pass gate fail closed。
- [ ] replacement `failed` 后未继续恢复，pass gate fail closed。
- [ ] failed/manual unfinished 后无 resume/replacement completion，pass gate fail closed。
- [ ] `completed` event 本身不等于 Phase 2 check / Branch Review Gate pass。
- [ ] Existing review round / raw report / fresh final reviewer tests 继续通过。
- [ ] `check-agent-assignment.sh` 与 `review-branch.sh --agent-assignment` 对新 liveness chain 使用同一 validator；不存在旧 status chain 能通过而新 liveness chain 失败的分叉。
- [ ] review finding owner replacement 同时要求新 liveness `replacement-started` recovery chain 与既有 `reuse_decisions[] decision=replace from_round/to_round` 一致。

#### Installer / overlay tests

- [ ] preset installer 复制新增 scripts。
- [ ] scripts executable。
- [ ] README installed-file list 覆盖新增 scripts。
- [ ] overlay 文案不再出现旧 heartbeat / 5 分钟 stale / long-command wrapper 口径。
- [ ] dogfood overlay drift check 通过。

## 验证命令计划

实施后至少运行：

```bash
bash -n trellis/workflows/guru-team/scripts/bash/*.sh
bash -n .trellis/guru-team/scripts/bash/*.sh
python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py
python3 -m py_compile .trellis/guru-team/scripts/python/guru_team_trellis.py
python3 -m unittest trellis.workflows.guru-team.scripts.python.test_guru_team_trellis
python3 trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py
python3 trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py
python3 -m json.tool trellis/index.json
python3 -m json.tool trellis/workflows/guru-team/schemas/intake-handoff.schema.json
python3 ./.trellis/scripts/task.py validate
python3 ./.trellis/scripts/get_context.py --mode phase
trellis/presets/guru-team/scripts/bash/apply.sh --repo .
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
git diff --check origin/main...HEAD
```

`python3 -m unittest ...` 的 module path 可能因 hyphen 目录不可导入而不适用；若失败，应使用现有 repo 惯例的 file-path runner，并在 Phase 2 check 记录原因。

## 开箱即用 / upgrade-update 验证计划

### 必须验证或报告未验证

- [ ] `trellis/index.json` 仍能被 Trellis 识别，`guru-team` workflow id/path/type 正确。
- [ ] README 中的新项目安装命令必须能安装 Guru Team workflow。
- [ ] 已有项目必须能通过 `trellis workflow --marketplace ... --template guru-team --create-new` 预览，并能切换 `.trellis/workflow.md`。
- [ ] preset installer 安装 `.trellis/guru-team/`、platform overlay、scripts、schema、config template，新增 recorder/checker scripts 有 executable permission。
- [ ] 新安装项目无历史 patch 时必须能运行 `get_context.py`、Phase 0 intake/preflight（`check-env.sh` / `prepare-task.sh`）、planning approval checks、`record-subagent-liveness-event.sh`、`check-subagent-liveness.sh`、`check-agent-assignment.sh`、Phase 2 check artifact validators、Branch Review Gate validators 和 finish-work readiness 入口。
- [ ] throwaway repo 或干净临时 repo 中验证 Guru Team workflow / preset 安装后，planning、check、review gate、finish-work 预期入口都可发现并可执行；如无法完整跑通，最终报告必须列出未验证入口与风险。
- [ ] Codex / Claude / Cursor / channel runtime agent 文案一致，不出现某个平台保留旧 heartbeat / 5 分钟 stale / long-command wrapper 口径。
- [ ] README 安装命令真实可执行，不依赖本机隐藏状态。

### 可能受限项

如果本地无法完整跑 throwaway `trellis init` 或 GitHub marketplace branch source 验证，最终报告必须明确哪些开箱即用/upgrade-update 门禁未验证、风险是什么、已用哪些替代命令覆盖。

## Branch Review Gate 计划

实现完成并通过 Phase 2 check 后：

1. 提交 task work commit。
2. 派发独立 review subagent 审查 `origin/main...HEAD` 完整 diff。
3. 记录 task-local `reviews/*.md` raw report 和最终 `review.md` rollup。
4. 通过 `agent-assignment.json` 记录 review round、status/reuse/replacement chain。
5. 用 `review-branch.sh --review-source independent-agent --review-report <task-local review.md> --agent-assignment <task-local agent-assignment.json>` 记录 Branch Review Gate。
6. 任意 finding 都阻断；修复后必须 same-agent closure 或完整 replacement closure chain，再派发 fresh 最终放行审查代理。
7. Gate 必须覆盖 docs、code、tests、Trellis artifacts、config、scripts、schemas、CI/CD、container、K8s/Kustomize/Helm、DB migration、Makefile、preset installer、generated marketplace files、Issue Scope Ledger、publish readiness。

## Rollback / 风险点

- 风险：新 liveness schema 破坏旧 `agent-assignment.json`。缓解：additive normalize，老字段保留，新增 tests。
- 风险：旧 `record-agent-assignment.sh --status-event` 与新 `record-subagent-liveness-event.sh` 并存导致两个 stale/replacement 解释。缓解：旧 status path fail closed，workflow/overlay/docs 删除旧 active status 示例，新增 no-duplicate tests。
- 风险：checker 把 artifact 自身 mtime/diff 当 progress。缓解：snapshot 明确排除 `{TASK_DIR}/agent-assignment.json`，并有回归测试。
- 风险：deadline 已过后补发 `status-requested` 错误延长 deadline。缓解：`max_progress_silence_deadline_at` 始终来自 `progress_anchor_at + max_progress_silence`。
- 风险：旧 overlay 保留 5 分钟 stale / heartbeat 文案。缓解：全 overlay `rg` 搜索，apply dogfood，drift check。
- 风险：脚本越界判断 AI review 质量。缓解：脚本只校验 objective event/chain/schema，不生成 pass 判断。

## 本轮规划后的下一步

等待用户 review 本 task 的 `prd.md`、`design.md`、`implement.md`。确认后，主会话再记录 planning approval、启动 task，并进入 Phase 2 实现。
