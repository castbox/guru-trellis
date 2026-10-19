# #637 候选适用性设计增量

状态：proposed。唯一Task详细方案及来源处置位于所选D1 design.md。原RDT .113生命周期完整定义、ADR-028/030/033仍为比较约束；Architecture贡献由原独立owner审核和晋升。

## D637-01 / CON637-01：唯一共享定义与原职责

canonical workflow-contract的候选适用性小节拥有三类事实和覆盖差额规则。Architecture/Check/TaskCommit/Branch Review/Delivery Review/Publication/Merge在原step-local Skill显式读取，workflow/continuation只编排加载。不新增公共Skill/profile/exit、GateResult字段或状态机；runtime保留客观绑定，不代AI判断。

## D637-02 / CON637-02：合法覆盖与finding接续

首次完整独立覆盖保持。后继固定B..Hi，由原合规reviewer读取原真实覆盖、Hr..Hi全部差额、冲突组合和未改consumers，亲自形成当前完整结果。原passed public full_review定位candidate/scope/plan/outcome；首次非pass仅定位finding，来源不足补审。finding owner核闭合后可同职责完成最终覆盖，fresh_final_review wire显式窄迁移，不以身份变化强制全量。

## D637-03 / CON637-03：执行事实与阶段绑定

当前owner先确定范围/风险/check set，再审原命令实际输入、依赖、定义/版本、工具链/环境/参数/期望，采用或补命中项。计划ref不当命令日志，同树不证明环境。原Check/full_review仍生成绑定当前candidate/predecessor的新正式结果；同Delivery恢复，末端owners核自身payload和live事实。

## D637-04 / CON637-04：分发、退出与证据

MIGRATION-637成套切换matching workflow/preset/packages/consumers，旧安装固定或原owner恢复迁移，不热改开发Task。#636早期Draft不自动产生full_review，正式结果仍真实Check predecessor。canonical/platform/installed/apply/reapply/drift和在途恢复分别验证。新旧同构Agent先比充分性/检错再按语义/命令/正式记录/远端等待计时；无固定收益承诺。原RDT/Architecture按独立Phase2、expected-current晋升及最终Check/committed Review顺序承接。
