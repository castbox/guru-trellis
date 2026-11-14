# Gen1：bootstrap 验证误报实施与验证计划

## 1. 输入与引用

读取[本批 PRD](prd.md)、[design](design.md)及其第 3 节唯一来源设计处置、[根 PRD](../../prd.md) R-01/03/04/05/06 和原 D1/D2/Finish 实际事实。Task 为 `808-release-v070-guru9` / gen1，Delivery 为 `107413ac-2b33-408e-a97f-e46e63ac420c`，固定 B 为 `50b9ffbefca36454363eb7ae1128ed5974cf7ba4`，PR 目标为 main；该 B 已由原只读 constructor 实际确认。

原失败 C 的 existing 输出、原 inventory、实际文件身份与 tools 成功结果在当前会话保持，不能编辑或重标。本批从源代码和同对象证据确定比较表示误报，修复与验证仍待实施。原独立 candidate_assessment 已实际 no-impact；Wording、final_plan、Approval/Activation 仍是实施前置。

必要规范为[私有发布合同](../../../../../.agents/skills/release-guru-trellis-version/references/contract.md) Two-Stage Lifecycle 及后置责任、[MIGRATION-794](../../../../../trellis/presets/guru-team/MIGRATION-794.md)、[quality-guidelines](../../../../../.trellis/spec/workflow/quality-guidelines.md) Test And Validation Value/Validation Scope Ownership、[减法规则](../../../../../.trellis/spec/workflow/subtraction-first-compatibility.md)和[因果语义](../../../../../.trellis/spec/workflow/causal-completion-semantics.md)。源码/回归/Task 写入前由原 checkout boundary checker 核同 key 和唯一 checkout。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | 前置/owner、实际动作和文件 | 完成观察 |
| --- | --- | --- |
| I1 | 原实施 owner 在完整规划批准和 Activation 后重读 verifier 两比较、局部 `raw()` 全部真实调用及原 producer；保同 B/Task/key | 当前因果与接口仍成立；真实新事实回最早 owner，不从旧 pass 推断 |
| I2 | 原实施 owner 只改 `trellis/presets/guru-team/scripts/python/verify_trellis_compatibility_matrix.py` 两处 post-check，将 actual snapshot 按原身份语义对齐；保原 `raw()` 及其他 source 消费 | native/legacy 同机制均修，真实差异拒绝和其他完整内容保持；无 producer/API/schema、锁、版本或工具机制改动 |
| I3 | 原实施 owner 新建 `trellis/presets/guru-team/scripts/python/test_verify_trellis_bootstrap_preservation.py`，按 design V1/V2 编写并执行原函数入口回归 | 合法保留、两种真实差异拒绝、legacy source 内容承接实际被观察；不替换原比较或自证字典 |
| I4 | 原工程核 V3/V4；原 RDT/Architecture owners 核真实 after 和唯一 Docs Plan，必要差额在提交前合法整合/readback | 未变映射/锁/managed 输入可采用原证据；真实 no-change 不造空贡献或状态文档 |
| I5 | 原 TaskCommit 提交全部本批 after，原 constructor/begin_check 保 B 并含新测试实际 paths，新独立 reviewer 审完整候选 | Architecture/九维/full Review 和真实 check/full_review 两槽均成立后才 readiness/Publication/expected-head Merge |
| I6 | 原 Completion 核本代全部范围；Closure no_mutation、Finish/Cleanup 后，原发布 owner fresh main 再冻结 | 不把本切片合并当 Task/Issue/Release 完成；旧失败 C 保留，新候选独立验收 |

本批不写源码以外的通用机制，不修改失败 C、旧样本、gen0 规划/结果或无关资源。代码文件当前 2912 行，应保持局部修改；不能为小修复扩成未批准重构。新增回归文件由实施 owner 在实际存在后通过官方 add-context 纳入实现/审核上下文。

## 3. 验证入口、输入与预期观察

### V1/V2：原函数入口行为回归

在当前 Task checkout 使用现有 Python unittest 风格，不安装新的测试框架。预计入口为：

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s trellis/presets/guru-team/scripts/python \
  -p 'test_verify_trellis_bootstrap_preservation.py'
git diff --check
```

测试设置原函数需要的 source/provider、单 workspace、无 session、唯一 bootstrap 和适用 schema。调用真实 `_upgrade_bootstrap_fixture`；维护动作可在组件边界外用合法替身隔离，但保留原 plan 组装与 post-check。分别观察 native 与 legacy 合法未变 artifacts 成功，其他 file source 的原内容仍完整，以及普通字节变化和 mode 变化的原错误。

用已知 fixture 原始字节作为独立期望，并解码原函数实际输出的 source 内容；不能复制 `raw()` 或比较实现来生成“预期”。不得 patch 原比较、补回丢失输出、删 artifact 或只断言 mock 自身。原 native/legacy 版本参数和公共 owner 行为不因测试方便改变。

新回归文件本身须有独立行为价值。若 I2 影响到另外一个已有消费者，按真实依赖补其定向验证；未受影响的 stream/platform 等 suite 不因同一模块路径而惯例重跑。当前回归只能证明所声明组件边界，不能宣称真实 Plan2/tools 执行或 Release existing 已通过。

### V3：完整映射及实际采用适用性

使用原 installer 的 `managed_source_projections`，读取实际 changed source paths，检查 verifier 和新回归文件在映射 source/target 中均无项；同时核 source lock、canonical managed assets、installed/provenance 没有本批新差额。不复制映射或 digest 算法，不新增长期 helper/证明文件。

原 gen0 的实际 source_locked 采用及原样本信息保持其截止点。当前新 checkout 的自身 resolver/installed/native 已实际验证，但源修复后仍按实际输入/依赖/工具/参数/定义/期望判其适用性。仅 helper/test 不进入映射时，没有新增 tools 安装动作；若新增受管资产或依赖差额，原 tools owner 重新审精确范围，不能用本说明越过它。

### V4/V5：完整质量、文档和交付

核实际 diff、测试入口/断言、两处比较及未改 `raw()` 消费者，检查 `git diff --check`、必要局部语法/导入和无 Python residue。回归实际导入源文件已覆盖其语法时，不再加同义静态命令。文档改动则检查 changed links/anchors 和完整语义；源码小修复没有自动全矩阵责任。

原 RDT/Architecture owners 对真实 after 判断 no-change 或必要文档整合；独立 committed Review 再判断。所有真实 after 进入自身 TaskCommit 和固定完整 B..H；原 reviewed-content token 与 Git/public Candidate 各用其原 owner，不手填身份。当前 PRD/方案或命令存在不证明实施成功。

当前因果依据已由原失败和直接代码/身份观察建立，不固定要求再次改跑旧冻结 C、回退或重复红绿。必需的 V1/V2 验收仍实际执行；若分支是否命中、断言是否检测该缺陷仍不明，先核入口与观察，再补能回答该问题的最小诊断。具体证据充分后停止追加实验。

Stage 2 的 focused/existing、真实前驱升级、ordinary self-reapply、source/installed/parity/ownership/drift、scanner、tag/smoke/Release 及最终本地目标仍按原合同对新 fresh candidate 执行，不在本批预记通过。

## 4. 停止条件与适用回退点

| 实际条件 | 原停点与处理 |
| --- | --- |
| scope、Issue、源或六项版本输入真实变化 | 原 Clarify/Planning 核 authority，不私改根 PRD 或另选版本 |
| producer/consumer 或 raw 真实用途与本设计不同 | 原 Author/Architecture 刷新受影响机制；保原消费者，不扩大修复 |
| 新测试未命中比较、fixture 绕过前置或只测替身 | 原实施补足真实入口/观察；不将绿色当验收，不放松断言 |
| 合法保留仍失败，或真实 bytes/mode 变化未拒绝 | 原实施修复当前机制并补受影响回归；未解决不进入 Review pass |
| 发现新 managed source、锁、安装或 owner 差额 | 回原 tools/Architecture/Planning；不自动安装、不手改 manifest |
| 必要环境缺失或基础设施重复失败 | 原工程重评最小复现方法，保具体缺口；无法证明的依赖验收不记 pass，不扩无关基础设施修复 |
| Commit/Review/Publication/Merge 输出丢失或 stale | 原 producer 核同操作和真实结果恢复，内容修复需后继提交/覆盖；不造空提交、旧 pass 或第二 PR |

无业务数据、生产部署或工具状态改变，不新增 rollback 协议。未授权并行改动和旧资源保持；本批各 Git/GitHub 副作用由原 owner 展示精确边界执行，授权只在当前对话。

## 5. Delivery Policy（唯一）

选择 **full**，覆盖本 generation 当前选择的完整 verifier 修复切片。进入条件为真实 gen1 Reactivate/Creation、当前完整规划、Wording、final_plan、Approval 与 Activation。当前 scope_ref 为根 AC-01/03/04/05/06 的本批适用责任；没有延期给下一 Delivery 的本次比较修复、必要 consumer 适配或行为回归。

退出条件是两个比较消费者均正确承接原身份，真实字节/mode 差异仍拒绝，raw 其他内容消费者保持，V1～V4 及必要知识判断完成；全部 after 经原完整提交/独立质量/readiness/Publication/Merge 实际 delivered。原 gen0 实际交付与终态只作为历史和依赖事实，不充当本次 pass。

本代完整准备仍由原 Completion 判断，随后 Closure no_mutation、acceptance-finish Architecture、Finish/Cleanup。Stage 2 是本 Task 之后的独立发布阶段：新 fresh main 冻结，原失败 C 不变，完整新候选门禁、tag/smoke/Release、两个最终本地目标和 #808 关闭仍归原发布 owner。它们不是本切片组件回归的循环前置，也没有被本次交付完成。

当前没有真实临时运行限制被解除后需要新增状态账本；消除的是 verifier 误报。原失败观察与本次修复后观察分别保留原身份和截止点，不将局部改进扩大为整体发布通过。

## 6. Docs SSOT Plan（唯一）

选择 **no_docs_update_needed**。依据是修正原 `sha256/mode` 判据的消费实现，既有 requirements/design/test/Architecture 和私有发布合同均继续要求原行为；没有规范性字段、接口、发布边界或版本变化。实施 after 仍由各原 maintenance owners 复核，不能用本计划预填其结论。

| 目标与原 writer | 当前判断、直接 consumer 与验证 |
| --- | --- |
| verifier 及新行为回归；原实施 owner | 真实代码差额与可执行回归承接既有要求；直接 consumer 为 existing 验证调用方和工程/Review。必要代码注释在自身源码维护，不另写状态文档 |
| [R649/R794](../../../../../docs/requirements/current/task-delivery-lifecycle.md)、[D649/D794](../../../../../docs/design/current/task-delivery-lifecycle.md)、[T794](../../../../../docs/test/current/task-delivery-lifecycle.md) 完整当前单元；原 RDT owner | 已承接结果层次、原质量链及 source/installed 分层；本批无新通用文义，真实 no-change 不造空贡献。实施后发现真实差额才由原 owner 准备完整目标、提交前整合/readback |
| [Architecture](../../../../../docs/architecture/README.md) 的 ARCH-DOM-010、ARCH-INT-015 与[change contract](../../../../../docs/architecture/06-governance/change-contract.md)；原 Architecture owner | candidate assessment 已 no-impact，原 owner/来源/采用/终态/发布关系不变；实施后仍核实，最终独立 committed 判断不由当前计划代替 |
| 三 README、私有发布合同、migration、manifest/source lock | 没有当前指令被本修复废止，不需要新增版本说明或通过登记；消费者仍使用原入口。保历史失败与 evidence cutoff |
| 本批三正文及官方 context；原 Author | 完整承接来源、方案、验证、Policy/Docs Plan。后续源码/测试路径实际出现后通过原 task.py add-context 补必要项，不改旧 Delivery 规划或根 scope |

不创建 release-notes、PR/Release body handoff、动态执行 checklist、发布 ledger、空 ADR/contribution 或共享 root/index 登记。若实施引入真正规范性变化，先回原 owners 修订本 Docs Plan并履行原完整整合及审核，而非静默沿用 no-change。
