# #861 准备 v0.7.0-guru.10 正式发布：整体需求

## 1. 来源与术语

| 标识 | 来源及章节 | 角色 | 本 Task 用途 |
| --- | --- | --- | --- |
| S1 | https://github.com/castbox/guru-trellis/issues/861 ，完整正文 | 要求 | 无其它 Issue 前置、最新 main、准备与正式发布边界 |
| S2 | `.agents/skills/release-guru-trellis-version/references/contract.md`：Stage 1、Complete Source Before Actual Adoption、Whole Preparation Completion | 约定设计 | 准备交付、真实采用、reference-only Closure 与 Finish |
| S3 | 同一合同：Stage 2、Local Installation Convergence、Independent Mutation Confirmations | 约束 | Task 外正式发布和本地收尾的直接后继职责 |
| S4 | `.trellis/workflow.md`：Phase 1、Phase 2、Phase 3 | 约定设计 | 原 Author、Architecture、Approval、提交和交付 owner 顺序 |
| S5 | `trellis/guru-team-extension.json`；`trellis/presets/guru-team/source/trellis-source.json`；`.trellis/.version` | 当前事实 | 区分 Guru 版本和 Fork CLI/source lock |
| S6 | `README.md`；`trellis/workflows/guru-team/README.md`；`trellis/presets/guru-team/README.md` | 当前事实 | 正式安装入口、同源 ref 和版本说明 |
| S7 | `trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`；`verify_trellis_compatibility_matrix.py`；`verify_native_platform_load.py`（后两者同目录） | 失败证据及当前实现 | Stage 2 已确认的退役测试、AGENTS 替换及平台选择消费者缺口 |
| S8 | `trellis/presets/guru-team/scripts/python/test_verify_trellis_upgrade_contract.py:NormalPhase0AuthoringTests`；同目录 `verify_installed_phase0_transcript.py:clarification_owner_for_issue` | 当前代码与正常失败证据 | 当前 helper 的 owner envelope 与既有测试消费不一致 |
| S9 | `trellis/skills/guru-team/packages/guru-discover-change-context/{commands.json,interface.json,runtime/issue_review.py}`；该包 context-request 2.0 与 supplement 1.0 schema | 当前公开合同与正常复现 | 四个命令帮助的 context-request 引用过期；supplement 1.0 仍是当前合法合同 |

“准备完成”表示本 Task 的全部交付及收尾完成；不表示 tag、smoke 或 Release 已完成。“真实采用”指原 tools owner 对准备 checkout 完成 `source_locked` 更新并验证；临时安装不替代它。正式发布后的本地目标仅为保留主目录 `/Users/wumengye/Documents/GoProjects/guru-trellis`，由 Stage 2 处理。

## 2. 背景与问题

首次准备开始时，正式版本及 canonical extension 均为 `0.7.0-guru.9`。原准备已将 canonical extension 更新为 `0.7.0-guru.10`，正式前驱仍为 `v0.7.0-guru.9`。已合入 main 的后继变更尚未通过下一正式版本提供给安装者。下一正式 tag 与 extension revision 采用 `v0.7.0-guru.10` / `0.7.0-guru.10`。执行相关写入前重新核实占用，不覆盖已有 tag。

固定 Fork 的 CLI 为 `0.7.0-castbox.6`。本次 Guru 发版不单独提升 Fork 版本；复核 manifest、lock、实际构建和 CLI 记录的一致性。版本说明与实际安装必须共同准备，不能只改版本号或用验证器通过代替真实采用。

gen0 准备的两次交付已分别合入 PR #865、#866，终态簿记经 PR #867 合入 main。随后 Stage 2 完整候选审核确认两个 P2：installer 测试仍要求退役 Wording 资产；合法 AGENTS 受管区块替换被前驱升级验证器误判为 template-hash drift。实际 Claude focused 安装还暴露平台检查器错误要求两个 Codex-only Skills。gen1 后继准备修复这三个必要消费者，并收敛原真实安装验收发现的 current input schema inventory 差额。当时 canonical manifest 比42个 active Interface 的有效 JSON input 声明多11项历史输入，typed output 集合无差额。原交付及其终态结论保留历史身份，不作为修复或新候选通过证据。

上述 gen1 准备已通过 PR #871、#875 交付，终态簿记 PR #876 合并。其后从最新 main 冻结的 `5dc0708a1d817fb9fb02edb64419b7b3c3f7cc10` 完整发布审核确认两项后继缺陷：Phase 0 authoring helper 已使用 `{owner_result, owner_context}`，现有测试仍按 flat owner 读取，四例中一例报 `KeyError: review_target`；Discovery runtime/Interface 的 context_request 已采用 input 2.0，而四个命令的帮助仍引用 closed input 1.0，按该声明装配的正常输入与实际入口不一致。该包自己的 issue_readiness_supplement 仍采用合法 input 1.0，不能与 Clarify 同名 profile 的 2.0 混用。gen2 只修复这两项及其直接回归、分发和实际采用责任。前一候选的其余工程结果保留原身份，不作为新候选发布通过证明。

## 3. 目标与非目标

本 Task 完成 Stage 1：可分发的完整目标版本源、公开说明、受管投影、适用知识整合、准备 checkout 的真实 tools 采用，以及完整交付和终态收尾。没有其它 Issue 的完成、关闭、合并或归档前置。

本 Task 不创建最终发布候选、tag 或 GitHub Release，不执行 tag-pinned smoke，不关闭 #861，不升级业务仓库或部署生产，不清理其它 Task、分支或 worktree。准备 PR 和 Finish bookkeeping PR 均使用 `Refs #861`，不产生 Issue 关闭效果。

## 4. 真实调用方、场景与流程

| 场景 | 调用方、条件与触发 | 行为 | 可观察结果 |
| --- | --- | --- | --- |
| SC1 | 发布 owner 从最新 main 开始准备 | 原流程规划并交付完整目标版本源 | 目标版本的 manifest、公开安装入口、可分发资产和适用验证相符 |
| SC2 | 完整干净源已经实际交付，准备 checkout 需要采用 | 原 tools owner 使用该完整匹配源执行 source_locked | 真实 installed 内容、provenance、CLI、lock、平台入口得到验证 |
| SC3 | 准备整体范围全部满足 | 原 Completion、reference-only Closure 和 Finish 执行收尾 | Task 正常终态，终态归档进入 main，#861 保持开放 |
| SC4 | Stage 2 接续准备结果 | 发布 owner 重新读取届时最新 main 并冻结候选 | 准备分支的审查结果不被当作最终候选发布 pass |
| SC5 | Stage 2 的正常验证发现必要消费者缺陷 | 同一 Task 的后继 Delivery 修复消费者，经原完整交付及 Task 收尾后返回 Stage 2 | 修复实际进入 main；最终候选重新冻结，受影响门禁使用新内容验证 |

## 5. 行为要求

- **R1 版本与来源**：目标 Guru tag/revision、前驱、Fork CLI 和 source lock 保持各自含义。workflow 与 preset 的正式或候选安装入口使用同一 immutable 来源。尚未正式发布的版本说明保留真实执行条件。
- **R2 完整可分发源**：收敛目标版本的 canonical manifest、直接版本消费者、公开说明和必要兼容迁移说明。原维护 owner 处理真实命中的 Requirements/Design/Test 和 Architecture 单元；不追加无消费方的 release ledger 或全局版本登记。
- **R3 交付顺序**：准备使用同一 Task。D1 先独立交付完整可分发源及其验证；D1 的完整性不能依赖 D2 已执行。D1 实际 delivered 后，原 Completion 对尚未实施的采用返回 additional_delivery_required，原路由才建立并规划 D2。不得提前创建 D2 或把采用缺口记作仅待补证据。
- **R4 真实采用**：D2 从 D1 实际交付的完整干净匹配源，经原 tools owner 完成准备 checkout 的 source_locked 更新。验证 installed extension、完整受管内容、平台投影、真实来源、CLI、source lock、native entry、可执行位和 sidecar。保留 Task、archive、workspace、session、用户配置、peer tools 和 common runtime。
- **R5 定向验证**：每个 Delivery 按其独立承诺完成 source/package、声明平台投影、安装或 reapply/drift、兼容直接消费者和真实采用所需验证。临时安装证明源行为，不证明准备 checkout 已采用。不自动扩张为累计多平台 Release Gate 矩阵。Stage 2 的最终候选门禁由其 owner 重新执行。
- **R6 全部准备收尾**：每个 Delivery 通过当前原 Author、Architecture、Approval、工程检查、知识整合、TaskCommit、一次独立完整 Check/Branch Review、Delivery Review、Publication 和 Merge。整体 Completion 覆盖所有准备责任；Closure 为 no_mutation；Finish 将精确终态归档及簿记合入 main。资源清理由原 owner 单独审查。
- **R7 后继与失败**：Stage 2 在准备及簿记合并后获取最新 main，冻结唯一 candidate commit/tree，并按 #861 在发布副作用前复核推进。准备阶段的失败、stale、内容变化或来源不匹配返回原 owner，保留真实失败及未验证边界。后续 tag、smoke、Release、主目录安装和 Issue 关闭保留各自确认边界。
- **R8 退役消费者**：原 installer 测试及其 manifest/inventory 断言必须承接 Wording 退役：验证退役产物缺席及当前合法合同，不恢复已退役生产资产。保留受支持的用户修改保护行为及必要后继职责。
- **R9 AGENTS 受管更新**：前驱升级及 clean/reapply 验证必须接受原 installer 对既有 AI-first 区块的合法替换，精确核对原正文到目标正文的受管变换，并保持区块外用户正文。不得更改 template hash、忽略未知漂移或跳过失败门禁以获得通过。
- **R10 平台预期集合**：native projection 检查必须按当前选择的平台、投影 root 与 registry 的 `supported_platforms` 合同计算必需集合。Claude/Cursor 不要求 Codex-only Skills；Codex 仍要求它们。实际必需 Skill 缺失、非预期投影或私有测试泄漏仍按既有合同报错。

- **R11 当前清单与采用**：canonical `public_api.skill_contracts.public_input_schema_ids` 精确承接 active Interface 的当前结构化输入；保留 instruction-only 不贡献 JSON I/O、历史 schema 文件及原固定 provider 恢复边界，不将历史 schema 继续宣告为当前可调用输入。核清并纠正11项旧登记，提供明确兼容迁移说明，同批适配真实安装测试及直接能力消费者。修改可分发 manifest 后，原准备 checkout 必须通过原 `guru-upgrade-tools(source_locked)` 从本批已交付的完整干净源实际采用；该采用依赖前一批实际 delivered，在同Task的后继独立Delivery执行。不得手改installed清单或用临时安装替代真实采用。

- **R12 Phase 0 envelope 消费**：既有 authoring 回归必须消费当前 `{owner_result, owner_context}`，继续检查 owner 不预填 recorder 派生字段、duplicate 事实来自原输入、checker 接收同一 recorded owner 及匹配来源上下文。不得恢复旧生产 shape、删去原绑定断言或用 mock 自证代替实际 helper 执行。
- **R13 Discovery 命令输入合同**：record、check、invoke、read-source 四个既有命令的 context_request 声明改为 runtime/Interface 已采用的 2.0；该包 issue_readiness_supplement 的当前合法 1.0 引用保持。context_request 的正常 review_focus 与返回身份，以及 supplement 1.0 原有 profile/mode/issue/base_source/continuation_id/source_exit/gap 形状，分别能按公开帮助进入原验证入口。保留历史 schema 文件与原固定 provider 恢复边界，不新增 profile/schema/API、不改变实际业务路由。修复后的受管投影及真实准备 checkout 采用按 R3–R5 的有序责任完成。

## 6. 约束与依赖

复用当前 Markdown workflow、私有发布合同和原公共 Skill API；不修改上游或全局包，不模拟审批链，不写共享 journal，不持久化授权。当前流程没有默认独立 Wording 关卡；表达和语义保持由原写作、审核 owner 在其职责内完成。

D2 只依赖本 Task 内实际完成的 D1 完整源交付。这不是对其它 Issue 的状态依赖。真实工具采用、版本来源或安装冲突不能由临时测试替代。历史 Task guard 不授权转换历史数据、普通 apply 绕过或手工覆盖受管文件。

准备 checkout 的采用属于本 Task；正式发布后保留主目录的安装收敛属于 Stage 2。两者的目标、来源和证据分别核实，不互相代替。

后继修复复用原 canonical installer、平台选择及验证入口，不新增公共 Skill、schema、发布状态或持久校验账本。gen1 源切片已同批包含验证器/测试、必要 canonical manifest 清单修复和明确兼容说明。后继分发改变触发的真实 source_locked 采用仍属于同 Task 剩余责任，由完整源切片实际交付后原 Completion/Creation 分配，不预建或选中第二 Delivery。正常用户正文变化、受支持平台选择及真实前驱升级属于验证范围；不扩张到对抗输入或累计完整矩阵。

gen2 的完整源切片覆盖 R12–R13 及其适用 R1–R7：只迁移测试断言、修正现有命令 schema 引用并补足必要正常回归。Guru 目标仍为尚未正式发布的 `.10`，Fork lock/CLI 不变。实际准备 checkout 的 tools 采用不能从 dirty 或未交付源启动；D1 delivered 后才由 Completion/Creation 分配 D2。主目录仍是正式发布后唯一最终本地安装目标，本准备切片不将它变为工具采用目标。

## 7. 可观察验收与验证方式

| 验收 | 对应要求/场景 | 入口与预期结果 | 证据边界 |
| --- | --- | --- | --- |
| AC1 | R1–R2 / SC1 | 检查完整目标源、公开入口和版本映射；目标版本及同源安装规则一致 | 不声称远端正式 Release 已存在 |
| AC2 | R3 / SC1–SC2 | 读取实际 Delivery 事实；D1 独立 delivered 后才分配 D2 | 计划、单次提交或验证器不等于 delivered |
| AC3 | R4–R5 / SC2 | 原 tools owner 在真实准备 checkout 执行并验证 source_locked；实际资产、来源和 CLI/lock 相符，无未处理 sidecar | throwaway 只覆盖其明确测试层 |
| AC4 | R5–R6 / SC1–SC3 | 各 Delivery 原阶段输出和适用验证覆盖完整承诺；Task Completion 覆盖全部准备责任 | 不复用失效或跨候选 pass |
| AC5 | R6–R7 / SC3–SC4 | main 包含准备交付及精确终态归档；Closure no_mutation，#861 保持开放 | 最终候选发布门禁、本地发布后收尾仍待 Stage 2 |
| AC6 | R8 / SC5 | 原两个 installer 测试及受影响消费者回归执行真实安装入口；退役资产缺席、当前合同及用户修改保护相符 | 测试更新不恢复生产资产，不把 fixture 自证当安装结果 |
| AC7 | R9 / SC5 | 受管区块替换回归验证旧正文到新正文及区块外保留；真实 `.9` 前驱 existing 原入口完成其完整校验 | `tools_upgraded` 单独不能代替 existing 验证通过；原失败输出保留 |
| AC8 | R10 / SC5 | 混合 shared/Codex-only registry 的定向回归，以及 Claude/Cursor clean/update/reapply 原入口覆盖平台集合 | 投影检查不声称真实客户端 Agent 或生产行为通过；三平台替代证据仍须最终发布 owner 审查 |
| AC9 | R11 / SC5 | 原真实安装测试对current JSON input/output与active Interface作exact比较，11项旧登记退出current但历史schema保持；本批delivered后，后继采用Delivery从完整干净交付源验证实际source_locked及全量受管内容 | 当前输入支持范围不新增，历史恢复不混装；完整existing在新源实际采用后、Whole Completion前完成 |
| AC10 | R12 / SC5 | 执行现有 `NormalPhase0AuthoringTests`；实际 helper 调用的 recorder/checker envelope 能完成派生字段与来源绑定断言，四例无该 KeyError | 测试适配不证明真实 GitHub 或客户端 Agent 流程完成 |
| AC11 | R13 / SC5 | 从四个实际命令帮助取得 current 声明，使用两个受支持 profile 的正常输入验证与 runtime/Interface 一致；完整 source/临时 installed 投影无旧 current 声明，后继实际采用验证同一合同 | 不恢复历史 schema 为 current；临时安装不替代准备 checkout 的实际采用 |

## 8. 实际未决项

没有阻塞整体准备需求的未决产品选择。R8–R11 保留其原交付及历史结果；gen2 当前完整源切片承担 R12–R13 和适用的 R1–R7，实际采用作为其有序后继责任，不提前创建 D2，也不将必要修复延期到发布后。各 Delivery 的实际文件集合、验证命令、Docs 策略和 Architecture 承接由原规划 owner 在相应切片展开；它们不降低以上整体责任。正式发布候选和发布结果只在 Stage 2 从 live main 与真实结果取得，不在本文件预填。
