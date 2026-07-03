# Guru Trellis 项目通用指令

本仓库维护 Guru Team 对 Trellis 的可复用扩展：workflow marketplace、preset installer、平台入口 overlay、项目技能、spec 模板与少量 companion scripts。所有 AI Agent 在本仓库工作时，必须把“AI 判断流程”和“确定性脚本执行”严格分层。

## 1. 官方 Trellis 优先

修改任何 Trellis 扩展前，先对照官方文档，不要凭记忆或旧实现假设扩展方式。

必须优先参考：

- Trellis 官方文档首页：https://docs.trytrellis.app/
- 自定义 workflow：https://docs.trytrellis.app/advanced/custom-workflow
- 自定义 spec template marketplace：https://docs.trytrellis.app/advanced/custom-spec-template-marketplace

本仓库扩展必须遵从 Trellis 官方最佳实践：

- workflow 行为优先通过 `.trellis/workflow.md` 和 marketplace workflow 的 Markdown 定义；`workflow.md` 是 AI 运行时读取的流程合同，不通过修改 Trellis 上游源码、全局 npm 包、`node_modules`、hook 脚本或 companion script 实现流程分叉。
- skill routing、phase、workflow-state breadcrumb、review gate、finish/publish 规则应写在 Markdown workflow / skill / prompt / command overlay 中，让 AI 在运行时读取并执行。
- spec template marketplace 只放可复用工程约定、目录/API/测试/错误处理规则、review checklist 和去敏后的真实例子；不得放 active task、workspace journal、平台 prompt 文件、项目私有运行状态或只属于单一业务仓库的 PRD。
- template id、workflow id、preset 文件路径视为团队公共 API；破坏性调整要新建 id 或清晰记录迁移方式。

## 2. 核心边界：Markdown 定义流程，脚本执行事实

Markdown 控制面负责“过程”和“判断”：

- `.trellis/workflow.md`
- `trellis/workflows/guru-team/workflow.md`
- `.agents/skills/`
- `.codex/prompts/` 与 `.codex/skills/`
- `trellis/presets/guru-team/overlays/`
- `.trellis/spec/`

Python / shell 代码只负责确定性动作：

- 创建或检查 worktree、branch、commit、push、PR；
- 读取 Git/GitHub/Trellis 状态；
- 写入结构化 artifact；
- 校验 JSON/schema/hash/HEAD/diff range；
- 检查固定文件是否存在、内容是否满足机器可验证条件；
- 阻塞缺失证据或过期证据的后续步骤。

绝对不要把需要智能判断的步骤写进 Python / shell。只要某一步需要理解意图、权衡风险、判断充分性、发现遗漏、审查 diff、决定 issue close/ref/followup、判断 PR 是否 ready，就必须由 AI Agent 按 Markdown prompt/workflow/skill 执行。脚本可以记录和校验结果，但不能替代判断。

## 3. Companion Script 的允许角色

本仓库脚本只能扮演三类角色：

- Executor：按明确输入执行具体副作用，例如创建 worktree、提交、push、创建 PR。
- Validator：校验客观、机器可判定的条件，例如 schema、必填字段、HEAD 是否匹配、gate 是否过期。
- Recorder：把 AI/human 已审查过的结论写成结构化 artifact。

脚本不得扮演：

- Planner：决定需求含义、任务边界、是否需要新 issue。
- Reviewer：判断分支没有缺陷、实现满足需求。
- Product owner：决定 issue 关闭范围或 scope 扩张是否合理。
- Publisher of record：在没有 AI 审查的情况下生成最终 PR 论证、安全说明和验证声明。

如果某个 gate 需要脚本参与，顺序必须是：AI review / human confirmation 先发生，脚本随后 recorder / validator。不能反过来用 `--pass`、默认模板或脚本返回值冒充审查过程。

## 4. 必须保留的 AI 判断门禁

以下步骤必须由 AI Agent 明确执行判断，并把证据写入任务 artifact、review report、PR readiness report 或等价记录；脚本只能提供原始事实和阻塞校验。

- 判断用户请求是否需要 GitHub issue、Trellis task、worktree 或 branch。
- duplicate search 后决定复用 issue、强制创建新 issue，或把候选交给用户确认。
- 创建 GitHub issue、worktree、branch、Trellis task 前展示 handoff plan 并获得确认。
- `prd.md`、`design.md`、`implement.md` 是否足够进入实现；`task.py start` 只是状态写入，不代表规划已审查。
- 实现是否满足需求、设计、测试和兼容性约束。
- `trellis-check` 是否完整覆盖当前 task scope；不能用几个命令通过替代完整 check。
- 是否需要更新 `.trellis/spec/`。
- Branch Review Gate 是否覆盖完整 `origin/<base>...HEAD` diff，是否有 P0/P1/P2/P3 finding。
- `issue-scope-ledger.json` 中 `close_issues`、`related_issues`、`followup_issues` 是否正确。
- PR readiness：PR 标题、正文、验证结果、安全说明、部署影响、关闭 issue 语义是否真实充分。

## 5. 开箱即用门禁

任何修改 workflow / preset / marketplace / overlay / companion scripts 后，都必须验证“新仓库安装后开箱即用”。不能只验证当前 dogfood 仓库里的已安装副本。

最低验收要求：

- 从干净临时仓库或 throwaway repo 安装 workflow marketplace 和 preset。
- 验证 `trellis/index.json` 能被 Trellis 识别，`guru-team` workflow id、path、type 正确。
- 验证新项目可通过 `trellis init -u <name> --workflow guru-team --workflow-source gh:castbox/guru-trellis/trellis` 或 README 中等价命令安装 Guru Team workflow。
- 验证已有项目可通过 `trellis workflow --marketplace gh:castbox/guru-trellis/trellis --template guru-team --create-new` 预览，并在确认后用不带 `--create-new` 的命令切换目标 `.trellis/workflow.md`。
- 验证 preset installer 能安装 `.trellis/guru-team/`、平台 overlay、脚本、schema、配置模板，且脚本有可执行权限。
- 验证新安装项目在无历史 patch 的情况下可以运行 `get_context.py`、Phase 0 intake/preflight、planning、check、review gate、finish-work 的预期入口。
- 验证 Codex / Claude / Cursor 等声明支持的平台入口文案一致，不出现某个平台仍停留旧流程的情况。
- 验证 README 中给出的安装命令是真实可执行的，不依赖本机隐藏状态。

如果暂时无法跑完整 throwaway 安装，必须在最终说明中明确未验证项和风险，不能声称开箱即用。

## 6. Upgrade / Update 抗漂移门禁

本仓库扩展必须在官方 Trellis `upgrade` / `update` 后仍然可维护、可恢复、不会静默丢失。不要依赖对已安装生成文件的一次性 patch。

修改规则：

- 长期源头必须在本仓库 canonical 位置：`trellis/workflows/guru-team/`、`trellis/presets/guru-team/`、`trellis/index.json`、`trellis/presets/guru-team/overlays/`。
- 当前仓库 `.trellis/workflow.md`、`.agents/skills/`、`.codex/prompts/`、`.codex/skills/` 等 dogfood 安装副本只是运行副本；改动 canonical 后要同步 dogfood 副本，但不能把 dogfood 副本当作唯一源头。
- 每次修改 workflow/preset/overlay 后，要检查后续 `trellis update` 是否会覆盖、删除或回退这些文件；如果会，必须调整为官方支持的 marketplace / preset / overlay 机制。
- 旧版本上打过 patch 的文件不能因为“升级时未触碰”而继续保持旧状态；必须通过 canonical source、installer、hash/diff 或显式升级验证确认已迁移到新版本语义。
- 对会被 Trellis 官方模板管理的文件，必须了解 `.trellis/.template-hashes.json`、`.new`、`.bak` 或官方冲突处理语义；不得静默覆盖用户本地修改。
- 任何升级兼容性结论都要基于命令或 diff 证据：版本、安装路径、变更文件、被保留文件、`.new/.bak` 结果、重新应用 preset 后的状态。

## 7. 非 hack 扩展原则

优先使用 Trellis 官方扩展面：

- workflow marketplace 管理团队流程；
- spec template marketplace 管理可复用规范；
- skills / commands / prompts / hooks / sub-agents 管理平台入口；
- project-local `.trellis/spec/` 管理项目约定；
- companion scripts 只补充 Trellis 没有覆盖的确定性执行和校验。

不要：

- 修改 Trellis 上游源码、全局 npm 安装目录或 `node_modules` 来实现项目需求；
- 把业务仓库私有规则写入公共 marketplace / preset；
- 在 spec template 中放 `.trellis/tasks/`、`.trellis/workspace/`、平台 prompt 文件或 active task 状态；
- 用 hook/script 绕过 `.trellis/workflow.md` 中应由 AI 执行的流程；
- 在没有官方文档或本仓库证据的情况下发明 Trellis 行为。

## 8. 副作用控制

除非用户明确要求，或已经确认清晰 handoff plan，否则不要创建 GitHub issue、worktree、branch、Trellis task、commit、push 或 PR。

执行副作用前必须说明：

- 目标 GitHub repo / issue / PR；
- base branch、目标 branch、worktree path；
- 是否会写 `.trellis/tasks/`、`.trellis/guru-team/handoff.json` 或 workspace journal；
- 将 stage / commit / push 的文件；
- 将使用的命令和预期结果。

工作区有无关改动时，只能 stage 本次请求明确范围内的文件。不得 revert、覆盖、格式化或提交用户未授权的并行改动。

## 9. Evidence 与 Gate Artifact

所有关键 gate 都应留下可审计证据。良好的 gate artifact 至少记录：

- task 与 issue scope；
- 被审查的源文件、规划文件、spec、diff range 或 file hash；
- reviewer / AI process 身份；
- findings、severity、处理状态；
- 验证命令和结果；
- 当前 HEAD 或 working tree 状态；
- 阻塞/通过结论和理由；
- evidence 是否与当前 HEAD 匹配，是否 stale。

通过 gate 不能是空白断言。`summary` 和 `evidence` 必须说明实际审查了什么、为什么足够继续、哪些范围明确不受影响。

## 10. 安全与发布

不得在日志、issue、task artifact、PR body、review evidence 或命令输出中泄露 token、secret、private key、签名 URL、`.env`、数据库 URL、客户数据或敏感原始记录。

PR 发布前必须由 AI 审查 PR readiness，至少确认：

- PR title 和 body 是否为中文且具体；
- `Closes #xx` 只用于 `issue-scope-ledger.json` 中已完整验收并被 review gate 覆盖的 `close_issues`；
- `related_issues` / `followup_issues` 不被关闭；
- 验证结果不是泛化占位；
- 安全说明、部署影响、配置/脚本/schema/CI/CD/容器/K8s/DB migration/Makefile 影响判断真实完整；
- 如果未验证完整链路，PR body 和最终回复必须明确说明。

## 11. 本仓库工作方式

开始修改前先读当前文件，不要凭记忆修改。涉及 Trellis 架构或扩展时，使用 `trellis-meta` 相关说明，并以本仓库当前 canonical 文件为准。

修改 workflow 行为时，至少检查：

- `trellis/workflows/guru-team/workflow.md`
- `.trellis/workflow.md`
- `trellis/presets/guru-team/README.md`
- `trellis/workflows/guru-team/README.md`
- `trellis/presets/guru-team/overlays/`
- `.agents/skills/`
- `.codex/prompts/` 与 `.codex/skills/`

修改 preset installer 或 companion scripts 时，至少检查 canonical 脚本、安装副本、README、配置模板和 schema 是否一致。

最终报告要明确：改了什么、验证了什么、哪些开箱即用/upgrade-update 门禁已覆盖、哪些未覆盖。
