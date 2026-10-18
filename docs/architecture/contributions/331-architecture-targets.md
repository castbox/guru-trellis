# #331 Architecture 正文候选定位

状态：`historical_pre_promotion_inventory`。本清单只供原独立 Phase2 reviewer 和原 promotion owner 定位实际完整拟写正文；不拥有规则、不记录审核结论，也不代替内容比较。归属和完整 concerns 由 [原 contribution](./331-current-effective-knowledge.md)拥有。

| 实际候选 locator | 前驱与本次差额 |
| --- | --- |
| `trellis/knowledge/technology-baselines/trellis-extension/README.md` | 新公共源版本导航；只含身份、版本、状态和 locator。 |
| `trellis/knowledge/technology-baselines/trellis-extension/versions/1.0/baseline.md` | 新实际通用技术定义 `trellis-extension-stack@1.0`，八项稳定技术选择由源 owner 拥有；无本 Task/分支/本机信息。 |
| `docs/architecture/00-foundation/stack-selection.md` | 新 `ARCH-FND-STACK-001`：本项目固定上述源/version，持有选择、约束、差异与实现证据读取关系。 |
| `docs/architecture/06-governance/rules.md` | 保留 `ARCH-GOV-001..011` 身份；008 直接给出 ADR-030 顺序，009/011 将已退休 lifecycle 片段换为 current owners。新增012定位完整知识和两层源关系。 |
| `docs/architecture/06-governance/change-contract.md` | 保留九 concerns、descriptor/check/result identities；直接展开阶段适用性、完整候选、pre-Check promotion、恢复和两层知识读取关系。 |

治理前驱是 Git `bdb5185c673c91b2fb5cfc66ffbb33849904a69c:docs/architecture/06-governance/`，对应阶段适用 Architecture `.100`。`ARCH-GOV-008` 的时机来自已接受 ADR-030；009/011 的 owner 边界来自 ADR-013/024/025 和当前公共 Skill Interfaces。旧 ADR、贡献、evidence 与 Git 正文不回写。

本清单写作时，源导航、源1.0和项目投影均为 `proposed`；当前接受状态读取各实际 authority。原 owner 只有完成独立拟写评估后，才按 exact reviewed targets 接受源与项目 FOUNDATION 选择，并把共享 Architecture successor 指向本批正文。接受不证明 CURRENT 已实现；唯一 Test/EVIDENCE 仍承担真实验证。未完成时保留旧 authority 和候选状态。共享入口、正式 ADR、实际结果与最终 promotion 由原协调 owner 处理，本清单不新增第二 authority。
