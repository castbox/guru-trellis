# #684 准备 v0.7.0-guru.7 正式发布：整体需求

## 1. 来源与术语

| 标识 | 来源与章节 | 角色 | 本 Task 用途 |
| --- | --- | --- | --- |
| SRC-684 | [castbox/guru-trellis#684](https://github.com/castbox/guru-trellis/issues/684)，完整正文，重点为“Stage 1：只负责准备的 Task” | 直接需求来源；本 Task 关系为 `reference_only` | 确定准备范围、版本、实际安装、独立审核及准备收尾；Stage 2 留在 release Issue |
| SRC-RELEASE | [.agents/skills/release-guru-trellis-version/references/contract.md](../../../.agents/skills/release-guru-trellis-version/references/contract.md)，`Two-Stage Lifecycle`、`Local Installation Convergence And Final Report`、`Independent Mutation Confirmations` | 已约定设计与流程约束 | 保留准备与发布分界、双完整 Review、原 tools owner 与独立副作用边界 |
| SRC-WORKFLOW | [.trellis/workflow.md](../../workflow.md)，当前全局路由和 continuation | 运行流程约束 | 使用 Task/Delivery、Author、Architecture、Check、Review、Completion、Closure、Finish、Cleanup 原 owners |
| SRC-VERSION | [trellis/guru-team-extension.json](../../../trellis/guru-team-extension.json)、[source lock](../../../trellis/presets/guru-team/source/trellis-source.json) 与 [README.md](../../../README.md#发布身份边界) | 当前事实与受影响定义 | 区分 repository tag、extension revision、CLI/source lock 及内部知识身份 |
| SRC-PREDECESSOR | [v0.7.0-guru.6 Release](https://github.com/castbox/guru-trellis/releases/tag/v0.7.0-guru.6)、[#656](https://github.com/castbox/guru-trellis/issues/656) | 已完成的历史发布事实 | 证明准备期稳定安装来源为已发布 `.6`；不继承其验证结论 |

Task 表示本次整体准备范围；Delivery 表示其经过独立规划的交付切片。准备 Task 完成不等于 release Issue 完成。`source_locked` 指原 `guru-upgrade-tools` 从完整、干净、已提交且与固定 Fork 构建匹配的来源执行 tools-only 更新。

## 2. 背景与问题

正式前驱 `v0.7.0-guru.6` 已发布。当前 canonical extension 仍为 `0.7.0-guru.6`，公开文档仍将 `.6` 描述为未发布的准备源码。正常读者会据此选择过期稳定来源，无法清楚区分本次 `.7` 候选与前驱。

当前固定 Fork 为 `castbox/Trellis@79a97ed60fe19e8f287eaddfa74722b5250ced35`，CLI/Core 为 `0.7.0-castbox.5`。该配对不因 Guru 发版而改变。已有 installed manifest 的版本字符串不能独立证明实际 tools 和来源正确；本 Task 必须通过原 tools owner 更新真实 dogfood。

#679 与 #666 已完成。#666 验证已有 #419/#657/#679 的因果及正常行为，没有新增源码修复。前序功能、旧 Release 或隔离样本不构成本次准备、实际安装或后续 exact-candidate 发布证明。

## 3. 目标与非目标

本 Task 完成 #684 Stage 1 的全部准备工作：将 canonical extension、maintenance target/const schema、必要断言和公开文档收敛到 `.7` 准备语义；通过原 owner 更新真实 dogfood 和受管投影；完成 Docs/Architecture/RDT 收敛、独立审核、Refs-only 准备交付及正常终态收尾。

整体 Completion 评审 R-01 至 R-06 的准备内容和 R-08 的适用证据规则。R-07 规定通过 Completion 后的生命周期收尾；后续 Closure、Finish 和 Cleanup 的结果不作为提前取得 Completion 的条件。

本 Task 不承担 Stage 2 的最终 candidate 冻结、正式发布最低门禁、tag、tag-pinned smoke、GitHub Release、发布后两个选定本地目标的最终收敛或 release Issue 关闭。这些是 #684 的后续责任，必须在准备交付与归档合并后重新取得证据。不能为使准备 Task 完成而删除或提前满足这些责任。

不实现其它 Issue，不修改上游源码、全局包或 `node_modules`，不转换历史 Task，不升级业务仓库或生产部署，不清理无关资源。完整累计多平台矩阵、所有 native-host、真实业务升级和 Himora 同因证明继续由各自 owner 承担。

## 4. 真实调用方、场景与流程

| 场景 | 调用方与前提 | 触发与行为 | 可观察结果 |
| --- | --- | --- | --- |
| SC-01 版本准备 | 发布 owner 已核定 #684 与已发布 `.6` | 进入正常准备流程，核对当前 canonical、文档、schema 与安装 | 唯一 `.7` 目标映射；稳定安装使用 `.6`，候选使用真实远端完整 SHA |
| SC-02 实际 dogfood 更新 | 完整匹配的 Guru 来源及 source-lock Fork 构建可用 | 原 tools owner 预览、prepare、执行 `source_locked` tools-only；若需干净来源，先走现有 early-commit/source-acquisition | 实际 installed extension、provenance、CLI、受管字节与来源一致；Task/archive/workspace/session/user config 保留 |
| SC-03 共享知识整合 | 已完成稳定 Delivery 规划与晋升前内容 | Phase 2、原提交、晋升前独立完整 Review；零开放 P0–P3 finding 后串行 Architecture/RDT promotion；晋升后再 Phase 2、原提交与第二次完整 Review | 两次审核各覆盖其完整 committed diff；晋升后实际字节未复核时不能进入发布准备 |
| SC-04 准备交付与收尾 | 晋升后完整 Review 通过 | Architecture publication check、Delivery Review、中文 Refs-only readiness、Publish、expected-head Merge；再评整体 Completion、Closure、Finish、Cleanup | 准备交付及唯一终态归档进入 main，精确资源收尾，#684 仍 Open |

失败、stale 或 output loss 返回原 owner 和同一操作。未知结果先回读；不能重复创建、提交、发布或合并，也不能另开修复支线代替当前 Task。

## 5. 行为要求

**R-01 版本映射（SC-01）**：repository 目标为 `v0.7.0-guru.7`，canonical/maintenance extension revision 为 `0.7.0-guru.7`。CLI/Core 保持 `0.7.0-castbox.5`，固定 Fork/source lock 保持当前配对。`.trellis/.version` 记录 CLI，不写 Guru revision。内部知识身份沿当前稳定规则维护，不因软件发版强制新增知识版本。

**R-02 公开来源与投影（SC-01）**：修正 README、workflow/preset README、canonical public-docs 的过期发布表述和准备期来源。稳定安装使用已发布 `.6`；workflow marketplace 与 preset 使用同一 immutable 来源。试用候选必须使用同一真实、远端可寻址完整 SHA 及其自身 lock 的匹配构建。`.7` 尚未发布时不能把其 tag 当作可用 provider。保留历史事实和未验证边界。canonical 修改经既有 installer/overlay 机制同步 dogfood，检查 drift 和每个 sidecar，不能只改安装副本。

**R-03 真实安装（SC-02）**：通过原 `guru-upgrade-tools` 的 `source_locked` 路线更新本 Task 的实际 dogfood，并将实际 changed managed scripts、schema、projection 和安装 manifest 纳入准备候选。遵守原 owner 的只读预览、单次 prepare、实际执行和同操作恢复；不以手改 manifest、旧版本号、validator 或 throwaway 成功替代真实安装。保留历史 Task 与用户状态，不绕过 guard。合法已提交等价来源按私有合同验证，不制造自引用 HEAD 状态提交。

**R-04 稳定规划与双审核（SC-03）**：整体范围由本 PRD 承载；所选 Delivery 在实际 `planning_root` 完成稳定 `prd.md`、`design.md`、`implement.md` 和 Docs SSOT Plan。原 `guru-create-task-commit` 独占每次提交。晋升前和晋升后分别执行 Phase 2、原提交与独立完整 Branch Review；每次 Review 覆盖完整 `origin/<base>...HEAD`，零开放 P0–P3 finding 后才前进。前一次结果不能覆盖 promotion-created bytes。

**R-05 串行知识收敛（SC-03）**：Architecture 与 RDT promotion 只由原 owner 在晋升前完整 Review 之后串行执行，纳入实际贡献、完整拟写正文和当前 authority。晋升后重新绑定候选并执行受影响门禁。不得从准备状态、脚本成功或旧证据推断 shared-current 或 semantic pass。

**R-06 Refs-only 交付（SC-04）**：原 Delivery Review 审核当前切片与剩余发布责任，生成中文、真实的 `Refs #684` PR title/body，不带关闭关键词。原 Publish 承接精确 push/PR/Ready，原 Merge 执行独立确认的 expected-head 合并。内容或 authority 改变返回受影响原 owner；结果未知优先同操作恢复。

**R-07 整体准备收尾（SC-04）**：Completion 评审本 Task 全部准备要求及全部 Delivery/evidence，不能只凭某 PR 合并。Closure 对 `reference_only` 返回 `no_mutation`。acceptance-finish Architecture check 后，原 Finish 分别完成归档、bookkeeping 发布与 expected-head 合并，再由原 Cleanup 审核精确资源。准备收尾不能关闭 #684，也不能宣称 Stage 2 通过。

**R-08 证据与交互（全部场景）**：每个 Git/GitHub、tools、Finish 和 Cleanup 副作用按原合同 fresh 展示精确对象并取得对应当前确认。授权及过程不写入任何 artifact、runtime、schema、DTO 或归档。不创建 task-local release notes、PR/Release body handoff、动态 checklist、release-status commit 或发布协调 ledger。`implement.md` 保持稳定计划。Gate 由 AI 实际审查，recorder/checker 仅记录或校验客观事实。

## 6. 约束与依赖

- 保留 Markdown 流程与 AI 判断、确定性脚本执行的边界；公共 API、Skill id、typed exits 和 source lock 未授权变化不得静默改义。
- 采用完整 matching workflow、preset/runtime 与声明平台投影。tools 所需完整干净来源和匹配 Fork 构建是实际更新的前提；缺失时停在原 owner，不能用其它 checkout 的结果代替。
- 历史 Task 保持原数据。普通 full reapply 的历史数据 guard 不授权转换或绕过。Stage 2 的 Historical-Task Preflight Observation 不替代本 Task 的真实 dogfood 更新。
- 采用足以证明准备 accepted scope 的定向验证。Stage 2 的完整 predecessor diff、focused/existing 安装、前驱清退、真实 secret scan、residue、独立候选 review 和后续真实本地收敛仍由发布 owner fresh 执行，本 Task 不预填通过。
- 保留当前知识 authority 的稳定 identity；源、完整正文、贡献与关联由原 Architecture/RDT owner 读取和维护。无需新增业务 API、数据库字段或数据迁移。

## 7. 可观察验收与验证方式

| 验收 | 对应要求/场景 | 验证入口与输入 | 预期可观察结果及边界 |
| --- | --- | --- | --- |
| AC-01 | R-01/R-02；SC-01 | 读取本准备候选的 canonical manifest、maintenance schema、公开 README/public-docs、CLI record 与 source lock | `.7` 目标、`.6` 稳定来源与 `.5` CLI 各有唯一含义，历史范围保留；不声称 `.7` 已发布 |
| AC-02 | R-02/R-03；SC-01/02 | 原 source/installed validators、声明平台 parity、ownership、installer/overlay reapply、drift 与 sidecar 检查 | canonical 与实际受管投影一致；无未处置 sidecar。按实际层次报告源码、安装和 native 结果 |
| AC-03 | R-03；SC-02 | 原 tools owner 在真实 dogfood 上执行并回读版本、来源、CLI、managed assets 和其要求的 native entry | 实际安装满足 target revision，来源与 lock 可证明；Task/archive/workspace/session/user config 保留。throwaway 不替代本结果 |
| AC-04 | R-04/R-05；SC-03 | 原 Check、TaskCommit、独立 Branch Review 与串行 Architecture/RDT owners | 晋升前后分别得到当前完整范围结果，零开放 P0–P3 finding；晋升字节纳入最终 Check/commit/Review |
| AC-05 | R-06；SC-04 | 当前 Architecture publication、Delivery Review/readiness、Publish、expected-head Merge | 真实中文 Refs-only 准备 PR 合入 main，完整记录实际验证与剩余责任，不自动关闭 #684 |
| AC-06 | R-07/R-08；SC-04 | 先由整体 Completion 评审准备内容，之后依次由 Closure、acceptance-finish Architecture、Finish 与精确 Cleanup 承接 | Completion 后 Closure=no_mutation、唯一终态归档被 main 包含、精确资源收尾；这些后续结果不前置到 Completion；#684 的 Stage 2 仍由原发布 owner 承接 |

本表定义待执行验收。文件存在、预检 ready、创建成功、旧功能验证、旧 Release 或历史 Gate 均不代表上述验收通过。

## 8. 实际未决项

当前没有阻塞整体需求写作的产品或范围选择。具体版本 surfaces、source-acquisition/early-commit 顺序、知识贡献与定向命令由所选 Delivery 的 Author 和独立 Architecture owner 从当前文件细化。

完整干净匹配来源、实际 tools 更新、native entry 与受影响测试尚待执行；其结果决定对应实施门禁，不是可以省略的准备责任。Stage 2 发布及两个选定本地目标的最终收敛不属于本 Task Completion，仍保留为 #684 的后续义务。
