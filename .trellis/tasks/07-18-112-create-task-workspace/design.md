# #112 技术设计

## 1. 设计目标

本设计把 Intake 最后一跳建模为一个可重复进入的 semantic closed-loop Skill。Markdown
package 负责 target 展示、命名、assignee route、副作用确认、AI Gate 与 typed exit；
companion runtime 负责 canonical facts、freshness、精确 mutation、artifact 写入和结果校验。
Global workflow 只编排 stable id 与出口。

## 2. SSOT 与 owner

| 层 | SSOT | Owner | 禁止行为 |
| --- | --- | --- | --- |
| Global workflow | `trellis/workflows/guru-team/workflow.md` | Intake 顺序、mandatory invocation、typed-exit consumer | 复制 step-local 正文 |
| Canonical Skill | `trellis/skills/guru-team/packages/guru-create-task-workspace/` | entry、forward behavior、AI Gate、confirmation、re-entry、exit | 携带 active task 或本机 path |
| Upstream evidence | 五个 prerequisite Skill 的 checker-passed result | target/disposition/context/clarity/wording/readiness authority | 由 workspace Skill 重新选择 target |
| Plan recorder | `record-task-workspace-plan` | canonical plan、digest、confirmation facts | 判断 naming/scope/route |
| Exact executor | `create-task-workspace` | issue 或 workspace/task 精确副作用 | 生成产品语义、重复创建 issue |
| Result checker | `check-task-workspace-result` | live/result/artifact/boundary 客观校验 | 代替 AI pass |
| Task context | 四个 task-local tracked artifacts | portable Intake evidence | 保存绝对 path 或 runtime cache |
| Runtime mapping | `.trellis/.runtime/guru-team/**` | disposable local path mapping | 成为 portability 前置 |
| Preset installer | `trellis/presets/guru-team/` | managed-hash distribution、platform selection、provenance | 覆盖 unknown local edit |
| Dogfood copies | `.trellis/guru-team/skills/` 与 platform roots | runtime discovery | 反向成为 canonical source |

## 3. Canonical package

```text
trellis/skills/guru-team/packages/guru-create-task-workspace/
├── SKILL.md
├── interface.json
├── references/
│   └── contract.md
├── schemas/
│   ├── task-workspace-plan.schema.json
│   └── task-workspace-result.schema.json
├── examples/
│   ├── task-workspace-plan.json
│   └── task-workspace-result.json
├── scripts/
│   ├── record-task-workspace-plan.sh
│   ├── create-task-workspace.sh
│   └── check-task-workspace-result.sh
└── tests/
    └── test_contract.py
```

`SKILL.md` 只包含 trigger、contract locator、闭环顺序、runtime entry、typed exits 与
fail-closed 规则。`references/contract.md` 独占 step-local 正文。三个 package scripts 只经
`run-skill-command` 调用 installed companion runtime，不复制 Python 逻辑。

Schema ids 固定为：

- `guru-task-workspace-plan-1.0`
- `guru-task-workspace-result-1.0`

## 4. Interface 与 mode parity

`interface.json` 使用 schema 1.2、`state=active`、`judgment_mode=semantic`。Workflow 与
standalone 声明同一组 entry precondition ids：

- `runtime_dependency`
- `base_evidence`
- `context_evidence`
- `clarity_evidence`
- `wording_evidence`
- `readiness_evidence`
- `target_authority`
- `naming_and_assignee`
- `side_effect_authorization`
- `invocation_freshness`

Standalone 只改变 caller routing，不削弱任何 precondition。Runtime dependency 继续绑定
完整 Guru preset、extension manifest、dispatcher、installed inventory 与所选 discovery copy。

## 5. Semantic closed loop

### 5.1 Forward behavior

AI 按固定顺序执行：

1. 验证 package/runtime 与五个 prerequisite result。
2. 投影 checker-passed final target、target disposition、duplicate decisions、authority impact、
   close/ref/followup 与 current source facts。
3. 读取 base/worktree/config/live Git facts，但不执行副作用。
4. 生成 semantic branch/workspace/task names，并检查与 existing branch/worktree/task 的关系。
5. 按固定顺序解析 assignee；遇到多个候选或 unresolved actor 时只问一个 assignee 问题。
6. 展示 exact side-effect plan、artifact paths、runtime writes、executor command 与当前 invocation
   的停止条件。
7. 执行 AI Review Gate。
8. 取得当前 invocation 专用确认。
9. 调用 plan recorder、exact executor 与 result checker。
10. 返回一个 typed exit。

### 5.2 AI Review Gate

Gate 必须逐项审查：

- upstream target/disposition/authority 仍为当前 checker-passed bytes；
- 当前 Skill 没有重新选择 duplicate 或 closed-state disposition；
- naming 表达 issue number、semantic action 与 task-workspace object；
- assignee 来源符合固定顺序；
- issue mutation 与 workspace/task mutation 没有混入同一 draft invocation；
- exact plan 覆盖 repo、base、branch、worktree、task、artifacts、runtime 与 command；
- close/ref/followup 与 readiness scope conclusion 一致；
- task-local/runtime/no-developer/no-shared-write 边界完整；
- recovery route 不会覆盖 identity 冲突对象；
- 当前场景没有越过正常运行范围。

Recorder 只验证 Gate shape、reviewed digests 与 status，不产生上述判断。

### 5.3 两类 confirmation

Plan 使用两个互斥副作用域：

| Scope | 触发 | 本次合法结果 |
| --- | --- | --- |
| `github_issue_mutation` | final target 是 reviewed draft，source action 是创建 exact issue | 创建并校验 issue 后返回 `refresh_review` |
| `workspace_and_task_mutation` | final target 是 checker-passed open issue | 创建或复用 branch/worktree/task 后返回 `created` |

Draft invocation 的 workspace/task authorization 固定为 `not_in_current_invocation`。Issue 创建后
旧 confirmation 失效。完整 Intake 重跑后的 open-issue invocation 必须重新展示 workspace/task
plan 并取得新确认。Open-issue invocation 的 GitHub mutation 固定为 `not_in_current_invocation`。

用户改变 target/disposition 时不把该要求视为 plan 修改，而是返回 `refresh_review`。用户明确
取消时返回 `cancelled`。

## 6. Plan 与 result 数据合同

### 6.1 `guru-task-workspace-plan-1.0`

Plan 顶层结构固定包含：

| 字段 | 内容 |
| --- | --- |
| `schema_version` / `skill_id` / `mode` | public identity |
| `invocation` | caller、target kind、当前 action scope、resume identity |
| `prerequisites` | 五个 result 的 schema/exit/facts/content/linkage digests |
| `target` | final issue 或 reviewed draft authority、disposition digest、duplicate decision digest |
| `scope` | primary、close、related、followup projection 与 scope digest |
| `base` | selected base、remote、decision/local/remote HEAD 与 sync digest |
| `naming` | branch/workspace/task names、AI reason、existing-object disposition |
| `assignee` | login、source enum、candidate projection、AI resolution evidence |
| `side_effects` | exact issue/worktree/task/artifact/runtime operations 与 command argv |
| `confirmations` | 两类 scope 的 status、source、reviewed plan digest 与 evidence |
| `ai_review_gate` | reviewer、reviewed digest、summary、evidence、status |
| `freshness` | captured facts 与 plan digest |

Plan 只经 stdout 传递，不写 repo cache。Command argv 记录结构化参数，不记录 shell 字符串拼接。
临时 issue body 使用受控临时文件，result 与 task artifacts 只保存 digest。

### 6.2 `guru-task-workspace-result-1.0`

Result 绑定 exact plan digest，并按 variant 记录：

- `created_issue`：live `created_issue_binding`、executor facts、checker status、
  `typed_exit=refresh_review`。
- `created_workspace`：branch/worktree/task identity、四个 artifact path/digest/size/mode、runtime
  mapping projection、workspace boundary、trackability 与 `typed_exit=created`。
- `no_side_effect`：target-change/cancel/block reason、zero-write snapshot 与对应 typed exit。

Result 不作为 tracked repo artifact。`created_workspace` 的 durable evidence 已由四个 task-local
artifact 承接；重复保存 result 会制造第五个 Intake SSOT，因此禁止写入 task 目录。

## 7. Final target 与 created issue binding

### 7.1 Existing issue

Plan 必须绑定：repo、number、canonical URL、`state=open`、title/body digest、`updated_at`、
clarity target-disposition digest、readiness target/content/linkage digest。Executor mutation 前再次
执行 live reread；任一字段 drift 返回 `refresh_review`，不创建 workspace/task。

### 7.2 Reviewed draft

Plan 必须绑定 draft id、repo、source request digest、title/body digest、labels、clarity disposition、
wording facts、readiness linkage 与 GitHub mutation confirmation digest。Executor 只创建 exact
payload，随后立即读取 live issue并构造 `created_issue_binding`：

```text
repo + number + canonical_url + state=open + title_sha256 + body_sha256
+ updated_at + reviewed_draft_id + reviewed_draft_sha256
+ creation_confirmation_sha256 -> facts_sha256
```

Checker 只在 binding 与 live issue/current draft完全一致时返回 `refresh_review`。Executor 不接受
workspace/task action。重入时，当前 Intake evidence 必须指向新 issue；binding 存在时精确比对，
binding 因会话中断不可用时通过 live duplicate/current-state evidence 识别同一 issue，再由完整
Intake chain 建立新的 checker-passed authority。

## 8. Naming 与 object reuse

AI 生成 branch/workspace/task names；deterministic runtime 只检查格式、碰撞与 live object facts。
名称必须包含 issue number、semantic action 与 task-workspace object。Low-information、非 ASCII
slug、纯编号或仅通用 token 使 Gate blocked。

Object disposition 是 closed enum：

- `create_new`
- `reuse_exact`
- `conflict_blocked`

`reuse_exact` 必须证明 repo、base、branch、issue、task slug 与现有 artifact identity 全部一致。
只有路径存在不足以复用。任何 mismatch 禁止覆盖、删除、重命名或静默采用另一对象。

## 9. Assignee resolution

Runtime 先输出客观候选 facts，AI 决定是否需要向用户提问：

```text
explicit input
  -> one issue assignee
  -> zero issue assignees: current `gh api user` login
  -> multiple/unresolved: one user assignee question
```

Plan 的 `source` 只能是 `explicit_input`、`single_issue_assignee`、`current_github_login`、
`user_selected_from_candidates` 或 `user_supplied_after_unresolved`。Executor 只接受已解析的非空
login，并始终向 official `task.py create` 传 `--assignee`。它不读取 `.trellis/.developer`，也不
调用 `init_developer.py`。

## 10. Workspace/task transaction 与普通恢复

Workspace path 来自 config `workspace_mode`、`worktree_root` 与 AI-reviewed naming。Executor 顺序：

1. 重验 runtime、plan、base、target、confirmation 与 current Git facts。
2. 对 draft 只执行 issue transaction，完成后停止。
3. 对 open issue 创建或复用 exact branch/worktree。
4. 在 target worktree 再次重验 base/target/plan。
5. 运行 official `task.py create ... --assignee <login>`，随后设置 branch、base 与 scope。
6. 写入 `issue-scope-ledger.json` 与 `task-start-context.json`。
7. 以 checker-passed canonical bytes 写入 `context-discovery.json` 与 `issue-review.json`。
8. 写 source/target 两侧 ignored runtime mappings。
9. 校验 task status、schema、artifact bytes、Git trackability、ignored runtime 与 workspace boundary。
10. 输出 result。

普通中断恢复按每一步的 live facts判断 `create_new` 或 `reuse_exact`。本设计不引入事务日志、锁、
原子写协议或 repo-level recovery cache。Artifact 已存在但 bytes不同，或 task 状态/branch/base/issue
不一致时固定 `blocked`。

## 11. Task-local artifact 设计

### 11.1 `task-start-context.json`

保持 schema version `1.0` 以兼容既有 archived tasks，在 closed `intake_summary` 中增加两个
additive 字段；旧 task 不强制回填，新 executor 必须写入：

- `final_source_issue_binding`
- `prerequisite_evidence`

`final_source_issue_binding` 记录 live open issue identity、title/body digest、`updated_at`、target
disposition digest、created-draft binding digest。`prerequisite_evidence` 记录五个 Skill 的 schema/
exit/facts/linkage digest。顶层 portable path 与 forbidden-key gate 保持不变。

### 11.2 `issue-scope-ledger.json`

Ledger 从 readiness `scope_conclusion` 投影 primary/close/related/followup，保留每项 title、URL、
reason 与空 acceptance evidence。Workspace Skill 不新增或改选 scope。Task #112 的 fixture 必须
得到 close `[112,99,54]`、related `[98,53]`、followup `[132]`。

### 11.3 Canonical upstream artifacts

`context-discovery.json` 与 `issue-review.json` 使用 recorder/checker 已通过的 exact bytes。写前先
验证 expected snapshot/facts digest，写后重读 bytes、hash、size 和 Git trackability。目标已存在且
内容不同固定 `blocked`。

## 12. Legacy `prepare-task` 收敛

`guru-create-task-workspace` 成为唯一 mutation owner。现有 `prepare-task` 保留无副作用兼容查询，
但 `--create-issue-confirmed`、`--create-worktree` 与 `--create-task` 不再直接执行 mutation；调用者
必须进入新 Skill 并提供完整 prerequisite evidence。Runtime 内部可复用 base、naming、GitHub、
worktree、task 与 artifact helper，但只有 `create-task-workspace` command 能触发副作用。

该设计消除两条并行实现路径，并满足 standalone 不绕过 review。旧 mutation CLI 调用返回稳定
migration error 与 prerequisite Skill 列表，不写任何路径。

## 13. Thin workflow integration

`guru-review-change-request:ready` 的既有 consumer id 保持不变。新增一组 unfenced markers：

```markdown
<!-- guru-skill-invoke: {"skill":"guru-create-task-workspace","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-create-task-workspace","exit":"created","consumer":{"kind":"workflow","id":"guru-task-workspace-created"}} -->
<!-- guru-skill-exit: {"skill":"guru-create-task-workspace","exit":"refresh_review","consumer":{"kind":"skill","id":"guru-sync-base"}} -->
<!-- guru-skill-exit: {"skill":"guru-create-task-workspace","exit":"cancelled","consumer":{"kind":"stop","id":"task-workspace-cancelled"}} -->
<!-- guru-skill-exit: {"skill":"guru-create-task-workspace","exit":"blocked","consumer":{"kind":"stop","id":"task-workspace-blocked"}} -->
```

`guru-task-workspace-created` 唯一进入 Phase 1，并明确 task workspace confirmation 不是 planning
approval。原 0.5-0.8 inline `check-env`/`prepare-task`/handoff route 从 active workflow 移除；命令
资产只保留 compatibility/runtime 用途。#132 后续处理 upstream entry overlay 的物理移除。

## 14. Developer identity 与官方边界

Guru runtime 删除 `infer_assignee -> .developer` fallback、
`ensure_workspace_developer_identity()` 调用与对应 mutation tests。Official `.trellis/scripts/**`
保持不变。

Public install command 省略 `TRELLIS_USER` 与 `-u`。由于 official `trellis 0.6.5` clean init 会从
Git config 创建 identity/workspace，文档必须准确标注该行为属于 official Trellis，不是 Guru
preset 前置或产物。Clean Guru preset fixture 在 official init 后建立“identity/workspace 已缺失”
的输入快照，再执行 apply/update/reapply并证明 Guru 不重建它们。Existing repo 的 official
identity/workspace 保持原状；preset 不删除用户数据。

## 15. Combined A/B merge fixture

Fixture 使用真实临时 Git repo、同一 base commit、两个 branch/worktree 与 production runtime：

1. 为 A、B 构造独立 checker-passed Intake inputs 与 exact side-effect plan。
2. 通过 `create-task-workspace` 分别创建 task A、B。
3. 为每个 task 生成去身份化 `finish-summary.json`，调用 production task-local closeout helper 与
   official `task.py archive` 完成 active 到 archive。
4. 分别提交完整 branch diff，记录 HEAD、base..HEAD、changed paths 与 forbidden-path audit。
5. 从同一 base 创建 integration-ab，依次 merge A、B。
6. 从同一 base 创建 integration-ba，依次 merge B、A。
7. 对第二次 merge 的 exit、conflict files、最终 tree metadata paths 与 path-set intersection 作断言。

任务目录和 archive locator 都包含独立 task slug，finish summary 只读取 task-local evidence，runtime
保持 ignored，因此两个 tracked Guru metadata path set 的交集必须为空。Fixture 不创建远程 PR，
不运行并发进程。

## 16. Distribution 与 upgrade

Registry activation 后，preset installer自动分发全部 package files到 installed/shared/selected
platform roots。实现必须同步：

- `trellis/guru-team-extension.json`
- canonical 与 dogfood workflow
- canonical runtime 与 installed runtime
- source/installed registry/package inventory
- shared、Codex、Cursor、Claude discovery copies
- public README、workflow README、preset README 与 durable specs
- throwaway/update/reapply/managed-hash tests

本 task 不改 `trellis/presets/guru-team/overlays/**`。运行 preset apply 只同步 Guru-owned package、
runtime、manifest 和 canonical workflow 产生的 dogfood copies；ownership validator 必须证明 legacy
overlay baseline未变化。`.new/.bak` 出现时逐项处理，最终集合为空。

## 17. Docs SSOT Plan

- docs state：`stale_docs`。
- strategy：`ssot_first`。
- 原因：durable requirements、specs 与 README 仍把 `prepare-task` mutation、handoff review、
  developer identity 和 `trellis init -u` 写成 Guru active contract；若先写代码，会同时存在两套
  Intake owner。
- Durable requirements 权威文件：
  - `docs/requirements/README.md`
  - `docs/requirements/requirement-main.md`
  - `docs/requirements/guru-team-trellis-flow.md`
- Durable workflow/preset specs：
  - `.trellis/spec/workflow/index.md`
  - `.trellis/spec/workflow/workflow-contract.md`
  - `.trellis/spec/workflow/skill-package-contract.md`
  - `.trellis/spec/workflow/data-contracts.md`
  - `.trellis/spec/workflow/companion-scripts.md`
  - `.trellis/spec/workflow/quality-guidelines.md`
  - `.trellis/spec/preset/installer.md`
  - `.trellis/spec/preset/overlay-guidelines.md`
  - `.trellis/spec/preset/upstream-ownership.md`
  - `.trellis/spec/docs/public-docs.md`
- Public operator docs：
  - `README.md`
  - `trellis/workflows/guru-team/README.md`
  - `trellis/presets/guru-team/README.md`
- 必须合并的 task delta：active Skill contract、mode parity、target binding、两类 confirmation、
  assignee order、no-developer boundary、四个 artifacts、thin workflow、A/B merge fixture、
  distribution/update 与场景排除项。
- Merge checkpoint：实现代理在修改 package/runtime 前先完成上述 durable docs；Phase 2 checker
  按当前代码再复核一次并更新实现事实。Task planning只保留本次决策、追踪和验证证据。
- Task-history-only：fresh base SHA、本次 task/worktree path、旧 attempt 废弃说明、临时 CLI 实验
  路径、planning approval 与后续 check/review evidence。
- Follow-up limit：#132 独占 upstream entry overlay removal 与 #98/#53 closure；本 task 文档不得
  把该内容并入 current implementation。

## 18. Compatibility 与 rollback

- 既有 task-start-context schema id 保持 1.0；新增 nested fields 为 additive，新 executor 强制写入，
  old archived tasks继续被现有 closeout reader接受。
- Existing official developer identity/workspace保留；Guru preset不读、不删、不新建。
- Legacy `prepare-task` query mode保留；mutation mode fail closed并指向新 Skill。
- Extension patch version递增。旧安装缺 package/runtime/schema时 direct invocation在副作用前失败，
  提示重放完整 preset并处理 sidecar。
- Workflow 已激活但 package/source-installed validation未通过时，回滚 registry activation与 markers，
  禁止发布半安装状态。
- Durable docs与 runtime/schema不一致时返回 Docs SSOT checkpoint，不进入 Phase 2 pass。
- A/B 任一顺序出现 shared metadata conflict 时禁止关闭 #112/#99/#54，并回滚 shared tracked write。

## 19. 需求追踪

| PRD | 设计 | 实现计划 | 验收 |
| --- | --- | --- | --- |
| R1-R2 | 3、4 | 4 | AC1-AC2 |
| R3 | 5 | 5 | AC3、AC6 |
| R4 | 6、7 | 6 | AC4-AC6 |
| R5 | 9 | 7 | AC7-AC8 |
| R6 | 6、10、12 | 8 | AC2-AC6、AC9 |
| R7 | 11 | 8 | AC9-AC10 |
| R8 | 14 | 3、7、10 | AC8、AC13 |
| R9 | 13 | 4、9 | AC11 |
| R10 | 15 | 11 | AC12 |
| R11 | 16 | 3、4、9、10、12 | AC13-AC15 |
| R12 | 5、6、10、15、18 | 2、6、11、13 | AC17 |
