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
| focused installed lifecycle A/B | 1/1 PASS | local deterministic installed lifecycle |
| upgrade contract | 18/18 PASS | exact version/matrix/reapply/migration contract |
| managed Python routing | 44/44 PASS | declared caller graph |
| Python compile / `git diff --check` | PASS | syntax/whitespace only |
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
| capability / installed projection | 6 | no blocking loss |
| installed Phase 0/workspace/closeout | 6 | PASS |

Current-head dual PATH-runtime run 的稳定 matrix SHA-256：
`660422848f6efba9f1c3c6fcf2d9d23a1e8b710af8ffd10bf0f12e0954910f49`。
无 dependency PATH Python 与 bootstrap-only poison PATH Python 两轮均为 6/6 PASS；
其 wrapper `summary_sha256` 分别是
`45bd2fd58a83d1ec959cb5ac4bc8fb90786c00c86c635e605e12e6a32f3ae414` 与
`ad70ec34c90c6a24cacaf57f6effbfd15b62032902cba2172b32fec368185a92`，
差异来自临时 A/B fixture commit identity，不代表 capability 或 matrix 语义漂移。
source commit=`5c059f4943edad7dfe25182a78af94759d41f9a1`，target CLI=`0.6.15`，
extension=`0.6.5-guru.37`。workflow evidence 是 `public_plus_local_candidate`；
这不是已发布 `.37` tag proof。

## A/B business-task compatibility

- A=`workspace_mode=worktree` / `finish_entry=github_pr`；B=`current` / `none`。
- local matrix Planning、Phase 2、Branch Review、Publication、fixture-local acceptance、
  Finish/archive、A provider failure、B Finish failure 与 cleanup failure recovery 全部通过。
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
- promotion 前的原始 matrix summary SHA-256
  `1801f7301f6ceaea1d1cef795822b52cf031a456f76196ae1f4ac80d7f65c633`
  仍只作为先前 run identity保留；它与 current-head rerun都保持
  `real_github_verified:false`，不替代后续独立真实 GitHub A evidence。

Phase 2 `guru-check-task`、reviewed commit、独立 Branch Review 与 Publication/Finalizer
仍须绑定最终完整 diff后执行；此前证据不替代这些 gate。
