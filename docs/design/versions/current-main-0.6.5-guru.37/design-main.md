# Guru Team Trellis Extension 当前设计

版本：`current-main-0.6.5-guru.37`；状态：`active`；provenance：`code_recovered`，绑定 baseline `5c059f49…` + #260 compatibility task delta（精确 revision 为当前 Git HEAD）。

## 分层与 ownership

- `DES-001` Canonical：`trellis/workflows/guru-team/`、`trellis/skills/guru-team/`、`trellis/presets/guru-team/` 是可分发源头；`.trellis/**` 与 `.agents/.codex/.claude/.cursor` 是 installed/dogfood/platform 投影。
- `DES-002` Orchestration：global workflow 只声明 Phase、mandatory Skill id、typed exit consumer 和 stop；step-local Skill 声明 entry、semantic/deterministic profile、re-entry 与出口。
- `DES-003` Judgment/runtime：semantic Skill 由 AI 执行正向行为与 gate，runtime 只校验 owner-authored result；deterministic Skill 只有在全部 pass/route 均可机器判定时适用。
- `DES-004` Lifecycle：Phase 0 Intake -> Phase 1 Planning -> Phase 2 Execute/check -> Phase 3 commit/review/publication/finalize/merge。base reconciliation 可在稳定边界插入但不重放未变化语义。
- `DES-005` State：task planning 与 closeout archive 是 tracked history；短生命周期 gate/recovery 属于 gitignored owner-private runtime；Git/GitHub live facts按需重读。
- `DES-006` Distribution：manifest、registry、interfaces、schemas、workflow、preset inventory、overlay 和平台 copies 组成同一安装单元；installer 处理 managed hash、mode 与 `.new/.bak`。
- `DES-007` Repository SSOT：RDT 和 Architecture 分别拥有其语义；Bootstrap 依序调用 upstream spec bootstrap、两个 foundation owner、cross-review 与最小 projection。
- `DES-008` Evidence：static/unit/integration/throwaway/live/release 各自只证明对应层级，Issue owner 决定最小验证范围。
- `DES-009` History/cleanup：current task identity 来自 `task.json`、ignored workspace mapping、
  current checkout 与 live worktree facts；archive/`finish-summary.json` 是可查询历史，cleanup 只消费
  merge 后 exact branch/worktree/task reachability。
- `DES-010` Compatibility：公共 Skill/schema/exit/command、managed paths 与平台 routes 形成
  before/after inventory；update/upgrade 只能通过明确 migration/adapter 改变，不得静默删除能力。
- `DES-011` Provider recovery：Git/GitHub drift、base evolution、partial finalization 与重试状态由
  当前 owning Skill 的短生命周期 private state 恢复；unknown/stale/mismatch 进入唯一 typed route。
- `DES-012` Finalizer terminal authority：正常 closeout 已退休 gate/transaction/plan 后，只有调用方提供的精确 retired owner locator 可触发 terminal reconstruction。runtime 读取六文件 archive 中的 durable summary，绑定 active/archive task locator、branch review commit、archive cleanliness，并重新读取 local/remote/Ready PR/title/body/base/branch/issue scope；全部一致才投影 `ready_for_merge`。
- `DES-013` Verifier inventory：source validator 从 registry/interface 形成 active package ids、commands 与 complete package commands；Throwaway verifier 只比较 validator projection 与 installed projection，不维护数量常量。
- `DES-014` Matrix orchestration：compatibility runner 由独立 cell executor 与 compact aggregator 组成；每个 cell 使用隔离 repo、npm prefix 与 runtime root，并输出 platform/scenario/version、inventory、template hash、sidecar 与 installed smoke 结论。
- `DES-015` Platform derivation：canonical/installed manifest、ownership claims、overlay entries 与 registry destinations 交叉派生声明平台；`.agents` 是 shared projection，不是独立 platform，集合不一致即 fail closed。
- `DES-016` Capability comparison：before/after projection 按 `distribution`、`skill_api`、`workflow`、`task_data`、`docs_authority` 排序比较，只允许版本 binding 与已审查 migration mapping 差异。
- `DES-017` Official migration order：existing cell 先运行 official upgrade/update dry-run 与条件式 migrate，再 workflow preview/switch，最后 preset reapply、backup reconciliation、recursive sidecar 与 ownership/drift gate。
- `DES-018` A/B compatibility：A=`worktree/github_pr`，B=`current/none`，使用隔离 clone；验证两种 merge order、零 metadata intersection、同 owner Finish/provider/cleanup recovery 与 retained-ref reachability。真实 GitHub A proof与 deterministic local fixture 分开绑定。
- `DES-019` Platform script boundary：`preview-change-context-history.sh` 是 package-private validator wrapper；platform public projection只发布 `scripts/invoke.sh`，matrix显式证明 private wrapper 未泄漏。

## Public I/O 与 private state

- `CON-001`：21 个 active Skill 以 registry/interface 为 public graph，typed exit 必须有唯一 consumer 或 fail-closed stop。
- `CON-002`：public output 是最小 handoff DTO；不携带完整审查、Git 可推导事实、用户授权或 private digest。
- `CON-003`：producer output 到 consumer input 是显式、薄、可确定性验证的 projection；consumer 不理解 producer private artifact。
- `CON-004`：terminal projection 不把 durable archive 当作 live provider；archive 只提供已提交 identity，Git/GitHub current facts仍必须精确匹配，缺失 locator 或任何 drift 均 fail closed。

## Capability owner map

| Capability | Skill / route | External exits |
| --- | --- | --- |
| mode | `guru-select-workflow-mode` | `standard_intake`, `task_free`, `blocked` |
| base/context | `guru-sync-base`, `guru-discover-change-context` | `synced/skipped/blocked`; `context_ready/refresh_base/blocked` |
| clarification/wording/readiness | `guru-clarify-requirements`, `guru-review-contract-wording`, `guru-review-change-request` | interface-defined closed exits |
| workspace/planning | `guru-create-task-workspace`, `guru-approve-task-plan` | `created/refresh_review/blocked`; `approved/revision_required/clarify_scope/blocked` |
| normal-path qualification | `guru-qualify-normal-scenario` | `classified/scope_confirmation_required/mechanism_revision_required/blocked` |
| task-free | `guru-execute-task-free-change` | 7 closed exits incl. `completed`/`blocked` |
| execute/check/commit | `guru-check-task`, `guru-create-task-commit` | check 4 exits；commit 3 exits |
| base evolution | `guru-reconcile-task-base` | 6 exits incl. continuity/implementation/planning routes |
| review/publication | `guru-review-branch`, `guru-review-task-publication` | review 5 exits；publication 3 exits |
| finish/merge | `guru-finalize-task`, `guru-merge-task-pr` | finalizer 6 exits；merge 3 exits |
| installation verification | `guru-verify-extension-installation` | `verified`, `blocked`；standalone only |
| RDT authority | `guru-maintain-requirements-design-test-ssot` | `ssot_current/sync_required/revision_required/baseline_incomplete/blocked` |
| Architecture authority | `guru-maintain-architecture-baseline` | 7 baseline/conflict/fitness exits |
| Repository Bootstrap | `guru-bootstrap-repository-ssot` | `completed/baseline_incomplete/repair_required/blocked` |

完整 stable ids、schema ids、commands 与 exits 以 `trellis/skills/guru-team/registry.json`、各 package `interface.json`、`commands.json` 和 `trellis/guru-team-extension.json` 为准，本表不复制 schema 正文。

## 关键时序

```text
Issue/current request
  -> mode -> sync -> context -> clarify -> wording -> readiness -> workspace
  -> planning -> plan approval -> user plan pause -> implementation -> Phase 2
  -> semantic commit -> full branch review -> publication review
  -> finalization transaction -> Ready PR -> expected-head merge -> closure check
```

```text
existing_repository Bootstrap
  -> source analysis -> trellis-spec-bootstrap
  -> RDT bootstrap_foundation <-> Architecture bootstrap_foundation
  -> cross-SSOT review -> minimal .trellis/spec projection -> validation -> current
```

```text
install / update / upgrade
  -> 选择 immutable workflow source 或明确 latest/canary source
  -> official Trellis init/update/upgrade 与 workflow preview/switch
  -> Guru preset initial apply/reapply
  -> 校验 extension manifest、managed inventory、platform bytes/mode
  -> 解析全部 .new/.bak -> source/installed/dogfood drift gate
```

```text
compatibility matrix
  -> live inventory derives claude / codex / cursor
  -> each platform runs clean-0.6.15 and existing-0.6.5-to-0.6.15
  -> installed RDT / Architecture / Bootstrap profile evals
  -> exact capability comparison + zero unknown drift/sidecar
  -> A/B local lifecycle matrix + separately authorized real GitHub A route
```

```text
delivery / Finish / cleanup
  -> Phase 2 passed -> semantic task commit -> full branch review
  -> publication readiness -> Finalizer expected-head transaction
  -> push / non-draft PR / archive / finish-summary -> Ready
  -> expected-head merge -> Issue closure verification
  -> exact branch/worktree/task cleanup（仅在 retained ref/reachability 已证明后）
```

任一步出现 base/provider/content drift 时返回该 owning Skill 的 re-entry；已创建 commit/PR/archive
事实由当前 owner 恢复，不重复副作用，也不回到 Phase 0 猜测状态。

## 数据与恢复

Task index/history 查询来自 task/archive；finish-summary 是 compact closeout history。Provider/base 状态从 live Git/GitHub 恢复；stale/mismatch 返回 owning typed route。两个并行 task 只写各自 task/worktree/contribution，promotion 由唯一 shared authority owner 串行投影；普通恢复不创建 handoff、shared ledger 或授权记录。Compatibility evidence只向下游输出 source/version、Finish profile、archive locator、tracked-write、commit reachability 与结果边界，不输出完整日志、用户授权或临时仓库状态。
