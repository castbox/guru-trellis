# 实现计划：Issue 44

## 顺序

1. 更新 `guru_team_trellis.py`
   - 将 Branch Review Gate blocker 改为任意 finding。
   - 新增 observation / followup candidate 解析与 payload 字段。
   - 新增 closure-before-final 与 fresh final reviewer 客观校验。
   - 更新错误文案中 “P0/P1/P2” 的 Branch Review Gate 语义。
2. 更新 `test_guru_team_trellis.py`
   - 覆盖 P3 / 任意 finding 阻断 pass。
   - 覆盖 observation 不阻断。
   - 覆盖 followup candidate 不阻断。
   - 覆盖缺少 finding owner closure review 阻断。
   - 覆盖 fresh final reviewer 0 findings 可放行。
   - 覆盖缺少 `--agent-assignment` 阻断。
   - 覆盖 final review round reviewed HEAD stale 阻断。
3. 更新 workflow 与 overlay 文案
   - canonical workflow 与 dogfood `.trellis/workflow.md`。
   - canonical overlay 中 continue entry。
   - 运行 preset apply 同步 dogfood installed copies。
4. 更新 specs 与 durable docs
   - `.trellis/spec/workflow/companion-scripts.md`
   - `.trellis/spec/workflow/workflow-contract.md`
   - `docs/requirements/requirement-main.md`
5. 验证
   - `python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
   - `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`
   - `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh`
   - `python3 -m json.tool trellis/index.json`
   - `python3 ./.trellis/scripts/get_context.py --mode phase --step 3.5`
   - `trellis/presets/guru-team/scripts/bash/apply.sh --repo .`
   - `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`
   - `git diff --check`
   - `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-05-44-branch-review-gate-finding-fresh`

## Phase 2 check 覆盖计划

- requirements: issue #44 与 `prd.md`。
- design: `design.md` artifact 与 workflow/spec contract。
- code: Python companion script。
- tests: unit tests 覆盖新 gate 语义。
- spec_sync: `.trellis/spec/workflow/*`。
- cross_layer: workflow -> overlay -> script -> tests -> docs 同步。
- docs_ssot: `docs/requirements/requirement-main.md`。
- deployment: 本任务不改变部署形态；验证中记录 CI/CD、Docker、K8s、DB、Makefile 无需更新。

## Branch Review Gate 计划

提交 task work 后，如果上一轮 reviewer 已发现 findings，先把当前 HEAD 交回该 reviewer 作为 `问题闭环审查代理` 复审到 0 findings；随后再调度新的 fresh `最终放行审查代理` 审查完整 `origin/main...HEAD` diff。若新的 fresh final reviewer 又发现 finding，该 agent 也先作为闭环代理复审到 0，再调度另一位新的 fresh final reviewer。

## 未计划执行

- 不计划完整 throwaway install，除非时间允许；若跳过，最终报告明确说明未覆盖。
