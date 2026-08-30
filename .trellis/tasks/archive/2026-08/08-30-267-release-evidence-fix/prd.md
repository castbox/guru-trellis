# #267 post-merge lifecycle authority evidence 修复需求

## Authority

唯一 current requirement authority 是 live Issue #267 body
`2026-08-30-r19`。本 recovery task 只处理 PR #315 合并后完整候选审查产生的
`BR-267-FULL-CAND-001`。旧 task、旧 Branch Review 和历史评论只提供事实背景，
不拥有本任务范围。

当前 base 固定为：

- repository：`castbox/guru-trellis`；
- `main` / `origin/main` / task base：
  `a41b8a34d237e1863225d069ca9c6b5ad6ae476a`；
- PR #315 merge commit：`a41b8a34d237e1863225d069ca9c6b5ad6ae476a`；
- target Release identity：`v0.6.15-guru.3`；
- extension revision：`0.6.15-guru.39`；
- Trellis CLI：`0.6.15`。

## Goal

修复 current Architecture 与 Test authority 对已完成 lifecycle 的过期表述，使其准确记录
promotion、r19、task commit、independent Branch Review、PR readiness、Finalizer 和
PR #315 merge 已完成，同时保持本 recovery fix 合并、fresh exact-candidate review、
十三项 pre-tag gates、tag、smoke、GitHub Release 与发布后 #311 业务验证为未完成状态。

## Accepted Scope

只修改以下两个 current authority 文件：

- `docs/architecture/evidence/current-evidence.md`；
- `docs/test/versions/current-main-0.6.5-guru.42/test-plan.md`。

两处修改必须表达同一 lifecycle：

```text
3efcce72 -> d3dca74b -> 351e61d1 -> 490b302a -> 9ceeede2
-> PR #315 merge a41b8a34
-> BR-267-FULL-CAND-001
-> recovery fix commit / review / merge pending
-> exact-candidate Release gates pending
```

## Required Boundaries

- `.trellis/tasks/archive/**` 字节保持不变。
- 不修改 Requirements、Design、Test、Architecture 的版本 identity、状态或历史正文。
- 不修改产品行为、公共 Skill API、runtime、schema、manifest、projection 或安装逻辑。
- 不修改 CI/CD、container、Kubernetes、database migration、Makefile、依赖或部署配置。
- 本 task commit 与 PR body 只使用 `Refs #267`，不关闭 #267、#311 或 #312。
- #311 在正式 `.3` 业务仓原失败路径与错误文件重试通过前保持 OPEN。
- 本 task 不创建 tag、GitHub Release，不执行 Issue closure，不清理旧 release worktree。

## Acceptance

1. Git dirty path 集合由本 task 文件和两个 accepted authority 文件组成，目标实现 diff
   只包含上述两个 authority 文件。
2. 两个 authority 文件不再将 PR #315 之前已完成的 lifecycle 写为 `pending`。
3. 两个 authority 文件明确阻断 recovery fix merge 前的 tag，并保留 exact-candidate
   Release gates 与 #311 post-release proof 为 `unverified`。
4. archived `implement.md` 与 `HEAD` blob identity 完全相同。
5. `git diff --check`、Markdown link、YAML/JSON parse、唯一 active `.42` scan 通过。
6. preset suite `81/81`、canonical verifier `17/17`、installed verifier `17/17` 通过。
7. `5b3b7bef73824ae78b8bf13a20cfd9ba01acb2b8`、
   `21c7da14798683193b460a5e7c5bd24c7c517804`、
   `3efcce72a0d47e38ec725aa8c0f8498992f3416f` 均为最终 recovery commit 的祖先。
8. Fresh Phase 2 与 committed full-range Branch Review 均无未关闭 P0-P3 finding，才进入
   push/PR 副作用计划。
