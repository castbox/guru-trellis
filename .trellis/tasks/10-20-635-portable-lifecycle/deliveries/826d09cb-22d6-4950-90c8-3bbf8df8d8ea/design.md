# 跨环境生命周期基础 D1 设计

## 1. 设计目标、需求承接与内容基线

本稿承接本批PRD全部R1–R5/S1–S8/AC-V1–V8。Task为`635-portable-lifecycle`，generation0；Delivery为`826d09cb-22d6-4950-90c8-3bbf8df8d8ea`。当前独立Architecture候选评估选择`architecture_impact / legacy_boundary_convergence`。它确认当前三项机制没有架构阻塞，只交原Author收敛方案；公共能力采用另有实际证据，不等于final_plan、Approval或Activation。

开发基线B和Planning H0均为`7a7b60743499653ffeb81f6b31e627a02c33f579`。B已通过原`DeliveryProjection.content_base(key, development_base=该SHA)`只读解析并读回，来源为独立基线clone的明确开发基线；无前序Delivery或既有candidate覆盖它。PR集成目标为`castbox/guru-trellis:main`。普通远端前进不改变B，不移动受保护主checkout的本地main。

阶段适用baseline为`guru-trellis-architecture`，constitution为`guru-trellis-design-constitution-v1`，change contract为`guru-trellis-architecture-change-contract-v1`。本稿保留其公共模型、原owner、唯一consumer和单写约束。第5/9节已更新实际公共API和精确采用目标；matching构建与canonical source采用已完成；第5.6–5.9/7.1节已形成全链适配与迁移方案，同目录真实贡献/ADR仍为proposed。当前方案交原Wording、Architecture final_plan和Approval；目标安装及V1–V8在实施阶段验证，不是规划前置。

## 2. 当前系统、边界与目标差额

本Task没有前序Delivery。当前canonical source lock已由7f050采用Trellis PR #55的精确merge `1e22a77b8edcec0269252436c1f6df6c52d99734`，CLI/Core仍同为`0.7.0-castbox.5`。准确source构建与validator已通过；这不表示目标安装已采用。

现行`guru-reactivate-task/runtime/invoke.py:archived_identity`读取公共Task2 Completion/Closure及summary后调用`verify_finish_seal`。后者把common-dir ledger或manual Finish/Cleanup作为准入条件。已在无原机私有记录、未修改archive的独立clone对真实#638归档得到`finish_result_unsealed/manual_finish_result`。该结果只证明入口缺陷。

目标是由原语义owner从共享公共记录、精确Git历史和live GitHub解释共享事实；本机状态继续服务当前执行与资源处置。不会把全部runtime改成缓存，也不会把其整体提交Git。只有证明共享记录不足、且直接consumer无法重新推导的必要输入，才沿既有任务位置或公共模型补充；字段及迁移先由原owner审查。

## 3. 来源设计处置（唯一）

本次Clarify的`source_selection=[]`，没有额外选入Issue中的规范性来源设计。整体要求和durable current约束继续有效，不因该空集取消。具体取舍只在本节维护，PRD/implement引用本节。

| 当前约束 | 处置与落点 | 原因及边界 |
| --- | --- | --- |
| ADR-024：公共Task/Delivery/session与转换归Trellis，Guru原owner判断语义 | retain，第4–7节 | 不在Guru实现Task2 converter/store或第二状态机 |
| ADR-027、ARCH-DOM-032：普通current-only，旧archive只读诊断/独立维护 | 窄change候选，第5/7节 | 增加明确受支持正式旧schema1归档的一次性公共转换；人工历史和未完旧事务保留原路线，不扩任意旧格式或普通dual-read |
| ARCH-DOM-054：公共维护writer、原私有controls owners与实际native/下一owner | retain，第4/6节 | 转换数据成功不能冒充native续接或业务完成 |
| Finish先投影归档→合并bookkeeping→验证target→封存本机资源 | retain，第6节 | 共享持久化与本机seal责任分离；不删除归档合法性验证 |
| Cleanup的repository/ref/expected-head及generation约束 | retain，第4/7节 | 保留新提交、未知ownership及其它Task资源，不用旧回执删除新代资源 |
| #636/#637/#638的Draft、当前候选适用性及晋升先于最终Check | retain，第6/8节 | 换机不继承旧pass；原owner亲自判断当前适用性，实际promotion进入同一最终候选 |

上述窄change由本D1的`architecture-contribution.md`与`adr-portable-lifecycle.md`提出真实候选，说明替代范围、实际consumer、迁移及退出条件。它们没有晋升shared CURRENT；不能把本表或候选当作已生效架构。

## 4. 模块、职责与设计取舍

下表是待落实的责任边界。现行原owner继续拥有内部行为；实现前仍需逐个读取其完整合同、实际读写和直接consumer，补齐未核实项，不能仅按此表宣称R1完成。

| 状态/producer | 直接consumer与目标处置 | 缺失入口及阻塞范围 |
| --- | --- | --- |
| 原Creation、公共Task writer的TaskId/source/accepted_scope | Identity/Clarify/Creation及whole Completion；从可获取公共记录核验共享身份 | Identity/原scope owner；身份或authority不唯一仅阻塞所选Task |
| 公共Delivery writer的key、phase、planning_root、历史结果 | 原阶段owner/Continuation；恢复同一实际切片，不新建替代Delivery | 原Creation selection/阶段owner；未知selection不能由目录猜选 |
| 原Bind/session pointer、C4 branch binding、checkout ownership | 原Ensure/Bind；当前环境重建或恢复，不携带原机路径 | 原Establish→Ensure→Bind；仅所选环境，保留原资源冲突 |
| Author/Approval/Activation的当前planning | implementation/Check；从公共关系与实际正文重新核当前资格 | 原Planning producer；文件和phase不证明批准，不补造freshness |
| 原Check/full Review的公开结果与可核验工程事实 | 当前Check/Review/Readiness；分别判断仍适用、需补审或需补跑 | 原producer重审命中项；缺checkpoint本身不要求重开Intake/Delivery |
| 原Publish的Open Draft/Ready与原输入 | 原Publish；核同repo/base/head/key与实际payload，只补剩余动作并重判readiness | 已知输入可取时原Publish恢复；不可推导输入缺失明确报告，不重新创建PR |
| 原Merge及公共Delivery result | whole Completion；复用现有manual merged recovery核实际双亲MERGED/Publication关系 | 原Merge；无匹配关系不冒领成功，不重复merge |
| 原Completion的whole-scope result | Closure；当前代真实整体审查，证据补充不造空Delivery | 原Completion/evidence_refresh；历史slice成功不代替整体完成 |
| 原Closure的action set、public source result | 原Finish/Closure；核精确动作、原输入、live状态，仅恢复已发生子动作 | 原Closure；只有CLOSED不能重建原归属；必要输入缺失保留具体停点 |
| 原Finish的archive/summary、bookkeeping与target历史 | 原Reactivate/Completion；共享终态从精确历史核验 | 原Finish恢复未完成事务；已证实共享终态不因本机seal缺失退回未完成 |
| 原Finish/Cleanup的seal/资源ledger/expected head | 原本机Cleanup；仅对应common-dir与原generation的资源责任 | 原资源owner保守处置；不能阻塞另一环境用不同合法资源继续 |

主要命中文件在`trellis/skills/guru-team/packages/`对应原package、`trellis/skills/guru-team/runtime/task_lifecycle/`及`runtime/delivery_projection/`。Markdown定义判断，runtime只读事实、执行明确操作及校验。global workflow仅改必要typed transition；不把step-local过程复制进workflow/overlay。

正式旧格式选择直接公共转换，不选择“保代resume→新的Completion→Closure→Finish→Reactivate”。后一组合可以产生真实新结果，不能一概称为伪造；但它为已完成旧归档新增旧代终态工作、bookkeeping/新archive及同代资源责任。现行ledger拒绝用establishment覆盖同代ledger，Finish拒绝覆盖既有archive。直接在公共模型一次增代能保留旧终态及旧资源责任，避免为迁移额外重做旧代收尾。

## 5. 接口与数据

原公共操作继续保留下列边界；PR #55已增加独立正式旧归档操作：

| 真实公开接口 | 已核实行为 | 与所选机制的差额 |
| --- | --- | --- |
| `prepareTaskConversion` | 只接受direct active Task；projection保留generation | 不能直接消费正式旧archive并增代 |
| `prepareArchivedTaskResume` / `validateArchivedTaskResumeProjection` | schema1/known legacy→Task2，保代；raw archive只读；禁止导入Completion/Closure/current gates | 不提供基于旧正式终态的`g→g+1` |
| `reopen_task` | 当前generation有匹配Completion时递增，并支持其限定恢复 | 旧正式schema1没有该数组，不能用旧status/summary合成Completion来放行 |

依赖owner仍为`castbox/Trellis`的CLI maintenance与Core Task模型。`prepareFormalArchiveReactivation`现为已合并的正式公开API；API存在、所选matching构建可调用及目标原生安装已采用是三项不同事实。

实际输入、结果和唯一公共writer见下节。Guru原语义owner核正式旧终态并作薄适配，不另建模型。完整扫描、Git派生hash、review过程和授权不进入公共handoff。

### 5.1 已合并公共前置及准确采用目标

Trellis PR #55的source为`1e22a77b8edcec0269252436c1f6df6c52d99734`，有序parents为`6202fc2da435a4d1f0e2e67eb01f2e61ec50ca51`、`86de668ee516d9f12461fe0638d4c9fa6579fdd0`，tree为`6074f7f8bebf6c8c43116e4c43c8554dc08db07c`。精确merge的成功push CI是`39449964080`，不是PR head的CI。CLI/Core均为`0.7.0-castbox.5`，package manager为`pnpm@10.32.1`；现有source-lock schema 1.0不加字段。

已采用的唯一canonical记录内容为：

```json
{
  "schema_version": "1.0",
  "repository": "https://github.com/castbox/Trellis.git",
  "commit": "1e22a77b8edcec0269252436c1f6df6c52d99734",
  "parents": [
    "6202fc2da435a4d1f0e2e67eb01f2e61ec50ca51",
    "86de668ee516d9f12461fe0638d4c9fa6579fdd0"
  ],
  "tree": "6074f7f8bebf6c8c43116e4c43c8554dc08db07c",
  "ci_run_id": 39449964080,
  "cli_version": "0.7.0-castbox.5",
  "package_manager": "pnpm@10.32.1"
}
```

相对旧lock 7f050，额外source差额除PR #55外仅包括#53的完成证据、规格和归档；不得把上游Task归档带入Guru任务树。真实merge checkout须保持干净，用自身lockfile安装依赖并按Core→CLI顺序build，成功后才生成`packages/cli/dist/.guru-source-commit`。同版本、同tree、此前86de的packed证据均不替代精确merge构建。source采用前的实际dist曾只报告旧4种operation且缺build-origin。现已用该merge自身冻结lockfile完成Core→CLI重建，成功后生成来源标记；实际contract已返回新operation和capability，source validator核对212个template通过。

Core拥有纯领域校验；CLI拥有参数、Git/文件事实与固定计划executor。是否正式完成、旧事务是否未完、恢复原因和下一语义owner仍归Guru。公共API不解释Guru summary、Issue disposition或semantic pass，不接收授权字段。独立Architecture本轮只读复核认为实际能力足够支持原方向，没有新增provider缺口；正式candidate/final_plan与下游门禁仍按原owner执行。

### 5.2 已合并公开合同与Guru适配

以下名称和字段已按上游`api.ts`、`tasks.ts`及`shared.ts`核验。Guru目标安装尚未采用；其调用前必须检查实际capability。

| 接口 | 输入与职责 | 输出及直接consumer |
| --- | --- | --- |
| Core `/task/maintenance`：`validateFormalArchiveReactivationProjection` | 原始schema1对象、完整Task2 projection、原owner核验的历史fact dispositions。校验不可变identity/source/metadata/tree，要求新generation恰为`g+1` | 返回经验证的Task2对象，唯一consumer为CLI preparation；不执行Git、文件写入或语义判断 |
| CLI maintenance namespace：`inspectFormalArchiveReactivation` | 明确root、旧TaskKey、archive task_ref、original_task_ref及archive commit；只读选定对象和可获取的同Task后继 | 返回前驱定位及带公开provenance的后继事实。原Guru owner判断复用、继续准备或真实歧义；不从目录数量选Task，不枚举其它机器 |
| CLI maintenance namespace：`prepareFormalArchiveReactivation` | 下表的封闭输入，经Core校验后构造新kind固定计划；prepare不写目标 | 返回`PreparedMaintenancePlan`的新`formal_archive_reactivation`分支，供现有preview/apply/recover/resume/rollback消费 |
| CLI `trellis maintain` | 新只读`inspect-formal-archive --input <file> --json`；现有prepare envelope增加`kind:"formal_archive_reactivation"` | 与SDK相同事实/计划；仍是单份JSON和原MaintenanceError约定 |

prepare已独立定义`FormalArchiveReactivationInput`，不把大量nullable字段并入普通conversion/resume输入：

| 字段 | 确切用途 |
| --- | --- |
| `root` | 已存在的目标checkout；maintenance不创建branch/worktree。原Guru资源owner在调用前选择合法执行位置 |
| `key:{task_id,lifecycle_generation}` | 精确前驱TaskKey，generation为`g`；原始source必须匹配 |
| `task_ref`、`original_task_ref`、`active_ref` | 原monthly archive、经审查原active路径、新active目的地。不得从basename猜原路径；新目的地必须未占用 |
| `archive:{commit,target_ref,target_head,evidence}` | `commit`为承载准确归档结果的已获取commit，可使用精确bookkeeping merge；`target_ref`为明确所选可解析Git ref；prepare时解析到`target_head`。CLI核归档commit可达所选目标、该归档树不存在原active路径；evidence只接受可核其准确历史内容的仓库文件AuthorityRef。Git OID复用原公开规则，不另限为40位。PR归属和终态充分性仍由Guru判断 |
| `projection` | 完整当前Task2，TaskId/source和Core校验要求的原metadata保持，generation为`g+1`且有实际accepted_scope authority。无当前新代Delivery或gate；旧代真实Delivery只作为历史结果保留 |
| `artifacts`、`legacy_facts` | 复用已有有限artifact disposition与原owner历史事实归属类型；保留原字节/模式/目录，只有真实planning projection写入现有允许位置，不补造历史成功 |

新输入不带旧session、branch binding、resource ledger或其退休动作。新generation的绑定由转换后原Establish/Ensure/Bind完成；旧generation本机责任留在原owner。下一语义owner也不由executor运行或持久化；调用方已拥有恢复目标，实际新key/ref足以交给原Continuation。

实际Core校验要求：仅schema1前驱，原status为completed，整数generation可安全递增，旧id/source/元数据/树关系不变，无补造Completion/Closure或继承gate。status条件只作必要格式/状态校验，不能单独证明正式完成。历史Delivery仍属于其原generation且为原producer核实的真实终态。不要先伪改source.generation再调用普通migration来通过保代校验。上游已将共同identity/history规则抽取为私有`migration-projection.ts`，保代与增代分别传明确规则；原public `validateTaskV2Projection`继续保代。

所有projection中的accepted_scope、plan/evidence AuthorityRef必须指向实际保留的archive、准确Git历史或计划将写入的真实文件，prepare按原public resolver/authority规则核对。不能只保证文件复制而留下旧active locator无法读取。`artifact_origin`仍遵循现行显式relocation合同，不为使新validator通过而方便性补写；若所选输入必须改变origin，先走该原公开owner，而不是增加第二重定位器。

### 5.3 固定计划、最小provenance与结果

新plan分支复用既有`operation_id`、候选CLI/Core identity、source/target snapshots、pending/apply/rollback逻辑。guard分别保留前驱key与目的generation，禁止直接复用当前只含`generation:g`的task_resume result投影，否则会把新结果错误返回为旧代。

写集仅含新active Task树、完整保留的原始`migration/source-task.json`、必要planning projection与一个新的`migration/formal-archive-reactivation.json`。原archive全树只读。新provenance只保留直接consumer需要且无法从新Task2单独推导的前驱key、archive_ref、archive commit和original_task_ref；新key可从当前Task2读出。原identity/history consumer据此定位并校验旧source，consumer仍须使用公共parser。该文件不是review pass、授权、资源ownership或第二生命周期ledger。

结果使用新kind的独立类型，保留原maintenance状态/恢复信息。只有`status=applied`的新结果交出`reactivated_task:{key,task_ref}`给调用方；prepared/pending/rolled_back不宣称active可用。普通task_resume的`resumed_task`返回仍保代。重复apply、recover与resume读回同operation和同新key，不二次增代。

私有事务丢失后，原owner先调用只读inspect。若公开新Task2/provenance与原始source、archive commit和前驱key完整匹配，复用实际可获取后继，不重新prepare或创建空事务。身份或关系不唯一时只返回具体事实/错误，交原owner。后继查询只覆盖明确可获取的当前source，不能声称其它clone不存在未发布incarnation。

首次转换必须恰为`g+1`；后继识别还需覆盖后来合法完成并再次reopen到`g+2`及以后。该分支核原provenance与真实公共历史关系，由原owner继续实际可获取的后继，不把任何同id高generation都当作同一操作结果。新代后来前进时，原operation的result仍描述其当时输出，不能改写成最新代；当前选择通过只读后继事实承接。

prepare固定准确归档commit及当时观察到的target_head。正常target前进时，只要原target_head和归档commit仍可达当前所选target，结果核验继续成立；不要求当前target与旧head完全相等。target不再含该归档、source或destination出现正常不匹配时沿原错误/恢复路线处理，不引入锁、租约或最新SHA追赶。

rollback只撤销该操作写入的新active树。新代出现真实后续Task修改、Delivery、session或branch binding时，保留这些工作并返回`later_work_conflict`；不能只核文件actions而遗漏operation之后由原Bind建立的新代session。旧代session/binding/seal/资源不在rollback写集。普通已完成操作的结果恢复与允许后续工作的只读后继识别分开，不能因native consumer已合法绑定就重复转换。

### 5.4 原生Python与分发边界

上游CLI/Core唯一完成转换，native不新增converter或放宽普通reopen。实际实现修订Core `v2/store.ts`与原生模板`common/task_utils.py`的身份预留reader：只有匹配保留前驱与真实转换关系时才允许relocation。普通create继续保留历史身份预留。模板与上游dogfood已同步；Guru必须经原官方工具owner取得该reader，preset不得代管Trellis-owned脚本。

`getMaintenanceContract()`保持`maintenance_api:"1.0"`，additive增加`formal_archive_reactivation` operation和同名capability：`task_families:["schema1"]`、`generation:"increment_once"`、`original_archive:"read_only"`。现有Guru transport能容纳operation集合扩展，但方法allowlist缺少`inspectFormalArchiveReactivation`与`prepareFormalArchiveReactivation`；本D1实施需在原transport增加两方法和显式capability检查，不只核版本字符串。

新result只有applied分支的`reactivated_task`可投影至原Establish/Ensure/Bind。successor inspection的`absent/verified/conflicting`由原Reactivate语义owner分别判断准备、复用或实际歧义。`archive.evidence`是repository-file AuthorityRef；GitHub PR URL只能供语义核验，不能直接塞入该字段。原生selection/continuation及下一owner需在Guru目标内实际执行，executor applied不构成其成功证明。

Core/CLI继续同版本成对构建和打包；本计划不预定下一个版本号或npm发布。原source owner已核验merge SHA、parents/tree、对应CI与包能力，并更新`trellis/presets/guru-team/source/trellis-source.json`。本地candidate proof、合入main、正式source-lock采用和实际目标安装分别报告。

### 5.5 两仓接续与退出

顺序为：上游独立Task规划/实现/Check及公开配对包验证→原Git交付流程→取得确切上游source与能力→Guru原source owner成套采用→本D1细化真实I/O及public projection/migration→原Wording/final_plan/Approval/Activation→实现并完成V1–V8。上游Task只完成公共能力范围，不替#635完成或关闭业务Issue。

Guru侧后续命中`runtime/maintenance_transport.py`的新方法allowlist/capability检查、Reactivate原package的语义及确定性适配、共享identity reader对新provenance的精确解释。人工历史archive_resume保持原合同；未完旧事务仍回原owner。legacy-only新入口的真实consumer退出后沿明确迁移删除，历史raw/Git证据继续只读。

公共前置已交付。精确matching构建与canonical source采用已完成，当前停点为Guru适配及实际目标消费；D1仍planning，旧阻塞规划没有因此取得批准。

### 5.6 D635-01 共享 Finish 判定与新 Reactivate 入口

原`guru-reactivate-task`增加闭合profile `delivery_reactivate_shared_archive`，独立input schema为`guru-reactivate-task-input-shared-archive-1.0`。input是`profile/mode/archived_lifecycle`与`archive_anchor:{repo_ref,archive_ref,archive_commit,original_task_ref,target_ref}`；anchor全部必填，不在旧输入上堆nullable字段。原语义owner从已选repository/Task与真实历史形成anchor，唯一来源可验证时自动承接；仅合法候选确有歧义时询问用户。schema1与Task2由准确历史对象的公共parser区分，不由调用方版本号决定。

当前实现的`archived_identity/verify_finish_seal/verify_archived_seal/release_resolved_prior_binding`将共享资格和本机责任混合。新路径由该package内的`runtime/shared_finish.py`承担确定性Git/GitHub与公共模型事实校验，SKILL/references保留AI对充分性、旧格式类别、恢复原因与下一owner的判断。该helper不是新skill、公共模型或持久化writer。

正常判定顺序如下：

1. 核实际repository identity及准确archive commit可获取；从该commit读取archive Task/summary/完整scope/history。按TaskId/generation/source/summary archive_dir与original_task_ref核同一前驱，不能先以当前工作树的active/archive状态排除历史。
2. 按原版本合同核共享终态。Task2必须有该generation、accepted_scope和Completion→Closure关系；指定schema1正式旧归档按固定真实旧安装的summary/交付/归档事实审查，不制造当前C/C数组。summary存在、completed、Issue CLOSED或一个PR MERGED都不足以单独通过。
3. 核精确bookkeeping PR属于所选repo/target，实际MERGED、归档结果含匹配archive且原active路径已移除，archive commit已进入所选target历史。只对实际缺失的Git对象交原事实owner有界获取；不移动任务分支、不Reconcile。target后续前进只检查历史包含关系，不要求当前HEAD等于旧merge，不要求把merge SHA写回自身archive。
4. 核当前可获取的同Task后继。Task2通过公共record及保留的原generation Completion/Closure历史、source与准确前驱关系判定；schema1使用公开`inspectFormalArchiveReactivation`。verified后继交原环境owners继续实际generation；conflicting交原语义owner，不重复reopen/prepare。不承诺发现其它clone未发布后继。
5. 没有后继才执行新代建立。Task2复用原公共`reopen_task`和既有合法archive relocation；指定schema1调用第5.2–5.3节正式公共operation。新格式不能绕过Completion；旧格式不能先补造Completion。prepared/pending/rolled_back不能投影已reactivated，applied只用实际key/ref。
6. 原Establish→Ensure→Bind取得本环境独立合法资源，原Continuation按真实新工作进入Author/Creation或无Delivery的Completion validation。旧代seal/本机退出/Cleanup只交原资源owner，不是新环境准入条件。同common-dir确实复用旧资源时仍核原冲突，不能用换入口跳过责任。

输出复用原`reactivated_to_planning`、`session_binding_recovery_required`、`resume_reactivation`和`reactivate_blocked`的独立合同及唯一consumers；不新增一个笼统成功出口。输出丢失先读公共实际后继，不依赖原机transaction。未入target的archive有唯一未完Finish事务时回原Finish；否则给具体缺口，不能把共享Finish已成立但seal缺失误报为未完成。

### 5.7 D635-02 Closure 的最小共享结果

已证实：原Closure `runtime/invoke.py`只在common-dir冻结完整`action_set`；public Closure只记source_closed/no_mutation、source_result和evidence。`runtime/task_lifecycle/closure_result.py`只读该私有交易，Finish据其完整集合逐Issue核OPEN/CLOSED。source_result无法在含额外Issue或retain/no-close处置时还原完整动作集。这是正常跨clone丢失私有状态的直接consumer缺口。

由原Closure单写一个task-local结果载体，路径为`closeout/closure/<safe-result-id>.json`。`safe-result-id`为ResultRef.result_id的UTF-8 base64url无padding编码，只作跨平台文件名映射，不是新增identity或索引。独立payload schema `guru-closure-shared-result-1.0`只含：`schema_version`、`result_ref`、`completion_result_id`、`source`、`action_set`。result_ref是原ResultRefDTO，actions保留现行issue_ref/disposition闭合类型。它们分别服务原Closure在public projection丢失时恢复原结果，以及Finish读取准确原动作/来源；不保留binding路径、gate、工程历史、Git快照bundle、review元数据、用户授权、逐轮verified状态或terminal断言。

原正常Closure在实际动作集语义审查后、执行provider动作前，根据同一冻结输入生成原result_ref和载体。它不是授权。调用方要在另一clone接续，Task/Completion及该最小必要输入须已提交并可从明确source ref/commit获取；不自动新增commit、PR或全链台账。仅原机未发布载体仍属于R3实际必要输入缺失，具体报告，不搬runtime。

成功核对所有required provider状态后，原公共`close_task`的evidence增加该载体AuthorityRef，保留原source evidence。公共Closure结果仍是既有schema/result，不向Trellis扩模型。载体本身不能证明动作已完成；消费者必须核准确ResultRef、Task/generation、Completion、accepted_scope与source关系，以及current provider状态。

`read_terminal_closure_result`以公共Closure的evidence和现有authority resolver读取载体，再按原snapshot2.0向Finish投影terminal/action_set/source；terminal从真实动作类型与公共结果核一致，不从载体字段或私有seal取得。payload读取及result/key不匹配停止原owner，不新增第二parser/生命周期。Finish原逐Issue重核和source漂移回Closure的语义保留。

增加闭合Closure profile `closure_shared_result_recovery`：输入为mode、精确TaskRef/ResultRef和共享载体AuthorityRef。公共结果已存在时核同一个并读回；结果投影缺失时，原AI重审准确Completion/source/actions及live状态后，才用原result_id补公共projection。这个profile执行零provider close。required CLOSED仍OPEN、required OPEN已CLOSED或归属变化时回原Closure具体缺口/外部变化；任何剩余真实close须回原正常profile并取得当前动作边界，不从共享载体恢复授权。

历史结果没有新载体时不伪造原集合。完整已完成旧archive仍按D635-01共享历史判定，不强加新carrier。旧在途记录仅在原必要输入仍可核验时由原Closure逐案写最小载体；确实缺动作集时报告这项输入及受影响Finish步骤，不能把它替换成找回原机隐藏receipt。载体与Task一起归档、按原artifact_origin解析历史，已有结果不覆盖。新代/新结果使用独立文件，后续原公共历史/Finish有直接consumer期间保留；不建立额外scan/index或每阶段日志。

### 5.8 D635-03 已有 Open PR 的跨环境恢复

原Publish `owner.py:unique_task_transaction/plan_from_input`在same_plan_resume/reprepare时要求原private交易；普通PR查找又使用当前本地binding分支。B可使用不同合法本地branch，因此不能按B分支创建第二PR或把旧Ready当新通过。原package增加两个独立闭合profile，复用同一Publish executor/现有typed outputs，不新建Publication模型：

| profile | 必填输入（另含mode/task_ref/delivery_key） | 原owner行为及唯一结果 |
| --- | --- | --- |
| `delivery_remote_draft_recovery` | `pr_ref:{repo_ref,pr_number}`、`source_commit`、`base_ref`、`candidate_head`、当前已审`pr_title/pr_body` | 核明确可获取source包含同Task/Delivery/Planning与B..H关系，读精确PR的repo/base/head/owner，审完整差额；复用该Open PR，补原Draft/metadata剩余动作。已有同head/payload不重复push/edit/create；Draft不写最终Publication gate |
| `delivery_remote_ready_recovery` | `pr_ref`、`source_commit`、`readiness_result_id`、`reviewed_head`、当前已审`pr_title/pr_body/remaining_work_state` | 核同key公共candidate/真实最终readiness及PR实际payload。实际已Ready且postconditions匹配只恢复原公共Publication；Draft只在当前readiness充分时补metadata/Ready。缺当前适用性回原Review/Check，不复制pass |

source_commit是承载共享Task/Delivery/必要代码的明确可获取commit，不要求已进入main。与PR candidate head不相等时，必须检查真实历史关系和完整内容差额，不按标题/branch猜身份。PR不存在、不属于原key/来源、base/head冲突或关系不唯一时返回原Publish具体缺口；这两个profile绝不创建新PR。

远端PR head ref与当前本地binding分开核验。确需push时原Publish在当前对话展示精确repository/full remote ref/expected head和待推内容，经原副作用边界后沿现有push owner更新同ref；不重写B的binding、不强制B认领A的本机资源。未知remote cleanup ownership仍保守保留；能更新PR不自动取得删除旧资源的资格。此处只恢复实际已发生子动作；返回Draft处理新未审修订仍走#636原回程。

MERGED Delivery继续原`delivery_merged_recovery`：精确public Publication、PR/双亲/target包含关系和actual内容足以恢复交付，不需要原Merge receipt，不发第二次merge。其delivered只交Completion；pending/failed CI、范围缺口及语义变化仍由实际owner处理，不因已合并补造readiness或Completion。

### 5.9 D635-04 全链状态处置与最小修改范围

| 原owner / 实际代码 | 分类及本轮处理 | 原始必要输入缺失时的准确路线 |
| --- | --- | --- |
| `task_lifecycle/identity.py`，Establish/Ensure/Bind及公共session API | 共享Task/source/ref由Git/public模型恢复；C4/session/local ownership在当前环境重建。复用#454，不提交本机映射 | source ref/commit不可获取或Task关系冲突回Identity；唯一合法来源不问routine选择 |
| Author/Approval/Activation、Check、Branch Review与`delivery_projection/gates.py` | public结果/实际正文是可核事实；语义当前资格必须原owner重审，工程命令按#464/#578/#637仅补缺失或不再适用的命令。新增Markdown明确这些恢复次序，不新增gate副本 | 不能以phase/旧prose补pass；缺实际正文或工程原始结果，仅阻塞缺失正文或工程结果的原producer |
| Publish `runtime/owner.py`、`draft.py` | 私有同操作恢复保留；无私有交易改走D635-03精确PR恢复，public key/PR事实可恢复，当前readiness仍重审 | 缺不可推导payload意图时原Publish从current scope重新审真实payload；不能读CLOSED/标题/branch猜归属 |
| Merge原manual recovery/query与Completion | 保留现行公开terminal恢复及无Delivery evidence-refresh；不把已发生merge等同整体完成 | actual PR/public Publication不匹配交Merge；真实代码不足回implementation，证据待获取留具体owner/condition |
| Closure、closure_result reader与Finish | D635-02只补不能重新推导的最小动作集；D635-01从Git验证共享Finish，不再用local seal否定它 | 未完成或不可获取归档回原Finish；确实缺原动作集/必要输入精确阻塞，不索取整套隐藏目录 |
| `task_lifecycle/resource_ledger.py`及Cleanup | common-dir local资源、repository/full remote ref共享资源、generation/expected-head保持原writer。旧代资源pending不设为新资源准入条件 | 同一确有未完责任的资源保持原冲突；unknown ownership保留，推进remote ref不删、不回退 |

以上是有实际consumer依据的修改边界，实施仍须逐行核完整caller及测试。未命中同类依赖的owner保留代码，只补必要合同/回归证据；不因全链要求重写所有package。原Task/D1、early Draft、候选适用性、final_integration先于最终Check，以及正常并行子Agent职责保持。

## 6. 状态、顺序、正常与失败流程

1. 原Identity明确同repository、TaskId/generation及可获取source ref/commit，核代码与Task/Delivery关系。活动路径恢复当前环境binding/session和实际Delivery，然后交当前原owner，不重新Intake或自动整链重跑。
2. 对归档路径，原Reactivate读取精确archive commit的Task/source/scope/summary及该版本终态关系。核bookkeeping PR/merge进入所选target、该归档结果移除active。target前进和后继active只改变当前选择，不改变精确历史。
3. 搜索当前可获取的后继incarnation。唯一可验证后继继续原后继；真实候选不唯一才询问实际选择。不证明其它clone未发布状态不存在。
4. 无后继时，当前Task2使用其正式公共reopen；指定正式旧schema1使用第5节已合并公共操作一次转换增代。matching source/build与目标capability缺失时停止该转换写入。人工历史仍走#577；未完成closeout回原事务。
5. 取得实际新key后，原Establish/Ensure/Bind建立新代环境责任，再由原Continuation进入真实新Delivery或无空Delivery的Completion验证。新代不继承旧gate；旧代seal/Cleanup仍只属于旧资源owner。
6. Publish/Merge/Closure分别核原输入和远端对象，恢复同一已经发生子动作。Open Draft/metadata未完成由原Publish补剩余工作；Ready已完成也新判readiness。MERGED进入整体Completion，不能直接推导completed。
7. 新工作满足全部scope后，依次原Completion→Closure→Finish。共享终态核验与本机seal/退出/Cleanup分别报告，后者pending不撤销前者。

不可获取ref/commit、仅原机dirty修改、不可推导必要输入、身份/归属不唯一均返回原owner的具体缺口。未合入目标的归档不能报告正式Finish。不会自动stash/reset/删除资源，不用异常分类转移原失败。

## 7. 恢复、兼容、迁移与集成

当前Task2与明确旧schema1正式归档分别解释，不因summary版本号混用公共模型。旧样本固定为`v0.7.0-guru.3@7d20a930341dae3e7dd2d214660ce3b99e28d863`的#503归档；PR505 merge `b0289465d0d83f41f1979401aff081e0c30849e0`可达当前开发基线。该样本还需完整原native续接，当前只有只读证据。

公共转换原始前驱/当前模型由上游一次收敛；后续正常执行只读current。legacy-only入口在真实旧consumer退出后的明确迁移删除，历史Git/raw继续只读。不能批量改档、自动把正式归档改为manual、退休未完成原事务或搬运原机hidden runtime。

本机local branch/worktree/ignored runtime以common-dir隔离；共享remote ref按repository identity+完整ref+expected-head核验。旧代Cleanup遇新head或新代资源必须保留并交原owner。不同Task独立恢复，不新增仓库全局current或队列。

matching分发包含canonical package/runtime、workflow、spec、声明平台overlay、dogfood和完整preset。上游能力交付后先核正式source/capability与本仓source lock采用边界，再定义配套Guru迁移。旧完整安装固定原版本；不把源码变更当安装热迁移。apply保留用户内容并逐项处理sidecar，不能为过门禁迁移无关旧档。

### 7.1 D635-05 成套兼容与在途接续

| 对象 | matching迁移及停止边界 |
| --- | --- |
| 新source与旧安装 | canonical lock已采用1e22，但目标内旧source projection、native reader和Guru packages仍不是新合同。只从同一真实Guru source执行原`guru-upgrade-tools`/`guru-upgrade-installation`，先preview实际文件/状态与sidecar；旧Task数据不因同版本CLI或`.version`被重标为已迁移 |
| Reactivate入口 | 新current input aggregate使用新schema identity并路由`delivery_reactivate_shared_archive`，旧bare-key/seal profile不被静默解释成新合同。旧完整安装保留其pinned source；matching迁移后退役旧profile执行路径、移除shared admission中的seal/manual-Cleanup依赖。原ledger/本机Cleanup依然保留，不迁移或制造旧seal |
| Publish/Closure公共I/O | 两个remote Publication profile与Closure共享恢复profile各有闭合独立schema；普通本地profiles保持旧输入语义。aggregate/interface/唯一exit consumer、workflow caller和声明平台投影成套演进，迁移说明列每个新profile及原typed exit；不靠大量optional字段兼容 |
| Task2与正式schema1 | Task2不转换格式，沿公共reopen与真实Completion规则；仅指定正式schema1通过formal operation一次收敛。raw/Git旧历史保留，人工历史继续#577，未完旧事务继续原owner。不能批量改档或退休无关未完事务 |
| 在途Publish/Merge | 原private交易仍完整时由原producer恢复原动作；private缺失而共享source/PR关系充分时走新精确PR恢复或既有manual MERGED recovery。公有phase/gate均按当前语义owner重审适用性，绝不从private迁移补造pass或新Delivery |
| 在途Closure/Finish | 新共享载体只服务原Closure/Finish。旧在途原动作输入可核时由原Closure逐案承接；缺真实动作输入具体停止，不要求找回原机目录作为产品方案。已完成旧Finish由精确历史独立证明，不要求补新载体或再次bookkeeping。归档投影已写入但未完成共享Finish时，有唯一原事务则恢复它，不能当正式Reactivate |
| 资源与回退 | tools/package迁移沿原preimage恢复；不能将新Task事实回滚成旧source而覆盖合法新工作。原local资源限定common-dir，remote ref继续用repository/full ref/expected head；old pending不撤销shared Finish，也不授权清理A或另一Task |

正式迁移说明拟由原implementation写`trellis/presets/guru-team/MIGRATION-635.md`，对应以上已选完整机制。官方模板reader更新归Trellis原工具owner；Guru installer只生成自己的packages/overlays/spec和source记录投影。full preset/reapply不能绕过既有旧数据前置，也不能靠迁移无关归档制造成功。

## 8. 验证设计

验证矩阵以本批PRD第6节AC-V1–V8为行为权威。V1需独立common-dir原native完整样本，分别证明新Delivery再次完成与仅补证再次完成；V2活动ref未入main；V3三类远端副作用与Draft/Ready分支；V4/6本机资源隔离、推进remote ref及正常双Task；V5真实缺失与未完归档；V7固定旧格式及人工/未完分类；V8完整分发、迁移、drift及至多一个代表安装样本。

原`guru-reactivate-task/tests/test_reactivate_contract.py`和`test_delivery_reactivate.py`可提供定向行为测试起点；Merge manual recovery现有路径可复用。手写completed/seal fixture、纯源码或脚本stdout均不替代V1/V7原native成功。原Check/Review亲自核全scope、完整候选与受影响未改consumer；真实最终Check、committed独立完整Review及readiness继续必需。

已知baseline bootstrap与只读drift结果不证明apply/reapply成功。完整Release多平台矩阵、tag/Release与业务现场不属于本批验证。公共能力已合并；Guru目标安装、原生E2E与安装样本仍待执行，不能宣称V1–V8通过。

## 9. Canonical 引用、本轮差额与实际未决项

命中RDT单元为`docs/{requirements,design,test}/current/task-delivery-lifecycle.md`及`completion-closure.md`；命中Architecture为ADR-024/027、ARCH-DOM-032/054与ARCH-GOV-009。原RDT/Architecture owner分别维护完整current单元，不以本稿替代shared authority。本D1的`architecture-contribution.md`和`adr-portable-lifecycle.md`说明共享终态、本机责任和正式旧格式的窄替代；实际final_integration仍在独立Architecture与candidate Check后、最终Check/commit/Review前。

当前方案已明确原transport/Reactivate、Closure/Finish、Publish及其全链consumer的精确适配。真实贡献/ADR已形成且完成候选Architecture评估；剩余规划门禁为当前Wording、Architecture final_plan和Approval。实现、目标安装和原生验证仍未执行，分别归实施及原Check。精确merge的matching构建及canonical source-lock采用已完成。旧“API不存在”停点已解除，不能继续用旧事实阻塞，也不能据此直接批准/激活D1。第5.1节source采用已完成，现由原Author收敛全部R1–R5/V1–V8方案、独立Architecture复核及原Wording→final_plan→Approval。所有验收继续未交付。
