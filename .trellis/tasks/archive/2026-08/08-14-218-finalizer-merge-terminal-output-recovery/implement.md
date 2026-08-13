# 实施计划

## Phase A：建立失败 fixture

- [ ] 在 Finalizer/Merge package tests 中增加真实 shell wrapper fixture，先证明 current mutation success path存在空 stdout或错误恢复。
- [ ] 为 fixture提供隔离 Git/GitHub adapter与操作计数，覆盖 fresh、output-lost recovery、stale/mismatch、closure mismatch。
- [ ] 断言 stdout恰好一个 JSON object，stderr不混入成功 payload。

## Phase B：Finalizer terminal 物化

- [ ] 修正 `runtime/execute.py` 与 owner helper的 state dispatch，使 `ready` 直接进入 terminal revalidation/materialization。
- [ ] 复用 current gate/output schema，不调用 Draft-only `cmd_finish_work`。
- [ ] 校验成功消费后的 transaction/gate/request/private state退休。
- [ ] 补 `ready` recovery零 mutation及关键 identity mismatch tests。

## Phase C：Merge terminal 恢复

- [ ] 在 merge/closure完成后先持久化最小 `terminal_output`，再返回 handler dict。
- [ ] 同 gate已 merged时只读重验 merge commit与closure，再消费 terminal output。
- [ ] 保留 `closure_mismatch` terminal route，补零重复 merge测试。

## Phase D：Current/legacy 合同

- [ ] 将无前缀 Finalizer gate/semantic review examples改为 current schema与 `ready_for_merge` consumer。
- [ ] 为 legacy schema/examples使用显式 legacy identity/文件名/说明。
- [ ] 更新 Interface、eval facts、SKILL/contract/README，确保 current business route拒绝 `verification_required`。
- [ ] 仅在确有跨 package不变量时更新 workflow specs。

## Phase E：投影同步

- [ ] 运行 targeted preset apply同步 installed与四平台投影。
- [ ] 逐一检查并处理已知 `.bak`/`.new`，reapply到零 sidecar。
- [ ] 验证 canonical/installed/platform byte equality、managed inventory与dogfood drift。

## Phase F：验证

- [ ] Finalizer package tests与真实 wrapper integration。
- [ ] Merge package tests与真实 wrapper integration。
- [ ] `verify_installed_closeout.py`覆盖 fresh transition、single JSON、ready/terminal recovery、closure mismatch、零重复 mutation。
- [ ] source/installed package validator、interface/schema/graph validation。
- [ ] targeted apply/reapply、managed inventory、dogfood drift、零未知 sidecar。
- [ ] 不运行完整 12-capability extension verification、完整 marketplace/update/全平台 throwaway或业务仓库 upgrade smoke；这些由 #222 承接。

## 风险检查

- dispatcher序列化修复不得造成双 JSON输出。
- terminal checkpoint不得扩大为审计artifact或包含用户授权。
- current schema迁移不得静默破坏 legacy identity。
- Finalizer修复不得开放 #208 existing-PR adoption。
- Merge恢复不得绕过 expected-head或Issue closure验证。

## 完成条件

- Issue #218全部验收标准有真实 wrapper证据。
- `guru-check-task` 完整九维审查通过且无未解决 finding。
- `implementation-handoff.md` 不存在。
