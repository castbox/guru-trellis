# D1：v0.7.0-guru.6 发布准备设计

## 1. 设计目标、需求承接与内容基线

本批承接 [D1 PRD](./prd.md) 的 D1-R1–R6、D1-S1–S5、D1-AC1–AC6，覆盖整体准备范围 AC1–AC6。目标是形成一致的版本、维护目标、公开来源和受管投影，并通过晋升前后两次完整独立正式 Review 完成 reference-only 准备交付。没有前序 Delivery，也没有预定 D2。

Development baseline B 固定为 `abe3701acbd278a10f6c6ebbdc5bbe19a938916b`。来源是本 Task 创建时已包含 #669 交付和终态归档的 main；Planning H0 是同一提交。后续内容范围为固定 B 到实际交付 H 的完整差额，PR target 为 main。共享 origin/main 前进不自行改变 B，也不替代真实集成和当前适用性判断。

架构约束由 `docs/architecture/README.md` 的 `guru-trellis-architecture`、`00-foundation/design-constitution.md` 的 `guru-trellis-design-constitution-v1` 和 `06-governance/change-contract.md` 拥有。本设计只对齐现有版本与分发事实，不新增架构决策、owner、状态、公共接口或兼容层，不创建空 Architecture 贡献或 ADR。实际候选扩大这些边界时重新进入原 Architecture owner。

## 2. 当前系统、边界与目标差额

| 实际模块 | 当前事实与本批目标差额 |
| --- | --- |
| `trellis/guru-team-extension.json` | Guru revision 仍为 `.5`；改为 `0.7.0-guru.6`，保留已选 CLI `.5`。 |
| `guru-upgrade-installation/runtime/owner.py` | TARGET_GURU 仍 `.5`、TARGET_CORE 仍 `.4`；分别改为 Guru `.6`、CLI/Core `.5`，使正式来源核验与当前 manifest/lock 一致。 |
| 安装升级输出合同 | package public output schema、package consumer、共享 production consumer 的 installed_version const 及当前示例同步 `.6`。tools output 的自由字符串类型保持。 |
| 三份 README 与 `.trellis/spec/docs/public-docs.md` | 当前稳定 `.4`、候选 `.5`、旧 Fork/知识入口描述过期；准确区分前驱已发布 `.5`、未发布目标 `.6`、当前锁和历史。后者是本仓专属规范的唯一 tracked 来源，不新增公共 preset 副本。 |
| canonical/installed/platform | canonical 为长期来源；通过原 preset 同步 dogfood、Shared/Codex/Claude/Cursor。当前运行副本不能成为唯一修订源。 |

当前 Fork 固定为 `79a97ed60fe19e8f287eaddfa74722b5250ced35`，tree 为 `7f83f41031181b1f12b83268e51cbde2b775ec5f`，来源 CI 为 `39905440951`，CLI/Core 为 `0.7.0-castbox.5`，pnpm 为 `10.32.1`。这些既有选择不因 Guru 发版改变。前驱 tag `.5` 的实际 Fork 为 `7bcbeaad31380e7a29c97898cb947c6120a61775` / CLI `.4`；不能用当前锁解释前驱。

本批不修改 Issue、私有 release 合同、公共流程 runtime 或 Fork，不实现其它 Issue，不清理评测资源，不执行业务安装或生产部署。Stage 2 仍是准备完成后的独立发布责任。

## 3. 来源设计处置（唯一）

| 来源与原承诺 | 处置与具体落点 | 理由、影响和原 owner 承接 |
| --- | --- | --- |
| #656「版本与来源」：Guru `.6`，保留 Fork/CLI/pnpm，独立前驱映射 | retain；第2/4节版本维护与第8节 V1/V2 | 软件轴独立；不得批量替换历史 fixture、原始失败或来源。 |
| #656「安装来源与文档收敛」：稳定 `.5`，同 ref providers，候选真实完整 SHA 与自身锁定构建 | retain；第4节公开文档和第8节 V2 | 未发布 `.6` 不能作 provider；来源必须实际可解析，不写未来自引用 SHA。 |
| 私有 release Stage 1 第1–5步：完整晋升前 Phase 2、TaskCommit、独立完整正式 Review 后才晋升 | retain 审查职责、完整性和先后；本次机制按第6节有界恢复承接 | 原 candidate Check 完整检查，原 early commit 形成真实 H；独立 Review 完整审 B..H 和拟写内容。首次结果仅供本次私有发布晋升前门禁，在当前对话消费，不冒充公共 Check/full_review 或 wrapper passed。 |
| 原 Check/TaskCommit/Branch Review：candidate_checked 不构成最终 Check；early DTO 不进入公共 formal Review | retain；第5/6节接口与阶段 | 不伪造公共 predecessor/result。提交后刷新实际候选绑定；最终公共门禁使用真实 after。 |
| 私有 release Stage 1 第6–9步：晋升后新 Check、TaskCommit、完整独立正式 Review、publication/Delivery/Publish/Merge | retain；第6节后半和 V4 | 第二次必须取得原 checker/public wrapper 的真实 passed；首次恢复结论不能替代。 |
| 私有 release Stage 1 第10–11步：整体 Completion、reference_only Closure no_mutation、正常 Finish/Cleanup | retain；第6/7节和 implement Policy | 准备交付不关闭 #656；归档与资源清理各按原 owner。 |
| current-knowledge 与 change-contract：隔离拟写、原 owners final_integration、实际读回和 after 重绑 | retain；第4/6节、implement Docs Plan | 两次 Review 都保留；有真实知识差额才拟写与晋升，无变化不制造空贡献或空提交。 |
| 私有 release Stage 2：准备和 bookkeeping 合并后丢弃旧证据，fresh main exact candidate，稳定入口全部检查后各自 tag/smoke/Release/closure | retain；第7/8节外部责任 | 本 Task 不预执行或声称通过这些后续门禁。 |
| workflow `Candidate migration boundary`、#656 Stage1 分发责任与原 verifier `local_sample` | retain；第4/7/8节 V3 | 开发 Task 保留原 installed graph；由同一完整冻结 source 的受控 repository 实际首装和自有 full reapply证明候选分发。#566 Test 第80–92行仅提供方法来源，不继承其 pass，不替代 Stage2。 |
| Forbidden Persistence、独立副作用确认 | retain；第5/7节 | 不保存授权、动态状态、body handoff 或 release-status commit。 |

## 4. 模块、职责与设计取舍

实现 owner 只改真实 current expectation：manifest version、维护执行器两常量、对应三个 installed_version const、两个当前输出示例及实际依赖它们的测试。`test_contract.py` 的 formal source 正例和 `test_delivery_upgrade.py` 的当前 source fixture 要随目标一致；描述旧来源、旧 receipt 或 CLI/Core 配对算法的历史 fixture 保留原义。通过现有测试覆盖正式 source 与输出 schema/consumer 一致性，不为简单常量制造镜像测试。

文档 owner 在 root/workflow/preset README 和本仓 public-docs 中维护一致事实。稳定安装使用实际 `.5` tag 和其自身 CLI `.4` 锁。试用候选由调用者选择一个真实远端完整 SHA，在操作时核其 manifest、lock、commit 和构建，并让 workflow/preset 使用同一 SHA。文档不硬编码尚未生成的准备提交，也不声称当前分支就是最终发布候选。保留非交互命令与 AI prompt 两种入口。

公开说明从实际前驱到候选的累计能力组织，包含 #669 已有实现恢复；#630 三系统脚本、原生 Agent、#649 有效样本/false/no-grade、#669 正式来源与 Backend 未验证项各保留原层次。不能把单项 CI、受控样本、重试或知识晋升写成完整安装、模型、业务采用或 Release 通过。

原 RDT owner 调查本批是否改变现有完整知识定义。仅有软件轴和公开映射更新而定义不变时返回真实 no-change。命中当前过期定义时，先写本 Task 隔离的完整 proposed targets，由原 candidate Check 审核，再在原 final_integration 写入读回；不复制全部未变正文、不总入口升版、不修改历史证据。Architecture 本设计没有共享写目标；后续发现真实影响时回原 owner，不能由实现者自行补 ADR。

Stage1 的 V3 使用一个受控完整 source repository。冻结作者实际完整 `trellis/` 的路径、文件 bytes、目录及文件 modes；快照一致性只供本轮复制和结束比较，不是审批或跨阶段 authority，也不写 tracked 冻结账本。先用锁定 Fork 的真实 CLI/Core `.5` 初始化 `native-delivery-v1`，再沿现有 verifier 的 `local_sample` 方法放置同一冻结 Guru workflow。初次完整安装由作者 source 的原 preset 执行；随后从包含冻结 canonical 与实际 installed 图的受控 source 自身执行三平台完整 reapply。该对象不带入作者 Task、archives、session或其它 checkout，不执行根 Plan2。

AC3 保留全部安装及分发观察：实际 manifest `.6`、受影响 runtime/schema 的 canonical bytes/modes、Shared/Codex/Claude/Cursor、ownership、source/installed validators、drift及零未处置 sidecar。私有 release Skill的四平台 parity仍在作者 checkout单独检查。作者旧安装的自洽校验与其原 apply失败单列，不能计作 `.6` adoption；受控结果不能改写那些原始事实。完整源的 paths/bytes/modes、匹配构建、初始化方式、必需义务或执行环境改变时，原 owners重新判断实际影响，补验受影响项；组合影响不明则完整重验本 V3。

本地 workflow sample及受控 `.6` adoption只证明 Stage1对应分发层，不证明远端 immutable marketplace、正式 `source_locked`、真实业务采用或 Stage2 exact candidate。软件实现与原安装算法不变；本轮只明确验证对象及证据归属，没有新的产品机制、公共状态或兼容分支。

## 5. 接口与数据

不新增 public DTO、schema 字段、profile、typed exit 或阶段。现有 upgraded output 的 installed_version 目标值从 `.5` 变为 `.6`，对应 package/shared consumer 同步；schema id 和其它输出语义保持。工具升级的 output 字段类型不收紧。

执行链使用现有 opaque DeliveryKey、固定 B 与真实候选。`candidate_checked` 仍只交原知识整合 router。early commit 仍只产生原 `draft_committed`，不改称 `committed`。晋升前完整独立正式 Review 的恢复结论在当前对话供私有 release owner 消费，说明 B/H、审查覆盖、验证、findings 和缺口；不写公共 `full_review`，不伪造 check_result_id，不把 `draft_content_reviewed` 重命名成 passed。实际 Git/GitHub 事实仍各由原 provider 证明。

最终 `check_result_id → TaskCommit → 完整 Branch Review full_review_result_id → Delivery Review` 保持原公共 producer/consumer。任务 PR body 由动作前 live facts 生成，只用 Refs #656；不存 body handoff。没有业务数据结构或数据库变化，因此没有数据迁移。

## 6. 状态、顺序、正常与失败流程

1. 稳定 Planning 经 Wording、final_plan Architecture、Approval 和 Activation 后，实施版本/公开文档/必要断言，并形成所有真实隔离拟写。原 preset 投影和本批定向验证覆盖整个候选。
2. 实施用固定 B、实际 HEAD 和全部 dirty 构造 candidate/begin_check；独立 Architecture phase2 与原 `delivery_candidate_check` 覆盖完整实现、拟写及未改消费者。失败按原 finding/Planning route 处理；成功只返回 candidate_checked，公共 phase 合法回 implementing。
3. 原 TaskCommit 通过 early profile预览精确内容、运行真实 hooks并在独立提交边界形成 H。随后原独立 Architecture committed-range 评估和 Branch Review semantic owner审查完整 B..H、全部拟写、消费者和真实验证。只有零开放 P0–P3且无阻塞缺口，私有发布 owner 才消费首次完整独立正式 Review（恢复承接）。它不写公共 gate，也不触发 early PR 发布。
4. 提交后 HEAD 已变，重新构造同 B/实际 H 的候选。原 Architecture/Check判断实际差额与可复用工程事实，刷新 candidate_checked 后，才交原 Architecture/RDT 串行 final_integration。原 owners 固定写前真实目标，核 expected-current、写入并完整读回；no-change跳过写入。
5. 实施把所有真实 after 内容重新 candidate/begin_check。原最终 Architecture/Check 检查完整实际候选，原 TaskCommit处理必要 dirty或 clean committed reentry。若提交改变 HEAD，沿原 owner刷新实际候选与 Check。禁止用空提交刷新状态。
6. 第二次独立 Architecture和完整 Branch Review覆盖固定 B..最终 H全部内容，不把首次结论当第二次通过。必须取得原 checker/public wrapper真实 passed，才进入 Architecture publication、Delivery Review、原 Publish/Ready/expected-head Merge。
7. 原 Completion核全部准备责任；completed才进入Closure no_mutation。acceptance-finish后原Finish归档及bookkeeping合并，Cleanup只处置精确本Task资源。Stage2之后另行开始。

普通验证失败、失效来源、实际 mismatch、输出丢失或未解决 sidecar都由原 owner有界恢复。不得手改 artifact/hash/state补 pass。源码或知识义务变化回最早受影响 owner；不因 reviewer/阶段变化无因重复无关命令。

## 7. 恢复、兼容、迁移与集成

恢复保持同 Task、generation、D1、worktree、branch和B。首次完整 Review结论只对其真实 H/拟写与验证有效；变更后原reviewer补审全部差额和受影响消费者，影响不明则完整复审。原知识晋升的 partial/output-loss仍由其同一意图读回恢复，不能重放已完成写入。

preset继续原官方 managed hashes、用户区块和 `.new`/`.bak` 机制。若作者 checkout的历史 archive前置校验拒绝普通 reapply，保留原失败并由原 owners判断适用性；不把它转成隐含的全仓迁移要求。受控目标必须通过同一个普通 full apply前置校验和真实 installed `.6`验证，不能跳过 guard、不改 `.version`、不制造历史 receipt，也不将 tools-only投影称为 full reapply。受控目标自身出现相同拒绝、实际 mismatch或 sidecar时，停止该 V3并回原维护 owner。

没有新公共 API或 legacy parser迁移。现有安装采用本次版本须走匹配 workflow/preset与自身固定 Fork；源码修改不证明旧安装已更新。本次准备不执行真实业务升级。正式来源 `source_locked` 验证需要已提交、干净、远端可寻址的匹配源，dirty/local_candidate不得冒充该层证据。

Stage2由#656在准备和bookkeeping合并后独立执行：从fresh main冻结candidate commit/tree，重跑私有release表中的全部稳定入口，分别确认tag、smoke、Release和Issue关闭。准备分支及先前Review身份不能替代最终candidate。

## 8. 验证设计

| ID／AC | 输入、层次和入口 | 预期观察与证据边界 |
| --- | --- | --- |
| V1／AC1 | manifest、lock、维护模块、三const、当前示例及原upgrade-installation/tools相关tests | Guru `.6`一致；TARGET_CORE/manifest/lock为CLI `.5`；原历史fixture保留。检查formal source、输出/consumer兼容和原恢复用例；不证明真实业务升级。 |
| V2／AC2 | 三README、public-docs、前驱tag固定树、当前锁、原#630/#649/#669 Test | 稳定/候选/历史轴、非交互入口和AI prompt准确；真实失败和未验证边界保留，不用当前锁解释前驱。 |
| V3／AC3 | 作者 source及私有 Skill parity；同一冻结 canonical的受控完整 source repository首装、自有三平台full reapply、installed `.6`、Shared/Codex/Claude/Cursor、ownership、drift、mode/sidecar | 受控 canonical/实际投影一致，用户内容按原机制保留，零未处置sidecar；作者原失败单列，不以旧安装自洽或源码parity代替实际 `.6`安装。 |
| V4／AC4 | 原完整candidate Check、真实H、晋升前完整独立Review、原晋升读回、最终Check/TaskCommit/完整独立公共Review | 两轮各有完整范围与真实语义判断；首次不冒充公共结果，第二次使用真实public gate；无开放P0–P3才继续。 |
| V5／AC5 | 原Delivery/Completion/Closure/Finish/Cleanup当前结果与GitHub/Git事实 | 准备与bookkeeping正常合并归档，Closure no_mutation，#656仍由Stage2关闭。 |
| V6／AC6 | 完整本批diff、Task正文、runtime写入边界、diff hygiene | 无动态发布账本、授权信息或body handoff；稳定计划不预填验证结果。 |

命令、依赖和定向测试选择见implement第3节。Stage1不跑累计多平台矩阵；Stage2的focused安装、真实前驱existing upgrade、secret scanner、exact diff及tag-pinned smoke仍全部保留，由后续独立candidate执行，不计为本Task提前通过。

## 9. Canonical 引用、本轮差额与实际未决项

Requirement/behavior使用整体PRD R1–R8及live#656；本批只交付准备。Design/Test使用私有release完整两阶段合同、原Check/TaskCommit/BranchReview合同和 `docs/{requirements,design,test}/current/knowledge-maintenance.md` 的R638/D638/T638及R648/D648/T648。后者约束来源、隔离拟写、真实当前判断和工程事实适用性，不把专项行为实验变成本次重复评测义务。

Architecture使用既有foundation/constitution、change-contract、ARCH-GOV-008及distribution的当前来源/分发约束。软件来源轴没有新决策，不创建Architecture贡献/ADR；RDT由原writer在本批实现前读取完整命中单元判断真实no-change或隔离拟写，不为留证制造空资产。

本方案没有待用户选择的产品问题。实际reapply、安装来源、测试或知识差额若出现真实阻塞，按第6/7节停止在受影响原owner，不能预填成功或静默删除验收。
