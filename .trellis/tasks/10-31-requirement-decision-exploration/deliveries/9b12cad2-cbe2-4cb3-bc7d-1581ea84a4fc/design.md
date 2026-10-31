# D1 需求歧义探索与分级确认设计

## 1. 设计目标、需求承接与内容基线

本批承担 PRD 的 DEC-R1 至 R8、DEC-S1 至 S7 和 DEC-AC1 至 AC6。目标是改进原有探索与确认行为，不创建平行工作流。

开发基线 B 来自本次已同步 main：`a4feadd99683e006580ef16b078c44e3ad3648a7`。这是首次 Delivery，无前序已交付 head；Planning H0 与 B 相同，最终实现 H 尚未产生。内容范围为 B 到实际实现候选；未来 PR 目标 main 不代表本次允许发布。

实际独立 Architecture candidate_assessment 返回 baseline_current、no_architecture_impact，freshness 为 `sha256:12816ce50c3f1f818faebdce830ced087786da7ab4942b1713e8abf0c0455007`。authority 为 `docs/architecture/README.md`、`docs/architecture/00-foundation/design-constitution.md` 和 `docs/architecture/06-governance/change-contract.md`。该结果只支持本候选的预写评估，不代替 final_plan 或实现检查。

## 2. 当前系统、边界与目标差额

Clarify 已有证据优先、真实选择、问题生命周期和语义 Gate。Author 已负责方案写作，并将真实范围问题回 Clarify。共享 Interaction Budget 支持重大方案选择、自然语言确认和独立副作用边界。

差额为：具体发现歧义的方法；轻度推荐清单的呈现规则；重大技术取舍与纯实现细节的区分；新问题及回答影响的实际验证。当前单问题表述和 thin SKILL 提示必须同步，不能只新增一份无人加载的指南。既有 brainstorm 属于 upstream-owned 方法，不修改其文件；Guru owner 在原职责中明确组织对话。

## 3. 来源设计处置（唯一）

| 来源及原承诺 | 处置与具体落点 | 理由、影响与上游处置 |
| --- | --- | --- |
| Clarify contract：每轮一个最高价值问题，只有不可分选择可 atomic_group | change：轻度独立问题可合并呈现；每项仍独立 question_id 和问题记录；重大或依赖选择保留逐步询问。落第4至6节 | 用户新增简便确认要求；不扩大 atomic_group，不变公共 schema |
| Author planning-body 第2节：技术未定交 Author/Architecture，不让用户提供实现 | retain并细化：常规实现自主；暗含需求选择或重大取舍时仍回原 owner。落第4节 | 保留实现责任，消除静默决定需求的误读 |
| Interaction Budget：只问真实选择及副作用，明确答复才生效 | retain：增加轻度也须确认及推荐不是决定。落第4、6节 | 不增加例行审批，不扩大需求确认的副作用权限 |
| 问题生命周期：partial 不关闭问题，未知不伪装回答 | retain：清单逐项判断回答范围。落第5、6、8节 | 不以批量呈现制造整体接受；不写新台账 |

## 4. 模块、职责与设计取舍

1. 共享 `trellis/presets/guru-team/spec/workflow/workflow-contract.md` 的 Interaction Budget 单写跨阶段原则：证据事实自行查证；需求歧义必须确认；轻度推荐、重大选项；纯实现自主；未答不等于接受。按钮只在平台支持时使用，普通清晰肯定答复同样有效。
2. Clarify package 的 `references/contract.md` 单写探索动作：用正常例子、行为差额、相关旧问题和适用边界区分两种合理解释；按真实性质组织问题；处理逐项答案及未决停点。原 SKILL 与其同一职责内的提示改为引用共享规则，消除每轮单问题的绝对表述冲突。
3. Author 的 `references/planning-body.md` 与 `references/authoring.md` 明确新发现需求选择回 Clarify；重大方案取舍先研究选项，不能要求用户写代码，也不能借技术细化改需求。现有 `clarify_scope` 路由承接，不新增出口。
4. `references/contract.md` 可链接 package 内新增的教学例子，展示事实自查、轻度清单、部分回答、否定推荐、重大取舍、纯实现自主、UI 旧行为保持及恢复。例子明确不是当前答复或真实测试。
5. 定向测试负责当前合同 consumer、问题 reducer 和分发一致性。新增 source-only 对话评测资产承载合成需求与后续测试用户回复；native runner 通过实际 `codex exec`/`resume` 分轮运行，只采集实际事件、退出码及工具错误，AI reviewer 判断语义。被测 Agent 首轮不能读取后续回复或评分答案。

不采用独立 Socratic Skill，因为它会复制 Clarify/Author 职责。也不整体引入兄弟模板的强制矩阵、ADR和 Issue 同步机制，因为当前没有这些额外 consumer。重大选择的形式由影响决定，不按文件数量判断。

## 5. 接口与数据

无新公共 API、typed exit、持久化状态或 schema。原 standard_intake、reviewed_plan_intake、active scope 与 Author profiles 仍经原入口及 consumer 执行。

轻度清单只是用户可见的呈现组合，不是新原子决定：每项有独立 question_id；实际同一回复可分别解决多项，按各项实际答复记录，不虚构多次用户发言。不使用 atomic_group 表示独立条目，不给未答问题填写 complete/refused。现有每条问题记录保持一条主问题与真实回答；记录的 round_id 按既有唯一约束使用，不新增 turn 状态。

原 `opened_question_ids`、`closed_question_ids` 和 `answer_status` 继续承接。一次明确接受完整已展示清单可逐项关闭；只接受一项时其余仍未决；修改推荐时写实际选择，不保留原推荐为已接受要求。

## 6. 状态、顺序、正常与失败流程

正常顺序：调查事实与有效决定 → 用例子发现歧义 → 区分事实、需求选择和常规实现 → 展示合适问题 → 等待实际回答 → 逐项更新需求/设计/验收 → 复核未决项 → 原规划审核。

无未决需求时直接规划，不为满足形式制造问题。未答或部分答复时暂停依赖行为，独立调查继续。用户问题或修订请求不是接受。Author 展开方案后发现新需求问题时走原 Clarify 回程，仅处理新问题；实际来源、约束或 scope 改变时刷新受影响规划。

事实证据不足时如实保留 gap；服务器等外部事实不能用用户偏好替代。UI 设计缺画面不自动建立删除业务的要求。原副作用、身份、freshness 和完整规划激活顺序均保持。

## 7. 恢复、兼容、迁移与集成

无数据迁移，因为公共字段和存储结构不变。旧问题 reducer 的关闭约束保持，需用真实 recorder/checker 验证清单的逐项映射；若现有接口不能表达，则回 Author/Architecture，不擅自增加 schema。

恢复时重用仍适用的决定和证据，新歧义重新处理。native 对话评测使用真实 thread.started 身份恢复同会话，不通过 --last 选择其他会话。执行错误不算语义通过，保留失败与未验证边界。

canonical 修改后通过本工作区 `trellis/presets/guru-team/scripts/bash/apply.sh --repo .` 同步 dogfood/安装副本，再检查 drift 和 sidecar。遇到非本次修改的文件冲突时保留并报告，不覆盖。源变更不代表其他项目已升级；已有项目采用需后续独立操作。

## 8. 验证设计

| 验证 | 要求与入口 | 预期观察及边界 |
| --- | --- | --- |
| DEC-V1 | Clarify package 定向 unittest，R3/R5 | 原 recorder/checker 接受真实逐项完整回答；部分回答、未答及 close-before-open 保持原约束；不是对话质量证明 |
| DEC-V2 | 规则 consumer 与规划/示例分发测试，R7 | 原 owner 实际引用、canonical 与安装投影字节一致，重复 apply 无未处理漂移 |
| DEC-V3 | 隔离 native 多轮对话，R1至R6/R8 | 场景含事实自查、清晰请求、轻度清单、重大取舍、部分回答、拒绝推荐、恢复和 UI 保持；AI 核对实际提问、回答影响与停点，不用关键词脚本评分 |
| DEC-V4 | native runner 定向测试，R8 | 后续回复不提前暴露；实际 session ID 承接；超时、非零退出及缺失事件不被报告成完成 |
| DEC-V5 | source/installed package、dogfood drift、JSON/Python/Bash与 diff 检查，R7 | 相关分发及工程约束通过；不代替完整多平台 Release/升级矩阵 |

DEC-V3 明确区分问题方法试验与完整 Guru 生命周期证据；前者不能宣称 owner 自动路由或正式 Gate 已通过。正式 per-question bookkeeping 由原 wrapper 定向测试覆盖，不用测试脚本预写语义结果。若需要正式入口的多轮验证，沿现有 native authoring 适配器使用真实前序，不虚构 context_ready。

## 9. Canonical 引用、本轮差额与实际未决项

requirement/design/test authority 分别由 `docs/requirements/README.md`、`docs/design/README.md`、`docs/test/README.md` 导航。本轮当前交互方法差额由原 RDT owner 在隔离候选中维护完整需求、设计与测试单元，再经原 final integration 晋升；规划不直接改共享导航。

Architecture candidate_assessment 确认无架构影响，不创建空贡献或 ADR；final_plan 仍须审当前实际设计。必要工程合同为 workflow 的 Interaction Budget、skill-package-contract 的最小公共 I/O/分发、quality-guidelines 的 Test And Validation Value 及 Validation Scope Ownership。无待用户选择的需求问题；native 行为尚未执行，不能声称效果已验证。
