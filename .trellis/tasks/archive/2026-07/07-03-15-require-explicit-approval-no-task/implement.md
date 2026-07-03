# Issue 15 实现计划

## Phase 1 完成条件

- [x] Phase 0 intake / preflight 已完成，worktree 与 task 已创建。
- [x] 读取 issue 15 live body。
- [x] 读取官方 Trellis `custom-workflow`、`custom-spec-template-marketplace` Markdown 文档。
- [x] 读取 `.trellis/spec/workflow`、`.trellis/spec/preset`、`.trellis/spec/docs`、`.trellis/spec/guides`。
- [x] Docs SSOT 结论：本仓库无业务 `docs/` 目录；长期文档面为 README、workflow README、preset README、workflow specs。
- [x] Middle-platform Knowledge Gate：不适用。

## 实现步骤

1. [x] 更新 canonical workflow：
   - `trellis/workflows/guru-team/workflow.md`
   - 搜索并更新 Request Triage、`[workflow-state:no_task]`、Phase 0 handoff、Rules 等相关段落。
2. [x] 同步 dogfood active workflow：
   - `.trellis/workflow.md`
3. [x] 更新 canonical start overlays：
   - `trellis/presets/guru-team/overlays/.agents/skills/trellis-start/SKILL.md`
   - `trellis/presets/guru-team/overlays/.codex/prompts/trellis-start.md`
   - `trellis/presets/guru-team/overlays/.codex/skills/trellis-start/SKILL.md`
4. [x] 运行 preset apply 同步 dogfood overlay 副本：
   - `trellis/presets/guru-team/scripts/bash/apply.sh --repo .`
   - 检查并处理 `.new` / `.bak`。
5. [x] 更新 specs / checklist：
   - `.trellis/spec/workflow/workflow-contract.md`
   - `.trellis/spec/workflow/quality-guidelines.md`
6. [x] 更新 durable docs：
   - `README.md`
   - `trellis/workflows/guru-team/README.md`
   - `trellis/presets/guru-team/README.md`
7. [x] 更新 `issue-scope-ledger.json` 的 acceptance evidence。
8. [x] 运行验证并记录结果。

## 验证命令

已执行并通过：

- `python3 -m json.tool trellis/index.json`
- `python3 -m json.tool trellis/workflows/guru-team/schemas/intake-handoff.schema.json`
- `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh`
- `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`
- `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-03-15-require-explicit-approval-no-task`
- `git diff --check`
- `python3 ./.trellis/scripts/get_context.py --mode phase`
- `python3 ./.trellis/scripts/get_context.py --mode phase --step 1.1`
- `python3 ./.trellis/scripts/get_context.py --mode phase --step 2.1`
- `python3 ./.trellis/scripts/get_context.py --mode phase --step 3.5`
- `trellis/presets/guru-team/scripts/bash/apply.sh --repo .`
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`
- `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`

开箱即用门禁结论：throwaway install 使用当前本地 preset installer 成功创建临时 repo，安装 `guru-team` workflow 和 companion assets，`check-env --json` 通过。当前未验证远端 `gh:castbox/guru-trellis/trellis` 能包含本分支未合并修改；该能力需等 PR merge 后由远端 marketplace 自然提供。

基础验证：

```bash
python3 -m json.tool trellis/index.json
python3 -m json.tool trellis/workflows/guru-team/schemas/intake-handoff.schema.json
bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh
python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py
python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-03-15-require-explicit-approval-no-task
git diff --check
```

workflow 解析：

```bash
python3 ./.trellis/scripts/get_context.py --mode phase
python3 ./.trellis/scripts/get_context.py --mode phase --step 1.1
python3 ./.trellis/scripts/get_context.py --mode phase --step 2.1
python3 ./.trellis/scripts/get_context.py --mode phase --step 3.5
```

overlay / preset：

```bash
trellis/presets/guru-team/scripts/bash/apply.sh --repo .
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
```

开箱即用门禁（尽量执行）：

```bash
trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh
```

如果 throwaway install 因本机网络、Trellis CLI 状态或远程 marketplace 未包含当前未合并分支而无法完全证明本次变更，最终报告必须明确说明未覆盖项和风险。

## 风险点

- canonical workflow 与 `.trellis/workflow.md` 漂移。
- overlay canonical 与 dogfood installed copy 漂移。
- README / workflow README / preset README 对 direct edit 的说法不一致。
- 误把 direct-edit override 写成 AI 可自行选择的捷径。
- 将 direct-edit override 错误扩展到 commit/push/PR。

## 回滚点

本次主要是 Markdown / spec / docs 变更。若验证发现解析或 overlay 同步问题，先回退对应 Markdown 段落到上一版，再缩小修改范围。
