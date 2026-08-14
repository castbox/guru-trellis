# v0.6.5-guru.6 发布说明（候选草稿）

本版本将 Guru Team extension revision 更新为 `0.6.5-guru.28`，目标官方
`@mindfoldhq/trellis` CLI 仍为 `0.6.5`。稳定 workflow 与 preset source 均固定到
annotated repo tag `v0.6.5-guru.6`。

> 当前为 pre-tag 候选正文。Exact peeled commit、candidate tree 和验证结果只能在
> preparation PR 合并、fresh `origin/main` candidate 冻结并完成全部门禁后填写。

## 版本映射

| 项目 | 值 |
| --- | --- |
| Repo tag | `v0.6.5-guru.6` |
| Extension revision | `0.6.5-guru.28` |
| Official Trellis CLI | `0.6.5` |
| Peeled candidate commit | 待 tag 前 exact candidate 冻结 |
| Candidate tree | 待 tag 前 exact candidate 冻结 |
| Workflow source | `gh:castbox/guru-trellis/trellis#v0.6.5-guru.6` |
| Preset source | annotated tag `v0.6.5-guru.6` |

## 主要变化

- #219：新增 repo-local、gitignored 的受管 Python runtime，使用 hash-locked
  dependency lock 和统一 resolver 运行 Guru-owned Python 入口，不依赖全局或用户
  site-packages，也不要求手工激活 virtualenv。
- #217：修复 `guru-review-branch` recorder 未持久化 owner-private gate 的问题，恢复真实
  `record -> check -> invoke -> retire/retain` 生命周期，保持现有 typed exits 和 consumer
  mapping 不变。
- #218：Finalizer 与 Merge 成功路径严格输出单个 JSON object；同计划 Ready/terminal
  recovery 重验既有事实并物化 terminal DTO，不重复 push、Ready 或 merge mutation；
  `closure_mismatch` 继续独立 fail closed。
- #227：移除 finish summary 两处路径集合的 2000 项固定上限，Publication Review 与
  Finalizer 可接受完整的大型变更路径集合，同时继续拒绝不安全、重复、未排序或集合不一致。

## 从 v0.6.5-guru.5 升级

在隔离或已确认可修改的目标业务仓 checkout 中执行：

```bash
npm install --global @mindfoldhq/trellis@0.6.5
trellis update
trellis workflow \
  --marketplace gh:castbox/guru-trellis/trellis#v0.6.5-guru.6 \
  --template guru-team --create-new
trellis workflow \
  --marketplace gh:castbox/guru-trellis/trellis#v0.6.5-guru.6 \
  --template guru-team
guru_trellis_source="$(mktemp -d)"
git clone --depth 1 --branch v0.6.5-guru.6 \
  https://github.com/castbox/guru-trellis.git "$guru_trellis_source"
"$guru_trellis_source/trellis/presets/guru-team/scripts/bash/apply.sh" \
  --repo . --all-platforms
```

先审查 `--create-new` 生成的 preview，再执行不带该参数的 workflow switch。Preset
reapply 后必须逐个处理 `.new` / `.bak` / conflict，并完成 source、installed、所选平台、
managed inventory、受管 Python runtime 与 sidecar 验证。不要混用 tag-pinned workflow
和 `main`、unpinned 或其它 tag 的 preset source。

## 发布验证

- `guru-verify-extension-installation` 完整 capability catalog：待 exact candidate pre-tag gate。
- Clean workflow install、existing preview/switch、preset initial apply、official Trellis
  update、preset reapply：待 exact candidate pre-tag gate。
- 受管 Python runtime、source/installed/platform equality、managed inventory、dogfood
  drift、递归零 sidecar：待 exact candidate pre-tag gate。
- Branch Review 真实 lifecycle 与 Finalizer/Merge single-JSON/recovery matrix：待 exact
  candidate pre-tag gate。
- 隔离业务仓 `.5 -> .6` pinned upgrade smoke 与原 2130 路径 Publication/Finalizer
  preflight：待 exact candidate pre-tag gate。
- Tag object、peeled commit、candidate tree、manifest revision、exact source 与 tag-pinned
  最小 clean install/upgrade entry smoke：待 tag 创建后门禁。

任一 required gate 缺失、skip 或失败，本发布停止，不创建 tag 或 Release，也不关闭 #222。

## 已知限制

- 当前 extension 明确以官方 Trellis CLI `0.6.5` 为目标；其它 CLI 版本不属于本次验证矩阵。
- 首次创建受管 Python runtime 需要可访问公开 PyPI，并需要 lock 支持的 CPython binary
  wheels；网络、venv/pip、兼容 wheel 或 hash 校验失败时 preset fail closed。
- 本版本不包含 #223、#208、#164、#220；这些 Issue 不因本次 Release 关闭。

## 安全与部署影响

- 不修改 Trellis upstream、全局 npm 包内容、系统 Python 或用户 site-packages；文档中的
  CLI 安装命令由目标仓 owner 在明确范围内执行。
- 不包含 secret、私有 index credential、客户数据、数据库 migration、容器、Kubernetes、
  CI/CD 或生产配置变更。
- 这是 workflow/preset 的显式安装与升级，不会自动修改或部署业务仓；业务仓必须在自己的
  受控 checkout 中执行 workflow switch、preset reapply 和验证。
