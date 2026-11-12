# D1：两类资格确认的正式 context 循环

## 1. 整体来源与术语

本批 DeliveryKey 为 `{task_id:811-qualification-context-continuation,lifecycle_generation:0,delivery_id:32f655a1-8b8e-4f02-94a0-7cf74fc39a6e}`。
`planning_root=deliveries/32f655a1-8b8e-4f02-94a0-7cf74fc39a6e`。
整体 authority 为本 Task [根 PRD](../../prd.md)，accepted_scope revision 为
`sha256:d244135d4117070f697a4e7f342369f22dc6c868d379b80b9878ea8d31035cf9`。
本批 scope_ref 选择 R811-01..07、AC811-01..08，整体定义和术语由根 PRD 单写。

| 来源 | 角色与本批用途 |
| --- | --- |
| [live #811](https://github.com/castbox/guru-trellis/issues/811)，完整正文 | Direct Source 要求，采用 2026-11-12T13:06:20Z 正文。两类确认、三种 context 状态、旧四类与本项独立正常 Task/Delivery 接续验收全部承接。 |
| 根 PRD 第4..7节 | 已接受整体要求；本批展开真实入口、差额和验证边界。 |
| `.trellis/spec/workflow/skill-package-contract.md`，完整公共 package 合同 | 规范性约束：最小 I/O、target-owned projection、版本迁移、原 producer 出口与受管分发。历史节只保历史含义。 |
| 两个 qualifier、Clarify、Discovery 的 current Interface/schema/runtime | 当前代码事实及迁移起点；具体设计处置由本批 design 第3节独占。 |
| 当前协作边界 | 保留同一 Task/gen0/D1、B 和有效工程事实；每次 merge 前交协调方处置。 |

这里的 context 是业务流程上下文，不是官方会话 context key；两者的获取与身份校验责任不能混淆。

## 2. 整体与本批目标、非目标

本批独立交付目标是修复 qualifier→Clarify→Discovery→Clarify→原 caller 的正式循环。
normal 和 solution 的确认均保留当前 candidate_refs、mode、target、Task/Delivery、continuation、resume consumer。
Task target 与来源 Issue authority 分别明确，缺失/普通过期 context 能从原 producer 获取和刷新。

D1 承担完整 R811-01..07 的实现、兼容、分发和验收，不预留实现责任给 D2。
AC811-07/08 中必须在业务交付之后执行的整体 Completion、Closure、Finish、main 可达性与资源处置，
仍是本 Task 后续原 owner 的义务；它们不是“业务 PR 创建前已经关闭 Issue”的循环前置。

非目标沿根 PRD 第3节：不绑定特定发布对象、版本或发布时间，不实施后续 Issue、不扩大完整发布矩阵，
不新增授权存储/审计链、第二路由或对抗与非常规加固。

## 3. 本批起点、前序结果、依赖与剩余责任

这是本 Task 首个 Delivery，没有本 Task 前序交付。固定 development baseline 与当前 H0 均为
`ca0b21f0dfc754a6979f919be14deee696719a4b`；PR target 为 `main`，两者职责不同。
#812 的业务 merge `4c30d5a90903996cfb2f65d0b973e53be1ae3067` 和归档 merge `ca0b21f0d…`
已包含在该 baseline。原 explicit-task 入口继续适用，不重做身份修复。

固定 B 的起点事实：Discovery `context_request` 2.0 与 `context_ready` 5.0 只承接旧四类返回；
Clarify invoke 明确拒绝两类确认的 `needs_context`。其 clear 又要求匹配的 context_current。
Discovery 把 live authority identity 直接作为 target，无法在 Task target 与来源 Issue 不同时返回。
现有 qualifier scope-confirmation DTO 有候选/目标/continuation/resume，Task/Delivery 目前由原 caller 在调用期保留。
这些事实构成本批差额，不能靠改写旧 transition 或预填 producer 结果解决。

本项使用独立、受支持的正常 Task/Delivery 场景验证同一工作接续，不依赖外部发布 Task。
五包实现、本 checkout 的 matching 工具采用和定向工程验证已经发生，实际结果及失败截止由配对 Test 单写。
本轮仅局部刷新验收与依赖；原 Check owner 仍须按当前验收判断证据充分性，既有工程事实不自动成为质量通过。

## 4. 本批调用方、场景与流程

| 本批场景 | 前置和动作 | 可观察结果 |
| --- | --- | --- |
| D1-N-CURRENT / D1-S-CURRENT | 原 caller 得到 normal/solution 的真实 scope_confirmation_required，持有该对象的真实当前 context | 原 Clarify 完成确认，正式 clear 返回同一 caller；不重复 qualifier 的准入判断。 |
| D1-N-MISSING / D1-S-MISSING | 同上，没有匹配 context | 原公共 context 请求进入 Discovery；其真实 context_ready 重建原确认输入，再正式 clear 返回，不手填被测 producer 输出。 |
| D1-N-STALE / D1-S-STALE | 通过正常来源更新或原合法对象演进使原 context 过期 | 原 owner 先拒绝旧事实/刷新所需上下文，经同一循环返回；不局部改 hash、target 或 continuation。 |
| D1-OLD-FOUR | 原 standard/reviewed/active/standalone 合法调用 | 成功、缺失/刷新与身份拒绝仍按原合同；原 source_locators、task/standalone resume 语义保留。 |
| D1-INDEPENDENT | 原入口已建立本项独立正常场景的合法 Task/generation/Delivery，caller 持有实际确认对象 | 两类真实 qualifier 公共输出经原 context producer 和正式 clear 回原 caller并实际消费；保场景内同一工作身份，不指定发布 Task，不捏造未决选择。 |

工程回归和实际 Agent/caller 观察分别陈述。测试 fixture 可建立 declared boundary 之前的 Task/Delivery/来源，
不能代替该 boundary 内的 qualifier、context producer 或 clear 输出。

## 5. 完整行为、条件与约束

- **D811-01 → R811-01/03**：两类确认均使用原 stable Skill 与真实公开入口。Clarify 只处理原 qualifier 交来的具体 authority 选择，context producer 只负责证据获取与返回，原 caller 消费结果继续其当前义务。
- **D811-02 → R811-02**：整个循环保留原候选、Task/Delivery、mode、target、continuation 和 resume consumer；区分 Task target 与实际来源 Issue/合法无 Issue authority。不能从项目 inventory 猜 Task/Delivery，也不能借用其他会话绑定。
- **D811-03 → R811-01/02**：当前 context 走正常确认；缺失与正常过期 context 走可执行的原 producer 获取/刷新路径。freshness、来源与匹配检查继续生效；真实缺权威或身份冲突保留 fail-closed 与原 owner 恢复。
- **D811-04 → R811-04**：旧四类返回和原 Skill/exit ID 保持。封闭 I/O 的实质改变使用 successor path/$id 与明确迁移；旧发布 schema/example 字节保留，原在途操作使用匹配完整 provider，不能给旧结果补字段冒充新出口。
- **D811-05 → R811-05**：AI 判断与脚本事实分层，不持久化授权或过程，不新增 qualifier checkpoint/审计 store。public output 字段只服务直接 consumer，producer 私有结果不能泄入 context handoff。
- **D811-06 → R811-06**：canonical、受管 installed、shared/Codex、Claude、Cursor 及实际声明投影同步；原 tools owner 保留 Task/session、用户改动与 provenance，处理实际 sidecar 后验证。
- **D811-07 → R811-07**：本项独立正常 Task/Delivery 场景完成真实公共链接续，fixture 语义输入与真实 producer/caller 输出分别陈述，不额外要求实际 Agent 或远端业务证明。#811 按自身要求完成交付与整体收尾，不绑定特定发布；merge 前均交协调方，Git/GitHub 副作用保留原边界。

来源设计约束已在第1节定位，具体 retain/change/reject 和落点只在本批 design 第3节维护。

## 6. 本批验收、验证方式与未决项

| 验收 | 对应行为与验证入口 | 预期结果及证据边界 |
| --- | --- | --- |
| AC811-01/02 | D811-01..03；两 qualifier 公共 invoke→Clarify→真实 Discovery→Clarify clear→原 caller | 六个行为不同的 context/profile 场景均取得正确接续；完整链不预填 producer，保留对象及来源关系。 |
| AC811-03 | D811-04；旧四类实际公共入口/投影回归、旧新 schema 及正常 mismatch | 原成功与拒绝语义保持；版本不能混用，错误有原 owner 恢复。 |
| AC811-04 | D811-01/05；检查测试实际 setup/call/observation 并执行目标回归 | fixture 不替代被测 producer；record/check、static、integration 与真实 Agent 证据各自成立。 |
| AC811-05 | D811-06；原 tools 更新与 source/installed/drift/sidecar 定向检查 | canonical 和实际安装一致；未做完整矩阵不称通过。 |
| AC811-06 | D811-07；D1-INDEPENDENT 的原公开调用链和 caller 消费 | 两类确认保持场景内同一合法 Task/generation/Delivery，从真实 qualifier 输出到正式 clear及原caller后续消费；不预填 producer结果、不捏造未决范围，不指定发布对象或时点。 |
| AC811-07/08 | 全部；原 Check/full_review/readiness、交付及整体 lifecycle owners | 实现与证据覆盖完整范围，独立已提交审查成立；交付后整体判断、关闭、归档、资源处置和 main 可达性实际完成。 |

需求层没有未决产品选择。既有 schema/薄投影机制保留；独立 Architecture 按本轮验收和依赖差额评估，
原 Author 随后局部刷新 design/implement。独立公共链的组合证据由原 Check owner 判断；其余未验证边界沿根 PRD。

## 7. Canonical 引用与本轮差额

- Requirements/Design/Test：`docs/{requirements,design,test}/current/local-fix-intake.md` 的 R692/D692/T692 保留原 owner、当前事实适用与错误恢复。本次明确迁移其“将 live Issue 当作 context target”的适用边界，不改其他诊断类别或增加 live provider 自动比较。
- qualifier 应用与显式身份：`docs/{requirements,design,test}/current/qualifier-applicability.md` 的 REQ/DES/TST-793/812，复用条件准入及显式 key 校验。本次只补 context 确认返回，不修改已交付三 qualifier 分类含义。
- Architecture：`docs/architecture/03-domains/workflow-context.md` 的 ARCH-CONTEXT-001，以及原 baseline/constitution/change-contract。保留唯一 graph、原 producer 恢复和 matching 分发；本次差额是两类确认的正式 context I/O 与 Task/来源关系，不新增第二 authority。
- 框架：`.trellis/spec/workflow/skill-package-contract.md`、`workflow-contract.md` 的 Candidate Applicability/Interaction Budget，及 `quality-guidelines.md` 的 Test And Validation Value/Validation Scope Ownership。完整公共 package 合同已读；实际验证和晋升由原 owner 完成，不预填结果。

这些当前知识需由原 RDT/Architecture owners 在本批选定 Docs Plan 下维护完整正文和真实关系；不直接改共享导航、不制造空贡献或每轮审计文件。
