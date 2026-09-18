# #435 Active Task Delivery Loop Requirements contribution

状态：`absorbed_historical_source`。本 contribution 已由 serialized RDT promotion 吸收到
`current-main-0.6.17-guru.55`；predecessor `.54` 保持 immutable，Architecture 为 `.55/active`。

- `R435-01`：新增 Delivery Review semantic owner，按 approved current slice 审查 requirement、Delivery
  policy、remaining work、independent delivery conditions、validation、RDT/Architecture、base 与 Branch
  Review；只输出 closed minimal typed exit。
- `R435-02`：新增 Delivery Publish owner，绑定 reviewed HEAD、repository/base/head branch 与 exact PR
  payload，执行一次 push/create-or-adopt/converge/Ready；#405 equal-head output loss 必须恢复同一 PR，零重复
  mutation。
- `R435-03`：新增 Delivery Merge owner，只允许 merge commit，以 expected head、checks、base、method 与
  exact subject/body 执行一次 mutation；merge body 必须携带 stable task、schema 1、reviewed head trailers，
  output loss 必须由 terminal live facts恢复同一 Delivery result。
- `R435-04`：Planning/Approval 必须区分 task scope、current delivery slice、remaining work 与 independent
  delivery conditions。Check、Task Commit 与 Branch Review 仍审查完整 current candidate，但只按 approved
  current slice 判断满足性；remaining work 不得被误判为当前遗漏或标记完成，也不新增第二组既有 gate owner。
- `R435-05`：同一 active task 必须支持多个顺序 Delivery cycles。Delivery history 通过 closed merge trailers
  与 GitHub PR/merge、merge commit、parents、repository/base 交叉验证后跨 branch/worktree 重建；禁止 ledger、
  PR-body identity、current-branch 推断或覆盖 immutable task creation facts。
- `R435-06`：#436 完成 Reactivate 与 current workspace binding 后，本闭环只消费新的 current active binding；
  historical merged PR 保持 immutable，新业务变更进入新 PR，tracked archive-to-active move随业务 Delivery
  提交，validation-only Reactivate 不产生空 Delivery，旧 Completion/Finish success 不得证明当前 cycle。
- `R435-07`：#407 base conflict 经 implementation route 与 fresh Phase 2 后，由 Reconcile 消费 exact resolved
  tree，绑定 prior task head、new base、tree object、index digest、ordered parents 与 semantic review，只创建或
  恢复同一个 local merge commit；该路径不 push、不修改 PR/Issue、不绕过完整 Branch Review。
- `R435-08`：三个新 package、closed schemas、consumer declarations、canonical/installed/platform projection、
  preset 与 package-local eval 必须 additive 完整分发并保持 `deferred`。#434 前 production graph、mandatory
  markers 与旧 lifecycle assets不变；禁止 adapter、dual graph 与提前 retirement。代表性验证不等于完整
  Release matrix。

#434 独占 production graph原子切换与旧edge retirement；#436 独占 Completion、Closure、Finish、Cleanup与
Reactivate。本文不授权 commit、push、PR、merge、release 或 cleanup。
