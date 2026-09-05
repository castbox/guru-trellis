# 设计

## 问题本质

当前失败发生在 eval corpus 的静态 schema 校验阶段，而不是 Merge runtime 执行阶段。
case 引用了公共 eval 合同未声明的 trace invariant，runner 也无法生成或解释该 invariant。

## 方案

在 canonical
`trellis/skills/guru-team/packages/guru-merge-task-pr/evals/evals.json` 中删除
`no-merge-mutation` assertion，只保留 `expected-route` assertion。

随后使用 Guru Team preset installer 同步 dogfood installed 和平台投影，不直接维护生成副本。

## 合同边界

- `skill-evals-1.0` 的三种 trace invariant 用于证明 public invocation 隔离边界，不承担
  每个业务出口的副作用语义验证。
- `phase2_reentry_required` 的无 Merge mutation 性质继续由 Merge package runtime test
  直接验证；该测试 mock 底层 command runner 并断言未被调用。
- public input/output、typed exit、consumer、Merge runtime 和 Release version mapping 均保持
  不变。

## 取舍

不向 schema/runner 新增 `no_github_write`。新增该能力需要定义可观测 GitHub write 的完整
trace 语义、adapter 采集和跨平台验证，会把一个局部 corpus 缺陷扩张为公共 eval API 变更；
现有 package test 已在更接近执行边界的位置证明目标性质。

## 回滚

该变更只删除一个 invalid assertion。若验证发现现有测试不足，应回到 Planning 重新设计可执行
的通用 trace 合同，而不是恢复未实现的枚举值。

