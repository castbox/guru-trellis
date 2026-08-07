# #178 Technical Design

## 1. Design Summary

采用“live cognition + minimal DTO + lazy private recovery”三层模型：

1. AI 在 discovery owner loop 中直接读取 live Git/GitHub/Trellis、当前/归档会话和必要 docs/code/tests；完整语义证据不成为 public handoff。
2. 正常 `context_ready` 只投影 Clarify 下一步所需的 route/target identity；producer wrapper 在 schema validation 后立即消费并退休 owner material。
3. 只有 active-task owner 真实跨调用恢复时才在现有 ignored `owner-checkpoints/<task-key>/` 下惰性持久化最小 state；正常完成或 terminal exit 后清理。

该设计不新增 workflow step，不改变全局 Intake 顺序，也不让 companion script 承担 semantic 判断。

## 2. Current-to-Target Contract

| Boundary | Current | Target |
| --- | --- | --- |
| Discovery private evidence | `context-discovery.json`, schema `guru-context-discovery-1.0`, `task_local_tracked` | 正常路径 stdout/current-session only；真实 active-task recovery 才使用 ignored runtime current-only checkpoint |
| Discovery public input | `pre_task` + `task_local_reentry` | 仅保留正常 invocation 所需 profile；恢复 locator 是 owner-private invocation detail，不成为跨-Skill public payload |
| `context_ready` output | 含 `handoff_context_locator` | `exit_id`, `handoff_profile`, `handoff_mode`, `handoff_target_locator`, `handoff_continuation_id` |
| Clarify initial input | 含 `context_locator` | `profile`, `source_exit`, `mode`, `target_locator`, `continuation_id` |
| Stale/re-entry | prior snapshot + superseded digest/history | 重读 live authority 并重跑 owner；只有未完成的 active-task recovery 保留一个 current checkpoint |
| Workspace prerequisite | 解析完整 discovery/clarity/readiness artifacts 与 hash linkage | 消费 reviewed typed DTO/authoring seed 与 live facts；不读取 discovery private artifact |
| Cleanup | 多处结果与 superseded runtime 可存活到后续步骤 | producer wrapper consume-and-clean；terminal sweep 验证 owner namespace 零残留 |

## 3. Consumer Inventory

### 3.1 `guru-discover-change-context -> guru-clarify-requirements`

Clarify 的唯一直接需要是：

- 当前 target locator，用于重读 live issue/draft；
- workflow/standalone mode；
- continuation id 与固定 `initial_change_request` profile/source exit，用于确定路由。

Clarify 不需要 discovery artifact path、snapshot digest、history preview、scan inventory 或 reviewer metadata。它自己的 forward behavior 本就要求检查 current Docs/code/tests/history/GitHub/Git evidence；同一 AI 会话可直接承接 discovery cognition，而跨会话 freshness 通过重读 live authority 获得。

### 3.2 `guru-clarify-requirements -> wording/readiness`

Clarify 的 public exits 继续保持最小 route DTO。其 owner result 内的 `context_evidence` 只能作为该 owner 的 transient gate evidence；Wording/Change Request Review 不得通过 `context_locator` 回读 discovery snapshot。需要的 target/scope facts由各 owner 的 current input 与 live reread提供。

### 3.3 `guru-review-change-request -> guru-create-task-workspace`

Workspace planner 只消费 current `ready` DTO、live issue/task naming facts、base sync identity 与当前对话中已完成的 semantic decisions。删除 `TASK_WORKSPACE_PREREQUISITES.context` 对完整 `guru-context-discovery-1.0` artifact 的依赖，以及 example/schema 中的 artifact/digest bundle。Workspace executor仍只执行已审查的确定性 workspace/task mutation。

## 4. Runtime Design

### 4.1 Normal pre-task and standalone invocation

- recorder/checker 接受 stdin (`-`)，使 owner result 按 `record -> check -> invoke` 串联且不写 repo-relative文件。
- `stage0_owner_path`/`stage0_owner_result` 对 discovery 的 pre-task/standalone profile支持 stdin owner result；其它需要持久恢复的 profile仍遵循其 owner-private路径合同。
- public output先经 owner checker、projection 和 output schema验证；成功后 stdout只输出一个 typed exit DTO。
- 正常路径不创建 `.trellis/tasks/**`、`.trellis/workspace/**`、`.trellis/.runtime/**` 文件。

### 4.2 Active-task recovery checkpoint

- 复用 `ai_first_owner_checkpoint_path`，为 discovery、clarification 和本 task consumer inventory 列出的 owner 增加明确的 current-only artifact name/ownership。
- checkpoint只在 owner loop确实要暂停并由同一 owner后续恢复时创建；不能因为“可能有用”预写。
- checkpoint字段限制为恢复不可重新推导的最小 current semantic state与 task identity；live Git/GitHub/Trellis facts、扫描历史、文件 metadata、用户授权与 process metadata全部重读或不保存。
- wrapper成功消费后调用统一 retire helper；失败只在同一 owner可修复时保留。stale checkpoint被删除并从 live authority重新开始，不建立 supersession chain。

### 4.3 Terminal cleanup

- 将现有 `ai_first_retire_owner_checkpoints` 扩展为由明确 owner artifact inventory 驱动的 cleanup，保持 exact target与 regular-file安全检查。
- task terminal/publication/finalization路径在各自 typed exit成功后清理已消费的 owner input/result/checkpoint和空目录。
- verifier对当前 task key的 owner namespace做递归零残留断言；不删除其它 task或用户文件。

## 5. Contract and Schema Changes

- `guru-discover-change-context` 发布 current-only Interface 1.3 shape：移除 tracked `context_snapshot` private artifact、`task_local_reentry` profile和旧 schema/example/eval声明；如需要恢复 checkpoint，声明为 `ignored_runtime` 且只由同一 owner wrapper消费。
- `public-context-ready-output` 与 `guru-clarify-requirements:public-initial-change-request-input` 删除 locator字段并同步唯一 rename projection。
- Clarify、Change Request Review、Workspace 的 input/output schemas、examples、evals、interface projection 与 contract wording 删除 `context_locator` 和完整 snapshot dependency。
- runtime删除 context task artifact resolver、trackability检查、formal replacement、prior/superseded digest与archive reader的 current入口；保留 side-effect-free history preview算法和 semantic evidence校验能力。
- extension manifest、managed assets与ownership inventory删除退役的 context snapshot schema/example/path，并以 current source/installed closure证明无孤儿资产。

Breaking strategy：#178 明确要求 current contract收敛，因此不保留旧 alias/reader/migration。历史 archive仅作为历史文件存在，不参与 current package/runtime validation。

## 6. Markdown vs Deterministic Boundary

- Markdown Skill继续拥有 current-state review、history candidate选择、充分性、finding、semantic pass/block与 route intent。
- Python/shell仅负责：读取确定性 live facts、schema/projection验证、stdin/stdout transport、private checkpoint exact write/read/delete、manifest/overlay/install检查。
- 脚本不得从 snapshot内容推断 semantic conclusion，也不得生成预制 context summary 冒充 AI discovery。

## 7. Distribution and Upgrade/Update

- canonical修改顺序：durable specs -> canonical Skill/runtime/workflow/README -> preset/manifest/overlay -> dogfood/platform copies。
- 运行 `trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms` 同步；逐个检查 `.new`/`.bak`，不得静默覆盖用户修改。
- `check-dogfood-overlay-drift.sh`、source/installed package closure和ownership检查必须为零漂移。
- clean throwaway覆盖 fresh workflow/preset install、existing-project `--create-new` preview与切换、官方目标 Trellis版本 update/reapply、两轮 installed validation和最终零 sidecar。
- remote branch marketplace install只有在后续 push获得授权后才能执行；未执行时必须明确为 publication gate的外部证据缺口。

## 8. Failure and Recovery Matrix

| Failure | Required behavior |
| --- | --- |
| owner semantic gate blocked | 返回 `blocked`，不写正常-path checkpoint |
| base/live authority stale | 返回 mapped refresh/retry route；删除无效 current checkpoint并重读 live authority |
| projection/output schema invalid | fail closed；只保留同一 owner修复所需最小 checkpoint |
| wrapper成功 | 先验证 DTO，再删除 owner input/checkpoint/result/temporary projection |
| cleanup目标缺失 | 重复执行仍成功 |
| cleanup目标为 symlink/dir/越界 | fail closed，不删除 |
| task terminal | 精确 task-key owner namespace必须无 superseded文件或空目录 |

## 9. Risks and Rollback

- 风险：删除 locator后某个 consumer仍隐式读取 snapshot。缓解：用 repo-wide current-path扫描、source/installed contract tests与真实 wrapper集成测试证明零 reader。
- 风险：stdout transport破坏现有 wrapper调用。缓解：为 pre-task/standalone增加直接 wrapper测试，并保留其它 Skill的 current owner-result path行为。
- 风险：cleanup过宽。缓解：cleanup 目标严格限定为固定 `AI_FIRST_OWNER_ARTIFACTS`、resolved task key 与 regular-file exact paths，不做 glob 删除。
- 风险：installed副本漂移。缓解：只从 canonical同步并执行 dogfood/throwaway/update gates。
- 回滚：在未 commit前可回退本 task reviewed-content变更；不得通过恢复 tracked `context-discovery.json` 或旧 compatibility reader作为“临时回滚”。
