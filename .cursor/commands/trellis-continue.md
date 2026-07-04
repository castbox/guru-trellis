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
- after commit: first perform an AI/human review in code-review stance over the full diff, then run Branch Review Gate before `/trellis-finish-work`, including Docs SSOT reconciliation evidence.

```bash
.trellis/guru-team/scripts/bash/review-branch.sh --json --pass \
  --reviewer "cursor-main-session" \
  --summary "中文审查结论" \
  --evidence "已按 intake base 到 HEAD 的完整 diff 覆盖文档、代码、测试、Trellis artifacts、CI/CD、容器、K8s/Kustomize、数据库 migration、Makefile，并判断本次变更的部署影响及是否需要同步修改部署资产"
```

Use `--finding` or `--findings-file` when the review has P0/P1/P2/P3 findings. P0/P1/P2 block finish-work. A passing gate must include a Chinese `--summary`, at least one concrete `--evidence` line, and `--reviewer` or `--review-report`. `review-branch.sh` records and validates the prior review; it is not the reviewer.

Do not push the branch, create a PR, call `publish-pr`, or invoke `finish-work` from `/trellis-continue`. Stop after Branch Review Gate and wait for the user/session to explicitly invoke `/trellis-finish-work`; publish happens only inside that finish entrypoint after archive and journal succeed.

The full contract lives in `.trellis/workflow.md`.
