# Issue #452 上游平台与 OpenCode 研究证据

研究日期：2026-09-19；2026-09-20 按 live Issue #452 superseding platform-contract amendment 刷新结论

## Authority

- 上游 checkout：`castbox/Trellis` remote-tracking ref `upstream/main`
- 上游 HEAD：`43fffc170927c85d9f7fc106cc5a059e80d4530b`
- 官方文档：`https://docs.trytrellis.app/index.md`
- 官方 workflow 文档：`https://docs.trytrellis.app/advanced/custom-workflow.md`

## Registry evidence

上游 `packages/cli/src/types/ai-tools.ts` 的 `AITool` 与 `AI_TOOLS` 是平台配置的 registry。当前 registry 的 22 个 `AITool` id 为：

`claude-code`, `cursor`, `opencode`, `codex`, `kilo`, `kiro`, `gemini`, `antigravity`, `devin`, `qoder`, `codebuddy`, `copilot`, `droid`, `dsh`, `pi`, `reasonix`, `zcode`, `trae`, `omp`, `grok`, `kimi`, `snow`。

该 registry 同时定义 `templateDirs`、`configDir`、`cliFlag`、默认选择和模板上下文，因此本 Issue 不应通过本仓库目录枚举推断“上游全平台”。canonical inventory 必须同时保存 `AITool` id 与唯一 `cliFlag`；public `--platform` 和 installed `selected_platforms` 使用 `cliFlag`。例如 canonical id `claude-code` 对应 public value `claude`，两者不得混为一个字段。

## OpenCode native projection evidence

上游 registry 对 OpenCode 的配置为：

- id：`opencode`
- template dirs：`common`, `opencode`
- config dir：`.opencode`
- CLI flag：`opencode`
- default checked：`false`
- agent capable：`true`
- hooks：`false`

上游平台文档与模板结构进一步确认：

- skills：`.opencode/skills/`
- agents：`.opencode/agents/`
- plugins/extensions：`.opencode/plugins/`
- commands：`.opencode/commands/`

因此 Guru projection 不能只复制 `.opencode/skills/`；必须按本仓库 public contract 明确 commands/skills、managed paths、ownership、manifest、reapply/update 与 actual-load 行为。由于 OpenCode 没有 session-start hook，actual-load 还必须验证其 command/prelude fallback，而不能把 hook 文件存在当作加载证明。

## Official extension boundary

官方 custom workflow 文档说明：项目 workflow 行为由 `/.trellis/workflow.md` 定义，扩展应通过 workflow Markdown、skills、commands 与 marketplace/template 机制承接；不需要修改 Trellis Python、hook 或全局安装。该边界与仓库 `AGENTS.md` 一致，本 Issue 只修改 Guru Team canonical preset、projection、validator、README/spec 与测试。

## Scope consequence

以下结论以 2026-09-20 live Issue amendment 为 current authority；此前“三层/Guru-supported/deferred”研究假设已废弃：

- registry 全部 22 个 `cliFlag` 都必须具有完整 descriptor/projection；缺少任一平台是 blocking defect，不是 deferred success。
- repeated `--platform <cli-flag>` 是唯一显式选择入口；公开 CLI 不提供全集安装快捷方式。
- 未提供 `--platform` 时固定选择 `claude,codex,cursor`；这只是新安装默认策略。guru-trellis dogfood 也显式安装这三个值。
- 业务仓库升级从目标 manifest/provenance 读取 exact `cliFlag` selection 并原样 reapply，不从 source dogfood、默认值或完整 inventory 推断。
- OpenCode 是普通 upstream member；其代表性 actual-load 验证不把其提升为独立中间层。
