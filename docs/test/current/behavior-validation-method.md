# 行为测试与因果验证的测试策略

Identity：RDT-TST-BEHAVIOR-VALIDATION；别名 T735/SC735。原语义 owner：guru-maintain-requirements-design-test-ssot。来源 Issue #735，状态 current。变更起点 main@b78edbbdc32e77392bc3775366473971050ccb4b；精确当前定义由包含本文件的 Git revision 绑定。晋升依据：原 candidate_checked 后，原 RDT owner 完成 final integration 写入与读回。

## T735-01..06 / SC735-NATIVE

R735-01..03 → D735-01..03。从正常完整 Author、根因资格与实施派工入口，给事实而不注入预期答案，观察以下实际行为：明确普通功能自主选顺序；有效失败与修后证据复用并停止；新回归触达存疑先查路径再按真实缺口选择检出验证；异步未知原因进行有界诊断且准入不先要修后绿；设施失败与目标缺陷、有效预期错误测试区分；无具体缺口的固定红绿/阶段重跑被收敛而必要验收与回归保持。

host 在运行前持有事实与期待，collector 记录实际输入、工具、动作、结论及限制，AI逐例判断。无触达依据不能宣称测试有效，结构和出口不能替代语义证据。设施执行失败保留首轮事实，修设施或采用能回答同一问题的观察；受影响验收未完成不得记通过。不将本次案例转为所有任务固定次数或旧版本回退义务。

## T735-07 / SC735-DISTRIBUTE

R735-03 → D735-03。命中 package contract/runtime、source/installed/实际平台投影、tools maintenance/reapply/drift/mode 与 sidecar 分别检查。普通本项不扩完整多平台Upgrade/Release矩阵，不证明外部项目采用、统计改善或业务生产效果。

## 结果定位与关系

本批实际输入、动作、结论和证据边界唯一由 TaskId 735-behavior-causal-validation、generation0、DeliveryId 51cf3d42-d210-4938-a20a-da800f158795 的 validation 正文承担，Task 活动或归档路径由原身份解析；本单元不复制执行记录为第二结果authority，不预填最终pass或自身最终HEAD。需求R735位于 docs/requirements/current/behavior-validation-method.md，设计D735位于 docs/design/current/behavior-validation-method.md。正式 Check、Review、Delivery、Completion 仍读取原公共结果与实际 Git/PR事实。

## T826-01..04 / SC826-PROJECT-COMPARE

R826-01/02→D826-01。T826-01以可运行去敏CLI项目执行启动、可用就绪、真实读写、结果和副作用、清理后证据读取；T826-02改变覆盖入口或行为后更新并重跑受影响验证。T826-03事前固定同材料/host准则，用现行/候选方法各自实际Agent执行，独立评价者先匿名读完整输出与工具，原owner报告改善、退化及未证，不预设胜出。T826-04通过真实定向分发/reapply/drift/sidecar检查证明方法可读与状态保留；结构不证明行为。

本批实际观察由TaskId 826-verification-experiment-methods、generation0、DeliveryId e74b8c49-7042-4896-a74f-61527e7050c0 的validation.md承担，未执行项保持未证，不推断完整平台矩阵、外部采用或统计改善。原735历史观察和结果定位保留原义。

本单元的826增量由原RDT owner在本Task实施与真实Sol medium案例验证后完成整合及回读；正式提交后独立Review与Delivery/Completion仍待各原owner，不从本文推定最终通过。
