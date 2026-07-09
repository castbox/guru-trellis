# #64 实施计划

## 前置状态

- Worktree: `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/064-docs-ssot-plan-contract`
- Branch: `codex/064-docs-ssot-plan-contract`
- Base branch: `main`
- Source issue: https://github.com/castbox/guru-trellis/issues/64
- Middle-platform Knowledge Gate: 不适用。本任务只修改 Trellis workflow / preset / docs，不涉及 Guru Team SDK / framework。
- Docs SSOT Plan: 见 `design.md`。本任务 docs 状态为 `complete_docs`，策略为 `ssot_first`。

## 执行清单

1. 更新 canonical workflow。
   - 在 `trellis/workflows/guru-team/workflow.md` 的 Planning Artifacts、Repo Docs SSOT Reconciliation、workflow-state planning、Phase 1.1、Phase 1.4、Phase 1.6 中加入 `Docs SSOT Plan` 合同。
   - 保持 Phase 2 / Branch Review / finish-work 只是消费或记录 reconciliation，不新增 #65 / #66 阻断逻辑。
2. 更新 durable docs 与 specs。
   - `docs/requirements/guru-team-trellis-flow.md`
   - `docs/requirements/requirement-main.md`
   - `.trellis/spec/workflow/workflow-contract.md`
   - `.trellis/spec/workflow/quality-guidelines.md`
   - `.trellis/spec/preset/overlay-guidelines.md`
3. 更新 public README surfaces。
   - `trellis/workflows/guru-team/README.md`
   - `trellis/presets/guru-team/README.md`
4. 更新 platform overlays。
   - canonical overlay continue entries for shared, Codex, Cursor, Claude。
   - 确保 planning route 明确要求 `Docs SSOT Plan`，但不复制整段 workflow。
5. 同步 dogfood installed copies。
   - 运行 `trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms`。
   - 检查并处理 `.new` / `.bak`。
   - 运行 `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`。
6. 执行验证。
   - 运行本文件下方验证命令。
   - 若完整 throwaway install / upgrade 未跑，在 Phase 2 / final report 明确说明未覆盖项。

## Docs SSOT merge checkpoint

在进入 Phase 2 check 前必须确认：

- `design.md` 中的 `Docs SSOT Plan` 枚举和策略已经进入 `trellis/workflows/guru-team/workflow.md`。
- durable requirements docs 已说明 Phase 1 `Docs SSOT Plan` 的位置、枚举、策略和 artifact 责任。
- workflow specs / overlay guidelines 已把该计划合同作为未来维护规则。
- task artifact 中没有未 merge 回 durable docs 的长期合同。

## 验证命令

```bash
python3 -m json.tool trellis/index.json
bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh
python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py
python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-09-064-docs-ssot-plan-contract
python3 ./.trellis/scripts/get_context.py --mode phase
python3 ./.trellis/scripts/get_context.py --mode phase --step 1.1
python3 ./.trellis/scripts/get_context.py --mode phase --step 2.1
python3 ./.trellis/scripts/get_context.py --mode phase --step 3.5
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
git diff --check
```

## Review 重点

- `Docs SSOT Plan` 是否完整覆盖四个 docs 状态和四个策略。
- `prd.md` / `design.md` / `implement.md` 是否能定位同一个计划。
- 是否误把 docs 内容充分性判断写入 Python / shell。
- canonical workflow、dogfood copy、platform overlays、public docs、spec 是否一致。
- 是否遗漏 Cursor / Claude / Codex 的 continue 入口。
- 是否把 #65 / #66 的消费 / 阻断范围提前实现。

## 回滚点

- Markdown 改动可通过对应文件 diff 精确回滚。
- 若 preset apply 产生 `.bak` / `.new`，先人工审查再删除或合并；不得盲目提交。
- 若 dogfood drift check 失败，优先修 canonical overlay 或重新 apply，而不是手工只改 dogfood copy。
