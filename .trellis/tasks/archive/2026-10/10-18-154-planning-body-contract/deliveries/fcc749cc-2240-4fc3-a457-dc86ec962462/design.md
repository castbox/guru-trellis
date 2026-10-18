# #154 D1 规划正文合同与读取链设计

## 1. 设计目标、来源与本批边界

本设计落实 [本批 PRD](./prd.md) 的 R1–R7、V1–V7 和 AC1–AC10。整体要求由 [Task PRD](../../prd.md) 与公共 accepted_scope 承载。本批是全量首次 Delivery，尚无前序交付；全部实现和验证责任留在 D1，没有另外分配的剩余切片。

固定开发基线 B 为 `855f236850714edc4b78169218c09568c823f336`，来源是本批明确选定的开发 main 基线；Planning H0 当前等于 B。内容范围从 B 开始；PR 目标为 main，目标前进不自动改变 B。后续实际 HEAD 由原实施/交付 owner 绑定，本设计不预填实现结果。

阶段适用 Architecture authority 为 `docs/architecture/README.md` 的 `current-main-0.6.17-guru.98`，constitution 为 `docs/architecture/00-foundation/design-constitution.md` / `guru-trellis-design-constitution-v1`，change contract 为 `docs/architecture/06-governance/change-contract.md`。候选评估选择 `architecture_impact / target_native`，沿 ADR-022 唯一 Author 和 ADR-024 Task/Delivery authority；本轮不提出新 ADR。Architecture contribution 位于 `docs/architecture/contributions/154-planning-body-contract.md`，尚待最终独立评估与后续实施阶段晋升。

目标是在既有 Author 和审核链中补齐正文能力，不改变 Task/Delivery 模型、阶段、Skill I/O、typed exits、accepted_scope、scope_ref 或 freshness 语义。不修改上游 seed、generator、hook、官方 agents 或全局包。

## 2. 当前能力、调查与目标差额

| 现有对象 | 当前事实与原责任 | 本批差额 |
| --- | --- | --- |
| `trellis/skills/guru-team/packages/guru-author-task-plan/SKILL.md`、`references/authoring.md` | 唯一 writer；已有来源设计处置、Policy、Docs Plan 和九个独立 profiles，但未规定四类正文骨架。 | 在同 package 增加共享正文合同、四类模板、两组完整过程示例，并在适用 profile 显式加载。 |
| `.trellis/scripts/common/task_store.py:_default_prd_content` | 原生 PRD seed 含初始目标和 TBD，仅创建初始文件。 | 保持不变；由 Author 在整体范围接受前完成正文。不能把初始文件当成成熟需求。 |
| `.trellis/scripts/common/delivery_store.py` | 创建选定 Delivery 的空 PRD/design/implement 与两个官方 JSONL。 | 保持不变；不把语义模板或充分性判断放入创建脚本。 |
| Clarify、Wording、Approval、Check、Delivery Review、Completion 的原 Skill packages | 原 owners 已按职责判断来源、规划充分性或质量；读取规则未统一指向四类正文合同。 | 在各原合同中指向同一 Author 正文合同及适用模板，核对当前阶段内容和实际引用读取，沿原出口返工。 |
| `trellis/workflows/guru-team/workflow.md` 与 preset overlays | 编排唯一 writer/审核/实施及平台入口。 | 只补全局 dispatch 必需的合同定位；不复制 step-local 章节规则。Guru 实施 dispatch 与官方 add-context 承接正文读取。 |
| `apply_guru_team_trellis_preset.py:skill_package_source_files/skill_package_installed_files/skill_platform_public_files` | 现有递归收集完整 package，并按现有公共投影规则分发 Agent 可读文件。 | 复用递归分发；正文模板和示例保持 Agent 可读，不误登记为 package-private artifact。无需新 installer 分支或公共 DTO。 |
| 现有 Planning chain fixtures | 结构/transport 检查不证明 Agent 调查、成文或审核行为。 | 单列真实 Codex Agent 场景、确定性校验和安装结果，不把三者混作一个通过声明。 |

现状与目标的差额是写作能力、明确加载和验证充分性，不是 Task 创建缺陷。现有合法草稿可以不完整，但在各原接受边界前必须收敛。

## 3. 唯一来源设计处置

来源为 Issue #154 当前正文（2026-10-18，正文更新于 `2026-10-18T05:09:11Z`），Task PRD 已区分规范约束与历史案例。下表只处置规范设计承诺；#577/#599/#589/#575 的历史事实不变成新功能。所有处置为保留，没有已知偏离，也不要求用户提供技术实现。

| 来源与原承诺 | 处置 | 真实设计落点 | 理由、影响及上游处置 |
| --- | --- | --- | --- |
| R1：原 Author 唯一拥有四类正文模板，并在对应入口显式加载；公共规则共享。 | retain | 第4节同 package 的共享合同、四个模板及逐 profile 加载。 | 正文能力归唯一 writer，避免跨 owner 副本；无范围变化。 |
| R1：整体 PRD 与 Delivery 方案分工；各产物在原接受边界完成。 | retain | 第4.2节正文职责及第5节三个接受边界。 | 不新增 Task 根 design/implement，不提前要求未来产物。 |
| R2：稳定章节、字段、场景深度、明确裁剪及验收映射。 | retain | 第4.2–4.4节具体结构与必填/条件规则，第8节验证设计。 | 非空和编号不替代语义；不新增机器评分。 |
| R3：先调查事实，Clarify 判断真实选择，Author/Architecture 负责技术细化。 | retain | 第5节按来源和返工原因分流。 | 不编造事实或用户回答，不把技术未定升级为产品缺口。 |
| R4：保留全部已接受语义，来源设计由 Delivery design 唯一处置。 | retain | 本节唯一矩阵、第4.4节来源整合与必要引用、第5节偏离回程。 | PRD/implement 仅引用矩阵，不新建第二份处置权威。 |
| R5：每批含全量 D1 均展开本批正文、前序事实、差额、剩余责任及 Completion 关系。 | retain | 第4.2节三个 Delivery 模板，第5节切片处理和第8节 V1/V5/V6。 | 复用不免除阶段上下文；历史事实不换成当前要求。 |
| R6：复用既有中文写作规范，准确性和完整性优先。 | retain | 第4.1节唯一 clear-writing 引用；各原 owner 在第5节自检/审核。 | 不复制语言规则，不引入字数、词表或认证。 |
| R7：canonical Author package 与原受管分发；原生 seed 不判断语义。 | retain | 第2节边界、第4.1节资产、第6节安装投影。 | 不修改上游生成器/官方 agents，无公共 API 迁移。 |
| R7：完整去敏示例必须包含输入、调查/澄清、切片、设计细化及审核修订。 | retain | 第4.3节 detailed/brief 两组过程示例。 | 示例是方法材料，不能冒充实际 Agent 验证。 |
| R7：原 owners 接入充分性与实际读取，正常遗漏回最早 owner。 | retain | 第5节明确 consumer 加载和回程；第8节 V7。 | 不增加通用 reviewer 或审批阶段。 |
| R7：RDT/Architecture 仍走原 contribution/promotion，不因模板填充写共享导航或空 ledger。 | retain | 第7节 delta_first 与真实贡献边界。 | 本轮贡献描述真实差额；shared-current 仅由原 owner 晋升。 |

## 4. 正文合同、模板与完整示例

### 4.1 单一源与资产

以下路径均相对 `trellis/skills/guru-team/packages/guru-author-task-plan/`：

- `references/planning-body.md`：共享格式、来源引用、阶段完成、深度和裁剪规则，定义四模板的适用关系。
- `templates/task-prd.md`、`templates/delivery-prd.md`、`templates/delivery-design.md`、`templates/delivery-implement.md`：各自列出顺序、字段及条件标记，只引用共享规则。
- `examples/planning-body/detailed/`、`examples/planning-body/brief/`：分别包含来源及过程说明、完整 Task PRD、Delivery PRD/design/implement 和具体审核修订。

现有 Author SKILL 与 authoring reference 保持入口职责，显式定位共享正文合同和本 profile 的模板。所有写作/审核加载唯一 `.trellis/spec/workflow/clear-technical-writing.md`。模板不复制该规范。新增正文文件没有 public handoff consumer，不进入 public output/schema，也不以 interface artifact 清单扩大 I/O。

### 4.2 各模板章节、顺序和字段

下表列出的章节按序保留。每节均在模板内带填写提示；共享规则只定义一次，差异字段由各模板明确指向。

| 模板 | 顺序与必要内容 | 阶段专属字段与条件 |
| --- | --- | --- |
| Task PRD | 1 来源/术语；2 背景/问题；3 目标/非目标；4 真实调用方/场景/流程；5 行为要求（条件、例外、失败结果）；6 约束/依赖；7 可观察验收及验证方式；8 实际未决项。 | 来源表定位角色与条款；要求和验收用稳定 ID；工程场景字段为 caller/precondition/trigger/behavior/observable result。不存在真实业务用户时不编用户故事。 |
| Delivery PRD | 1 整体来源/术语；2 整体与本批目标/非目标；3 本批起点/前序结果/依赖/剩余责任；4 本批调用方/场景/流程；5 完整行为/条件/约束；6 本批验收/验证方式/未决项；7 canonical refs/本轮差额。 | 包括 Task 覆盖项、本批排除项、首次无前序或实际前序事实、后续输入/边界及 Completion 关系。全量 D1 仍填写这些字段。 |
| Delivery design | 1 设计目标/需求承接/内容基线；2 当前系统/边界/目标差额；3 来源设计处置；4 模块/职责/设计取舍；5 接口/数据；6 状态/顺序/正常与失败流程；7 恢复/兼容/迁移/集成；8 验证设计；9 canonical refs/本轮差额/未决项。 | 有规范性来源设计时维护唯一矩阵，字段为来源、承诺、处置、具体落点、理由、影响和上游处置；无此设计时说明依据，不生成空矩阵。 |
| Delivery implement | 1 输入/引用；2 有依赖顺序的步骤与文件责任；3 验证入口/输入/预期观察；4 停止条件/适用回退点；5 唯一 Delivery Policy；6 唯一 Docs SSOT Plan。 | Policy 按既有 full/partial/staged 合同填写，不新增字段协议；Docs Plan 选择既有一种 strategy，说明 writer、直接 consumer 和晋升时点。 |

接口、数据与状态不是强制创造新对象：workflow 变更可写成“原 profile/输入 → 加载对象 → 原出口/consumer”，并说明既有公共数据不变。确有服务、API、持久化、迁移或状态转换时，必须给出名称、方向、字段/值、顺序、失败结果和必要恢复。不能把适用内容统写“不适用”。

### 4.3 完整去敏示例

detailed 组采用含接口或流程约束、完整条件和例外的技术来源，展示原文角色识别、语义承接、整体需求、全量及部分/后续切片、实际设计细化和一次具体审核修订。brief 组采用简单工程请求，展示可查证事实调查、尚缺信息的处理、无规范性来源设计的说明和完整正文。每组过程文件将输入、调查事实、真实选择或无选择的理由、初稿缺口、审核意见和修改后正文关联起来。

示例明确标为去敏教学材料；历史案例不自动成为当前要求，虚构对话也不作为实际用户答复或测试证据。可参考成熟实践的结构，但不复制业务私有材料或引入额外门禁。实际行为证明单独按第8节执行。

### 4.4 来源、引用与裁剪

Author 先读完整当前来源及相关条件，再组织正文；不得从摘要二次推导。来源表区分要求、约定设计、建议、候选、历史及原始证据。详细来源允许原文保留或等义组织，但内容须落入适用章节。简略来源先调查、后澄清真实缺口，技术细节由原设计 owners 完成。

每个必要引用带可解析 locator、章节/条款及本批用途。共享定义、完整规格可以引用；本批行为、条件、约束、设计差额及执行安排仍在对应正文展开。实施者和审核者实际加载引用以及它的关联条件；不能把链接存在当成读取。引用失效或来源实质变化返回原来源/阶段 owner，不创建摘要缓存或第二范围权威。

始终适用的来源、目标、调用方/场景、行为、范围、可观察验收和实际未决项不能因简单任务而消失。简单任务可以短写；条件章节逐项写明不适用的真实理由或等效位置。无状态变化则说明执行顺序，无迁移则说明没有数据/接口迁移；没有未决必要问题时如实说明，不制造问题。草稿只标具体缺口和待处理 owner，在原接受边界前补齐；空标题、TBD、宽泛编号或预填通过不算完成。

## 5. 加载入口、数据关系与正常返工

| 原 owner / 入口 | 必须实际加载与判断 | 原回程或接受边界 |
| --- | --- | --- |
| Discovery / Clarify | 当前来源、可查证仓库事实；Clarify 在原范围内加载 planning-body 的来源/充分性规则。 | 真实需求/范围选择由 Clarify 处理；不要求用户提供实现机制。 |
| Author task_scope_requirements | 共享合同 + Task PRD 模板 + 完整来源。 | 整体 PRD 完成后返回 scope_requirements_ready，原 Clarify 审查再 accept_scope；此处不要求 Delivery 方案。 |
| Author requirements profiles | 共享合同 + Delivery PRD 模板 + accepted_scope、当前 scope_ref/前序事实。 | requirements_ready 前完成本批需求/上下文；正常候选进入独立 candidate_assessment。 |
| Author solution/revision profiles | 共享合同 + design/implement 模板 + 当前 candidate_assessment、必要 PRD 引用。 | plan_ready 前完成方案/实施/官方 context；revision 读取实际受影响模板，机制变化重入候选评估。 |
| 原 Wording | 当前三份正文、共享合同及必要来源，按其原受控措辞范围核对语义。 | 等义修订刷新受影响 gates；实质承诺/机制变化经原出口回 Author，不接管通用充分性审核。 |
| 原 Architecture / Approval | Architecture 仍按独立 read order 审实际设计/消费者/贡献；Approval 读取三正文、模板合同、必要来源及 final_plan。 | Architecture 不成为 writer；Approval 核对场景→要求→设计→实施→验证→验收，普通缺口经 revision_actions 返回最早 owner。 |
| Guru 实施 dispatch / 官方 context | 当前三正文、planning-body、适用模板及必要本地规格，由原 task.py add-context 写实际路径/理由。 | 实施 worker 原地读取；缺规划依据回原阶段 owner，不修改官方 agents/hook 以强制新流程。 |
| 原 Check / Delivery Review / Completion | 按原完整范围加载正文合同、必要规划引用、实际实现/验证；Completion 另读整体范围和历史 Delivery。 | 普通遗漏回最早 owner；不以单批交付替代整体完成，不以静态检查替代真实写作验收。 |

公共 Task/Delivery 数据保持不变，模板只输出 Markdown。来源变更触发原 Clarify 的实际影响判断；等义更正只刷新受影响 gates，要求变化先发布整体 scope 再修订同批，机制变化刷新候选。恢复读取当前 key/planning_root、适用模板和引用，不重用已过期语义结果，不覆盖历史 Delivery。

## 6. 安装、兼容和故障处理

canonical package 是唯一正文源，dogfood `.trellis/guru-team/skills/packages/`、`.agents/skills/`、`.codex/skills/` 及声明平台内容由现有 preset 投影。canonical workflow、preset/workflow README 和 overlays 只定位原 owner/合同，不建立正文副本。采用现有 apply/reapply、drift、sidecar 与上游所有权检查，不修改 installer 的语义责任。

当前所有受控 consumers 同步使用新正文合同，无长期兼容 reader、adapter 或第二模板 authority。已有业务安装不会因源码改动自动更新；只通过完整匹配 workflow/preset 和原冲突处理采用新正文能力，保留用户自有内容及 `.new/.bak`。历史 Task/归档不追溯重写，既有合法半成品由原 owner 继续成文。

文件缺失、不可解析引用和普通 stale/mismatch 沿现有 owner 阻塞真实依赖；本地可独立工作继续。普通安装冲突先比较 source/current/sidecar 再按原规则处理，不能静默覆盖用户文件。正文不引入新状态机、锁、授权存储或攻击模型。

## 7. 长期文档与 Architecture 差额

三份规划命中的 requirement/design/test authority 为 `docs/requirements/README.md`、`docs/design/README.md`、`docs/test/README.md` 的 RDT `current-main-0.6.17-guru.107` 继承链，重点为 #250/#292/#531/#599 贡献。Architecture refs 见第1节。本轮增量为 Author 正文能力与原消费者加载，不改变既有身份、生命周期、API 或单 writer 决策。

Docs strategy 选择 delta_first。原 RDT owner 在 `docs/requirements-design-test-contributions/154-planning-body-contract/` 写真实需求/设计/唯一 Test 差额，原 Architecture owner 按真实 task-owned contribution 与既有晋升合同维护长期 authority。模板填充自身只写当前规划，不预创建空贡献、不直接改共享导航。Planning 的 Architecture contribution 是对真实候选的设计贡献，非已实现或晋升声明。实施阶段独立评估后由原 owners 在最终 Phase 2 前完成必要 reconciliation/promotion，后续 Check/commit/独立完整 Branch Review 覆盖实际写入。

## 8. 验证设计与验收追踪

### 8.1 真实 Agent 行为

使用一个代表性、完整匹配的 Codex 安装环境，经现有正常入口运行实际 Planning owners。宿主仅提供去敏来源、仓库 fixture 和合法起始上下文；Agent 自行调查、成文、审核并调用原 wrappers。不得预写最终正文、owner result 或 pass；录入 wrapper 输入只发生在真实判断之后。原始会话/工具轨迹保留在平台日志，唯一 Test 记录可定位入口、加载模板、正文、具体修订和结果，不另造审计链。

| 场景 | 执行设计与输入 | 必须核对的行为及证据 | AC |
| --- | --- | --- | --- |
| V1 | 带明确接口/流程约束、条件与例外的详细技术来源，原 Intake → Task PRD → full D1 Planning。 | Agent 读取全文；四正文按模板成文，逐项核对承诺和来源设计落点；观察真实审核及必要修订。 | AC1/2/3/6/7/9 |
| V2 | 简略工程 Issue，fixture 含可查代码/文档事实；调用原 Discovery/Clarify/Author。 | 先调查再处理真实需求选择；用户未答时保留 gap，不代填。需求明确但方案未定由 Author/Architecture 设计；无来源设计时无空矩阵。 | AC2/3/4/7/9 |
| V3 | 无 Issue 的实际请求，同一正常 intake/write/review 入口。 | 从请求与事实形成完整需求/设计，不能绕过原 mode/Task 规则，也不把 Issue 完整度作为 Planning 前置。 | AC3/4/7/9 |
| V4 | 去敏的真实多来源分歧，保留要求/建议/历史角色；交原 Clarify。 | 审核是否调查冲突并保留旧承诺；存在真实人类选择时交实际用户，未回答不假定成功。技术冲突归技术 owner。 | AC5/9 |
| V5 | 原支持的部分切片与后续 Delivery；前序结果必须由实际原 Delivery owner 或可核对的正常历史事实提供。 | 实际生成两批正文并读取前序；检查独立目标/差额、剩余责任、Policy 与 Completion。不得宿主伪写 delivered 或把当前 full D1 假称后续批次。 | AC6/7/8 |
| V6 | 让来源正常更新、保留支持的部分草稿；新原生 Codex 会话通过原 Bind/Selection 选同一身份。 | 原 owner 判断影响后仅重做受影响阶段；新会话实际加载必要引用；检查当前与历史要求分离、身份与停点保持。 | AC6/8/10 |
| V7 | 正常 Agent 初稿遗漏或原入口支持的未完成规划，交原审核而非篡改已接受事实。 | 实际指出具体缺口，沿原出口回 Author 修订，再审最终内容；保留缺口与修复前后定位，不把宿主造好的修订当成 Agent 能力。 | AC2/7/8/9 |

使用 V1/V5 中需要展开设计的样例检查复杂深度，使用 V2/V3 的简单工程样例检查裁剪。场景可复用环境和 Task；资源创建遵守原入口的前置条件与副作用边界。若平台、真实选择或前序路径不可用，记录精确缺口并阻止对应 AC 被标为通过；这不缩减 AC，也不阻断无依赖的实现与验证。规划时设计验证方法，实际执行和结果在实施阶段产生。

### 8.2 确定性与安装验证

| 验证层 | 入口与观察 | 覆盖 |
| --- | --- | --- |
| source / package | 原 source package checker、受影响 package tests 与上游 ownership checker；检查模板/示例可达、无新增 I/O 及上游改动。 | AC1/2/10 的客观分发事实。 |
| dogfood / 声明平台 | canonical apply 后检查 installed package、overlay drift、引用/模板实际投影、所有声明平台；逐个处理 sidecar。 | 原 consumers 可加载同源正文，不能推定各平台实际写作已通过。 |
| 一次代表性 clean + reapply | 使用官方 marketplace/完整 preset 路径及当前匹配 provider，在干净临时仓库安装；同环境 reapply，保留用户 sentinel 内容并核对 `.new/.bak`。 | AC10 开箱与用户内容保留；若普通更新也影响受管文件，沿原 update 冲突机制核对，不执行完整多平台矩阵。 |
| 实际读写/审核 | 第8.1节真实 Codex 入口与轨迹。 | V1–V7；不能被前三行机械结果替代。 |

AC1/2 由资产盘点、逐 profile 加载、模板正文及实际接受边界共同证明；AC3–6/8 由表中场景证明；AC7 由设计/实施/测试对应与原 Approval 语义审查证明；AC9 由原写作/审核 owners 对最终内容自检证明；AC10 要求安装与真实代表平台行为分列。当前没有实现、真实场景或安装通过声明。

## 9. 取舍、停止条件与未决边界

选择四个薄模板加一个共享合同，是为了使各正文差异显式可加载，同时避免两套公共规则。采用 Markdown 语义规则而非 Python 生成器，是因为充分性、来源角色、裁剪与设计取舍均由 AI 判断。复用现有分发而不加新 loader/DTO，是因为当前 consumer 已可直接读取受管文件。

当前没有待用户决定的产品/范围选择。尚待实施验证的风险是 Agent 实际加载/深度/返工能力和代表性安装冲突处理；必须通过第8节取得证据。若发现机制、owner 或 authority 边界扩大，先回原资格/Architecture owner；若 accepted scope 变化则回 Clarify。完整 Release 矩阵、其他平台实际行为、软件发布和业务安装均不在本批证明范围。
