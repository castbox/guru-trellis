# #119 Finish-family combined integration 设计

## 1. 设计原则

1. Global workflow 只拥有跨 Skill 编排，三个 active Finish Skills 独占内部判断与状态。
2. Guru namespace 拥有新增平台入口；upstream namespace legacy overlay 在 #119 不改 bytes。
3. Combined integration 只连接 public Interface 1.3 DTO，不读取 owner-private evidence。
4. #105 engine 是既有 deterministic transaction owner，本 task 只做回归和入口整合。
5. AI-first：mapped exits 自动承接；只在 exact closeout side effects、new authority 或
   material scope 发生变化时停给用户。

## 2. 目标路由

```text
trellis-continue / frozen legacy compatibility progress
  -> current Branch Review Gate passed
  -> guru-review-task-publication
       ready -> stop at explicit Phase 3.7 finish-entry boundary
       return_to_task_work -> Phase 2 complete rerun
       blocked -> stop

guru-finish-work (canonical explicit entry)
  -> guru-review-task-publication when no current ready result exists
       ready -> guru-finalize-task
       return_to_task_work -> Phase 2 complete rerun
       blocked -> stop
  -> current guru-review-task-publication ready result when it exists
  -> guru-finalize-task
       verification_required -> guru-verify-extension-installation
       publication_review_stale -> guru-review-task-publication
       resume_finalization -> guru-finalize-task same-plan re-entry
       reprepare_required -> guru-finalize-task preview/review/confirmation
       published -> final response
       blocked -> stop
  -> guru-verify-extension-installation
       verified | not_required -> guru-finalize-task
       return_to_task_work -> Phase 2 complete rerun
       blocked -> stop
```

`verification_required`、stale、resume 和 reprepare 是 AI workflow 内部 transition，
不显示为用户选择。`guru-finalize-task` 第一次确认一个完整 closeout side-effect plan；同 plan
recovery 不重复确认，cross-month reprepare 只有 plan 改变后才重新确认。

在 #132 删除 frozen legacy compatibility overlay 之前，`trellis-continue` 与
`guru-finish-work` 共用同一 Phase 3.6 publication review owner；前者只能在
`guru-review-task-publication:ready` 停下，不能进入 Phase 3.7。Canonical
`guru-finish-work` 从 live state 进入 Phase 3.6 或消费当前 `ready` 结果后进入 Phase 3.7。
该兼容行为不形成第二条 publication route，也不复制 owner 内部步骤。

## 3. Workflow 薄化边界

### 3.1 保留

- Phase 3.5 -> 3.6 -> 3.7 全局顺序和 explicit finish-entry boundary；
- stable Skill id、mandatory invocation marker；
- 每个 external exit 的唯一 Skill/workflow/stop consumer marker；
- entry evidence 的一句摘要和 missing/stale/unmapped fail-closed；
- `workflow-state:completed` 的短 breadcrumb；
- task-local `pr-body.md` / `finish-summary-index.json` 由 workflow caller 在 publication
  owner 调用前创建这一必要 ownership 边界。

### 3.2 删除或下沉到已有 owner

- publication 十维审查、metadata revision、finding closure：
  `guru-review-task-publication` contract；
- extension applicability/capability/adequacy：
  `guru-verify-extension-installation` contract；
- closeout plan review、confirmation、transaction/recovery：
  `guru-finalize-task` contract；
- path/symlink/mode/blob/hook/children/PR identity/failure matrix 算法：
  durable specs、schema 和 #105 engine/tests；
- 平台 entry 中的重复 artifact、command flag、schema 字段教程。

Canonical `trellis/workflows/guru-team/workflow.md` 先改，随后通过 preset apply 同步
`.trellis/workflow.md` dogfood copy；两者必须一致。

## 4. 平台入口与兼容迁移

### 4.1 Canonical Guru entry

新增三个显式平台 adapter：

| 平台 | Canonical overlay | Dogfood copy | 作用 |
| --- | --- | --- | --- |
| Codex | `trellis/presets/guru-team/overlays/.codex/prompts/guru-finish-work.md` | `.codex/prompts/guru-finish-work.md` | 显式 prompt |
| Claude | `trellis/presets/guru-team/overlays/.claude/commands/guru/finish-work.md` | `.claude/commands/guru/finish-work.md` | `/guru:finish-work` command |
| Cursor | `trellis/presets/guru-team/overlays/.cursor/commands/guru-finish-work.md` | `.cursor/commands/guru-finish-work.md` | `/guru-finish-work` command |

每份 adapter 只包含：读取 live context/workflow、进入 Phase 3.6/3.7、mandatory load 三个
Skills、自动 route mapped exits、只返回 `published` 或具体 blocker。它们不是第四个
closed-loop Skill，不新增 package/interface/schema/artifact。

Shared 路径不新增 `.agents/skills/guru-finish-work` wrapper。Shared execution 的公开入口是
global workflow 对三个 active packages 的 mandatory invocation；这样避免违反“只做 route
的 wrapper Skill”禁令，也不制造 registry 外 `guru-*` Skill id。

### 4.2 Additive Guru ownership

Issue #128 validator 当前把 overlay root 限定为 43 条 frozen legacy paths。实现需要把
“legacy identity”与“additive Guru-owned entry”分开：

- `legacy_entries[]`、43-path digest、baseline payload digest 保持原值；
- ownership inventory 新增三个窄 Guru path rule/managed claim；
- extension manifest `public_api.managed_paths` 增加三个精确 entry claims；
- validator 继续对 frozen path 做 exact identity/hash；每个额外 overlay 必须恰好命中一个
  declared Guru rule 和 managed claim，且必须是 regular file；其它新增 path 仍 fail closed；
- dogfood/install manifest 记录新 entry bytes，preset selected-platform 逻辑继续决定安装。

这不是 #132 的 upstream overlay removal；scope 严格限定为 #119 需要的 additive Guru entries。

### 4.3 Legacy compatibility inventory

以下现有路径在 #119 **保留且 bytes 不变**，作为 bounded compatibility router；其物理
删除仍由 #132 执行：

- `.agents/skills/trellis-finish-work/SKILL.md`
- `.codex/prompts/trellis-finish-work.md`
- `.codex/skills/trellis-finish-work/SKILL.md`
- `.claude/commands/trellis/finish-work.md`
- `.cursor/commands/trellis-finish-work.md`
- 上述 canonical overlay counterparts。

兼容入口与 `guru-finish-work` 最终都读取同一 live workflow 并进入同一三个 owner；不
双写 artifact。Durable docs 和 direct helper blocker 将 `guru-finish-work` 作为 canonical
guidance，旧名称只出现在 compatibility/ownership inventory 中。

内部 `finish-work.sh`、`publish-pr.sh` blocker、`--from-trellis-finish-work` private marker
仍有生产 consumer，不属于 dead surface；本 task 不重命名该 internal API。

## 5. Cross-skill combined evidence

### 5.1 Evidence 模型

不新增长期 integration artifact。测试在临时目录生成 transcript，Phase 2/Branch Review
记录命令结果。Combined runner/test 的读取集合严格限定为：

- package `interface.json` 的 public contracts；
- per-exit public output schema/example；
- consumer input schema、projection、target-owned authoring example；
- real public `scripts/invoke.sh` wrapper 的 stdout DTO；
- global workflow markers 和 platform entry text。

禁止读取/导入 package private artifact、owner result body、closeout journal、
`guru_team_trellis.py` 或 adapter-private staging details作为路由依据。Package-local eval
eval 使用 checker-passed owner result 执行真实 wrapper；combined layer 不重做 semantic gate。

### 5.2 Transcript 场景

| 场景 | 路径 | 终点 |
| --- | --- | --- |
| normal non-extension | publication ready -> finalizer -> verifier not_required -> finalizer | published |
| extension | publication ready -> finalizer verification_required -> verifier verified -> finalizer | published |
| return-to-task-work | publication 或 verifier return_to_task_work | Phase 2 router |
| publication stale | finalizer publication_review_stale -> publication stale profile -> ready -> finalizer | published/next finalizer route |
| same-plan resume | finalizer resume_finalization -> same-plan target profile | published/next legal route |
| cross-month reprepare | finalizer reprepare_required -> reprepare preview target profile | reviewed new plan boundary |
| published recovery | archived recovery public wrapper | published |
| blocked | 三个 owners 的 blocked routes | unique stop |

Tests 同时断言 13 个 exits 恰好闭合、六条关键 Skill edges 存在、每个 field 有直接 consumer
use、private fields 不进入 DTO、`expected_exit` 不进入 native request。

## 6. #105 事务回归

不改 transaction state machine。以完整
`trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py` 为主证据，避免用少数
smoke 冒充 matrix；其 `CloseoutTransactionContractTest` 和 production finish tests 已覆盖
Issue #105 正文场景。Throwaway verifier继续两次运行 installed closeout：fresh install 后一次，
`trellis update` + workflow/preset reapply 后一次。

如 combined entry 需要修改 helper 的 canonical guidance，只更新错误文案/契约断言；不得
改变 prepare/push/verifier/draft/projection/archive/ready/recovery 语义。

## 7. 安装、upgrade/update 与 reapply

Throwaway 顺序保持官方扩展面：

1. 非交互 `trellis init` 安装 marketplace workflow；验证 `trellis/index.json` 和
   `guru-team` id/path/type。
2. preset apply 安装完整 `.trellis/guru-team/**`、三个 active Finish packages、三平台
   Guru entry 和 selected discovery copies。
3. 运行 source/installed contract validation、13-exit/combined tests、initial installed
   closeout。
4. `trellis workflow --create-new` preview，再强制 switch。
5. `trellis update --force`，记录 upstream file 保留/覆盖/sidecar 状态。
6. 重新选择 workflow、preset reapply；验证 managed inventory、`.new`/`.bak`、新入口 bytes/
   mode、legacy compatibility inventory、zero unresolved sidecars。
7. 再运行 installed contracts/combined tests/closeout。
8. 在 source repo 运行 overlay apply、dogfood drift、ownership validator。

## 8. Dead/duplicate inventory 判定

只有满足以下任一条件才删除：

- 同一 Finish route 正文在 workflow/entry/test 中重复，已有 active Skill/durable spec owner；
- test 只硬编码 legacy 主入口名称，没有兼容或 current route 价值；
- wrapper/helper 没有生产 caller，且 public wrapper/consumer contract 已完整替代；
- fixture 双写旧/新 artifact schema 或依赖 PR #160 task artifact。

保留项必须记录唯一 owner/consumer：#105 engine、finalizer private adapter、publish blocker、
frozen legacy compatibility entries 和 #132 ownership inventory 均不得误删。

## 9. Docs SSOT Plan

- **docs_state**: `stale_docs`
- **strategy**: `ssot_first`
- **原因**: 当前 durable docs 已覆盖 Finish Skills 和 transaction，但 canonical entry、
  compatibility ownership 与 #119 closure 仍是旧语义；这是长期 workflow/install contract。
- **durable paths**:
  - `.trellis/spec/workflow/workflow-contract.md`
  - `.trellis/spec/workflow/companion-scripts.md`
  - `.trellis/spec/preset/overlay-guidelines.md`
  - `docs/requirements/requirement-main.md`
  - `README.md`
  - `trellis/workflows/guru-team/README.md`
  - `trellis/presets/guru-team/README.md`
- **task delta 回写**: Guru entry、legacy retained/removal owner、thin routing、combined evidence、
  install/update/reapply/multi-platform acceptance 和 #119/#115 close scope。
- **merge checkpoint**: 实现每个 contract group 时先更新对应 durable doc，再改 workflow/
  installer/test；Phase 2 前完成全部回写并做 Docs SSOT reconciliation。
- **task-history-only**: 本次 acceptance audit、Phase 0 digests、规划 provenance、执行命令输出
  与 gate evidence；不复制到 durable docs。

## 10. 回滚策略

- 新 Guru entry 和 ownership claim 为 additive；若安装/平台发现失败，回滚该组文件和 claim，
  frozen legacy bytes 不受影响。
- Workflow thinning 若破坏 marker closure，回滚该 section 并从 durable contract 重新生成
  最小编排，不修改 Skill internals。
- Combined tests 只生成临时 transcript；失败不产生 repo/task runtime 状态。
- 不用 destructive Git 操作；实现阶段仅修改本 task 明确文件，commit/push 另行授权。

## 11. 中台知识门禁

不适用。本 task 修改 Trellis workflow/preset/平台入口与测试，不使用 Guru Team 业务中台
SDK/framework。
