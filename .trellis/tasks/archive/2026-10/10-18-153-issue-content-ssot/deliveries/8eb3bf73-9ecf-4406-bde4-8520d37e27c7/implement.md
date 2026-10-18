# D1：Issue 内容 SSOT 的实施与验证计划

## 1. 输入与引用

整体 authority 为 Task 根 `prd.md` 的 accepted_scope revision `sha256:717162576799e6b2cb44d93de98335bf28381c572b37a348beb80c38247dec48`。本批 PRD 第1–7节定义全量 D1、来源/场景/AC，design 第3节独占来源设计处置；本计划不复制矩阵。design 第1节的 B=`ed59e851b6c1257bac6316a9571274427e383c93`、Planning H0 与 PR main target 各自保持原意义。没有前序交付。

实施前实际读取：`clear-technical-writing.md` 全文、原 Author `references/planning-body.md` 第2–5节及本批三正文；四个当前 Issue packages 的 SKILL/必要 references；design 第9节的 current RDT108、Architecture99/constitution-v1/change-contract-v1、#154 贡献。官方 Trellis workflow/marketplace 扩展规则由原 Trellis meta/实施入口读取，流程变更落 Markdown，不改上游/hook。

已收到真实 Architecture candidate_assessment 的 `architecture_impact/target_native`，并消费 Normal、Solution qualified_current 与 Root not_incident_applicable。它们不替代 Wording、最终 Architecture、Approval 或实际行为验证；没有 incident/protection 机制，不新增事故问卷。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | 前置与原责任 | 文件/操作与可审核产物 | 完成观察 |
| --- | --- | --- | --- |
| I1 核对基线 | 实施 owner 读取完整来源和原四入口；延续 R1 | 四 package 当前 SKILL/contract；实际正常入口观察与现有研究核对 | 记录合同/指引/遗漏/读取差额；不把 scan 当 semantic pass，已满足写入/回读/固定 scope 直接复用 |
| I2 写共同正文及示例 | I1、已审设计；原 Clarify 内容责任 | 新 `trellis/skills/guru-team/packages/guru-clarify-requirements/references/issue-content.md`；`examples/issue-content/{brief,detailed,revision}/process.md` | 一份规范涵盖适用内容、深度、裁剪、最终整理与局部范围；准确引用语言和原来源规则；示例有输入/事实/未知/正文/审核修订且明确教学身份 |
| I3 接入四原 owners | I2；原四 package 责任 | Clarify/Wording/Readiness/CreateIssue 的 SKILL 与必要 contract | 每入口显式可解析同一规范，原职责内实际使用；不复制标准、不改变 public I/O/scanner/executor/typed exits/原写入与恢复 |
| I4 定向工程验证及安装 | I2/I3；原 preset/工具维护 owner | 新 `trellis/presets/guru-team/scripts/python/test_issue_content_distribution.py` 复用真实 preset fixture；source/dogfood/installed 与声明平台投影；普通 apply/reapply 或原 tools-only 同步 | 字节/相对引用/完整 package 闭包、reapply、用户自有文件、sidecar、drift 有结果；历史迁移前置不被绕过 |
| I5 实际 Agent 与 GitHub 验证 | I4 的完整 matching installation；原 Discovery/Clarify/Wording/Readiness/CreateIssue | 支持平台正常入口生成三类需求样例，覆盖 V1–V7；一个专用验证 Issue 的实际创建/回读与后续评论/正文修订/回读；原审核普通遗漏修订重审 | 记录实际输入、加载、调查、正文、缺口、修订、正式出口及外部回读；不得宿主预写成品，不以 schema 代替 Agent |
| I6 知识与最终验证 | I2–I5；原 RDT、Architecture、Check、Commit/Review owners | 独立 #153 RDT contribution；已编写 Architecture task contribution 依实际差额更新；原 owners 在最终 Phase2 前 reconciliation/promotion | 唯一 Test 写真实结果和边界；原 Architecture 独立审完整候选/拟晋升后才晋升；最终 Check/commit/committed 完整 Review 覆盖实际晋升写入 |

I2/I3 可在同一内容写作批次完成，I4/I5 仍须实际验证完整匹配候选。没有前后 Delivery 接口待接。若独立切片需要变化，必须由原 scope/Planning owner 处理，不能把 full 写成 partial 掩盖未完成。

## 3. 验证入口、输入与预期观察

所有命令从本 Task 注册 checkout 根执行。下面是执行计划，不是已通过结果。

| 验证 | 入口、输入与依赖 | 预期观察及对应设计/验收 |
| --- | --- | --- |
| E1 source/ownership | `bash trellis/workflows/guru-team/scripts/bash/check-skill-packages.sh --root . --mode source --json`；`bash trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json`；`git diff --check` | 四原 packages 闭包及 upstream 所有权合法、无格式错误；design T1/T4，AC1/7/8。只证明工程事实 |
| E2 分发与引用 | 用匹配 Fork CLI 提供 `GURU_UPSTREAM_DELIVERY_SCRIPTS=<匹配安装的 dist/templates/trellis/scripts>`，从仓库根运行 `python3 -m unittest discover -s trellis/presets/guru-team/scripts/python -p test_issue_content_distribution.py -v` | 真实 preset writer 安装/重复应用全部声明平台受影响资产；同一规范字节/入口相对链接、示例、用户文件/旁文件有观察；design T4，AC2/8/9。不是多平台 Agent 行为或 Release矩阵 |
| E3 dogfood/matching installed | `bash trellis/presets/guru-team/scripts/bash/apply.sh --repo .`，再 `bash trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh --repo .`；installed 原 package checker | canonical 与 dogfood/installed 受管投影同步；每个 `.new/.bak` 单独处理并记录。若 apply 被旧历史前置阻塞，由原 tools-only owner 正常恢复，失败不能算成功；design T4/T5，AC8 |
| E4 一代表环境 | 当前隔离worktree作为Codex目标安装，匹配当前Fork/CLI，沿原tools-only/完整matching preset采用并reapply；保留用户自有文件。只有实际改动确需clean证明时才用最多一个throwaway | 当前候选规范及四入口实际可读，用户内容保持，旁文件与source身份明确；design T5，AC8。未执行clean、未覆盖平台及完整upgrade/Release矩阵分别说明；普通Issue不因缺完整矩阵失败 |
| E5 V1/V2/V6 | installed 原 Sync/Discovery/Clarify→Wording→Readiness；简略工程请求先调查，详细技术/缺陷来源带条件/例外与已确认约束；语义等价需求分别从新草稿和既有修订入口执行 | Agent 实际完整读取同一 issue-content 和 clear-writing；生成完整正文、保留未知事实/来源承诺；章法按输入裁剪；design T2，AC2–4/6/9 |
| E6 V3/V4/V5/V7 | 原 Clarify 完善明确验证对象，读取正文与有效评论；原 Wording/Readiness 检查实际普通遗漏/跨段不一致，回原 owner 修订再审核；独立只读与完整正文输入 | 必要评论内容进入正文，建议/历史不升级；完整title/body审核；本轮语言检查限修改文本；无关内容不扩写，范围外缺口保留结论影响；只读不写入。design T3，AC2/4/5/6/7/9/10 |
| E7 实际创建/修改 | 原 CreateIssue 对明确命名“#153 验证”用途的同 repo Issue 创建、live readback；原 Clarify 在同对象执行评论/正文修改及live readback；结束时沿原边界关闭验证对象 | 两条写入与回读均能对应实际审查草稿/正文；不重复创建、不建验证Task/branch；草稿不代替外部效果。design T5，AC6/7 |
| E8 最终语义验证 | 原 Wording/Readiness（行为场景）与本 Task Check/Architecture/BranchReview/Completion，读取实际最终diff、唯一Test和现有authority | 原 owners 判断充分性、正常范围和当前证据；最终验收不靠recorder或章节数。RDT/Architecture晋升后新差额仍被最终门禁覆盖 |

功能变更、缺陷修复、工程变更由 E5/E6 的样例合计覆盖，不要求每场景安装或建Issue。场景可复用同一验证环境。V4/V7 使用真实写作产生或原入口支持的未完成正文；禁止宿主预写最终文档/通过结论，或篡改已接受状态来制造案例。语言规范缺失/恢复按正常入口所需路径观察，不引入故障注入矩阵。

唯一 Test 分开记录 Agent、确定性、安装和外部证据、实际首次失败/修复及未验证项。代表平台以外的实际 Agent 行为、完整多平台 upgrade/Release 和业务仓采用不推定通过。原 package targeted suite 如因实际改动受影响，由实施/Check owner 在最小可靠验证集内运行；没有 runtime/schema 变化时不扩张无关全套测试。

## 4. 停止条件与适用回退点

- 语言规范或共同正文缺失/读取失败时，仅报具体缺口并暂停依赖实质文本；完整读取恢复后继续原请求，无新增审批。来源/范围有真实未决选择回 Clarify；机制/架构冲突回原 Architecture/Author。
- 实际 Agent 行为证据不足时，对应 AC 保持缺口，回原写作/审核或实施 owner 补齐；不把工程绿测、投影一致或草稿当实际创建/修改成功。
- 普通 stale/mismatch/输出丢失沿原 producer 重入、同事务恢复；不新建身份、Task或验证Issue掩盖失败。GitHub mutation后先回读查实际结果，不盲目重发。
- 安装或分发失败保留实际首次错误，交原 installer/tools owner；不删除无关历史任务、改上游或手动修补 generated files绕过前置。对 `.new/.bak` 逐路径审查，不静默覆盖用户内容。
- 本地正文改错时，只修本Task实际变更；不 revert/格式化并行改动。没有数据库迁移或软件部署，因此不创建数据/发布回滚协议。验证Issue关闭只处理选定对象，保留正文/评论及历史结果供核查。
- 共享 RDT/Architecture 晋升发生预期current错配时，仅由原promotion owner处理当前差额；无关ref/版本前进不重置本Delivery固定B，实际新差额重新过原门禁。

## 5. Delivery Policy（唯一）

策略为 `full`。D1 交付整体 accepted_scope 的 R1–R4、V1–V7、AC1–AC10，没有延期或分配给后继Delivery的已接受责任。完整交付条件是共同内容规范与四owner加载落地，来源/局部范围边界保持，真实Agent三类需求场景及原审核修订完成，创建和正文修改均有实际写入/回读，定向分发和一个代表目标安装/reapply满足本Issue范围，长期知识由原owners正确承接，正式Check/Review/Delivery及整体验收满足原合同。

Delivery 合并只建立切片交付事实，Task Completion 仍须检查整体责任和实际证据。未验证其它平台Agent/完整多平台Release矩阵不算本Task延期责任，也不得宣称已通过。

## 6. Docs SSOT Plan（唯一）

策略为 `delta_first`。当前完整 authority 为 RDT `current-main-0.6.17-guru.108/active`、Architecture `.99/active`；具体引用与本轮差额见 PRD第7节、design第9节。先保留本批规划和task-owned差额，再由原owners在最终Phase2前reconcile/promote，避免规划填充直接改共享导航。

| 文档责任 | 真实差额/原 writer | 直接consumer与时点 |
| --- | --- | --- |
| Requirements/Behavior | 原 RDT owner 在 `docs/requirements-design-test-contributions/153-issue-content-ssot/` 维护 #153 R1–R4 对应长期责任，不复制 package规范正文 | 实施/Check/Review/Completion读取；最终Phase2前完成三层一致与promotion |
| Design/Contract | 同一原RDT owner定位 Clarify内容单写、四入口同源读取及原分发边界，继承 #154 来源/Planning分工 | 原RDT promotion和当前门禁消费；不由Author替写SSOT pass |
| Test/Traceability | 同一贡献唯一Test记录本轮Agent V1–V7、真实GitHub写入回读、工程/安装、首次失败和未验证项，建立要求→设计→验证关联 | Check/BranchReview/DeliveryReview/Completion消费；不将计划写成结果 |
| Architecture | Author已按真实candidate写 `docs/architecture/contributions/153-issue-content-ssot.md`，before为main `ed59e851...` 的`.99`；原Architecture独立评估/更新并expected-current晋升 | Wording后final_plan审实际设计/贡献；Phase2独立评估完整候选与拟写差额后晋升；最终Check/commit/committed完整Review覆盖实际写入 |

不新增 ADR，因为现有 ARCH-FND-002/005、ARCH-DOM-039/055、ADR-022/024 足以承接本候选；如实施产生新决策回原Architecture owner。Author不写共享README/index/manifest、CURRENT或RDT结论，不预建空ledger。规则正文仍在原Clarify package；任务规划、唯一Test与Architecture贡献各承担原职责，互不成为第二范围权威。
