# D1：v0.7.0-guru.6 发布准备需求

## 1. 整体来源与术语

本批使用公共 Task `accepted_scope` 指向的 [整体 PRD](../../prd.md)，选择 AC1–AC6 全部准备责任；实际 DeliveryKey 和 planning_root 由原 Creation 返回。本批为首个 pull_request Delivery。

| 来源 | 章节、角色与用途 |
| --- | --- |
| https://github.com/castbox/guru-trellis/issues/656 | 全文要求；确定 .6、来源、文档及准备/发布边界 |
| .agents/skills/release-guru-trellis-version/references/contract.md | 完整两阶段约定设计；Task Commit、双完整 Review、串行整合和各副作用 owner |
| trellis/guru-team-extension.json；trellis/presets/guru-team/source/trellis-source.json | 当前版本与来源事实 |
| .trellis/spec/docs/public-docs.md | Install and Upgrade Prompts；本仓专属公开文档规范的唯一tracked来源，不进入业务preset；需修订当前过期映射 |
| docs/requirements/current/knowledge-maintenance.md；docs/design/current/knowledge-maintenance.md；docs/test/current/knowledge-maintenance.md | 当前知识身份、隔离拟写、最终整合及验证层次约束 |
| trellis/presets/guru-team/MIGRATION-669.md；docs/requirements-design-test-contributions/669-existing-implementation-reactivation/test.md | 累计集合中新恢复入口与受控验证边界 |
| docs/requirements-design-test-contributions/649-stage-result-convergence/test.md | 当前独立评测与实际收益、当前受控组合与安装观察；历史 false/no-grade/失败和限制 |

前驱指已发布 v0.7.0-guru.5；候选指包含准备交付和正常收尾后的真实 main commit/tree。本批不把准备分支当最终发布候选。规范性来源设计的唯一处置由后续本批 design 第3节拥有。

## 2. 整体与本批目标、非目标

本批独立目标是交付一致的 .6 准备内容：canonical revision、maintenance target/const、公开文档、必要当前断言、managed 投影和原知识收敛。当前差额是 Guru/maintenance仍.5，公开文档还将 .5写作未发布、使用旧稳定.4及旧Fork。消除这些冲突，保留真实历史。

本批覆盖整体 R1–R8、AC1–AC6 所需准备内容；整体 Completion 仍需独立判断全部准备责任和正常收尾。Stage2 exact-candidate、tag、smoke、Release、#656关闭由后续发布边界负责。继承整体非目标：不修改Fork或Backend，不实现#669等其它Issue，不做业务安装部署，不碰#649/#651/PR650资源，不扩完整累计多平台/native-host/生产/live模型矩阵。

## 3. 本批起点、前序结果、依赖与剩余责任

尚无前序 Delivery。本批从已包含 #669 交付和正常归档的 main 开始；Development B 在 design 中以真实 Git identity 固定，不以之后移动的 origin/main 作为内容范围。PR target 仍为 main。

依赖是当前 source lock 的 Fork79a97ed/CLI.5/pnpm10.32.1、已发布前驱.5自身的7bcbeaad/CLI.4、当前完整 Guru runtime和知识authority。源代码/单项CI/受控样本只保留原层次，不替代匹配构建或最终发布门禁。

本批没有预定D2。若准备范围仍有真实缺口，由原owner修订同批或按整体范围判断；不制造空Delivery。完成本批实际交付后，整体准备还要由Completion、Closure no_mutation、acceptance-finish、Finish/Cleanup原owners收尾。

## 4. 本批调用方、场景与流程

| ID | 调用方和条件 | 行为与可观察结果 |
| --- | --- | --- |
| D1-S1 | 发布维护Agent读取版本、maintenance和source锁 | Guru target/const同步.6；Fork锁/CLI/pnpm不随Guru发版变化 |
| D1-S2 | 安装/升级用户读取三份README | 稳定workflow/preset同.5 tag；候选用同一实际远端完整SHA与自身匹配Fork构建；未发布.6不作为provider |
| D1-S3 | 原Architecture/RDT和Check/Review owners消费完整候选 | 稳定规划→晋升前完整Phase2→TaskCommit→独立完整分支Review→串行整合→实际变化再Phase2/commit/独立完整Review |
| D1-S4 | 原Delivery owners消费最终当前结果 | Architecture publication与Delivery Review后Refs-only PR、expected-head合并；不因merge关闭#656 |
| D1-S5 | 来源/内容变化、普通失败或输出丢失 | 原owner重读/恢复同身份及受影响门禁；不复制历史pass，不补写动态发布状态 |

## 5. 完整行为、条件与约束

- D1-R1 / 整体R1/R2：revision和maintenance的current目标及对应输出/consumer const改为0.7.0-guru.6。保留Fork79a97ed、CLI/Core0.7.0-castbox.5、pnpm10.32.1；前驱manifest/lock独立核对为.4。只调整真实current expectation，不批量替换历史fixture或证据。
- D1-R2 / R3：更新root/workflow/preset三份README及canonical public-docs。准备期稳定tag仍.5；候选workflow与preset同一实际immutable完整SHA，依该树source lock构建。不提供未发布.6安装命令，不凭CLI版本号选择错误构建。
- D1-R3 / R3/R4：canonical先修改，再通过原preset/overlay分发到dogfood/installed/声明平台，保留用户区块与原冲突处理；无未解决.new/.bak。公开知识入口保持guru-trellis-rdt / guru-trellis-architecture，原owners收敛完整适用知识，不强制总版本递增或重写历史。
- D1-R4 / R4：累计发布说明承接实际.5..最终candidate diff，包含#669的新恢复能力而不重做实现。#649的false/no-grade、合法路由期待差异、历史失败及#669受控原生、正式来源维护和Backend生产未验证边界准确保留；不得泛称全部验证通过。
- D1-R5 / R5：晋升前和晋升后各有覆盖其实际完整内容的Phase2、原TaskCommit和独立origin/main...HEAD Review。零开放P0–P3才串行最终整合；晋升前结果不供晋升后复用，当前知识/代码/验证义务变化回最早受影响owner。
- D1-R6 / R6/R7/R8：原Architecture publication、Delivery Review、Publish和Merge拥有最终准备PR；中文payload只Refs #656。副作用分别展示并确认，脚本不替代判断。Task Completion/Closure/Finish/Cleanup与Stage2各自独立。无tracked动态状态、body handoff、授权持久化或自引用证明提交。

## 6. 本批验收、验证方式与未决项

| 本批验收 | 整体验收/要求 | 入口与预期观察 |
| --- | --- | --- |
| D1-AC1 | AC1；D1-R1 | canonical/maintenance/output与consumer const定向验证：一致.6，source lock和CLI/pnpm保持 |
| D1-AC2 | AC2；D1-R2/R4 | 全文检查三份README、canonical public-docs及知识差额：稳定/候选/历史轴明确，累计能力和证据边界准确 |
| D1-AC3 | AC3；D1-R3 | source/installed、四投影/私有发布skill parity、ownership、三平台reapply与drift：字节/权限一致，零未处置sidecar |
| D1-AC4 | AC4；D1-R5 | 两轮完整Phase2/TaskCommit/独立完整Review，串行原知识整合及actual after重绑：每轮无开放P0–P3，原已完成晋升不重放 |
| D1-AC5 | AC5；D1-R6 | 原Delivery链与整体Completion/Closure/Finish/Cleanup：Refs-only准备合并及正常准备终态，不关闭#656 |
| D1-AC6 | AC6；D1-R6 | Task和交付差额检查：无动态发布账本、body handoff或授权记录；没有以准备结果宣称Stage2通过 |

需求阶段没有阻塞性的产品选择。具体current const、测试选择与完整知识拟写落点在独立candidate assessment之后由Author细化；缺失authority按原owner处理，不预填未来方案或通过。

## 7. Canonical 引用与本轮差额

- Requirement/behavior：整体PRD R1–R8、live#656全文；知识规则RDT-REQ-KNOWLEDGE的“唯一authority与完整知识”“四profiles、日常闭环与晋升”“阶段适用版本与实际变化”。本轮改变软件版本/当前公开映射，不改变知识owner或全局升版规则。
- Design：私有release contract的Stage1/Stage2、Forbidden Persistence和Independent Mutation Confirmations；RDT-DES-KNOWLEDGE中独立owner与最终整合关系。本轮沿现有机制执行，没有新流程分支或公共Skill。
- Test：RDT-TST-KNOWLEDGE的证据层次与T638最终整合边界，以及原私有release contract稳定可执行入口。准备定向证明与最终同candidate门禁分开，不继承旧矩阵pass。
- Architecture：docs/architecture/README.md、00-foundation/design-constitution.md、06-governance/change-contract.md及04-integrations/distribution.md。独立Architecture先审实际版本/分发候选及受影响consumer，再由原owner确定真实影响、贡献和整合；本批不预定impact结论。
