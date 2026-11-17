# #880 Issue 责任层与验收场景收敛设计

## 1. 设计目标、需求承接与内容基线

本设计承接[本批 PRD](prd.md) D1-R1–R7、D1-AC1–AC2 和[整体 PRD](../../prd.md) R1–R7。开发基线 B 固定为 `76198a53b4da989b66d2e5f135ff4d2b703ca3cf`；Planning H0 等于 B，最终内容范围为完整 B..实现 HEAD 加实际未提交增量。PR 目标为 `castbox/guru-trellis:main`。

Architecture candidate assessment 已由未读取 Task 规划的独立 reviewer 正式返回 `baseline_current / no_architecture_impact`，baseline=`guru-trellis-architecture`、constitution=`guru-trellis-design-constitution-v1/current`、change-contract=`guru-trellis-architecture-change-contract-v1`。候选复用现有 owner、Markdown 控制面、验证单一来源、既有 eval 和受管分发，没有新 public interface、runtime state、持久化、部署路径、生命周期或 approval step，因此不产生 Architecture contribution/ADR。该结论只覆盖预写候选；最终 design 仍须新的 final_plan assessment。

## 2. 当前系统、边界与目标差额

当前 `issue-content.md` 已定义结果与支撑证据、Issue 边界内最外沿验收、删除重复义务及完整正文审核；`quality-guidelines.md#test-and-validation-value` 已定义跨阶段责任、最小证据和复用；Clarify、Readiness、Create Issue 已通过薄引用消费同一内容正文；`issue-acceptance-boundary-source.json` 已有组件、显式 CLI 联合交付、消费方 E2E、重复层级和定向补证场景。

本批没有前序 Delivery。目标差额有三项：

1. `issue-content.md` 未明确组件、调用方、跨组件和目标环境责任层可以组合，也未明确普通 Issue、共享 test 部署和业务“发布模板/配置”之间的边界。
2. 现有最小充分规则主要判断单条验收和验证层级，未明确“验收场景集合”不得把同一次 Agent 行为按创建、复审、方法或阶段重复拆分。
3. 现有 eval/fixture 没有目标环境结果与业务发布动作，也没有场景集合重复的对照；现有 distribution test 还未把 `acceptance-boundary` 示例纳入受管投影检查。

本批保留已有完整规则、公共 I/O、typed exits、语义 owner、安装/升级流程和历史 Issue；不建设第二规范、评测平台或部署流程。

## 3. 来源设计处置（唯一）

| 来源 locator/条款 | 原承诺 | 处置 | 本设计落点、理由与影响 |
| --- | --- | --- | --- |
| Issue #880 R1 | 组件、调用方、跨组件和发布/环境责任可以组合 | change | `issue-content.md` 责任切面新增可组合责任层；三个原 consumer 已引用该正文，无需新增 I/O |
| Issue #880 R2 | 明确联合或目标环境承诺不得删除 | retain | 继续使用现有“边界内最外沿有效结果”和必要最小证据；fixture 增加正例 |
| Issue #880 R3 | 验收、证据、服务部署与业务发布分离 | change | `issue-content.md` 定义 Issue 侧语义；`quality-guidelines.md` 只补跨阶段责任边界，不复制 Issue 场景规范 |
| Issue #880 R4 | 验收场景按独立风险收敛 | change | 在 `issue-content.md` 的原验收切面段新增场景集合规则；现有层/方法去重规则保留 |
| Issue #880 R5 | 三个原 owner 在原门禁落实 | retain | 现有 Clarify/Readiness/Create Issue 薄引用和原 exits 已足够，不新增审批或重复正文 |
| Issue #880 R6 | RDT、canonical、dogfood、平台和安装同步 | change | 原 RDT owner 更新 current；原 installer/tools owner 同步受管投影 |
| Issue #880 R7 | 复用真实 Agent/eval，不用固定文本代替 | change | 扩展现有 acceptance-boundary eval 和教学示例，不新增 runner |
| #868 已完成边界与持续去重 | 结果/证据区分、最外沿验收、写前与后续审核去重 | retain | 仍为完整基础；本批只在原段落展开责任层与场景集合，不改 owner/public I/O |
| `quality-guidelines.md#test-and-validation-value` 当前责任边界 | 跨阶段停止外推、最小充分、证据复用 | retain/change | 保留全部现有规则；仅补目标环境/共享环境/业务发布区分的跨阶段表述 |
| 现有 acceptance-boundary fixture | 组件和 CLI 联合交付、消费方 E2E 拒绝、内部承诺补证 | retain/change | 保留原证据与断言，新增目标环境正例、业务发布非部署与重复场景负例 |
| 现有 distribution tests | 真实 writer/reapply、平台 bytes、用户保留、sidecar | retain/change | 复用真实安装器；把已存在但未纳入的 acceptance-boundary 示例加入检查 |

没有 reject 的规范来源。Issue #826/#747 仅作真实 Agent 方法建议，不要求整项完成，也不写入产品合同。

## 4. 模块、职责与设计取舍

### 4.1 Issue 内容规范

修改 `trellis/skills/guru-team/packages/guru-clarify-requirements/references/issue-content.md`：

- 在“验收切面与必要结果”中增加责任层可组合、目标环境结果、共享环境验证、服务部署和业务发布操作区分。
- 增加独立风险场景集合规则：一个场景可含多个条件；同一行为不因创建、复审、验证方法或阶段重复；其他入口只有必要差异才增加场景。
- 保留现有结果/证据/无依据义务分类、原 owner 表和完整审核规则。
- 更新 `examples/issue-content/acceptance-boundary/process.md`，用同一去敏场景覆盖目标环境与业务发布正反例。

选择在原段落内展开，因为现有规则已经拥有相同责任边界；新增第二文档会产生双 writer 和 consumer 歧义。预计新增成本为每次原 owner 读取必要规则和判断场景独立价值，不增加持久状态或额外调用。

### 4.2 跨阶段验证规范

修改 `trellis/presets/guru-team/spec/workflow/quality-guidelines.md#test-and-validation-value`，只在原责任边界小节补充：

- 目标环境/共享环境验证属于相应部署/发布责任，只有有效需求或仅该环境可判断时才需要。
- 业务对象“发布/同步配置”不等同服务版本部署。
- 额外验证仍是替代证据；场景集合的 Issue 专属定义由 `issue-content.md` 拥有。

`review-sufficiency.md` 继续薄引用同一小节，不新增审阅阶段或 per-test 理由。

### 4.3 原 owner 与 eval

Clarify、Readiness、Create Issue 继续使用现有薄引用、完整正文检查、`clarify_requirements`/`refresh_review` 回程；本批不为形式重复改所有 Skill。扩展 `issue-acceptance-boundary-source.json`：

- 有效来源明确 page CLI 在目标 runtime 版本读取既有配置，保留目标环境结果。
- “发布分页配置”是业务命令，不属于服务部署。
- 普通审核意见建议逐 Issue 部署共享 test 环境、真实业务应用 E2E，并把创建、联合、复审、验证方法各列为场景；这些候选不具独立有效依据。
- 现有组件/CLI/内部 load 时机证据继续复用，不用固定文本或分发成功替代语义判断。

### 4.4 RDT 与分发

新增 task-owned contribution `docs/requirements-design-test-contributions/880-issue-responsibility-acceptance/`，保留本批 R/D/T proposal、traceability 与 proposed targets。实现和工程结果完成后，由原 RDT owner 将真实差额整合到 `docs/requirements/current/issue-content.md`、`docs/design/current/issue-content.md`、`docs/test/current/issue-content.md` 及 behavior-validation 三个 current 文档。

受管 dogfood 由原 `guru-upgrade-tools` 以完整 matching source 同步，不手工覆盖 `.trellis/`、`.agents/`、`.claude/` 或 `.cursor/` 投影。`test_issue_content_distribution.py` 将 `acceptance-boundary` 示例加入真实 writer/reapply 资产检查。

## 5. 接口与数据

没有公共 Skill input/output、profile、schema、typed exit、DTO、生命周期字段或命令变化。现有消费者路径保持：

`Clarify/Readiness/Create Issue 原门禁 -> 读取 issue-content.md -> 原 Gate/exit`。

`quality-guidelines.md` 仍由原 validation/review owner 读取，不新增代码接口。RDT contribution 是 planning/evidence artifact，不是 runtime API。Issue/eval fixture 只增加事实文本和语义标准，不增加运行时字段。

## 6. 状态、顺序、正常与失败流程

1. Clarify 整理完整 Issue：识别责任层，删除无依据下游/部署义务，保留明确环境承诺，合并重复场景。
2. Readiness 在原十维检查完整正文；普通内容缺口回 Clarify。
3. Create Issue 在首次 provider 写前检查同一正文；不合规返回 `refresh_review`。
4. 现有 Issue 后续修订写回前检查完整 postimage；新增/恢复义务无据时在本轮输出前删除。
5. 实施完成后原 RDT owner 整合 current；原 tools owner 同步 dogfood/平台投影。

正常成功是正文边界正确、场景独立且有来源承诺得到保留。失败：

- 必要目标环境结果被删：原 writer 恢复该承诺，不能以最小验证放行。
- 普通 Issue 被追加共享部署/整站 E2E：原 writer 删除义务及派生阻塞。
- 同一行为拆成多个场景：合并为一个场景，除非存在真实不同结果/风险。
- 受管同步冲突或 sidecar：停在原 installer/tools recovery，不手改伪通过。

没有持久状态转换或发布副作用，因此不需要数据回滚协议。Git 提交/PR 等副作用仍由原阶段 owner 执行。

## 7. 恢复、兼容、迁移与集成

不改变已有 consumer 契约，旧 Issue 不强制重写。新规则在后续正常编写/审核和实际写回时生效；本轮只扩展当前规范。

源码变更后通过原 upgrade-tools/reapply 将受管副本更新到同一语义，保留 Task/session、用户修改和 sidecar。若已有在途 Skill 操作，按原 `refresh_review`/context refresh 继续，不热改运行中 provider。没有数据库、服务配置或持久化迁移。

关联 #826/#747 只提供可复用真实 Agent 方法；若其入口当前不可用，使用现有 native eval 或匹配 Skill 入口，不把关联 Issue 关闭状态作为本任务完成前置。

## 8. 验证设计

| ID | 对应要求/AC | 入口与输入 | 预期观察 | 证据边界 |
| --- | --- | --- | --- | --- |
| V1 | D1-R1–R4/R7；D1-AC1 | 更新后的 `standard-intake-authoring-acceptance-boundary` native eval，事实仅来自 fixture | 原 Clarify/Readiness 保留组件、CLI/目标环境必要承诺，拒绝消费方 E2E、逐 Issue 部署、业务发布误推部署和重复场景；最终 `ready` | 真实 Agent transcript 独立判断；DTO/关键词不代替；不证明其他平台 |
| V2 | D1-R5/R6；D1-AC2 | package schema/eval discovery 与 distribution test | eval 可被原 runner 发现；真实 writer/reapply 分发完整正文/示例/owner links，用户保留、零 sidecar | 只证明传递/分发，不证明语义 |
| V3 | D1-R6；D1-AC2 | `test_issue_content_distribution.py`、`test_review_sufficiency_distribution.py`、必要 package tests | 受影响投影、规范引用、acceptance-boundary 示例与现有 consumer 一致 | 不扩完整多平台矩阵 |
| V4 | D1-R6；D1-AC2 | 原 `guru-upgrade-tools` 对本 checkout reapply/readback/drift | source/installed/平台/native/drift 一致，Task/session/peers 保持 | local_candidate 不证明 formal source lock/Release |
| V5 | 工程完整性 | Python/bash/JSON/context/diff 定向检查 | 改动文件语法、JSON、Task context、canonical/dogfood 无 drift | 不重新执行已充分且不相关的历史矩阵 |

先完成规范/fixture 实现，再运行 V2/V3；V1 在可执行 native runner 上由实际 Agent 完成；V4 在代码和工程结果稳定后执行。证据充分后停止，不因阶段变化重跑无变化检查。

## 9. Canonical 引用、本轮差额与实际未决项

- 需求：`docs/requirements/current/issue-content.md` R153/R818/R868，新增 R880/BEH880；`docs/requirements/current/behavior-validation-method.md` 保留 R868 关系并补跨阶段责任边界。
- 设计：`docs/design/current/issue-content.md`、`docs/design/current/behavior-validation-method.md` 新增 D880/CON880 差额，保留原正文和路径。
- 测试：`docs/test/current/issue-content.md`、`docs/test/current/behavior-validation-method.md` 新增 T880/SC880 对 AC1/AC2 的关系与证据边界。
- Architecture：`docs/architecture/README.md`、`docs/architecture/03-domains/review-sufficiency.md` 当前 active；候选正式 no-impact，无需 contribution/ADR。
- Task-owned proposal：`docs/requirements-design-test-contributions/880-issue-responsibility-acceptance/`，由原 RDT owner 在实现和工程结果后 final integration。

当前没有未决需求或机制选择。实现中如果实际行为需要新增公共 I/O、runtime state、部署机制或跨 owner 边界，回到原 Author/Architecture；若出现真实需求歧义，回 Clarify。
