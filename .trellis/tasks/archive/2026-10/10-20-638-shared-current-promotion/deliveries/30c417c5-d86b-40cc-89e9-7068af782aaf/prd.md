# D1：共享知识身份与最终整合晋升需求

## 1. 整体来源与术语

本批 scope_ref 绑定整体 [Task PRD](../../prd.md)，accepted_scope revision 为 sha256:25a442e26ebd74734a38f3886e531e58575ee32e56c79dffb1d68c22556d95fc，覆盖 AC638-01..07。DeliveryKey 为 TaskId=638-shared-current-promotion / generation=0 / delivery_id=30c417c5-d86b-40cc-89e9-7068af782aaf；公开 planning_root=deliveries/30c417c5-d86b-40cc-89e9-7068af782aaf。

| 来源 | 章节 / 角色 | 本批用途 |
| --- | --- | --- |
| [#638](https://github.com/castbox/guru-trellis/issues/638) | 目标与行为、最终合入准备、验收、边界；Direct Source 要求与规范性阶段/兼容约束 | 本批全量行为及验收，原 source_selection 原样保留 |
| [完整知识合同](../../../../../trellis/skills/guru-team/packages/guru-maintain-requirements-design-test-ssot/references/current-knowledge.md) | #331 的唯一正文、薄导航、稳定身份及原维护方；约束 | 保留原子能力，演进晋升时机和公共消费 |
| [候选适用性合同](../../../../../.trellis/spec/workflow/workflow-contract.md#candidate-applicability-and-coverage) | #637 实际已安装合同；约束 | 复用合法原覆盖/真实差额/受影响依赖，补 #636/#637 组合 |
| [当前完整知识设计](../../../../../docs/design/current/knowledge-maintenance.md) / [Architecture change-contract](../../../../../docs/architecture/06-governance/change-contract.md) | 现行设计/项目职责，包含本批需替代的 phase2 时机 | 本批 design 第3节单写 retain/change/reject 与具体落点 |

完整知识单元、稳定身份、Git 精确快照、拟晋升正文与最终整合阶段沿整体 PRD 定义。本批固定候选与 shared target 分别判断；候选可审核不表示已晋升，晋升不表示已交付。

## 2. 整体与本批目标、非目标

整体问题是 Task 隔离后仍共同编辑共享 Architecture/RDT 正文、导航与全局版本。D1 独立交付全部 R638-01..07 和 AC638-01..07：在两个原维护 owner 及全部消费者间一次完成身份、候选审核、最终实际晋升和迁移闭环。最终 PR 同时交付实现、公共合同和长期文档，不能拆出以后补文档义务。

本批排除 #635、Backend 业务现场/跨仓实现、合入调度器与队列前置、分布式锁、服务端权限治理、全仓知识平台、部署、tag/Release 及完整 Release 矩阵。正常 honest-but-fallible 操作、stale/mismatch 和普通实现缺陷仍处理，不扩攻击/伪造、压力竞态、TOCTOU、fault injection 或 crash consistency。

## 3. 本批起点、前序结果、依赖与剩余责任

本 Task 没有前序 Delivery。D1 起点为 main@9cec623833b61814f1175f31acde4fa81334cdb0；H0 等于该起点，最终实现 HEAD 尚未形成。开发基线、Delivery 固定完整内容范围 B..H 与 PR target castbox/guru-trellis:main 分开；后续无关 main 前进不替换 B，不要求同步提交。

该起点已包含 #636 早期 Draft 和 #637 通用候选适用性。它们分别由原 TaskCommit/Publication 及唯一候选合同拥有，本批是后交付项，必须使用实际安装接口补组合回归；相关 [#637 Test](../../../../../docs/requirements-design-test-contributions/637-candidate-review-reuse/test.md) 是历史事实与边界，不能代替本批结果。

D1 不预留后续实现责任，整体要求在本批完整承接。独立 Architecture 的候选/最终规划评估、Wording、Approval、Activation、真实 Check/独立 Review/readiness，以及外部发布/合并和 Completion/Closure/Finish/Cleanup 均仍真实完成。D1 合并只是一项 Delivery 事实，整体 Completion 还核全部要求和证据。原主 checkout 不移动；执行在本 Task 独立 worktree。

## 4. 本批调用方、场景与流程

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

## 5. 完整行为、条件与约束

以下七项均为本批交付责任，完整承接整体要求。规范性来源设计只在本批 design 第3节处置；本节不另建处置矩阵。

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

同一 Delivery 的首次拟写审核和最终实际写入审核均必须真实完成。只有后者能证明实际 current 已更新；只有实际 satisfying PR 合并及整体终态能证明对应交付/Task 完成。不能用目录名、导航、schema pass、planning ref 或旧语义 pass 替代上述事实。

#637 的原适用性合同决定保留/失效/补充范围；全部实际写入及未改消费者都在覆盖内。没有新架构事实时不为了阶段或 reviewer 身份重建相同理解；缺证据补缺，影响无法界定则扩大审核。文档改变行为/接口/验证义务时补对应质量检查。

## 6. 本批验收、验证方式与未决项

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

本批通过真实原 owner 调用链、独立 Agent 语义判断、公共 wrapper/consumer 和必要实际安装/远端事实证明这些结果。fixture/静态投影不替代 Agent 对语义合成与覆盖的判断。普通安装最多一个 clean 代表样本；多平台源码/声明投影校验不等于完整 Release 安装矩阵。

整体无阻塞产品问题。具体 identity、profile 迁移、最终整合路由、代表性正文及实际样本由后续 Author/独立 Architecture 细化。遇到 #637 已记录的 Check 基线红测、Architecture 整组未完成、228 archives 普通 reapply 阻塞或 formal_fork_source_lock 未验证时，本批 fresh 判断命中影响并保留实际结果，不删除历史或伪称全绿。

## 7. Canonical 引用与本轮差额

| Authority | 命中内容与用途 | 本轮差额 |
| --- | --- | --- |
| [RDT Requirement 当前知识](../../../../../docs/requirements/current/knowledge-maintenance.md) | R331-01/02/05 与阶段适用性、单一 authority、完整正文及历史 | 保留完整能力；减少共同编辑并改变实际晋升时机 |
| [RDT Design 当前知识](../../../../../docs/design/current/knowledge-maintenance.md) | D331-01..05、D600/ADR-030 的现行阶段关系 | 明确窄替代提前晋升要求；新旧 consumer 成套迁移 |
| [RDT Test 当前知识](../../../../../docs/test/current/knowledge-maintenance.md) | 完整单元/并行贡献/历史/安装的策略与结果分责 | 增加本批 AC 入口与真实组合，不抄旧测试结果 |
| [Architecture](../../../../../docs/architecture/README.md) / [constitution](../../../../../docs/architecture/00-foundation/design-constitution.md) / [change-contract](../../../../../docs/architecture/06-governance/change-contract.md) | .105 起点、constitution-v1、九 concern 和原 project-check 协议 | 原 owner、独立判断及单一 current 保持；精确阶段/身份影响交候选评估 |
| [候选适用性](../../../../../.trellis/spec/workflow/workflow-contract.md#candidate-applicability-and-coverage) / [ADR-034](../../../../../docs/architecture/adr/034-candidate-applicability-and-coverage.md) | #637 原覆盖加全部差额/消费者与工程事实适用性 | 直接消费，不复制机制；补本轮与 #636 已安装接口组合 |
| [维护包](../../../../../trellis/skills/guru-team/packages/guru-maintain-architecture-baseline/SKILL.md) / [RDT包](../../../../../trellis/skills/guru-team/packages/guru-maintain-requirements-design-test-ssot/SKILL.md) | 公共 profile、typed exits、runtime 与原 owner 边界 | 必要 I/O 演进有版本和在途恢复，不静默改变旧 API |

尚未写共享 current、导航或 manifest；首次独立候选评估之后才进入本批方案写作。无关单元、历史归档及其它项目内容不在本批改写范围。
