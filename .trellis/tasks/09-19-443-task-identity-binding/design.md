# #443 设计：task identity-centered multi-session binding

## 1. 设计结论

新增一个独立的 `guru-bind-task-session` capability package，拥有 session binding、rebind、switch、resume 的语义判断、私有 runtime、deterministic validator、typed exits 与 consumer projections。global workflow 只在 #434 接入时消费该 package 的 public contract；本 Issue 不修改现有 22-step production graph。

现有官方 `task.json`、task/workspace runtime mapping、live Git/worktree 与 Trellis session resolver 继续是 identity authority。新能力不得创建第二 task ledger、workspace/developer 机制、Issue scope ledger 或全局 lifecycle store。

## 2. Identity model

```text
task_identity = task.json + task artifact locator + source Issue identity
workspace_identity = task mapping + workspace mapping + live worktree + branch + repository common dir
session_binding = session_id + task_identity + workspace_identity + lifecycle_generation + current_route + freshness
```

- task identity 长期稳定；branch/worktree/session 可替换。
- `session_binding` 只写入 `.trellis/.runtime/guru-team/session-bindings/` 下的 ignored owner-private 文件，完成 direct consumer 后删除或标记过期。
- `lifecycle_generation` 来自 current task/re-activate facts；generation 变化自动使旧 binding、Finish/Cleanup receipt 失效。
- session context 缺失、binding owner 不匹配或 current route 不唯一时，validator 返回 fail-closed stop，不做修复猜测。

## 3. Capability flow

```text
caller intent
  -> live task/repository/workspace/session discovery
  -> semantic AI Gate: choose resume | rebind | switch | blocked
  -> deterministic identity validator
  -> conditional binding write / revoke / projection
  -> typed exit to one declared consumer
```

支持四类入口：

- `resume_current_task`：已有合法 binding，fresh reread 后继续当前 owner。
- `rebind_missing_session`：当前 session binding 缺失，基于完整 live identity 建立同一 task 的新 binding。
- `switch_task`：经当前对话授权后切换到独立 task，写入新 current route，不覆盖另一个 task 的 binding。
- `reactivate_rebind`：消费 #436 Reactivate 的新 lifecycle generation，撤销旧 generation 并建立新 binding。

每类入口均只返回最小 `task_ref`、`session_binding_ref`（必要时）、`lifecycle_generation`、`resume_target` 或 stop reason。authorization、完整 live snapshot、绝对路径、digest bundle 和私有 recorder 数据不进入 public DTO。

## 4. Ownership and integration

| 责任 | Owner | 本 Issue 行为 |
|---|---|---|
| task identity | official Trellis task store + current Git/worktree facts | 只读取并校验 |
| session binding | `guru-bind-task-session` | 新增唯一 writer/validator |
| task creation attach | `guru-create-task-workspace` | 保留 #438 attach；成功后投影 binding seed，不复制逻辑 |
| Reactivate generation | `guru-reactivate-task` | 输出 generation 与 rebind input；不由新 package 改写 Reactivate 语义 |
| Completion/Finish/Cleanup | #436 owners | 只消费 current generation/fresh binding，不接受旧 receipt |
| global route | #434 | 后续单独接入；本 Issue 只提供 contract/consumer declarations |

## 5. Fail-closed and idempotency

- repository common dir、task ref、task.json identity、branch、worktree、base HEAD、两份 runtime mapping、session id、lifecycle generation 必须同一轮一致。
- rebind 重试若 identity 与现有 binding 完全相同，返回同一 binding projection，不创建第二记录、不执行 task/worktree mutation。
- 任一 mismatch、未知 task、外国 session、过期 generation、旧 Finish/Cleanup receipt 或缺少 session context 均 zero-write stop。
- 只处理诚实协作下的正常 stale/mismatch/状态丢失，不扩展并发锁、恶意伪造或故障注入防御。

## 6. Public contracts and migration

新增 package 使用 `judgment_mode=semantic`、Interface 1.4、独立 input/output schemas、四个正向 exits 与一个 blocked exit；consumer projections 在 interface.json 中声明。旧 `guru-create-task-workspace`、`guru-reactivate-task` 与现有 workflow contract 保持兼容，只增加 additive handoff 字段或 package-local bridge；不改变旧 exit/schema 的语义。

canonical source 位于 `trellis/skills/guru-team/packages/guru-bind-task-session/**`，通过现有 registry、manifest、preset apply 分发到 `.trellis/guru-team/`、`.agents/skills/`、`.codex/skills/`、`.cursor/skills/`、`.claude/skills/`。任何旧 session binding reader 若与新 owner 重叠，必须在实现阶段删除或改为薄 projection，并更新 ownership inventory。

## 7. Tests

- package contract/schema/projection tests：入口互斥、typed exits、最小 DTO、unknown field 与 stale stop。
- runtime tests：合法 resume、missing binding rebind、idempotent retry、task/repo/branch/worktree/mapping/base/session/lifecycle mismatch zero-write。
- integration fixtures：A→B→A、跨 session resume、Reactivate generation invalidation、Finish/Cleanup old receipt rejection、#438 attach handoff。
- distribution tests：registry/manifest counts、canonical↔installed/platform parity、preset reapply、dogfood drift、ownership 与 `git diff --check`。
- 不宣称 #434 production graph activation；由 #434 另行执行完整 cutover 验收。

## 8. Docs SSOT Plan

采用 `capability_addition + architecture_contract_sync`：

1. 更新 task-local Requirements/Design/Test trace，明确 #443 与 #434/#436/#438 的 owner 边界。
2. 新增 architecture contribution/ADR，记录 stable task identity、短期 binding、single writer、generation invalidation 与 fail-closed route。
3. 更新 `.trellis/spec/workflow/{data-contracts,skill-package-contract,workflow-contract,quality-guidelines}.md` 中的 current identity/binding contract 与验证清单。
4. 更新 registry/manifest/preset README 与 package references；只同步 canonical source → installed/dogfood projection。
5. 不修改 Evolution Requirements 的产品目标，不提前把 #443 标记为 #434 activation 或 Release completion。

## 9. Manual recovery extension

新增 `manual_recovery` semantic profile 与 `session_manually_recovered` typed exit。它只在用户明确授权的当前对话中进入；runtime 先从 task artifact 与 live workspace/branch/HEAD/base 重建最小 identity，再写 task/workspace mapping 与 current session binding。该 profile 不能消费或生成 semantic pass、task activation、Completion/Finish/Closure/PR/Issue 事实。

当 mappings 缺失时，resolver 允许一个显式的 `allow_missing_mappings` preflight 分支，但仍要求 task artifact、worktree、branch、base、repository common directory 和 session context 全部可验证；普通 resume/rebind 继续要求现有 mapping 完整。manual recovery 完成后必须重新运行同一 boundary validator，任一 post-write mismatch 进入 blocked。


## Corrective review: base provenance and profile contracts

缺少任一 runtime mapping 时，base HEAD 必须来自当前 task 顶层/metadata 或仍存在的 mapping 的既有 `base_head`，并与 fresh live base ref 一致；没有 provenance 时在任何恢复写入前以 `stale_identity/base_head` 停止，不从当前 base HEAD 反推历史边界，不新增 checkpoint 恢复机制。

profile→route 为闭集：`resume_current_task→resume`、`rebind_missing_session→rebind`、`switch_task→switch`、`reactivate_rebind→reactivate`、`manual_recovery→manual_recovery`。schema 和 runtime 均拒绝其它组合。每个 profile 指向独立、schema-valid 且 discriminator 一致的 input example；switch example 明确 source 与 target。该修订不接入 #434 production graph。

## Corrective review follow-up: legacy mapping provenance

无论 mapping 是否存在，只要当前 task identity、metadata 与现有 mapping 集合无法提供可信 `base_head`，identity validator 都必须在任何 session/mapping 写入前停止；不能将 live base ref 的当前 HEAD 反推为历史边界。`base_branch` 的顶层字段和 `meta.base_branch` fallback 先统一解析为 `facts.base_branch`，recovery writer 只消费该解析结果。
