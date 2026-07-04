---
name: trellis-continue
description: "Guru Team Trellis continue entry. Use to advance the current task through planning, implementation, commit, and Branch Review Gate before finish-work."
---

<!-- guru-team-overlay: v1 -->

# Guru Team Trellis Continue

Resume through the canonical workflow, not by remembering ad hoc steps.

```bash
python3 ./.trellis/scripts/get_context.py
python3 ./.trellis/scripts/get_context.py --mode phase
```

Route by current task status and `.trellis/workflow.md`.

- `planning`: keep `prd.md`, `design.md`, and `implement.md` in Chinese where required; run Docs SSOT discovery and the Middle-platform Knowledge Gate when relevant; ask for review before `task.py start`.
- `in_progress`: confirm knowledge-gate and docs responsibilities from artifacts, implement, check, reconcile specs/docs, then commit in Phase 3.4.
- after commit and before `finish-work`: first perform an AI/human review in code-review stance over the full diff from the intake base branch to HEAD, including Docs SSOT reconciliation evidence; write the review to task-local `{TASK_DIR}/review.md`; then record that review with Branch Review Gate:

```bash
.trellis/guru-team/scripts/bash/review-branch.sh --json --pass \
  --reviewer "codex-main-session" \
  --review-report ".trellis/tasks/<task>/review.md" \
  --summary "中文审查结论" \
  --evidence "已按 intake base 到 HEAD 的完整 diff 覆盖文档、代码、测试、Trellis artifacts、CI/CD、容器、K8s/Kustomize、数据库 migration、Makefile，并判断本次变更的部署影响及是否需要同步修改部署资产"
```

Use `--finding 'P2|message|path'` or `--findings-file findings.json` when review finds issues. P0/P1/P2 block finish-work; P3 may be recorded without blocking. A passing gate must include a Chinese `--summary`, at least one concrete `--evidence` line, and `--review-report` pointing at task-local `review.md`; `--reviewer` is identity metadata only. `review-branch.sh` records and validates the prior review; it is not the reviewer.

Do not stage/commit `review.md`, `review-gate.json`, handoff, journal, archive, or other Trellis metadata in `trellis-continue`. Do not push the branch, create a PR, call `publish-pr`, or invoke `finish-work` from `trellis-continue`. Stop after Branch Review Gate and wait for the user/session to explicitly invoke `trellis-finish-work`; that finish entrypoint commits remaining metadata-only changes and publishes after archive and journal succeed.
