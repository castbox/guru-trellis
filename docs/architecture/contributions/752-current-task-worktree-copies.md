# #752 current-schema Task 副本迁移：Architecture 差额

本贡献属于 Task ce0248be-6b58-4239-8c1f-7444625adf73、generation 0、Delivery cffee5bc-4a87-465e-b056-534b530951d5。来源为 https://github.com/castbox/guru-trellis/issues/752；方案由本 Delivery design.md 单写。独立 candidate_assessment 已选择 architecture_impact / target_native，ADR-024/017 继续有效，不新增 ADR。

## Authority、before 与差额

适用 authority 为 guru-trellis-architecture，constitution 为 guru-trellis-design-constitution-v1，change contract 为 guru-trellis-architecture-change-contract-v1。晋升前来源为固定 Git 2ab135ed2d3908966785bb23ad42ada0790f0c81 的两个命中完整单元；实际晋升前原 owner 另读 live target 与 expected-current。

ARCH-DOM-043 拥有公共 Task/Delivery/session/转换与 Guru 语义/私有 owner 分工；本轮在同一单元展开 current peer 的 public parser/group/binding 唯一责任和 private conversion 排除。ARCH-INT-046 拥有 matching mixed source 安装和旧副本接续；本轮展开 current-schema peer、新 source pair、actual installed/resume/rollback 的证明边界。#531 的历史 148 roots、受控验证与未验证项保留其观察截止，不能改写成当时已完成。

## 完整拟写单元与职责

| 目标 | 差额和仍有效条件 |
| --- | --- |
| docs/architecture/03-domains/ownership.md / ARCH-DOM-043 | Fork 独占 current peer parser/group/authority；Guru 透传原 binding，不建第二 copy 模型或 binding writer。只有 selected workspace 的 projected Task 进入原 private owners；peer 不提供 lifecycle/selection/Delivery authority。保留整体 scope、唯一 Author、各 gate、远端恢复及终态分工。 |
| docs/architecture/04-integrations/distribution.md / ARCH-INT-046 | 全部 registered roots 纳入，唯一 bound checkout 与 complete parsed equality；peer raw bytes/modes/metadata 保留。新/旧计划各用原匹配 source pair 和 anchors，实际 installed 验证与 source/CI 分开。保留原 canonical/preset/platform、reapply/drift、业务采用与 Release 边界。 |

同名目录 proposed/docs/architecture 保存这两个文件的完整拟写；只有上述单元改变，其他字节保留。Author 准备隔离候选；独立 Architecture phase2 和完整 candidate Check 通过后，原 Architecture owner 在 final_integration 读取实际目标、整合有效条件、写入并读回，再由 implementation 绑定实际 after，最终 Check/commit/独立完整 Review 覆盖。此贡献不直接使 CURRENT 生效。

## Required concerns

authority-binding / constitution-binding：固定 before、当前独立候选和真实 after 分开；遵守既有五原则，不以目标或 CI 自证。
boundary-and-decision / owner-and-single-writer：Fork 承载公共模型，Guru 保持原语义和私有 owner；复用 defer 的 selector2，不新增模型/writer。
compatibility-and-exit：旧 executor 不接新计划；旧冻结 source/checkpoint 留原 pair 同计划恢复，不换包续跑，不加 runtime 双读。
gap-and-deviation：本轮能力缺口由 matching successor 关闭；没有新 GAP、宪法例外或第二 authority。
parallel-scope：只写隔离拟写，shared 两目标留原 promotion owner；不覆盖他方 source/worktree。
evidence-and-freshness：源码、上游 CI、本地组件、actual installed、原业务及 Release 分层；实际结果由 RDT 唯一 Test 记录。
review-and-promotion：final_plan 审本贡献，候选 Check 之后才晋升，实际 after 仍需最终 Check 和 committed Review。

## 验证与边界

Delivery design V1–V5 及 RDT 贡献 test.md 拥有 current-copy dry-run/migrate/resume/rollback、匹配 source/build、代表性多 workspace actual installed、Task/session/peer 保留、private 排除和 projection/drift/mode 事实。当前贡献是拟写，不预填执行通过。完整多平台 Release 矩阵、远端 immutable marketplace 和原业务仓升级由独立 owner 承担。
