# PLAN

| 顺序 | Issue | 已知目的 | 状态语义 |
| --- | --- | --- | --- |
| completed predecessors | #264 -> #263 -> #265 -> #266 -> #275 -> #260 -> #285 | 建立三项 SSOT package、激活 current authority、完成 replacement release/compatibility 与 merge message contract | `source_confirmed` closed/merged；已完成项不因本 baseline 重开 |
| completed current baseline | #283 -> #290 -> #295 | Architecture 单向收敛、detached base authority、Sync/Discovery public handoff 与 reviewed promotion | implementation/review/promotion 已进入 current `.40` authority；不替代重构前 Release gate |
| #311 completed prerequisite | #311 | installed Finalizer source/target separation 与 verifier failure evidence 已进入 current authority | Issue 已按独立 scope 完成；正式 release 安装态业务仓验收由 #332 exact-candidate Release Gate fresh 承接 |
| current release | #332 | 发布 `v0.6.15-guru.5` / extension `.40` / Trellis `0.6.15`，在 preparation PR 合并后冻结 fresh `origin/main` exact candidate，完成 Issue 要求的 Release Gate、tag-pinned install 与 post-publish smoke | Issue OPEN；Architecture/RDT `.44` 已修订提升并承接 #240/#348 reviewed authority；promotion-created diff 的 fresh Phase 2/commit/Branch Review 尚未完成；tag/Release/smoke 均为 `unverified` |
| post-stable refactor | #247 -> #249 -> #250 -> #292 -> #293 -> #261 -> #248 -> #252 -> #267 | Phase/owner 解耦、Intake、Planning、Publication、Acceptance/Finish、cleanup 与最终重构版 Release | TARGET/PLAN 候选参考；不作为重构前 Release 的前置、owner 或验收范围 |

PLAN 记录依赖与 owner，不证明 outcome，也不改变各 Issue 的 live authority。
