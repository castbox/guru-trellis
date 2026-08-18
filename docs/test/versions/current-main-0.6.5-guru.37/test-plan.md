# 当前测试计划与证据

版本：`current-main-0.6.5-guru.37`；状态：`active`；source baseline：main
`5c059f4943edad7dfe25182a78af94759d41f9a1` + #260 compatibility task delta。

## Replacement before-state authority

- Issue #275：CLOSED/COMPLETED；PR #282 rebase-merged。
- annotated tag：`v0.6.5-guru.10`；tag object
  `b5fd47e9dc45ca4d6950f87f38d495776ce676ce`；peeled commit
  `5c059f4943edad7dfe25182a78af94759d41f9a1`。
- GitHub Release：non-draft、non-prerelease、zero assets；extension
  `0.6.5-guru.36`，official Trellis `0.6.5`。
- 该 release 是 existing cells 的 immutable before-state，不是 `.37` target release。

## #260 focused implementation evidence

| Check | Result | Boundary |
| --- | --- | --- |
| focused installed lifecycle A/B | 1/1 PASS | local deterministic installed lifecycle；A archive 后 history query 返回唯一 `PR #301` finish-summary candidate |
| upgrade contract | 20/20 PASS | exact version/matrix/reapply/migration/source-binding contract |
| preset / ownership unit suite | 83/83 PASS | installer、installed manifest、ownership、mode 与 reapply contract |
| managed Python routing | 44/44 PASS | declared caller graph |
| Python compile | PASS | affected Python syntax only |
| package/runtime installed profiles | PASS | RDT 6 cases/4 profiles；Architecture 4/4；Bootstrap 4 cases/3 profiles |

## Full six-cell compatibility matrix

live-derived platforms：`claude`、`codex`、`cursor`。每个平台使用独立 repo、npm
prefix 与 runtime，分别执行 clean `0.6.15` 和 existing `0.6.5 -> 0.6.15`：

| Cell family | Count | Result |
| --- | --- | --- |
| clean official `0.6.15` + current preset | 3 | 3/3 PASS |
| existing `v0.6.5-guru.10` + official migration + reapply | 3 | 3/3 PASS |
| final recursive `.new/.bak` | 6 | all `0` |
| template hash unknown drift | 6 | all `0` |
| candidate source binding | 1 | HEAD、tracked delta、untracked path/mode/content 与 isolated-index candidate tree 形成单一 `source_state`；run 前后 identity 相同 |
| capability / installed projection | 6 | Skill package、ordinary managed asset、overlay executable mode 保持；extension identity 独立于 version field 比较，无 blocking loss |
| Docs authority | 6 | recursive `docs/**` 全文件 hash 保持，Requirements/Design/Test/Architecture 均含 versioned body |
| installed Phase 0/workspace/closeout | 6 | PASS |
| post-archive history discovery | 1 | A archive 后返回唯一 non-empty `PR #301` candidate，locator 指向该 task 的 `finish-summary.json` |

最终 dirty candidate 使用 source HEAD
`868fada5f6296cca6c58ed725946b870865b1e0c`，target CLI=`0.6.15`，
extension=`0.6.5-guru.37`。精确 `source_state.candidate_tree`、source identity 与
matrix digest 由最终只读 run 输出绑定；它们不写回 tracked 文档，避免文档修改让
candidate tree 自引用失效。workflow evidence 是 `public_plus_local_candidate`；这不是
已发布 `.37` tag proof。

## A/B business-task compatibility

- A=`workspace_mode=worktree` / `finish_entry=github_pr`；B=`current` / `none`。
- local matrix Planning、Phase 2、Branch Review、Publication、fixture-local acceptance、
  Finish/archive、A provider failure、B Finish failure 与 cleanup failure recovery 全部通过。
- A archive 完成后，installed history preview 对非空 query 返回唯一 `PR #301`
  candidate，并精确指向该 archive 的 `finish-summary.json`。
- 两种 merge order均通过，tracked Guru metadata intersection=`[]`，B GitHub PR call
  count=`0`，workspace journal存在但不 tracked。
- cleanup 后 protected work/archive/Finish commits 对 retained refs 仍可达。

真实 GitHub A route 在单独确认后完成：private disposable repo PR #2 从 source head
`6a7b721adfd8a70be9cc56883bf5e2b2133fdf84` expected-head rebase merge为
`a5c73c49ca38e593e11bafb62a2f142ca208f97f`；Issue #1 于 merge 后一秒 CLOSED/COMPLETED。
首次 provider failure 分类 `github_api_unavailable`，同一 Finalizer transaction恢复；
remote branch 与 disposable repository 已删除，本地 scenario resources移动到 Trash且可恢复，
删除远端后 retained-ref reachability 已重验。

## Current boundaries

- `.37` stable tag、GitHub Release、tag-pinned clean install与 release smoke：`unverified`，owner=#267。
- #248 Acceptance/Finish handoff 与 #252 cleanup public owner未实现；本次只提供可消费兼容事实。
- full matrix logs、临时 repository/runtime、用户授权与完整 hash bundle不进入 current SSOT。
- #263/#264/#265 semantic contracts未在 #260 重写；已知 #264 Skill wording混入 selector
  保持 pre-existing owner defect，不由本任务修复。
- 所有 matrix run 都保持 `real_github_verified:false`；最终 candidate 的精确
  source/matrix identity 只保留在 runtime/conversation evidence，不替代独立真实
  GitHub A evidence。

Phase 2 `guru-check-task`、reviewed commit、独立 Branch Review 与 Publication/Finalizer
仍须绑定最终完整 diff后执行；此前证据不替代这些 gate。
