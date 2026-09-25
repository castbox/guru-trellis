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
| `ARCH-DOM-016` | active-task continuation | Guru workflow独占detailed continuation；adjacent DTO的consumer、deterministic producer recovery、semantic owner fresh rerun与activation owner各保持单写；upstream独占extractor和thin entries |
| `ARCH-DOM-017` | active-task Delivery capability | Delivery Review独占slice readiness与PR payload truth；Delivery Publish独占push/PR/Draft/Ready及同计划恢复；Delivery Merge独占merge readiness、受控merge commit与Delivery result；Reconcile独占resolved-tree commit；#434独占production graph activation，#436独占Completion及其后续lifecycle |
| `ARCH-DOM-018` | post-delivery terminal lifecycle | Completion、Closure、Finish、Cleanup与Reactivate各自拥有独立semantic judgment、最小DTO与owner-private recovery；#434独占production graph activation，shared authority promotion仍由Architecture/RDT owners串行完成 |
| `ARCH-DOM-019` | task identity session binding | official Trellis task/session store拥有稳定task identity与底层resolver/persistence；`guru-bind-task-session`独占lifecycle-aware resume/rebind/switch/reactivate/manual-recovery判断与最小runtime write；#438保留creation attach，#436保留terminal lifecycle receipts，#434独占production route activation |
| `ARCH-DOM-020` | platform inventory and exact selection | pinned upstream `AI_TOOLS` owns the complete 22-platform inventory and canonical `AITool`/`cliFlag` mapping；Guru preset owns projection descriptors and managed paths；each installed repository manifest/provenance owns its exact selected set；dogfood consumes only Claude/Codex/Cursor；OpenCode remains explicit-only for guru-trellis |
| `ARCH-DOM-021` | task lifecycle identity and stage evidence | Fork 独占 official TaskId/TaskRef/generation/session primitives；Guru shared lifecycle catalog/runtime 独占 package-neutral DTO、normalization、resolver adapter 与稳定错误；Reconcile 独占 integration commit，Task Commit 独占 exact committed candidate，Branch Review 独占 full/continuity review；本边界不替代 `ARCH-DOM-019` 的现有 deferred binding owner |
| `ARCH-DOM-022` | task checkout substrate | Guru shared lifecycle runtime 独占 call-local checkout plan/candidate/resolution/selection、common-dir live facts、adopt/provision transaction、bounded rollback 与 read-only recovery；machine path 不进入 durable task/session/branch/resource authority；`guru-ensure-task-checkout` 仅是 planned ID，E434 独占完整 package 与 activation |
| `ARCH-DOM-023` | checkout acquisition provenance | acquisition transaction独占transaction-created worktree marker写入，output-loss recovery是唯一只读consumer，direct handoff独占retirement；marker不成为task/session/branch/workspace/resource authority，replacement resource不得继承Guru ownership |
| `ARCH-DOM-024` | task branch association | C4 shared lifecycle runtime 独占 Git common-dir TaskBranchBinding、live candidate discovery、establishment/rebind transaction 与 lost-output recovery；C5 ownership owner只通过窄 port提供current/snapshot/restore/establish/rebind/unresolved-ref能力，不向C4暴露ledger representation；E434独占planned package activation |
| `ARCH-DOM-025` | session and resource control | Fixed Fork official schema-2 session store 独占持久化；C5 adapter 独占 path-free TaskId/generation 投影，缺 context key 不写 session。C5 resource ledger 独占 Git common-dir incarnation/ownership、active conservative recovery、remote HEAD advance、Finish seal 与 Cleanup resolution；C4 只消费 `OwnershipPort`，E434 独占 planned package/production activation |
| `ARCH-DOM-026` | task creation and activation inputs | 独立 Issue owner 仍负责 draft Issue；C6 shared composition 消费 reviewed target 与 C2-C5 primitives，建立 TaskId/generation 0、初始 binding/ledger、optional path-free session，并只读恢复 exact creation result。未来 `guru-create-task` 与 `guru-activate-task` 在 E434 package/graph activation 才获得完整 semantic gate、status mutation 与 recovery；C6 input preparation 只校验 planning/current base 连续性，不越权执行 activation |

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

## #419 Active-task continuation 归属

- workflow只分类并调用原owner，不生成semantic pass或mutation success。
- workspace created-result、activation、Phase 2与Task Commit的恢复分别留在原producer。
- Branch Review与Publication成功checkpoint退休后，跨会话只允许fresh semantic review。
- upstream start/continue/hooks/platform/meta不进入Guru preset或managed inventory。

## #435 Active-task Delivery 归属

- 三个Delivery packages只提供additive capability；当前production workflow仍使用原22 invokes / 98 exits图。
- `delivered`只表达一个业务Delivery完成并保持task active；它不是task completion、Issue closure、archive、Finish或Cleanup。
- Merge owner写受控merge commit trailer；历史发现只读GitHub/Git immutable facts，不读取PR body、当前branch存活或task-local ledger作为identity authority。
- #434在#435与#436 capability均ready后原子激活新图并退休旧edges；#436单独拥有Completion、Closure、Finish、Cleanup与Reactivate。

## #443 Task identity session binding 归属

- task.json、artifact locator、repository common dir、live Git/worktree与official runtime mappings共同提供identity facts；新package不复制task/session store。
- binding/rebind/switch/resume/manual recovery只由`guru-bind-task-session`判断并执行；public DTO不携带runtime binding identity或private snapshot。
- #438 creation attach、#436 Reactivate/Finish/Cleanup generation/receipt、#434 global route cutover保持各自单写；package存在不表示production route可达。

#408 的独立手动请求不进入上述 Guru lifecycle domain，由当前会话 AI 依
[全局操作边界](../../../trellis/workflows/guru-team/workflow.md#manual-gitgithub-operations)
执行已明确的 Git/GitHub 操作。它不新增 lifecycle owner，也不改写 task、Finalizer 或 archive 的完成状态。
