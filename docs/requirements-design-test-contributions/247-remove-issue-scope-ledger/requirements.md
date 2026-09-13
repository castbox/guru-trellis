# #247 Issue Scope Ledger retirement Requirements contribution

本 contribution 绑定 live Issue #247 `2026-09-13-r24`、task planning、immutable predecessor
`current-main-0.6.5-guru.49` 与 reviewed serialized promotion。其稳定 ID 已合并到唯一 active
`current-main-0.6.5-guru.50`；本文件只保留 provenance，不是第二 current authority，不实施 #305
Evolution 大规模重构，也不建立旧 task migration 或 compatibility contract。

Promotion status：`reviewed_promoted`；Architecture inheritance：`current-main-0.6.5-guru.50` / accepted
`ADR-009`；current Requirements locator：
`docs/requirements/versions/current-main-0.6.5-guru.50/requirement-main.md`。

- `R247-01`：current active graph 必须移除 `issue-scope-ledger.json`、
  `guru-issue-scope-ledger-*` 和 `primary_issue` / Issue-array aggregate 的 writer、reader、
  precondition、schema registration 与 consumer。
- `R247-02`：失去唯一 ledger consumer 的 current Skill Markdown、interface/consumer schema、
  eval/example JSON、DTO 字段、runtime/script、fixture/test、manifest/registry 内容必须在同一
  change set 删除，不保留 nullable 壳、dead file、alias、adapter 或 dual-read/write。
- `R247-03`：task/workspace creation 只创建 official task/worktree/mapping identity，不写入、
  登记或恢复 ledger；Clarification/Readiness 不再投影 Issue aggregate。
- `R247-04`：Planning、qualification、Phase 2、Task Commit 与 Branch Review 直接读取 current
  requirement/planning/source/diff authority；Commit/Review 不从 `primary_issue` 推导引用或 scope。
- `R247-05`：Publication 是唯一关闭意图判断 owner。Issue-backed task 完整解决对应 Issue 时默认
  关闭；只有 live Issue 明确存在合并后仍待完成的验证、观测、发布或其它条件，或当前交付不完整时，
  才 remain-open/reference-only；no-external-work-item 不产生 Issue 引用或关闭效果。
- `R247-06`：默认分支 PR 的 closing keyword 只来自 Publication 已审查决定；非默认分支 PR 不宣称
  其 body 关键字会关闭 Issue，后续目标默认分支 Publication 基于届时 current authority fresh 判断。
  Finalizer 保留既有 preparation、push、PR create/update、official archive、Ready、handoff 与 recovery，
  并通过 `ready_for_merge` transition 投影 archive locator 和 exact reviewed body 的最小 SHA-256 identity；
  Merge 在 mutation 与 closing-scope 推导前校验 live body，不一致时直接 fail closed并由调用方重新进入
  fresh Publication/Finalizer。Finalizer/Merge 不重新决定关闭范围、不调用 Issue close API，Merge 不新增
  reprepare typed exit，只保留独立 readiness semantic review、expected-head、current confirmation 和 live
  post-merge Issue/PR verification。
- `R247-07`：Finalizer archive、Merge 四 exits、current terminal 与
  `phase2_reentry_required -> guru-restore-archived-task` 保持修改前语义；Finish、Restore、re-entry 与
  Cleanup 只消费各自 current task/archive/Git/provider facts，不读取 ledger。
- `R247-08`：preset/update 不拥有或主动触碰已存在的 legacy ledger 文件；active runtime不读取、
  解析或登记它。absent、present-A、present-B 不得改变 current task/runtime 结果。
- `R247-09`：旧 ledger-bound task、DTO、schema 与 invocation 不迁移或 backfill；不提供 conversion、
  ledger compatibility reader 或 fixture。该边界不删除新 ledger-free 流程既有的 archived Restore、
  existing-PR、lost-result 或 reprepare recovery。
- `R247-10`：canonical、dogfood、installed、Shared、Codex、Claude、Cursor 与 preset
  apply/reapply/update 投影必须一致；声明 `guru-ledger-free-runtime@1.0.0` 并严格绑定 current projection
  identity；本 Issue 不改变现有 Skill id、owner、typed route、四阶段顺序，不修改 Trellis upstream、
  global npm、`node_modules`、业务仓库或完整 Release matrix。提前归档、PR 冲突和多 PR 接续局限保持
  已知问题，不宣称已解决。

`BEH-019`：在相同 current task、Git、external authority 和 reviewed PR effect 下，ledger absent、
present-A 与 present-B 的 current lifecycle 结果一致；present 文件不被 active runtime打开，且
preset/update 因不拥有该路径而不主动触碰。

`BEH-020`：Issue-backed completed、Issue-backed remain-open 与 no-Issue 三条 Publication 判断路径
分别产生默认关闭决定、有 current-authority 原因的保持 open 决定和无 Issue 引用；默认/非默认分支
分别由当前或后续目标默认分支 PR 的 closing keyword 交给 GitHub 自动执行，均不依赖 task-local aggregate。
