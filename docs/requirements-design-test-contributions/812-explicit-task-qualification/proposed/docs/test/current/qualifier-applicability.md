# qualifier 条件调用验证策略

Identity：RDT-TST-QUALIFIER-APPLICABILITY；aliases：TST-793、conditional qualification。
原语义 owner：guru-maintain-requirements-design-test-ssot。来源 Issue #793；状态 current，
适用源 Git e30c7bb5d4c24bc075dc14cfcd04c1da00fcf78e。原 RDT owner 于
final_integration 从隔离完整拟写晋升并读回；[REQ-793](../../requirements/current/qualifier-applicability.md) →
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

条件调用 #793 的实际结果由[原 Test](../../requirements-design-test-contributions/793-conditional-qualifiers/test.md)
记录，正式阶段以原公共结果和Git/PR事实为准。必要行为、非通过和分发证据充分后
停止额外实验；设施未触达目标不记产品失败/通过，保具体缺口。不新增通用评测框架、
固定案例数或成本阈值。历史#382/#735观察保原输入和截止，不重写为本批通过。

## TST-812 / 显式身份与续接

本节承接 REQ-812-01～05 与 DES-812-01～05，适用前驱 Git
f16bb562e4ea844939786cebd5c6c20e686914b2。它增加以下必要验证，保 TST-793 的
条件调用与历史截止。#812 的工程与原生观察按下述配对 Test 读取，独立 committed Review 和外部交付终态另由原 owners 判断。

1. 公共合同与共享事实：三个原 package 定向 contract/runtime、共享身份集成测试
   通过原 public Creation/Identity/Ensure/Bind/Scope/Delivery 建真实前提，再调用
   三个 qualifier 公开 wrapper。观察七类显式输入及四类不变输入、新旧 schema
   各自有效和交叉替代拒绝。既有单元夹具只证明其声明边界，不证明原 owner 创建事实。
2. 普通 mismatch：当前 generation、registered checkout、Planning/candidate 发生
   正常变化或 caller 选错已有对象时，旧输入拒绝；有官方 context 时原选择必须和
   显式 key 匹配。状态准备不能伪造 artifact/hash/context key，不为攻击场景加负例。
3. 实际 AI/caller：主实施调用方真实无 context，正常子 Agent 使用平台真实官方
   context，经原 Identity/Ensure/Bind/Selection。按实际适用集合读完整合同并选择
   三个原语义结果，执行公开 wrapper，消费原唯一出口后继续原阶段。已拒绝的
   “跳过 Planning”修复替代用于观察原机制修订及 Author 移除替代后的续接；其余
   未变路由采用仍适用覆盖。不把 qualifier 输出当作实现成功。
4. matching 采用：原 tools owner 更新后，目标自己的 resolver、installed checker、
   原公开入口以及 canonical/dogfood/声明平台、drift/sidecar 定向验证通过；原
   Task/session/peer 与 common pointer 保持。local_candidate 的正式 Fork source-lock
   未验证边界单列，不声明完整多平台安装/升级/Release 矩阵或生产效果。
5. 工程/交付：实际 RDT/Architecture integration/readback 后形成固定本地完整提交，
   由新独立 committed reviewer 承担完整 Check/full_review。readiness、Delivery、
   Completion、Closure、Finish 各自以原公共结果与 Git/GitHub 事实判断；merge 前
   仍交协调方处置。不得由这些后续义务预填当前验收结果。

#812 的实际命令、结果与边界由[配对 Test](../../requirements-design-test-contributions/812-explicit-task-qualification/test.md)单写，必要证据充分后停止
重复验证。设施未触达目标保具体缺口，既不算产品通过，也不虚构产品缺陷。
