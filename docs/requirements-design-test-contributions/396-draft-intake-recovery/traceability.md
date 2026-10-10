# #396 双向 trace

| Requirement / behavior | Design owner | Test |
| --- | --- | --- |
| R396-01 / BEH396-CHAIN | D396-01, D396-02, D396-03 | T396-01 |
| R396-02 / BEH396-IDENTITY | D396-01, D396-02 | T396-01, T396-02 |
| R396-03 / BEH396-AUTHOR | D396-01, D396-02 | T396-01 |
| R396-04 / BEH396-MISTAKES | D396-02, D396-03 | T396-02 |
| R396-05 / BEH396-RECOVER | D396-02, D396-03, D396-04 | T396-02, T396-04 |
| R396-06 / BEH396-REFRESH | D396-02, D396-03, D396-04 | T396-03, T396-04 |
| R396-07 / BEH396-AGENT | D396-04 | T396-04 |
| R396-08 / BEH396-DISTRIBUTE | D396-05 | T396-05 |
| R396-09 / BEH396-CAUSE | D396-01..04 | T396-01..04 |
| R396-10 / BEH396-CLOSE | 原 lifecycle owners | T396-06 |

[requirements](requirements.md)、[design](design.md)、[test](test.md)分别拥有本层内容。当前 RDT .83/predecessor .82 与 public Architecture .82/active 从 manifest 引用；没有 Architecture contribution/ADR。结果不复制到本 trace；后续晋升形成新 diff 时重新执行完整 current gates。
