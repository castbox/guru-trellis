# #122 实现 `guru-create-task-commit` 闭环 Skill 并收敛 Task work commit SSOT

## 目标

把每一次 Trellis task work commit 收敛到公共闭环 Skill
`guru-create-task-commit`。Skill 必须在提交前绑定任务、Issue Scope Ledger、
planning approval、Phase 2 check、`HEAD`、完整 dirty snapshot、精确 stage
路径与候选消息，并在提交后验证真实 commit 的 parent、message bytes、path set
和未提交路径状态。

## 来源与已确认事实

- Primary issue：<https://github.com/castbox/guru-trellis/issues/122>。
- 关联合同 #92 已在 `check-commit-messages` 与
  `validate_commit_message()` 中实现中文 Conventional Commits parser/validator。
- 关联基础设施 #120 已建立 `trellis/skills/guru-team/` canonical root、
  registry/interface schema、typed-exit marker、managed-hash installer 和
  `check-skill-packages`。
- `main` 在任务创建时与 `origin/main` 同步到
  `6b9495a17dc953c7a54c105e39c23a786edcd8a7`。
- Trellis 官方 custom workflow 与 custom skills 文档确认：workflow marketplace
  安装 `.trellis/workflow.md`，外部 skill package 必须由 Guru Team preset 分发到
  平台 skill roots。

## 需求

### R1：公共 id 与迁移合同

- 新 active skill id 必须为 `guru-create-task-commit`。
- `guru-create-work-commit` 必须保持 `reserved`，其 reason 必须声明
  `guru-create-task-commit` 是正式替代入口。不得把已公开 reserved id 静默复用为
  不同语义。
- Skill、external exit、artifact schema 与 executor command 必须登记为 Guru Team
  公共 API；破坏性变更必须使用新 id 或提供迁移合同。

### R2：mandatory invocation 与重复进入

- Final Phase 2 check 通过后、任何 task work stage/commit 副作用前，canonical
  workflow 必须通过 unfenced `guru-skill-invoke` marker 显式调用
  `guru-create-task-commit`。
- Branch Review finding 引起非 metadata task work 后，流程必须返回实现和完整
  Phase 2 check，再次调用该 Skill。每次调用必须绑定新的 Phase 2 digest、
  pre-commit `HEAD` 与 dirty snapshot。
- Frontmatter auto-match 只能承担 standalone discovery，不能替代 mandatory marker。

### R3：entry preconditions

Skill workflow mode 与 standalone mode 必须执行同一组检查：

- task worktree boundary、task identity、task status；
- schema 1.2 planning approval 与 planning document freshness；
- passed `phase2-check.json`、recorded `HEAD`、dirty paths 与 checked artifact
  digests；
- `issue-scope-ledger.json.primary_issue`、base identity；
- staged、unstaged、untracked、delete、rename 的完整 Git snapshot；
- 每个 dirty path 的 diff 与 task scope；
- commit 副作用授权来源。

读取 dirty files 只产生事实，不产生提交授权。

### R4：AI candidate 与 task-local artifact

- AI 必须根据当前 diff、task docs、durable Docs SSOT、Phase 2 evidence 与 ledger
  选择 exact stage paths、type/scope、中文 subject、固定顺序 body 和
  `Refs #<primary_issue>`。
- 每次候选必须写入独立 task-local artifact：
  `task-commit-plans/<sequence>.json`。
- Artifact 必须绑定 task/base/pre-commit `HEAD`、evidence digests、完整 dirty
  classification、exact stage paths、message bytes digest、AI Review evidence、
  authorization、freshness 与 post-commit result。
- Artifact 只能记录 repo-relative path、digest 和结构化事实；不得记录 secret、
  文件正文、credential、签名 URL、客户数据或本机绝对路径。

### R5：path classification 与 stage 边界

每个 dirty path 必须且只能属于一个分类：

- `task-reviewed`：属于 task scope，并被 fresh Phase 2 evidence 覆盖；
- `unrelated-preserved`：不属于 task scope，必须保持原状态；
- `unreviewed-blocking`：属于或可能属于 task scope，但未被 Phase 2 覆盖；
- `ambiguous-blocking`：AI 无法完成可靠归类。

只有 `task-reviewed` 和本次 candidate artifact 能进入 exact stage paths。
Executor 不得使用 `git add -A` 或 `git add .`。任何未列入计划的 staged path 必须
阻塞提交，executor 不得自动 unstage、reset 或 stash 用户状态。

### R6：AI Review Gate 与 human confirmation

AI Review Gate 必须在提交副作用前检查 stage scope、message 语义、issue refs、
部署/升级/安全边界、unrelated preservation 与 evidence freshness。

消息候选本身不触发用户暂停。以下状态必须触发用户确认或 fail-closed stop：

- path 无法归类或与并行工作冲突；
- commit 副作用授权缺失；
- 操作涉及 amend、rebase、reset、force 或已发布历史；
- hook 计划或结果引入 artifact 外路径；
- task、issue、scope 或 evidence owner 存在语义冲突。

### R7：唯一 parser、candidate validator 与 exact executor

- 必须扩展现有 `check-commit-messages`，提供 candidate artifact mode。
- Candidate mode 必须调用现有 `validate_commit_message()`；不得新增第二套
  subject/body parser。
- 必须新增 deterministic `create-task-commit` executor。Executor 只能消费已通过
  AI Review 与 candidate validation 的 exact artifact，只 stage exact paths，使用
  exact message file 与 `git commit --cleanup=verbatim -F`，不得 push 或改写历史。
- Executor 必须在提交前再次验证 evidence、`HEAD`、snapshot、index 与 artifact
  freshness。

### R8：post-commit validation 与 typed exits

Post-commit validation 必须检查：

- new `HEAD` parent 必须与 artifact 的 pre-commit `HEAD` 一致；
- raw commit message bytes 必须与 candidate bytes 一致；
- committed path set 必须与 exact stage paths 一致；
- commit 通过统一 `validate_commit_message()`；
- `unrelated-preserved` path 状态未改变；
- hook 未引入未规划 commit path 或 dirty/staged drift；
- result status、commit SHA、message digest、path evidence 已回写 artifact。

Skill 每次只能返回一个 external exit：

- `committed`：唯一 consumer 是 Branch Review / finding closure flow；
- `revision-required`：唯一 consumer 是本 Skill re-entry；
- `blocked`：唯一 consumer 是 fail-closed stop。

Unknown、multiple 或 unmapped exit 必须阻塞。

### R9：SSOT 收敛

- Step-local 正文必须只存在于 canonical skill package 的 `references/`。
- Global workflow 只能保留 mandatory invocation、repeat condition、typed-exit
  consumer 与 fail-closed transition。
- Continue prompt、command、breadcrumb 与 platform launcher 只能加载 stable
  skill id 并消费 exit，不得复制 candidate、review、confirmation、executor 或
  postcondition 正文。
- Phase 2 必须移除 planned message 人工确认要求；Branch Review 必须移除 work
  commit 格式正文，只引用 durable contract 与统一 validator。

### R10：分发、安装、升级与测试

- Canonical package 必须由 production registry 激活，并由 preset 安装到
  `.trellis/guru-team/skills/`、shared root 与选中的 Codex/Cursor/Claude roots。
- Extension manifest、public API、managed assets、README 与 dogfood installed
  copies 必须同步。
- Contract tests 必须拒绝 workflow/platform entry 中的完整 subject/body 模板、
  直接 task work `git commit` 路径与第二套 parser。
- Clean throwaway 必须覆盖 skill discovery、初次 commit、finding-fix re-entry、
  `trellis update`、workflow reapply、preset reapply、source/installed validation、
  drift 与零 unresolved sidecar。
- Remote current-ref marketplace verification 必须在 reviewed content push 后由
  `trellis-finish-work` 生成；pending 证据不得满足 publish。

## 验收标准

- [ ] AC1：production registry 保留 `guru-create-work-commit` reserved tombstone，
  并激活 `guru-create-task-commit` 完整 package/interface/schema/test contract。
- [ ] AC2：canonical workflow 对 initial commit 与 finding-fix commit 都存在唯一
  mandatory invocation 和三条唯一 typed-exit mapping。
- [ ] AC3：standalone description 命中创建 task commit、提交 Phase 2 changes、
  提交 finding fix、创建 revision commit 四类表达。
- [ ] AC4：candidate validator 在 `base..HEAD` 空时仍校验 candidate；
  `checked_commits=[]` 不能冒充 candidate pass。
- [ ] AC5：stale planning/Phase 2/ledger/HEAD/snapshot/message digest、wrong issue、
  missing/wrong-order body section、placeholder、close keyword 全部返回非零。
- [ ] AC6：executor 只提交 exact stage paths；unrelated path 被发现、排除并保持
  原状态；unrelated staged content 阻塞且不被自动改写。
- [ ] AC7：post-commit parent/message/path/parser/preservation/result evidence 全部
  匹配真实 `HEAD`；hook extra path 使 exit 为 `blocked`。
- [ ] AC8：每次 finding-fix commit 使用新的 sequence artifact、fresh Phase 2、
  fresh `HEAD` 与 fresh snapshot；旧 artifact 不可复用。
- [ ] AC9：workflow、continue entries、Branch Review prose 不复制 step-local
  contract，contract tests 能发现回归。
- [ ] AC10：canonical/dogfood runtime、package、platform copies、manifest 与 README
  无漂移，source/installed validator 通过。
- [ ] AC11：unit tests、package tests、preset tests、local throwaway、dogfood drift、
  task validation、Git diff check 全部通过。
- [ ] AC12：remote feature-ref verifier 在 publish 前通过；若外部状态阻断，PR body
  与最终报告必须写明未覆盖项及风险。
- [ ] AC13：PR 只关闭 #122；#92、#120 只作 related，不使用 close keyword。
- [ ] AC14：公共 package、schema、example、manifest、日志和文档不包含 secret、
  客户数据、`.env`、签名 URL、本机绝对路径或 workspace journal。

## Docs 状态与影响

- docs state：`partial_docs`。
- 现有 durable docs 已定义公共 skill 基础设施与 commit message 合同，但没有
  `guru-create-task-commit` 的 active lifecycle、artifact、executor 与 re-entry
  contract。
- 同步策略和文件清单由 `design.md` 的 `Docs SSOT Plan` 独占定义。

## 范围外

- 不修改 Trellis upstream、全局 npm package 或 `node_modules`。
- 不接管 Trellis metadata commit、merge commit、push、PR、archive 或 publish。
- 不改变 Issue Scope Ledger 的 close/ref/followup 判断 owner。
- 不把 message 语义、stage scope、AI Review 或 route 判断写入 Python/shell。
- 不修改 #98、#115 及其子任务。
- 不关闭 #92、#120 或其它 issue。

## 阻塞问题

无。Issue #122、Trellis 官方文档、当前仓库代码、#92 和 #120 durable evidence 足以
进入实现。
