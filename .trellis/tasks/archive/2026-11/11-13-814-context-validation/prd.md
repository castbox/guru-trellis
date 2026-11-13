# 原生 context 校验开销与超时接续：整体需求

## 1. 来源与术语

| 来源 | 章节／条款 | 角色与用途 |
| --- | --- | --- |
| [castbox/guru-trellis#814](https://github.com/castbox/guru-trellis/issues/814) | 完整正文：背景、要求1–4、验收、交付与兼容边界；当前无评论 | 唯一 Direct Source，定义本 Task 的整体责任。 |
| [Fork PR #68](https://github.com/castbox/Trellis/pull/68) | 改动、验证、安全与部署影响、证据边界 | 已交付前置修复及约定设计约束；保留原校验、预算和恢复语义，不作为 Guru 已安装或验收通过的证明。 |
| [Fork 固定合入提交](https://github.com/castbox/Trellis/commit/e3793251fad8bd261d0c370d408c7675b9f6a140) | 实际 commit、parents、tree；[main CI 43341080020](https://github.com/castbox/Trellis/actions/runs/43341080020) | 本次后续 source-lock 必须采用的来源身份；不是版本发布承诺。 |
| `trellis/presets/guru-team/source/trellis-source.json`；`trellis/presets/guru-team/README.md` | 构建所选 Fork、tools-only owner、官方投影检查 | 当前来源与既有采用合同。 |
| `trellis/skills/guru-team/packages/guru-upgrade-tools/references/contract.md` | 来源配对、未终结操作、forward、目标验证、同操作恢复 | 原安装与恢复 owner 的兼容约束。 |
| `docs/architecture/01-current/runtime-location.md` | 工具维护、固定 Git 来源、冻结资产源恢复 | 既有职责与状态边界；不在 Guru 复制官方身份原语。 |

context 指公开原生 `get_context.py` 入口解析当前会话或显式 Task、绑定分支及唯一 checkout 的事实。外层调用等待结束与 executor 实际结束是不同事件。同事务恢复保留原 operation、recovery ref、candidate、plan 和 preimages，不创建替代操作。

## 2. 背景与问题

#814 保留的历史观察来自 #793/#794：约169个注册工作区下，#793 原 tools postvalidation 的10秒 runtime-contract probe 报 ETIMEDOUT；原会话记录约509次 Git 子进程，直接入口约12秒。临时优先同版本实际 Git 后约5.2秒并恢复成功，但这不证明源码缺陷已修复。这些是历史观察，不是本 Task 新候选的计时结果。

本 Task 的 Guru 起点为 `origin/main@ce4644392d1ed9815d59071388b9bff9978d1cee`。其 canonical 和 installed source-lock 仍为 Fork `aa898d090fc27c9ce6145cfa3c787a6f400da4e2`。Fork PR #68 已交付单次解析内 Git 事实复用与候选缩小，PR #69 已归档其 native Task。固定合入提交为 `e3793251fad8bd261d0c370d408c7675b9f6a140`，main CI 的5个 job 成功。

Guru 尚须采用该来源、通过原 owner 更新实际目标并完成自身验收。Fork 的本机定向结果不提供跨环境延迟保证；Fork 未自然复现 #793 历史内部超时，其新固定候选同 ref 恢复证明不能改称为恢复了旧历史事务。

## 3. 目标与非目标

目标是在日常多工作区规模下减少 context 身份解析的无关重复 Git 开销，使公开 tools 校验及其正常同事务接续可用，同时保留身份、唯一位置、stale/conflict 和证据边界。

整体范围包括固定 Fork source-lock、必要的 canonical/受管 dogfood/声明平台投影、原 tools owner 采用、定向原生与恢复验证，以及 #814 的独立交付、Task Completion、Closure 和必要归档。最终核实实际合入结果在 live main 可达。

不实施 #815 的 manifest 冲突恢复能力，不承担 #808 或其他 Release，不绑定版本或发布时间。不转换无关历史 Task，不修改已完成历史，不新增替代 child、身份 authority、授权存储或审计 ledger。不扩展到恶意伪造、攻击、压力、锁、并发加固、crash 或额外 fault injection。

## 4. 真实调用方、场景与流程

| 场景 | 调用方与前置 | 触发及行为 | 可观察结果 |
| --- | --- | --- | --- |
| S1 日常多工作区 | 原 context/tools caller；约169个合法注册工作区 | 从真实原生入口解析当前会话或显式 Task，减少无关重复 Git 查询 | 返回正确 owner/Task/唯一 checkout；有耗时与 Git 调用来源记录，必要 peer 校验仍执行。 |
| S2 小规模与身份拒绝 | 同一入口；小规模拓扑，或正常 stale/conflict/非唯一身份 | 运行原解析和校验 | 小规模正确；必要身份拒绝仍阻止错误接续，不借用其他会话或跳过验证。 |
| S3 等待结束与恢复 | 原 tools owner；存在原操作或外层等待已结束 | 先核 executor 与原操作状态；尚未结束则跟随原执行，需恢复则使用原 ref | 不重复 prepare/invoke，不替换 candidate/plan/preimages，不将外层等待结束等同于 executor 失败。 |
| S4 Guru 正式采用 | 已有精确 Fork 来源和匹配构建；实际 Guru successor candidate | canonical lock 固定来源，原 owner preview/prepare/执行并检查目标 | 实际目标自身 resolver、installed/native 和投影通过；原 Task/session/peer/common pointer 保持。 |
| S5 独立交付 | 当前需求与上述实际证据完整 | 走原 Review、Delivery、Completion、Closure、Finish | 分别证明交付与整体完成；没有目标安装或恢复证据时不宣称相应验收通过。 |

## 5. 行为要求

- R1 来源采用：canonical source-lock 必须固定 Fork `e3793251fad8bd261d0c370d408c7675b9f6a140`，parents 为 `7a9c62e842001b1d91d6b7feeed36ddd38370da7`、`cd1d5064f3ec8f97c19cf61f2193694edd4c3ba0`，tree 为 `8d7d0c3fe28a3464d92f723539a63da241e5485e`，CI 为 `43341080020`。CLI/Core `0.7.0-castbox.6` 与 `pnpm@10.32.1` 保持；同版本标签不能替代精确源码和构建身份。关联 S4。
- R2 性能与身份：消费 Fork 已交付的单次 `RepositoryFacts` 内事实复用与既有分支拓扑筛选，保留 eligible peer 校验、原 prunable 例外、唯一性判断及选中分支的独立查询。保留当前会话/显式 Task 身份与必要 stale/conflict 检查，不通过跳过验证、仅改 PATH 或无界等待替代修复。关联 S1/S2。
- R3 原生校验：继续执行真实 native contract/context probes，两个10000ms预算保持。用与历史观察相当的正常拓扑和小规模入口验证，记录实际耗时与 Git 调用来源；不从源码或测试桩推断实际入口已经可用。关联 S1/S2/S4。
- R4 原操作接续：区分调用等待与 executor 结束，未知结果先读取原 handle、进程及原操作事实。恢复保留原 ref/operation/candidate/plan/preimages；跨 candidate 的 `candidate_mismatch` 不放宽。已有事务先由其原 owner 处理，不修改旧 checkpoint 或重新 prepare 伪装恢复。关联 S3。
- R5 诊断与证据：诊断只含必要安全字段，不输出敏感配置、原始 stderr 或凭据。保留历史首次超时及真实失败；自然复现、控制样本、恢复与未验证项分别报告，不编造根因或通过结论。关联 S1/S3/S5。
- R6 受管采用：从完整真实 Guru successor candidate 及其自身 lock 配对构建，沿原 source-lock/tools owner 更新实际目标、官方脚本和受影响声明平台。不得手改受管副本、伪造 manifest、只改 `.version` 或在 Guru 复制官方身份逻辑。保留原语义门禁、Task/planning/archive/session、无关工作、peer tools 与 common/peer pointers，按原 owner 解决必要 sidecar。关联 S4。
- R7 独立完成：按 #814 自身范围执行最小可靠验证，经原交付与整体完成流程，核实合入结果在 live main 可达。Fork 修复、lock 更新、命令成功或 Delivery 合并各自只证明其实际范围，不替代 Task Completion。关联 S5。

## 6. 约束与依赖

Fork 前置已满足；后续实际采用必须从该精确提交单独构建，保留正常 ESM/workspace 布局和 mode，不用旧 dist、相同版本号或全局 npm patch 替代。正式 `source_locked` 验证需要包含新 lock 的完整、clean、committed Guru successor SHA。开发 `local_candidate` 证明保留其 `formal_fork_source_lock` 未验证边界，不能冒充正式采用。

原 `guru-upgrade-tools` 拥有实际 preview、一次 prepare、冻结执行及原 ref 恢复。实际文件清单、平台与冲突处置由其真实 preview/prepare 得出；后续 Delivery 规划展开所需步骤。scope-only 本文不提前批准安装，也不产生 Delivery 方案。

Markdown/AI 保留需求、充分性、finding 和 route 判断；脚本只查询、执行、记录及校验确定性事实。公共 Skill/API/schema/命令及其消费者如有实际变化，必须提供明确兼容/迁移合同；本 Task 不因 source-lock 改变而发明新公共 API。

本项没有业务服务、数据库或部署迁移需求。普通任务仅执行 accepted scope 所需 package/runtime、canonical/dogfood/installed、声明平台、reapply/sidecar 定向验证；完整多平台 installer/upgrade/Release 矩阵由其专门 owner 承担。

## 7. 可观察验收与验证方式

| 验收 | 要求／场景 | 入口、输入与预期结果 |
| --- | --- | --- |
| AC1 来源一致 | R1/R6；S4 | 核实际 lock、Fork commit/parents/tree/CI、CLI/Core 构建身份与真实 Guru candidate；官方和受管副本由原 owner 生成并一致。 |
| AC2 大小规模原生行为 | R2/R3；S1/S2 | 在约169个合法注册工作区和小规模拓扑，从实际安装后的原生入口覆盖当前会话与显式 Task，记录耗时/Git来源，返回正确身份与唯一 checkout；两个原预算不变。 |
| AC3 必要拒绝与保持 | R2/R6；S2/S4 | 对支持的普通 stale/conflict/非唯一身份验证原拒绝；核对 Task/session/peer 文件内容、mode 和实际选中 owner，不用故意篡改 artifact 扩展范围。 |
| AC4 同事务接续 | R4/R5；S3 | 经公开 tools 校验和正常同候选原 ref 恢复检查原 operation/plan/preimages 保持。等待结束时核 executor 实际状态。保留首次失败；未自然复现旧内部超时时明确该限制，不声称恢复了旧历史事务。 |
| AC5 安装与分发 | R3/R5/R6；S4 | 原 owner 完成目标自身 resolver、installed/native、必要声明平台与 sidecar/reapply/drift；运行官方 dogfood projection checker 及其测试，不能只用 Guru overlay drift 代替官方脚本/哈希/版本检查。 |
| AC6 独立完成 | R5/R7；S5 | 原独立审查核完整范围及实际证据；交付后分别完成 Completion、Closure、Finish 并验证 live main 可达。未执行的实际安装、恢复或矩阵分别披露。 |

验收表定义后续必须证明的结果，当前均不预填通过。Fork 的已完成结果可作为仍适用的前置证据采用，不能抵扣 Guru 目标验证。

## 8. 实际未决项

没有需要新增产品或范围选择的需求未决项。首个 Delivery 的具体设计、实际安装写集与验证安排由原 Author/Architecture 在接受整体 scope 后细化；整体需求接受不代表 Delivery Planning 批准或实现激活。Task 创建调用的输出丢失已按同一原操作恢复，不据此新增另一修复范围。
