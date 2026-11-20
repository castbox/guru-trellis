# 行为测试与因果验证的测试策略

Identity：RDT-TST-BEHAVIOR-VALIDATION；别名 T735/SC735。原语义 owner：guru-maintain-requirements-design-test-ssot。来源 Issue #735，状态 current。变更起点 main@b78edbbdc32e77392bc3775366473971050ccb4b；精确当前定义由包含本文件的 Git revision 绑定。晋升依据：原 candidate_checked 后，原 RDT owner 完成 final integration 写入与读回。

## T735-01..06 / SC735-NATIVE

R735-01..03 → D735-01..03。从正常完整 Author、根因资格与实施派工入口，给事实而不注入预期答案，观察以下实际行为：明确普通功能自主选顺序；有效失败与修后证据复用并停止；新回归触达存疑先查路径再按真实缺口选择检出验证；异步未知原因进行有界诊断且准入不先要修后绿；设施失败与目标缺陷、有效预期错误测试区分；无具体缺口的固定红绿/阶段重跑被收敛而必要验收与回归保持。

host 在运行前持有事实与期待，collector 记录实际输入、工具、动作、结论及限制，AI逐例判断。无触达依据不能宣称测试有效，结构和出口不能替代语义证据。设施执行失败保留首轮事实，修设施或采用能回答同一问题的观察；受影响验收未完成不得记通过。不将本次案例转为所有任务固定次数或旧版本回退义务。

## T735-07 / SC735-DISTRIBUTE

R735-03 → D735-03。命中 package contract/runtime、source/installed/实际平台投影、tools maintenance/reapply/drift/mode 与 sidecar 分别检查。普通本项不扩完整多平台Upgrade/Release矩阵，不证明外部项目采用、统计改善或业务生产效果。

## 结果定位与关系

本批实际输入、动作、结论和证据边界唯一由 TaskId 735-behavior-causal-validation、generation0、DeliveryId 51cf3d42-d210-4938-a20a-da800f158795 的 validation 正文承担，Task 活动或归档路径由原身份解析；本单元不复制执行记录为第二结果authority，不预填最终pass或自身最终HEAD。需求R735位于 docs/requirements/current/behavior-validation-method.md，设计D735位于 docs/design/current/behavior-validation-method.md。正式 Check、Review、Delivery、Completion 仍读取原公共结果与实际 Git/PR事实。

## #868 本次整合与关系

原RDT owner在批准规划、实际实现及真实工程结果后，于固定前驱Git `b85ea7bdf80db97ba8aceb1298dd61ed5f1ebeec` 的Task隔离checkout完成final_integration和读回。状态为`integrated_pending_review`，尚待TaskCommit及独立committed Review；不产生质量或Completion通过。来源和替代范围见[#868追踪](../../requirements-design-test-contributions/868-issue-acceptance-boundary/traceability.md)。既有来源、完整条件及旧观察截止保持。

## T868-03 / SC868-TRANSPORT

R868-04 → D868-03。原native staging装配固定public正文及必要依赖，测试真实投影/allowlist读取、字节与私有目录排除；只证明传递边界。Readiness native corpus由原runner执行，独立判断完整轨迹。

关联[Issue内容测试](issue-content.md)的T868-02/04：观察明确联合交付与边界外调用链的区别、已有充分覆盖复用和真实内层缺口定向补证。实际原runner standard-intake-authoring-acceptance-boundary取得ready，主协调器独立grade后正式passed；投影、传输和真实语义分层说明见[#868 Test](../../requirements-design-test-contributions/868-issue-acceptance-boundary/test.md)。对应R868-04、D868-03；沿原T735停止及因果方法，无新固定矩阵或实验门槛。

## T880-02/03 / SC880-ENVIRONMENT

R880-02/03 → D880-02。实际更新后的 `standard-intake-authoring-acceptance-boundary` 在同一 native run 中保留明确目标 runtime 4.2 与业务配置更新/revision，同时拒绝逐 Issue 共享 test 部署、服务部署和消费方 E2E；两条 semantic assertions 经独立 transcript 读取后通过。`test_review_sufficiency_distribution.py` 与 `test_issue_content_distribution.py` 的真实 writer/reapply 和 sidecar 检查通过，分别证明跨阶段薄引用与传播边界；不新增环境矩阵。

## T747-D1-01 / SC747-JOURNEY

R747-D1-01 → D747-D1-01。V1 在本批的完整候选 provider 上，经实际原生 Agent 入口使用冻结的去敏材料。Clarify 和 Author 的观察覆盖上传等待中再次操作、局部确认后退出、恢复和最终保存。读取实际输出，核对它是否区分已确认行为、未决产品选择和设计职责。用同一素材的独立审核记录检查是否从交出者释放唯一引用而接收者尚未接管的顺序推导出空档，并把技术缺口交给原 owner。

原评价者在执行前冻结判据，保留实际输入、工具动作及输出。按 [T747-D1-02](review-sufficiency.md) 核对独立审核与分发，区分已观察到的行为、失败和未执行范围。观察对应 JQ-AC1、AC2 及本批 AC8，结论限于实际素材和方法入口。
