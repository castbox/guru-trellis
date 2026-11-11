# D1：按当前出口查询与按步加载实施计划

## 1. 输入与引用

[整体PRD](../../prd.md)全部已接受anchors、[本批PRD](prd.md)全部范围和[design §3](design.md#3-来源设计处置唯一)唯一来源设计处置为输入。独立Architecture候选评估由design §1承接，不降低其约束。没有前序Delivery；B/H0和PR目标见design §1。

实施与Check实际加载design §4–8、canonical workflow/Interfaces、ADR-035、清晰写作规范、skill-package-contract、workflow-contract的consumer continuity、quality-guidelines的Test And Validation Value、subtraction-first及原current-knowledge合同。它们分别限定I/O和路由、正常场景、最小验证、文件拆分及隔离知识晋升。引用不是已加载证明。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | 前置与owner | 文件/改动及可审核观察 |
| --- | --- | --- |
| I1 单图和加载正文 | 完成Wording/final Architecture/Approval/Phase1接受及Activation；实现owner | canonical workflow和新references/routing.md、legacy.md：保留原标记、条件及恢复，重排Phase Index/唯一continuation。观察一个图引用、当前提取及原legacy可达。 |
| I2 reader及查询 | I1布局；runtime owner | installed.py、discovery.py及原runtime tests：共用reader、显式layout/完整图校验和最小出口投影。公开wrapper覆盖合法/错误/演进，无exit兼容，无语义router。 |
| I3 直接consumer | I1/I2；原compatibility/preset owner | verify_trellis_compatibility_matrix.py reader/snapshot/preview、MANAGED_ASSET_PATHS及定向测试：同一reference、matching preview root；遵守3000行拆分规则。 |
| I4 说明/迁移 | I1–I3；各Markdown原owner | workflow/preset两处README、MIGRATION-792.md、实际受影响spec及Claude/Codex等overlay/Skill references：明确I/O/恢复/matching，不复制内部步骤或改#793/#794。 |
| I5 原安装与观察 | I1–I4定向回归；guru-upgrade-tools原owner | 完整匹配源沿原maintenance入口同步dogfood，保留Task/session，逐项处理sidecar；installed/drift与V6实际AI消费。不得手工覆盖受管副本。 |
| I6 完整知识候选/候选Check | 实现及V1–V6实际证据；实现和原RDT/Architecture owner | 本planning_root隔离Architecture/ADR及requirement/design/test完整拟晋升正文；如实写证据限制，candidate Check不冒充最终Check。 |
| I7 最终整合/复核 | 独立Architecture及candidate Check通过；原owner | final_integration晋升，重建同B完整candidate，begin_check和最终Check/commit/full Review按原流程；共享差额进入最终完整范围，停在merge前。 |

代码前加载trellis-before-dev和实际package specs。需要Agent时沿当前workflow原dispatch，不改平台配置。没有必须留后继Delivery解除的临时功能限制。

## 3. 验证入口、输入与预期观察

| 验证 | 入口和输入 | 预期观察/边界 |
| --- | --- | --- |
| V1/V2 | 原discover-skill-contract.sh，source及installed模式，真实producer/exit；runtime原unittest入口及新增出口用例 | 合法Skill/workflow/stop/instruction-only合同可消费；普通错误停止；合法演进自动更新，无exit兼容。断言来自真实Interface和正文。 |
| V3 | 原get_context.py的phase/step/continuation入口（先按--help确认argv）；test_active_task_continuation_integration.py和新增提取覆盖 | 当前步骤和唯一continuation可用、必要约束/恢复保持，upstream无修改；不靠长度阈值。 |
| V4 | 原guru-maintain-legacy-task入口和完整references，legacy相关原出口查询 | 原支持/准确来源可读，普通路径最短转交；不实际批量维护。 |
| V5 | 原package/source/installed validators；compatibility reader/snapshot/preview定向用例；bash trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh | matching图/资产一致，原tools更新保留Task/session，冲突/sidecar如实处置；不调用完整矩阵。 |
| V6 | 更新安装后的公开context入口及一次真实出口查询，AI实际读取entry和consumer前置；普通接续/维护读取各一条 | 实际正确接续或stop，读取范围满足当前步骤；与静态/分发证明分开。 |
| 最终 | candidate Check→原知识晋升→rebound final Check→完整range Branch Review | 全R/AC及真实共享差额/migration；未执行链路保留限制。 |

先跑最接近行为的V1–V3长期回归，再补V4–V6真实消费/采用。只有accepted范围确需证明clean安装时最多一例；不承担完整升级/Release矩阵。具体残余风险才追加实验，不安排惯例红绿、重复回退或固定成本指标。

## 4. 停止条件与适用回退点

Task/key/selection/scope不匹配回原Identity/Bind/Selection/Clarify，缺producer输出回原producer。来源/范围变化停止受影响步骤回Clarify；机制变化回Author candidate与独立Architecture。不能从文件存在补pass。

graph/reference错误停止查询并回原Markdown/Interface owner。安装遇current-only/legacy或sidecar阻塞留原tools owner，不绕过preflight或手工覆盖。验证失败回实际实现/规划owner；设施反复失败先重评有界复现并明确证据缺口，未解决不预填验收。证据充分后停止可选验证。

没有DB迁移、服务部署或远程发布恢复。仅有界修复本任务本地文件，保留无关并行改动。commit/push/PR沿后续原边界；不stage无关文件。merge由协调方处理，本聊天止于merge前。

## 5. Delivery Policy（唯一）

**full**。D1完整承担已选全部R792与AC792：查询、当前加载、legacy按需、实际reader和受影响分发/采用，没有延期必需实现或未分配后继。

完成条件是实际实现、独立断言、必要安装/AI加载观察、matching迁移说明及知识晋升完成，并通过原最终Check和完整Branch/Delivery Review。当前尚未取得这些结果；Policy不是通过声明。D1合并不等于Task Completion，整体仍检查全部accepted scope、历史结果和剩余义务。发布、merge、Closure/Finish由原owner独立判断；本聊天不merge。

## 6. Docs SSOT Plan（唯一）

strategy：**delta_first**。先在本planning_root准备真实、完整、可审核拟晋升正文。原RDT owner承接requirement/design/test contribution，原Architecture owner承接architecture-contribution与必要ADR。candidate Check后由原owner在final_integration核live expected-current并晋升，最终Phase2前reconcile，再把实际写入纳入最终Check。规划不直接写共享索引/baseline。

| canonical目标/差额 | 原writer及直接consumer | 时点/限制 |
| --- | --- | --- |
| docs/requirements-design-test-contributions/792-step-context/{requirement,design,test}.md及必要原导航 | 原RDT owner；Check/Review/Completion、维护者 | 完整正常场景、reader/查询/加载/legacy与实际V1–V6；执行后写真实test结果。 |
| docs/architecture/contributions/792-step-context.md、docs/architecture/adr/step-context-loading.md及必要baseline投影 | 原Architecture owner；final Check、Review及未来维护 | 当前隔离贡献/ADR提案先审；实际证据更新后刷新，完整拟写内容在原final_integration晋升。 |
| canonical workflow/README/MIGRATION-792、适用spec/overlay及dogfood | 各原产品/安装owner；AI调用方、安装者 | I1–I5产品内容进入完整candidate，不能替代知识晋升。 |

历史归档及旧观察保持。不新增ledger、授权记录或位置缓存；共享导航只由原owner在真实晋升时写。无临时功能限制需要后继解除文档。
