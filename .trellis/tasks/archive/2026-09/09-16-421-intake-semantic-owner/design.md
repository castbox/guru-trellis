# #421 技术设计

## 1. 最小修复与责任边界

需求和验收以 [prd.md](./prd.md) 为准。生产变更只修订四个 Intake Skill 的执行入口与合同；脚本仍不产生语义结论。测试层复用 #415 的 `semantic_authoring`，增加现行 standard Intake 链的真实 native 执行能力，不新增生产控制面。

官方扩展依据为 Trellis 的 [custom workflow](https://docs.trytrellis.app/advanced/custom-workflow.md) 与 [spec marketplace](https://docs.trytrellis.app/advanced/custom-spec-template-marketplace.md)：流程在 Markdown 中，spec 放可复用约定，不修改上游 hook 或全局包。

## 2. 四个入口的直接修订

固定范围是 `trellis/skills/guru-team/packages/` 下的 `guru-discover-change-context`、`guru-clarify-requirements`、`guru-review-contract-wording`、`guru-review-change-request`。

每个入口直述：读取完整 contract；当前 AI 读取 authority 并审查；author 当前 owner result；调用该 package 已声明的 recorder、checker、public wrapper；消费唯一 typed exit。保留各自前置动作：Discovery 当前态与 history、Clarification 真实选择、Wording scan/classification、Readiness 十维审查。

`owner_not_yet_executed` 促使当前 AI 继续执行，而非另找 producer。真正的 authority、freshness、schema 或需求选择缺失按该 Skill 原有 route 处理。不得通过增加脚本自动 pass、放宽 recorder 或绕过 workspace 来消除停滞。

## 3. Eval-only authoring flow

### 3.1 声明与现有模式

Codex eval 可选 `--codex-model` 为 corpus 未固定模型的 case 选择运行模型；省略时保持原默认行为。仅 Codex 接受此参数，空值拒绝；已有 semantic-authoring/qualification 的固定模型继续按原合同，不被此参数覆盖。使用现有 adapter request 的 model_id 传递运行身份，post_owner 仅在 Codex 显式选择时允许该字段；不修改 corpus schema 或生产 Skill I/O。原 codex exec 使用 --model 携带选择，不修改全局配置、工具或包装器，不改变 fresh/saved、评分和错误传播。

在原 eval corpus 的 `semantic_authoring` case 内增加闭合的 `native_authoring_flow=standard_intake` 声明，由当前 eval runner/adapter 直接消费；未声明者保持既有 single-Skill 执行语义。该字段仅用于 eval 调度，不进入生产 Skill I/O。`post_owner` 携带此字段必须拒绝。

两个 case 放在 Readiness package 的 eval corpus，分别使用清晰需求事实和未决范围冲突事实。case prompt 只描述输入任务，不透露 ready/blocked 期望，也不对某个 case 特判生产路径。单 Skill Architecture case 与现有 post_owner case 继续使用原路径；不创建兼容 wrapper。

集成 main@78651e20 后，同时保留 #417 的 Phase 2 authoring 分支及其真实 Architecture、双 qualification、最终 Phase 2 调用顺序。Intake 的多命令协议与 Phase 2 的 owner-specific 协议分别按原声明选择，不能把所有非 Intake case 归为单次调用，也不能把 Intake 的同次输入修正规则套用到 Phase 2。

### 3.2 Facts-only installed fixture

复用 `stage_clean_installed_owner_repo` 和真实 preset；fixture 提供干净 Git、repo-bound GitHub 事实响应、需求、Docs/code/tests、history 和正式包。GitHub fixture 只返回 source facts，不返回 owner result、gate 或 route。

host 不运行 `build_context_owner`、readiness owner recipe 或 record/check 来准备前置结论。当前 native Agent 自行调用 Sync，再按现行链执行 Discovery、Clarification、Wording、Readiness。四个 owner 的结果仅留在该 native invocation 的内存；生产 recorder/checker 的 stdout 被原样传给同 owner 的下一命令。

模型可见投影使用最小声明 allowlist：四个真实 semantic Skill 与既有 Sync 前置的 SKILL.md、完整 contract、Interface、当前调用必要的 schema/consumer schema、原命令边界及必要事实。不得复制整个 schemas/examples/scripts/references 目录；Interface 的 input/output/error example 引用也不产生投影资格。examples、owner-result/output/pass 样例、eval corpus、expected output、grader policy 与 private runtime 均不暴露。helper 与 trace validator 只接受声明资产，不因某个文件存在就认可其读取。提供真实 Git/source 内容与派生 source identity，不把 expected decision 作为事实。

### 3.3 原命令与 trace 边界

现有 `native_adapter.py` 的单最终 invoke 限制不能直接用于四步 authoring。为已声明的 standard_intake flow 在原 adapter/trace helper 内增加有序多命令协议；只转发声明的 Sync、Discovery preview/record/check/invoke、Clarification record/check/invoke、Wording scan/record/check/invoke、Readiness record/check/invoke。

该协议是 eval 内的受控命令转发，不是第二生产 wrapper。必须使用完整 trace 与命令回执证明真实执行，不让 host 根据 case 预选路由。Agent 负责公共 DTO 的薄投影，validator 只检查实际输入与前一步输出的声明映射一致；owner-private result 不跨 Skill。

成功 trace 必须证明所有四个 contract 与必要证据先读取，语义 authoring 的输入到达真实 recorder，再到 checker 和 invoke；最终输出是 Readiness 实际 public stdout。阻塞 trace 以实际 declared blocker 的 public stdout 结束，后续命令计数为零。不能强制错误路径穿过全部四个 owner。

最终消息仍由 native Agent 返回，不能把工具中打印 stdout 当作最终消息已经交付。Intake 传输指引要求 Agent 在内存解析本次实际终态 stdout，用标准 JSON serializer 缩进呈现完整对象，并核对最终回复不增删字段或括号，不附说明、围栏或截断。仅使用既有合法 JSON 空白归一化，不改输出 parser、trace/receipt 一致性校验或失败传播；不新增结果通道，不由 host 取回执代答、清洗或修复模型输出。

flow 的终止 owner 由最后一个真实 public wrapper 回执确定，runner 按该 owner 的 interface/exit schema 校验原样 stdout，不套用 corpus 所属 Readiness 的 schema，也不把 Clarification blocked 包装成 Readiness blocked。eval-only trace 绑定 terminal producer identity；生产 DTO 不增加字段。当前 Skill/consumer 图规定有序边与 stop，adapter 只校验这组事实，不另建决定 pass/block 的 router。该 flow 的声明 case-id 集合继续纳入 full-run aggregate 完整性检查。

Wording 的 step-local 合同明确原 checker 响应与其 validation_receipt 字段的区别：保持完整 record/check 输出在当前 owner 内存，invoke 只原样取实际 checker_response.validation_receipt。若仅 invoke 封装错误且 review/source/result 仍 current，修正封装后再次调用原 invoke，不把已成功的 checker 当作失败步骤重跑。事实或 result 变化仍回原审查/record/check；不改 schema、runtime、harness 或错误门禁，不提供 owner/pass 样例。

expected-versus-actual exit 比较只在 runner 控制侧进行；语义充分性由独立 AI 阅读 native transcript 与所用 authority 审查。命令次序、字段一致或关键词出现均不能独立形成 semantic pass。

两个 Intake case 必须声明 `evidence_selector=transcript` 的 semantic assertions。首次在新 run-root 执行时不提供评分；即使结构项全通过，缺少 external semantic grading 仍必须是 evaluation_failed，不能把空 semantic_results 当作成功。

只有声明 `native_authoring_flow=standard_intake` 的 case 行可进入 completed-run 两阶段补评分。focused 和包含 Intake 的完整 full/mixed run 均必须保持首次执行的完整 applicable case/side 集合；先严格验证完整 aggregate identity，再只更新 Intake 行的 semantic results/status。grading 恰好覆盖该运行的 Intake case/side/assertion 集合，non-flow assertion 或多余行一律拒绝。所有 non-flow 行的 execution、actual exit、deterministic/semantic results、status、timing、顺序及原始证据不变，仅重新计算整个 aggregate status。普通 post_owner、Architecture、Phase 2、qualification 的 fresh/saved 原行为不变，不新增通用 saved-run 生命周期。

独立 AI 现场读取该次完成执行的 Intake transcript、source facts 和原命令回执后，生成现有 schema 1.0 评分。使用同一原 run-skill-evals 入口、相同 selection/run-root 与既有 --semantic-grading 参数消费评分，先核对完整 case/side identity、Intake assertion、corpus、调用身份及保留的执行证据，不重跑模型，不改原始 transcript/trace/receipts，只更新 Intake semantic_results/status 与派生聚合。缺失或不匹配的执行必须停止；execution_error、unsupported 或确定性失败不能被评分覆盖为通过。不得为完成 full aggregate 而伪造 non-flow 通过或丢弃其失败行。

既有 grading schema 不含完整 transcript 字节身份；本任务不新增字段或解析 summary 中的隐藏协议。绑定来自同次执行定位、现有身份一致性检查和现场独立审查，不声称具有新增逐字节评分绑定。新执行必须使用新 run-root，不复用本轮之前的 native 或 Phase 2 结论。

## 4. 成功与阻塞样例

- 成功样例：live fixture 需求完整、无 duplicate 决策争议、无 wording 修订、无 scope 冲突；同一 native Agent 产出四步正式 public outputs，到 ready 停止，不执行 workspace。
- 阻塞样例：真实需求正文同时要求互斥的交付范围且无优先级，不能由仓库事实消解；Clarification owner 必须指出未决产品选择并返回 declared blocked，绝不预填用户答案或继续下游。
- 已有维护失误回归继续证明 stale/mismatch/schema 与缺正式前置结果的 fail-closed。测试只使用受支持入口和普通维护错误，不增加威胁或非常规故障模型。

## 5. 分发、规模与回退

canonical Skill 和 eval assets 经原 preset 分发到 dogfood installed 与声明平台；不得仅 patch 安装副本。运行 `apply.sh --repo . --all-platforms` 后检查 managed bytes/mode、overlay drift 和本任务 residue。

当前读取的 native_adapter.py 为 1157 行、owner_staging.py 为 693 行、stage0_fixtures.py 为 1268 行，runtime/tests/test_runtime.py 已有 2820 行。新增链路专属事实/trace 逻辑保持测试层内聚，新增成组测试置于独立 test_intake_semantic_authoring.py；触及文件达到 3000 行时先做有界机械拆分，不借机重构生产 runtime。

回退为撤销本任务源码与 eval-only 声明后重新应用同一 preset；无数据迁移、生产新状态、双读或长期兼容路径。旧 post_owner fixture 保留其仍有 consumer 的 serializer 验证责任，但不得作为 A1/A2 证据。

## 6. Architecture 与 Docs 边界

设计判断为 `no_architecture_impact`：四个生产 semantic owners、single writer、public I/O、外部集成、持久化与生命周期均不变。eval flow 扩展只落实既有验证职责。Architecture Planning owner 必须 fresh 核对 current baseline、constitution 和 change contract 后给出正式结果；本段不是替代该结果。

若实现需要生产 owner/协议变更、新 shared authority 或跨仓能力，停止并重入规划。Docs SSOT Plan 只引用 [prd.md 第 7 节](./prd.md#7-docs-ssot-plan)，本文件不复制其决策表。
