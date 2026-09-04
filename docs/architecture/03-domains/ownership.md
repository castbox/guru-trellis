# DOMAIN Ownership

| Identity | Domain | Authority |
| --- | --- | --- |
| `ARCH-DOM-001` | workflow lifecycle | global workflow + 23 step-local Skill interfaces |
| `ARCH-DOM-002` | task/workspace/history | task scripts、workspace creator、finalizer、merge owner |
| `ARCH-DOM-003` | semantic governance | planning/check/review/publication/SSOT Skills |
| `ARCH-DOM-004` | deterministic runtime | canonical shared runtime 与 package runtime |
| `ARCH-DOM-005` | distribution | marketplace workflow、preset installer、overlay、manifest |
| `ARCH-DOM-006` | repository knowledge | RDT authority、Architecture authority、minimal spec projection |
| `ARCH-DOM-007` | compatibility harness | #260 live-derived matrix 与 A/B fixture；只证明 task-local lifecycle/provider/archive/recovery/reachability，不成为 #248 Acceptance 或 #252 cleanup public owner |
| `ARCH-DOM-008` | architecture lifecycle governance | `guru-maintain-architecture-baseline` 拥有 impact/path/check/review/promotion 语义；项目 Architecture Baseline/change contract 拥有 decision、GAP、owner、concern 与具体 check semantics；global workflow 只拥有 stage order 和唯一 router |
| `ARCH-DOM-009` | Finalizer provenance | `guru-finalize-task` 拥有 source/target binding、两棵临时 checkout 与 metadata-tail producer；installer 独占 manifest source provenance；`guru-verify-extension-installation` 独占 standalone failure evidence；不存在 shared resolver、跨 lifecycle 调用或第二 writer |
| `ARCH-DOM-010` | repository release orchestration | 仓库私有 `release-guru-trellis-version` 只拥有正式发布两阶段编排、fresh authority/candidate 分类与独立动作边界；既有 task lifecycle owner 和 tag/smoke/Release/Issue closure/cleanup 边界继续各自单写结果 |
| `ARCH-DOM-011` | solution mechanism qualification | `guru-qualify-solution-mechanism` 独占机制资格；normal-scenario owner、caller severity/route 与 deterministic runtime 不复制该判断 |
| `ARCH-DOM-012` | archived-task recovery | Merge 独占 task-work finding 分类；`guru-restore-archived-task` 独占原身份本地恢复；Phase 2 与后续 gates fresh 重跑 |

跨 domain 只使用 interface/schema/typed projection；不得读取对方 private checkpoint 作为 public contract。
