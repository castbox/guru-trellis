# Issue #97 Branch Review Gate 替换问题发现审查报告

## 审查身份

- 技术身份：`/root/issue97_branch_finding_replacement`
- 逻辑角色：`问题发现审查代理`
- 平台显示名：`issue97_branch_finding_replacement`
- 审查模式：独立替换审查，review-only
- 审查结论：`FAIL`
- Findings：P0=0，P1=0，P2=4，P3=1，共 5 项

## 替换链

- 前任技术身份：`/root/issue97_branch_finding`
- 前任 stale evidence：`evt-0041-987e0ccea6`，事件为 `stale-assessed`
- 前任 unfinished evidence：`evt-0042-cf2b0928e1`，事件为 `terminated-unfinished`
- 替换派发：`evt-0043-d769f85a29`
- 替换开始：`evt-0044-d582a01916`
- 替换原因：`max_progress_silence_exceeded`
- 前任在 cutover 后写入的 `reviews/round-001-finding.md` 仅标记为 stale partial；本报告未使用该文件的内容、证据或结论，所有 finding 均从固定 HEAD、live issue、durable docs、task artifacts、代码和测试重新取证。

## 固定审查范围

- Repository：`castbox/guru-trellis`
- Worktree：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/097-finish-summary-replaces-add-session`
- Base：`origin/main`，SHA `ff8c03abb259c2a048626ea72e0bf57138db2c14`
- Reviewed HEAD：`53f265f3949ca8374c7b534da309a4c924325450`
- Diff range：`origin/main...HEAD`
- Commit subject：`feat(workflow): #97 用任务完成摘要替代工作区日志`
- 完整 diff：45 个文件，5396 insertions，2094 deletions；包含 workflow、companion、schema、preset、overlay、dogfood copy、durable docs、task planning artifacts、测试、配置/ignore，以及 3 个 tracked workspace 文件删除。
- 审查时 working tree 只有 task-local 未跟踪 Trellis metadata；未发现 reviewed HEAD 之后的 source、workflow、schema、preset、docs、test、deployment 或 Makefile 漂移。

## 问题清单

### P2 - Guru Team 启动与会话注入仍读取 workspace journal，违反 context non-read 合同

- 路径与行号：`.agents/skills/trellis-start/SKILL.md:17`、`.trellis/scripts/common/session_context.py:437`、`.trellis/scripts/common/session_context.py:621`、`.codex/hooks/session-start.py:409`、`.cursor/hooks/session-start.py:652`
- 证据：Guru Team `trellis-start` 仍要求运行默认 `get_context.py`。默认 context 在 `get_context_json()` 中调用 `get_active_journal_file()`，读取 journal 全文计算行数并把 journal path/line count 写入 context；文本模式也输出 `JOURNAL FILE` 和 workspace path。Codex/Cursor session-start hook 同样调用 `get_active_journal_file()` 与 `count_lines()`，把结果注入启动上下文。
- 合同冲突：live #97 与 `trellis/workflows/guru-team/workflow.md:221-224` 明确声明 Guru Team 不把 `.trellis/workspace/**` 用作 finish/readiness/context evidence。ignore 与停止 `add_session.py` 只消除了 Git 写入和 finish 写入，不能阻止已有本机 journal 被启动/上下文路径读取。
- 影响：安装或升级后只要 upstream init、旧版本或人工保留了 ignored journal，Guru Team AI 上下文仍会受 workspace journal 的存在、路径和内容行数影响；“不读取 context evidence”的验收未完成，README/PR body 的 no-read 声明不真实。
- 建议修复：通过 canonical Guru Team workflow/overlay 增加不读取 workspace 的 context 路径或安全模式，并让 shared start、Codex/Cursor hook 使用该路径；不要修改 Trellis upstream/global npm。增加 fresh install sentinel 测试，放置 workspace journal 后证明 Guru Team 启动/上下文输出不打开、不枚举、不输出该文件。

### P2 - Recovery 未把 repo/base/head/title/body/draft 绑定到失败时的同一发布输入

- 路径与行号：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:8527`、`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:8870`、`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:8938`
- 证据：`publish_recovery_command()` 只把 `args.title`、body 文件/ready artifact 路径和显式 draft flag 带回命令；normal finish 常见的默认 title/draft 不会写入命令。每次 `cmd_publish_pr()` 又从当前 task/config 和当前 body 文件重新解析 title、draft、body。`publish_inputs` 只是本次错误 JSON payload 中的快照，没有持久化、digest 或 recovery 输入校验，recovery command 也不引用该快照。
- 可复现场景：normal `gh pr create` 失败后，修改 archived `pr-body.md`，或修改 task title / publish draft config，再执行原样 recovery command。task metadata dirty 被允许，新的 body 只要仍满足结构校验即可进入 0-open 分支并用不同输入创建 PR；当前测试只断言错误 payload 含 `publish_inputs`，没有跨调用修改输入并要求 fail closed。
- 合同冲突：live #97、PRD R4 与 durable workflow 要求 recovery 使用同一 repo/base/head/title/body/draft。当前实现保证了错误可观察性，但没有保证下一次执行的输入同一性。
- 影响：恢复可能创建内容、标题或 draft 状态与 AI 审查/首次 publish 不同的 PR，破坏幂等性和发布 readiness 证据链。
- 建议修复：将失败时的发布输入或其不可变 digest 写入 task-local recovery artifact，并让 recovery command 只引用且验证该 artifact；至少绑定 exact title、body bytes/hash、draft、repo、base、head 与 reviewed source。补充跨调用 mutation tests，分别修改 body、title、draft 后必须在 PR query/create 前 fail closed。

### P2 - Git path snapshot 失败直接中止，未实现 live #97 的空 paths 加原因合同

- 路径与行号：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:713`、`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:715`、`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:725`
- 证据：`finish_summary_git_path_snapshot()` 在 `git diff --name-only -z` 或 initial snapshot 的 `git ls-files --others` 返回非零时直接抛出 `WorkflowError`。builder/final rewrite 没有回退为 `git.changed_paths=[]`、`index.search_terms.paths=[]`，也没有追加说明 diff 计算失败原因的 `contract_changes[]`。
- 合同冲突：live #97 字段规则明确要求“无法计算 diff 时必须写入空数组 `[]` 并在 `index.contract_changes[]` 中记录原因”。批准后的 PRD/design 未承接该分支，测试也只有 all-protected/mixed/no-filter，没有 diff-command failure fixture。
- 影响：Git ref 暂时不可解析、shallow/remote ref 缺失或 Git 命令失败时，finish/publish 行为与公开 schema 产品合同不一致；任务无法形成要求的降级摘要。
- 建议修复：把 snapshot 命令失败转换为 deterministic 空安全集合和不泄露路径的原因 contract fact，同时保持 schema/path validator fail closed；为 initial `git diff`、initial `ls-files`、final/recovery `git diff` 分别增加失败测试，并验证两个 path 数组相等且 retrieval_text 重新派生。

### P2 - Durable 全流程文档仍把 Guru Team finish 描述为 add_session/workspace journal

- 路径与行号：`docs/requirements/guru-team-trellis-flow.md:18`、`docs/requirements/guru-team-trellis-flow.md:77`、`docs/requirements/guru-team-trellis-flow.md:353`、`docs/requirements/guru-team-trellis-flow.md:375`、`docs/requirements/guru-team-trellis-flow.md:398`、`docs/requirements/guru-team-trellis-flow.md:412`
- 证据：该 durable 文档仍将 companion 职责写成 `archive/journal/publish`，总图与 finish 图保留 `archive task + journal`、`add_session.py -> workspace journal`，dry-run 仍写“不 journal”，Artifact 责任图仍把 workspace journal 列为 finish-work 输出，讲解主线仍说 `trellis-finish-work` 执行 archive、journal、metadata、publish。
- 合同冲突：本任务的 `Docs SSOT Plan` 采用 `ssot_first` 并要求 requirements 说明 Guru Team 不再使用 workspace journal；implementation handoff、Phase 2 check 与 `pr-body.md:45-46` 均宣称 requirements/durable docs 已同步。`requirement-main.md` 已更新，但同目录面向外部演示的完整流程文档仍是旧合同。
- 影响：用户和后续 AI 会从 durable 文档得到互相冲突的 finish/publish 时序；当前 PR body 的 Docs SSOT 声明失实，Branch Review Gate 必须阻断。
- 建议修复：完整重写该文档的 finish 图、dry-run、Artifact 责任图、companion 职责和讲解主线，加入 AI index、initial finish-summary、marketplace verifier、0/1/>1 recovery 与 PR URL metadata tail；修复后回到 Phase 2 检查并更新 PR body 的真实 Docs SSOT 证据。

### P3 - Throwaway verifier 在 preview/switch 后不再检查或清理 `.new`/`.bak`

- 路径与行号：`trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh:149`、`trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh:266`、`trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh:271`、`trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh:279`
- 证据：唯一的 `.new/.bak` 扫描发生在 workflow preview 之前。脚本随后运行 `trellis workflow --create-new`，明确断言 `.trellis/workflow.md.new` 存在，再执行 `--force` switch，但结尾既不删除预览 sidecar，也不重新扫描 `.new/.bak`，仍输出验证成功。
- 合同冲突：仓库开箱即用与 upgrade/update 门禁要求 `.new/.bak` 被逐个处理并记录，不能在验证脚本成功退出时留下未处理 sidecar。
- 影响：throwaway verifier 的成功结论不能证明最终安装状态无冲突 sidecar；后续 switch/reapply 新增的未知 sidecar 也会漏检。
- 建议修复：验证 preview 内容后显式删除预期 `.trellis/workflow.md.new`，并在所有 switch/apply/update/reapply 完成后做最终递归 `.new/.bak` 检查；若保留 sidecar 是测试目标，应单独记录后清理，成功退出前仍要求 clean。

## 观察项

- finish-summary schema 与 Python validator 对绝对路径、反斜杠、CR/LF、dot/parent segment、`.trellis/workspace/**`、`.trellis/.runtime/**` 继续 fail closed；canonical/installed schema、companion、workflow byte-equal。
- `sanitize_finish_summary_git_paths()` 的 all-protected、mixed、no-filter 三类正常输入，以及唯一固定 protected filtering fact 的容量与去重规则已有测试覆盖；本轮 finding 针对命令失败分支，不否定正常 sanitizer 行为。
- 当前 Git index 已不跟踪 `.trellis/workspace/**`；`origin/main...HEAD` 仍保留 3 条预期 `D`，`.gitignore` 与 preset 配置包含 workspace ignore，`session_auto_commit: false` 已物化。
- `.trellis/guru-team/extension.json` 的 `managed_backups` 保留一次 apply 产生过的 `.bak` provenance，但当前 worktree 实际没有 `.new/.bak` 文件；此项不单列 finding。
- issue-scope-ledger 的 primary/close 仅为 #97，#53/#96/#100 为 related，#98/#99 为 follow-up；`pr-body.md` 的 close/ref 语义正确。远端 marketplace evidence 仍为 pending，发布前必须由真实 current-ref verifier 替换，不能以本轮本地测试代替。

## 后续候选

- #100 archived task backfill、#98 历史上下文分级发现、#99 developer identity 解耦均为 live #97 明确非目标，保持现有 related/follow-up 分类，不并入本轮修复。
- 未发现需要新增 GitHub issue 的独立范围；5 个 finding 均属于 #97 当前 close scope，必须在同一分支回到 Phase 2/3 修复并复审。

## Docs SSOT 判断

- 状态：`FAIL`。
- `trellis/workflows/guru-team/workflow.md`、`requirement-main.md`、README、workflow/data/companion/preset specs 与 finish entry overlays 已表达 finish-summary 新流程。
- `docs/requirements/guru-team-trellis-flow.md` 仍是旧 journal/add_session 链路，且启动/context 实现与 durable “never uses workspace context evidence” 声明不一致。
- `ssot_first` 计划未完成 reconciliation，Phase 2 `docs_ssot=true` 和 PR body 的“requirements 已同步”结论已被最终 diff 证据推翻。

## 部署与安全判断

- 本 diff 未修改 GitHub Actions/CI/CD、Dockerfile/Compose、Kubernetes/Kustomize、数据库 migration、Makefile，也未新增 API、服务、后台 worker、定时任务、队列消费者、数据库结构或运行时配置入口；无需同步业务部署资产。
- 变更影响 Guru Team marketplace workflow/preset 安装与 finish/publish 元数据控制面，真实 remote marketplace verification 仍是发布前 fail-closed 门禁。
- 未发现 token、secret、private key、签名 URL、`.env` 内容、数据库 URL、客户数据或 workspace journal 内容迁移。删除的 tracked journal 只存在于 Git 删除记录，本报告不复述其内容。

## 独立验证

- `gh issue view 97 --repo castbox/guru-trellis --json ...`：live issue 为 OPEN，复读字段合同、0/1/>1 recovery、diff 失败降级与 acceptance criteria。
- `curl -fsSL https://docs.trytrellis.app/index.md`：核对官方 workspace/journal 基线。
- `curl -fsSL https://docs.trytrellis.app/advanced/custom-workflow.md`：确认 workflow 行为应由 Markdown 与 runtime injection 承担，不需要 fork upstream。
- `curl -fsSL https://docs.trytrellis.app/advanced/custom-spec-template-marketplace.md`：确认 public spec template 不承载 active task/runtime 私有状态。
- `python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`：293 tests passed。
- `python3 -m unittest trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`：33 tests passed。
- `python3 -m py_compile ...`：canonical companion、preset installer、dogfood companion 通过。
- `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh .trellis/guru-team/scripts/bash/*.sh`：通过。
- repository JSON 全量 `python3 -m json.tool`：通过。
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`：通过。
- canonical/dogfood `workflow.md`、companion、finish-summary schema `cmp`：byte-equal。
- `git diff --check origin/main...HEAD`：通过。
- `git ls-files '.trellis/workspace/**'`：空；`git diff --name-status origin/main...HEAD -- '.trellis/workspace/**'`：3 条预期删除。
- `git rev-parse HEAD`：审查结束前仍为 `53f265f3949ca8374c7b534da309a4c924325450`；source checkout `main` 仍干净并位于 `ff8c03abb259c2a048626ea72e0bf57138db2c14`。

## 结论

当前分支不能通过 Branch Review Gate，也不能进入 `trellis-finish-work`。5 个 current-scope finding 均需修复；修复涉及 canonical workflow/overlay/context、companion recovery/snapshot、durable docs、throwaway verifier 与测试，因此必须回到 Phase 2，重新完成独立 check、提交，并由符合 replacement/closure 身份规则的审查代理闭环后，再派发 fresh 最终放行审查代理。
