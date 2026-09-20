# 07 自动推导、候选选择与显式指定

## 1. 要解决的问题

统一模型必须同时阻止两类失败：系统把不唯一或不合法的 hint 当成 authority，以及系统在不能自动得到
唯一结果时拒绝用户指定合法 target。所有 task、branch、checkout、session recovery 和 manual cleanup 都
必须使用同一 resolution protocol。

## 2. Shared resolution protocol

每次 resolution 固定经过以下阶段：

```text
discover -> validate_all -> classify -> select_or_specify -> revalidate -> act
```

各阶段职责如下：

1. `discover`：从 current durable authority 与 live facts 发现候选，不作选择；
2. `validate_all`：对每个候选执行同一完整 validator；
3. `classify`：按 validated candidate 数量返回 automatic 或 selection-required；
4. `select_or_specify`：用户选择已展示 candidate，或输入未展示 target；
5. `revalidate`：mutation 前重新发现并执行同一 validator；
6. `act`：只有 fresh validation 成功后进入 owning transaction。

Hint 只参与 discovery。Task directory、branch name、cwd、Issue number、旧 mapping、历史 path 与唯一文本
命中均不能跳过 validator。

Validator必须区分 `invalid_candidate` 与 `authority_conflict`。当 discovered object 声称绑定当前 authoritative
TaskLifecycleKey/branch，却在 repository、TaskId、generation 或 exclusivity 上冲突时，owner返回 conflict，
不得把该对象降级为普通 rejected candidate 后继续自动选择。Selection只处理没有 authority contradiction
的零/多候选状态。

## 3. Automatic result

只有 validated candidate set 的数量恰好为 1 时返回 automatic selection。以下情况均不返回 automatic：

- discovery 只有一个候选，但 validator 失败；
- 多个候选中只有一个路径与 cwd 相同；
- 多个候选中只有一个为 primary checkout；
- 多个候选中只有一个 name 与 TaskId 相似；
- legacy hint 与一个候选匹配，但 identity 未建立；
- candidate facts 在 mutation 前已变化。

Automatic selection 不授予 ownership，不代表 semantic gate pass，也不代表 mutation authorization。

## 4. Selection-required

不存在 authority conflict，且 validated candidate 数量为 0 或大于 1 时，owner进入 `selection_required`，
当前对话展示：

- candidate label；
- portable identity；
- 当前 live path，仅在 checkout/resource 场景展示；
- branch/ref；
- HEAD；
- validation result；
- 被拒绝原因；
- 选定后将执行的 mutation 类型。

Candidate label 与 candidate snapshot 只服务当前交互。它们不写入 tracked artifact、ignored control state、
session record、gate artifact 或 public typed exit。

`selection_required` 不是 terminal failure。Owner保持当前 lifecycle 不变，等待本次对话中的 target input。

## 5. User input routes

用户输入只有两个结构化 route：

- `select_candidate`：引用当前展示的 candidate label；
- `specify_target`：提供 target 所需的 portable identity，并在 checkout 场景提供当前 path hint。

未列出的 target 与已列出的 candidate 使用同一 validator。显式输入不降低以下校验：

- repository identity；
- TaskId 与 generation；
- TaskRef 指向的 artifact identity；
- branch exclusivity；
- reserved control-ref exclusion；
- resource claim conflict；
- checkout registration/common dir/branch；
- operation-specific cleanliness 与 HEAD relation；
- current source/scope/target freshness。

合法显式 target 必须恢复流程。非法 target 返回精确 reason code、失败字段与可修正条件，保持
`selection_required`；它不得把整个 task 标记为不可恢复。

## 6. Freshness

用户选择后不信任旧 snapshot。Owner重新执行 discovery 与 validation：

- target 仍存在且 facts 不变：进入 action；
- target path 移动但 portable identity 仍唯一：使用 fresh path；
- target HEAD、branch、ownership、task artifact 或 registration 变化：旧选择失效；
- candidate set 变化：展示新的 current set；
- target 已消失：返回 correctable `target_no_longer_present`。

Candidate label 不作为 freshness token。Mutation identity 由 fresh portable facts 与 owning transaction
precondition组成。

## 7. Public contract boundary

跨 Skill public DTO 不传递 candidate path、候选列表、HEAD snapshot 或用户选择。处理选择的 semantic owner
在同一 invocation/re-entry 内重新取得 target，然后只输出下游直接需要的 stable identity。

当平台无法保持当前对话内存时，owner重新 discovery 并重新展示候选。它不得把候选 snapshot 写入 durable
state 以绕过重新读取。

## 8. Protocol applications

| 场景 | Candidate identity | Validator owner |
| --- | --- | --- |
| Legacy TaskId establishment | proposed TaskId | `guru-establish-task-identity` |
| Active task resume | TaskLifecycleKey | Session/Task resolver |
| Missing branch association | full branch ref | `guru-establish-task-branch-binding` |
| Checkout resolution | registered checkout | Checkout resolver |
| Rebind target | new ref in current checkout，或 existing branch + live checkout target | `guru-rebind-task-branch` route-specific validator |
| Cross-machine task artifact与destination binding | repository + explicit ref + TaskId/generation + declared current branch ref | `guru-checkpoint-task-state` / `guru-transfer-task-machine` |
| Terminal manual cleanup | exact resource identity | `guru-cleanup-task-resources:manual_cleanup` |
| Archived intent | explicit intent,不是 candidate inference | Finish/Reactivate router |

Archived `finish_recovery` 与 `reactivate` 不使用 candidate count 推断。用户先声明 intent，再进入对应
validator。

`refs/heads/guru-task-lifecycle/*`是machine-transfer control namespace，不是task branch、Delivery target、
checkout acquisition或Rebind candidate。任何显式输入命中该namespace都返回`reserved_control_ref`，保持原
lifecycle state不变。

## 9. Failure matrix

| Candidate result | Route |
| --- | --- |
| 恰好一个 valid | automatic target，mutation 前 revalidate |
| 零 valid且存在 rejected candidates | selection-required，展示 rejection reasons |
| 零 discovered | selection-required，接受 explicit target |
| 多个 valid | selection-required，禁止 heuristic selection |
| discovered object 与 authoritative identity冲突 | conflict owner，禁止 selection绕过 |
| 用户选择 stale candidate | rediscover 并展示 current result |
| 用户指定 valid unlisted target | 正常进入 action |
| 用户指定 invalid target | correctable rejection，保留 lifecycle |
| 用户选择 caller-owned resource | ownership 保持 caller-owned |
| 用户选择 cleanup target | 只确定本次 manual deletion candidate，不改写历史 ownership |

## 10. 当前设计结论

本问题固定以下结论，最终状态仍由全量审核决定：

1. 自动选择只发生在恰好一个 validated candidate；
2. 零候选与多候选都进入可继续的 selection-required；
3. 用户能选择 candidate，也能显式输入未列出的 target；
4. 自动与人工 target 使用同一 validator；
5. 用户选择不授予 ownership、semantic pass 或 mutation authorization；
6. candidate path 与 HEAD 不进入 public或 durable state；
7. invalid manual input 返回可修正原因，不造成不可恢复 fail-close。
