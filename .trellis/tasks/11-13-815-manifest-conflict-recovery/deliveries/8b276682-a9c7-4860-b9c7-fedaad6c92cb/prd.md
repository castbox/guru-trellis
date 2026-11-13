# #815 D1：受管 manifest 冲突到原 tools owner

## 1. 整体来源与术语

整体 accepted_scope 为 {"locator":".trellis/tasks/11-13-815-manifest-conflict-recovery/prd.md","revision":"sha256:efda5be37560b85ba3892d669d731e0b767507964157d70f2f7f330879d7a272"}。整体定义由 [Task PRD](../../prd.md) 拥有；D1 scope_ref 选中 R815-01 至 R815-06 及 AC815-01 至 AC815-06。公共 DeliveryKey 为 {"delivery_id":"8b276682-a9c7-4860-b9c7-fedaad6c92cb","lifecycle_generation":0,"task_id":"815-manifest-conflict-recovery"}，planning_root 为 deliveries/8b276682-a9c7-4860-b9c7-fedaad6c92cb。Direct Source 为 https://github.com/castbox/guru-trellis/issues/815 的要求、验收及兼容边界。该来源的完整旧 blob、原 provenance/hash、原 installer、同身份及原事务恢复是规范性约束；#792 案例仅属历史事实。术语使用整体 PRD 第1节。

## 2. 整体与本批目标、非目标

当前 tools inventory 先解析现存 manifest，正常 Git 冲突标记会阻止 preview/prepare。D1 独立交付有界前像恢复合同及正常两分支的组合验收，覆盖全部整体要求。恢复由现有 Reconcile、tools installer 和 Publication owners 承接。

本批不增加通用恢复框架、公共 Skill/exit/schema，也不变更原语义门禁或旧安装兼容读域。不修改上游，不处理恶意、锁、压力、crash 加固，不绑定发布版本，不执行其它 Issue。完整多平台矩阵不在本批范围。

## 3. 本批起点、前序结果、依赖与剩余责任

本 Task 尚无前序 Delivery。开发 baseline B 和 Planning H0 都是 cb8b4ce349b54cd832ff5b8f72602c5a721ce875；目标 main 与固定内容 B 分开。现有能力包括 tools preview/prepare/invoke、逐路径决定、原 installer、resolved metadata 保留以及 Publication retire_completed。D1 修复这些能力之间的公开接续，并验证实际组合。

依赖当前完整匹配 Guru/Fork 安装及原工具 owner；源码、真实安装和 native 证据分别说明。无延期实现责任；Delivery 后仍由 Task Completion 审查整个 accepted scope，原 Closure/Finish 完成关闭、归档和 live main 可达性。D1 合并不等于 Task 完成。

## 4. 本批调用方、场景与流程

- DS815-01：原整合 owner 在两个正常 canonical 分支及各自 installer 生成物之间遇到 manifest Git 冲突，固定 prior H 与完整旧 blob。临时恢复其原字节以启动旧安装 inventory；原 tools owner审查真实受管差异并重建组合投影。
- DS815-02：tools 正常失败或输出丢失时复用原 frozen plan、preimages 和 recovery_ref。实际未知 mutation 先查事实并沿原操作恢复，不重放。
- DS815-03：最终 installed/native/drift 验证后，原 resolved executor 使用最终组合候选，保留同 Task/Delivery/branch/worktree/PR 和自然 dirty metadata，无关 Task/session/peer 不变，零 unmerged。
- DS815-04：后续 Publication 原 owner 只按 retire_completed 退役已完成私有事务，公共发布事实保留；未完成原操作先恢复。

## 5. 完整行为、条件与约束

D1 承担整体 R815-01..06 的全部条件：只复用固定已生成完整旧 blob，保留原 provenance/hash；AI 逐路径 preserve/replace，最终字节和 manifest 由原 installer 生成；临时前像不进入最终候选。原 dirty task.json 例外保持，不扩大到其它 metadata。未知状态和失败回原事务。

Markdown 拥有判断及入口合同；脚本仅执行已有 Git/installer/validator 动作。既有 public Skill I/O/typed exits 保持；如调查证明必须实质改变原 API，先回原规划和兼容 owner，不静默扩张。规范性来源承诺的唯一具体处置在 design 第3节完成；当前阶段不预填未完成方案。

## 6. 本批验收、验证方式与未决项

| 验收 | 对应整体项、入口与预期结果 |
| --- | --- |
| DAC815-01 | AC815-01：真实 Git 两分支 canonical 和各自 installer 输出重现 manifest 冲突；正常公开路径固定完整 blob，原字节和 provenance/hash 保持 |
| DAC815-02 | AC815-02/05：原 tools owner 逐路径判断并生成最终组合安装，installed/native/drift 与受影响平台一致性通过；无临时前像或未处理 sidecar |
| DAC815-03 | AC815-03：原 resolved 整合提交绑定正确父序和最终树；零 unmerged，当前 dirty Task metadata、无关 Task/session/peer 和原身份保留 |
| DAC815-04 | AC815-04：同操作恢复与 Publication retire_completed 定向回归，公共发布事实不丢，未知 mutation 不重放 |
| DAC815-05 | AC815-06：后续完整 committed review、独立交付和 Task 终态流程核实 scope、Issue 和 live main 可达性 |

以上均待执行。原 installed/native harness 和 app 冲突测试只复用实际覆盖，不冒充本场景通过。需要补正常 manifest 分支组合和实际 Agent 按正文接续的证据。当前 requirements 无未决项，具体源码/测试写集与命令待 Architecture candidate_assessment 后收敛。

## 7. Canonical 引用与本轮差额

- Requirement/behavior：整体 PRD R815；docs/requirements/current/task-delivery-lifecycle.md 的原 single-writer、同身份与 recovery 条件；增加 manifest 冲突有界接续，保持其它条件。
- Design：原 Reconcile/tools/Publication package 的完整 SKILL.md 与 references/contract.md；增加原步骤内入口、临时前像与退出条件，不新增 authority。
- Test：.trellis/spec/workflow/quality-guidelines.md 的 Test And Validation Value、Validation Scope Ownership；采用受影响回归并补真实组合，不执行完整矩阵。
- Architecture：docs/architecture/README.md、constitution 和 change contract 由原独立 owner 在 authority-first 顺序读取；当前候选从真实既有职责作事实评估，尚无最终结论。
