# PLAN

| 顺序 | Issue | 已知目的 | 状态语义 |
| --- | --- | --- | --- |
| completed predecessors | #264 -> #263 -> #265 -> #266 -> #275 -> #260 -> #285 | 建立三项 SSOT package、激活 current authority、完成 replacement release/compatibility 与 merge message contract | `source_confirmed` closed/merged；已完成项不因本 baseline 重开 |
| completed current baseline | #283 -> #290 -> #295 | Architecture 单向收敛、detached base authority、Sync/Discovery public handoff 与 reviewed promotion | implementation/review/promotion 已进入 current `.40` authority；不替代重构前 Release gate |
| #311 post-promotion closure | #311 | installed Finalizer source/target separation 与 verifier failure evidence 已进入 `.41` current | promotion-created diff 仍需 fresh Phase 2/commit/Branch Review，随后复用现有 fixture、Publication/Finalizer、PR/merge、生产发布与错误文件重试；Issue OPEN |
| current release | 独立的重构前稳定版 Release Issue | 冻结旧 graph，发布 `v0.6.15-guru.1` / extension `.37` / Trellis `0.6.15`，完成 exact-candidate matrix、tag-pinned install 与 post-publish smoke | Issue 创建前未授权执行；tag/Release/smoke 均为 `unverified` |
| post-stable refactor | #247 -> #249 -> #250 -> #292 -> #293 -> #261 -> #248 -> #252 -> #267 | Phase/owner 解耦、Intake、Planning、Publication、Acceptance/Finish、cleanup 与最终重构版 Release | TARGET/PLAN 候选参考；不作为重构前 Release 的前置、owner 或验收范围 |

PLAN 记录依赖与 owner，不证明 outcome，也不改变各 Issue 的 live authority。
