# #76 subagent liveness、progress/stale 判定与 replacement cutover 状态机

## 需求来源与取舍

- Source issue: https://github.com/castbox/guru-trellis/issues/76
- Live title: `subagent liveness、progress/stale 判定与 replacement cutover 状态机`
- 最新读取时间：2026-07-09，本 task 以 issue 正文为需求 / 设计 SSOT。
- Issue comment 取舍：2026-07-08 17:57:40Z 的最新澄清明确当前 issue 正文取代旧 comment 中的 heartbeat、task-local heartbeat、旧语义 180s observation window、long-command wrapper 口径；实现与验收只按正文执行。
- `Refs #60` 与 `Refs #62` 是背景依赖，不纳入本任务 close scope。#76 本身是 `issue-scope-ledger.json.close_issues[]` 的唯一默认候选，publish 前必须由实现、验证和 Branch Review Gate 补齐验收证据。

## 背景

#62 已明确：`wait_agent` timeout 只是等待窗口结束，不代表 subagent 失败，也不能把未完成 subagent 的半成品当作完成证据。#70 暴露了新的缺口：主会话缺少可执行的 subagent liveness 判断流程，容易在已有公开进展时误判 subagent stale。

真实案例中，implement subagent 一直有输出，但先写到了 source checkout，随后才把改动挪到 task worktree。主会话只检查 task worktree，导致多次 `wait_agent` timeout 被误判为无进展，错误终止仍在工作的 subagent。这个问题关联 #60：source checkout 出现新改动本身就是“有进展但写错位置”的信号，必须先按 progress 处理，再进入 workspace boundary 纠偏。

本任务不是给 subagent 增加定时 heartbeat，也不是让主会话凭记忆判断 stale；目标是用 task-local liveness artifact、required recorder、required checker 和 fail-closed gate，把“继续等待 / 请求状态 / stale_allowed 与 stale-assessed 成立条件 / 何时必须替换”的判断固定成可审计状态机。

## 核心目标

1. 定期判定 subagent 是否 alive：主会话必须以不超过 `progress_scan_interval=120s` 的间隔运行 liveness checker。checker 的 progress 判定覆盖两类公开 evidence：主会话已写入 `status_events[]` 的非机器可读 progress，以及 checker 本次采集到的机器可读 task/source checkout 变化。
2. Alive 存疑时立即 ping：本轮 checker 未发现新 progress 且当前没有 pending status request 时，必须输出 `status_request_required`；主会话必须立即向 subagent 发送显式 status request，并把公开回复记录为 `status-response-observed`，作为 progress 刷新 liveness。
3. 及时判定 stale：从 `progress_anchor_at` 起算，主会话不得让无 progress 状态超过 `max_progress_silence=180s` 后仍无判定；只有已有 pending `status-requested`、未产生 progress 响应、无任何新 progress、且 `checked_at >= max_progress_silence_deadline_at` 时，checker 才能输出 `stale_allowed`，主会话才可记录 `stale-assessed`。
4. 及时精确替换已 stale 的 subagent：`stale-assessed` 成功写入后，后续 `replacement-started.replacement_reason` 必须是 `max_progress_silence_exceeded`。status request 未产生 progress 是防误判的必要确认条件，不是 replacement 的唯一原因。主会话不得继续等待或 resume stale predecessor，必须在同一 liveness handling turn 内完成 `terminated-unfinished termination_reason=stale_cutover -> replacement assigned -> replacement-started` cutover，并用 `predecessor_agent_id`、`predecessor_event_id`、`handoff_summary` 和后续 replacement `completed` 证据闭环。

## 目标用户与问题

目标用户是 Guru Team Trellis workflow 中会派发 subagent 的主会话、实现代理、检查代理和后续 review gate。主会话必须能在 subagent 长时间运行、`wait_agent` 单次等待窗口结束、平台 UI 有非机器可读输出、或 task/source checkout 发生变化时，做出可审计、可重复的 liveness 判断。

本任务要解决的问题：

- `wait_agent` timeout 不能代表 subagent 失败或 stale。
- 只看 task worktree 会漏掉 source checkout 中的真实进展。
- 只凭主会话记忆或聊天 UI 判断 stale 不可审计。
- 要求 subagent 定时写 heartbeat 或启动后台 wrapper 不能可靠保证。
- 过去缺少明确 replacement cause 和 replacement timing，导致仍有 progress 的 subagent 被轻率替换。

## In Scope

- Guru Team workflow、platform prompts、skills、subagent prompts 中关于 subagent liveness、status request、stale、resume、replacement、termination 和 gate evidence 的流程文字。
- task-local `agent-assignment.json` 中 agent assignment、liveness state、workspace snapshot 和 `status_events[]` 审计流。
- required recorder/checker companion scripts、Bash CLI 入口、schema/validator、preset managed assets、overlay 安装和 dogfood drift 检查。Bash CLI 入口只指 recorder/checker 薄入口，不包括 long-command wrapper、后台 heartbeat wrapper 或常驻进程。
- task worktree 与 source checkout 的机器可读 progress 检测：`HEAD`、dirty status、diff stat、非 `.git` 文件 mtime。
- 非机器可读 progress 的主会话记录入口：显式消息、tool activity、命令输出、平台 progress/status event 和 status response。
- replacement cause、replacement timing、predecessor termination/cutover、handoff summary 和 replacement completion chain 的结构化记录与 gate 校验。
- 默认时间窗口：`progress_scan_interval=120s`、`max_progress_silence=180s`。
- 现有 `agent-assignment.json` / `record-agent-assignment.sh` / `check-agent-assignment.sh` / `review-branch --agent-assignment` 能力的替代与兼容：本任务不得新增第二套同目的 assignment/status ledger；必须在同一个 task-local artifact 和同一组 validator/gate 里收敛旧粗粒度 status 语义与新 liveness 状态机。
- Canonical 与 dogfood 同步：`trellis/workflows/guru-team/**`、`trellis/presets/guru-team/**`、`.trellis/guru-team/**`、`.trellis/workflow.md`、`.agents/.codex/.cursor/.claude/.trellis/agents` overlay 副本。
- Durable docs / spec 更新：`docs/requirements/**`、`.trellis/spec/workflow/**`、`.trellis/spec/preset/**`。

## Out of Scope / 非目标

- 不实现 subagent 自主定时 heartbeat。
- 不新增 `{TASK_DIR}/agent-progress.jsonl` 或其它 task-local heartbeat 文件合同。
- 不要求 daemon、sidecar、long-command wrapper 或后台进程定时写 liveness。
- 不读取或依赖 subagent private thinking。
- 不让 subagent 写 liveness 状态。
- 不让 checker 读取平台 UI 或推断不可机器读取的 tool/message/progress stream。
- 不让脚本判断实现是否充分、review 是否通过、issue 是否可关闭；脚本只做 recorder / validator / checker。
- 不把 status response 当作实现完成、Phase 2 check 完成或 Branch Review Gate 通过证据。

## 功能需求

### Liveness baseline 与调度

1. 派发 subagent 后，主会话必须记录 `assigned`，并建立该 agent 的 liveness 基线。基线只作为静默计时起点，不作为 progress evidence。
2. 主会话必须按 checker 输出的 `next_wait_ms` 等待 subagent；初始等待为 120000ms，后续不得固定 sleep 到越过最大静默 deadline。
3. 每次等待结束或观测到 progress 后，主会话必须先把非机器可读 progress 写入 artifact，再调用 checker 获取唯一 decision。

### Progress 判定

4. checker 本次调用只对当前采集到的 task worktree snapshot 与 `last_scan_snapshot` 做比较；如果发现新机器可读变化，输出 `progress_observed`，刷新 progress anchor，主会话继续等待同一 agent。
5. checker 本次调用只对当前采集到的 source checkout snapshot 与 `last_scan_snapshot` 做比较；如果发现新机器可读变化，输出 `workspace_boundary_violation_progress`，刷新 progress anchor，主会话要求纠偏到 task worktree，并阻止 stale。
6. 任一新增公开 progress 都必须纳入判断：subagent 显式消息、tool calls、命令输出、平台 progress/status event、task worktree 变化、source checkout 变化、status request 的回复。
7. 脚本无法直接读取的平台/UI progress 必须由主会话显式记录到 `status_events[]` 后才可成为 checker evidence。
8. 只有相对上一轮 scan 的新增变化才算 progress。未变化的既有 dirty diff、旧事件、control/bookkeeping event 和 liveness artifact 自身变化不能反复刷新 `progress_anchor_at`。
9. 被记录 `terminated-unfinished` 的 predecessor 后续迟到输出只能作为 predecessor audit evidence 记录，不得刷新 predecessor 或 replacement agent 的 `progress_anchor_at`，不得取消已启动的 replacement chain。

### Status request 与 stale

10. 无任何新 progress 且 artifact 中没有 pending status request 时，checker 必须输出 `status_request_required`；主会话只有在该 decision 下才能发送 status request。
11. status request 发送成功后，主会话必须记录 `status-requested`，立即再次运行 checker，并使用新的 `next_wait_ms`；发送失败时记录 `status-request-failed`，但不得设置 pending request 或进入 stale/terminate/replacement。
12. 已有 pending status request 且 `checked_at < max_progress_silence_deadline_at` 时，checker 必须输出 `continue_waiting_no_repeat_ping`；主会话继续等待且不重复发送 status request。
13. 只有无新 progress、存在 pending status request、该 request 未产生 progress 响应、且 `checked_at >= max_progress_silence_deadline_at` 时，checker 才能输出 `stale_allowed`；主会话只有在该 decision 下才能记录 `stale-assessed`。
14. 如果没有 pending status request，即使 `checked_at >= max_progress_silence_deadline_at`，checker 也必须先输出 `status_request_required`；deadline 已过后补发的 `status-requested` 只补齐 stale 前置审计条件，不得延长 `max_progress_silence_deadline_at`。
15. `status-requested` 本身不刷新 `progress_anchor_at`，不会延后 `max_progress_silence_deadline_at`。

### Replacement / resume / terminal

16. `completed` 只表示 agent 执行链路结束；仍必须经过 Phase 2 check 和 Branch Review Gate。
17. `failed` 不能作为 pass evidence，后续必须 same-agent resume 或 replacement completion 后才能进入 pass gate。
18. `stale-assessed` 成功写入后，表示 checker 已证明 predecessor 满足 stale replacement 前置证据：从 `progress_anchor_at` 起已超过 `max_progress_silence`、无任何新 progress、已成功发送一次 status request、该 request 未产生 progress 响应、且 `checked_at >= max_progress_silence_deadline_at`。
19. `stale-assessed` 后不得继续等待 predecessor，不得记录 `resume-same-agent`，后续 `replacement-started.replacement_reason` 必须是 `max_progress_silence_exceeded`。
20. `stale-assessed` 后必须在同一 liveness handling turn 内记录 `terminated-unfinished termination_reason=stale_cutover termination_source_event_id=<stale-assessed.event_id>`，再派发 replacement 并记录新 agent 的 `assigned`，随后记录 `replacement-started predecessor_event_id=<stale-assessed.event_id> replacement_reason=max_progress_silence_exceeded`。
21. 平台没有 stop/interrupt 原语时，`terminated-unfinished` 表示 workflow 层停止接受 predecessor 后续输出作为 pass evidence；predecessor 迟到输出只能作为 audit evidence。
22. `replacement-started` 必须通过 `predecessor_event_id` 引用 predecessor 的 `stale-assessed`、`failed` 或 `terminated-unfinished` 证据，并记录 `replacement_reason`、`predecessor_agent_id`、`predecessor_event_id` 和 `handoff_summary`。
23. `handoff_summary` 必须覆盖 predecessor output、当前 diff、task artifacts、剩余工作和 gate blockers。
24. `failed` 或 `terminated-unfinished termination_reason=manual_or_platform_terminated_unfinished` 后，后续仅能通过 `resume-same-agent` 或 `replacement-started` 继续；只有后续 same-agent 或 replacement agent 产生 `completed` 后，最终输出才能进入 pass gate。

## Artifact / 审计需求

- 当前 task 的 liveness 单一 artifact 必须是 `{TASK_DIR}/agent-assignment.json`。
- artifact 必须包含 `agents[]`、`liveness[agent_id]`（含 `last_scan_snapshot`）和 `status_events[]`。
- `status_events[]` 必须记录 progress、terminal、workspace-boundary audit 和 control/bookkeeping 事件，且每条事件必须包含可追溯 evidence。
- checker/recorder 写 artifact 必须原子化，失败时不得留下半截 JSON。
- artifact/schema/snapshot 缺失或不可校验时必须 fail closed，不能 stale、terminate、replacement、Phase 2 check 或 Branch Review Gate。
- 当前仓库已有 `agent-assignment.json.status_events[]` 粗粒度记录能力。本任务必须把它替换为 issue #76 的精确事件合同：旧 `wait-timeout` / `continue-waiting` / 粗粒度 `progress-observed` / 无结构化 cause 的 `stale-assessed` 等主动写入路径不得与新 recorder 并存。旧 `record-agent-assignment.sh --status-event` 必须 fail closed 并提示改用 `record-subagent-liveness-event.sh`；旧 assignment 兼容入口必须改为 thin shim 调用同一个 `assigned` core，不得独立写 `agents[]` 或 `status_events[]`。

## 角色职责

- Main Session：观察平台可见事件、调用 recorder/checker、发送 status request、根据 checker decision 推进 wait/resume/replacement/terminate 分支。
- Subagent：就 liveness 合同而言，不负责写 liveness，不承担定时输出义务；收到 status request 后必须通过平台可见消息回复当前状态。正常执行中的显式消息、tool activity 或命令输出属于 progress source。
- Recorder：只负责记录和校验事件、维护 artifact 字段、执行 fail-closed 约束；不得判断 subagent 是否卡死或实现是否充分。
- Checker：主会话按需启动的短生命周期命令；只在单次调用内采集一次机器可读 snapshot、比较 artifact 状态、更新 liveness 字段、输出唯一 decision JSON 并退出；不得常驻、watch、sleep、等待 subagent、发送 status request、读取平台 UI 或替代 review 判断。

## 成功标准

- 有任何新增 progress 时，系统不会发送 status request 或 stale，而是输出 `progress_observed` / `workspace_boundary_violation_progress` 并继续等待或进入 workspace boundary 纠偏。
- 没有新增 progress 且没有 pending request 时，checker 输出 `status_request_required`，主会话会且只会针对当前无 progress 周期发送一次 status request；后续只有新 progress 刷新 `progress_anchor_at` 并清除 pending request 后，新的无 progress 周期才进入下一次 status request 发送路径。
- 已发送 status request、无新增 progress、且 `checked_at < max_progress_silence_deadline_at` 时，checker 输出 `continue_waiting_no_repeat_ping`，主会话继续等待且不重复发送 status request。
- 已发送 status request、无新增 progress、且 `checked_at >= max_progress_silence_deadline_at` 时，checker 才能输出 `stale_allowed`，主会话才能记录 `stale-assessed`。
- `stale-assessed` 成功写入后，系统能精确记录 stale replacement 前置证据，并在后续 `replacement-started.replacement_reason` 写入 `max_progress_silence_exceeded`，表示最大无 progress 时间窗超时，而不是仅因 status request 本身未产生回复；及时完成 `terminated-unfinished termination_reason=stale_cutover -> replacement assigned -> replacement-started -> replacement completed` replacement chain；不得继续等待或 resume stale predecessor。若 replacement `failed`，必须继续恢复或再次 replacement，不能进入 pass gate。
- 所有 `stale-assessed`、`terminated-unfinished`、`resume-same-agent`、`replacement-started`、`completed`、`failed` 和 gate 使用的证据都能在 artifact 中追溯。
- 新安装项目通过 preset/overlay 后具备同一 liveness 合同、脚本、schema、prompt/workflow 文案和测试覆盖。

## Acceptance Criteria

### 合同与 artifact

- [ ] 不新增 `{TASK_DIR}/agent-progress.jsonl` 或 task-local heartbeat 文件合同。
- [ ] subagent prompt 不再要求定时写 heartbeat，也不承诺 subagent 每 120 秒一定有产出。
- [ ] `agent-assignment.json` schema 明确定义 `liveness[agent_id]`（含 `last_scan_snapshot`）和 `status_events[]` 的必填字段、事件枚举、decision 枚举。
- [ ] `last_scan_snapshot` 必须包含 `progress_events_count`、`progress_events_digest`、`progress_events_newest_event_id`，且三者只统计 progress events。
- [ ] recorder 对 `assigned` 创建 `agents[]` 的字段映射固定：`assigned_at=observed_at`、`assigned_head=current HEAD`、`reason=evidence`。
- [ ] `completed` 只进入正常审查，不等于 Phase 2 check 或 Branch Review Gate pass。
- [ ] Phase 2 check / Branch Review Gate 不能把 unfinished/failed/stale subagent partial output 当作 pass evidence。

### Recorder

- [ ] 提供 `record-subagent-liveness-event.sh`，能写入并校验 `assigned`、progress events、`workspace-boundary-violation`、`status-requested`、`status-request-failed`、`status-response-observed`、`stale-assessed`、resume/replacement/terminal events。
- [ ] `resume-same-agent` 必须结构化记录 `predecessor_event_id` 和 `handoff_summary`。
- [ ] validator 能校验 `resume-same-agent.predecessor_event_id` 引用同一 agent 已存在的 `failed` 或 `terminated-unfinished termination_reason=manual_or_platform_terminated_unfinished` 证据。
- [ ] `resume-same-agent` 不得引用 `stale-assessed` 或 `terminated-unfinished termination_reason=stale_cutover`。
- [ ] `replacement-started` 必须结构化记录 `predecessor_agent_id`、`predecessor_event_id`、`replacement_reason` 和 `handoff_summary`。
- [ ] validator 能校验 replacement 新 agent 已 assigned、`predecessor_event_id` 引用 predecessor 的 `failed`、`stale-assessed` 或 `terminated-unfinished` 证据，且 `replacement_reason` 与该 evidence event 匹配。
- [ ] stale cutover 的 `replacement-started` 必须引用 `stale-assessed`，且同一 predecessor 已存在后续 `terminated-unfinished termination_reason=stale_cutover termination_source_event_id=<same stale-assessed.event_id>`。
- [ ] `terminated-unfinished` 必须结构化记录 `termination_reason` 和 `handoff_summary`，覆盖 predecessor output、当前 diff、剩余工作和 gate blockers。
- [ ] `termination_reason=stale_cutover` 时必须结构化记录 `termination_source_event_id` 并引用同一 agent 的 `stale-assessed`。
- [ ] `termination_reason=manual_or_platform_terminated_unfinished` 时 `termination_source_event_id` 必须为空。
- [ ] recorder 在 `stale-assessed` 前校验 `last_decision == stale_allowed`，并验证当前 task/source 机器 snapshot 与 progress event count/digest/newest event id 仍匹配 `last_scan_snapshot`；否则 fail closed 并要求重跑 checker。

### Checker

- [ ] 提供 `check-subagent-liveness.sh`，作为按需启动、单次采样、立即退出的短生命周期命令。
- [ ] checker 能采集 task/source checkout snapshot，比较 `last_scan_snapshot`，更新 artifact，并输出唯一 decision JSON。
- [ ] `progress_sources[]` 必须按固定结构列出触发 progress 的机器可读来源。
- [ ] checker 输出 `max_progress_silence_deadline_at` 和 `next_wait_ms`，且 `next_wait_ms` 不得让主会话睡过最大静默 deadline。
- [ ] `progress_anchor_at` 的刷新取时规则必须按机器 snapshot `captured_at`、最新 progress event `observed_at`、source snapshot `captured_at` 固定实现，并且 anchor 必须单调不回退。
- [ ] checker 按 decision 输出 `next_wait_ms`：`status_request_required` / `stale_allowed` / `blocked_missing_evidence` 必须为 0；`continue_waiting_no_repeat_ping` 不得超过剩余 deadline；progress 类 decision 必须基于刷新后的 anchor 重新计算。
- [ ] source checkout 有新 `HEAD` / dirty status / diff stat / mtime 变化时，checker 输出 `workspace_boundary_violation_progress`，不会判定 stale，也不会只记录普通 progress。
- [ ] `stale_allowed` 必须满足：`checked_at >= max_progress_silence_deadline_at`、存在 pending `status-requested` 且未产生 progress 响应、且没有任何新 progress。

### Workflow / gate

- [ ] workflow 明确：非机器可读 progress 必须由主会话 recorder 写入 `status_events[]` 后才算 checker evidence。
- [ ] workflow 明确：`progress_scan_interval=120s` 到期只触发 checker 扫描并取得 decision；`max_progress_silence=180s` 是从 `progress_anchor_at` 起算的 stale eligibility threshold；checker 只在已有 pending status request 且未产生 progress 响应后输出 `stale_allowed`。
- [ ] workflow 明确：只有相对上一轮 scan 的新变化才算 progress；既有 dirty diff 或旧 event 不能反复刷新 anchor。
- [ ] workflow 明确：`{TASK_DIR}/agent-assignment.json` 的 liveness/bookkeeping 写入不算 task worktree content progress，control/bookkeeping event 不得通过 mtime/digest 间接刷新 anchor。
- [ ] workflow 明确：`status-requested` 本身不算 progress，不能刷新 anchor。
- [ ] workflow 明确：已有 pending status request 时不重复发送 status request。
- [ ] workflow 明确：只有 checker 输出 `status_request_required` 时主会话才能发送 status request。
- [ ] workflow 明确：status request 发送成功并记录 `status-requested` 后，主会话必须立即再次调用 checker，不能沿用发送前的旧 decision/timeout。
- [ ] workflow 明确：无新 progress 且无 pending status request 时，即使 `checked_at >= max_progress_silence_deadline_at`，checker 也必须输出 `status_request_required`，不得直接输出 `stale_allowed`。
- [ ] workflow 明确：deadline 已过后才首次得到 `status_request_required` 时，主会话发送并记录 `status-requested` 后必须立即再次运行 checker；若仍无新 progress，checker 必须输出 `stale_allowed`；该补发的 `status-requested` 不得延长 deadline。
- [ ] workflow 明确：只有 checker 输出 `stale_allowed` 时主会话才能记录 `stale-assessed`；只有 `stale-assessed` 成功写入后，stale replacement cutover 才能记录 `terminated-unfinished termination_reason=stale_cutover` 并启动 replacement。
- [ ] workflow 明确：checker 输出 `stale_allowed` 后、`stale-assessed` 写入前，如果主会话又观察到任何新的公开 progress，必须先记录该 progress 并重跑 checker。
- [ ] workflow 明确：`stale-assessed` 成功写入后表示 stale replacement 前置证据已成立；后续 `replacement-started.replacement_reason` 必须记录为 `max_progress_silence_exceeded`，主会话不得继续等待 predecessor，也不得对该 predecessor 记录 `resume-same-agent`。
- [ ] workflow 明确：`stale-assessed` 后必须在同一 liveness handling turn 内完成 `terminated-unfinished -> replacement assigned -> replacement-started`。
- [ ] validator / gate 必须拒绝只有 `stale-assessed` 但缺少后续 `terminated-unfinished -> replacement-started` recovery chain 的 pass evidence。
- [ ] Phase 2 check / Branch Review Gate pass 必须要求后续 replacement chain 最终到达 `completed`；若 replacement `failed`，必须继续恢复或再次 replacement。
- [ ] workflow 明确：`wait_agent` 返回 terminal failure 时必须记录 `failed`，并进入 resume/replacement 链路；不能把 failed output 当作 pass evidence。

### 测试与安装验收

- [ ] 测试覆盖 task worktree `HEAD` / dirty status / diff stat / mtime 更新、source checkout `HEAD` / dirty status / diff stat / mtime 更新、recorded explicit-message / tool-activity / command-output / platform-progress / status-response event 更新时，checker 均输出 progress，不得发送 status request 或 stale。
- [ ] 测试覆盖无新 progress 且无 pending request 时，checker 输出 `status_request_required`。
- [ ] 测试覆盖无新 progress 且 pending request 未超过 `max_progress_silence` 时，checker 输出 `continue_waiting_no_repeat_ping`。
- [ ] 测试覆盖无新 progress、存在 pending request、超过 `max_progress_silence` 时，checker 输出 `stale_allowed`。
- [ ] 测试覆盖无新 progress、无 pending request、但 `checked_at >= max_progress_silence_deadline_at` 时，checker 仍输出 `status_request_required`；记录 `status-requested` 后立即重跑 checker，若仍无 progress，才输出 `stale_allowed`，且 deadline 不被 `status-requested` 延后。
- [ ] 测试覆盖存在 `stale-assessed` 但没有后续 `terminated-unfinished`、`replacement-started` 和 replacement `completed` 时，Phase 2 check / Branch Review Gate fail closed；replacement `failed` 只能触发继续恢复，不能作为 pass evidence。
- [ ] 测试覆盖 `stale-assessed` 后记录 `resume-same-agent` 时 validator fail closed；stale cutover 只能走 replacement。
- [ ] 测试覆盖 `terminated-unfinished` 缺少 `termination_reason`，或 `termination_reason=stale_cutover` 但缺少/错填 `termination_source_event_id` 时 validator fail closed。
- [ ] 测试覆盖 `replacement-started` 缺少 `predecessor_event_id` / `replacement_reason`，或 `replacement_reason` 与 predecessor 证据不匹配时 validator fail closed。
- [ ] 测试覆盖 checker 输出 `stale_allowed` 后、`stale-assessed` 写入前新增 recorded progress event、task worktree 机器变化或 source checkout 机器变化时，recorder 必须拒绝写入 `stale-assessed` 并要求重跑 checker。
- [ ] 测试覆盖 status request 发送失败并记录 `status-request-failed` 后，不设置 pending request，checker 不得输出 `stale_allowed`，主会话不得 terminate/replacement。
- [ ] 测试覆盖第一次 120s scan 无 progress 并记录 `status-requested` 后，必须立即再次运行 checker；checker 给出的下一次 `next_wait_ms` 不超过剩余静默时间，默认值下不得超过 60000ms。
- [ ] 测试覆盖未变化的既有 dirty diff / 旧 event 不会重复刷新 `progress_anchor_at`；迟到写入且 `observed_at` 早于当前 anchor 的 progress event 不会把 anchor 往回拨。
- [ ] 测试覆盖 recorder 写入 `status-requested`、`status-request-failed`、`stale-assessed`、`workspace-boundary-violation` 等非 progress digest event 后，下一轮 checker 不会因 `{TASK_DIR}/agent-assignment.json` mtime/diff/digest 变化而误判为 progress。
- [ ] dogfood overlay drift check 和 preset installer 验证覆盖新增脚本、schema、overlay 文案。

## Repo Docs SSOT 与知识门禁

- Durable docs 存在：`docs/requirements/README.md`、`docs/requirements/requirement-main.md`、`docs/requirements/guru-team-trellis-flow.md`。
- Durable spec 存在：`.trellis/spec/workflow/**`、`.trellis/spec/preset/**`。
- 本任务会改变长期 workflow、artifact、script、preset、overlay 和 gate 合同，必须同步 durable docs/spec；task artifact 不能成为唯一长期来源。
- Middle-platform Knowledge Gate：不适用。本任务修改 Trellis workflow/preset/companion scripts，不涉及 Guru Team middle-platform SDK/framework 使用。

## 官方 Trellis 扩展边界

已对照官方 Trellis 文档：

- https://docs.trytrellis.app/
- https://docs.trytrellis.app/advanced/custom-workflow
- https://docs.trytrellis.app/advanced/custom-spec-template-marketplace

本任务必须继续遵守：workflow 行为通过 marketplace workflow Markdown、platform entry、skill/prompt/agent overlay 和 project-local assets 表达；脚本只做确定性 recorder/checker/validator/executor；不修改 Trellis 上游源码、全局 npm 包或 `node_modules`；spec template marketplace 不承载 active task、runtime state 或单一业务仓库私有 PRD。
