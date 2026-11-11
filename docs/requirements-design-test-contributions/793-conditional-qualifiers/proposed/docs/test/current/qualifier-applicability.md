# qualifier 条件调用验证策略

Identity：RDT-TST-QUALIFIER-APPLICABILITY；aliases：TST-793、conditional qualification。
原语义 owner：guru-maintain-requirements-design-test-ssot。来源 Issue #793；状态 proposed，
适用源 Git e30c7bb5d4c24bc075dc14cfcd04c1da00fcf78e。原 final_integration 前不是
shared current；[REQ-793](../../requirements/current/qualifier-applicability.md) →
[DES-793](../../design/current/qualifier-applicability.md) 的必要策略如下。

## TST-793-01 / 确定性闭环

运行实际改变包/consumer的必要contract/runtime及public wrapper覆盖，核非空输入、
当前facts、stale、enum aggregation与原唯一consumer。采用仍适用覆盖，只补真实
改变的前置/投影缺口。脚本不分类是否触发，schema/string比较不能证明AI语义判断。

## TST-793-02 / 普通未触发

从完整provider的真实原caller入口给已接受普通工作事实，host不注入verdict。读取
实际工具事件：先读短条件，未触发不读全文/装配/调用；原owner仍完成本阶段判断。
完整入口必需前提不可由fixture替掉。纯函数Author可观察此路径，不要求全阶段乘积。

## TST-793-03 / root-only、真实触发及非通过

实际caller接收范围已清楚、无authority-placement改变的真实诊断/修复/保护候选时，
由行为决定哪些owner触发。root-only路径不强求不存在的normal/solution结果。
触发使用原wrapper；拒绝、机制修订、诊断、范围选择、blocked仍回原consumer。
未变原非通过consumer覆盖可采用；实际改变的消费分支需补命中观察。

## TST-793-04 / 采用、刷新与恢复

同机制的authority/条件/证据仍适用时采用真实结论，同时审当前工作；提供实质材料
变化后刷新受影响owner，必要结论丢失经原producer恢复/重判。实际新wrapper仍绑定
当前facts，不复播旧envelope。保留可核对的实际输入、工具和结果，证据仅覆盖被
执行的声明层级；不从模型exit0、历史pass或文件存在推导语义通过。

## TST-793-05 / matching采用

沿原tools owner同步canonical、dogfood、Claude Code/Codex和真实受影响受管路径，
核source/installed package、投影、必要drift及sidecar，Task/gen/key/root/session保持。
不要求完整clean/update/多平台矩阵，不证明业务安装采用、成本降低或事故修复。

## 结果与停止

本轮实际结果由[唯一Test](../../requirements-design-test-contributions/793-conditional-qualifiers/test.md)
记录，正式阶段以原公共结果和Git/PR事实为准。必要行为、非通过和分发证据充分后
停止额外实验；设施未触达目标不记产品失败/通过，保具体缺口。不新增通用评测框架、
固定案例数或成本阈值。历史#382/#735观察保原输入和截止，不重写为本批通过。
