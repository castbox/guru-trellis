# #267 Release routing caller inventory 修复需求

## Authority And Current Facts

唯一 current requirement authority 是 live Issue #267 body
`2026-08-30-r19`。本任务从
`main@736ef3335f1b1b0dcbf92f1e8e53343f922aa32a` 开始，只处理该 SHA 的
pre-tag verifier 已确认的 caller inventory drift。历史 Issue comments、旧 task 结论和
`736ef333...` 上的失败证据只提供事实背景，不是新候选的通过证据。

固定 Release identity 保持不变：

- repo annotated tag：`v0.6.15-guru.3`；
- Guru Team extension revision：`0.6.15-guru.39`；
- target / required / tested Trellis CLI：`0.6.15`；
- predecessor peeled commit：`d907fcc5e17f23b6499648e5e9a208457f2d6f8b`。

`736ef333...` 已包含以下 required ancestors：

- Issue #311 fix commit：`5b3b7bef73824ae78b8bf13a20cfd9ba01acb2b8`；
- PR #313 merge commit：`21c7da14798683193b460a5e7c5bd24c7c517804`；
- PR #314 merge commit：`3efcce72a0d47e38ec725aa8c0f8498992f3416f`。

该 SHA 的 exact-candidate verifier 和独立 routing reproduction 均返回：

```text
secondary caller inventory drift:
missing=['package-runtime-python_subprocess_second_hop-e38ded41d714']
stale=['package-runtime-python_subprocess_second_hop-f16c2314ce2a']
```

## Goal

修复 Finalizer subprocess second-hop 的 canonical caller inventory 锚点，使 inventory
discovery 与 checked inventory 再次一致，为修复合并后的 fresh remote `main` 重新冻结
exact candidate 消除该 blocker。

## Requirements

### R1 Replace The Exact Stale Row

只修改
`trellis/presets/guru-team/tests/throwaway-python-callers.json` 中 `id` 为
`package-runtime-python_subprocess_second_hop-f16c2314ce2a`、`anchor_sha256` 为
`f16c2314ce2a58849f85dbaa00ebe495a6be7171d275b3c682acdc9ee38de6c3` 的唯一现有记录。
该记录同时满足 owner 为
`trellis/skills/guru-team/packages/guru-finalize-task/runtime/owner.py`、kind 为
`python_subprocess_second_hop`、ordinal 为 `1`。同一 owner 下存在其它 second-hop
记录，不能只用 owner/kind/ordinal 选择目标。

保留该记录的 `owner`、`kind`、`classification`、`expected_launcher` 与 `ordinal`，只把：

- `id` 从 `package-runtime-python_subprocess_second_hop-f16c2314ce2a` 替换为
  `package-runtime-python_subprocess_second_hop-e38ded41d714`；
- `anchor_sha256` 从旧值替换为
  `e38ded41d71415ba6ad37adf6bc282c13798ce4b1d7181444ac7abb0d2843ea6`。

### R2 Preserve Behavior And Public Contracts

- 不修改 Finalizer runtime、routing discovery 算法、launcher resolution 或 subprocess
  behavior。
- 不修改公共 Skill input/output、schema、typed exit、consumer、registry 或 package
  ownership。
- 不修改 Release identity、extension manifest、README、preset installer 或平台 projection。
- 不修改 Requirements/Design/Test/Architecture `.42` current authority。

### R3 Preserve Release And Issue Boundaries

- 本任务不创建 tag、GitHub Release 或 asset。
- 本任务不关闭 #267、#311 或其它 Issue。
- 修复分支验证只证明 inventory consistency，不证明十三项 exact-candidate Release Gate
  已通过。
- 修复合并后必须从 fresh remote `main` 记录新 candidate SHA/tree，并在该单一 SHA 上
  重跑 live Issue #267 r19 的全部十三项 pre-tag gates。
- `736ef333...` 的失败证据不得转写成新 candidate 的通过证据。

## Exact File Boundary

实现 diff 固定为：

- `trellis/presets/guru-team/tests/throwaway-python-callers.json`；
- `.trellis/tasks/08-30-267-release-routing-inventory-fix/` 内的本任务文件。

实现阶段若发现必须修改上述边界外的 tracked file，立即停止并返回 scope review。

## Acceptance Criteria

1. inventory JSON 可解析；实施前旧 `id` + 完整旧 `anchor_sha256` 精确匹配一条记录；
   实施后目标数组中精确存在一条新记录，旧 `id` 与旧 `anchor_sha256` 均不存在。
2. 新记录的五个保留字段与修复前完全相同，只有 `id` 与 `anchor_sha256` 发生变化。
3. caller inventory checker 返回 PASS，missing 与 stale 集合均为空。
4. routing 定向测试完成 `44/44`，error 与 failure 数均为 `0`。
5. `git diff --check`、task validation、exact-path scan 与 JSON structural check 均通过。
6. `.new`、`.bak`、未声明 sidecar、secret 和边界外 dirty path 数量均为 `0`。
7. fresh Architecture Planning/Phase 2/Branch Review judgments 均确认没有架构 authority
   或行为合同变化。
8. 合并后的 fresh candidate 仍包含三个 required ancestors；`.3` tag/Release 在十三项
   pre-tag gates 全部通过前保持不存在。

## Out Of Scope

- 修改 Finalizer 的 `*platform_args` 实现或回退 `ef5a916a`。
- 调整 caller discovery、anchor 生成算法或 inventory schema。
- 扩张为完整多平台 Throwaway/Release matrix；该矩阵由 #267 在 post-merge exact
  candidate 上独占执行。
- 修改 Trellis upstream、global npm、`node_modules` 或业务仓。
- commit、push、PR、merge、tag、Release、Issue closure 或资源清理。

## Blocking Open Questions

无。
