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

- `planning`: keep `prd.md`, `design.md`, and `implement.md` in Chinese where required; ask for review before `task.py start`.
- `in_progress`: implement, check, update specs, then commit in Phase 3.4.
- after commit and before `finish-work`: run Branch Review Gate over the full diff from the intake base branch to HEAD:

```bash
.trellis/guru-team/scripts/bash/review-branch.sh --json --pass \
  --summary "中文审查结论" \
  --evidence "已按 intake base 到 HEAD 的完整 diff 覆盖文档、代码、测试、Trellis artifacts、CI/CD、容器、K8s/Kustomize、数据库 migration、Makefile，并判断本次变更的部署影响及是否需要同步修改部署资产"
```

Use `--finding 'P2|message|path'` or `--findings-file findings.json` when review finds issues. P0/P1/P2 block finish-work; P3 may be recorded without blocking. A passing gate must include a Chinese `--summary` and at least one concrete `--evidence` line.

Do not add a user-facing publish step. Publish PR remains the automatic follow-up inside `finish-work`.
