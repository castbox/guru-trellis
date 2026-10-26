# v0.7.0-guru.6 发布准备：整体需求

## 1. 来源与术语

| 来源 | 章节与角色 | 本 Task 用途 |
| --- | --- | --- |
| https://github.com/castbox/guru-trellis/issues/656 | 全文；Direct Source，reference_only | 版本、来源、准备范围、验收及两阶段发布边界 |
| .agents/skills/release-guru-trellis-version/references/contract.md | Stage 1、Stage 2、Reviewed-Content Freshness、Forbidden Persistence、Independent Mutation Confirmations；约定设计约束 | 准备执行顺序、原 owner、证据有效性和独立副作用边界 |
| trellis/guru-team-extension.json；trellis/presets/guru-team/source/trellis-source.json | 当前 canonical 事实 | 独立核对 Guru revision、Fork CLI/Core 和固定源码 |
| docs/requirements/README.md；docs/design/README.md；docs/test/README.md；docs/architecture/README.md | 当前知识导航与约束 | 由原维护 owners 读取完整适用单元并收敛本次版本事实 |
| https://github.com/castbox/guru-trellis/issues/669；trellis/presets/guru-team/MIGRATION-669.md；docs/requirements-design-test-contributions/669-existing-implementation-reactivation/test.md | 已完成依赖、当前合同与有界证据 | 将已有实现恢复能力纳入实际累计发布集合，保留其验证限制 |
| https://github.com/castbox/guru-trellis/issues/649；docs/requirements-design-test-contributions/649-stage-result-convergence/test.md | 已完成依赖及历史证据 | 保留 false/no-grade、历史失败和验证边界，不重复实现或清理原资源 |
| trellis/skills/guru-team/packages/guru-upgrade-tools/references/contract.md | Forward behavior 第4步；约定设计约束 | verifier 必须向原 tools owner 提供唯一的 AGENTS.md custom decision，保留实际 source snapshot 与已审查正文 |
| trellis/presets/guru-team/scripts/python/verify_trellis_compatibility_matrix.py；test_verify_trellis_upgrade_contract.py | `_upgrade_native_bootstrap_tools` 及其现有合同测试；当前实现事实 | 定位 existing 验证入口的输入遗漏及本轮必要回归 |
| 当前构建要求 | 使用新版 pnpm，不锁定执行版本；复用 Trellis 本地 checkout | 区分源码声明与实际执行工具，避免新增 clone |

本 Task 只承担私有发布合同的 Stage 1 准备。repository tag、extension revision、Fork CLI/Core 与知识 identity 是独立版本轴。最终发布集合由已发布前驱至最终候选的实际完整 diff 决定，不能只用 Issue 摘要列举代替。

## 2. 背景与问题

已发布前驱为 v0.7.0-guru.5。初始准备需要将 canonical extension、maintenance target 和公开文档收敛到 0.7.0-guru.6；既有准备交付已经处理这一差额。本 Task 保留这些整体要求与历史交付，本轮增量不重复实现版本准备。

真实前驱的 stable existing 验证在 tools prepare 阶段失败。`_upgrade_native_bootstrap_tools` 只为 optional conflict 生成 preserve decision；当 preview 将 AGENTS.md 标为 unchanged 时，caller 完全遗漏该文件。现有 tools owner 要求唯一的显式 AGENTS.md custom decision，因此在 public prepare 和写入前返回 schema_mismatch。本轮修复该 caller，使原稳定验证入口能够继续执行；原失败观察保留，修复与准备验证不代替最终候选发布门禁。

累计集合包含 #669 的独立已有实现恢复入口及其知识和分发变化。该 Issue 的交付与正常归档不证明 Backend 生产恢复，也不证明本次 Release。#649 已完成；#656 中仍称其未完成的旧句不产生重新实现责任，历史失败样本和边界继续保留。

## 3. 目标与非目标

整体目标是完成可独立合并的 reference-only 发布准备，随后由原 Completion、Closure、Finish 和 Cleanup 正常收尾。准备交付和收尾 PR 使用 Refs #656，不包含关闭关键词。

范围包括 extension revision、maintenance target 与对应 const schema、公开安装/升级/发布文档、必要断言、managed 投影及 Docs/Architecture/RDT 收敛。本轮另包含 existing verifier 对既有 AGENTS custom 合同的 caller 适配及必要验证。

本 Task 不承担 Stage 2 的最终 candidate 验证、tag、tag-pinned smoke、GitHub Release 或发布 Issue 关闭。这些工作由 #656 在准备交付和 Finish bookkeeping 合并后独立承担。不实现其它 Issue，不修改 Fork、Backend 或业务安装，不做生产部署，不清理 #649、#651、PR #650 或其它无关资源。不扩张完整累计多平台/native-host、真实业务升级与原始在途任务、生产或 live 模型矩阵。

## 4. 真实调用方、场景与流程

| 场景 | 调用方、前置条件 | 触发与处理 | 可观察结果 |
| --- | --- | --- | --- |
| S1 版本准备 | 发布维护 Agent；读取 live #656 与各自固定树的 manifest/lock | 更新 Guru revision、maintenance target 和当前 const，保留 Fork 轴 | 当前交付一致声明 Guru .6，CLI/Core 和固定源码不因发版改变 |
| S2 安装说明 | 使用公开 README 的安装/升级调用方 | 区分已发布前驱、未发布候选与历史来源 | 稳定来源使用同一 .5 tag；候选 workflow/preset 使用同一真实完整远端 SHA及其自身匹配构建 |
| S3 知识收敛 | 原 Architecture/RDT owners；完整隔离候选已形成 | 晋升前 Check、commit、独立完整 Review 后串行整合；实际变更重新 Check、commit 和完整 Review | 规范正文与交付一致，晋升前结果不代替晋升后结果 |
| S4 准备收尾 | 原 Delivery、Completion、Closure、Finish、Cleanup owners | 审核并合并准备切片，再完成整体准备范围判断和正常归档 | Closure 对 #656 为 no_mutation，准备完成不宣称 Release 完成 |
| S5 变化与恢复 | 原受影响 owner；实际内容或来源变化、普通失败或输出丢失 | 重读 live authority，按原合同恢复或刷新受影响门禁 | 不重复创建身份，不沿用 stale/cross-SHA pass，不新增发布状态账本 |
| S6 existing caller 维护 | 原 release verifier；真实前驱、匹配的当前和前驱本地 Fork 构建、固定 init fixture | preview 后，无论 AGENTS.md 为 unchanged 或 conflict，都传唯一 custom decision；原 owner render、prepare 一次、冻结计划，再执行原 invoke | 输入满足现有合同，保留其它 optional conflict 的 preserve 决策；完整 existing 入口继续完成 maintenance、reapply、退休资产与终态检查 |

## 5. 行为要求

- R1 / S1：repository 目标 tag 为 v0.7.0-guru.6，extension revision 为 0.7.0-guru.6。保持 Fork castbox/Trellis@79a97ed60fe19e8f287eaddfa74722b5250ced35、CLI/Core 0.7.0-castbox.5。前驱 .5 自身为 Fork 7bcbeaad31380e7a29c97898cb947c6120a61775 / CLI-Core 0.7.0-castbox.4，不能与候选错配。源码的 packageManager 声明不是本次 pnpm 执行版本约束；实际构建按 R10 使用新版 pnpm。
- R2 / S1：maintenance target、对应 public output/consumer const schema、必要当前示例及断言与 canonical revision 同步。只更新真正的 current target；历史 fixture、归档、原始验证来源不批量替换。
- R3 / S2：同步 README.md、trellis/workflows/guru-team/README.md、trellis/presets/guru-team/README.md 和 canonical public-docs，再由既有 installer/preset 同步 dogfood。准备期稳定 provider 仍为已发布 .5，同次 workflow 与 preset 同一 immutable ref。未发布 .6 不作为可用 provider；只有发布并核验远端 tag identity 后才可作为新稳定来源。
- R4 / S2：当前知识入口使用 guru-trellis-rdt 和 guru-trellis-architecture，按当前导航与完整 Git revision/locator读取。由原维护 owners 判断贡献与最终整合，不因软件发版强制增知识版本或改写历史。公开说明覆盖真实累计集合，保留 #630、#649、#669 各自失败、未验证和实际验证层次。
- R5 / S3：稳定 Delivery prd/design/implement 与唯一 Docs SSOT Plan 完成后，执行晋升前实现及完整 Phase 2。由 guru-create-task-commit 提交，再由 guru-review-branch 独立审核完整 origin/main...HEAD；零开放 P0–P3 后才串行 Architecture/RDT 最终整合。晋升产生的实际变更重新 Phase 2、Task Commit 和独立完整 Branch Review。两个 Review 不能互相代替。
- R6 / S4：当前 Architecture publication check 和 Delivery Review 通过后，由原 Publish/Merge owners 完成 Refs-only PR 和 expected-head 合并。Completion 只判断整体准备范围；其 completed 才进入 Closure no_mutation。acceptance-finish Architecture 后，原 Finish 分别处理归档、bookkeeping 发布和合并，随后由 Cleanup 独立处置本 Task 精确资源。
- R7 / S3–S5：实际交付、公开文档、配置、schema、脚本或测试变化，刷新原受影响门禁。确定性 recorder/checker 只证明客观条件，不能代替语义通过。FAIL、SKIP、stale、cross-SHA 或身份/出口不明按原 owner 停止，不以 metadata commit 修复证据。
- R8 / S5：不创建 task-local release notes、PR/Release body handoff、动态 checkbox checklist 或 tracked 发布进度。implement 保持稳定计划。用户授权只在当前对话，不写入任何 artifact、runtime、schema、DTO 或归档。每个 Git/GitHub 副作用由其原 owner 展示精确动作后独立确认。
- R9 / S6：verifier 从本次真实 preview 读取 AGENTS.md source snapshot，解码为本固定 fixture 的已审查 UTF-8 base content，生成唯一 `path=AGENTS.md, action=custom, source=<实际 snapshot>, content=<base>` decision。AGENTS.md 不再进入 optional conflict preserve 列表；其它路径仍按原规则 preserve。原 tools owner 继续核对 capability、在副本上更新 Guru block，并且只调用一次 public prepare；冻结计划、执行与恢复均沿原 owner，不修改 runtime/Fork、不复制 updater、不手改生成输入。该固定 init fixture 已存在 AGENTS.md，不新增缺失文件兼容分支。
- R10 / S6：复用当前和前驱的 Trellis 本地 checkout，保持各自 source lock 的 commit/tree 与 CLI/Core 一致；不另行 clone，不修改 Fork 源码、packageManager 或锁文件。构建使用当前新版 pnpm，例如 `pnpm with current run build`，不指定固定 pnpm 执行版本。验证 caller 的 unchanged 与 conflict 两条正常输入、唯一 decision、source/content 保留及原 compose 消费；使用真实本地 CLI 验证原 tools prepare/幂等/回滚，并从新空 work root 重跑完整 stable existing 入口。prepare 通过不能单独作为完整 existing 成功。

## 6. 约束与依赖

Markdown 定义流程和 AI 判断；脚本只执行、记录或验证明确事实。保持既有公共 Skill/profile/exit 的职责和兼容边界，不为版本准备发明额外 workflow 或发布状态机。

准备验证执行 accepted scope 所需的最小可靠集合：相关 maintenance/const 定向测试、source/installed validators、Shared/Codex/Claude/Cursor 与私有发布 skill parity、ownership、三平台 reapply、dogfood drift、sidecar 和 diff hygiene。具体命令与直接证据由 Delivery 规划及原 Check owner 承接。

本轮 caller 修复只改变验证脚本与现有合同测试，不新增公共 Skill I/O、schema、数据字段或迁移。本轮沿用既有 tools owner 与完整 existing 入口；缺失构建、远端来源或运行依赖时，报告具体缺口，不以单元测试代替真实入口。既有准备要求只按实际依赖检查，不为两文件修复重复运行无关完整矩阵。

Stage 2 必须在准备和终态归档合并后，从 fresh main 冻结同一 clean candidate commit/tree，依私有合同稳定入口重跑前驱 ancestry/完整 diff、版本文案、source/installed/parity、ownership/reapply/drift、匹配锁的干净 Fork 构建、Codex focused 与真实前驱 existing upgrade、退休资产/冲突、真实 scanner 和 residue，并独立完整语义审核。专项或准备 pass 不转为这些门禁通过。全部通过后才分别确认 tag、smoke、中文 stable Release 和 Issue 关闭。

## 7. 可观察验收与验证方式

| 验收 | 要求与场景 | 输入和验证入口 | 预期结果 |
| --- | --- | --- | --- |
| AC1 | R1/R2；S1 | 当前 canonical manifest、maintenance owner 与 output/consumer schema、定向验证 | Guru revision/target/const 一致为 .6；固定 Fork/CLI 不变，前驱映射独立准确；pnpm 执行遵守 R10 |
| AC2 | R3/R4；S2 | 三份 README、canonical public-docs、当前知识完整单元和必要历史证据 | 前驱/候选/历史来源无错配；准备不将未发布 .6当provider；证据限制没有被泛化为通过 |
| AC3 | R2/R3；S1/S2 | 原 preset 三平台 reapply、source/installed/parity、ownership、drift 和 sidecar检查 | canonical/dogfood/声明平台一致；无未解决冲突或 .new/.bak，用户内容按原机制保留 |
| AC4 | R4/R5/R7；S3/S5 | 晋升前后完整候选及原 Check、TaskCommit、独立 Branch Review | 两轮覆盖各自完整内容；零开放P0–P3才继续；原Architecture/RDT完成实际整合，变化按实际依赖刷新 |
| AC5 | R6；S4 | 原 Delivery、Completion、Closure、acceptance-finish、Finish/Cleanup | 准备PR和收尾PR合并；准备Task正常终态归档；Closure no_mutation，精确资源由原owner处置 |
| AC6 | R7/R8；S5 | 完整Task差额与原owner的记录/恢复行为 | 无动态发布账本、body handoff或授权持久化；未执行Stage2不声称Release通过或关闭#656 |
| AC7 | R9；S6 | 现有 `test_native_bootstrap_tools_freezes_one_original_owner_plan`，真实 unchanged 与 conflict preview，以及原 compose consumer | 唯一 AGENTS custom 携带实际 source 与 base；其它 preserve 决策保留；prepare/invoke 各一次，不修改冻结计划 |
| AC8 | R9/R10；S6 | 原 `test_agents_target.py` 使用匹配本地 CLI；从新空 work root 运行 stable `--mode existing --platform codex`，使用真实前驱版本来源 | 原 public prepare、幂等和回滚满足合同；完整 existing 完成 maintenance、reapply、退休资产、冲突与终态断言。准备验证只证明该修复，最终新 candidate 仍由 Stage2 owner 重新验证 |

## 8. 实际未决项

整体准备范围没有阻塞性的产品或来源选择。本轮只需完成明确的 caller 合同适配与同路径验证；具体设计和知识落点由原 Author/Architecture/RDT owners 处理，普通写作遗漏回原 Author。Stage 2 是准备完成后的独立发布责任，不计为本 Task 未完成工作。原 candidate 的失败和既有历史未验证边界继续保留，不由本轮准备结果改判。
