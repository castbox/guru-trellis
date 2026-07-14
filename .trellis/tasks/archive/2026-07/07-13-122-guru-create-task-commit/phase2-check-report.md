# #122 阶段二独立检查报告

## 结论

Replacement 阶段二检查代理 `trellis_check_122_replacement` 已按
`ssot_first` 策略完成完整未提交实现检查。前任代理报告的 4 个 finding 均已独立
复核并闭环；replacement 新发现 1 个 candidate index freshness finding，已完成小型
范围内修复、canonical/dogfood 同步和回归验证。当前开放 finding 为 0，本报告足以
支持主会话后续记录 `phase2-check.json`。

本报告不替代 `phase2-check.json`、task work commit、Branch Review Gate 或
`trellis-finish-work`。本检查未执行 recorder、commit、push、PR 或 Branch Review。

## 检查身份与边界

- 技术身份：`trellis_check_122_replacement`。
- 逻辑角色：`阶段二检查代理`。
- Active task：`.trellis/tasks/07-13-122-guru-create-task-commit`。
- 审查 HEAD：`6b9495a17dc953c7a54c105e39c23a786edcd8a7`。
- 分支：`feat/122-guru-create-task-commit`。
- workspace boundary：通过；actual repo root 与 task worktree 一致，source checkout
  无改动，未发现 suspicious source artifact。
- planning approval：schema 1.2、`explicit-post-planning-review`、ambiguity review、
  fixed scanner 与三份 planning digest 均通过。
- 前任 `trellis_check_122` 在 `evt-0018-6d2199a1bd` 被判定 stale，并由
  `evt-0019-5e86492b1c` 记录 `terminated-unfinished`；其 partial output 未作为通过
  证据。本代理从 task artifacts、specs、完整 diff 与命令结果独立复核。

## 审查输入

- 需求与规划：`prd.md`、`design.md`、`implement.md`。
- 实现证据：`implementation-handoff.md`、`issue-scope-ledger.json`、
  `agent-assignment.json`。
- Docs SSOT Plan：`design.md` 第 14 节，strategy=`ssot_first`。
- `check.jsonl` 只有模板条目，因此未把它当成 spec manifest；改为读取 docs、preset、
  workflow 三层 index 与本次修改的全部 8 个 spec 正文。
- 官方 Trellis 文档：`index.md`、`advanced/custom-workflow.md`、
  `advanced/custom-skills.md`、`advanced/custom-spec-template-marketplace.md`；当前实现
  符合 workflow Markdown 控制流程、skill 为扩展点、平台目录分发和 template/public
  state 边界。
- 完整未提交 diff：durable docs、canonical workflow、active skill package、registry、
  schema、runtime、wrapper、preset installer、platform overlay、dogfood installed copy、
  extension manifest、throwaway verifier 与 tests。

## Finding 生命周期

### F-01 已修复：executor 使用被禁止的 broad add

- Severity：P1。
- 原问题：task executor 使用 `git add -A`，违反 R5、R7 与仓库确定性 executor
  边界。
- 独立复核：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:10082`
  现在只执行 `git --literal-pathspecs add -- <exact paths>`；没有 reset、stash、
  unstage、push 或 history rewrite。
- 回归证据：reviewed add/delete/rename、Unicode、空格、pathspec metachar、unrelated
  staged blocking 与真实 throwaway commit 均通过。

### F-02 已修复：非 NUL path 解析损坏 Unicode/raw path

- Severity：P1。
- 原问题：porcelain/name-only 的换行解析和 `.strip()` 会破坏 Unicode 或特殊字符
  路径事实。
- 独立复核：`guru_team_trellis.py:9676` 的 snapshot 使用
  `git status --porcelain=v1 -z --untracked-files=all` 并按 NUL record 解码；
  `git_nul_path_set()` 对 index/commit path query 同样使用 NUL 集合；rename source 与
  destination 被保留，postcondition 用 `--no-renames` 比较 add/delete path set。
- 回归证据：`test_exact_executor_commits_only_reviewed_paths_and_preserves_unrelated`
  和 `test_exact_executor_preserves_rename_source_and_destination` 通过。

### F-03 已修复：sequence/history freshness 不完整

- Severity：P1。
- 原问题：plan sequence 未强制 next-unused，candidate path 可能已存在于
  pre-commit `HEAD`，导致旧 artifact 复用或覆盖历史。
- 独立复核：`guru_team_trellis.py:9784` 强制从 `001` 开始的 next-unused contiguous
  sequence，并通过 literal `git ls-tree HEAD -- <candidate>` 拒绝 HEAD 已存在路径。
- 回归证据：`test_sequence_must_be_next_unused`、
  `test_old_plan_cannot_be_reused_after_first_commit` 以及 throwaway old-plan reject 通过。

### F-04 已修复：exact staging 失败未回写 blocked evidence

- Severity：P2。
- 原问题：unexpected staged path 或 exact stage/index 前置失败可能只返回异常，不把
  typed-exit evidence 回写 plan。
- 独立复核：`guru_team_trellis.py:10038` 对 artifact 外 staged path 先回写
  `blocked`；`guru_team_trellis.py:10193` 对 stage/index/commit 前置异常统一回写
  `blocked`；post-commit failure 在 `guru_team_trellis.py:10152` 回写 commit、parent、
  message digest、committed paths、unrelated preservation、hook mutation 与 errors。
- 回归证据：unrelated staged 与 hook extra path tests 均验证 `result.status/exit` 为
  `blocked` 且不自动改写 Git 现场。

### F-05 已修复：已 staged 的 candidate 可能提交旧 plan bytes

- Severity：P1。
- 发现者：replacement 阶段二检查代理。
- 原问题：candidate self path 为避免 recursive digest 被 snapshot 排除；如果 plan 先
  stage、再由 AI 更新 working-tree plan，executor 只比较 staged path set，可能提交旧
  index bytes，破坏 AI review/authorization/freshness 绑定。
- 修复：`guru_team_trellis.py:10077` 无条件把 validated candidate self path 加入
  exact restage 集合，保证 commit tree 包含当前已验证的 `planned` bytes。
- 回归：`test_guru_team_trellis.py:532` 新增
  `test_exact_executor_restages_current_candidate_bytes`，先 stage 旧 plan、再修改 review
  与 digest，验证 commit 中是最新 plan 且 result 仍为预期的 pre-commit `planned`。
- 同步：canonical runtime 修改后通过 preset apply 同步 dogfood runtime；二次 apply
  为 `updated_managed=[]`、`managed_backups=[]`。

## R1-R10 与 AC1-AC14

| 范围 | 独立复核结论 |
| --- | --- |
| R1 / AC1 | production registry 保留 reserved `guru-create-work-commit` tombstone，并激活 `guru-create-task-commit`；manifest 版本为 `0.6.5-guru.5`，CLI baseline 仍为 `0.6.5`。 |
| R2 / AC2 / AC8 | canonical/dogfood workflow 各只有 1 个 unfenced mandatory invoke 与 3 个唯一 exit consumer；finding fix 返回完整 Phase 2 并使用 fresh sequence/HEAD/snapshot。 |
| R3-R4 / AC3-AC5 | workflow/standalone precondition 集合一致；plan 绑定 task、ledger、planning、Phase 2、HEAD、snapshot、message、AI review、authorization、result；candidate mode 在空 commit range 下仍调用共享 parser。 |
| R5-R8 / AC6-AC8 | 四类 path 全覆盖；literal exact staging、unrelated preservation、NUL/rename/pathspec、sequence/history、parent/raw message/path/parser/hook/result postcondition 均有正负测试。 |
| R9 / AC9 | step-local 正文只在 canonical package `references/contract.md`；workflow 与五个平台 continue entry 只做 stable id invocation/typed-exit route，contract scan 阻止 direct task work commit 与正文复制回流。 |
| R10 / AC10-AC11 | canonical/shared/Codex/Cursor/Claude/dogfood package、runtime、manifest、README 与 installer 同步；source/installed validator、preset idempotence、drift、full tests、throwaway/update/reapply 全部通过。 |
| AC12 | local throwaway 完成；remote current feature-ref marketplace verifier 依合同必须等 reviewed content push 后由 `trellis-finish-work` 生成，当前 pending 不被误报为通过。 |
| AC13 | ledger 只把 #122 放入 `close_issues`；#92、#120 仅为 `related_issues`，candidate contract 使用 `Refs #122`，无 close keyword。 |
| AC14 | public package/schema/example/manifest/docs 未发现 secret、客户数据、`.env` 内容、签名 URL 或机器绝对路径；测试中的 fake token/path 只用于负向安全扫描。 |

## Docs SSOT

- `ssot_first` 已执行：design 第 14 节列出的 14 个 durable evidence path 全部存在
  语义修改，没有遗漏的 no-change evidence path。
- Requirements/flow 定义 active lifecycle、artifact、AI review/exact executor、typed
  exits 与 finding-fix re-entry；workflow/preset/docs specs 分别拥有 global route、skill
  package、companion script/data contract、installer/overlay 与 public docs 规则。
- Durable docs、task artifacts、canonical workflow、runtime、schema、tests、installer、
  manifest 与 installed copies 对 active/reserved id、sequence、candidate self exception、
  exact staging、postcondition 和 upgrade/reapply 语义一致。
- Task-history-only 内容仍只位于 task artifacts；公共 package 未携带 active task、
  workspace journal、单次 command output 或本机临时路径。

## 验证结果

- Workspace boundary：通过；source checkout status 为空。
- Planning approval validator：通过，approved/reviewed HEAD 均为当前 pre-commit HEAD。
- Targeted executor suite：11 tests，5.206s，`OK`。
- Full package/runtime/preset suite：489 tests，128.868s，`OK`。
- Canonical package self-test：3 tests，`OK`。
- Source validator：reserved=1、active=1、invoke=1、exit=3，`passed`。
- Installed validator：selected platforms=Claude/Codex/Cursor、managed files=43、
  sidecar/removal/conflict=0，`passed`。
- Preset apply：首次同步 replacement delta 只更新 dogfood runtime并生成 1 个已核对
  `.bak`；清理后第二次 apply 幂等，无 update/backup/new/conflict。
- Dogfood overlay drift：通过；canonical/dogfood workflow、runtime、registry 与 wrapper
  hash/bytes 一致。
- Full clean throwaway：通过公开 marketplace discovery 后覆盖当前本地 unpublished
  canonical workflow sample；初次 commit、fresh finding-fix revision commit、old plan
  reject、unrelated preservation、`trellis update --force`、workflow preview/switch、
  preset reapply、source/installed validation、closeout smoke 和最终 sidecar scan均通过。
- Static gates：`bash -n`、`py_compile`、changed JSON parse、task validate、phase
  2.2/3.4/3.5 context parse、`git diff --check`、wrapper executable mode、recursive
  `.new/.bak` scan与安全扫描均通过。
- TypeCheck：不适用；本仓库本次变更没有独立静态类型检查器，Python compile 与完整
  unittest 已覆盖语法和行为。
- Lint：项目无独立 lint 命令；`git diff --check`、Bash syntax、JSON parse 与 tests
  通过。

## 部署、安全与兼容性

- 未修改 GitHub Actions、Dockerfile/Compose、Kubernetes/Kustomize、数据库
  migration、Makefile、应用 service、worker、queue 或 runtime config；无需应用部署或
  数据迁移。
- 变更影响 Trellis workflow/preset 安装与 task work Git commit executor；upgrade
  风险已通过 clean install、`trellis update`、workflow/preset reapply、managed hash、
  drift 与 sidecar scan覆盖。
- Executor 不 push、不 amend/rebase/reset/force/stash；message temp file 权限 `0600`
  且在 `finally` 删除；失败保留 Git 现场。
- 当前 CLI compatibility target 为已批准的 `0.6.5`。本机观察到更新版本不扩大本
  issue 的兼容范围，后续 baseline 升级需单独评估。

## Dirty Paths

写报告前，NUL-delimited `git status --porcelain=v1 -z --untracked-files=all
--no-renames` 记录 98 个 dirty path；本报告新增后为 99 个。范围如下：

- 11 个既有 task-local planning/approval/liveness/handoff artifact，加本报告 1 个；
- 8 个 canonical `guru-create-task-commit` package 文件；
- installed canonical、shared、Codex、Cursor、Claude 各 8 个 package 文件；
- canonical 与 dogfood runtime/wrapper/registry/workflow/manifest；
- 五个平台 continue overlay 与 dogfood copies；
- 14 个 Docs SSOT evidence path；
- preset installer、throwaway verifier与 package/runtime/preset tests。

未发现 task 范围外 dirty path、staged path、`.new/.bak`、workspace journal、runtime
cache、secret 或 source checkout artifact。完整精确 dirty path 集应由主会话在记录
`phase2-check.json` 时从当前 NUL-delimited Git 状态获取；报告新增后必须使用 fresh
状态，不能复用写报告前的 98-path snapshot。

## 最终判断

- 已检查：R1-R10、AC1-AC14、Docs SSOT、canonical/dogfood/overlay/manifest/installer、
  workflow/runtime/schema/package/tests、AI-vs-script boundary、candidate freshness、
  rename/path/message/executor/postcondition、upgrade/reapply/throwaway、安全与部署影响。
- Findings：5 个，均已修复并复核；开放 0 个。
- Phase 2：`PASS`。本报告可以支撑主会话记录 fresh `phase2-check.json`；记录后仍需
  由 `guru-create-task-commit` 获得独立 commit side-effect authorization，之后才可
  执行 task work commit 与独立 Branch Review Gate。
