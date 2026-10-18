# D1：统一 Issue 内容规范的设计

## 1. 设计目标、需求承接与内容基线

本批全量承接本目录 `prd.md` R1–R4、S1–S6、V1–V7、AC1–AC10。目标是在原 Clarify package 建立唯一 Issue 内容规范，由创建/修订与三个原审核或创建 owners 共同实际读取。保留来源承诺、局部修改范围和原执行路径；真实 Agent 行为、确定性检查、安装结果分开验收。

development baseline B=`ed59e851b6c1257bac6316a9571274427e383c93`。来源是用户指定的 main，在本次 Planning 通过原 `DeliveryProjection.content_base(key, development_base=<该 main commit>)` 得到；本 D1 没有前序交付。Planning H0 同为该 commit，只是规划时观察。最终内容范围为 B 到实际候选 H，PR integration target 为 `main`；不因目标分支前进自动改 B，也不把 H0 当最终实现 HEAD。

原 Architecture 的实际 `candidate_assessment` 返回 `baseline_current`，阶段 `planning`，baseline=`current-main-0.6.17-guru.99`，constitution=`guru-trellis-design-constitution-v1/current`，impact=`architecture_impact`，path=`target_native`。理由是四原 owners 新增对原 Clarify 单写内容规范与示例的可复用读取依赖。决定 refs 为 ARCH-FND-002/005、ARCH-DOM-039/055、ADR-022/024。适用 change contract 为 `docs/architecture/06-governance/change-contract.md` 的 `guru-trellis-architecture-change-contract-v1`，required concerns v1。该候选评估不是最终 Planning、Implementation 或 promotion 通过。

## 2. 当前系统、边界与目标差额

当前四个 canonical packages 位于 `trellis/skills/guru-team/packages/`：Clarify 已负责需求意图、来源角色、草稿及正文/评论动作；Wording 已固定完整 title/body scope；Readiness 已有需求完整性等十维度；Create Issue 已绑定最终草稿、创建、回读及恢复。四入口已有清晰写作规范定位。#154 的 Author package 已拥有 Planning 正文合同和来源保留规则。原 preset 递归分发 package references/examples，现有分发测试可复用其真实 writer 方法。

实际差额是原合同未显式共同加载一份 Issue 内容正文规范，也未明确“用户要求创建/完善 Issue”时必要已确认内容应汇入最终正文的目的边界。基线观察不证明现有每次写作失败，也不证明 scanner 或 mutation executor 缺陷。本设计不改它们的语义或 schema。

目标新增 `guru-clarify-requirements/references/issue-content.md`。该正文定义 Issue 必要内容、适用深度、裁剪、最终整理及原职责内审核，引用原语言及 #154 来源规则。两条写作路径和三个后续 owners 都定位此文件。去敏过程示例放在同 package 的 `examples/issue-content/`，只演示输入、查证、实际未决选择、正文及修订，不形成第二规范或当前用户答复。没有前序交付或跨批接口差额。

## 3. 来源设计处置（唯一）

| 来源条款 | 已约定承诺 | 处置 | 具体落点 | 理由、影响与上游处置 |
| --- | --- | --- | --- | --- |
| #153 R2 首段及来源整合段 | Clarify 拥有完整读取、来源角色、保留旧承诺及整合当前变更 | retain | 第4节 M1；第6节 F1/F2 | 同一原 owner 整理正文，不引入第二 writer；无偏离 |
| #153 R2 末段 | 既有修改沿原操作/确认/回读/刷新，新 Issue 经原审核再创建 | retain | 第5节 IO1/IO2；第6节 F1/F2 | 原动作和 typed exits 不变；无新 mutation executor |
| #153 R3 首段 | 共同内容规范由 Clarify 规范包唯一维护并受管安装 | retain | 第2节路径；第4节 M1/M4 | 四 consumers 同源，不在模板/README 复制正文 |
| #153 R3 语言与保留段 | 唯一引用 clear-technical-writing，来源保留沿 #154 | retain | 第4节 M1/M2；第5节 IO3 | 不另造语言/来源规则，保留强制、建议、例外与精确字面 |
| #153 R3 裁剪/技术设计段 | 适用内容完整但可合并简写；不要求提交者先设计，已有技术承诺保留 | retain | 第4节 M1；第6节 F1/F3 | 内容充分性由 AI 判断，不用标题数/关键词或空 N/A 代替 |
| #153 R4 四 owner 列表 | 四个现有语义 owners 显式实际读取同一规范，并保持原职责 | retain | 第4节 M2；第5节 IO1–IO4 | 不扩展 scanner 到评论，不新增审查 owner |
| #153 R4 完整审核及局部范围段 | 内容审核覆盖修改后完整 title/body/来源；语言检查限本轮；范围外缺口不静默扩写 | retain | 第6节 F2/F3；第8节 T2/T3 | 保持完整性阻塞但不自动越界，真实选择回 Clarify |
| #153 §4、AC6/8 | 一个实际支持平台、真实创建及修改回读、定向安装，分开证据 | retain | 第8节 T1–T5；implement第3节 | 草稿/机械检查不能替代外部结果；完整矩阵归专门 Issue |
| #154 R3/R4/R7 与 planning-body §2 | 完整来源/角色/语义、原 Author 与受管分发边界 | retain | M1 的来源规则引用；第7节 | Issue 格式不迁入 Planning；不新增共享来源规则副本 |

没有 change/reject 项，不存在待批准的来源偏离。若实施出现真实约束或范围变化，回原 Architecture/Clarify 后刷新受影响候选，不在本矩阵静默覆盖承诺。

## 4. 模块、职责与设计取舍

| 模块 | 输入、行为与输出 | 实际文件与责任 |
| --- | --- | --- |
| M1 Clarify 内容规范 | 读取完整请求、正文、相关评论、必要事实。按来源角色保留所有仍有效承诺；规定 Issue 适用内容及裁剪；创建/完善产出完整草稿/正文，自检未知事实、真实选择与跨段一致性 | 新 `trellis/skills/guru-team/packages/guru-clarify-requirements/references/issue-content.md`；Clarify 唯一维护。来源保留准确引用同级其它 package 的 `planning-body.md` 第2节，语言准确引用安装的 clear-writing，不复制公共规则 |
| M2 四原入口与合同 | Clarify 编写/修订/自检；Wording 审清楚、术语、语义；Readiness 审完整性、独立单位和可观察验收；CreateIssue 核对共同规范及前序结果适用、最终待写字节并回读。发现缺口回最早 owner | 四个 `SKILL.md` 及有实际必要的原 `references/contract.md`。从其它 package SKILL 用可解析相对链接定位同一个 Clarify 正文；references 内链接按自身层级定位；不复制内容基线 |
| M3 过程示例 | 展示简略工程请求调查、详细技术/缺陷条件保留、分散评论与局部修订/正常遗漏；区分必要事实、未决问题、建议、历史、最终正文及修订原因 | Clarify 的 `examples/issue-content/{brief,detailed,revision}/process.md`；正文可嵌入去敏完整结果。示例明确为教学，不能作当前真实回答或行为证据 |
| M4 原分发及定向检查 | 原 recursive package/preset writer 安装规范/示例及四入口至完整 installed 和声明平台；重复应用保留用户文件与 sidecar 事实 | 不改 installer 行为。新增 `trellis/presets/guru-team/scripts/python/test_issue_content_distribution.py`，复用现有真实 preset fixture，核对同源资产与相对链接、投影字节、reapply、用户文件及旁文件；测试不判断内容语义 |
| M5 实际行为及知识承接 | 实际支持的 Codex/installed 原 owners 执行 V1–V7；原审核指出普通遗漏，Clarify 修订并重审；真实创建/修改回读独立记录。RDT/Architecture 原 owners 承接已确认长期差额 | 实际结果由本 Task 唯一 RDT Test 维护；Author 仅写本 Task Architecture contribution；共享晋升由原 owners 完成 |

选择在 Clarify package 维护内容正文，因为 Clarify 已拥有来源/意图/正文写作，四 owners 已存在且有直接 consumer。单独新 Skill、脚本正文生成器或全仓语言评分器会重复职责，没有本轮必要性。创建/修订共用规则但保留各自原操作，无需 dual-read 或新兼容 adapter。

## 5. 接口与数据

本批不新增 public API、DTO 字段、schema、phase、typed exit 或持久化协议。新增的 Markdown 文件是可复用内容 authority，不是 gate artifact。以下为原接口的读取关系：

| 接口 | 原 producer/input → 新读取 → 原 output/consumer |
| --- | --- |
| IO1 草稿 | 原 Clarify `standard_intake` / proposed draft/request → issue-content + clear-writing + 当前来源 → 原草稿/`new_task` 或原澄清/blocked；继续 Wording/Readiness/CreateIssue |
| IO2 修订 | 原 Clarify 已有 `issue_body_edit`，live preimage/精确 payload → 同一正文与语言规范 → 原 repo-bound gh 写入、live reread、`refresh_context`；继续原上下文回程。不调用 create |
| IO3 审核 | 原 Wording `change_request`、原 Readiness 当前 target/已审结果 → 同一正文/语言/必要来源上下文 → Wording 原 `pass` / `content_changed` / `blocked`，或 Readiness 原 `ready` / `clarify_requirements` / `review_wording` / `refresh_context` / `blocked`。Wording 仍固定完整 title/body，评论仅是 AI 读取的必要来源，不宣称被 scanner 扫描 |
| IO4 创建 | 原 Readiness `ready` proposed_draft → CreateIssue 同源规范检查、最终 draft 与 current reviewed identity → 原 executor 创建/marker/readback、`created` 或 `refresh_review`/blocked；created 仍回 Sync/fresh Intake |

跨 package 引用只指向同一 installed package 布局，不传入 producer-private review evidence。内容与语言判断仍由原 AI owners 负责。脚本只验证分发、引用、schema、字节和原 freshness。已有 mutation payload、digest、marker 和恢复输入保持原语义；不把授权写进任何文件。

## 6. 状态、顺序、正常与失败流程

本轮没有新增业务状态转换，只有现有阶段的读取与判断顺序。

F1 创建：用户请求创建 → 原 Discovery 调查可查事实 → Clarify 完整读取来源并分类 → 有真实影响需求成立的选择才沿原流程澄清 → 按同一内容规范写完整草稿并自检 → Wording/Readiness 各在原职责审核最终 title/body → CreateIssue fresh 核对规范、前序结果和待写内容 → 原创建并回读 → 原 Sync/fresh Intake。必要问题未解决时保留具体缺口，不宣称完整；技术机制未定交原规划方。

F2 完善：用户请求修订 → Clarify 读取完整当前 title/body、相关评论、请求和必要事实 → 保留此前仍有效承诺，处理本轮明确替换/撤回/范围变化 → 将必要已确认内容整合进拟修订完整正文，并对照来源自检 → 沿原正文修改路径写入、回读并返回 `refresh_context` → 刷新上下文后，原 Wording/Readiness 按既有规则审核实际修改后的完整 title/body 与必要来源。只在评论/会话存在不能免除最终正文内容；建议与历史不自动升级。

F3 局部修订：原 owner 先界定本轮范围，修改后检查完整 title/body 的跨段关系；语言检查只处理本轮文本及必要上下文。发现本轮普通不一致则返回原 owner 修订并重审。发现范围外旧缺口时说明其影响，不自动扩写；若影响完整性判断，保留该判断的阻塞，真实范围选择回 Clarify。无关历史不因语言偏好改写。

F4 只读/已有完整正文：状态查询、只读审核、讨论或过程评论不触发正文写入；可给建议，后续修改沿原边界。完整简短正文满足适用内容时保留，不为模板重写。

F5 依赖失败/恢复：语言规范缺失或读取失败，仅报告具体路径并暂停依赖实质文本；恢复后完整读取继续原请求，不增审批。共同规范或必要来源不可读时回对应原 owner/安装修复后继续。普通 stale/mismatch、漏读和输出丢失沿既有 freshness/re-entry/recovery，不新增恢复状态、锁或强制重建资源。

## 7. 恢复、兼容、迁移与集成

公共 I/O、四原 owners、原确认/写入/回读/刷新和恢复均保持，所以无需公共协议迁移。本轮没有数据库或服务数据变化，没有数据迁移/回滚协议。历史 Issue、Task 和归档不追溯改写。

canonical 新增/修改须经完整 matching preset 安装；dogfood/现有项目不靠一次性 patch。按原 apply/reapply 保留用户文件并检查 `.new/.bak`。如当前仓库历史迁移前置阻止普通 apply，由原 tools-only owner 在其原合同内恢复，不删除或迁移无关历史来制造成功。未更新的既有安装不能宣称已采用新规范。

当前 D1 没有前序集成接口。完整安装后从至少一个当前支持平台实际调用原链，确认跨 package 引用与新正文被实际读取。其它平台的投影字节相同只证明分发，不推定其 Agent 行为。受影响公共 API 未变，无新增兼容双写或旧规范 reader。

## 8. 验证设计

| 验证 | 要求/场景/AC | 层、入口、输入与预期观察 | 证据边界 |
| --- | --- | --- | --- |
| T1 基线 | R1/S1–S5/AC1 | 原四入口读取与真实写作观察，盘点写作/评论/审核/读取/示例；具体记录共同规范差额，复用已满足能力 | 研究/scan 不算行为或 semantic pass；不先认定脚本失效 |
| T2 简略与详细来源 | R2/R3；V1/V2/V6；AC2–4/6/9 | Codex installed 原 Clarify→Wording→Readiness，简略工程和详细技术/缺陷输入；实际查证后成文，保留条件/例外/技术承诺、未知事实角色；语义等价输入分别经创建草稿和既有修订同源规范 | 不宿主预写成品；每 owner 实际加载两规范；原用户回答不得编造 |
| T3 分散与遗漏/局部 | R2/R4；V3/V4/V5/V7；AC2/4–7/9/10 | 原 Clarify 读取正文/评论/明确修订；原 Wording/Readiness 实际指出普通遗漏/跨段不一致，回原 owner 修订重审；只读/完整正文无写入或形式重写；范围外缺口保留影响 | 审核实际完整 title/body；语言限定本轮。三类需求样例合计覆盖，不用测试宿主篡改已接受状态制造案例 |
| T4 分发/工程 | R3/R4；AC2/7–9 | 新定向真实 preset writer 测试、四 package source/installed 检查、相对链接/投影字节、reapply、用户文件、sidecar 与 drift | 机械检查不判内容充分，不是完整多平台 throwaway 矩阵 |
| T5 实际外部与代表安装 | V6/AC6/8；R2原写入 | 明确同 repo 专用 #153 验证 Issue，原 CreateIssue 创建并回读，复用于原 Clarify 评论/正文修订及回读；以当前隔离worktree作为一个匹配当前候选的Codex目标安装/reapply环境，实际加载新内容规范；仅当实际改动需要时再使用最多一个clean throwaway | 草稿不能替代真实写入；代表平台不推定其它平台实际行为；未执行的clean与完整upgrade/Release矩阵明确保留边界 |

每项实际结果、首次失败、修订与未验证范围在唯一 Test 中记录，不在本设计预填通过。最终 Check、独立 Architecture、Branch Review 和 Completion 分别复核其职责内充分性。

## 9. Canonical 引用、本轮差额与实际未决项

当前 RDT 为 `current-main-0.6.17-guru.108/active`，具体 requirement/design/test 引用和已读取用途见本批 PRD 第7节；当前 Architecture 为 `.99/active`，constitution-v1 和 change-contract-v1 见第1节。#154 的 R154-02/04/05/06、D154-01..03 与测试分层作为继承边界。本轮新增 Issue 内容规范及四原 owners 的读取关系，长期责任由独立 #153 RDT contribution 承接，规则正文仍只在 canonical package。

真实 task-owned Architecture contribution 为 `docs/architecture/contributions/153-issue-content-ssot.md`。before authority 为 `git:ed59e851b6c1257bac6316a9571274427e383c93:docs/architecture` 的 `.99/active`，本文与 contribution 不写共享 CURRENT、不创建新 ADR。原 Architecture final_plan 必须在 Wording 后独立评估真实 design/contribution；后续按 ADR-030 独立 Phase2 完整候选及拟晋升评估后，由原 owner 执行 expected-current-bound promotion，再做最终 Check/commit/committed 完整 Review。

当前没有未决产品范围选择或来源偏离。实际验证与安装尚未执行，是本批实施及验收责任，不能提前当通过。若有内容规范边界、来源角色或真实跨段冲突，分别回原 Clarify/Architecture，不扩张异常场景。
