# D1 架构机制审核设计

## 1. 设计目标、需求承接与内容基线

本设计承接本批 PRD 第5节及 D1-AC1至D1-AC6，全量覆盖整体 R1至R8。目标是让原 owners 先独立判断机制必要性和代价，再解释实现；以模型防御偏好为重点纠偏对象，但不声称证明训练成因或保证消除所有偏差。

原 `DeliveryProjection.content_base` 已解析内容基线 B 为 `2f70796103406683a2f63adfb6b54d247a7433a5`，来源是 D1 无前序候选时明确选定的 development baseline。Planning H0 与观察到的 `origin/main` 均为该提交；H0 不是最终实现头。交付目标为 `castbox/guru-trellis:main`，后续内容范围保持 B 到实际候选 H。

独立 Architecture candidate_assessment 的实际正式出口为 `baseline_current`，影响为 `architecture_impact`，路径为 `target_native`。阶段适用 authority 是 `guru-trellis-architecture`、`guru-trellis-design-constitution-v1` 和 `guru-trellis-architecture-change-contract-v1`。原因是本批实际修改项目 change-contract 的规范性方法投影；该写入必须由原 Architecture owner 承接。这个候选结论不替代 Wording-current final_plan、实施候选检查或晋升。

## 2. 当前系统、边界与目标差额

没有前序 Delivery。当前公共系统已具有正常场景、solution、root/protection 资格，原 Architecture 独立审查、current-knowledge 和 whole-task Completion，脚本只验证客观事实。

| 当前位置 | 当前事实 | 本批差额 |
| --- | --- | --- |
| Architecture contract 的 Constitution applicability / Responsibility and change causality | 已拒绝旧实现自证，但明确入口偏重 added capability 和单项原则；更直接替代要求保留 current contract，容易把受审旧技术规则也固定下来 | 在同一 owner 定义采用机制的适用判断，区分真实约束与受审技术选择 |
| root-cause contract 的 Protection | 已要求 protected object、real harm、direct owner、current-layer necessity | 补提出方责任、现有缺口/收益/代价和合法输入影响；保密约束不以事故为前置 |
| current-knowledge | 已有完整单元、适用来源、文档迁移与旧 reader 退出 | 加入能力/适用性文档足够时的取证边界、错误决策的存量实现处置和当前事实表达 |
| Author / Approval / Check / Branch Review / Completion | 有机制准入、设计充分性、完整候选与整体完成职责；Check/Review 仍突出 added capability + 单项原则 | 只补直接引用和当前职责中的消费，不复制新的全流程或问卷 |
| 项目 change-contract / RDT knowledge 与 completion 单元 | 现行方法投影和完整行为来源 | 形成隔离拟写，按各自原 owner 最终整合；不让公共新正文自行证明项目已采用 |

不改变公共 Skill/profile/typed exit、Task/Delivery API、状态模型、single-writer、技术栈或分发机制。保留完整五原则，不修订原则排序，不给最短 diff 优先权。

## 3. 来源设计处置（唯一）

本矩阵逐项承接研究 proposal 第2至9节；原文完整 locator 在 PRD 第1节。没有改变、拒绝或降级其承诺。

| 来源条款与原承诺 | 处置 | 具体落点、理由和影响 |
| --- | --- | --- |
| §2.1 本次采用机制，含无 diff 复用；普通 helper 不逐个审 | retain | §4 Architecture 主正文定义行为/约束单元、直接消费者和轻量无影响路径 |
| §2.2 作者、reviewer、模板提出保护均负举证；缺技术手段不独立成立 finding | retain | §4 Architecture 与原 Protection 职责承接，Check/Review 消费；不转移反证责任 |
| §3 五项聚焦判断，完整宪法，无全局最优或逐项产物 | retain | §4 紧凑语义问题，实际命中时给事实，不做评分或新字段 |
| §4 高发机制按承重事实判断，保留必要协调/密码学 | retain | §8 四组事实正反对照；分类是素材，不作关键字拒绝规则 |
| §5 晋升单元说明行为、owner、范围、理由、代价和重审条件 | retain | §4 current-knowledge 中既有完整单元与 Architecture 晋升责任；不新增单元 schema |
| §5.1 纠正同一决策须查存量，同步/分期/场景保留；Task 义务不消失 | retain | §4/§6/§7；Completion 原路由判断未实现与仅缺证据，分析不授权全仓迁移 |
| §6 已覆盖可简短承接；真实条件或证据变化才补重审 | retain | §4 Architecture 与 current-knowledge，复用现有 Candidate Applicability And Coverage |
| §7 RDT/Architecture 优先；实际行为、全部相关消费者、性能或冲突再查实现 | retain | §4 方法正文；不为证明能力存在无限源码考古 |
| §7 可质疑旧技术规则，受审变更后实施，再按原合同晋升 | retain | §4/§6；项目方法投影由 Architecture 隔离贡献承接，不提前写 CURRENT |
| §7 吸收必要性与能力复用，拒无 consumer 预留，不机械六步 | retain | §4 方案比较；不要求每个原因归一个 helper，不阻止必要边界/消费者纠正 |
| §7 缺证只限制依赖结论；旧保护不擅删、不把缺证视为通过 | retain | §6 三类处置；保留实际安全和权限约束 |
| §8 原 owners 及知识晋升/Completion 分工，不加阶段/台账 | retain | §4/§5/§9；只使用原公共输出与真实贡献 |
| §9 相同事实和可比上下文真实执行，答案隔离，机械与行为分别报告 | retain | §8/implement §3；保留原方法已具能力、首次失败、修复和未覆盖范围 |

## 4. 模块、职责与设计取舍

### 4.1 唯一方法正文和直接 consumers

1. **Architecture 原 contract**：在原 Constitution applicability 与责任因果段落中组织机制审核方法。审本次新增、修改、复用、扩大使用及直接影响。判断对象依据行为、状态和依赖，不依据文件名或 diff 大小。普通调用与无因果依赖不递归建单元；纠正同一错误决策时扩大到其受影响存量分析。
2. **Protection 原 contract**：在现有 Protection 分支补提出方的证据责任。作者、reviewer、模板都要说明真实要求/可信事实、现有保障缺口、补齐关系、收益与整体代价。保留真实权限、身份、资金和保密事实；不以事故发生为前置，也不从保护标签自动推出 AES、长期 key 或全局锁。
3. **current-knowledge 原正文**：维护完整单元的实际范围、取舍理由、适用条件与重审触发；从适用 RDT/Architecture 回答充分的问题。实际行为、性能、全部相关调用者或文档冲突有缺口时才追实现。纠正决策时在原单元/change contract 说明存量与过渡，不另建 ledger。
4. **Author / Approval**：Author 在原候选形成和方案比较中消费该方法；Approval 在现有 design adequacy/acceptance/Docs/provenance 维度核具体承接。只补必要定位，不能再形成一套五项问卷。
5. **Check / Branch Review**：将其 Current constitution consumption 的局部强调改为完整宪法下的采用机制审查。核实际候选、未改消费者、首次失败与证据范围；提出新增保护的 reviewer 同负举证。finding 仍先走正常场景/solution/root 原准入，不以新文字绕开它们。
6. **Completion**：在原 Stage facts / whole-task judgment 内明确：新入口、新决策、旧实现、环境是不同完成事实。已在 accepted scope 的迁移拆 Delivery 仍未完；实现遗漏走原 remaining/revision，真实外部证据缺口才 evidence_pending。正文引用 current-knowledge 的存量关系，不复制迁移台账。
7. **分发及 eval**：原 preset 和声明平台投影完整分发。既有 native adapter 的 Architecture 与 Completion factual staging 承接本批场景，host corpus 只供测试 owner 核对，不进入受测上下文；不建设新的通用评测框架或生产审核服务。

上述位置均在 `trellis/skills/guru-team/packages/` 对应 package 的原正文；Completion 的正文为其 `SKILL.md`。受管副本由原 apply 写入，不能手工 patch 副本冒充源修复。

### 4.2 语义判断与选择

原 owner 在找到设计依据后，先独立判断当前选择是否必要、范围是否匹配、代价是否值得。重点问题是：承担什么真实行为；谁决定/提供事实/维护状态；哪些对象和时间段被协调或拒绝；引入哪些共享写、扫描、阻塞时长、重试、key、状态与恢复前置；移除、缩小、替换或保留的后果及证据是什么。只有实际命中时说明事实，不要求逐项持久填报。

方案比较保持真实业务与外部合同，允许质疑被审的旧技术选择。采用既有能力、平台原生能力、已安装依赖或新代码都须符合实际场景；仓库已有不是自动采用理由。新增抽象须有当前职责和直接 consumer。局部删 key 却新建会话台账不自行证明简化；必要职责隔离、消费者适配和旧路径退出也不能为最短 diff 被省略。

### 4.3 存量关系

- 共存会破坏同一不变量、产生不兼容读写或使纠正失效：承接必要旧路径适配与退出，必要 scope/切片变化回原 owner；相关纠正未完成不能对外宣告完成。
- 可独立保留：写明共存如何保持约束、实际剩余采用者、保留理由、owner、具体后继交付或可观察触发条件、退出证据。工期、改动量、一个链接或“以后碰到再改”不能替代安排。尚未承接须如实记为待承接；新消费者不得扩入已判错模式。
- 场景不同且旧理由仍成立：明确范围后保留，不将它误报为全仓纠错。

分析可以大于实现范围。必要本地适配不为保持 diff 小而拆走；真正独立的工作沿已有收敛路径安排。只在原后继规划及真实触发点核退出，不增加巡检系统。

## 5. 接口与数据

公共 I/O 和持久化数据不变。现有链路为：Author 的 candidate → Architecture candidate_assessment → Author solution → Wording → Architecture final_plan → Approval；后续保持实施/候选 Check/原 final_integration/after 重绑/最终 Check/committed Review。

原 evidence、reason、finding、Docs Plan、完整知识单元和贡献字段承接具体结论，不新增 per-mechanism DTO、分数、授权字段或跨阶段 digest 链。脚本不根据文字、关键词或缺少某技术手段生成 semantic pass/finding。

测试 corpus 与事实运输只属于测试设施，其读取/结果文件不成为正常 workflow authority。raw traces 放 repo 外临时运行目录，唯一长期 Test 文档保留必要来源与具体观察，不持久化用户授权过程。

## 6. 状态、顺序、正常与失败流程

本批不增加状态或阶段。原 owner 先还原受支持的正常完成路径及必要权限/数据/业务约束，再针对具体异常或时序判断保护，最后反查对正常请求的损害。

- 依据充分：采用或简短承接，使用仍适用的真实工程事实；不因阶段/版本变化重跑全部命令。
- 已证实不必要、代价失衡或职责偏离：说明具体偏离、真实 owner、可行替代、消费者适配与旧路径退出，沿原机制修订；真实范围/authority 变化回原路径。
- 关键依据不足：补证并限制依赖结论。新保护不先升级为强制义务；旧保护不擅删也不把缺证视为复用通过；无关工作继续。
- 无因果历史债务：如实报告，不自动成为 finding、强制新 Issue 或跨仓修改；同一被纠正决策的受影响存量按§4.3处理。

实施依赖的来源或方案前提失效时，停受影响写入并回原 Author/Architecture/Clarify。测试/断言错误留原实施/Check，不靠加强拒绝、串行化、重试或弱化预期造绿。

## 7. 恢复、兼容、迁移与集成

本批直接修订同一公共方法和受控 consumers，不建设第二执行路径、兼容 parser 或旧新双 authority。历史 contribution、旧任务及不可变 snapshot 保持原义；仍适用的在途结论按真实差额判断，不能只凭新版本使其全链失效，也不能继续扩大已证错误模式。

现有安装只有经匹配 workflow/package 的原更新和完整 preset reapply 才采用新规则，沿原机制保留本地内容、处理 sidecar 并验证。源码分发不证明后端安装、业务迁移或生产切换，本 Task 不执行那些动作。

`docs/architecture/06-governance/change-contract.md` 的拟写只在本 Task 的 Architecture 隔离贡献下保存。RDT 的 knowledge/completion 三层拟写由原 RDT owner 准备。独立 Architecture 和完整候选 Check 先看全部实现/拟写；原 Check 合法回 implementation 后，分别由原维护方 final_integration 写入、读回，实施 owner 用同 B 与全部 after 路径重绑，再最终 Check/commit/完整 committed Review。Planning 不写共享正文。

## 8. 验证设计

验证先冻结事实/预期、当前 B 的规则文本和运行配置，再修改方法。每组原/新各一次独立 native 执行，共八次；这是有界案例观察，不是统计结论。若事实或共同运输改变，双方同口径重做，保留首次结果。若两边都正确，记原有能力，不记新增收益。

| 验证 | 对应验收 | 相同事实与入口 | 必须观察 |
| --- | --- | --- | --- |
| V1 游标与保护 | D1-AC1 | 原 Architecture native owner：普通分页参数/opaque、既有可信 token 哈希记录、reviewer 新签名提案；另给明确保密载荷 | 区分保密、完整性、归属/范围绑定和签发证明；无缺口不新增长期 key/会话台账；必要保密不因未出事故而取消 |
| V2 协调与重试 | D1-AC2 | 原 Architecture native owner：配置稳定时独立账号争用控制记录，与真正共享库存约束对照；附首次竞争失败及之后恢复事实 | 判断最小协调范围，保留必要全局约束，分别报告首次可用性与重试恢复；不一律拒锁或以恢复自证 |
| V3 旧机制复用 | D1-AC3 | 原 Architecture native owner：新入口复用旧 AES/协调但 Utility 无 diff，另有已论证同类消费者；受审旧技术规则与删除合同未核清 | 当前适用性有实质理由；合法复用简短；可比较替代且不让受审规则自证；缺证不擅删/全局停工 |
| V4 存量与完成 | D1-AC4 | 原 Completion native factual fixture：新旧 writer 同状态；可独立迁移与不同场景旧入口；Task 内迁移被拆后继 Delivery | 识别必要同步适配、真实可执行分期和场景保留；原 whole-task owner 不以新入口交付/CURRENT 晋升抹去未完成义务 |
| V5 机械与分发 | D1-AC5 | 命中 package/runtime tests，source/installed 校验，preset apply/reapply、平台 parity/drift/sidecar/mode | 真实 wrapper/投影与受管写入正确；不以规则字符串快照证明语义 |
| V6 语义证据复核 | D1-AC6 | 逐次读取 V1至V4 原输入、实际 Agent 输出/trace 与原 wrapper stdout，之后再看 host 预期 | 具体机制和因果映射正确，预期未泄漏；执行失败不评分为语义通过；结论限于实际版本、模型和场景 |

V1至V4 复用 `adapters/eval/architecture_authoring.py`、`stage_result_authoring.py` 与原 `run-skill-evals.sh`。既有事实运输不能表达本批四组输入时，在原 adapters/corpus 增加 fact-only 场景和运输测试；不写选择结论的分类器。原方法侧使用 B 的实际规则，双方使用相同去敏事实、前置、运输、有效模型配置与权限；不载入另一侧答案。新方法须满足所选场景的完整预期；规则存在、出口相同和命令绿不能代替核对。

只在一个已安装临时 fixture 证明完整 packages 与全部声明平台可读、同版本 reapply 后本地用户内容保持及零未处置 sidecar。该代表性验证不扩成全部平台/升级历史/Release 矩阵，不运行业务 Docker/生产链路。缺 native/模型/工具依赖保留具体 execution gap，本 Task 的该项验收仍未完成。

## 9. Canonical 引用、本轮差额与实际未决项

实际源位置与各 owner 见§4。项目 RDT 只对 `docs/{requirements,design,test}/current/{knowledge-maintenance,completion-closure}.md` 的命中完整单元形成拟写及追踪；测试实际结果唯一进入 `docs/requirements-design-test-contributions/architecture-mechanism-review/test.md`。历史、导航身份和全局版本不因普通方法修订重编号。

Architecture 贡献为 `docs/architecture/contributions/architecture-mechanism-review.md`，完整项目方法拟写位于 `docs/architecture/contributions/architecture-mechanism-review/proposed/docs/architecture/06-governance/change-contract.md`。其关联现有 ARCH-GOV-007/008/012、ARCH-DOM-008 和 ADR-034。当前没有原则例外、owner/single-writer、compatibility exit 或技术栈决策变化，不另建 ADR；若实际实现改变这些事实，回原 Architecture 重新判断。

没有阻塞方案编写的未决产品问题。规则、安装、八次 native 对照及最终质量链尚未执行；它们是后续工作，不能记为通过。
