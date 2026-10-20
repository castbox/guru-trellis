# #635 追踪与替代边界

固定适用前驱为 Git `7a7b60743499653ffeb81f6b31e627a02c33f579` 的六个 `docs/{requirements,design,test}/current/{task-delivery-lifecycle,completion-closure}.md` 完整单元。沿用 `RDT-REQ/DES/TST-LIFECYCLE` 和 `RDT-REQ/DES/TST-COMPLETION`；不递增全局版本或改无关导航。六个完整 current 单元已由原 owner 最终整合并读回；manifest 与 proposed 目录保留对应关系和候选历史。

| 来源 | 行为 | 设计责任/合同 | 完整测试策略 |
| --- | --- | --- | --- |
| #635 R1 | R635-01 / BEH635-STATE | D635-04 / CON635-ENVIRONMENT | T635-02/03/04/05；全链状态、consumer 与缺失范围 |
| #635 R2 | R635-02 / BEH635-REACTIVATE | D635-01 / CON635-SHARED-FINISH | T635-01/05/06；历史 target、后继优先、无本机 seal |
| #635 R3 | R635-03 / BEH635-RECOVER | D635-02/03 / CON635-CLOSURE/PUBLICATION | T635-02/03；活动 ref、Draft/Ready/MERGED/Closure |
| #635 R4 | R635-04 / BEH635-RESOURCE | D635-04 / CON635-ENVIRONMENT | T635-04/05；common-dir、generation、expected head、双 Task |
| #635 R5 | R635-05 / BEH635-MIGRATION | D635-01/05 / CON635-SHARED-FINISH/DISTRIBUTION | T635-06/07；固定旧格式、matching 分发与原生消费 |

前驱 `R434-03 / R436-05 / R454-D436-05` 与 `D454-D436-05` 的 TaskId、source、严格增代及旧状态分类保留；仅替代以原机 seal/manual Cleanup receipt 证明共享 Finish 的准入片段。原 Cleanup 的真实本机资源资格保持。`R436-02 / R547-*` 和 D547 的 disposition 资格与逐项 OPEN/CLOSED 规则保留；只补不能从原公共记录重新推导的最小动作输入和零 close 共享恢复。D531-05/D636-02 的同操作恢复保持，新增明确共享 PR/source 的跨环境入口，不重解释原本地 profile。

#636/#637/#638 的稳定身份、首次独立完整审核、当前候选、真实最终门禁、Refs-only、原知识 owners 晋升/读回与重绑规则全部保留。正式前驱与人工历史/未完 closeout 分路；历史安装及归档不回写。没有 consumer 的审计状态、授权信息和本机路径不进入贡献或公共结果。
