# #638 降低共享知识晋升争用：整体需求

## 1. 来源与术语

| 来源 | 章节与角色 | 本 Task 用途 |
| --- | --- | --- |
| [castbox/guru-trellis #638](https://github.com/castbox/guru-trellis/issues/638) | 目标与行为、最终合入准备的精确定义、验收、边界与依赖；Direct Source，exact_source | 完整要求；本轮 live OPEN、updatedAt=2026-10-19T16:24:34Z、无评论 |
| [完整知识合同](../../../trellis/skills/guru-team/packages/guru-maintain-requirements-design-test-ssot/references/current-knowledge.md) / [当前完整设计](../../../docs/design/current/knowledge-maintenance.md) | 原 #331 的完整正文、稳定身份、薄导航、贡献隔离与历史；现行约束 | 保留原子能力，只演进本轮阶段/身份差额 |
| [候选适用性合同](../../../.trellis/spec/workflow/workflow-contract.md#candidate-applicability-and-coverage) / [ADR-034](../../../docs/architecture/adr/034-candidate-applicability-and-coverage.md) | #637 的首次完整独立审核、真实差额与工程事实适用性；现行约束 | 消费原机制，不另建复用体系 |
| [Architecture](../../../docs/architecture/README.md) / [constitution](../../../docs/architecture/00-foundation/design-constitution.md) | 起点 .105 与 guru-trellis-design-constitution-v1；架构约束 | 保留原 owner、完整职责和唯一 authority，按真实阶段适用性承接 |
| [#637 Test](../../../docs/requirements-design-test-contributions/637-candidate-review-reuse/test.md) | 历史实际验证与未验证边界 | 本轮承接 #636/#637 实际安装接口组合，不继承旧 pass |

**完整知识单元**是按能力或职责组织的唯一完整正文及必要关系，身份不随展示顺序变化。**精确快照**由 Git 提交定位；真实公共 API/合同版本仍保留原兼容含义。**拟晋升正文**是尚未写入 shared current 的完整候选，不是第二 current authority。**最终整合阶段**是同一 Delivery 固定候选上完成最终知识写入、补充审核并进入原 Ready/Merge owner 的边界，不是 Git 同步门禁或队列准入。

## 2. 背景与问题

当前已有完整单元、任务隔离贡献和 promotion 读取真实 shared target。现有 Architecture delivery_promotion 输入仍固定 stage=phase2，validator 要求不同 baseline successor identity 和该入口的实际写入；Architecture/RDT 集中入口仍维护全局递增版本和历史摘要。隔离 worktree 因而没有消除共享文档的共同编辑。

来源中的 Backend [PR #693](https://github.com/castbox/ai-chat-roleplay-backend/pull/693) 是历史案例：与 #689 的前两轮冲突集中三份架构文件，同号承载不同内容；与 #687 的第三轮六处文本冲突也均在文档。来源记录其北京时间 2026-10-19 23:28:58 合入 dev，merge=08d84b0053271d15f9ffa69358e4c83aa6de7835，最终 HEAD=8e13d0deb08b26096289d50eeeccaaf2ead03a97。约 3 小时 34 分钟包含真实修复、整合验证、审核及 CI，不能全归因于无效流程，也不证明本轮优化已通过。代码自动合入仍需检查组合影响；案例不授予业务现场写入权限。

本 Task 收敛实际晋升时机与共同编辑，不能只更换编号文本，也不能删有效条件或保留两套 current 来换取少冲突。

## 3. 目标与非目标

使正常并行 Task 先独立形成和审核完整拟晋升内容，再在各自最终整合阶段合成唯一 current。普通读者直接取得完整定义；未变单元和引用保持。实现、公共合同及长期文档在同一最终 PR 交付。

范围包括 Architecture、RDT、Check、Review、Publication 阶段消费、必要公共 I/O 与在途迁移、代表性知识单元，以及实际安装组合验证。整体 Completion 核全部要求、Delivery 和真实验收，单次合并不替代 Task 完成。

不启动 #635，不改 Backend 业务现场，不跨仓实现，不建调度器、分布式锁、服务端权限治理或全仓知识平台。不执行部署、tag/Release 或完整 Release/多平台升级矩阵，不强制重写全部历史。不扩攻击/伪造、TOCTOU、压力竞态、fault injection 或 crash consistency 范围。队列不是前置。

## 4. 真实调用方、场景与流程

| 场景 | 调用方、前置与触发 | 行为和可观察结果 |
| --- | --- | --- |
| S638-01 不同能力并行 | 两个 Task 同基线，改不同完整单元 | 各自贡献及完整候选独立审核、依次晋升，保留双方；不因全局计数器冲突或完整重审 |
| S638-02 首次候选审核 | 实现及完整拟写正文已形成，shared current 尚未变 | 独立 owner 读取完整候选、精确来源及必要关系；真实审核，不宣称已晋升 |
| S638-03 同单元合成 | 后一 Task 命中单元已有前一 Task 的有效晋升 | 原 owner 读真实目标，保留有效条件并明确真实语义差额，形成唯一组合正文；前提推翻回原 scope/Planning |
| S638-04 最终实际晋升 | 同 Delivery 固定候选将进入 Ready/Merge | 原 owners 写实际 current 及命中关系/导航；质量 owners 审全部写入差额和受影响消费者，同最终 PR 交付 |
| S638-05 无知识变化 | 原 owner 判断无 Architecture/RDT 影响 | 既有 no-change 接续，不造空贡献、ADR、导航或晋升 |
| S638-06 无需 Git 整合 | 有知识变化，无冲突、必要依赖承接或平台更新阻塞 | 核真实命中目标并完成最终晋升；不为祖先关系 merge/rebase，不追赶最新 SHA，不要求队列 |
| S638-07 历史与在途恢复 | 原 Task 固定旧适用来源，或操作输出中断 | 旧引用保持原含义及精确历史定位；原 owner 同身份恢复或按明确迁移改选，不生第二 current |
| S638-08 实际安装组合 | #636/#637 与本轮接口在 matching 安装可用 | 早期 Draft、候选审核、后继适用性和最终 Ready/Merge 接续同 Task/Delivery/PR；分层验证投影与 reapply/drift/sidecar |

## 5. 行为要求

### R638-01 唯一完整正文

对应 S01..04。按能力/职责维护唯一完整正文和稳定身份；导航只定位，不复制业务摘要。正文保留有效条件、否定、例外、顺序、义务及必要关系。晋升后普通读者不通过拼接 Task contribution 历史理解 current。

### R638-02 身份与精确快照

对应 S01/06/07。普通 Task 不竞争同一全局递增版本。Git 提交定位精确正文快照，真实公共合同版本及兼容关系保留，不能批量改名抹去历史。具体 identity 由原 Author/Architecture 按直接 consumer 确定，不预设全仓 hash 清单。集中 README 全局编号、重复历史摘要和无行为变化的全仓身份刷新，不是每个任务的必做动作。

### R638-03 候选先完整审核

对应 S02。并行开发和首次审核只写本 Task 贡献及完整拟晋升正文，固定适用来源。shared current 尚未更新时仍可审核实现、设计和拟写内容。不能要求先实际晋升才审核候选，也不能要求尚未写出的最终 current 先通过全部消费者。首次完整独立审核真实完成，不由 Planning 或作者自检替代。

### R638-04 最终整合阶段实际晋升

对应 S03/04/06。实际 shared current 晋升收敛到本 Delivery 最终整合阶段。原 owner 读真实命中目标，保留已合入条件，形成唯一组合正文并更新命中关系/导航。最终审核覆盖最终提交全部实际变化及受影响消费者，包括正文、关系、导航和定位对齐，不只冲突标记所在行。文档改变运行行为、接口或验证义务时，回对应质量 owner 补检查，不能按文档晋升统一豁免。

实际写入必须在 Ready/Merge 前接受适用检查，实现、合同和 current 文档在同一最终 PR 交付，不另留以后补文档工作项。没有实际冲突、必要依赖承接或平台更新阻塞时，不要求 merge/rebase 最新目标。其它单元前进只保留其现状；命中单元变化解决实际差额。一次操作固定目标，后续只处理仍存在的真实阻塞，不恢复持续追赶最新 SHA。

### R638-05 真实适用性与语义合成

对应 S01/03/07。其它能力 current 推进不等于本 Task 所有设计失效。同一单元真实语义冲突由原 owner 明确冲突及合成结果，Git 自动合入不能替代组合判断。变化推翻需求前提时回原 scope/Planning。消费已安装 #637 的候选适用性合同，以真实原覆盖、全部已审差额与受影响依赖形成当前结论；不复制复用机制，不复制旧 pass。

### R638-06 全部消费者与迁移

对应 S02/04/07/08。同步 Architecture、RDT、Check、Review、Publication 与迁移合同。不能一端支持候选、下游仍要求旧式提前晋升；不能同时维护两套 current authority。必要公共 I/O 演进有明确版本、受控 consumer projection 和既有在途恢复合同。不能静默重解释旧结果，不能凭补 key/digest 生成新 pass。

### R638-07 代表性采用与原子能力保留

对应 S05/07/08。只迁移证明新模式所需的代表性知识单元和既有在途入口，不强制重写全部历史。无影响任务沿 no-change，不造贡献、ADR 或导航更新。未变单元和引用不批量改写，历史引用保持原含义且可解析。

canonical、dogfood、声明平台及 matching installed 通过原受管机制分发，保留用户内容，逐项处理 .new/.bak、mode 和漂移。作为后交付项，针对 #636/#637 实际已安装接口完成组合回归；前项尚未验证未来接口不算本项通过。

## 6. 约束与依赖

开发起点 main@9cec623833b61814f1175f31acde4fa81334cdb0，PR 目标 castbox/guru-trellis:main。TaskId=638-shared-current-promotion、generation=0；开发基线、Delivery 固定范围和 PR target 分别判断。本 Task 使用独立 worktree，不移动原主 checkout 的 main。

#636/#637 已交付接口在起点实际安装，分别拥有早期 Draft 和通用候选适用性。本项消费并组合验证，不重建其机制。Backend #702 队列消费本项合同，不反向成为前置。业务仓实际采用由其原 owner 承担，本 Task 不改其代码、配置或现场。

Markdown 定义语义，脚本执行/记录/校验事实。保留独立 Check/Review、readiness、各自副作用边界、Task/Delivery 身份及 Completion/Closure/Finish/Cleanup 职责。不持久化授权，不建审计链，不读取其它 owner 私有 checkpoint 来复用证据。

#637 保留的 Check 两项基线失败、Architecture 整组未完成、228 个 legacy archives 阻塞普通全仓 reapply，以及 formal_fork_source_lock 未验证，不自动成为本轮结果。本轮遇到时 fresh 判命中影响并如实报告；不清理历史归档绕过，不伪称整组全绿。普通安装验证最多一个代表性 clean 样本，完整 Release 矩阵属于专门 owner。

## 7. 可观察验收与验证方式

全部待实施和验证。真实 Agent 语义、deterministic wrapper、安装和 GitHub 事实分别证明各自范围。

| AC | 要求 / 场景 | 输入、入口与预期结果 |
| --- | --- | --- |
| AC638-01 | R01/02/03/05；S01/02 | 两不同能力 Task 同基线，经原候选审核/晋升入口完整审核和写入双方贡献；不因全局计数器冲突或完整重审 |
| AC638-02 | R04/07；S05/06 | 无知识变化及有变化但无需 Git 整合均接续；不出现空贡献、祖先同步提交或队列准入 |
| AC638-03 | R01/04/05；S03/04 | 两 Task 改同单元，后一 owner 读真实已晋升目标，保留前一有效条件并审真实组合差额；读者直接取得最终完整定义 |
| AC638-04 | R03/04/06；S02/04 | 首次审核完整拟晋升正文及精确来源；写入后审全部实际差额及未改消费者，拟写/已写/已交付状态区分 |
| AC638-05 | R01/02/07；S01/07 | 比较命中/未命中单元及旧引用/Git 历史；未变正文/引用不批量改写，历史含义和解析保持 |
| AC638-06 | R04/06；S04 | 同一最终 PR 交付实现、公共合同和长期文档；原 Check/Review/Publication 消费新时机，Ready/Merge 不接受缺消费者覆盖 |
| AC638-07 | R06/07；S07/08 | 代表性既有 Task/Delivery 恢复、公共 I/O 迁移、#636/#637 实际 installed 组合，以及 canonical/dogfood/声明平台/reapply/drift/sidecar 分层证据；明确未覆盖项 |

## 8. 实际未决项

整体需求无阻塞的产品或范围选择。具体单元身份、公共 I/O 迁移、最终整合路由、代表性迁移对象和样本由 Delivery Author/独立 Architecture 细化，不得削减验收。root PRD 只承载整体要求，不代表方案批准、实施启动、验收或发布通过。
