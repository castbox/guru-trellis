# #578：独立判断与跨 owner 工程执行事实

状态：`reviewed_promoted`；identity：`architecture-contribution-578-cross-owner-validation-facts-v1`；change_path：`target_native`。按 expected `current-main-0.6.17-guru.93/active` 晋升 `.94`。constitution v1、project change contract v1、原 owners、GAP lifecycle 与软件四轴保持；ADR-029 窄补充 ADR-019 并继承 ADR-028。

首次通过的独立完整 committed Review 范围为 `origin/main@404d3f4d7635b19fb2c9f0d6aa642e2f1bf925b4...5ba72ba9ca40d990d8250fbc0c174475bc3d98f4`；[不可变 task-owned contribution](https://github.com/castbox/guru-trellis/blob/5ba72ba9ca40d990d8250fbc0c174475bc3d98f4/.trellis/tasks/10-16-578-cross-owner-validation-facts/architecture-contribution.md)保留原候选。长期机制由[唯一 Design](../../requirements-design-test-contributions/578-cross-owner-validation-facts/design.md)、canonical 三 owners 与 MIGRATION-578 单写；[ADR-029](../adr/029-cross-owner-validation-facts.md)拥有窄架构决定。

Before：Architecture personally executes、BranchReview reruns、Check same-owner-only 会使依赖未变化的工程事实无法跨 reviewer/阶段采用。After：原 owner 先独立确定当前完整范围、风险、消费者与检查集合，再核对合法可访问、可核查的原始事实和定义/版本、真实依赖、工具链、参数、环境、测试期望；在现有 summary 如实说明执行来源与适用理由。变化、未知、缺失和新义务只补受影响检查。当前语义判断、project-check/freshness、typed routes、private checkpoint 退休和独立完整 Review 保持，无 ledger/cache/第二 writer。

| Concern | 适用及处理 |
| --- | --- |
| authority-binding | applicable：planning3.0双purpose、原nonplanning2.0与阶段适用authority不变 |
| constitution-binding | applicable：只改原owner、现有summary和最小真实验证，避免第二存储和语义脚本 |
| boundary-and-decision | applicable：区分语义判断、工程执行事实和当前结果绑定；窄补充ADR-019，继承ADR-028 |
| owner-and-single-writer | applicable：原owner判断适用性；脚本只绑定客观事实；shared-current只由原promotion单写 |
| compatibility-and-exit | applicable：公共I/O保持；采用经完整安装，旧私有状态不新增兼容reader |
| gap-and-deviation | applicable：不新增/关闭/重开无关GAP；不改变GAP-006/008原owner；未验证外部边界保持 |
| parallel-scope | applicable：仅本Task贡献和必要canonical；不写业务仓、他人Task或CI/CD |
| evidence-and-freshness | applicable：当前结果仍新绑定；源工程结果原对象保持，执行来源和采用理由可核查 |
| review-and-promotion | applicable：首次独立完整committedReview后expected-current晋升；新差额重新Check/Commit/独立Review |


知识晋升只承接首次已审贡献；晋升新差额必须 fresh Phase2/TaskCommit/不同 reviewer 完整 Review。实际结果与失败、skip/incomplete及未验证边界只由[唯一 Test](../../requirements-design-test-contributions/578-cross-owner-validation-facts/test.md)拥有，不证明完整 Release/Upgrade 矩阵、source-lock 精确安装、remote marketplace、业务采用或生产效果。
