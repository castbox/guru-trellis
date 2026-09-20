# Issue #452 上游平台与 OpenCode 研究证据

研究日期：2026-09-19

## Authority

- 上游 checkout：`castbox/Trellis` remote-tracking ref `upstream/main`
- 上游 HEAD：`43fffc170927c85d9f7fc106cc5a059e80d4530b`
- 官方文档：`https://docs.trytrellis.app/index.md`
- 官方 workflow 文档：`https://docs.trytrellis.app/advanced/custom-workflow.md`

## Registry evidence

上游 `packages/cli/src/types/ai-tools.ts` 的 `AITool` 与 `AI_TOOLS` 是平台配置的 registry。当前 registry 的 22 个 `AITool` id 为：

`claude-code`, `cursor`, `opencode`, `codex`, `kilo`, `kiro`, `gemini`, `antigravity`, `devin`, `qoder`, `codebuddy`, `copilot`, `droid`, `dsh`, `pi`, `reasonix`, `zcode`, `trae`, `omp`, `grok`, `kimi`, `snow`。

该 registry 同时定义 `templateDirs`、`configDir`、`cliFlag`、默认选择和模板上下文，因此本 Issue 不应通过本仓库目录枚举推断“上游全平台”。实施时应读取/绑定该 registry 事实，并把无法完成 Guru public projection 与 actual-load 验证的平台列入 deferred inventory。

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

- `default_dogfood_platforms` 继续保持当前 Guru 默认行为（Codex/Cursor；按现有 installer 合同保留 Claude 的既有显式支持语义）。
- `guru_supported_platforms` 只有在 projection、ownership、manifest、reapply/update、throwaway 和 actual-load 都有可执行证据后才能加入；OpenCode 是本 Issue 目标。
- 其余 upstream registry 平台不因存在于上游 registry 就自动进入 `--all-platforms`；缺少 Guru 完整投影的项必须输出稳定 deferred/unsupported 结果。
