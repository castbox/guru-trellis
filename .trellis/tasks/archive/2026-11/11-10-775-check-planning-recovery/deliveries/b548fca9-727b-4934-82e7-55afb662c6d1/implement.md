# D1：Check 规划回退交接与恢复实施计划

## 1. 输入与引用

读取[本批PRD](prd.md)、[design](design.md)及其第3节唯一来源设计处置、[整体PRD](../../prd.md)与Issue775完整正文。初始D1无前序交付；固定B为313d80215f65777fc70893a90c6d8dce8005d6dd，交付目标main。实施前加载原Check/Author合同、现有test_candidate_check fixture、适用workflow/skill-package/companion-scripts/quality specs、写作规范、设计列明的Architecture及RDT单元。所有原owner结果通过实际typed出口承接，不用phase或文件存在推定通过。

## 2. 有依赖顺序的步骤与文件责任

1. P1 原Author完成三正文、必要Architecture contribution和ADR候选、官方implement/check JSONL。Wording→原独立Architecture final_plan→Approval后展示具体规划，等待本对话计划接受；只有原Activation写Planning结果。
2. P2 原implementation coordinator加载trellis-before-dev并按项目dispatch规则运行trellis-implement。实现范围只在canonical Check package、原Author来源说明、workflow及同名consumer中；不改上游模型、全局包或其他Task。
3. P3 同一test_candidate_check fixture先扩V1/V2观察；原Check抽取共享planning_stale投影，修订route与scope决策一致性和输出schema；更新正式router到Author字段投影。真实scope变化使用Clarify，不删除真实scope_decisions。
4. P4 原Check recorder/schema增加planning_stale专用的最小rollback_binding；新增恢复profile、其私有恢复schema、interface/examples/命令说明。恢复分支不调用要求current Planning的普通_binding/checker；纠正使用原recorder dry-run，保留原结果。旧现场通过已有原公共Planning事实转换，缺证据走原blocked，不增第二checkpoint。
5. P5 在MIGRATION-775明确直接演进、成套采用及design第7.1节旧现场顺序：完整目标外provider的既有--root先恢复未变目标，原consumer接续后再合法采用工具；补invoke元数据/help的既有--root声明及目标公共API前置；更新Check/Author合同及workflow说明。原RDT/Architecture writers准备隔离完整拟写，保留原字节和必要关系，不提前改共享current。
6. P6 本框架开发checkout按原tools owner同步当前源码；旧业务现场须先完成P5所述恢复交接、停止复用旧结果，再沿其原tools owner更新目标，不能先改变旧候选工具字节。通过guru-upgrade-tools原owner预览并准备本checkout的matching受管写集，展示精确安装副作用并取得该写入确认后同步；保留当前Task、session和peer状态，处理实际sidecar。不得因普通apply历史Task阻塞改走迁移或手工覆盖。
7. P7 完成全部实现与隔离拟写，构造包含全部dirty增量的完整Candidate并begin_check。独立Architecture phase2和原guru-check-task候选Check覆盖完整内容；仅实际candidate_checked进入原维护owners final_integration/readback。
8. P8 原implementation owner重绑全部实际after并begin_check，执行最终Architecture/Check；之后原TaskCommit、完整committed Branch Review、Delivery Review/readiness和Publication。具体commit/push/PR副作用各按原门禁展示。PR目标main；发布后停止，等待协调器的合并处置。

## 3. 验证入口、输入与预期观察

| ID | 命令／入口与顺序 | 预期结果与证明边界 |
| --- | --- | --- |
| V1/V2 | 使用项目managed Python对 `trellis/skills/guru-team/packages/guru-check-task/tests/test_candidate_check.py` 的真实wrapper fixture运行unittest discovery | current_scope+reapprove_plan正式输出通过真实Author schema；实际回退后恢复/纠正/旧结果转换满足design第8节，不重复rework或写pass |
| V3 | 同包 `test_*.py`，并按改动依赖运行Author/router/public example/consumer与package结构相关测试 | 已有no-scope、真实scope变化和成功Check不回归；不为未改机制复制测试，不重跑独立Task创建前置 |
| V4a | 原source/installed package validator；源 `trellis/skills/guru-team/tests/test_skill_packages.py` 命中结构和projection验证 | 当前interface、profiles、schemas、examples、commands及consumer声明闭合；结构成功不代替语义验证 |
| V4b | 原tools owner完成本checkout matching同步后执行 `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh` 及命中的installed/mode/sidecar检查 | canonical、dogfood、声明平台投影一致，Task/session/peer不变；完整安装/升级/Release矩阵不在本批范围 |
| V5 | 对本次Python/Bash/JSON改动执行适用syntax/schema检查及 `git diff --check`；官方 `task.py validate` 按实际help支持入口校验本Task | 只验证实际改动与当前Task；不将文本命中或测试数量作为充分性门禁 |

运行命令前用已有managed resolver选择解释器，不安装系统Python依赖；根据实际文件依赖构造最小可靠测试集。V1/V2共享前置；旧格式转换只补新入口／转换实际改变的断言，明确外部完整provider的公开--root入口及目标工具未写入观察；目标工具发生真实变化时保留原stale拒绝，不把fixture称为安装全链验证，不重演业务现场、完整Intake/Author/native链或多平台矩阵。所有结果在实际执行后报告。来源工程事实仍适用时复用，只有新失败或未解风险才追加实验；不强制旧版红、反向rollback或多次同样回退。

## 4. 停止条件与适用回退点

- 身份、scope或来源真实变化：回原Identity/Clarify或受影响Planning owner，保留Task/Delivery和并行改动。
- 恢复缺原scope/plan因果来源或规划字节已变：原Check blocked/stale并给具体字段及原owner，不从当前值补造原事实，不以工具成功制造pass。
- 新机制改变candidate_assessment已评估边界：回原Author和独立Architecture；普通代码缺陷由原implementation修复，再按当前完整范围执行Check。
- 安装源、写集或sidecar冲突变化：回原工具owner重审；同一合法操作恢复用原recovery_ref，不能刷新旧preimage或覆盖用户修改。
- 必要验证未通过或缺证据：保留实际失败，原owner判断因果和最早修订点。设施反复失败时重评复现方式并说明未证结论，不制造绿色。

本批无数据库或业务数据迁移，也不执行部署。代码本地修订只处理本任务文件；不reset/revert其他人改动。证据足以支持全部本批验收且规定检查通过后停止追加测试；合并前必须等待协调器。

## 5. Delivery Policy（唯一）

选择full。D1覆盖R1、R2及AC1–AC3，无隐藏剩余修复或后继实现阶段。独立交付条件为：原交接通过真实consumer；已回退同对象可恢复或合法纠正；真实变化、缺原因果来源与旧结果迁移有明确原owner结果；命中回归、同步和完整质量链完成。

本批验收层为框架代码、实际公共wrapper fixture、schema/projection和命中installed/drift。未承诺业务仓部署、生产修复效果、完整native或Release矩阵；这些边界不是本批延期实现。Task-wide Completion仍须由原owner在Delivery实际交付后检查全部accepted scope。PR发布和Delivery合并均不自动代表Task完成。本执行段只到PR发布，不执行merge/Closure/Finish。

## 6. Docs SSOT Plan（唯一）

选择delta_first。原RDT writer为guru-maintain-requirements-design-test-ssot；原Architecture writer为guru-maintain-architecture-baseline。两者以本Task隔离完整拟写承接：

| 当前完整单元 | 本轮实际差额／直接consumer |
| --- | --- |
| docs/requirements/current/task-delivery-lifecycle.md 的R713 | 增补所有范围内规划回退可消费、原Check恢复及旧现场缺证据边界；consumer为后续Intake/规划/Check |
| docs/design/current/task-delivery-lifecycle.md 的D713 | 替换旧非空refs分支说明，明确最小局部binding与原owner转换；consumer为实施与审核 |
| docs/test/current/task-delivery-lifecycle.md 的T713-03 | 承接V1/V2/受影响回归与证据层次；consumer为后续Check/Review |
| docs/architecture/04-integrations/distribution.md 的公开执行资料与原生产能力 | 原交接与恢复职责、结果生命周期、matching采用；consumer为Architecture后续评估 |
| 原Check／Author package合同、workflow与MIGRATION-775 | 精确profiles/字段/薄投影和恢复操作唯一由原package拥有；consumer为正常业务Agent与工具owner |

原Author写真实Architecture contribution及ADR-CHECK-PLANNING-RECOVERY候选。原RDT owner生成task隔离R/D/T拟写，不直接改共享导航或扩大到其他Issue。独立Architecture与完整候选Check后，各维护owner在同Delivery final_integration重读实际目标并整合/readback；随后重绑after并执行最终质量链。并行目标变化只处理真实受影响差额，不覆盖别的贡献、不新增全局版本或共享登记。历史证据保留原观察；最终PR同时交付实现、公开合同和已整合当前文档。
