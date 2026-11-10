# D1：新增范围归属合同设计

## 1. 设计目标、需求承接与内容基线

本设计承接 [本片 PRD](prd.md) 的 R1–R3、S1–S3 与 AC1–AC3，以及 [整体 PRD](../../prd.md) 的完整范围。首片尚无前序 Delivery。目标是补足原 Clarify 的差额归属判断，并让原 Author 按该判断维护真实切片。

固定 development baseline B 和 Planning H0 均为 `313d80215f65777fc70893a90c6d8dce8005d6dd`。B 来源是明确选定且当时与远端一致的 origin/main；后续 Candidate 仍由原 constructor 覆盖 B..实际 HEAD 和 dirty 增量。PR integration target 单独为 main，不用其后续移动替换 B。

阶段 authority：`docs/architecture/README.md` 的 `guru-trellis-architecture`、`00-foundation/design-constitution.md` 的 `guru-trellis-design-constitution-v1`、`06-governance/change-contract.md`。原独立 Architecture candidate_assessment 已正式返回 no_architecture_impact，说明候选在既有职责和路由中补足方法，不改变公共模型、持久化、single-writer 或兼容边界。本设计仍须经 Wording、fresh final_plan 和 Approval；候选结论不替代这些结果。

## 2. 当前系统、边界与目标差额

Clarify 已拥有来源、整体范围和真实选择；schema2 的 pre-Author → 根 PRD → acceptance → 原阶段路线已存在。Author 已拥有唯一规划写作、full/partial/staged Policy 和 implementing scope-revision 承接。Creation 已拥有首片/后继创建，Candidate/base/Review 已覆盖完整内容。

缺口位于整体接受新增责任与当前切片承接之间：当前 Author 默认 full，范围变化的说明主要展开同片回规划，没有集中要求先辨别独立可后置差额。本片直接修改两个 canonical Markdown：

- `trellis/skills/guru-team/packages/guru-clarify-requirements/references/contract.md`：在当前 Delivery scope revision 附近集中定义归属判断。
- `trellis/skills/guru-team/packages/guru-author-task-plan/references/authoring.md`：在 Policy 与实施范围修订说明中消费该结果，明确当前片与整体剩余责任。

两包 SKILL 入口已经要求完整加载各自合同，workflow 已有唯一消费者和合法返工/撤回/Creation 路由，因此计划不复制内部规则到 workflow、launcher 或新增入口。实施若发现真实路由引用缺口，先回原 Author/Architecture 判断差额。

## 3. 来源设计处置（唯一）

#778 包含规范性 owner、顺序、数据和验证约束。下表保留这些承诺，不将其降为建议。

| 来源条款与原承诺 | 处置 | 具体落点、理由与影响 | 上游处置 |
| --- | --- | --- | --- |
| R1：先读完整来源，区分修复、替换、独立新增；同 Task 不推出同 Delivery | retain | §4 Clarify 判断单元与 §6 顺序；修复错误归属前提 | 无偏离 |
| R1：说明当前缺口、依赖、独立后置条件；仅真实选择询问，承接具体委托 | retain | Clarify 新增正文引用原 Interaction Budget；不增加固定问答 | 无偏离 |
| R2：修复、不可分依赖、立即替换沿同片返工；旧片无效走撤回/重新规划 | retain | §4 Author 与 §6 分支，保留原阶段执行权限 | 无偏离 |
| R2：独立可后置且允许分阶段进入剩余责任；后继实施再 Creation，不建第二 current | retain | Author 更新 PRD/唯一 Policy 的真实边界，Creation 路由不变 | 无偏离 |
| R2：full 不吸收未来全部要求；partial/staged 必须改变实际边界和 Completion 说明 | retain | 修改原 Policy 段与 implementing scope-revision 解释，不新增 Policy 类型 | 无偏离 |
| R3：先归属再新增实现；混合内容不能靠新 UUID、少选路径、未交付前序规避范围 | retain | Clarify 归属段指向原内容合同；Author 保留 fixed B..HEAD 与真实前序依赖 | 无偏离 |
| R3：Clarify 判断、阶段执行、Author 写作、Creation 建后继，原 Review 核验 | retain | §4/§5；不新增拆片审核或公共字段 | 无偏离 |
| 实施边界与最小验收：原 owner 同步投影，三场景和实际差额检查 | retain | §7/§8 和 implement；不扩张 #734、#765 或 Release 矩阵 | 无偏离 |

## 4. 模块、职责与设计取舍

Clarify 的输入仍是当前源、整体 accepted scope、受影响 Delivery 规划和真实候选。它先比较新增差额，再说明当前缺口、依赖、来源的交付时序约束和独立交付条件。判断留在原 Markdown semantic owner 内，结果通过原 source_selection/revision_refs、scope_action 和实际规划承接，不增加分配字段或账本。

Author 消费已发布整体 authority 和原 Clarify 的判断。需要同片修复时，当前阶段按原 rework 交 Author 刷新受影响正文。独立新增能力后置时，Author 保持当前片实际实现/验收，更新必要来源、边界、依赖、剩余责任和唯一 Policy；原阶段仍判断当前候选有效性并刷新受影响门禁。旧片失效时走原撤回/重新规划。

替代方案是默认全纳当前片或每次强制拆片：前者仍混淆整体接受与切片分配，后者违背不可分修复、共同交付和立即替换要求。直接补原 owner 的判断和承接即可满足正常路径；新增算法、状态、gate 或持久化没有直接 consumer，因此不采用。既有 full/partial/staged 和合法阶段操作保持；没有新协调、等待或兼容路径。

## 5. 接口与数据

没有 API、schema、DTO、CLI 或存储字段变化。原 profile/输入 → 原 Clarify 读来源与整体/切片 → 原 scope_ready/Author/acceptance → 原阶段按实际义务返工、撤回或后继接续。Creation 仍是后继创建 owner，Approval/Delivery Review 仍审独立交付，Completion 仍审整体剩余责任。

当前 slice `scope_ref`、PRD 与 implement Policy 承载实际边界。workflow 只消费既有出口；不要求 consumer 理解新的 private artifact。本文描述现有接口如何承接新增方法，不定义第二份字段合同。

## 6. 状态、顺序、正常与失败流程

不新增状态。新增输入出现后先暂停受影响推进并读完整来源；Clarify 比较原合同和新增差额；整体范围仍经原两段 Author/acceptance 发布；当前阶段再处理受影响片。

S1：能力独立、来源允许后置且旧片仍合法独立交付时，新增能力保留整体剩余责任。Author 更新当前片必要正文和 Policy；当前实现/验收不自动加入新增能力。下一片实施时由 Creation 建立，不并行创建 current。

S2：原合同缺陷、遗漏或不可分依赖仍同片修复；受影响规划和原审核随真实差额刷新。S3：立即替换旧行为或旧片已失效时，原阶段返工或合法撤回/重新规划，旧合同不能继续放行。

有真实范围/时序选择时按原 Interaction Budget 询问；明确当批共同交付和已有具体委托按其实际范围承接。来源缺失/冲突或归属未定时回原 Clarify，不自行默认拆片或全纳。内容已混合时先判断实际可分离性，再沿原固定范围和真实前序事实处理，不降低 Review 覆盖。

## 7. 恢复、兼容、迁移与集成

源文件直接演进，没有公共 API 破坏或业务数据迁移，不新增旧读/双写兼容。既有 Task/Delivery 返工和输出恢复继续由原 producer 负责。本片不恢复历史事故，也不把源码修改当作业务安装已采用。

canonical 修改后的 dogfood 同步由完整源的原 `guru-upgrade-tools` 处理，目标仅此 checkout，保留实际 Claude/Codex/Cursor 选择、当前 Task/session、其它 Task、peer checkout 和 common runtime。先按其 preview/prepare 核完整源、匹配 CLI/Core、既有未完事务和精确写集；实际安装按该 owner 的独立写边界执行。采用 local_candidate 时明确 formal_fork_source_lock 未验证，不能称正式升级或 Release 通过。禁止手工覆盖受管文件或用普通 apply 的历史 Task 阻塞发起无关迁移。

处理实际 `.new/.bak` 时保留原 owner 和原 preimage；遇到冲突停在同步 owner，不制造通过。无已发布前序或部署动作，因此没有跨 Delivery 数据集成或部署回滚协议。

## 8. 验证设计

| 验证 | 要求/AC | 层次、输入与预期观察 | 限制 |
| --- | --- | --- | --- |
| V1 三场景与 owner 对照 | R1–R3 / AC1–AC2 | 原 Check/独立 Review 直接读修订合同，以 S1、S2、S3 追踪到现有阶段/Author/Creation 路线；核真实选择条件、Policy 与固定内容覆盖 | 合同语义审核，不是 Agent 运行评测 |
| V2 两包现有 contract tests 与 source package validator | AC2–AC3 | 执行现有公共入口/consumer/schema 覆盖和 source inventory 校验，预期原 public I/O 及声明投影保持有效 | 不通过关键词新增自证测试，不证明 Agent 行为 |
| V3 原 owner 同步、installed/平台与 drift | AC3 | 在本 checkout 通过 tools owner 同步，验证 installed validator、实际声明投影、dogfood drift、差额 sidecar 与 Task/session 保持 | 不等于多平台实际运行、业务采用或 Release 矩阵 |
| V4 Task/context 与 diff | AC2–AC3 | 官方 context validate、命中清单与 git diff --check；预期必要上下文存在，变更仅属于本 Task | 不替代语义门禁 |

先修订合同，再 V1/V2，再原 owner 同步及 V3/V4。现有 scope/Policy/consumer 组件覆盖仍适用；本片没有 runtime 分支变化，不新增混合 Git 集成、Agent 回放或重复常量断言。已选证据足够且无失败/新增差额时停止追加实验。失败只补对应缺口；不能将设施失败写成合同验收通过。

## 9. Canonical 引用、本轮差额与实际未决项

本片 PRD 第7节定位 RDT 和 Architecture。当前完整生命周期单元已区分整体责任、切片、Policy、合法返工及固定内容范围，需求决策单元已定义真实选择交互；本轮方法细化由原 step-local 合同单写，不向共享 current 复制同一规则。Docs Plan 在 implement 第6节拥有最终策略，原 RDT owner 后续仍须核实际知识影响。

候选 Architecture 为 no_architecture_impact，不生成空 contribution/ADR。没有未决产品选择。尚未执行的同步、package、三场景实现审核和独立最终门禁均保留为待办；其结果不由本设计预填。
