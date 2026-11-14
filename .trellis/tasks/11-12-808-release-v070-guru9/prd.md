# #808 准备 v0.7.0-guru.9 发布：整体需求

## 1. 来源与术语

本 Task 的来源是 [castbox/guru-trellis #808](https://github.com/castbox/guru-trellis/issues/808)，source disposition 为 `reference_only`。本 Task 只承接其中的准备阶段；发布 Issue 继续承担准备合并后的候选验收、正式发布、本地收敛和最终关闭。本文不缩减 #808 的整体完成条件。

| 来源 | 章节或条款 | 角色与本 Task 用途 |
| --- | --- | --- |
| [#808](https://github.com/castbox/guru-trellis/issues/808) | 背景与目标；前置与准备范围 | 要求：定义版本映射、#794 硬前置和本 Task 的准备责任 |
| [#808](https://github.com/castbox/guru-trellis/issues/808) | 冻结候选与验收；正式发布与本地收尾；完成条件与范围边界 | 要求：保留 Stage 2 的全部责任、失败停止条件、两个选定本地目标和非目标 |
| [MIGRATION-794](../../../trellis/presets/guru-team/MIGRATION-794.md) | 新正常链；公开边界；在途处置；完整采用与验证 | 约定设计：原工程整合、本地提交、一次独立完整审核及原消费者迁移 |
| [私有发布合同](../../../.agents/skills/release-guru-trellis-version/references/contract.md) | Two-Stage Lifecycle；Stage 2；Local Installation Convergence；副作用与持久化边界 | 现有编排约束：Stage 1 的旧重复门禁按 #808 和 #794 修正；Stage 2 locator、原 owner、独立副作用及禁止持久化规则继续承接 |
| [当前 workflow](../../../.trellis/workflow.md) | Phase 1、Phase 2、Phase 3、Workspace and task boundary | 流程约束：规划、整合、提交、审核、交付、Completion、Closure、Finish、Cleanup 各归原 owner |
| [公开文档规范](../../../.trellis/spec/docs/public-docs.md) | Document Responsibilities；Version and Evidence Sources | 文档约束：三个 README 的职责、版本轴、immutable 同源安装及证据边界 |
| [验证规范](../../../.trellis/spec/workflow/quality-guidelines.md) | Test And Validation Value；Validation Scope Ownership | 验证约束：行为与实际入口决定验证范围，复用适用证据，不扩张累计完整矩阵 |
| [仓库指令](../../../AGENTS.md) | 第6、7节 | 仓库约束：canonical、dogfood、installed、平台与 drift 验证完整履行；既有 checkout 的工具更新归原 tools owner |
| [原 Clarify 合同](../../../.trellis/guru-team/skills/packages/guru-clarify-requirements/references/contract.md) | Delivery scope revision；Whole-scope writer and publication migration | 分配约束：同 Task 可有顺序 Delivery；Clarify 判断分配，Author 写正文，实际接受后由当前阶段 owner 修订切片 |
| [原 Delivery Review 合同](../../../.trellis/guru-team/skills/packages/guru-review-task-delivery/references/contract.md)；[原 Completion](../../../.trellis/guru-team/skills/packages/guru-review-task-completion/SKILL.md) | Stage facts in this slice and payload；实现接续 | 验收约束：来源交付、dogfood 投影与目标采用分别取证；剩余实施经 additional_delivery_required 进入原 Creation，不以单 slice 合并推导 Task 完成 |

术语：

- **Stage 1 / 准备阶段**：本 Task 的业务交付，加上原生命周期 owners 的正常终态收口。
- **Stage 2 / 发布阶段**：准备交付和 Finish bookkeeping 合并后，由发布 owner 对 fresh main 冻结的唯一 candidate 执行验收、tag、smoke、Release、本地收敛和 Issue 关闭。
- **Task Completion**：审核本 Task 的全部准备业务范围。它不等于 #808 完成，也不代替随后 Closure、Finish 和 Cleanup 的结果。
- **candidate**：Stage 2 冻结的一个精确 commit/tree。准备分支的 HEAD 或既有审查结果不能代替它。
- **真实 dogfood**：本仓实际 checkout 的完整受管工具与安装状态；throwaway 成功不能替代其更新与验证。

## 2. 背景与问题

#808 要求在 #794 完整交付、完成关闭和必要归档之后发布正式 `.9`。发布内容包含 #793、#792、#794，以及真实 `.8` 前驱之后到最终 candidate 的全部差额，不能只按三个 Issue 选取发布集合。

准备前的源码仍以 extension `.8` 为版本标识。私有发布合同及其 [回归测试](../../../.agents/skills/release-guru-trellis-version/tests/test_contract.py)仍要求晋升前后两轮旧 Check/Review。#794 已定义的新链将必要知识整合放在本地提交前，并由提交后的同一次独立完整 Review 承担 Check 与 Branch Review 的适用职责。准备阶段必须修正这个私有消费者及其平台副本，不能为了遵从旧文字重建退休门禁，也不能漏审后继内容变化。

版本标签不能证明内容或安装相同。真实前驱和当前来源的 CLI 字面版本可以相同，但 Fork commit 不同；前驱升级验证必须从真实前驱自己的 manifest/lock 派生来源。源码同步、Git 快进、validator 或 throwaway 也不能证明实际 checkout 已完成 `.9` tools 更新。

因此，需要先完成一个可独立收口的准备 Task，形成版本、文档、私有消费者、受管投影及真实 dogfood 一致的准备交付，再由独立的发布阶段完成 #808 剩余责任。

## 3. 目标与非目标

### 3.1 目标与版本输入

| 输入 | 要求 |
| --- | --- |
| repository | `castbox/guru-trellis` |
| release Issue | `#808` |
| repository tag | `v0.7.0-guru.9` |
| extension revision | `0.7.0-guru.9` |
| Trellis CLI/Core | `0.7.0-castbox.6` |
| predecessor tag | `v0.7.0-guru.8` |

本 Task 完成下列准备业务范围：

1. 对齐 canonical extension revision、公开文档、兼容迁移说明及真实受影响的 Docs/Architecture/RDT。
2. 使私有发布消费者、测试和四个平台发现副本合法采用 #794 当前链，保持私有分发边界。
3. 由原 tools owner 从完整干净匹配来源，实际更新并验证本 Task checkout 的 dogfood；受管变化进入最终提交及完整审核范围。
4. 通过原提交、独立审核、Delivery Review、Publication 和 Merge owners 将准备交付合入 `main`。准备 PR 仅使用 `Refs #808`。
5. 原 Completion 判断全部准备业务责任后，依次完成 Closure `no_mutation`、必要 acceptance-finish Architecture 判断、Finish 终态归档和精确 Cleanup。

准备业务验收与生命周期终态按各自先后阶段判断。Completion 不能要求尚未发生的自身结果、Finish 或 Stage 2 作为前置；准备业务完成也不能免除后续归档与资源收口。Stage 1 正常结束需要原 Finish 与 Cleanup 的真实结果。

### 3.2 非目标与保留责任

- 本 Task 不执行 Stage 2 的候选冻结、发布验收、tag、tag-pinned smoke、正式 Release、发布后本地收敛或最终 #808 关闭。这些义务按第 5.6 节保留。
- 不等待 #736 整体完成，不实施其他开放 Issue，不改 Trellis 上游源码、全局包或 `node_modules`。
- 不提升 Fork CLI/Core 版本，不升级业务仓库，不部署生产，不清理无关 Task/worktree。
- 不扩张为累计完整多平台 Release Gate 矩阵，不承诺其他 native host 或真实业务升级已验证。
- 不新增公共发布 Skill、流程权威、schema、checkpoint 或发布状态账本。

### 3.3 同 Task 的顺序准备交付

本 Task 保留全部 AC-01～AC-08。准备业务按完整来源交付、实际采用的依赖顺序分配；各 Delivery 都必须独立满足自己的完整实施、验证、提交、审核和交付要求。

| 切片 | 独立目标与必须完成的责任 | 保留的后继责任 |
| --- | --- | --- |
| 当前 D1，保留 `b40421e8-6213-4f29-bb11-8d3919e533b0` | 交付完整可分发的 `.9` canonical 来源、版本直接消费者、私有发布编排及四份发现副本、真实回归、必要文档和知识整合。来源自身的版本、接口、依赖、安装可用性及本 slice 必需验证不得留给 D2 才修复。经原 TaskCommit、独立完整 Review、readiness、Publication 和 Merge 形成实际 delivered 来源 | 本 checkout 对该来源的实际受管采用及相关验证由同 Task 后继 D2 承担；D1 准确说明当前安装与来源差额，不声明采用通过 |
| 后继 D2，由原 Completion 接续后再经原 Creation 建立 | 读取实际 D1 交付结果，从完整干净匹配来源以原 tools 的 `source_locked` 更新本 Task checkout。完整 package/platform/workflow 投影、installed/native、preservation、ownership、mode、sidecar、parity 和 drift 验证均须完成；安装及必要文档 after 全部进入 D2 的真实候选、独立完整审核和交付 | 若仍有准备业务或必要证据缺口，原 Completion 按实际情况返回原 owner；全部准备业务满足前不进入 Closure/Finish |

D1 来源交付不能以先完成 D2 实际采用为自身成立条件。若后续 Author、Architecture、Approval 或 Review 发现这种依赖，必须回原分配/规划 owner；不得把 D1 自身缺陷或必需验证失败列为后继工作来取得通过。D1 的原候选 Policy 不决定新的切片分配，只有实际接受的整体范围和当前阶段 owner 修订后的 scope_ref 才能供后续规划消费。

canonical 修改后的 dogfood 同步仍是本 Task 必须完成的义务。分配期间的旧安装、公开 schema 投影差额和 drift 失败必须如实报告，不能改记 pass，也不能证明 `.9` 已采用。只在原 owners 已接受独立来源切片及剩余采用责任后，才按各 slice 的真实验证边界作判断。若 D1 实际扩大到必须同时采用的 workflow/overlay 或执行机制变化，先回原 owners 重新判断，不能沿用本分配豁免同步。

## 4. 真实调用方、场景与流程

| 场景 | 调用方、前置与触发 | 行为与可观察结果 |
| --- | --- | --- |
| SC-01 核实发布输入 | 准备 owner 开始工作，或版本/来源事实变化 | fresh-read #808、#794 的交付/关闭/归档及 main 可达性、tags/Releases、版本面和 lock。六项输入唯一且可用才继续；占用或实质变化回原范围 owner |
| SC-02 采用当前审查链 | 原 Planning/实施 owner 处理旧私有发布消费者 | 保留原职责、接口与恢复边界，完成必要文档整合和工程自检，再本地提交并进入固定完整区间的独立 Review；同一未变候选不因阶段切换重复完整审查 |
| SC-03 实际 dogfood 更新 | D1 已实际 delivered，后继 D2 已经原 Creation、Planning/Activation；原 `guru-upgrade-tools` 取得完整干净匹配来源 | 以 `source_locked` 对精确 Task checkout 做 preview、prepare、执行和读回；实际版本、受管字节、provenance、CLI/lock 与 native entry 得到验证，原 Task/session/user config 保留 |
| SC-04 准备交付 | 当前 slice 的完整实施、所选验证和必要整合已形成真实本地候选；D2 候选包含全部安装 after | 每个 Delivery 由新开的未参与实现的 reviewer 完整审核，原 Delivery Review 判断 readiness，Publication 才执行已审 push/PR。原 Merge 按独立 expected-head 边界合并到 main；前一 slice 通过不代替后一 slice 审核 |
| SC-05 接续与正常终态 | 某 Delivery 的原 Merge 已给出真实 delivered | Completion 核全部准备业务范围；D1 后剩余实际采用使用 additional_delivery_required，经原 Creation 建立 D2。全部准备业务满足后才进入 Closure no_mutation、acceptance-finish Architecture、Finish 及精确 Cleanup |
| SC-06 后置发布 | Stage 1 业务与 Finish bookkeeping 均已合并 | 发布 owner 重新读取 main，证明 lineage，冻结唯一 candidate；第 5.6 节的验收及独立副作用依序执行，不采用准备候选的 pass 冒充发布 pass |
| SC-07 中断或不一致 | 任一原 owner 发现 stale/mismatch、失败或输出丢失 | 由该原 owner 核实际副作用、同一 identity/source/operation 并恢复；内容变化刷新受影响门禁。保留已发生事实，不重复创建或借用旧通过结果 |

## 5. 行为要求

### 5.1 R-01 输入、来源与版本一致

SC-01 必须满足第 3.1 节映射。执行前重新核实 #794 的实际交付、完成关闭、必要归档及 live main lineage。版本被占用或来源发生实质变化时回原范围 owner，不覆盖已发布 tag，不自行选择替代版本。

`trellis/guru-team-extension.json.version` 是 canonical extension revision；installed manifest 的 `extension.version` 和 `source` 表示实际安装与 provenance；`.trellis/.version` 表示 CLI。CLI 不变时不得将该文件写成 Guru revision。当前与前驱 Fork 来源分别读取各自真实 lock，版本相同不能替代 commit/build 匹配。

marketplace 与 preset 必须采用同一个 immutable Guru 来源。公开文档区分准备目标、候选试用与已发布稳定版本，不在 tag/Release 尚未存在时声称已发布。最终发布说明以完整前驱 diff 为依据，不以 Issue 列表代替内容审核。

### 5.2 R-02 私有消费者采用 #794

SC-02 必须核对 `.agents/skills/release-guru-trellis-version/` 的合同、实际测试和必要消费者，修正仍要求旧 Check/晋升后固定第二轮审查的 Stage 1 编排。新的正常顺序为：Planning/Activation → 实现与工程自检 → 原 RDT/Architecture 必要整合及 readback → 原 TaskCommit 本地提交 → 固定完整 committed candidate 的一次独立 Review → 原 Delivery Review/readiness → Publication。

独立 Review 保留需求/设计承接、实现和测试有效性、必要消费者、减法优先、可维护性、兼容及完整范围责任。实现后的独立 Architecture 判断由同次新独立 reviewer 按原读取顺序完成；Planning 的独立架构判断仍有效。真实修复或内容变化形成后继候选并刷新受影响覆盖，不能用“一次”免除后继审查。原工程结果和可核验覆盖先判适用性，再补真实缺口。

采用范围还包括退休 gate、early Draft、Skill/package/command 消费者及受支持在途恢复。保留原 PR/HEAD、固定 B 和原事务；已执行效果只恢复，pending 新远端动作必须先满足当前独立审核和 readiness。不得静默转换旧 pass，或先 push/建 PR 再补审。

私有合同及 `SKILL.md` 在 Shared、Codex、Claude、Cursor 的实际发现副本保持一致；测试须验证改变的真实调用/消费行为，不能只比较旧链条文字。该私有 Skill 不进入公共 registry、extension manifest、marketplace、preset、overlay 或业务仓安装。

### 5.3 R-03 公开文档与知识收敛

版本、公开安装入口、兼容迁移说明、受管投影与真实受影响的 Requirements/Design/Test/Architecture 定义保持一致。原 Author 在 Delivery 规划内选择完整 Docs SSOT Plan，原 RDT/Architecture owners 在合法边界整合必要正文并读回；整合事实不冒充独立语义通过。

只更新实际受影响的完整单元和必要关系，保留历史版本、证据原义及未验证边界。不为发布制造全局知识版本、共享索引登记、状态提交或重复定义。规范性来源设计的保留、修改和理由由后续 Delivery design 的唯一处置承担，本整体 PRD 不另建方案矩阵。

### 5.4 R-04 真实 dogfood 与工程验证

SC-03 由原 `guru-upgrade-tools` 从完整干净匹配来源执行 `source_locked`，不以普通 apply 绕过历史 Task 前置，不以 throwaway 替代真实更新。来源取得按第3.3节：D1 完整交付并实际 delivered 后，后继 D2 才消费该来源。D1 的本地来源提交仍须走原 TaskCommit 的完整前置及其唯一 constructor/begin_check/Review consumer；没有专用 early source 分支，也不安排已知缺陷审核来取得返工路线。

D2 的来源必须有真实 D1 交付依据及可读取的精确 commit，执行 provider 的 HEAD、完整干净来源、该来源自己的 lock 和匹配 CLI/Core 构建由原 owner 核对。未交付提交、dirty 来源或未来 SHA 不能代替它。安装产生的受管内容变化纳入 D2 的完整提交及最终独立审核；D1 的来源审核不证明 D2 的实际采用通过。

原 owner 验证实际 extension revision、完整 managed assets、source provenance、CLI、lock、目标自己的 resolver/installed validator 与实际 native entry。允许证明与最终候选受管内容和 lock 等价的真实已提交来源，不追逐自引用 HEAD，不手改 manifest 伪装安装。未知用户修改、冲突和 `.new`/`.bak` 按原 owner 处理，未解决不得报成功。

保留 Task、archive、workspace、session、用户配置、peer 工具和 common runtime 指针。原失败事务先由其原 owner 按原 source pair、冻结计划和恢复合同处置，不换源直接续跑，不扩张成历史 Task 转换。

准备验证按实际变更选择 package/runtime、canonical/dogfood/installed、声明平台、ownership、mode、sidecar 和 drift 的最小可靠集合。D1 完成来源和消费者自身的全部必需验证；D2 完成真实目标采用及完整匹配验证。两者共同覆盖本 Task 的全部验证义务，不能因分配而删项。复用仍适用的工程事实，补必要缺口；静态检查、fixture、投影一致、真实 Agent 行为和实际安装分别说明。Stage 2 的 focused/existing 与完整候选门禁不提前记作准备通过。

### 5.5 R-05 交付与终态

SC-04 的本地提交只由 `guru-create-task-commit` 拥有。独立完整 Review 及原 readiness 通过前不新 push、不建 PR。原 `guru-review-task-delivery` 审查当前 slice、剩余准备工作、验证和边界，形成具体中文 PR 标题正文，仅使用 `Refs #808`。Publication、Merge 的原事务、freshness 和独立副作用边界保持。

SC-05 的 Completion 只判断本 Task 的全部准备业务范围和所有 Delivery/证据；业务 PR 合并不自动证明整体准备业务完成。D1 交付后，未实施的实际采用是剩余实施责任，应由原 Completion 使用 `additional_delivery_required`，其唯一 consumer 进入原 Creation 和新 slice Planning，不能把它改称仅待观察的 evidence_pending。D2 不提前创建，D1 不重开为当前执行切片。其他实际缺口按其性质回最早受影响 owner，不提前 Finish。全部准备业务完成后 Closure 必须为 `no_mutation`，不得关闭 #808。

随后由原 acceptance-finish Architecture owner 和 `guru-finish-task` 完成必要判断、唯一归档、独立 bookkeeping 发布及 expected-head 合并。main 实际包含终态归档后，原 Cleanup 审查精确资源；本 Task 采用的 caller-owned 分支和 worktree 不自动删除。资源失败保留其原恢复责任，不撤销或伪造已完成阶段。不得清理其他 Task/worktree。

### 5.6 R-06 Stage 2 的完整独立责任

以下是 #808 保留的后置责任，不是本 Task 准备业务 Completion 的前置，也不由本 Task 的 `no_mutation` 代替：

1. 准备交付和 Finish bookkeeping 合并后，fresh-fetch main，证明真实前驱、准备交付及唯一终态归档 lineage，从干净 checkout 冻结一个 candidate commit/tree。此前候选的 pass 失去直接发布证明作用。
2. 对同一 candidate 完整审核 `.8` 到 candidate 的 diff、版本映射、公开变更说明、兼容边界和 immutable 同源安装。执行 source/installed validators、Shared/Codex/Claude/Cursor parity、ownership、普通 self-reapply、dogfood drift，以及实际 candidate 安装的版本/字节/provenance/CLI/lock 核对。
3. 使用匹配的干净 Fork 构建执行私有合同的 focused clean install、existing update/reapply，并从真实 `.8` 安装做一次定向 existing upgrade。前驱 CLI/commit 必须从真实前驱 manifest/lock 一致值派生。核对前驱与 candidate inventory，确认退休资产退出、用户配置保留，且无未处理冲突或 sidecar。
4. 用真实 secret scanner 扫描完整适用 changed-file bytes，完成 residue、diff hygiene 和独立完整候选语义审核。FAIL、SKIP、stale、cross-SHA 或身份不符均阻止后续发布；内容变化回原 owner，刷新受影响门禁并重新冻结。
5. 普通 self-reapply 必须实际执行并如实保留结果。仅当私有合同 Historical-Task Preflight Observation 的全部条件满足，原独立 Release reviewer 才能接受其限定替代证明：唯一停止原因是已审历史记录触发的 `upstream_delivery_migration_required`；实际 candidate dogfood 已独立满足完整身份与内容门禁；同一 candidate 的干净 standalone 完整安装、Claude/Codex/Cursor reapply、installed validation、来源/字节/mode/lock/workflow 及无残留证据齐全。该证明只覆盖可分发 preset，不转换历史 Task，不替代实际 dogfood 或本地目标，也不将原停止改写为通过。其他错误走原停止路线。
6. candidate gate 通过后，分别展示并确认 annotated tag 创建/push、tag-pinned smoke、GitHub Release。远端 tag 的 peeled commit 必须等于 reviewed candidate；smoke 通过后才发布中文、非 draft、非 prerelease 的正式 Release，并核实 published/latest 和实际资产。
7. 发布后处理本轮已选的两个本地目标：调用 checkout 与保留主仓；实际路径在当前对话由发布 owner fresh-resolve 和展示，不写持久 workspace 映射，也不扩至 peer/worktree 或业务仓。通过原 tools owner 从完整干净 published source 做 `source_locked` 收敛及实际版本、provenance、CLI、managed assets、native-entry 验证；已经一致的目标只验证，不重复写入。
8. 本地安装或恢复未完成时保留已发布远端事实，由原 owner 恢复，不重复创建 tag/Release，不自动排除阻塞目标，不提前关闭 #808。全部责任完成后，回读 live Issue、远端发布及本地结果，单独审查关闭边界并确认关闭，再验证实际关闭状态。

Stage 2 继续使用私有合同的原 locator 和可执行入口，不以临时命令集合代替。最终分别报告远端事实、两个本地目标结果，以及其他 native host、完整多平台矩阵和真实业务升级的未验证边界。

## 6. 约束与依赖

- **C-01 来源前置**：#794 的实际完成、关闭、归档和 main 可达性是发布准备依赖。六项输入、source lock 或来源变化由原 owner 重判；不存在以版本字面相同免验来源的路径。
- **C-02 Markdown 与脚本**：AI 按原 Markdown 合同判断范围、充分性、发现、路由和 readiness；脚本只执行或校验确定性事实。本文不新增公共 I/O、独立审批链或空白通过结果。
- **C-03 规划边界**：本根 PRD 定义全部准备要求；原 Clarify 审查并发布 `accepted_scope` 后才进入显式 Delivery 创建及其独立规划。根 PRD 不创建 Delivery，也不承载根 design/implement/context。必要共享文档只能由原维护 owners 写入。
- **C-04 兼容与恢复**：#794 的旧 gate、early Draft 和原合法在途操作按完整匹配 provider 及原 owner 处置。普通源码同步不改 Task/session；不能通过伪造旧结果或新增备用正常路径接续。
- **C-05 副作用**：TaskCommit、push/PR、各次 merge、Finish/cleanup、tag、smoke、Release、每个本地 tools 更新和 Issue 关闭都保留各自原精确边界。每次 merge 前向 coordinator 展示并停止；其他副作用也按原 owner 展示精确方案后处理。授权仅在当前对话，不进入 tracked、runtime、schema、DTO 或 archive。
- **C-06 持久化与敏感数据**：不创建 task-local release-notes、PR/Release body handoff、动态 implement checklist、release-status commit 或发布 ledger。不持久化候选/发布逐步状态、过程证明或授权。保留 secret/credential redaction、权限和破坏性副作用边界。
- **C-07 验证范围**：只覆盖受支持的诚实正常路径、常见误操作、stale/mismatch 和正文明确的恢复。不增加攻击模型、故意伪造、竞态压力、TOCTOU、锁、fault injection 或累计完整矩阵要求。
- **C-08 生命周期责任**：Completion 审准备业务；Closure/Finish/Cleanup 各自验证后续终态。Stage 2 不进入本 Task Completion，Stage 1 终态也不表示 #808 已完成。没有业务 API、数据库或生产部署变化，本 Task 不新增相应迁移或部署验收。

## 7. 可观察验收与验证方式

以下均为待执行验收，不预填通过。AC-01 至 AC-07 是本 Task 的准备业务验收；AC-08 是其后由原生命周期 owners 消费的终态义务。

| AC | 对应要求/场景 | 验证入口与输入 | 可观察结果与证据边界 |
| --- | --- | --- | --- |
| AC-01 | R-01 / SC-01 | fresh-read live #808/#794、tags/Releases、canonical/installed manifest、CLI 和各自 source lock | 六项输入一致，前置可证明；占用、来源实质变化或身份不符回原 owner。版本和发布状态不混淆 |
| AC-02 | R-02 / SC-02 | 私有合同、四份发现副本、原 packages/interfaces 及受影响的真实调用/消费回归 | 新链承接完整职责，无独立重复 Check 或早期发布旁路；真实后继刷新、原合法在途恢复和私有排除分发成立 |
| AC-03 | R-03 / SC-02 | 原 Docs Plan、RDT/Architecture 目标完整单元、整合/readback 与公开文档 | 版本、行为、兼容和证据边界一致；必要关系无遗漏，历史不被重写，整合事实未冒充审核通过 |
| AC-04 | R-04 / SC-03 | 后继 D2 的原 tools owner source_locked 正常调用与实际目标读回 | 实际 dogfood revision 为 `.9`，完整受管内容与匹配来源/lock 一致；target resolver、installed/native entry 可用；Task/session/user config/peer/pointer 保留，无未解决冲突或 sidecar；完整 package/platform/workflow、parity 和 drift 验证成立。D1 来源交付或 throwaway 不替代此项 |
| AC-05 | R-02、R-04 / SC-04 | 每个实际 Delivery 的原工程自检、TaskCommit、固定完整 committed candidate、独立 Review | D1 全部来源、消费者与文档 after，以及 D2 全部最终安装和必要文档 after，分别进入各自完整实际候选；原 reviewer 完成全部适用职责，零开放 P0–P3 finding 后才进入各自 readiness；单个命令、fixture 或前一 slice 通过不替代语义审核 |
| AC-06 | R-05 / SC-04 | 每个实际 Delivery 的原 Delivery Review → Publication → Merge，目标 main、完整真实 PR payload 与 expected head | 每份中文 PR 如实说明当前 slice、验证、剩余责任和未验证边界，仅 Refs #808；各自审核/readiness 前无新 push/PR，实际 merge 与已审内容一致。D1 的 payload 不声明实际采用或 Task 完成 |
| AC-07 | R-05 / SC-05 | 原 Completion 对全部准备要求、所有 Delivery、当前来源与证据的审核 | 没有剩余准备业务义务或遗漏 slice；不借合并推导完成，不把 Stage 2 加为准备 Completion 前置，缺口返回原 owner |
| AC-08 | R-05 / SC-05 | Completion 之后原 Closure、acceptance-finish Architecture、Finish 与 Cleanup | Closure no_mutation；main 包含唯一终态归档及必要 bookkeeping；Cleanup 只处理原精确范围并保留 caller-owned 资源，#808 仍留给 Stage 2 正确关闭 |

R-06 的 candidate、发布、两个选定本地目标和最终 Issue 关闭验收由 Stage 2 owner 在自己的边界实际执行。本 Task 的业务、终态、测试或安装证据都不能预先宣布那些门禁通过。

当前 D1 分配 AC-01、AC-02、AC-03、AC-05、AC-06；其中 AC-03、AC-05、AC-06 按第3.3节承担当前来源 slice 的完整责任。AC-04 完整保留给同 Task 后继 D2；D2 同样必须满足自身 AC-05/06，并按实际来源 freshness 和文档差额承接 AC-01/03 的适用责任。原 Creation 建立 D2 时判断其实际 scope_ref，本文不预建 key 或执行选择。AC-07 要求所有 slice 及全部准备业务均满足，AC-08 和 Stage 2 不因顺序分配减少。

## 8. 实际未决项

整体准备范围和 Stage 2 责任边界没有待用户决定的需求问题。顺序分配及完整验收责任见第3.3、5.4、5.5和7节；它们不表示 D1 新 Planning 已形成或来源依赖已实际解决。原当前阶段 owner 修订同 D1 scope_ref 后，原 Delivery Author 刷新实际五份规划/context，重新进入受影响的独立 candidate assessment、Wording、final_plan assessment 和 Approval；原 Activation 之前仍不实施。

具体私有消费者迁移落点、必要 Docs Plan、D1 来源自身必需验证、D2 实际来源/构建取得及工程验证集合由后续原 Delivery Author/Architecture/Approval 在已明确约束内形成完整方案。若来源可分发性依赖尚未完成的实际采用，或发现不能由证据回答的来源/范围冲突，回原 Clarify/规划 owner。不能只改 Policy 标签、删一项验收或删除过期引用就宣布 GAP-SOURCE-01 解决。

若规划发现真实来源冲突、版本占用、规范性承诺变化或不能由证据回答的范围选择，回原 Clarify/来源 owner，并停止依赖该选择的工作。根正文通过原 Author 完整性判断后，只输出 `scope_requirements_ready`；原 Clarify 仍须审查实际正文并以真实 AuthorityRef 发布 `accepted_scope`。在此之前，正文存在不表示范围已接受，也不授予 Delivery 创建、激活、实现或发布。
