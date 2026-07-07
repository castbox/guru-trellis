# #72 默认 sub-agent mode 下强制 implement、check 与 branch review 均由 subagent 执行

## 目标

在 Guru Team 默认 `sub-agent` mode 下，主 agent 必须真实调度并等待三个独立 subagent 边界：

- `trellis-implement` / channel `implement` 负责实现。
- `trellis-check` / channel `check` 负责 Phase 2 check。
- commit 后的 Branch Review 由独立 review subagent 完成。

主 agent 只负责规划、调度、等待/恢复/替换、记录 evidence、commit、review gate recorder 与 finish 前准备；Python / shell 只做 executor、recorder、validator。不得用主 agent 自己实现、自检、自审或脚本校验通过来冒充上述 subagent 工作。

## 需求

- 更新 canonical workflow 与 dogfood workflow，明确默认 `sub-agent` mode 的三个强制 subagent 执行边界。
- 更新 `trellis-continue` 相关 overlay / prompt，让主 agent 在 `in_progress` 和 commit 后路径中明确只做协调，不直接替代实现、Phase 2 check 或 Branch Review。
- 更新 `trellis-implement` overlay，要求实现代理读取 task artifacts / spec / JSONL，完成修改并输出实现 handoff；不得把未完成工作报告为 completed。
- 更新 `trellis-check` overlay，要求 Phase 2 check 基于实现后的真实 diff、task artifacts、spec、durable docs 责任和验证命令完成，发现问题时返回实现修复或自修复，不把命令结果或脚本结果冒充 AI check。
- 更新 Branch Review handoff 文案，要求 review subagent 审查完整 `origin/<base>...HEAD` diff，不继续实现、不替 implement/check 代理补工作，输出可被 #44 Branch Review Gate 规则消费的 report。
- 明确 `phase2-check.json` 是 Guru Team 固化 `trellis-check` AI check 结论与验证证据的 artifact，不是 Trellis 原生步骤本身，也不是脚本替代 AI check 的入口。
- 明确 inline/self-exemption 只在有 artifact evidence 时成立；默认 sub-agent mode 下缺少 implement/check/review subagent evidence 必须 fail closed。
- 保持 #43 的 agent identity 模型、#44 的 Branch Review Gate pass 语义、#62 的 wait timeout / stale / unfinished termination 合同不被复制、改写或弱化。

## 非目标

- 不修改 Codex UI agent display name。
- 不重设 `agent-assignment.json` 的身份模型。
- 不重写 #44 的 Branch Review Gate pass 条件。
- 不把 Phase 2 check 收进 `trellis-implement` 的完成定义。
- 不把实现充分性、check 充分性、review 充分性等 AI 判断写进 Python / shell。
- 不修改官方 Trellis npm 包、`node_modules` 或上游源码。

## Durable Docs SSOT

仓库存在 durable docs：`docs/requirements/requirement-main.md` 与 `docs/requirements/guru-team-trellis-flow.md`。本任务改变长期 workflow 行为合同，应同步更新对应 durable requirements / README 文档中关于 subagent 边界、主 agent 协调边界、`phase2-check.json` 证据语义和 Branch Review review subagent 的说明。

## Middle-platform Knowledge Gate

不适用。本任务修改 Trellis workflow / preset / overlay 文档和 companion evidence contract，不涉及 go-guru、proto-guru、Unity、Flutter 或其他中台 SDK/framework。

## 验收标准

- 默认 `sub-agent` mode 下，workflow 明确要求实现必须由 `trellis-implement` / channel `implement` 执行。
- 默认 `sub-agent` mode 下，workflow 明确要求 Phase 2 check 必须由 `trellis-check` / channel `check` 执行。
- 默认 `sub-agent` mode 下，workflow 明确要求 Branch Review 必须由 review subagent 执行。
- `trellis-implement` overlay 明确承担读取 PRD/design/implement/spec、完成实现、输出实现 handoff。
- `trellis-check` overlay 明确承担检查实现 diff、task artifacts、spec/docs/overlay/config/test、验证命令、findings、剩余风险，并输出可支撑 `phase2-check.json` 的 evidence。
- Branch Review subagent 明确承担审查完整 `origin/<base>...HEAD` diff，不继续实现，并输出可被 #44 Branch Review Gate 消费的 review report。
- `phase2-check.json` 被明确为固化 `trellis-check` AI check 结论和验证证据的 Guru Team artifact；脚本记录不能替代 `trellis-check`。
- 文档明确区分 subagent 执行工作、主 agent 协调流程、Python / shell recorder/validator。
- 主 agent 直接实现、主 agent 直接 check、主 agent 自审或脚本校验通过都不能替代三个 subagent 边界。
- inline/self-exemption 必须有明确 artifact evidence，否则 fail closed。
- 不改变 #43、#44、#62 的既有边界和语义。
- 修改 canonical overlay 后，dogfood installed copies 同步且 drift check 通过。
- 运行 workflow / preset 相关验证命令；如无法完成开箱即用或 upgrade/update 验证，最终说明明确未覆盖项和风险。
