# #31 实施计划

## 前置上下文

已读取：

- GitHub issue #31 正文；
- `.trellis/spec/docs/*`；
- `.trellis/spec/preset/*`；
- `.trellis/spec/workflow/*`；
- `.trellis/spec/guides/*`；
- README、preset README、workflow README、durable requirements docs；
- installer 和 workflow helper 当前代码。

Middle-platform Knowledge Gate：不适用。

## 实施步骤

1. 新增 canonical manifest
   - 创建 `trellis/guru-team-extension.json`。
   - 使用 SemVer `0.1.0`。
   - 写明 Trellis CLI compatibility、workflow id、public API 高层路径。

2. 扩展 preset installer
   - 增加 manifest/provenance helper。
   - 写入 `.trellis/guru-team/extension.json`。
   - `main()` JSON output 增加 `guru_team_extension`。
   - 支持 `apply.sh --version`。
   - 加入 `version.sh` managed asset。

3. 扩展 workflow helper
   - 新增 `version` subcommand。
   - `check-env --json` 输出 `guru_team_extension`。
   - missing/invalid installed manifest 只 warning，不让 check-env 整体失败。

4. 同步 canonical 与 dogfood managed assets
   - 新增 `trellis/workflows/guru-team/scripts/bash/version.sh`。
   - 通过 preset apply 同步 `.trellis/guru-team/**` dogfood copy。
   - 如产生 `.bak` 或 `.new`，逐个处理。

5. 更新文档
   - `README.md` 安装/升级命令、prompt、最小验证和版本治理说明。
   - `trellis/presets/guru-team/README.md` installed files 与 manifest/provenance 说明。
   - `trellis/workflows/guru-team/README.md` marketplace/version 分层说明。
   - `docs/requirements/requirement-main.md` 记录 #31 能力。

6. 更新测试
   - `test_apply_guru_team_trellis_preset.py` 覆盖 installed manifest、`--version`、selected platforms。
   - `test_guru_team_trellis.py` 覆盖 check-env/version output、missing/invalid manifest。
   - `verify-throwaway-install.sh` 覆盖 installed manifest 和 `check-env.guru_team_extension`。

7. 验证
   - JSON / bash / py_compile 基础校验。
   - 运行两个 Python unittest 文件。
   - 运行 `apply.sh --repo . --all-platforms`。
   - 运行 `check-dogfood-overlay-drift.sh`。
   - 运行 throwaway install verification；如果因当前分支无法验证 public marketplace，按脚本提示明确记录。
   - `task.py validate` 和 `git diff --check`。

8. Phase 2 check / commit / Branch Review Gate
   - 记录 `phase2-check.json`。
   - 提交本任务变更。
   - 请求独立 review / `trellis-check` 覆盖完整 diff。
   - 通过 `review-branch.sh` 记录 gate。

## 预期改动文件

- `trellis/guru-team-extension.json`
- `trellis/workflows/guru-team/scripts/bash/version.sh`
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
- `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
- `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`
- `trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`
- `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`
- `.trellis/guru-team/**` dogfood copy
- `README.md`
- `trellis/presets/guru-team/README.md`
- `trellis/workflows/guru-team/README.md`
- `docs/requirements/requirement-main.md`
- task artifacts

## 验证命令

```bash
python3 -m json.tool trellis/index.json
python3 -m json.tool trellis/guru-team-extension.json
bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh
python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py
python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py
python3 -m unittest trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py
trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh
python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-04-31-guru-team-extension-version-manifest
git diff --check
```

## 回滚方案

- 删除 `trellis/guru-team-extension.json`、`version.sh` 和相关代码路径。
- 从 `MANAGED_ASSET_PATHS` 移除 `version.sh`。
- 恢复 README / docs。
- 重新 apply preset 到 dogfood copy，确保 drift check 通过。
