# #332 pre-tag manifest Skill 顺序修复设计

## 设计边界

本 task 修复一项 release-gate consistency defect，不改变 Skill 集合、Skill 生命周期、schema、
external exit、command、版本映射或用户流程。变更只收敛 public manifest 的列表顺序、focused
test 的期望来源与 dogfood installed projection。

## Authority 与数据流

单一数据流如下：

```text
trellis/skills/guru-team/registry.json
  -> active entries
  -> Skill ID 升序列表
  -> trellis/guru-team-extension.json public_api.skill_contracts.active_skill_ids
  -> preset apply
  -> .trellis/guru-team/extension.json extension.public_api.skill_contracts.active_skill_ids
  -> source/installed validators + focused preset test + throwaway compatibility gate
```

- Registry 拥有 Skill identity 与 lifecycle state。
- `trellis/guru-team-extension.json` 拥有发布给 installer 的 explicit public API manifest。
- Preset apply 拥有 dogfood installed manifest 生成。
- Focused preset test 从 installed registry 读取 `state=active` entries，提取 ID 并升序排序，
  再与 installed public API 比较。该测试不保留第二份手写顺序。

## 修改设计

1. 在 canonical manifest 中仅移动 `guru-restore-archived-task`，使四项局部顺序成为：
   `guru-qualify-normal-scenario`、`guru-qualify-solution-mechanism`、
   `guru-reconcile-task-base`、`guru-restore-archived-task`。
2. 在 focused preset test 中删除 23 项手写期望列表，改为从
   `.trellis/guru-team/skills/registry.json` 派生 active Skill ID 升序列表。
3. 运行 preset apply，让 installed projection 继承 canonical manifest；审查 apply 产生的全部 diff，
   仅保留本 task 接受的 manifest projection 变化。
4. apply 若产生 `.new` 或 `.bak`，立即停止实施并检查冲突来源；不得把 sidecar 当作成功投影。

## 兼容性与迁移

- Skill ID 集合与数量保持不变，故不存在 public API 增删或 schema migration。
- JSON array 顺序收敛到 validator 已执行的 registry-derived 升序合同。
- 旧 installed projection 通过 preset apply/reapply 进入新顺序；不得手工补丁替代 installer 路径。
- Release Gate 继续 fail closed；本修复不得放宽任何 validator 或跳过 exact-candidate throwaway。

## Docs SSOT Plan

策略：`no_docs_update_needed`。

本修复没有用户合同、安装命令、版本映射、workflow phase 或 architecture decision 变化。
`prd.md`、`design.md`、`implement.md` 记录 task-local 缺陷与验证计划；公共 README、RDT 与
Architecture current authority 不发生正文修改。后续 impact owner 若发现真实 public contract
变化，必须返回 planning revision，不能在 Phase 2 静默扩张范围。

## Issue 关闭语义

Corrective PR 完成时只恢复 pre-tag gate，不满足 #332 Definition of Done。task 激活前必须把
Issue Scope Ledger 收敛为 `close_issues=[]`，保留 #332 为 primary authority 并列入
`related_issues`。Tag、tag-pinned smoke、GitHub Release 与 #332 closeout 仍由 release workflow
按独立副作用边界执行。

## 回滚与停止

未提交阶段的修复仅存在于 `fix/332-pretag-manifest-order` worktree。验证失败时停止在该分支，
不修改 `origin/main`、历史 tag、Release、旧 task、旧 branch 或旧 worktree。Tag 前没有不可逆
发布副作用。
