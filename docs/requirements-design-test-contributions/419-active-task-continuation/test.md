# #419 Active-task continuation Test contribution

状态：`absorbed_historical_source`。以下为 R419/D419 promotion来源；实际current策略位于`.54`。
Promotion-created diff仍须fresh Phase 2、Task Commit与independent full Branch Review。

- `T419-01`（R419-01）：canonical 与 dogfood workflow 各恰有一个非空 continuation block；上游
  candidate extractor 返回相同 Guru body。六类 state/invalid state 进入声明 owner/stop，零 inventory fallback。
- `T419-02`（R419-02）：真实 task/worktree fixture 覆盖 current created DTO direct consume、created output
  loss same-owner recovery、partial planning、wording stale、Planning Architecture stale、Approval loss、
  confirmation loss、activation initial 与 activation output-loss recovery；initial current identity mismatch
  必须在 task status/counter 变化前失败，断言零第二 workspace/branch/task/start。
- `T419-03`（R419-03/04）：Phase 2 adjacent DTO 直达 Task Commit；lost DTO 只通过 current retained
  checkpoint 的 existing checker -> invoker rematerialization。Missing/stale/consumed checkpoint 必须 fresh
  rerun，测试不得声明或注册新 Phase 2 recovery profile。
- `T419-04`（R419-04）：Task Commit 真实 Git fixture 覆盖 same-candidate stdout/output loss，ref 只前进一次，
  返回同一 commit；拒绝第二 candidate、空 commit、amend、same-content commit 与无法唯一证明的 Git shape。
- `T419-05`（R419-03/04）：Branch Review adjacent `passed` 直达 Publication；lost/retired output 对 current
  complete committed range fresh Architecture + independent review。Publication adjacent `ready` 直达 Finalizer；
  lost/retired output fresh review current payload。Base/HEAD/content/authority drift 回最早受影响 owner。
- `T419-06`（R419-05）：SessionStart、UserPromptSubmit、显式 start/continue、“继续”和无 pending plan 的
  “确认继续”对同一 exact task 收敛。Current plan 确认只执行展示 payload；成功 exit 自动续接，新副作用/
  选择/stop 暂停；executor failure 零 success exit；无 exact task 零 inventory selection。
- `T419-07`（R419-06）：ownership/overlay/preset tests 证明 upstream-owned start/continue/hooks/platform/meta
  不在 Guru inventory/overlay/managed claims；#419 task diff 不修改这些 bytes 或 active workflow ownership。
  Guru preset 缺失返回明确的 incomplete-dependency failure，不推断 native fallback。
- `T419-08`（R419-07）：先验证 candidate full SHA
  `43fffc170927c85d9f7fc106cc5a059e80d4530b`、ordered parents 与 tree，再运行 upstream extractor、
  `get_context.py --mode continuation`、`trellis-start` 与 `trellis-continue` 定向合同测试。
- `T419-09`（R419-07）：运行 source/installed package runtime、eval、正式 wrappers 与真实 Git/task fixture，
  比较 source/installed/dogfood/declared-platform Guru-owned projections，运行 ownership 与 dogfood drift
  validators，并检查当前工作树 `.new`/`.bak`、`__pycache__`、`.pyc`、`.pyo` 与 `git diff --check`。
- `T419-10`（全部）：测试使用正式 production wrappers 与真实 fixtures，不预填 semantic pass、不手写
  downstream DTO、不复用旧 candidate/evidence、不保留成功 retired checkpoint、不以静态关键词命中代替
  route/mutation/consumer 行为。
发布安装、更新、workflow switch 与 preset reapply 的验收完全由 #410 拥有。#419 合并后 #410 必须从新的
live `origin/main` 重新冻结 Guru release candidate 并从零执行其 Release Gate；#419 的部分或中断结果不是
#410 evidence。
