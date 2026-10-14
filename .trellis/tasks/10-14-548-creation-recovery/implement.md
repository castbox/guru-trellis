# #548 执行计划

## Delivery Policy

- policy：full；一个Delivery完成PRD AC1-7验证及必要回归/证据。
- slice：当前正式创建、同Task恢复、D1接续、旧untracked逐记录处置。
- remaining work：无独立后继切片；未验证的原业务恢复与完整Release矩阵是排除边界。
- whole-task Completion：每AC有正确层级结果，真实context与fixture不混报；无伪造gate、无删除重建；正式Check/完整Review/readiness/Delivery通过。
- remaining-work owner：本Task原Completion owner。

## Docs SSOT Plan

`delta_first`：专属RDT contribution为 docs/requirements-design-test-contributions/548-creation-recovery/，原guru-maintain-requirements-design-test-ssot拥有唯一Requirement/Design/Test/traceability；最终Phase2前reconcile。Architecture专属贡献见design唯一定位；首次committed独立完整Review后原owners晋升expected .92/.88，晋升diff fresh Check/commit/完整Review。docs/testing/task-creation-recovery.md只链接唯一Test及原owner合同，不复制结果。

## 顺序和精确验证

1. 已执行：live #548、正式Intake/Create/C3、固定current创建回归与native sample；保留首次环境失败。完成current Planning gates后实施。
2. 修复design所述原adapter显式读取、Creation恢复/退休及已有key的五consumer；step-localMarkdown同步。联合创建到D1测试从正式Guru Create开始：原公共Create/Bind/Author/Clarify/CreateDelivery/Planning/Activation，same-result recover；有key/explicit-mode各一条。断言同Task/gen/单一D1、正向phase与slot、规划/Git资源保留；原no-key失败sample复用原pending UUID恢复，不重建。
3. 隔离旧Task样本：官方前驱writer、真实untracked Task、公开升级/Plan2 preview与逐记录defer/stop；不伪造已提交planning identity。
4. current targeted：Create Task、Bind、TaskLifecycle、CreateDelivery、Author chain、Activation、必要Migration测试；明确零skip或具体依赖阻断。仅扩大与新增失败有关的测试。
5. installed/native：保留一个代表sample，actual Codex context正式创建/恢复后current+continuation指向同Task/当前owner；成套preset reapply和managed字节/mode、平台投影/drift核验。不半升级旧主dogfood。
6. 唯一Test证据、RDT delta reconciliation、独立Architecture与完整Phase2 Check；精准TaskCommit、不同reviewer完整origin/main...HEAD BranchReview；原owners晋升后新diff重跑各gate。
7. fresh readiness与Refs-only Publication/merge；whole-task Completion、独立Closure关闭#548；Finish bookkeeping及资源处置。仅处理本Task-owned资源，不删除caller-owned checkout或样本之外资源。

## 写入范围

本Task规划/context、原adapter/Creation/五Planning consumers与必要step-local合同、两处联合回归、RDT/Architecture专属贡献与review后共享promotion。无public I/O或新owner，无业务仓升级/cleanup，无完整安装/Release矩阵。
