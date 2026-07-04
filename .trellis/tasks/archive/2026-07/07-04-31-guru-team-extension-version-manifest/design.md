# #31 技术设计

## 设计原则

1. 官方 Trellis 与 Guru extension 分层：官方 Trellis CLI version 继续由 `trellis --version` 和 `.trellis/.version` 表达；Guru Team extension version 由本仓库 manifest 表达。
2. canonical source 单一：repo 内只设置一个 extension manifest 源头，installer、docs、check-env 都读取或传播该源头。
3. 脚本只执行事实动作：installer 写 installed manifest，check-env 读取 installed manifest；是否升级、是否回滚、版本是否足够解决问题由 AI/human 判断。
4. 向后兼容：旧业务 repo 缺少 `.trellis/guru-team/extension.json` 时，`check-env` 仍可运行，但输出 missing/unknown 状态和 next step。
5. 最小敏感面：provenance 记录 source repo/ref/commit 和 dirty/archive 状态，不记录 token、auth detail、`.env` 或本机绝对 source path。

## 数据流

```text
trellis/guru-team-extension.json
  -> preset installer reads canonical manifest
  -> installer probes source Git metadata
  -> installer writes target .trellis/guru-team/extension.json
  -> target check-env/version reads installed manifest
  -> README / AI prompts report extension version + provenance
```

## Canonical Manifest

新增 `trellis/guru-team-extension.json`：

```json
{
  "schema_version": "1.0",
  "extension_id": "guru-team",
  "version": "0.1.0",
  "name": "Guru Team Trellis Extension",
  "workflow_template_id": "guru-team",
  "marketplace_index_schema_version": 1,
  "requires": {
    "trellis_cli": ">=0.6.0"
  },
  "tested": {
    "trellis_cli": []
  },
  "public_api": {
    "workflow_template_id": "guru-team",
    "managed_paths": []
  },
  "release_notes": "README.md#guru-team-extension-version"
}
```

`version` 是 extension SemVer。`marketplace_index_schema_version` 与 `trellis/index.json.version` 保持概念区分。

## Installed Manifest

preset installer 写入 `.trellis/guru-team/extension.json`：

```json
{
  "schema_version": "1.0",
  "extension": {
    "extension_id": "guru-team",
    "version": "0.1.0",
    "workflow_template_id": "guru-team"
  },
  "installed_at": "2026-07-04T...",
  "source": {
    "repo": "https://github.com/castbox/guru-trellis.git",
    "ref": "codex/31-guru-team-extension-version-manifest",
    "commit": "...",
    "tree_state": "dirty",
    "is_mutable_ref": true
  },
  "install": {
    "selected_platforms": ["codex", "cursor"],
    "all_platforms": false,
    "managed_assets": [],
    "workflow_marketplace": "gh:castbox/guru-trellis/trellis",
    "workflow_template": "guru-team"
  }
}
```

`source.tree_state` 规则：

- `clean`: source 在 Git repo 内且 `git status --short` 为空；
- `dirty`: source 在 Git repo 内且有未提交变更；
- `archive`: source 不在 Git repo 内，但存在 canonical manifest；
- `unknown`: metadata 探测失败。

`source.commit` / `source.tree_state` 表示 installer 运行时观测到的 Guru Team extension
source 快照。对于本仓库 dogfood 提交，`.trellis/guru-team/extension.json` 记录的是上一次
apply 的安装事实，不是“该 installed manifest 自身所在提交”的自指证明；canonical version
仍只以 `trellis/guru-team-extension.json` 为准。

`source.is_mutable_ref` 规则：

- `true`: branch name、`main`、`master`、`dev`、`develop`、`HEAD` 等可移动 ref；
- `false`: tag 或 detached commit；
- `null`: unknown/archive。

## Installer 设计

修改 `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`：

- 新增 `EXTENSION_MANIFEST = Path("trellis/guru-team-extension.json")`。
- 新增 helper：`load_extension_manifest()`、`source_provenance()`、`build_installed_extension_manifest()`、`write_installed_extension_manifest()`。
- `install_assets()` 在 managed assets / overlays / codex dispatch 后写 installed manifest。
- `main()` JSON output 增加 `guru_team_extension`。
- `--version` 输出 canonical extension version 后退出。

`.trellis/guru-team/extension.json` 是 installer 管理的安装事实记录，允许每次 apply 更新；它不覆盖用户 config，也不走 `.new`。

## check-env / version 设计

修改 `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`：

- 新增 `read_guru_team_extension(root)`。
- `check_env_payload()` 增加 `guru_team_extension`。
- missing/invalid installed manifest 只 warning，不阻塞整体 `check-env`。
- 新增 `version` subcommand，返回同一核心 payload。

新增薄 wrapper：

- `trellis/workflows/guru-team/scripts/bash/version.sh`
- 调用 `guru_team_trellis.py version --root "$ROOT" --json`

`version.sh` 作为 managed asset 加入 `MANAGED_ASSET_PATHS`、preset README installed files、单测和 throwaway 验证。

## 文档同步

需要更新：

- `README.md`：最小验证、安装/升级 prompt、版本治理说明。
- `trellis/presets/guru-team/README.md`：installed manifest 与 `version.sh`。
- `trellis/workflows/guru-team/README.md`：marketplace workflow id 与 extension version 的关系。
- `docs/requirements/requirement-main.md`：将 #31 加入历史覆盖矩阵和 P1 安装/升级能力。

本任务不改变 `.trellis/workflow.md` Phase 语义，不需要同步 active workflow copy。

## 测试设计

### Installer unit tests

- default install writes `.trellis/guru-team/extension.json`；
- installed manifest records selected platforms；
- `main --version` prints canonical version；
- source state helper 能表达 dirty / archive / unknown。

### Workflow helper tests

- `check_env_payload()` includes `guru_team_extension` when manifest exists；
- missing manifest yields `status: missing` and warning；
- invalid manifest yields `status: invalid` and warning；
- `cmd_version` returns same core extension payload。

### Integration / validation

- JSON / bash / py_compile 基础校验；
- 两个 Python unittest；
- `apply.sh --repo . --all-platforms`；
- dogfood overlay drift check；
- throwaway install verification；
- `task.py validate` 和 `git diff --check`。

## 风险与缓解

- 版本号多处漂移：通过 single canonical manifest 缓解。
- 业务 repo 从 branch/main 安装误以为 immutable release：installed manifest 标记 `is_mutable_ref` 和 `tree_state`。
- 无 `.git` 安装场景：manifest 仍可写入，source state 为 `archive` / `unknown`。
- 旧安装缺 installed manifest：check-env 只 warning，不阻塞。
- 脚本承担升级判断：脚本文案和 artifact notes 明确只记录事实，不判断是否应升级。
