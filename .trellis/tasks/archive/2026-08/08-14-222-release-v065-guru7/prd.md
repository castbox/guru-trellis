# #222 v0.6.5-guru.7 累计发布需求

## 目标

在 #219、#217、#218、#227、#231 全部合并关闭后，从 fresh remote `main`
准备 release-owned bytes，合并后冻结唯一 exact candidate，并完成一次不可拆分的
Trellis Release Gate。发布映射为 repo tag `v0.6.5-guru.7`、Guru Team extension
revision `0.6.5-guru.31`、official Trellis CLI `0.6.5`。

固定顺序：

```text
#219 -> #217 -> #218 -> #227 -> #231 -> #222 -> 发布
```

## 当前事实

- 本 task base、local `main` 与 fresh `origin/main` 均为
  `2aef3cb9481c2413fbfe6c93af5246ba873049f8`，且该 commit 包含五个 prerequisite
  的完整 merge result。
- 最新正式 tag 与 GitHub Release 均为 `v0.6.5-guru.5`。
- 旧 preparation 曾把文档指向 `v0.6.5-guru.6`，但该版本绑定过已废弃的不同 bytes，
  且 live remote 不存在该 tag；本轮不得复用 `.6`、旧 candidate、SHA 或验证证据。
- 当前 canonical extension manifest 为 `0.6.5-guru.30`；本轮 release-owned bytes
  必须使用新 revision `0.6.5-guru.31`。
- #223、#208、#164、#220 仍是独立 follow-up，不属于本次实现、发布或关闭范围。
- 官方 Trellis 当前扩展面确认：自定义 workflow 由 `.trellis/workflow.md` 与
  marketplace Markdown 控制；spec marketplace 只承载可复用规范，不能承载 active
  task 或平台私有运行状态。

## 功能需求

1. 更新 canonical/dogfood manifest、workflow/preset/public README、安装与升级命令、
   stable tag/source 映射、verifier release identity fixtures/tests 与中文 Release notes。
2. preparation 合并后，从 clean 且 `HEAD == local main == origin/main` 的 checkout
   冻结唯一 candidate commit/tree；任何 release-owned byte 或 `main` 演进都使证据失效。
3. 对 exact candidate 正式执行一次完整 `guru-verify-extension-installation`，覆盖 clean
   workflow install、existing preview/switch、preset initial apply、official update 和
   preset reapply。
4. 验证用户级共享受管 Python runtime 在 PATH Python 缺少 `jsonschema` 时仍能安装、
   选择并运行公开 wrapper；相同 identity 重复 reapply 的结果必须不变，不得创建
   per-skill venv。
5. 验证 source/installed/platform equality、managed inventory、executable mode、dogfood
   drift，以及零 `.new`、`.bak`、conflict、removal 和未知 sidecar。
6. 真实验证 Branch Review `record -> check -> invoke -> retire/retain`；验证
   Finalizer/Merge single-JSON stdout、fresh transition、ready/terminal recovery、
   closure mismatch 与零重复 mutation。
7. 在隔离业务仓副本执行 pinned upgrade smoke，并以原 2130 路径集合验证 Publication
   Review/Finalizer preflight 能继续；不得修改、commit、push 或部署任何现有业务 checkout。
8. pre-tag 全部通过后展示 exact candidate/tree/revision/tag/命令与副作用；取得确认后
   创建、push immutable annotated tag。
9. tag 后核对 tag object、peeled commit、candidate tree、manifest revision 与 exact
   source，并运行最小 tag-pinned clean install/upgrade 入口；bytes 一致且入口通过时不
   重复全部 pre-tag 内部测试。
10. GitHub Release、#222 证据评论和 #222 close 是三个独立远端 mutation，必须分别
    展示精确内容并取得当前确认。

## 非目标与安全边界

- 不重新实现 #219、#217、#218、#227、#231 的 correctness 代码。
- 不处理或关闭 #223、#208、#164、#220。
- 不修改 Trellis upstream、全局 npm、系统 Python、global/user site-packages。
- 不读取或发布 secret、credential、客户数据、真实业务配置或私有原始记录。
- 不自动升级或部署真实业务仓；业务 smoke 只在临时 clone/copy 和隔离 remote 中执行。
- 任一 required gate 缺失、skip、失败或 bytes mismatch 时停止，不创建 tag、Release，
  不关闭 #222，也不作发布就绪声明。

## 验收标准

1. `.7` / `.31` / CLI `0.6.5` 与唯一 post-merge candidate commit/tree 一一对应。
2. release-owned manifests、README、命令、fixtures/tests 与 Release notes 字节一致。
3. 完整 standalone verifier 返回 `verified`，所有 required capability 都有本轮 fresh
   evidence，且不复用旧 candidate 的结果。
4. 用户级共享 runtime、workflow/preset/update/reapply、inventory/equality/drift/sidecar
   门禁全部通过。
5. Branch Review、Finalizer、Merge 的公开 wrapper 正常和恢复生命周期全部通过。
6. 隔离业务 upgrade 与原 2130 路径 Publication/Finalizer preflight 通过，真实业务仓
   前后状态完全不变。
7. annotated tag 仅在独立确认后创建并 push；tag-pinned identity 和最小入口通过。
8. 中文 Release notes 准确覆盖五个 prerequisite、升级步骤、版本映射、验证证据、
   已知限制、安全与部署影响。
9. Release、证据评论、Issue closure 分别确认并 live reread；最终只关闭 #222。
