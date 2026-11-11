# #793 双向追踪与替代边界

适用源 Git `e30c7bb5d4c24bc075dc14cfcd04c1da00fcf78e`，authority
`guru-trellis-rdt`，Architecture `guru-trellis-architecture`。
proposed 镜像最终路径，内部相对链接按最终位置解释。

| accepted scope | requirement | design responsibility | strategy |
| --- | --- | --- | --- |
| R1/R2、AC1 | REQ-793-01/02 | DES-793-01/02 | TST-793-01/02/03 |
| R3、AC2 | REQ-793-03 | DES-793-02/03 | TST-793-01/03 |
| R4、AC3 | REQ-793-04 | DES-793-04 | TST-793-04 |
| R5/R6、AC4 | REQ-793-05/06 | DES-793-03/05 | TST-793-01/05 |

前驱为源 Git 中三原 qualifier/caller/workflow 及已晋升 #382 REQ-382-01、
DES-382-04 的调用前置；后继只替代固定调用与上游结果普遍前置。原 #382
其他目标感知因果职责、原公开最小出口、consumer、完成边界与历史观察保持。
未迁移主题仍沿其原完整来源读取；没有全库迁移或全局版本前进结论。

原 Architecture/Check 审完整 proposed 与实际实现；candidate_checked 后原
RDT owner 集成当前完整单元并读回，实施重绑 actual after 后最终 Check/Review。
不修改旧不可变版本、历史 Test、根导航或别的 Task contribution。
