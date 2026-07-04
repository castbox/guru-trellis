# #33 设计：版本源、tag 策略与文档同步

## 设计结论

采用单一 release coordinate：

```text
trellis/guru-team-extension.json.version = 0.6.5
Git release tag = v0.6.5
workflow marketplace stable source = gh:castbox/guru-trellis/trellis#v0.6.5
workflow template id = guru-team
```

这样既保留 `guru-team` 作为稳定公共 template id，又让 GitHub release/tag、安装命令和
可观测 manifest version 指向同一个版本。

## 边界与数据流

```text
canonical manifest
  trellis/guru-team-extension.json
        |
        | apply.sh / apply_guru_team_trellis_preset.py
        v
installed manifest
  .trellis/guru-team/extension.json
        |
        | check-env.sh / version.sh
        v
用户和 AI 排障输出
```

文档和 release tag 的关系：

```text
PR 修改 manifest/docs/spec
        |
        v
merge commit on main
        |
        v
annotated tag v0.6.5
        |
        v
Trellis marketplace source gh:castbox/guru-trellis/trellis#v0.6.5
        |
        v
throwaway install / existing workflow preview verification
        |
        v
删除旧 guru-team/v0.6.5 tag
```

## 版本概念分离

| 概念 | 来源 | 本次处理 |
| --- | --- | --- |
| 官方 Trellis CLI 版本 | `trellis --version` | 不修改；仅在 docs 中说明要实时检查 |
| Trellis project template 版本 | `.trellis/.version` | 不修改 |
| Marketplace index schema version | `trellis/index.json.version` | 不修改，继续为 `1` |
| Guru Team extension version | `trellis/guru-team-extension.json.version` | 改为 `0.6.5` |
| Installed provenance | `.trellis/guru-team/extension.json` | 通过 preset installer 同步 |
| Git release tag | GitHub repo tag | PR merge 后创建 `v0.6.5` |

## 文档同步面

需要同步的长期文档：

- `README.md`：稳定安装命令、AI install/upgrade prompt、版本说明、release tag 策略；
- `trellis/workflows/guru-team/README.md`：marketplace workflow 安装和已有项目切换；
- `trellis/presets/guru-team/README.md`：throwaway install、workflow marketplace source 和
  preset installer 关系；
- `docs/requirements/requirement-main.md`：把 #33 作为已实现能力的 requirement 记录；
- `.trellis/spec/workflow/data-contracts.md` / `.trellis/spec/preset/installer.md`：沉淀后续
  版本发布必须遵守的维护规则。

## Release / rollback 策略

本 PR 只修改文件，不创建 `v0.6.5`。原因是远程 tag 必须指向包含 `version: 0.6.5` 和
文档更新的 merge commit。

PR merge 后执行：

```bash
git fetch origin main --tags
git checkout main
git pull --ff-only origin main
git tag -a v0.6.5 -m "Guru Team Trellis extension v0.6.5"
git push origin v0.6.5
```

然后验证：

```bash
trellis init -y -u <name> --codex --cursor \
  --workflow guru-team \
  --workflow-source gh:castbox/guru-trellis/trellis#v0.6.5

trellis workflow \
  --marketplace gh:castbox/guru-trellis/trellis#v0.6.5 \
  --template guru-team \
  --create-new
```

验证通过后再删除旧 tag：

```bash
git push origin :refs/tags/guru-team/v0.6.5
git tag -d guru-team/v0.6.5
```

旧 tag 删除是破坏性发布操作，应在 `v0.6.5` 创建且验证通过后执行。

## 兼容性

- 现有不带 `#ref` 的安装命令继续可用，但文档将其定位为 latest/canary。
- 已安装旧版本的目标 repo 可以继续通过 `apply.sh` 升级 installed manifest 和 companion
  assets。
- `guru-team` workflow template id 不变，因此已有 marketplace id 不需要迁移。
- `trellis/index.json` 不变，因此官方 marketplace schema contract 不受影响。

## 中台知识门禁

本任务不涉及 Guru Team 中台 SDK / framework、go-guru、Unity 或 Flutter SDK。Middle-platform
Knowledge Gate 不适用。
