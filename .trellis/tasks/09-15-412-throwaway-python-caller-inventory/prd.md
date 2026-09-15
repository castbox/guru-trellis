# #412 修复 throwaway Python caller inventory 漂移

## 目标与价值

恢复 canonical caller inventory 与当前正常源码发现结果的一致性，使 `v0.6.17-guru.1` 的 focused clean install/update/reapply gate 能在新的 exact candidate 上重新建立可信证据。

## 已确认事实

- 外部需求权威是 OPEN Issue [#412](https://github.com/castbox/guru-trellis/issues/412)；关联发布权威是保持 OPEN 的 [#410](https://github.com/castbox/guru-trellis/issues/410)。
- intake base 是 `main@6b97d4c7d659105a7a0d443946f89ba42866b72b`。
- 支持的 source inventory 检查在干净基线上稳定报告：
  - missing：`helper-python_subprocess_second_hop-559881091ab0`
  - stale：`helper-python_subprocess_second_hop-c2f9a2db85f3`
- canonical 数据 owner 是 `trellis/presets/guru-team/tests/throwaway-python-callers.json`；发现与校验 owner 是 `trellis/presets/guru-team/scripts/python/verify_throwaway_python_routing.py`。
- 当前缺陷是普通维护遗漏，不需要伪造 artifact、绕过 workflow、攻击输入或修改运行时行为即可复现。
- Phase 2 fresh Architecture/RDT 检查确认 `docs/architecture/README.md` 与三层 RDT `.52` authority 已把唯一 current identity 晋升为 `current-main-0.6.17-guru.52`，但六处 current projection/README 导航仍停留在 `.51`、#408 source binding 或保留错误的 active 状态。
- 该 projection 漂移来自 #410 preparation PR #411 的既有 promotion 漏项，预存在本 task base `6b97d4c7d659105a7a0d443946f89ba42866b72b`；它不是 caller inventory 修改引入的回归，但按 projection 自身 freshness 合同阻塞 #412 mandatory Phase 2。
- fresh RDT review 进一步确认 `.52` authority 自身存在内部冲突：#410 contribution 定义 `D410-01..06` / `T410-01..06`，versioned Design 仅投影 `D410-01..04`，versioned Test 投影 `T410-01..08`；Requirements、Design、Test 三层 `.52/traceability.md` 缺少完整 #410 双向 trace 且残留 `.51/current`，contribution manifest 同时声明互斥的 reviewed/pending promotion state。
- live Issue #412 已明确接纳该 repair 为同一交付单元；#410 仍保持 OPEN，并继续独占 merge 后 exact-candidate、tag、tag-pinned smoke、GitHub Release 与最终关闭责任。

## 需求

### R412-01 唯一 canonical 行修复

使用旧 `id` 和完整旧 `anchor_sha256` 定位唯一 stale object，把其 `id` 与 `anchor_sha256` 更新为当前 discovery 计算结果，并将同一 object 移到 discovery 产生的 canonical 顺序位置。必须保留 owner、kind、classification、expected launcher、ordinal 和其他 object 的相对顺序。

### R412-02 canonical 与 projection 一致性

source 与 installed inventory validator 必须读取同一 canonical 语义并通过。若 preset apply 产生受管理 installed/dogfood projection，必须使用 canonical installer 同步并通过四平台 projection parity、ownership、preset reapply 和 dogfood drift；不得手工建立第二个 inventory authority。

### R412-03 focused throwaway 验证

在干净临时环境执行 Issue #412 要求的 focused install、existing-project update/reapply、workflow/preset 检查。任一 `FAIL`、`SKIP`、stale、unknown、multiple、unmapped 或未解释 mutation 都阻断交付。

### R412-04 发布证据边界

本任务的 branch 验证只证明 #412 remediation。PR 合并后必须回到 #410，从 fresh `origin/main` 冻结新的 exact candidate，并从零重跑该 candidate 的发布证据；不得复用 `6b97d4c7` 的 pass/fail assertion。

### R412-05 副作用边界

task commit、push、PR、merge 和 post-merge candidate 操作分别展示精确 ref、HEAD、路径、命令和范围并取得当前确认。不得创建 tag 或 GitHub Release，不得关闭 #410。

### R412-06 `.52` current projection repair

修复以下六处 pre-existing projection 漂移，使其与 live Architecture/RDT `.52` authority 一致：

- `.trellis/spec/architecture/baseline-usage.md`
- `.trellis/spec/docs/requirements-design-test-ssot.md`
- `.trellis/spec/docs/public-docs.md`
- `docs/requirements/README.md`
- `docs/design/README.md`
- `docs/test/README.md`

只更新 current identity、current source binding 及 active/superseded 导航。`.51` 和更早版本化 authority 保持 immutable，合法历史说明不得机械替换；repair 不新增产品能力、公共 API、runtime 行为、release lifecycle 状态或新的 authority version。

### R412-07 `.52` authority repair

在同步六处 current projection 前，由 RDT owner 修复 #410 `.52` authority 内部冲突，修改范围仅限：

- `docs/requirements-design-test-contributions/410-release-v0617-guru1/design.md`
- `docs/requirements-design-test-contributions/410-release-v0617-guru1/test.md`
- `docs/requirements-design-test-contributions/410-release-v0617-guru1/traceability.md`
- `docs/requirements-design-test-contributions/410-release-v0617-guru1/manifest.yaml`
- `docs/design/versions/current-main-0.6.17-guru.52/design-main.md`
- Requirements、Design、Test 三层 `current-main-0.6.17-guru.52/traceability.md`

RDT owner 必须基于 reviewed #410 contribution、Requirements/Test 正文、Architecture `.52/active` inheritance 和 release contract 决定唯一正确的 D410/T410 投影，不预设 `D410-01..04`、`D410-01..06`、`T410-01..06` 或 `T410-01..08` 哪一组为准。repair 只统一 identifier 集合、Architecture inheritance、三层双向 trace closure 与唯一 promotion state；不得创建 `.53`、改变 #410 lifecycle 或引入新的产品/API/runtime 行为。

## 验收标准

1. stale row 的旧 `id` 和旧完整 `anchor_sha256` 在 inventory 中均为 0 次，新值均为 1 次；目标 object 位于 discovery 要求的 `secondary_callers[7]`，其余字段及其他 object 的相对顺序不变。
2. source 与 installed caller inventory 检查不再报告 missing 或 stale。
3. focused clean install、existing-project update/reapply、workflow/preset 检查全部成功且无未解释 sidecar。
4. Shared、Codex、Claude、Cursor projection parity、ownership、preset reapply、dogfood drift、changed-file secret scan、`git diff --check` 和 residue hygiene 全部通过。
5. Phase 2、task commit、完整 `origin/main...HEAD` 独立 Branch Review、Publication、Finalizer、preparation PR 和 merge 按标准 owner 顺序完成，所有 P0-P3 finding 关闭。
6. 合并后的新 candidate 与所有后续发布 gate 绑定同一 commit/tree；#410 继续保持 OPEN。
7. 六处 projection 均指向 `current-main-0.6.17-guru.52` / `active` 的 live authority，source binding 承接 reviewed #410 contribution 与 immutable `.51` predecessor；Requirements、Design、Test 三个 README 均将 `.52` 标为唯一 active、`.51` 标为 superseded，并清除仍被描述为 current 的 #408 / extension `.41` / `.51` trace wording。
8. Architecture 与 RDT `repair`、scope-change 后 fresh Planning owners、Phase 2 Architecture 和 `guru-check-task` 均不再因 projection stale 阻塞。
9. #410 contribution、`.52` Design/Test/traceability 与 manifest 对 D410/T410 集合、Architecture `.52/active` inheritance、三层双向 trace closure 和 promotion state 给出单一无冲突 authority，且 RDT repair checker 通过。

## 明确排除

- 不修改 caller discovery 算法、helper 行为、公共 Skill API、schema、workflow exit 或 release identity。
- 不修改 Trellis upstream、全局 Python/npm、`node_modules`、业务仓库或生产环境。
- 不创建 tag、GitHub Release、task-local release notes、动态 release checklist 或 tracked lifecycle state。
- 不清理本任务创建前已经存在的 `__pycache__`，也不清理未由 #412 创建的 worktree/runtime 资源。
- 不改写 `.51` 或更早版本化 Architecture/RDT authority 的正文，不借 projection repair 扩展新的产品、架构或发布需求。
- 不创建 `.53`，不改变 #410 release lifecycle、tag/Release/Issue closure ownership，不借 authority repair 新增产品能力、公共 Skill API 或 runtime 行为。

## 阻塞问题

无开放的产品或范围问题。进入实现前仍需完成 active-task scope-change 的 task update 校验、fresh wording/Planning owners、Architecture/RDT repair route 与新的 planning approval；这些是流程 gate，不是未决需求。
