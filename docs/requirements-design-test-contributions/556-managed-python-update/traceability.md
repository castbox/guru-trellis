# #556 双向追踪

状态：reviewed_delta；delta_first；前像 RDT `.94/active`，继承 Architecture `.89/active`。唯一需求正文见 [requirements](./requirements.md)，职责见 [design](./design.md)，实际结果与边界见 [test](./test.md)。首次完整 committed 独立 Review 后由原 RDT owner 判断必要 promotion；新差异重新进入原 gates。

| Requirement / behavior | Design / contract | Test | Source |
| --- | --- | --- | --- |
| R556-01 / BEH556-SELECT | D556-01 | T556-01/04 | #556 目标1 |
| R556-02 / BEH556-ADMIT | D556-02 | T556-02/03 | #556 目标2 |
| R556-03 / BEH556-IDENTITY | D556-02/03 | T556-02/03/05 | #556 目标3、验收 |
| R556-04 / BEH556-ACTIVATE | D556-03 | T556-03/04/05 | #556 目标3、验收 |
| R556-05 / BEH556-DIAGNOSE | D556-04 | T556-01/03 | #556 目标4 |
| R556-06 / BEH556-DISTRIBUTE | D556-05 | T556-04/05/06 | #556 目标5、边界 |
| R556-07 / BEH556-EVIDENCE | D556-03/05 | T556-01..06 | #556 验收、边界 |
