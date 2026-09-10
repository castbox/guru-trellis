# #392 Release v0.6.16-guru.1 Test contribution

状态：`reviewed_candidate`；关系：`pending_promotion`。以下条目定义 candidate 的验证合同，
不记录动态执行结果，也不把定向文档检查、Stage 1 evidence 或历史 #378 evidence 表述为
#392 Release pass。

- `T392-01`：验证 canonical、dogfood、installed manifest 以及 current release-facing 文档、
  fixture、schema、validator 和安装入口只投影
  `v0.6.16-guru.1` / `0.6.16-guru.41` / CLI `0.6.16` / fixed Fork full SHA；
  历史 predecessor mapping 只存在于明确 released/superseded context。
- `T392-02`：验证五文件 RDT contribution、Architecture contribution identity、expected `.47`
  与 candidate `.48` 的 predecessor/successor 及 traceability 完整；promotion 前唯一 active
  authority 仍为 `.47`，`.48` 不得被标记为 promoted/current/active。
- `T392-03`：验证 source/installed package、managed byte/mode parity、Shared/Codex/Claude/
  Cursor projection、ownership、all-platform preset reapply、dogfood drift、`.new`/`.bak`/
  sidecar 与 `git diff --check` 等 Stage 1 preparation checks。
- `T392-04`：验证 repository-private release skill 四平台 contract 字节一致，且 Stage 1
  在 promotion 前后分别执行 fresh Phase 2、task commit 和完整 `origin/main...HEAD` Branch
  Review，覆盖全部 delivery/Docs contribution bytes；P0-P3 open findings、stale review 或
  promotion-created 未复核 diff 均阻止 Publication/Finish。
- `T392-05`：preparation merge 后从 clean fresh `origin/main` candidate 执行 predecessor
  lineage/full diff、version mapping、source/installed validators、四平台 parity、
  install/update/workflow switch/reapply、Fork source/build、代表性业务仓库 installed smoke、
  secret scan 与递归 residue gate；所有结果必须绑定同一 commit/tree identity。
- `T392-06`：验证 annotated tag、tag-pinned smoke、GitHub Release、Issue close 与 cleanup
  各自重新读取 live authority并保持独立动作边界；任一 required `FAIL`、`SKIP`、stale、
  cross-SHA 或 unknown/multiple/unmapped exit 都在后续 mutation 前停止。

## Fixed scenarios

| Scenario | Expected result |
| --- | --- |
| `SCN-077 Stage 1 serialized promotion` | pre-promotion committed review 通过前 `.47` 保持唯一 active authority；promotion 后必须对 created diff 完成 fresh Phase 2/commit/Branch Review，第二次 review 通过前 Publication/Finish 不可达。 |
| `SCN-078 exact-candidate release` | Stage 1 merge 后只接受 fresh `origin/main` exact candidate；同一 candidate 完成全部 required gate 后才可依序进入独立 tag、smoke、Release、Issue close 与 cleanup 边界，缺失或失败立即停止。 |

当前 Stage 1 Phase 2、task commit、完整 Branch Review、PR merge，以及 Stage 2 exact
candidate、Release Gate、annotated tag、tag-pinned smoke、GitHub Release、latest-stable
晋升、Issue close 与 cleanup 均保持 `unverified`。本段只声明稳定验证边界，不持久化
Gate/checkpoint 或 runtime 状态。
