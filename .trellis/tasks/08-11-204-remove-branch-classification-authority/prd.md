# #204 移除分支分类与 GitHub Rules 操作限制

## Goal

移除 Guru Team 在 commit、push、PR 与 merge 前对分支类型、发布状态和 GitHub Branch Rules 的资格判定，让当前对话中的精确操作请求成为副作用 authority，同时保留 repo、remote、target ref、HEAD、scope、内容和 freshness 的一致性门禁。

## Background

- 当前 `guru-create-task-commit` 为构造 `routine_auto_commit_facts` 调用 GitHub `/rules/branches/{branch}`。私有仓库在套餐不支持该 API 时返回 HTTP 403，导致本地 commit 被错误阻断。
- 该资格矩阵来自 Issue #180，完整包含 dedicated、default、protected、shared、other-task、remote branch 与 Open PR 分类事实；Issue #204 明确取代 Issue #180 的 routine auto-commit 资格设计。
- 用户未指定其它路径时，标准 Guru Team workflow 创建专用 task branch/worktree；该条件路由不是操作资格证明。

## Requirements

### R1 删除错误的资格层

- 从 `guru-create-task-commit` 候选、合同、Schema、examples、runtime、eval 和 tests 中删除 `routine_auto_commit_facts`、`routine_auto_commit_eligible` 及其全部资格事实。
- 必须删除 `dedicated_task_branch`、`default_branch_excluded`、`protected_branch_excluded`、`shared_branch_excluded`、`other_task_branch_excluded`。
- 同时删除仅服务于该资格矩阵的 remote branch、Open PR、worktree ownership 和 Branch Rules 查询，不以改名、三态、别名或语义结论重新引入。

### R2 当前请求拥有操作 authority

- 用户精确请求 commit、push、创建/更新 PR 或 merge 到指定目标时，Guru 不按分支名称、角色、保护状态、共享状态、task ownership 或发布状态自行否决。
- 没有当前精确请求时，不得自行执行上述副作用；用户授权只存在于当前对话，不写入 artifact、runtime、checkpoint、schema 或 DTO。
- GitHub 实际拒绝远端 mutation 时返回真实 blocked/recovery，不预读 Rules API，也不增加绕过逻辑。

### R3 保留正确性门禁

- commit 继续校验 task/HEAD、Phase 2 freshness、完整 snapshot、精确 staging、message、scope、Git operation state 和 unrelated preservation。
- push 继续校验 repo、remote、target ref、expected HEAD 和精确 push 动作。
- PR 继续校验 repo、base/head、diff、Issue scope、payload 和 publication 请求。
- merge 继续校验 PR identity、expected head、mergeability、close scope 和精确 merge 动作。

### R4 版本化迁移

- task commit candidate 从 `guru-task-commit-candidate-4.0` 升级为 `guru-task-commit-candidate-5.0`，Schema、example、interface、runtime validator 与文档同时切换。
- 未完成的 4.0 owner-private candidate 不转换、不补造旧事实；进入 task commit 时删除/拒绝旧候选并从当前 Phase 2 evidence 完整 reprepare。
- stable skill id 与 script command 保持不变；迁移不得形成第二条执行路径。

### R5 canonical 与安装副本一致

- canonical runtime/package/docs/tests 是修改源；通过 preset apply 同步 `.trellis/guru-team/`、`.agents/skills/`、`.codex/skills/`、`.claude/skills/`、`.cursor/skills/`。
- throwaway 安装、upgrade/update 漂移、Codex/Claude/Cursor 一致性与 README 命令必须验证。

## Acceptance Criteria

- [ ] 全仓非历史归档中不存在五个已废弃字段、`routine_auto_commit_facts`、`routine_auto_commit_eligible` 或 `/rules/branches/` 前置读取。
- [ ] 标准 task branch 与用户指定任意目标 ref 的 commit 前置判断均不依赖 Branch Rules、分支分类、remote branch 或 PR 状态资格矩阵。
- [ ] Rules API 403/不可用不会参与本地 commit、push、PR 或 merge 的前置流程。
- [ ] repo/ref/HEAD/scope/content/freshness mismatch 仍 fail closed，远端真实 mutation 拒绝仍被准确报告。
- [ ] 4.0 candidate 明确迁移为完整 reprepare，5.0 candidate 不包含授权或分支资格事实。
- [ ] canonical、dogfood、preset、platform copies、schema、examples、eval、tests 与中文文档同步。
- [ ] targeted tests、完整 runtime/preset tests、clean throwaway install、overlay drift、upgrade/update 门禁通过。
- [ ] 独立 current-HEAD semantic review 无未关闭 P0-P3 finding。

## Out Of Scope

- 修改 GitHub 仓库 Branch Rules、Ruleset、权限或套餐。
- 承诺 GitHub 必然接受 push、PR 或 merge。
- 削弱 secret redaction、精确目标核对、scope/staging/HEAD freshness 或无关改动保护。
- 引入恶意篡改、并发锁、TOCTOU 或其它非 Issue 正文要求的加固。

## Open Questions

无。Issue #204 与当前代码、合同和 Issue #180 历史已覆盖所有 load-bearing 决策。
