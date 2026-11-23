# 正式步骤跨会话交接设计

## 1. 设计目标、需求承接与内容基线

本批覆盖 AC01–AC03。开发和规划基线 B/H0 均为 `1174ab49c7187ead613eb338ef1bb5ef1eb0e994`，目标为 castbox/guru-trellis:main。独立候选评估返回 `baseline_current`、`target_native`，依据 ADR-035、ADR-EXPLICIT-REVIEW-OBJECT 和 ADR-POSTCOMMIT-INDEPENDENT-REVIEW。

## 2. 当前系统、边界与目标差额

Workflow 已具备 Identity/Ensure/Bind/Selection 顺序和标准只读查询。Planning 路由已经引用续接。提交后独立审核与代理换人、接回的调用点需要清楚执行同一规则。

## 3. 来源设计处置

保留 Issue #912 指定的原 owner 续接、真实冲突返回和显式只读边界。既有 ADR 的接口与角色选择复用。

## 4. 模块、职责与设计取舍

在 canonical workflow 的接收会话续接节集中跨阶段交接要求。Planning、Phase 2 派发及 Phase 3 Branch Review 和接回正向路径引用该节。正式 Branch Review Skill 在首次依赖当前会话的资格判定、证据记录和调用前应明确执行适用接收前置。派发给出执行角色、当前对象、所用正式入口及预期的正式结果类型，并明确是否允许原 owner 写入必要会话状态。预期结果类型不预设评审结论。保留 Architecture authority-first 和新评审者空历史。维持上游代理及 hooks 的职责。

| 出现点 | 实际调用会话、首个前置检查与结果 |
| --- | --- |
| 首次或替换的独立 Architecture 候选评审 | 新评审会话在原 authority-first 顺序中确认自身 Task 与适用 Delivery，调用原 candidate_assessment 并交回其实际 typed exit。 |
| Author、Approval、Activation | 原阶段 owner 在本会话写入或调用前读取匹配 Delivery。仅委派该正式职责时才由子会话完成同样检查。接回的下一调用者重新读自己的会话。 |
| Phase 2 执行或实现发现 | 仅提供实现/检查事实的代理按原工程职责。实际执行 Delivery 资格判定、Architecture 或其他正式 Check 的会话先满足原入口所需绑定/选择。 |
| 提交后 Branch Review 与替换 reviewer | 同一个独立评审会话先核对接收前置，再走已固定 B/H 的 Architecture、资格判定、record/check/invoke，交回实际 Branch Review exit。 |
| Publication、Merge、Completion、Closure、Finish | 原流程默认由当前阶段调用者接回。跨会话时执行新调用者自己的前置，按原入口区别 Delivery、Task-only、显式恢复等适用条件。 |
| final_plan、独立只读、仅工程证据 | 继续各自的显式或只读入口。接收该结果后的正式调用者独立满足自身前置。 |

## 5. 接口与数据

复用公开 `read-continuation-context.sh --root .` 的无目标锁定读取，随后与收到的身份匹配。Task 定位、选择、现行正式输入输出和 schema 原样使用。禁止在未核实选择时把目标 Delivery 作为已匹配断言。

## 6. 状态、顺序、正常与失败流程

实际执行者从本会话读取状态。必要时按原 owner 补 Task 或仅补 Delivery；成功读回后进入原入口。匹配直接继续。不同选择、终态、真实失配与读取错误归原 owner。Task-only 调用止于 Task 前置。显式只读和仅提供工程证据的派发依原 profile 条件执行。移交之后由实际下一调用会话重新判断。

## 7. 恢复、兼容、迁移与集成

同候选继续使用原恢复和正式结果规则。Workflow 与受影响 Skill 通过 matching 发行同步，已有 checkout 保留 Task/session。无需数据迁移。当前无 context 时仍走原显式对象路径。

## 8. 验证设计

V1 在同一 Task/Delivery 派发空历史候选评审者与提交后正式 Branch Reviewer。以实际首次调用前的 current 读回及原 wrapper stdout 验收。V2 运行已有会话续接测试，覆盖仅缺选择、匹配、冲突、Task 和显式对象。V3 盘点实际原入口与调用者、读取点和原 owner，并核 canonical/dogfood/declared platform、相关子代理入口和匹配同步。定向验证，共享路径复用证据。

## 9. Canonical 引用、本轮差额与实际未决项

本 Delivery 的 architecture-contribution.md 给出 ARCH-CONTEXT-001 的计划差额。Architecture 和 RDT 原 owner 完成前提交整合及读回。目标为 docs/architecture/03-domains/workflow-context.md 及 Task/Delivery 生命周期 requirements、design、test 三层。无待决产品问题。
