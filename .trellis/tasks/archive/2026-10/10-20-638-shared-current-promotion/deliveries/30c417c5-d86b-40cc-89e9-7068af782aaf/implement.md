# D1：共享知识晋升实施与验证计划

## 1. 输入与引用

整体范围由 [root PRD](../../prd.md) 及已接受scope拥有。本批输入是 [D1 PRD](prd.md)、[design](design.md)；规范性来源设计仅在design第3节处置。固定B/H0=`9cec623833b61814f1175f31acde4fa81334cdb0`，D1没有前序Delivery，目标`castbox/guru-trellis:main`。不启动#635。

实施前加载design引用的完整知识合同、候选适用性合同、Architecture constitution/change-contract、命中的RDT/current完整正文，以及实际package代码/schema/consumer。只列链接不证明已读。清晰写作规范、Skill I/O/private-state、subtraction-first、validation value和validation scope规则适用于本批实际工作。

当前仅首次Architecture candidate_assessment完成。Wording、final_plan、Approval及Activation尚待各原owner真实完成；本文件不表示已激活或实施完成。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | 前置 / owner | 实际文件、行为与完成观察 |
| --- | --- | --- |
| I638-01 接口和迁移 | Activation；implement worker，原语义owners负责判断 | 在`trellis/skills/guru-team/packages/guru-maintain-architecture-baseline/`增加Arch5.0/Delivery3.0当前schemas/examples/consumer投影，迁移`runtime/invoke.py`与`promotion.py`；删除普通promotion的总入口必写/distinct successor/全局README token依赖，bootstrap仍保持distinct successor。旧runtime入口退出，历史schema保持原义。产物能通过真实wrapper检出普通mismatch且接受稳定identity的实际目标写入 |
| I638-02 候选Check与RDT | I01；原Check/RDT包，implement worker | 原Check新增`delivery_candidate_check`/`candidate_checked`、6.0 private payload及唯一consumer；不记录final public Check。RDT impact/promotion2.0和candidate_ready独立output，保留no-change。命中`runtime/delivery.py`、record/check/common、Interface/commands/registry选择及明确schema，不改官方Task/Delivery模型。通过wrapper观察拟写/已写不同结果 |
| I638-03 控制面和消费者 | I01/02；canonical workflow及原skills/spec owners | 修改`trellis/workflows/guru-team/workflow.md`全局编排；原Arch/RDT/Check/Review/Delivery/Publication/TaskCommit/Author/Approval的命中合同和`trellis/presets/guru-team/spec/workflow/`保持新顺序。workflow不复制step-local内部行为。更新两个README和MIGRATION-638，所有新出口有唯一consumer，Ready/Finish不消费candidate_checked或reviewed_candidate |
| I638-04 隔离正文与代表迁移 | I03；implement writer及原RDT/Architecture维护方 | 写本Task RDT contribution五件套及完整proposed正文；Architecture contribution/必要ADR候选按design§9。迁移知识维护、命中生命周期及必要Architecture完整单元；根README稳定identity/薄导航是本次切换内容，之后普通Task不强制再写。不触碰其它Task贡献或历史归档。尚未晋升时共享current保持原状 |
| I638-05 定向测试和实际安装 | I01..04形成可审候选；trellis-check worker/原验证owners | 按§3执行生产wrapper、公共投影、direct consumer和一个representative clean install/reapply；新增测试只检测独立行为，不锁mutable配置或照抄实现。运行实际Agent样本，host不填pass。保留首次失败/修复和层次边界 |
| I638-06 dogfood与工具切换 | matching完整source已形成；原installer/tools owner | canonical overlay变化后原`apply.sh --repo .`和drift；如legacy archives阻塞，记录未通过并保留归档，走原支持的matching tools升级，不局部复制。workflow通过官方preview/显式apply同步；不改上游、全局npm或node_modules。需要commit/安装副作用时在原边界展示精确计划 |
| I638-06a local-clone 来源恢复 | 新 candidate assessment、Wording、final_plan、Approval、Activation；原 installation/tools 实现与审核 owners | 按 design D638-06 直接修改 `guru-upgrade-installation/runtime/owner.py` 的原 manifest/source reader；`owner.py:preview`、`guru-upgrade-tools/runtime/tools_owner.py:inventory`、`delivery_upgrade.py:old_installation`/preview 传原已选完整 source。补真实 installer receipt、已删除旧 clone、exact object/metadata/preimage 的定向测试。原 GitHub、dirty 和 unknown-preimage 行为保留，不新增 public DTO 或第二来源路径。定向验证后从完整匹配 source 重新原 preview→prepare→独立安装边界→invoke/readback/recovery，保全本 Task/session/peer 和用户配置 |
| I638-07 首次候选检查 | I05/06可用；原implementation、独立Architecture与Check owners | implementation在implementing按固定B、实际HEAD及完整差额paths调用candidate/begin_check，进入checking。独立Architecture/Check读取完整实现/拟写及消费者；原Check选candidate_checked时先合法rework到implementation，只清readiness、保留planning和既有真实历史，再发给final integration，不写Check gate或进入TaskCommit |
| I638-08 最终整合与最终质量 | I07后公共phase=implementing；原两maintenance、implementation及质量owners | 固定真实目标，#637补真实组合差额/消费者，原owners写入读回。implementation以同B、实际HEAD及全部晋升/关系/导航paths重建candidate并begin_check回checking；最终Architecture/Check校验新content_ref并覆盖实际候选，只有finalCheck record_gate进入reviewing。无知识变化也走合法candidate回程，无空文件/提交。随后TaskCommit和独立committed Review/readiness |
| I638-09 实际交付与终态 | I08及对应副作用授权；各原owner | 原Publish/merge、Completion、Closure、Finish/bookkeeping、Cleanup分别执行和readback；只用实际终态证明完成。此计划不授予commit/push/PR/merge/closure/archive/cleanup权限，不持久化授权 |

canonical之外的`.trellis/guru-team/`、`.agents/skills/`、`.codex/skills/`和平台入口是受管投影；不能只改运行副本。所有非生成触及代码文件检查3000行阈值；超过时先由原owner审核并做必要机械拆分，不借本批重构无关模块。

## 3. 验证入口、输入与预期观察

命令使用匹配managed Python；当前已解析解释器位于`/Users/wumengye/Library/Caches/guru-team/python/c5898e3ddcd9197c2cc683bf/venv/bin/python`，执行时通过`.trellis/guru-team/runtime/resolve-python.sh`重新解析，不把该本机路径写入公共package。

| 顺序 / design验证 | 入口与实际输入 | 预期观察与边界 |
| --- | --- | --- |
| T01 / V01/02/04 | `python -m unittest discover -s trellis/skills/guru-team/packages/guru-maintain-architecture-baseline/tests -p 'test_promotion.py'`及本批新增final-integration测试文件；真实临时Git、两组贡献、stableidentity、普通mismatch/partial/output-loss | 当前wrapper接受不同能力独立target与无总入口写入；同单元组合保留条件；当前拒绝旧shape。fixture只证明deterministic层，不声称AI合成成立 |
| T02 / V03/04/05 | RDT、Check的命中`tests/`与`runtime/delivery_projection/tests/`；真实begin_check/rework/写入/重新begin_check/finalCheck及same-key恢复 | 公共phase逐步为implementing/checking/implementing/checking/reviewing，写前后content_ref不同且旧candidate被拒绝。候选Check无publicgate，finalCheck才记录；planning/key/B保持，旧覆盖仅作历史。no-change无空文件；输出丢失恢复不直接改state |
| T03 / V05 | Review/TaskCommit/Delivery Review/Publish命中contract及flow测试，current selectors/source package validator | 全部直接consumer接受新时机及Arch输出，最终Ready拒绝未晋升或缺最终覆盖。现有初次/修复/无Git整合路径保持；无实际义务不跑完整无关suite |
| T04 / V06 | 原preset source validator、canonical/dogfood drift、声明平台projection/mode、Markdown本次链接与旧Gitref检查 | 当前source与投影一致、历史引用解析、无用户内容损失；静态成功不等于运行行为或Release矩阵 |
| T05 / V06 | 一个matching source clean native Codex安装；同样本完整preset reapply，在途Task/Delivery public文件/phase/selection比对，`.new/.bak` inventory | 匹配CLI/Core与package从零可用；reapply保全。若普通仓库apply命中legacyarchives写前阻塞，单列失败；matching tools-only及fixture结果分开 |
| T05a / V06a | installation/tests 新增 local-source receipt 行为用例；原 `test_dirty_source_provenance.py`、`test_contract.py` 命中 source-reader cases；tools `test_native_install.py`、`test_recovery.py` 与 installation `test_delivery_upgrade.py` 命中 callers；最后执行本 Task 原 tools preview/prepare/invoke | 使用真实 Git 对象和原 producer/consumer，观察旧 clone 删除后精确旧 bytes 可恢复、不同新 HEAD 不替代旧 source、缺失 object/clean metadata mismatch 在写前停止。GitHub/dirty/unknown preimage 既有结果不退化；实际 target 安装及其同操作恢复单独记录，不从 fixture 推断通过 |
| T06 / V07 | design§8冻结的不同能力双Task、同单元双Task、no-change/无需Git整合样本，由真实nativeAgents读写和调用原installed owners | 正式候选review、原owner合成、实际写入后完整差额/未改consumer覆盖分别有真实public输出及Git；不从host预填DTO、目录名或最后retry推断成功 |
| T07 / V07 | matching已安装#636早期Draft入口、#637覆盖适用性和本轮finalintegration链；同Task/key与同PR身份 | Draft保持非最终结果；后继真实变化按#637判断；最终Check/Review/Ready只消费实际最终内容。远端写入另按具体授权，transport与真实GitHub层分别记录 |
| T08 / V08 | 本D1原正式Check、TaskCommit、完整B..H Review、Publish/Merge和终态readback | 实际源码/文档同PR交付；Issue closure、Task Finish和Cleanup都取各自最终结果，不因单次merge宣称整体完成 |

新增case分别捕获全局identity依赖、提前晋升、候选被当finalgate、同单元条件丢失、未改consumer漏审、普通恢复/旧入口误接续；不为每个文本短语加固定字串断言。命中红测先定位与本轮因果，证明无关就停止扩展；不能删历史或弱化断言制造绿。#637记录的Check两项失败、Architecture整组未完成及formal source lock只作调查线索，本轮用当前输出归因。

唯一长期结果文档为本Task RDT contribution的`test.md`。记录命令/受检对象、真实结果、原结果适用性、首次失败及未验证边界；不复制完整raw transcript，不创建review/test账本或授权记录。公共Task结果、Git和当前正文提供可重读事实。

## 4. 停止条件与适用回退点

live Direct Source、scope或必要依赖变化时，停止受影响步骤并回原Clarify/Author/Architecture；技术细化和mapped恢复自动接续。独立review缺实际执行或输出、拟写正文不完整、组合前提变化、消费者覆盖缺失时不晋升或不Ready。普通target mismatch先读真实差额再由原owner处理，不覆盖已合入条件。

schema/consumer/freshness验证失败结束该invocation，原owner重新读取并新一轮判断，不能把错误当pass。实现、接口、验证义务改变时回原相应quality owner；不能用promotion-reference-alignment处理实质正文变化。缺测试环境/正式source lock/外部证据如实标未验证，不以重复retry或静态结果替代。

local-clone receipt 的旧对象缺失或 clean metadata mismatch 时，停止依赖它的 preview/写入并返回原维护 owner。preimage 不能唯一恢复时，保留 unknown preimage 并继续只读 preview；原维护 owner 完成原 preserve/replace 判断前，不进入 prepare 或目标写入。不得改写 receipt、从新 HEAD 补旧 hash 或要求已删除目录复活。实际安装仍有独立精确 write-set 边界；本规划不授权执行尚未展示的 tools 写入。

本地实现修复保留无关dirty与untracked，stage仅本批明确路径。安装失败保留用户内容及原受管恢复结果；shared entry尚未切换时保持原authority。无数据库/服务部署，因此没有新增DB回滚或生产恢复协议。Git/GitHub、archive与cleanup仍由各自原owner展示并确认精确动作。

## 5. Delivery Policy（唯一）

Policy=`full`。D1覆盖整体全部R638-01..07和AC638-01..07，没有拆给后续Delivery的实现、current文档或验收责任。完成条件是实现/公共合同/长期正文同一最终PR交付，全部适用验证及独立审核有真实结果，必要未验证边界不冒称通过，再由整体Completion判断全部scope。外部业务采用与完整Release/升级矩阵是整体非目标，不伪装成延期本批义务。

原Delivery Review检查本Policy，不成为规划writer；一次Delivery合并仍不等于Task Completion。若整体scope实质改变，回原scope/Planning，而非静默改成partial。

## 6. Docs SSOT Plan（唯一）

Strategy=`delta_first`。原RDT writer维护`docs/requirements-design-test-contributions/638-shared-current-promotion/{manifest.yaml,requirements.md,design.md,test.md,traceability.md}`及完整`proposed/`正文，原Architecture writer维护本Task贡献与必要ADR候选。Planning阶段只写真实task-owned贡献；实施阶段形成完整拟写正文；首次候选Check前shared current不改。

直接consumer是原Architecture/RDT assessment/promotion、候选Check、最终Check、独立BranchReview与Delivery/Completion。命中RDT knowledge-maintenance和生命周期正文、Architecture current/domain/integration/governance/change-contract与必须定位的新ADR；关系/根入口只写真实差额。来源设计处置仅引用design§3，不在此复制矩阵。

在同Delivery最终整合阶段，两原maintenance owners读真实target并晋升完整正文和必要关系，随后最终Phase2 Check/committed Review检验所有实际变化。当前Task若仍使用固定旧完整安装，遵守其实际旧门禁；采用新时机前必须通过原matching tools/installation owner成套切换并验证同key保全，不以source编辑热迁移。此迁移/安装边界由MIGRATION-638明确；本计划不跳过当时实际运行合同。

无变化能力/层说明无影响，不填空贡献/ADR。历史版本、旧引用与未迁移scope保持可读，普通查询不回放贡献链。canonical与dogfood/installed验证、实际Agent行为和远端事实分别报告；在最终Check前完成真实reconciliation，不把首次晋升留到Review或未来文档PR。
