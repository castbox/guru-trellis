# #456 对齐 #443/#436/#434 public consumer 到 #454 lifecycle contract

## 1. 目标

在当前独立 task/worktree 中，只对 #443、#436、#434 三组 public consumer 执行 contract reconcile，形成可直接交给后续实现任务使用的 current inventory、逐项 disposition、迁移 owner/依赖/阻塞边界和最终承接结论。

本 Issue 只交付 reconcile 设计与迁移合同，不修改 production code、schema、package interface、workflow、registry、manifest、projection 或 installer。

## 2. Authority

### 2.1 Live requirement authority

- GitHub Issue：`castbox/guru-trellis#456`
- Live Issue 更新时间：`2026-09-21T06:17:54Z`
- 当前 task：`.trellis/tasks/09-21-456-task-lifecycle-contract-reconcile`
- 当前分支：`codex/456-task-lifecycle-contract-reconcile`
- task base：`main@9d541be35a0cb4c6bef60a0c19b9c8eac39e6690`

### 2.2 Exact target contract

```text
repository: castbox/guru-trellis
branch: codex/454-task-lifecycle-state-model
commit: b695adc928c2064bd27f07e2bb3bbbd034540571
design root: .trellis/tasks/09-20-454-task-lifecycle-state-model/
```

必须读取且只引用以下 #454 文件作为 target authority：

- `prd.md`
- `design.md`
- `design/10-composition-and-migration.md`
- `design/11-public-contract-migration.md`
- `design/12-final-consistency-review.md`

若该 exact commit 出现设计缺口，当前 reconcile 立即停止；不得在 #456 内发明替代 contract。

## 3. Reviewed Consumer Groups

### G-443 Session binding

只覆盖 `guru-bind-task-session` 及 session resume、switch、rebind、Reactivate binding public contract。

### G-436 Post-delivery lifecycle

只覆盖 Reactivate、Completion、Closure、Finish、Cleanup 对 lifecycle/session/resource contract 的直接消费。

### G-434 Production graph consumer

只覆盖 #434 对 #443/#436 contract 的 workflow target、external exit、projection、consumer schema 与 package interface 消费。

未列入以上三组的其它 package 一律为 `out_of_scope`。

## 4. Reconcile Rules

每个字段、DTO、schema、exit、consumer、route、workflow target/stop、command、registry/manifest selector 和 platform projection 引用必须有且只有一个 disposition：

| Disposition | Meaning |
| --- | --- |
| `retain` | 当前 contract 与 #454 exact target 一致，保持现状。 |
| `replace` | 当前 contract 必须迁移到指定的新 DTO、schema、exit、consumer 或 owner。 |
| `retire` | 当前 contract 必须从 active graph 和 public package 删除。 |
| `out_of_scope` | 不属于三组 consumer 或本 Issue 的 planning-only delivery，并写明理由。 |

每个 `replace`/`retire` 项必须同时声明：受影响 package/文件、唯一迁移 owner、依赖的 #454 contract、迁移完成前禁止激活的 consumer/route、是否阻塞后续实现、唯一承接任务。

## 5. Fixed Authority Boundaries

1. Session public payload 只保留 `TaskId + lifecycle_generation`；不得携带 path、branch、HEAD、resource ownership 或 authorization。
2. `task_workspace`、workspace mapping 和 path-bearing locator 不再是 active domain/public authority；其 current reader/writer/selector 必须按逐项 disposition 收敛。
3. 旧 Reactivate public exits 必须映射到 #454 的 target exit closure；不保留 alias。
4. Resource ownership ledger 只有 lifecycle resource substrate owner；Finish 只封存 terminal archive projection 与 sealed generation inventory；Cleanup 独占 cleanup result 和 resource deletion。
5. #434 只编排 #443/#436 的 public contracts，不复制 TaskId、generation、session、checkout、branch association、resource ledger、Finish inventory、Cleanup result 或 Reactivate transaction authority。
6. 不存在长期 dual-read、dual-write、alias、translation adapter 或 compatibility shim。

## 6. Fixed Deliverables

本 task 必须交付且保持相互一致：

1. `reconcile/01-current-contract-inventory.md`
2. `reconcile/02-contract-mapping.md`
3. `reconcile/03-migration-boundary.md`
4. `reconcile/04-reconcile-result.md`

`prd.md`、`design.md`、`implement.md` 负责 Phase 1 workflow planning；四份 `reconcile/*.md` 是 Issue #456 的固定业务产物。

## 7. Acceptance Criteria

- [ ] AC-456-01：#443、#436、#434 三组 consumer 均有完整 current inventory。
- [ ] AC-456-02：每个受影响字段、DTO、schema、exit、consumer、target/stop、command、manifest/registry selector 和 platform projection 都有唯一 disposition。
- [ ] AC-456-03：每个 `replace`/`retire` 项都有唯一 owner、#454 依赖、禁止激活边界、阻塞结论和承接任务。
- [ ] AC-456-04：session payload 固定为 `TaskId + lifecycle_generation`，machine-local path/branch/HEAD/ownership/authorization 字段处置完整。
- [ ] AC-456-05：workspace、Reactivate、resource ledger、Finish inventory、Cleanup result 的 authority 边界没有第二套解释。
- [ ] AC-456-06：#434 只消费 public contract，不复制 substrate authority。
- [ ] AC-456-07：四份 reconcile 文档互相一致并绑定同一个完整 #454 commit SHA。
- [ ] AC-456-08：不存在未分类、未指派或依赖自然语言推断才能继续的项目。
- [ ] AC-456-09：不修改 #454、#443/#436/#434 历史 task、#434 dirty worktree 或 production surfaces。
- [ ] AC-456-10：完成声明不包含 substrate/package/graph 实现、业务验证、production cutover 或多平台验证。

## 8. Non-Goals

- 不修改 #454 设计。
- 不修改 #443/#436/#434 历史 task 和旧 Issue evidence。
- 不修改 production code、schema、interface、workflow、registry、manifest、projection 或 installer。
- 不实现 #454 substrate，不实现或激活 #434 production graph。
- 不执行安装、业务验证、production cutover 或多平台验证。
- 不处理三组 consumer 以外的 package。

## 9. Docs SSOT Plan

- Live Issue #456 是 requirement authority。
- #454 exact commit 是唯一 target lifecycle contract authority。
- 四份 `reconcile/*.md` 分别独占 current facts、mapping、migration boundary 和 final result。
- 历史 task/evidence 保持 immutable，只作为 live fact provenance。
