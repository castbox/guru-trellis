# D1：按当前出口查询与按步加载设计

## 1. 设计目标、需求承接与内容基线

本批完整承接 [PRD](prd.md) D1-R1–R5、S1–S5、AC1–AC3，以及[整体 PRD](../../prd.md)全部已选 anchors。目标是一次查询取得当前出口的唯一 consumer 和必要入口合同，正常会话按当前步骤加载，同时保留原 legacy 维护能力。

固定 development baseline B 为 `05a16a5989669ca216d8ba34b9b419776410f04d`，来源为创建时已包含 #793 的 main；没有前序 Delivery。后续候选通过原 construct-delivery-candidate 入口保留 B。Planning H0 是规划时同一 HEAD 的观察，不是最终实现 HEAD。内容范围为 B 后本批实际变更；PR 目标独立为 `castbox/guru-trellis/main`，执行分支为 `codex/792-step-context`。

独立 Architecture 实际返回 `candidate_assessment / baseline_current`：baseline `guru-trellis-architecture`，constitution `guru-trellis-design-constitution-v1`，`architecture_impact / target_native`。影响是全局路由的发现、按需加载和受管分发，以及既有查询扩展。依据为 ADR-035、ARCH-FND-001/002、ARCH-DOM-016/038、ARCH-GOV-012。采用当前 [constitution](../../../../../docs/architecture/00-foundation/design-constitution.md)、[change contract](../../../../../docs/architecture/06-governance/change-contract.md)；候选评估不证明完整方案或实现通过。

## 2. 当前系统、边界与目标差额

当前 canonical workflow 同时携带全量 graph、router/stop 正文、阶段正文和 continuation。原 `get_phase_index()` 从 Phase Index 提取到 Phase 1，因此夹带 continuation 和 Intake；原 `extract_continuation_contract()` 原样提取唯一块。discovery 只按 Skill 发现 public contracts；`installed.workflow_facts` 和 compatibility verifier 的 `_workflow_markers` 直接读取 workflow 标记。

目标差额：

- 全量 graph 标记及 router/stop 正文移到唯一 `trellis/workflows/guru-team/references/routing.md`，由 workflow 显式引用。Interface 仍拥有各 Skill 合同，图校验继续比较二者，不建立第二映射。
- 既有 discovery 增加可选 `--exit`，返回本次 consumer 合同及原 Markdown 入口。无出口查询保持原语义。
- Phase Index 紧邻 Phase 1；唯一 continuation 位于该提取区间之外，保留全局约束、当前阶段入口和原 producer 恢复定位，详情按需读取。
- 正常路径只识别 legacy 并交原维护 owner；必要历史详情进入原 references 或全局独有的按需 legacy 引用。

本批没有前序 Delivery。不改 upstream get_context、extractor、hook、trellis-* Skill，不增加身份查询，不改变 #793 qualifier 条件，不实施 #794。

## 3. 来源设计处置（唯一）

| 来源与条款 | 原承诺 | 处置和落点 | 理由、影响与上游处置 |
| --- | --- | --- | --- |
| #792 行为1 | 复用 runtime/get_context、标记、consumer；单一权威 | retain；§4、5，原 discovery/reader | 现有能力足以承接，无 wrapper 或第二 workflow，无需上游变更。 |
| #792 行为2 | 一次定位 consumer、入口/前置；异常停止 | retain；§5、6 | 返回合同和原正文，不让脚本解释条件；判断仍归 AI。 |
| #792 行为3 | 全表退出正常必读，当前上下文可达 | retain；§4、8 V3/V6 | 正文移动不改变阶段或 mandatory invocation。 |
| #792 行为4、边界 | legacy 按需加载，保留支持及来源，不改历史 | retain；§4、7 | 维护 authority 留原 owner，不按版本号截断。 |
| #792 行为5、迁移 | 明确查询 I/O/恢复，同步平台和在途采用 | retain；§5、7、8 | 新选项兼容扩展；matching 更新避免引用和reader混装。 |
| ADR-035 Decision、迁移 | 唯一 continuation、接收会话检查、原producer恢复；phase非pass | retain；§4、6、7 | 改加载组织，不改生命周期、选择或恢复资格。 |
| AGENTS §1–8、AI-first | Markdown判断，脚本执行事实；原安装owner、最小状态 | retain；§4–8及implement | 无脚本语义router，无新状态或授权；dogfood沿tools owner。 |

没有 change/reject 的规范性来源承诺。PRD 和 implement 引用本表，不复制第二处置。

## 4. 模块、职责与设计取舍

### 4.1 单一图与正常正文

canonical workflow 用一个机器可识别的 `guru-routing-reference` 注释声明 extension-relative `references/routing.md`，另用 Markdown 链接说明按需读取。source 扩展根为 `trellis/workflows/guru-team`，installed 为 `.trellis/guru-team`，由实际 mode/layout 显式确定。缺引用、重复声明或 matching reader 缺失停止，不搜索备用路径。正常source/installed runtime及出口查询直接采用reference-only；旧inline布局不进入新runtime。旧安装保留其原matching完整provider，完成原owner整体更新后才使用新查询。

`routing.md` 完整拥有原 mandatory invoke、exit、workflow/stop target及行为。每个 target 的原marker及其正文组织为可提取小节；共享原行为可用正文引用，不复制出口→target映射。保留原 conditional router 的全部条件、projection、恢复和stop语义。AI读取后理解实际profile，不由Python推断最终Skill。

全局workflow保留阶段顺序、mandatory显式调用、入口分类和通用停止。Phase Index只含全局约束、概览和当前上下文入口。唯一continuation保留接收会话检查入口、按公共current实际phase定位、缺失结果回原producer；其详细矩阵移到同一workflow按需章节，不建立并行continuation或缓存。原workflow-state breadcrumb仍定位唯一continuation。native phase/step/continuation API保持。

### 4.2 既有查询及直接reader

`runtime/installed.py`提供共用图读取/解析，原workflow_facts复用并继续校验registry/Interface、mandatory标记、出口与target。`runtime/discovery.py`基于已校验事实增加本次投影。source按出口查询除原package validate之外，须实际完成图/Interface校验；不能假定package校验已经证明图正确。

`verify_trellis_compatibility_matrix.py`的reader、source/installed snapshot、`.new` preview按同一引用规则读取。verifier仅对明确before-snapshot保留原inline标记读取作为只读历史观察输入；它不是新runtime兼容入口，也不用于当前安装成功判定。新候选preview显式传matching candidate扩展根：本地候选用source assets，installed snapshot用已装assets，不能拿旧installed reference配新preview。该历史观察分支仅由现有矩阵before输入消费，由verifier owner维护；支持的before样本不再含inline时删除该分支及对应定向用例。reader只比较图事实，不执行语义。本次运行其定向用例，不运行完整矩阵。如touched文件超过3000行，按subtraction-first先评估并拆出真实reader能力，不复制实现。

### 4.3 legacy与受管资产

正常workflow和平台入口仅保留识别/转交原 `guru-maintain-legacy-task`、upgrade/tools owner的最短说明。历史详情优先回原owner references；全局独有说明放 `references/legacy.md`，由实际入口显式链接。原family、conversion、control-retirement、manual archive resume及historical closeout的准确pin/source和支持/停止条件保持。不得移走原owner必要资格判断。

原preset `MANAGED_ASSET_PATHS`注册两个workflow references。当前dogfood沿 `guru-upgrade-tools` 的完整源维护合同同步并保留Task/session。实际受影响spec、Claude/Codex等launcher及README只改加载定位，不复制图或Skill内部步骤。不新增registry、通用include框架、wrapper Skill、缓存或ledger。

## 5. 接口与数据

公开命令仍为原wrapper，增加一个可选出口参数：

```bash
bash trellis/workflows/guru-team/scripts/bash/discover-skill-contract.sh --root . --mode source --skill guru-author-task-plan --exit plan_ready --json
bash .trellis/guru-team/scripts/bash/discover-skill-contract.sh --root . --mode installed --skill guru-author-task-plan --exit plan_ready --json
```

最小新增输入为 `--exit <id>`，继续要求root/mode/skill。前置为完整matching provider、active stable Skill及其一个合法出口。installed出口查询启用完整workflow/graph校验；无出口合同发现保留原校验与输出。多个 `--exit` 参数作为普通多重出口误用明确拒绝，不让argparse静默取最后值。

| 响应内容 | 原来源 | 直接consumer与用途 |
| --- | --- | --- |
| status、skill_id、exit_id | 输入与客观结果 | 当前AI识别查询；不是正式Skill exit。 |
| consumer kind/id | 唯一Interface exit且graph一致 | 当前AI进入Skill、workflow target或stop。 |
| output_contract、consumer_input、projection | 该出口对应的public_contracts，保持原schema/Markdown形状 | 当前AI按原producer→consumer投影准备输入；不返回private_artifacts。instruction-only按实际Markdown合同提供。 |
| entry | Skill的原SKILL.md定位、entry_preconditions/input/invocation；或workflow/stop target原Markdown定位和对应正文 | 当前AI加载入口/前置，显式执行原Skill或router/stop。conditional target保留全部相关分支，脚本不替AI选择。 |

响应提供足够正文及合同定位，使调用方无需遍历全图。只返回当前出口的直接消费内容，不返回registry、全图、hash/mtime、历史扫描或私有恢复状态。无新Skill I/O schema、typed exit、consumer或Task/Delivery字段；CLI查询结果不成为跨阶段authority。

错误复用现有stderr `code / field_path / remediation`和非零退出。unknown Skill/exit、multiple、unmapped、target mismatch、缺引用、installed drift均停止。输入错误修正原输入；matching/分发错误回原tools owner；图缺陷由原Markdown/Interface owner修复后重查。不生成成功空结果。

## 6. 状态、顺序、正常与失败流程

没有新增持久状态转换。

1. 原owner实际执行并返回一个typed exit。
2. AI用producer Skill和exit调用discovery；reader校验完整matching图及Interface，再提取唯一consumer合同和入口。
3. Skill consumer由AI显式加载并执行完整前置；workflow consumer由AI按返回原正文处理实际条件；stop由AI报告原原因并停止。
4. 缺失语义结果回原producer恢复，不能从phase、文件存在或查询成功推导pass。
5. 实际legacy入口由原维护owner加载必要合同，保留其退出/支持条件；普通新Task不加载历史详情。

步骤2发生unknown/multiple/unmapped或引用不一致时停止，不猜测下游。步骤3的scope/profile/充分性仍由原owner判断并返回原出口。局部matching缺口只阻塞依赖路径。查询不记录授权、不改变selection、不激活Delivery。

## 7. 恢复、兼容、迁移与集成

新增CLI选项保留无exit调用；原Skill id/schema/exit/consumer均不变。正常新runtime直接演进为reference-only，不新增inline旧格式reader、fallback或双读。verifier只读before-snapshot的原inline输入覆盖见§4.2，不赋予当前runtime旧格式资格。

新增 `MIGRATION-792.md`：采用单位是matching workflow、references、runtime、preset和受影响入口，由原tools/upgrade owner检查完整源、冲突和sidecar后同步。仅更新workflow、尚缺引用或reader时停止，完成matching更新后重试。marketplace `.new`预览与force应用保留原规则；预览不等于完整安装。

在途Task/Delivery没有状态或数据迁移，固定B、scope、plan、selection和历史副作用保持。查询可重跑，丢失语义output仍回原producer，过期pass不升级。旧Task维护阻塞不授权手工覆盖受管副本或批量迁移历史。本批没有数据库、服务部署或外部发布恢复协议。

## 8. 验证设计

采用quality-guidelines的Test And Validation Value。先验证最接近行为的公开入口，再验证实际consumer、native提取、受管安装；仅为具体残余风险补实验。复用适用现有覆盖，不用声明副本或行数比较证明行为。

| 验证 | 要求/入口与输入 | 独立观察与边界 |
| --- | --- | --- |
| V1 查询回归 | R1/2/5、AC1；runtime测试调用真实wrapper，覆盖Skill、conditional workflow、stop、instruction-only合法出口和无exit调用 | 合同与真实Interface/目标正文一致，consumer能按原schema准备输入；无全图/私有内容，无exit保持。查询不证明下游pass。 |
| V2 错误/演进 | R1/2/5、AC1；isolated source/installed fixture的unknown、多exit参数、正常漏映射/重复声明、缺引用/matching drift，以及单一权威和Interface的合法映射演进 | 错误非零且无consumer；合法演进后同入口自然返回新consumer。fixture模拟普通更新遗漏，不测试人为伪造/攻击。 |
| V3 native提取 | R3、AC2；真实get_context phase/step/continuation及原native integration | Phase Index不夹带全图/历史详情；当前步骤/唯一continuation的必要约束、原owner及恢复定位可用。语义审核必要性，不设长度阈值。 |
| V4 维护可达 | R4、AC2；正常识别入口、原legacy Skill及完整references | 原支持家族、转换、控制退役和历史恢复的准确来源可取；普通路径只转交。静态可达不证明转换实际执行。 |
| V5 reader/分发 | R5、AC3；workflow_facts、source/installed snapshot、matching `.new` preview定向用例，原tools更新、installed validator、dogfood drift及受影响平台 | 同一图被读取，preview不用旧installed引用；匹配采用与Task/session保留。只覆盖受影响reapply/sidecar，不执行完整矩阵。 |
| V6 实际AI消费 | R2/3/4/5、AC1/2/3；更新安装后经原context入口取当前步骤，查询真实出口并加载consumer；普通接续与实际维护读取各一条 | 观察必要内容及原owner接续/stop；正常入口不要求无关全表/历史。维护只读不执行未授权转换。与source/installed证据分开，不宣称所有平台或固定成本降幅。 |

V1–V3是长期回归；V4/V6是本批语义和行为观察。已有discovery/native测试可复用，缺口为出口投影、reference consumer及正常加载。设施失败先限定复现并报告缺口；证据充分后停止追加，不扩展为评测框架或Release矩阵。

## 9. Canonical 引用、本轮差额与实际未决项

requirement/behavior为live #792及整体PRD；design为canonical workflow、原Interfaces及ADR-035；test为runtime/native integration及受影响验证说明；Architecture为当前baseline/constitution/change contract。差额仅为加载组织、查询和受管采用，原阶段及AI owner保持。

本目录 `architecture-contribution.md` 是真实隔离贡献，`adr-step-context.md` 是必要新决策候选。完整实现及隔离知识候选通过candidate Check后，由原Architecture/RDT owner在final_integration晋升，再重建最终候选和Check。规划不写共享README/index/manifest，不预称promoted。拟晋升目标与实际时点见implement §6，最终位置由原owner核live authority。

当前无必要需求、技术选择或接口未决项。实现/验证尚未执行，没有installed/native Agent全链、性能或成本结论。Wording、final Architecture、Approval及Phase1当前方案接受仍是独立边界。
