# #119 技术设计：Finish family combined integration

## 1. 设计结论

实现采用 current-main-first 的窄集成：保留 PR #165 的三个 Skill packages、public I/O、
semantic gates 与 mapped-exit graph，只补平台启动面、两个 terminal eval、checked #117
evidence 到 legacy transaction validator 的 private projection bridge、#105 regressions 与
安装/ownership 收敛。

不创建第四个 Finish Skill，不创建 route handoff artifact，不把 private evidence 投射到
public DTO，不修改五个 legacy `trellis-finish-work` payload。Guru entry 是新的日常入口；
legacy entry 在 #132 前保留 compatibility status。

## 2. Current main delta

| Area | Current main | #119 delta |
| --- | --- | --- |
| Skill packages | 三个 owners active，13 exits 与六组 routes 已闭合 | 不改内部 semantic contracts |
| Workflow | AI-first mapped routing 已 active | 日常入口名迁移到 `guru-finish-work`，保留 legacy note |
| Platform | 五个 `trellis-finish-work` thin overlays | 新增 Codex/Claude/Cursor Guru entries |
| Eval | Finalizer corpus 有八个 cases | 新增两个 terminal `published` cases 与 staging recipes |
| Runtime | 已生成 #117 compatibility projection | 将 checked projection 贯通 archive validators 与 recovery |
| Install | 已有 clean/update/reapply verifier | 加入 Guru entry 与 ownership assertions |
| Ownership | 五个 legacy entries 仍被 #119 阻塞 | 清空其 #119 blocker，保留 #132 removal owner |

## 3. Workflow 与入口设计

### 3.1 Canonical route

```text
guru-finish-work
  -> guru-review-task-publication
       ready -> guru-finalize-task
       return_to_task_work -> complete Phase 2 route
       blocked -> stop
  -> guru-finalize-task
       verification_required -> guru-verify-extension-installation
       publication_review_stale -> guru-review-task-publication
       resume_finalization -> guru-finalize-task
       reprepare_required -> guru-finalize-task preview
       published -> terminal response
       blocked -> stop
  -> guru-verify-extension-installation
       verified -> guru-finalize-task
       return_to_task_work -> complete Phase 2 route
       blocked -> stop
```

Standalone `not_required` 仍只经过 finalizer 的
`standalone_verification_not_required` profile。Workflow 不把它当作
`verification_required` 的替代 exit。

### 3.2 Platform adapters

Canonical ownership位于 `trellis/presets/guru-team/overlays/` 下三个 Guru entry files。
`apply.sh --repo . --all-platforms` 生成 dogfood copies。三个文件采用一份薄路由语义，平台
目录与触发格式各自独立；文件不承载 schema 字段教程、recorder/checker steps 或 transaction
flags。

五个 legacy overlay bytes 不变。Ownership inventory 只更新 `blocking_issues`，并在
durable docs 中把它们标成 compatibility-only；这一步不把 #132 的 physical cleanup 移入 #119。

## 4. Private evidence bridge

### 4.1 输入与投射

唯一输入是 current `guru-verify-extension-installation` checker-passed owner result 与 current
closeout plan。`finalization_marketplace_verification_compatibility_projection()` 继续负责把 owner
execution facts 投射成 legacy transaction validator 需要的 private object。

Projection 只存在于进程内。#117 artifact 仍由 #117 owner 独占；legacy
`marketplace-verification.json` parser 不获准解释新 owner schema；public output 不新增字段。

### 4.2 调用链

Projection 由 finalizer preview 或 transition entry 构建后，按同一 object reference 贯通：

```text
finalization preview / execute transition
  -> resolve_closeout_pre_draft_state
  -> cmd_finish_work
       -> build_final_archive_projection
       -> execute_archive_metadata_transaction
            -> validate_closeout_active_projection
                 -> validate_closeout_marketplace_artifact
  -> resume_active_archive_move
       -> validate_closeout_active_projection
       -> execute_archive_metadata_transaction
```

Plan 不要求 marketplace verification 时，参数值为 `None`，现有 non-extension path 不变。
Plan 要求 verification 而 projection 缺失或 contract invalid 时，validator 在 archive move 前
失败。Formal path 在没有外部 checked owner result的 legacy executor profile中仍走现有
deterministic verifier；finalizer profile只消费 checked owner projection。

### 4.3 Recovery invariants

- Retry 读取同一 plan 与 checked owner result，`resolve_closeout_pre_draft_state` 得出唯一
  `evidence_ready` state。
- Active task 已完成但尚未 move 时，recovery 先验证 projection、evidence commit 与 draft PR，
  再执行 archive transaction。
- Archived exact-commit recovery 继续只消费 immutable commit/plan/PR facts，不重新打开 #117
  private artifact。
- Projection 不写 task artifact，不改变 archive move set，不制造 metadata commit。

### 4.4 Publication freshness compatibility

`execute_closeout_content_push()` 保持 #105 事务顺序：先固定 plan/readiness，再写
pending remote-verification machine evidence。Finalizer 不重写 publication semantic gate，而是
执行一个精确 deterministic augmentation：

- current ledger 去掉所有 `remote_marketplace_verification` 后的 canonical digest 必须
  与 immutable plan 的 `inputs.issue_scope_ledger` 一致；
- primary issue 与所有 close issues 必须持有同一个 plan-owned pending evidence，或由
  current checked #117 owner projection 精确派生的 passed evidence；
- stored publication artifact/entry bindings 必须唯一匹配无 evidence、legacy pending、
  current plan pending 或 current checked passed 中的一个 reviewed preimage；
- 只替换 `issue-scope-ledger.json` artifact binding、`issue_scope_ledger` entry binding
  和派生 `review_range_and_working_tree` binding，其余 artifacts、entries、repository facts、
  semantic findings/conclusions 与 `publication_ref` 保持字节级一致。

这一规则只处理诚实正常流程中的 finalizer-owned machine update，不扩展为通用 stale
放宽、hostile-input 防御或额外 transaction protocol。

## 5. Eval 与 combined test 设计

### 5.1 Finalizer terminal cases

Canonical `guru-finalize-task/evals/evals.json` 新增：

- `publication-ready-published`：`publication_ready` input 处于 non-extension terminal ready state；
- `same-plan-published`：`same_plan_resume` input 处于 unchanged-plan terminal ready state。

每个 case 使用一个最小 facts fixture 与现有 public invocation。Native staging adapter 只新增
两个 recipe 到 current PR #165 state table，不改 request protocol、trace schema、public wrapper
或 grader顺序。Canonical 变更经 preset 同步到 shared/Codex/Claude/Cursor discovery copies。

### 5.2 Dedicated integration suite

新增 `trellis/skills/guru-team/tests/test_finish_family_integration.py`，从 current package interfaces
与 workflow markers 构建 graph assertions，覆盖：

- 13 exits、六组 cross-skill routes 与唯一 consumers；
- private artifact fields 未进入 public DTO；
- Guru entries 的 mandatory owners、automatic mapped routes 与无 generic continuation prompt；
- canonical/installed/platform corpus equality 与两个 terminal cases；
- legacy entries 只承担 bounded compatibility，ownership 不再被 #119 阻塞。

该 suite 不复制三个 package-local behavior tests，也不重新判定 #116/#117/#118 semantic pass。

## 6. Installer、update 与抗漂移设计

`verify-throwaway-install.sh` 沿用 current official workflow install、preset apply、
`trellis update`、workflow reselect、preset reapply 与 closeout transaction fixture。新增 assertions
固定三个 Guru entries 的存在、canonical bytes、managed inventory 与 executable inputs；五个
legacy entries仍按 recognized compatibility asset 处理。

Ownership inventory 的 `target_trellis_cli` 驱动
`trellis upgrade --dry-run --tag <version>`，验证 global upgrade command 具有显式版本绑定且
host installation 零变更。现有 pre-current-preset upgrade fixture 继续验证 backup/replacement
与 `.new` conflict semantics；throwaway 中的 `trellis update` 执行真实 project-file refresh。

Preset unit tests验证 all-platforms、单平台选择、recognized generated file replacement、unknown
local edit sidecar 与 no-sidecar happy path。Dogfood 只由 canonical apply生成，drift checker 验证
零差异。

## 7. Ownership 与重复 SSOT 处理

- Canonical workflow 拥有 global order、mandatory invocation 与 typed exit consumer mapping。
- 三个 Skill packages 各自拥有 step-local loop、public contracts、private artifact 与 exits。
- Guru platform files只负责启动与路由。
- Legacy `trellis-finish-work` files 保持 frozen compatibility payload；ownership inventory 不再把
  #119 写成 blocker，#132 继续拥有删除动作。
- Runtime helper 只传递 private projection；它不判断 applicability、adequacy、finding 或 route。
- Integration test只验证 graph 与 distribution，不复制 package-local test matrix。

## 8. Compatibility、rollout 与回滚

### 8.1 Rollout

1. Canonical source 与 durable docs先修改。
2. Runtime bridge 与 focused regressions 完成。
3. Eval corpus、adapter recipes 与 integration suite完成。
4. Preset apply 生成 dogfood copies并更新 managed hashes。
5. Full deterministic suite、CLI upgrade dry-run、throwaway install/update/reapply 与 drift gates通过。

### 8.2 Compatibility

- Public schema ids、Skill ids、external exit ids、script command ids 与 DTO fields不变。
- Legacy entry paths不删除、不改 payload、不改变 upstream producer classification。
- New Guru entry paths是 additive Guru-owned platform API。
- #132 后续负责 legacy overlay physical cleanup；本 task不声明该 cleanup 已完成。

### 8.3 Failure handling

任一 schema、projection、test、installer、sidecar 或 drift gate失败时，停止在当前 worktree，
保留 diff 与失败证据供审查，不执行 commit、push、PR、Issue mutation 或资源清理。若实现路线
需要改变 public contract 或扩大 scope，回到 `guru-clarify-requirements`。

## 9. Unusual scenario review

本设计没有 scope expansion candidate。Malicious actor、forgery、并发竞态、TOCTOU、锁、
新 fault injection、偶发 crash consistency 与跨 OS atomicity 全部排除。#105 正文明列的
deterministic failure/recovery matrix 保持 current owner 与 current边界。

## 10. Docs SSOT Plan

### 10.1 Docs state

`stale_docs`。Current docs仍把 `trellis-finish-work` 写为日常入口，ownership inventory仍把
#119 写为五个 legacy finish entries 的 blocker，preset 文档未列三个 Guru entries。

### 10.2 Strategy

采用 `ssot_first`。先更新 durable workflow/spec/README 与 canonical overlay，再通过 preset
apply生成 dogfood copies。Task docs只保存本次 provenance、设计选择、执行次序与验证记录。

### 10.3 Durable update paths

- `trellis/workflows/guru-team/workflow.md`
- `.trellis/workflow.md`
- `README.md`
- `trellis/workflows/guru-team/README.md`
- `trellis/presets/guru-team/README.md`
- `.trellis/spec/workflow/workflow-contract.md`
- `.trellis/spec/workflow/companion-scripts.md`
- `.trellis/spec/workflow/data-contracts.md`
- `.trellis/spec/workflow/skill-package-contract.md`
- `.trellis/spec/workflow/quality-guidelines.md`
- `.trellis/spec/workflow/index.md`
- `.trellis/spec/preset/installer.md`
- `.trellis/spec/preset/overlay-guidelines.md`
- `.trellis/spec/preset/upstream-ownership.md`
- `.trellis/spec/docs/public-docs.md`

### 10.4 Audited no-update owners

- `docs/requirements/`：current files不含 legacy finish entry 文案，实施后复核零 stale hit。

### 10.5 Task delta merge

Entry name、compatibility status、installer行为与 private bridge职责合并到上述 durable owners。
Planning provenance、命令日志、审查过程与 branch-specific验证结论只保留在 task history。
#132 limitation 写入最终 Docs SSOT 与 PR body。

## 11. Provenance Matrix

| ID | Planning locator | Class | Authority | Coverage |
| --- | --- | --- | --- | --- |
| R1 | `prd.md` §1 | explicit_requirement | Issue #119, user boundary | bounded combined goal与 close scope |
| R2 | `prd.md` §2 | explicit_requirement | PR #162, PR #165, live main | completed baseline不重做 |
| R3 | `prd.md` §3.1 | explicit_requirement | Issue #119 comment, workflow contract | thin order与 typed consumers |
| R4 | `prd.md` §3.2 | explicit_requirement | Issue #119 revision, preset specs | Guru entry与 legacy boundary |
| R5 | `prd.md` §3.3 | explicit_requirement | Issue #119, #117/#118 current contracts | checked evidence bridge |
| R6 | `prd.md` §3.4 | explicit_requirement | Issue #119 comment | two terminal eval cases |
| R7 | `prd.md` §3.5 | explicit_requirement | Issue #105, Issue #119 | transaction/recovery regressions |
| R8 | `prd.md` §3.6 | explicit_requirement | Issue #119, AGENTS.md | install/update/reapply gates |
| R9 | `prd.md` §3.7 | explicit_requirement | Issue #119 revision, Issue #132 | ownership减法与 follow-up boundary |
| R10 | `prd.md` §4 | explicit_requirement | PR #165, skill-package contract | AI-first与 minimal DTO |
| R11 | `prd.md` §5 | explicit_requirement | user boundary, AGENTS.md | exclusions |
| R12 | `prd.md` §6 | explicit_requirement | Issue #119, Issue #105 | deterministic acceptance |
| C1 | `design.md` §4.2 | necessary_implementation_choice | runtime private-state contract | in-memory projection threading |
| C2 | `design.md` §5.2 | necessary_implementation_choice | Issue #119 combined review | dedicated graph/distribution suite |
| R13 | `design.md` §10 | explicit_requirement | AGENTS.md, docs specs | Docs SSOT Plan |
| R14 | `implement.md` §2 | explicit_requirement | workflow contract | ordered execution |
| R15 | `implement.md` §3 | explicit_requirement | Issue #105, Issue #119 | command/test matrix |
| R16 | `implement.md` §4 | explicit_requirement | AGENTS.md, workflow gates | objective review gates |
| R17 | `implement.md` §5 | explicit_requirement | user side-effect boundary | authorization stops |

### 11.1 Implementation choice C1

选项 `private-in-memory-projection` 被选中：复用 current checked owner projection，并沿 private
call chain显式传参。选项 `rewrite-owner-artifact` 会破坏 #117 private ownership；选项
`expand-public-dto` 会增加无 direct consumer use 的字段。选中项不扩大 product scope 或 risk
scope。

### 11.2 Implementation choice C2

选项 `dedicated-integration-suite` 被选中：单独验证 graph、entry、distribution 与 ownership。
选项 `append-monolithic-package-tests` 会把 combined assertions继续堆入 package-local suite，
弱化 test ownership。选中项不扩大 product scope 或 risk scope。
