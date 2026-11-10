# #773 Task 分支发现诊断与同身份恢复：整体需求

## 1. 来源与术语

| 来源 | 章节／角色 | 本 Task 用途 |
| --- | --- | --- |
| [Issue #773](https://github.com/castbox/guru-trellis/issues/773) | 完整正文；唯一 Direct Source，要求与约定技术约束 | R1、R2、最小验收及非目标。读取时为 OPEN，无 accepted comments。 |
| 同一 Issue「问题与已核验证据」 | #223 个案的历史事实与证据 | 复用已核实结果，保留历史门禁缺口；不重新操作该业务仓库。 |
| `trellis/skills/guru-team/packages/guru-establish-task-branch-binding/runtime/invoke.py` | 当前实现事实 | discovery／plan recorder 在候选枚举前调用 `resolve_task_ref`；正式 invoke 已转换生命周期异常。 |
| `trellis/skills/guru-team/runtime/task_lifecycle/branch_resolution.py` | 当前候选读取事实 | 区分工作区 Task 与未绑定候选 HEAD Git 树的读取边界。 |

TaskId/generation 标识原 Task 及生命周期。Delivery 标识交付切片；恢复绑定不创建交付结果。Git 载体指可定位原 Task、完整规划和历史事实的固定 Git 对象。工作区 Task 可读，不代表未绑定分支的 HEAD 树已满足候选条件。

## 2. 背景与问题

#223 个案中，业务修复已移植至 dev，但原 schema2 Task 和规划仅存在旧 release Git 载体。接收 checkout 缺少 Task 时，Identity 返回 `task_not_found`；branch discovery 却返回 `internal_error`、退出码 2、空 stderr。当前 discovery 与 plan recorder 的共用路径未转换 `LifecycleContractError`。异常发生在枚举候选之前，不能归因为分支枚举失败。

该个案已保留原 TaskId、generation 0 和 Delivery，恢复文件、调整所选目标并建立 caller-owned 分支／checkout 关联和接收聊天绑定。正文记录了 Identity、Branch、Ensure、Bind、原生 current 和 continuation 的实际结果。这些历史结果不证明公开指引已完整，也不补齐历史 Publication、Delivery、full_review 或 readiness。

## 3. 目标与非目标

目标是让当前 AI 根据准确诊断识别正常缺失 Task，并在用户明确选择同身份恢复、原 Git 载体、目标基线和精确写集后，沿原 owner 完成有界恢复。

本 Task 承担 R1 诊断、R2 指引及其必要的最小公开执行缺口、定向回归和受管投影同步。整体完成需要这些范围全部有适用证据；绑定成功或一个 Delivery 合并都不独立证明 Task 完成。

非目标：不修复 #223 在线业务代码，不操作生产存量、部署、删除、退款或业务 Issue 关闭；不补历史 Publication／Delivery 归属，不重合并 PR，不创建替代 Task、Delivery 或空交付。不建设通用恢复框架、预览缓存、跨会话恢复账本、授权记录、锁、压力或对抗性保护。#766、#772、#734 保持各自责任边界。

## 4. 真实调用方、场景与流程

| 场景 | 调用方、条件与动作 | 行为和可观察结果 |
| --- | --- | --- |
| S1 缺失 Task 诊断 | 当前 AI 以规范 TaskRef 调用 branch discovery 或 plan recorder，但接收 checkout 正常缺失该 Task 文件 | 仍拒绝前置缺失；现有诊断结构定位 `task_not_found` 和 TaskRef，并指向原恢复 owner。不得输出无候选成功。 |
| S2 同身份恢复 | 原身份及固定 Git 载体可以唯一核对，用户选择同身份恢复、目标基线和精确本地写集 | 核对原 TaskId/generation/Delivery、完整规划和真实历史缺口；恢复同一载体，建立分支／资源关联，再绑定接收聊天自身会话并读取 continuation。 |
| S3 已有有效关联 | C4/C5 与 checkout、身份及当前聊天绑定有效 | 直接复用，按实际 continuation 继续；不重建身份，不伪造阶段结果。 |
| S4 载体前提不足 | Identity 能读工作区恢复目录，但未绑定候选 HEAD 树不含对应 Task | 指引说明前提差异并交原 owner 处理；不得把重复扫描当作载体恢复，也不得隐含要求提交。 |

S2 顺序为：固定原 Git 载体 → 核对身份／规划／缺口 → 确认目标基线及写集 → 恢复同一身份载体 → 分支与资源关联 → 接收聊天绑定 → current／continuation。无法唯一确定身份或载体、存在矛盾、缺必要公开动作或新增副作用未确认时，在原 owner 停止依赖步骤。已有授权内的同目标恢复自动接续；真实目标变化沿原交互规则处理。

## 5. 行为要求

### R1 准确的错误诊断

discovery 与 plan recorder 遇到正常缺失的规范 Task 文件时，必须在现有命令诊断结构中定位 `task_not_found`、TaskRef 及原恢复处理。复用现有 `LifecycleContractError` 转换方式，保持原拒绝语义，不扩大通用异常框架。若需要调整公共合同，必须显式说明兼容边界。对应 S1。

### R2 可执行的同身份恢复

原 Identity、Branch、Ensure Checkout、Bind 及实际承接恢复的 step-local owner 必须说明 S2–S4 的适用条件、顺序、公开调用、写入边界和停止条件。基线变更、文件恢复、分支／资源关联、会话绑定分别表述真实结果。保留原 TaskId/generation/Delivery 和历史缺口，不把绑定成功描述成交付或 Task 完成。

指引优先复用现有公开能力和原 writer。不得以内部 Python 类调用、手编 common-dir JSON 或手改受管脚本作为正常公开操作。Author 必须核对公开入口能否承接全部步骤；只有存在具体、可证明的缺口时，才补必需的最小确定性动作及原 owner 合同。不得预设新增工具，不调整候选枚举或排序算法。

指引必须说明：Identity 读取恢复后的工作区 Task；未绑定候选按 HEAD Git 树读取，单纯未跟踪目录仍不够。不得以此强制提交或反复扫描代替恢复载体。

## 6. 约束与依赖

- Markdown 拥有意图、充分性、路线及语义判断；工具仅执行读取、写入及客观校验。保持各步骤现有 `judgment_mode`、typed exit 和原 owner 职责。
- Canonical 范围为分支绑定包、原恢复 owners 的合同／必要示例、候选读取边界和必要受管投影。安装副本由匹配的安装／升级 owner 同步，保留 Task/session。
- 公共 Skill API、schema、exit 或命令若确需调整，必须说明兼容方式，不静默改变既有 API。
- #223 结果的证据来源为 Issue 正文。只修改指引时不重建真实聊天，不重跑全部 Identity／Ensure／Branch／Bind／current／continuation 入口。
- 若新增或改变恢复执行动作，以一条去敏代表性场景验证变化步骤、同身份绑定结果及历史缺口保留。
- 本项无数据库、部署或服务配置变更要求，因此不要求数据迁移或生产运行验收。完整多平台安装、native Agent 全链与 Release 矩阵不属于本项验收。

## 7. 可观察验收与验证方式

| 验收 | 对应要求／场景 | 入口、输入与预期观察 |
| --- | --- | --- |
| AC1 缺失诊断 | R1／S1 | 对 branch discovery、plan recorder 共用缺失 Task 路径做定向回归。调用仍拒绝；诊断识别 `task_not_found`、定位 TaskRef 并指向恢复处理，不能变成无候选成功。复用受影响的成功／只读回归，不另建全链诊断套件。 |
| AC2 指引可执行 | R2／S2–S4 | 对照原公开入口审核身份、载体、规划、历史缺口、目标基线、写集、关联、绑定及 continuation 顺序；明确工作区与 HEAD 前提差异、写入边界和停止条件。不得依赖私有调用或手编状态。 |
| AC3 变化动作结果 | R2／S2、S3 | 仅当新增或改变执行动作时，用一条去敏代表性场景观察变化步骤和同身份结果，并断言历史 Publication／Delivery／门禁缺口仍保留。仅改指引时复用正文适用证据并说明边界。 |
| AC4 安装投影 | R1、R2 | 经原 owner 同步受影响副本，执行与改动匹配的 package、分发和 dogfood drift 检查，核对 sidecar。结论限定于实际执行范围。 |

以上定义验收义务；本 PRD 不声明实现、测试、开箱即用、升级兼容或 Release Gate 已通过。

## 8. 实际未决项

整体需求无待用户选择的范围问题。Author 在 Delivery 方案阶段必须回答：现有公开入口如何承接已要求的同身份关联并满足候选载体前提，是否存在具体最小执行缺口。该问题由代码和公开合同调查回答，阻塞完整方案就绪，不阻塞整体需求收敛。指引不得隐含要求提交；实际新提交仍属于独立副作用。
