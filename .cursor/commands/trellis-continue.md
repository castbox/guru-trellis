<!-- guru-team-overlay: v1 -->
# Guru Team Continue Current Task

Resume work through `.trellis/workflow.md`; do not introduce extra user-facing stages.

```bash
python3 ./.trellis/scripts/get_context.py
python3 ./.trellis/scripts/get_context.py --mode phase
```

Route by task status:

- planning: keep required artifacts in Chinese and ask for review before `task.py start`.
- in_progress: implement, check, update specs, then commit.
- after commit: run Branch Review Gate before `/trellis-finish-work`.

```bash
.trellis/guru-team/scripts/bash/review-branch.sh --json --pass \
  --summary "中文审查结论" \
  --evidence "已按 intake base 到 HEAD 的完整 diff 覆盖文档、代码、测试、Trellis artifacts、CI/CD、容器、K8s/Kustomize、数据库 migration、Makefile，并判断本次变更的部署影响及是否需要同步修改部署资产"
```

Use `--finding` or `--findings-file` when the review has P0/P1/P2/P3 findings. P0/P1/P2 block finish-work. A passing gate must include a Chinese `--summary` and at least one concrete `--evidence` line.

The full contract lives in `.trellis/workflow.md`.
