# D1：当前共享差额判断的诊断设计

## 1. 设计目标、需求承接与内容基线

本设计承接本批 PRD D1-R1–D1-R7、D1-S1–D1-S5、D1-AC1–D1-AC4，整体责任为根 PRD R1–R8、AC1–AC4。目标是取得原判断入口的当前消费和行为依据，再决定最小处理；不以新增方法作为预定交付答案。

development baseline B 显式选定为 `a72981db56d2070d8140b468cab3a97ae82effd3`，来源是本 Task 经 Sync/read 和创建采用的固定 git_object。Planning H0 也是该提交；两者角色不同，后续实现头 H 将变化。PR 目标为 `castbox/guru-trellis:main`，不以远端较新 SHA 自动改变 B。实现产生真实 business paths 后，原 constructor 用此 B 构造完整候选；不得把 Task 文档或内部状态当业务 paths，也不得遗漏 B..H 已提交差额。

阶段适用 authority：`docs/architecture/README.md`（`guru-trellis-architecture`），`docs/architecture/00-foundation/design-constitution.md`（`guru-trellis-design-constitution-v1`），`docs/architecture/06-governance/change-contract.md`（`guru-trellis-architecture-change-contract-v1`）。独立 reviewer 已针对真实 call-local 候选执行 candidate_assessment，正式返回 `baseline_current / no_architecture_impact`；设计事实 freshness 为 `sha256:7a74acd7f24bca9ee725b01bc540ebe5b168693d10e8dfa275d9225f3bd49873`。该结果不替代本设计的 Wording、final_plan、Approval，也不批准尚未选定的修复。

## 2. 当前系统、边界与目标差额

原实际实施判断职责从 `.trellis/workflow.md` §2.1 进入；其 caller 读取当前选中 Task／Delivery、规划、共享 Author 正文／模板、质量与必要 spec，再消费被派工 worker 的真实工程事实。共享消费者方法在 canonical `workflow-contract.md` 的 Candidate Applicability And Coverage；原 Reconcile 只处理真实整合需要。`.codex/agents/trellis-implement.toml` 和 `.trellis/agents/implement.md` 是上游实现角色，不是本 Task 任意改写方法的落点。

现有 `trellis/skills/guru-team/packages/guru-qualify-root-cause/tests/run_behavior_validation.py` 已有 `provider`、`author_fixture`、`run_case(kind=dispatch)`：复制完整当前 Guru provider，使用真实 upstream Task/Delivery fixture，建立前置事实，再通过 `codex exec --ephemeral --json` 启动实际 Phase2 判断。现有代码只采退出码、工具/输出和文件，不生成语义通过。

本批先复用这些能力，在同一 test-only collector 增加共享差额及普通承接材料，事实资产放该包 `tests/fixtures/shared_dependency/`。不增加第二生产 runner、公共命令或 runtime 状态。工作区为仓库外临时项目；本 Task 根／D1 正文、Issue #853、host 预期和 evaluator 源码不进入被测工作区。被测 provider 的原方法全文按正常入口可见，不在测试 prompt 复制或强调正确答案。

首批 source 写入范围限 collector 及其事实 fixture，另由原 owner 写本 D1 的最小 validation 结果。未选择任何规范性入口／方法修复。若运行证据支持消费或具体方法缺口，先回原资格、Author 与受影响 Architecture／Approval 形成精确修复规划，再编辑对应规范正文；不能借当前诊断计划直接添加规则。

## 3. 来源设计处置（唯一）

S1 的技术约束属于已接受合同，尚未给定规范性实现机制。以下保留其完整行为承诺；本批 collector 装配是技术候选，不是来源预定答案。

| 来源与承诺 | 处置 | 本设计落点、理由及影响 |
| --- | --- | --- |
| #853 当前能力／最小落点：先查实际入口、加载与使用，再判断消费／方法缺口或无需修复 | retain | §2、4、6 的原入口追踪及证据分支；不从历史或正文存在先选修复 |
| #853 行为§1：仅已知实质影响或具体结论缺事实触发，适用结论直接复用 | retain | §4、8 的 material／ordinary 输入与有界补证；不新增 start/commit/review 默认调查 |
| #853 行为§2：已交付、在途、冻结实验分开，草稿非基线，不建快照／账本 | retain | §4、5 的实际文件与观察来源；外置日志只用于本次直接评估，不构成跨任务状态 |
| #853 行为§3：从实现、增量、签名/调用、生成链及验证形成具体必要依赖 | retain | §4 的可读产品文件与 host 独立判定；不把路径冲突或 Issue 状态当依赖判据 |
| #853 行为§4：原 Reconcile 固定对象，保留身份，不自动同步草稿或接管另一任务 | retain | §6、7；本次观察只读，不在 fixture 外执行 merge 或协作指令 |
| #853 行为§5及验收§2：中性材料经原入口，不追加完整方法/答案/非日常加载 | retain | §4、5、8 的隔离装配与 prompt 检查；脚本只运输事实，原审核 owner 判断 |
| #853 验收§4：真实修订才分发，无 API 改变不新增 DTO/exit，不扩 Release 矩阵 | retain | §7–9 与 implement §6；无规范性修订不制造受管或共享知识写入 |

本批无 change/reject 来源承诺，无新增兼容例外或已选 ADR；若后续机制改变上述承诺，先回原 owner，不静默修改本表。

## 4. 模块、职责与设计取舍

| 模块／owner | 输入、行为、输出与边界 |
| --- | --- |
| 原实施协调 owner | 从生产 Phase2 入口及其必要引用追踪当前加载职责，核对现有可采用行为证据。没有充分当前证据才实施下述观察；不将链接存在当实际消费 |
| 既有 test-only collector | 在 `run_behavior_validation.py` 增加 `shared-material`、`shared-ordinary` 事实类型，复用 provider／upstream fixture／dispatch／采集逻辑；只在外置临时项目建立事实，不生成判断或预写模型答复 |
| `tests/fixtures/shared_dependency/` | 提供去敏缓存实现、真实调用文件、生成链身份、冻结实验入口及有来源的观察记录。它是中性工作输入，不携带 #853 方法、AC、预期结论或 hidden oracle |
| 原 Phase2 入口中的真实 Agent | 读取正常 provider、Task／Delivery 前置和本轮工作材料，自己选择必要读取、比较、验证与后续动作。只读评估，不记录 formal Check、不改产品／Task、不建远端资源 |
| 外置 host 评估 owner | 在被测工作区之外持有本设计§8及来源期望。阅读实际 prompt、完整工具事件、读取正文、最终答复，判断入口、方法消费和结论。进程成功、关键词或固定 true 不产生 semantic pass |
| 原修复／安装／知识 owners | 只在当前证据定位真实缺口并形成受审修复候选后承接规范性修改、工具同步和知识整合，不由 collector 决定 |

选择复用现有 collector，比增加另一套启动、状态或结果解析路径更薄。只做静态引用／字符串扫描无法回答“是否通过日常入口加载并使用”；把完整方法放进 prompt 会改变待测条件。重放原业务树、云端或 SDK 生产实验不能回答本仓当前 Agent 方法问题，且不在范围内。

### 中性材料的具体组成

`shared-material` 选择一个去敏共享缓存场景：当前可执行树有一个标量缓存核心及其既有 caller；另一侧工作材料包含同一模块的在途缓存适配、新消费者与 SDK/生成物差额。目录明确区分当前已提交树、观察到的在途草稿和冻结实验。新增调用文件与 helper 的签名存在跨文件静态差异；不预跑该组合然后虚构编译失败。两侧增量通过真实 import／调用关系可核对，不能只给作者声称“复用同一实现”的摘要。

去敏观察记录分别标注对象与原范围：dirty 快照的文本预演有七处冲突；固定已提交 dev 的实际整合仅有两个文档冲突，且不含在途 SDK／生产调用增量。这些作为来源提供的 fixture 观察，不冒充 collector 本轮执行的真实业务 merge。冻结实验使用旧依赖和固定入口；host 在 fixture 中执行能执行的本地纯行为并保留真实结果，未执行的外部／新组合结果如实缺失。材料只列事实和所需业务行为，不写“应当如何推导”。

`shared-ordinary` 保持相同共享调用和当前消费者，没有行为影响的版本标识变化；提供同入口、依赖、环境及期望仍适用的本地观察。当前分派是继续已接受工作并判断下一步；不提示“请不要盘点”或“直接采用旧结果”。该材料观察无实质共享差额时的原路径，以及已有事实的适用性承接，不新增日常义务。

两组材料各有独立检出作用；这里选定工作输入，不把样本数或固定轮次数量变成验收条件。具体文件和真实记录在实现时检查互相一致；fixture 装配错误先修事实，不拿设施失败当目标判断失败。

## 5. 接口与数据

不改公共 Skill id、profile、DTO、schema、typed exit、公共 Task/Delivery API 或业务仓库接口。使用现有 collector CLI `--source`、`--output`、`--case`、`--jobs`；只增加 test-only case 值，不加入公共 registry。`provider` 从当前 canonical packages/runtime/consumers/contracts/spec/workflow 装配完整可用来源，tests/evals/host expectations 不复制进被测工作区。

真实 upstream 依赖选用当前安装声明的 `castbox/Trellis@e3793251fad8bd261d0c370d408c7675b9f6a140` 的 `packages/cli/src/templates/trellis/scripts`，经 `GURU_UPSTREAM_DELIVERY_SCRIPTS` 提供给原 fixture。已核本机匹配源码干净且含所需 `common/delivery_store.py`；执行前仍核版本／目录与 actual setup 结果，不使用较旧全局 CLI 或伪造 model 代替。此依赖选择不授权改 upstream 或全局包。

中性 fixture Task／Delivery／Planning acceptance 是产品判断前已存在的公开前置事实，不是本轮观察的 semantic result。仅在外置测试项目内通过原 fixture API 建立及选择；本仓唯一正式 Task/Delivery 不变。原生 prompt 只指向正常 Phase2 责任、明确 fixture key/root、facts 的位置和只读权限；不额外要求读取特定消费者方法，不写分类、通过条件或完整推导。

collector 的 `collection.json` 仅是进程、命令和退出事实，`native.jsonl`／`native-final.txt` 保持实际输入输出。原始日志留外置临时目录，不写入 tracked 或 gitignored 的长久转录。Task-local `validation/diagnosis.md` 由原 owner 写最小可查依据、判断和边界，不复制完整日志、全量读取历史、hash bundle、用户确认或过程台账。

## 6. 状态、顺序、正常与失败流程

1. 激活前只完成本批 Planning 原门禁。激活后实施 owner 先核真实 checkout／scope／entry 与方法路径，采用仍完整适用的行为事实。当前没有足够事实时才运行已选中性观察。
2. collector 检查完整 provider 和匹配 upstream 依赖，建立隔离中性项目、其真实公开 Task／Delivery 前置及事实。若 setup 失败，保留首轮真实错误并修装配；未启动 Agent 不属于判断失败或行为通过。
3. 启动全新 `codex exec --ephemeral --json`，只读执行原 Phase2 责任。采集 prompt、工具、实际读取和结论；不把本会话上下文或 #853 答案传入。禁止对 fixture 外的产品、Task、GitHub 或其它聊天写入。
4. host 先确认原入口确已执行、实际读了哪些正文／事实、行为材料与观察层是否一致，再按§8判断。未读已有方法但结论碰巧正确，不独立证明其消费；已读正文但无推导，不独立证明方法有效。
5. 已有方法足够且实际入口缺消费时，形成只改原引用／调用位置的候选；已消费但仍缺具体推导内容时，形成唯一正文的最小差额候选。两者均回原资格和 Author／受影响 Architecture、Wording、Approval、展示/激活边界后才改规范内容。不得由当前诊断计划跳过该依赖。
6. 已有能力及足够当前行为满足目标时不改方法或入口；原审核 owner 明确证据范围和未来未知，完成其当前职责。仍不足时只补影响诊断/验收的具体问题，保持同 Task／Delivery；不能宣布完成。

fixture 无生产状态迁移。Agent 选择的只读源码／本地纯函数检查在 fixture 内执行；真实依赖整合的建议须落到具体已提交接口或结果，并沿原 Reconcile 说明后继，不由 collector 自动 merge。本 Task 真实 source/scope 改变时回 Clarify，原 full D1 身份和整体责任保留。

## 7. 恢复、兼容、迁移与集成

没有新生产 API／数据或兼容双路径，因此没有预定 migration、锁或回滚协议。原 test collector 的既有 cases 与 CLI 保留其真实直接消费者；新事实 preparation 仅在新 case 分支执行，不改变旧场景的 fixture 正文或预期。实现若发现旧 fixture helper 与当前 public API 有实际不匹配，先判断是否能在本次装配局部修正；不凭旧工具缺口扩张为全仓 upgrade。

同一次观察若进程输出丢失，先读该次外置实际文件，唯一可恢复时采用原事实；不重复 native run 制造更多“成功”。失败或未执行的事实保留；设施持续失败时重评能否更直接观察相同入口和未决问题，或者保持明确证据缺口。不得删除失败样本、弱化独立预期或塞入答案来得到通过。

实际规范性修订若改变 canonical skill/spec/workflow/overlay，原 tools owner 通过 `guru-upgrade-tools` 的匹配完整来源同步 dogfood，保留 Task/session，并执行受影响 projections、reapply/drift、sidecar 和 mode 验证。没有该修订时不触发这组安装工作。干净安装只有实际差额确需证明时执行一个代表性 throwaway；不执行完整多平台 Release 矩阵。无新 API 则不新增迁移 DTO／exit。

## 8. 验证设计

以下预期由 #853 与根 PRD 取得，不由 fixture 输出自行定义。当前尚未运行。

| ID／对应验收 | 层级、入口与输入 | 独立观察及失败含义 | 边界与停止 |
| --- | --- | --- | --- |
| V1／AC1 | 静态调用路径＋原生工具事件；当前 Phase2→共享方法／worker context→必要 consumers | 能定位真实判断职责、日常加载位置和实际读取；区分“文件可见”“读取发生”“推导被使用”。无法定位时保留具体缺口 | 静态引用不证明真实消费；不全量盘点所有 Skill；当前证据足以回答则停止对应调查 |
| V2／AC2、AC3、AC4 | `shared-material`，正常 Phase2 原生入口；实际缓存、调用、生成链、对象及观察记录 | 从真实文件判断是否同一实现增量；区分 dirty 七冲突与已提交两文档冲突；新无参 caller 与所需参数是静态差额，不能说成未执行的编译失败。冻结实验不证明新 SDK／新生成物／生产。必要工作落到具体接口、caller和验证，独立部分继续 | 不把七/二数字命中当通过。错误归属、整项等待、只merge dev即全部解决、否定适用本地事实或扩大另一 Task 工作均不满足原要求；不能以进程0掩盖 |
| V3／AC2、AC3 | `shared-ordinary`，同一正常入口；无影响变化和适用既有观察 | 原 owner判断是否有实际新差额并采用适用事实；没有必要线索时继续原路径，不新增全 Task/PR/chat 检查或只因换阶段重跑 | 合法必要检查不因简化被取消；观察只覆盖该事实条件，不证明所有未来判断 |
| V4／AC1、AC2 | 只有V1–V3仍有明确未决问题时，由原 owner选择窄对照或消费者补读 | 说明现有证据不能回答什么、补读/观察如何改变消费／方法／无需修复判断。若形成实质修复，原资格审候选和验证计划，修后经同类原入口确认效果 | 不要求统一A/B或固定轮次。额外加载完整方法只能回答局部诊断问题，不能单独作为修复效果／无需修复验收 |
| V5／AC4 | 确定性 collector/fixture 检查与实际选中 cases；修改Python做内存AST，fixture材料和采集字段定向单测，`git diff --check`，Task官方context validate | 机械检查只证明代码、事实装配、host/model隔离、真实启动/错误传播及context可用；没有预写转录/固定pass/关键词grader | 新单测须执行真实装配/命令路径，不比对自己的常量得出语义通过；当前改动无受管投影则不重跑安装 |
| V6／AC4 | 仅实际方法／入口修订后的 source/installed/package/platform、原tools同步与drift/sidecar检查 | 分发的完整匹配性和实际消费分别证明；原Check／独立完整Review仍覆盖全部真实候选 | 无修订不制造分发；不宣称外部业务采用、生产修复或完整Release兼容 |

实现先准备并核对最小事实装配，再运行原生观察，因为当前问题是加载与判断是否存在缺口；不先写预定方法或为固定红绿而回退。既有 #735 设施事实只支持装配可复用，不能替代本批 V1–V3。每项证据充分后停止；无方法修订也必须有足够当前行为依据，不能用单次加长提示成功替代。

## 9. Canonical 引用、本轮差额与实际未决项

RDT沿 `docs/{requirements,design,test}/current/behavior-validation-method.md` 的 R735/D735/T735；通用唯一方法沿 canonical quality-guidelines 的 Test And Validation Value。当前新增差额是本批 test-only 事实与行为观察，不修改共享方法定义。整体 source selection 与 PRD 约束不因 fixture 方便而变化。

Architecture沿§1 authority及原独立结果；当前 no-impact 不创建 contribution／ADR或共享导航改动。若诊断后规范性 owner、准入、接口、持久化或架构事实实质变化，回原 owner重新判断；旧 no-impact 不自动覆盖。

当前未决为原入口实际消费／判断、是否具体缺口及是否修复，这是本批诊断对象。当前可执行方案为有界观察及条件回原 owner，不是已确认根因修复方案；无待用户决定的需求歧义。实施 owner 按证据选择后续，并保留整体 Completion 条件。
