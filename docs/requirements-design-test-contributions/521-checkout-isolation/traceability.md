# #521 双向 trace

| Requirement / behavior | Design responsibility / contract | Test |
| --- | --- | --- |
| R521-01 / BEH521-FACTS | D521-01/02 / CON521-PREWRITE/CALLER | T521-01/02/04/05 |
| R521-02 / BEH521-ISOLATE | D521-01/03 / CON521-PREWRITE/C6 | T521-01/02/05 |
| R521-03 / BEH521-NO-TASK | D521-01/02 / CON521-PREWRITE/CALLER | T521-01/03/04 |
| R521-04 / BEH521-CONTINUE | D521-02 / CON521-CALLER | T521-03 |
| R521-05 / BEH521-BINDING | D521-01/02 / CON521-PREWRITE/CALLER | T521-04 |
| R521-06 / BEH521-PRESERVE | D521-01/04 / CON521-PREWRITE/EVOLUTION | T521-05/06 |
| R521-07 / BEH521-EVOLVE | D521-04 / CON521-EVOLUTION | T521-06/08 |
| R521-08 / BEH521-CREATE | D521-03/05 / CON521-C6/DISTRIBUTE | T521-01/07/08 |
| R521-09 / BEH521-EVIDENCE | D521-02/05 / CON521-CALLER/DISTRIBUTE | T521-03/06/07/08 |

Requirements/Design/Test 各层由本目录的[requirements](requirements.md)、[design](design.md)、[test](test.md)拥有。manifest 绑定晋升 preimage RDT .84、新 current .85 和 Architecture .84；本 contribution 已晋升，晋升差额仍须 fresh Phase2/TaskCommit/独立完整 Branch Review。必要ADR与九concern由Architecture contribution拥有，不复制第二authority。

