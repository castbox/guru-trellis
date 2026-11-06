# D1：公开执行合同与真实入口闭合设计

## 1. 设计目标、需求承接与内容基线

本设计承接 [本批 PRD](prd.md) S1–S5、AC1–AC4、缩减后的 AC6–AC8 与 AC9；AC5 取消。D1 是完整切片，没有前序 Delivery。目标是让业务 Agent 从正式安装的正常入口找到合同、作者自己的判断、调用原执行器并消费原结果。补 schema、错误信息或测试入口只是必要组成，不能单独完成本项。

development baseline B 与 Planning H0 均为 `8378b8d500a974ae1c01bd0571f30149f56541b0`，来源是 Intake 已核实的可获取本地 main/origin/main，含 #710 的 #715/#716。内容范围固定从 B 到实际实施 HEAD；PR integration target 是 main，二者独立。后续 candidate 优先恢复同 Delivery 的 B；后续 Delivery 使用原算法选实际前序 delivered head。本批不 fetch、整合新 target 或把 H0 当最终实施 HEAD。

采用 `guru-trellis-architecture`、`guru-trellis-design-constitution-v1` 与 `guru-trellis-architecture-change-contract-v1`。本轮独立 Architecture 的实际 candidate_assessment 返回 baseline_current / architecture_impact / target_native，decision_refs 为 ARCH-FND-002、ARCH-FND-004、ADR-028。整个 D1 仍包含公开生产入口与 consumer 收敛，不能把验收删减当作全批无架构影响；本轮不新增生产机制。最终方案仍须经过 Wording 和原 Architecture final_plan。

## 2. 当前系统、边界与目标差额

| 当前能力及实际定位 | 本批目标差额 |
| --- | --- |
| `contracts/task-lifecycle/task-creation-input.schema.json` 已定义封闭 issue/no_issue；`guru-create-task` 的 public creation 只写普通 object | public creation 引用已有 source/target 定义，正文与两个正常输入例一同指明字段及关系 |
| Completion Interface 指当前 delivery invocation；commands 的 semantic binding 仍指旧 schema | 按当前 profile 给一致导航，明确历史资产适用入口，保留真实旧 consumer |
| `.trellis/scripts/delivery.py candidate --paths …` 只返回 content_ref；begin-check/rework 可接完整 operation | 公开原投影的固定 B 和完整 Candidate 构造；阶段写入继续走现有 CLI |
| `runtime/command.py`、`runtime/schema.py` 和已定位 errors 指向 Inspect runtime 或笼统 linkage | 原错误 owner 输出可确定的字段、合同及原恢复入口；内部故障保留失败，不假定根因 |
| eval 有 schema 选择、精确提示及 candidate 计算；旧 continuous chain 预置 Task/D1 且止于 Completion | 逐职责移除生产补偿，复用原公开能力与现有定向结果；不再新增完整 native 链 |

长期源仍在 `trellis/skills/guru-team/`、`trellis/workflows/guru-team/`、`trellis/presets/guru-team/`。dogfood 和平台入口是受管投影。业务 #994、#711 的知识布局、#712 新 legacy 家族、完整 release 矩阵均不进入本设计。现有 Reactivate/维护家族仍在支持集合内。

## 3. 来源设计处置（唯一）

下表只拥有本批规范性承诺的处置。生产行为与兼容条款 retain；S4 验收按修订后的源 Issue change。源 Issue 已同步，根范围已接受，D1 已合法 scope revision；本设计承接当前切片。

| 来源 locator / 条款 | 原承诺 | 处置与具体落点 | 理由、影响及上游处置 |
| --- | --- | --- | --- |
| #713「公开合同与范围口径」及 S1 导航 | 固定可获取 B；按调用语义覆盖，当前/旧、多 profile 各有合同 | retain；本节1、4、5；implement 第3节43包清单与family表 | 固定声明集合，不追逐无关新需求；交付时纳入本项声明差额 |
| #713 S1 输入域 | 公开当前成功域，优先已有权威定义，issue/no_issue 正向例 | retain；第4节 R1 与第5节来源输入 | 引用共享定义，保留 task_ref 日期约束，不用新增拒绝代替正向执行 |
| #713 S1 AI/producer/recorder | 作者语义、实际公共身份与确定性字段分清 | retain；第5节字段责任与receipt | 不以完整结果作authoring；#710当前语义不变 |
| #713 S1 兼容 | 保留真实已发布成功调用，语义变化须显式迁移 | retain；第7节逐consumer | 不新增长期兼容层；现存支持资产不因历史名称被删除 |
| #713 S2 原执行入口 | 先核既有 CLI；真实缺额才补原 owner 最小能力 | retain；第4/5节construct入口 | 已核实candidate输出缺额；复用content_base/candidate，不改upstream或写第二算法 |
| #713 S2 workflow边界 | workflow只拥有全局顺序/mandatory invocation/exit | retain；第4/6节 | 局部装配说明回Author/implementation owner；不造wrapper Skill |
| #713 S3 错误/恢复 | 字段/合同/stale/内部故障区分，保留原失败 | retain；第5/6/7节 | 输入修复回原合同；真实故障交维护，不要求业务Agent修runtime |
| #713 S3 输出纪律 | 完整exit/stdout/stderr；receipt.result/checker/typed exit不同 | retain；第5节输出和第8节V3/N2 | 运输成功不冒充语义通过；截断显示不用于重建 |
| #713 S4 R5 | 逐项对照生产职责，环境与观测可保留 | retain；第4节R5三项表 | 必需知识/计算归原owner；不因import存在机械删fixture |
| #713 修订 S4 三族 | 取消新的完整首次链及独立恢复 native；保留历史结果 | change；第8节 | 取消不等于通过，正确性和正式质量链保持 |
| #713 修订 S4 声明族 | 保留声明/导航/consumer 核对；取消追加非等价 native | change；第8节与 implement 第3节 | 现有证据按层级使用，未验证模型行为不标通过 |
| #713 S5 | canonical/dogfood/platform/实际安装匹配，定向reapply/drift/sidecar/mode | retain；第7/8节I1 | 原installer/tools owner；至多一个必要clean，不扩Release矩阵 |
| MIGRATION-710「当前调用者」「恢复」 | 11字段recorder authoring；完整6.0 checker/invoke/recovery，两个token不同 | retain；第5/7节 | 沿原Check使用，不增加full-result recorder reader，不回填私有字段 |
| AGENTS §2–§4、§9–§10 | Markdown判断、脚本事实、唯一owner、最小状态及副作用边界 | retain；第4–7节 | 无新判断脚本、授权持久化或长期台账；当前仅写规划 |
| 官方custom workflow / marketplace文档及Architecture change-contract | 官方扩展面、隔离贡献、候选Check后原owner晋升、最终质量链 | retain；第7/9节 | 不改上游/global/node_modules；共享current不在Planning写入 |

## 4. 模块、职责与设计取舍

R1 由 `guru-create-task` 原合同 owner 修改 `schemas/public-delivery-task-creation-input.schema.json`，引用 `contracts/task-lifecycle/task-creation-input.schema.json` 的实际 source/target 定义。同步 Skill、Interface、commands 的输入binding及正常 examples。保留 public 局部 task_ref 约束和原 executor；不另写source领域定义。验证通过原create入口，区分合法Issue/no_issue和普通relation误填。

R2 由每个受影响原Skill owner维护其profile导航。首要定位 `guru-review-task-completion/{SKILL.md,interface.json,commands.json,references/contract.md,examples/,schemas/}`。命令help通过已有command dispatcher展示当前输入、semantic authoring及输出合同；多profile按实际 discriminator/entry条件选择。不新增全包总input或万能manifest。原共享 `runtime/command.py` 只分发声明信息，不能猜语义profile。相同缺口在固定清单中实证复现后归该包修复。

R3 在原 `runtime/delivery_projection/` 增加小型只读 CLI module `candidate_cli.py`，经 `trellis/workflows/guru-team/scripts/bash/construct-delivery-candidate.sh` 稳定安装入口暴露。它复用原 `DeliveryProjection.content_base/candidate`，不复制Git范围、排除路径或内容摘要算法。preset原managed asset/runtime inventory声明新文件和mode。保留 upstream `.trellis/scripts/delivery.py`；begin-check/rework/apply继续执行原operation。全局workflow不再教业务Agent导入Python；Author的固定范围合同和implementation原step提供完整调用顺序。此命令有独立的事实构造职责与现有Candidate consumer，不是新workflow或Skill。

R4 原 `runtime/command.py`、`runtime/schema.py` 及受影响包error catalog补具体诊断。schema组合错误保留实际field path与可判定约束；不确定时只报已知范围。正常stale给原producer/re-entry入口，内部错误保留原异常范围和非零状态并交维护。现有error shape/code保持；如有真实对外shape变更，先走第7节迁移而非顺带实现。

| R5辅助与当前职责 | 与生产对照及目标处置 | 保留和验证 |
| --- | --- | --- |
| `stage_result_authoring.owner_schema/public_reads` 硬选semantic schema | 正常Agent应从Skill/Interface/command读当前profile合同；补齐生产导航后，native路径不再由adapter预选并注入正确schema。纯schema测试可继续选定被测合同 | read allowlist/观测可留；保留原 native trace 的实际证据边界，不追加方法加载补证 |
| `native_adapter.py` 精确合同路径、参数与阶段操作提示 | 测试环境只给业务目标、正常入口及环境事实；当前生产必须知道的调用说明由原Skill负责。删除其额外authoring/正确答案提示，不把旧详细prompt当正常入口证明 | 环境准备、provider、路径映射、run运输和原输出观测保留；前后prompt差额人工审核 |
| `implementation_authoring.observe_candidate` 私有构造B/H/paths/content identities | 生产与 eval 调用公开 construct 入口和已有公共 facts/recorders；adapter转发实际公共输出。不能自己重建Candidate或Phase2私有token。host独立观测可以保留但不能作为模型缺失输入的补给 | 对比原命令回执与实际模型输入；单元完整合法fixture继续证明consumer边界 |

## 5. 接口与数据

来源输入保持原闭合union：issue `{kind:"issue",repo_ref,number,disposition:"exact_source"|"reference_only"}`；无Issue为 `{kind:"no_issue"}`。creation目标沿已有 `{repo_ref,branch_ref}` 及原条件。不存在relation别名，不新建第二source或自动把普通错误解释为已接受source。

新桥接仅服务当前声明的 Git `pull_request` Delivery，前置是原Identity/Ensure核实的Git checkout、C4绑定和当前Delivery。计划调用为：`bash .trellis/guru-team/scripts/bash/construct-delivery-candidate.sh --root . --task <TaskRef> --delivery-key <JSON> --development-base <B> --head <HEAD> --paths <repo-relative paths...>`。`--observed-target <OID>` 是无显式development-base时的原算法输入，二者选择条件写入help；均不fetch。Task/Delivery来自实际Identity/Ensure/Selection，不能由目录名猜。上游既有 `delivery.py candidate --kind git_free` 保持其原Candidate内容引用和合法consumer边界；新桥接不接收git_free/null refs，也不新增无Git Task/Delivery能力。

stdout仅为现有 Candidate `{kind,content_ref,paths,head_ref,base_ref}`，无新DTO/schema或持久文件。B按同Deliverycandidate→可比较前序delivered head→显式B/唯一merge-base原顺序；HEAD解析为完整OID；paths由AI选定，执行器按原算法补齐完整committed范围。缺commit、历史不完整、身份/阶段冲突保留具体拒绝。该输出直接供原begin-check operation及当前Check/commit owner输入，绝不承载semantic pass。

业务Agent将完整Candidate和原公开declaration的implementation owner放入已有operation：`api_version=1.0, operation=begin_check, key, owner_role=implementation, owner_id, expected_phase=implementing, candidate`，交 `python3 .trellis/scripts/delivery.py begin-check --task <TaskRef> --input <regular UTF-8 JSON file>`。该CLI不支持stdin `-`，不写成通用载体。rework同样沿原operation和owner，不由新命令选择返工目标或失效结果。声明中的其他命令各按其实际inline/file/stdin能力公开。

字段分工：AI写需求、scope/finding、证据充分性及route；原producer返回的key、public token、scope_ref、receipt路径原样传递；recorder计算其私有Task/HEAD/摘要。Phase2只写11字段语义authoring，不能拿public Candidate token冒充Phase2私有内容token。公开author_identity这类必要事实若仍只能从源码推导，须在其原公开owner补足事实生成或已约定计算说明，不让业务Agent复制私有算法。

每次调用先完整捕获原exit/stdout/stderr，再解析：dispatcher receipt取其`result`；recorder的artifact_path交checker及原invoke；checker receipt只证明机器检查；只有成功的正式invoke输出唯一typed exit才按其consumer继续。非零退出、无效/多输出、缺失字段停止消费。输出展示可截断，解析不得依靠截断显示。无新增审计对象或全链日志写入协议。

## 6. 状态、顺序、正常与失败流程

1. 正常平台入口加载workflow与mandatory Skill；Skill按当前profile完成必要正文读取，从公开资料装配输入。preTask仍side-effect-free。
2. 原Task/Delivery创建、scope、Planning owners完成当前语义步骤；需副作用或真实选择时保留当前对话边界。没有跳过Architecture/Approval的测试捷径。
3. implementation选择B/paths，公开construct生成Candidate；原begin-check进入checking。原Check候选检查后依法rework回implementing；RDT/Architecture原owner最终整合，重新构造候选并执行最终Check。
4. 原commit→完整committed Review→readiness→publication/delivery→Completion→Closure→Finish依次消费真实结果；Delivery delivered不等于Task完成。清理仅经原明确目标确认。
5. 普通输入错误回同profile合同更正；原错误及新调用分别保留。真实内容编辑使适用旧结果stale；由最早受影响原owner重新判断，不能刷新旧摘要续命。输出丢失优先恢复原producer结果，缺必要前提则重入原owner。
6. 真实内部故障准确停止该路径并交维护；其余不依赖工作可继续。已有 native 若需要源码诊断或额外提示，保留该案例不满足正常入口验收的结论；本批不再追加重跑。

## 7. 恢复、兼容、迁移与集成

保持以下真实consumer：原Delivery CLI的content_ref读取者；各包声明的当前/旧profile consumers；#710的完整6.0 checker/invoke/recovery；既有legacy control inspection/retirement及Reactivate/maintenance入口。新增construct是缺失能力的独立事实入口，不改变现有candidate stdout。当前入口改导航，历史示例仍按其声明consumer使用。若盘点证实某deprecated资产只剩测试或历史引用，原owner在同批直接退出该路径及注册/说明；不能用文本零匹配认定无外部consumer。

本设计不增加relation alias、双recorder输入、fallback parser或新兼容状态。固定旧完整安装保持旧合同；采用本项需完整matching package/runtime/workflow/preset/platform切换。成功语义若确需变化，先形成精确迁移合同并回原Planning/兼容边界；当前设计没有此类变化，不能据此预先造长期兼容层。

本仓已有Task/session，dogfood更新必须走原 `guru-upgrade-tools` 完整source合同；不以普通apply绕过历史Task阻塞，不手拷受管文件。代表性隔离安装可按满足current-only条件的原apply/reapply；逐个处置`.new/.bak`、用户修改和mode。runtime inventory及managed asset包含新桥接；更新前后当前Task/D1身份仍一致。至多一个必要clean并与实际候选来源绑定。

结果恢复依原creation、selection、record/check/invoke或publication shared recovery入口；不重建另一owner私有结果。新只读construct不保存恢复checkpoint；相同事实重读原Candidate，真实变化让旧证据按原规则失效。无业务数据迁移、新Task字段或授权持久化。

## 8. 验证设计

采用原公开合同、源实现、原生产命令、定向组件/consumer 和匹配安装结果。V1 输入/导航、V2 Candidate/阶段/stale/恢复、V3 错误与 receipt/typed exit、V4 eval 职责及 I1 分发的范围保持；只刷新本轮真实变更所影响的结果。
固定 43/127/180 声明及 F1–F13 对应保持。已有局部 native、synthetic 和结构/命令结果分别报告。取消项、失败和缺失方法证据不变成 pass。

| 取消项 | 范围 | 结果口径 |
| --- | --- | --- |
| C1 / AC5 | 新的 preTask→Finish 首次正确完整 native 链 | 取消本批验收；已有首装配失败与后续生命周期事实保留，不记全链通过。 |
| C2 / AC6 | 新的独立 N3 public-only 变化/结果恢复链及旧 fixture 接续 | 取消追加 native 和历史状态恢复；已有普通错误、stale、同结果恢复按实际层级采用。 |
| C3 / AC7 | F10、其余非等价 family/profile/caller/goal 的追加 native 代表 | 取消追加模型验收；保留 43/127/180 声明、导航与 consumer 映射和已有定向结果，未验证行为明确列出。 |
| C4 / AC8 | R5 完整方法加载、Planning→同 fixture Activation/resume、Drift 的模型方法补证 | 取消补证及重跑；保留职责对照、生产入口、alias/consumer 模块结果，以及 execution_error、fitness_regression 和方法证据不足。 |
| C5 / AC9 | 为补上述 native 而重复准备环境、恢复损坏 clean 或再次安装 | 取消重复准备与安装；复用完整且仍匹配的安装/投影、reapply/drift/sidecar/mode 实绩。 |

本批不再要求新的完整 Agent 生命周期、独立 N3 或额外 family native。原 runner、合法 fixture 和历史结果保留；不做旧 fixture 接续或为补证重复安装。当前正式质量链仍按第6/9节完成。

## 9. Canonical 引用、本轮差额与实际未决项

需求/设计/测试当前authority为 `docs/{requirements,design,test}/current/{task-delivery-lifecycle,completion-closure,knowledge-maintenance}.md`；本批差额是公共调用、生产操作和证据边界，不迁移其布局。共享工程合同为 `workflow-contract.md` 的consumer连续性/固定B、`skill-package-contract.md` 的公共I/O、`quality-guidelines.md` 的验证价值/范围、`companion-scripts.md` 的receipt；均通过原RDT/Architecture writer承接完整单元。

真实隔离贡献见 [architecture-contribution.md](architecture-contribution.md)，由Author写实际差额与九concerns，独立Architecture在final_plan审核；无新架构决策，当前不需要新ADR。若实际方案改变owner/GAP/兼容退出或原则例外，回原Architecture重评。共享晋升只能在完整实施/隔离拟写经候选Check后由原owners final_integration/readback执行，再做最终候选/Check/commit/完整Review。

技术机制已能据此实施，没有待用户补充的产品选择。保留范围的结果适用性仍须当前原 owner 判断；取消或未验证 native 不以静态结果替代。明确不承担的完整矩阵、正式source-lock、部署及业务采用保留边界。
