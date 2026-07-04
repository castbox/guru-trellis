# 设计：preset installer 平台过滤

## 边界

修改范围限定在 preset installer、installer 单测、throwaway 验证脚本、顶层 README 和 preset README。canonical overlay 文件本身不变；workflow marketplace、companion scripts、schema 和 active dogfood workflow 不变。

## CLI 合同

- `--platform <name>`：可重复参数，指定要安装的平台 overlay。
- 支持平台初始集合：`codex`、`cursor`、`claude`。
- 默认值：未传 `--platform` 且未传 `--all-platforms` 时，使用 `codex` + `cursor`。
- `--all-platforms`：安装所有已知平台 overlay，等价于历史全量行为。
- `--platform` 与 `--all-platforms` 互斥；同时传入时 fail closed。
- 不合法平台名称由 argparse choices 或集中校验阻塞，避免静默跳过。

## Overlay 分组

采用集中映射而不是散落路径判断：

- `ALWAYS_OVERLAY_PREFIXES`: `.agents/`
- `PLATFORM_OVERLAY_PREFIXES`:
  - `codex`: `.codex/`
  - `cursor`: `.cursor/`
  - `claude`: `.claude/`

`install_overlays(repo, guru_root, platforms)` 只复制共享 prefix 和所选平台 prefix 下的 overlay 文件。输出 payload 增加 `platforms` 与 `all_platforms` 信息，便于安装日志和验证脚本审计。

## 兼容性

- 默认行为从历史“安装全部 overlay”调整为“安装 Codex + Cursor + 共享 overlay”，这是 issue 明确要求的策略调整。
- 需要历史行为的维护者可显式使用 `--all-platforms`。
- 已存在的目标仓库 `.claude/` 不会被本任务删除；installer 只保证未选择平台不会被新建或更新。
- overlay conflict 处理继续使用现有 `copy_overlay()`：缺失安装、相同跳过、已知 Trellis 生成入口替换、未知本地改动写 `.new`。

## 文档同步

- `README.md` 非交互安装命令追加 `--platform codex --platform cursor`，让复制命令显式表达默认平台。
- AI 安装/升级 prompt 中的 apply 命令同步追加平台参数，并把“清理未选择平台目录”改为“确认 installer 未创建未选择平台 overlay；若历史目录已存在，说明并请用户确认是否清理”。
- `trellis/presets/guru-team/README.md` 增加平台选择说明，并把 Installed Files 从固定全量列表调整为共享文件、默认平台文件和 Claude 可选文件三组。

## 验证设计

- 单测直接调用 Python 函数，在临时 repo 中构造 `.trellis/` 后执行 `install_assets(..., platforms={...})` 或 CLI 解析相关路径，验证文件存在/不存在。
- 默认 Codex + Cursor 场景断言 `.agents/`、`.codex/`、`.cursor/` 存在且 `.claude/` 不存在。
- 重复 apply 场景断言未选择平台不会在第二次恢复。
- `--all-platforms` 场景断言 `.claude/` 被安装。
- throwaway 验证脚本在 `apply.sh --platform codex --platform cursor` 后加入 `test ! -e "$TARGET/.claude"`。

## 风险与回滚

- 风险：平台映射遗漏新增 overlay prefix，导致未来新增平台文件未被安装。缓解：集中常量、README 说明、单测覆盖当前平台；未来新增平台时只扩展映射。
- 风险：默认行为改变影响依赖 Claude 默认安装的仓库。缓解：README 明确 `--all-platforms` 和 `--platform claude`，并在 payload 输出平台范围。
- 回滚：恢复 `install_overlays()` 全量遍历，或在命令中使用 `--all-platforms` 获取历史行为。
