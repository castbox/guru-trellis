# #383 因果完成设计

## 设计对象与当前事实

Canonical 包在 trellis/skills/guru-team/packages/，installed runtime 在 .trellis/guru-team/skills/packages/；平台 .agents/.codex/.claude/.cursor 是发现与调用投影。共同 causal SSOT 尚不存在。guru-qualify-root-cause 已区分目标并提供最小 disposition；guru-review-task-completion 已有 Delivery-based 与 Reactivate-only pending/refresh。现有 runtime 只校客观输入并序列化 AI 路由，不具备因果判断权限。

设计保留既有 semantic owner 和公共 I/O。新增行为由 Markdown 声明，由 AI 读取事实作判断，脚本执行检查与路由。先直接修改原 owner，不新增 wrapper、规则引擎、adapter 或第二 state machine。

## D383-01 共同语义 authority

新增 trellis/presets/guru-team/spec/workflow/causal-completion-semantics.md；dogfood/installed 唯一投影为 .trellis/spec/workflow/causal-completion-semantics.md。文件声明 causal_semantics_version=1、稳定 semantic identity 与 content-identity 解析方式：版本、canonical locator 和当前正文精确 bytes；当前读取方可计算 SHA-256 作局部一致性检查，不在正文保存自引用 hash，不把 digest 当 approval 或新增跨阶段 freshness 协议。

共同正文定义 diagnosis/implementation/static/integration/external/production/root resolution/mitigation/remaining risk，及 diagnosis_incomplete、root_cause_identified、mitigation_applied、implementation_validated、external_effect_unverified、production_effect_verified、root_cause_fixed 的适用条件。按目标核对 admission、failure stage、classification、outcome、owner、time window、completeness；同一维度改善不推出其它维度完成。混合目标按各项判断，完整 task 按全部 scope 判断。

诊断/缓解未知根因不是固有阻塞；其自有验收仍不能省略。生产要求由 accepted scope 决定，ordinary feature 不继承故障问卷。严格等价性由 Completion 对原机制和证据作语义判断，fixture 只证明 workflow 判断。现有权限与 dangerous replay 边界保持。

Installer 的 MANAGED_SPEC_PATHS 当前是显式枚举；新增文件不会自动安装。将新 canonical→installed 路径对注册到 trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py，仍由原 installer 执行 managed hash/sidecar 语义；不写新安装器。当前文件 2961 行，这次一对映射保持低于 3000 行。

共同文件不包含 stage route、Skill invocation、public DTO 或 recorder 算法。发生语义变化时更新本文件与受影响 eval，原 owner 判断依赖，从最早受影响阶段重新读取；无关字节变化不自动全链失效。

## D383-02 各 owner 的读取与判断

| Owner / canonical source | 当前要承接的本阶段职责 |
| --- | --- |
| guru-qualify-root-cause/references/contract.md | 用正式共同引用替换“#383 文件未存在”的临时说明；继续独占候选准入，不复制完成正文。 |
| guru-approve-task-plan/references/contract.md | planned diagnosis/mitigation/repair 的证据目标与 validation 条件引用共同文件；不重新定义资格。 |
| guru-check-task/SKILL.md + references/contract.md | 完整 current worktree 检查实际 consumer/机制/失败样本；按本阶段目标选择已声明出口。 |
| guru-review-branch/SKILL.md + references/contract.md | exact base/head/full diff 独立审实现期增量、样本/fixture 与失败迁移，不能复用 Phase2 pass。 |
| guru-review-task-delivery/SKILL.md + references/contract.md | reviewed PR payload 分层报告证据与风险，防止把 mitigation/merge/静态结果包装成修复；Refs-only。 |
| guru-review-task-completion/SKILL.md | whole-task accepted scope、全部 Delivery、live source、适用证据与 closure disposition 的唯一最终语义判断。 |
| guru-reconcile-task-base/SKILL.md + references/contract.md | base/authority 演进改变共同语义或机制依赖时，从实际最早受影响 owner 重入；不自动重复未变化资格。 |

Delivery Review 的证据门槛是本次独立 slice 的 accepted 条件，Completion 的门槛是 whole-task accepted completion definition。若生产效果只有 merge/deploy 后才能取得，交付前报告 production_effect_unverified 与本 task 的剩余证据 owner/条件；不存在以完成生产验证作为正常交付先决条件的循环。仅当当前 slice 自身 required evidence 不可取得，Delivery 才走其 blocked。

以上 entry 显式加载共同 spec，各 contract 只拥有 stage-local 正向行为与 routing，不复写共同维度。workflow 只维护 invocation/transition/consumer，不承载共同因果正文。Skill public input/exit/schema 保持 current version；本设计不引入字段或新的 DTO。

## D383-03 Current exit 与唯一 consumer

| Producer | 条件 | Current exit -> consumer |
| --- | --- | --- |
| Check | 根因修复计划缺本阶段必要因果依据；或诊断/缓解自身计划不完整 | planning_stale -> guru-task-check-planning-router |
| Check | 已证实症状抑制、机制偏离或 required test 缺失 | implementation_required -> guru-resume-implementation |
| Check | 本阶段 scope 完整且无阻塞证据缺口 | passed -> guru-create-task-commit |
| Branch | committed 实现偏离 mechanism/样本/consumer 合同 | implementation_required -> guru-branch-review-implementation-router |
| Branch | 实际 accepted product scope 需改变 | scope_confirmation_required -> guru-branch-review-scope-router |
| Branch | full diff 本阶段要求满足 | passed -> guru-review-task-delivery |
| Delivery | slice/policy 本身缺失或含义不完整 | planning_revision_required -> guru-task-delivery-planning-router |
| Delivery | public claim 与实际实现/证据不符 | implementation_required -> guru-resume-implementation；同 slice 纯 payload 修订由本 owner fresh review |
| Delivery | accepted scope authority 真正改变 | scope_confirmation_required -> guru-task-delivery-scope-router |
| Delivery | 已验证 slice 与 truthful payload complete | ready -> guru-publish-task-delivery |
| Completion | accepted work 尚未完成 | remaining_work -> active-task-continuation |
| Completion | requirement/plan 需修订 | requirements_revision_required -> task-requirements-revision-router |
| Completion | 当前实现需修订 | implementation_revision_required -> guru-resume-implementation |
| Completion | 需第二次业务 Delivery | additional_delivery_required -> task-delivery-planning-router |
| Completion | accepted external/production evidence 尚未到达 | evidence_pending -> guru-review-task-completion 的 evidence_refresh |
| Completion | whole scope 完成且 disposition current | completed -> guru-complete-task-closure |

各 owner 的 blocked 保持 current Interface 对应 stop，只用于不能可靠判断的实际缺 authority/依赖，不将正常待证据改挂 stop。root_cause_fixed、mitigation_applied、external_effect_unverified 是 semantic disposition，不能当新 success exit。

evidence_pending 无新证据时等待，说明缺口、取得证据的既有 owner 和重入条件；不立即再次调用 Completion。Delivery-based refresh 保留原 exact merge_result；Reactivate-only 保留 current reactivation_anchor，使用本代 evidence。当前 Delivery evidence_slots 仍只使用 planning、delivery_review、delivery_publication；Reactivate-only 仍只使用 reactivation、validation。生产/外部事实由 owner fresh 读取其正常证据来源，在现有字段中绑定本轮 evidence identity，不增设 global causal 或 production slot。completed 不能跳过 Closure。diagnosis/mitigation/implementation-only 与 source/parent root-fix requirement 不一致时不得产生 close_source 结论；source 范围确需变化返回 requirement owner。

## D383-04 验证机制

现有 package tests 与 wrapper transport 证明 objective contracts，不能证明 AI cognition。行为矩阵由独立事实输入驱动真实 native semantic authoring：native 读取 current owner Skill、共同 spec、真实当前事实/候选差异，输出本阶段 owner judgment；host 才读取期待出口并通过实际 installed wrapper 观察。期待答案、预填 pass、mocked semantic review 不进入 native 输入。

C01..C07 检查四阶段目标感知和抑制/迁移/protection；C08..C18 检查 diagnosis/mitigation/ordinary/repair 和生产等价边界；C19..C21 使用真实 Git/lifecycle fixture、同任务二次 Delivery 与两种 refresh anchor。复用已有 Completion tests fixture 和 caller contracts；fixture/mock 证据只证明流程，不证明生产修复。验证失败保留实际结果，修订最早受影响 owner，不扩充通用 validator。

## Docs SSOT Plan

策略：ssot_first。需求 authority 为 live #383 r9，语义正文先写 canonical，受影响 Skill 只引用并声明本阶段行为。Task PRD 是规划入口，不是第二长期共同语义 authority。

RDT isolated contribution：docs/requirements-design-test-contributions/383-causal-completion-semantics/{manifest.yaml,requirements.md,design.md,test.md,traceability.md}。Requirements 拥有 R383-01..09 映射；Design 拥有 D383-01..04 与 current Interface 引用；唯一 Test 拥有 C01..C21 的实际结果、失败与未验证边界。Contribution 不复制共同 spec 正文，完成独立 committed review 后按 expected .79 由原 owner 串行 promotion；promotion diff fresh Phase2/commit/Branch Review 后才可公开交付。

Architecture 由 fresh independent subagent 从本 design 事实、现有实现和 live authority 判 impact/path，不由本文件预选 pass。若判 impact，task-only contribution 为 docs/architecture/contributions/383-causal-completion-semantics.md，按项目九 concern 和适用 project-check protocol 承接；ADR 仅在 reviewer 认定实际 decision/owner/compatibility 变化时新增。若 no-impact，不创建贡献或 ADR。共享 current 在 promotion 前不改。

导航/spec/README 只加职责与唯一引用，不复制共同语义。Installer apply 同步所有 manifest-selected 投影；声明平台 inventory 不以三平台 dogfood 代替全集分发检查。历史 #382 文档保持 immutable；本任务退出临时 missing-SSOT 说明，没有 legacy 双读。

## 权限与边界

Implementation 激活、commit、Delivery publish、merge、Closure、Finish 和 Cleanup 分别按其当前边界执行。接管 branch/worktree 为 caller_owned，清理不能推断为自动授权。生产无访问或写入；普通任务不执行累计完整 matrix。若需要 public API、owner、scope 或新增兼容路径，先回 Planning/Clarification 与显式迁移，不能按本设计静默扩展。
