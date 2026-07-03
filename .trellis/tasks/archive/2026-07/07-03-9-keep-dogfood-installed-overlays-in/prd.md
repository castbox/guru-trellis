# #9 Keep dogfood installed overlays in sync with canonical preset overlays

## 目标

解决 GitHub issue #9：让本仓库 dogfood 安装副本与 canonical preset overlay 对齐，并提供可重复运行的漂移检查，避免 `.agents/.codex/.cursor/.claude` 等平台入口再次静默落后于 `trellis/presets/guru-team/overlays/`。

## 已确认事实

- Source issue: https://github.com/castbox/guru-trellis/issues/9。
- Base branch: `main`。
- 工作分支: `codex/9-keep-dogfood-installed-overlays-in`。
- 工作区: `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/9-keep-dogfood-installed-overlays-in`。
- 官方 Trellis 文档确认 workflow 行为应主要由 `.trellis/workflow.md` 控制，平台入口应引用 workflow，而不是分叉实现流程。
- 官方 Trellis 文档确认 spec template marketplace 应只放可复用工程约定，不能当远端 task/runtime state 存储。
- 本仓库当前 canonical overlay 已包含 Docs SSOT / Middle-platform Knowledge Gate 语义，但 dogfood installed copies 存在漂移。
- 本仓库没有 `docs/` 目录；长期维护说明位于 `README.md`、`trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md` 和 `.trellis/spec/`。

## 需求

1. 重新应用 Guru Team preset，使本仓库 dogfood installed overlay copies 与 canonical overlay 文件一致。
2. 增加一个只读 drift check，用于比较 `trellis/presets/guru-team/overlays/` 与本仓库相同相对路径的 installed dogfood copy；发现 missing / changed 时失败并输出报告。
3. 文档化维护规则：修改 canonical overlay 后必须同步或重新应用 dogfood installed copy，并运行 drift check。
4. 不覆盖未知用户改动；若 preset installer 产生 `.new` 或 `.bak`，必须记录并人工处理。
5. 不把 AI 判断写入脚本；drift check 只做确定性的文件存在和内容一致性验证。

## 验收标准

- [x] `trellis/presets/guru-team/overlays/.agents/skills/trellis-continue/SKILL.md` 与 `.agents/skills/trellis-continue/SKILL.md` 无差异。
- [x] `.codex/prompts` 与 `.codex/skills` 中的 Guru Team installed copies 与 canonical overlay 对齐。
- [x] 受 preset 声明支持的平台入口（包括 `.cursor` 与 `.claude` command overlay）与 canonical overlay 对齐或被 drift check 明确报告。
- [x] 新增 drift check 可重复运行，并在当前仓库对齐后通过。
- [x] README / workflow / preset 维护文档说明 drift check 的使用时机。
- [x] 验证命令覆盖 JSON、shell、Python compile、Trellis task 校验、overlay drift check、throwaway install 验证和 `git diff --check`。

## 非目标

- 不修改 Trellis npm 全局包、上游源码或 `node_modules`。
- 不改变 preset installer 的 `.new` / `.bak` 冲突处理语义。
- 不引入新的用户日常 workflow phase。
- 不重做 spec bootstrap，不修改业务仓库私有规则。

## Docs SSOT

- 本仓库没有 `docs/` 目录。
- 本任务改变的是 preset/workflow 维护合同，应更新 `README.md`、`trellis/presets/guru-team/README.md`、`trellis/workflows/guru-team/workflow.md`、`.trellis/workflow.md` 与相关 `.trellis/spec/`。

## Middle-platform Knowledge Gate

本任务修改 Trellis preset / overlay / companion validation，不涉及 go-guru、proto-guru、Unity3D Guru SDK、Flutter Guru SDK 等中台 SDK 或框架；Middle-platform Knowledge Gate 不适用。

## 用户确认

用户明确要求“解决 https://github.com/castbox/guru-trellis/issues/9”，随后触发 `trellis-continue`。本任务按 issue #9 验收标准进入实现，不扩大到平台筛选、installer 架构重写或 PR 发布策略变更。
