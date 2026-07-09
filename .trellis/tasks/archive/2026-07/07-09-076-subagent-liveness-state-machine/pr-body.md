## 变更摘要

实现 issue #76 要求的 subagent liveness、progress/stale 判定与 replacement cutover 状态机，并同步 Guru Team workflow、preset、overlay、dogfood 安装副本、spec、README 与测试。

主要变更：

- 在 `agent-assignment.json` 1.1 schema 内新增 `status_events[]` liveness ledger 与结构化事件合同，覆盖 `spawned`、`progress-observed`、`status-requested`、`stale-assessed`、`terminated-unfinished`、`replacement-started`、`replacement-completed`、`completed`、`failed` 等状态事件。
- 新增短生命周期 companion script 入口：`record-subagent-liveness-event.sh` 负责结构化记录主会话已判断的事件，`check-subagent-liveness.sh` 负责按需单次采样并立即退出。
- 实现 deterministic checker decision：`workspace_boundary_violation_progress`、`progress_observed`、`status_request_required`、`continue_waiting_no_repeat_ping`、`stale_allowed`、`blocked_missing_evidence`。
- 将 stale replacement cause 固定为 `max_progress_silence_exceeded`；`status-requested` 不作为 progress，不延长 `max_progress_silence_deadline_at`。
- 结构化记录 unfinished termination：stale cutover 使用 `termination_reason=stale_cutover` 与 `termination_source_event_id=<stale-assessed.event_id>`；manual/platform unfinished 使用独立结构化字段区分。
- Branch Review Gate 明确禁止把 unfinished/failed/stale subagent partial output 当作 pass evidence，必须由 replacement completed 或合法 completed agent 产出 evidence。
- 将新增 public API、managed assets、overlay 文案、平台入口、workflow/preset README、durable specs 与 dogfood 副本同步到 `0.6.5-guru.3`。

## 影响范围

影响 Guru Team Trellis 本仓库的 workflow marketplace、preset installer、平台 overlay、dogfood 安装副本、companion scripts、schema/docs/spec、测试与 public extension metadata。

不包含以下行为：

- 不新增 `{TASK_DIR}/agent-progress.jsonl`。
- 不实现 subagent 周期 heartbeat。
- 不实现 daemon、sidecar、long-command wrapper 或后台 liveness 进程。
- 不读取平台 UI，不判断实现质量，不替代 AI review。
- 不把非机器可读 progress 直接作为 checker evidence；只有主会话 recorder 写入 `status_events[]` 后才进入 checker evidence。

无 CI/CD、容器、Kubernetes、数据库 migration、Makefile 或线上服务运行时变更。

## 验证结果

已通过：

- `python3 trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`：180 tests OK
- `python3 trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`：27 tests OK
- `python3 -m json.tool trellis/guru-team-extension.json .trellis/guru-team/extension.json trellis/index.json trellis/workflows/guru-team/schemas/intake-handoff.schema.json`
- `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh .trellis/guru-team/scripts/bash/*.sh`
- `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py .trellis/guru-team/scripts/python/guru_team_trellis.py`
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`
- `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-09-076-subagent-liveness-state-machine`
- `python3 ./.trellis/scripts/get_context.py --mode phase`
- `python3 ./.trellis/scripts/get_context.py --mode phase --step 3.5`
- `.trellis/guru-team/scripts/bash/check-agent-assignment.sh --json --task .trellis/tasks/07-09-076-subagent-liveness-state-machine`
- `.trellis/guru-team/scripts/bash/version.sh --json`：`0.6.5-guru.3` / target `0.6.5`
- public docs/scripts/tests/spec/manifests 内旧 `0.6.5-guru.2` residual scan：无残留
- `.new` / `.bak` scan：无残留
- `git diff --check`
- `git diff --check origin/main...HEAD`

开箱即用与 upgrade/update 门禁：

- 已验证 dogfood overlay drift 无漂移。
- 已验证 canonical/dogfood extension manifest 均为 `0.6.5-guru.3`，public API 包含 `agent-assignment.json`、`reviews/*.md`、`record-subagent-liveness-event`、`check-subagent-liveness`。
- 已验证 preset installer tests 覆盖 managed asset 安装、可执行位与新增 liveness assets。
- 已验证 README、workflow README、preset README、workflow/preset/spec/overlay 文案与 dogfood 副本一致。
- 未验证 merge 后 tag-pinned marketplace install：`v0.6.5-guru.3` tag 尚不存在，不能在本 PR 创建前执行 tag-pinned `trellis init` / `trellis workflow` 实测。merge 并创建 annotated tag 后需要执行该验证。

## Review Gate

Branch Review Gate 已通过，`reviewed_head` 与当前 HEAD 均为 `e0ee89401bef4739bf416ab4b29538ea407bc17a`。

审查生命周期：

- Round 1 final release review 覆盖 `origin/main...HEAD`，发现 P2：新增 liveness public API 未纳入 canonical/dogfood manifest。
- Round 2 closure review 在提交 `e0ee89401bef4739bf416ab4b29538ea407bc17a` 后确认 P2 关闭。
- Round 3 fresh final release review 覆盖当前 `origin/main...HEAD` 完整 diff，`findings_count: 0`。

Phase 2 check 已记录 issue #76 完整 scope 与 manifest/version 修复 delta 复核，`findings=[]`。

## Issue 关闭范围

Closes #76

`issue-scope-ledger.json` 已将 #76 列入 `close_issues`，并记录需求/设计承接、实现承接、Phase 2 check、review lifecycle 与验证证据。没有 related issue 或 follow-up issue 被本 PR 关闭。

## 安全说明

本 PR 不引入 token、secret、private key、签名 URL、`.env`、客户数据或敏感原始记录。

新增 checker 只读取本地 Git metadata、diff stat、mtime 与已结构化写入的 progress event digest；不读取平台 UI，不读取 private thinking，不输出 secrets，不迁移 patch，不终止进程。
