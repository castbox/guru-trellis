# D1：实际 PR 范围与前驱安排的规划方法

## 1. 设计目标、需求承接与内容基线

承接 [本批 PRD](prd.md) 的 R1–R6、S1–S5、AC1–AC5，以及 [整体 PRD](../../prd.md) 的完整约束。目标是把必要的内容关系判断放在原 Author 确定 PR 目标时，由原 Approval 判断安排能否执行，减少晚期返工。

开发起点及拟选固定 B 为 `e30c7bb5d4c24bc075dc14cfcd04c1da00fcf78e`，来源是本 Task 从同步 main 独立创建；Planning H0 为同一提交。目标为 `castbox/guru-trellis:main`，观察目标也为该提交。起点未继承旧查询/旅程 Task，当前没有未交付继承前驱。本 Task 未来实际候选按原 constructor 绑定 B..H 全部内容，不能用变化的目标替换 B。

已实际消费独立 Architecture 的 `baseline_current / planning / candidate_assessment`，Dkey 为 `delivery-target-preflight / 0 / ab2f681d-68b8-4678-8f76-bb4dfad94c6b`。结论为 `no_architecture_impact`；baseline identity 为 `guru-trellis-architecture`，constitution 为 `guru-trellis-design-constitution-v1`。原 DTO 位于外部 `delivery-target-preflight-architecture-candidate-public.json`。本方案保持其理由：原职责内补文本，不改 owner、接口、runtime、状态、发布能力或晋升边界，不创建 contribution/ADR；最终方案仍须独立 final_plan。

## 2. 当前系统、边界与目标差额

原 Author 已分别定义固定内容范围和目标，PRD/Policy 已有依赖及剩余责任；Approval 已有独立交付判断。缺口是 D1 无同 Task 前序容易被当作没有跨 Task 继承，未要求具体判断起点内容如何进入计划 PR 目标。

本轮只修改五处 canonical Markdown：Author 的 `references/planning-body.md` 和三个 Delivery 模板，Approval 的 `references/contract.md`。共享方法写在 planning-body 第4节；模板定位并消费它，Approval 在原 Policy 维度消费它。无需新脚本、schema、公共 DTO、状态或发布能力。原 Delivery Review 仍核发布时实际事实，原 Publish/Merge 仍执行其已支持动作。

## 3. 来源设计处置（唯一）

唯一需求来源为外部 `delivery-target-preflight-request.md` 全文，producer locator 沿本批 PRD 第1节；外部 proposal 是拟改参考，不增加 authority。以下逐项保留其已约定约束，PRD/implement 引用本节。

| 来源条款 | 原承诺与处置 | 本方案落点、理由及影响 |
| --- | --- | --- |
| request 要求1 | retain：起点、固定内容、目标分开；差额只是线索 | 第4/6节的方法先观察再判断，不用路径数直接阻塞 |
| 要求2 | retain：同/跨 Task 必要依赖，信息关联不加义务 | planning-body 主定义明确调查命中的必要关系，不盘点接手其它 Task |
| 要求3 | retain：原 PRD/唯一 Policy 承载动作、条件、owner、恢复事实；独立开发合法 | 第4/6节及 implement 第5节，不加统一前驱合并前置 |
| 要求4 | retain：原 Approval/Delivery Review，发布安排受真实能力约束，变化回原 owner | 第4–7节；不实现任意堆叠 PR 或自动 retarget |
| 要求5 | retain：最小五处文本、原分发，禁止新状态/台账/门禁 | 第2/4/7节；受管投影由原安装 owner 写 |
| 要求6与验收 | retain：真实回放和控制，观察识别及误阻塞，机械检查不能替代行为 | 第8节；不预填候选成功或新版优胜 |
| 非目标 | retain：旧Task、业务、远端交付和产品缺陷率不纳入 | 第2/7/8节及本批PRD；无承诺变更或上游处置需求 |

## 4. 模块、职责与设计取舍

所有下列路径相对 `trellis/skills/guru-team/packages/`。

| 文件/原 owner | 具体修改与消费 |
| --- | --- |
| `guru-author-task-plan/references/planning-body.md` 第4节 | 在既有上下文之后补两段主定义：分别核同Task前序与跨Task继承；确定目标时读来源明确的Git内容关系和必要公共交付/PR事实，判断内容归属、会否进入PR及必要依赖；在原PRD/唯一Policy写可继续工作、依赖动作前提、原责任及恢复观察。前驱Check/Review不能替代实际交付；普通目标前进不自动同步/Reconcile/重跑。 |
| `guru-author-task-plan/templates/delivery-prd.md` 第3节 | “首次无前序”限定为同Task，并引用共享第4节核必要跨Task依赖；保留当前状态、剩余责任和Completion条件。 |
| `guru-author-task-plan/templates/delivery-design.md` 第1节 | 引用共享第4节核目标与起点实际内容关系；顺序与依赖条件归唯一Policy，不复制方法。 |
| `guru-author-task-plan/templates/delivery-implement.md` 第5节 | 引用共享第4节落实实际发布安排、可继续动作、依赖前提/原责任/恢复观察；分支名称不能替代安排。 |
| `guru-approve-task-plan/references/contract.md` 既有 closed Delivery policy 段后 | 引用同一主定义，判断实际内容、适用审核覆盖与发布顺序是否经原owner可执行；明确前提可留给后续依赖动作，批准不等于前提满足或Ready。缺安排回原修订，真实scope/target选择回原authority。 |

不修改 runtime 来推断依赖，也不增加通用 helper 或前驱登记。与保持原文相比，本方案使方法更明确，但增加必读文字与核事实成本；只调查实际命中的必要依赖，模板用短引用控制重复。与新增机器门禁相比，它保留 AI 语义判断及合法路径，不制造额外状态和恢复成本。若候选观察出现无收益且成本明显增加，先收窄重复表述；出现误阻塞则修订对应规则，不改冻结输入制造优胜。

## 5. 接口与数据

无 public 输入/输出、字段或状态变化。原调用链为：Author 原 profile 加载共享正文与模板 → 在原 PRD/design/implement 写事实及 Policy → Wording → 独立 Architecture final_plan → 原 Approval → 原 Activation。输出仍是现有 `requirements_ready`、`plan_ready`、`pass`、`approved` 等原合同出口。

Git/公共 Delivery/PR 是事实来源，不获得 scope 或 pass authority。目标名称不等同可执行发布安排；必须读取原 Publish/Merge 的实际目标绑定和支持条件。本文不宣布任何额外 target/stack 生命周期支持。

## 6. 状态、顺序、正常与失败流程

没有新增状态转换。确定目标时先记录起点、固定内容范围、观察目标，再按命中差额调查归属和必要交付事实。同Task D1无前序仍核跨Task继承。内容已进入目标或有充分等效事实时，不因历史目录、旧叙述或SHA不同阻塞。

必要前驱仍待交付时，在原Policy写明哪些独立动作现在可做、哪个后续动作等待什么结果及哪个原owner补齐。Draft能否继续以原能力和范围为据，不加统一等待规则。缺事实只暂停实际依赖动作；不可执行安排回原Author修订，真实scope/目标选择回原authority。普通无关目标前进不改变固定B。

Approval消费同一安排，核内容、审核覆盖和顺序能否落实；规划通过不表示前驱已交付。Delivery Review在发布前核实际范围及变化。原流程支持的选择/恢复继续使用原typed exits，本方案不改其语义。

## 7. 恢复、兼容、迁移与集成

五处改动是原文本方法的补足，无API/schema/data迁移；在途工作仍由其当前owner读取适用合同，不靠本Task重建旧身份、重写固定B或刷新无关门禁。安装更新由原 `guru-upgrade-tools` 完整source的preview→prepare→invoke执行，先审冻结写集与保留路径，再实际同步本checkout受管包及已声明Claude/Codex/Cursor投影；不手补安装副本、不修改用户配置或其他Task/session。

RDT差额只由原维护owner更新既有 `task-delivery-lifecycle.md` 三层完整单元，按原隔离拟写、候选Check、final integration/readback顺序晋升；不新建平行current文件或共享README/index。no-impact不创建Architecture贡献/ADR。普通安装失败或sidecar冲突交原owner恢复，同操作不扩大为历史迁移或完整Release矩阵。

## 8. 验证设计

| 验证 | 要求/验收、入口与输入 | 观察和边界 |
| --- | --- | --- |
| V1 文本/分发 | R5/AC4；五处diff，原source/installed validation，原分发测试 `test_planning_body_distribution.py`，reapply/drift与三平台投影 | 方法主定义唯一，投影一致且Task/session保留；机械层不证明Agent消费 |
| V2 四case方法对照 | R1–R4/R6、AC1/AC2/AC5；冻结四case、同模型medium/工具/预算，旧main与仅变五处候选 | 记录首次识别、安排可执行性、误阻塞、耗时/调用/输出及途中干预；控制四case已exit0且本问题均正确是当前主会话观察，不声称候选已跑或新更好 |
| V3 Approval-only最小对 | R4/AC3；相同事实，一份缺交付安排、一份含明确可执行安排，独立给方法执行者；不透露判据/另一输入结果 | 观察缺安排被识别、完整安排不误阻塞。若四case原始观察已真实覆盖这两个分支且输入可分辨，采用其结果免重复；否则主会话协调一次短pair。方法消费/自评不等正式独立Approval。 |
| V4 原质量链 | R5/R6；完整源码、受管投影、原RDT三层差额及真实工程结果 | 原Check、独立审查各按既有范围执行，不以方法回放代替正式gate；此阶段不预填pass |

先采用仍适用工程事实，再跑命中检查。行为协议已冻结，不修改输入、不给中途答案、不延长预算掩盖首次失败。保留环境失败/未完成/行为错误的不同归因。若控制已经正确，报告本样本无新增行为收益；正确性和成本分开，候选漏检或过度阻塞时先修订/撤回规则。证据足够即停，不追加等价参数。完整多平台Release矩阵、生产采用与产品缺陷率未验证。

## 9. Canonical 引用、本轮差额与实际未决项

RDT-REQ-LIFECYCLE、RDT-DES-LIFECYCLE、RDT-TST-LIFECYCLE 分别位于 `docs/{requirements,design,test}/current/task-delivery-lifecycle.md`；本批PRD第7节已定位命中关系。由原RDT owner在原单元补规划/消费/验证方法。Architecture依据本轮真实candidate_assessment与 `docs/architecture/00-foundation/design-constitution.md`、`06-governance/change-contract.md`；no-impact不产生贡献或晋升写入。

当前无新增重大scope/技术选择。候选效果、安装冻结写集及真实验证均待执行，不用控制成功代候选通过。是否可实施由后续原Wording、独立final_plan和Approval判断；当前计划不是激活或完成结果。
