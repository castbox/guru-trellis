# D1：Check 规划回退交接与恢复设计

## 1. 设计目标、需求承接与内容基线

本设计承接 [本批需求](prd.md) S1–S4、R1/R2、AC1–AC3及[整体需求](../../prd.md)。D1覆盖完整选定范围，无前序Delivery。固定development baseline B及Planning H0均为 `313d80215f65777fc70893a90c6d8dce8005d6dd`，来源为Intake实际选定的origin/main；PR目标为main。B是内容范围起点，H0不是最终实现HEAD，不跟随无关main推进自动改选B。

阶段适用authority为B中的 `docs/architecture/README.md`（guru-trellis-architecture）、`docs/architecture/00-foundation/design-constitution.md`（guru-trellis-design-constitution-v1）及 `docs/architecture/06-governance/change-contract.md`。独立candidate_assessment正式返回architecture_impact、target_native及decision_ref `ADR-CHECK-PLANNING-RECOVERY`。本设计只承接该prewrite结果，不宣称实现、晋升或最终Architecture已通过。

## 2. 当前系统、边界与目标差额

现有Check的 `runtime/delivery.py::_binding` 要求当前Planning结果；`planning_stale`把全部scope_decisions的ID投影为proposal_refs，只有refs为空才附reason形成revision_actions，再经原rework回planning并清四类结果。Author `delivery_approval_revision`需要具体actions且不接proposal_refs。原6.0 Check结果只记Task、HEAD、内容及语义结果，没有原scope/plan绑定；内容算法排除了Task目录。公共rework保留plan_ref/candidate/scope_ref，所以当前planning/空slots不能独立证明仍是原次回退。

本批直接演进原Check输出与router，新增原Check自己的只读恢复profile。首次回退前，把原scope/plan及必要evidence记录在同一既有Check结果中；恢复不走要求已清Planning结果的普通_binding。AI判断和业务authority保持原owner，不修改上游Delivery模型或原Author规划职责。

## 3. 来源设计处置（唯一）

| 来源与原承诺 | 处置、具体落点 | 理由、影响与上游处理 |
| --- | --- | --- |
| Issue775 R1：AI分类、动作、路线；复用原owner/exits/projection | retain；第4–6节 | 脚本只投影并校验已作出的判断；无新增语义执行器 |
| Issue775 R1：目标consumer真实接收，不预设跨包运行门禁 | retain；第5、8节 | 用生产Author schema做长期测试；运行时复用原输出schema，不每次加载Author全包 |
| Issue775 R1/R2：公共合同变化明确兼容 | retain；第7节 | 同步受控consumer并发布MIGRATION-775；旧现场只经原恢复入口转换，不保留旧路由 |
| Issue775 R2：不要求已清Planning pass、不重复回退、不补造或手改旧结果 | retain；第5–7节 | 独立恢复校验使用原事实与当前状态，不调用原rework或record_gate |
| Issue775 R2：旧已回退现场复用现有结果与因果证据 | retain；第5、7节 | 原6.0保留；缺原绑定时从实际仍持有的原公共Planning事实转换，缺真实来源明确blocked |
| Issue775 R2：不新建通用事务、跨阶段账本、授权记录或全链digest | retain；第4–5节 | 仅扩现有Check私有结果中恢复直接消费的局部绑定，无第二checkpoint |

除上述规范性约束外，Issue未指定DTO字段或具体算法；本节没有改写来源行为。PRD与implement只引用本节，不另建处置矩阵。

## 4. 模块、职责与设计取舍

| 原owner／模块 | 本批责任 |
| --- | --- |
| Check SKILL/references | AI判断scope归属与路线；定义首次回退、原恢复、纠正和缺证据路线；只恢复交接，不批准规划 |
| Check runtime/delivery.py | 拆出原身份／候选校验与planning_stale输出投影供首次和恢复复用；普通Check仍要求current Planning，恢复使用自己的已回退前置 |
| Check runtime/record.py及phase2-check.schema.json | 正常11字段语义authoring保持；首次planning_stale recorder根据显式原skill-input派生必要rollback_binding，存入原6.0结果 |
| Check runtime/invoke.py及profile schema/interface | 声明delivery_planning_stale_recovery，分派同owner恢复；完整解析、输出验证在任何阶段写入前完成 |
| workflow／Check consumer schema | reapprove_plan只投影task_ref/key/revision_actions给原Author；clarify_requirements保留真实proposal refs交原Clarify |
| 原Author package | 更新接收来源说明及命中consumer测试，保留delivery_approval_revision字段和写作职责 |
| 原工具升级owner | 从完整matching source同步受影响workflow/packages/平台投影，保留Task/session，处理sidecar并检查drift |

选择直接修改原producer与受控consumer；不放宽Author缺actions要求，不清空AI原scope_decisions。只重试原_binding会再次失败；补造Planning结果或新建身份违反R2。单靠当前phase/空slots无法区分后续scope修订；增加通用事务或第二checkpoint超过直接consumer所需。原scope/plan事实在回退后不可重推，因此只在现有Check结果保存最小恢复绑定。

新增私有binding仅服务原Check恢复，随原Check结果被后续正常record替换或由原owner退休而结束；不扩为跨Skill handoff，不将完整审核过程或授权信息放入其中。普通通过结果不增加该字段。旧现场转换复用相同6.0 schema和上游公共Planning事实，不维持另一个历史parser或双写状态机。

## 5. 接口与数据

### 5.1 首次planning_stale交接

AI继续填写原11字段authoring。scope_decisions保留全部真实判断。route为reapprove_plan时，原输出携带 `revision_actions=[reason]`，proposal_refs为空；reason须是具体可执行修复动作。scope_change_required与reapprove_plan不相容，validator只检查AI结果的该显式一致性，不能替AI改路线。route为clarify_requirements时，仅真实scope变化决策提供非空proposal_refs，不能制造scope proposal以满足schema。

现有planning_stale输出/consumer schema直接演进为上述两种闭合分支；保留exit id和route值。router对Author只复制task_ref、delivery_key、revision_actions并加固定profile/mode，绝不把proposal_refs交给Author。真实变化仍进原Clarify。完整输出验证成功后才执行一次既有rework。匹配采用及旧结果说明见第7节，不保留当前已不可执行的旧非空refs→Author路径。

### 5.2 原结果中的最小恢复绑定

首次planning_stale记录时，通过原 `record-phase2-check.sh --skill-input <原公开Check输入>`读取真实当前Delivery/Planning，派生 `rollback_binding`：

- delivery_key、原Planning result_id：绑定原调用，不能只凭Task目录推选Delivery；
- scope_ref、plan_ref：恢复时区分原范围/计划与合法后续修订；
- candidate：绑定原候选的HEAD、内容、paths及B；
- planning_evidence：原Planning result的三份规划AuthorityRef，恢复核PRD/design/implement原字节；不能只用排除了Task目录的Check内容摘要。

该结构只进入原Check私有6.0结果，不进入planning_stale公开输出。recorder从原公共事实派生，AI不手填摘要或复制当前事实冒充原事实。schema6.0允许保留的旧无binding结果；新的首次planning_stale invoke要求具备与原public input相符的binding，缺失时在rework前回原recorder重新记录。普通成功Check、原11字段语义authoring和其他profiles不增加该义务。

### 5.3 有界恢复与纠正入口

新增 `delivery_planning_stale_recovery` public input携带mode、task_ref、delivery_key及 `original_check_input`（实际原公开Check输入）。同owner的private owner_result携带 `original_result`（原完整6.0），需要纠正时另带 `corrected_result`（真实当前判断后生成的完整6.0）；旧无binding现场携带 `original_delivery`（已有原公共query的key和delivery，其中保留原Planning result及candidate）。这些是原owner内部输入，不交后继consumer。

使用新的私有恢复schema分别验证原结果、可选纠正结果与旧来源。原结果必须是planning_stale并匹配原Task/mode/HEAD和调用key；不接受passed作为恢复来源。优先消费原结果的rollback_binding。旧结果缺binding时，original_delivery必须来自仍持有的原公共query，或由原公共parser读取精确Git Task对象后选取同key；不能手工以当前值拼接。其原Planning result_id须等于original_check_input的planning_accepted_result_id。由同owner提取原scope_ref、plan_ref、三规划evidence及candidate；原candidate还须与原Check的内容/路径观察相符。只有原Planning结果而没有可定位原candidate的事实时，来源不完整，返回具体缺口。没有这些实际来源时不得从当前值补齐。

恢复对比同Task/generation/key与C4、当前scope_ref/accepted_scope、plan_ref及三规划evidence、candidate和原Check HEAD/内容/paths。要求当前phase=planning、planning/check/full_review/readiness已清。当前公共选择必须匹配；无context仅走原明确key校验。任何真实变化保留原错误类别和具体字段，返回受影响Planning/Clarify/身份owner重新判断。

纠正沿同owner新schema和原recorder dry-run能力形成新结果，不覆盖旧6.0。更正后的结果必须仍是本次planning_stale，同样绑定当前事实；AI重新决定scope分类、动作与路线。恢复与纠正都只验证并投影5.1的公开交接，不调用rework、record_gate或覆盖candidate。缺原来源返回既有blocked并说明缺什么以及原owner处理入口；不能把它称为恢复完成。

## 6. 状态、顺序、正常与失败流程

1. 普通Check在checking状态完成当前语义判断及原recorder/checker；planning_stale记录原绑定。
2. 首次invoke核current Planning和候选、真实语义一致性及完整输出；只有成功后调用一次原rework到planning并清四结果槽。
3. 输出丢失或旧handoff需要纠正时，原Check读取原input/result及当前公共对象。已清Planning不再是普通Check入口的可用前置，因此恢复明确分派到新profile。
4. 恢复一致时返回可消费planning_stale；同一结果重试不写阶段。Author/Clarify随后各自执行本阶段，恢复结果不代替其批准。
5. 若phase已离开planning、结果槽出现新阶段结果、scope/plan/candidate或原内容变化，停止复用原判断并返回受影响原owner。普通身份失配、缺证据和真实stale不改成pass。

不处理恶意伪造、并发压力、额外锁/原子写或故障注入。字段校验服务普通错误与过期检测，不构成真实性认证系统。

## 7. 恢复、兼容、迁移与集成

### 7.1 修复前现场的 provider 与目标采用顺序

旧现场先保留原业务 checkout 的候选、HEAD、规划字节、原 Check 6.0、原公开 input 及实际原公共来源。选择位于目标 checkout 之外的完整 matching Guru provider，由该 provider 提供当前 workflow/router、Check package、consumer 合同与 managed runtime；不复制单个 package，也不以目标旧 dispatcher 代替新 provider。目标继续提供其已安装且兼容的 Task schema2 / Delivery API1.0、C4 和真实当前选择。provider 的脚本与 runtime 负责执行，目标公共 API 仍拥有 Task/Delivery 身份和状态，没有第二 authority。

原 owner 从完整 provider 的公开 Check wrapper 调用既有 `--root <目标checkout>`，使用本设计第5.3节恢复输入和真实原事实。launcher 在 provider 根选择完整 runtime，Check 的 --root 明确目标；invoke 命令元数据和 help 必须声明这个既有参数及目标公共 API 前置。目标无兼容公共 API、身份/选择不符或原来源缺失时，按原诊断停止，不加载 provider 内私有 Task 实现作 fallback。

必须先恢复旧交接，再由原 Author/Clarify 消费实际输出进入当前重规划；在不再复用旧结果后，才由原 tools owner 按单独审查的写集成套采用目标工具。恢复本身不向目标安装或更新工具。后续 implementation 从真实 after 构造新候选并重新 Check。先原地升级已跟踪工具会改变原结果覆盖的内容与 candidate；这种现场只能由受影响原 owner 判断真实变化，不能补旧 token 或放宽内容校验来继续旧恢复。

此采用方式复用现有 wrapper/--root 和目标公共 API，不新增远程执行服务、备用 runtime、身份环境覆盖、恢复状态或账本。原结果字段、R1/R2和交接语义不变；新增代价是原 owner 明确选择完整 provider 与目标，并核兼容前置及采用顺序。

### 7.2 成套采用及状态边界

采用原合同直接演进及受控consumer同步。MIGRATION-775写明matching Check package、workflow/router、consumer schema和Author说明必须成套采用。旧完整安装保持原发行，沿原工具owner切换；不对旧6.0文件手改字段或digest，不新增长期历史parser。

修复前已回退现场：原Check读取完整旧6.0、原public input及已有原Planning因果来源，经新恢复入口作当前判断并转换交接。原Planning结果只作为保留的历史事实，不要求当前已清结果槽恢复pass，也不调用旧Activation私有checkpoint。缺来源时明确blocked；原Planning/Clarify在当前真实范围重新判断，不制造恢复证据。

新入口不改Task/Delivery身份、上游状态协议或业务数据，不做数据库迁移。现有结果中增加的恢复字段由原Check独占消费；后继原Author只接最小actions。工具投影使用guru-upgrade-tools的单checkout合同，完整源、精确写集与安装副作用另行展示；不手工覆盖受管副本。后续Check/commit/PR及最终整合仍按原workflow。

## 8. 验证设计

| 验证 | 要求、层级、入口与输入 | 独立观察与边界 |
| --- | --- | --- |
| V1 | R1/AC1；原test_candidate_check fixture，经真实recorder/checker/invoke生成current_scope+reapprove_plan | 输出actions保留原具体reason；正式router字段投影通过Author真实schema；只验producer schema不算通过 |
| V2 | R2/AC2；同fixture的真实首次planning_stale，随后在Planning已清状态调用恢复；同组补真实纠正及旧无binding转换，明确由目标外完整provider wrapper的--root指向未变目标 | key/phase/candidate、目标工具与业务字节保持；无第二rework或Planning/Check pass；旧转换只消费真实原来源，原6.0字节保持；目标工具真实改变时旧恢复拒绝，不将局部fixture称为升级全链证明 |
| V3 | R1/R2/AC3；采用已有no-scope、真实scope变化、成功Check回归并补命中差额 | Author与Clarify唯一consumer可接收；真实合法后续scope/计划/内容变化不能恢复原判断；不新增攻击或无独立价值重复场景 |
| V4 | AC3；source package/公开example与consumer校验、受管dogfood/声明平台、reapply/drift/sidecar定向验证 | matching投影一致、Task/session保留；不证明业务现场、完整native或Release矩阵 |

先实现或扩展同一行为fixture，再实现命中的生产合同；无需重复Task创建或要求统一红绿/rollback序列。V1/V2是长期回归，必要临时诊断在因果问题解决后停止。命令与实际执行顺序由implement第3节列出。已有适用覆盖可采用；新事实、失败或真实影响才追加验证。

## 9. Canonical 引用、本轮差额与实际未决项

本批沿本PRD第7节命中R713、D713、T713及Architecture分发完整单元，修订其中旧非空refs路径和原恢复说明。原Author维护本Task隔离Architecture contribution及 `ADR-CHECK-PLANNING-RECOVERY` 候选；原RDT owner维护隔离R/D/T完整拟写。完整candidate Check后，原维护owners在final_integration重读实际目标、整合并读回；implementation重绑全部after，再执行最终Architecture/Check/commit/独立Review。

没有新增需求选择。计划中的字段、原公共事实读取和异常字段位置需在实现中按现有parser/错误合同落地；如果无法取得所选旧来源或合法普通场景被拒绝，停在原Check/Author/Architecture补真实证据或修订，不能扩大到任意planning放行。共享authority尚未晋升，未来验证结果尚未发生。
