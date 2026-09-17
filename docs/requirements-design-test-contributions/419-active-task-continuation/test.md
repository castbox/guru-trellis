# #419 Active-task continuation Test contribution

状态：`task_isolated_candidate`。以下为 R419/D419 的验收设计，不是 PASS 记录；实际 evidence 必须由
Phase 2、independent full Branch Review 与 exact-candidate matrix owner 从当前 bytes 重新产生。

- `T419-01`（R419-01）：canonical 与 dogfood workflow 各恰有一个非空 continuation block；上游
  candidate extractor 返回相同 Guru body。六类 state/invalid state 进入声明 owner/stop，零 inventory fallback。
- `T419-02`（R419-02）：真实 task/worktree fixture 覆盖 current created DTO direct consume、created output
  loss same-owner recovery、partial planning、wording stale、Planning Architecture stale、Approval loss、
  confirmation loss、activation initial 与 activation output-loss recovery；断言零第二 workspace/branch/task/start。
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
  不在 Guru inventory/overlay/managed claims；preset reapply 前后这些 bytes 与 active workflow bytes 完全相同。
  Guru preset 缺失返回明确的 incomplete-dependency failure，不推断 native fallback。
- `T419-08`（R419-07）：matrix 先验证 candidate full SHA
  `43fffc170927c85d9f7fc106cc5a059e80d4530b`、ordered parents 与 tree，再执行 clean install、supported
  existing update、native -> Guru -> native switch 和 preset reapply。每次 switch 后立即读取 current
  continuation，拒绝 cached/old route。
- `T419-09`（R419-07）：matrix 最终比较 source/installed/dogfood/declared-platform Guru-owned bytes 和
  executable modes，运行 ownership/package/drift validators，并递归断言 `.new`/`.bak`、`__pycache__`,
  `.pyc`, `.pyo` 均为零。
- `T419-10`（全部）：测试使用正式 production wrappers 与真实 fixtures，不预填 semantic pass、不手写
  downstream DTO、不复用旧 candidate/evidence、不保留成功 retired checkpoint、不以静态关键词命中代替
  route/mutation/consumer 行为。
- `T419-11`（R419-08/D419-09）：扫描 current manifest、installer、installed validator、matrix source/tests
  不存在 removed-API migration capability 或专项 allowlist；existing cell 更新后 current source/installed
  runtime contract exact parity，任一 missing、extra、identity 或 version drift 均 fail closed。
- `T419-12`（R419-09/D419-10）：扫描 runtime、installer、validator、matrix、spec、active package tests 与
  promoted shared-current authority，不存在已退役内部 API capability、专用命名、fixture、例外分支、兼容
  reader 或 migration path。Immutable superseded/history 仅作为历史记录，不计入 current contract 或
  parity input。

本 test contribution 不声称 full multi-platform Release matrix、tag、GitHub Release、生产业务验证或 #410
candidate evidence 完成。#419 合并后 #410 必须从新的 live `origin/main` 重新冻结候选并重跑自己的 gate。
