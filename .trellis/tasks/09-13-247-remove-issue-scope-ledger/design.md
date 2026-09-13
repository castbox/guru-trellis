# Design

## Current Contract

唯一 current authority 为 live Issue #247 `2026-09-13-r24`。本设计只移除 ledger authority，
保持当前旧 lifecycle 的 producer/consumer、target/stop、成功、归档、关闭验证与恢复语义。

## Design Decision

采用 subtraction-first 的直接删除与同步 current consumer input。ledger 不是被替换成另一份
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
| publication/merge execution | Publication-reviewed PR payload + exact task/base/head identity | Finalizer 保留 push、PR create/update、archive、Ready 与 recovery，并向 Merge 投影 exact PR body SHA-256；Merge 验证 identity、readiness、expected-head、closure effect 和 declared exits |
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
3. **Publication / Finalizer / Merge**：删除 ledger loader、validator、binding 和 aggregate projection；
   Publication 继续判断本次 Issue effect，Finalizer 保留既有 preparation/push/PR/archive/Ready/recovery，
   Merge 保留 readiness/expected-head/confirmation、closure verification 与四个 declared exits。
4. **Finish / Restore / Cleanup**：只删除 ledger reader/fixture，保留现有 task/archive/Git/provider
   facts、current terminal 和 `phase2_reentry_required -> guru-restore-archived-task` 恢复链。
5. **Package contract surface**：删除只为 ledger 存在的 Skill Markdown、interface、consumer
   schema、eval/example JSON、DTO 字段、runtime/script、fixture/test、commands/manifest/registry
   registration；共享资产仅在存在其它 verified active consumer 时保留。
6. **Distribution surface**：先修改 canonical，再通过 preset apply 同步 dogfood 与 Shared、
   Codex、Claude、Cursor 投影；更新 installed inventory、verification、mode/byte 和 sidecar checks。
7. **Current docs authority**：创建 #247 task-owned RDT/Architecture contribution；independent
   committed review 通过后由 serialized owners 将其提升为唯一 active `.50`，并让 promotion-created
   diff重新进入 Phase 2、Task Commit 与 Branch Review。

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

Finalizer 承接已 reviewed PR payload 与 exact task/base/head identity，保留 current transaction 的
local preparation、push、PR create/update、official archive、Ready、handoff 和已声明 recovery，
并在 `ready_for_merge` 最小 handoff 中携带 exact reviewed body UTF-8 bytes 的 SHA-256。Merge 先对 live PR body 重算同一 identity；
body-only metadata drift 与 head/base/branch drift 一样在 mutation 前直接 fail closed；调用方必须重新
进入 fresh Publication/Finalizer，Merge 不新增 reprepare typed exit。identity 一致后，Merge 才基于
live PR body、policy、CI、review、mergeability 完成独立 readiness
review、expected-head 检查和本次确认，但不重新决定 Issue 是否应关闭，也不调用 Issue close API。
Merge 后重新读取 live Issue/PR facts验证 GitHub 自动效果；成功进入 current terminal，
`closure_mismatch` 保留精确 mismatch，task-content finding 继续携带 archived identity 进入 Restore。

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

选择 `dedicated_refactor_slice`：本 Issue 直接移除 ledger aggregate，并把必要输入改由现有 semantic
owner fresh 读取；旧 lifecycle 的业务行为、owner、edge、target/stop、archive/Ready/closure verification
和 Restore 语义保持不变。没有 remaining ledger compatibility reader，也不恢复 #305 target 大重构。

命中的设计原则：

- `concept-semantic-completeness`：reference、closure intent、closure result 各有独立语义与 owner。
- `cohesion-change-isolation`：owner 只交换最小 typed projection，不共享 task aggregate。
- `minimum-necessary-complexity`：直接删除，不增加 wrapper、fallback 或 graph scanner。
- `debt-one-way-convergence`：active legacy ledger 单向退出，legacy 文件仅 inert preservation。

本任务需要 task-owned Architecture contribution 与 ADR decision，因为它同时改变长期的
closure-intent owner、GitHub closing-keyword 执行边界、Merge result verification、GAP lifecycle 与
compatibility exit。该 candidate 已在 independent committed review 后由 serialized promotion 接受为
`ADR-009` 并进入唯一 active `.50`；不引入新 owner、旧 task migration 或兼容层。

## Failure And Recovery

- 缺少 current requirement/source/PR effect 时返回现有 semantic clarification/review route。
- mixed old/new package、残留 reader/writer/schema registration、平台投影不一致或 preservation
  变化均 fail closed。
- Finalizer 完成后、Merge 前的 live PR body 漂移必须在 merge mutation 前 fail closed；不得仅凭
  unchanged HEAD/base/head branch 接受漂移后的 closing effect。
- 已存在 PR/transaction、archive-month、post-archive Ready、lost-result 与 archived Restore 仍按现有
  declared contract 恢复，以 live PR/Git/task/archive identity 与当前 reviewed payload为准，不读取 ledger。
- 旧流程的提前归档、PR 冲突和多 Delivery 接续局限明确保留为后续 Issue，不冒充本 Issue 已修复。
- 不新增 retry、lock、并发协议、迁移状态机或第二 recovery owner。

## Rollback

发布前回滚为本 change set 的源码 revert。legacy 文件不由本任务修改，无数据恢复动作。发布后如需
回退，必须回退整个相容 package unit；不得单独恢复 reader 而不恢复全部旧合同，但本 Issue 不为该
未来回退保留兼容代码，也不提供旧 task migration。

## Maintainability

实施前后分别计算 active consumer inventory。任何 touched non-generated code file 超过 3000 行时，
先在本 Issue 内做与 ledger 删除直接相关的机械拆分或小型解耦；不得借机泛化重构。净增长必须按
production、test、generated/managed 和 docs 分类解释，兼容壳导致的增长不接受。
