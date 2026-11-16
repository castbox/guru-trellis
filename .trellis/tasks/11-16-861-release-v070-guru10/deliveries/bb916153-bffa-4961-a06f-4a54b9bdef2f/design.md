# #861 gen2 D1：发布门禁消费者完整源修复设计

## 1. 设计目标、需求承接与内容基线

本设计承接本批 PRD B1–B4、BS1–BS4、BC1–BC4，选定整体 R1/R2/R3/R5/R6/R7/R12/R13 及 AC1/AC2/AC4/AC10/AC11。目标是独立交付两项消费者修复的完整可分发源；准备 checkout 的正式采用仍是后继责任。

development baseline B 为 `5dc0708a1d817fb9fb02edb64419b7b3c3f7cc10`，来自 gen2 acquisition 时已同步的 main。原 constructor 已按三处候选路径观察并返回此 B；Planning H0 也是该提交。H0 是实施前观察，不是待提交结果或最终发布候选。PR 目标为 main；实施后由原 constructor 捕获完整 B..H 和 dirty increment，不以本文件预选路径排除真实内容。

Architecture authority 为 `docs/architecture/README.md` 的 `guru-trellis-architecture`；constitution 为 `00-foundation/design-constitution.md` 的 `guru-trellis-design-constitution-v1/current`；项目合同为 `06-governance/change-contract.md`。实际 candidate_assessment 已返回 `baseline_current/no_architecture_impact`：仅适配现有 envelope 与 schema 引用，不变 owner、路由、API、状态或安装路径。本设计仍须经 final_plan 与 Approval，未形成实现 pass。

## 2. 当前系统、边界与目标差额

gen0 PR #865/#866、gen1 PR #871/#875 及簿记 #876 已进入 main；原终态和验证保持历史身份。本批是 gen2 的首个 Delivery，不重做这些交付。当前源已提供 `.10` manifest、合法 envelope、context_request 2.0、Discovery supplement 1.0 与原安装 writer。

差额只有三处源码文件：`trellis/presets/guru-team/scripts/python/test_verify_trellis_upgrade_contract.py` 的既有测试观察；`trellis/skills/guru-team/packages/guru-discover-change-context/commands.json` 的四条 context-request 引用；同包 `tests/test_runtime.py` 的直接回归。生产 helper、Discovery runtime/Interface/schema、manifest、版本和 source lock 不改。三文件分别约2571/301/364行，均未达到项目拆分阈值，不因总行数拆文件。

## 3. 来源设计处置（唯一）

| 来源／原承诺 | 处置 | 设计落点、理由、影响与上游处置 |
| --- | --- | --- |
| 私有发布合同 Complete Source Before Actual Adoption：完整源先独立交付 | retain | 第6–8节与 implement Policy：本批自行验证源与临时安装；D1 delivered 后才分配实际采用，无偏离 |
| 同合同 Whole Preparation Completion / Stage 2：整体准备收尾后重新冻结最新 main | retain | 第6–7节：保留 D2、Completion/Closure/Finish 与 Task 外发布门禁，不把本批 HEAD 当发布基础 |
| 当前 helper clarification_owner_for_issue：record/check 的 owner_result 与 owner_context 分开 | retain | 第4–5节：修测试消费和独立绑定断言，生产 shape 不变；无需上游修改 |
| Discovery context_request 2.0：两种 review_focus 与匹配 return_identity | retain | 第4–5节：四处帮助改指已有 schema，正常输入走原验证，无新 profile/API |
| Discovery 自己的 supplement 1.0：无 review_focus 的原形状 | retain | 第5/8节：四个现有引用保持，独立输入兼容回归；不能借用 Clarify 同名 profile 的2.0 |
| R850/D850 的完整匹配分发与固定旧 provider 恢复 | retain | 第7节：历史 schema 文件和固定旧恢复不动，当前安装由原 writer 执行；不手抄受管副本 |

没有来源设计偏离或尚待用户选择的替代方案。

## 4. 模块、职责与设计取舍

M1 为既有 `NormalPhase0AuthoringTests.test_clarification_leaves_owner_derivations_to_recorder`。捕获真实 helper 发给 recorder 的 envelope 后，从 `owner_result` 取 authored。保留 content_identity、facts_sha256、disposition_digest、payload_sha256、action_digest 尚未由 owner 预填的检查，以及 duplicate_facts_sha256 来自 snapshot 的检查。对第二次调用，检查其 `owner_result is recorded`，并检查两次 envelope 的 change_request 与当前 issue 身份、标题、正文、updated_at 相符；继续观察 helper 返回 `(recorded, checked)`。mock 只隔离外部 recorder/checker，不伪造被测 helper 发出的参数。回退生产 helper 或删除原断言会隐藏真实偏差，因此不采用。

M2 为 Discovery 命令目录。只把 record-context-discovery、check-context-discovery、invoke-guru-discover-change-context、read-change-context-source 的 `schemas/public-issue-context-request-input-1.0.schema.json` 改为同目录已有2.0。保留每条 supplement1.0、output及owner schema声明。新增 schema、放松验证器或改业务分流都不是这项声明修复所需。

M3 为现有 package test。复用 `runtime.command.main` 的实际 help 与原 `issue_review.validate` 输入验证逻辑，在同文件补充定向行为回归。捕获 help 得到声明 schema 后，用正常输入证明该声明可用于装配，并与实际验证选择一致；不只比较固定字符串。不新增跨包通用测试框架、生产 validator 或状态。

## 5. 接口与数据

没有新公共 API、持久字段或数据迁移。M1 的生产者是现有 helper，消费者是测试：record/check payload 皆为 `{owner_result, owner_context:{change_request}}`，checker 的 owner_result 必须是 recorder 返回对象，来源内容保持同一真实 fixture。

M2/M3 的公开消费者从四个 help 取得 schema_bindings。context_request 2.0 正常输入有 profile、source_exit=needs_context、mode、issue、base_source、continuation_id、gap、review_focus 与 return_identity。return_identity.profile 为 Clarify 的 issue_readiness_supplement，其余身份与 focus 匹配。两种 focus 为 requirements/wording_only，按原 runtime 验证并观察匹配返回身份。

Discovery 自己的 supplement1.0 是另一输入：profile、mode、issue、base_source、continuation_id、source_exit=supplement_context、gap。它不接受新增 focus 字段。其兼容回归止于公开声明 schema 和原输入验证边界，不据此承诺未修改业务出口的全部行为。所有当前输入用正常合法 fixture，不手改 artifact/digest 构造范围外负例。

## 6. 状态、顺序、正常与失败流程

本批修复不新增生命周期状态。批准并 Activation 后，先修 M1/M2/M3，执行 V1/V2，再执行源合同与临时安装 V3/V4。只有工程验证及必要知识整合完成后，才进入原 TaskCommit、constructor/begin_check、一次独立完整 Check/Branch Review、readiness、Publish、Merge。

源码或安装失败保留原输出，在当前修复职责内处理；新需求选择回 Clarify，机制变化回 Author/Architecture。不能删失败输入、降低断言或借旧候选 pass 放行。本批 delivered 后 Completion 评估未实施的正式采用，并通过 additional_delivery_required 进入原 Creation；现在不创建或选中 D2。整体准备完成及 Finish 簿记合并后，Stage 2 重新获取最新 origin/main 冻结唯一候选。

## 7. 恢复、兼容、迁移与集成

历史1.0 schema文件保持；固定旧 provider 已开始的操作仍沿完整旧 provider 恢复，不混装或改写历史结果。当前 schema、DTO与运行语义未新增版本，因此没有数据库或状态迁移。测试消费迁移和帮助引用修正由当前源码提交提供。

临时项目使用原 CLI/workflow marketplace 与 canonical preset writer；声明为 local candidate 分发观察，不能证明 source_locked 或真实客户端 Agent。现有准备 checkout 的 installed 内容保持，后继 D2 从本批实际 delivered 的完整干净源经 guru-upgrade-tools 正式采用。Task/session/配置/peer保留由该原 owner 验证；主目录发布后最终收敛属于 Stage 2。临时安装或普通 apply 成功不能替代它。

## 8. 验证设计

| ID | 要求／验收 | 入口、输入与独立预期 | 层级及边界 |
| --- | --- | --- | --- |
| V1 | B1/BC1/AC10 | 执行既有四例 NormalPhase0AuthoringTests；真实 helper 原输入不变，record/check envelope、派生字段与来源绑定断言完整，无原 KeyError | 长期单元回归；不证明真实 gh 或 Agent |
| V2 | B2/BC2/AC11 | 四实际help→各自声明schema→正常context_request两种focus及匹配return_identity→原输入验证；supplement1.0独立合法shape同时验证 | 长期package回归；只锁公开输入可用性，不扩业务路线 |
| V3 | B2/B3/BC3 | 受影响Discovery package tests及原source package validator；Python改动内存语法、diff hygiene | 直接回归及静态合同，不声称安装采用 |
| V4 | B3/BC3 | 一个干净throwaway同时选择Claude/Codex/Cursor，经原CLI/workflow及当前preset完整安装、同源reapply；完整managed_source_projections集合/bytes/modes、installed validator、实际四help、manifest/lock/workflow、私有tests排除、sidecar核验 | 一次代表安装与三平台内容投影；不运行累计矩阵或真实客户端 |
| V5 | B4/BC4 | 完整当前B..H独立Review及真实delivered事实；Completion依真实采用缺口路由 | 生命周期事实，不用计划或临时安装冒充整体完成 |

原失败观察和未改helper/runtime可作为因果依据；不重新执行旧候选全部release suite。V1/V2修后观察原失败路径及最终结果，V4观察分发后消费，不将失败转移到安装层。只有实际触达或解释仍不清楚时补最小诊断；已有充分证据后停止，不要求重复红绿或回退实验。

## 9. Canonical 引用、本轮差额与实际未决项

本批 PRD 第7节定位的 R850-01/04、R868-03、R735-01..03/R868-04及对应 D/T，要求原owner与完整分发、最小充分验证和分层证明。本批修过期测试／命令声明，不改变这些当前能力定义。Architecture 的三份 authority 与实际 candidate_assessment 支持无影响；不创建空 contribution、ADR、共享索引或发布ledger。若实施揭示真实规则差额，由原 RDT/Architecture owner 在提交前 final_integration/readback，不能由源码 writer改共享authority制造符合性。

当前没有阻塞实施设计的产品或技术未决项。实际工程通过、final_plan、Approval、Activation、D1交付及后继采用均须在各自原边界取得，不能从本设计推断。
