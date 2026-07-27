# #118 Branch Review Round 11 语义门禁汇总

## 门禁结论

- Task：`.trellis/tasks/07-26-118-guru-finalize-task`
- Branch：`feat/118-guru-finalize-task`
- Base：`origin/main@7820a9eeec2a2a75fb52fba156a7211d9f9fb09c`
- Committed HEAD：`77ad13f0a65f652e68e655afbe11917aa659df5c`
- 完整范围：`origin/main...77ad13f0a65f652e68e655afbe11917aa659df5c`
- Diff：526 paths，70807 insertions，4753 deletions
- Review intent：`fresh_final_review`
- 独立审查代理：`/root/issue118_branch_final_review_round11`
- Current findings：P0=0、P1=1、P2=0、P3=1
- Scope proposals：0
- AI Review Gate：`implementation_required`

Round 11 使用未参与 implementation、Phase 2 或 Round 1-10 review/closure 的全新 technical
reviewer，完整覆盖 current committed range。该轮在正常、受支持且无需恶意输入、伪造、并发、
锁、TOCTOU 或 crash 的路径中资格化一个 P1 correctness finding，并确认一个 P3 lint finding。
因此旧 `passed` Branch Review 与所有 publication/finalization evidence 均已 stale；必须先修复、
重跑完整 Phase 2、创建新 task commit，再重新执行完整 Branch Review。

## Scope 与边界

- Live Issue #118 与 accepted-current comment `issuecomment-5045036678` 仍是当前 authority。
- `issue-scope-ledger.json` 仍只将 #118 作为 close issue；#115 不关闭，#119 独占 global Finish
  family integration、combined acceptance 与关闭 #115，#132 独占 upstream overlay cleanup。
- #105 transaction/recovery/legacy takeover 语义不得改变或重新关闭。
- 完整 diff 对 global workflow、upstream `trellis-finish-work` family、official `task.py` 与 preset
  overlays 的 changed-path count 均为 0。
- 恶意 actor、artifact/hash/state forgery、攻击模型、并发 finalizer、锁、TOCTOU、额外 fault
  injection、偶发 crash consistency 与跨 OS atomicity 继续 out of scope。

## Qualification-First Findings

### P1 `F-VERIFICATION-METADATA-REENTRY-01`

- 场景：`normal_required_behavior`；current scope。
- Requirement：`prd.md` R6/R10、AC3/AC6，以及 durable workflow/package/runtime Docs SSOT 要求
  content push 后由 #117 recorder 写出 current、same-plan/ref/HEAD verification evidence，#118 再消费
  `verified` 或 task-bearing standalone `not_required` 继续 finalization。
- 正常 recorder 将 task-local owner evidence 写入 `marketplace-verification.json`。
- 真实 `finalization_preview_context()` 在读取 verification owner 前先执行 publication owner check；
  finalizer compatibility augmentation 的 `finalization_paths` allowlist 仅包含
  `closeout-plan.json` 与 `task-finalization-gate.json`，遗漏上述 #117 artifact。
- 独立最小 Git fixture 稳定返回
  `unexpected_status_paths=[.../marketplace-verification.json]`；真实 preview 因此提前路由
  `publication_review_stale`，无法到达 verification owner checker。
- Source/installed shared eval 各 8/8 通过不能关闭 finding，因为
  `GURU_TEAM_EVAL_STAGING=1` 在真实 publication owner 校验前 early return。
- Severity：P1。该缺陷稳定阻断 content push 后的 required verified/not_required 主发布链。
- Required closure：精确接纳并 owner-validate current plan-bound
  `marketplace-verification.json`，不得放宽 arbitrary metadata；增加不使用 eval staging、真实调用
  #117 recorder 后执行 #118 public wrapper 的 regression。

### P3 `F-ROUND9-TRAILING-WHITESPACE-01`

- 场景：`normal_required_behavior`；current scope。
- `git diff --check origin/main...77ad13f0` 仅命中
  `.trellis/tasks/07-26-118-guru-finalize-task/reviews/round-009-finding-closure.md:203` trailing
  whitespace。
- Severity：P3。它不改变 runtime 行为，但使 required diff hygiene/lint 失败。
- Required closure：删除该行尾空格，并在新 Phase 2 与 Branch Review 中重新验证。

## Current Evidence

- Raw Round 11 report：
  `.trellis/tasks/07-26-118-guru-finalize-task/reviews/round-011-final-release.md`
- Raw report SHA-256：`bbd4d927574b69ea4d8d5deb6c2103e317a714e8db78f24b1a92a2193b2ff56f`
- Raw report：15283 bytes，235 lines。
- Assignment/liveness：Round 11 从 `evt-0374-21142bb1d6` assigned 到
  `evt-0391-c3fd27fd8d` completed；review round 11 与 from10/to11 `new-agent` 决策已登记。
- Round 12 discovery owner report：
  `.trellis/tasks/07-26-118-guru-finalize-task/reviews/round-012-problem-discovery.md`，
  SHA-256 `fb0b284130f09e71db74c2909adc6b96bb7de4bf9908b41e5e5fed47e1b50dcb`，
  15042 bytes，276 lines；from11/to12 `reuse` 决策与 review round 12 已登记，两项 finding 的
  `owner_round=12`。
- Runtime full：620 passed，13 skipped。
- Skill package full：179 passed。
- Preset/ownership：54 passed。
- Publication allowlist + closeout contract focused：100 passed。
- Source/installed shared wrapper eval：各 8/8 passed，但明确属于 staging-only evidence。
- Fresh throwaway：terminal exit 0，覆盖 marketplace discovery、fresh install、official update、
  workflow switch、preset reapply、`.new/.bak` 处理、platform distribution、ownership、overlay drift、
  installed closeout 与 wrapper smoke。
- Workspace boundary passed；source checkout clean；HEAD 在审查前后保持 `77ad13f0`。
- Exact feature ref 尚未 push，remote verification 正确保留给 content push 后的 #117 owner gate。
- Claude native 仍受外部 `401 Invalid API key` 阻塞，未声称 native success。

## Docs SSOT、安全与部署

- Docs SSOT strategy=`ssot_first`。Durable SSOT 已定义 verifier metadata-tail compatibility 与
  verified/not_required re-entry；P1 是 code/test 对 SSOT 的偏离，不是缺少首次 docs merge。
- 未发现 secret、credential、private key、signed URL、`.env` 或客户数据泄漏。
- Dependency、CI/CD、container、Compose、Kubernetes、Helm/Kustomize、DB migration、Makefile、
  Terraform 与 production data-write changed-path scan 均为 0；无需 deploy 或数据迁移。

## 结论与唯一出口

Round 11 current P0/P1/P2/P3=`0/1/0/1`，两个 findings 都已通过 current scope、正常行为和 requirement
binding 资格审核，并由 Round 12 discovery owner 正式持有；没有 scope proposal。唯一合法 typed
exit 为 `implementation_required`，handoff
只包含 task identity、reviewed HEAD 与两个 finding refs。该出口不授权 publication review、push、PR、
archive、Ready、merge 或 Issue closure。
