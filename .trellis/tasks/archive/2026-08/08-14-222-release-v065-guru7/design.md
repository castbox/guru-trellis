# #222 v0.6.5-guru.7 发布设计

## 身份模型

```text
preparation base          2aef3cb9481c2413fbfe6c93af5246ba873049f8
repo release tag          v0.6.5-guru.7
extension revision        0.6.5-guru.31
official Trellis CLI      0.6.5
stable workflow source    gh:castbox/guru-trellis/trellis#v0.6.5-guru.7
stable preset source      annotated tag v0.6.5-guru.7
exact candidate           preparation merge 后 fresh origin/main，当前未知
```

`v0.6.5-guru.5` 是 live 稳定基线；`.6` 已绑定过被后续 #230/#232 替代的不同
bytes，不能因 live tag 尚未创建而回收。`.30` 是当前合并态 manifest revision；新的
release-owned bytes 分配 `.31`。preparation branch HEAD 不是最终 candidate，只有合并后
clean `origin/main` 的 commit/tree 才能冻结。任何 byte 或 remote-main 演进都要求重新
冻结并重跑受影响门禁。

## 发布状态机

```text
live prerequisites and version allocation
  -> release-owned bytes + task planning/check/review
  -> preparation commit/push/PR/merge
  -> fresh origin/main exact candidate freeze
  -> full pre-tag verifier + lifecycle fixtures + isolated business smoke
  -> user tag confirmation
  -> annotated tag push + tag identity verification
  -> minimal tag-pinned clean install/upgrade smoke
  -> user Release confirmation -> GitHub Release + reread
  -> user evidence confirmation -> #222 comment + reread
  -> user close confirmation -> close #222 + final identity check
```

## Release-owned surfaces

- `trellis/guru-team-extension.json`：canonical extension revision。
- `.trellis/guru-team/extension.json`：preset 生成的 dogfood installed manifest。
- `README.md`、`trellis/workflows/guru-team/README.md`、
  `trellis/presets/guru-team/README.md`：稳定 source、安装、升级与版本映射。
- `.trellis/spec/docs/public-docs.md`、`.trellis/spec/preset/installer.md`、
  `.trellis/spec/workflow/data-contracts.md` 及 canonical preset specs：durable contract。
- verifier release-identity examples/tests/fixtures：只更新新映射，不固化未来 candidate
  commit，也不携带旧验证结果。
- task-local `release-notes-zh.md` 与 evidence 草稿：只作为待审核文本，不能冒充 live
  GitHub Release、tag 或验证事实。

canonical 变更后使用 `apply.sh --repo . --all-platforms` 同步 dogfood 与 Claude/Codex/
Cursor projections。installer 每次运行后都必须检查 tracked diff、managed removal、
conflict/sidecar 和 source tree identity，避免未传 `--platform` 或 `--all-platforms` 时的
自动检测误删其它受管 projection。

## Pre-tag 验证架构

`guru-verify-extension-installation` 以 exact source commit 为 authority，从 standalone clean
checkout 执行完整 capability catalog。额外 cumulative gate 包括：

- workflow marketplace 的 new-repo install 与 existing-repo preview/switch；
- preset initial apply、official `trellis update`、preset reapply 和 upgrade 后保留语义；
- 用户级、按完整 identity 隔离的共享 Python cache，同仓 linked worktree 继承以及
  PATH Python 缺依赖场景；不创建每 Skill/每 checkout venv；
- canonical/source/installed/四平台 byte equality、managed inventory、mode、dogfood
  drift 和递归 sidecar scan；
- Branch Review 的 checkpoint lifecycle，以及 Finalizer/Merge 的 single-output、fresh/
  recovery/mismatch/zero-repeat-mutation 路径；
- 从 live stable `.5` 到 candidate 的隔离业务 upgrade，并用 2130 个安全、唯一、排序
  path 完整进入 Publication Review 与 Finalizer preflight。

完整命令、临时目录、facts digest 和 candidate identity 必须在执行时从 live contracts
生成；planning 文档不预填 PASS。业务 smoke 使用临时 clone/copy 与隔离 remote，前后
对真实业务 checkout 执行只读状态对比。

## Tag 后最小复核

tag 前展示 commit、tree、revision、annotated message 和 exact push refspec。tag 创建后
核对 tag object type、peeled commit、tree、manifest 与 source ref；从 tag-pinned source
仅重跑 README 暴露的 clean install/upgrade 入口。只有 bytes 不一致或入口暴露新问题时
才重新执行完整内部矩阵。immutable tag 不移动、不删除、不 force。

## Docs SSOT Plan

- strategy：`ssot_first`。
- durable owners：三份 public README、canonical manifest、public-docs、installer、
  data-contracts 与 verifier release-identity tests/fixtures。
- generated projections：dogfood manifest 和 Shared/Claude/Codex/Cursor managed copies 由
  canonical preset `--all-platforms` 生成，并以 equality/drift/inventory 验证。
- task history：本目录只保留 #222 的 planning、scope、release-notes 与最终去敏证据；
  不复制完整运行日志、secret、临时绝对路径或用户授权过程。
- follow-up：#223、#208、#164、#220 继续由各自 Issue 持有，不进入 release notes 的
  “已完成”范围。

## 失败与恢复

- tag 前失败：修复 preparation，重新 check/review/merge/freeze，并重跑受影响证据。
- tag 后失败：不移动或删除 tag；停止 Release/closure，以新 revision/tag 修复。
- Release 后、close 前失败：保留 Release 和 open Issue，补充真实限制或 successor。
- skip、环境限制、输出不完整或无法证明真实业务仓零变化都按缺失证据处理。
