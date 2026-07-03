# #9 设计

## 边界

本任务只处理 canonical overlay 与本仓库 dogfood installed copy 的同步与漂移验证。长期源头仍是：

- `trellis/presets/guru-team/overlays/`
- `trellis/workflows/guru-team/`
- `trellis/index.json`

Dogfood installed copy 仍是运行副本：

- `.agents/skills/`
- `.codex/prompts/`
- `.codex/skills/`
- `.cursor/commands/`
- `.claude/commands/`

## 同步策略

使用现有 preset installer 重新应用 overlay：

```bash
trellis/presets/guru-team/scripts/bash/apply.sh --repo .
```

理由：

- 该 installer 已实现 missing install、identical skip、known Guru/Trellis entry replacement 和 unknown local edit `.new` 保护。
- 直接复制文件会绕过 `.new` / `.bak` 语义，不符合本仓库 AGENTS 与 preset spec。

## Drift Check

新增只读验证脚本：

```text
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
```

脚本职责：

- 定位仓库根目录与 canonical overlay root。
- 遍历 `trellis/presets/guru-team/overlays/` 下所有文件。
- 对每个相对路径检查本仓库是否存在 installed dogfood copy。
- 使用 `cmp -s` 判断内容一致性。
- 输出 missing / changed 报告；任何差异返回非 0。

脚本不负责：

- 自动修复漂移。
- 判断语义是否合理。
- 决定是否覆盖本地改动。
- 替代 AI review / Branch Review Gate。

## 文档更新

维护说明需要同时出现在：

- `README.md`：维护原则和常用验证命令。
- `trellis/presets/guru-team/README.md`：preset maintainer 如何检查 dogfood overlay drift。
- `trellis/workflows/guru-team/workflow.md` 和 `.trellis/workflow.md`：Phase 3 review / validation 覆盖 overlay drift check。
- `.trellis/spec/preset/overlay-guidelines.md` 和 `.trellis/spec/workflow/quality-guidelines.md`：未来开发前置规范。

## 兼容性

- 新脚本位于 source repository 的 maintainer 工具路径，不加入 `MANAGED_ASSET_PATHS`，因此不会安装到业务仓库。
- 重新 apply preset 可能新增本仓库缺失的 `.claude/commands/trellis/*` dogfood entry；这与 preset installed files 清单一致。
- 若生成 `.new` 或 `.bak`，本任务必须停下检查，不能静默提交。

## 风险

- 当前 installer 会无条件安装所有 overlay 平台入口；本任务不改变该行为。
- Drift check 会要求 canonical overlay 中声明的所有文件在 dogfood copy 中存在，因此会暴露 `.claude` 这类以前缺失的 installed copy。
