# #861 gen2 D2：正式采用设计

## 1. 设计目标、需求承接与内容基线

本批承接PRD A-R1–6/A-AC1–5，public current选定anchors保持，不重新承担前序历史源码。目标是M完整源在gen2准备checkout的正式采用及本批完整交付。

原public constructor实际选出固定B=343bc3100ea8f157bfd20d7a6a226455dbe482f4，来源是本Task前一实际delivered head；Planning H0同B。M=2938801829c8b8862e71d522891c79e8efb2d47a是拟采用source，不是D2 fixed B。PR target为main。当前不记录实施Candidate或开始Check；TaskCommit后由原constructor完整枚举全部实际installed dirty increment。

独立Architecture candidate_assessment实际返回baseline_current/no_architecture_impact：复用ARCH-INT-015及原tools owner，无产品机制/API/authority扩张。适用authority为docs/architecture/README.md（guru-trellis-architecture）、docs/architecture/00-foundation/design-constitution.md（guru-trellis-design-constitution-v1）及docs/architecture/06-governance/change-contract.md（guru-trellis-architecture-change-contract-v1）。候选判断不代替final_plan/Approval。

## 2. 当前系统、边界与目标差额

D1内容H343经PR #877合并为M。远端M parents为5dc0708a1d817fb9fb02edb64419b7b3c3f7cc10与H343，M/H343 tree均为20211932191f2d63ddff8c5dbd844eaa8902e873。当前本地尚无M对象，clean primary仍5dc；Activation后才原Sync取得来源并核HEAD==M、canonical clean。main推进时先判断差额/刷新来源，不用M source_ref执行另一HEAD。

唯一target为/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/861-release-v070-guru10-gen2。installed extension虽为.10，source仍79c25b5eaafdbcf415393535a16a7b1c0d281284。四处旧commands.json位于installed Discovery package、shared/.agents、Claude、Cursor。此前完整mapping其余bytes/modes匹配；配置仅注释/空白不同，必须preserve原bytes。起点观察不代替after验证。

原installer生成完整M资产及provenance，保留三平台选择，CLI/Core .6及Fork e379325。预计受管根包括.trellis/guru-team、workflow、spec、公共Skills/platform overlay和上游public tools；实际写删必须以actual frozen plan为准，不能只手补四文件。AGENTS由原renderer维护Guru block；目标checkout-local pointer可变。canonical产品源码、历史Task、session、用户配置、peer/common pointer不属于tools写集。

## 3. 来源设计处置（唯一）

| 来源/条款 | 原承诺 | 处置与落点 | 理由、影响、上游处置 |
| --- | --- | --- | --- |
| private release：Complete Source Before Actual Adoption | 完整D1 actual delivered后Completion/Creation才有D2 | retain；PRD§3、设计§2/6 | 真实上游已成立，不用dirty源或提前建片 |
| 同合同：目标证据与保留 | 全量installed、source/CLI/lock/native/mode/sidecar与保留 | retain；§4/8、implement V2/V3 | 临时安装不替代真实采用 |
| 同合同：Whole Preparation Completion | 全部准备后原Completion/Closure no_mutation/Finish，Refs-only | retain；§6/7、Policy | D2 merge不自行关闭Issue或完成Task |
| 同合同：Stage 2 | 准备/簿记合入后最新main冻结，各发布动作分别确认 | retain；§7 | M仅采用源，不是最终发布候选 |
| tools：Forward behavior/write boundary | 完整source launcher、actual inspection、prepare一次及精确写集确认 | retain；§4/5、implement V1/V2 | 不用旧dispatcher，不猜preimage或重prepare |
| tools：AGENTS/target/preservation | custom workflow、恰一custom AGENTS原renderer、target自身执行、peer/common保留 | retain；§4/8 | 保持单writer和最小目标隔离 |
| tools：same-operation recovery | 原ref/source/plan/preimages，complete仅验证 | retain；§6/7、implement V3 | reapply须真实执行原installer |
| Sync：sync profile | clean注册main、fetch/ff-only，不安装tools | retain；§4、implement V1 | source取得与target安装分离，不新建checkout |
| root AC9 whole-source条件 | 新源实际采用后、WholeCompletion前完整existing | retain；§8 V4 | 一项Codex cell承接R4/R5/AC3兼容，不重做R11源码或扩矩阵 |

全部retain，无change/reject或新的上游范围选择。

## 4. 模块、职责与设计取舍

1. 原Sync对clean primary main执行既有sync；实施owner核M。primary只供应完整clean canonical，不安装primary；dirty authority由原Sync阻塞，不换更容易的peer。无需新worktree、临时commit或source映射。
2. 原tools从M的trellis/skills/guru-team/packages/guru-upgrade-tools/scripts/{preview,prepare,invoke}.sh进入。先核相交未完事务、actual maintenance inspection、旧来源与managed edits，逐路径preserve/replace，不接管上游trellis-*或用户文件。完整冻结计划由原API产生。
3. 原public applyMaintenance写已审upstream tools/workflow；原Guru installer安装完整资产、生成manifest、激活checkout-local pointer。同operation拥有恢复。手复制四文件无法承担完整provenance/保留责任；不新增安装器或第二authority。
4. 实施验证owner读取完整mapping并独立比较实际集合/bytes/modes。config、AGENTS renderer结果、manifest/source各按自身语义检查，不一律raw-template比较。复用target resolver/validator/native continuation及existing driver，不建结果账本。
5. 原RDT/Architecture复核实际after；真实差额才整合/readback。TaskCommit及独立完整Check/Branch Review/readiness/Publication/Merge保持原边界。

## 5. 接口与数据

无新API/schema/profile/业务字段。正式public input：
    {"profile":"install","source_ref":"2938801829c8b8862e71d522891c79e8efb2d47a","dependency_mode":"source_locked","checkout":"/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/861-release-v070-guru10-gen2"}

upstream_source来自锁定Fork实际CLI/Core roots、byte identity及public maintenance API1.0。private-prepare沿现有schema带该source、target实际selected_platforms、逐路径guru_decisions与public tools_input。workflow为install/custom、canonical全文、guru-team模板及immutable M provider，不标bundled native。AGENTS恰一custom决定，source为actual snapshot，content为已审原全文base，由原pure renderer组合；其它required/skip/user-edit按actual inspection，config preserve。

preview/prepare完整receipt保留exit/stdout/stderr并消费result；prepare result.plan不改值，临时regular UTF-8文件只供本operation。invoke只消费该frozen plan。tools_upgraded仅证明安装结果，unverified不得含formal_fork_source_lock；resume_required回同owner原ref，blocked停。不存在安装pass直接进入Completion的投影；不持久化用户授权。

## 6. 状态、顺序、正常与失败流程

当前为planning。已完成Author需求→独立candidate；接着本方案→Author plan_ready→独立final_plan→Approval→展示并停Activation前。未来接受后原Activation进入：clean M来源→preview→prepare一次→审真实写集及安装确认→invoke→目标验证→真实同操作reapply/drift→完整existing→知识整合/readback→TaskCommit→固定B..H→一次独立完整Check/Branch Review→readiness/Refs-only Publish/Merge→原Completion。

source/lock/API缺失、相交未完事务、unknown edits、sidecar由原owner停止/恢复。tools不把旧Task解析为current，也不转换历史。必要验证失败保真实输出；区分执行/环境与源缺陷。source/机制实变回Author/Architecture；真实范围选择回Clarify。不删断言、改hash或manifest换取pass。

## 7. 恢复、兼容、迁移与集成

仅工具采用，无Task数据迁移、数据库或生产部署。部分写入/输出丢失使用原ref/source/plan/preimages，不重prepare、不刷新anchors、不纳入后续业务改动。rollback为原tools另审的有界写，先核public兼容再原序恢复，不resetGit。

真实reapply复用现有native install test的same-operation install_assets及原proof；complete后resume仅验证。普通apply历史Task guard保持。完整existing从正式.9正常安装后经原维护路径升M。历史schema及原固定provider恢复保留，旧schema不回current。四help的context_request2.0与Discovery自身supplement1.0分别核。

D1临时分发、回归和CI事实仅在输入/依赖/工具链/参数/检查定义仍适用且可核验时采用。本批target采用/preservation/native/reapply/existing是新增事实，不从前序推断。D2后原Completion审整体，Stage2另冻结latest main，无其它Issue状态前置。

## 8. 验证设计

| ID | 需求/验收、层和观察 |
| --- | --- |
| V1 | A-R1/A-AC1；来源层：actual delivered、clean M、Fork lock/build/API、target/peer布局和未完事务。M不是最终发布candidate |
| V2 | A-R2/3、A-AC2；真实tools写入：actual frozen plan与target after及保留，无formal lock未验证；exit不替代内容验证 |
| V3 | A-R4/A-AC3/4；目标集成：完整map/集合/modes、manifest/source/CLI/lock、target自身resolver/installed/native continuation、四help合法输入与返回，同operation真实reapply/drift/sidecar。不声称所有客户端Agent业务成功 |
| V4 | A-R5/A-AC4；原.9→M Codex完整existing及aggregate，实际init/维护/reapply/全validate；不是累计矩阵或Stage2 pass |
| V5 | A-R6/A-AC5；原知识、完整fixed B..H Review及Refs-only交付；未实施后继不声明完成 |

命令/环境见implement§3。前序长期回归定义/输入未变不因换Delivery重跑；V1–V4是本批必要真实观察。不新增镜像实现的测试，不要求重复旧失败/回退红绿；充分后停止可选诊断。

## 9. Canonical 引用、本轮差额与实际未决项

docs/{requirements,design,test}/current/codex-skill-distribution.md：R724-01–06/D724-01–04/T724-01–05的共享root、平台选择、旧根退出、原维护writer及证据分层；不改变定义或把历史native结果当本次执行。.trellis/spec/preset/installer.md的Existing checkout tools maintenance、Codex shared discovery migration、Tools-only target runtime isolation及原tools完整contract约束实际写入。Architecture见§1及ARCH-INT-001/006/014/015，无新authority/GAP。质量方法为Test And Validation Value、Validation Scope Ownership及workflow Candidate Applicability And Coverage。

当前无规范性差额，不预建contribution/ADR/共享导航。原RDT/Architecture在真实after复核；新事实确有差额则回Author刷新规划，由原writer提交前final_integration/readback，随后独立committed Review审before/after。无待用户选择；actual frozen writes和工程结果仍是未来前置。当前不Activation、不安装。

