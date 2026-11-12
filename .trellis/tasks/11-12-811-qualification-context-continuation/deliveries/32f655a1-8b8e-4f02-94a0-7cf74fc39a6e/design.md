# D1 资格确认 context 接续设计

## 1. 设计目标、需求承接与内容基线

本设计承接本批 PRD 的 D811-01..07、整体 R811-01..07 和 AC811-01..08。
目标是让两个真实 qualifier 的确认出口，经过原 Clarify 和原 Discovery，正式返回原 caller。
缺失 context、正常过期 context、Issue mutation 后的刷新都必须保留同一确认对象。

Task 为 `811-qualification-context-continuation` / gen0，D1 为
`32f655a1-8b8e-4f02-94a0-7cf74fc39a6e`。固定 development baseline B 与 Planning H0 均为
`ca0b21f0dfc754a6979f919be14deee696719a4b`，来源是 Intake 实际选定的 `origin/main`。
内容范围由原 Delivery candidate constructor 以 B、实际后续 H 和 owner 选定文件构造；PR target 为 `main`。
H0 不是最终实施 head，也不要求同步落后的 primary main。

阶段适用 authority 为 `docs/architecture/README.md`、`00-foundation/design-constitution.md`
及 `06-governance/change-contract.md`。独立 candidate 复评已通过原公开 invoke 返回
`baseline_current / architecture_impact / target_native`，决定 ref 为
`ADR-QUALIFICATION-CONTEXT-CONTINUATION`。本设计承接真实 mutation refresh 和 authority disposition
事实投影；候选通过不是最终规划或实施通过。

实施期发现原 Interface1.8 无法声明 context4，且 baseline_ready 的普通 profile selector
遗漏 Discovery 所需的 AI authoring 字段。原 Architecture 返回 contract_incomplete 后，同一 Delivery
已合法 rework 到 planning，整体 accepted scope 不变。本轮原 Author 的补充候选经真正
candidate_assessment 返回 baseline_current；以下第5.4节承接共享合同和直接 consumer 迁移。
原先的 Planning 接受不供本轮 Activation 复用。

本轮最新 live #811 将验收收敛为本项独立正常 Task/Delivery 公共链接续。原 Clarify 已发布新整体范围，
同 D1 已合法 rework 到 planning；新的独立 candidate_assessment 实际返回 baseline_current / architecture_impact / target_native。
本轮只刷新验收、依赖与追踪，保留下面的已实现接口机制及有效工程事实，不重做未变实现。

## 2. 当前系统、边界与目标差额

这是全量 D1，没有本 Task 的前序 Delivery。#812 的 explicit-task/key 校验已在 B 内，继续复用。

| 固定 B 的起点事实 | 本批差额及原位置 |
| --- | --- |
| 两 qualifier output 2.0 有候选、target、continuation、resume；Task/key 由原 caller 在调用期保留 | 在两个 `public-scope-confirmation-required-output-3.0.schema.json` 中仅为 Task-bound 分支投影已校验的 task_ref/key，供新的跨 Skill context consumer 使用；其余出口不变 |
| Clarify 两确认 input 1.0 不带 Task/key，invoke 拒绝确认的 needs_context，clear 走普通 target disposition | 两 input 2.0 和独立确认 clear 合同承接真实对象；缺失 bootstrap 正式 needs_context，确认 clear 不制造重复 Issue disposition；mutation disposition使用真实authority snapshot |
| Discovery context_request 2.0/ready5 只保旧四类；transition.target_locator 来自 live Issue | 新确认分支独立保留 Task target、return identity 与 authority_locator；旧四类保持原支持边界 |
| Clarify refresh2 不带返回对象，Sync read 固定 pre_task/stage0-current | 新 refresh3 经 Sync confirmation-refresh read 实际 baseline_ready2，继续原 Discovery context_request3，不退回 Intake |
| 普通 Interface1.8 不能声明 context4、Skill 结构化 call-local input 或 profile-selected authoring seed；1.9只属 Codex instruction-only | 新普通 Interface1.10承接这三项；registry、manifest、直接reader、installer和ordinary eval receipt同批迁移 |

改动 canonical packages、shared consumers/runtime、原 routing reference、受影响 overlay、文档与定向测试。
不新增 Skill、workflow exit、Task/Delivery 状态、qualification store、授权字段或另一流程图。
既有 sync executor 的 fetch/ff-only 行为不变；确认刷新只用 read，不要求 clean business worktree。

## 3. 来源设计处置（唯一）

| 来源/条款 | 原承诺 | 处置与具体落点 | 理由、影响与上游处置 |
| --- | --- | --- | --- |
| #811 要求1、3及验收 | 两类确认经过真实 producer，再 clear 回原 caller | retain：第5、6、8节 | 两 profile 分别验证，不能用单类或 fixture 输出替代 |
| 最新 #811 验收及交付边界 | 本项独立正常 Task/Delivery 验证同一工作接续，不绑定发布对象或时点 | retain：第7、8节，V811-05 | 原指定外部发布对象已退出当前范围；fixture 语义输入与真实 producer/caller 产物分层，原 Check 判断充分性，无新增实际 Agent/远端证明前置 |
| #811 要求2 | Task target 与 Issue authority 有明确关系；不改旧 transition | retain：第5节对象与 authority、第6节刷新 | 原 Task.source/accepted_scope 是来源关系；context 必须由 Discovery 生成 |
| #811 要求4/交付边界 | 原 ID、四类返回、fail-closed 与明确迁移 | retain：第5节版本表、第7节 | 同批迁移消费者；旧发布 schema/example 保字节，不做 current 双读 |
| 公共 package 合同 Public Skill I/O And Private State | output 最小、consumer 拥有 input、薄投影、无 consumer 的字段不入 DTO | retain：第4、5节 | Task/key 的直接 consumer 是确认及 context 返回；不携扫描、review、授权或恢复历史 |
| Sync→Discovery 原 authoring seed 与 reviewed-plan alternate | 原AI补change_input/clarify_profile，reviewed-plan还保source_locators | retain：第5.4节 | 新context_request仍需AI补写，不能以完整skill_input替代seed而遗漏必填字段 |
| 普通Interface1.8、instruction-only1.9及registry/manifest发布边界 | 各自只声明已发布支持集合 | change：第5.4、7节新版本及直接consumer | 不改旧字节、不把context4冒充3、不扩大1.9职责；本次候选和ADR承接版本演进 |
| 原 Clarify Source Actions And Mutation Boundary | load-bearing Issue 选择须执行原 comment/body action、live reread，返回 refresh_context | retain：第6节 mutation 分支 | 不将 mutation 伪装为 clear；保持 payload/preimage/结果一致性与语义 owner |
| 原 Clarify Target Disposition/Discovery duplicate_search | mutation前当前disposition需要完整duplicate_query/checked_at/candidates/facts_sha256；由Discovery供事实 | retain：第5.2节authority_duplicate_snapshot和第6节 | 确认需新增最小公开投影，snapshot绑定真实authority，不能伪造Task=Issue、重复搜索或跨读private |
| Discovery Caller-aware context requests 与旧 transition | 原四类 return；live authority identity 同时作为 target | change：只在新增确认分支分离 target/authority；第5、7节 | 保留四类原行为，Task target 不再被 Issue URL 替代；由本次版本迁移和必要 ADR 承接 |
| ADR-EXPLICIT-TASK-QUALIFICATION 的 output 不新增 key | caller 自持 Task/key，输出不扩张 | change：仅两种 scope_confirmation_required 的 Task-bound 分支；第5、7节 | 新直接 consumer 无法从另一个 caller 的调用期对象取 key；独立 ADR 窄替代，三 qualifier 的 classified 输出及其余 #812 决定保持 |
| current-knowledge 与 postcommit review 合同 | 三层 RDT/Architecture 各归原 owner，提交前整合/readback、提交后独立完整 Review | retain：第9节及 implement 第6节 | 规划不直接晋升 shared authority；整合不代表 reviewed_promoted |

## 4. 模块、职责与设计取舍

1. 两 qualifier 仍独占准入判断。原 `runtime/common.py` 的 typed output 从已验证 target 投影最小 Task 对象。
   非 Task profile 保独立合法形状；不能从 inventory 找 Task，也不让 qualifier 取得新的 session writer 权限。
2. Clarify 仍独占具体来源、范围及真实选择。`runtime/invoke.py`、原 recorder/checker 与私有 owner schema
   明确确认 profile 的 context bootstrap、freshness、source_actions、clear；脚本不推断选择。
3. Discovery 仍独占当前证据获取和语义充分性。`runtime/common.py` 校 Task/key/source 关系；
   `runtime/invoke.py` 从实际 owner result 产生 context，分别写确认 target 与 authority locator。
4. Sync 继续 deterministic。只对确认刷新接受完整、已规范化 return identity，执行 read 并原样投影。
   不选择 Issue、裁决 scope、生成 AI pass，原 sync profile 不改。
5. Interface1.10、shared consumer schema、projection 与原 workflow routing reference 共同声明同一条边。
   shared runtime的原discovery/validator解析consumer自有输入和封闭authoring profile，
   installed projection保留实际公开示例；不新增独立resolver或语义决策。
   原 caller 只消费正式 DTO，按原职责 reread authority、刷新受影响准入或进入 scope revision；clear 不代表实施准入。
6. tools owner 同步 matching workflow/packages/runtime/spec/platform，保 Task/session/peer 和用户内容。

直接演进原生产者及消费者比新增 wrapper、side store、通用 continuation engine 更直接。
代价是五个包和受影响消费者必须成套维护，确认 DTO 多了有当前 consumer 的 Task identity。
不用旧 Issue context 代替 Task context，也不放宽 mismatch 来减少这个成本。

## 5. 接口与数据

### 5.1 确认对象与 authority

两个确认 profile 保原名称，`candidate_refs` 是原 qualifier 实际返回的非空唯一集合。
`target_locator`、`continuation_id`、`resume_target` 均来自该正式出口，不从 phase 或命名规则重建。
Task-bound 分支使用 `task_ref` 和完整上游 `delivery_key`；两字段同时必填。
非 Task 分支不出现这两字段。合法 no_issue Task 仍属于 Task-bound 分支。
`mode` 放每个 public DTO 的外层并逐边检查一致性，不在 return_identity 再复制。

`return_identity` 是 Discovery 直接消费的封闭 profile union：旧四类保原字段；两个新分支包含
`profile,target_locator,continuation_id,resume_target,candidate_refs` 及 Task-bound 的 `task_ref,delivery_key`。
确认 context_ready 返回这些相同字段到原 Clarify input，source_exit 改为真实 `context_ready`。
task_ref/key 通过原公共 model、generation、registered checkout 和 Delivery 关系检查；可用官方 context
必须匹配，无 context 时只用原 explicit-object 合法分支，绝不自动选中或绑定其他对象。

Task target 保持原 Task locator；Issue authority 根据当前 `Task.source.repo_ref/number` 读取。
Discovery 新 context transition 的 `authority_locator` 是实际来源 Issue canonical URL，或合法 no_issue
accepted_scope/draft/source locator；`target_locator` 仍是确认对象。原 authority content/time 证据绑定实际来源。
无 Issue 时不能发明 URL；读取当前 accepted_scope 和原 draft/source 合同所要求的完整正文。
非 Task 来源由原 target/draft 合同取得 authority。来源缺失、scope revision 或身份冲突回其原 owner。

确认的 private `invocation_context` 保留确认profile与Task对象；`review_target` 则定位实际Issue/draft authority。
`target_disposition` 是该authority的当前决定，不是Task身份选择。普通Task target不进入Issue duplicate snapshot。

### 5.2 Producer → consumer

| 实际出口 | 薄投影与直接 consumer |
| --- | --- |
| qualifier scope_confirmation_required | 直接投影原字段与已验证 Task 对象至原 Clarify 对应 input2 |
| Clarify needs_context | 原 Sync 实际 base_current 保持不变；`handoff_profile=context_request`，原 return_identity 与检索线索交 Discovery |
| Clarify refresh_context | operation=read、route=repo_change、原 selected base commit、mode/repo、return_identity 交原 Sync confirmation-refresh 分支 |
| Sync baseline_ready | 实际 base_current，加 `handoff_profile=context_request`、原 continuation、return_identity，进入 Discovery context_request；普通输出仍为 pre_task/stage0-current |
| Discovery context_ready | 新 context transition、原确认对象与authority_duplicate_snapshot直接映射回 Clarify；不交 private owner result、完整扫描或审计数据 |
| Clarify clear | 独立确认输出只含 exit/profile/mode、原 target/candidates/continuation/resume、Task-bound identity 与本轮 source_selection，交原 clear router 的唯一 resume consumer；不带普通 Intake 的 target_disposition/clarity digest bundle |

change_input 的十类线索仍归 Discovery input 和原 AI retrieval owner。Task 入口从已解析 source 提供 Issue ref，
no_issue 从实际 accepted_scope/source 路径提供线索；新增字段不负责自动决定检索充分性。
所有公共字段均服务下一 consumer，私有 recorder schema 只保当前校验必需事实，无长期新 checkpoint。

`authority_duplicate_snapshot` 复用原snapshot的封闭字段：`query,checked_at,target_locator,authority_content_sha256,
candidates,facts_sha256`。candidates中每项保原 `repo,number,url,updated_at,facts_sha256`；不投影历史scan或AI决定。
Discovery从本轮真实owner duplicate_search确定性投影，snapshot.target_locator为实际Issue canonical URL或draft authority locator，
authority_content_sha256对应当前authority body，不能用Task locator或Task PRD hash替换Issue事实。
确认的 `source_exit=context_ready` 必须携该实际snapshot；原scope_confirmation_required bootstrap不凭空携snapshot。
Clarify按原规则对每个duplicate作AI选择，用snapshot原query/time/candidates构造当前target_disposition，
并校snapshot locator/content与transition.authority_locator/authority_content_sha256、review_target、disposition事实一致。
非空duplicate集合的真实选择仍遵守原对话条件，snapshot不表达授权或决定。Clarify不重复Discovery搜索。
需要替换Task source的选择回原source/scope owner，不因snapshot或context改变既有Task.source。

缺失snapshot或正常authority变化使其过期时，不能构造disposition或继续mutation；原Clarify needs_context请求Discovery重取。
Issue mutation后刷新生成新context和新snapshot，原snapshot不进入Sync return_identity，不局部改旧snapshot取得通过。
no_issue accepted_scope仅作为当前scope来源时仍沿原scope owner，不把它伪装为Issue；真实draft动作使用draft snapshot。

### 5.3 明确版本切换

以下 path 相对各 package `schemas/`，除 transition/envelope 位于 shared consumers。
所有 successor 使用独立 `$id`，Interface、examples、consumer、projection、runtime selector 同批切换。

| 边界 | 当前 → 本批 current |
| --- | --- |
| normal/solution 确认输出 | public-scope-confirmation-required-output-2.0 → -3.0；input aggregate3 不变 |
| Clarify 两确认 input | 无后缀的1.0 → 各自 -2.0；public-input-delivery-index-2.0 → -3.0 |
| Clarify needs/refresh | public-needs-context-output-3.0 → -4.0；public-refresh-context-output-2.0 → -3.0 |
| Clarify clear | 新独立 normal/solution confirmation clear1.0；public-clear-output-delivery-index-2.0 → -3.0；原 generic clear4 保原分支 |
| Discovery | context-request2 →3、public-input4 →5、context-ready5 →6 |
| Shared context transition | context-current3 →4，明确确认分支 target/authority 和原 base 形状；原 base-current2 不改 |
| Sync | 新 confirmation-refresh-read input1.0、deterministic-sync envelope2.0、baseline-ready1 →2；新 aggregate 为普通原形状与确认分支的封闭 union |

Clarify 私有确认对象使用 `requirements-clarification-confirmation-5.0.schema.json`，
普通3.0和旧active4.0保持各自原支持边界，不原地改旧发布schema。
source_actions、mutation_results与当前事实仍由同一recorder/checker校验。
确认的无 mutation clear 可不作普通 duplicate target disposition；Issue mutation 仍需原当前 disposition
及 action 条件，不能把 null 当作绕过。旧四类输出不改变语义。

### 5.4 共享 Interface 与直接 consumer

新 `schemas/skill-interface-1.10.schema.json` 从普通1.8演进，只增加本轮三个真实表达能力。

1. `transitionDescriptor` 支持实际context-current4的schema id/path，保原支持集合。
2. `invocation.call_local.public_input` 声明 `{schema,example}`，引用归该consumer package。
   Sync声明本包 `public-input-current-2.0.schema.json` aggregate及匹配公开示例。
   Clarify refresh的Skill consumer使用封闭合同
   `{kind:skill_call_local_input,interface_path:packages/guru-sync-base/interface.json,input_kind:structured_json}`。
   原reader从目标Interface自己的call_local.public_input解析schema，校验其示例和实际envelope输入。
   Producer不另指定schema；return_identity不装作scalar参数。Sync原scalar_cli入口、argv及deterministic边界保持。
3. `skill_input_authoring_seed` 新增profile-selector分支。
   `profile_selector={source:producer_output,field:handoff_profile}`；`authoring_profiles`为封闭非空列表，
   每项复用 `profile_id,seed_fields,authoring_fields,authoring_example` 和原 `alternate_authoring`。
   真实handoff_profile唯一选中一项；缺失、未知、重复不得改选其他profile。

Sync baseline_ready声明下列两项；原synced继续固定pre_task的authoring合同。

| profile_id | 从真实输出投影的seed_fields | 原AI补写及完整consumer校验 |
| --- | --- | --- |
| pre_task | source_exit、profile、mode、continuation_id | change_input、clarify_profile；reviewed-plan alternate另保source_locators；依Discovery原pre_task input |
| context_request | 上述四项及真实return_identity | change_input；依Discovery context_request3；return_identity不由AI重建 |

seed与AI字段不交叠。投影只复制实际原字段；普通pre_task不制造return_identity。
AI补写后完整输入须匹配真实consumer schema；seed不是完整输入。
base_current transition仍按原descriptor独立承接。reader只校固定profile、字段和引用，
不判断检索充分性、scope或source selection。

| 直接位置/consumer | 本批成套迁移 |
| --- | --- |
| Clarify、Discovery、Sync interface.json | 普通1.10；未用新增元数据的两qualifier保普通1.8 |
| 新schemas/skill-registry-1.5.schema.json、registry.json | 新1.5支持1.10，保原1.9独立职责；current切新引用 |
| 新production-contract-manifest-6.0.schema.json、contracts/production-current-6.0.json及current alias | 新6纳registry1.5和实际ordinary Interface集合；原5保字节；1.9不列ordinary执行 |
| trellis/guru-team-extension.json public_api | 当前registry、production manifest及run支持引用切匹配集合 |
| runtime/discovery.py、validate.py | 原discovery解析target Interface call-local schema；validator校声明、唯一profile及seed/AI字段绑定；沿原graph，不新增resolver |
| runtime/installed.py及installer CURRENT_SKILL_SHARED_SCHEMAS | 原公开投影识别call-local示例、authoring_profiles和alternate示例；安装新shared schema，保平台/mode |
| 新skill-eval-run-5.0.schema.json、runtime/eval_runner.py及直接receipt消费者 | ordinary run5从run2有限演进，只补普通1.10支持；ordinary执行/读取切5；qualification专用run3/4及生产矩阵不改 |
| tests/test_skill_packages.py、test_delivery_contract_graph.py、runtime/tests及直接installer/adapter tests | 原graph/schema/projection消费者识别新合同；验证输入补写和receipt消费，不以固定文本比较替代行为 |

上述shared schema均位于 `trellis/skills/guru-team/schemas/`。旧1.8/1.9、registry1.4、manifest5、
run2/3/4在内的全部已发布schema/example保原字节，只作既有固定验证或仍支持的独立协议资产。
Current selector不双读旧确认形状。普通1.10不复制1.9 instruction-only能力，不增加任意schema通道、
通用表达式、业务状态或跨阶段digest authority。

## 6. 状态、顺序、正常与失败流程

没有新增持久状态或 Task phase。只增加原 public graph 的确认分支。

1. 原 caller 实际运行当前所需的 normal 或 solution qualifier，得到 scope_confirmation_required 并保留当前工作义务。
2. 有匹配 context_current 时，Clarify 核对 target、候选、Task/key、mode、continuation、source authority/content/time。
   缺失时先通过原 Sync read 取得真实 base_current，再由经过语义 record/check 的 Clarify 正式 needs_context。
   普通过期时拒绝旧 context，回原 owner 取得新 read baseline 并走 needs_context，不修旧 transition。
3. Discovery 消费实际 needs_context，读原来源、历史与 current knowledge，完成原 AI gate、record/check/invoke。
   实际 context_ready 返回同一确认 profile/identity及本轮authority_duplicate_snapshot。
   Clarify只从该公开snapshot取得原duplicate事实，在实际authority上完成disposition，不把 Issue URL当 Task target。
4. Clarify 对真实选择执行原语义门禁。non_load_bearing 且当前 authority 已足够时，原无动作条件下正式 clear。
   真实未决 scope 仍在当前对话处理，不能写假答复、假选择或未经判断的 pass。
5. load_bearing Issue 选择通过原 source_actions 执行精确 comment/body mutation，live reread 后正式 refresh_context。
   该输出携原 return_identity，经 Sync read 的实际 baseline_ready 到 Discovery context_request。
   Discovery 重读 mutation 后 Issue 全文及选择来源，生成新的 context。Clarify 核对已经生效的选择，
   不重复 mutation，再正式 clear；不要求第二次无意义的 context digest 变化。
   合法draft的load_bearing选择执行原proposed_draft_update并重读真实draft，经同一保身份刷新分支取新context；
   no_issue Task需要改变accepted_scope时仍回原whole-scope owner，不能由context刷新修改scope authority。
6. 原 resume consumer 消费实际 clear 后，重读受影响 authority，刷新原 qualifier 判断或执行原 scope revision。
   若 Task accepted scope 需变化，必须走原 whole-scope writer/acceptance 和 Delivery rework，不能凭 clear 扩写实现。

来源缺失、真实 Task/key/source mismatch、closed/terminal 对象或未解决 product choice保原 stop/owner 路由。
普通输入遗漏修正后重进实际 owner；record/check 成功不产生正式 exit。Git baseline 不可得回 Sync，
原 source mutation 失败保实际失败，不生成 clear；不增加重试协议、锁或 crash 恢复框架。

## 7. 恢复、兼容、迁移与集成

新增 `trellis/presets/guru-team/MIGRATION-811.md` 列出上述精确支持集合和 current consumer 退出。
旧 schema/example 的 path/id/bytes 保作 pinned validation 资产；新 runtime 不双读旧确认形状，
不替旧 output 补 key/改 continuation。已完成结论按原 applicability 采用，不能改称当前阶段通过。
待调用输入由原 caller 从真实已知对象重新装配；丢失必要对象回原 Identity/Ensure/Bind/Selection。
旧未完成操作在固定完整旧 provider 及原输入下恢复，不重放已完成 mutation；随后再采用完整 matching source。
旧四类保持其各自 current 或 pinned-old 支持边界，本项不恢复退休 Task-status active 路径。
MIGRATION-811列出第5.4节的版本集合、原authoring字段和直接reader/installer采用关系。
新package与旧registry/reader混装保原版本错误；不能删descriptor、伪标版本或手补对象取得通过。

本项 matching dogfood 采用使用 `guru-upgrade-tools` 的完整源合同：preview/prepare 固定真实 tools 写集，
展示具体 source/target/command/paths 后按其副作用边界执行，验证目标自己的 resolver/native/installed。
本地 candidate 明示 formal_fork_source_lock 未验证；不把本地安装成功当作正式 release lock 证明。
保 Task/session、用户业务 dirty、peer tools/common pointers；实际 sidecar由原 owner逐个处理。
不手工复制受管目录，不为普通 apply 的 Task inventory 阻塞迁移其他历史。

本 checkout 已由原 tools owner 完成 matching 采用，实际 resolver、installed/native、投影、mode/sidecar 与 drift 结果由配对 Test 单写。
本轮未改变工具来源，不重放已完成采用；只有真实源码或安装状态变化影响后续入口时，才回原 tools owner 判断。
接续验收使用本项独立正常 Task/Delivery 场景，场景内对象通过原公共入口建立并保持同一工作身份。
现有 test_qualification_context_chain.py 真实调用 qualifier、Sync、Discovery、Clarify 和返回后的消费；
fixture 的语义输入显式属于测试层，不冒充真实用户未决选择，也不新增实际 Agent 或远端业务证明。

## 8. 验证设计

| ID / 对应AC | 层与实际边界 | 输入、动作、独立观察及限制 |
| --- | --- | --- |
| V811-01 / 01、02、04 | 长期公共链回归；扩展原 package tests | 真正调用两个 qualifier public invoke，以其输出进入 Clarify；缺失、当前、普通来源变更过期分别取得真实 Sync/Discovery context并 clear。断言原 candidates/target/key/continuation/resume及 caller消费结果；fixture只能建 boundary 之前Task/Issue/Delivery，不能预填被测出口 |
| V811-02 / 01、02、04 | 长期 mutation refresh公共链 | 两 profile 从真实Discovery的authority_duplicate_snapshot构造原disposition；用受控 repo-bound gh外部替身执行load_bearing source_actions，真实 recorder/checker/invoke走 refresh→Sync read→Discovery→clear；断言snapshot为实际authority、原duplicate事实匹配、Issue已更新、fresh snapshot已取、身份不丢且不重复mutation。此测试不证明真实远端写入或AI选择 |
| V811-03 / 03 | 旧四类/正常错误回归 | 采用原有效tests并补实际受影响边：source_locators、active/standalone resume、普通 Sync pre_task、失配和过期仍拒绝。no_issue Task/合法非Task分支分别观察原authority解析；旧发布资产按B验证字节，版本混用不被当前入口接受 |
| V811-04 / 05 | package/图/安装投影 | source与实际installed package、consumer/projection、source/installed graph/出口查询、mode、平台声明、reapply/drift/sidecar定向验证；目标自身native入口运行。不能替代真实Agent或完整多平台矩阵 |
| V811-05 / 06 | 本项独立正常 Task/Delivery 公共链接续 | 复用现有完整公共链 fixture 经原入口建立的合法对象，两个 qualifier 的真实输出经原 context producer、正式 clear 和原 caller 后续消费；核同一 Task/generation/Delivery、候选、target、continuation/resume。fixture 语义输入不等于实际 Agent 判断，不指定发布 Task 或时点、不捏造未决选择；原 Check 按当前验收判断组合证据 |
| V811-06 / 07、08 | 原质量与lifecycle | 原知识整合/readback→TaskCommit→固定完整B..H独立Architecture/Check/full Review→readiness/交付；之后整体Completion/Closure/Finish及live main可达性。规划不预填pass |
| V811-07 / 03、04、05 | 共享metadata与ordinary receipt | source/installed discovery解析context4与Sync自有call-local schema；从真实baseline_ready按两profile取seed，补AI字段后由Discovery schema校验；reviewed-plan保source_locators。ordinary eval smoke真正调用一个1.10包，生成并由run5 reader消费receipt。旧发布资产按B保字节。不证明qualification生产矩阵或实际Agent行为 |

先补廉价且行为明确的身份/路由回归，再实现并跑公共链；已有有效旧四类覆盖按影响采用。
必要断言来源于 #811 的输入、动作和可观察返回，不照抄实现计算expected。临时诊断只用于尚未解释的断链；
原失败和代码因果已足够时不追加固定rollback/red循环。若新回归是否到达原缺陷仍不明确，先查实际入口/条件/观察，
再按具体问题选一次有界旧版比较。设施反复失败时重评方法，未补证据不能宣称验收通过。
上述必要范围足够后停止追加验证；完整多平台/Release矩阵与生产效果保持未验证边界。

## 9. Canonical 引用、本轮差额与实际未决项

原 RDT writer 维护 `docs/{requirements,design,test}/current/qualifier-applicability.md` 的 #811完整定义，
并处理命中的 `current/local-fix-intake.md` 中 target/authority关系；不复制另一个current主题。
三层各自新增实际来源、行为/设计/测试关系和验证边界，原历史观察不追改。
Architecture writer维护 `03-domains/qualifier-applicability.md` 的确认对象关系及
`03-domains/workflow-context.md` 的上下文边；必要ADR窄替代 #812输出约束。
同一workflow-context单元还维护共享Interface声明、AI authoring与事实投影职责；
ADR承接普通1.10及直接consumer迁移，不向共享root/system/ownership/index登记新主题。

本批真实隔离贡献为 `docs/architecture/contributions/811-qualification-context-continuation/contribution.md`，
ADR候选同目录 `qualification-context-continuation.md`。它们由本Task持有，最终共享整合由原Architecture owner执行。
规划不写 shared-current、root/system/ownership/index，不新增 GAP台账。完整拟写与真实工程结果形成后，
原RDT/Architecture各自在提交前final_integration核live expected-current、整合/readback；
TaskCommit后一次独立完整Review核真实before/after，不能提前称reviewed_promoted。

设计层没有待用户决定的产品选择。private确认schema5.0按第5节对象与原consumer展开；
若需要超出本设计的authority/owner/支持边界，回原Author/Architecture。五包、共享metadata及本 checkout 的 matching 采用已经实施，
工程结果、整包初试失败与后续定向通过由配对 Test 分别保留。当前范围不再有外部发布 Task 验收依赖；
新规划接受后采用仍适用事实，补实际覆盖缺口，再由原 Check/full_review 判断完整候选。知识整合与质量/交付终态尚未完成。
