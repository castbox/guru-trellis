# #130 设计：`guru-check-task` Phase 2 semantic closed loop

## 1. 设计目标

把 Phase 2 complete check 从 global workflow 展开步骤、official `trellis-check` worker 和 shared recorder/checker 的隐式组合迁移到一个 active Guru Skill package。迁移后：

- `guru-check-task` 独占 task-scope adequacy、scope qualification、severity、finding loop、Docs SSOT verification、pass/fail和route intent；
- global workflow只保存mandatory invocation、四出口唯一consumer和global phase transition；
- official未修改的`trellis-check` worker只产出review evidence；
- shared runtime只执行命令、采集事实、记录AI结论和验证freshness；
- `phase2-check.json`保持唯一Phase 2 artifact；
- preset只additive分发Guru namespace package，不触碰upstream-owned overlay。

## 2. 所有权模型

| 层 | 唯一职责 | 明确不拥有 |
| --- | --- | --- |
| Global workflow | Phase 2顺序、mandatory invocation、typed-exit consumers、implementation/commit targets、fail-closed stop | check dimensions、scope qualification、severity、finding loop、recorder参数 |
| `guru-check-task` package | entry contract、repository check选择、adequacy、scope classification、severity、Docs SSOT review、AI Gate、re-entry、artifact schema、typed exits | implementation修复、planning authority mutation、post-commit Branch Review |
| Official `trellis-check` worker | 按unchanged upstream entry执行AI review并产出raw report/handoff | Guru pass、artifact owner、final scope/severity/route |
| `guru-approve-task-plan` | approved planning/provenance/Docs SSOT Plan authority | Phase 2 implementation adequacy、finding severity |
| `guru-clarify-requirements` | requirement/scope authority mutation和active-task route | current-scope finding修复、Phase 2 pass |
| Shared runtime | command execution、path/hash/size/exit code、schema、HEAD/diff/dirty、planning/agent linkage、artifact write/check | sufficiency、scope、severity、Docs consistency、semantic pass |
| `guru-create-task-commit` | fresh passed artifact后的candidate/stage/commit closed loop | Phase 2 semantic review |
| Preset installer | registry/package/platform discovery copy、manifest、mode/hash和upgrade/reapply | upstream check patch、AI route judgment |

## 3. Entry 与 Mode Parity

`interface.json` 的 workflow/standalone `entry_precondition_ids` 使用同一有序集合：

1. `runtime_dependency`
2. `task_workspace`
3. `approved_planning`
4. `requirement_provenance`
5. `implementation_handoff`
6. `repository_check_inputs`
7. `docs_ssot_plan`
8. `issue_scope_ledger`
9. `agent_assignment_recovery`
10. `repository_snapshot`
11. `invocation_freshness`

Workflow mode从task progression获得direct active task locator。Standalone mode从current checkout和ignored runtime mapping发现同一task，再执行完全相同的boundary、planning、authority、agent和repository checks。

Entry validator复用现有workspace boundary、`validate_planning_approval`、task context、issue ledger、agent assignment recovery、Git status/diff/path digest helper。Planning activation后的正常HEAD/dirty变化不得单独使planning evidence stale；planning文档、Docs SSOT locator、authority、ledger分类、task/branch/base identity变化强制完整re-entry。

## 4. Canonical Package

新增：

```text
trellis/skills/guru-team/packages/guru-check-task/
├── SKILL.md
├── interface.json
├── references/contract.md
├── schemas/phase2-check.schema.json
├── examples/phase2-check.json
├── scripts/record-phase2-check.sh
├── scripts/check-phase2-check.sh
└── tests/test_contract.py
```

`SKILL.md`只保留trigger、routing、entry、fail-closed摘要；完整step-local行为位于`references/contract.md`。Wrappers必须只经`run-skill-command` dispatch manifest中声明的runtime commands。

Registry新增active entry：

```json
{
  "id": "guru-check-task",
  "state": "active",
  "package": "packages/guru-check-task",
  "workflow_route_id": "phase-2-task-check"
}
```

## 5. Closed Loop

### 5.1 Forward Behavior

1. 验证完整preset runtime、direct task workspace和current approved planning evidence。
2. 读取`prd.md`、`design.md`、`implement.md`、Docs SSOT Plan、issue ledger、requirement provenance、implementation handoff、agent assignment、code/tests/docs/spec和完整dirty diff。
3. 根据repository-defined commands形成validation plan，执行每条命令并采集argv、exit code、stdout/stderr digest、size和结果摘要。
4. 读取official unchanged `trellis-check` worker report；worker缺失时只能记录当前平台合同明文声明的替代evidence，不能伪造worker结果。
5. 为每个candidate issue先执行scope qualification。
6. 只为`current_scope`candidate分配P0/P1/P2/P3并生成current finding。
7. 审查requirements -> design -> implementation -> tests -> Docs SSOT完整承接、cross-layer和deploy/config/schema/CI/CD/container/K8s/DB/Makefile影响。
8. 形成unverified items、findings、route和AI Review Gate。
9. Recorder写入唯一`phase2-check.json`，checker重建objective facts。
10. 返回exactly one typed exit。

### 5.2 Scope Qualification Model

每个candidate使用closed disposition：

- `current_scope`
- `scope_change_required`
- `followup_proposal`
- `out_of_scope`

每条记录必须包含：

- stable candidate id；
- summary；
- requirement/planning trigger refs；
- supported normal-path reproduction evidence；
- disposition；
- route basis；
- severity，只有`current_scope`为P0/P1/P2/P3，其余必须为null；
- finding id，只有进入current finding时非null。

Runtime只验证field shape、references、digest和“非current_scope severity必须为null”的invariant。AI负责判断trigger是否充分、路径是否属于正常支持范围和disposition语义。

### 5.3 Adequacy Review

固定dimensions：

1. `requirements`
2. `design`
3. `implementation`
4. `tests`
5. `docs_ssot`
6. `cross_layer`
7. `compatibility`
8. `deployment_and_operations`
9. `agent_recovery`
10. `verification_completeness`

每个dimension记录status、summary、evidence refs、affected hashes、finding ids和unverified ids。Structural complete不代表semantic pass。

## 6. Typed Exits 与唯一 Consumers

| Exit | Gate条件 | Consumer |
| --- | --- | --- |
| `passed` | 所有dimensions通过；零blocking current finding；零blocking unverified item；current planning/agent/repository evidence；full rerun identity成立 | Skill `guru-create-task-commit` |
| `implementation_required` | current approved scope存在blocking finding；无需改变requirement/scope | workflow target `guru-resume-implementation` |
| `planning_stale` | candidate需要scope/authority/planning变化，或planning evidence失效 | 由result中的closed route discriminator选择Skill `guru-approve-task-plan`或`guru-clarify-requirements`，其余组合拒绝 |
| `blocked` | 外部依赖缺失、无法形成可靠check或无法安全re-enter | stop `task-check-blocked` |

`planning_stale`的route discriminator使用`reapprove_plan`或`clarify_requirements`。Schema和checker必须要求discriminator与consumer一一对应，禁止同时声明两个consumer。

## 7. `phase2-check.json` 演进

Artifact basename保持不变，schema升级为closed `guru-phase2-check-2.0`。Top-level结构：

```text
schema_version / skill_id / generated_at / mode
task / planning / requirement_provenance / docs_ssot_plan
implementation_handoff / agent_assignment
repository_snapshot / check_execution
scope_qualification / semantic_review
human_confirmation / typed_exit / route / reason / consumer
facts_sha256
```

关键合同：

- `repository_snapshot`绑定base、HEAD、`origin/<base>...HEAD`、完整dirty paths和reviewed path digests。
- `check_execution.commands[]`记录实际命令及结果事实；`worker_evidence[]`记录official unchanged worker或明确替代来源。
- `scope_qualification`先于`semantic_review.findings`，finding必须反向引用一个`current_scope`candidate。
- `unverified_items[]`区分blocking/non-blocking并记录具体reason/impact。
- AI Gate绑定planning digest、snapshot digest、scope qualification digest、adequacy digest和findings count。
- `passed`必须绑定本轮full-scope identity；finding fix后旧round不能升级为pass。
- Legacy active schema 1.0不能由新package直接消费为pass，必须完整re-entry；archive保持历史字节。
- Post-commit audit接受recorded HEAD为当前HEAD祖先的唯一条件是：后续committed non-metadata paths全部被recorded dirty paths覆盖，且current worktree不存在unreviewed non-metadata dirty path。

## 8. Runtime Boundary

Shared runtime保留`record-phase2-check`与`check-phase2-check`command id，内部升级为新package的recorder/checker。Compatibility wrapper继续存在，但必须要求AI-authored closed input；旧`--pass --coverage`调用不得继续生成新schema semantic pass。

新增或重构的deterministic helpers：

- current task/workspace/planning/ledger/agent projections；
- repository snapshot和reviewed path digest；
- command result facts；
- scope/adequacy/finding引用检查；
- exit/gate/consumer closed union；
- legacy migration error；
- post-commit coverage reuse。

禁止实现：

- 由coverage flags自动判定adequacy；
- 由命令exit 0自动判定pass；
- 由路径或关键词推断scope disposition/severity；
- 由script判定Docs SSOT一致；
- 由worker报告直接生成final route。

## 9. Workflow Thin Route

Canonical workflow Phase 2.2替换为：

```markdown
<!-- guru-skill-invoke: {"skill":"guru-check-task","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-check-task","exit":"passed","consumer":{"kind":"skill","id":"guru-create-task-commit"}} -->
<!-- guru-skill-exit: {"skill":"guru-check-task","exit":"implementation_required","consumer":{"kind":"workflow","id":"guru-resume-implementation"}} -->
<!-- guru-skill-exit: {"skill":"guru-check-task","exit":"planning_stale","consumer":{"kind":"workflow","id":"guru-task-check-planning-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-check-task","exit":"blocked","consumer":{"kind":"stop","id":"task-check-blocked"}} -->
```

`guru-task-check-planning-router`只消费checker-validated discriminator并路由到`guru-approve-task-plan`或`guru-clarify-requirements`，不得重新判断scope。Workflow删除旧coverage checklist、recorder command、finding算法和recovery正文；implementation/check agent dispatch的global orchestration保留，但final semantic owner明确为package。

## 10. Docs SSOT Plan

- Docs state：`complete_docs`
- Strategy：`ssot_first`
- Strategy reason：本任务改变长期Phase 2 public workflow、artifact schema、Skill package、runtime boundary和distribution；durable contracts必须先表达最终语义，再驱动实现。
- Durable requirement docs：
  - `docs/requirements/requirement-main.md`
  - `docs/requirements/guru-team-trellis-flow.md`
  - `docs/requirements/README.md`
- Durable specs：
  - `.trellis/spec/workflow/skill-package-contract.md`
  - `.trellis/spec/workflow/workflow-contract.md`
  - `.trellis/spec/workflow/data-contracts.md`
  - `.trellis/spec/workflow/companion-scripts.md`
  - `.trellis/spec/workflow/quality-guidelines.md`
  - `.trellis/spec/workflow/index.md`
  - `.trellis/spec/docs/public-docs.md`
  - `.trellis/spec/preset/overlay-guidelines.md`
  - `.trellis/spec/preset/upstream-ownership.md`
- Public docs：
  - `README.md`
  - `trellis/workflows/guru-team/README.md`
  - `trellis/presets/guru-team/README.md`
- Task delta merge checkpoint：canonical package/runtime实现前，durable requirement/spec先更新；最终Phase 2前再次对照实现收敛。
- Task history only：intake evidence、research note、implementation/check handoff、agent liveness、bootstrap和review round。
- No-update exception：不存在。上述durable paths必须由实现diff或明确的逐路径复核结论覆盖。

## 11. Requirement Provenance Matrix

| ID | Load-bearing statement | Planning locator | Classification | Authority / reason |
| --- | --- | --- | --- | --- |
| P1 | `guru-check-task`是Phase 2和`phase2-check.json`唯一semantic owner | PRD R1、R8；本设计1/7 | `explicit_requirement` | Issue #130定位、artifact acceptance |
| P2 | Workflow/standalone entry parity与semantic五阶段 | PRD R1、R2；本设计3/4 | `explicit_requirement` | Issue #130 closed loop与AGENTS Skill-first合同 |
| P3 | Official unchanged worker只产出evidence | PRD R3；本设计2/5 | `explicit_requirement` | Issue #130 upstream boundary |
| P4 | Scope qualification先于severity | PRD R4；本设计5.2 | `explicit_requirement` | Issue #130 closed loop与acceptance |
| P5 | 未触发的非常规场景不成为P0-P3 | PRD R4；本设计5.2 | `explicit_requirement` | Issue #130 normal-operation boundary |
| P6 | Requirements到Docs SSOT的complete adequacy review | PRD R5；本设计5.3 | `explicit_requirement` | Issue #130 closed loop |
| P7 | Finding fix后full-scope rerun与agent recovery闭环 | PRD R6；本设计5/7 | `explicit_requirement` | Issue #130 acceptance |
| P8 | 四出口和唯一consumer | PRD R7；本设计6 | `explicit_requirement` | Issue #130 External Exits |
| P9 | 复用唯一artifact并保持post-commit freshness | PRD R8；本设计7 | `explicit_requirement` | Issue #130 Artifact；archived Phase 2 evidence |
| P10 | Script不决定semantic judgment | PRD R9；本设计8 | `explicit_requirement` | Issue #130 Script边界与根AGENTS.md |
| P11 | No upstream-owned overlay mutation | PRD R10；本设计9/12 | `explicit_requirement` | Issue #130、#128和upstream ownership spec |
| P12 | Docs使用`ssot_first` | PRD 6；本设计10 | `necessary_implementation_choice` | alternatives=`ssot_first`,`delta_first`；public contract跨层变更要求durable SSOT先行，产品/风险scope均不扩张 |
| P13 | Artifact升级为closed v2而非在schema 1.0上追加松散字段 | PRD R8；本设计7 | `necessary_implementation_choice` | alternatives=`extend-v1`,`closed-v2`,`parallel-artifact`；closed-v2满足四出口和single artifact，拒绝parallel artifact，产品/风险scope均不扩张 |
| P14 | `planning_stale`使用closed discriminator路由 | PRD R7；本设计6 | `necessary_implementation_choice` | alternatives=`two exits`,`ambiguous multi-consumer`,`closed discriminator`；保持issue定义四出口并实现唯一consumer，产品/风险scope均不扩张 |
| P15 | 保留runtime command ids并使legacy CLI fail closed | PRD R8/R9；本设计8 | `necessary_implementation_choice` | alternatives=`new command ids`,`retain ids with new input`,`silent compatibility`；保留public id并拒绝semantic降级，产品/风险scope均不扩张 |
| P16 | #81/#108/#131/#132不进入当前实现 | PRD 4.2 | `explicit_requirement` | Issue #130 Scope与issue ledger |

当前matrix无`approved_scope_expansion`或`out_of_scope_proposal` load-bearing entry。

## 12. Compatibility、Rollback 与风险

- Extension public API变化：新增active Skill id和artifact schema id，extension version递增。
- Legacy active artifact：稳定migration error，完整re-entry；archive不改写。
- Legacy recorder CLI：不得静默产生新pass；tests固定拒绝或明确compatibility projection。
- Rollback：package/runtime/workflow/schema任一层无法保持single owner时停止activation，回到本规划修订；不得新增第二artifact。
- Overlay风险：任何implementation需要改upstream-owned path时立即阻塞并返回Phase 1。
- Deployment影响：无应用runtime、DB migration、container、K8s和production config变更；preset安装/升级行为属于必须验证的distribution影响。
