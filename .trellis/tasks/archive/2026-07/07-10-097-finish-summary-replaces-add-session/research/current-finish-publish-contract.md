# 当前 finish/publish 合同证据

## Live Issue

- #97 定义 finish-summary schema、两阶段 PR URL 回写、workspace 清理、测试与 throwaway/update 门禁。
- #100 把 #97 作为 schema 唯一 SSOT，并定义 backfill metadata 与缺失字段例外。
- #98 只扫描 `.trellis/tasks/archive/**/finish-summary.json`，要求 issue/PR/branch/path/term 与自然语言检索信号。

## 实施前基线代码（历史证据，非当前合同）

以下条目记录本任务实现前的 `main` 基线，不描述 commit `53f265f` 或本轮待修实现：

- `cmd_finish_work()` 当前顺序：Branch Review Gate -> PR body readiness -> `task.py archive` -> `add_session.py` -> metadata commit -> `cmd_publish_pr()`。
- `build_finish_work_dry_run_plan()` 当前仍返回 `plan.journal` 和 `add_session.py` command。
- `cmd_publish_pr()` 当前在 push 与远端 marketplace verification 后执行 `gh pr create`，取得 URL 后直接返回，不写 task artifact。
- `METADATA_ONLY_PREFIXES` 当前含 `.trellis/workspace/`，会把 workspace dirty path 识别为 metadata。
- `.trellis/config.yaml` 当前只注释 `session_auto_commit: true`；官方 `task.py archive` 因而具备 auto-commit 行为。

## 实施前安装面（历史证据，非当前合同）

以下条目记录本任务实现前的安装面，不描述 commit `53f265f` 或本轮待修实现：

- `MANAGED_ASSET_PATHS` 当前只安装 task-start-context 与 marketplace-verification schema。
- preset installer 当前只 materialize Codex dispatch mode 和 runtime ignore。
- `normalize_business_doc_language_guidance()` 当前会扫描并改写 workspace index，这与 #97 禁止 Guru Team 写 workspace 的合同冲突。
- 本仓库 tracked workspace 文件为 `.trellis/workspace/index.md`、`.trellis/workspace/wumengye/index.md`、`.trellis/workspace/wumengye/journal-1.md`。

## 官方 Trellis 边界

- 官方 workflow 由 `.trellis/workflow.md` 控制；Guru Team 改动留在 marketplace workflow、preset、skill/prompt/overlay 和 companion。
- 官方 `session_auto_commit: false` 只关闭 add-session/archive 的 Git stage/commit，文件写入仍会发生。
- 官方 workspace 是 developer journal 面；#97 不删除 upstream 能力，只让 Guru Team 不调用它。
- 官方 `task.py archive` 保留，Guru Team 用 `session_auto_commit: false` 接管 task metadata commit。

## 规划结论

- `finish-summary-index.json` 保存 AI 判断，final summary recorder 保存确定性事实。
- schema 与 Python validator 同源维护，#100 复用同一 validator。
- PR URL metadata commit 位于 remote verifier 后，必须使用精确 archived task path allowlist，并为 recovery 复用现有 PR。
- recorder 对 raw `git diff --name-only <base>...HEAD` 排序去重，再过滤 workspace/runtime 受保护前缀；过滤结果写入 `git.changed_paths` 与 `index.search_terms.paths`。
- 被过滤集合非空时，recorder 追加一条固定且不含具体路径的 `contract_changes[]` 事实记录；被过滤集合为空时不追加。
- schema 与 validator 继续禁止 final summary 任一 path 字段包含 workspace/runtime 受保护前缀，不设置删除态例外。
- 验证必须覆盖全过滤为空、混合路径与无过滤三类输入。

## GitHub 同步证据

- 主会话已通过 GitHub MCP/API 同步 issue #97 body，并经 live reread 确认包含方案 A 的安全过滤、固定事实记录与三类测试规则。
- 2026-07-11 live reread 的 #97 line 162 明确写明：PR 创建失败时保持 initial summary，publish retry 成功后再执行回写。这一条要求 recovery 在未发现 open PR 时具备安全 create retry，而不是直接失败。

## 独立检查 P1 Planning Blocker（历史已闭环）

- 独立 Phase 2 check 最终报告为 `FAIL / Planning Blocker`：批准版 `design.md` 第 6.3 条把 0 个 open PR 与多个 open PR 都定义为失败，未承接 live #97 line 162 的 publish retry。
- 当前实现的 `unique_open_pull_request()` 要求匹配数量精确为 1；0 个或多个都会抛错。`cmd_publish_pr()` 的 recovery 已能复用既有 passed marketplace verifier evidence，并能接续 PR-exists dirty/staged summary，但尚未实现 0 open PR 时以同一发布输入安全重试 `gh pr create` 一次。
- 当前 normal create 客户端失败会返回 recovery command。recovery 必须先查询 open PR，才能区分“服务端已创建、客户端报错”的 1 个分支与“服务端未创建”的 0 个分支，避免重复 PR。

## 规划修订结论

- recovery 前置复核固定为 branch/base identity、AI-reviewed body/readiness、review gate、current HEAD 与 remote HEAD；marketplace-required recovery 只严格 validate 既有 passed verifier evidence，不重跑 verifier。
- open PR 查询只接受三个确定结果：1 个复用；0 个使用同一 repo/base/head/title/body/draft 只重试 create 一次；多于 1 个 fail closed。
- 取得或创建 PR URL 后继续既有 idempotent summary rewrite/validation、精确 metadata commit/push 与 remote SHA 校验；单次 create retry 失败时保持 initial summary 并返回同一 recovery command。
- 主会话已通过 GitHub MCP/API 把精确 0/1/>1 合同同步到 live #97 body，并再次 live reread 确认；本轮更新后的 `prd.md`、`design.md`、`implement.md` 尚待新的 post-planning approval，当前 Phase 2 只因此项继续阻塞。

## Branch Review round 1 新证据

- commit `53f265f` 后的独立替换问题发现审查给出 P2=4、P3=1；此前 Phase 2 PASS 早于这些 finding，不能作为修复后的 PASS 证据复用。
- Guru Team shared start、Codex session-start、Cursor session-start 仍调用 journal path/line-count 读取链；修复路径已固定：shared start 只组合 phase/packages/task/Git facts，Codex/Cursor canonical overlays 删除 journal helper import/call，不修改 upstream `session_context.py`。
- 当前 recovery error payload 虽含 `publish_inputs`，下一次 invocation 仍会重读可变 title/body/draft。修订采用现有 task-local `pr-readiness.json` 保存已审阅且已提交的 publish snapshot，并在 PR query/create 前验证 snapshot/body digest、Git blob、reviewed HEAD 与 repo/base/head identity。
- current `finish_summary_git_path_snapshot()` 对 initial diff、initial untracked snapshot 或 final/recovery diff 命令失败直接抛错。修订要求两个 path 数组同时降级为空，只追加固定且不披露路径/命令错误的 snapshot-unavailable fact，并重新派生 `retrieval_text`；path validator 不放宽。
- `docs/requirements/guru-team-trellis-flow.md` 仍描述 archive+journal/add_session，必须按 `ssot_first` 完整重写 finish/publish 主线后再运行 Phase 2 check。
- throwaway verifier 在 preview 之后未清理预期 `.trellis/workflow.md.new`，也未做最终 sidecar scan。修订要求校验后显式清理，并在 switch/update/reapply 全部完成后递归确认 `.new/.bak` 为空。

## 本轮规划收敛

- 五个 finding 全部属于 #97 current close scope，不新增或重分类 issue。
- 本轮只更新 task-local 规划与研究证据；实现、Phase 2 check、追加 fix commit、closure review 和 fresh final review 必须在新的 post-planning approval 后依次执行。

## Post-planning 实现证据

- 新的 post-planning approval 已通过；本轮实现按批准方案继续，不改变 issue scope。
- canonical shared start 现只组合 phase/packages/current-task/Git facts；Codex/Cursor SessionStart overlays 已删除 journal helper import/call，并由 fresh-install Path access guard + sentinel 测试证明不打开、不枚举、不输出 workspace journal/path/basename/content/line count。
- `finish-work` 在 archive/metadata commit 前生成 task-local `pr-readiness.json.publish_inputs`；formal publish/recovery 只消费 committed snapshot，验证 canonical/body digest、HEAD Git blob、dirty/staged、artifact one-commit history、review gate ancestry 与 repo/base/head/current/remote identity。Recovery command 不携带 title/body/draft/base/validation override。
- initial diff、initial untracked enumeration 与 final/recovery diff 任一失败时 recorder 返回空 path 集合，只追加一次固定 snapshot-unavailable fact，移除 filtering fact，并重新派生 retrieval text；path schema/validator 未放宽。
- `docs/requirements/guru-team-trellis-flow.md` 的总图、finish 图、dry-run、Artifact 责任图、companion 职责与讲解主线已改为 AI index -> initial summary -> immutable readiness -> marketplace verifier -> 0/1/>1 recovery -> PR URL metadata tail。
- throwaway verifier 校验并删除预期 preview `.new`，执行 switch、`trellis update --force`、preset reapply 后递归扫描 `.new/.bak`，任何 sidecar 都会阻塞成功。
