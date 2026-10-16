# #578 设计增量
需求身份见 requirements.md，实际验证唯一见 test.md；task设计来源处分仍在原 task design.md。继承原owner、ADR-019/028及九concern。

## D578-01 独立语义判断与工程事实
Architecture、Check、BranchReview先独立确定当前完整候选、消费者、风险和适用检查集合，再读取原始工程执行结果。由本轮owner判断定义/版本、真实依赖、工具链、参数、环境和测试期望的适用性，在现有summary/evidence locator如实说明实际执行或采用、来源与理由。
前序semantic pass、DTO、private checkpoint不成为工程事实。当前语义判断与结果绑定均由本轮owner完成；现有recorder/checker和public I/O不变。

## D578-02 受影响补跑
任一真实依赖变化、未知或结果不可用执行受影响检查；新适用检查执行。文档改行为合同或新风险同样纳入实际消费者；相同tree不自动豁免，缺单项不触发无关全量。无因全量与一次后永不重跑均不成立。
原始结果保持原对象，当前owner新结果不改写历史事实；不新增跨Skill账本/缓存或延长private checkpoint生命周期。

## D578-03 承接与安装
直接演进三个canonical owner和冲突派发/提示文案，不新增phase/Skill/exit/DTO或脚本语义分类。窄Architecture决策由task-owned ADR candidate及原promotion owner承接。
完整preset安装投影规则、声明平台与reapply/drift沿原installer；开发Task保持原完整安装，在独立匹配source dogfood验证产品，不热替换活跃Task。MIGRATION-578拥有采用指引，README只导航。

