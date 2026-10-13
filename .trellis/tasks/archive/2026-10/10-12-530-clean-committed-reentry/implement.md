# #530 实施与验证计划

状态：Planning；尚未实施。完整范围 R530-01..06，一次 Delivery，无剩余实现；软件 Release/backend升级不属于本 Delivery。

## 顺序

1. 在本 Task checkout 更新 task-owned RDT与Architecture候选，明确current source、输入profile、owner职责、old-path保留及未验证边界。先完成Planning wording、独立Architecture、Planning approval与方案展示；激活后才能实现。
2. 扩展 canonical guru-create-task-commit 的 invoke、closed public schema、commands/interface、contract/SKILL/examples。复用 Phase2现有 checker端口，验证 current passed/checkpoint/content以及Task/branch/base/clean/operation事实；不复制semantic判断或内容身份算法。输入 profile和互斥参数按design定义。
3. 更新 Workflow Phase2→TaskCommit分支和TaskCommit→pair guard→BranchReview恢复语义、当前consumers与eval；有 dirty保留原prepare/executor。finding-fix/fresh-final intent保持其原owner。
4. 执行风险匹配回归及canonical→installed/platform投影验证，更新唯一test.md和traceability。定向测试从实际producer stdout接续，不手写passed/committed成功DTO。
5. Trellis check owner完整Phase2；经精确提交确认后TaskCommit；不同reviewer执行freshArchitecture与完整committed BranchReview。后续晋升/Delivery/lifecycle与每项Git副作用遵守原owner边界。

## 验证设计

| Test | 实际入口与 defect detection |
| --- | --- |
| T530-01 | 临时真实Git repo/正式Task和branch binding，真实dirty TaskCommit生成工作提交，base前移，正式post_commit Reconcile生成整合提交，fresh Phase2正式passed/post_check unchanged后使用committed_reentry正式invoke。输出的commit必须等于真实HEAD且 no new commit；再进入首次initial_review完整范围，而非continuity。实现前保留该正常链的首次失败为 exact_stage_paths。 |
| T530-02 | 同一passed检查后产生真实dirty任务增量，原prepare和invoke完成exact commit；只读profile不能承接dirty。验证stage路径与实际Git结果，避免只断言新增函数结构。 |
| T530-03 | 用正常编辑、提交和base前移造成checkpoint/content/anchor/branch/base stale，正式入口拒绝并指向现有freshPhase2或Reconcile恢复；不构造恶意伪造artifact。 |
| T530-04 | 正常 active merge未结束时只读入口不得替代 #407；沿原resolved-tree恢复处理。finding-fix结束后仍由原closure/fresh-final流程消费，不能被入口当首次full pass。 |
| T530-05 | invoke成功前后比较HEAD、tree、index语义和status、commit count；只读无hooks/ref写入/空candidate/推进文件/新receipt；Phase2checkpoint消费符合原owner规则。 |
| T530-06 | canonical contract/runtime/schema/consumer/eval与preset投影parity；一个standalone临时安装验证clean/current-update/reapply及正式新profile入口。不要修改backend444或扩大完整Release平台矩阵。 |

使用package现有生产wrapper和安装验证入口；选择能检测实际链路闭锁的定向测试。真实外部依赖不可用明确unverified，不声称全通过。测试实现不得仅重复schema枚举或镜像内部helper。

## 实施范围与风险

canonical路径：trellis/skills/guru-team/packages/guru-create-task-commit/**、guru-check-task既有checker端口必要共享抽取、guru-review-branch职责文档/consumer、guru-reconcile-task-base关联eval/consumer、trellis/workflows/guru-team/workflow.md、直接命中的durable spec和preset投影。
风险：Phase2内容算法/退休边界、base再次演进、full review intent、public参数互斥与projection drift。若机制或owner/persistence范围变化，先qualification/Architecture/Planning重入，不能自动扩实现。
Docs唯一结果：docs/requirements-design-test-contributions/530-clean-committed-reentry/test.md。所有未来阶段在当前证据之前保持未执行。
