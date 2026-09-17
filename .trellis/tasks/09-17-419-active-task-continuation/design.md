# #419 技术设计：workflow-owned active-task continuation

状态：实现与定向验证进行中。Architecture/RDT contribution 与 draft ADR 已建立；Phase 2、exact-candidate throwaway matrix 和 shared-current promotion 尚未完成。

## 1. 设计原则与边界

本设计采用 `target_native`：上游只提供结构化协议与 workflow-neutral 薄入口，Guru workflow 独占 Guru continuation 语义。不会保留旧 coarse route table 作为 compatibility authority，也不会新增长期 stage-state store。

三类事实必须分离：

1. upstream active-task resolver 提供 exact current-session task identity；
2. `task.json.status` 只表示 coarse lifecycle active/inactive；
3. 当前 `.trellis/workflow.md` 的唯一 `[trellis-continuation]` 区块决定 resume owner、recovery 或 stop。

命中的设计宪法原则为 `concept-semantic-completeness`、`cohesion-change-isolation`、`minimum-necessary-complexity` 与 `debt-one-way-convergence`。

## 2. D419-01 唯一 Guru continuation 区块

在 `trellis/workflows/guru-team/workflow.md` 增加一个完整、非空区块，并同步 `.trellis/workflow.md`：

```md
[trellis-continuation]
<Guru active-task continuation contract>
[/trellis-continuation]
```

区块先校验 exact task identity/status，再按 closed state family 分发。`planning-inline` 与 `in_progress-inline` 只改变执行载体，不改变 mandatory owners/gates。

Phase Index 和 `[workflow-state:planning*|in_progress*|completed]` 收敛为 broad breadcrumb：要求加载 continuation，不再独立决定具体下一步。`no_task` 保留初始请求合同，不进入 active-task continuation。

## 3. D419-02 Phase 1 owner-preserving recovery

Phase 1 使用有序矩阵，而不是从文件存在推断 gate：

| 当前可证明事实 | 合法 owner |
| --- | --- |
| current `guru-create-task-workspace:created` DTO 尚在 | task-created attach consumer |
| created DTO 跨会话丢失 | 原 workspace/task-create owner 的 recovery/rematerialization |
| 三份规划文件尚未全部完成 | current planning author，重读 live Issue 与 task contents |
| wording 缺失/stale | fresh `guru-review-contract-wording:planning_artifacts` |
| Planning Architecture 缺失/stale | fresh `task_impact_sync(stage=planning)` |
| Approval output 丢失 | fresh `guru-approve-task-plan` |
| approved plan 已展示但确认丢失 | 重新展示 current plan 与 activation side effect，重新确认 |
| activation 尚未执行 | workflow-owned `phase-1-task-activation` |
| activation mutation 已成功但 output 丢失 | activation owner 读取 current task state并只重物化成功结果 |

现有 `start-task.sh` 直接执行 upstream `task.py start`，没有 closed activation receipt/output。实现时优先在 Guru workflow-owned activation wrapper 内增加最小 `initial|recovery` 合同：initial 在 boundary/approved DTO/current planning 通过后执行一次；recovery 只接受同一 task 已为 `in_progress`、branch/worktree/mapping/current pair 完整一致，返回同一正式 activation success，不再调用 `task.py start`。该状态只服务 activation 的直接 consumer，不携带或持久化用户确认。

若 live implementation inspection 证明现有 upstream start 已同时提供 task/branch/worktree/current-pair 绑定、idempotent success recognition 和正式 typed output，则复用该输出并删除上述新增 profile 计划；不得并行保留两条 activation authority。

## 4. D419-03 Phase 2 至 Finalizer 前 recovery

Continuation 每个节点先区分：

- **Adjacent DTO current**：task/base/HEAD/content/authority pair guard current 时，直接进入唯一 consumer。
- **DTO lost**：回原 producer。Deterministic mutation/output-loss 走 producer-owned recovery；semantic result fresh 重跑。

具体路径：

1. Phase 2 无 current output：fresh Architecture phase2 + `guru-check-task`。
2. Phase 2 `passed` checkpoint 仍可由 checker wrapper合法投影：由原 producer重物化 DTO，再进入 Task Commit；不能从 checkpoint 名称或存在性直接手写 `passed`。
3. Task Commit 已有 current candidate/receipt：调用原 `guru-create-task-commit` same-candidate recovery；没有唯一 receipt 则停在原 owner。
4. Branch Review DTO 丢失：fresh Architecture branch_review + 完整 committed `origin/<base>...HEAD` review。
5. Publication DTO 丢失：fresh Architecture publication + live PR/Issue/payload ten-dimension review。
6. Current Publication `ready` 只进入现有 `guru-finalize-task`；Finalizer 内部及之后由原合同处理。

如 Phase 2 producer 目前只能保留 checkpoint、但无正式 rematerialization public entry，则在 `guru-check-task` 内增加只消费 current checkpoint/current content/current Architecture 的最小 recovery profile。它只能重新投影原 `passed` DTO，不重做或替代 semantic judgment；checkpoint不current时回 fresh check。

Branch Review 与 Publication 成功 checkpoint 会退休，因此新会话必须 fresh 重跑，不能增加 reader 恢复已退休结果。

## 5. D419-04 自然语言与副作用 continuation

Workflow continuation 明确规定：

- 无 current side-effect plan 且有 exact active task：自然语言“继续”或“确认继续”加载 continuation。
- 有唯一 current side-effect plan：“确认继续”只授权该 payload；executor 后 live verify，成功才返回正式 typed exit。
- Mapped transitions 自动继续，直到出现新副作用、真实选择或 stop。
- payload/target/authority 变化使旧确认失效，重新展示。
- 确认过程不进入 task、runtime、checkpoint、DTO、schema 或 archive。

SessionStart/UserPromptSubmit hooks 继续只提供 facts/breadcrumb；不让 hook/parser/runtime 输出 Guru route classification。

## 6. D419-05 ownership、canonical 与 projection

预期修改面：

- canonical/dogfood workflow 与 workflow README；
- continuation/recovery 直接涉及的 Guru Skill package contracts/runtime/schema/tests；
- Guru workflow integration/native tests；
- preset ownership/update/reapply validator 与 exact-candidate matrix tests；
- `.trellis/spec` canonical source、dogfood copy、public docs；
- task-owned Architecture contribution、必要 ADR、RDT contribution。

明确禁止修改：upstream-owned `trellis-start`、`trellis-continue`、official hooks、official platform entries、official agents、official `trellis-meta`。Preset overlay仍必须保持三项 additive `guru-finish-work` entries。

Canonical 先改 `trellis/**`，再运行 preset apply 同步 dogfood/selected-platform Guru-owned copies。任何 `.new/.bak` 必须逐项解决；不得把 sidecar 留作成功状态。

## 7. D419-06 native regression architecture

新增真实 workflow continuation integration fixture，覆盖：

- 六类 state 与 invalid state；
- planning partial/wording/Architecture/Approval/confirmation/activation recovery；
- Phase 2 adjacent/lost output；
- Task Commit stdout-loss recovery只执行一次；
- Branch Review/Publication adjacent direct consumption与跨会话 fresh rerun；
- natural-language与显式入口一致；
- side-effect failure不产生成功 exit；
- missing Guru preset依赖明确阻塞。

测试使用 canonical 或 installed workflow、真实临时 Git repo/task/mapping、正式 package wrappers。语义 owner 的 fresh judgment由测试外 AI gate证明；deterministic fixture只验证 I/O、恢复与副作用，不用预填 pass、fake checkpoint、关键词断言或手写 DTO冒充 end-to-end semantic success。

## 8. D419-07 exact-candidate 集成矩阵

扩展现有 compatibility matrix，以 immutable Fork checkout `43fffc170927c85d9f7fc106cc5a059e80d4530b` 运行：

1. clean target init/install Guru workflow + preset；
2. predecessor existing target 使用 candidate CLI 执行 dry-run 与唯一 preserve-mode update；
3. switch 到 native workflow，确认读取 upstream native continuation；
4. switch 回 local exact Guru candidate，确认读取 Guru continuation且无 cache/旧 route；
5. reapply preset，比较 upstream-owned start/continue/hooks/meta bytes 与 reapply 前完全相同；
6. 比较 Guru workflow continuation bytes与 canonical完全相同；
7. 运行 source/installed package、ownership、platform discovery、dogfood drift、mode与recursive sidecar检查；
8. 扫描并拒绝 `.new/.bak`、`__pycache__`、`.pyc`、`.pyo`。

Matrix 不再比较 predecessor 与 current 的内部 API 集合，也不声明 migration capability 或 removed-API
allowlist。Predecessor projection 只记录安装前 evidence identity；update、workflow switch 与 preset reapply
完成后，matrix 对 current canonical source 与 current installed runtime contract（extension/workflow/task-data）
执行 exact parity gate；repository-only Docs authority 继续由独立 snapshot/validator 验证，同时由
真实 update 行为、package validator、ownership validator 和 residue scan 证明迁移结果。

删除范围覆盖 current source、installed、dogfood、声明平台、active package tests 以及 promotion 后的
shared-current Architecture/RDT authority。不得把已退役 marker、旧 Issue fixture 名、专项 allowlist、兼容
reader 或 migration capability 留作“已删除证明”。Immutable superseded/history 只保留历史事实，不进入
current projection、validator、matrix comparator、安装合同或支持承诺。

Matrix 输出必须绑定 candidate full SHA，不接受 branch name、PR head、short SHA 或旧 result。

## 9. Architecture change contract

本任务为 `architecture_impact/target_native`，计划创建 `docs/architecture/contributions/419-active-task-continuation.md`。它记录 authority、before/target、owner、single-writer、compatibility exit、parallel scope、evidence 与 promotion；完整 DTO/route 技术正文只留在本 design。

本任务改变 active-task recovery authority 与 confirmation-to-transition 决策，计划新增 draft ADR `docs/architecture/adr/011-active-task-continuation-authority.md`。只有 independent committed full-diff review 通过并由 Architecture owner serialized promotion 后，才能成为 accepted/current；普通 task 不直接改 shared current。

## 10. Docs SSOT Plan

策略：`delta_first`。

- durable docs：canonical workflow/README、preset README、workflow/preset specs、Architecture/RDT contribution 与必要 ADR；
- evidence paths：package tests、workflow integration tests、compatibility matrix output、source/installed validators、dogfood drift、recursive sidecar/residue scans；
- task artifacts：`prd.md` / `design.md` / `implement.md` 只保留本任务需求、设计、执行与验证映射，不成为 shared authority；
- merge checkpoint：Phase 2 前收敛 durable docs，Branch Review 后按 expected-current serialized promotion，再对 promotion-created diff fresh 重跑 Phase 2/commit/review；
- follow-up：#410 重新冻结自己的 exact release candidate，本任务不提供跨 SHA release proof。

## 11. 替代方案与回滚

- 保留 status/artifact route table：形成双 authority，拒绝。
- 新增 global resolver/persistent stage state：跨 owner重建 semantic pass，拒绝。
- Guru preset patch upstream entries：违反 ownership，拒绝。
- 从缺失 checkpoint推断 pass：违反退休合同，拒绝。

回滚必须把 Guru continuation、producer recovery、integration tests、specs 与 durable docs 作为一个合同单元回退。不能只回退 workflow block 或只保留 recovery runtime；本任务不迁移用户数据。
