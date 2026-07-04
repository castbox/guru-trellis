# #27 让 finish-work --dry-run 成为真正无副作用的 readiness preview

## 目标

修复 Guru Team companion helper 中 `finish-work --dry-run` 的危险语义：dry-run 必须只做客观 readiness 校验与 planned action 输出，不得 archive task、写 journal、写 metadata、创建 metadata commit、push branch 或创建 PR。

## 需求来源

- GitHub issue: https://github.com/castbox/guru-trellis/issues/27
- Handoff: `.trellis/guru-team/handoff.json`
- Intake base: `main`
- Task branch: `codex/27-finish-work-dry-run-readiness`
- Worktree: `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/27-finish-work-dry-run-readiness`

## 需求

- `finish-work --dry-run --from-trellis-finish-work` 在通过 review gate、dirty path、PR body/readiness 等校验后，必须在任何 archive、journal、metadata commit、publish 副作用前返回 JSON plan。
- dry-run plan 至少包含 review gate 路径、reviewed HEAD、dirty path 检查结果、PR body source/readiness 结果、journal 前置计划、将要 archive 的 task、将要 publish 的 PR base/head/title/body source/draft 状态。
- 正式 `finish-work` 行为保持不变：非 dry-run 仍按当前流程 archive task、记录 journal、提交 Trellis metadata，然后由内部 marker 调用 publish。
- parser help 必须从“Run archive/journal, then dry-run publish”改成无副作用 readiness preview 语义。
- 相关单测必须反转 dry-run 预期：dry-run 不调用 `task.py archive`、不调用 `add_session.py`、不调用 `commit_if_metadata_dirty`，且不通过 publish 产生 push/PR 副作用。
- canonical workflow companion 与 dogfood 安装副本必须同步。
- 文档必须说明 dry-run 是无副作用 preview，throwaway install 验证不能依赖 dry-run 执行 archive/journal。

## 非目标

- 不改变正式 `finish-work` 的 archive/journal/publish 链路。
- 不处理 worktree `.trellis/.developer` 继承问题，该问题属于 #26。
- 不把智能判断写入 Python / shell；脚本只做机器可判定的 readiness 校验和计划输出。
- 不修改 Trellis 上游源码、全局 npm 包或 `node_modules`。

## Docs SSOT 与知识门禁

- 本仓库没有独立 `docs/` 目录；长期文档 SSOT 是 `README.md`、`trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md` 与 reusable workflow 文档。
- 本任务改变的是 Guru Team companion helper 的 dry-run 语义和用户文档，需要同步以上 README / workflow surfaces。
- Middle-platform Knowledge Gate 不适用：本任务不涉及 go-guru、proto-guru、Unity/Flutter SDK 或 Guru 中台框架。

## 验收标准

- `finish-work --dry-run --from-trellis-finish-work` 不修改 `git status --porcelain` 输出。
- dry-run 后 active task 不移动到 `.trellis/tasks/archive/`。
- dry-run 后不新增或修改 `.trellis/workspace/<developer>/journal-*.md`。
- dry-run 后不产生 commit。
- dry-run JSON 输出包含 archive/journal/publish plan 与 readiness 结果。
- 相关 Python 单测通过。
- `python3 -m json.tool trellis/index.json`、Bash syntax、Python compile、task validate、dogfood overlay drift、`git diff --check` 通过。
- 如无法完成 throwaway install 验证，最终报告必须列出未覆盖项与风险。
