# #222 v0.6.5-guru.6 发布设计

## 版本与候选模型

```text
initial base             fresh origin/main after PR #228
repo release tag         v0.6.5-guru.6
extension revision       0.6.5-guru.28
official Trellis CLI     0.6.5
stable workflow source   gh:castbox/guru-trellis/trellis#v0.6.5-guru.6
stable preset source     annotated tag v0.6.5-guru.6
```

`.5` tag 与 `.27` manifest 是历史稳定基线。release preparation 产生不同 bytes，
因此必须分配 `.6` 与 `.28`。preparation branch 上的 HEAD 只能作为待评审 candidate；
最终 exact candidate 必须是 preparation 合入后 fresh `origin/main` 的 commit。若合入
结果 tree 与已验证 tree 不同，或 `main` 在冻结后演进，则冻结失效并重跑受影响门禁。

## 发布状态机

```text
live prerequisites
  -> release preparation bytes
  -> task check / branch review / publication / merge
  -> fresh origin/main exact candidate freeze
  -> complete pre-tag verifier + business upgrade smoke
  -> user tag confirmation
  -> annotated tag push + identity verification
  -> minimal tag-pinned entry smoke
  -> user Release confirmation
  -> GitHub Release + live reread
  -> user evidence-comment confirmation
  -> evidence comment + live reread
  -> user close confirmation
  -> close #222 + final live identity check
```

## Release-owned surfaces

- `trellis/guru-team-extension.json`：canonical extension revision。
- `.trellis/guru-team/extension.json`：由 canonical preset apply 生成的 dogfood manifest。
- `README.md`、`trellis/workflows/guru-team/README.md`、
  `trellis/presets/guru-team/README.md`：公开 stable source、安装、升级与版本映射。
- `.trellis/spec/docs/public-docs.md`：仓库内当前稳定映射规范。
- verifier 的 release identity examples/tests/fixtures：仅更新稳定映射，不固化 future
  candidate commit 或复用旧验证结果。
- task-local release notes/evidence 草稿：发布前为可审核正文，不冒充 GitHub live 事实。

canonical 变更完成后运行 preset `apply.sh --repo .` 同步 dogfood/platform projections，
逐个处理 sidecar，再用 drift、inventory、source-installed equality 证明无漂移。

## Pre-tag 验证模型

`guru-verify-extension-installation` 以 source checkout identity 为入口，从 clean source
执行完整 standalone capability catalog。额外 release gate 覆盖：

- public Branch Review wrapper 的 checkpoint 创建、checker 消费、invoke projection、
  passed retirement 与 non-terminal retain/recovery；
- Finalizer/Merge 的 stdout JSON cardinality、fresh transition、ready/terminal recovery、
  closure mismatch、重复调用零 mutation；
- 从 `v0.6.5-guru.5` 到 candidate 的隔离业务仓 upgrade；
- 以隔离 fixture 表达 2130 个安全、唯一、排序路径，分别进入 Publication Review 与
  Finalizer preflight，证明完整集合无需裁剪即可继续。

业务 smoke 使用临时 clone/copy 与隔离 remote；不读取 secret，不触碰真实业务仓
worktree/branch/index/remote，也不执行 deploy。

## Tag 与发布边界

tag 前展示 candidate commit/tree、extension revision、tag 名称、annotated message、
`git tag -a` 与 exact `git push origin refs/tags/...`。tag 后只在 bytes 一致且最小入口
通过时复用 pre-tag 内部测试；任一 mismatch 立即停止。

GitHub Release、#222 evidence comment、#222 close 是三个独立 mutation。Release notes
只声明实际通过的证据；安全说明明确无 secret、无生产数据、无 upstream/global runtime
改动；部署影响说明这是 workflow/preset 更新，需要显式 upgrade/reapply，不自动部署。

## 回滚与失败策略

- tag 前：修复 release preparation，重新 commit/review/merge/freeze/retest。
- tag 后：immutable tag 不移动、不删除、不 force；发现问题停止 Release/close，另建修复
  revision/tag。
- Release 后、close 前：保留 Release 与 Issue open 状态，补充真实限制或 successor。
- 任一环境限制、skip 或未执行项均按缺失证据处理，不转换为 PASS。
