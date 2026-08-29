# #267 v0.6.15-guru.3 successor Release 设计

## 身份模型

repo tag、extension revision 与 Trellis CLI 是三个独立版本轴。本任务使用一个固定映射：

```text
v0.6.15-guru.3 -> 0.6.15-guru.39 -> Trellis CLI 0.6.15
```

`trellis/guru-team-extension.json` 是 extension identity canonical owner；根
`README.md` 是 stable public install owner；workflow/preset README 承接 immutable
source、preview/switch、official update 与 reapply 合同。preset apply 将 canonical
manifest 投影到 `.trellis/guru-team/extension.json`。verifier source/installed tests
绑定同一 extension identity。

## Candidate 状态机

```text
preparation base
  -> planning approved
  -> release identity edits
  -> Phase 2 check
  -> task commit
  -> committed full-diff Branch Review
  -> Publication / Finalizer
  -> confirmed push / PR / merge
  -> fresh remote-main candidate freeze
  -> exact-candidate pre-tag gates
  -> confirmed annotated tag
  -> tag identity reread
  -> confirmed tag-pinned smoke
  -> confirmed GitHub Release
  -> Release identity reread
  -> confirmed #267 closure
  -> separate formal .3 business-repository proof
  -> conditional #311 closure
```

preparation branch HEAD 不能充当最终 candidate。PR merge 后必须 fresh fetch 并绑定
remote `main` commit/tree；其后 `main`、tree、version mapping 或 evidence SHA 发生变化，
candidate freeze 立即失效并重新执行 Release preflight。

## Source 与 Projection

实现只改 `prd.md` 所列文件。canonical 变更后运行 preset apply，随后验证：

- canonical 与 `.trellis/guru-team/extension.json` 的 extension payload byte identity；
- canonical 与 installed `guru-verify-extension-installation` assertion identity；
- source/installed package registry、schema、consumer graph、mode 与 permission；
- dogfood overlay drift 为零；
- `.new`、`.bak`、undeclared sidecar 与 owner-private residue 数量均为零。

preset apply 生成的 managed bytes 若超出 reviewed 文件边界，Phase 2 停止并进入 scope
confirmation。脚本只执行确定性 projection 与校验，不决定 Release readiness。

## Docs SSOT Plan

- `ssot_first`：release mapping 的 durable owners 是
  `trellis/guru-team-extension.json` 与根 `README.md`。
- `.trellis/spec/docs/public-docs.md` 同步 stable public documentation contract 中的
  `.3/.39/CLI 0.6.15` mapping。
- `docs/requirements`、`docs/design`、`docs/test` 与 `docs/architecture` 的 active
  authority 保持 `current-main-0.6.5-guru.41`；#311 已完成该 authority promotion，
  本 Release 不改变产品行为、Skill public API、架构 decision、owner、GAP 或
  compatibility exit。
- `release-notes-zh.md` 是 task-local Release notes source；它记录 payload、验证结果、
  安全/部署影响、空 assets 与未验证边界，不成为共享 Requirements/Design/Test 或
  Architecture authority。
- historical tasks、released-history 和 live Issue historical comments 明确属于
  non-contract history，不参与 mutable release mapping uniqueness check。

## Architecture Impact

Planning-stage impact 预期为 `no_architecture_impact`：本任务只更新 release identity、
public install projection、test assertion 与 task-local evidence，不改变
`guru-trellis-design-constitution-v1`、`guru-trellis-architecture-change-contract-v1`、
architecture owner、single-writer、public API、runtime boundary 或 GAP lifecycle。

Architecture owner 必须基于 live baseline `current-main-0.6.5-guru.41` 重新判定并返回
`baseline_current`。若 live authority 或实际 diff 证明存在 architecture impact，本设计
失效并进入 architecture planning route；不得用本段预期替代 owner judgment。

## Test 与 Evidence 分层

### Preparation branch evidence

- release identity literal scan；
- manifest/schema/fixture unit tests；
- preset apply 与 overlay drift；
- source/installed package validators；
- Finalizer、Publication、routing、ownership、workspace-boundary 定向 regression；
- credential、secret、private-key、signed-URL 与 sensitive-path scan。

这些结果只证明 preparation branch，不证明 published exact candidate。

### Post-merge exact-candidate evidence

- predecessor peeled commit 到 candidate 的完整 committed diff review；
- required ancestor checks；
- full package/runtime/routing/ownership/release identity suite；
- clean throwaway workflow install、preview、switch、preset apply、reapply、official update、
  clean install、existing install/update；
- Shared、Codex、Claude、Cursor actual-load 与 projection equality；
- 不含 source tree 的 installed business repository Publication/Finalizer 全链；
- #312 clean tracked planning-file 正常路径及 untracked/staged/unstaged/deleted/renamed/
  review-metadata/reviews fail-closed matrix；
- metadata-tail provenance-only diff 与 publication fast-forward identity；
- residue-zero 与 secret scan。

每条 evidence 绑定同一 candidate commit/tree。任何 FAIL、SKIP 或 SHA mismatch 阻断 tag。

## GitHub 副作用边界

commit、push、PR create、merge、annotated tag、tag-pinned smoke、GitHub Release、Issue
closure 与 cleanup 分别展示 live target、命令和预期结果，并分别取得当前确认。PR body
使用 `Refs #267`。tag 与 Release 不由 Finalizer 自动创建。

#311 不进入 preparation PR 的 `close_issues`，也不随 #267 Release closeout 自动关闭。
Release 发布后，独立业务仓验证先绑定正式 `.3` 安装身份，再重试原 Finalizer 失败路径与
错误文件路径。只有全部通过且 live #311 仍与该根因一致时，才进入独立 Issue closure；
失败、SKIP、stale、身份不匹配或根因未闭环时保持 OPEN。

## Recovery

- pre-tag failure：保留 branch/candidate facts，修复动作必须取得新 scope authority；修复后
  重新走 affected check、commit、review、merge 与 candidate freeze。
- tag 后 smoke failure：保留 immutable tag，记录 failure，停止 Release creation。
- Release reread mismatch：不关闭 #267，停止并报告 live mismatch。
- #311 business-repository proof 缺失或失败：不关闭 #311；不把该缺口写成本 Release tag
  identity failure。Release 已成功时保留其 immutable identity，另行报告业务仓验证结果。
