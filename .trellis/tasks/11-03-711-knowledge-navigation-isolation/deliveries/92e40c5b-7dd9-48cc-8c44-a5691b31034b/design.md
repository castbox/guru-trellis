# D1 并行知识导航隔离设计

## 1. 设计目标、需求承接与内容基线

本批全量承接整体 R711-01..08、S711-01..07 与 AC711-01..08。development baseline B 为 main@f75f0f5dd078a0c2c4c9a54ac861383774162806，来源是本次原 Sync 固定 Git object；首次 D1 无前序 delivered head。Planning H0 同 B，内容范围为 B 到实际候选 H，PR 目标 castbox/guru-trellis:main；后续真实冲突由原 owner 处理，不追赶无关 target SHA。

独立 Architecture 原 owner 已实际发出 candidate_assessment baseline_current：baseline guru-trellis-architecture；constitution guru-trellis-design-constitution-v1/current；architecture_impact / target_native；decision_refs ADR-031、ADR-KNOWLEDGE-FINAL-INTEGRATION、ADR-KNOWLEDGE-NAVIGATION-ISOLATION。该输出只准入本方案，不能代替 Wording 后 final_plan。项目 change contract 为 docs/architecture/06-governance/change-contract.md / guru-trellis-architecture-change-contract-v1，concern set guru-trellis-architecture-change-concerns-v1，project-check descriptor 保持原 identity 与语义协议。

## 2. 当前系统、边界与目标差额

现有能力包括完整按能力知识、稳定身份、阶段适用、隔离贡献、候选检查与最终整合。根 README 与三层 current/README 仍逐项登记；current-knowledge、RDT spec 与 Architecture contract 的必要导航更新规则仍允许新增独立主题触及共享导航。当前项目读取 projection 又要求从 current/README 列表定位。

目标保留正文路径和原 owner，直接收敛上述规则及消费者。RDT 继续 docs/{requirements,design,test}/current/<stable-capability>.md；一个能力内部需多文件时使用该能力目录下的局部 README。Architecture 保留 FOUNDATION/CURRENT/TARGET/DOMAIN/INTEGRATION/GOV/GAP/PLAN/ADR/EVIDENCE 职责目录。独立能力写自身文件或自身目录，不能以 Task/Issue 新建第二 current。没有新服务、索引生成器、运行时 registry、schema、config switch 或语义脚本。

## 3. 来源设计处置（唯一）

Issue 没有预选具体目录布局，但其技术约束是规范性承诺，逐项 retain；不把它们降为建议。

| 来源条款 | 原承诺 | 处置与具体落点 | 理由、影响与上游处置 |
| --- | --- | --- | --- |
| #711 行为1 | 根稳定，禁转移共享登记，全局版本/历史不日常追加；列真实读写者 | retain；第4节读写表、第5节入口合同 | 直接去掉竞争原因；入口自身真实变化仍由原 owner 一次维护，无上游偏离 |
| #711 行为2 | 稳定能力完整正文与必要关系，真实重叠不拆散 | retain；第4/6节 | 沿既有能力路径更新；不按 Issue 复制 |
| #711 行为3 | 同步读取，区分 current/target/贡献/历史；维护稳定引用 | retain；第5/7节 | 检索只定位，原晋升及适用来源决定 authority |
| #711 行为4 | 原 RDT/Architecture、隔离贡献和各质量边界保持 | retain；第6节 | 不改 public I/O 或 formal stage owner |
| #711 行为5 | 同能力原 owner 语义整合；文本合并不能证明语义 | retain；第6/8节 V3 | 核组合完整定义与消费者，不取单侧 |
| #711 行为6 | 兼顾 RDT 与 Architecture，只改真实关联合同 | retain；第4/8节 | 只调整命中导航/读取者及本仓代表迁移 |
| #711 行为7 | 可执行迁移、未达/已达、在途版本、恢复与旧写退出 | retain；第7节与 MIGRATION-711 | 安装和文档切换分别完成，无长期双写 |
| #711 行为8 | canonical/spec/必要consumer、dogfood/installed/平台同步 | retain；第4/8节 V5 | 原工具维护 owner 同步，无手工受管覆盖 |
| #711 验收首段及各样本 | 旧新等价、实施前固定、实际 Agent 原入口/Check、两序合并与完整文件集 | retain；第8节冻结样本与观察 | 不减内容、不串行改写，不以结构或绿色包装通过 |

## 4. 模块、职责与设计取舍

共同方法唯一维护于 canonical RDT references/current-knowledge.md；RDT/Architecture 自身 SKILL 与 references/contract.md 只纠正命中的读取/写入条件并引用同一合同。RDT managed spec 变更相同语义。原 workflow mandatory owner、phase、typed exit 和 runtime 均保持；公共 README 给 matching 采用 locator，不复制方法。源码实际搜到的新 consumer 只有属于同一导航职责才纳入；其它新机制回原 qualification。

| 实际读者/写者 | 旧读取与写入点 | 采用后的读取与写入路径 |
| --- | --- | --- |
| RDT impact/promotion/bootstrap/repair | 三层根及 current/README 列表；必要导航可写共享列表 | 稳定根给 scope/current目录/历史边界；限定搜索到完整单元；写自身正文与真实受影响关系；根仅其自身合同变化时写 |
| Architecture 各原 profiles | Architecture README 个体条目，完整职责正文和共同方法 | 根按职责给固定目录发现；读完整单元及适用状态，写所属单元/必要关系；不将新主题加入 system/ownership 等统一列表 |
| Author/实施/Check/Branch Review/独立 review | 原 current-knowledge + 适用知识；项目 usage projection 指向 current/README 列表 | 原 Skills 继续加载同一共同方法；项目 projection 改为稳定入口→目录/稳定ID限定检索→完整定义及必要关系 |
| Bootstrap projection owner | 写 .trellis/spec 项目读取顺序 | 一次迁移更新 docs/requirements-design-test-ssot.md、architecture/baseline-usage.md 等实际有旧读假设的投影；不产生逐单元索引 |
| 公共 workflow/preset README 读者 | #331/#638 安装及知识采用说明 | 增加 #711 matching迁移链接，纠正当前宽泛导航条件；历史迁移快照不改含义 |
| installer / upgrade-tools | 递归 package与managed spec安装，平台投影 | 原维护机制同步实际源，保留Task/session/用户内容；不迁移业务 docs、不判断语义 |

备选共享生成索引仍需每 PR 提交，因果不变；不采用。单一聚合目录 README 也被拒绝。外部知识服务/全局 registry 没有当前必要性，不加入。选定方案使用现有文件和 rg，代价是读取端先限定检索、再核状态及关系；它保留原 AI authority 成本，无额外运行依赖。

## 5. 接口与数据

公共 Skill id、profile、input、typed exit、schema、recorder 与原 projector 不变。RDT task_impact_sync(phase2)→candidate_ready、promotion(final_integration)→实际 ssot_current；Architecture candidate/final/phase2/promotion 原入口保持，Check 继续实际 matching profile。

根入口保留体系稳定 identity、scope/status、真实公共版本、历史/未迁移边界与查找方法。RDT 根/current入口给 current/** 的限定范围；Architecture 根按职责给目录级 locator。它们不枚举所有知识单元，不增加共享 metadata。普通新增不改根、current/README、全局 index/manifest/version/history。

每个完整单元在自身正文或自身目录内保留稳定 identity/aliases、状态、原 semantic owner、适用来源与晋升依据、完整定义、必要关系及替代边界。这是现有 Markdown 职责的收敛，无新 machine schema。已有 canonical 接口正文仍唯一拥有精确规格，单元不复制接口。

Agent 先读本阶段适用入口和迁移范围；再用 rg --files 限定 current或Architecture职责目录，并用稳定ID/概念检索；读命中完整单元并核其原 owner 晋升事实、适用来源及状态，展开回答所需 R/D/T/Architecture关系。目录名、文件存在、标题、排序、日期、版本或搜索命中均不能单独建立 current。未晋升正文留 task contribution/proposed；accepted target 在目标范围；历史/被替代路径保其语义。缺晋升依据/来源、重复 current或断链回原 repair/澄清，保留最后可读 authority。

改名保稳定ID；替换/删除保前驱/后继及旧引用意义。需要旧路径解析时保留只定位转换的说明或固定Git引用，不留另一份活动完整正文。局部引用/关系改动由关系原 owner 管理；两任务共同修改同一有效关系属于真实重叠，不能复制规避。

## 6. 状态、顺序、正常与失败流程

无新状态机。既有 isolated contribution/proposed→候选 Check→原 owners final_integration 实际写入/读回→implementation重绑全部实际after→最终Architecture/Check→commit→独立完整committed Review保持。

在 Task candidate 内先准备完整 proposed docs、根入口迁移及必要关系，shared current 此时保持原样。候选检查后两维护 owners 固定一次真实目标branch/commit，重读命中单元与原贡献，按语义整合差额并实际写入。新独立单元只写自身路径；根合同迁移是一次真实入口改变，在本批受审目标内，不变成以后登记义务。

同能力/同关系并行须比较 applicable base、双方完整proposal、实际target及受影响未改consumers，保留全部仍有效条件。合法Git自动合并是文本工具，不能替代这次判断。范围变回Clarify；机制变回Author/Architecture；验证义务变回原质量owner。partial/output-loss沿原唯一intent恢复，不加账本/锁。

## 7. 恢复、兼容、迁移与集成

MIGRATION-711.md 定义文档组织合同 knowledge-navigation-1；这是采用边界标签，不是新 Skill API 或共享递增版本。安装新规则与项目文档切换分两步。

迁移 owner 先固定旧完整Git版本和全部旧入口，列实际读写者、目标能力、稳定ID/aliases、必要关系与未迁移范围。候选完整正文须通过原语义/traceability/样本门禁，再由原 owners final_integration 切入口。未满足条件：原 authority仍可读，候选 proposed，明确未迁移范围，不声称消除共享写入。满足后：根只提供发现方法，所有已迁移单元自身可定位且关系完整，新任务不继续登记旧索引。

本仓代表迁移：三层根与 current/README从枚举变发现；逐项核原导航alias在原完整单元中仍可检索，缺失alias只补所属单元，不复制正文。原能力正文路径保持。legacy .109范围、固定旧Task及 predecessor Git引用保留；未迁移历史语料不宣称已完成。Architecture根保体系和职责目录/状态、真实版本及旧来源，原具体单元identity与关系在各自正文保留；治理/变更合同补新决策，不向ADR shared index追加逐项登记。

旧Task读原阶段适用版本，退出触发仍为Finish、合法Reactivate改选或真实依赖变化；最终集成如命中已迁移单元，由原owner重读真实目标并整合到当前单元，不回写旧根/current索引。未触及范围不为新规则重做历史。失败在切换前保持旧入口；切换后普通问题走原repair/受审successor。历史Git、versions及原始失败字节不回填。

完整 matching source采用通过原 guru-upgrade-tools（已有checkout）或适用full installer（新代表安装）同步；canonical先改，再由原owner同步dogfood及真实installed。对旧安装使用同provider workflow preview/create-new、审差额后force；当前本批不改workflow bytes。sidecar逐项处理，不手工覆盖受管投影。项目docs切换另由maintenance owners执行，不由安装器暗迁移。

## 8. 验证设计

下列正常样本和必答事实在实现前固定。所有旧新 Agent 侧使用同一个实际配置的Codex模型版本、CLI、工具权限及等价起点；记录实际配置/模型与首次执行。不得向任一侧预载另一侧答案、轨迹或host验收表。样本全部去敏、无业务仓修改；没有成本改善比例或统计推断要求。

固定公共事实：示例仓具备“审计查询”与“通知文案”两独立能力。审计查询仅租户拥有者可读，不能跨租户，输出不含secret；通知文案按profile locale选模板、无匹配回en，不能输出token。每能力有完整R/D/T与Architecture职责，稳定ID、来源和仍有效条件。另有不迁移的旧账单范围，明确保其完整旧来源；历史审计定义与未晋升审计proposal同时存在，不能覆盖current。

| 验证 | 要求/样本/正常入口与执行 | 必须观察与边界 |
| --- | --- | --- |
| V711-1 独立A/B | S01；A在审计能力下新增独立CSV导出单元（owner租户校验、固定列无secret、失败无副作用及对应R/D/T/Architecture）；B在通知能力下新增独立locale预览单元（profile locale→en回退、无token、只读及对应关系）。旧新各从不含对方贡献的同一B克隆为A/B，实际installed原maintenance与matching Check/晋升完成后固定候选 | 保存旧首次冲突；新A→B/B→A均无导航/全局版本/历史冲突；核全部文件集合无下层共享登记。分别核两单元全部事实及关系。不得先合A再让B改写 |
| V711-2 读取与既有修改 | S02/03；合并后实际Agent从稳定入口查两新增主题及审计current、target、未晋升proposal、历史。修改既有审计正文：支持原查询同时增加CSV列的UTC时间字段，保owner校验与无secret | 当前完整答案和必要trace/source可核，不混状态或第二current。实际写原能力完整正文及关系，不创建每Issue副本或修改全局登记。RDT与Architecture均覆盖 |
| V711-3 真重叠 | S04；两个独立Task修改同审计导出能力：一方要求每次最多100行并明确超限拒绝；另一方要求时间字段统一UTC且空结果仍有列头。原owner在实际target整合 | owner辨识真实差异；组合保既有租户校验/无secret和双方三条件，审核受影响R/D/T/Architecture；不取一侧、不以无文本冲突宣称语义通过 |
| V711-4 迁移与生命周期 | S05/06；同等已有文档样本，先提供尚缺必要测试关系的候选，后补齐并经原链切换；保未迁移账单与旧Git引用。一个旧阶段Task在已切换目标final integration。改名audit-csv→audit-export保稳定ID，再替换或删除旧展示单元并维护存活引用 | 未达条件保原authority/标未迁移，已达才切换；旧Task仍按其计划版本读，集成写当前单元不恢复旧索引；仍有效引用与关系解析，历史不改；不声称业务仓已迁移 |
| V711-5 分发与采用 | R08；一个代表clean安装，先取得matching旧侧snapshot，更新同代表安装得新侧snapshot，之后样本克隆此已安装环境而不重复clean。dogfood由原tools owner同步；定向source/installed/package、所声明平台、reapply/drift/mode/sidecar | 实际安装入口成功且正文可读，用户内容和Task/session保留。reapply后不漂移。源码/安装与Agent证据分别记录；完整多平台升级Release及业务项目采用未覆盖 |
| V711-6 正式任务质量链 | 全部AC；本任务本身原Architecture、完整候选Check、实际晋升/读回、after重绑、最终Check、commit/独立完整Review、Delivery/Completion | 样本不是本Task正式门禁。最终完整当前定义和公开规则同一PR交付；无未证通过声明 |

native样本从正式安装Skill进入，执行实际公开owner与所测基线匹配的Check合同。host可以建立边界前合法Task/Delivery/Plan起点及环境，但不能替本阶段owner填语义结果、私有摘要、修改Agent输出或跳过关键条件。需要独立Architecture时使用真实独立Agent；其正式结果原样消费。旧侧规则若导致冲突，保首次证据并按旧原owner合法整合完成必要后续读取，不能改写B候选再声称无竞争。环境/命令失败保留并如实判execution gap；修订重跑单列，不能重名首次。

确定性脚本只建样本、执行Git/CLI、收集输入输出/路径并核预先指定的事实；AI在原owner职责判断语义充分性。原始native轨迹留repo外run-root，唯一test.md记录实际摘要、首次失败、原结果locator和证据边界。避免为文档规则写只搜索固定句子的自证测试；定向结构检查服务分发/引用，不能冒充行为证明。

## 9. Canonical 引用、本轮差额与实际未决项

命中RDT-REQ/DES/TST-KNOWLEDGE的R331/R638/R693及其完整前驱；Architecture ARCH-GOV-012、change-contract与根发现职责；原ADR-031/ADR-KNOWLEDGE-FINAL-INTEGRATION保持，新增ADR-KNOWLEDGE-NAVIGATION-ISOLATION只拥有导航决策。

真实Architecture contribution为 docs/architecture/contributions/711-knowledge-navigation-isolation.md，必要ADR候选同目录711-knowledge-navigation-isolation-adr.md。RDT差额位于 docs/requirements-design-test-contributions/711-knowledge-navigation-isolation/，在phase2形成完整proposed目标；原owner最终整合。当前无未决产品或机制选择。actual Agent、安装与合并证据尚待实施，未完成前不得宣称验收或整体完成。
