# #669 已有实现分支的归档 Task 恢复：整体需求

## 1. 来源与术语

| 来源 | 章节 / 角色 | 本 Task 用途 |
| --- | --- | --- |
| https://github.com/castbox/guru-trellis/issues/669 | 全文；Direct Source / 要求 | 唯一问题、范围与验收来源 |
| https://github.com/castbox/ai-chat-roleplay-backend/issues/802 | 历史案例 | 定位原 Task，不引入业务实现义务 |
| https://github.com/castbox/ai-chat-roleplay-backend/pull/825 | 已合并归档；证据 | generation 1 的正常前驱 |
| https://github.com/castbox/ai-chat-roleplay-backend/pull/838 | 开放 Draft PR；证据 | 既有实现与原 PR 的保留场景 |
| `.trellis/delivery-contract.md` | Task reopen / 公共模型约束 | TaskKey、历史保留和正式后继阶段 |
| `docs/architecture/03-domains/ownership.md` | ARCH-DOM-060 及共享生命周期职责；架构约束 | 保持原 Reactivate、public Task writer 和环境 owners |

TaskId 是 repository-local 稳定身份；generation 是生命周期代数。实现 HEAD 是既有业务提交的准确提交身份，base HEAD 是当前目标分支的准确提交身份，两者必须分别核验。恢复成功只建立后继身份及正确后续 owner，不证明 Delivery Review 通过。

## 2. 背景与问题

当前 `guru-reactivate-task/runtime/invoke.py:acquisition_plan` 要求 acquisition 的 `decision_head` 等于 `reviewed_base_head`；`task_lifecycle/checkout_resolution.py:_candidate` 要求实际 HEAD 匹配且工作区干净。正常归档后已经编写并提交后续实现的分支无法满足该条件。

真实案例是 backend #802 generation 1。归档已通过 #825 合入 dev，实现分支及 Draft PR #838 的 HEAD 是 `a169e0374c25e126ecdf3836bfe24f3ebf013f22`。目标工作区还有 source-locked 工具升级产生的本地改动。工具升级或 S3 实验结果不证明 Task 已恢复。当前 rebind 的 clean/base-contained 边界不能承担未交付实现迁移。

## 3. 目标与非目标

本 Task 在原 Reactivate/acquisition 职责内建立明确恢复入口，复用已审核的实现分支及 Draft PR，恢复同一 TaskId 的下一 generation。保留原提交、完整工作区改动、PR 与历史公共结果。只修改满足这些要求必需的合同、实现、测试、分发和长期架构/RDT正文。

不创建替代 TaskId，不把历史通过写成当前通过，不自动新建或合并业务 PR，不自动推送、关闭业务 Issue 或清理资源。不修改 #802 的业务代码、实验合同或云权限，不执行模型调用，不新增通用迁移框架、并发加固或攻击防御机制。完整多平台 Release 安装矩阵不属于本 Task。

## 4. 真实调用方、场景与流程

| ID | 调用方与前置条件 | 触发与处理 | 可观察结果 |
| --- | --- | --- | --- |
| S1 | Reactivate AI owner；合法归档、无后继、已有实现分支及 Draft PR | 读取前驱、base、实际 HEAD、工作区、PR 与资源归属；通过原公开 owner 执行已审恢复 | 同 TaskId 下一 generation 的真实 key/ref 和正确后续 owner |
| S2 | 同一操作调用方；输出丢失或已有合法后继 | 原 owner 查找公共后继并恢复同一操作 | 不再次增代，不重复创建 Task/PR |
| S3 | 同一调用方；HEAD/分支/仓库/归档/后继/ownership/本地改动与已审对象不符 | 具体停止并保留现场 | 诊断指出失配；不丢失提交、改动、PR 或资源 |
| S4 | 安装后原生 Agent；匹配源码与工具来源 | 在受控 Git 案例调用原生恢复入口，分别记录安装、恢复与后续正式审核状态 | 安装成功与恢复成功分别有证据，旧审核未自动成为当前 gate |

## 5. 行为要求

- R1：原 Reactivate/acquisition owner 单写恢复路径。前驱必须是已正常完成且归档已在目标基线上核验的准确 TaskId/generation。新代保留原 source、公共 Completion/Closure 与历史，不伪造历史字段。
- R2：首次恢复分别审核真实 base、实际实现 HEAD、允许保留的准确本地改动、原分支/checkout 与 PR repository/base/head 关系。恢复不要求丢弃实现或把实现重置到 base，也不能简单取消当前一致性检查。
- R3：完整保留已有提交、staged/unstaged/untracked 工作区改动及原 Draft PR。工具升级改动与业务改动保持实际来源，不因恢复自动进入远端 PR。
- R4：输出丢失和同操作重试接续实际后继；已存在合法后继时不得创建第二个 incarnation。冲突后继停止。
- R5：HEAD、分支、所选仓库、归档关系、资源 ownership 或已审本地改动失配时具体停止；不得为了完成恢复改写错误对象或清理现场。
- R6：恢复输出交原 Establish/Ensure/Bind 与所需的当前 Task/Delivery owner。历史测试或 review 不作为当前 Planning、Check、Branch Review 或 Delivery Review 的通过。
- R7：源码、真实 Git 和安装后原生恢复验证分别报告。架构决策与当前边界在架构基线合适完整单元收敛；canonical、dogfood 和安装投影按原分发机制同步。

## 6. 约束与依赖

Markdown 拥有语义判断、scope、后续 route 与副作用边界；确定性脚本只核验事实并执行原公共 operation。用户授权仅在对话存在，不进入 artifact、schema 或 runtime。复用原 Task/public reopen、resource ownership 与恢复机制；公共 API 如需扩展，采用独立明确合同和迁移说明，保留旧入口原义。

安装后的验证依赖匹配 Fixed Fork CLI/Core 与完整 Guru preset。真实 backend 案例仅为需求证据；本 Task 授权对象是 guru-trellis repo 和 #669。先在受控安装案例证明能力，不将业务仓库写入或原 Draft PR 发布推定为已授权。

## 7. 可观察验收与验证方式

| AC | 对应要求 | 输入 / 入口 | 预期结果与证据边界 |
| --- | --- | --- | --- |
| AC1 | R1/R2/R6 | 合法已合并归档、无后继、实现 HEAD 不同于 base、原 Draft PR；公开 Reactivate | 返回同 TaskId 的 generation+1、真实 ref 与后续 owner |
| AC2 | R3 | 已审核的 staged/unstaged/untracked 改动及工具升级改动 | 恢复前后提交身份和完整工作区内容可比对；原 PR 不变，无额外远端写入或清理 |
| AC3 | R4 | 成功输出丢失后的同操作重试及已有合法后继 | 相同后继身份；不再次增代或创建 PR |
| AC4 | R5 | 普通 HEAD/分支/仓库/前驱/后继/ownership/本地改动失配 | 具体停止且保留现场；不使用恶意篡改构造范围外测试 |
| AC5 | R7 | 源码定向套件、真实 Git 回归、完整安装后的原生恢复入口 | 各层独立记录真实结果与限制，不把安装或单测成功当正式业务 Delivery Review |

## 8. 实际未决项

整体需求没有阻塞性产品或范围未决项。具体 acquisition 表达、最小一致性数据及公共迁移方式由唯一 Author 与独立 Architecture candidate assessment 确定，不在整体需求阶段预定机制。实际业务后继交付仍由原业务 owners 承担。
