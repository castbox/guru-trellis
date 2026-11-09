# worktree 配置路径追踪

| Requirement / Behavior | Design / Contract | Test / Scenario |
| --- | --- | --- |
| R760-01 / BEH760-ROOT | D760-01 / CON760-PATH-FACTS | T760-01 / S760-ROOT |
| R760-02 / BEH760-CONSUME | D760-01/02 / CON760-PATH-FACTS、CON760-CREATE | T760-02/03 / S760-TASK、S760-TASK-FREE |
| R760-03 / BEH760-PRECHECK | D760-02 / CON760-CREATE | T760-02/03 |
| R760-04 / BEH760-LOCATION | D760-02/03 / CON760-CREATE、CON760-MIGRATION | T760-03 / S760-TASK-FREE |
| R760-05 / BEH760-MIGRATION | D760-03 / CON760-MIGRATION | T760-04 / S760-DISTRIBUTE |

R718→D718→T718 原关系与历史观察完整保留；三个 stable runtime-location 单元就地修改，
无替代 identity。R760 只补配置生成差额。Issue #212 为历史配置承诺，#718 保留独立身份，
#759 与 #152 不进入本项。Architecture引用原公开locator/identity，不复制其正文。

实际 candidate_checked 后，原 RDT owner重读三个真实 current 与本完整贡献，保留仍适用定义、
历史及稳定identity，补修复版真实观察后写入并回读。单元修订 `worktree-config-path-760`；
没有修改共享根/索引。Architecture由原owner独立整合，implementation随后重绑actual-after。
既有历史测试截止点和完整Release/业务未覆盖边界继续适用；最终Check/Review及Completion不由本贡献替代。
