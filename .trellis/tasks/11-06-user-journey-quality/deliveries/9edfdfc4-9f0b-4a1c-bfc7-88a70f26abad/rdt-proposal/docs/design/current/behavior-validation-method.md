# 行为测试与因果验证方法的职责设计

Identity：RDT-DES-BEHAVIOR-VALIDATION；别名：D735/CON735。原语义 owner：guru-maintain-requirements-design-test-ssot。来源：Issue #735；状态 current。变更起点 main@b78edbbdc32e77392bc3775366473971050ccb4b；精确当前定义由包含本文件的 Git revision 绑定。晋升依据：原 candidate_checked 后，原 RDT owner 完成 final integration 写入与读回；不预填最终质量或交付结论。

## D735-01 / CON735-METHOD

承接R735-01/03。quality-guidelines Test And Validation Value 单写通用验证方法，Author planning-body 和 design/implement 原验证章节加载并应用；Phase2 派工、Check/Branch 原职责引用同一正文，避免复制第二套标准。确定性 runner 只运输事实和采集输入/工具/输出，AI 判断行为与证据边界。

## D735-02 / CON735-ADMISSION

承接R735-02。guru-qualify-root-cause 在原修复候选条款区分证据充分性与实验形式，并保留普通功能、诊断、缓解、修复、保护的原分类。没有新状态/字段；原阶段 owner 依据实际结果判断完成。共用 causal-completion-semantics 的证据维度不复制到本单元。

## D735-03 / CON735-ADOPTION

承接R735-03。沿现有 package/spec/preset 和 tools maintenance 分发完整 canonical/dogfood/installed 与实际声明平台。工具维护保留 Task/session；不手工覆盖受管副本。真实语义观察与结构、分发和正式交付证据分别报告。单一方法增量的维护成本为原正文/引用和定向评估，不引入固定重跑、时间限额、理由文件或兼容双读。来源行为、证据需要或原owner变更时重新判断影响。

## 关系

需求：docs/requirements/current/behavior-validation-method.md R735-01..03；测试：docs/test/current/behavior-validation-method.md T735-01..07。Architecture 对 #735 原变化的 no impact 使用其原独立结果，该历史范围不制造贡献/ADR。quality/root/Author canonical 精确合同保持唯一来源。

## D-JQ-JOURNEY / CON-JQ-METHOD：原职责内的方法增量

承接 BEH-JQ-JOURNEY；适用来源为 Task `user-journey-quality` generation 0 的已接受整体范围和 D1 方案，相关说明为 Issue #747。新增方法已落实于 canonical 合同和必要消费者，现有 D735 职责不被替代。本次 JQ 定义由该 Delivery 的实际 candidate_checked 后，原 RDT owner 在 final integration 整合并读回；当前定义由包含本文件的精确 Git revision 绑定。方法实现、有限行为观察与受管采用分别判断，最终 Check、Review、Delivery 和 Completion 仍由原 owner 的实际结果建立。

Clarify contract 的 Discover the actual choices 负责连续正常动作及真实选择发现。Author planning-body 负责在所属 PRD/design/implement 展开行为、阶段交接机制及验证顺序。交接条件依当前实际 writer/reader 和资源归属展开，不引入新的 scope writer 或公共状态。

quality-guidelines 的 Test And Validation Value 单写最小完整旅程的风险/依赖选择、实际入口、替身语义及代表性输入方法；Author 模板与 Phase2 消费引用，避免平行标准。review-sufficiency 单写独立问题推导，原 reviewer 首读与隔离优先；Architecture 在自身 authority 顺序内判断，不预载实施总结作为问题答案。

去敏过程例子在原 Author examples 内教学，不作为当前用户回答或验收。实际 Agent 采集沿已有执行方式，collector 运输输入、工具及输出，原审核 owner 判断语义。维护成本限于原正文、必要消费者与定向观察；没有新 Skill、gate、DTO、runtime/schema、账本或固定矩阵。需求/来源、真实入口、依赖或证明层级变化时重新评估相关方法及证据。

既有无影响架构结论仅对应 #735 的原变化。本方法增量的职责关系由 ARCH-REVIEW-SUFFICIENCY 的原 Architecture 本次晋升及后续阶段判断；不能将历史 no impact 扩张为本轮结论。

关系：BEH-JQ-JOURNEY → D-JQ-JOURNEY → T-JQ-NATIVE/T-JQ-DISTRIBUTE；共享独立审核关系由 docs/design/current/review-sufficiency.md 的 CON-JQ-INDEPENDENCE 承接。


## D-JQ-JOURNEY 当前方法修订候选

本段是同一 Task/Delivery 的拟晋升差额，基于 Git `7b14b6f83f274bd3b08e2721be8624516374b73d`。Clarify contract 在原连续旅程段反推最终结果并正向核对承诺；Author planning-body 在原来源读取与自检职责内承接完整单元加载、条件保全和最终观察对应。真实未决分支不替代独立明确的普通完成路径。教学 process 说明局部确认不提交及普通最终保存的服务端一致性观察，保持来源已有字段和真实未决项。

原职责、单一方法来源、受管分发及知识维护关系不变，无新公共合同或持久状态。原 Architecture 独立判断本轮无职责和知识关系差额；当前阶段判断仍由原 owner 亲自执行。完整读取不能单独证明模型持续保全原承诺；实际效果须检查独立产物，不能从规则增加推定改善。


## 当前同批方法与证据差额（完整拟晋升，未生效）

适用基础为 Git `7b14b6f83f274bd3b08e2721be8624516374b73d` 的原完整单元；现有 identity、历史晋升和原观察保持。本节是 Task user-journey-quality、generation 0、同一 Delivery 的 proposed 差额，尚未共享晋升。

Author planning-body §2 的来源等价比较、§3 的 design 展开和同对象推演、§5 的复核分别服务原承诺保全、实际机制形成和正文一致性。design 形成之初先带入关键条件与结果，再细化接口/状态/顺序；内容变化后既说明旧结果适用边界，也连接新内容取得匹配结果到普通成功终点。具体结论写回原 design 所属段，不制造表或账本。必要读取/恢复/结果合同缺失由原合同/工程职责补齐，只阻塞依赖分支，不能偷换为更窄需求。方法的唯一细节仍由 canonical planning-body 拥有。
