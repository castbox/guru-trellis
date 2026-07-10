# Branch Review Round 4：最终放行审查报告

## 审查元数据

- 审查轮次：Round 4，最终放行审查。
- 审查角色：最终放行审查代理（全新独立 reviewer）。
- Reviewed HEAD：`f05cd662e852984f7f07cf6336d0867eb6532302`。
- Diff 范围：`origin/main...HEAD`。
- 审查提交：`a84e572`、`90a2d45`、`f05cd66`，共 3 个提交、64 个文件、4570 insertions、1244 deletions。
- 工作区：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/096-task-runtime-boundary`。
- Workspace boundary：通过；expected workspace 与 actual repo root 均为指定 worktree，source checkout 干净且无可疑 task artifact。审查开始前 task worktree 已存在主会话维护的 `agent-assignment.json` dirty 状态与未提交 `reviews/round-3.md`，本 reviewer 未修改这些既有文件。
- 独立性：已读取 live Issue #96、`prd.md`、`design.md`、`implement.md`、planning approval、implementation handoff、Phase 2 check、issue scope ledger、agent assignment、Round 1/2/3 raw reports、`check.jsonl` 引用的 spec/research、durable docs、canonical/dogfood/overlays，以及完整 committed diff；未把 Round 3 结论当作最终结论。

## Finding 生命周期

### Round 1 Finding 1 — P1：任务启动上下文 SHA 映射

- 历史状态：Round 1 阻塞，Round 2 已闭环。
- Round 4 独立证据：`build_task_start_context()` 读取 producer 的 `local_head_after` / `remote_head`，并对 `fresh`、`remote_only`、`fetch_failed` 分支执行约束；对应回归测试通过。
- 最终状态：已闭环。

### Round 1 Finding 2 — P1：clean clone preset fixture

- 历史状态：Round 1 阻塞，Round 2 已闭环。
- Round 4 独立证据：obsolete schema fixture 固化在 `trellis/presets/guru-team/scripts/python/fixtures/intake-handoff.schema.json`；固定 HEAD clean clone 的 30 项 preset tests 全部通过。
- 最终状态：已闭环。

### Round 1 Finding 3 — P1：push 后 marketplace verifier

- 历史状态：Round 1 阻塞，Round 2 主链闭环并产生 failed artifact contract P2，Round 3 宣称全部闭环。
- Round 4 独立证据：`cmd_publish_pr()` 在 `gh pr create` 前先 push reviewed content HEAD，执行 `execute_marketplace_verification()`，只从 schema-valid `passed` payload 回写 ledger，提交并 push 精确 artifact + ledger 双文件 metadata tail，再交叉校验 artifact、ledger、当前/远端 HEAD、Branch Review Gate；任何异常均抛出 `WorkflowError`。
- 当前真实状态：真实 GitHub 远端 `codex/096-task-runtime-boundary` branch 尚不存在，`marketplace-verification.json` 不存在，primary/close #96 的 `remote_marketplace_verification` 均为 `required=true,status=pending`；当前不能 publish 或创建 PR。
- 最终状态：执行链已闭环，真实远端验收仍按设计 pending；pending 状态 fail closed，不构成已通过证据。

### Round 1 Finding 4 / Round 2 Finding 1 — P1：Issue Scope Ledger 真实验收证据

- 历史状态：Round 1/2 阻塞，Round 3 宣称闭环。
- Round 4 独立证据：ledger 已包含 AC1~AC10；远端 marketplace 项使用固定结构 pending evidence，最终 validator 仅允许 marketplace 变更在 verifier 执行前暂时 pending，真实 verifier 后必须回写 exact passed facts，并重新执行最终 ledger 校验。
- 最终状态：代码合同已闭环；当前远端证据仍 pending，因此尚未满足最终 publish，但不会被误判为 passed。

### Round 2 Finding 2 — P2：failed marketplace payload schema

- 历史状态：Round 2 阻塞，Round 3 宣称闭环。
- Round 4 独立证据：runtime contract 与 Draft 2020-12 schema 均允许 `failed` payload 使用空 digest/false flags，同时要求 step command、exit code、stdout/stderr digest 与 size、passed 字段；early/partial/passed 定向测试在 239 项 suite 内通过。
- 最终状态：已闭环。

## 最终审查

### Finding 1 — P1：现行平台入口与 Docs SSOT 仍依赖已删除的 `handoff.workspace_path`

- 状态：阻塞，未修复。Branch Review 模式禁止 reviewer 修改实现或首次合并 durable docs。
- 代码/文档位置：
  - `.agents/skills/trellis-start/SKILL.md:34`、`.codex/skills/trellis-start/SKILL.md:34` 和对应 preset overlays 写成“`task-start-context.json` 的 `workspace_path`”，但 `task-start-context.schema.json` 固定字段中不存在 `workspace_path`，`validate_task_start_context()` 还明确把 `workspace_path` 列为 forbidden key。
  - `.agents/skills/trellis-continue/SKILL.md:19`、`.agents/skills/trellis-continue/SKILL.md:56`、`.codex/prompts/trellis-continue.md:13`、`.codex/prompts/trellis-continue.md:50`、`.codex/skills/trellis-continue/SKILL.md:19`、`.codex/skills/trellis-continue/SKILL.md:56`、`.cursor/commands/trellis-continue.md:13`、`.cursor/commands/trellis-continue.md:50` 仍要求确认或使用 handoff `workspace_path`。
  - `README.md:295`、`README.md:296`、`README.md:307`、`docs/requirements/README.md:35` 仍把 executor handoff / `handoff.workspace_path` 描述为现行 workspace boundary SSOT。
  - `.trellis/spec/workflow/companion-scripts.md:69`、`.trellis/spec/workflow/companion-scripts.md:179` 仍写“handoff is written”及 actual repo root equals handoff；`.trellis/spec/workflow/workflow-contract.md:28` 仍要求 Phase 0 resolve handoff。
- 与需求冲突：Issue #96 的固定决定要求运行路径、schema、workflow、skill、prompt、config 和 public API 完整删除 handoff 概念；任务启动上下文只允许 portable 字段，本机绝对 workspace path 只能来自 local runtime/worktree reconstruction。当前文案不仅是历史术语残留，而是活跃 start/continue 执行指令和公开边界合同。
- 实际影响：新安装或 dogfood agent 会尝试读取一个 schema 禁止且永远不存在的字段；当编辑工具不能显式设置 `workdir` 时，入口无法从该指令取得合法绝对路径，可能退化为 source checkout 相对写入或错误阻塞。不同平台入口也未完成 Issue #96 要求的一致迁移。
- 测试缺口：239+30 tests、dogfood drift 和 canonical byte equality 均未检测“活动入口不得引用旧 handoff workspace contract / 不得声称 task-start-context 含 workspace_path”。现有 active reference audit 范围不足以覆盖这些文档与 overlay。
- 建议修复：统一改为“以 handoff/task-start-context 中的 repo-relative `task_artifact_dir`、当前 checkout、`git worktree list` 和 `.trellis/.runtime/guru-team/**` local mapping 由 `check-workspace-boundary` 重算 expected workspace”；编辑工具无法传 `workdir` 时使用 boundary validator 输出的 expected workspace 或显式 task worktree absolute path。同步 canonical overlays、dogfood copies、README、requirements 与 workflow specs，并增加活动入口 forbidden-reference 回归测试。

## 证据

- 完整 diff：已审查 `origin/main...f05cd662e852984f7f07cf6336d0867eb6532302`，未只审查最新提交。
- Clean clone：使用 `git clone --no-local` 固定 reviewed HEAD；core tests 239 项通过，preset tests 30 项通过。
- 静态验证：Python compile、shell syntax、task JSONL validation、JSON/JSONL parse、dogfood overlay drift、`git diff --check` 均通过。
- Commit messages：3 个提交均通过 `check-commit-messages.sh --base-ref origin/main`。
- Canonical/dogfood：workflow、Python helper、task-start-context schema、marketplace-verification schema byte equality 通过；无 `.new` / `.bak`。
- Workspace/runtime：task-start portable field/forbidden-key、runtime mapping、cache miss reconstruction、parallel task distinct tracked/runtime paths、obsolete cleanup 测试通过。
- Verifier/ledger：pending/passed ledger、failed payload contract、exact two-file metadata tail、tampered ledger digest 与 publish 顺序测试通过；代码路径在 `gh pr create` 前 fail closed。
- 真实远端 verifier：未执行成功证据；远端 branch 当前不存在，artifact 缺失且 ledger pending，因此不得声称远端 marketplace 已通过。
- Issue scope：`close_issues` 仅 #96；#53 为 related；#97/#98/#99/#100 为 followup。Issue #96、#53、#97、#98、#99、#100 均未因本审查被关闭或修改。
- 安全：diff 未发现 token、private key、`.env`、数据库 URL、签名 URL或客户数据；verifier 只记录输出 digest/size，display command 隐去 remote URL 与临时目录。
- 部署：无业务服务、DB migration、容器、Kubernetes、CI/CD 或 Makefile 变更；影响限于开发工作流、marketplace/preset 安装、task metadata 与 publish gate。

## 观察项

- `agent-assignment.json` 已记录 Round 1~3，但本 reviewer 开始时尚未记录 Round 4 assignment/review round；这是主会话 recorder 的后续职责，不由 reviewer 写入。
- 默认 stable-tag throwaway 路径仍受尚未发布 tag 限制；本任务新增的真实 branch verifier 可在正式 publish 首次 push 后提供当前 branch 证据，但在 passed artifact 生成前不能把开箱即用宣称为远端已验证。
- 多处“implementation handoff”“agent handoff”“handoff_summary”属于实现代理交接或 sub-agent 继任语义，不等同于本 issue 删除的 Guru Team intake artifact；本 finding 只覆盖仍作为 task workspace/intake 公共 API 使用的引用。

## 后续候选

- 增加 deterministic active-reference test，覆盖 canonical workflow、start/continue/finish overlays、dogfood copies、README、requirements 和 workflow specs；仅允许 obsolete cleanup fixture、forbidden-key guard、历史 finding/report 中出现旧 intake handoff 字符串。
- 正式 publish 时先 push reviewed/fixed content HEAD，再运行 remote marketplace verifier；只有生成 schema-valid passed artifact、回写 primary/close ledger、提交并 push精确双文件 tail、重新验证 Branch Review Gate 后才可创建 PR。

## 结论

- 当前 findings：P0 0、P1 1、P2 0、P3 0。
- 历史 Round 1/2 findings 的代码与测试生命周期均已闭环；Round 4 新发现 1 个当前范围 Docs SSOT / active platform contract P1。
- Reviewed HEAD `f05cd662e852984f7f07cf6336d0867eb6532302` 不是零 finding，**不建议通过 Branch Review Gate，不予最终放行**。
- 修复该 P1、同步 canonical/dogfood/overlays/docs、补充回归测试并生成新 HEAD 后，应由新的独立闭环/最终 reviewer 重新覆盖完整 `origin/main...HEAD`。
