# D1：新增范围的 Delivery 归属合同

## 1. 整体来源与术语

整体 authority 是 [Task PRD](../../prd.md)，accepted_scope revision 为 `sha256:50eb69092514127d481eb17f37ebc7b82ca0e58dcad779ba18072c355f29cd67`。本片 scope_ref 选择 R1、R2、R3；DeliveryKey 为 `778-delivery-scope-allocation / 0 / 6fbd5927-6045-42be-9d44-b4e01f8e86b3`，planning_root 为本目录。

| 来源 | 章节、角色与用途 |
| --- | --- |
| [#778](https://github.com/castbox/guru-trellis/issues/778) | R1–R3、边界和最小验收；完整要求与约定 owner/机制约束 |
| [#734](https://github.com/castbox/guru-trellis/issues/734) | R1 及其它治理的责任边界；相关证据，不是本片额外验收 |
| 原 Clarify `references/contract.md`、原 Author `references/authoring.md` | 当前实现与差额定位，不是新增需求 authority |

Task 负责整体 accepted scope；Delivery 负责所选切片。full/partial/staged 是现有 Policy 选择，不是未来新要求的默认分配规则。

## 2. 整体与本批目标、非目标

当前合同允许 Task 范围修订后沿原阶段回到同片规划，但未集中说明新增差额的归属判据。本片交付原 Clarify 的判据及原 Author 的承接规则，使整体扩围不会自动扩大当前片实现/验收，同时保留不可分修复和立即替换的合法同片/撤回路线。

本片完整覆盖整体 R1–R3。只修改其实际命中的 step-local Markdown 和必要原路由引用，并经原安装 owner 同步受管投影。整体非目标全部适用：不实现 #734 的预算、规模、QA、设备治理，不承担 #765；不新增 Skill、DTO、状态、账本、算法或固定门槛，不改上游或 Candidate。

## 3. 本批起点、前序结果、依赖与剩余责任

这是首片，尚无前序 Delivery 或已交付提交。开发基线为 `313d80215f65777fc70893a90c6d8dce8005d6dd`，PR target 为 main。起点是现有 Clarify、Author、Creation、阶段返工/撤回和 Candidate/base/Review 合同。

原 installed owner 必须保留本 Task/session，同步本片真正改变的 package/平台投影。没有 #734 整项交付前置。本片完成全部 R1–R3 后无计划内后继实现；Task Completion 仍须审查全部 AC 与交付事实。发布 PR 只完成本执行段，合并、Completion、Closure 各留原 owner。

## 4. 本批调用方、场景与流程

| 场景 | 调用方、前置、触发 | 处理与结果 |
| --- | --- | --- |
| S1 可后置新增能力 | 当前阶段接到允许分阶段且能独立后置的同 Task 能力 | Clarify 比较当前缺口、依赖和独立交付条件；将新增能力留整体剩余责任。Author 更新当前片必要来源/边界/依赖/Policy，当前实现/验收不自动包含新增能力；后继实施时由 Creation 建片 |
| S2 原合同遗漏 | 当前候选缺少原合同已经要求的行为 | Clarify 识别为原合同修复；原阶段同片返工，刷新受影响规划和门禁，不强制拆片 |
| S3 立即替换旧行为 | 新来源要求立即替换，旧片已不再有效 | 原阶段合法返工或撤回/重新规划；不得按旧合同发布旧行为 |

顺序是完整读新增来源 → 原 Clarify 判断归属 → 整体要求由原 Author/Clarify 写入并接受 → 当前阶段依法承接受影响切片。存在真实范围/时序选择才询问；具体委托按原交互合同承接。

## 5. 完整行为、条件与约束

R1：以已接受的需求、行为、验收为基准，区分修复、替换、独立新增能力。说明当前候选尚缺什么、新要求的依赖和后置后的合法独立交付条件。只要求同 Task 不能推定同 Delivery；明确当批共同交付的选择必须保留。

R2：修复、不可分依赖、必须立即替换沿原同片返工及受影响审核。独立可后置且来源允许分阶段的能力留整体剩余责任；当前片只维护必要边界和 Policy，不自动加入新增实现/验收。旧片失效时沿原撤回/重新规划。Author 在 Delivery PRD 和 implement 的唯一 Policy 中写真实当前覆盖、剩余责任和整体 Completion 条件；仅换 full/partial/staged 标签不算承接。

R3：归属判断优先于新增实现。已有混合内容先审实际可分离性，固定 B..HEAD 和实际 dirty 内容仍完整进入原 Candidate/base/Review。不能以新 UUID、少选路径或未交付提交充当前序规避范围。Clarify 判断、阶段执行、Creation 后继创建、workflow 路由、Approval/Delivery Review 核验各保原 owner，不新增拆片审核。

本片规范性来源约束的唯一设计处置由后续 design 第3节维护。复用全部公共字段、出口和原 scope_ref。没有脚本判定、运行数据或外部部署变化。

## 6. 本批验收、验证方式与未决项

| 验收 | 对应要求/场景 | 输入、入口与预期观察 |
| --- | --- | --- |
| AC1 | R1–R3 / S1–S3 | 原审核 owner 对修订后合同逐场景审查，得到 S1 后继责任、S2 同片修复、S3 旧行为不得发布的清晰路线 |
| AC2 | R1–R3 | 对照 Clarify、Author、Creation、原阶段和 workflow，确认边界、Policy、剩余责任、Completion 和询问条件均由原 owner 承接 |
| AC3 | 分发约束 | 经原安装 owner 同步实际差额，运行命中 package/投影和 dogfood drift 检查，副本一致且无未处理差额 sidecar |

当前无未决产品问题。技术落点由原 Author/Architecture 细化。上述尚未执行，不证明真实 Agent 行为、历史根因修复、成本下降或完整 upgrade/Release 矩阵。

## 7. Canonical 引用与本轮差额

仓库根定位：`trellis/skills/guru-team/packages/guru-clarify-requirements/references/contract.md` 的 Delivery scope revision，`guru-author-task-plan/references/authoring.md` 的 Policy 与实施范围修订。实际差额是在现有语义 owner 内补归属和承接方法。

RDT：`docs/requirements/current/task-delivery-lifecycle.md` 的整体责任/固定范围/返工，`docs/design/current/task-delivery-lifecycle.md` 的对应 owner，`docs/test/current/task-delivery-lifecycle.md` 的现有验证边界；`docs/requirements/current/requirement-decisions.md` 的真实选择合同。Architecture：`docs/architecture/README.md`、`00-foundation/design-constitution.md`、`06-governance/change-contract.md` 及 owner/distribution 单元。后续 owner 读取必要正文后判断实际知识差额，不以链接存在宣称无影响或预建空贡献。

Evolution 目标映射：EVO-001 来源保真、EVO-003 整体 authority、EVO-004 唯一 owner、EVO-005 真实选择才交互、EVO-006 原路由闭环、EVO-007 投影一致；EVO-002 继续由独立 Architecture 判断。本片不执行 Evolution 整体重构或扩展其验证集。
