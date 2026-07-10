# 实现代理交接

## 身份与范围

- 实现代理：`019f4b63-b84b-7091-90a0-e108488589ec`（Build Agent）
- 工作区：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/096-task-runtime-boundary`
- 任务：`.trellis/tasks/07-10-096-task-runtime-boundary`
- 执行边界：完成 Issue #96 实现与实现期验证；未执行 `trellis-check`、Phase 2 recorder、commit、push、PR 或 Branch Review Gate。

## Docs SSOT 承接

- Strategy：`ssot_first`。
- Durable primary inputs：`trellis/workflows/guru-team/workflow.md`、`trellis/workflows/guru-team/schemas/task-start-context.schema.json`。
- Durable sync result：已同步 `.trellis/spec/workflow/**`、`docs/requirements/**`、仓库/marketplace/preset README、canonical overlays 和 dogfood installed copies。
- Task delta merged：任务启动上下文、本机运行态、workspace boundary、obsolete managed artifact 清理合同已合并到 durable workflow/schema/spec/docs。
- Task-history-only：`prd.md`、`design.md`、`implement.md`、`research/*.md`、planning approval、agent assignment 和本交接记录仅作为任务审计历史，不复制到公共 marketplace/spec template。
- Follow-up / limitation：实现代理报告固定 tag `v0.6.5-guru.3` 不存在，当前分支远端 marketplace 内容在 commit/push 前无法通过该 tag 验证；本地 canonical preset 与公开 main marketplace 组合验证通过，但不能替代当前分支远端 marketplace 验证。

## 实现完成项

- 新增严格 portable `task-start-context.json` writer/loader/validator 和 schema。
- 新增 `.trellis/.runtime/guru-team/workspaces|tasks/*.json` local-only mappings。
- 迁移 workspace boundary、planning/check/review/finish/publish 下游读取路径。
- 删除旧 `.trellis/guru-team/handoff.json`、`intake-handoff.schema.json`、`handoff_path` config/public API。
- preset installer 增加 obsolete managed file 安全清理：未修改 managed copy 删除；用户修改副本保留并报告冲突。
- preset installer 管理 `.trellis/.runtime/` ignore，canonical overlays 已 apply 到 dogfood。

## 实现期验证

- canonical unit tests：241 项通过（含 Round 1 SHA、Round 2 ledger/verifier/schema/metadata-tail、Round 4 active-reference 及 Round 5 dogfood agent scanner mutation 回归）。
- preset installer tests：30 项通过；obsolete clean fixture 不依赖 Git history。
- JSON、shell syntax、Python compile、task validation、phase context、workspace boundary、dogfood drift、`git diff --check` 通过。
- throwaway preset 安装通过，新安装含 runtime ignore、不含旧 handoff/schema、包含新 schema。
- 无遗留 `.new` / `.bak`。

## Phase 2 检查重点

- portable context forbidden-key / absolute-path 扫描。
- cache 删除后的 `git worktree list` 重建。
- finish/publish workspace boundary 执行顺序。
- 普通 task 写入 allowlist 与并行 task 隔离。
- obsolete cleanup 的未修改删除和用户修改 fail-safe 双路径。
- canonical/dogfood/docs/overlay 一致性及 marketplace 当前分支验证限制。

## Branch Review Round 1 修复

- Finding 1：`build_task_start_context()` 改读 producer 的 `local_head_after` / `remote_head`；writer 对 `fresh`、`remote_only`、`fetch_failed` 状态执行 fail-closed SHA 约束，并新增三类数据流测试。
- Finding 2：obsolete schema 内容固化为 `trellis/presets/guru-team/scripts/python/fixtures/intake-handoff.schema.json`，测试不再读取 `git show HEAD:`，clean clone 当前 commit 可独立复现。
- Finding 3：新增 `verify-marketplace` companion command、`marketplace-verification.schema.json` 与 publish fail-closed 数据流。公共 marketplace/preset 变更发布时执行：push reviewed content HEAD → remote branch init → preview → switch → clone 已 push 的 remote branch → 从该 clone 执行 canonical preset reapply → 记录命令结果与 digest → metadata-only commit/push verification artifact → 校验 artifact/current HEAD/remote HEAD → `gh pr create`。任何步骤失败、artifact 缺失或 stale 都在创建 PR 前阻断；不创建 tag。AI 继续负责 PR readiness 判断，脚本只执行/记录/校验确定性事实。
- Finding 4：`issue-scope-ledger.json` 已按 Issue #96 十项验收写入真实文件/命令/结果。远端 marketplace 项明确要求由真实 push 后 `marketplace-verification.json` 补齐并由 publish validator 校验，当前未写 passed。

## Round 1 后验证计划

- core/preset unit tests、JSON/schema、shell syntax、Python compile。
- `apply.sh --repo . --all-platforms`、dogfood drift、`.new/.bak`、task validation、workspace boundary、`git diff --check`。
- 不执行真实 push；远端 verifier 的真实执行点保留在 formal `finish-work` / `publish-pr`，届时缺失或失败会阻止 PR 创建。

## Branch Review Round 2 修复

- Finding 1：`issue-scope-ledger.json` 的 primary/close #96 已把 AC9 deferred 文字改为固定结构的 `remote_marketplace_verification` pending evidence；pending、普通非空文字或缺失结构均不能通过最终 publish。
- Verifier recorder：真实 push 后只有 schema-valid `status=passed` payload 才能回写 ledger；回写事实包含 artifact repo-relative path、SHA-256、verified content HEAD、verifier remote HEAD、publish content HEAD 和全命令通过结果。AI 仍决定 #96 是否属于 `close_issues` 以及证据是否充分。
- Metadata tail：只允许 `marketplace-verification.json` 与 `issue-scope-ledger.json` 两个精确路径；任何第三路径阻断。metadata push 后重新校验 artifact schema/identity/digest、ledger artifact digest/HEAD 事实、verified HEAD 到当前 HEAD 的精确双路径 diff、远端 metadata HEAD 和 Branch Review Gate，全部通过后才允许 `gh pr create`。
- Finding 2：公开 `marketplace-verification.schema.json` 允许 `failed` payload 保留空 asset digest/false flags，同时要求每个 step 具备 command、exit code、stdout/stderr digest 与 size、passed 字段；运行时 exact-contract validator 在 artifact 写盘前执行。early failure、partial failure、passed 三类 payload 均有回归测试，失败证据不会因 schema 不合法而丢失审计能力。
- Canonical/dogfood：workflow、README、workflow specs、finish-work skills/commands/prompts、managed helper/schema 已通过 `apply.sh --repo . --all-platforms` 同步；`.bak` 已逐个处理，dogfood overlay drift 通过。
- 本轮未生成 `marketplace-verification.json`，未把 pending 伪造成 passed；真实远端证据只会在后续显式 finish/publish 的真实 push 后生成并回写。

## Final Review Round 4 P1 修复

- Active workspace contract：canonical workflow、start/continue/finish skills、Codex prompts/skills、Claude/Cursor commands、implement/check agent overlays、README、requirements 和 workflow specs 已统一：tracked `task-start-context.json` 只提供 portable `workspace_slug`、`task_workspace_id` 与 repo-relative `task_artifact_dir`，不包含且不得读取 absolute `workspace_path`。
- Local runtime boundary：本机 task worktree 必须通过当前 checkout、`.trellis/.runtime/guru-team/**`、`git worktree list` 推导，并由 `check-workspace-boundary.sh --json --task <task-path>` 校验；编辑工具无显式 `workdir` 时只能使用该 helper 已确认 worktree 下的绝对路径。
- Active-reference classification：活跃公共 API 中已清除 `handoff.workspace_path`、`task-start-context.workspace_path`、`task_start_context.workspace_path` 和旧 fixed `.trellis/guru-team/handoff.json`。旧字符串只保留在 obsolete installer fixture/cleanup、verifier absence check、forbidden-key 测试，以及 task-local planning/research/review/history/agent handoff 自然语言中。
- Regression：新增 `ActivePublicReferenceContractTest`，只扫描 canonical workflow/README/requirements/spec/overlays 与 dogfood start/continue/finish/agent copies，不扫描 `.trellis/tasks/**` 历史报告；任一旧 public workspace 引用回流即失败。scanner 路径由 canonical overlay 文件集合映射到 dogfood targets，明确覆盖 `.codex/agents/**`、`.claude/agents/**`、`.cursor/agents/**` 与 `.trellis/agents/**`；隔离 mutation fixture 向 dogfood `.codex/agents/trellis-check.toml` 注入 forbidden reference 并确认 scanner 必须失败。core suite 当前为 241 项。
- Sync：已运行 `apply.sh --repo . --all-platforms --json` 同步 Claude/Codex/Cursor 与 `.trellis/agents` dogfood copies；无 `.new` / `.bak`。

## 补充 Phase 2：Branch Review Gate Validator 增量

- Plan strategy：保持 Issue #96 已批准需求与 portable task/runtime 边界不变，仅修复 Branch Review Gate closure validator 对正常跨代理问题闭环的错误拒绝。显式 `reuse_decisions[] decision=new-agent` 必须精确匹配 `from_round`、`to_round`、closure `agent_id`、`logical_role=问题闭环审查代理`、reviewed `head` 与非空 `reason`；closure round 若仍有 findings，则成为新的 finding owner，必须继续显式闭环。finding owner、同代理 closure agent、fresh new-agent closure agent 和 replacement closure agent 均不得成为最终放行代理；最终轮仍要求 fresh `new-agent`、当前 HEAD、零 findings。
- Docs SSOT sync：canonical `trellis/workflows/guru-team/workflow.md`、dogfood `.trellis/workflow.md`、`.trellis/spec/workflow/companion-scripts.md`、`.trellis/spec/workflow/data-contracts.md`、`trellis/presets/guru-team/README.md`、五个平台 canonical continue overlays 及其 dogfood copies 已同步 validator 语义。canonical/dogfood Python helper、workflow 和五组 overlay 均 byte equal，`check-dogfood-overlay-drift.sh --repo .` 通过。
- Validator evidence：当前真实 `.trellis/tasks/07-10-096-task-runtime-boundary/agent-assignment.json` 的 Round 1–7 调用 `final_review_round_errors(..., expected_head=30f4f4a5bc42cfb099ea07fa7e64c9af5dd5e623)` 返回空列表，`check-agent-assignment.sh --json` 返回 `status=ok`；新增正向跨代理 closure、链式 closure，以及缺失 relation、未闭环 finding、closure agent 充当 final 等负面测试均通过。
- Verification：core tests `247/247`、preset tests `30/30`、新增定向 tests `8/8` 通过；Python compile、全部 canonical/dogfood/preset shell syntax、JSON/JSONL 解析、task validation（implement 9 / check 10）、workspace boundary、active-reference scanner/mutation、dogfood drift、`git diff --check` 通过。在临时初始化仓库执行 `--all-platforms` preset apply 成功，安装副本包含新 closure 合同且无 `.new` / `.bak`；未对真实仓库执行 preset apply/installer。
- Boundary judgments：Docs SSOT 已覆盖且文案与 validator 一致；未触碰 secret、credential、客户数据或日志安全边界；dirty diff 不包含 CI/CD、容器、K8s/Kustomize、数据库 migration 或 Makefile 资产。`issue-scope-ledger.json` 仍仅关闭 #96，#53 为 related，#97/#98/#99/#100 为 follow-up；remote marketplace AC9 保持结构化 `pending`，本轮未 push、未生成 verifier artifact、未伪造 passed。
- Expected stale artifact：现有 `phase2-check.json` 记录 HEAD `f48abcf1f73da439efc68f7342dde562c4c9c452`，且 dirty paths 与当前增量不一致，因此 `check-phase2-check.sh` 按设计返回 stale；主会话必须基于本次补充检查重新记录 Phase 2 artifact，本检查代理未写 `phase2-check.json`。
- Dirty paths observed：`.agents/skills/trellis-continue/SKILL.md`、`.claude/commands/trellis/continue.md`、`.codex/prompts/trellis-continue.md`、`.codex/skills/trellis-continue/SKILL.md`、`.cursor/commands/trellis-continue.md`、`.trellis/guru-team/scripts/python/guru_team_trellis.py`、`.trellis/spec/workflow/companion-scripts.md`、`.trellis/spec/workflow/data-contracts.md`、`.trellis/tasks/07-10-096-task-runtime-boundary/agent-assignment.json`、`.trellis/tasks/07-10-096-task-runtime-boundary/review.md`、`.trellis/tasks/07-10-096-task-runtime-boundary/reviews/round-6.md`、`.trellis/tasks/07-10-096-task-runtime-boundary/reviews/round-7.md`、`.trellis/workflow.md`、`trellis/presets/guru-team/README.md`、五个平台 canonical continue overlays、`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`、`trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`、`trellis/workflows/guru-team/workflow.md`，以及本次追加的 `implementation-handoff.md`。未回退或改写其他代理的 task metadata/review files。
