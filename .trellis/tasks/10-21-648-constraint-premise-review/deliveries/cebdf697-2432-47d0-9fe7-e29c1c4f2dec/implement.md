# D1：约束与关键前提审查方法实施与验证计划

## 1. 输入与引用

整体范围由[根PRD](../../prd.md)承载；本批[PRD](prd.md)展开D1-R01..07和AC；[design第3节](design.md#3-来源设计处置唯一)是唯一来源设计处置。本批无前序Delivery，固定B为`cca65742bc485f8ab4e6399623b70dd5aebc25bd`，同DeliveryKey贯穿。

实施前读取design第4至8节、live #648完整正文与10/21补充、Author shared planning-body和三模板、命中原Skill contract、`workflow-contract.md#candidate-applicability-and-coverage`、`quality-guidelines.md`测试价值与验证范围、current RDT知识维护完整单元及Architecture的constitution/change-contract。引用只定位，不能代替加载完整条件。独立candidate_assessment已返回no-impact，后续仍需Wording-current final_plan、Approval与Activation。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | 前置、原责任与实际文件 | 行为与完成观察 |
| --- | --- | --- |
| I648-01 | 进入实施后；当前协调AI；repo外固定B源码与原eval runner | 冻结design第8节样本/期待/次数/模型权限；修复原调用的trace遗漏，不弱化runner检查；完整before在方法修改前执行，审核实际语义并保留失败 |
| I648-02 | I01得到逐组证据；原Author/Architecture/实施/Check/Review/task-free owners | 在design第4节列出的原Markdown合同/模板/去敏示例补实际缺口；保留已有充分定义，不复制SSOT或新增公共边界。修改前逐文件读取当前内容，每批写前执行checkout boundary checker |
| I648-03 | I01定义的事实；原test staging writer；`trellis/skills/guru-team/adapters/eval/{architecture_authoring,phase2_authoring,native_adapter}.py`与对应test、原package evals/files | 扩原入口的真实事实/跨阶段调用与trace，先对B方法取before，再对I02新方法复核；脚本只收集执行/投影事实，AI逐次判断；超过3000行触发机械拆分评估 |
| I648-04 | I02/03候选稳定；原RDT writer；contribution648目录 | 准备完整R/D/T/traceability及manifest，保留原条件与#637/#638；不提前写sharedcurrent，不建空Architecture贡献 |
| I648-05 | canonical完成；原preset分发机制 | 完整apply同步dogfood、.agents/.codex/声明平台，逐个处置sidecar和mode；执行source/installed/reapply/drift；需要clean时只用一个代表throwaway |
| I648-06 | 全候选及隔离拟写完成；implementation/原Architecture/RDT/Check | 原candidate/begin_check→独立Architecture及完整candidateCheck→合法rework→原final_integration/readback→以实际after重建candidate/begin_check→最终Check；no-change保持合法回程 |
| I648-07 | 最终Check真实通过；原Commit/独立Review/Delivery/Publish/Merge/Completion/Closure/Finish/Cleanup | 分别在其原精确副作用边界执行；完整B..H committedReview和live main可达、Issue CLOSED/completed、Finish/Cleanup均须真实完成；不得把计划或单次合并当整体完成 |

I02不先于依赖它的I01证据。I03可以先准备fixture事实，但不能先改方法后宣称before。无冲突文件工作只有在无真实依赖时继续。公共API或owner职责扩大时停止本候选，回最早原owner。

## 3. 验证入口、输入与预期观察

V648-01..06严格按design第8节的固定样本、两次before/new与实际owner执行。使用原run-skill-evals入口，不给被测Agent期待出口/答案，原模型声明、high、隔离权限与相同起点保持。模型/输入/权限口径变化时双方重跑。保存repo外原运行记录，结果摘要逐样本说明具体约束/因果/路由、已有能力/新增收益/失败/未验证；不只报出口。

V648-07先跑命中package tests及原`test_architecture_authoring.py`、`test_phase2_authoring.py`，再执行项目规定的内存Python语法、JSON与Bash语法、Task validate、source/installed contract discovery、完整preset apply/reapply和`check-dogfood-overlay-drift.sh`、平台投影、模式与sidecar检查，最后`git diff --check`。workflow变化时执行`get_context.py --mode phase`及1.1/2.1/3.5代表context读取。命令选择以实际改动为准，不因本计划执行无关全套矩阵。

V648-08由原owners完成RDT追踪/实际整合/after重绑/final质量链。最终结果分别列确定性、native行为、分发安装与live GitHub事实。一个代表clean不能证明全平台Release或业务采用；没有执行的项保持未验证，不能把局部阻塞写为通过。

## 4. 停止条件与适用回退点

原始来源/关键前提缺失时，只停依赖该事实的判断和写入，回原incomplete/blocked；发现有效约束与已批准方案冲突，即使scope不变也按design第6节停点/三分流。协调者核实真实解决、受影响规划审核与候选重新匹配后恢复。不得迁就错误实现改测试预期。

native环境/trace/格式失败保留首次结果，通过原入口恢复，不补造public DTO或pass。before尚不完整时不宣称方法效果；方法差额依赖该证据时先完成样本。真实范围/authority变化进Clarify；机制变化回qualification与Architecture；规划有效的实现/断言缺陷留implementation/Check。

只编辑本Task明确文件，保留其他checkout和并行dirty内容。本项无生产数据迁移、部署或发布操作，没有数据回滚协议。回退只恢复本人未交付变更的精确preimage，不能重置用户工作。commit/push/PR/merge/资源删除分别遵守原owner和当前对话的精确副作用边界。

## 5. Delivery Policy（唯一）

选择`full`。D1覆盖全部R648-01..07、AC648-01..08，没有延期到#649/#651的本项责任。独立交付条件是：当前匹配before与新方法真实行为覆盖全部所选场景；原Markdown/示例只补实际缺口；canonical/installed投影和RDT一致；原candidate/finalCheck与完整committedReview真实通过；satisfying PR全部MERGED且可达live main。

整体Completion仍须核查全部accepted scope与结果，再由原Closure将#648置CLOSED/completed，原Finish完成归档bookkeeping并由原Cleanup处理选定资源。Delivery合并不等于Task完成。完整Release/多平台upgrade矩阵、业务现场采用和后继Issues属于明确边界，没有从本项转移的未完成责任。

## 6. Docs SSOT Plan（唯一）

选择`delta_first`。原RDT维护Skill准备`docs/requirements-design-test-contributions/648-constraint-premise-review/`的manifest、requirements、design、test、traceability，命中`docs/{requirements,design,test}/current/knowledge-maintenance.md`的来源/前提/真实对照/原owner方法部分。需求记录当前accepted行为，设计定位原Skill职责与不变公共边界，Test展开V648的输入/owner/观察及唯一实际结果位置。稳定身份和原#637/#638条件保持，无关导航不写。

直接consumer是原RDT candidate review、candidateCheck及final_integration。完整隔离目标在candidateCheck前可读；Check后由原owner对真实目标整合/读回，最终Phase2前完成reconciliation，再对实际after重绑并最终Check。不能把contribution proposed或源码改动称shared current/业务已采用。

Architecture沿当前no-impact处理，不建贡献、ADR或新baseline。若实际设计产生架构影响，原Author停止并刷新候选评估，按其实际结果补真实贡献；不得从旧no-impact直接晋升。workflow/spec/Skill公共可复用规则各归原canonical职责，不复制authority全文或新增全局摘要。
