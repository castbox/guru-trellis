# #713 D1：原公开执行边界收敛贡献

## 身份、authority与真实起点

TaskId=`713-public-execution-contracts`，generation=0，DeliveryId=`a163bca1-b051-4f04-b5aa-2727a4e7abb2`。固定B=`8378b8d500a974ae1c01bd0571f30149f56541b0`；完整方案在同目录design，执行/验证安排在implement。此贡献是Planning的实际方案，不是实施或安装通过记录。

当前 accepted_scope=`sha256:bacc8a5f1a574dd76dc4274dece5bfd14cd27d2ccdef5942046a93683d6667ff`。本轮只收缩验证义务：C1–C5取消，AC5不计通过，AC6–AC8按当前正文缩减，AC9只复用仍匹配的实绩。S1–S5生产职责、AC1–AC4、43 packages / 127 commands / 180 profiles支持声明和最终质量链保持；取消项不转成通过，也不生成新Delivery或必需follow-up。

当前authority为 `docs/architecture/README.md` 的 `guru-trellis-architecture`、`00-foundation/design-constitution.md` 的 `guru-trellis-design-constitution-v1`、`06-governance/change-contract.md` 的 `guru-trellis-architecture-change-contract-v1`。candidate_assessment的真实结果为architecture_impact/target_native；final_plan另由同一独立Architecture owner在Wording后判断。

before：creation公开schema未完整引用现有source域；Completion当前/旧导航分裂；workflow直接使用内部投影方法，而公开candidate只输出content_ref；错误恢复有Inspect runtime；eval以精确路径/事实计算补足模型。after计划：原Skill提供适用profile的完整调用合同，原deterministic owner公开完整Candidate构造，原operation执行阶段写入，eval只保留环境/运输/观测及合法consumer fixtures。需求、证据充分性和route仍归AI。

## 机制、原owner与直接consumer

原Author/implementation step负责选择范围/B/paths及阶段，原 `runtime/delivery_projection` 提供只读 `candidate_cli.py`，通过已安装 `construct-delivery-candidate.sh` 返回既有Candidate。桥接只服务当前Git pull_request Delivery，前置是原Identity/Ensure核实的Git checkout、C4与当前Delivery。它调用原content_base/candidate，优先同Delivery固定B，再用实际前序delivered或显式development baseline/唯一merge-base；不fetch、不保存新状态。输入Task/key来自原Identity/Ensure/Selection。原Delivery begin-check/rework消费完整operation，其owner/phase和freshness不被桥接替代。上游既有candidate --kind git_free及其consumer保持原边界，不进入新桥接，也不新增无Git Delivery。

原Skill/Interface/commands/help/schema/example单写各自profile导航。共享task-creation source定义继续拥有issue/no_issue，不引入relation alias或第二来源。错误owner返回具体合同/字段/stale/内部故障范围，恢复归原producer。recorder给私有字段，AI只作者语义；公共producer token原样承接。eval改用同一公开能力，不重写算法；正常native从生产入口发现合同，不由host给当前答案。

## Implementation discovery 的原边界补充

此前原 Architecture 在 implementation_discovery 返回 contract_incomplete，缺项是本节与完整拟晋升单元对实际公开 handoff 的具体承接。本节保留当时补齐的原贡献及其边界；该历史结果不充当本轮 Architecture current 结果。

C4 的既有 discovery 在 already_established 时，从原 resolver.binding 公开最小 binding_ref（TaskId、generation、binding_revision），供 Closure 直接消费。原 resolver 仍是唯一事实 authority；typed binding_established、建立/ownership/recover 行为和持久状态不变。未建立时不提供引用，不从 Task metadata、路径或默认0推断 revision。

原 Check 允许无 scope 变化的 planning 遗漏。保留旧非空 proposal_refs 分支；仅 reapprove_plan/空 scope_decisions 增加 proposal_refs:[] 与 revision_actions。动作直接复制原 Check AI 在既有 reason 写出的具体修订要求，原 workflow 薄投影到 Author delivery_approval_revision。11 字段 authoring、完整6.0结果、原 typed exit和原 Author input不变，不为技术返工制造scope proposal。原 Check 先构造并校验完整 output，再执行其原 rework/record_gate；该顺序只校验已形成的 AI 结果，不替代判断。

原 legacy finalize 明确现有 REVIEW envelope 与两类 profile；observations 取原 observe 的 receipt.result.result。原 owner 在重执行 target-native/next-owner 前诊断普通缺字段，保留额外caller字段、两层receipt与原观察/route/identity比较。Planning freshness只公开原JSON/文件bytes的精确格式，不修改算法或由eval提供当前答案。

上述新增承接按 trellis/presets/guru-team/MIGRATION-713.md 成套采用。C4与Closure导航、Check output/consumer/router/Author导航和legacy原合同/示例/执行器必须匹配。旧完整安装保持原合同或沿原owner切换；同operation恢复不换ref、不重写旧失败、不重放已完成transition。无新command、Skill、状态或ADR。证据缺口按当前适用AC判断；已取消的扩展native不再构成验收义务，其失败与未知仍保留原结论。

## 载体与 Discovery 说明补充

这部分是同一 accepted scope 内待原 Architecture 判断的实施方案。Publication 的公共 preview/record/check/execute/invoke 在原 public 参数边界使用既有 runtime.io.read_json，一次解析 JSON 参数后交原 schema/plan/执行流程。原 owner preview/invoke 只做必要的已解析对象薄承接，同时保留原文件调用；不把私有 Task、transaction、Gate 或 recovery 的 file reader 改成通用输入解析器。stdin 不为 profile 选择和正式调用反复消费。AI 判断、原确认边界、事务、输出和恢复不变。

六个原 legacy intermediate run 的初次公开输入读取复用同一既有 reader。Publish/Merge/Finish 在固定 B 已明确 inline/file/stdin，修复履行该承诺；Approval/Check/Branch Review 原来只声明 JSON，本次以明确 additive 表示收敛支持这三种载体，不追认旧 inline 成功。保留原文件优先、相对路径、symlink 文件和 stdin 成功域；schema、execute、正式 retirement loader 和私有 plan/recovery 读取不变。Maintain legacy 自身只说明现有 file/stdin，不扩大通用 read 的域。没有新 helper、flag、command、Skill 或状态。

Discovery 的原执行 AI 在语义资料读取前核对 Sync transition 与原 Git 公开事实；record/check 中原 observer 后续重读并派生 base_observation。文案应清楚区分这两项职责，不新增读前 observer command，不用未发生的 Gate 提前调用 recorder。无外部 Issue 的本地文本 draft 给出一个合法 source-capture 正向例，保留其它合法 capture、原 producer identity 和 issue_binding 语义，不规定唯一新 digest 投影。

MIGRATION-713 的拟补充条款为：公共 JSON 参数与私有文件引用分别由原边界读取；Publication 公共参数及六 legacy intermediate 的三载体行为与其声明成套采用。前三 legacy 恢复旧明示合同，后三为本次 additive 表示收敛，原业务 payload、旧文件/stdin、输出与同 owner 恢复保持。Maintain legacy 的 plan/review/private checkpoint 不被该修复扩大。Discovery 只明确既有 Git 前置和本地 draft 合法捕获例，不新增 pre-task artifact、observer wrapper、固定全链摘要或语义判断脚本。待本次原 Architecture 实际出口允许后，原 implementation writer 才把这段兼容说明纳入 canonical 迁移正文并改原 package。

## 九concerns与项目检查输入

| Concern | 适用性、理由、before/after及责任 |
| --- | --- |
| authority-binding | applicable；Planning3.0/Delivery1.0，candidate_assessment先于写方案，final_plan绑定当前design与实际贡献；非Planning仍沿5.0/Delivery3.0及原Check6.0，不能混用 |
| constitution-binding | applicable；原公开owner有当前consumer与真实能力差额，复用成熟CLI/官方扩展面，保留语义职责完整性、变化隔离和最小必要能力；不制造原则评分或第二authority |
| boundary-and-decision | applicable；ARCH-FND-002/004、D531-01/08、ADR-028与ADR-PHASE2-RECORDER-INPUT；唯一target_native，原缺口回原边界，既有范围算法及Check决定保持 |
| owner-and-single-writer | applicable；Author写方案，独立Architecture评估，原projection执行事实，RDT/Architecture各自最终晋升；eval无生产判断职责，shared-current不由Task并行写 |
| compatibility-and-exit | applicable；原candidate content_ref consumer和已声明旧profile保留既有语义，完整6.0结果consumer及历史控制恢复继续原合同；新入口不造dual-read，若成功语义变化先显式matching迁移 |
| gap-and-deviation | applicable；本批收敛R1–R4执行合同及R5中由生产入口承担的正常导航与事实能力。取消额外模型实证不证明这些行为已全面通过；不新增/重开Architecture GAP或宣称已关闭ARCH-GAP。若实施引出owner/GAP变化回原评估；原GAP生命周期不凭Planning删除 |
| parallel-scope | applicable；当前仅本Task/D1规划及必要原owner runtime；未来实现限本Task已选原模块和受管投影。禁止改业务#994、其它Task、shared journal或竞争shared-current |
| evidence-and-freshness | applicable；design当前字节供final_plan；真实实现后完整candidate/Check绑定。V1–V4、I1及当前缩减AC按适用范围承接；已有部分native、取消C1–C5和未验证边界分别报告，不新增运行。工程源码诊断及#710历史不充当新public-only通过 |
| review-and-promotion | applicable；真实贡献供独立final_plan；promotion_state只能是reviewed_candidate或原owner依法产生的reviewed_promoted。完整隔离拟写先经候选Check，再final_integration/readback与真实after最终质量链；不提前晋升 |

descriptor=`guru-trellis-architecture-convergence:repository:1`，check id/version=`guru-trellis-architecture-convergence/1`，result contract=`guru-project-architecture-check-result-2.0`。这些是原独立owner当前检查的输入引用；本贡献不预填其pass或公共出口。

## 拟晋升完整单元

目标是 `docs/architecture/04-integrations/distribution.md` 的新增完整小节，定位为“公开执行资料与原生产能力”。原Architecture writer在final_integration以真实实施/验证更新其事实与验证定位后才晋升；共享README、constitution、change-contract、owner与GAP定义不因本贡献自动变化。完整结果文件为 `architecture-proposed/docs/architecture/04-integrations/distribution.md`，逐字保留固定B的原单元前缀。该小节proposed正文如下，当前没有写入共享authority：

> ## 公开执行资料与原生产能力
>
> Guru业务Agent通过正式安装的workflow、Skill及其引用正文、Interface、命令help、profile schema/authoring示例和实际命令结果执行。Skill独占step-local调用合同，workflow只拥有全局顺序、mandatory invocation和typed exit consumer。当前profile、历史支持入口和实际输入载体必须明确，完整结果不能冒充正常authoring输入。
>
> 原implementation owner选择内容范围、固定development baseline和paths。原delivery_projection执行器在Git checkout、C4与当前pull_request Delivery前置下，公开构造既有Git Candidate所需的确定性事实，复用同Delivery固定B优先、实际前序交付与既有内容算法；原Delivery operation继续执行begin-check/rework。公开构造不新增scope/pass/route判断、持久状态或第二算法，不要求业务Agent导入Guru私有实现。上游既有git_free Candidate内容引用入口与其consumer保持原边界，不因桥接增加无Git Delivery支持。
>
> AI作者语义内容；原producer的公共身份原样承接；recorder计算其私有字段。Phase2语义authoring、完整6.0结果consumer与两类内容token按MIGRATION-710保持边界。完整exit/stdout/stderr先捕获，再按原合同消费receipt.result、checker receipt和唯一typed exit；运输或checker成功不能替代正式阶段结果。普通输入/stale回具体原合同与恢复入口，内部故障保留已确认范围交原维护owner。
>
> eval只在其声明边界建立合法历史前提或隔离环境、外部替身、路径映射、运输和观测。当前native语义前提由Agent实际产生；正常必需导航和事实能力来自生产owner，不能由adapter补充隐藏调用知识或私有身份。native验证范围由当前accepted scope规定；实际执行的案例在模型外比较预期出口，取消项不产生通过结论。源码诊断和修订后新run不改写原失败。
>
> canonical package/runtime/workflow/preset和声明平台沿完整matching安装与原tools owner成套采用。用户内容、Task/session、sidecar、mode、reapply和drift保持原合同；源修改不证明目标已采用。旧完整安装保持原合同或由原owner成套切换，不新增长期双parser。实际安装、Agent行为、受控外部provider、真实发布/部署及Release矩阵分别报告，不互相推定。

此单元沿既有决策解释执行承接，不引入新的Architecture API、owner或状态。它不预写当前native/安装结果；实施后原owner必须核对真实after与证据限制，缺必需结果不晋升为已验证事实。

## 兼容、ADR、验证与晋升

保留的真实consumer是原candidate stdout读取、当前/旧合法profile、#710完整结果checker/invoke/recovery、既有legacy control及Reactivate/maintenance。当前没有新兼容例外或运行时第二路径。无consumer的deprecated资产由原owner核实注册/外部依赖后在同批退出；不能只凭文件名或测试引用作删除判断。新成功语义变化须先回原兼容/Planning边界，不从本贡献获得额外授权。

本方案没有改变架构决策、single-writer、GAP生命周期或兼容退出，因此无需新ADR。若实际implementation改变其中任何一项，原Architecture owner重评并要求真实ADR candidate，不以本结论提前豁免。

后续实现/隔离拟写先入完整候选Check；原Check合法rework后，RDT与Architecture各自final_integration、readback，并绑定写前expected-current。真实after再candidate/begin-check、最终Architecture/Check、commit、完整committed Review/readiness。Planning仅提供reviewed_candidate，不提前写共享current，也不以contribution或checker成功替代semantic judgment。

当前验证沿design/implement的适用性与证据表执行，已有V1–V4、I1和安装实绩仅在仍匹配时复用。C1–C5已取消，不再补跑三族完整native、额外非等价family代表或R5完整method-loading，也不为这些验证重复准备环境、恢复安装或重装。候选及最终Check、完整committed Review/readiness、交付、Completion/Closure/Finish与fresh merge gate仍须实际完成。正式source-lock、完整Release矩阵、业务采用与生产效果仍未验证，不进入本项新增阻塞。当前适用AC的实际缺口仍阻止Task Completion；本贡献不证明完整Agent行为或根治已完成。
