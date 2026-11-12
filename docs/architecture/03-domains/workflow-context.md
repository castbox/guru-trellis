# 当前步骤上下文与出口查询

Identity：`ARCH-CONTEXT-001`；aliases：step-context、exit discovery、routing reference、
按当前出口查询、流程上下文按步骤加载。原 semantic owner：`guru-maintain-architecture-baseline`。
状态：current。适用来源是[Issue #792](https://github.com/castbox/guru-trellis/issues/792)与固定 before Git
`05a16a5989669ca216d8ba34b9b419776410f04d`。原 Architecture owner 在 #792 D1 的完整候选 Check 后，
通过 final_integration 整合并读回本单元。知识晋升不证明最终 Check、committed Review、Task 完成或环境效果。

## 1. 责任与适用范围

本单元拥有 Guru 当前步骤上下文的加载组织、出口查询及其分发边界。真实 caller 是
已经取得一个原 Skill 合法 typed exit 的 AI，或需要定位当前 Task/Delivery 未完义务的
start/continue/resume caller。它不拥有 Task/Delivery 身份、selection、阶段转换或 semantic pass。
这些职责保留在原 workflow、原 Skill 与官方模型，具体续接决定沿
[ADR-035](../adr/035-current-continuation-scope-routing.md)。

本次直接承接 R792-01..05/BEH792；RDT 的完整要求位于
[生命周期 Requirements](../../requirements/current/task-delivery-lifecycle.md)，设计关系为
[生命周期 Design](../../design/current/task-delivery-lifecycle.md)的 D792-01..04/CON792，
验证关系为 [生命周期 Test](../../test/current/task-delivery-lifecycle.md)的 T792-01..06。
三层 RDT 与本单元分别由各原 owner 维护；完整最终候选核验各自实际晋升及关系，不以单方写入推断另一方已生效。
决定理由见 [ADR-STEP-CONTEXT-LOADING](../adr/step-context-loading.md)；来源归属见
[#792 贡献](../contributions/792-step-context.md)。这些关系不要求修改共享 root/ownership/index。

## 2. 唯一权威与确定性读取

全局 workflow 拥有阶段顺序、mandatory invocation、typed exit 的唯一 consumer、
workflow target 及 stop 条件。其 `guru-routing-reference` 注释只指向一个
extension-relative `references/routing.md`。source 扩展根是
`trellis/workflows/guru-team`，installed 扩展根是 `.trellis/guru-team`，不得从另一个
provider 猜路径。完整标记及 router/stop 正文只在该受管 reference 中维护。

各 Skill 的 Interface 保持原 public input/output、consumer input、projection 和
entry preconditions。原图 validator 校验 active registry、mandatory 标记、exit/consumer
及 target 一致性。reference 缺失、声明重复、inline 与 reference 混用、target kind 或
Interface 不一致时，停止依赖调用。正常新 runtime 为 reference-only；不读取旧 inline，
不搜索备用路径，不以缓存、摘要或派生 digest 建立另一流程 authority。

`installed.py` 的共用 reference reader 承接上述客观读取。它和 discovery 不解释
Markdown 条件、不评估 scope/充分性、不作 profile 意图判断，不代替原 AI owner。

## 3. 出口查询的正常路径与错误

原 `discover-skill-contract` 的输入仍是实际 root、mode 和 active stable Skill id；
提供一个 `--exit` 才进入当前出口查询。caller 必须持有原 owner 的实际出口，不能从
phase 或文件存在编造。省略 exit 时仍执行原 Skill public contract discovery，不把它
升级为下一步通过。

出口查询先校验 matching provider、Interface 和完整图，再返回该出口的唯一 consumer、
producer output contract、consumer input/projection 及必要 entry。Skill consumer 的 entry
定位原 SKILL.md 和前置/input/invocation；workflow/stop consumer 的 entry 定位原 target
正文。producer output 的相对合同路径仍以原 `contract_root` 解释。JSON schema 类型的
consumer contract 另提供 repo-relative `consumer_schema_locator`，按原 package 优先、
shared consumers 根其次的规则定位实际 schema；AI 直接读取该 locator，不把 shared
consumer schema 拼到 producer package。原 `consumer_input` 和 producer `contract_root`
保持，Markdown consumer 不生成该 JSON schema locator。此定位是原合同的确定性可读投影，
不产生另一份 schema authority，也不要求 caller 理解 private runtime。查询只提供当前
出口的直接消费内容，不返回整图、全 registry、历史扫描或 private checkpoint。

AI 按原 projection 准备参数，并显式加载、调用原 stable Skill。conditional router 的
全部相关原分支仍可获得；AI 根据实际输入执行，脚本不替 AI 选择。stop consumer 报告
原原因并结束自动链。查询成功仅证明客观合同可取得，不证明入口前置满足或下游 pass。

unknown Skill/exit、多个 exit 参数、重复/未映射合同、缺 reference、kind mismatch、
graph/Interface mismatch 或 installed drift 返回非零与原 code/field_path/remediation，
没有成功空 consumer。普通输入错误修正输入后重查；matching 缺口回原 tools owner；
真实正文/Interface 错误回各自原 writer。丢失语义结果仍由原 producer 恢复，不能用查询补造。

## 4. 正常上下文与维护上下文

正常 `get_context.py --mode phase` 读取相邻 Phase Index 与 Phase 1 之间的简短内容，
取得全局约束和当前入口；`--mode phase --step <step>` 读取原步骤。唯一
`[trellis-continuation]` 块位于该 Phase Index 提取区间外，负责实际当前会话、公共
Task/Delivery availability、当前步骤和原 producer 恢复定位。

接收会话检查、完整 phase/recovery 矩阵保留在同一 workflow 的按需章节；caller 只在
当前条件命中时加载其原完整合同。公共 phase 仍只是 availability，不是 Planning、
Check、Review、readiness 或 Completion pass。正常入口不要求加载全量 router/stop
和历史恢复详情，但适用全局约束、mandatory 调用及未知结果停止原则保持。

正常路径识别真实 legacy 条件后，转交原 `guru-maintain-legacy-task`、tools 或
upgrade owner；实际维护才加载 `.trellis/guru-team/references/legacy.md` 及原 package
references。原 family、conversion、control-retirement、manual archive resume、historical
closeout 的支持/停止条件和准确 source pin 保持。不得按版本号一刀切、批量转换无关
Task、改历史归档，或把旧 Finalizer/历史 gate 转成当前 pass。原维护算法不复制到本单元。

## 5. Reader、分发与历史观察

正常 source 图校验、installed graph validator 和出口查询使用同一 reference reader。compatibility
verifier 的 source snapshot、installed snapshot 和新 workflow `.new` preview 也读取
对应 matching reference；本地 candidate preview 显式使用 source 扩展根，不能误读旧
installed asset。workflow marketplace 只更新 workflow 不代表完整 preset 已采用。

verifier 仅对显式 before-snapshot 保留原 inline 标记的只读观察。它服务已存在的历史
before 输入，不授予新 runtime 或当前 installed validation 旧格式资格。该分支由
verifier owner 维护；当受支持 before 样本不再含 inline 时，删除分支及对应定向用例。
这不是新的 legacy runtime 或 fallback，也不扩大本批验证为完整多平台矩阵。

原 preset 声明并分发 routing/legacy 两个 reference；原 tools/upgrade owner 同步完整
matching workflow、runtime、packages 和实际受影响平台/spec，保留 Task/session、用户
内容、mode 及原 sidecar 处置。工具更新前旧安装继续用原完整 provider，更新后正常
runtime 只使用 reference。没有 Task/Delivery 状态或数据迁移，没有新增 query store、
长期位置缓存、ledger、用户授权字段、wrapper Skill 或跨阶段 DTO。

## 6. 选择、总成本与重评条件

直接路径是“原出口→既有查询→原 consumer”。复用现有 wrapper、Interface、reader、
native 提取和 preset 使职责留在原位置；单一 reference 避免手工同步第二映射。
脚本执行条件 router、额外 wrapper、通用 include 和持久缓存均无当前必要 consumer，
不属于本机制。原 qualifier 适用条件沿
[ARCH-DOM-QUALIFIER-APPLICABILITY](qualifier-applicability.md)，本单元不改 #793。

本选择降低的是正常 AI 被要求读取无关全表/历史的范围。查询仍付出完整 matching 图
校验与一次显式命令的 I/O/顺序成本；维护者须同步真实 reader、引用和受管资产。
无结果缓存意味着丢失查询时重查，语义结果则回原 producer。不能将文件变短、查询
成功或分发一致当作端到端效能证明，也没有固定成本降幅或性能验收。

若实际消费者不能从一次查询定位必要入口、native 提取边界变化、原 Interface/图职责
变化、真实历史输入退出，或观察发现成本被转移到重复查询/其他 owner，原 Architecture
及直接责任 owner 重评必要性与更直接路径。真实需求或兼容范围变化回原 Clarify/Planning；
源码查询错误回原实现/质量 owner，不自动增加兼容、状态、缓存或全局升级门禁。

## 7. 验证与当前知识采用

本批验证分别观察公开 source/installed 查询、普通错误及合法映射演进、原生
phase/step/continuation、legacy 合同可达、matching reader/preview/分发，以及实际 AI
查询后加载 consumer。结构检查、source 行为、installed 投影与实际 Agent 行为各自
只能证明其观察层。结果与未验证范围见
[#792 唯一 Test](../../requirements-design-test-contributions/792-step-context/test.md)。
本单元不预填当前 Check、Review、安装、生产、费用或 Release pass。

#792当时的晋升记录采用候选Check后回implementing再整合的顺序；该观察保留历史含义。
当前执行顺序由[ADR-POSTCOMMIT-INDEPENDENT-REVIEW](../adr/postcommit-independent-review.md)及项目change contract拥有：
批准Planning、完整实施和工程验证后，原Architecture/RDT owners提交前核live expected-current、整合并readback，
不要求candidate Check或提交前独立实施Architecture pass。TaskCommit包含全部after，再进入同次独立committed
Architecture/Check/full Review。整合仅为integrated_pending_review；晋升、Task完成和环境采用分别判断。

[MIGRATION-792](../../../trellis/presets/guru-team/MIGRATION-792.md)拥有具体 matching
采用/普通恢复说明；旧完整 Git、ADR 与原始观察保持历史含义。本主题经上述原晋升合同形成当前完整定义。原隔离拟写保留为来源，不是第二 current；后续质量与交付状态仍从原公共结果读取。


## 8. 资格确认共享合同与AI补写（#811）

本节来源为[Issue #811](https://github.com/castbox/guru-trellis/issues/811)，before为
ca0b21f0dfc754a6979f919be14deee696719a4b；本节由原 Architecture owner 在 #811 final_integration 整合并读回，
状态为 integrated_pending_review；独立 committed Review 尚待执行。
确认对象及scope/source职责由[ARCH-DOM-QUALIFIER-APPLICABILITY](qualifier-applicability.md#资格确认的原context接续811)拥有，
本节只维护同一原graph的共享接口表达、AI字段与确定性读取职责。

普通Interface1.10从普通1.8演进，承接context-current4的真实descriptor、consumer自有结构化call-local input和
按真实handoff_profile选择的authoring seed。1.9仍为Codex instruction-only，旧发布schema/example保字节。
Clarify refresh的skill_call_local_input只指向Sync注册Interface；原discovery从目标Interface的
call_local.public_input声明取得本包schema/example，不让producer指定另一schema，也不把return_identity当scalar。
Sync保原scalar CLI和deterministic语义；结构化确认输入通过其原call-local入口。

Sync baseline_ready的skill_input_authoring_seed以producer_output.handoff_profile唯一选中authoring_profiles。
pre_task seed为source_exit/profile/mode/continuation_id，原AI补change_input/clarify_profile，reviewed-plan另保source_locators；
context_request另从真实输出保return_identity，原AI补change_input。原synced固定pre_task authoring不变。
seed与AI字段不交叠，补写后的完整input经Discovery schema校验；base_current transition仍单独承接。
缺失、未知或重复profile保原错误，不改选其他profile。普通pre_task不制造identity，confirmation identity不由AI重建。
这是固定声明的客观解析；检索充分性、authority、scope和原typed route仍由原AI owner判断。

registry1.5、production manifest6/current alias、extension public_api、discovery/validator、installed公开投影和installer
shared schema inventory成套切换；公开投影包含call-local及selected authoring/alternate示例。
ordinary eval run5从run2有限演进以消费普通1.10，直接runner/receipt reader同步，qualification专用run3/4保持。
production submanifest不成为完整workflow selector。精确版本、旧pending重装、固定provider恢复与matching采用由
[MIGRATION-811](../../../trellis/presets/guru-team/MIGRATION-811.md)拥有。

原graph/projection tests和source/installed discovery分别验证context4、目标call-local声明及两profile的完整consumer输入；
ordinary smoke须调用新Interface包原wrapper并消费实际receipt。只更新白名单或比较版本文本不证明这些行为。
原tools owner核精确source/target/write set后采用并验证目标自身；source成功不等于installed或独立公共链接续成功。
本项不以特定发布Task为验收依赖；独立合法Task/Delivery场景使用真实producer和正式出口，fixture语义输入与实际产物分层。
原Check按当前验收判断充分性，不新增实际Agent或远端业务证明前置。
本扩展无新resolver、wrapper Skill、通用表达式、状态或授权存储，未验证层保持其原边界。
