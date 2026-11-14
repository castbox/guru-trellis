# Issue 内容的设计责任

Identity：`RDT-DES-ISSUE-CONTENT`。导航别名：`D153`、`CON153`、`D153-01..03`、`CON153-01..03`。原语义 owner：`guru-maintain-requirements-design-test-ssot`。本完整拟写承接 [#153 原设计](../../requirements-design-test-contributions/153-issue-content-ssot/design.md)与 #818 D1；状态及整合边界见本贡献 `manifest.yaml`、`traceability.md`。

## 来源、适用性与替代范围

适用基线为 Git `fd0ee32618433a92ae934e29afb5b72e7136b4f7`。需求关系为 `docs/requirements/current/issue-content.md` 的 R153/BEH153 与 R818/BEH818。本单元只承接 `.109` 设计入口所连接的 D153-01..03 / CON153-01..03 Issue 内容设计，不迁移 `.109` 对前驱的其他继承，不改历史 ADR、贡献或原验证结果。新要求的设计差额由下列 D818 身份承接。

原 Architecture 独立 final_plan 为 `baseline_current / no_architecture_impact / no_change`，公开 authority 为 `docs/architecture/README.md / guru-trellis-architecture / active`。本设计沿既有 owner、Markdown 控制面与受管分发，没有新的运行依赖、数据状态或 public I/O；不制造 Architecture contribution 或 ADR。

## D153-01 / CON153-01：唯一内容方法

[canonical Issue 内容正文](../../../trellis/skills/guru-team/packages/guru-clarify-requirements/references/issue-content.md)由原 Clarify package 单写。它复用 Author `planning-body.md` 第2节的来源合同及安装的 `clear-technical-writing.md` 语言合同；三个去敏过程示例只演示方法。内容规范负责写作、整理、裁剪及完整性方法，RDT 定位能力责任与关系，不复制规则或示例为第二定义。

来源和规范不可读时沿原 owner 恢复；不能凭摘要补出正文或通过。方法来源与外仓参考不成为新的运行时读取依赖。对应 R153-01/02/03、R818-01..04；由 T153-01/02/03 和 T818-01/02 观察。

## D153-02 / CON153-02：原入口执行及写入边界

Clarify、Wording、Readiness、Create Issue 的 SKILL 与前三者原合同完整加载同一内容正文，并在各自原门禁内使用。方法只通过必要薄引用承接，完整定义仍在 D153-01 的正文。Wording 的 scanner 范围保持 title/body；必要评论是 AI 读取的来源，不冒称被 scanner 扫描。Readiness 保留原十维，Create Issue 核对已审内容而不变成第二 writer。

草稿更新、已有正文修订、真实创建和只读请求各沿原动作、确认、live reread、刷新及重审路径。内容缺口不自行授权写入。没有新 Skill、审核节点、typed exit、schema 或最小 DTO 差额。对应 R153-02/04/05、R818-01..04；由 T153-02/03 和 T818-01/02 观察。

## D153-03 / CON153-03：受管分发及现有目标采用

既有递归 package/preset writer 分发完整正文、必要示例、四入口及三个合同；受影响 managed spec 沿原机制安装。定向 fixture 实际执行 writer/reapply，核声明平台字节、引用、用户保留和 sidecar。正式 Task checkout 使用完整 matching source 的原 `guru-upgrade-tools`，按其 preview、审查、prepare、invoke 和 readback 更新，保留 Task/session 与用户内容。原管理机制处理冲突，禁止手抄受管副本。

源码、实际目标安装及 Agent 行为分别证明本层结果。`local_candidate` 不能建立 `formal_fork_source_lock`、其他业务仓采用或完整升级/Release 矩阵。对应 R153-03/05、R818-04；由 T153-04/05 和 T818-03/04 观察。

## D818-01 / CON818-01：原完整段落内修改方法

#818 在唯一正文原第2节修改整理与必要性判断，在第3节承接完整规则及验收，在第4节承接独立阅读与反查，在第5节定位四个原职责。采用直接修改及薄引用，使一个 consumer 仍只需读取一份完整方法。原来源保留、局部完整性和必要保护继续有效；不以叠加摘要、平行准入流程或语义脚本承接方法。

该选择服务 R818-01..04，复用 T818-01/02 的原入口观察。后续若真实改变 owner、状态、I/O 或依赖，须回最早受影响的原 owner，本单元不预留另一机制。

## D818-02 / CON818-02：共同审核规范只定位专题

[共同审核充分性规范](../../../trellis/presets/guru-team/spec/workflow/review-sufficiency.md)在原覆盖形成职责中定位同 provider 的 Issue 内容正文。它保留 [D717](../../design/current/review-sufficiency.md) 的方法归属、目标 authority 分开及原阶段边界，不复制 Issue 方法，也不将 #818 扩成所有审核阶段改造。对应 R818-03/04；T818-02/03 分别观察行为与分发。

## D818-03 / CON818-03：分发测试的证据边界

`test_review_sufficiency_distribution.py` 保留十二个 consumer 的完整安装及平台字节比较、provider spec/manifest、引用、reapply、用户保留和 sidecar。固定 `read` 措辞正则及依赖它的重复规范读取退出；合法 recovery-only consumer 的措辞差异不能被该测试误判为未分发。语义加载仍由实际 Agent 观察，不能改 SKILL 迎合测试。对应 R153-05、R818-04，由 T818-03 记录首轮失败及修正重跑。

## R/D/T 整合与历史

完整测试策略及观察位于 `docs/test/current/issue-content.md`；本贡献 [traceability](../../requirements-design-test-contributions/818-issue-minimal-sufficiency/traceability.md)定位原身份、提案和实际目标。只有原 RDT owner 在真实工程验证后重读实际 target、整合并逐项 readback，才返回整合事实；其后仍待 TaskCommit 和同一次独立 committed Review。当前知识状态不替代 Delivery、Completion、Closure 或发布判断。
