# #376 实施计划

## Ordered Checklist

1. 对照现有 `guru-reconcile-task-base` contract、workflow、quality guideline 与 test fixture，确认 integration/authority/task-content 三类事实的现状。
2. 在 canonical workflow/spec 与 reconcile package 中收敛独立时钟语义，保持现有 typed exits、consumer 和无关 base delta 的 `resume_target`。
3. 更新 dogfood、preset 及声明平台投影，确保 canonical source 与安装副本一致。
4. 增加/修订正向 fixture：无关 base delta 保持 `reconciled`；真实 authority/planning assumption 变化返回 `planning_stale`；`post_plan` 不因单纯 base 更新回退。
5. 运行 package contract/runtime/eval 定向验证和 source/projection 一致性检查。
6. 通过 Phase 2 check 后，再执行 commit、完整 Branch Review 与 publication readiness；本规划阶段不执行这些动作。

## Validation Commands

```bash
python3 -m json.tool trellis/index.json
find trellis/skills/guru-team/runtime trellis/skills/guru-team/packages -name '*.py' -type f -print0 | xargs -0 python3 -m py_compile
python3 -m py_compile trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py
python3 ./.trellis/scripts/task.py validate .trellis/tasks/09-07-376-reduce-base-interference
git diff --check
```

追加执行 `guru-reconcile-task-base` 的 canonical unittest、runtime subset、eval/contract discovery，以及 preset projection drift 检查。

## Risk Points

- 不能把 base freshness digest、integration delta 或 recorder 输出当作 semantic planning decision。
- 不能把无关 base delta 误路由为 `planning_stale`，也不能放宽真实 authority 变化的 stale 路径。
- 不能覆盖当前 workspace 之外的 `main` dirty 文件、既有 sidecar 或其他 task workspace。

## Pre-start Gate

- 规划文档完成且无阻塞 open question。
- `implement.jsonl` 与 `check.jsonl` 各有真实研究/验证条目。
- 用户明确批准本规划摘要后，才允许 `task.py start` 和实现。
