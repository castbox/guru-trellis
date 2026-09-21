# Design: #456 Public Consumer Contract Reconcile

## 1. Design Position

本设计不创建新的 lifecycle model。它把 live #443/#436/#434 public consumer facts 与 #454 exact contract 做逐项对照，并将四类内容分离到固定产物：

| Document | Sole responsibility |
| --- | --- |
| `reconcile/01-current-contract-inventory.md` | 记录当前三组 consumer 的 live facts 与证据 locator。 |
| `reconcile/02-contract-mapping.md` | 为每个 current item 绑定 #454 target 与唯一 disposition。 |
| `reconcile/03-migration-boundary.md` | 为每个 replace/retire 项绑定 migration owner、依赖、阻塞与承接任务。 |
| `reconcile/04-reconcile-result.md` | 汇总闭包、未解决项和唯一后继。 |

## 2. Identity And Join Keys

四份文档统一使用稳定 `Item ID` 连接，不依赖表格行号或自然语言推断：

```text
443-SESSION-*
436-REACTIVATE-*
436-COMPLETION-*
436-CLOSURE-*
436-FINISH-*
436-CLEANUP-*
434-GRAPH-*
```

每个 Item ID 在 inventory 中定义一次，在 mapping 中恰有一个 disposition；`replace`/`retire` 项在 migration boundary 中恰有一行，在 final result 中按 owner/承接任务汇总。

## 3. Inventory Shape

每个 current item 必须记录以下全部字段：

- group、package/Skill id、surface type；
- canonical/installed/interface/schema/consumer/workflow/command/registry/manifest/platform locator；
- current schema identity、input/output DTO、external exit、unique consumer、workflow target/stop；
- current metadata/session/workspace/branch/checkout/Reactivate/resource dependency；
- live evidence classification 与备注。

同一逻辑 contract 的 canonical/installed/platform projection 可聚合为一个 Item ID，但必须列出全部适用 locator 和 parity 状态。

## 4. Mapping Shape

每个 mapping 行必须包含：

- Item ID；
- current contract；
- #454 target contract section/DTO/exit；
- `retain|replace|retire|out_of_scope`；
- disposition reason；
- target public owner/consumer；
- no-alias/no-dual-read 约束。

`retain` 只用于 current bytes/semantics 已与 #454 一致的项目；名称相同不构成 retain 证据。

## 5. Migration Boundary Shape

每个 `replace`/`retire` 行必须包含：

- affected package/files；
- unique migration owner；
- exact #454 dependency；
- forbidden activation consumer/route；
- blocking=`yes|no`；
- successor task；
- completion proof。

承接任务按 authority owner 分组，禁止把 #454 substrate 实现、#443 session migration、#436 lifecycle migration 和 #434 graph activation 合并成一个无边界任务。

## 6. Fixed Cross-Document Invariants

1. 所有文档引用完整 SHA `b695adc928c2064bd27f07e2bb3bbbd034540571`。
2. `Inventory Item ID set = Mapping Item ID set`。
3. `Mapping replace/retire Item ID set = Migration Boundary Item ID set`。
4. `out_of_scope` 不产生迁移动作；必须给出排除理由。
5. Session payload、workspace authority、Reactivate exits、resource/Finish/Cleanup owner 使用 PRD 固定边界。
6. #434 只拥有 route composition 与 activation，不拥有 substrate state。
7. 历史 task、Issue evidence 和 #434 dirty worktree 不写入。

## 7. Validation Design

- 文档结构与交叉引用：Item ID 集合、disposition enum、完整 SHA、owner/successor 非空检查。
- Live evidence：repository search + interface/schema/workflow/registry/manifest/platform locator 人工语义核验。
- Workflow validation：`task.py validate`、`git diff --check`、planning wording review、Architecture impact、plan approval。
- 不执行实现、安装、runtime 或多平台矩阵验证。

## 8. Design Conclusion

新 #454 exact commit 已统一 Bind stored/public payload：session record 与 Bind success handoff 均只携带
`TaskLifecycleDTO(task_id, lifecycle_generation)`，需要 artifact 的 consumer 按 TaskId fresh 派生 TaskRef。

四份 reconcile 文档已形成完整 Item ID 闭包：Inventory 与 Mapping 均为 47 项，Mapping 中所有
`replace|retire` 项均在 Migration Boundary 中有唯一 owner、依赖、禁止激活边界、blocking 与 successor。
本 task 仍保持 `planning`，下一步是 Phase 1 wording、Architecture impact 与 plan approval，不是实现或激活。
