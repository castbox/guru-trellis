# #26 worktree 创建后应继承 Trellis developer identity

## 目标

修复 Guru Team `prepare-task.sh --create-worktree` / `--create-task` 在创建或复用 task worktree 后没有可用 `.trellis/.developer` 的问题，确保新 task worktree 能立即运行 `get_context.py`、`add_session.py`、`task.py list --mine` 等依赖 developer identity 的 Trellis 步骤。

## 背景与证据

- Issue: https://github.com/castbox/guru-trellis/issues/26。
- `.trellis/.developer` 是 Trellis 本地 runtime identity，并被 `.trellis/.gitignore` 忽略，不存在于 base branch。
- 当前 `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py::prepare_workspace()` 只执行 `git worktree add` / 复用 existing worktree，没有复制或初始化 `.trellis/.developer`。
- 本 task 创建出的 worktree 已复现问题：第一次运行 `python3 ./.trellis/scripts/get_context.py` 返回 `ERROR: Not initialized. Run: python3 ./.trellis/scripts/init_developer.py <name>`。
- 当前 `infer_assignee()` 直接读取整个 `.trellis/.developer` 文件内容，导致 `create_task_command --assignee` 可能变成多行 `name=wumengye\ninitialized_at=...`，而不是 developer 名字。

## 需求

1. `prepare-task` executor 路径在创建或复用 worktree 后必须确保目标 worktree 有 `.trellis/.developer`。
2. 优先从发起 preflight 的源 checkout 复制 `.trellis/.developer` 到目标 worktree，保持 runtime identity 与源 checkout 一致。
3. 当用户显式提供 `--assignee` 或脚本能解析出 developer 名字时，如果源 checkout 缺失 `.trellis/.developer`，可以在目标 worktree 初始化等价 developer identity。
4. 当源 checkout 缺失 `.trellis/.developer` 且没有可用 developer 名字时，executor 路径必须 fail closed，并输出恢复命令，不要等 finish-work / journal 阶段才失败。
5. `infer_assignee()` 必须解析 `.trellis/.developer` 的 `name=` 字段，避免把整个 identity 文件内容当作 assignee。
6. 更新 canonical workflow / preset README 或 workflow text，说明 executor worktree developer identity 继承/初始化语义。
7. 同步 canonical 与 dogfood 安装副本，确保当前 dogfood 仓库和新安装项目使用同一脚本语义。

## 非目标

- 不处理 `finish-work --dry-run` 仍执行 archive / journal / metadata commit 的语义问题。
- 不修改 Trellis upstream npm 包、`node_modules` 或全局安装目录。
- 不把需要 AI 判断的流程放进脚本；脚本只做 deterministic executor / validator / recorder。

## Docs SSOT 与中台知识

- 本仓库没有 `docs/` 目录。长期 SSOT 是 `README.md`、`trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md`、`.trellis/spec/`、canonical workflow / preset 文件与 dogfood 安装副本。
- 本任务只涉及 Guru Team Trellis companion scripts、workflow/preset 文档与本地 runtime identity，不涉及 Guru Team 中台 SDK / framework；Middle-platform Knowledge Gate 不适用。

## 验收标准

- [ ] 新增/更新单测覆盖 `--create-worktree` 后目标 worktree 获得 `.trellis/.developer`。
- [ ] 单测覆盖源 checkout 缺失 `.trellis/.developer` 且无 assignee 时 executor 路径阻塞，并包含恢复命令。
- [ ] 单测覆盖源 checkout 缺失 `.trellis/.developer` 但显式 `--assignee` 可初始化目标 identity。
- [ ] 单测覆盖 `infer_assignee()` 从 `.trellis/.developer` 的 `name=` 字段解析出 `wumengye` 这类 developer 名字。
- [ ] `python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py` 通过。
- [ ] `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh` 通过。
- [ ] `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py` 通过。
- [ ] 运行 preset apply 同步 dogfood 安装副本，并通过 `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`。
- [ ] 通过 throwaway 或等价验证证明新仓库安装后 `prepare-task --create-worktree` 能创建带 developer identity 的 worktree；若无法完整验证，最终报告明确未验证项和风险。
