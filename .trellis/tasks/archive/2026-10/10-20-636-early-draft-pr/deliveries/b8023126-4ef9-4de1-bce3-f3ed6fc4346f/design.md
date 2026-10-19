# D1 提前 Draft 与独立最终门禁设计

## 1. 设计目标、需求承接与内容基线

本批承担 PRD 的 R636-01..07、S636-01..07 和 AC636-01..10。目标是让原公共提交/发布 owner 在完整质量门禁前形成真实 Draft 反馈；最终 Ready、Merge 与整体 Completion 的责任保持。

D1 没有前序 Delivery。development baseline 与固定内容 B 均为 `b470580d4f79f61c66d72db97861fe1564b5e746`，来源为本次已同步默认 main 和 Task 创建起点。原 `DeliveryProjection.content_base` 在尚无候选时消费该明确起点；已有候选后保持其 base。Planning H0 为同一提交，只是写作时观察。PR target 是 `castbox/guru-trellis:main`，不是每次内容审核的新 base。实现形成 H 后审核完整 B..H；目标前进本身不中断审核。

阶段适用 Architecture 为 `current-main-0.7.0-guru.103`，constitution 为 `guru-trellis-design-constitution-v1`，change contract/concerns 为 v1。独立 candidate_assessment 已正式返回 `baseline_current / architecture_impact / target_native`，理由是原提交前置和原发布时序改变。它只约束当前设计，不证明 final_plan 或实现通过。

## 2. 当前系统、边界与目标差额

现行 `guru-create-task-commit/runtime/common.py` 和 `runtime/delivery.py` 的所有当前 profile 都绑定 `check_result_id`。精确 staging、完整 dirty 分类、中文结构化消息、真实 hook 隔离事务及同提交输出恢复已存在，保留这些职责。差额是在同一 owner 中加入早期候选 profile，以有界内容检查代替这类提交对完整 Check 的统一依赖。

现行 `guru-publish-task-delivery/runtime/owner.py` 在 readiness 后执行 `push_content -> bind_pr -> converge_metadata -> mark_ready -> ready`。创建时虽用 Draft，但该事务最终统一转 Ready。差额是在原事务中区分 Draft 反馈终点和最终 Ready 终点，并支持更新前先退回 Draft；复用同 PR、元数据收敛、远端实际状态读回和恢复。

上游 Delivery API 1.0、Task schema 2.0 的身份、phase、gate predecessor、PublicationFact/DeliveryFact 不变。不修改官方 Trellis 源码、全局包或 `.trellis/scripts/common` 来实现流程分叉。Draft 是原 Publication 的远端反馈结果，不写成最终 PublicationFact，不新增公共 phase 或第二 Delivery store。只有最终 Ready 事实沿原 API 写入 PublicationFact。

Check、正式 full_review、readiness、Merge、Completion、Closure、Finish 与 Cleanup 保留原 owner。#637 的跨阶段审核复用、#638 的文档晋升调整、Backend 队列/CI 改造均不进入本批。

## 3. 来源设计处置（唯一）

本矩阵只列规范性约束的实际处置。Issue 的业务要求和验收在 PRD，不在此重复成第二范围权威。

| 来源与原承诺 | 处置 | 设计落点、理由与影响 | 上游处置 |
| --- | --- | --- | --- |
| #636 行为3、7：经原 TaskCommit/Publication，不旁路 Git/gh | retain | §4、§5 原 owner 新 profile 与同步 consumer；deterministic executor 不判断 scope/readiness | 本 Issue 已要求 |
| #636 候选阶段边界与 #567 固定候选：审核固定 base/head，target 前进不中断 | retain | §1、§6 分开 B/H 与 integration target；不要求持续同步或 latest-target ancestry | 既有固定候选能力保持 |
| current task-delivery-lifecycle 的所有提交依赖 Check、Publication 在 readiness 后完成 Ready | change | §5 给早期 profile 独立闭合输入/出口；旧最终提交/Ready 路径不降低门禁。差额由 #636 明确要求 | 本 Issue 授权演进原 owner；MIGRATION-636 成套切换 |
| 同一 current 设计的 full_review 以 Check 为 predecessor | retain | §6 早期完整内容分析并行开始，但不写 public full_review；Check 后原 Branch Review fresh 判断及正式记录，不能把早期 pass 自动映射为最终 pass | candidate_assessment 已明确约束 |
| ADR-024 / current RDT：全部 Delivery PR Refs-only；整体 Closure 独占关闭 | retain | §5 早期与最终 body 都禁关闭关键字；最终 Publication 重读范围/目标确认 Refs-only，整体关闭留给 Closure | 不恢复历史 Publication 关闭语义 |
| ADR-028 / ADR-030：阶段适用性、独立 Phase2 评估拟晋升内容后，原 owner 晋升，再最终 Check/committed Review | retain | §8、§9 本批实现和文档实际差额进入原顺序，不做 #638 的新时机优化 | 无偏离 |
| 官方 workflow marketplace/preset 扩展、Markdown 决策/脚本执行 | retain | §4 workflow 只编排 stable skill 与 typed exits；脚本只做确定性 Git/GitHub/API 读写和校验 | 沿官方机制分发 |

## 4. 模块、职责与设计取舍

**D636-01 TaskCommit。** 原 package 的 SKILL、contract、interface、schemas/examples/consumers 及 `runtime/common.py`、`delivery.py`、必要 execute/invoke 投影共同演进。新增 `delivery_draft_commit`：只在已激活且 implementing 的当前 Delivery 内，有界审查完整 dirty snapshot、实际拟提交内容、需求范围、最小自检、敏感内容与精确目标。新增 `delivery_draft_committed_reentry` 恢复无新 dirty 的早期已提交候选。两者不要求完整 Check，不执行 `begin_check`、不写 gate。现有提交 profiles 和 `committed` 保持最终 Check 链含义；新的早期出口不能进入正式 Branch Review。复用原 executor、receipt 和分类机制，不增加第二 commit writer。

**D636-02 Publication。** 原 package 拥有 Draft 创建/更新、Ready 回退、最终 Ready 及同操作恢复。新早期 profile 不消费 readiness；最终 `delivery_review_ready` 仍要求当前 readiness、候选与完整前置链。拆出 package-local Draft 处理模块只在 owner.py 责任过密时进行，不添加通用框架。metadata/closing 检查、同 repo/base/head 校验和可恢复事务继续共用原实现。

**D636-03 独立内容审核与质量验证。** Draft 输出由 workflow 的唯一反馈 router 消费。它以同一 B/H 同时调度独立完整内容分析与风险匹配验证。原 Branch Review 增加早期 `delivery_draft_content_review`；只审完整固定 diff、契约、调用方、测试与 Architecture 边界，不写 public full_review，不读取 Check 私有结论。其 call-local 结果供原 implementation/Check owner 修正与证据汇总，最终正式 Branch Review 仍独立重新判断。Check 的完整 scope 和正式 recorder 不变；早期命令结果只有原 Check owner判断仍适用时才能作为执行事实使用。不得建立跨阶段 review cache。

**D636-04 编排与分发。** canonical workflow 只显式加载上述 stable skills，消费唯一出口，安排反馈后的并行工作。当前 session continuation 根据公开 phase 与 live PR/原事务事实接续，不从 Draft 推导 gate。改动 canonical packages 后通过完整 preset 同步 installed packages、dogfood workflow、声明平台 overlay 和 discovery projection。平台入口不复制内部判断。

**D636-05 最终门禁。** Delivery Review 明确区分 HEAD 验证与组合候选验证，判断当前适用证据及真实缺口。Merge继续读取实际 PR 非 Draft、HEAD/body 与当前完整 gate 链；旧 readiness、Draft 结果或早期审核不能放行。所有 Delivery body 只 Refs，Closure关闭整体 Issue。

选择直接演进原 owners，保留现有成功能力；不建 Draft 专用公共 Skill、统一候选账本、通用状态机、第二 public gate 或兼容双读。新增 profile/出口只服务当前早期提交、远端反馈和并行审核场景。

## 5. 接口与数据

以下名称是本批拟实现公共合同；实现时由原 interface 注册唯一 consumer，缺 schema/projection 或 unknown/multiple exit 一律停止。每种输入独立闭合，不把缺失 Check 写成 null 伪装最终输入。

| 入口/生产者 | 本批输入与结果差额 | 直接 consumer |
| --- | --- | --- |
| TaskCommit `delivery_draft_commit` | mode、task_ref、delivery_key、固定 base_ref；原 prepare 消费当前 path classifications、消息与真实 AI review；无 check_result_id。输出 `draft_committed`：task_ref/key、base_ref、commit_sha | workflow draft-commit router 薄投影到 Publication `delivery_draft_publish` 的 candidate_head |
| TaskCommit `delivery_draft_committed_reentry` | 同一 task/key/B 与实际非空固定 diff、已提交规划/身份；无 Check。同一 `draft_committed`，不 stage、commit、hook | 同上 |
| Publication `delivery_draft_publish` | mode、task_ref/key、base_ref、candidate_head、中文 pr_title/pr_body。body 明确 HEAD/组合对象和已执行、失败、SKIP、未执行/待完成；Refs-only | `draft_published` 的唯一 feedback router；DTO 仅 task/key/B/H、repo_ref/pr_number，供并行调度和同 PR核验 |
| Publication `delivery_return_to_draft` | mode、task_ref/key 与具体 revision reason；以 live 已绑定同 PR为对象，先回读状态/HEAD，再按原 publication role 合法 rework 到 implementation，失效 check/full_review/readiness、保留 planning/身份/历史事实；返回 `draft_revision_ready` 的 task/key 与 repo/pr | 同一 Delivery implementation router；早期提交/更新接续，不生成新 Delivery |
| Publication `delivery_same_plan_resume` | 保持 transaction_ref 的原恢复入口；2.0事务存动作/终点，恢复真实 Draft 或 Ready；旧成功事实与新 readiness 分别判断 | 原同 owner恢复、feedback router 或 Merge router，依正式单一 typed exit |
| BranchReview `delivery_draft_content_review` | mode、task_ref/key、base_ref、branch_review_commit；不接收 check_result_id，phase 不作最终通过。早期审核覆盖完整固定 diff | `draft_content_reviewed`：task/key/B/H；无正式 gate。发现问题返回独立 `draft_revision_required`：task/key 与即时消费的具体 revision_refs，进入原 implementation；blocked 保持原 stop |
| 原最终 TaskCommit / BranchReview / DeliveryReview / Publish | 保留 check_result_id、full_review predecessor、readiness 和 PublicationFact 合同；draft DTO 不能充当任一 gate | 既有下游 owners |

TaskCommit 的当前 candidate 私有格式升级为独立2.0闭合 union：早期形状不含 Check；最终形状继续绑定真实 Check。receipt 只恢复同一次实际 commit，消费后按原策略删除/替换。不得持久化用户授权。最终公共 `committed` schema/含义不变。

Publication 的当前事务采用2.0：同一 owner 内写明确动作/终点与实际 mutation preimage/postimage；Draft 动作含 `ensure_draft`，在 push 前完成。该局部事务的最小结果只供同 owner恢复；不把 PR live事实另建长期账本。Draft终态不调用上游 `record_publication`；Ready终态才写现有 PublicationFact。Draft结果消耗后保留的仅是同操作输出丢失恢复所必需状态；下一轮由原 owner核对并退休已完成旧事务，不保留历轮审计。

现有 aggregate/interface 和 dispatcher 注册新独立 schema/consumer。新增 schema 使用新 identity；既有 stable profile 的最终语义保持。MIGRATION-636 精确声明切换集合和旧 current 输入退出，不能只机械加 key 或改变旧 `committed` 含义。

## 6. 状态、顺序、正常与失败流程

**F636-01 首次早期反馈。** 已接受计划并处于 implementing；实现 owner形成可审查内容，执行本计划最小自检。TaskCommit AI检查并 prepare 精确提交，按当前对话取得该次提交确认后 invoke。`draft_committed` 不触发Check或Review通过。Publication预览同repo/base/head/正文和最大副作用，完成语义检查及当次远端动作确认，再 `ensure_draft -> push_content -> bind_pr -> converge_metadata -> draft`。创建无完整 Check 的真实 Draft；此后才能使用Draft反馈推进验证。

**F636-02 并行内容分析和验证。** feedback router 固定 B/H；启动独立 BranchReview早期 profile 和 implementation/Check 的命中验证。两者在相同候选上并行，不因目标前进取消内容审核。早期问题由原 owner修复；HEAD 改变后旧分析只保留历史含义，对新候选 fresh 审核。验证命令绑定 branch HEAD H；组合验证另写 target T 与组合 M。冲突、无 merge ref、pull_request CI 未触发时，仍执行本地/业务受支持 HEAD 入口，组合项目写明确未运行原因、恢复条件。不得把 source-code/package测试当远端CI通过。

**F636-03 更新Draft。** 修正、实际冲突解决或新候选需先回原当前 phase owner 合法 rework 到 implementing；原 TaskCommit早期 profile再提交。Publication只采用同 repo/base/head 的唯一Open PR及可快进分支，保持 Draft，更新同PR正文。无实质dirty时恢复现有提交，不造空提交。若没有实际整合需求，不制造同步commit。

**F636-04 Ready 后修订。** 在当前 publishing 阶段由 Publication `delivery_return_to_draft` 显示同PR/HEAD与回退计划。原 owner先读回实际状态，按自己合法上游 rework失效受影响gates并回implementation；同一可恢复动作将 PR退回Draft。已经退回的实际状态直接恢复，不重复转换。新未审候选必须在远端Draft事实确认后才push。随后早期提交/发布仍用原key/PR。旧readiness不接受新HEAD；最新完整Check、正式BranchReview、readiness完成后，原最终Publication再转Ready。

**F636-05 最终质量与交付。** 完成实际RDT和Architecture reconciliation/promotion，原implementation对实际候选 `begin_check`，独立Check完整判断并正式记录。必要最终提交仍走原Check绑定路径；若HEAD变化，按原router重新获得适用Check。正式独立BranchReview固定完整B/H，不能自动采用早期审核pass；其正式记录保留Check predecessor。DeliveryReview检查完整证据、范围与正文；Publication readback 当前候选与PR状态后Ready。Merge仍需完整live gate与单独合并授权。Completion/Closure/Finish/适用Cleanup依整体事实执行。

**F636-06 普通失败和结果丢失。** 本地prepare后内容/HEAD变化返回原提交owner重备。commit已成功但stdout丢失由同receipt恢复，禁重复/空提交。远端Draft创建、push、编辑、Draft/Ready转换已成功但输出丢失，原Publication从原事务与实际同PR/HEAD/payload恢复；只接受原preimage或已完成postimage。新候选不匹配旧动作时，先恢复旧事实，再fresh预览新动作；不把历史ready变成新pass。失败、SKIP、未执行逐项保留，不能填green。多个PR、非同repo/base/head、非快进或缺上游当前身份均阻塞实际mutation并给原owner修复条件。

以上只处理诚实协作下的正常差错、外部状态变化和明确输出丢失，不增加攻击模型、锁、压力竞态或非常规crash协议。

## 7. 恢复、兼容、迁移与集成

本批采用直接演进加一次性迁移，无长期runtime兼容分支。旧完整安装维持其固定版本；切换时完整 matching workflow、packages、runtime、schemas、manifest、preset及平台投影成套应用。旧schema诊断/不可变历史资产只保留真实原consumer，不作为新运行时fallback。MIGRATION-636逐项定位受影响profile/DTO/私有事务、producer/consumer与退出条件。

- implementing 的在途Task保留identity/accepted_scope/planning；新早期入口无需伪造Check。没有合法accepted Planning时回原Planning，不自动放行。
- checking/reviewing 的任务可完成当前最终链；需提前发布修订则由当前原owner合法rework到implementation。已有固定B和历史事实保留。
- publishing的同PR Ready修订由原Publication退Draft/rework，不由implementation冒用publication角色。
- 未执行旧commit candidate不转换为早期pass；原TaskCommit从实际dirty和当前gate重新prepare。已成功receipt先经原owner恢复同提交，禁止为了迁移制造commit。
- 旧Publication事务由原owner的一次性迁移处理：读回原PR/HEAD/载荷/阶段，completed Ready保持历史；pending动作保留已完成事实和剩余动作，仍需真实适用readiness才完成Ready。迁移不把旧Ready意图改写成Draft，不执行远端mutation，不合成gate。输出丢失在原producer恢复后才切换；同操作匹配不明确时停止。
- 新Draft事务恢复继续原same-plan入口；终态历史事实与当前gate分别处理。delivered/stopped、已归档和无PR任务不转换为活动Draft，也不重开Issue。

所有升级通过canonical preset/official支持面，保留用户修改、模板hash与`.new/.bak`冲突处理。重apply后检查actual安装、可执行权限、sidecar和drift。没有后续Delivery接口依赖；本批不能要求安装#637/#638。

## 8. 验证设计

| 验证 | 对应场景/验收 | 输入、入口与预期观察 | 证据限制 |
| --- | --- | --- | --- |
| V636-01 | S01、AC01/02 | 无Check的已激活候选经公共TaskCommit真实提交，再经公共Publication创建Draft；正文含待完成项，最终Ready/Merge拒绝缺gate | 需真实GitHub副作用计划；单元测试不能替代真实Draft |
| V636-02 | S02/03、AC03/04 | 同PR更新真实新候选；Ready先退Draft后push，适用证据后再Ready；唯一PR/key保持，旧readiness不能放行新HEAD | 状态机fixture覆盖每个阶段；真实远端链另列 |
| V636-03 | S04、AC06 | 正常executor/recorder输出丢失场景：commit、push、create、edit、Draft/Ready转换已执行后，同原调用恢复同身份；无第二commit/PR | 不手改hash/artifact构造安全负例；只覆盖合同要求的恢复点 |
| V636-04 | S05/06、AC05/07 | 独立Agent在固定B/H审核完整diff，验证worker同时运行HEAD命中检查；fixture中target前进、冲突/无merge ref/CI未触发仍进入HEAD入口，组合结果分开失败/SKIP/未运行 | fixture不证明业务CI真实运行；本仓不创建Backend CI |
| V636-05 | S07、AC08/09 | full/partial、默认/非默认目标均Refs-only；正式Check predecessor及current候选完整；Draft结果/旧gate不Ready/Merge；最终收尾仍由原owners | 本项不自动关闭Issue；整体Closure另作实际判断 |
| V636-06 | S01..07、AC10 | package/interface graph、runtime/family集成、canonical/installed、Codex/Claude/Cursor投影、完整preset reapply/drift和sidecar | 非完整Release/多平台throwaway矩阵 |
| V636-07 | S04/07、AC06/10 | 正常旧在途各phase、commit receipt、Publication pending/Ready事务经原owner一次性迁移；不丢PR/HEAD/已执行动作，不造gate | 不承诺未知旧版本；精确支持范围由matching migration列出 |

最小早期自检为：人工读完整拟提交diff与untracked内容/敏感信息、`git diff --check`、受影响Python语法/JSON schema检查，以及最小TaskCommit/Publication正常新入口定向测试。实际命中测试须在实现中定位并运行；完整package/runtime、平台和reapply不作为所有Draft提交统一前置。Draft后执行本批完整验证。任何失败/SKIP均在正文和证据中如实区分。

## 9. Canonical 引用、本轮差额与实际未决项

`docs/{requirements,design,test}/current/task-delivery-lifecycle.md` 分别拥有当前行为、D531职责/时序和T531/T530/T600/T557/BEH567验证定义；本轮差额为早期提交/Draft、同PR状态转换、候选与验证对象及在途迁移。原RDT维护owner在Phase2前将真实差额按implement的Docs Plan收敛，不复制整个旧定义。

Architecture引用 `.103` README、constitution、`06-governance/change-contract.md`、ADR-024/028/030、ARCH-DOM-042/043 与 ARCH-GOV-008/009。本批真实贡献在本planning_root的 `architecture-contribution.md`，决策候选在 `adr-early-draft-pr.md`。它们只描述本Task的拟变更，不晋升共享CURRENT；final_plan独立评估后仍须Phase2实际候选和完整拟写内容独立评估、原owner晋升/实际写入判断，再最终Check和committed独立Review。

本方案没有未决产品选择。具体实现若发现上游API不能合法承接已设计的原owner rework，或真实支持边界需改变，则停止该动作，返回原Author/Architecture修订，不改官方源码或开新Issue绕过。真实远端验收尚未发生；计划接受不替代commit、push、PR、merge或cleanup的具体授权。
