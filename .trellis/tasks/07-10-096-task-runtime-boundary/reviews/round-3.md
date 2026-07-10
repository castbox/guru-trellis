# Branch Review Round 3：问题闭环审查报告

## 审查元数据

- 审查角色：Branch Review Round 3，问题闭环审查代理；全新独立 reviewer。
- 审查 HEAD：`f05cd662e852984f7f07cf6336d0867eb6532302`。
- 审查范围：`origin/main...HEAD`；merge base / `origin/main` 为 `59d6c0caf404c4c927fe8aada92811d1ced907d5`。
- 完整提交序列：`a84e5720d0ea18482b46b165062930e50cf54b34`、`90a2d45c823775ff0eaa485ef10640d8b4aa96f5`、`f05cd662e852984f7f07cf6336d0867eb6532302`。
- 完整 diff：64 个文件，`4570 insertions(+), 1244 deletions(-)`。
- Workspace boundary：expected workspace 与 actual repo root 均为 `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/096-task-runtime-boundary`；source checkout 干净，task worktree 开始时仅 `agent-assignment.json` 为主会话审查 metadata dirty，无 suspicious source artifacts。
- 审查输入：`prd.md`、`design.md`、`implement.md`、`implementation-handoff.md`、`planning-approval.json`、最新 `phase2-check.json`、`issue-scope-ledger.json`、`agent-assignment.json`、Round 1/2 reports、`check.jsonl` 引用的 spec/research、Issue #96 实时正文、相关 issue #53/#97/#98/#99/#100 状态以及三提交完整 committed diff。
- 审查行为：未修改实现、未 commit、未 push、未创建 PR、未写 `review-gate.json`；仅新增本 raw review report。

## Finding 生命周期

### Round 1 Finding 1 — P1：任务启动上下文 SHA 映射

- Round 1 状态：阻塞。
- Round 2 状态：已闭环。
- Round 3 复核：保持闭环。
- 证据：`build_task_start_context()` 使用 producer 的 `local_head_after` / `remote_head`；fresh、remote-only、fetch-failed 状态均有 fail-closed 回归测试。固定 HEAD clean clone 的 239 项 core tests 通过。

### Round 1 Finding 2 — P1：clean clone preset fixture

- Round 1 状态：阻塞。
- Round 2 状态：已闭环。
- Round 3 复核：保持闭环。
- 证据：obsolete schema fixture 已固化为 `trellis/presets/guru-team/scripts/python/fixtures/intake-handoff.schema.json`；固定 HEAD clean clone 的 30 项 preset tests 通过，不依赖 `git show HEAD:<deleted-path>`。

### Round 1 Finding 3 — P1：push 后 marketplace verifier

- Round 1 状态：阻塞。
- Round 2 状态：主执行链闭环，遗留 failed artifact contract P2。
- Round 3 状态：全部闭环。
- 证据：`cmd_publish_pr()` 在首次 branch push 后执行 verifier，在 `gh pr create` 前完成 verifier artifact、ledger 回写、精确双文件 metadata commit/push、artifact/ledger/current HEAD/remote HEAD/Branch Review Gate 交叉校验；任一步失败即 fail closed。

### Round 1 Finding 4 / Round 2 Finding 1 — P1：AC9 deferred 文字与 ledger 真实验收证据

- Round 2 状态：阻塞。
- Round 3 状态：已闭环。
- 证据：
  - `issue-scope-ledger.json` 的 `primary_issue` 与 `close_issues[#96]` 均包含唯一固定结构 `remote_marketplace_verification`，当前为 `required=true`、`status=pending`。
  - `validate_ledger_for_publish(..., allow_pending_remote_marketplace=True)` 只允许 verifier 前的固定 pending；最终 `validate_ledger_for_publish()` 明确拒绝 pending、普通文字、缺失或非唯一结构。
  - `write_remote_marketplace_evidence()` 只接受 contract-valid `status=passed` verifier payload，并同时回写 primary/close ledger；passed evidence 固化 artifact repo-relative path、artifact SHA-256、verified content HEAD、verifier remote HEAD、publish content HEAD 与 `commands_passed=true`。
  - verifier 后重新加载 ledger；`validate_marketplace_verification(..., ledger)` 逐项比对 primary/close evidence 与 artifact digest/HEAD/command facts；随后再次执行最终 ledger validator。
  - 定向测试 `test_pending_remote_marketplace_evidence_blocks_final_publish`、tampered digest 和 post-verifier ledger 校验均通过。
- 当前真实状态：远端 branch 尚不存在，`marketplace-verification.json` 尚未生成，ledger 仍保持 pending；因此当前不会被误判为可 publish，真实 push 后才允许回写 passed。

### Round 2 Finding 2 — P2：failed marketplace payload 不满足公开 schema

- Round 2 状态：阻塞。
- Round 3 状态：已闭环。
- 证据：
  - 公开 `marketplace-verification.schema.json` 对 `status=failed` 允许空 asset digest 与 false flags，同时每个 step 必须保留 command、exit code、stdout/stderr SHA-256、size 和 passed 字段。
  - runtime `marketplace_verification_contract_errors()` 对顶层 keys、SHA/digest、step audit fields、asset keys/flags 和 passed/failed 条件执行固定合同校验；artifact 写盘前执行该校验。
  - 独立使用 `jsonschema.Draft202012Validator` 对真实 executor 生成的 passed、early failed、partial failed 三类 payload 验证，三类均 schema-valid；对应 runtime contract errors 均为空。
  - 定向回归及完整 239 项 core tests 通过。

## Round 2 专项闭环证据

### AC9 required pending 与最终 publish 阻断

- verifier 前：只有固定 pending 结构可进入首次 push/verifier 阶段；pending 明示“不满足最终 publish”。
- verifier 成功后：只允许 schema-valid passed payload 回写 ledger；failed/invalid payload 被 `write_remote_marketplace_evidence()` 拒绝。
- verifier 后：重新加载 ledger并执行 artifact facts 比对与 final ledger validation；pending 或伪造 passed 无法进入 `gh pr create`。

### Artifact + ledger 精确双文件 metadata tail

- `commit_marketplace_verification_metadata()` 的 allowed set 仅为当前 task 的 `marketplace-verification.json` 与 `issue-scope-ledger.json`。
- 缺任一文件、出现第三个 dirty path、staged diff 为空均阻断。
- 定向测试证明 exact two-file tail 允许，额外 `agent-assignment.json` 即阻断。

### Metadata push 后交叉校验

- verifier artifact 的 `verified_head` 必须是首次 push 的 reviewed content HEAD。
- `git diff --name-only <verified_content_head>..<current_publish_head>` 必须精确等于 artifact + ledger 两个路径。
- ledger 中 artifact SHA-256、verified content HEAD、remote HEAD、publish content HEAD、commands result 必须与 artifact 事实完全一致。
- metadata push 后远端 branch HEAD 必须等于当前 publish HEAD。
- 最后再次以 `allow_metadata_after_gate=true` 校验 Branch Review Gate；出现非 Trellis metadata tail 或 stale gate 即阻断。

## 完整 Diff 审查

### AI / 脚本边界

- AI 仍负责 issue close scope、PR readiness、证据充分性与真实性判断；脚本只执行 push、远端命令、记录 deterministic command evidence、hash/HEAD/path/schema 校验和 fail-closed 阻断。
- 未发现脚本代替 reviewer 判断 findings、决定 issue 分类或自动宣称 PR ready。
- workflow 行为保留在 canonical/dogfood Markdown；未修改 Trellis upstream、全局 npm、`node_modules` 或官方 task lifecycle 脚本。

### 任务运行态与可移植边界

- `task-start-context.json` 不含本机 worktree 绝对路径；task artifact dir 为 repo-relative。
- `.trellis/.runtime/guru-team/workspaces|tasks/*.json` 为 gitignored local runtime；cache-miss/worktree reconstruction 和并行 task 独立路径由 core tests 覆盖。
- tracked active paths 已移除旧 `.trellis/guru-team/handoff.json` 与 canonical `intake-handoff.schema.json`；仅保留 preset obsolete cleanup fixture，用于安全删除旧 managed copy。

### Canonical / dogfood / docs / overlays

- canonical workflow 与 `.trellis/workflow.md` 字节一致。
- canonical/dogfood Python companion、marketplace schema、task-start schema、config template 字节一致。
- `check-dogfood-overlay-drift.sh` 通过；未发现 `.new` / `.bak` 残留。
- Agents/Codex/Claude/Cursor finish-work 入口均同步 verifier、ledger、two-file metadata tail 和 fail-closed 语义。
- Docs SSOT strategy 为 `ssot_first`；workflow、workflow specs、README、workflow README、preset README 与 requirements docs 对任务启动上下文、本机运行态和远端 marketplace gate 的定义一致。

### Clean clone / 开箱即用 / upgrade-update

- 固定 checkout 到 reviewed HEAD 的 `git clone --no-local`：239 项 core tests 与 30 项 preset tests 均通过。
- `task.py validate`、Python compile、shell syntax、JSON parse、commit message、dogfood drift、`git diff --check` 均通过。
- 仓库现有 `verify-throwaway-install.sh` 默认 source 指向尚未发布的 `v0.6.5-guru.3`，该 tag 在远端不存在，直接运行会在 marketplace index 获取处失败。该默认值与失败条件已存在于 `origin/main`，本分支未修改该脚本，不作为本任务新 finding；当前分支远端安装的真实验证由新增 publish 后 verifier 强制执行，且 branch 未 push 时 ledger pending 会阻断发布。
- 因当前 reviewer 明确禁止 push，本轮没有执行真实远端 branch init/preview/switch/preset reapply，也不把它声明为已通过；该证据必须由后续正式 publish verifier 生成。

### Issue close scope

- live Issue #96 仍为 OPEN，scope 与任务实现一致。
- `close_issues` 仅 #96；#53 为 related，#97/#98/#99/#100 为 followup，均为 OPEN，未发现误用 close semantics。
- 最终 `Closes #96` 仍受 AC9 passed evidence 和 Branch Review Gate 约束；pending 状态不能关闭。

### 安全与部署影响

- committed diff 未发现 token、private key、`.env`、数据库 URL、签名 URL或客户敏感数据。
- verifier command evidence 对 remote URL 与 temp path 使用展示占位符，artifact 只记录 digest/size，不落完整输出。
- 临时验证目录使用 `TemporaryDirectory` 自动清理。
- 不涉及业务服务、容器、Kubernetes、数据库 migration、CI/CD 或 Makefile；影响仅限开发工作流、marketplace/preset 安装、task metadata、finish/publish gate。

## 验证结果

- Workspace boundary：通过。
- 完整 diff：已审查 `origin/main...f05cd662e852984f7f07cf6336d0867eb6532302` 三提交。
- Clean clone core tests：239 tests，通过。
- Clean clone preset tests：30 tests，通过。
- Marketplace pending/passed、exact two-file tail、tampered ledger：定向测试通过。
- Marketplace passed/early failed/partial failed：runtime contract 与 Draft 2020-12 JSON Schema 均通过。
- Python compile：通过。
- Shell syntax：通过。
- JSON / JSONL / task context validation：通过。
- Commit messages：3 个提交，通过。
- Dogfood overlay drift：通过。
- Canonical/dogfood byte equality：通过。
- `git diff --check origin/main...HEAD`：通过。
- 真实远端 branch marketplace：未执行；远端 branch 尚不存在，pending gate 正确阻断。
- 默认 stable-tag throwaway script：失败，原因是 `origin/main` 已存在的未发布 `v0.6.5-guru.3` 默认 source；不属于本分支回归。

## 问题清单

- P0：0。
- P1：0。
- P2：0。
- P3：0。

## 观察项

- 当前 task worktree 的 `agent-assignment.json` 由主会话维护且在审查开始前已 dirty；本 reviewer 未修改该文件。
- 后续正式 publish 必须让 verifier 生成真实 `marketplace-verification.json`、把 primary/close ledger 从 pending 回写为 passed，并完成 metadata push 后交叉校验；任何失败不得创建 PR。
- 稳定 tag `v0.6.5-guru.3` 尚未发布，因此不能用默认 throwaway script 声称稳定 tag marketplace 已验证；该限制应在后续 PR readiness 中如实说明，或在 release/tag 可用后补验。

## 证据交接

- Diff 范围：`origin/main...HEAD`，Reviewed HEAD 为 `f05cd662e852984f7f07cf6336d0867eb6532302`，覆盖完整三提交与 64 文件累计 diff。
- Round 2 闭环：AC9 pending/passed ledger、primary/close 回写、exact two-file metadata tail、metadata push 后 artifact/ledger/gate/remote HEAD 交叉校验均已闭环；passed/early/partial failed marketplace payload 均满足公开 schema并保留可审计 step evidence。
- Docs SSOT：`ssot_first`；durable docs、task artifacts、canonical/dogfood/overlays、代码和测试一致。
- 部署/安全：无业务部署、DB、容器或 CI/CD 影响；未发现敏感信息泄露。
- 本报告 findings 为零，可作为 Round 3 raw report 供后续最终放行审查和 Branch Review Gate 汇总使用；本 reviewer 未记录或修改 gate。

## 结论

Round 2 的 1 个 P1 与 1 个 P2 均已闭环，Round 1 历史 findings 保持闭环；本轮未发现新的 P0/P1/P2/P3 finding。建议进入最终放行审查。真实远端 marketplace 验证仍必须在正式 publish 的首次 push 后执行，并由当前 fail-closed pending/ledger/verifier 链约束；在真实 passed evidence 生成前不得创建 PR 或关闭 #96。
