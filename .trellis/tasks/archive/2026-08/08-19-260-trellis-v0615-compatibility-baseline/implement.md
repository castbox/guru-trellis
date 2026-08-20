# 实施计划

## 0. 激活前检查

- [x] 展示 `prd.md`、`design.md`、`implement.md` 与 Planning AI 结论，完成 workflow-owned plan review pause。
- [x] 用户确认当前计划后再执行 `python3 ./.trellis/scripts/task.py start .trellis/tasks/08-19-260-trellis-v0615-compatibility-baseline`。
- [x] 激活后运行 `trellis-before-dev`，加载 `implement.jsonl` 与当前 package/spec context。

## 1. 冻结 live authority 与 before inventory

- [x] 重读 Issue #260、#263/#264/#265/#266/#275 completion authority、remote main、replacement tag object/peeled commit、npm `0.6.5` / `0.6.15` package identity。
- [x] 从 canonical/installed manifests、registry、interfaces、ownership manifest 与 marketplace index 派生平台、managed paths、modes、skills、schemas、typed exits、commands 和 routes。
- [x] 读取 current Requirements -> Design -> Test -> Architecture locators，验证 version/status/source binding。
- [x] 生成排序后的 before capability projection；记录 exact candidate HEAD 和 inventory identity，禁止把临时完整扫描写入 repository。

## 2. 建立 official Trellis 行为探针

- [x] 在隔离 repo安装 `@mindfoldhq/trellis@0.6.5` 与 `0.6.15`，记录 `version`、`upgrade`、`update --dry-run`、条件式 `update --migrate`、workflow preview/switch 的真实行为。
- [x] 对照官方 custom workflow 与 spec template marketplace 文档，确认 Guru extension 仍使用官方扩展面。
- [x] 将 upstream-managed path、template hash、`.new` / `.bak` 和 local edit preservation 行为映射到 installer/ownership contract。

## 3. 实现 canonical migration

- [x] 更新 `trellis/guru-team-extension.json`、preset manifest/template、README version matrix 与验证器的 Trellis target binding。
- [x] 修复探针和矩阵发现的 installer/workflow/preset/overlay/runtime compatibility defect；只修改 #260 owner 范围。
- [x] 对 `.agents/skills/guru-discover-change-context/scripts/preview-change-context-history.sh` 完成 `declared_asset_missing` / `not_a_public_asset` 唯一归属判定，并实现该结论要求的分发或证明。
- [x] 同步 canonical package、dogfood installed package、`.agents`、Claude、Codex、Cursor 副本，保持 executable mode 和 public interface identity。
- [x] 不修改 Trellis upstream、全局 npm、`node_modules`、其它 Issue 正文或生产环境。

## 4. targeted validation 与 dogfood migration

按变更面运行 package/runtime、manifest、ownership、mode、routing 与 migration tests。基线命令集合：

```bash
python3 -m unittest trellis/presets/guru-team/scripts/python/test_verify_trellis_upgrade_contract.py
python3 -m unittest trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py
bash trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh
bash trellis/presets/guru-team/scripts/bash/verify-managed-python-runtime.sh
bash trellis/presets/guru-team/scripts/bash/test-verify-throwaway-python-routing-matrix.sh
bash trellis/presets/guru-team/scripts/bash/apply.sh --repo .
bash trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
```

- [x] 在 dogfood repo运行 official upgrade/update、workflow preview/switch 和 preset reapply。
- [x] 逐个处理 `.new` / `.bak`，最终运行 recursive zero-sidecar scan。
- [x] 运行 source/installed package checks、registry/interface/schema checks、executable/managed mode checks 与 current platform equality checks。
- [x] 任一 dogfood authority、sidecar 或 inventory drift 未闭合时停止矩阵。

## 5. 全平台 Throwaway 矩阵

对 live 派生平台逐个执行，不以当前静态三平台列表替代派生结果：

### 5.1 clean cell

- [x] 创建独立临时 Git repo 与隔离 npm/Trellis config。
- [x] 使用 official `0.6.15` 执行 marketplace init 和 `guru-team` workflow install。
- [x] 对 exact #260 candidate执行 preset initial apply。
- [x] 验证 index、workflow、preset、hooks、skills、commands、prompts、schemas、scripts、modes、template hashes、sidecars 与 installed identity。
- [x] 运行 Phase 0、Planning、Check、Branch Review、Finish-family representative installed smoke。
- [x] 运行 #263/#264/#265 package/profile smoke 和 #266 docs/projection assertion。

### 5.2 existing cell

- [x] 从 `v0.6.5-guru.10` 构建独立业务 repo并验证 before identity。
- [x] 使用 official package执行 `trellis upgrade` 和 `trellis update --dry-run`。
- [x] dry-run 含 `MIGRATION REQUIRED` 时执行 `trellis update --migrate`；否则记录未执行。
- [x] 执行 workflow marketplace preview，再执行正式 switch。
- [x] 对 #260 candidate执行 preset reapply。
- [x] 重跑 clean cell 的 installed、inventory、#263/#264/#265/#266 与 sidecar/mode 断言。

### 5.3 cell gate

- [x] 每个 cell 绑定 platform/scenario/source/Trellis version/result，mandatory failure count 为 `0`。
- [x] 每个 repo最终 `.new` / `.bak` 计数为 `0`。
- [x] clean 与 existing 之间不得复用 repo、runtime checkpoint 或 install manifest。

## 6. before/after capability comparison

- [x] 生成 after projection，并按 `distribution`、`skill_api`、`workflow`、`task_data`、`docs_authority` 比较。
- [x] AI 审查每个差异并分类；存在 `blocking_loss` 时返回实施，禁止进入 Phase 2。
- [x] 证明 history/index/query、semantic naming、Docs SSOT、Finish、cleanup 和平台 routes 未回退。
- [x] 将版本绑定和已审查 migration mapping 写入 current docs，不保存完整扫描日志。

## 7. A/B 独立 business task 验证

- [x] 从一个 fixed clean base生成 A/B 隔离 clone。
- [x] A：在展示 exact GitHub test repo/ref/action 并取得该副作用确认后，使用 `workspace_mode=worktree`、真实 `github_pr` route完成完整 task 生命周期并绑定唯一 A PR；缺少授权 target 时 fail closed。
- [x] B：`workspace_mode=current`、`none` route；完成完整 task 生命周期，PR read/create count 为 `0`。
- [x] 检查 A/B tracked diff 无 fixed handoff、workspace journal、shared index、shared runtime cache、parent/child mutation 或跨 task metadata。
- [x] 检查 archive 只移动 exact task-local path，A/B 不互相 merge bookkeeping commit。
- [x] 分别注入 Finish、provider、cleanup normal failure，验证 typed recovery 只恢复原 owner，不回到 Phase 0，不重建另一 task。
- [x] 验证 A -> B 与 B -> A 两种 merge 顺序；第二次合并的 Guru metadata conflict count 为 `0`，tracked Guru metadata path intersection 为空。
- [x] cleanup 前后验证 retained refs 与 reviewed-content/archive/Finish/bookkeeping commit reachability。

## 8. Docs SSOT promotion

- [x] 调用 `guru-maintain-requirements-design-test-ssot:task_impact_sync`，消费 `sync_required` 后写 task contribution并执行 `promotion`。
- [x] 调用 `guru-maintain-architecture-baseline:task_impact_sync`，同步 Architecture current/evidence 与 fitness 结论。
- [x] 更新 versioned Requirements / Design / Test、Architecture、四个 README locator 和最小 `.trellis/spec` projection。
- [x] 写入 current-main compatibility identity、矩阵结果、能力差异、A/B 结论、known gaps 与 #267 release boundary。
- [x] 验证 `.trellis/spec` 只含摘要/index projection，未复制 versioned docs 正文。

## 9. 完整质量门禁

- [x] `python3 ./.trellis/scripts/task.py validate .trellis/tasks/08-19-260-trellis-v0615-compatibility-baseline`
- [x] 运行全部受影响 package/runtime tests、source/installed distribution checks、dogfood drift、full platform matrix、A/B lifecycle matrix 与 Docs SSOT checks。
- [x] `guru-check-task` 对完整 scope执行 Phase 2 semantic review；实现 finding 修复后重跑完整受影响 evidence。
- [ ] `guru-create-task-commit` 只 stage #260 文件并创建中文 Conventional Commit。
- [ ] 独立 `guru-review-branch` 覆盖 `origin/main...HEAD` 完整 diff；P0/P1/P2/P3 finding 全部闭合。
- [ ] `guru-review-task-publication` 复核中文 PR title/body、验证边界、安全/部署影响、Docs SSOT 与 `Closes #260` 唯一关闭范围。
- [ ] push 和 PR 前重新核对 remote main；base 演进时执行 `guru-reconcile-task-base`，不弱化矩阵。

## 10. 合并、Finish 与边界

- [ ] PR full merge gate 通过后展示 exact PR/head/base/merge 动作并询问 `合并PR`。
- [ ] 合并后验证 merge-head identity、Issue #260 closure、archive/history/Finish/cleanup 与 primary checkout convergence。
- [ ] 不创建 stable tag，不创建 GitHub Release，不执行 #267 release smoke，不开始 #267 task。
- [ ] #248/#252 只消费最小兼容合同，本任务不实现其 Phase-owner 变更。

## 11. 回滚点

- canonical migration、dogfood apply、每个平台 cell、A/B fixture、Docs promotion 各自形成独立回滚点。
- throwaway failure 删除并重建 exact cell；dogfood failure 保留 sidecar 和 diff供审查，修复 canonical 后从 clean candidate重跑。
- 不使用 `git reset --hard`、`git checkout --` 或覆盖用户并行改动的清理命令。
- scope/authority drift、未处理 sidecar、capability loss、cross-task write、unreachable commit、平台 cell failure 均 fail closed。
