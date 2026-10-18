# #154 D1 实施与验证计划

## 1. 输入、范围与引用

整体范围由 [Task PRD](../../prd.md) 和公共 accepted_scope 承载；本批需求见 [PRD](./prd.md)，方案、唯一来源设计处置和验证设计见 [design](./design.md) 第3、8节。D1 全量覆盖 R1–R7、V1–V7、AC1–AC10。当前仅完成规划正文，不宣称实现或验证通过。

实施前实际加载 `.trellis/spec/workflow/clear-technical-writing.md`、`.trellis/spec/workflow/quality-guidelines.md`、`.trellis/spec/workflow/subtraction-first-compatibility.md`、`.trellis/spec/preset/upstream-ownership.md`、`.trellis/spec/workflow/skill-package-contract.md`，以及 design 定位的当前 requirement/design/test 与 Architecture authority。原官方 JSONL 只记录实际 file/reason，不能替代加载或充分性判断。

## 2. 实施顺序、文件责任与依赖

| 步骤 | 责任与文件 | 操作和可审核产物 | 依赖及完成观察 |
| --- | --- | --- | --- |
| I1 | 原 Author package；`trellis/skills/guru-team/packages/guru-author-task-plan/{SKILL.md,references/authoring.md,references/planning-body.md}` | 写共享正文合同、按九 profile 明确加载适用模板；保留唯一 writer、阶段边界和原 exits。 | 从当前文件与实际消费者出发；scope-only 不要求未来方案，solution 在 plan_ready 前补齐。 |
| I2 | 同 package 的 `templates/` 与 `examples/planning-body/{detailed,brief}/` | 按 design 第4节写四模板和两组完整去敏过程示例，包含输入、调查/澄清、切片、四类正文和具体审核修订。 | 依赖 I1；AI 逐项审语义和裁剪，不以关键词/文件数通过替代。 |
| I3 | 原 Clarify、Wording、Approval、Check、Delivery Review、Completion packages 的 SKILL/reference；Guru workflow 实施 dispatch | 指向同源正文合同；各 owner 在原范围内核对当前正文、来源和必要引用；普通遗漏走原回程。Architecture 保持原独立合同，必要引用不能让其首轮预载 PRD/验收。 | 依赖 I1/I2；无新 Skill、出口、DTO、审计或 generator/hook/官方 agent 改动。 |
| I4 | canonical workflow、preset/workflow README 与必要 overlays；现有 preset apply | 说明真实加载与完整匹配版本采用；运行 canonical apply 同步 dogfood，核对 declared platforms、sidecar 与用户内容。 | I3 后；仅改变真正需要的定位，不复制 step-local 规则，不自动修改业务仓。 |
| I5 | 原实施与审核 owners；一个代表性 Codex installed 环境 | 按第3节真实执行 V1–V7，Agent 自行调查、写作、审核、修订；将证据与机械结果分列。 | I4 后；宿主不预写最终文档/pass；真实选择与前序事实缺失时保留相应 gap。 |
| I6 | 原 RDT / Architecture owners；任务独占贡献及既有 shared authority | 写真实差额和唯一 Test；独立实施阶段 Architecture 审完整候选后，由原 owners 在最终 Phase 2 前 reconciliation/promotion。 | I1–I5 的实际变化与证据已可审查；晋升新 diff 纳入最终 Check/commit/独立完整 Review。 |
| I7 | 原 Check / TaskCommit / Branch Review / Delivery Review / Completion | 原范围完整质量检查，核对 R1–R7/AC1–AC10；按后续实际结果处理发布与整体完成。 | 当前不执行 Git/GitHub 写入；这些动作有各自副作用边界。任何未验证场景保持未通过。 |

主会话协调与更新规格；实施/check 由 Trellis 对应子 Agent 执行，子 Agent 实际加载本规划与官方 context。Architecture 新评估使用其合同要求的 fresh generic reviewer，不能由已暴露需求叙述的 implement/check worker 代替。

## 3. 实际验证入口、输入与预期结果

### 3.1 Agent 场景

使用当前支持的 Codex 原生会话/Agent 能力，运行完整匹配安装中的原 Planning owners。开始先核对 installed provider、实际入口及模板路径；原 wrappers 只在 AI 作出判断后调用。详细步骤和字段见 design 第8.1节、PRD 第4节。

| 场景 | 执行入口与关键输入 | 预期观察和停止条件 |
| --- | --- | --- |
| V1 | 原 intake → task_scope_requirements → Clarify accept_scope → Delivery Creation/Author/candidate Architecture/solution/Wording/final Architecture/Approval；输入详细技术来源。 | Agent 实际读取条件、例外和已约定设计；四正文成文、来源设计逐项落地。缺一项则原 owner 修订，不由宿主补造结果。 |
| V2 | 原 Discovery/Clarify/Author；简略 Issue + 可调查仓库事实。 | 留下实际调查和必要澄清；无产品缺口时不制造问题。若真实问题待答，等待真实用户，不能编造答案。 |
| V3 | 同一无 Issue 支持入口；当前请求而非预制 PRD。 | 形成完整需求/方案，遵守原 mode/Task 及阶段规则；没有规范性来源设计时说明依据，无空矩阵。 |
| V4 | 原 Clarify 来源处置 → Author；多来源含真实分歧、建议与历史事实。 | 原承诺保留；冲突由正确 owner/真实用户处置。未解决真实选择不能计通过。 |
| V5 | 原合法 partial Delivery → 原支持的后续 Creation/Planning，读取实际前序结果。 | 两批目标、上下文、设计差额、剩余责任和 Completion 条件可核对；缺正常前序 producer 路径时保留缺口，不手写 delivered。 |
| V6 | 原来源更新/返工 + 新原生 Codex 会话的 Bind/Selection/continuation。 | 同一 TaskId/generation/DeliveryKey，读取当前适用模板/引用，仅重做受影响阶段。仅 DTO/schema 演示不能证明新会话行为。 |
| V7 | 实际 Agent 草稿或正常入口支持的未完成规划 → 原 reviewer → Author revision。 | reviewer 指出具体遗漏，Author 实际补齐并重审；不得篡改已接受 artifact 或预填 pass。 |

在同一验证环境覆盖简单工程裁剪与复杂设计深度。保存实际平台日志 locator、模板路径、最终正文、具体修订及结果到唯一 Test 的必要证据引用；不新增过程 ledger 或 tracked 审核流水账。不能把本次 #154 旧合同下的 Planning 自动计作新合同验证。

### 3.2 确定性与安装检查

以下命令从仓库根执行，参数以当前脚本 help/合同核对。每项预期退出成功；失败先判断真实原因，不删掉失败项以冒充通过。

| 检查 | 入口 | 输入与预期观察 |
| --- | --- | --- |
| source packages | `trellis/workflows/guru-team/scripts/bash/check-skill-packages.sh --root . --mode source --json` | 最终 canonical packages；公共接口/引用/投影合法，正文没有被误排为私有文件。 |
| upstream ownership | `trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json` | 受影响全 diff；无上游 seed/generator/hook/official agent 越界。 |
| dogfood apply | `trellis/presets/guru-team/scripts/bash/apply.sh --repo .` | 同一最终 canonical；同步原安装副本。对每个 `.new/.bak` 比较并按原规则处理，保留用户内容。 |
| overlay drift | `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh` | apply 后 dogfood；无未解释漂移。 |
| installed packages | `.trellis/guru-team/scripts/bash/check-skill-packages.sh --root <target> --mode installed --json` | 完整匹配安装；四类正文资产和 consumers 引用可达。 |
| focused regression | 受影响 Author/消费者 package tests；现有用例不能检出本轮模板分发/引用或阶段边界回归时，使用现有测试 runner 新增小型定向测试 | 覆盖真实行为，不为 Markdown 低风险编辑镜像一套关键词测试。任何受影响非生成源码文件若将超过3000行，先机械拆分或小幅解耦；分发回归新增到独立 focused 文件。 |
| clean/reapply/user preservation | 官方 marketplace workflow + 完整 preset 的实际命令；一个代表性临时仓库 | 先读官方 custom-workflow/marketplace 文档与当前 README，使用当前匹配 source/provider；核对 workflow id、模板可读、reapply 稳定、用户 sentinel 保留、sidecar 正确处理。existing replacement 先 create-new 预览，显式 force 才应用。 |

临时仓库、分支或 Task 的实际创建仍由原 owner 展示精确副作用后执行；不因这是测试而绕过既有边界。验证不扩成完整跨平台升级/Release 矩阵。已有安装更新的冲突语义依据 `.trellis/.template-hashes.json` 和官方机制检查，不靠“文件未被触碰”推定新语义已采用。

### 3.3 验收消费

AC1/2：核对四类合同、profile 加载、裁剪与三个原接受边界。AC3–6/8：实际 V1–V7 的来源、切片、恢复和修订行为。AC7：本批设计/步骤/测试映射与原 Approval。AC9：各原 owner 对最终正文的语义和语言审查。AC10：source/dogfood/installed/声明平台、clean/reapply/sidecar/用户内容和代表平台真实行为分别报告。未执行、失败、缺 provider 或待用户选择均不能标通过。

## 4. 停止、返工与回退点

正文缺失或引用不可加载时，停止依赖步骤，由原 writer 修订；来源角色/范围变化回 Clarify，机制/owner/authority 扩大回原资格与 Architecture owner。普通 wording 或同机制遗漏只刷新真正受影响 gates，不重建 Task 或切片。

在 canonical apply 前保留当前 diff；只撤销本次明确文件内的错误改动，保留并行用户内容。遇到 sidecar 冲突先比较，不静默覆盖。无 DB、远程服务或持久化 schema 迁移，本批不设计服务回滚协议。若新模板方案确需公共 I/O 变化，先停止并定义迁移/consumer 适配，再进入原规划回程。

尚未取得真实行为证据时继续其他独立验证，但 Completion 保留对应 AC。Git stage/commit/push/PR/merge、资源清理和软件发布仍各归原边界，不能由本计划推导已获授权或已经执行。

## 5. Delivery Policy（唯一）

策略为 `full`。当前 D1 独立交付正文合同/模板、示例、原 owner 接入与本批全部验证。整体 accepted scope 为 R1–R7、AC1–AC10；未另分配工作 `remaining_work=[]` 只说明没有故意延期的切片，不表示验收已完成。

完成条件：实现符合正文合同、所有适用 AC 有真实证据，原 Check/Review/Delivery 与 whole-Task Completion 分别作出当前判断。单次 PR 合并、模板存在、package checker 或 Planning 批准都不能替代上述条件。发现独立新目标返回原 Clarify；不能临时改 partial 以掩盖未完成验证。

## 6. Docs SSOT Plan（唯一）

策略为 `delta_first`。原 RDT writer 在 `docs/requirements-design-test-contributions/154-planning-body-contract/` 写真实 requirement/design/唯一 test 差额，直接 consumer 为原 RDT reconciliation/promotion 和后续 Check/Review/Completion。当前命中 authority：`docs/requirements/README.md`、`docs/design/README.md`、`docs/test/README.md` 的 RDT107，以及 #250/#292/#531/#599 已接受贡献。

Architecture 差额由原 Author 编写 `docs/architecture/contributions/154-planning-body-contract.md`，原 Architecture owner 独立审查；命中基线98、constitution-v1、ADR-022/024 与 change-contract。当前无需新 ADR、GAP 或兼容 ledger。真实贡献可以在任务中形成；模板填充本身不晋升 README/index/manifest 或 spec projection。

在最终 Phase 2 前按现有合同将真实差额与长期 authority reconciliation/promotion；共享写入由原 owners 基于 expected-current 完成。晋升实际 diff 必须纳入最终 Check/TaskCommit/独立完整 Branch Review；验证结果、首次失败/修复和未验证边界只由唯一 Test 承接，不复制第二份测试权威。完整多平台矩阵、业务安装及软件 Release 继续明确为未验证/范围外边界。
