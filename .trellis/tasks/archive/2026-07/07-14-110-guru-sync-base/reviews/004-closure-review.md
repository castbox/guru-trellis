# 第 4 轮问题闭环审查

## 审查身份与范围

- 角色：`问题闭环审查代理`
- 技术代理：`/root/branch_review_110_release`
- 复用决策：`reuse-for-closure`
- 审查 HEAD：`2def8b748dae986e6f9e4d2912c2f8e6d617917a`
- 基线：`origin/main`（`f9f094f0a995e230226c8a94ff34944ba9d87b53`）
- Finding-fix 差异：`420602b34759b7299861a7ab5b1a3a9876873419..2def8b748dae986e6f9e4d2912c2f8e6d617917a`，52 个文件、3133 行新增、266 行删除
- 完整差异：`origin/main...2def8b748dae986e6f9e4d2912c2f8e6d617917a`，105 个文件、16288 行新增、592 行删除
- 上一轮报告：[第 3 轮问题发现报告](003-final-review.md)
- 本轮职责：同一 finding owner 仅复核 F-006 的闭环状态；本轮不承担最终放行。

## 问题闭环

| 编号 | 状态 | 闭环证据 |
| --- | --- | --- |
| F-006 | 已关闭 | `synced` 将 external resolution file/raw bytes/digest 的 lease 转交 Phase 0；`prepare-task` 的 planner、issue、worktree 与 task mutation guards 始终重验同一 lease；confirmation pending 保留 lease，task-created、blocked、aborted、superseded 与 standalone 终态释放；result evidence 在 validator 成功或失败路径均消费并清理；throwaway 已覆盖真实 `synced -> prepare-task -> release` 与零残留。 |

Runtime 安全边界：

1. `guru_team_trellis.py:3348` 校验 absolute、repo-external、component/symlink 与 regular-file 边界。
2. `guru_team_trellis.py:3479` 在 cleanup 前重验类型与 exact raw bytes，并在删除后确认零残留。
3. `guru_team_trellis.py:3497` 将 release 绑定 canonical resolution 与 expected digest，返回 `released` 或 `already_released`。
4. `guru_team_trellis.py:3604` 的 CLI dispatch 拒绝冲突参数；`:3659` 的 result validator 通过 `finally` 保证验证失败时也清理 result evidence。
5. `prepare-task` 在 `:9849`、`:9942`、`:9992`、`:10087` 对初始读取、GitHub issue、worktree 与 task mutation 逐级重验；digest、source provenance 或 raw-byte drift 均在副作用前 fail closed。
6. `workflow.md:603`、`:635`、`:651`、`:663`、`:717`、`:783` 覆盖 lease transfer、blocked release、confirmation pending retain、prepare 终态 release、task-created release 与 planning handoff。

## Findings

- `findings_count=0`
- P0：0
- P1：0
- P2：0
- P3：0

未发现新的当前范围缺陷，F-006 已完全关闭。

## 验证证据

- 本轮独立只读复验通过：BaseSync runtime 13 项、prepare planner/issue/worktree/task guard 4 项、`guru-sync-base` package contract 5 项、source/distribution 66 项、preset installer 36 项，共 124 项。
- Fresh `phase2-check.json` 另记录 Runtime 290、Skill packages 66、Package contract 5、Preset 36，共 397 项通过，`findings_count=0`。
- Throwaway 覆盖 fresh marketplace discovery/preset install、standalone resolve/execute/validate/release、workflow resolve/execute/validate、真实 `synced -> prepare-task` planner、worktree mutation guard、重复 `already_released`、`trellis update`、workflow/preset reapply、零 resolution/result evidence 与零 `.new`/`.bak`。
- 六份 canonical/installed/Agents/Codex/Cursor/Claude Skill package 的 8 个文件 blob 与 executable mode 一致；canonical/installed runtime、wrappers 与 workflow byte-identical。
- Source/installed package validation 与 dogfood overlay drift 通过。
- Planning 三文档 SHA、schema 1.2 planning approval、Phase 2 SHA 与 commit plan 003 一致。
- Commit `2def8b7` 的 parent、message bytes、52 个 exact paths、tree `b03a137e43e8252a537dbe2d29f959dca8f336f9` 匹配，`hook_mutation=false`。
- Source checkout 干净；task worktree 未提交内容仅为 task-local commit/review/assignment metadata。

## Docs SSOT

- 状态与策略：`partial_docs + ssot_first`。
- Resolution lease 生命周期已同步到 requirements、spec、workflow、Skill contract、README、runtime/tests、平台副本与 throwaway acceptance。
- Canonical、dogfood、installed 与平台副本的合同和字节证据一致。
- 结论：Docs SSOT 通过，无 current-scope inconsistency。

## 开箱即用与 Upgrade/Update

- Fresh install、standalone/workflow 两类入口、真实 `synced -> prepare-task -> release`、workflow preview/switch、`trellis update` 与 preset reapply 均已验证。
- 安装与升级后无 `.new`、`.bak`、conflict、removal 或 base-sync evidence residue。
- 当前分支尚未 push，真实 branch-pinned remote marketplace verification 保持 publish gate pending；本轮只验证公开 marketplace 发现与当前本地分支样本，不能替代 push 后门禁。

## Issue、部署与安全

- Issue scope：关闭 `#110`，关联 `#98`，后续 `#111`；三者当前均为 OPEN。
- 未修改 CI/CD、Docker/Compose、Kubernetes/Kustomize/Helm、数据库 migration/schema 或 Makefile。
- 运行影响限于 Phase 0 selected-base sync 与 resolution/result evidence 的受控 lease、重验和释放。
- 敏感信息扫描无命中；repo、task 与 throwaway 均无 base-sync evidence 残留。

## 观察项

1. 真实远端 branch-pinned marketplace verification 尚未执行，属于 push 后 publish 门禁。
2. `issue-scope-ledger.json.acceptance_evidence` 仍需在 publish 前绑定最终 Branch Review 验收证据。

## 后续候选

1. 保持 `#111` 为独立 follow-up，不在 `#110` 内实现或关闭。

## 结论

HEAD `2def8b748dae986e6f9e4d2912c2f8e6d617917a` 上 F-006 已闭环，本轮 `findings_count=0`，`reuse_decision=reuse-for-closure`。下一步必须派发从未参与任何 earlier review round 的全新 `最终放行审查代理`，对同一 HEAD 的完整 `origin/main...HEAD` diff 进行最终放行审查；本报告不构成最终放行。
