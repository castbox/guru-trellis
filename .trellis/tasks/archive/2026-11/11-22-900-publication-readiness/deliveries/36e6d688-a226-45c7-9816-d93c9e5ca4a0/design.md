# #900 发布入口设计

## 1. 设计目标、需求承接与内容基线

实现本批 PRD 的 S-R1–S-R5 和 AC1、AC2。开发基线 B 为本 Task 创建时固定的 `origin/main@f06eddb6ccf97ddd2d1a41c117692f5957cb2dc7`。当前规划 HEAD H0 等于 B。实施提交后由原构造器固定真实 H 和完整 B..H。PR 目标为 `castbox/guru-trellis:main`。若后续出现实际冲突或依赖变化，由 Reconcile owner 判断影响。

候选评估返回 `baseline_current / architecture_impact / target_native`。阶段权威为 `guru-trellis-architecture`、`guru-trellis-design-constitution-v1` 和 `guru-trellis-architecture-change-contract-v1`，依据包括 ARCH-DOM-017、ADR-POSTCOMMIT-INDEPENDENT-REVIEW 及 ADR-009。

## 2. 当前系统、边界与目标差额

当前 Branch Review 通过后触发发布架构资格和 Delivery Review。Delivery Review 写入公开 readiness 槽并提供 PR 载荷。Publication 用该结果预览、确认、执行并恢复事务。当前 `plan_identity` 绑定最大动作集合和载荷。具体远端动作另列在 preview 上。

新链把 readiness、PR 文本和预览归 Publication。预览与执行之间按实际待执行动作和目标判断确认是否仍适用。独立内容审查、架构资格、原 Merge 及整体 Closeout 的现有职责继续执行。该 Delivery 无前序结果。

## 3. 来源设计处置

| 来源及原承诺 | 处置 | 落点及影响 |
| --- | --- | --- |
| #900 行为 1、2 和 #736 第 8 项及 AC7 发布部分。发布入口判断 readiness，展示准确预览。 | retain | §4–6。Publication 接手语义判断和 PR 文本，归并当前链。 |
| ADR-POSTCOMMIT-INDEPENDENT-REVIEW。首次完整独立审查及适用 Architecture 资格在新远端动作前成立。 | retain | §5–6。仍按固定候选和适用范围消费实际结果。 |
| ARCH-DOM-017 与 ADR-009 下的当前 readiness writer 分工。 | change | §4–5。单写角色从 Delivery Review 迁到 Publication，原项目 Architecture 原路径审查及晋升。 |
| #900 行为 3、4，MIGRATION-794 的已执行与待执行动作分界，及 #896 合并恢复。 | retain | §6–7。按当前事实恢复同一动作，已合并直接回原 Merge。 |

## 4. 模块、职责与设计取舍

- `guru-publish-task-delivery` 的 Markdown 拥有 readiness、PR 文本、所需前置和当前执行判断。将旧 readiness 校验与投影归入此包，直接复用公开 gate 写入、事务预览、writer 与 readback。运行时继续处理已给定语义结果与客观状态。
- `guru-review-branch` 输出实际 TaskRef、DeliveryKey、固定 H 和 full_review 身份，相邻 Architecture 资格为 Publication 准备入参。Merge 刷新、scope 修订、撤回和显式续接按原阶段及精确对象换接新的 Publication 准备或恢复入口。
- canonical workflow、routing、registry 和 interface 同时切换。同步受影响的 preset、spec 和声明平台投影。移除无活动消费者的独立 Delivery Review 正常入口和写入路径。已发布的前驱合同由固定完整 provider 解释。
- 将单独旧 Skill 保留为正常 wrapper 会保留双入口与跨 owner 的 ready 装配。选择直接切换，由一个 owner 在同一调用链完成准备和执行。代价是同步更新发布、Review、Architecture、Merge 及各续接消费者。

## 5. 接口与数据

| 边界 | 输入和产出 | 约束 |
| --- | --- | --- |
| Publication 准备 `delivery_prepare_publication` | TaskRef、DeliveryKey、适用的 full_review 和 Architecture 结果。复核当前 B..H。通过后输出当前候选、中文标题正文、切片交付、剩余责任、未验证项及实际待执行动作。 | 新版公开输入和结果 schema。调用方不装配旧 `ready`。既有 readiness role 的 owner 声明改为 `guru-publish-task-delivery`。 |
| Publication 执行 `delivery_execute_publication` | 同一 Delivery 的精确预览及其客观比较身份，由调用方在当前对话完成确认后传给原事务 owner。 | 响应字段只保留执行、显示及路由需要的内容。身份比较检查候选、载荷及实际待执行动作。授权只存在当前对话。 |
| Publication 终态 | 当前合并前置满足后输出既有 `ready_for_merge`，沿原 Merge 消费。 | 原公开 PublicationFact、readiness role 和 Task schema 保持。既有结果仍保留原 producer 字面。当前新写通过当前 owner 声明。 |

准备入口按前置、规划、实现、范围和结果失效返回各自的唯一 consumer。为现有 profile/exit 改义时发布后继合同。具体版本号随项目当前 Interface 下一版分配。

## 6. 状态、顺序、正常与失败流程

1. 先按 DeliveryKey 读取公开结果、同一发布事务和已有 PR。发现已合并时根据公开 PublicationFact 是否存在，交原 Merge 的 `delivery_merged_recovery`，或在具备其准确归属与历史前置时交 `delivery_adopt_merged_pr`。缺法定前置时由 Merge 返回实际缺口。
2. 新动作需要当前候选匹配、独立审查与架构资格适用。AI 判断 readiness 与真实载荷。规划、实现或范围问题交其原 owner。缺审查或架构结果时回原入口。待执行远端写入在回程期间暂停。
3. AI 通过后记录 readiness，保留 full_review predecessor，并沿既有公开操作从 reviewing 进入 publishing。Publishing 中已有 readiness 若失效，由 Publication 在适用 full_review 下按原 rework 回 reviewing，刷新 readiness。如果同一有效预览仍可获得，按原预览与当前事实核对后继续。readiness 槽本身没有 PR 原文。如果 readiness 已记录而预览未返回，且没有可恢复的预览或发布事务，Publication 先回读同一 Delivery 和已有 PR。full_review 适用时，通过原 publication → readiness rework 清除 readiness，回到 reviewing。AI 重新生成标题、正文与预览，只记录一次当前 readiness 后再次展示。full_review 失效时返回原 Review。
4. 预览列出 repo/base/head、候选 H、已绑定 PR 或待创建对象、相关远端 HEAD 及实际 push/create/edit/Ready 动作。确认前保持远端事实。执行前复查影响剩余动作的事实。正常的已完成动作回读可推进同事务。剩余动作或预览发生实质变化时重新展示并确认。
5. 由原事务持有同一个 Delivery 与 PR 的执行及完成事实。先回读再记录实际 PublicationFact，只在当前 Merge 前置满足时交 Merge。正常输出丢失用第 7 节恢复。

## 7. 恢复、兼容、迁移与集成

| 实际状态 | 接续 |
| --- | --- |
| 已执行 push、PR 创建、元数据更新或 Ready，回执缺失 | 用原事务核对操作后事实并恢复缺失投影。已有 PR 继续使用同一身份。 |
| 还有待执行动作 | 先回读完成与待执行集合。按新入口取得适用准备与确认。Publication 的 reprepare 接收当前 readiness 引用。用原事务引用找到唯一活动记录，保留原动作输入、绑定 PR 和已完成事实。回读已有 push、PR 及合法的元数据和 Ready 后像。缺少唯一归属或实际事实不兼容时停在原 owner。为仍待执行的动作生成当前预览并重新确认。执行继续使用同一事务。新预览适用的候选、载荷与动作以明确的私有版本字段绑定。避免通过重算旧引用把旧输入改义。 |
| 私有事务不可用，明确已有同一 Open PR | 使用现有 shared Open PR 恢复能力。保持明确 PR、来源和候选条件，附当前待执行动作的必要前置。 |
| 已合并 | 采用 §6 对应的原 Merge 恢复入口，不以当前 readiness 刷新作为终态回读前置。 |
| 固定旧 provider 的合法操作 | 由匹配旧 provider 恢复已经执行的原结果，再把实际公共事实交当前入口。已执行事务消歧和切换步骤写入 MIGRATION-900。待执行动作按当前候选、预览与确认继续。 |

仅在原事务由回读证明已经完成后，才执行既有 retire_completed。未完成事务由 reprepare 接续原记录。当前读取仍沿原事务职责。若当前 readiness 或预览变化需要追加私有字段，则采用单次定向升级，完成实质旧动作的回读后形成待执行部分，保持单一活动事务。旧正常调用入口退出。若实现发现确切存量必须新增旧格式 reader 或其它兼容层，回 Author 和 Architecture，展示实际消费者、退出条件和证据，按 subtraction-first 合同取得具体决定。

## 8. 验证设计

- V1（AC1）使用真实公开 Publication 准备与执行入口和可控 Git/gh 依赖。以独立审查后的合法固定候选观察 readiness、中文正文、具体 preview、确认前远端无变化、确认后精确调用及可由 Merge 消费的结果。
- V2（AC2）定向覆盖前置失效、readiness 拒绝和预览后实质漂移。观察唯一回程、无待执行远端写入和确切再确认动作。
- V3（AC2）复用原同 PR 事务测试中仍适用的断言。补做新入口受影响的已执行动作回读、待执行续接、Open PR 恢复与已合并分流。已合并执行本身可采用 #896 仍适用的证据。
- V4 运行 source、installed、平台及 drift 定向验证。通过原托管更新验证现有 checkout 保留 Task/session，读回 sidecar 和受影响投影。用一次受控真实 Agent 观察语义入口与预览边界，并单列实际 GitHub 使用证据。

## 9. Canonical 引用、本轮差额与实际未决项

RDT 更新三个 `current/task-delivery-lifecycle.md` 的发布与恢复条款及受影响稳定引用。Architecture 的隔离贡献和 ADR 候选承接 ARCH-DOM-017、ARCH-CUR-075 及相关项目分工与集成合同。原 owners 在工程验证后、TaskCommit 前完成必要整合和读回。

当前方案选择直接迁移和原 provider 恢复。当前未发现需要新增兼容机制的实际消费者。发布准备、恢复和安装的实际验证留在实施阶段。
