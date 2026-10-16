# D1 实施与验证

## Delivery Policy

policy=full。task_scope/delivery_slice 均为整体 AC01–AC10；remaining_work=[]。独立可交付条件：摘要完全兼容，原正常入口和恢复保持，冻结的两类树性能/资源标准全部通过，canonical/dogfood/installed定向分发证据完整。validation_boundary 为本 Issue 的正常 Reconcile 路径，不承担 Release #575 全矩阵；Completion owner 为 guru-review-task-completion，逐项核对整个 Task 后由 Closure 关闭 #588。

## Docs SSOT Plan

strategy=no_docs_update_needed：本变更只优化已存在确定性内部机制，无需求/架构/公共API新语义。唯一长期测试证据为本Delivery的性能结果与验收核对；包内 contract 仅在描述实现机制已不准确时保持语义同步。原 RDT owner guru-maintain-requirements-design-test-ssot 保留 durable authority，无新的业务规则需要其写入。design 唯一 source-design disposition 表为来源承接依据。

## 顺序

1. 完成 Wording、独立 final_plan Architecture、Approval、Activation 后修改运行时代码；保留 design 冻结的基准阈值。
2. 在原 common.py/invoke.py 做批量读取、唯一OID摘要和本invoke不可变树memo；增加独立oracle、调用预算、正常对象失败与memo失效/独立验证回归。复用现有真实wrapper fixture与路径覆盖，不造无consumer框架。
3. 将同输入正式链/独立摘要benchmark保留为可复现实验脚本；原B与修复候选分别跑duplicates/unique两轮，记录耗时/进程/RSS/来源。性能报告区分摘要、其余估计、validation、整链及测量边界。
4. 跑Reconcile全套正常路径回归、py_compile、task validate、git diff --check；按design执行canonical/dogfood/installed、reapply/drift/platform/mode/sidecar定向验证。
5. 完成fresh Phase2 Architecture与完整Check、精确staging的TaskCommit、fresh完整committed B..H Architecture/BranchReview；根据实际finding修复并刷新直接依赖门禁。
6. Delivery Review审核中文Refs-only PR、Publish、Merge；Completion核对AC01–AC10，Closure、Acceptance/Finish Architecture、bookkeeping归档与受管资源收尾。合并不声称正式版本发布或同事业务仓升级。

## 验证映射

| AC | 直接证据 |
| --- | --- |
| AC01/02/03/05 | 独立旧摘要oracle、真实batch请求预算、去重与memo生命周期测试；临时文件传输回归 |
| AC04/08 | 既有及新增真实wrapper正常路径测试；resolved/continuity/recovery使用原consumer |
| AC06/07 | design冻结合同、前后两类fixture各两次完整链与摘要阶段性能/资源结果 |
| AC09 | canonical→apply→dogfood、声明平台、干净installed链、reapply/drift/sidecar/mode结果 |
| AC10 | 完整Check/Review/PR、Completion与Closure及Finish实际结果 |
