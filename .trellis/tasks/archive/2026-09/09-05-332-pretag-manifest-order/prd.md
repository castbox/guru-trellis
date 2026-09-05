# #332 pre-tag manifest Skill 顺序修复需求

## 目标

以 fresh `origin/main@d4d9c07945786b50411fe900a9056f4444128e62` 为执行基线，修复
`v0.6.15-guru.5` exact candidate 的 pre-tag throwaway gate：Guru Team extension
manifest 中的 `active_skill_ids` 必须与 Skill registry 派生的 active Skill ID 升序列表逐项一致，
使 #332 在任何 tag 副作用发生前重新取得 fresh PASS evidence。

## 当前事实

- live Issue [#332](https://github.com/castbox/guru-trellis/issues/332) 保持 open，并继续拥有
  `v0.6.15-guru.5` 的发布合同。
- task branch、worktree 与 `origin/main` 当前均绑定
  `d4d9c07945786b50411fe900a9056f4444128e62`。
- exact-candidate single-repository compatibility 命令在比较
  `api["skill_contracts"]["active_skill_ids"]` 与 registry-derived `active_ids` 时失败。
- 两侧均含 23 个 Skill ID，集合相同。唯一差异是 canonical manifest 把
  `guru-restore-archived-task` 放在 `guru-qualify-normal-scenario` 之前；registry-derived
  升序列表把它放在 `guru-reconcile-task-base` 之后。
- focused preset test 当前复制 manifest 的错误顺序，故该测试通过时仍无法证明 pre-tag
  排序合同成立。
- `trellis/guru-team-extension.json` 是 extension public API 的 canonical owner；
  `.trellis/guru-team/extension.json` 是 preset apply 生成的 dogfood installed projection。
- 当前 `issue-scope-ledger.json` 把 #332 写入 `close_issues`。本修复完成时尚未完成 tag、
  tag-pinned smoke、GitHub Release 与 Issue closeout，因此该 ledger 不满足 #332 的关闭条件。

## 需求范围

1. 将 `trellis/guru-team-extension.json` 的 `active_skill_ids` 修正为 registry 中
   `state=active` 的 23 个 Skill ID 的确定性升序列表。
2. 修改 focused preset test，使期望序列从 installed registry 的 active entries 派生并排序；
   测试不得继续维护第二份手写 Skill ID 顺序。
3. 通过 `trellis/presets/guru-team/scripts/bash/apply.sh --repo .` 生成 dogfood installed
   projection，不直接编辑生成清单来替代 canonical 修改。
4. 运行 focused preset test、source/installed validators、dogfood overlay drift 检查与
   exact-candidate single-repository compatibility profile。
5. 在 task 激活前修订 Issue Scope Ledger：`primary_issue` 保持 #332，`close_issues` 置空，
   #332 进入 `related_issues`；corrective PR 仅引用 #332，不得通过 merge 提前关闭 #332。
6. 保持任一 FAIL、SKIP、stale、cross-SHA、unknown、multiple 或 unmapped exit 阻断 tag。

## 验收标准

- AC1：canonical manifest 的 `active_skill_ids` 与 registry 中 active Skill ID 升序列表
  逐项完全一致，数量精确为 23。
- AC2：`guru-qualify-normal-scenario`、`guru-qualify-solution-mechanism`、
  `guru-reconcile-task-base`、`guru-restore-archived-task` 在目标序列中连续出现且顺序固定为
  本句顺序。
- AC3：focused preset test 从 installed registry 派生 active Skill ID 升序列表，并验证
  installed public API 与该列表逐项完全一致。
- AC4：preset apply 完成后，canonical source、dogfood installed projection 与 declared platform
  projection 通过项目现有 source/installed validator、managed parity 与 drift 检查。
- AC5：corrective PR 合并后，从 fresh `origin/main` 读取 `CANDIDATE_SHA`，以下命令绑定该
  candidate 并 fresh PASS；不得继续使用缺陷复现基线 `d4d9c07945786b50411fe900a9056f4444128e62`：

  ```bash
  CANDIDATE_SHA="$(git rev-parse refs/remotes/origin/main)"
  GURU_TEAM_THROWAWAY_SINGLE_REPO_COMPATIBILITY=1 \
  TRELLIS_WORKFLOW_SOURCE="gh:castbox/guru-trellis/trellis#${CANDIDATE_SHA}" \
  ./trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh
  ```

- AC6：工作树不残留 `.new`、`.bak`、`__pycache__`、`.pyc`、未声明 sidecar 或本次命令生成的
  owner-private residue。
- AC7：corrective PR 的 Issue Scope Ledger 不关闭 #332；tag、tag-pinned smoke、GitHub Release
  与 Issue closeout 继续由 #332 release workflow 承担并取得独立确认。

## 范围外

- 不修改 release tag、extension revision、Trellis CLI version 或历史 Release facts。
- 不重做已经合入的 release preparation、RDT/Architecture promotion 或历史 Branch Review。
- 不修改 Trellis upstream、全局 npm、`node_modules` 或业务仓库。
- 不创建、移动、删除或重写 tag、GitHub Release、`main` history、旧 branch 或旧 worktree。
- 本轮 planning 不执行 `task.py start`、产品文件修改、commit、push、PR、merge、tag、Release、
  Issue closeout或 cleanup。

## 未验证边界

planning 阶段不声明 manifest 修复、preset apply、focused test、throwaway compatibility、tag、
Release 或 post-publish smoke 已通过。所有发布证明必须绑定实际执行时的同一 exact candidate。
