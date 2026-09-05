# Docs SSOT Plan

## 结论

本修复不改变产品需求、Architecture、Design、Test strategy、Skill public I/O、runtime 行为或
release version mapping，因此不修改 shared Requirements/Design/Test/Architecture SSOT。

## 依据

- 当前 SSOT 已要求 `phase2_reentry_required` 不执行 Merge mutation。
- 现有 package test 已直接验证底层 mutation runner 未被调用。
- 当前 eval 合同明确把 deterministic trace grading 限定为三种 public-invocation isolation
  invariant；删除未实现 assertion 是恢复既有合同一致性，而不是修改合同。

## Task-local 记录

缺陷证据、最小修复方案、验证范围和发布后续门禁保留在本 task 的 `prd.md`、`design.md` 与
`implement.md`。若实施中发现必须新增通用 trace capability，则判定为 material scope change，
返回 Planning 并重新评估 Architecture/RDT 影响。

