# D3：README 正式归档恢复说明设计

## 1. 设计目标、需求承接与内容基线

承接 [本批 PRD](./prd.md) 的 R1–R4、S1/S2 和 D3-AC1–4；公共 scope_ref 只选整体 AC2。development baseline B 与 Planning H0 均为 `fad4f082231e5058c6f4d5f7ce5fc8c55e424937`，PR target 为 main。B 来自原 `DeliveryProjection.content_base`：本代无前序已交付切片，采用显式开发基线；实际实现 H 尚未形成，内容范围固定为 B..H。

独立 Architecture 已实际返回 `candidate_assessment / no_architecture_impact`：只纠正已有 family 说明，不改变决策、职责、接口或兼容范围。适用 authority 为 `guru-trellis-architecture`、`guru-trellis-design-constitution-v1` 与 `docs/architecture/06-governance/change-contract.md`；最小必要复杂度在此体现为直接补正文案，不增机制、测试或空贡献。candidate assessment 不是 final_plan。

## 2. 当前系统、边界与目标差额

D1 已完成版本与文档准备，D2 已完成 existing caller 修复；两代交付保持原历史。现行 workflow、Reactivate Skill、RDT 和 Architecture 已支持当前 Task2 及指定正式 schema1。顶层 `README.md` 的“已归档任务复审”段仍只写当前上游 schema，目标差额仅是该段的准入说明。

将过窄句改为简短说明：两类正常正式归档沿原 Reactivate 合同；先核当前合法后继，无后继且满足资格时才经匹配公共操作增代；同操作恢复继续原操作。完整资格只由链接指向的原 owner 定义，不在 README 复制协议。

## 3. 来源设计处置（唯一）

| 来源/原承诺 | 处置与落点 | 理由、影响及上游处置 |
| --- | --- | --- |
| 原 Reactivate Skill：Task2 使用原 reopen；所选正式 schema1 经 matching formal operation | retain；本设计第2/5节，README 原合同链接 | 补齐已存在 family，公共 SDK/parser/owner 无变化，无需上游改约。 |
| 同 Skill：优先核验合法后继；输出丢失及同操作恢复不重复增代 | retain；第2/6/7节，README 简短条件 | 不把每次阅读或重试写成新 generation。 |
| canonical workflow 的正常归档段：人员字段排除，人工历史、未完成 closeout、旧 Finalizer 各走原路线 | retain；第2/6节，README 完整段 | 保持否定与例外，不扩任意 legacy schema1；没有迁移写入。 |
| MIGRATION-669：原 clean-base profile 与新增 existing-implementation profile 独立，matching 安装与历史证据分层 | retain；第5/7节及原合同链接 | README 不增加第三入口或重解释旧 profile；不重跑无关工程验证。 |
| 整体 PRD R5–R8 与 #656：两次完整独立 Review、原收尾、Stage 2 独立 | retain；第9节统一执行路线 | 新 D3 本身执行两轮，不借 gen1 pass；不新增公共 phase/schema 或发布账本。 |

## 4. 模块、职责与设计取舍

README 写作 owner 只修本段两句及必要换行。原 Reactivate owner 继续判断历史、资格、后继、公共操作和 route；Trellis 继续单写公共 Task/generation。原 RDT/Architecture owners 判断共享知识是否有真实差额。当前定义已正确，无 contribution 或 ADR 候选，不新建全局文案分类器、校验器或镜像字面测试。

## 5. 接口与数据

调用关系为 README 的原 Skill 链接 → `guru-reactivate-task` 的既有独立 profile → 原 reopen/formal 公共操作 → 真实 key/ref 与既有 Planning/Bind/recovery consumer。完整闭合 I/O 仍由原 Skill 拥有；本批不改 public input/output、schema、runtime 或持久化数据。D3 planning 与 Task 生命周期资料只是本次正常交付对象，不是新业务协议。

## 6. 状态、顺序、正常与失败流程

文案修改本身没有运行状态转换。先完整对照旧段及现行合同，再补正常正式 family 和后继条件，最后核保留的旧状态分流与链接。正常读者可定位原 owner；具体恢复仍由原 owner 核完整资格，不能仅凭 README、summary 或已合并 PR 放行。发现来源冲突或扩大 legacy 准入时停止文字修改，回原 Author/Architecture；真实 scope 冲突才回 Clarify。

## 7. 恢复、兼容、迁移与集成

原 Reactivate 同操作 recovery 和合法后继优先继续的语义不改，未完成 closeout 仍回原 Finish/维护路线。本批没有数据转换、安装升级或新恢复协议，也不改既有 profile 的 consumer 兼容。旧规划、归档、失败样本、native/业务/生产未验证边界保持原观察。新 README 与本批实际质量结果合并后，原 Release owner 从新的精确候选完整执行 Stage 2；旧候选 pass 不迁移到新候选。

## 8. 验证设计

| 验证 | 对应 AC、入口与输入 | 预期观察及边界 |
| --- | --- | --- |
| V1 语义对照 | D3-AC1/2；AI 读 README 完整段、原 Skill、canonical workflow 和第3节来源 | 两类正式 family、原 owner、后继优先/同操作恢复和所有旧分流一致；这是正文语义审查，不是 runtime/native 行为证明。 |
| V2 链接与范围 | D3-AC3；解析 README 本段 Markdown 链接并核原 Skill 文件；`git diff --check`；完整 B..H 与 dirty/untracked 差额 | 链接可解析；除 D3 规划和正常生命周期资料外，业务差额只含顶层 README。无 code/runtime/Fork/公共合同变更。 |
| V3 分发与文档合同 | D3-AC3；原 source/installed package validators、四个 source platform roots 及私有 release Skill parity | 相关分发仍一致。当前 Check owner 先定完整必要集合，再判断未变输入的现有工程事实是否适用；受影响或缺失项实际执行，不能以旧 semantic pass 替代。 |
| V4 双 Review 与收尾 | D3-AC4；第9节各原 owner 的真实输入、完整候选与结果 | 两次独立完整 Review 均真实发生；第一轮不写正式 full_review，第二轮消费当前最终 Check。准备不声称 Stage 2 或 Release 成功。 |

不新增镜像文本测试，不重复 heavy 安装、existing upgrade 或多平台矩阵。本批不改 V3/V4 工程机制；后续原 owner 只按实际输入适用性消费既有事实，最终 Stage 2 仍按发布合同重跑全部定向 gates。

## 9. Canonical 引用、本轮差额与实际未决项

Canonical requirement/design/test 与 Architecture 引用及差额见 [PRD第7节](./prd.md#7-canonical-引用与本轮差额)；本批只修派生 README，现行 RDT/Architecture 定义无差额，不创建空 contribution 或共享 promotion。Docs SSOT strategy 只在 implement 第6节定义。

本 generation 2 / D3 的有界恢复路线如下；它是当前计划，不继承 gen1 例外或 pass：

1. 原 Wording、final_plan Architecture、独立 Approval 和 Activation 完成后，写 README 并做 V1/V2 最小自检。
2. 原 TaskCommit 的 early 入口形成真实 H，原 Publish 只建立同 PR Draft 反馈；它们不制造最终 Check、Publication 或 full_review。
3. 实施按固定 B/真实 H/完整内容 candidate 与 begin_check；原独立 Architecture/RDT candidate 阶段及完整 candidate Check 覆盖全部九维，成功只返回 `candidate_checked` 并合法回 implementing。
4. 使用原 `delivery_draft_content_review` carrier，由独立原 Review owner 完整审 B..H、需求/规划/适用消费者/验证及正常场景，零开放 P0–P3 才继续。该次是本批晋升前完整独立恢复 Review；它不伪装公共 `full_review`，也不替代下一次正式 Review。
5. 消费步骤3的真实 `candidate_checked`，原 Architecture/RDT 串行 final_integration 复核实际内容。当前无共享差额则真实 no-change，不造空贡献、promotion 或提交；有实际差额回最早受影响 owner 和必要 gates。
6. 实施重新绑定 actual after candidate/begin_check；原最终 Architecture 与完整公共 final Check 覆盖实际内容。
7. 原 TaskCommit 对 clean committed candidate 使用 committed reentry；有必要真实 dirty 差额则走原精确提交。无差额不造空提交。
8. 独立原 Review owner 再审完整 B..当前 H，形成当前正式 `full_review`。即使 H 不变，也独立判断当前最终 Check predecessor、全部范围和原质量责任；步骤4不能代填。
9. 原 publication Architecture/readiness、Ready Publish、expected-head Merge 后，再由全 Task Completion、Closure `no_mutation`、acceptance_finish Architecture、Finish 和精确 Cleanup 各原 owner 接续。Stage 2 留原 Release owner。

各真实 Git/GitHub 动作由原 owner 在动作前展示精确目标与写集，授权及过程不写入任何 artifact。现无产品或设计未决项；上述原 gates 尚待各 owner 实际执行，本文不声明通过。
