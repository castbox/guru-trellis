# D1：公开执行合同与真实入口闭合实施与验证计划

## 1. 输入与引用

本批是首次、全量 D1，覆盖公共scope_ref选中的 S1–S5、AC1–AC4、缩减后的 AC6–AC8 与 AC9；AC5 取消，没有前序切片。实施前读取 [整体PRD](../../prd.md)、[本批PRD](prd.md)、[design](design.md) 全文及第3节唯一来源设计处置。固定 B/H0=`8378b8d500a974ae1c01bd0571f30149f56541b0`；后续实施HEAD与PR target main独立。本轮独立候选 Architecture 返回 architecture_impact/target_native；当前真实贡献在 [architecture-contribution.md](architecture-contribution.md)，不能代替Wording-current final_plan。

必要输入包括：#713正文的R1–R5/S1–S5/修订后的取消项与AC；`trellis/presets/guru-team/MIGRATION-710.md` 的11字段authoring、完整6.0结果及两类token；`docs/requirements-design-test-contributions/710-phase2-recorder-authoring/test.md` 的候选、安装与旧失败边界；`docs/architecture/00-foundation/design-constitution.md` 和 `06-governance/change-contract.md` 的独立评估/晋升；`.trellis/delivery-contract.md` 的Candidate与operation；Author固定范围合同；workflow-contract的consumer连续性和quality-guidelines验证价值。实施/审核实际加载必要完整条件，不以本段引用代替读取。

#710 merge已在B；tools9是0.7.0-guru.7 local candidate、CLI/Core0.7.0-castbox.6，clean只到tools6。本批工程Intake和源码诊断不算public-only首次证据。采用现有 matching 结果时由原 owner 判断其适用性；不再追加 native 或重复安装。#711/#712不作为本批完成前置，也不提前实施其新增能力。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | 依赖、原owner与实际文件 | 具体动作与完成观察 |
| --- | --- | --- |
| P1 当前合同与真实consumer | Planning后进入implementation；固定B下registry、每包Interface/commands/SKILL及实际caller | 逐清单核当前profile、载体、semantic authoring、producer字段、输出和恢复。对R1–R5及同类普通路径缺口给可复现调用；确认旧consumer，删除/替换只走原owner，不把盘点当完成 |
| P2 creation与profile导航 | P1；`guru-create-task`、Completion及实证命中的包owner；`contracts/task-lifecycle/task-creation-input.schema.json`、包schemas/examples/interface/commands/references | creation引用原闭合source/target，补两种正常例；Completion当前/旧binding按profile选定。公共help显式给适用合同及载体；完整结果例与作者输入区分。Issue/no_issue经原入口正向执行并验证N2原误填 |
| P3 原Candidate生产能力 | P1；原delivery_projection执行owner；新`runtime/delivery_projection/candidate_cli.py`、workflow `scripts/bash/construct-delivery-candidate.sh`、preset `scripts/python/{skill_runtime_inventory.py,apply_guru_team_trellis_preset.py}` | 用原content_base/candidate构造完整Candidate；输入/输出按design第5节。无新算法/状态；原Delivery CLI消费完整operation执行begin-check/rework。保留旧candidate stdout，验证同DeliveryB优先及后续delivered范围 |
| P4 控制面与诊断 | P2/P3；`runtime/{command.py,schema.py}`、受影响包errors、Author正文、canonical workflow与implementation原step | 诊断具体field/constraint/contract/re-entry，内部故障保留范围。删除workflow内部导入操作说明；只保留全局调用路由。原step完整说明读取、输入载体、producer字段和receipt消费；已公开却跳读的偏离由Agent实际纠正 |
| P5 eval职责收敛 | P2–P4；`adapters/eval/{stage_result_authoring.py,native_adapter.py,implementation_authoring.py}`及`test_stage_result_authoring.py`、`test_implementation_authoring.py`、`test_native_constraint_transport.py` | 按design R5表逐项对照；生产导航/事实补偿改用原public入口。环境/替身/路径/透明运输/独立观测保留，当前语义判断由Agent写。不得按import机械删除合法单元fixture |
| P6 分层证据采用 | P5；原公开入口与现有验证结果 | 按修订 AC 核对现有命令、组件、consumer、安装及局部 native 结果；取消新 N1/N3/F10/R5 方法补证，不续旧 fixture，不改旧失败 |
| P7 分发及代表安装 | P2–P6；原installer/`guru-upgrade-tools`；canonical package/workflow/preset/受影响overlays、READMEs | 修改canonical后通过原tools owner同步本仓dogfood，保留Task/session；更新runtime/managed assets/mode。采用现有匹配安装/reapply/drift/sidecar/mode 结果；只刷新实际代码变更依赖，不重复 clean 安装。禁止手拷受管投影或用普通apply绕Task阻塞 |
| P8 完整知识与质量链 | P1–P7及实际候选；原RDT/Architecture writer、原Check/Commit/Review/Readiness | 完整拟写与实现先入候选Check；合法回implementation后原owners final_integration/readback；重新candidate/begin-check与最终Check；后续完整committed Review/readiness覆盖真实after。每次真实内容变化回最早受影响owner |

已有实现与验证结果保持其真实状态；本次只调整范围和证据采用规则，不据本计划宣称最终门禁已完成。每个触碰的非生成代码文件保持≤3000行；超出时由原AI先审机械拆分/小解耦，不扩大到历史未触碰文件。新增eval较长时拆独立case职责，不继续堆入native_adapter。Git/GitHub副作用仍由各原owner在实际边界处理。

## 3. 验证入口、输入与预期观察

先判断 V1–V4 和 I1 现有结果的适用性，只补实际变更影响的定向验证；再执行当前范围完整 Check 与 committed Review。取消项见本节，不再追加 native。

| ID | 实际入口、输入和验证方式 | 预期观察、AC与限制 |
| --- | --- | --- |
| V1 | `python3 -m unittest discover -s trellis/skills/guru-team/packages/guru-create-task/tests`；Completion及P1实证受影响包各自tests；原`run-skill-command.sh --help`及invoke | 正常Issue/no_issue真实进入executor；当前profile导航/authoring与原成功consumer可用。AC1/2；测试fixture不算Agent首写 |
| V2 | 在Git checkout/C4和当前pull_request Delivery前置下，为原construct CLI增加原delivery_projection定向测试并执行；输出直接交`python3 .trellis/scripts/delivery.py begin-check --task <TaskRef> --input <file>`及rework | 同D1固定B、正常后续delivered、完整路径、真实编辑stale、结果恢复。上游既有candidate --kind git_free只验证原consumer边界，不进入新桥接或被说成无Git Delivery。AC3/6；不复制算法计算期望 |
| V3 | `python3 -m unittest discover -s trellis/skills/guru-team/runtime/tests`；受影响包运行record/check/invoke及原普通错误 | 完整exit/stdout/stderr、receipt.result/实际artifact/typed exit承接；具体field/contract/stale/内部fault语义。AC4；不额外做fault injection |
| V4 | `python3 -m unittest discover -s trellis/skills/guru-team/adapters/eval -p 'test_*authoring.py'`及P5受影响运输测试 | eval透明消费原公开事实；当前判断无host预填；合法fixtures仍测试其consumer。AC8；不算N1 |
| N1（取消） | 不再运行新的完整首次 native 链 | 原失败及局部生命周期事实保留，AC5 不记通过 |
| N2（采用已有结果） | 已发生的字段/载体/receipt 普通错误及公开纠正 | 分别保留首失败和后续结果；不冒充首次正确 |
| N3（缩减） | 采用现有正常变化/stale/同结果恢复的局部结果 | 取消追加 public-only native 和旧 fixture 接续；不刷新旧摘要 |
| F（缩减） | 固定 family 的声明、导航、consumer 与现有定向结果 | 取消追加非等价 native；证据只覆盖其实际层级 |
| I1 | 原`guru-upgrade-tools`以完整matching source同步本仓；`bash trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`；原preset测试与代表性实际安装/reapply | AC9：源/installed provenance、平台投影、sidecar、mode、旧成功consumer及session/Task保留；原owner按live条件决定工具入口。至多一个clean；不扩完整矩阵 |

原 runner/tests/历史结果保留。取消项不再生成新 run、恢复旧 fixture 或补 native 环境；缺失能力不改记为通过。

### 3.1 调用语义family及代表性选择

family 是导航与证据对应，不是公共 API 或新状态。所有 profile 保留输入/输出/consumer 核对；下表按真实已存在结果采用，不要求新增 native，也不将同 family 推定为行为等价。

| Family | 不可合并的实际语义与代表案例 | 证据安排 |
| --- | --- | --- |
| F1 Intake/source | standard Issue intake、reviewed-plan、no_issue、proposed draft/standalone review、Issue创建与结果恢复；Discovery pre_task/context_request | 采用已有导航、creation/恢复命令与局部 native；其余模型行为未验证。 |
| F2 Task与checkout | Identity/Ensure；Bind的resume/missing/switch/reactivate/manual；branch establishment/rebind与丢输出 | 采用现有 Identity/Ensure/Bind/branch 定向结果及真实恢复事实。 |
| F3 scope/Planning | 根requirements→accept_scope、D1创建/selection、Author八Delivery profiles、Wording、Architecture两planning目的、Approval/Activation；withdrawal与revision分开 | 采用已有 Planning/Activation、alias/consumer 结果；取消 R5 同 fixture 接续和方法补证。 |
| F4 qualifiers | normal/solution/root三owner；11caller profiles具有不同authority与candidate上下文 | 采用原三 qualifier 的实际命令/consumer 结果；不新增 caller/goal 模型代表。 |
| F5 candidate/Check | candidate vs final、finding_fix、planning reentry、resolved reconciliation、scope withdrawal/revision；legacy control另列F12 | 采用当前 Check 与各 profile 的现有定向结果；最终 Check 仍实际执行。 |
| F6 commit/Review/readiness | initial/revision/finding_fix/recovery、committed reentry；完整branch、base continuity、archived、promotion reference；Draft独立 | 采用已有 commit/Review/readiness 合同与定向结果；主交付仍实际执行。 |
| F7 publication/merge/base | Ready/reprepare/same-plan、remote recovery、Draft；merged recovery；base演进发生于不同stage及resolved candidate | 采用现有定向及隔离 transport 结果；主 publication/merge gate 仍实际执行。 |
| F8 Completion/terminal | completion/evidence_refresh/reactivation_validation；**无当前Delivery**；Closure shared recovery、Finish reentry、Cleanup normal/explicit/machine | 采用现有 Completion/Closure/Finish 结果并保留其边界；取消新 native 全链。 |
| F9 Reactivate/知识维护 | archive vs existing implementation；RDT/Architecture bootstrap/impact/promotion/repair，Architecture阶段不同 | 采用现有 Reactivate/知识维护定向与贡献结果；主知识 final integration/readback 仍执行。 |
| F10 task-free/独立review | selected_route/interaction_resume；working_tree/committed_range；无Task/无Issue | F10/H2 非通过，R3 仅环境准备通过；取消追加 native，不启动原旧 fixture。 |
| F11 install/tools | 完整安装upgrade initial/resume/rollback、Delivery变体；tools install/resume/rollback；extension source verification | 采用仍匹配安装/tools、reapply/drift/sidecar/mode 实绩；不重复安装。 |
| F12 既有legacy control | Approval/Check/Review的inspection/retirement；Publish/Merge历史核验；maintain-legacy convert/history/resume/rollback/archive_resume | 采用原支持合同、合法历史 fixture 和现有定向结果；不新增 #712 家族。 |
| F13 instruction-only编排 | DAG与sequence两种不同选序/续接行为，standalone-only、无命令 | 采用既有 synthetic forward 和机械投影结果；不宣称 live 编排通过。 |

### 3.2 固定声明清单

以下从固定B的registry、各Interface与commands读取。每行给实际profile和全部command id；`W/S`只列routing非not_applicable的模式。列表用于逐项导航核对和family映射，不宣称所有profile语义等价。交付时只将本项相对B的新增/变更声明并入此处或原验证结果，不另造manifest。

| Active Skill / family | Modes | 当前input profiles | Command ids |
| --- | --- | --- | --- |
| `guru-activate-delivery` / F3 | W/S | `delivery_activation`<br>`delivery_scope_withdrawal`<br>`delivery_scope_revision` | `invoke-guru-activate-delivery` |
| `guru-approve-task-plan` / F3/F12 | W/S | `delivery_initial_review`<br>`delivery_revision_reentry`<br>`delivery_clarification_reentry`<br>`legacy_control_inspection`<br>`legacy_control_retirement` | `resolve-planning-artifacts`<br>`record-planning-approval`<br>`check-planning-approval`<br>`invoke-guru-approve-task-plan`<br>`legacy-maintenance-guru-approve-task-plan` |
| `guru-author-task-plan` / F3 | W/S | `task_scope_requirements`<br>`delivery_initial_review`<br>`delivery_active_task_scope_change`<br>`delivery_wording_reentry`<br>`delivery_approval_revision`<br>`delivery_delivery_plan_revision`<br>`delivery_requirements_revision`<br>`delivery_solution_planning`<br>`delivery_architecture_conflict_resolution` | `invoke-guru-author-task-plan` |
| `guru-bind-task-session` / F2 | W/S | `delivery_resume_current_task`<br>`delivery_rebind_missing_session`<br>`delivery_switch_task`<br>`delivery_reactivate_rebind`<br>`delivery_manual_recovery` | `invoke-guru-bind-task-session` |
| `guru-bootstrap-repository-ssot` / F9 | W/S | `new_repository`<br>`existing_repository`<br>`repair` | `invoke-guru-bootstrap-repository-ssot` |
| `guru-check-task` / F5/F12 | W/S | `delivery_candidate_check`<br>`delivery_initial_check`<br>`delivery_finding_fix_rerun`<br>`delivery_planning_reentry`<br>`delivery_resolved_reconciliation`<br>`delivery_scope_withdrawal`<br>`delivery_scope_revision`<br>`legacy_control_inspection`<br>`legacy_control_retirement` | `record-phase2-check`<br>`check-phase2-check`<br>`invoke-guru-check-task`<br>`project-resolved-reconciliation`<br>`legacy-maintenance-guru-check-task` |
| `guru-clarify-requirements` / F1/F3 | W/S | `standard_intake`<br>`reviewed_plan_intake`<br>`standalone_review`<br>`normal_scenario_scope_confirmation`<br>`solution_mechanism_scope_confirmation`<br>`delivery_active_task_scope_change`<br>`delivery_task_scope_revision`<br>`task_scope_requirements_acceptance` | `record-requirements-clarification`<br>`check-requirements-clarification`<br>`invoke-guru-clarify-requirements` |
| `guru-cleanup-task-resources` / F8 | W/S | `normal`<br>`select_explicit_cleanup_targets`<br>`machine_handoff` | `invoke-guru-cleanup-task-resources` |
| `guru-complete-task-closure` / F8 | W/S | `completion_approved`<br>`closure_shared_result_recovery` | `invoke-guru-complete-task-closure` |
| `guru-create-delivery` / F3 | W/S | `delivery_creation`<br>`delivery_selection` | `invoke-guru-create-delivery` |
| `guru-create-issue` / F1 | W/S | `issue_creation` | `record-issue-creation-plan`<br>`create-issue`<br>`check-issue-creation-result`<br>`recover-created-issue-result`<br>`invoke-guru-create-issue` |
| `guru-create-task` / F1 | W/S | `delivery_task_creation` | `record-task-plan`<br>`create-task`<br>`check-task-creation-result`<br>`recover-created-task-result`<br>`invoke-guru-create-task` |
| `guru-create-task-commit` / F6 | W/S | `delivery_initial_commit`<br>`delivery_revision_reentry`<br>`delivery_finding_fix_commit`<br>`delivery_recovery_resume`<br>`delivery_committed_reentry`<br>`delivery_draft_commit`<br>`delivery_draft_committed_reentry` | `prepare-task-commit`<br>`check-commit-messages`<br>`create-task-commit`<br>`invoke-guru-create-task-commit`<br>`migrate-task-commit-planning-source` |
| `guru-discover-change-context` / F1 | W/S | `pre_task`<br>`context_request` | `preview-change-context-history`<br>`record-context-discovery`<br>`check-context-discovery`<br>`invoke-guru-discover-change-context` |
| `guru-ensure-task-checkout` / F2 | W/S | `delivery_active_task` | `invoke-guru-ensure-task-checkout` |
| `guru-establish-task-branch-binding` / F2 | W/S | `delivery_active_task` | `discover-task-branch-binding-candidates`<br>`record-task-branch-binding-plan`<br>`establish-task-branch-binding`<br>`check-task-branch-binding-result`<br>`recover-established-task-branch-binding-result`<br>`invoke-guru-establish-task-branch-binding` |
| `guru-establish-task-identity` / F2 | W/S | `delivery_active_task` | `invoke-guru-establish-task-identity` |
| `guru-execute-task-free-change` / F10 | W/S | `selected_route`<br>`interaction_resume` | `record-task-free-change`<br>`check-task-free-change`<br>`invoke-guru-execute-task-free-change` |
| `guru-finish-task` / F8/F12 | W/S | `closure_completed`<br>`finish_reentry`<br>`legacy_control_retirement` | `invoke-guru-finish-task`<br>`legacy-maintenance-guru-finish-task` |
| `guru-maintain-architecture-baseline` / F3/F9 | W/S | `bootstrap_foundation`<br>`task_impact_sync`<br>`promotion`<br>`repair`<br>`delivery_task_impact_sync`<br>`delivery_promotion`<br>`delivery_repair`<br>`delivery_bootstrap_foundation` | `invoke-guru-maintain-architecture-baseline` |
| `guru-maintain-legacy-task` / F12 | S | `convert`<br>`history_closeout`<br>`resume`<br>`rollback`<br>`archive_resume` | `invoke-guru-maintain-legacy-task`<br>`preview-legacy-task-maintenance` |
| `guru-maintain-requirements-design-test-ssot` / F9 | W/S | `bootstrap_foundation`<br>`task_impact_sync`<br>`promotion`<br>`repair` | `invoke-guru-maintain-requirements-design-test-ssot` |
| `guru-merge-task-delivery` / F7/F12 | W/S | `delivery_ready_for_merge`<br>`delivery_scope_withdrawal`<br>`delivery_scope_revision`<br>`delivery_merged_recovery`<br>`legacy_control_retirement`<br>`legacy_history_verification` | `preview-task-delivery-merge`<br>`record-task-delivery-merge`<br>`check-task-delivery-merge`<br>`discover-task-deliveries`<br>`execute-task-delivery-merge`<br>`invoke-guru-merge-task-delivery`<br>`migrate-task-delivery-merge`<br>`legacy-maintenance-guru-merge-task-delivery` |
| `guru-orchestrate-issue-dag` / F13 | S | instruction/CLI合同，无structured profile枚举 | instruction-only，无commands.json |
| `guru-orchestrate-issue-sequence` / F13 | S | instruction/CLI合同，无structured profile枚举 | instruction-only，无commands.json |
| `guru-publish-task-delivery` / F7/F12 | W/S | `delivery_review_ready`<br>`delivery_same_plan_resume`<br>`delivery_reprepare_publication`<br>`delivery_scope_withdrawal`<br>`delivery_scope_revision`<br>`legacy_control_retirement`<br>`legacy_history_verification`<br>`delivery_draft_publish`<br>`delivery_return_to_draft`<br>`delivery_remote_draft_recovery`<br>`delivery_remote_ready_recovery` | `preview-task-delivery-publication`<br>`record-task-delivery-publication-gate`<br>`check-task-delivery-publication-gate`<br>`execute-task-delivery-publication`<br>`invoke-guru-publish-task-delivery`<br>`migrate-task-delivery-publication`<br>`legacy-maintenance-guru-publish-task-delivery` |
| `guru-qualify-normal-scenario` / F4 | W/S | `task_free_pre_write`<br>`task_free_evolution`<br>`requirements_scope_set`<br>`change_request_candidate_set`<br>`planning_scenario_set`<br>`implementation_discovery`<br>`base_impact_candidate_set`<br>`phase2_candidate_set`<br>`branch_review_candidate_set`<br>`publication_candidate_set`<br>`author_candidate_set` | `record-normal-scenario-qualification`<br>`check-normal-scenario-qualification`<br>`invoke-guru-qualify-normal-scenario` |
| `guru-qualify-root-cause` / F4 | W/S | `task_free_pre_write`<br>`task_free_evolution`<br>`requirements_scope_set`<br>`change_request_candidate_set`<br>`planning_scenario_set`<br>`implementation_discovery`<br>`base_impact_candidate_set`<br>`phase2_candidate_set`<br>`branch_review_candidate_set`<br>`publication_candidate_set`<br>`author_candidate_set` | `record-root-cause-qualification`<br>`check-root-cause-qualification`<br>`invoke-guru-qualify-root-cause` |
| `guru-qualify-solution-mechanism` / F4 | W/S | `task_free_pre_write`<br>`task_free_evolution`<br>`requirements_scope_set`<br>`change_request_candidate_set`<br>`planning_scenario_set`<br>`implementation_discovery`<br>`base_impact_candidate_set`<br>`phase2_candidate_set`<br>`branch_review_candidate_set`<br>`publication_candidate_set`<br>`author_candidate_set` | `record-solution-mechanism-qualification`<br>`check-solution-mechanism-qualification`<br>`invoke-guru-qualify-solution-mechanism` |
| `guru-reactivate-task` / F9 | W/S | `delivery_reactivate_shared_archive`<br>`delivery_reactivate_existing_implementation` | `invoke-guru-reactivate-task`<br>`observe-task-reactivation-implementation` |
| `guru-rebind-task-branch` / F2 | W/S | `delivery_task_branch_rebind` | `record-task-branch-rebind-plan`<br>`rebind-task-branch`<br>`check-task-branch-rebind-result`<br>`recover-task-branch-rebind-result`<br>`invoke-guru-rebind-task-branch` |
| `guru-reconcile-task-base` / F7 | W/S | `delivery_post_plan`<br>`delivery_post_check`<br>`delivery_post_commit`<br>`delivery_post_branch_review`<br>`delivery_post_publication`<br>`delivery_finalizer_base_mismatch`<br>`delivery_resolved_candidate` | `execute-base-candidate`<br>`execute-base-reconciliation`<br>`execute-resolved-base-reconciliation`<br>`project-resolved-full-review`<br>`record-base-reconciliation`<br>`check-base-reconciliation`<br>`invoke-guru-reconcile-task-base` |
| `guru-review-branch` / F6/F12 | W/S | `delivery_branch_review`<br>`delivery_base_continuity`<br>`delivery_archived_review`<br>`delivery_scope_withdrawal`<br>`delivery_scope_revision`<br>`legacy_control_inspection`<br>`legacy_control_retirement`<br>`delivery_promotion_reference_alignment`<br>`delivery_draft_content_review` | `review-branch`<br>`check-review-gate`<br>`invoke-guru-review-branch`<br>`review-branch-content-identity`<br>`legacy-maintenance-guru-review-branch` |
| `guru-review-change` / F10 | S | `working_tree`<br>`committed_range` | `capture-review-change-context`<br>`invoke-guru-review-change` |
| `guru-review-change-request` / F1 | W/S | `current_issue`<br>`proposed_draft`<br>`standalone_request` | `record-change-request-review`<br>`check-change-request-review`<br>`invoke-guru-review-change-request` |
| `guru-review-contract-wording` / F1/F3 | W/S | `change_request`<br>`delivery_planning_artifacts`<br>`explicit_paths` | `record-contract-wording-review`<br>`check-contract-wording-review`<br>`invoke-guru-review-contract-wording` |
| `guru-review-task-completion` / F8 | W/S | `delivery_completion`<br>`delivery_evidence_refresh`<br>`delivery_reactivation_validation` | `invoke-guru-review-task-completion` |
| `guru-review-task-delivery` / F6 | W/S | `delivery_delivery_review`<br>`delivery_scope_withdrawal`<br>`delivery_readiness_refresh`<br>`delivery_scope_revision` | `record-task-delivery-review`<br>`check-task-delivery-review`<br>`invoke-guru-review-task-delivery` |
| `guru-select-workflow-mode` / F1/F10 | W/S | `initial_request` | `check-workflow-environment`<br>`invoke-guru-select-workflow-mode` |
| `guru-sync-base` / F1 | W/S | instruction/CLI合同，无structured profile枚举 | `sync-base`<br>`check-base-sync`<br>`invoke-guru-sync-base` |
| `guru-upgrade-installation` / F11 | S | `initial_upgrade`<br>`resume`<br>`rollback`<br>`delivery_upgrade`<br>`delivery_resume`<br>`delivery_rollback` | `invoke-guru-upgrade-installation`<br>`preview-installation-upgrade` |
| `guru-upgrade-tools` / F11 | S | `install`<br>`resume`<br>`rollback` | `invoke-guru-upgrade-tools`<br>`preview-tools-upgrade`<br>`prepare-tools-upgrade` |
| `guru-verify-extension-installation` / F11 | S | `source_repository_verification` | `show-extension-version`<br>`execute-extension-verification`<br>`record-extension-verification`<br>`check-extension-verification`<br>`invoke-extension-verification`<br>`verify-extension-content-identity` |

固定声明共 43 active packages、127 commands、180 structured input profile条目；instruction-only与CLI-only并非遗漏。表中历史profile仍需按Interface/原合同判断是否当前可调用，不能仅凭列出便扩张支持。


## 4. 停止条件与适用回退点

源 Issue、根 requirements/accept_scope 与 D1 合法 scope revision 已完成。后续新范围变化仍回原 Clarify→Author→accept_scope→原阶段 owner；不直接覆盖 accepted_scope 或伪造 stage。方案/owner/兼容退出变化回原 Author/Architecture；等义文案仅刷新直接依赖。
| 取消项 | 范围 | 结果口径 |
| --- | --- | --- |
| C1 / AC5 | 新的 preTask→Finish 首次正确完整 native 链 | 取消本批验收；已有首装配失败与后续生命周期事实保留，不记全链通过。 |
| C2 / AC6 | 新的独立 N3 public-only 变化/结果恢复链及旧 fixture 接续 | 取消追加 native 和历史状态恢复；已有普通错误、stale、同结果恢复按实际层级采用。 |
| C3 / AC7 | F10、其余非等价 family/profile/caller/goal 的追加 native 代表 | 取消追加模型验收；保留 43/127/180 声明、导航与 consumer 映射和已有定向结果，未验证行为明确列出。 |
| C4 / AC8 | R5 完整方法加载、Planning→同 fixture Activation/resume、Drift 的模型方法补证 | 取消补证及重跑；保留职责对照、生产入口、alias/consumer 模块结果，以及 execution_error、fitness_regression 和方法证据不足。 |
| C5 / AC9 | 为补上述 native 而重复准备环境、恢复损坏 clean 或再次安装 | 取消重复准备与安装；复用完整且仍匹配的安装/投影、reapply/drift/sidecar/mode 实绩。 |

取消项的历史失败、部分结果和未验证保持；已知真正影响交付正确性的缺陷仍归原 owner 修复。并行改动、Task/session 和历史资源保持，不 reset/revert 无关内容。

## 5. Delivery Policy（唯一）

Policy=full。D1 独立交付修订后 S1–S5、AC1–AC4、缩减后的 AC6–AC8 与 AC9；AC5 取消，没有隐藏 D2 或必需补证支线。
可交付条件是当前范围实现和适用证据、Docs final reconciliation、最终 Check、完整 committed Review、Delivery Review/readiness 及原发布/交付链成立。Task Completion 仍判断整体 accepted_scope 与真实 Delivery 结果，实际 merge 前保留 fresh merge gate。
取消或未验证的完整 native 生命周期、R5 方法、其余模型行为和完整发布矩阵均明确披露，不称通过。

## 6. Docs SSOT Plan（唯一）

strategy=`delta_first`。实施期间原RDT writer在Task内准备真实完整差额；最终由 `guru-maintain-requirements-design-test-ssot` 对 `docs/{requirements,design,test}/current/task-delivery-lifecycle.md`、`completion-closure.md`、`knowledge-maintenance.md` 的实际命中单元及必要canonical Skill/命令引用执行reconciliation。要求层承接公开支持行为和修订后的定向验收及取消项；设计层承接原 owner 事实能力/导航/错误恢复；测试层承接分层结果、未验证行为和安装限制。具体完整单元由原owner按实际实现确定，保持稳定authority identity与合法现有布局，不做#711迁移。

Architecture贡献为当前D1内真实文件；原Architecture owner审核并准备必要完整proposed单元。此方案沿既有owner/固定B/recorder决定，无新ADR；若发生决策/GAP/原则例外变化再回原owner产生真实ADR。RDT不能改Architecture，Author不晋升共享current。共享导航仅在实际定位/状态变化时由所属writer维护，不预建空索引或贡献。

直接consumers是当前Check、完整Review、readiness、Delivery Review和Task Completion。顺序为：完整实现与隔离拟写→独立Architecture phase2及原候选Check→合法rework回implementation→原RDT/Architecture final_integration与readback→after重绑、重新candidate/begin-check→最终Architecture/Check→commit→完整committed Review/readiness。真实写入或内容变化必须被最终质量链覆盖，不能靠后补文档commit绕过Review。

历史Issue/归档/原验证记录保留其原身份和失败，不批量改写；只在当前authority中更新适用说明、合同与验证边界。受管spec/workflow/Skill/platform投影由原preset/tools分发，reapply/drift/sidecar/mode由P7验证。当前规划不写共享RDT/Architecture authority或journal。
