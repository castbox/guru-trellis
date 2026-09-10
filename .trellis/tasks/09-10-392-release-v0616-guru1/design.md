# Design

## Release Identity

| Axis | Current | Target |
| --- | --- | --- |
| Repository tag / GitHub Release | `v0.6.15-guru.6` | `v0.6.16-guru.1` |
| Guru Team extension | `0.6.15-guru.40` | `0.6.16-guru.41` |
| Trellis CLI/core | `0.6.16` | `0.6.16` |
| Framework source | `castbox/Trellis@ad332e3fe5a19d7274cb03e7c2f3e2128f8de291` | unchanged |
| Architecture/RDT knowledge identity | `current-main-0.6.5-guru.47` | successor `.48` |

四个发布轴分别保留独立 authority，但所有 current release-facing surfaces 必须投影
同一 mapping。Fork full SHA 是 source/build authority；CLI 和 extension 版本不能替代它。

## Two-Stage Boundary

### Stage 1: Preparation Task And PR

准备分支只产生最终 delivery bytes：

1. 提升 manifest revision 并同步 canonical、dogfood、installed projection。
2. 直接更新受控 current 文档、fixture、schema/validator expectation；不保留双版本
   current parser、fallback 或 compatibility adapter。
3. 从 `.47` 复制并派生 `.48` RDT authority，新增 #392 requirement/design/test trace；
   Architecture 通过独立 contribution 和 promotion 将 `.48` 设为唯一 active。
4. 执行 scoped Phase 2 validation、task commit、完整分支独立 review、publication 和
   Finalizer，再由 expected-head merge owner 合并准备 PR。

task/provenance 元数据不属于 release delivery identity；不得用 metadata commit 记录
gate 或发布进度。

### Stage 2: Post-Merge Exact Candidate

PR 合并后丢弃 Stage 1 HEAD、Branch Review、Publication 和所有旧 Release Gate 结果。
fresh-fetch `origin/main` 后冻结一个 commit/tree candidate，所有 gate、tag、smoke 和
Release 文案都绑定该 identity。任一命令结果来自其他 SHA 时 fail closed。

## Authority And Ownership

- `trellis/guru-team-extension.json` 是 canonical extension manifest；preset reapply
  负责同步 dogfood/installed managed copies，随后以 byte/mode/drift 检查证明一致性。
- `README.md`、`.trellis/spec/docs/public-docs.md`、workflow/preset README 是稳定用户
  安装与版本 mapping authority。
- `docs/requirements`、`docs/design`、`docs/test` 和 `docs/architecture` 由各自 SSOT
  owner 派生 successor identity；历史目录只改导航状态，不改历史正文事实。
- `release-guru-trellis-version` 只编排已有 owner，不新增 runtime、schema、checkpoint
  或公共 inventory 项。
- `issue-scope-ledger.json` 保持 `close=[392]`、`related=[378]`、`followup=[]`。

## Compatibility And Subtraction

这是 current version/publication authority 的直接演进。受控 current consumers 同步
迁移到新 mapping，旧 mapping 只在明确的 historical/released/superseded context 中保留。
不新增长期双读、别名、fallback、第二发布状态机或 task-local发布资产。若某个旧 current
fixture/字段失去唯一 consumer，则在同一任务中更新或删除其入口、测试和文档。

## Validation Model

Stage 1 验证 preparation bytes、current authority、canonical/installed parity 和完整
branch diff。Stage 2 从 clean exact candidate 执行：

- predecessor lineage、完整 diff/name-status 和 version-axis mapping；
- source/installed package validators 与 Shared/Codex/Claude/Cursor projection parity；
- ownership、preset all-platform reapply、dogfood drift 和 unexpected mutation 检查；
- clean/existing install、update、workflow preview/switch、preset reapply；
- Fork checkout/source lock/build marker/CLI identity；
- 代表性业务仓库只读或 throwaway installed smoke，不写业务生产状态；
- 对 predecessor-to-candidate changed-file bytes 的真实 secret scan；
- `git status --short`、`git diff --check` 和递归 residue/sidecar 检查。

任何 unavailable scanner 或未执行的 required path 记为 `SKIP` 并阻止发布，不能降级为
通过。完整 Issue gate 通过后才进入 tag mutation。

## Publication And Recovery

task commit、push、PR、merge、tag、tag-pinned smoke、Release、Issue close 和 cleanup
分别回读 live authority并获取独立确认。失败动作不授权重试。恢复仅使用对应 owner 接受的
same-identity live facts；不得移动 tag、伪造旧 receipt 或创建 lifecycle 状态文件。

## Risks And Controls

- 710-file predecessor diff 可能隐藏 version/authority drift：以完整 diff、定向版本扫描和
  独立 Branch Review 覆盖，而不是复用 focused test。
- preset reapply 可能产生 managed copy 或 sidecar：在 clean candidate 中执行并拒绝任何
  未解释 mutation、`.new`、`.bak` 或未知文件。
- Fork CLI 同版本 stale build 风险：同时验证 source lock full SHA、构建输入、build marker
  和实际 CLI identity。
- 远端在确认前变化：每个 mutation boundary 重新读取 ref/object/Issue/Release 状态并使用
  expected-head 或 exact tag target。

## Rollback Boundary

Stage 1 仅通过普通 PR 回滚。Stage 2 在 tag push 前停止时不产生发布对象；annotated tag
push 后不得移动或重建，只能保留 immutable history 并通过新的 successor release 修复。
