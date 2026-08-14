# v0.6.5-guru.6 发布说明（候选草稿）

本版本将 Guru Team extension revision 更新为 `0.6.5-guru.30`，目标官方
`@mindfoldhq/trellis` CLI 仍为 `0.6.5`。稳定 workflow 与 preset source 均固定到
尚未创建的 annotated repo tag `v0.6.5-guru.6`。

> 当前为 pre-tag 候选正文。Exact peeled commit、candidate tree 和验证结果只能在
> 修复 PR 合并、fresh `origin/main` candidate 冻结并完成全部门禁后填写。

## 版本映射

| 项目 | 值 |
| --- | --- |
| Repo tag | `v0.6.5-guru.6`（尚未创建） |
| Extension revision | `0.6.5-guru.30` |
| Official Trellis CLI | `0.6.5` |
| Peeled candidate commit | 待 tag 前 exact candidate 冻结 |
| Candidate tree | 待 tag 前 exact candidate 冻结 |
| Workflow source | `gh:castbox/guru-trellis/trellis#v0.6.5-guru.6` |
| Preset source | annotated tag `v0.6.5-guru.6` |

## 主要变化

- #219：新增 repo-local、gitignored 的受管 Python runtime，使用 hash-locked
  dependency lock 和统一 resolver 运行 Guru-owned Python 入口。
- #222 release blocker：修复 shared validator、contract discovery、eval discovery、
  eval execution 与 compatibility wrapper 仍直接调用 PATH Python 的遗漏。Source 与
  installed wrapper 现在分别使用自身 checkout 的受管 runtime；PATH Python 缺少
  `jsonschema` 时不再错误失败或回退外部环境。
- #222 Branch Review finding：修复 shared、Codex、Claude、Cursor eval adapter 的
  `native_adapter.py` 第二跳 PATH fallback，并让 fresh source fixture 使用真实 commit
  identity；PATH 完全没有 `python3` 时，source/installed adapter 仍绑定各自受管 runtime。
- #217：恢复 `guru-review-branch` owner-private gate 的真实 record/check 生命周期。
- #218：Finalizer 与 Merge 成功路径保持 single-JSON 与幂等恢复合同。
- #227：移除 finish summary 大路径集合的固定上限，同时保留路径安全和集合一致性校验。

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

先审查 preview，再执行 workflow switch。Preset reapply 后必须处理 `.new` / `.bak` /
conflict，并完成 source、installed、平台 equality、managed inventory、受管 Python runtime
与 sidecar 验证。不得混用 tag-pinned workflow 与其它 preset source。

## 发布验证

- PATH Python 无 `jsonschema` 的 source/installed shared wrapper gate：待新 candidate 验证。
- `guru-verify-extension-installation` 完整 capability catalog：待新 candidate pre-tag gate。
- Clean workflow install、preview/switch、preset apply、official update、reapply：待新 candidate
  pre-tag gate。
- Platform equality、ownership inventory、dogfood drift、递归零 sidecar：待新 candidate
  pre-tag gate。
- Branch Review、Finalizer/Merge、隔离业务仓 pinned upgrade 与 2130 路径 preflight：待新
  candidate pre-tag gate。
- Tag object、peeled commit、candidate tree 与 tag-pinned smoke：待 tag 创建后门禁。

任一 required gate 缺失、skip 或失败，本发布停止，不创建 tag 或 Release，也不评论或关闭
#222。

## 已知限制

- 当前 extension 明确以官方 Trellis CLI `0.6.5` 为目标。
- 首次创建受管 Python runtime 需要可访问公开 PyPI，并需要 lock 支持的 CPython binary
  wheels；网络、venv/pip、兼容 wheel 或 hash 校验失败时 preset fail closed。
- 本版本不包含 #223、#208、#164、#220。

## 安全与部署影响

- 不修改 Trellis upstream、全局 npm、系统 Python 或用户 site-packages。
- 不包含 secret、客户数据、数据库 migration、容器、Kubernetes、CI/CD 或生产配置变更。
- 这是 workflow/preset 的显式安装与升级，不会自动修改或部署业务仓。
