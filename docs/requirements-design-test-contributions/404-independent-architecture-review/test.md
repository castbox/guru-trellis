# #404 Test 增量

状态：RDT 合同已晋升至 `current-main-0.6.17-guru.78`；实际行为结果仍按下表记录。本文件是 #404 实际验证结果的唯一文档来源；Requirements、Design、traceability 与其它导航只引用本页。继承 current `current-main-0.6.17-guru.77` / `active`。下列 `T404-01..10` 对应 task acceptance `A404-01..10`，是验证合同，编号存在不代表已执行或通过。

| Test | 正常候选与观察目标 | 实际结果 |
| --- | --- | --- |
| T404-01 | 通用能力新增/扩大业务职责；独立读取、真实因果和必要局部收敛，不以设计/代码/测试/contribution 一致放行。 | `PASS/native-r3`：两个一致但错误的业务候选均自主识别职责冲突；真实 SKILL/authority/source/callers 读取、独立判断后核对 contribution、自主 wrapper、具体局部收敛评分均通过。r2 失败保留。 |
| T404-02 | 共享 default 影响未修改 caller；实际消费者取证，合法技术语义不误报，不泛化 exported 审计。 | `PASS/native`：技术 selector/no-impact 对照通过；r3 业务 fallback 对未改 summary caller 的影响被真实识别，不泛化 exported 审计或误拒绝合法请求。 |
| T404-03 | 必要调用方迁移/旧路径退出与无关历史债务对照；不留下最小 diff hack，不自动扩大当前责任。 | `PASS/native-r3`：继承案例区分既有 inference 与新 public 参数固化，具体要求 import owner 语义、summary caller 适配、transport fallback 退出；保留 optional tag/合法 retry，不接管无关 cache debt。 |
| T404-04 | 红测的回归、不可分割前置、历史、环境和未归因；有限调查与对应停止/处理，不以全绿反向改合同。 | `PASS/native-r5`：历史/环境/未归因整体 Check 通过；测试断言回归及既有共享列表断言必要前置，均实际整体 Check 返回 implementation_required 并通过评分；既有生产负向与严格 bounds helper 的合法 Architecture 停止独立保留。 |
| T404-05 | 合法非默认配置、已有硬不变量及缺诊断标签；保持合法范围，缺标签不新增拒绝。 | `PASS/native`：no-impact、约束及 r3 业务候选保留 retries 0/6/8、真实 0..8 不变量和 optional diagnostic；clean/history 整体 Check 同样保留合法配置，缺标签不新增业务拒绝。 |
| T404-06 | Planning 真实候选/无候选、仅任务拥有的最小约束及不足约束；真实评估或既有 incomplete/blocked。 | `PASS/native`：真实候选、无候选、最小任务约束充分/不足均完成独立读取、自主 wrapper 与语义评分。 |
| T404-07 | Planning/discovery/Phase2/committed 的实际 fresh 派发、输入/read 顺序、自主 author/wrapper；正常主会话自填不作为独立 proof。 | `PASS/fixture-native`：Planning、discovery、独立 Phase2、真实 fixture committed range 四阶段均 fresh 执行并评分；本任务 committed review 尚未发生。 |
| T404-08 | fresh worker 先专项后整体，叙事暴露/参与实现者另派，no-impact 仍判断；两个 Skill 真实结果分别成立。 | `PASS/native`：clean 与 historical-red 均实际先 Architecture 后整体 Check，独立 trace 与两个 wrapper 分别成立；四阶段 no-impact 无贡献/ADR；此前实际叙事泄漏失败保留。 |
| T404-09 | missing/unfinished/mismatch/unavailable、正常 stale/新候选与 promotion diff；已有唯一 consumer、matching-stage eligibility 接续，不降级自审。 | `partial`：两匹配下游 stage 已真实 eligibility 调用；异常路由/identity 单元测试仅作确定性证据；本任务 promotion-created diff 尚未产生。 |
| T404-10 | source/installed graph、package/runtime、实际平台 native 与其它投影、apply/reapply/drift/ownership/零 sidecar。 | `PASS/targeted`：Codex 九个独立 Architecture 场景和四个整体 Check 场景评分通过；三个合法上游停止独立保留。source/installed/投影/reapply/drift/ownership/零 sidecar 通过；其它平台仅投影证据。 |

## 文档增量检查

`T404-DOCS`：PASS，仅覆盖本增量的确定性文档事实。五个 contribution 文件通过 UTF-8、末尾换行与 trailing whitespace 检查；18 个本次增量/README 导航的相对链接目标存在；R404-01..08、D404-01..08、T404-01..10 定义及八行 requirement trace 已核对。`git diff --check -- README.md trellis/workflows/guru-team/README.md trellis/presets/guru-team/README.md` 退出 0。此结果不代表 T404-01..10 的行为验收或共享 current 晋升。

## 当前结果与边界

当前 HEAD 为 `07b89e48985761035777d15fdb82476174e277a6`，以下证明该 HEAD 上尚未提交的 #404 工作区候选；不构成 committed review。

- managed Python 定向 package 测试：normal-scenario 23、solution-mechanism 24、Planning approval 23、Branch Review 36、Phase2 29、Delivery 18 项通过。Completion/Finish 使用临时测试依赖目录中的 pytest 8.4.2、`--import-mode=importlib` 与 managed interpreter，合计 83 项通过；产品 runtime lock 未修改。
- Completion/Finish 首次 unittest 收集因缺 pytest 失败；供给临时依赖后的首次 pytest 合并收集遇到两个同名 `tests` 包的导入冲突，使用 pytest 支持的 importlib 模式后通过。两次环境/调用失败保留，不计为产品通过。
- canonical source 与 installed package checker 通过；35 active packages / 106 commands，production 33 invokes / 153 exits；selected platforms 为 Claude、Codex、Cursor。首次 source checker 的错误 `--root` 参数导致 missing registry，改为仓库 root 的受支持调用后通过。
- preset apply 更新 managed copies，产生 69 个 `.bak`；每个备份与 HEAD 旧副本逐字节相等，保存到 repo 外临时验证目录后移除。reapply `status=ok`，package/overlay conflicts 与 sidecars 均为空；installed activation、upstream ownership 与 dogfood drift 通过。此证据只证明选定平台的安装投影，不证明各平台 native 执行或官方 update。
- Architecture package 首次 25 项通过、1 项失败：原 corpus exact-case inventory 尚未包含新 native cases；按其真实 corpus consumer 更新后 26/26 通过。Architecture adapter 定向测试 5/5、Phase2 adapter 定向测试 6/6 通过。
- Codex native 首次在 model 启动前缺少隔离 home/qualification source locator；补齐 repo 外私有执行环境后，Planning 实际独立运行到 wrapper。后续一轮因 adapter 在 invoke 后追加 read 而失败；再一轮因 reviewer 缺少既有 output identity 字段在 wrapper 失败。均保留真实失败及归因，新 run 必须自行评估、author、invoke，未使用预填结果或把失败 relabel 为 pass。

RDT owner 已实际调用 `task_impact_sync` 返回 `sync_required`，随后按 reviewed contribution 完成 `.78` 三层知识合同晋升并调用 `promotion` 返回 `ssot_current`，继承仍 active 的 Architecture `.77`。immutable `.77` 版本文件未修改；此结果不表示实现完成。

## 当前 r2 原生与复用验证

冻结 r2 的原生调用依次串行执行。实际模型为 corpus 声明的 `gpt-5.6-sol`；仅 Codex 实际执行，Claude/Cursor 及其它声明平台只有相应投影证据。评分检查实际 ephemeral prelude、模型输入、读序、candidate/source/未改 callers、AI authored gate/envelope、一次 formal wrapper 和 stdout；不以 expected exit 或绿色 checker 自动评分。已有 completed-run replay 消费评分不重新运行模型。

| 原生场景 | 实际 wrapper/检查与语义结果 |
| --- | --- |
| planning-semantic-authoring | `baseline_current/no_change`；六项确定性与独立因果评分通过；实际执行 73550 ms。 |
| implementation-discovery-independent-native | `baseline_current/no_change`；六项确定性与独立因果评分通过；completed replay 通过。 |
| phase2-independent-native | `baseline_current/no_change`；六项确定性与独立因果评分通过；实际执行 126702 ms。独立 Architecture 场景不替代整体 Check。 |
| branch-review-independent-native | `baseline_current/no_change`；六项确定性与独立因果评分通过；实际执行 71488 ms。实际 fixture range `06fd96dbd81e27f14bc525617c8d2bf735fcbe30..99bcd87eba365b5468bb54c827a9ada02e4aa179` 与 owner HEAD 一致，不替代 #404 本任务 committed review。 |
| planning-business-default-native | `execution_error`：实际 AI/wrapper 得到职责冲突，但 trace 缺初始 SKILL.md read；不能用语义评分转成通过。 |
| planning-inherited-business-default-native | 实际 `architecture_conflict`、六项确定性通过、独立读取/因果评分通过；`candidate-causality` 和 `before-after-necessity` 未通过：实际输出缺必要局部迁移、caller 适配和旧 fallback 退出的具体解释。正确 exit 不证明完整方法。 |
| planning-missing-candidate-native | 实际 `contract_incomplete`；六项确定性与两项语义评分通过。空 patch、相同 base/head、无 design 候选，不作 authority-only approval。 |
| planning-constraint-sufficient-native | 实际 `baseline_current/no_change`；六项确定性与两项语义评分通过；实际执行 155355 ms。只取带来源的 endpoint 能力事实，保留显式 Responses callers 与合法配置。 |
| planning-constraint-insufficient-native | 实际 `contract_incomplete`；六项确定性与两项语义评分通过；实际执行 83681 ms。provider response/lifecycle 事实不足保持不确定性。 |
| native-owner-clean | 独立 Architecture invocation 22 先于整体 Skill read 23、task narratives 49..52；qualifications 67/68 后 Check 69，实际 passed，九维度由模型自主 author，评分及 completed replay 通过；250444 ms。 |
| native-owner-historical-red | Architecture 21 先于 narratives 49/50，qualifications 73/74 后 Check 75，实际 passed，评分及 replay 通过；254110 ms。历史格式测试 before/after 同样失败；service 缺失为环境错误；external unknown 缺 before/cause 保持未归因。owner 如实保留红测/不确定性，按无 range dependency 的非 gating authority 停止且不修复、不扩张 follow-up、不宣称全绿。 |
| native-owner-finding | 独立 Architecture 实际 fitness_regression，定位 upper-exclusive predicate 扩散至未改 filter；current-only guard 在整体 Check 启动前停止，保留 execution_error/upstream DTO；158799 ms。此结果只证明真实上游停止/implementation 路由，不产生整体 Check finding 或 implementation_required。 |
| native-owner-required-dependency | 独立 Architecture 实际 fitness_regression，定位既有 strict lower<upper policy 被新 predicate→policy 依赖传播到合法 singleton/filter；before/after dependency test 均红，真实 source/docs 因果成立。guard 在整体 Check 前停止，保留 execution_error/upstream DTO；135425 ms。不可把它评分为整体 Check 通过。 |

Architecture owner 另行读取上述 still-applicable 独立 committed fixture 结论及 live authority/source/callers/Git，完成 `publication` 与 `acceptance_finish` 两次真正的 matching-stage eligibility 判断并各自亲自调用 2.0 wrapper，均返回当前 stage 的 `baseline_current/no_change`。新输入、freshness 与 gate 自行形成，未修改/relabel Branch Review DTO。仅证明 fixture Architecture eligibility，不表示 Delivery、Completion 或实际任务 committed review。

- r2 同步后 Architecture authoring 7、Architecture package 26、completed grading 16、Phase2 authoring 7、Check 29 项通过。
- runtime 全套实际执行 64 项，62 项通过、2 项旧合同断言失败（要求第一轮 PRD read 与固定旧 no-impact/narrative prompt）。两项经当前 qualification 后退役旧断言并保留实际 source/caller/trace validation，定向重跑 2/2 通过；未声称完整 64 项重跑。其它 62 项定义/依赖未变，原结果由最终 owner 按 Dependency-Scoped Validation 重新判断 applicability。
- `task.py validate` 首次发现空 implement/check JSONL；资格通过后仅配置 workflow index 与 semantic-retrieval 的两项 durable spec 引用，当前验证无 warning。未向独立 reviewer 注入 PRD/acceptance。
- 实际 trace 暴露 project change-contract 迟于 candidate/source 读取，经两项 qualification 后调整为 constitution → baseline → change contract → candidate → consumers。当前七个评分通过的 Architecture 场景具有真实正确顺序，objective read-order 测试只作其确定性辅助。
- r2 apply 首次产生 14 个 `.bak`，全部匹配 apply 前立即保存的 installed preimage，保留 repo 外后逐个移除。reapply `status=ok`；source/installed、selected Claude/Codex/Cursor、activation、ownership、dogfood drift 与 recursive zero sidecar 均通过。JSON/bash syntax、managed Python compile 219 文件、platform projection 5 项通过。
- 第一波并行外层 native group 共用隔离 home 的 permission-profile preparation 发生正常协调冲突；停止外层后 active children 各自结束，r2 改为单队列串行。另一次 clean Check 的 qualifier shell authoring `invalid_json` 是实际模型调用错误，不能只归因协调；前序 Architecture 的真实 current 结果保留，不据此宣布整体通过。此前 reviewer 读取 stale native-context 造成叙事暴露的失败同样保留，fresh re-entry 重新执行而非修补旧输出。

`C404-actionable-causal-report` 经 current implementation-discovery 两项 qualification 返回 `classified`：实际责任冲突输出不足以承接必要局部收敛。r2 队列结束后，仅在既有 Architecture gate evidence 要求一般性的具体因果/替代职责/caller 适配/旧路径退出说明；无新公共字段、fixture 答案或脚本判断。

`C404-consistent-wrong-candidate` 经 current implementation-discovery 两项 qualification 返回 `classified`：旧业务 fixture 设计声称 import caller 传 stage，而真实 caller 未传，且缺 matching green tests/contribution，不能证明一致但错误的架构候选。r3 仅修订 Architecture authoring adapter 与其定向测试：实际 import caller 传 `metric_stage='import_stage2'`，summary caller 不变；managed interpreter 实际执行匹配设计/代码的三个候选测试、返回 0；覆盖实际调用、defaults/tags、retries 0/6/8 和真正无效 bounds。proposed contribution 与候选一致且无 pass 叙事，其 locator 留在 facts，第一轮 required_reads 不含它。其它 no-impact、constraint、Check branches 与 corpus 未改。定向 authoring 测试 8/8 通过；两个业务场景的 fresh native re-entry 结果见下。其它结果能否复用由最终 owner 对实际依赖判断，不以 path/hash 本身推定。

r3 canonical 同步首次 apply 产生七个 `.bak`，逐个与立即保存的 installed preimage 字节匹配，保留 repo 外后在 checkout boundary 校验下移除。reapply exit 0；随后 fresh source/installed package checker 与 dogfood drift 均 exit 0，selected platforms 仍为 Claude/Codex/Cursor，零 sidecar。该证据不替代其它平台 native 或官方 update 验证。

r3 仅对受影响两个业务场景 fresh 串行重入，未重写旧结果：

- `planning-business-default-native`：135488 ms，实际 `architecture_conflict`；六项确定性、两项语义评分与 completed replay 均通过。trace 首先读取 SKILL.md；constitution → baseline → change contract 在 candidate/callers 之前，独立判断在 contribution 之前。真实 source/test/contribution 一致且三个测试通过，reviewer 仍定位 transport 新 business fallback 与未改 summary caller 的误标，要求 owner-specific import tagging、optional pass-through 与旧 fallback 退出；retry default 3 保持合法。
- `planning-inherited-business-default-native`：96404 ms，实际 `architecture_conflict`；六项确定性、三项语义评分与 completed replay 均通过。reviewer 读取真实 before/candidate，明确 inherited inference 被 public parameter 固化；具体说明 import owner 语义、summary caller 适配与 shared fallback 退出，保留 optional diagnostic、合法 0/6/8 与真正 bounds，不将无关 cache debt 变为 finding/follow-up。其对未证明必要的 default-change 观察不拒绝合法业务调用。

两次模型均在 semantic authoring 后亲自 formal invoke，一次实际 wrapper 返回后结束；缺路径的探索性 read 失败如实留在 trace，未发生 wrapper/schema 失败后修补输出。原生队列现已结束，无 active child；本文件如实保留整体 Check finding/prerequisite 无最终结果的边界，覆盖充分性由真实任务 Phase2 owner 判断，不能以累计场景数替代。

## 真实任务初次 Phase2 与合法补证

空历史 generic reviewer 在读取任务 PRD/验收/实现叙事之前完成本任务独立 Architecture，亲自原 wrapper exit 0：`baseline_current / architecture_impact / reviewed_candidate`，阶段 `phase2`，绑定仍 active 的 `.77`、current constitution 和 `implementation-v2` contribution；九项 concern 检查无 finding。随后才读取完整任务、独立执行整体 Check。原 recorder/checker/public invoke 均 exit 0，实际结果 `{"exit_id":"blocked"}`：当前负向两案例只有真实 Architecture 停止，不能证明整体 Check 的回归/不可分割前置归因、qualification、finding 与 implementation_required。

这轮 owner 实际运行完整 runtime 128/128、adapters 15/15，Architecture 26、Check 29、normal 23、mechanism 24 均通过，source/installed/drift/ownership 通过。它完成两项实际资格判断后记录四处 P3 extra blank EOF：task design、implement 与 Architecture contribution/ADR。原 overlay 中不存在 recorder 脚本的探索性调用 shell exit127 保留；随后使用原 installed package recorder/checker、public invoke 成功。blocked checkpoint 与临时 author/public input 已按原生命周期退役。

四处 EOF 各移除一条空行，无语义规划改变。`C404-phase2-upstream-route-coverage` 的 normal 资格为 rejected_not_reproduced：current-only guard 保留正确入口前置，不能为补证放宽。另一个 `C404-overall-negative-native-evidence` 经 current implementation-discovery 两项原 wrapper 返回 classified/qualified_current：只允许新增两类真实测试层红测事实（本次测试回归、当前必要测试依赖阻塞），保留正确纯 predicate、未改生产 caller、原 Architecture guard 和原有负向停止案例；由 fresh Architecture 与完整 Check 自主判断，不预填 current/pass。

r4 新增中性 `native-owner-test-boundary` 与 `native-owner-test-support`，只扩展 Phase2 authoring adapter、其因果测试、Check corpus 与既有 package test consumer。boundary 候选是测试 assertion 改动，真实 before-green/after-red；support 是现有共享 assertion entry 的 legal singleton 验证，真实 helper 自测 before/after 均红，当前新 singleton 验证直接受阻。两者纯生产 predicate 与实际未改 filter 的三个测试 before/after 均绿，完整候选含新 test/helper，Architecture 第一轮按 authority-first 读取，不向模型输入诊断或期待出口。定向一项因果测试实际覆盖两案例及直接 test_interval.py 红测，通过；完整 authoring 8/8（67.107s）、Check package 29/29 通过。r4 apply 产生七个 `.bak`，全部与即时 preimage 匹配并保留 repo 外后逐个移除；reapply/source/installed/drift 均 exit 0、零 sidecar。

- `native-owner-test-boundary`：209763 ms，独立 Architecture 实际 baseline_current/no_architecture_impact/no_change；constitution、baseline、change contract 在 candidate/callers 之前。Architecture invoke 20 在整体 Skill read 21 与 task narratives 48..51 之前，两项 qualification 65/66 在 Check 67 之前。整体 owner 自主 author 九维度，保留必需 suite 7/8 与 production caller 前后 3/3；实际 implementation_required/F1（owner severity P1）。六项确定性、三项语义评分及 completed replay 全通过，未为评分修改 severity、代码或红测证据。
- `native-owner-test-support`：207010 ms，独立 Architecture 实际 fitness_regression：既有 assertLess(lower, upper) 加上新 singleton caller 扩大了未经许可的严格 bounds 拒绝。reviewer 给出具体 helper/caller/旧路径局部收敛；current-only guard 在整体 Check 前停止。raw execution_error 如实保留，无整体 Check DTO，不通过评分改成 pass。

`C404-prerequisite-assertion-native-evidence` 经 current implementation-discovery 两项原 wrapper 返回 classified/qualified_current：只允许新增一个普通共享列表断言实现错误的测试层前置案例；保留既有 support、所有历史失败与 Architecture guard，不预填判断，不改变生产 predicate/filter/bounds。第一次资格调用使用 repo 外/URL candidate locator，被原 validator 以 unsafe_path 退出；改为当前 repo-relative locators 后两项正式调用通过，未持久化资格 artifact。r4 reviewer 已独立首轮取证与定向检查，但新增候选使其适用性失效，未 author/formal invoke；冻结后已重新派发 fresh reviewer，正式结果尚未完成。

r5 仅新增中性 `native-owner-selection-assertion`：已有 test-only helper 比较 actual list 与 `expected_values.sort()` 的返回值，未改 helper 自测 before/after 均红；本次新增 singleton selection test 通过该 entry 直接受阻。实际生产 predicate/filter 与直接 caller 测试前后仍绿；helper 没有生产 import、bounds 校验或更严格的拒绝规则。新案例保留所有旧 corpus 内容/期待与 guard，不向模型输入归因或期待出口。因果测试 1/1（11.162s）、完整 Phase2 authoring 9/9（76.689s）、Check package 29/29（7.652s）通过。apply 首次 exit 2 仅因七个已知 `.bak`；每个匹配即时 preimage，保留 repo 外后逐个移除。reapply/source/installed/drift 均 exit 0、零 sidecar；只覆盖既有选定平台投影，不等于官方 update 或完整矩阵。

该案例 native 实际执行 172795 ms。fresh Architecture 先 authority/source/helper/callers 后独立判断，invoke 25 返回 baseline_current/no_architecture_impact/no_change；整体 Skill 26 与 task narratives 52..55 随后读取。整体 owner 比较 before helper 一项失败、after helper 与新 caller 两项失败，以及 production caller 前后 3/3，定位 list.sort() 返回 None；明确 R2 要求的既有 shared entry 及新 singleton 验证离不开此局部修正。两项资格 wrapper 72/73 在 P1 finding 与 Check 74 之前，原 recorder/checker/public invoke 均 exit 0，真实结果 implementation_required/P1-selection-assertion-sort-return。required suite 8/10 如实保留；六项确定性、三项语义评分与 completed replay 通过。不把它当作无关历史债务，不改变生产语义或强制全绿。

本任务 passed Phase2、Task Commit、独立 committed review、Architecture promotion 与 promotion-created diff fresh gates 尚未完成；当前不声明 whole-task Completion、Delivery readiness 或发布已通过。

静态 schema、wrapper unit tests、字符串、mock 或 package checker 只能证明其确定性范围，不能代替受支持正常路径中的 AI 派发、独立判断、停止及 consumer 行为。native 不可用或证据不足保留 pending/block，保留首次失败与有限归因；未归因不得写成历史失败。

完整累计多平台 clean/existing/update/Release matrix、真实业务仓安装/部署及生产验证不属于本任务验证范围，均未验证。最多一个确有当前安装证明需要的代表性 throwaway；实际 native 执行的平台与仅投影验证的平台分别记录。官方 update 兼容性不能由 apply/reapply 推定。
