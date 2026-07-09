# #65 实施计划

## 前置状态

- Worktree: `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/065-docs-ssot-phase2-sync-gate`
- Branch: `codex/065-docs-ssot-phase2-sync-gate`
- Base branch: `main`
- Source issue: https://github.com/castbox/guru-trellis/issues/65
- Middle-platform Knowledge Gate: 不适用。本任务只修改 Trellis workflow / preset / docs / specs，不涉及 Guru Team SDK / framework。
- Docs SSOT Plan: 见 `design.md`。本任务 docs 状态为 `complete_docs`，策略为 `ssot_first`。

## 执行清单

1. 更新 canonical workflow。
   - 在 `trellis/workflows/guru-team/workflow.md` 的 Phase 2 / implementation / check / scope drift 文案中加入 `Docs SSOT Plan` 消费合同。
   - 保留 `phase2-check.json` `docs_ssot` coverage 和 dirty-path audit 作为 objective evidence，不新增脚本语义判断。
2. 更新 durable docs 与 specs。
   - `docs/requirements/guru-team-trellis-flow.md`
   - `docs/requirements/requirement-main.md`
   - `.trellis/spec/workflow/workflow-contract.md`
   - `.trellis/spec/workflow/quality-guidelines.md`
   - `.trellis/spec/preset/overlay-guidelines.md`
3. 更新 public README surfaces。
   - `trellis/workflows/guru-team/README.md`
   - `trellis/presets/guru-team/README.md`
   - 仅当 top-level `README.md` 的日常入口或 install/upgrade 说明需要新增 Phase 2 docs 策略消费说明时才修改。
4. 更新 platform overlays。
   - continue overlays 的 `in_progress` route 要求确认并执行 `Docs SSOT Plan`。
   - implement agents 要求读取 plan、按策略执行、输出完整 docs handoff。
   - check agents 要求按策略验证 durable docs / task artifacts / code / tests 一致性。
5. 同步 dogfood installed copies。
   - 运行 `trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms`。
   - 检查并处理 `.new` / `.bak`。
   - 运行 `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`。
6. 执行验证。
   - 运行本文件下方验证命令。
   - 若完整 throwaway install / upgrade-update 未跑，在 Phase 2 / final report 明确说明未覆盖项和风险。

## Docs SSOT merge checkpoint

进入 Phase 2 check 前必须确认：

- `design.md` 中的 #65 Docs SSOT Plan 消费合同已经进入 canonical workflow、durable docs、spec 和 overlays。
- implement/check agent definitions 的 canonical overlay 与 dogfood installed copies 已同步。
- `delta_first` / `ssot_first` / `bootstrap_or_repair_docs` / `no_docs_update_needed` 四种策略的 Phase 2 实现和检查责任均有明确文案。
- task artifact 中没有未 merge 回 durable docs 的长期合同。

## 实现代理 handoff 要求

后续 `trellis-implement` / channel `implement` 完成时，报告必须包含：

- plan strategy: `ssot_first` / `delta_first` / `bootstrap_or_repair_docs` / `no_docs_update_needed`；
- durable docs 已更新或检查结果；
- task artifact delta 已 merge 回 durable docs 的内容；
- 只保留为 task history 的内容；
- 未同步限制、follow-up、当前 PR 声明限制；
- docs/spec/overlay responsibilities handled；
- validation run or deferred；
- concrete `trellis-check` focus areas。

## 阶段二检查要求

后续 `trellis-check` / channel `check` 必须覆盖：

- durable docs 是否已经按 `Docs SSOT Plan` 策略更新；
- task `prd.md` / `design.md` / `implement.md` 与 durable docs 是否冲突；
- workflow / overlay / agent definitions / specs / docs 是否表达同一合同；
- code/API/schema/config/deploy/test 是否与 durable docs 或已确认 task delta 一致；
- 测试计划或验证命令是否覆盖本次 docs/代码变化；
- scope drift 是否已回到 planning artifacts 和 `Docs SSOT Plan`，必要时重新 planning approval。

## 验证命令

```bash
python3 -m json.tool trellis/index.json
bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh
python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py
python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-09-065-docs-ssot-phase2-sync-gate
python3 ./.trellis/scripts/get_context.py --mode phase
python3 ./.trellis/scripts/get_context.py --mode phase --step 1.1
python3 ./.trellis/scripts/get_context.py --mode phase --step 2.1
python3 ./.trellis/scripts/get_context.py --mode phase --step 3.5
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
git diff --check
```

## Review 重点

- Phase 2 implementation/check 是否明确消费 #64 `Docs SSOT Plan`。
- 四种策略的实现责任和 check 责任是否完整。
- 是否误把 docs 内容充分性判断写入 Python / shell。
- canonical workflow、dogfood workflow、canonical overlays、dogfood installed copies、public docs、spec 是否一致。
- 是否遗漏 channel runtime、Codex、Cursor、Claude 的 implement/check agent definitions。
- 是否提前实现 #66 的 Branch Review / finish-work / PR body 阻断语义。

## 回滚点

- Markdown 改动可通过对应文件 diff 精确回滚。
- 若 preset apply 产生 `.bak` / `.new`，先人工审查再删除或合并；不得盲目提交。
- 若 dogfood drift check 失败，优先修 canonical overlay 或重新 apply，而不是只手工改 dogfood copy。
