# 在规划中识别实际 PR 范围与未交付前驱：整体需求

## 1. 来源与术语

本 Task 的 source 为 `no_issue`。唯一需求来源为 `/Users/devSC/Documents/JobProject/guru-validation-evidence/fizz-filter-controlled-2026-11-10/host/delivery-target-preflight-request.md` 的完整正文；原 readiness public 的 `transition.target_locator` 为 `draft:07939adebf332aeec2dc22a4b78d48ff84849ebdd44d3f20047e9e800791d86b`，`source_selection=[]` 是实际空选择，不表示来源丢失。

| 来源 | 角色与用途 |
| --- | --- |
| 上述 request 的“当前请求”“要求与设计约束”“非目标与当前交付边界”“验收” | 当前要求及约束；完整承接本 Task 的目标、边界与验收 |
| request 的“问题与事实” | 历史案例，用于回放，不把旧 Task 交付纳入当前范围 |
| `trellis/skills/guru-team/packages/guru-author-task-plan/references/planning-body.md` 第1–5节、`references/authoring.md` 的 Fixed Delivery range 与 Policy 合同 | 当前已有规则与实现事实；补足原职责，不新增阶段 |
| `trellis/skills/guru-team/packages/guru-approve-task-plan/references/contract.md` 的独立交付维度 | 原审核消费方；判断具体交付安排是否可执行 |
| 外部 `delivery-target-preflight-proposal.md` | 拟实现候选参考，不替代 request，不作为新增需求 authority |
| 外部 `delivery-target-preflight-behavior-protocol.md` | 已冻结的行为对照方法；不能用其存在证明行为通过 |

开发起点是实际开始本切片的 Git 内容；固定内容审核范围是本 Delivery 的 B..H；计划 PR 目标是拟接收内容的分支。三者分别判断。未交付前驱指起点继承、尚未进入目标且对实际交付有必要影响的内容；同 Task 和跨 Task 均可能存在。提交或路径差额只提供调查线索，不独立证明归属、已交付或阻塞。

## 2. 背景与问题

历史 `resume-step-context` 审核范围为 `26630149070e2988ad08102679931468b3535ef8..7027b75c845d35278022bb06f66d48320e0d6eb9`，123路径；当时 main 为 `e30c7bb5d4c24bc075dc14cfcd04c1da00fcf78e`，实际三点 PR 差额177路径，其中额外54路径来自尚未交付的跨 Task 前驱。最终 Delivery Review 因 `predecessor_delivery_pending` 停止。该历史事实来自 request，不表示本 Task 已运行回放。

原规划已有前序事实、依赖、独立交付及固定内容范围规则，但没有充分展开跨 Task 继承与实际 PR 目标的关系。D1 没有同 Task 前序，不代表起点没有未交付前驱。期望在 Author 确定目标时形成可执行安排，Approval 审核它，减少实现后才发现发布依赖的返工。

## 3. 目标与非目标

整体目标是在原规划中提前识别实际 PR 内容关系，并对真正依赖给出可执行交付安排。范围为五处 canonical：Author 的 `references/planning-body.md`、`templates/delivery-prd.md`、`templates/delivery-design.md`、`templates/delivery-implement.md`，以及 Approval 的 `references/contract.md`。受管分发、原 Docs 维护和定向验证属于该改动的必要交付责任。

不修改客户端/后端业务，不接手查询或旅程 Task 的交付，不修改旧123路径提交或旧 Task 状态。不新增 runtime、DTO/schema、phase、审批轮次、持久化前驱台账、授权记录、全链 digest/freshness 或仅因目标前进而触发的 Reconcile 门禁。不为教学案例增加通用门禁。不在本请求内 push、创建 PR、merge、部署、归档或 journal。效果声明限于规划识别及返工边界，不宣称产品缺陷率下降。

## 4. 真实调用方、场景与流程

| 场景 | 调用方、前提与动作 | 要求行为及可观察结果 |
| --- | --- | --- |
| S1 未交付跨 Task 继承 | Author 在继承前驱的起点上确定 main 目标 | 读 Git 与公共交付事实，判断实际归属、必要依赖和支持的交付安排；首次规划即可说明范围差额、可继续动作及真正停点 |
| S2 前驱已进入目标 | Author 读取已合入或等效内容关系 | 依据内容和实际事实判断已满足，不仅凭 SHA 不同增加阻塞 |
| S3 明确且受支持的发布安排 | 前驱尚未进入最终目标，但原 Publish/Merge 有可用的具体安排 | Policy 写明顺序、条件、剩余责任与恢复事实；独立开发继续，Draft 依实际能力判断，不一律等前驱合并 |
| S4 目标仅有无关前进 | 起点与目标比较出现无关提交 | 不将该差额升级为必要依赖，不追加同步、全链重审或阻塞 |
| S5 方案遗漏或条件改变 | Approval 审规划，或 Delivery Review 发布前发现变化 | Approval 在原独立交付维度识别遗漏/不可执行安排；后续变化回真实原 owner，不自动改范围、固定 B 或 PR 目标 |

连续流程为：确定起点/固定审核范围/目标 → 读取实际内容与公共事实 → 判断必要依赖 → 在原 PRD 与唯一 Policy 说明动作和条件 → 原 Approval 判断可执行性 → 后续 Delivery Review 核对实际变化。此流程不新增状态或 public route。

## 5. 行为要求

- R1（S1–S4）：原 Author 确定计划 PR 目标时，分别说明开发起点、固定审核范围和发布目标，核对当时可得的实际内容关系。差额不能直接作为归属、已交付或阻塞结论。
- R2（S1–S4）：识别同 Task 与跨 Task 的必要依赖。尚未进入目标的继承内容须明确归属及交付安排；信息性关联、普通目标前进和无关变化不新增义务。
- R3（S1、S3）：结果留在原 Delivery PRD 上下文及唯一 Delivery Policy。写明可继续动作、依赖动作的具体条件、剩余责任 owner、恢复所读的实际事实。必须保留带明确依赖继续独立开发的合法路径，不一律要求前驱合并后才可编码或创建 Draft。
- R4（S3、S5）：原 Approval 判断安排是否可执行，原 Delivery Review 保留最终核对。安排以原 Publish/Merge 的实际能力为依据，不虚构堆叠 PR 支持。未知或变化回真实原 owner，不自动重写范围、固定 B 或目标。
- R5（全部场景）：在第3节五处 canonical 的原职责中完成最小修改，沿原安装机制分发；保留全部禁止扩展边界及原语义门禁。
- R6（全部场景）：验证未交付前驱回放、前驱已进入目标、受支持安排和无关目标前进。观察首次识别、可执行 Policy 及误阻塞，不以模板/关键词存在或 scanner 成功代替 Agent 行为。

## 6. 约束与依赖

本 Task 从 `main@e30c7bb5d4c24bc075dc14cfcd04c1da00fcf78e` 独立创建，当前开发起点和观察到的目标均为该提交，不继承 `7027b75c…` 或旅程未交付内容。当前没有因内容继承产生的发布前驱。后续 HEAD 的实际内容、审核和目标事实仍由原 owner 判断。

五处源码合同的受管安装投影由原安装 owner 同步；不能手补安装副本。原 RDT/Architecture 维护各自当前知识，仅维护本轮真实差额，不靠 Task 文档替代 shared authority。数据/API/公共状态均无新增，因此无数据迁移或运行时兼容切换。普通目标前进不是重新同步的统一前置。

原 Publish/Merge 支持何种发布安排须据实际合同判断；未知能力只限制依赖该能力的安排，不阻止独立实施。后续规划/架构负责技术展开，不要求需求方提供代码。

## 7. 可观察验收与验证方式

| 验收 | 要求/场景 | 入口、输入与预期观察 |
| --- | --- | --- |
| AC1 | R1/R2，S1 | 从原 Author/Approval 行为入口输入历史等效未交付跨 Task 前驱；首次规划识别范围关系并给出具体交付顺序，不能只写 D1 无前序 |
| AC2 | R2/R3，S2–S4 | 同一冻结方法输入前驱已进入目标、实际受支持安排、无关目标前进；保留合法独立工作，不凭 SHA/差额增加误阻塞或同步/重审 |
| AC3 | R3/R4，S3/S5 | 原 Approval 对遗漏或不可执行 Policy 给出原职责内修订；完整可执行安排能够继续，Delivery Review 最终核对仍保留 |
| AC4 | R5 | 检查五处 canonical 的职责及原分发/reapply/drift、受影响声明平台投影；不新增 runtime/DTO/phase/台账/审批 |
| AC5 | R6 | 分别报告源码、实际安装与实际 Agent 行为证据，保留失败、未执行及环境差异；效果限于该样本规划行为，不宣称产品缺陷率下降 |

行为对照采用冻结协议，主会话协调执行；本 PRD 不把尚未运行的实验记为通过。分发测试证明对应机械层，不能代替 AC1–AC3。必要工程检查和独立审核继续归原阶段 owner。

## 8. 实际未决项

当前需求与范围没有待用户回答的必要问题。技术候选、具体 Policy 和 Docs Plan 由后续原 Author/独立 Architecture 展开；其可实施性尚未审核，源码、安装和行为效果尚未验证。范围接受不是 Planning 批准或实施完成。
