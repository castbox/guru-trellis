# #779 D1 委托结果承接与介入方法实施与验证计划

## 1. 输入与引用

本批 DeliveryId 为 `e769c486-5b4d-47ff-a940-047a23793543`，TaskId 为 `779-delegation-results-intervention`，generation 为 `0`。本批读取 [整体 PRD](../../prd.md)、[Delivery PRD](prd.md) 全部要求、[design](design.md) 第3节唯一来源设计处置及第4至8节的实际方案。固定 B/H0 为 `221f74caef372414a1c7d700575742eb1e075af4`，PR 目标 main，无前序 Delivery。

实施者实际加载 canonical workflow-contract 的完整 Phase 2、Candidate Applicability And Coverage，global workflow 2.1/2.2 的 discovery 与正式 Check 路由，以及 `.trellis/spec/workflow/quality-guidelines.md` 的验证方法/范围。Author 的 planning-body 与三份 Delivery templates 是规划理解依据，由官方 add-context 为当前 Delivery 选择实际 file/reason，不修改上游 agent 或 hook。

独立候选 Architecture 已实际返回 no_architecture_impact。原 tools owner 使用完整 canonical `trellis/skills/guru-team/packages/guru-upgrade-tools/` 合同；RDT owner 使用 current-knowledge 和当前三层生命周期完整单元。实际规划仍须 Wording、Architecture final_plan、Approval 和当前计划接受后才激活实施。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | 依赖、owner 与文件 | 行为、可审产物与完成观察 |
| --- | --- | --- |
| I779-01 | Planning 激活后；原实施 coordinator 和配置 implement worker；canonical workflow-contract Phase 2 | 每写批前核 live checkout boundary。按 design 第6节补委托后方法；保留原 worker scope/discovery 与 Check/Review；当前 diff 可逐项对照六项要求 |
| I779-02 | I779-01；同实施 owner；canonical global workflow 2.1 | 只补加载方法正文的必要引用，不复制方法。检查 preset/workflow README 与平台入口的实际关系，仅真实变化才编辑，不为凑投影制造改动 |
| I779-03 | 正文候选可读；原 RDT owner；`docs/requirements-design-test-contributions/779-delegation-results-intervention/` | 读命中完整单元和必要关系，核行为/职责/验证差额，准备三层完整 proposed definitions 与真实 traceability；不写共享 current，不造空 Architecture contribution |
| I779-04 | I779-01/02 与实际 tools 前置；原 guru-upgrade-tools | source-owned preview→精确 public/Guru/pointer 写集审查→prepare 一次→实际写入边界→invoke。保留 Task/session/历史/peer；按原 owner 验目标 native、mode、sidecar 和受管 projection，不手工覆盖 |
| I779-05 | 完整实现、隔离 Docs 候选及命中验证；实施 coordinator→独立 Architecture phase2→原 Check | 用原 construct-delivery-candidate 以固定 B、实际 HEAD 和完整路径构造 Candidate，原 begin-check；独立 Architecture 审完整候选与 before，原 delivery_candidate_check 完整审查，真实出口才进入整合 |
| I779-06 | candidate_checked 的合法回 implementing；原 RDT/Architecture final_integration | 原 owner 固定实际目标，整合命中完整定义并读回；no-change 不造空文件。实施重绑全部 after 路径，再最终 Architecture/Check→精确 TaskCommit→独立 committed Review→Delivery readiness/Publication |

本批不拆后继能力，也没有真实临时功能限制。所有未完成实施和证据仍归本 Delivery；Task 整体完成由原 Completion 单独判断。PR 发布后停止，合并等待协调器具体处置。

## 3. 验证入口、输入与预期观察

验证 ID 与设计第8节一致，以下均为待执行安排。

- **V779-01**：原 Check 和独立 Review 用当前完整 diff、三份规划、#779 和实际 consumers，逐项核六项要求、四个场景、完整条件与例外，检查自主执行、介入、运行事实层次、原句柄接管、自然边界交接及正式职责。预期无越界、无逐轮审批或隐含完成条件。
- **V779-02**：沿 source-owned `guru-upgrade-tools/scripts/{preview,prepare,invoke}.sh` 读取实际 public profile 和真实 installed CLI/Core roots，选匹配 source HEAD 与依赖模式；由原 owner 完成实际目标 postvalidation/native/preservation。精确 argv/写集在 prepare 后展示，不预填未知来源。若使用 local_candidate，报告 formal_fork_source_lock 未验证；不把局部安装当作正式发布证明。
- **V779-03**：同步后运行 `bash trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh --repo .`。它实际检查 ownership、所选平台、workflow 与 managed spec parity；另按原安装 owner 的结果核 mode、`.new/.bak` 及 peer/Task/session 保留。预期实际命中投影无漂移、无未解决 sidecar。
- **V779-04**：原 RDT owner 审查隔离完整 proposed definitions 和 traceability，候选 Check 后才 promotion/readback；重新构造实际 after 候选并完成最终质量链。最终运行 `git diff --check`，预期无空白错误，三层关系可解析，方法正文只有一个执行来源。

没有确定性运行逻辑变化，不添加冻结文字的测试。采用仍适用的原工程事实，缺失或变化只补命中验证。顺序为正文→原 owner 同步/知识候选→命中机械检查→候选完整审查→真实整合/重绑→最终审查；语义问题先修正文，再补受影响检查，不无条件重复整套实验。

证据不覆盖设备、整场事故重放、消息计数、全平台实际 Agent、完整 clean/existing/update/reapply/Release 矩阵、业务安装或成本节省。源码 parity 和 schema 成功不代替这些层次。

## 4. 停止条件与适用回退点

checkout identity/binding/注册关系失配时，写前停止并回原 Identity/Ensure owner，不重建映射或换目录规避。新范围/机制/风险候选只返回原 discovery 形状并资格化；真实范围变化回 Clarify，机制变化刷新 Architecture，不由 worker 自动实现或测试。

tools 缺 matching API/source、重叠未完成事务、未知 managed edits 或未解决 sidecar 时，停在原 tools owner；只沿其同操作 resume/rollback，不重复 prepare、不迁移无关旧 Task。任何恢复均保留后续业务工作和并行资源。无数据/部署迁移，故不新增回滚协议；本地内容修订限本次明确文件，不 revert 用户并行改动。

语义或 drift 检查失败时，只修具体缺口并刷新受影响证据。设施反复失败由原 owner 重评复现方式，必要缺口如实保留，不能预填 AC 通过。证据足够后，停止本计划以外且没有具体证据缺口的验证，不追加设备或完整矩阵。commit、tools 实际写入及 push/PR 仍按各原 owner 的具体边界处理；不合并 PR。

## 5. Delivery Policy（唯一）

选择 **full**：本批覆盖当前 scope_ref 的 R779-01..06，不留下后继实现或本项必需补证切片。完成条件是合同完整、原职责一致、实际受管同步/drift 和必要知识整合完成，且真实完整候选经过最终 Check、独立 committed Review、readiness 和正式发布。full 是选定范围责任，不是当前验收已通过。

整体 Task Completion 仍需原 owner 审查全部 accepted scope、Delivery 结果和必要证据。PR 发布不是合并，也不是 Task 完成。本次执行在目标 main 的 PR 发布后停下，不执行 merge、Issue closure、Finish 或 Cleanup。

## 6. Docs SSOT Plan（唯一）

选择 **delta_first**。原 writer 为 `guru-maintain-requirements-design-test-ssot`；直接 consumer 为候选 Check、原 final_integration、最终 Check/Review，以及后续生命周期知识读取者。Planning 仅描述策略，不提前写共享 authority。

命中 `docs/{requirements,design,test}/current/task-delivery-lifecycle.md` 的三个完整单元：需求层补委托后结果承接的能力与边界，设计层补 canonical Phase 2/coordinator/worker/原 tools owner 的职责关系，测试层补最小语义与受管同步预期及未验证层次。精确方法继续由 canonical workflow-contract 单写。原 RDT owner 在 Phase 2 核实际必要差额，保持现有 identity、条件和历史，仅在 task-owned contribution 准备完整 resulting definitions。无需 root/current 导航、全局版本或无关条目更新。

候选 Check 前准备完整 proposed definitions；candidate_checked 后原 owner 在同 Delivery final_integration 读取真实 target、整合并读回。随后实施重绑实际 after，最终 Check/commit/独立完整 Review 覆盖全部知识写入。贡献保留来源与窄替代边界，不作为第二 current。Architecture 当前无影响，不新增空 contribution/ADR；若后续独立评估有真实差额，回原 owner 处理并刷新相关规划。
