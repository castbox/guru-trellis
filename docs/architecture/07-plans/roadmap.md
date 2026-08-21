# PLAN

| 顺序 | Issue | 已知目的 | 状态语义 |
| --- | --- | --- | --- |
| completed predecessors | #264 -> #263 -> #265 -> #266 -> #275 -> #260 -> #285 | 建立三项 SSOT package、激活 current authority、完成 replacement release/compatibility 与 merge message contract | `source_confirmed` closed/merged；已完成项不因本 baseline 重开 |
| current | #283 | Architecture 单向收敛、三类路径、设计宪法/project-check consumption 与 reviewed promotion | implementation/review 已完成；promotion 后 gates 进行中 |
| next | #290 -> #267 | 严格串行完成后续 live Issue，再由 #267 执行 `.37` exact merged-main stable tag/Release 与 tag-pinned smoke | 未开始、未授权；#283 不提前执行 |
| post-stable refactor | #247 -> #249 -> #250 -> #261 -> #248 -> #252 | Phase/owner 解耦、Intake、Publication、Acceptance/Finish 与 cleanup 重构 | TARGET/PLAN；未开始、未授权 |

PLAN 记录依赖与 owner，不证明 outcome，也不改变各 Issue 的 live authority。
