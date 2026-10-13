# #531 远端恢复验证仓 Architecture Baseline

版本：531-validation-foundation-1。状态：active。由原 Architecture bootstrap_foundation owner 对本验证仓 foundation 完成职责、依赖与适用性审查后激活；不代表 Delivery candidate pass。
适用范围：独立远端事务恢复样本；不继承 Guru 产品仓架构 authority。

## FOUNDATION 与 CURRENT
仓内 README 将此仓定义为 #531 受控远端事务恢复验证临时分支。唯一可交付运行内容为 validation/531-remote-next.txt，另有稳定 Task 与 Delivery 规划以及本仓 foundation。没有业务应用、服务或 provider 实现。
已安装 .trellis/.version 为 0.7.0-castbox.3；.trellis/guru-team/extension.json 声明 Guru 0.7.0-guru.3，source.commit 为 f03e8a04c487e64722e90697543ec7398de2b338，tree_state=dirty。这是安装 provenance，f03 是 base HEAD，不能据此断言正式 source-lock 或 clean 发布候选。冻结 source snapshot 的 3740 个文件已逐一核对，local_candidate full SHA 为 f12aa5e9542fe5076f9192d585d1fc794efa9276a22e2b2766d798feb91f6923。mixed CLI tar SHA 为 5aeeb81ca72508081b7dd94ddb7a19f69444714f78b3a38858d908196cc77916；Core tar SHA 为 45bbfee507ed4964649610f703a90ba01c5f5cea21fb95d0845f92ed45302967，两者已实际重算。它们是本次冻结依赖的身份，不是正式 source-lock。此仓现有 .trellis/scripts/common/runtime_contract.py 与原样本字节一致；mixed CLI 仅在迁移执行显式选择其 bin，不能声称此仓全部 CLI 已切换。
上游 .trellis/scripts/common/runtime_contract.py 明确支持 delivery_api=1.0、task_schema=2.0。安装文件事实不证明远端恢复执行通过。

## 职责与 TARGET
Task/Delivery schema 与合法状态转换由安装上游 public API/store 拥有；Guru runtime/delivery_projection/adapter.py 只投影原 owner 的最小输入与结果。
原 Publish owner 拥有 push、PR 绑定、metadata、Ready 与 same-plan recovery。原 Merge owner 拥有 expected-head merge、message/parents/trailers 验证与 terminal recovery。Completion 独立判定整体完成；历史成功不替代当前门禁。
TARGET 是在本仓专用 base codex/531-remote-next-base 上保持这些职责，并通过原 owners 实际观察同结果恢复。当前尚未获得该样本远端执行证据。

## 决策、GAP 与兼容边界
DEC-531-OWNER-1：复用已安装原 owners 与上游状态 authority，不增加恢复 ledger、业务 provider 或私有状态模型。
GAP-531-INSTALL-1：冻结 source 的新增 scope stage 模块曾未进入 installed projection；由原安装修复 owner 处理和验证，foundation 不抹除该失败、不宣称修复通过。后续 gate 必须读取其实际修复结果。
GAP-531-LIVE-1：新样本真实 Publish/Merge/历史 discovery 尚未完成；由该 Task 的原执行 owners 产生事实，再由 Check/Review/Completion 各自判断。基础文档不能关闭该 GAP。
更改冻结安装依赖或目标 refs 时重入原规划与门禁。旧样本和产品仓保持只读；本仓不产生 Issue 关闭效果，不证明 V07 旧clean迁移或完整 Release 矩阵。

## 导航与版本
[设计宪章](00-foundation/design-constitution.md)；[变更合同](06-governance/change-contract.md)；[需求](../requirements/README.md)；[设计](../design/README.md)；[测试](../test/README.md)。
本版本为首次 foundation，无 predecessor。新版本保留 identity 与 successor 导航，不能静默替换冻结依赖或历史证据。
