# #557 双向 Trace

状态：reviewed_promoted；RDT .96 / Architecture .90。来源承诺 matrix 保留于 design.md 所链的不可变 task design；当前行为只由 canonical 合同定义，实际结果只由 test.md 拥有。

| Requirement / behavior | Design | Test strategy and cases |
| --- | --- | --- |
| R557-01/02，BEH-557-01 | DES-557-01，D557-01/02 | T557-01/03；test_manual_recovery：wrong_pr_selection_and_ambiguous_publication、unmerged_and_base_mismatch。 |
| R557-03/04/05，BEH-557-02 | DES-557-02，D557-03 | T557-02/04；all_ci_states、completion_fixtures、actual_head_extra_path。 |
| R557-06/07，BEH-557-03 | DES-557-03，D557-04 | T557-05；base_advance_branch_deletion、public_projection_failure、recorded_manual_fact/query2；test_history的bookkeeping/schema1/2。 |
| R557-08/09，BEH-557-04 | DES-557-04，D557-05 | T557-06/07/08；test_runtime/test_delivery_migration/test_contract；matching clean/reapply/installed公开wrapper与真实GitHub链。 |

每个新增profile/schema由原Merge invoke直接消费，query2由原history读取消费，
delivered输出沿既有Completion seed消费。Test fixtures仅模拟语义/provider，
不能替代独立Architecture、Phase2/完整BranchReview或实际外部证据。
