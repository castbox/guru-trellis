# #530 双向 trace

| Requirement / behavior | Design responsibility / contract | Test |
| --- | --- | --- |
| R530-01 / BEH530-CONTINUE | D530-01/03/05 / CON530-ENTRY/PROJECT/REVIEW | T530-01 |
| R530-02 / BEH530-IDENTITY | D530-02/03 / CON530-CHECK/PROJECT | T530-01/03 |
| R530-03 / BEH530-READONLY | D530-01/03 / CON530-ENTRY/PROJECT | T530-05 |
| R530-04 / BEH530-RECOVER | D530-01/04 / CON530-ENTRY/RECOVER | T530-02/03/04 |
| R530-05 / BEH530-FULLREVIEW | D530-05 / CON530-REVIEW | T530-01/04 |
| R530-06 / BEH530-DISTRIBUTE | D530-06 / CON530-INSTALL | T530-06 |

Implementation locators: `trellis/skills/guru-team/packages/guru-create-task-commit/`, `guru-review-branch/references/contract.md`, `guru-reconcile-task-base/references/contract.md`, `trellis/workflows/guru-team/workflow.md`。具体结果只由 [test.md](test.md)持有；架构 contribution 独立持有 concerns/expected-current/promotion，不重复测试结论。
