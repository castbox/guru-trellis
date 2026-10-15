# #569 双向追踪

| Requirement / Behavior | 唯一设计职责 | 验证场景 | 观察入口 |
| --- | --- | --- | --- |
| R569-01 / BEH569-01、R569-02 / BEH569-02 | D569-01、CON569-01 | T569-01、02、03、04 | 原discover wrapper、真实Git组件与installed链 |
| R569-03 / BEH569-03 | D569-01、CON569-02 | T569-05、06 | 真实caller/peer文件与Git数据前后核对 |
| R569-04 / BEH569-04 | D569-01、CON569-01、02 | T569-03 | 公开cutoff、实际B2和原consumer |
| R569-05 / BEH569-05 | D569-01、02 | T569-04、05 | 原query错误与合法空结果 |
| R569-06 / BEH569-06、R569-07 / BEH569-07 | D569-02 | T569-03、04、05 | public writer→query2、混合trailer、后继核验 |
| R569-08 / BEH569-08 | CON569-01、02 | T569-02、03、07 | 同版schema/interface/commands、公开consumer |
| R569-09 / BEH569-09、R569-10 / BEH569-10 | CON569-02 | T569-01、02、03、07 | 原Merge→query→Completion及恢复公开入口 |
| R569-11 / BEH569-11 | D569-01、CON569-02 | T569-06、07 | matching安装、apply/reapply、投影bytes/modes/drift |

test.md每个T569行反向引用上述设计与需求；无孤立需求、设计或测试。现有RDT .98中#557/#567的有效职责保持，其关于#569尚未实现的数据准备边界由此增量承接，不隐式改其它阶段或发布authority。Architecture contribution仍位于本Task目录，尚未晋升shared current。
