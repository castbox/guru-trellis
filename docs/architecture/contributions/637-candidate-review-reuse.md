# #637 候选适用性架构贡献

状态：`reviewed_promoted`（本贡献已由原 Architecture owner 在分支内晋升到 `current-main-0.7.0-guru.105`；最终 main Check 与独立 committed Branch Review 尚未验证）。change_path：`target_native`。TaskId=`637-candidate-review-reuse`，generation=0，Delivery=`5499bb2d-86d7-4a5c-9747-9b06e00f4ef9`。唯一详细方案是该 Task 所选 Delivery 的 design.md。本文保留本 Task 的贡献及晋升结果，不替代共享 CURRENT 或正式 gate 结果。

## Authority、职责与前后变化

比较起点：Git `39169628f5f79cb48673eae96a36670e73f4dbbb:docs/architecture/`，Architecture `current-main-0.7.0-guru.104`，constitution `guru-trellis-design-constitution-v1`，change-contract `guru-trellis-architecture-change-contract-v1`。需求与设计的前像是 RDT `current-main-0.7.0-guru.113` 的完整生命周期单元。晋升后，RDT 使用 `current-main-0.7.0-guru.114`，Architecture 使用 `current-main-0.7.0-guru.105`。原 owner 在写前重读各自 expected-current；版本前进不充当 semantic pass。

Guru Planning 使用 3.0/Delivery1.0；非 Planning 使用 4.0/Delivery2.0；project descriptor1/result2.0 保持。九项 concern、现有 descriptor、check 与 result identity 均不新增或改名。本 Markdown 贡献沿用既有兼容格式；不新增第二份结构化贡献。

变更来源是 Issue #637 的八项行为及合法证据边界。Before：finding 修正后的 distinct fresh 完整重审和后继架构重建条款会要求重复已有适用覆盖。After：七个原 owner 读取 workflow-contract 的唯一适用性定义，首次完整独立审核仍然执行。后继 owner 用可核验的原覆盖、全部实际差额和受影响依赖形成当前完整结论。没有新架构事实时，不仅因身份或阶段变化重建同一评估。同一合规独立 reviewer 可以先执行 Architecture，再执行 Branch Review；两个阶段的判断和正式结果仍须实际完成。

各 Skill 继续独占阶段语义，workflow 只编排。原 runtime 只承担 executor、validator 和最小 recorder；官方 Trellis 继续拥有 Task/Delivery 公共状态。Task writer 只写本 Task，RDT 与 Architecture 由各自原 owner 单写共享晋升，平台入口不复制业务步骤。原 GateResult、Git 和当前正文已经能承接所需覆盖；没有新增通用覆盖字段、reviewer 状态、cache、审计链、兼容 reader 或第二 store。

## 九个 required concerns

| Concern | 当前适用性、承接与边界 |
| --- | --- |
| authority-binding | applicable：绑定上述 `.104`/RDT `.113` 前像与原 Guru/project identities；后继为 Architecture `.105`/RDT `.114`。写前 live expected-current 与写后完整正文均由原 owner 核验；无关版本不使在途候选自动失效。 |
| constitution-binding | applicable：constitution v1。以原结果、Git 和当前正文承接最小必要复杂度，不加账本或判断脚本；其它原则按实际职责、概念与单向收敛判断，不建立第二评分表。 |
| boundary-and-decision | applicable：单一共享规则和七个原职责保持。ADR-019/028/029/030/033 继续有效；ADR-034 只替代无因 fresh 重审及后继架构重建的冲突片段。 |
| owner-and-single-writer | applicable：原 semantic owners、官方状态 owner 及 RDT/Architecture 晋升 single-writer 不变。独立性来自未参与当前实现的实际责任，不由身份变化或字段证明。 |
| compatibility-and-exit | applicable：直接演进受控 Markdown 及 matching consumers；保留 `fresh_final_review` wire，但显式迁移其窄含义。完整旧安装固定继续或成套升级；同 key 回原 owner，旧结果不转换成新 pass。 |
| gap-and-deviation | applicable：不新增 GAP，也不宣布关闭 ARCH-GAP-006/008。首次完整覆盖、独立性或真实质量缺失仍阻塞相应门禁；闭合须有命中证据和原 owner 的当前判断。 |
| parallel-scope | applicable：允许本 Task 隔离 source、贡献和验证；不写其它 Task 贡献、不抢写共享 CURRENT/GAP、不热改其它安装。共享晋升继续按原 owner 序列化。 |
| evidence-and-freshness | applicable：采用原公开 GateResult/调用对象、精确 Git、当前正文和可核验原命令事实。当前候选仍由当前 owner 判断；计划 ref 不证明工程命令，private 退休后不重建或跨 owner 读取。实际 Agent、fixture、installed 与 remote 结果分别报告。 |
| review-and-promotion | applicable：独立 Phase2 评估完整候选、全部拟写差额与 before authority，原 owners 按原入口完成分支内晋升并读回适用性。最终 Check、commit 和独立 committed Review 仍须覆盖晋升后的全部差额；本状态不证明这些后续门禁已通过。 |

## 最终职责、正文与兼容退出

完整 Architecture 定义位于 [system](../01-current/system.md)、[ownership](../03-domains/ownership.md)、[distribution](../04-integrations/distribution.md)、[rules](../06-governance/rules.md) 和 [change-contract](../06-governance/change-contract.md)。[ADR-034](../adr/034-candidate-applicability-and-coverage.md) 承接本次必要决定；ADR-028 的固定范围、ADR-030 的晋升顺序及 ADR-033 的 Draft 非最终结果继续保留。RDT 的最终完整单元位于 `docs/requirements/current/task-delivery-lifecycle.md`、`docs/design/current/task-delivery-lifecycle.md` 和 `docs/test/current/task-delivery-lifecycle.md`；对应版本入口为 `.114`。

finding 闭合与最终完整覆盖可由同一合规独立 reviewer 完成，但修复、旧 pass 或闭合结果不能投影成新通过。覆盖不足时补审；组合影响不明时完整审核。Publication/Merge 判断各自 payload、Issue、candidate 与 live facts，并消费仍适用的内容判断，不重复无变化业务设计。

首次 `implementation_required` 没有 passed full_review，refs 只定位对象与 finding。采用已有审核工作时，仍须有实际原调用、公开结果、Git 和当前正文支持覆盖。原 GateResult shape 保持，不更改 public I/O。`MIGRATION-637.md` 负责 matching 切换、旧条款退出和同 Delivery 在途接续；原 owner 消费并退休自己的 private 状态，source 编辑不隐式热迁移活动 runtime。

原评估 descriptor 继续为 `guru-trellis-architecture-convergence:repository:1`，入口为 `docs/architecture/06-governance/change-contract.md`，结果合同为 `guru-project-architecture-check-result-2.0`。当前适用性逐次判断，不复用旧 semantic pass。临时 proposed-target 副本已由本次最终目标消费并删除；本贡献不依赖这些临时路径恢复。

## 实际实施与验证边界

canonical 控制面与 matching 平台投影已实施。真实工程命令、独立 Agent 同构样本、文档冲突整合、共享 Runtime 检错与局部闭合、缺项补跑、公开结果恢复、private 退休以及实际安装结果，由唯一 [RDT Test](../../requirements-design-test-contributions/637-candidate-review-reuse/test.md) 单写；本文不复制耗时、命令清单或逐轮结果。

开发 Task 已通过原 `guru-upgrade-tools` 从干净完整 H source 执行 matching tools 切换，正式结果为 `tools_upgraded`。目标 installed validator、原生 current/continuation 入口及三平台 dogfood drift 已执行通过。该安装使用合法 `local_candidate` provenance；`formal_fork_source_lock` 未验证，不手填安装 manifest。新 clean 样本的 reapply/在途保全有成功证据，但含 228 个 legacy archives 的普通全仓库 preset reapply 仍在写前返回 `upstream_delivery_migration_required`，未通过，未通过删除归档绕过。

main 最终完整当前 Check、独立 committed Branch Review 和 #636 最终同 PR 组合尚未验证。共享 Runtime 的局部闭合不代表正式 Branch finding-fix 循环已执行。#638 未来接口、外部业务采用与生产效果、完整 Release 及多平台升级矩阵均未验证。分支内知识晋升不证明 Task Completion、最终 publication、merge、部署或采用通过。
