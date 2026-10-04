# #490 reference-only 与官方来源 adoption contribution

Identity：`architecture-contribution-490-reference-only-adoption-v1`；state：`implementation_candidate`；task：`.trellis/tasks/10-04-490-reference-only-adoption`；source：castbox/guru-trellis#490；expected current：`current-main-0.6.17-guru.70`。绑定 `guru-maintain-architecture-baseline:2.0`、`guru-trellis-architecture-change-contract-v1`、current `guru-trellis-design-constitution-v1`。change path 为 `target_native`；不改变 ADR-015 的 Fork/Guru ownership 和 ADR-009 的 source/closure ownership，无新 ADR。

## Required concerns

| Concern | Applicability 与判断 |
| --- | --- |
| authority-binding | applicable：当前 .70 为 shared authority，#490 为 requirement，task 三份规划为本次行为设计。 |
| constitution-binding | applicable：命中 mature-practice-applicability、concept-semantic-completeness、cohesion-change-isolation、minimum-necessary-complexity；正常官方生成、既有 source 概念与单 writer，无原则例外。 |
| boundary-and-decision | applicable：已有 C6 接受 reference_only，并采用 #25 合并 source；source pin 更新属于当前已受测边界，不改变全局 lifecycle phase。 |
| owner-and-single-writer | applicable：现有 Guru creator 管理 invocation，上游 task.py 唯一写 task.json；session/branch/resource/closure owner 不变；本 task 写 contribution，Architecture owner 独占 shared promotion。 |
| compatibility-and-exit | applicable：additive enum，exact_source/no_issue 保持；不新增 legacy runtime，旧档案只读诊断不迁移；旧 0.6.17 仍拒绝 update。 |
| gap-and-deviation | applicable：修复 C6 对支持 disposition 的拒绝和 source 未采用差异；不宣称完整 Release matrix 已通过，不关闭其它 GAP、不复活已关闭 GAP。 |
| parallel-scope | applicable：允许本 task 的 source/schema/tests/managed projection/独立 contribution；禁止与 #489 竞争 Stage 1、tag、Release 或 shared authority promotion。 |
| evidence-and-freshness | applicable：before 为旧 const 和 64fe9a15 source；after 需正式创建/recovery、现有 lifecycle 回归、真实 source checker、官方投影、一个 clean install/update/reapply；每个 gate 绑定当前候选。 |
| review-and-promotion | applicable：Phase 2 后完整 committed diff 独立 review，再 expected-current-bound promotion 至 .71；promotion diff 重新 check/commit/review。 |

## Project check 与未验证边界

`guru-trellis-architecture-convergence:repository:1` 在 planning 适用且 blocking。规划 review pass：九项 concerns 完整，target_native 唯一路径，owner 和单 writer 未扩大，没有额外状态、双读或无退出兼容机制。此结论只证明规划满足 current contract，不证明实现或安装。

实现证据：正式 create-task/recovery/source identity fixture 16/16、current lifecycle 152/152、Closure 18/18 与 dogfood 9/9 已通过；source checker 核验真实 Fork identity、main CI 与 183 个官方文件，canonical/source、installed、Claude/Codex/Cursor projection、ownership 与 drift 均通过。一个代表性 Codex focused clean install、同候选双次 update/reapply、session binding 与零 sidecar 已通过；该次使用 local marketplace sample，native load 为 projection parity。独立 committed review 和 promotion 仍是后续必需门禁。完整发布矩阵、predecessor 拒绝无写证明、public marketplace/tag smoke/Release 由 #489 继续；本 contribution 不把上游已通过 CI 等同于 Guru release proof。
