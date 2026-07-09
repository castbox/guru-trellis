# #76 技术设计：subagent liveness 状态机

## 设计来源

本文承接 issue #76 正文的 artifact schema、`status_events[]` 事件合同、recorder/checker 职责、CLI 输入输出、decision 状态机、时间语义、progress source 处理和 fail-closed gate。2026-07-08 17:57:40Z issue comment 明确废弃旧 heartbeat / task-local heartbeat / 旧 180s observation window / long-command wrapper 口径。

## 总体边界

### Markdown 控制面

以下文件定义 AI 判断流程、主会话动作、subagent prompt 和 gate 规则：

- `trellis/workflows/guru-team/workflow.md`
- `.trellis/workflow.md`
- `trellis/presets/guru-team/overlays/**`
- dogfood installed copies：`.agents/skills/**`、`.codex/prompts/**`、`.codex/skills/**`、`.codex/agents/**`、`.cursor/**`、`.claude/**`、`.trellis/agents/**`
- durable docs/spec：`docs/requirements/**`、`.trellis/spec/workflow/**`、`.trellis/spec/preset/**`

这些文件负责告诉主会话什么时候等待、什么时候发送 status request、什么时候由 checker 输出 `stale_allowed` 并记录 `stale-assessed`、什么时候必须 replacement，以及哪些 output 不能作为 pass evidence。

### Deterministic 脚本层

以下新增入口只做 recorder/checker/validator，不做 AI 判断：

```text
trellis/workflows/guru-team/scripts/bash/record-subagent-liveness-event.sh
trellis/workflows/guru-team/scripts/bash/check-subagent-liveness.sh
.trellis/guru-team/scripts/bash/record-subagent-liveness-event.sh
.trellis/guru-team/scripts/bash/check-subagent-liveness.sh
```

内部实现放在 `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`，安装副本同步到 `.trellis/guru-team/scripts/python/guru_team_trellis.py`。Bash 文件保持薄 wrapper。

脚本不得读取平台 UI、不得等待 subagent、不得发送 status request、不得判断实现质量、不得判断 review 是否通过、不得判断 issue 是否可关闭。

## Artifact Schema

单一 liveness artifact 是当前 task worktree 内：

```text
{TASK_DIR}/agent-assignment.json
```

在现有 assignment/review ledger 基础上扩展：

```json
{
  "schema_version": "1.1",
  "agents": [],
  "liveness": {
    "<agent_id>": {
      "progress_anchor_at": "2026-07-08T16:00:00Z",
      "last_scan_snapshot": {
        "captured_at": "2026-07-08T16:02:00Z",
        "task_head": "...",
        "task_content_status_digest": "...",
        "task_content_diff_stat_digest": "...",
        "task_content_max_mtime": "2026-07-08T16:01:30Z",
        "source_head": "...",
        "source_status_digest": "...",
        "source_diff_stat_digest": "...",
        "source_max_mtime": "2026-07-08T16:01:30Z",
        "progress_events_count": 0,
        "progress_events_digest": "...",
        "progress_events_newest_event_id": ""
      },
      "pending_status_request_at": null,
      "last_checked_at": "2026-07-08T16:02:00Z",
      "last_decision": "progress_observed"
    }
  },
  "status_events": []
}
```

字段规则：

- `progress_anchor_at`：最近一次被 checker 接受的公开 progress 时间锚点。初始化为 assignment/dispatch 时间，只作为静默计时基线，不是 progress evidence。刷新规则：task snapshot progress 使用本轮 task snapshot `captured_at`；recorded progress event 使用新增 progress events 中最新一条 `observed_at`；source checkout progress 使用本轮 source snapshot `captured_at`。该字段必须单调不回退。
- `last_scan_snapshot`：上一轮 checker 保存的机器可比较快照。后续 checker 只把相对该快照的新变化计为 progress。必须排除 `{TASK_DIR}/agent-assignment.json` 自身的 bookkeeping 写入。
- `progress_events_count` / `progress_events_digest` / `progress_events_newest_event_id`：只统计 progress events，不统计 terminal、workspace-boundary audit 或 control/bookkeeping events。
- `pending_status_request_at`：成功发送 status request 且之后尚未观测到 progress 的时间。无 pending request 时为 `null`。
- `last_checked_at`：checker 最近一次执行时间。
- `last_decision`：checker 最近一次输出的 decision。
- `status_events[]`：审计事件流。非机器可读 progress 必须先写入这里，checker 才能把它计为 progress。

`assigned` 事件创建 `agents[]` 时字段映射固定：

- `logical_role = --logical-role`
- `agent_id = --agent-id`
- `platform_nickname = --platform-nickname`
- `assigned_at = --observed-at`
- `assigned_head = current task worktree HEAD`
- `reason = --evidence`

除 required recorder/checker 外，workflow 不要求 AI 手工编辑 `liveness` 字段。

## 当前实现盘点与替代关系

当前仓库已经存在一套与本任务高度相关的 sub-agent assignment / status / review gate 能力，不能并排新增同目的实现：

- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py` 现有 `AGENT_ASSIGNMENT_SCHEMA_VERSION = "1.0"`，`agent-assignment.json` 已包含 `agents[]`、`review_rounds[]`、`reuse_decisions[]`、`status_events[]`。
- `record-agent-assignment.sh` 现在同时承担三类职责：写 `agents[]` assignment、写 `review_rounds[]` / `reuse_decisions[]` review 复用证据、通过 `--status-event` 写粗粒度 sub-agent 状态。
- 现有 `status_events[]` 枚举是 `wait-timeout`、`progress-observed`、`stale-assessed`、`continue-waiting`、`resume-same-agent`、`replacement-started`、`terminated-unfinished`、`completed`、`failed`；现有 `decision` 枚举是 `continue-waiting`、`resume-same-agent`、`start-replacement`、`terminate-unfinished`、`mark-completed`、`mark-failed`。这些只是粗粒度人工记录，不能表达 issue #76 要求的 `status-requested`、`status-response-observed`、`workspace-boundary-violation`、`termination_reason`、`termination_source_event_id`、`replacement_reason`、`progress_sources[]`、`last_scan_snapshot` 和 stale 前置审计条件。
- `check-agent-assignment.sh` / `review-branch.sh --agent-assignment` 已经会读取同一个 `agent-assignment.json`，并通过 `status_event_completion_errors()` 拦截未闭环 `terminated-unfinished` recovery chain。#76 必须扩展这条 validator/gate 路径，而不是新增第二个 gate artifact 或第二套 Branch Review Gate。
- `check-workspace-boundary.sh` 已经提供 expected workspace、actual repo root、source checkout status、task worktree status 和 suspicious source artifacts。#76 checker 应复用/抽取这类路径与 workspace boundary helper，但 checker 自身只做单次 snapshot 比较；不得另起一个 workspace guard 语义。
- durable docs 当前仍写有 “stale 默认至少 5 分钟无可观察进展” 和旧 `record-agent-assignment.sh --status-event` 示例。实现必须用 `progress_scan_interval=120s`、`max_progress_silence=180s`、required recorder/checker 和 fail-closed state machine 替换这些文字。

替代策略：

- `agent-assignment.json` 继续是唯一 task-local assignment/status/liveness/review 证据 artifact；不新增 `{TASK_DIR}/agent-progress.jsonl`，也不新增平行的 liveness ledger。
- Schema 从当前 `1.0` additive 升级到 `1.1`：保留 `agents[]`、`review_rounds[]`、`reuse_decisions[]`，新增 `liveness[agent_id]`，并把 active `status_events[]` 改为 issue #76 的精确事件合同。
- `record-subagent-liveness-event.sh` 是 active liveness/status event 的 canonical writer，负责 `assigned`、progress、workspace-boundary、status request/response、stale、resume/replacement/termination、terminal events，并在 `assigned` 时同步创建 `agents[]` 和 liveness baseline。
- `record-agent-assignment.sh` 保留为 non-liveness recorder：继续写 review round / reuse decision。旧 assignment 兼容入口必须改为 thin shim 调用同一 `assigned` core，避免 `agents[]` 和 `status_events[] assigned` 不一致；`--status-event` 旧入口必须 fail closed 并提示改用 `record-subagent-liveness-event.sh`。不得维护两套 event enum、两套 validator 或两套 stale cause 解释。
- 旧 `wait-timeout`、`continue-waiting`、旧 `progress-observed` 主动写入语义被 checker decision / explicit progress events 取代；它们只能作为 legacy archived artifact 可读字段，不得作为新 active liveness progress source 或 pass evidence。
- `check-agent-assignment.sh` 和 `review-branch.sh` 必须调用同一新 liveness validation helper 来校验 `status_events[]`、`liveness`、replacement/resume/termination chain、legacy status event 风险和 Phase 2 / Branch Review Gate pass evidence；不能只让新 checker 校验，而让旧 gate 继续按旧字段放行。
- Review-agent replacement 仍需保留既有 `review_rounds[]` / `reuse_decisions[]` 语义：当 review finding owner 被替代时，新的 `replacement-started` status event 与既有 `reuse_decisions[] decision=replace from_round/to_round` 必须互相一致。#76 不替代 review round 证据，只替代 sub-agent liveness/status 事件合同。

## `status_events[]` 事件合同

### 通用字段

每条事件必须包含：

```json
{
  "event_id": "...",
  "event": "explicit-message-observed",
  "agent_id": "...",
  "logical_role": "实现代理",
  "platform_nickname": "Implement Agent",
  "observed_at": "2026-07-08T16:02:00Z",
  "recorded_at": "2026-07-08T16:02:03Z",
  "head": "...",
  "source": "main-session",
  "evidence": "...",
  "predecessor_agent_id": "",
  "predecessor_event_id": "",
  "termination_reason": "",
  "termination_source_event_id": "",
  "replacement_reason": "",
  "handoff_summary": ""
}
```

字段语义：

- `event_id`：task-local 唯一事件 id。
- `event`：属于事件枚举。
- `agent_id`：目标 subagent id。
- `logical_role`：如 `实现代理` / `阶段二检查代理`。
- `platform_nickname`：平台显示名；未知时空字符串。
- `observed_at`：事件被观察到的时间。
- `recorded_at`：recorder 写入 artifact 的时间。
- `head`：记录事件时 task worktree 的 `HEAD`。
- `source`：`main-session` / `recorder` / `checker`。
- `evidence`：非空证据摘要，不得写泛化占位。
- `predecessor_agent_id`：仅 `replacement-started` 使用非空。
- `predecessor_event_id`：`resume-same-agent` 和 `replacement-started` 必填。
- `termination_reason`：仅 `terminated-unfinished` 使用，至少支持 `stale_cutover`、`manual_or_platform_terminated_unfinished`。
- `termination_source_event_id`：仅 `terminated-unfinished termination_reason=stale_cutover` 使用，必须引用同一 agent 的 `stale-assessed`。
- `replacement_reason`：仅 `replacement-started` 使用，至少支持 `max_progress_silence_exceeded`、`terminal_failed_incomplete`、`manual_or_platform_terminated_unfinished`。其中 `max_progress_silence_exceeded` 表示最大无 progress 时间窗超时；status request 未产生 progress 是该判定的确认条件，不是独立 replacement cause。
- `handoff_summary`：仅 `resume-same-agent`、`replacement-started`、`terminated-unfinished` 使用。`replacement-started` / `terminated-unfinished` 必须覆盖 predecessor output、当前 diff、task artifacts、剩余工作和 gate blockers；`resume-same-agent` 必须说明继续执行范围、已知输出、剩余工作和 gate blockers。

### 事件枚举

Progress events，会刷新 `progress_anchor_at`，前提是相对上一轮 scan 为新增：

- `explicit-message-observed`
- `tool-activity-observed`
- `command-output-observed`
- `platform-progress-observed`
- `status-response-observed`

Terminal events，清除 `pending_status_request_at` 并停止该 agent 的 liveness 循环，但不是 pass 结论：

- `completed`
- `failed`

Workspace boundary audit event：

- `workspace-boundary-violation`

Control/bookkeeping events，不刷新 `progress_anchor_at`：

- `assigned`
- `status-requested`
- `status-request-failed`
- `stale-assessed`
- `resume-same-agent`
- `replacement-started`
- `terminated-unfinished`

### 事件专属校验

- `replacement-started`：`agent_id` 表示新 replacement agent，必须已有 `assigned` 事件；`predecessor_agent_id` 必填；`predecessor_event_id` 必须引用同一 task 中属于 `predecessor_agent_id` 的 `failed`、`stale-assessed` 或 `terminated-unfinished`。`replacement_reason` 必须与前置事件匹配：引用 `stale-assessed` 时只能是 `max_progress_silence_exceeded`，含义是最大无 progress 时间窗已超时；引用 `failed` 时只能是 `terminal_failed_incomplete`；引用 `terminated-unfinished termination_reason=manual_or_platform_terminated_unfinished` 时只能是 `manual_or_platform_terminated_unfinished`。stale cutover 的 `replacement-started.predecessor_event_id` 必须引用 `stale-assessed`，同时 validator 必须确认同一 predecessor 已存在后续 `terminated-unfinished termination_reason=stale_cutover termination_source_event_id=<same stale-assessed>`。`handoff_summary` 必填，必须说明 predecessor output、当前 diff、task artifacts、剩余工作和继任 gate blockers。
- `resume-same-agent`：`agent_id` 表示被继续使用的同一 agent；`predecessor_event_id` 必须引用同一 agent 的 `failed` 或 `terminated-unfinished termination_reason=manual_or_platform_terminated_unfinished`；不得引用 `stale-assessed` 或 `terminated-unfinished termination_reason=stale_cutover`，因为 stale cutover 只能进入 replacement。`handoff_summary` 必填，必须说明继续执行范围、已知输出、剩余工作和 gate blockers。
- `terminated-unfinished`：`agent_id` 表示被终止的 unfinished agent；`termination_reason` 必填。`stale_cutover` 必须设置 `termination_source_event_id` 并引用同一 agent 的 `stale-assessed`；`manual_or_platform_terminated_unfinished` 必须让 `termination_source_event_id` 为空并在 evidence 中说明独立终止原因。`handoff_summary` 必填，必须包含 predecessor output、当前 diff、剩余工作和 gate blockers 摘要。
- `stale-assessed`：recorder 必须校验 `liveness[agent_id].last_decision == stale_allowed`，并重新验证当前 task/source 机器 snapshot 与 `last_scan_snapshot` 仍一致，progress events count/digest/newest event id 也仍一致。若有新 progress，fail closed 并要求重跑 checker。
- `completed` / `failed`：必须清除该 agent 的 `pending_status_request_at`。

## Recorder CLI 合同

新增 canonical Bash 入口：

```bash
record-subagent-liveness-event.sh \
  --task <TASK_DIR> \
  --agent-id <agent_id> \
  --event <event> \
  --observed-at <ISO8601_UTC> \
  --evidence <non_empty_text> \
  --source-repo <SOURCE_CHECKOUT_PATH> \
  [--logical-role <role>] \
  [--platform-nickname <name>] \
  [--predecessor-agent-id <agent_id>] \
  [--predecessor-event-id <event_id>] \
  [--termination-reason <reason>] \
  [--termination-source-event-id <event_id>] \
  [--replacement-reason <reason>] \
  [--handoff-summary <text>]
```

参数规则：

- `--task` 必须指向当前 task worktree 内的 task 目录。
- `--agent-id` 必须匹配 `agents[]`；仅 `assigned` 事件创建新 agent。
- `--logical-role` 在 `assigned` 必填，其它事件从 `agents[]` 推导，无法推导则失败。
- `--platform-nickname` 在 `assigned` 必须提供；平台没有昵称时传空字符串。
- `--event` 必须属于事件枚举。
- `--predecessor-agent-id` 仅 `replacement-started` 必填，其它事件必须省略。
- `--predecessor-event-id` 仅 `resume-same-agent` 和 `replacement-started` 必填，其它事件必须省略。
- `--termination-reason` 仅 `terminated-unfinished` 必填，其它事件必须省略。
- `--termination-source-event-id` 仅 `terminated-unfinished --termination-reason stale_cutover` 必填，其它情况必须省略。
- `--replacement-reason` 仅 `replacement-started` 必填，其它事件必须省略。
- `--handoff-summary` 在 `resume-same-agent`、`replacement-started`、`terminated-unfinished` 必填。
- `--observed-at` 必须是 UTC ISO-8601 时间。
- `--evidence` 必须非空，不能是 `N/A`、`unknown`、`placeholder` 等占位。
- `--source-repo` 必须指向 source checkout，用于初始化和校验 baseline snapshot。

成功 stdout JSON：

```json
{
  "recorded": true,
  "event_id": "...",
  "event": "status-requested",
  "agent_id": "...",
  "artifact": "{TASK_DIR}/agent-assignment.json",
  "head": "...",
  "updated_liveness": true
}
```

失败必须非零退出并保持 artifact 原子性，不留下半截 JSON。`status-requested` 只有在主会话已经成功发送 status request 后才能记录；recorder 不负责发送 status request。

## Checker CLI 合同

新增 canonical Bash 入口：

```bash
check-subagent-liveness.sh \
  --task <TASK_DIR> \
  --agent-id <agent_id> \
  --progress-scan-interval 120 \
  --max-progress-silence 180 \
  --source-repo <SOURCE_CHECKOUT_PATH>
```

成功 stdout JSON：

```json
{
  "decision": "progress_observed",
  "agent_id": "...",
  "checked_at": "2026-07-08T16:02:00Z",
  "progress_anchor_at": "2026-07-08T16:01:30Z",
  "pending_status_request_at": null,
  "max_progress_silence_deadline_at": "2026-07-08T16:04:30Z",
  "next_wait_ms": 60000,
  "progress_sources": [],
  "artifact": "{TASK_DIR}/agent-assignment.json",
  "reason": "..."
}
```

`progress_sources[]` 是机器可读数组；元素必须包含 `source`、`observed_at`、`evidence`。`source` 枚举固定为：

- `task_head`
- `task_status`
- `task_diff_stat`
- `task_mtime`
- `source_head`
- `source_status`
- `source_diff_stat`
- `source_mtime`
- `status_event`

当 `source=status_event` 时，还必须包含 `event_id` 和 `event`。无新增 progress 时返回空数组。

## Decision 状态机

Decision 枚举固定：

- `workspace_boundary_violation_progress`：source checkout snapshot 相对上一轮 scan 出现新 `HEAD` / dirty status / diff stat / mtime 变化。优先级高于普通 `progress_observed`，刷新 anchor，清除 pending request，要求 workspace boundary 纠偏。
- `progress_observed`：task worktree content snapshot 或已记录 progress event 相对上一轮 scan 出现新变化。刷新 anchor，清除 pending request，主会话继续等待。liveness artifact 自身变化不属于 task content progress。
- `status_request_required`：无新 progress 且没有 pending status request。主会话必须发送一次 status request。即使 deadline 已过，没有 pending status request 时也必须先输出该 decision。
- `continue_waiting_no_repeat_ping`：无新 progress，已有 pending status request，且 `checked_at < max_progress_silence_deadline_at`。主会话继续等待，不重复发送 status request。
- `stale_allowed`：无新 progress，已有 pending status request 且未产生 progress 响应，且 `checked_at >= max_progress_silence_deadline_at`。主会话才能记录 `stale-assessed`。
- `blocked_missing_evidence`：artifact 缺失、schema 不合法、snapshot 无法采集、source repo 未提供、agent 未登记、时间字段无效或其它会让 stale 判断不可审计的问题。主会话必须补齐 evidence，不能 stale、terminate、replacement 或进入后续 gate。

Decision 优先级：

1. artifact/schema/path/snapshot/time 字段不可审计 -> `blocked_missing_evidence`
2. source checkout snapshot 有新增变化 -> `workspace_boundary_violation_progress`
3. task worktree snapshot 或新增 recorded progress event 有新增变化 -> `progress_observed`
4. 无新 progress 且无 pending request -> `status_request_required`
5. 无新 progress、已有 pending request、且未到 deadline -> `continue_waiting_no_repeat_ping`
6. 无新 progress、已有 pending request、且已到/超过 deadline -> `stale_allowed`

## 时间语义

- `progress_scan_interval=120s` 是常规扫描间隔，不是 stale 判定阈值。
- `progress_scan_interval` 到期后，主会话运行 checker；checker decision 决定下一步操作。该 interval 本身不授权 status request 或 stale。
- `max_progress_silence=180s` 是从 `progress_anchor_at` 起算的 stale eligibility threshold，不是调度器、后台计时器或自动终止定时器。
- `max_progress_silence_deadline_at = progress_anchor_at + max_progress_silence`。
- `max_progress_silence` 必须大于 `progress_scan_interval`。
- `max_progress_silence` 只在 checker 调用时被评估。checker 不得在 deadline 前输出 `stale_allowed`；在 deadline 或之后且仍满足无新 progress、存在 pending request、该 request 未产生 progress 响应时必须输出 `stale_allowed`。
- 主会话不得用固定 120s sleep 越过 deadline。checker 必须令 `next_wait_ms <= min(progress_scan_interval, max_progress_silence_deadline_at - checked_at)`。如果剩余时间小于等于 0，`next_wait_ms` 必须为 0，主会话必须立即再次调用 checker 或执行当前 decision 要求的立即动作。
- `status_request_required`、`stale_allowed`、`blocked_missing_evidence` 的 `next_wait_ms` 必须为 0。
- `continue_waiting_no_repeat_ping` 的 `next_wait_ms` 必须不超过剩余 deadline；剩余时间为 0 时下一次 checker 若仍无 progress 且 pending request 存在，必须输出 `stale_allowed`。
- `progress_observed` / `workspace_boundary_violation_progress` 用刷新后的 anchor 重新计算 deadline 和 `next_wait_ms`。
- `status-requested` 本身不算 progress，不能刷新 anchor。
- 只有新增 progress event、task worktree content snapshot 新变化、source checkout 新 snapshot 变化或 recorded status response，才能刷新 anchor。liveness artifact 自身变化和 control/bookkeeping event 不刷新 anchor，也不得通过 mtime/digest 间接制造 progress。

## Progress Source 处理

### 机器可读 progress

checker 每次按需调用时采集一次并立即退出：

- task worktree `HEAD`
- task worktree `git status --porcelain`，排除 `{TASK_DIR}/agent-assignment.json`
- task worktree `git diff --stat`，排除 `{TASK_DIR}/agent-assignment.json`
- task worktree 非 `.git` 文件 max mtime，排除 `{TASK_DIR}/agent-assignment.json`
- source checkout `HEAD`
- source checkout `git status --porcelain`
- source checkout `git diff --stat`
- source checkout 非 `.git` 文件 max mtime
- `status_events[]` 中 progress 事件的 length / digest / newest `event_id`

source checkout 使用保守规则：本次 snapshot 相对 assignment baseline 或上一轮 scan 出现新的 `HEAD`、dirty status、diff stat 或非 `.git` mtime 变化，就视为 `workspace_boundary_violation_progress`。checker 不做“是否与当前 task 语义相关”的 AI 判断。

### 非机器可读 progress

subagent 显式消息、tool calls、平台 progress event、UI 中命令输出只有一个合法入口：主会话调用 recorder 写入 `status_events[]`。

没有写入 `status_events[]` 的 UI 观察不能作为 checker evidence，不能刷新 anchor，也不能用于阻止或触发 stale gate。

## 主会话状态机流程

1. 派发 subagent 后，调用 recorder 写入 `assigned` 并初始化 `liveness[agent_id]`。
2. 使用 `next_wait_ms` 执行 `wait_agent(..., timeout=<next_wait_ms>)`；初始 120000ms，后续使用 checker 输出。
3. subagent `completed`：调用 recorder 写入 `completed`，然后进入正常完成审查；completion 不跳过 Phase 2 check 或 Branch Review Gate。
4. subagent `failed`：调用 recorder 写入 `failed`，停止该 agent liveness 循环，进入 same-agent resume 或 replacement；`failed` 不能作为 pass evidence。
5. timeout 后，先把本轮看到的非机器 progress 通过 recorder 写入 `status_events[]`。
6. 调用 checker。
7. `workspace_boundary_violation_progress`：调用 recorder 写入 `workspace-boundary-violation` 审计事件，保留 source snapshot evidence，要求纠偏到 task worktree，继续等待同一 agent。
8. `progress_observed`：继续等待同一 agent。
9. `status_request_required`：发送一次 status request；成功后 recorder 写入 `status-requested`，立即再次调用 checker，使用新 `next_wait_ms` 进入下一轮。发送失败时写入 `status-request-failed`，先处理平台/工具错误，不进入 stale、terminate 或 replacement。
10. `continue_waiting_no_repeat_ping`：使用 checker 输出的 `next_wait_ms` 继续等待，不重复发送 status request。
11. `stale_allowed`：写入 `stale-assessed` 前，如果主会话又观察到任何新的公开 progress，必须先 recorder 记录 progress 并重跑 checker。`stale-assessed` 成功后不得继续等待 predecessor，不得记录 `resume-same-agent`，必须进入 stale replacement cutover。
12. stale replacement cutover：记录 `terminated-unfinished termination_reason=stale_cutover termination_source_event_id=<stale-assessed.event_id>`；派发并记录 replacement `assigned`；记录 `replacement-started predecessor_agent_id=<stale predecessor> predecessor_event_id=<stale-assessed.event_id> replacement_reason=max_progress_silence_exceeded`。
13. `blocked_missing_evidence`：补齐 artifact/snapshot evidence，不能 stale、terminate、replacement 或进入后续 gate。
14. 人工或平台原因导致 unfinished termination：记录 `terminated-unfinished termination_reason=manual_or_platform_terminated_unfinished`、predecessor output、当前 diff、剩余工作和 gate blockers，并要求 same-agent resume 或 replacement completion。

## Gate Fail-Closed 规则

- 没有 checker `stale_allowed`，不得记录 `stale-assessed`。
- 记录 `terminated-unfinished termination_reason=stale_cutover` 时，必须设置 `termination_source_event_id` 并引用同一 predecessor 的 `stale-assessed`。
- 人工/平台 unfinished termination 必须记录 `termination_reason=manual_or_platform_terminated_unfinished`，`termination_source_event_id` 必须为空，并在 evidence 与 handoff 中说明独立原因。
- `stale-assessed` 后不得记录 `resume-same-agent`；必须记录 `terminated-unfinished termination_reason=stale_cutover termination_source_event_id=<stale-assessed.event_id>`，随后记录 `replacement-started replacement_reason=max_progress_silence_exceeded`。
- `resume-same-agent.predecessor_event_id` 只能引用同一 agent 的 `failed` 或 `terminated-unfinished termination_reason=manual_or_platform_terminated_unfinished`。
- `replacement-started.predecessor_event_id` 必须引用同一 predecessor 的 `failed`、`stale-assessed` 或 `terminated-unfinished`；新 replacement agent 必须先 assigned；没有 predecessor terminal/stale 证据不得启动 replacement。
- stale cutover 的 `replacement-started.predecessor_event_id` 必须引用 `stale-assessed`，同时 validator 必须确认同一 predecessor 已存在后续 `terminated-unfinished termination_reason=stale_cutover termination_source_event_id=<same stale-assessed.event_id>`。
- 只有 `completed` 事件后的输出，才能进入 Phase 2 check / Branch Review Gate 的正常审查；`completed` 本身不是 pass evidence。
- `stale-assessed` 后必须有 replacement chain，且 replacement agent 产生 `completed` 后，Phase 2 check / Branch Review Gate 才能使用最终输出。
- `failed` 或 `terminated-unfinished termination_reason=manual_or_platform_terminated_unfinished` 后，必须有 `resume-same-agent` 或 `replacement-started`，并且后续 agent 产生 `completed`，Phase 2 check / Branch Review Gate 才能使用最终输出。
- `blocked_missing_evidence` 出现时，不得进入 stale、replacement、Phase 2 check 或 Branch Review Gate。

## 代码集成设计

### Python helper

在 `guru_team_trellis.py` 中新增子命令：

- `record-subagent-liveness-event`
- `check-subagent-liveness`

实现必须使用单一共享 helper/core 承载以下能力，供新 recorder/checker、`check-agent-assignment.sh` 和 `review-branch.sh` 复用：

- path/boundary：复用现有 task-local path 与 workspace boundary 校验。
- artifact IO：复用原子 JSON 写入；老版本 artifact 缺少 `liveness` / `status_events` 时 additive normalize。
- snapshot：采集 task/source checkout `HEAD`、status digest、diff stat digest、mtime。
- progress event digest：只对 progress events 计数/摘要/newest event id。
- liveness validation：事件专属字段、前置证据、stale-assessed snapshot freshness、replacement/resume chain。
- decision engine：按固定优先级输出唯一 decision 和 `next_wait_ms`。

### Bash wrappers

新增薄 wrapper，遵循 `.trellis/spec/workflow/companion-scripts.md`：

```bash
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SCRIPT_DIR/../python/guru_team_trellis.py" <subcommand> "$@"
```

### Preset managed assets

在 `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py` 的 `MANAGED_ASSET_PATHS` 增加：

- `scripts/bash/record-subagent-liveness-event.sh`
- `scripts/bash/check-subagent-liveness.sh`

脚本必须保留 executable bit。README installed-file list 也必须更新。

### Canonical / dogfood 同步

Canonical 变更后运行：

```bash
trellis/presets/guru-team/scripts/bash/apply.sh --repo .
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
```

如生成 `.new` / `.bak`，必须逐个处理并记录。

## 需要更新的文件族

### Canonical workflow / scripts / docs

- `trellis/workflows/guru-team/workflow.md`
- `trellis/workflows/guru-team/README.md`
- `trellis/workflows/guru-team/scripts/bash/record-subagent-liveness-event.sh`
- `trellis/workflows/guru-team/scripts/bash/check-subagent-liveness.sh`
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
- `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
- `trellis/workflows/guru-team/config-template.yml` only if timing defaults become configurable; otherwise keep fixed CLI defaults and document no config key.

### Preset / overlay / installer

- `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`
- `trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`
- `trellis/presets/guru-team/README.md`
- `trellis/presets/guru-team/overlays/.agents/skills/trellis-continue/SKILL.md`
- `trellis/presets/guru-team/overlays/.codex/prompts/trellis-continue.md`
- `trellis/presets/guru-team/overlays/.codex/skills/trellis-continue/SKILL.md`
- `trellis/presets/guru-team/overlays/.cursor/commands/trellis-continue.md`
- `trellis/presets/guru-team/overlays/.claude/commands/trellis/continue.md`
- subagent prompts: `.trellis/agents/implement.md`, `.trellis/agents/check.md`, `.codex/agents/trellis-implement.toml`, `.codex/agents/trellis-check.toml`, Branch Review Gate / review subagent prompt sections embedded in `trellis-continue` overlays, and Cursor/Claude equivalents. Current repo review agents are driven through independent `trellis-check` / Branch Review Gate flow rather than a separate canonical review-agent file.

### Dogfood installed copies

- `.trellis/workflow.md`
- `.trellis/guru-team/scripts/bash/**`
- `.trellis/guru-team/scripts/python/guru_team_trellis.py`
- `.agents/skills/trellis-continue/SKILL.md`
- `.codex/prompts/trellis-continue.md`
- `.codex/skills/trellis-continue/SKILL.md`
- `.codex/agents/trellis-implement.toml`
- `.codex/agents/trellis-check.toml`
- `.trellis/agents/implement.md`
- `.trellis/agents/check.md`

### Durable docs/spec

- `.trellis/spec/workflow/companion-scripts.md`
- `.trellis/spec/workflow/data-contracts.md`
- `.trellis/spec/workflow/workflow-contract.md`
- `.trellis/spec/workflow/quality-guidelines.md`
- `.trellis/spec/preset/installer.md`
- `.trellis/spec/preset/overlay-guidelines.md`
- `docs/requirements/README.md`
- `docs/requirements/requirement-main.md`
- `docs/requirements/guru-team-trellis-flow.md`

## Backward Compatibility

- Existing `agent-assignment.json` artifacts without `liveness` must normalize to `liveness={}` and existing `status_events[]` must remain readable.
- Existing review-round and reuse-decision behavior must remain compatible. New liveness fields are additive.
- Existing `record-agent-assignment.sh` remains only as the compatibility/non-liveness entry for review-round and reuse-decision evidence. Its assignment compatibility path must delegate to the exact `assigned` core used by `record-subagent-liveness-event.sh`. Its old `--status-event` path must fail closed with a clear migration message that points callers to `record-subagent-liveness-event.sh`. Existing legacy `status_events[]` entries remain readable for archived artifacts, but new active gates must not treat legacy coarse events as issue #76 progress/stale/pass evidence.
- Existing installed repos receive new scripts through preset managed assets; existing `.trellis/guru-team/config.yml` must remain preserved.

## 安全与副作用

- 脚本输出和 artifacts 不得泄露 tokens、secrets、private keys、signed URLs、`.env`、数据库 URL 或客户数据。
- Snapshot evidence 只记录 Git/objective metadata 和摘要，不打印敏感 file contents。
- Recorder/checker 只写 task-local `agent-assignment.json`；不清理 source checkout、不迁移 patch、不终止 OS 进程、不发 status request。
