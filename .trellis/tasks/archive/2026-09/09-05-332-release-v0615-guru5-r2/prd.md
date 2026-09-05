# #332 v0.6.15-guru.5 正式发布需求

## 目标

以 fresh `origin/main@3f888c1ad2d0bad5f257794b1f09da24af73f397` 为当前基线，完成
`castbox/guru-trellis` 的正式发布：将 Guru Team extension 从
`0.6.15-guru.39` 提升到 `0.6.15-guru.40`，发布 annotated tag
`v0.6.15-guru.5`，并创建对应的正式 GitHub Release。Trellis CLI 目标保持
`0.6.15`。

## 当前 authority

- 唯一 primary Issue：[#332](https://github.com/castbox/guru-trellis/issues/332)，保持 open，正文是本任务的发布合同。
- selected-base Requirements / Design / Test / Architecture authority：`current-main-0.6.5-guru.43`；
  本 preparation 的 reviewed successor 为 `.44`，并消费 #240/#348 已合入、已独立审查但尚未进入
  shared current 的 owner/RDT/ADR contribution。
- 最新正式 Release：`v0.6.15-guru.4`；其 predecessor peeled commit 为
  `40f8aa8312bfd9650f47e1fa9d6d21b4ff18d5b6`。
- #240、#311、#333、#339、#348、#358、#361 已合入 `main`，其影响必须在本次 exact-candidate
  Release Gate 中重新验证，历史 PR 或 Issue 描述不能替代 fresh evidence。

## 需求范围

1. 将 canonical release identity、manifest、README、workflow/preset 文档、fixtures、
   verifier 断言、canonical/dogfood/installed projection 收敛到
   `v0.6.15-guru.5` / `0.6.15-guru.40` / CLI `0.6.15`。
2. 在 preparation PR 合并后，从 fresh `origin/main` 冻结 exact candidate，审查
   `v0.6.15-guru.4..candidate` 的完整 committed diff。
3. 通过 serialized RDT/Architecture promotion 将 #240 solution-mechanism owner、`ADR-008` 与
   #348 archived-task recovery owner/RDT contract 纳入 `.44` current authority；promotion-created diff
   必须重新进入 Phase 2、task commit 与独立 Branch Review。
4. 承接 #240、#311、#333、#339、#348、#358、#361 的 Release Gate 验收，包括 mechanism
   qualification、archived-task recovery、installed Finalizer、Issue recovery、Finalizer rebind、
   Publication Review re-entry 与两阶段 release orchestration。
5. 运行 source/package/runtime、registry/interface/schema、ownership、managed
   parity、dogfood drift、preset installer、upgrade/update/reapply、平台入口和
   tag-pinned smoke 验证。
6. 在所有 required gate 通过后，分别完成 tag、tag-pinned smoke、GitHub Release 和
   Issue #332 closeout；每个远程或不可逆副作用独立确认。

## 验收标准

- AC1：所有 current release-facing surfaces 对 `.5/.40/0.6.15` 保持一致，历史
  tag、Release 和 authority 原始事实不被改写。
- AC2：preparation PR 合并后 candidate 是 fresh、clean、可复现的 `origin/main`
  commit/tree，完整 diff review 无 P0-P3 open finding。
- AC3：`.44` 是唯一 active RDT/Architecture authority，包含 #240/#348 reviewed contracts、accepted
  `ADR-008` 与 live-derived 23 Skills / 97 exits / 81 commands；promotion-created diff 已完成 fresh
  Phase 2、task commit 与独立 Branch Review。
- AC4：Release Gate 对 #240、#311、#333、#339、#348、#358、#361 的承接链有 exact-candidate
  fresh evidence；FAIL、SKIP、stale、cross-SHA、unknown 或 unmapped exit 均阻断。
- AC5：clean throwaway 与 installed business-repository 验收覆盖 marketplace
  install、workflow preview/switch、preset apply/reapply、official update、
  Publication/Finalizer 代表性全链和 tag-pinned post-publish smoke。
- AC6：annotated tag 的 peeled commit/tree 与 candidate 完全一致，GitHub Release
  非 draft、非 prerelease，标题、正文、target、版本映射和验证边界准确。
- AC7：preparation PR 使用 `Refs #332` 且 `close_issues=[]`，合并时不自动关闭任何 Issue；
  #332 在 Release Gate、annotated tag、tag-pinned smoke 与 GitHub Release 完成后独立 closeout，
  #240、#267、#311、#348 和其他相关 Issue 不被修改或关闭。

## 明确边界

- 不修改 Trellis upstream、全局 npm、`node_modules` 或业务仓库。
- 不移动、删除或重写历史 tag、Release 或 `main` history。
- 不把 `current-main-0.6.5-guru.43` 或旧 Release evidence 当作本次发布通过证明。
- 不将完整累计多平台矩阵、业务部署或未取得的 live model evidence 虚构为已验证。
- 不把用户授权写入 task artifact、gate、tag message 或 Release body。

## 未验证边界

规划阶段不声明任何实现、candidate、tag、Release 或 production smoke 已通过。
具体平台、installed business repository、升级重放和 tag-pinned 结果必须绑定到
实际执行时的 exact candidate。
