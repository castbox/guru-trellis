# #267 Release routing caller inventory 修复设计

## 1. Root Cause

Commit `ef5a916a` 把 Finalizer preset apply 调用改为通过 `*platform_args` 组装参数。
该行为修复改变了 subprocess second-hop 的 AST anchor，inventory discovery 因此生成新
identity `e38ded41d714...`。canonical caller inventory 仍保存旧 identity
`f16c2314ce2a...`，导致 checker 同时报告一条 missing 与一条 stale。

discovery 输出与 source AST 一致；缺陷位于声明式 inventory 未随 owner 调用点更新，不在
runtime routing 或 launcher resolution。

## 2. Single-Row Correction

实施只对目标 JSON object 执行两个字段替换：

```json
{
  "id": "package-runtime-python_subprocess_second_hop-e38ded41d714",
  "owner": "trellis/skills/guru-team/packages/guru-finalize-task/runtime/owner.py",
  "kind": "python_subprocess_second_hop",
  "classification": "installed_managed",
  "expected_launcher": "sys.executable",
  "anchor_sha256": "e38ded41d71415ba6ad37adf6bc282c13798ce4b1d7181444ac7abb0d2843ea6",
  "ordinal": 1
}
```

不重新排序数组，不格式化整个 JSON，不重写邻接记录。这样可把实现 diff 限制为 discovery
已经证明的 identity 漂移，不引入 runtime 或 contract delta。

## 3. Preserved Invariants

- owner 仍是 canonical Finalizer `runtime/owner.py`；
- call kind 仍是 `python_subprocess_second_hop`；
- classification 仍是 `installed_managed`；
- launcher contract 仍是 `sys.executable`；
- ordinal 仍是 `1`；
- source/dogfood/installed runtime bytes 均不改变；
- Release `.3/.39/CLI 0.6.15` mapping 与 `.42` authority 均不改变。

同一 owner 下存在四条合法 second-hop 记录，因此目标选择器固定为旧 `id` + 完整旧
`anchor_sha256`，再校验五个保留字段。若该 exact preimage 不是唯一一条，或 fresh discovery
不再生成上述 new identity，本设计失效并返回 Planning，不猜测另一条 inventory 修改。

## 4. Alternatives And Trade-offs

### Selected: Replace The Stale Declarative Identity

该方案直接恢复 source discovery 与 canonical inventory 的一一映射，修改面最小，并保留
`ef5a916a` 已验证的平台参数修复。

### Rejected: Revert Finalizer Platform Arguments

回退 `*platform_args` 会重新引入 Claude-only installed repository 被扩张为全平台的已修复
缺陷，违反 #267 current contract。

### Rejected: Loosen Inventory Checking

忽略 anchor drift 会削弱 caller ownership 与 launcher consistency gate，并使真实 source
变化无法阻断 Release，不满足 current checker contract。

### Rejected: Regenerate Or Reformat The Whole Inventory

全量重写会扩大 review surface，掩盖单条 identity 修复，并制造与本缺陷无关的排序或格式
delta。

## 5. Validation Design

### Task-Level Proof

1. 使用 JSON parser 验证文件结构。
2. 实施前断言旧 `id` + 完整旧 `anchor_sha256` 精确匹配一次；实施后断言新 `id` 与完整
   new `anchor_sha256` 各出现一次，旧值出现次数为 `0`。
3. 对比目标 object 的五个保留字段，断言值未变化。
4. 执行 caller inventory checker，要求 missing/stale 数量均为 `0`。
5. 执行 routing 定向 suite，要求 `44/44` 通过。
6. 执行 task validation、exact dirty-path check、sidecar scan 与 `git diff --check`。
7. 在 Phase 2 与 committed full-diff Branch Review 中重新判断实现边界和未关闭 finding。

### Post-Merge Release Proof

分支级 PASS 只解除当前 inventory blocker。PR 合并后由 #267 从 fresh remote `main` 形成
新 candidate，重新执行 required ancestor、完整 committed diff review、package/runtime、
platform/install/update、installed Finalizer、secret 与 residue checks，以及 live r19 定义的
其它 pre-tag gates。任何 FAIL、SKIP、stale、cross-SHA 或 live identity drift 均阻断 tag。

## 6. Docs SSOT Plan

策略：`task_local_only`。

- 本任务只修复由 source AST 重新推导出的 inventory identity，不改变 requirement、behavior、
  architecture、public API、schema、operator workflow 或 release mapping。
- current RDT/Architecture authority `current-main-0.6.5-guru.42` 已准确声明
  `.3/.39/CLI 0.6.15` 与 Release matrix 未验证边界，保持不变。
- planning 文档与后续 task evidence 只记录本 task 的修复边界，不晋升为 durable
  Requirements/Design/Test/Architecture authority。
- Phase 2 fresh scan 若发现 durable authority 与实际 delta 冲突，返回 Docs SSOT
  reconciliation；实现阶段不复制 shared authority。

## 7. Architecture Impact

预期 Planning route 是 `baseline_current` + `no_architecture_impact`。本修复恢复既有
inventory-to-source consistency，不改变 Architecture decision、owner、single-writer、runtime
boundary、GAP lifecycle、compatibility exit、设计原则权衡或 project check descriptor。

若 Architecture owner 返回 impact、conflict、contract incomplete、fitness regression 或
sync route，停止计划批准并消费该 typed route；不把该结果改写成 no-impact。

## 8. Risk And Rollback

- 主要风险是抄错完整 anchor；exact discovery output 与 count assertion 共同阻断该错误。
- 误改邻接记录会被 exact object comparison 和 dirty diff review 阻断。
- branch PASS 被误述为 Release PASS 的风险由 post-merge fresh-candidate boundary 阻断。
- 未提交状态的 rollback 只撤销本 task inventory delta；不得删除 task/worktree、移动 tag、
  rewrite main 或修改业务仓。
