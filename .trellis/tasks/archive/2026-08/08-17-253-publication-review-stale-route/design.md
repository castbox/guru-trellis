# #253 技术设计

## 根因

`finalization_validate_route()` 在非 executor output 的通用字段循环中，先执行：

```python
(
    "branch_review_commit",
    plan["git"]["branch_review_commit"] if plan is not None else None,
)
```

`publication_review_stale` 的 authority 不来自 closeout plan。该 route 在 plan 创建前由 `finalization_publication_owner_result()` 验证 Publication payload，并把原 reviewed commit 投影到 `context["publication_branch_review_commit"]`。通用循环错误地把 plan-backed authority 应用于所有 routes，导致合法 stale commit 在进入专属校验前被拒绝。

## 设计原则

1. 不改变 public schema、Interface 或 consumer projection。
2. 不从当前 HEAD、缺失 plan 或 recorder 输入猜测 reviewed commit。
3. 每个 distinct route 使用其 owner 已验证的 current facts。
4. 修复只调整 stale route 的 authority 选择，不移动或删除相邻 route 的强校验。

## 目标校验流程

```text
Publication owner validates payload
  -> preview context exposes stale status/reason/task/owner commit
  -> AI authors publication_review_stale output
  -> schema validation
  -> task_ref binds public input
  -> branch_review_commit binds Publication owner commit
  -> stale-specific exact status/reason/state checks
  -> recorder/checker/public invocation
  -> guru-review-task-publication
```

## 实现方案

### Route-aware generic field expectation

在现有非 executor output 校验中，仅对 `publication_review_stale` 将 `branch_review_commit` 的期望值切换为 `context["publication_branch_review_commit"]`；其他 exit 继续使用 `plan["git"]["branch_review_commit"]` 或当前既有规则。

这保留通用 schema、task ref 与 plan ref 检查，同时消除 planless stale 对不存在 plan 的依赖。

### Stale-specific exact validation

`publication_review_stale` 分支验证：

- `publication_status == "stale"`；
- transaction state 与 `publication_review_stale` 相容；
- `output.task_ref == public_input.task_ref`；
- `output.branch_review_commit == context.publication_branch_review_commit`；
- `output.stale_reason == context.publication_stale_reason`。

schema 已限制 output 形状和 40 位 commit，runtime 只比较 owner facts，不重复实现 schema。

## 测试设计

### 原生 fixture

在 `guru-finalize-task/tests/test_contract.py` 构造真实临时 Git task：

- Publication reviewed commit 为祖先 commit A；
- 当前 task HEAD 为后续 commit B；
- 无 current closeout plan 与 transaction；
- Publication payload 仍绑定 A。

先断言 preview 识别 stale 且零副作用，再使用 AI-authored合法 output 运行 production route recorder/checker/public invocation。

### 负例

- task ref 被替换；
- commit 不是 Publication owner 返回值；
- stale reason 被替换；
- Publication evidence 已 current；
- adjacent plan-backed output 使用非 plan commit。

### 分发与聚焦安装态

1. 修改 canonical runtime/test/contract。
2. 更新 canonical preset workflow contract SSOT。
3. 运行 preset apply，检查 dogfood/platform equality 与 overlay drift。
4. 在 clean temporary repository 中仅执行 managed preset projection 和 Finalizer stale production wrapper smoke。
5. 不调用 `verify-throwaway-install.sh`，不执行 full initial/update/platform/tag matrix。

## 影响面

### Canonical

- `trellis/skills/guru-team/packages/guru-finalize-task/runtime/owner.py`
- `trellis/skills/guru-team/packages/guru-finalize-task/tests/test_contract.py`
- `trellis/skills/guru-team/packages/guru-finalize-task/references/contract.md`
- `trellis/presets/guru-team/spec/workflow/companion-scripts.md`

### Managed projections

- `.trellis/guru-team/skills/packages/guru-finalize-task/**`
- `.agents/skills/guru-finalize-task/**`
- `.codex/skills/guru-finalize-task/**`
- `.claude/skills/guru-finalize-task/**`
- `.cursor/skills/guru-finalize-task/**`
- `.trellis/spec/workflow/companion-scripts.md`

只有 apply 实际投影的文件进入最终 diff；不手工修改 managed copies。

## 公共 API 与兼容性

- `publication_review_stale` 的三个 seed fields 不变。
- `guru-review-task-publication` consumer/profile 不变。
- schema id、Interface id、command ids、exit ids 和 public examples 不变。
- 旧安装仍表现为 fail closed；新安装接受既有 schema 下原本就合法的 owner-bound stale output。

## 回滚

回滚 route-aware expectation、专属测试与合同文字，再运行 preset apply 恢复 managed copies。无数据、schema、task artifact 或 transaction migration。
