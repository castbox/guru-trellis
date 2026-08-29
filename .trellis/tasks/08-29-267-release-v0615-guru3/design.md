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

初始 preparation commit `2a5461002856ebcb981156f892e41ef4020d3626` 的独立 Branch
Review 已发现 `.39` source manifest 与 `.37` active authority 冲突。该 commit 只作为
被阻断的历史节点保留；r18 先形成 task-owned RDT/Architecture contributions，完成
Phase 2、commit 与独立 Branch Review，再由 serialized promotion 激活 `.42`。promotion
产生的 shared-current diff 已重新执行 Phase 2 与 commit；post-promotion Branch Review
随后发现历史 `.39` status marker 仍声明 active，r19 只追加该状态收敛后再重新进入
Phase 2、commit 与独立 Branch Review。

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
- 当前 `.41` authority 中的 `.37` current-candidate facts 与 committed `.39` source
  manifest 冲突。contribution 阶段只写
  `docs/requirements-design-test-contributions/267-release-v0615-guru3/` 与
  `docs/architecture/contributions/267-release-v0615-guru3.md`；shared current 仍由
  serialized promotion owners 单写。
- promotion 已按 live owner dependency 先执行 Architecture、后执行 RDT；两条最小
  `.trellis/spec` locator/usage projection 同步到 `.42/#267`，不形成第三 authority。
- successor knowledge authority 固定为 `current-main-0.6.5-guru.42`。promotion 后
  `.42` 是唯一 active RDT/Architecture authority，`.39` 与 `.41` 保留为 superseded history，
  current/canonical extension candidate 为 `0.6.15-guru.39`，Trellis CLI 保持
  `0.6.15`。
- r19 对 `.39` 的收敛只修改六个 versioned authority 文件的 status marker；历史内容、
  source binding、extension identity 与 evidence 不变。递归 scan 必须只命中 `.42`
  active，不以 README navigation 单独替代 versioned-file status 证明。
- `.42` 只承接 release/current facts、traceability、navigation、evidence 与历史绑定；
  不改变产品行为、Skill public API、Architecture decision、owner、GAP 或
  compatibility exit。
- `release-notes-zh.md` 是 task-local Release notes source；它记录 payload、验证结果、
  安全/部署影响、空 assets 与未验证边界，不成为共享 Requirements/Design/Test 或
  Architecture authority。
- historical tasks、released-history 和 live Issue historical comments 明确属于
  non-contract history，不参与 mutable release mapping uniqueness check。

## Architecture Impact

本 r19 scope 对 shared Architecture knowledge authority 存在受控
`architecture_impact / target_native`：变化是从 `.41` 到 `.42` 的 current fact、evidence
与 predecessor/successor binding，不是 Architecture decision、owner topology、runtime
boundary、GAP lifecycle 或 compatibility exit 变化；新增 `.39` 历史 status 收敛不改变
Architecture Baseline identity 或上述边界。

Architecture contribution 绑定 current baseline `current-main-0.6.5-guru.41`、
constitution `guru-trellis-design-constitution-v1`、change contract
`guru-trellis-architecture-change-contract-v1` 与 expected-current `.41`。ADR
`required=false`。shared current 只有在 contribution 通过独立 committed full-diff review 后
才由 promotion owner 激活；promotion-created diff 必须重新进入 Phase 2、commit 与 Branch
Review。

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
- contribution review failure：不写 shared `.42`；保留 `.41` current，并返回 task work。
- promotion 时 live current 不再是 `.41`：返回 `sync_required`，不得覆盖新的 current。
