# #66 实施计划

## 前置门禁

- [ ] 用户确认本 `prd.md` / `design.md` / `implement.md` 后，记录 `planning-approval.json`，运行 `check-planning-approval.sh --json`，再 `task.py start`。
- [ ] 实现前运行 `check-workspace-boundary.sh --json --task .trellis/tasks/07-09-066-docs-ssot-phase3-enforcement`。
- [ ] 默认 sub-agent 模式：实现由 `trellis-implement` / channel `implement` 执行，Phase 2 check 由 `trellis-check` / channel `check` 执行；main session 只协调、记录和验证。

## 实现步骤

1. 更新 workflow durable contract
   - 修改 `trellis/workflows/guru-team/workflow.md`。
   - 同步 `.trellis/workflow.md`。
   - 明确 Branch Review Gate 的 Docs SSOT 验证职责、finding/blocking 规则、review 后 non-metadata drift 回 Phase 2/3、finish-work 不做首次 docs merge、PR body Docs SSOT 结果要求。

2. 更新 specs 和 durable docs
   - 修改 `.trellis/spec/workflow/workflow-contract.md`、`.trellis/spec/workflow/quality-guidelines.md`。
   - 修改 `.trellis/spec/preset/overlay-guidelines.md`。
   - 修改 `docs/requirements/requirement-main.md`、`docs/requirements/guru-team-trellis-flow.md`。
   - 按实际影响检查 `trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md` 是否需要补充。

3. 更新 platform overlays 与 installed copies
   - Continue overlays：强调 review sub-agent 只验证 Docs SSOT reconciliation，发现当前 scope 不一致必须 finding，不可补救。
   - Finish-work overlays：强调 PR body Docs SSOT section/result，finish-work 只处理 metadata tail，non-metadata docs/spec/source/test drift fail closed。
   - Check/review agent definitions：如当前 Branch Review mode wording 不足，补充 Docs SSOT judgment 必须检查 Phase 2 结果而非补做。
   - 修改 canonical overlay 后运行 preset apply 同步 dogfood installed copies。

4. 可选脚本增强
   - 如选择增强 `validate_pr_body_quality`，新增 `Docs SSOT` / `文档同步` section alias 或 key presence check。
   - 同步 test helper `valid_pr_body`。
   - 添加单测：缺失 Docs SSOT section 被阻断；包含 section 的 reviewer-readable body 通过。
   - 不添加任何语义充分性判断。

5. Phase 2 check 和提交前验证
   - 确认 implementation handoff 记录 strategy、durable docs sync result、merged delta、task-history-only、follow-up/limit。
   - 运行 `trellis-check` / channel `check`，覆盖 durable docs、task artifacts、workflow/overlay/script/test 一致性。
   - 记录并验证 `phase2-check.json` 后提交任务工作。

6. Phase 3 Branch Review Gate
   - 提交后由独立 review sub-agent 审查 `origin/main...HEAD`。
   - Raw report 和 `review.md` 使用中文，包含 Docs SSOT 判断、部署/安全影响、findings/observations/follow-up candidates。
   - 如有 finding，回 Phase 2 修复并由同一 finding owner 闭环，再换 fresh final reviewer。
   - 通过后由 main session 运行 `review-branch.sh` 记录 gate，停止等待 `trellis-finish-work`。

## 验证计划

基础验证：

```bash
python3 -m json.tool trellis/index.json
bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh
python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py
python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py
python3 -m unittest trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py
python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-09-066-docs-ssot-phase3-enforcement
python3 ./.trellis/scripts/get_context.py --mode phase
python3 ./.trellis/scripts/get_context.py --mode phase --step 3.5
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
git diff --check
```

Overlay / install 验证：

```bash
trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
```

尽量补充 throwaway install / workflow preview：

```bash
trellis init -y --workflow guru-team --workflow-source gh:castbox/guru-trellis/trellis
trellis workflow --marketplace gh:castbox/guru-trellis/trellis --template guru-team --create-new
```

如果当前分支无法通过 public remote marketplace 被 Trellis CLI 直接采样，最终报告必须说明只验证了本地 canonical/dogfood drift，未完整验证新仓库开箱即用。

## Docs SSOT checkpoint

- durable docs/spec/workflow/overlay 更新必须在 Phase 2 check 前完成。
- `phase2-check.json` 需要包含 Docs SSOT strategy 执行结果和一致性检查。
- Branch Review Gate evidence 必须明确记录 Docs SSOT reconciliation 已由 Phase 2 完成，final reviewer 只验证不补救。
- `pr-body.md` 必须包含 Docs SSOT / 文档同步结果，不能用“详见 artifact”替代。

## 回滚点

- 如果脚本 PR body section 检查误伤现有合理 body，回滚脚本检查，只保留 AI readiness workflow/overlay 要求。
- 如果 overlay apply 产生 `.new` / `.bak`，逐个检查，必要时暂停说明冲突，不静默提交。
- 如果 throwaway install 失败且与本任务无关，保留核心 workflow/docs/script 改动，但在 PR body 和最终回复中记录未覆盖的开箱即用风险。
