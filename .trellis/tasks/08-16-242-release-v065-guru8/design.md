# #242 v0.6.5-guru.8 发布设计

## 身份模型

```text
stable repo tag           v0.6.5-guru.7
stable peeled commit      9b054f01ead8edf03a5713ec10aa7c3e1a4d99d1
initial preparation base  0e315fcf41c6fc918364927b93f4b84c9b944aba
reconciled current base   09d29ad3b37e681b3cede129028e161ab9b1d682
target repo tag           v0.6.5-guru.8
target extension version  0.6.5-guru.33
official Trellis CLI      0.6.5
exact candidate           preparation PR 合并后 fresh origin/main，当前未知
```

`0.6.5-guru.32` 是 guru.7 后初始四个 payload 合并完成时的未发布 extension version；
#243 随后恢复 versioned production 3.0 contract 的 immutable bytes，但不分配新的 extension
version。`.33` 仍是本次 release-owned bytes 的唯一新版本。preparation branch 只产生待合并
bytes，不会被提前称为 candidate。candidate authority 由合并后的 fresh `origin/main`
commit/tree 唯一确定。

## Payload 冻结模型

```text
v0.6.5-guru.7
  -> #208 merged bytes
  -> #164 merged bytes
  -> #236 merged bytes
  -> #237 merged bytes
  -> #243 / PR #244 immutable contract corrective bytes
  -> PR #245 archived #243 task metadata
  -> release-owned .33/guru.8 preparation bytes
  -> PR merge
  -> fresh origin/main candidate commit/tree
```

`c8c2409cbb79759dae8be8ce95ce03655d5cf518` 的 bootstrap archive 与 PR #245 的 #243 task
archive 进入 exact byte range，但不形成 release feature claim。冻结记录必须分别列出全部
26 个 commit、1008 个 path、五个 payload Issue/PR 与 administrative commits 的语义分类。

## Release-owned surfaces

### Canonical owners

- `trellis/guru-team-extension.json`：extension version authority。
- `README.md`：公开版本矩阵、stable install 与 upgrade 入口。
- `trellis/workflows/guru-team/README.md`：marketplace workflow stable source。
- `trellis/presets/guru-team/README.md`：preset source、安装、更新与 reapply 合同。
- `.trellis/spec/docs/public-docs.md`、`.trellis/spec/preset/installer.md`、
  `.trellis/spec/workflow/data-contracts.md`：当前仓库的 durable release mapping 约束。
- canonical verifier examples/tests：`.33`/`guru.8` release identity fixture。

### Generated projections

- `.trellis/guru-team/extension.json`；
- Shared/Codex/Claude/Cursor 的 `guru-verify-extension-installation` public example；
- preset 内复制的 workflow spec 与 installed package projection。

canonical 变更后只通过 preset `apply.sh --repo . --all-platforms` 生成这些副本。生成后用
byte equality、managed inventory、ownership、mode、registry/workflow graph 与 overlay drift
证明一致性，不手工把 dogfood 副本当成 source。

## 发布状态机

```text
Planning approved
  -> Phase 2 release preparation
  -> guru-check-task
  -> confirmed task commit
  -> independent fresh-final Branch Review
  -> PR readiness
  -> confirmed push
  -> confirmed PR creation
  -> “合并PR” authorization
  -> PR merge + fresh origin/main freeze
  -> cumulative pre-tag gate
  -> confirmed annotated tag creation/push
  -> confirmed tag-pinned fresh clone smoke
  -> confirmed GitHub Release
  -> confirmed Issue #242 close
  -> final live reread
```

每个 Git/GitHub mutation 只消费其前一轮展示后取得的当前确认。tag、tag-pinned smoke、
Release 与 Issue close 使用四个互不复用的确认边界。

## 验证分层

### Phase 2 preparation evidence

- manifest/JSON/schema/package/integration/eval targeted tests；
- canonical/dogfood/platform equality；
- preset apply、ownership、overlay drift、mode 与零 sidecar；
- release identity fixture/test；
- task planning、Docs SSOT、scope ledger 与 release notes wording；
- independent implementation/check work 和 `guru-check-task`。

这些证据只证明 preparation branch 的实现质量，不替代 post-merge candidate gate。

### Post-merge candidate evidence

- `v0.6.5-guru.7..candidate` 完整 commit/path/payload freeze；
- `guru-verify-extension-installation` source-repository public verifier；
- clean initial install、existing preview/switch、official update、preset reapply；
- linked worktree/closeout；
- 双 PATH managed interpreter identity；
- deterministic/no-model/fake-production、sandbox、schema/route 与独立 review；
- source/installed/platform equality、inventory、mode、ownership、overlay drift；
- 零 `.new`、`.bak`、conflict、removal 与未知 sidecar。

任何 candidate byte 或 release-owned metadata 变化只使绑定该 identity 的 evidence stale；
不受影响的 evidence 仍需由当前 owner 合同确认是否可复用，不能由调用方自行假定。

## Bytecode staging 边界

本任务不创建新的 canonical bytecode mechanism。当前 installer/package inventory 已排除
`__pycache__`、`.pyc`、`.pyo`；本发布在 caller-owned staging 中增加以下执行约束：

1. clone/export/rsync/tar staging 使用显式排除规则：`__pycache__/`、`*.pyc`、`*.pyo`；
2. staging 首次执行前扫描 staged roots，发现 bytecode 就按精确 path 失败；
3. postflight 重复扫描 staged roots，结果必须仍为零；
4. source checkout ignored bytecode 不进入扫描 identity、freshness token 或 blocker；
5. 语法检查使用读取 source 后调用 `compile(source, path, "exec")` 的无落盘路径；
6. 必须产生 bytecode 的外部工具使用 snapshot/source 外的 owner-private temporary root；
7. staged root 命中只报告 staging/runner hygiene failure，不报告 candidate drift。

上述约束只属于 #242 本轮 release evidence。任何多 consumer、canonical runtime、Trellis
0.7 多 workflow 设计继续由 #239 或未来独立 authority 持有。

## 模型证据设计

#237 定义的正常场景资格 runtime、deterministic/no-model/fake-production eval、sandbox 与
schema/route 是本发布的 current evidence。`160x5`、`160x1` 和其他 live GPT-5.6 Sol
production matrix 不执行。所有公开与 task-local 文案固定披露：

> 本发布未取得 live GPT-5.6 Sol production semantic evidence；deterministic/no-model
> 结果不能证明模型压力矩阵或未来模型稳定性。

## Docs SSOT Plan

- strategy：`ssot_first`。
- durable owners：canonical manifest、三份 public README、`public-docs.md`、
  `installer.md`、`data-contracts.md` 与 canonical verifier release-identity tests/fixtures。
- generated projections：dogfood manifest、installed package 与四个平台 public example
  由 canonical preset 生成，并由 equality/drift/inventory 复核。
- task-local history：本目录保存 planning、scope ledger、中文 Release notes 与最终去敏
  release evidence；不保存 secret、用户授权过程、完整临时日志或机器绝对路径 bundle。
- no durable spec expansion：临时 bytecode staging 规则留在 #242 planning/evidence，不写入
  #239 的 canonical product projection、runtime 或多 workflow SSOT。
- follow-up：#240 只记录发布后顺序，不进入本次实现或关闭范围。

## 失败与恢复

- Planning/Phase 2 失败：修复 task-local 或 release-owned bytes，完整重跑受影响门禁。
- PR 合并前 base 演进：停止，执行 base reconciliation，再重新 review 当前完整 diff。
- PR 合并后 candidate 演进：重新冻结 commit/tree，并重跑所有 candidate-bound evidence。
- tag 前失败：不创建 tag、Release 或关闭 Issue。
- tag 后 smoke 失败：immutable tag 不移动、不删除；停止 Release/closure，并以新的独立
  version/tag 修复。
- Release 后、Issue close 前失败：保留 live Release 和 open #242，报告真实限制。
- unknown/multiple typed exit、required gate failure、SKIP 或外部 authority 缺失：fail closed。
