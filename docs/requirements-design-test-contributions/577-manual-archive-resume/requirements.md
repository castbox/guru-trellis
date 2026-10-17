# #577 Requirements 增量

状态：active，随 RDT `.106` 晋升。来源为 [Issue #577](https://github.com/castbox/guru-trellis/issues/577)，公共模型和操作依赖 [Trellis #46 / PR #52](https://github.com/castbox/Trellis/pull/52)。继承 RDT `.105/active`、Architecture `.97/active` 的有效合同，扩展 #566 的 maintenance-only 能力，不改变正式 Reactivate 或完整 Plan2。

| Identity | 当前行为承诺 |
| --- | --- |
| R577-01 / BEH577-01 | 人工旧归档可从完整匹配来源显式选择，审查原Task、人工说明、scope、交付、source、binding和未完成责任后继续同一Task；不要求旧dispatcher、预先绑定或人工搬移。身份/来源不唯一时写前停止，不能删除重建。 |
| R577-02 / BEH577-02 | 公共Trellis定义支持格式、归档/活动关系、generation和精确public写入。Guru消费公共返回TaskKey/active_ref；原归档和转换来源可读且仅作历史，不与active共同成为current authority。 |
| R577-03 / BEH577-03 | 人工历史归档、正式Finish归档和未完成closeout分别走旧归档恢复、原Reactivate和原事务恢复；不补造Completion/Closure/Finish/Cleanup/seal。 |
| R577-04 / BEH577-04 | 写集只涉及选定Task、必要规划、确切关联session/binding与同操作恢复。原Guru owners核验历史/维护各自controls；工具更新独立审查，保护其它Task/session/checkout及dirty/untracked。 |
| R577-05 / BEH577-05 | 历史交付和当前补差分别保留。旧gate不成为当前pass；scope变化交原Clarify，真实新切片才创建Delivery，仅补证据/验收进入对应owner，无空Delivery或替代Task。 |
| R577-06 / BEH577-06 | 同操作普通重试、丢输出、写集前缀已应用后的恢复和回退保持既有身份、generation及一次历史导入。stale/mismatch、缺依赖或后续工作冲突给出具体owner/输入/入口，不循环重装或扩大写集。 |
| R577-07 / BEH577-07 | 恢复后目标自身原生identity/continuation及下一实际Guru owner承接同一公共返回key；分开报告工具、数据、历史、会话、native与业务完成。实际source/build/API和受影响投影/reapply/drift/sidecar须定向验证；最多一个代表旧安装拓扑。 |

真实CMS恢复、正式Fork采用、跨仓实现、全局安装修改、任意旧格式通用框架、完整Release矩阵和软件发布不在本增量范围。需求到设计与测试的唯一双向索引为 [traceability](./traceability.md)。
