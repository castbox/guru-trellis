# D1 独立审查执行条件与恢复设计

## 1. 设计目标、需求承接与内容基线

本批承接PRD的D1-R01..06及D1-AC01..06，目标是让独立审查在声明权限内完成，失败提前且可定位，同候选沿原结果恢复。Task整体范围见../../prd.md，不改业务项目。

内容基线B与Planning H0均为63e71ffd72300dee4f5bfdc030c2a5f342b97f32，来自本Task创建采用的main固定Git对象；PR目标仍是main，实施完成后另取真实H，不从浮动origin重选B。独立candidate_assessment实际返回baseline_current / architecture_impact / target_native，baseline=guru-trellis-architecture、constitution=guru-trellis-design-constitution-v1；decision_refs为ADR-POSTCOMMIT-INDEPENDENT-REVIEW与ADR-KNOWLEDGE-NAVIGATION-ISOLATION。此结果不是final_plan或实现通过。

## 2. 当前系统、边界与目标差额

现session位于Git common-dir/trellis/sessions，linked checkout默认写范围不能据此覆盖。Bind adapter将projection读取、既有session读取及写入放同try；底层官方write_json可能只返回False，errno已丢失。Review原record/check/invoke使用同candidate checkpoint，顺序记录check和full_review，官方Task writer单写task.json。现有双槽恢复、公共结果恢复、同reviewer续审与工程事实适用性规则不重做。

D1无前序交付。本批在原Review package增加一个实际供caller使用的执行条件事实查询；Architecture/Review原入口在必要工程合同后、昂贵authority前使用它，原独立语义读取和正式调用仍在后。Bind按真实操作输出脱敏诊断。知识导航沿用现current-knowledge，不对后端大README做本地patch，不新增第二writer。

## 3. 来源设计处置（唯一）

| 来源/承诺 | 处置与落点 | 理由/影响 |
| --- | --- | --- |
| Issue929六项结果与声明候选只读/最小元数据 | retain；第4..8节 | 必须走到真实正式结果，probe不是验收终态 |
| Issue候选reviewer/writer拆分 | 本批不采用；第4/7节 | 新writer/结果交接不是修复写集遗漏所必需，原双槽/恢复已有；无公共结果模型迁移 |
| Architecture independent assessment：fresh、authority-first | retain；第6节 | 前置能力事实不读Task叙述、不审候选，不替代独立判断；design_facts是合法对象 |
| Review单次独立check/full_review及predecessor/恢复 | retain；第6/7节 | 不引入第二门禁、状态机或恢复ledger |
| 官方session_storage/io API及namespace归属 | retain；第4/5节 | 只消费公开位置/读写API，不改上游或复制存储；丢失errno保未知 |
| current-knowledge/#711导航/历史职责 | retain；第4节 | 已有完整定义直接复用，必要历史按影响读，完整authority不压缩/剪枝 |

## 4. 模块、职责与设计取舍

1. 原guru-review-branch拥有确定性执行条件查询，拟新增scripts/inspect-review-execution.sh、runtime/execution_facts.py及对应commands.json/interface声明。它不是新Skill或semantic gate。caller输入精确TaskRef/DeliveryKey、实际purpose与必要固定commits；查询使用原公开parser、live Git/官方session位置API取得事实，不选择Task/Delivery、不修改正式记录、不授予执行资格。Architecture/Review原AI owner按当前职责消费事实，决定修正执行环境或沿原blocked/re-entry。不得由脚本根据关键词、阈值或成功数产生pass/route。
2. 查询区分planning assessment与committed review的实际写需求。planning必须另带实际planning_purpose。candidate_assessment在有真实context时沿原绑定/选择职责核session写集，confirmed no-context保持原显式对象语义。final_plan严格保留ADR-EXPLICIT-REVIEW-OBJECT：完整显式对象只读校验，合法已有选择复用；无绑定/选择不要求恢复，不探测session/Task/checkpoint写能力，不以有context推导写需求。不同选择、损坏绑定或真实冲突仍由原owner处理。branch_review才需要完整session、Task JSON父目录及原ignored checkpoint写集，不能只检.git session。固定commit可读、Task/Delivery可读/匹配与实际目录操作分别报告，不把一个目录成功推成整链成功。
3. 写能力由显式probe操作建立：在所需目录内创建唯一临时文件，写入固定无敏感内容，rename、删除；需要缺失的目标目录时仅创建该次明确需要的目录，记录本次新建项，结束时只清理本次空项。已有文件/目录和正式session/task.json/checkpoint不写。失败保首个实际操作、脱敏location、exception_class、可取得errno；清理失败也如实报告，不伪报无残留。probe是短生命周期事实，不落证明文件/授权信息。路径和已有对象沿正常public/path边界校验，不新增攻击/竞态加固。
4. 实际正常写集：common-dir/trellis/sessions；Task目录内task.json及官方JSON writer同目录temp；checkout/.trellis/.runtime/guru-team/owner-checkpoints/<task-dir-name>/<delivery UUID>/review-gate.json；原允许临时目录内必要call-local carrier。源码/测试/文档保持职责只读，复核固定候选与工作区变化；无Git refs、别的Task或workspace journal写入。CLI workspace-write仅补common-dir中的必要目录，不能默认放开整个.git或danger-full-access。最终以实际正式journey证明完整职责，而非只probe。
5. session_adapter.py增加最小内部失败信息，分别在projection读取、既有record读取、write_record、post-write reread边界捕获。原Bind runtime消费内部信息输出stderr JSON。公共exit/reason_code/reason_refs保持，原语义判定及状态不改变。通过原异常链取得errno；官方bool失败或无cause时errno未知，禁止重试探测来猜原失败。输出不含原exception message、context key、payload或本机用户名；location用<git-common-dir>等标签和稳定相对片段。
6. 原Architecture independent entry明确actual prelude检查及允许的candidate对象，已派发generic/CLI直接执行同职责；只在实际不满足独立性或未执行/unfinished时走原blocked/re-entry。干净受支持载体按真实能力选择，不新增模型黑名单或通用fallback框架。无反馈核本次原句柄、阶段事件、实际阻塞/结果，不把PID/存活/无输出视作pass；不反复等待或循环新开。独立current reviewer可续审后继/最终计划，保留真实可见正文，不用父read marker。
7. authority/历史采用指引放原Architecture合同、preset/workflow README及知识引用处；复用current-knowledge/#711完整单元发现与根入口职责。其他Task历史pass不代表当前pass，也不一律是污染。本批不创建缓存、切片、已读证明、第二导航或共享登记。

## 5. 接口与数据

新增事实查询是原package的标量CLI，参数固定为--root、--task、--delivery-key、--purpose（planning或branch_review）及--probe-writes；planning必须提供--planning-purpose（candidate_assessment或final_plan），branch_review不接受该参数并必须提供--base-ref/--head-ref。planning只观察当前HEAD及显式对象。--delivery-key接受inline JSON或原声明stdin/regular file载体；不得猜选切片。未传--probe-writes只报告必要对象/位置及未探测状态，不能据此宣称写能力已验证。不增加全optional总artifact。purpose与planning_purpose只定位caller已确定的原职责，不判业务route。final_plan无正式写职责，即使传--probe-writes也不得执行任何写probe，只报告原显式对象关系与读取事实；不生成not_probed写项来暗示必要写权限。candidate_assessment按原context条件确定是否有绑定写职责。

stdout遵循既有intermediate receipt语义；新增execution-facts-output-1.0输出schema只约束result.checks中的必要操作事实。available行包含operation、脱敏location与status；failed行另含exception_class与errno（可得整数或未知null）；未显式探测的写行标not_probed。没有passed、approved、授权、reviewer身份、digest链或语义route字段。caller逐项读取并判断，事实用后丢弃，不缓存作为未来权限保证。错误目录/只读目录/缺对象是实际错误；unknown errno保持null/明确未知，不编造底层原因。

Bind stdout保持现有公共JSON形状；诊断仅通过stderr交当前caller，字段只为定位原owner操作。兼容说明MIGRATION-929明确新增query与stderr的适用版本、旧caller可忽略stderr、原code的跨操作含义及完整安装采用要求。无Task/session schema迁移、无新增GateResult或writer。

## 6. 状态、顺序、正常与失败流程

读取必要最小工程合同→核actual prelude、明确对象和目的→查询执行条件/必要probe→原AI判断是否具备执行条件→完整authority-first读取→按实际职责接续：candidate_assessment/branch_review保留原Identity/Ensure/Bind/Selection；final_plan按ADR-EXPLICIT-REVIEW-OBJECT只读验证显式对象，合法已有选择复用、缺失绑定/选择不写入且不恢复，不同选择/损坏/真实冲突回原owner→真实独立候选/完整diff及消费者判断→原recorder/checker/invoke。

预检失败仅说明尚不能执行，给实际操作与原能力/权限owner；不会进入大规模读取或生成semantic pass。支持条件修正后同对象重入。正式操作仍各自校验当前事实并处理真实失败；probe不是未来写成功承诺，不增加TOCTOU协议。final_plan的session不可写不会自行阻塞：只要原显式对象/关系可读且有效，即可继续独立判断；这个例外不扩展到Author/Approval/Activation或其他stage。

Review通过时原顺序check→full_review(predecessor=check)不变。中途失败保留原同candidate checkpoint，重入读取公共已写结果并只补缺步；checkpoint退休后从原public results恢复lost stdout。覆盖不完整必须补实际审查，不能空pass。合规同reviewer优先接续，真实污染/coverage丢失按原owner处理，工程命令仅补失效/缺失的部分。

## 7. 恢复、兼容、迁移与集成

保留现profile、typed exits、结果writer及旧错误码。新增public companion command遵循当前Interface和commands.json注册，不改变已有输入语义；匹配source/workflow/preset一起采用，禁止运行副本热补。旧完整provider的在途操作先按其原合同完成/恢复，再由原tools owner更新；当前Task/session/peer受原preservation校验。

新方法采用后，旧“必须长authority之后才发现能力不足”的顺序直接退出，但authority-first语义顺序不退。已有合法session/选择复用；不同选择/真实损坏/阶段冲突保原诊断，不覆盖。无新的持久preflight状态、独立pass、dual-read或第二恢复机制。

新增诊断不追溯改写历史。source侧临时会话全文不可读、native额外委托注入具体环节和嵌套worker底因仍未知；只在Guru可修的隔离检查/直接执行/原出口上承接，不宣称修复平台本身。

## 8. 验证设计

| 验证 | 入口/输入与断言 | 边界 |
| --- | --- | --- |
| V1→AC01/02 | query真实linked worktree，session额外范围缺失/具备，对应目录真实临时操作、固定对象读取；断言失败operation/errno及无正式记录变化，probe成功仍无gate；另以有context、无绑定/选择、完整final_plan对象和不可写session目录证明只读例外保持，且没有写probe/Bind/Selection；不同合法选择和真实损坏保持原错误 | module/CLI证明能力；必须再走V3 |
| V2→AC06 | 原bind_session及Bind public wrapper，分别使projection/旧record读/真正write/读回发生普通OSError/内容错误；核稳定stdout和脱敏stderr、cause可取得/已丢失两种errno语义 | 定向mock只覆盖该异常分层，不冒充sandbox |
| V3→AC02/03 | 采用现postcommit fixture及normal owners的最小可丢弃Task/Delivery/B..H准备，真实fresh Agent从正常入口完成正式独立判断与原双槽投影；必要最小写集配置，候选内容前后不变 | 不手写semantic pass；真实完整结果是验收终态。无设施则未验证 |
| V4→AC03 | 原test_postcommit_review.py已有合法setup在第一槽完成后写失败重入、以及checkpoint退休loststdout，观察同结果/前驱、仅缺步写入；同reviewer/适用工程事实采用 | 复用现覆盖，仅补新输入真实差额；不重复完整审查或整套测试 |
| V5→AC04/05 | 正常带其他Task历史pass的authority与当前design对象，真实generic/CLI直接执行，观察无递归；代表未执行/缺结果时caller有界定位并走原出口 | 复用本轮真实入口轨迹；不能把native污染或prompt误读轮记通过，也不宣称通用成本比例 |
| V6→全AC | source/installed/声明平台投影、同worktree tools-only采用/reapply/drift/sidecars及Task/session保持 | 最小受影响验证；无完整多平台安装/Release矩阵 |

已有实际观察：Codex0.172.0受控sandbox同sessions目录仅workspace写失败PermissionError errno1，额外精确目录后唯一temp成功并删除；真实fresh CLI在同范围完成Identity/Ensure/Bind/Selection并独立candidate_assessment。它只证明session和候选阶段，不证明V3完整Branch Review或修复后的入口。原native fork_context=false仍收到委托的报告、CLI误把合法design_facts当叙述的停止以及修正后的独立读取均保留其实际含义，不冒充已修复。

V5评估入口方法对Agent行为的差异时，按Real Agent method comparison执行最小有界对照：使用相同普通审查请求、固定对象及含其他Task历史的authority，在独立中性副本分别采用固定B原方法和本批方法。执行前固定判据为执行条件发现相对大规模读取的先后、合法design对象/历史处理、是否递归及原正式结果；保持模型/设置尽量相同，执行者不接收判据、期望答案或优选标签。评价方先在未知方法映射下读原输出和工具记录作判断，再揭示映射核对。保留首次失败/环境差异，观察足以回答该场景即停；不以本轮前期不同prompt轨迹冒充受控对照，也不推出普遍成本百分比。

按Test And Validation Value选择最小充分层次，已有有效证据采用；仅为真实剩余问题追加实验，证据充分即停止，不要求惯例红绿回退或固定运行轮数。

## 9. Canonical引用、本轮差额与未决项

必要引用为PRD第7节、原Review/Architecture合同、session_adapter及原Review runtime、current-knowledge、preset ownership/installer和官方自定义workflow/spec文档。本批使用官方Markdown扩展面，脚本只承载上述事实。根workflow若不需要新跨Skill转移则保留，step-local行为只改原Skill，不复制到launcher。

真实隔离Architecture贡献位于docs/architecture/contributions/929-review-execution.md，完整拟写为其proposed目录下04-integrations/review-execution.md；不写共享根/ownership/system索引，不新增ADR（原两项decision已覆盖writer/导航）。RDT差额由原maintenance owner在提交前整合真实相关定义，Architecture原owner写新完整单元并readback，均为integrated_pending_review，提交后同一次独立Review审核before/after。

产品范围无待决选择；具体probe父目录创建/清理和CLI参数须在实现中按本合同完整固定，若需扩大写集/公共数据/owner则回原Author/Architecture。完整Review与安装证据尚未获得，不预填通过。
