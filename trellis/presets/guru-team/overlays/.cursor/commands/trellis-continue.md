<!-- guru-team-overlay: v1 -->
# Guru Team Continue Current Task

Resume work through `.trellis/workflow.md`; do not introduce extra user-facing stages.

```bash
python3 ./.trellis/scripts/get_context.py
python3 ./.trellis/scripts/get_context.py --mode phase
```

Route by task status:

- planning: apply the business-project Chinese documentation default from `.trellis/workflow.md` across `.trellis/spec/**`, `.trellis/tasks/**`, `docs/**`, `00-bootstrap-guidelines` docs SSOT, and human-readable artifact fields; run Docs SSOT discovery and the Middle-platform Knowledge Gate when relevant, use `trellis-brainstorm` when intake evidence is ambiguous, update GitHub issue comment/body or proposed issue body as appropriate, then ask for review, record/check `planning-approval.json`, and only then run `task.py start`.
- in_progress: confirm knowledge-gate and docs responsibilities from artifacts, implement, record sub-agent assignment/status events when dispatching implement/check agents, run full `trellis-check`, record/check `phase2-check.json` with the current pre-commit `dirty_paths`, reconcile specs/docs, then commit.
- after commit: obtain an independent Agent review over the full diff, record review role/reuse/status decisions in `agent-assignment.json` when sub-agents are used, write task-local `{TASK_DIR}/review.md`, then run Branch Review Gate before `/trellis-finish-work`, including Docs SSOT reconciliation evidence. Do not pass the gate from main-session self-review.

If a user adds requirements, references another issue, or discovers new scope during the task, pause and follow `.trellis/workflow.md` Scope Change Gate before continuing implementation: recommend whether the change belongs in current `close_issues`, `related_issues`, or `followup_issues` / new issue, get user confirmation when classification is not explicit, update planning artifacts and `issue-scope-ledger.json`, and leave GitHub-visible issue evidence.

```bash
.trellis/guru-team/scripts/bash/review-branch.sh --json --pass \
  --review-source independent-agent \
  --reviewer "trellis-check-agent" \
  --review-report ".trellis/tasks/<task>/review.md" \
  --agent-assignment ".trellis/tasks/<task>/agent-assignment.json" \
  --summary "中文审查结论" \
  --evidence "已按 intake base 到 HEAD 的完整 diff 覆盖文档、代码、测试、Trellis artifacts、CI/CD、容器、K8s/Kustomize、数据库 migration、Makefile，并判断本次变更的部署影响及是否需要同步修改部署资产"
```

Use `--finding` or `--findings-file` when the review has any current-scope issue. Any finding priority P0/P1/P2/P3 blocks Branch Review Gate and finish-work. The findings recorder path still requires `--review-source independent-agent` and `--review-report` pointing at task-local `review.md`; failed artifacts also record a prior independent review, not reviewer identity alone. Use `--observation` for non-blocking notes and `--followup-candidate` for out-of-scope future work; do not downgrade an actual defect to either category to pass the gate. If a review agent finds findings, fixes must be returned to that same technical `agent_id` as `问题闭环审查代理` until it records `findings_count: 0` for its finding; only then dispatch a fresh new `最终放行审查代理` for the full current HEAD diff. A passing gate must include zero findings, the fresh final review, `--review-source independent-agent`, a non-main-session `--reviewer`, a Chinese `--summary`, at least one concrete `--evidence` line, `--review-report` pointing at task-local `review.md`, and task-local `--agent-assignment` so the recorder can validate closure-before-final and final reviewer freshness. `--reviewer` is identity metadata only. `review-branch.sh` records and validates the prior independent review; it is not the reviewer. Independent review sub-agents review docs, code, tests, artifacts, and diffs as AI reviewers and must not run Guru Team recorder/validator extension scripts such as `review-branch.sh`, `check-review-gate.sh`, `record-agent-assignment.sh`, or `record-*`; the main session runs those scripts only after the review result exists. If independent Agent review is unavailable, stop with Branch Review Gate pending instead of writing a passing gate.

Sub-agent identity rule: `logical_role` is the Chinese Trellis role (`实现代理`, `阶段二检查代理`, `问题发现审查代理`, `问题闭环审查代理`, `最终放行审查代理`); `agent_id` is the technical identity; `platform_nickname` is display-only and never used for gate judgment. Any review agent that found findings, including a previous final reviewer that found a new issue, may be reused only as `问题闭环审查代理`; it must not become final. The final passing review must be the last round, use a fresh new `最终放行审查代理` with `findings_count: 0`, `reviewed_head` equal to current HEAD, and `reuse_decision: new-agent`. Use `record-agent-assignment.sh` / `check-agent-assignment.sh` only as recorder/validator tools, not to decide agent reuse.

Sub-agent wait/termination rule: `wait_agent`, `trellis channel wait`, or equivalent timeout is only a wait-window result, not failure or acceptable partial-completion evidence. Do not stop a still-progressing sub-agent because total runtime is long; stale means no observable progress for a recent window, default at least 5 minutes. Record wait timeout, progress, stale assessment, interruption, unfinished termination, resume/replacement, completion, or explicit failure in `agent-assignment.json.status_events[]`. If an unfinished agent is interrupted or terminated, resume the same `agent_id` or start a replacement with predecessor output, current diff, task artifacts, remaining work, and gate blockers; Branch Review Gate pass is blocked until that recovery chain has a later `completed` or `failed` event.

`task.py start` is only a status transition; `planning-approval.json` is the start gate evidence. Validation commands are only evidence inside `phase2-check.json`; they do not replace complete `trellis-check` coverage. `review-branch.sh` validates that Phase 2 check evidence exists before recording Branch Review Gate and performs the post-commit audit: committed non-metadata task work after the Phase 2 recorded HEAD must be covered by `phase2-check.json.dirty_paths`, and the current working tree must not contain non-metadata dirty paths. Task-local Branch Review Gate / publish readiness metadata (`issue-scope-ledger.json`, `pr-body.md`, `pr-readiness.json`, `agent-assignment.json`, `review.md`, `review-gate.json`) may change after Phase 2 and is revalidated by gate or publish validators. Do not re-record Phase 2 after the task work commit just to make HEAD match; return to Phase 2 only when new non-metadata changes appear or evidence is invalid.

Do not stage/commit `review.md`, `review-gate.json`, handoff, journal, archive, or other Trellis metadata in `/trellis-continue`. Do not push the branch, create a PR, call `publish-pr`, or invoke `finish-work` from `/trellis-continue`. Stop after Branch Review Gate and wait for the user/session to explicitly invoke `/trellis-finish-work`; that finish entrypoint commits remaining metadata-only changes and publishes after archive and journal succeed.

The full contract lives in `.trellis/workflow.md`.
