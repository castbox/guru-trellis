<!-- guru-team-overlay: v1 -->
# Guru Team Continue Current Task

Resume work through `.trellis/workflow.md`; do not introduce extra user-facing stages.

```bash
python3 ./.trellis/scripts/get_context.py
python3 ./.trellis/scripts/get_context.py --mode phase
```

Route by task status:

- planning: keep required artifacts in Chinese, run Docs SSOT discovery and the Middle-platform Knowledge Gate when relevant, then ask for review, record/check `planning-approval.json`, and only then run `task.py start`.
- in_progress: confirm knowledge-gate and docs responsibilities from artifacts, implement, run full `trellis-check`, record/check `phase2-check.json` with the current pre-commit `dirty_paths`, reconcile specs/docs, then commit.
- after commit: obtain an independent Agent review over the full diff, write task-local `{TASK_DIR}/review.md`, then run Branch Review Gate before `/trellis-finish-work`, including Docs SSOT reconciliation evidence. Do not pass the gate from main-session self-review.

```bash
.trellis/guru-team/scripts/bash/review-branch.sh --json --pass \
  --review-source independent-agent \
  --reviewer "trellis-check-agent" \
  --review-report ".trellis/tasks/<task>/review.md" \
  --summary "中文审查结论" \
  --evidence "已按 intake base 到 HEAD 的完整 diff 覆盖文档、代码、测试、Trellis artifacts、CI/CD、容器、K8s/Kustomize、数据库 migration、Makefile，并判断本次变更的部署影响及是否需要同步修改部署资产"
```

Use `--finding` or `--findings-file` when the review has P0/P1/P2/P3 findings. P0/P1/P2 block finish-work. A passing gate must include `--review-source independent-agent`, a non-main-session `--reviewer`, a Chinese `--summary`, at least one concrete `--evidence` line, and `--review-report` pointing at task-local `review.md`; `--reviewer` is identity metadata only. `review-branch.sh` records and validates the prior independent review; it is not the reviewer. If independent Agent review is unavailable, stop with Branch Review Gate pending instead of writing a passing gate.

`task.py start` is only a status transition; `planning-approval.json` is the start gate evidence. Validation commands are only evidence inside `phase2-check.json`; they do not replace complete `trellis-check` coverage. `review-branch.sh` validates that Phase 2 check evidence exists before recording Branch Review Gate and performs the post-commit audit: committed non-metadata task work after the Phase 2 recorded HEAD must be covered by `phase2-check.json.dirty_paths`, and the current working tree must not contain non-metadata dirty paths. Do not re-record Phase 2 after the task work commit just to make HEAD match; return to Phase 2 only when new non-metadata changes appear or evidence is invalid.

Do not stage/commit `review.md`, `review-gate.json`, handoff, journal, archive, or other Trellis metadata in `/trellis-continue`. Do not push the branch, create a PR, call `publish-pr`, or invoke `finish-work` from `/trellis-continue`. Stop after Branch Review Gate and wait for the user/session to explicitly invoke `/trellis-finish-work`; that finish entrypoint commits remaining metadata-only changes and publishes after archive and journal succeed.

The full contract lives in `.trellis/workflow.md`.
