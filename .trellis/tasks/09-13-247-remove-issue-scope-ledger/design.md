# Design

## Design Decision

采用 subtraction-first 的直接删除与同步 consumer migration。ledger 不是被替换成另一份
task context，而是从 current graph 中完全退出。各 owner 直接读取其职责所需的 current
authority 和 live facts，并只向唯一 consumer 投影不可重新推导的最小数据。

不保留 compatibility reader、schema alias、旧 DTO optional 字段、双读/双写、隐藏 cache、
journal 或聚合 closure frame。legacy ledger 文件本身不参与 active graph；安装/更新不得
主动删除或改写它，但不为旧 task 建立识别、迁移、恢复或继续运行能力。

## Authority And Owner Boundaries

| Concern | Current source after #247 | Owner behavior |
| --- | --- | --- |
| task identity/status/branch/worktree | official `task.json`、current checkout、live `git worktree`、ignored mapping | Workspace/Finish/Restore/Cleanup 只验证自己的 current identity |
| requirement/scope/source reference | live external authority、Phase 0 reviewed authority、current planning provenance | Clarification/Planning/Check/Review fresh reread，不持久化 aggregate |
| commit reference | current task/source/requirement authority | Commit owner fresh 生成，不读取 `primary_issue` |
| reviewed PR reference/closure decision | current requirement authority、reviewed diff、target/default branch、live Issue/PR facts | Publication 唯一判断 issue-backed completed/remain-open/no-item；completed 默认关闭 |
| publication/merge execution | Publication-reviewed PR payload + exact task/base/head identity | Finalizer 绑定发布事务；Merge 独立检查 readiness、expected-head 并确认本次 merge，不重判关闭决定 |
| actual closure action/result | 进入默认分支的 GitHub closing keyword + merge 后 live Issue/PR facts | GitHub 自动执行关闭；Merge/closeout 只验证结果，不调用 Issue close API |
| task completion/resource state | official Finish/task/archive/Git/provider facts | Finish/Restore/Cleanup 不读取 Issue 分类 |

`close_issues`、`primary_issue` 这类同名字段按 provenance 处理：作为 ledger aggregate 或跨阶段
authority 传递的字段删除。Publication 的 current reviewed closure decision 只属于 PR payload
审查；Finalizer/Merge 不获得新的关闭判断权，也不沿用 ledger 名称、语义或完整数组分类。

## Active Asset Retirement

实施时从 fresh `origin/main` inventory 建立 current active set，并按以下类别处理：

1. **Workspace creation**：删除 ledger authoring、plan/result artifact declaration、writer、
   checker、schema、example 和恢复分支；creation output 只保留 official task identity 及
   现有唯一 consumer 必需字段。
2. **Intake / Planning / Qualification / Check / Commit / Review**：删除 ledger path、
   precondition、`scope_ledger_path`、`primary_issue` 和 Issue-array aggregate 输入；各 semantic
   owner直接重读 current requirement/planning/source authority。
3. **Publication / Finalizer / Merge**：删除 ledger loader、validator、binding、hash、recovery
   和 closeout projection；Publication 唯一判断 Issue 是否应关闭并形成 PR payload，Finalizer
   只绑定发布事务，Merge 只完成 readiness/expected-head/confirmation 和 live closure verification。
4. **Finish / Restore / Cleanup**：删除任何由 ledger 决定完成、恢复、清理或 release route 的
   reader/fixture，改用现有 task/archive/Git/provider facts。
5. **Package contract surface**：删除只为 ledger 存在的 Skill Markdown、interface、consumer
   schema、eval/example JSON、DTO 字段、runtime/script、fixture/test、commands/manifest/registry
   registration；共享资产仅在存在其它 verified active consumer 时保留。
6. **Distribution surface**：先修改 canonical，再通过 preset apply 同步 dogfood 与 Shared、
   Codex、Claude、Cursor 投影；更新 installed inventory、verification、mode/byte 和 sidecar checks。
7. **Current docs authority**：创建 #247 task-owned RDT/Architecture contribution；更新 current
   contract 的候选只在 serialized promotion 后生效。

历史 archive、ADR、superseded/released RDT、旧 release evidence 和当前 task 创建时已经生成的
`issue-scope-ledger.json` 都不作为 active match-zero 检查的删除目标；它们不被迁移、解析或作为
新 runtime 输入。preset/update 不主动触碰已有 ledger 文件。

## Data Flow

### Task Creation

Readiness 到 Workspace 的 public transition 只携带创建当前 task/workspace 所需的 reviewed
identity，不携带 Issue 分类 aggregate。Workspace executor 创建 official task/worktree/mapping，
不写 ledger；checker 只验证这些 current facts。

### Planning Through Branch Review

Planning、qualification、Phase 2 和 Branch Review 直接读取 live Issue contract、task planning、
current code/test 与 exact diff。Commit owner从 task/source authority fresh 形成 message reference；
不存在 external work item 时不制造 Issue number。

### Publication Through Merge

Publication 读取 current requirement authority、完整 reviewed diff、current validation、目标
base/default branch 与 live Issue/PR facts，唯一判断 Issue 关闭意图并形成精确 PR payload。
Issue-backed task完整解决对应 Issue 时默认关闭；只有 live authority 中存在合并后仍待完成的
验证、观测、发布或其它条件，或当前交付不完整时，才形成带具体原因的 remain-open/reference-only。

目标为默认分支时，Publication 在 PR body 写入 closing keyword，GitHub 在 merge 后自动关闭。
目标为非默认分支时，当前 PR body 不承诺关闭效果，只引用 Issue；该 base 分支后续进入默认分支时，
由后续 Publication 基于届时 current authority fresh 判断并在目标默认分支 PR 编码 closing keyword。

Finalizer 仅承接已 reviewed PR payload 与 exact task/base/head identity。Merge 基于 live PR body、policy、
CI、review、mergeability 完成独立 readiness review、expected-head 检查和本次确认，但不重新决定
Issue 是否应关闭，也不调用 Issue close API。Merge 后重新读取 live Issue/PR facts验证 GitHub 自动效果。

source reference 与 closure decision 始终分离；reference-only 必须有 current-authority 原因，
非默认分支的技术性延迟关闭也不得被误报为当前 PR 已产生关闭效果。

## Legacy Non-Migration Boundary

- update/reapply 不枚举或迁移旧 task，也不为 ledger 建立专用 migration manifest/state。
- active runtime、validator、recovery 和 semantic owner 不打开或解析该文件。
- absent、present-A、present-B 不得改变 current task/runtime 的 typed result 或副作用计划；
  present 文件只是 preset/update 不拥有、不主动触碰的本地历史文件。
- 旧 task、旧 DTO、旧 schema 和旧 invocation 可直接被 current-only contract 拒绝；不提供转换、
  re-entry 或兼容 fixture。
- current lifecycle 的 authority不足仍返回其既有 semantic owner，但不得从 legacy 内容补全意图。

## Architecture Path

选择 `dedicated_refactor_slice`：本 Issue 在保持 Skill id、owner 和 lifecycle 行为边界不变的前提下，
移除跨 owner 的 legacy aggregate authority，并把现有 consumer 同步迁移到 owner-native current facts。
这是单一主写、可验证的小切片，不是 `legacy_boundary_convergence`，因为没有兼容层或 remaining
runtime legacy boundary；也不是 #305 target 大重构。

命中的设计原则：

- `concept-semantic-completeness`：reference、closure intent、closure result 各有独立语义与 owner。
- `cohesion-change-isolation`：owner 只交换最小 typed projection，不共享 task aggregate。
- `minimum-necessary-complexity`：直接删除，不增加 wrapper、fallback 或 graph scanner。
- `debt-one-way-convergence`：active legacy ledger 单向退出，legacy 文件仅 inert preservation。

需要 task-owned Architecture contribution，因为 current integration/distribution 与 task identity
authority 明确提到 ledger，且本任务改变这些 current architecture facts。无需 ADR：不引入新的
长期架构选择，只执行 current constitution 已要求的局部技术债收敛。

## Failure And Recovery

- 缺少 current requirement/source/PR effect 时返回现有 semantic clarification/review route。
- mixed old/new package、残留 reader/writer/schema registration、平台投影不一致或 preservation
  变化均 fail closed。
- 已存在 PR/transaction 的恢复仍以 live PR/Git/task identity 与当前 reviewed payload为准，不读取 ledger。
- 不新增 retry、lock、并发协议、迁移状态机或第二 recovery owner。

## Rollback

发布前回滚为本 change set 的源码 revert。legacy 文件不由本任务修改，无数据恢复动作。发布后如需
回退，必须回退整个相容 package unit；不得单独恢复 reader 而不恢复全部旧合同，但本 Issue 不为该
未来回退保留兼容代码，也不提供旧 task migration。

## Maintainability

实施前后分别计算 active consumer inventory。任何 touched non-generated code file 超过 3000 行时，
先在本 Issue 内做与 ledger 删除直接相关的机械拆分或小型解耦；不得借机泛化重构。净增长必须按
production、test、generated/managed 和 docs 分类解释，兼容壳导致的增长不接受。
