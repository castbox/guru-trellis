# Design

## 1. Architecture Boundary

保持现有 `guru-create-task-commit` semantic closed loop 与 stable skill/script id，不新增 wrapper：

```text
current exact commit request
  -> Phase 2 freshness + live task/HEAD/snapshot review
  -> AI semantic candidate review
  -> exact dialogue-local side-effect authority check
  -> candidate 5.0 recorder/checker
  -> isolated commit executor
```

删除位于 semantic review 与 executor 之间的 `routine_auto_commit_*` 资格分支。GitHub Rules、分支类别、remote branch 与 PR presence 不再参与本地 commit 决策。

## 2. Candidate 5.0 Contract

`guru-task-commit-candidate-5.0` 保留：

- task locator、current branch、task status；
- base、pre-commit HEAD、Phase 2 anchor；
- staged/unstaged/untracked/delete/rename/copy/gitlink snapshot；
- path classifications 与 exact stage paths；
- canonical commit message；
- AI review status、summary 与 evidence。

删除：

- `routine_auto_commit_facts`；
- `routine_auto_commit_eligible`；
- dedicated/default/protected/shared/other-task/remote-branch/open-PR 资格事实及其 evidence refs。

Schema 文件路径可保持稳定以便 installer 覆盖旧安装副本，但 `$id`、candidate `schema_version`、runtime 常量、interface objective scope 与迁移文档必须统一升级到 5.0。4.0 输入由 current validator fail closed，并要求完整 reprepare。

## 3. Runtime Changes

- 删除 `task_commit_protected_branch_excluded`、`task_commit_other_task_branch_owners`、`task_commit_remote_branch_absent`、`task_commit_open_pull_request_absent`、`task_commit_objective_eligibility_facts` 和 `task_commit_normalize_routine_eligibility`，前提是全仓调用审计证明它们仅服务旧资格层。
- candidate builder 不再读取 GitHub，也不再遍历其它 task/worktree 来产生操作资格。
- plan checker/executor 只重算 live identity、freshness、snapshot、classification、message/parser 与 index/tree/commit facts。
- public commit DTO 与 stable commands 不变，避免扩大跨 Skill handoff。

## 4. Authority And Confirmation

Skill 文档明确：

- 当前对话已有精确 commit 请求时，semantic gate 后可执行该精确动作；
- 没有精确请求时，在 recorder/executor 前取得一次仅存在于对话中的确认；
- 分支类别、保护状态、shared/other-task 或 published/unpublished 状态不得决定是否询问或是否执行；
- 候选与任何 runtime/checkpoint 均不持久化授权。

push、Publication、Finalizer、PR readiness 与 Merge 做全仓审计；只有发现同类主动资格门禁时才修改。repo、remote、target ref、HEAD、scope、content 与 freshness identity checks 保持原义。

## 5. Docs SSOT Plan

| SSOT | Planned change | Derived copies |
| --- | --- | --- |
| `trellis/skills/guru-team/packages/guru-create-task-commit/` | Skill、contract、interface、schema、example、tests 切换 candidate 5.0 | `.trellis/guru-team/skills/` 与四个平台 skill roots |
| `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py` | 删除资格函数、GitHub Rules read 与 runtime 分支 | `.trellis/guru-team/scripts/python/` |
| `.trellis/spec/workflow/*.md` | 记录 authority、candidate 5.0 与 reprepare 迁移 | preset/workflow README 的用户说明 |
| preset tests / throwaway verifier / eval adapter | 删除 Rules mock 与分类矩阵，改测无 Rules 调用及真实 identity/mutation failure | installed verification |

Canonical 先改，随后运行 `apply.sh --repo .` 同步安装副本，再运行 drift checker。不得手改 generated copy 后反推 canonical。

## 6. Compatibility And Recovery

- 4.0 candidate 是 ignored owner-private 短生命周期状态，不保留兼容执行器。
- 发现旧 candidate 时返回 stable stale/reprepare 结果或由当前入口清理后完整重建；不得把缺失的 5.0 字段投影回旧 candidate。
- 已创建 Git commit、Phase 2 checkpoint、public committed DTO 和后续 Branch Review 接口不变。

## 7. Validation Strategy

- 静态：全仓 banned-term audit、JSON schema validation、Python compile、shell syntax、diff check。
- 单元：candidate 5.0 shape、旧 4.0 拒绝/reprepare、arbitrary branch、identity mismatch、exact staging/unrelated preservation、remote mutation rejection。
- 集成：canonical runtime、package contract、preset apply、installed closeout、production eval。
- 分发：overlay apply/drift、clean throwaway workflow/preset install、upgrade/update 与 Codex/Claude/Cursor copy identity。

## 8. Risk And Rollback

- 最大风险是误删真实 identity/freshness 门禁。实现必须按函数消费者逐个证明“仅服务资格层”后删除。
- 若 candidate 版本、manifest 或 generated copy 漂移，整批回退到同一提交前状态；4.0 runtime 配 5.0 schema 的混合发布必须失败。
