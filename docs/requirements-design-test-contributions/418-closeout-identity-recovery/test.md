# #418 Test Contribution

状态：draft、unpromoted；证据分层沿用 TST-002/003/004/005/011/012/018。不能将局部unit通过声明为全链或release通过。

| Case | 证据与精确期望 |
| --- | --- |
| T418-01..03 | 正常producer/archive生成双端mapping；精确重入不重复Git/PR副作用，missing/conflict明确阻塞 |
| T418-04 | 真实Merge wrappers保持known/provider/stale诊断与redaction；未知异常仍internal_error |
| T418-05/08 | 正常archive fixture经实际四owner wrappers产生真实DTO，最终Merge preview成功；正常checkpoint退休不增加复审 |
| T418-06/09 | H/A分离、完整archive continuity、真正内容或authority变化阻塞；task/archive/refs/PR零mutation |
| T418-07 | source/installed/Shared/Codex/Claude/Cursor、reapply/drift、sidecar与executable mode一致 |
| T418-10 | title/body snapshot不能冒充Publication；新完整语义审查后的实际bytes才进入Finalizer |
| T418-11 | 原active profiles、status、锚点及旧成功/失败出口不回归 |
| T418-12 | 三个独立Architecture阶段只能current/blocked；写入route和stage错配在边界拒绝 |
| T418-13 | 只读Publication如实保留finding分类，不能将内容问题伪装为external blocker |
| T418-14 | B正常推进到B'或PRtitle/body改变后，下游拒绝旧范围/快照；不后台更新ref |

本轮在 `78651e20` 基线复跑：Finalizer 108、Merge 65、Branch Review 35、Publication 67、Architecture 26项通过；`test_archived_review_integration.py` 3项通过；`test_archived_fixtures.py` 3项通过（8个recipe）。实际source/installed/reapply/drift验证通过，保留Claude/Codex/Cursor与Shared投影，sidecar为0。task implement.md记录精确命令和区分的历史结果。

当前未证明：fresh native语义执行、原业务实例和Release Gate；尚无独立committed-diff review/promotion。Fake provider只隔离transport；fixture owner inputs不是native AI语义执行证据。完整release矩阵由专门owner负责。
