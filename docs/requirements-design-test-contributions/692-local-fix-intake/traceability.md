# #692 追踪与保留边界

适用基线为 `6a65ec8afe6d180850760b3b2edf3f94be6e3b20`；authority 为 `guru-trellis-rdt`。`proposed/` 镜像最终 repo-relative target，其内部链接按最终位置解释。三个完整正文和三个 current 导航仅由原 final_integration 写回。

| 整体要求/验收 | 完整需求与行为 | 完整设计与合同 | 完整策略与场景 |
| --- | --- | --- | --- |
| R692-01；AC692-01 | R692-01 / BEH692-ROUTE | D692-01 / CON692-OWNERS | T692-01 / SC692-ROUTE |
| R692-02；AC692-02 | R692-02 / BEH692-REUSE | D692-01 / CON692-OWNERS | T692-01 / SC692-REUSE |
| R692-03；AC692-03/04 | R692-03 / BEH692-DIAGNOSTIC | D692-02/03 / CON692-BINDING/CON692-ERROR | T692-02/03 / SC692-BINDING/SC692-CHANGE |
| R692-04；AC692-05 | R692-04 / BEH692-DISTRIBUTION | D692-04 / CON692-DISTRIBUTION | T692-04/05 / SC692-INSTALL/SC692-QUALITY |
| AC692-06 | 原整体生命周期责任 | 原 Completion/Closure/Finish owners | 原 Completion 及 live terminal facts；局部检查不代替 |

完整来源为 live [Issue #692](https://github.com/castbox/guru-trellis/issues/692)（updatedAt 2026-10-30T13:58:05Z；读取时无评论）及同基线的原 canonical owners。必要有效前驱为 `docs/{requirements,design,test}/current/task-delivery-lifecycle.md`（初始入口、唯一 Planning、恢复）、`json-input-carriers.md`（JSON 读取层）与 `knowledge-maintenance.md`（合同承接/证据方法）。这些稳定身份和义务保持；本贡献只新增具体 Intake 行为及诊断定义，不删除、合并、重编号或复制旧单元。

canonical Skill references/runtime 拥有精确行为与 I/O。R/D/T 单元的关联是能力关系，不是第二 schema。Architecture entry/constitution 保持，由原独立 owner 对当前候选及晋升作实际判断。本批实际命令结果唯一见 [test.md](test.md)，不得从历史来源、知识晋升或静态投影推断业务采用。
