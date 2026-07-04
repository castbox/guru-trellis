# 实施计划

## 执行清单

1. 在 `apply_guru_team_trellis_preset.py` 中新增平台常量、参数解析和 overlay 过滤。
2. 调整 `install_assets()` / `install_overlays()` 函数签名，让平台选择贯穿到复制逻辑和 JSON payload。
3. 补充 `test_apply_guru_team_trellis_preset.py`，覆盖默认 Codex + Cursor、重复 apply、Claude 显式选择、`--all-platforms` 和非法/互斥参数。
4. 更新 `verify-throwaway-install.sh`，用显式 `--platform codex --platform cursor` 调用 preset，并断言 `.claude/` 不存在。
5. 更新顶层 `README.md` 安装/升级命令和 AI prompt，移除默认路径依赖人工清理的表述。
6. 更新 `trellis/presets/guru-team/README.md`，说明默认平台、显式平台、全量安装和 installed files 分组。
7. 运行验证命令，记录结果到 Phase 2 check。

## 验证命令

```bash
python3 -m unittest trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py
python3 -m py_compile trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py
bash -n trellis/presets/guru-team/scripts/bash/apply.sh trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh
python3 -m json.tool trellis/index.json
git diff --check
python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-04-11-let-preset-installer-apply-only
```

如当前分支修改了 `trellis/presets/guru-team/overlays/`，还必须运行：

```bash
trellis/presets/guru-team/scripts/bash/apply.sh --repo .
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
```

本计划不修改 canonical overlay 文件；若最终 diff 确认未触碰 `overlays/`，记录无需 dogfood overlay re-apply 的判断，并可直接运行 read-only drift check。

## 重点检查

- 默认 apply 不创建 `.claude/`。
- `--all-platforms` 仍保留历史全量行为。
- `--platform claude` 可安装 Claude overlay。
- README 中所有 apply 命令都与新参数一致。
- 无 `.new` / `.bak` 被静默留下。
- 不提交 `.trellis/.developer`、`.env`、token、私钥或本机-only 配置。
