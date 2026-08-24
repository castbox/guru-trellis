# #304 Release readiness blockers 实施计划

## Implementation Checklist

- [ ] 逐段修订 `README.md` 的 stable identity、CLI install、workflow bootstrap/switch 与 clone 命令。
- [ ] 同步 `trellis/workflows/guru-team/README.md` 的 stable/current source 说明和 marketplace 命令。
- [ ] 同步 `trellis/presets/guru-team/README.md` 的 stable/current source、clone/switch/install 命令；保留明确 existing before-state 的旧版本。
- [ ] 修订 `.40` Requirements 的 `REQ-013`、`REQ-018` 及必要 traceability wording。
- [ ] 修订 `.40` Design 的 `DES-010`、`DES-016`、必要 inventory/traceability wording。
- [ ] 修订 `.40` Test 的 `TST-015`、`SCN-013`、test plan capability row 与 traceability evidence wording。
- [ ] 修订 Architecture distribution/current/evidence 中 capability-loss 与 consistency/installation 的边界。
- [ ] 重新检索 `.trellis/spec`；仅在发现相反定义时做最小 projection 同步。
- [ ] 检查 diff 只包含 accepted documentation/task scope，不含 verifier/workflow/Skill/schema/manifest/overlay/inventory 变化。
- [ ] 修正 `compare_capabilities()`：capability differences 只包含 `workflow`、`task_data`、`docs_authority`，extension identity 以独立一致性结果表达。
- [ ] 让 source/installed matrix consumer 分别对 extension identity drift 保持独立 fail-closed 阻断。
- [ ] 更新 owning test，覆盖 capability/identity 分类分离及两个 consumer 的独立阻断路径。

## Validation

1. 当前发布入口与历史 before-state 定向检索：

   ```bash
   rg -n "v0\.6\.5-guru\.10|0\.6\.5-guru\.36|@mindfoldhq/trellis@0\.6\.5|v0\.6\.15-guru\.1|0\.6\.5-guru\.37|@mindfoldhq/trellis@0\.6\.15" README.md trellis/workflows/guru-team/README.md trellis/presets/guru-team/README.md
   ```

2. Capability/consistency 语义检索，并与 verifier `compare_capabilities` 对照：

   ```bash
   rg -n "capability|skill_api|distribution|workflow|task_data|docs_authority|managed path|installed" docs/requirements/versions/current-main-0.6.5-guru.40 docs/design/versions/current-main-0.6.5-guru.40 docs/test/versions/current-main-0.6.5-guru.40 docs/architecture
   ```

3. 运行 `test_capability_comparison_isolates_version_binding` 及新增的 source/installed identity consistency consumer 定向测试，证明 identity drift 不构成 capability loss 但仍阻断 matrix。
4. 运行 current source package/ownership validator 与 dogfood overlay drift check；README-only preset 改动不调用 apply/reapply 写入 dogfood。
5. 验证 task 和 diff：

   ```bash
   python3 ./.trellis/scripts/task.py validate .trellis/tasks/08-24-304-release-readiness-fixes
   git diff --check
   git diff --name-only origin/main...HEAD
   ```

6. 进行完整 Phase 2 semantic check 与独立 committed full-diff Branch Review。完整 multi-platform Release matrix、Known Issue classification、candidate re-freeze、tag-pinned/post-publish smoke 由本 task 合并后的 #304 Release gates 从头执行。

## Stop Conditions

- verifier 修正需要超出 `compare_capabilities`、两个直接 consumer 与 owning test。
- 需要修改 workflow、Skill API/schema、installer inventory、manifest、overlay 或 candidate 功能代码。
- 发现 target tag/Release 已出现或 `origin/main` 在实施前演进，需先走 base reconciliation/candidate authority refresh。
- RDT/Architecture 修订无法保持现有 ID/traceability，需返回 Planning 而非临时扩张。
