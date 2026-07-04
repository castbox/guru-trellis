<!-- guru-team-overlay: v1 -->
# Guru Team Continue Current Task

Resume work through `.trellis/workflow.md`; do not introduce extra user-facing stages.

```bash
python3 ./.trellis/scripts/get_context.py
python3 ./.trellis/scripts/get_context.py --mode phase
```

Route by task status:

- planning: keep required artifacts in Chinese, run Docs SSOT discovery and the Middle-platform Knowledge Gate when relevant, then ask for review before `task.py start`.
- in_progress: confirm knowledge-gate and docs responsibilities from artifacts, implement, check, reconcile specs/docs, then commit.
- after commit: first perform an AI/human review in code-review stance over the full diff, write task-local `{TASK_DIR}/review.md`, then run Branch Review Gate before `/trellis:finish-work`, including Docs SSOT reconciliation evidence.

```bash
.trellis/guru-team/scripts/bash/review-branch.sh --json --pass \
  --reviewer "codex-main-session" \
  --review-report ".trellis/tasks/<task>/review.md" \
  --summary "中文审查结论" \
  --evidence "已按 intake base 到 HEAD 的完整 diff 覆盖文档、代码、测试、Trellis artifacts、CI/CD、容器、K8s/Kustomize、数据库 migration、Makefile，并判断本次变更的部署影响及是否需要同步修改部署资产"
```

Use `--finding` or `--findings-file` when the review has P0/P1/P2/P3 findings. P0/P1/P2 block finish-work. A passing gate must include task-local `--review-report`, a Chinese `--summary`, and at least one concrete `--evidence` line. `--reviewer` records identity only and cannot replace `review.md`. `review-branch.sh` records and validates the prior review; it is not the reviewer.

The full contract lives in `.trellis/workflow.md`.
