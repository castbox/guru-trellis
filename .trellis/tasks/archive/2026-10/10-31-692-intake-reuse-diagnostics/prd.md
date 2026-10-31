# #692 局部修复 Intake 与身份诊断整体需求

## 1. 来源与术语

| 标识 | 来源与章节 | 角色与用途 |
| --- | --- | --- |
| SRC692 | [Direct Source #692](https://github.com/castbox/guru-trellis/issues/692)，背景、当前差额、四项行为要求及非目标；本轮读取时更新时间为 2026-10-30T13:58:05Z，评论为空 | 整体需求 authority。完整行为、条件和边界均须承接。 |
| REQ692-RUN | 当前用户请求：按正常完整 Guru 流程实现并关闭 #692；串行次序 #695 → #694 → #693 → #692 | 执行范围与验证约束。不把前三项成果重复计入本项。 |
| HIST372 | [业务案例 #372](https://github.com/castbox/guru_ai_roleplay/issues/372)，仅采用 SRC692 中的脱敏历史时间线 | 历史案例；不是业务实现、Task/会话写入或现场根因确认 authority。 |
| BASE692 | main `6a65ec8afe6d180850760b3b2edf3f94be6e3b20`；当前 canonical workflow、selector、Discovery、Clarify、Author 与测试 | 当前实现事实。此前三项已 live CLOSED/completed；新合入 #706 的审核方法由后续原审核 owner 承接。 |
| CONTRACT692 | `trellis/presets/guru-team/spec/workflow/workflow-contract.md` 的 Interaction Budget；原 Skill 各自合同；`docs/architecture/00-foundation/design-constitution.md` | 约定职责、freshness、正常场景、独立副作用与最小必要复杂度边界。 |

Intake 指 selector 后的 Sync、Discovery、Clarify、Wording、Readiness 与原创建入口。Task 承担整体 accepted scope；Delivery 是其内独立交付切片。调查事实可否继续使用由当前原 owner 判断；旧 target 的 pass、私有 producer 结果和摘要不自动成为当前判断。

## 2. 背景与问题

SRC692 的历史快照显示：业务请求在草稿转正式 Issue、Task/Delivery 规划及一次内容读取不一致恢复中经历多轮处理。截至快照结束，业务修复和失败测试尚未观察到。快照同时包含必要调查、等待、基线阻塞和读取错误；没有可靠净耗时分类，不能归因全部时间或宣称节省分钟数。

当前已有按范围和风险选路、自动 mapped 恢复、fresh Sync/Intake、最小 authoring 与 `code/field_path/remediation`。#695 已改善 JSON 载体与读取层，#694 已改善独立 Architecture 显式对象入口，#693 已改善合同承接和证据判断方法。本项不从零重建这些能力。

剩余差额有两类：原 owner 尚需把局部修复中可继续使用的调查事实、必须重读的差额、须重做的判断及下一 consumer 说清；Discovery 的实际复合一致性检查和公开链仍存在整体字段或收窄错误细节，普通恢复难以定位应刷新哪类 evidence。具体代码路径和兼容方案由 Delivery 规划列明。

## 3. 目标与非目标

目标：保持现有全部原子能力，在原 owner 内减少有依据的重复调查、装配、审查与例行确认，并改善普通身份/内容不一致的定位和恢复说明。

本 Task 同时承担路线与诊断的完整交付、适用分发、正常开发验证、独立审核，以及真实 Completion/Closure/Finish。Delivery 合并不替代整体完成。

非目标：业务 #372 修复；业务实现、测试、数据、Task/Delivery、原聊天或工作区写入；价格、扣费及支付协议；新 Issue、release 或 tag；所有 Skill 诊断重构；额外审批链、跨 Skill digest authority、长期审计缓存；攻击、故意篡改、并发压力、TOCTOU、锁和 crash consistency 加固。

不新增专项回放、A/B、native eval、固定案例数量、耗时测量、额外安装或完整多平台矩阵。

## 4. 真实调用方、场景与流程

| 场景 | 调用方、前置与触发 | 要求行为与可观察结果 |
| --- | --- | --- |
| SC692-01 局部修复选路 | 尚无相关 formal Task；Agent 收到局部修复请求并取得当前范围和风险证据 | 原 selector 按实际影响判断路线。购买提示不自动等于支付核心变更；表面 UI 也不自动等于低风险。证据不足只处理必要真实选择。 |
| SC692-02 草稿成为 Issue | 原 Issue 创建成功；新的正式身份和完整 live 正文可读 | 由原 Sync/Intake owner 读取新身份、正文和实际差额，审查调查事实当前适用性，向下一 consumer 提供当前有效结果。不得复制旧 target pass 或伪造 producer 输出。 |
| SC692-03 正式 Task/Delivery 规划 | 已有真实 Task，整体来源明确；原 Author 进入整体或切片写作 | 保留各自需求、方案、执行和接受责任。按实际来源和范围差额减少重复调查、装配或审查；不能通过新身份或切换模式绕过生命周期。 |
| SC692-04 普通构造/输出读取恢复 | JSON 已成功读取；Discovery record/check/invoke 接收到普通不一致内容或身份 | 在确定性可判定范围内定位实际字段或 evidence 类别，说明重读对象、原恢复 owner 和支持的重入入口；旧绑定仍拒绝。不从 digest 差异猜测 UTF-8 根因。 |
| SC692-05 外部事实变化或新副作用 | 正文、base、目标身份或真实范围发生变化，或下一操作引入独立副作用 | 原 owner 判断受影响范围并执行当前 freshness/re-entry；真实 scope/authority 选择与资源、commit、发布、merge 等边界分别保留。无变化且无新增副作用的 mapped 恢复自动继续。 |

## 5. 行为要求

### R692-01 按实际影响选择路线

复用现有 selector 与执行 owner。对无相关 formal Task 的请求，按当前证据判断改动范围、风险和验证需要；不得用 Issue 存在、文件数、路径、购买关键词或 UI 表象独立选路。已有 Task 保持其身份与生命周期。真实范围或风险变化回现有 owner 重判。对应 SC692-01/03/05。

### R692-02 明确复用与重审边界

调查案例中的路线选择、草稿转正式 Issue、Task/Delivery 规划及普通恢复，区分必要调查/gate、重复装配和重复确认。每个实际受影响环节由原 owner 明确触发条件、必须重读/重审的内容、仍适用的调查事实与下一 consumer。

草稿转 Issue 必须读取正式身份、完整 live 正文和实际差额；以现行 fresh Sync/Intake 为兼容起点。原规划 owner 按证据决定如何减少重复工作，不预先固定完整重跑阶段集合，也不预授权跳过。改变跨 Skill 重入合同必须明确差额、受影响 consumers 和兼容或迁移。旧 target pass 与 producer 私有输出不能直接复用。对应 SC692-02/03/05。

同范围普通恢复、mapped exit、stale/re-entry 不新增例行继续问题。必要语义判断、真实选择、身份/freshness 和独立副作用边界不删减。当前对话已明确请求的同一动作不重复索取确认；授权及其过程均不持久化。

### R692-03 限定诊断入口与类别

从 Discovery 公开 record/check/invoke 链及实际共享校验定位修改范围，不扩展到全部 Skill。Delivery 设计须列出实际入口、每类问题现有诊断、具体不足、恢复 owner，并明确实际触及的正文、base 与目标身份变化路径。未触及类别保留原合同。

普通输出读取造成内容不一致时，校验在可判定范围内指出实际不匹配字段，或明确应刷新的 evidence 类别；说明重新读取什么、返回哪个原 owner、通过哪个原支持入口重入。仅能确认内容绑定不一致时，不得断言 UTF-8 解码是根因。保留现有错误合同；必要细分须同步真实 consumers、错误声明和调用说明。不强制新增 code，不输出正文、敏感值或原始字节片段。对应 SC692-04/05。

JSON 尚未成功读取时，由 #695 已交付的读取层处理，不统称 stale_identity。正常 recorder/executor 缺陷、普通 stale/mismatch 仍属于 correctness 范围；不增加防故意伪造机制。

### R692-04 职责、兼容与分发

Markdown/AI 继续负责风险、路线、证据充分性、语义判断及恢复；脚本只读取事实、验证一致性和执行确定性动作。通过 canonical workflow/Skill/runtime 与 preset 修改，同步 dogfood 和实际受影响声明平台。公共 I/O、typed exit 如需变化，必须说明兼容或迁移。

不新增通用审批链、跨 Skill digest authority 或无直接 consumer 的长期证据。保留 secret redaction、身份/freshness 拦截和副作用边界。沿原开发、Check、Review 和适用升级流程验证，不把 skipped/环境阻塞写成 pass。公共源码、dogfood 与外部安装采用分别说明。对应全部场景。

## 6. 约束与依赖

直接来源只为 #692。#695/#694/#693 已完成的公共能力是当前起点，成果不重复计入本项；任何真实共享 consumer 依赖按实际协调。本次无新的产品范围选择。业务案例与原聊天只读，缺失历史证据不得补写为已确认事实。

TaskId 为 `692-intake-reuse-diagnostics`，generation 0；后续修复、重试及恢复保持同一身份、Delivery、分支和工作树。代码、测试、Task 文件的每次写入前验证实际 checkout boundary。canonical 是长期来源，dogfood 是受管副本；既有安装通过匹配完整 preset/升级路径更新，源码修改不证明外部采用。

项目 authority 通过 `docs/{requirements,design,test}/README.md`、`docs/architecture/README.md` 及其完整适用正文定位。具体 Docs SSOT 策略、Architecture 影响、兼容及执行方案属于原 Planning/maintenance owners。无业务 API、数据库或支付协议变更需求，因此本 Task 不增加这些迁移职责。

## 7. 可观察验收与验证方式

| 验收 | 对应要求/场景 | 原验证入口、输入与预期观察 |
| --- | --- | --- |
| AC692-01 | R692-01；SC692-01/03/05 | 在原 selector/执行合同中核对实际影响判断和既有 Task 路由；不得以关键词替代判断，既有原子能力及 identity 保持。 |
| AC692-02 | R692-02；SC692-02/03/05 | 通过原 owner 的实际合同及正常 Planning/Check/Review，核对各受影响环节的触发、fresh 读取、仍适用事实、重审判断和 consumer；确认有具体减重差额，未复制旧 pass 或静默删门禁。 |
| AC692-03 | R692-03；SC692-04/05 | 在设计列明的 Discovery 原公开入口和实际共享验证处，用正常来源读取/构造不一致及正常外部变化观察字段或 evidence 类别、重读对象、恢复 owner/入口与原拦截；不根据摘要猜根因，不回显正文或敏感值。 |
| AC692-04 | R692-03/04；SC692-04 | 原 JSON 读取层与内容/身份层分工保持；受影响 code/field/status/错误形状、schema/catalog/consumer 和调用说明一致。正常一致输入仍可通过原链。 |
| AC692-05 | R692-04；全部 | 沿现行定向 package/runtime、source/installed、声明平台投影、mode、reapply/drift、sidecar 与适用升级流程验证；fresh Check、独立 Branch Review 和 PR readiness 覆盖实际最终范围。不得新增专项回放或扩大矩阵。 |
| AC692-06 | 整体范围 | 所有 satisfying PR live MERGED，reviewed/merged identity 对应且可达 live main；Issue live CLOSED/completed；Completion、Closure、Finish、归档和资源处置完成或说明非阻塞；明确真实验证边界。 |

这些是验收要求，不是已经执行或通过的结果。实际测试策略和唯一结果落点由选定 Delivery 的实现计划及原 RDT owner 定义。

## 8. 实际未决项

无阻塞整体需求写作的产品问题。具体实现差额、字段粒度、原 consumer 兼容和事实复用方式由 Author/Architecture 在 Delivery Planning 中决定，不能要求提交者先提供实现设计。

非阻塞证据边界：未取得业务案例当时安装快照及完整原聊天；当前版本不证明其当时行为；业务根因运行时验证与可节省时间未知。外部安装与完整多平台/Release 证据不由源码或定向检查推定。
