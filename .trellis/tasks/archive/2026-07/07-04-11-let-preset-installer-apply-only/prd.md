# #11 Let preset installer apply only selected platform overlays

## 目标

让 Guru Team preset installer 根据安装者选择的平台只应用对应平台 overlay，避免 `trellis init --codex --cursor` 后又由 preset 恢复 `.claude/` 等未选择平台入口。默认安装文档、升级 prompt、preset README、throwaway 验证都必须与 installer 实际参数一致。

## 已确认事实

- GitHub issue: https://github.com/castbox/guru-trellis/issues/11。
- 当前 installer 入口是 `trellis/presets/guru-team/scripts/bash/apply.sh`，实际逻辑在 `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`。
- `install_overlays()` 当前递归遍历 `trellis/presets/guru-team/overlays/` 下全部文件，因此会安装 `.claude/commands/trellis/continue.md` 与 `.claude/commands/trellis/finish-work.md`。
- 当前 CLI 参数只有 `--repo` 与 `--json`，无法表达平台选择。
- overlay 目录当前包含共享 `.agents/skills/`、Codex `.codex/`、Cursor `.cursor/`、Claude `.claude/` 四组入口。
- 顶层 `README.md` 默认安装/升级 prompt 要求只启用 Codex + Cursor，并要求清理未选择平台目录；这与当前 installer 行为冲突。
- 仓库没有 `docs/` 目录；长期公开文档 SSOT 是顶层 `README.md` 与 `trellis/presets/guru-team/README.md`。

## 需求

1. `apply.sh` / Python installer 支持显式平台过滤参数。
2. `--platform <name>` 可重复指定平台；本任务至少支持 `codex`、`cursor`、`claude`，并为未来平台保留集中映射。
3. 默认平台范围为 `codex` + `cursor`，与 README 当前默认安装/升级语义一致。
4. 共享 `.agents/skills/` overlay 始终安装，不受平台过滤影响。
5. `--all-platforms` 保留历史全量安装行为，用于需要所有 overlay 的维护或特殊仓库。
6. 只选择 Codex + Cursor 时，preset apply 不创建 `.claude/`；重复 apply 也不能恢复 `.claude/`。
7. README 的非交互命令、AI 安装 prompt、升级 prompt 必须展示与 installer 一致的参数。
8. preset README 必须说明默认平台范围、`--platform` 用法、`--all-platforms` 全量安装方式和安装文件范围。
9. throwaway install 验证覆盖 Codex + Cursor 场景，并断言未创建 `.claude/`。

## 非目标

- 不修改 Trellis upstream、全局 npm 包或 `node_modules`。
- 不改变 `.trellis/workflow.md` / marketplace workflow 行为。
- 不删除 canonical `trellis/presets/guru-team/overlays/.claude/` 文件；只控制安装目标。
- 不为目标 repo 自动清理已经存在的未选择平台目录；本任务保证不会新建或恢复未选择平台 overlay。
- 不实现从目标 repo 已有目录自动推断平台选择；平台范围由 installer 参数决定。

## 验收标准

- [ ] `python3 -m unittest trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py` 通过，并覆盖平台过滤、重复 apply、不合法平台、`--all-platforms`。
- [ ] `python3 -m py_compile trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py` 通过。
- [ ] `bash -n trellis/presets/guru-team/scripts/bash/apply.sh trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh` 通过。
- [ ] throwaway 验证脚本在 Codex + Cursor 默认路径断言 `.claude/` 不存在。
- [ ] README 与 preset README 的命令和说明不再要求安装后人工清理默认未选择平台 overlay。
- [ ] 本仓库 dogfood overlay drift check 按要求执行；若没有修改 overlay 文件，应记录无需重新 apply dogfood overlay 的判断。

## Repo Docs SSOT

本仓库没有 `docs/` 目录。本任务会更新长期公开说明 `README.md` 与 `trellis/presets/guru-team/README.md`；任务 artifacts 只保存本次规划、验证和 review 证据。

## 中台知识门禁

本任务只修改 Trellis preset installer、本仓库公开文档和本地验证脚本，不涉及 Guru Team middle-platform SDK 或框架；Middle-platform Knowledge Gate 不适用。
