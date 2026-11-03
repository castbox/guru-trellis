# D1 实施与验证计划

## 1. 输入与引用

整体范围 .trellis/tasks/11-03-711-knowledge-navigation-isolation/prd.md 与公共accepted_scope，本批.trellis/tasks/11-03-711-knowledge-navigation-isolation/deliveries/92e40c5b-7dd9-48cc-8c44-a5691b31034b/prd.md、design.md第3节唯一来源处置、第8节冻结样本。实际完整加载共同current-knowledge、RDT/Architecture原contract、项目constitution/change-contract及命中完整R/D/T。采用原Architecture candidate_assessment的target_native，不将它当最终plan通过。首次D1无前序。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | 前置/原owner | 文件及行为 | 可审核完成观察 |
| --- | --- | --- | --- |
| I711-1 固定样本与旧侧 | 已激活Planning；测试实现worker | 在repo外建立一个代表安装及正常语料，按design第8节冻结事实/入口；保旧侧matching安装snapshot。执行旧实际Agent维护/Check/晋升及独立A/B，固定候选保首次冲突 | 原始首次轨迹、完整文件集、两序合并结果真实；host不提供阶段答案 |
| I711-2 共同规则/消费者 | 原implementation worker | canonical RDT current-knowledge、RDT SKILL/contract、managed RDT spec，Architecture SKILL/contract命中导航语句；必要bootstrap/project读取投影和公共README引用 | 不再要求独立主题写共享根/current/index/metadata；原profile/I/O/阶段门禁保留 |
| I711-3 迁移与候选知识 | 原RDT owner与Author/Architecture | MIGRATION-711.md，RDT隔离贡献及完整proposed当前知识/根/current入口，真实Architecture贡献/ADR和完整proposed根/治理/项目projection | migration未达/已达、在途、旧引用、alias、未迁移范围、恢复和旧写退出完整；shared current未提前写 |
| I711-4 分发与新侧 | 原tools maintenance owner/测试worker | canonical后从完整源guru-upgrade-tools更新本worktree dogfood，保持Task/session；同代表安装更新新侧，生成matching新侧snapshot | 原source/installed、平台投影、reapply/drift/mode/sidecar可核，无手工覆盖或未处置冲突 |
| I711-5 native与合并 | 具名测试worker；AI原owners | 执行V711-1..5；旧新相同实际模型/权限/等价起点，各侧独立，验收预期仅由host持有，不注入受测Agent；原native公开入口不改写输出 | 新侧独立两序无共同导航写入，完整知识可发现；真实重叠/迁移/改名删除语义正确。首次失败与修订重跑分开 |
| I711-6 候选质量及晋升 | 主协调/原Architecture/Check/RDT | 绑定完整implementation+proposed candidates；独立Architecture phase2、原Check候选；实际candidate_checked后原owners固定目标重读整合并写/readback | 候选出口不当最终通过；实际after全部paths再绑定begin_check |
| I711-7 最终质量交付 | 原Check/TaskCommit/独立Review/Delivery owners | 最终Architecture/Check→精确commit→完整committed Review→DeliveryReview/Publish/Merge→wholeCompletion/Closure/Finish/Cleanup | #711全范围真实证据齐备，交付与整体完成分开；无额外发布版本或业务部署 |

每次Phase2源/测试/task写前运行check-task-checkout-boundary。workers只执行此批准方案；新范围/compatibility/owner候选在写前回主协调资格判断，不自行扩张。保留他人并行改动。

## 3. 验证入口、输入与预期观察

V711-1..6的事实和预期唯一读design第8节；实际轨迹repo外，唯一RDT contribution test.md维护结果及边界。native使用可用codex exec公开入口及实际installed原owner；旧新同CLI/模型/权限，记录实际执行版本，禁止预载另一侧答案。实际原Check缺前置不得补pass；环境或调用失败保execution gap。

工程验证使用最小可靠集合：两个maintenance package原contract/runtime相关测试；新增确定性Git组合/引用校验仅检验其边界；source/installed skill-package验证、upstream ownership、三平台dogfood投影与canonical声明平台的可分发性、同代表安装reapply、drift、脚本mode/零未处置sidecar、workflow必要context读取、task validate、git diff --check及原质量规范内存Python syntax。具体脚本argv从各public --help/Interface读取，不猜私有实现。runtime/profile/API不改则不制造全生命周期或完整Release矩阵。

旧侧实际独立A/B首次冲突保留；新侧要求两顺序均不因导航/全局版本/历史冲突且双方事实/关系保留。整合owner另核组合语义，不用Git exit替代。V2必须同时区分current、accepted target、unpromoted和history。V4覆盖尚缺关系不能切换，补齐后原链切换，以及一个在途Task写真实迁移目标和结构变更。

## 4. 停止条件与适用回退点

Direct Source/accepted scope改变回Clarify；真实机制/职责边界改变回Author/Architecture；普通实现缺陷回原implementation，actualCheck/Review按其原route闭环。缺实际native能力只阻塞其依赖验收，不能减少样本或改成静态通过。canonical/installed冲突沿原tools owner恢复，不能绕过原Task库存门禁。

迁移未达条件保留原authority，候选proposed；切换后修复走原repair/受审successor，历史immutable不改。真实重叠由原owner按base/proposal/target整合；不得取单侧、重写B候选或强制串行掩盖。无业务数据/DB/部署变更，因此没有业务回滚协议；工具维护回退只用原固定preimages及原owner合同，不reset用户Git。

## 5. Delivery Policy（唯一）

policy=full。D1覆盖#711全部八项行为和全部验收：共同规则、真实消费者、原晋升边界、RDT/Architecture导航、可执行迁移、旧新实际Agent与独立两序合并、重叠/状态/迁移/结构样本、分发安装及本仓代表采用。没有计划推后到D2的Task内工作；若真实发现剩余义务，Completion保留并返回原owner，不宣称full完成。

独立交付条件为本批全部要求有对应当前证据，shared current沿原owners晋升且最终Check与完整Review覆盖。业务仓迁移/生产效果和完整多平台Release矩阵是明确非目标；分别报告未覆盖。Delivery合并不自动完成Task，仍由wholeCompletion判断全部accepted scope。

## 6. Docs SSOT Plan（唯一）

strategy=delta_first。原guru-maintain-requirements-design-test-ssot拥有RDT三层完整知识与trace；Author只写真实Architecture贡献/必要ADR，原guru-maintain-architecture-baseline独占独立评估与最终共享架构写入。implementation worker可准备完整proposed targets，不能提前写shared current。

命中RDT-REQ/DES/TST-KNOWLEDGE的current知识完整单元及必要根/current发现入口，Architecture ARCH-GOV-012/change-contract/根发现和项目读取projection。差额是独立导航、owner晋升判据、稳定检索、迁移切换与旧写退出；原条件、真实API版本、历史来源保持。导航中aliases逐个迁入原所属正文（仅缺失时），legacy未迁移及旧Task来源继续明确。

直接consumer是原maintenance final integration与Planning/实施/Check/Review读者。候选Check前贡献含完整拟写正文；candidate_checked后原owners固定真实目标、整合并写/readback；随后implementation重新绑定全部实际after进入最终Architecture/Check/commit/Review。公共源码、安装采用、文档迁移、native行为、确定性合并和远端交付分别记录。无变化对象不造空贡献/ADR，不把late正式结果回填受审正文自身pass。
