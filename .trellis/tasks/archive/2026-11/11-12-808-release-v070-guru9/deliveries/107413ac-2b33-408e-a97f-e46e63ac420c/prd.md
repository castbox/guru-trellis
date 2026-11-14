# Gen1：修复 existing 验证器的 bootstrap 保留误报

## 1. 整体来源与术语

本批属于 Task `808-release-v070-guru9` / generation `1`，Delivery `107413ac-2b33-408e-a97f-e46e63ac420c`，profile 为 `pull_request`。整体权威仍为[根 PRD](../../prd.md)，accepted revision 为 `sha256:835586c0c5ca6a22a50a872ce8249a2548dfac4d6f84a4321f78f4d06addb950`。本批选择 AC-01、AC-03、AC-04、AC-05、AC-06，承接来源完整性、验证正确性及本批质量交付责任；不修改整体范围。

| 来源与章节 | 角色与本批用途 |
| --- | --- |
| [#808](https://github.com/castbox/guru-trellis/issues/808)：背景与目标、前置与准备范围 | 要求：保持 `.9` / CLI-Core `.6` 六项输入，由原准备 owner 修复来源缺陷 |
| 同一 Issue：冻结候选与验收、正式发布与本地收尾、完成条件与范围边界 | 要求：真实 `.8` existing 验收；失败回原 owner，内容变化后重新冻结；后置发布和本地收敛仍独立承担 |
| [根 PRD](../../prd.md)：R-01、R-03、R-04、R-05、R-06 与第 7 节 | 已接受要求：完整来源和真实验证、原切片质量链及 Refs-only 交付；旧通过不代替新候选 |
| [私有发布合同](../../../../../.agents/skills/release-guru-trellis-version/references/contract.md)：Two-Stage Lifecycle、Local Installation Convergence And Final Report、Independent Mutation Confirmations | 设计约束：原准备与终态 owners；fresh main 候选及 existing 入口；独立副作用与原始失败保留 |
| [MIGRATION-794](../../../../../trellis/presets/guru-team/MIGRATION-794.md)：新正常链、第 1/2/4/5 节 | 设计约束：提交前必要整合、提交后新独立完整 Review、真实 check/full_review 两槽及 matching 原 owner 恢复 |
| [verifier](../../../../../trellis/presets/guru-team/scripts/python/verify_trellis_compatibility_matrix.py)：`_upgrade_bootstrap_fixture` | 实现事实与修复对象：native/legacy 两条成功后的 artifacts 比较，以及 `raw()` 的其他调用 |
| [inventory producer](../../../../../trellis/skills/guru-team/packages/guru-upgrade-installation/runtime/delivery_upgrade.py)：`raw_snapshot`、`prepare_inventory` | 既有接口事实：artifacts 使用 `include_content=False`，提供 `sha256/mode`；其他 source snapshot 仍可携带内容 |

“保留身份”指原 inventory 比较文件原字节和权限所用的 `sha256`、`mode`。`content_base64` 是其他原消费路径需要的内容载体，不能因修复比较而全局移除。

规范性来源设计的唯一处置见 [design 第 3 节](design.md)，本 PRD 不另建处置矩阵。

## 2. 整体与本批目标、非目标

原 Stage 2 在冻结候选 `50b9ffbefca36454363eb7ae1128ed5974cf7ba4` 上执行真实 `.8` existing/codex 验收。原 tools 已返回 `tools_upgraded`、`unverified=[]`，verifier 随后报 `bootstrap fixture bytes or modes changed during tools maintenance`，使该候选停止。

现行 `raw()` 返回 `sha256/mode/content_base64`，两个比较点却将整个字典与仅有 `sha256/mode` 的原 artifacts 比较。原样本 bootstrap `prd.md` 的实际摘要和 mode 与 inventory 严格相等。当前证据支持 verifier 表示形状误报，不能重述为工具已损坏 Task。

本批目标是让原保留检查按原身份含义正确判断，覆盖同机制的 native 和 legacy 消费者，并以必要行为回归证明合法保留可通过、真实字节或 mode 变化仍拒绝。全部源码和测试 after 进入本批自己的完整质量交付链。

本批不改工具生产机制、公共 API/schema、Task 迁移或 source lock，不提升 Guru、CLI/Core 或前驱版本，不增加 wrapper、状态、fallback、ledger 或通用加固。不编辑失败候选、原样本或旧观察，不把失败改标通过，不实施其他 Issue、业务升级或生产部署。

## 3. 本批起点、前序结果、依赖与剩余责任

gen0 D1 已通过 PR839 交付完整 `.9` 来源，merge `647df4de6c4443720b4bacb674dbe3909333bf4d`；D2 已通过 PR840 交付实际 source_locked 采用，merge `997a57bec3e3f67c227cff3edc81efa0014da0fb`。gen0 Completion、reference-only Closure 和 Finish 均已实际完成；归档 bookkeeping PR841 merge 为 `50b9ffbefca36454363eb7ae1128ed5974cf7ba4`。这些历史结果保持原范围和截止点。

本批是候选验收失败后的同身份正常 Reactivate，不是补造 gen0 结果。当前 generation 为 1，根 scope 未变，起点 HEAD 为上述 PR841 merge。原 Reactivate 创建的新执行 checkout 及本机路径只由当前对话和原 owner 参数解析，不写持久 workspace 映射。

已实际核原完整 `managed_source_projections`：verifier 既不是任何映射 source，也不是映射 target。只修改本 helper 和必要回归时不产生新的受管字节；既有实际 tools 采用事实按输入、依赖和期望判适用性，不为 helper 修复重复安装。后续若真实改变 managed source、锁或工具机制，回原 owners 重判。

本批 delivered 后，原 Completion 重新审本代全部准备责任，再由原 Closure/Finish/Cleanup 收口。Stage 2 从新的 fresh main 重新冻结并完成原全部门禁及发布；原失败候选 gate 不改为新 candidate pass。其他 native host、累计完整矩阵和真实业务升级不是本批交付承诺。

## 4. 本批调用方、场景与流程

| 场景 | 调用方、前置与动作 | 可观察结果 |
| --- | --- | --- |
| G1-SC-01 native 保留 | existing verifier 从原 preview 取得合法 Task2 bootstrap inventory；原 tools 成功且文件未变；执行原保留检查 | 附带 `content_base64` 不使身份相同的文件失败；原 tools 结果与实际文件身份分别保留 |
| G1-SC-02 legacy 保留 | 原 legacy 分支完成既有 Plan2/upgrade 后执行同机制检查 | 原身份相同按原语义通过；其他 source snapshot 的内容载体仍供原消费路径使用 |
| G1-SC-03 真实未保留 | 受支持执行出现普通错误，导致原 artifacts 文件字节或 mode 不同 | 原 verifier 仍在原阶段拒绝；不得删项、忽略差异或改成成功 |
| G1-SC-04 修复验证 | 工程及审核 owner 使用合法 fixtures，通过原函数入口验证两个消费者 | 回归实际执行比较与相关 assembly；不以文本或自身字典断言自证，不把替身当完整外部安装 |
| G1-SC-05 正常交付 | 完整工程、必要知识整合及 TaskCommit 后，新 reviewer 审全范围，再 readiness/Publication/Merge | 中文 Refs-only 交付；本代收口后 Stage 2 再冻结。旧失败和旧终态保持历史原义 |

## 5. 完整行为、条件与约束

**G1-R-01 身份等义比较（AC-01/04；SC-01/02）**：原 artifacts 的身份字段与含义不变。比较只判断原身份是否保持，不能因另一表示为其他消费者附带内容而误拒。native 和 legacy 两个同机制比较点都须承接，不能只修首先命中的 native 分支。

**G1-R-02 真实差异仍拒绝（AC-04/05；SC-03/04）**：字节或 mode 不同仍按原检查失败。不得删除全部比较、固定成功、缩减原 artifacts、改写 preimage 或原失败样本来获得通过。只处理诚实正常路径和普通实现错误，不新增攻击、并发或 fault 场景。

**G1-R-03 保其他消费者（AC-01/04/05；SC-02/04）**：`raw()` 其他 legacy CorePlan2 文件 source 等调用仍需实际完整内容。修复不得全局删除 `content_base64`，不得改 inventory producer 的公共形状来迎合一个消费者。具体最小落点由独立 candidate assessment 后的原方案 owner 确定。

**G1-R-04 有效回归与证据（AC-04/05；SC-04）**：按 Test And Validation Value 执行足够层级的必要回归，观察原函数分支、输入、组装及结果。覆盖 native 合法保留、legacy 同机制保留与内容 source 承接，以及真实字节变化、真实 mode 变化这两类不同拒绝行为。每个用例须有独立缺陷发现价值，不新增镜像实现、常量自证或累计矩阵。保原失败、inventory、文件及 tools 输出；修复未实施前不预称根因已修复。

**G1-R-05 当前说明与采用边界（AC-03/04）**：原 Docs Plan 判断是否有真实规范性文义变化；预期是原判据的正确实现，不为证明通过写状态文档、空贡献或共享索引。真实规范/接口变化回原 owner。受管映射未变时复用仍适用的实际采用事实，真实失效项按输入和消费者补验证。

**G1-R-06 完整质量与后置责任（AC-05/06；SC-05）**：新代码及回归 after 经原工程和必要知识 owners、TaskCommit、完整 committed candidate、新独立 Architecture/九维/full Review、readiness、Publication 与 expected-head Merge。当前 Author 不写实现，也不作为新候选独立 reviewer；旧 gen0 gate 不能代替当前通过。PR 使用 `Refs #808`，不关闭 Issue。本代 Completion、Closure no_mutation、Finish 和 Stage 2 分别执行。

## 6. 本批验收、验证方式与未决项

| 验收 | 要求/场景、入口与输入 | 预期观察及边界 |
| --- | --- | --- |
| G1-AC-01 / 根 AC-01/04 | G1-R-01/03、G1-SC-01/02：原 inventory producer、原函数两消费者与合法 bootstrap fixtures | 同身份不因表示形状误拒；legacy 其他 source 仍有必要内容；版本和原接口不变 |
| G1-AC-02 / 根 AC-04/05 | G1-R-02/04、G1-SC-03/04：原函数路径中的普通字节变化与 mode 变化 | 两类真实不保留分别被检测，原失败阶段/语义保持，无断言放松或样本排除 |
| G1-AC-03 / 根 AC-03/04 | G1-R-05：真实改动、原 Docs Plan、完整 managed 映射及适用证据 | 明确必要文档/no-change及原 writer；不把 source helper 修复混为新 tools 采用，不制造无消费者资产 |
| G1-AC-04 / 根 AC-05/06 | G1-R-06、G1-SC-05：全部 after、原提交和完整独立质量/交付链 | 当前切片零开放 P0-P3 后才 readiness/远端交付，保原 scope、Refs-only及各副作用边界 |

根 R-06 的 fresh candidate existing/focused、scanner、dogfood、tag/smoke/Release、两个最终本地目标和 Issue 关闭仍由 Stage 2 承担。它们不由本批组件回归预记通过，也不被本次 source 修复免除。根 AC-07/08 由本代整体完成与终态 owners 按实际时序承担。

当前没有需求或范围选择待用户决定。独立 candidate_assessment 后形成的方案和具体工程安排见 [design](design.md) 与 [implement](implement.md)；实现和验证尚未执行。缺环境或真实新事实回原 owner，不预填通过。

## 7. Canonical 引用与本轮差额

- [RDT requirement](../../../../../docs/requirements/current/task-delivery-lifecycle.md)：R649 结果边界与 R794 完整当前质量/采用；本批修既有 verifier，不新增生命周期承诺。
- [RDT design](../../../../../docs/design/current/task-delivery-lifecycle.md)：D649、D794 原 writer、独立 Review及工程事实承接；原方案阶段判断是否真实有知识差额。
- [RDT tests](../../../../../docs/test/current/task-delivery-lifecycle.md)：T794-06/07 的 reviewer/安装/外部证据分层，以及原质量规范的行为测试方法；组件回归不是 Release existing 通过。
- [Architecture](../../../../../docs/architecture/README.md)：现行五原则/change contract、ARCH-DOM-010/ARCH-INT-015 保持来源、采用、终态和发布职责。新独立 owner 仍须判断本批候选，不预填 no-impact。
- [quality-guidelines](../../../../../.trellis/spec/workflow/quality-guidelines.md)：Test And Validation Value、Validation Scope Ownership；执行必要受影响行为回归，不扩累计矩阵。
- [subtraction-first-compatibility](../../../../../.trellis/spec/workflow/subtraction-first-compatibility.md)：直接演进两个比较消费者，保其他真实 raw source 消费者，不新增 adapter、双读或备用状态。
- [causal-completion-semantics](../../../../../.trellis/spec/workflow/causal-completion-semantics.md)：因果依据、机制资格、实现验证和后置外部验收分别判断；原 verifier false negative 不等于工具损坏 Task。

本文件拥有当前需求与候选上下文。design 拥有方案和唯一来源设计处置；implement 拥有执行验证及唯一 Policy/Docs Plan。三正文不改根 scope 或旧 Delivery 规划，完整规划也不代表 Approval、Activation 或实现通过。
