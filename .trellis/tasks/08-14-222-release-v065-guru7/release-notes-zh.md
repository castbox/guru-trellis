# v0.6.5-guru.7 发布说明（候选草稿）

本版本将 Guru Team extension revision 更新为 `0.6.5-guru.31`，目标官方
`@mindfoldhq/trellis` CLI 仍为 `0.6.5`。稳定 workflow 与 preset source 均固定到
annotated repo tag `v0.6.5-guru.7`。

> 当前仅完成 release-preparation 字节准备。完整 pre-tag gate 尚未执行，tag 尚未创建；
> post-tag identity 与最小 tag-pinned install/upgrade gate 也尚未执行。因此本文不得视为
> 发布就绪、已验证或已发布声明。Exact peeled commit、candidate tree 与验证结果只能在
> preparation 合并、fresh `origin/main` candidate 冻结并完成对应门禁后填写。

## 版本映射

| 项目 | 值 |
| --- | --- |
| Repo tag | `v0.6.5-guru.7`（尚未创建） |
| Extension revision | `0.6.5-guru.31` |
| Official Trellis CLI | `0.6.5` |
| Peeled candidate commit | 待 preparation 合并后冻结 |
| Candidate tree | 待 preparation 合并后冻结 |
| Workflow source | `gh:castbox/guru-trellis/trellis#v0.6.5-guru.7` |
| Preset source | annotated tag `v0.6.5-guru.7`（尚未创建） |

## 主要变化

- #219：让公开 Guru Skill wrapper 使用 hash-locked 的受管 Python runtime，避免依赖
  PATH Python 的 global/user site-packages，并以统一 resolver 执行 Python 入口。
- #217：修复 `guru-review-branch` recorder 未持久化 owner-private gate 的问题，恢复
  `record -> check -> invoke -> retire/retain` 生命周期，同时保持 typed exits 与 consumer
  mapping 不变。
- #218：Finalizer 与 Merge 的成功路径输出单个 JSON object；同计划 Ready/terminal
  recovery 重验已有事实并物化 terminal DTO，不重复 push、Ready 或 merge mutation；
  `closure_mismatch` 继续独立 fail closed。
- #227：移除 finish summary 变更路径集合的 2000 项固定上限，使 Publication Review 与
  Finalizer 能承接完整的大型路径集合，同时继续拒绝不安全、重复、未排序或集合不一致。
- #231：将受管 Python runtime 收敛为用户级、按完整 source identity 隔离的共享 cache，
  修复 linked worktree 的 source checkout 解析；相同 identity 的重复 preset reapply 复用同一
  runtime，不创建 per-skill 或 per-checkout venv。

## 从 v0.6.5-guru.5 升级

只在隔离或已明确授权修改的目标业务仓 checkout 中执行：

```bash
npm install --global @mindfoldhq/trellis@0.6.5
trellis update
trellis workflow \
  --marketplace gh:castbox/guru-trellis/trellis#v0.6.5-guru.7 \
  --template guru-team --create-new
trellis workflow \
  --marketplace gh:castbox/guru-trellis/trellis#v0.6.5-guru.7 \
  --template guru-team
guru_trellis_source="$(mktemp -d)"
git clone --depth 1 --branch v0.6.5-guru.7 \
  https://github.com/castbox/guru-trellis.git "$guru_trellis_source"
"$guru_trellis_source/trellis/presets/guru-team/scripts/bash/apply.sh" \
  --repo . --all-platforms
```

先审查 `--create-new` 生成的 preview，再执行不带该参数的 workflow switch。Preset
reapply 后必须逐个处理 `.new` / `.bak` / conflict，并完成 source、installed、所选平台、
managed inventory、用户级受管 Python runtime、dogfood drift 与递归零 sidecar 验证。
不得混用 tag-pinned workflow 与 `main`、unpinned 或其它 tag 的 preset source。

## 发布验证状态

- 本 preparation 已通过版本映射 targeted tests（verifier contract 12 项、preset manifest
  installer 5 项）、task JSONL validate、dogfood drift、managed removal/conflict/sidecar
  检查与 `git diff --check`；这些 preparation 证据不替代下列 exact-candidate release gate。
- `guru-verify-extension-installation` 完整 capability catalog：尚未执行，必须在 exact
  post-merge candidate 上完成 pre-tag gate。
- Clean workflow install、existing preview/switch、preset initial apply、official Trellis
  update、preset reapply：尚未执行完整 pre-tag gate。
- 用户级受管 Python runtime、source/installed/platform equality、managed inventory、
  dogfood drift、递归零 sidecar：尚未执行完整 pre-tag gate。
- Branch Review 真实 lifecycle 与 Finalizer/Merge single-JSON/recovery matrix：尚未执行
  exact candidate 的完整 pre-tag gate。
- 隔离业务仓 `.5 -> .7` pinned upgrade smoke 与原 2130 路径 Publication/Finalizer
  preflight：尚未执行。
- Tag object、peeled commit、candidate tree、manifest revision、exact source 与 tag-pinned
  最小 clean install/upgrade entry smoke：尚未执行 post-tag gate。

任一 required gate 缺失、skip 或失败，本发布必须停止，不创建 tag 或 GitHub Release，
不评论或关闭 #222。

## 已知限制与范围

- 当前 extension 明确以官方 Trellis CLI `0.6.5` 为目标；其它 CLI 版本不属于本次矩阵。
- 首次创建用户级受管 Python runtime 需要可访问公开 PyPI，并需要 lock 支持的 CPython
  binary wheels；网络、venv/pip、兼容 wheel 或 hash 校验失败时 preset fail closed。
- 本版本不包含 #223、#208、#164、#220；这些 Issue 不因本次 Release 关闭。

## 安全与部署影响

- 不修改 Trellis upstream、系统 Python、global/user site-packages 或全局 npm 包内容；
  文档中的 CLI 安装命令由目标仓 owner 在明确范围内执行。
- 不包含 secret、私有 index credential、客户数据、数据库 migration、容器、Kubernetes、
  CI/CD 或生产配置变更。
- 这是 workflow/preset 的显式安装与升级，不会自动修改或部署真实业务仓；业务 smoke
  必须在临时 clone/copy 与隔离 remote 中执行。
