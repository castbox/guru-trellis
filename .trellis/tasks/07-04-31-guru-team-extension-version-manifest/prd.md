# #31 Add Guru Team extension version manifest and installed provenance

## 需求来源

- GitHub issue: <https://github.com/castbox/guru-trellis/issues/31>
- Task: `.trellis/tasks/07-04-31-guru-team-extension-version-manifest`
- Base branch: `main`
- Task branch: `codex/31-guru-team-extension-version-manifest`

用户要求开始解决 issue #31：为 `guru-team` Trellis extension 建立独立版本号、安装态
provenance 和用户可直接查看的版本入口，便于跨业务 repo 排障、复现、升级和回滚。

## 背景问题

当前仓库提供的是团队级 Trellis extension bundle，而不是官方 Trellis CLI。它包含 workflow
marketplace、preset installer、managed companion assets、platform overlays 和公开安装/升级文档。

现状缺口：

1. `trellis --version` 和 `.trellis/.version` 只表示官方 Trellis CLI / project template 版本。
2. `trellis/index.json` 的 `version: 1` 是 marketplace index schema version，不应被误用为 extension version。
3. 业务 repo 安装或升级后，没有稳定入口能回答当前安装的 Guru Team extension version、来源 repo/ref/commit、source tree state、selected platforms 和 Trellis CLI 兼容范围。
4. README install / upgrade prompt 只要求报告 Trellis CLI version，没有要求报告 Guru Team extension version 和 provenance。

## 目标

### R1. 独立扩展版本

- 新增 repo 内 canonical manifest，作为 `guru-team` extension version 的唯一来源。
- 明确区分 official Trellis CLI version、`.trellis/.version`、`trellis/index.json.version`、Guru Team extension version。
- 初始版本使用 `0.1.0`，表达 public API 仍处于收敛期。

### R2. Public API 与 SemVer 合同

公开文档要说明 Guru Team extension public API 至少包括 workflow template id、managed install
paths、companion script CLI、config keys、artifact schemas / JSON output fields、platform overlay
entrypoints 和 `.new` / `.bak` upgrade conflict behavior。

SemVer 规则：

- patch：兼容 bugfix、文案澄清、非破坏性 guardrail 修正；
- minor：兼容新增字段、脚本能力、platform overlay、可选门禁；
- major：破坏 workflow id、script CLI、artifact schema、installed path、默认行为或升级语义。

### R3. 安装态 provenance

preset installer 在目标 repo 写入 `.trellis/guru-team/extension.json`，记录 canonical manifest 摘要、
`installed_at`、`source_repo`、`source_ref`、`source_commit`、`source_tree_state`、selected platforms
和 installed managed asset summary。

不得记录 token、`.env`、GitHub auth detail、signed URL 或不必要的本机-only 敏感路径。

### R4. 用户可查询入口

- `check-env.sh --json` 输出 `guru_team_extension` 节点。
- 新增 `.trellis/guru-team/scripts/bash/version.sh --json` 作为直接查询入口。
- `apply.sh --version` 或 installer JSON output 显示 source extension version。

### R5. 文档和 prompt 更新

- README 安装/升级 prompt 要求报告 Trellis CLI version、Guru Team extension version、Guru Team source ref/commit、selected platforms、source tree 是否 mutable/dirty。
- `trellis/presets/guru-team/README.md` 说明 installed manifest 文件。
- `trellis/workflows/guru-team/README.md` 说明 workflow marketplace 与 extension version 的关系。
- `docs/requirements/requirement-main.md` 追加 #31 对版本治理能力的覆盖。

### R6. 验证和回归

- 单测覆盖 manifest 读取、installed manifest 写入、source state、check-env output。
- throwaway install verification 检查 installed manifest 和 `check-env --json`。
- dogfood repo 重新 apply preset 后无 overlay drift。

## 非目标

- 不修改官方 Trellis CLI、全局 npm 包、`node_modules` 或 Trellis upstream。
- 不把智能判断写入脚本。脚本只做 deterministic reader / recorder / validator。
- 不实现完整 signed SLSA provenance；本任务只记录可追踪 source/ref/commit。
- 不新建 workflow id。
- 不把 active task、workspace journal 或平台私有 runtime state 放入 marketplace / manifest。

## Docs SSOT

本 repo 已有 durable docs：

- `docs/requirements/README.md`
- `docs/requirements/requirement-main.md`

本任务应更新 `docs/requirements/requirement-main.md`，把 #31 作为 P1 安装/升级/开箱验证能力的一部分。
README / workflow README / preset README 是公开安装与维护 SSOT，也必须同步。

## 中台知识门禁

本任务修改 Trellis workflow/preset/docs/companion scripts，不涉及 go-guru、proto-guru、Unity3D Guru SDK、
Flutter Guru SDK 或中台框架 API；Middle-platform Knowledge Gate 不适用。

## 验收标准

- [ ] 存在 canonical `guru-team` extension manifest，且不是 `trellis/index.json.version`。
- [ ] preset installer 安装 `.trellis/guru-team/extension.json`。
- [ ] installed manifest 含 version、workflow template id、source repo/ref/commit、source tree state、selected platforms、installed timestamp。
- [ ] `check-env.sh --json` 输出 `guru_team_extension`。
- [ ] `version.sh --json` 可直接查看 Guru Team extension version/provenance。
- [ ] README install / upgrade prompt 报告 Guru Team extension version 和 provenance。
- [ ] preset README 和 workflow README 说明 extension version / installed manifest。
- [ ] `docs/requirements/requirement-main.md` 更新 #31 能力。
- [ ] throwaway install verification 覆盖 installed manifest 与 check-env output。
- [ ] 现有 config preservation、`.new` / `.bak` conflict handling、platform selection 不回退。
- [ ] 脚本仍只做 deterministic 事实读取、记录和校验，不替代 AI/human 判断。
