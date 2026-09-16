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
| `ARCH-DOM-013` | public wrapper and closeout transaction | 每个 Skill 的原 command 独占 Happy/compatibility mode；Interface 独占 public wrapper path；preset/validator/matrix/eval 只消费 Interface，shared scripts 不承接 package-private facade |
| `ARCH-DOM-014` | post-review base continuity | Reconcile 独占 compatible base advance 的 semantic classification 与确认后的 local reconciliation commit；Review Branch 独占 bounded continuity judgment；Publication 独占 current reviewed-content acceptance；Finalizer 只投影 prior review identity，不复制任一 owner 的判断或写入 |
| `ARCH-DOM-015` | Issue reference and closure ownership | Guru lifecycle 内，current user/live external authority 与 lifecycle owner持有 requirement/source reference；Publication 独占 Issue reference/closure intent；Finalizer 执行 reviewed payload并投影 exact body SHA-256；GitHub 执行默认分支 closing keyword；Merge mutation前验证 live body identity且只验证 live result；无 task-local classification aggregate 或第二 closure owner |

跨 domain 只使用 interface/schema/typed projection；不得读取对方 private checkpoint 作为 public contract。

## #418 只读复审归属

`ARCH-DOM-002/003/008/013/015` 的 owner 不变；[ADR-010](../adr/010-archived-review-authority.md)
在这些既有边界内划分以下责任，不新增 domain writer：

- Finalizer 原 executor 负责双端归档映射收敛；只读 reader 只验证，不修复映射。
- Merge 只判断当前是否需要归档复审并捕获 PR 快照，不提前批准 merge。
- Branch Review 独占当前完整范围 `B...A` 的独立复审；Publication 独占现有 PR payload 的新语义判断。
- Finalizer 独占原 H 的归档连续性校验和原 `ready_for_merge` handoff；Merge 仍独占最终操作及结果验证。
- Architecture 在三个原阶段分别独立判断 current/blocked；只读来源不进入 promotion/repair 写入。

该链不替代 `ARCH-DOM-012` 的真实 task-work finding 恢复，也不增加 Issue closure owner。

#408 的独立手动请求不进入上述 Guru lifecycle domain，由当前会话 AI 依
[全局操作边界](../../../trellis/workflows/guru-team/workflow.md#manual-gitgithub-operations)
执行已明确的 Git/GitHub 操作。它不新增 lifecycle owner，也不改写 task、Finalizer 或 archive 的完成状态。
