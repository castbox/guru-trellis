# D1 局部修复 Intake 与 Discovery 身份诊断

## 1. 整体来源与术语

本批为 Task `692-intake-reuse-diagnostics` generation 0 的首个 Delivery，id 为 `6bbcdf6f-2687-446f-80b7-968f230ba574`，profile 为 `pull_request`。公共 planning_root 为 `deliveries/6bbcdf6f-2687-446f-80b7-968f230ba574`。公共 scope_ref 指向 [整体 PRD](../../prd.md) 的 R692-01..04 与 AC692-01..05，accepted_scope revision 为 `sha256:321e73fd28cf3e43b31fac125001fec4e31e4b58d2500342c55bec63fba68ffc`。

| 来源 | 章节、角色与本批用途 |
| --- | --- |
| [Direct Source #692](https://github.com/castbox/guru-trellis/issues/692) | 完整正文四项行为要求、当前能力、历史案例和非目标；需求 authority，评论为空。 |
| [整体 PRD](../../prd.md) | 第4..7节：本批场景、全部行为、兼容/分发边界和验收责任。第8节：历史现场未知。 |
| `trellis/skills/guru-team/packages/guru-{select-workflow-mode,discover-change-context,clarify-requirements,author-task-plan}/` | 当前实现与原 owner 合同；定义实际入口、职责、输出和恢复。不是本批已通过证明。 |
| `trellis/presets/guru-team/spec/workflow/workflow-contract.md` | Interaction Budget、当前 Intake 与候选承接；约定边界。 |
| main `6a65ec8afe6d180850760b3b2edf3f94be6e3b20` | 起点；含 #695/#694/#693 已交付能力及 #706 后续审核方法。本批只计新增净差额。 |

“事实复用”只指原 owner 审查后仍适用的来源/代码/测试调查事实；不复用旧 target 的 pass、私有 producer 结果或授权。“内容绑定不一致”是确定性观察；单一摘要差异不足以证明某种解码根因。

## 2. 整体与本批目标、非目标

整体目标是降低局部修复 Intake 的剩余重复成本，并使普通身份/内容不一致可定位、可按原 owner 恢复。本批完整交付 R692-01..04：原 selector 适用指导、各受影响 owner 的事实复用/重读差额、Discovery 公开链的具体诊断、兼容分发和定向验证。

本批不更换全局 owner，不删必要语义门禁，不建立新状态、缓存、审批链或 digest authority。公共 I/O、typed exit 如需改变，先明确 consumer 与迁移，不静默改语义。原身份/freshness、敏感信息保护及独立副作用边界保持。

保留整体全部非目标：业务案例/原聊天/原 Task 只读，不修支付、业务代码、测试或数据；不重做 #695/#694/#693；不新建 Issue、release/tag；不做全 Skill 诊断工程、攻击/篡改、并发/锁/TOCTOU/crash 加固；不新增专项回放、A/B、native eval、固定 case 数、耗时测量、额外安装或完整多平台矩阵。

## 3. 本批起点、前序结果、依赖与剩余责任

首次切片，无本 Task 前序 Delivery。Task 已创建、整体 PRD 已由原 Clarify 接受，当前 D1 为 planning；这不代表方案已接受或实现已开始。

已有 selector 可自动选择高置信度低风险 task-free；已有 Task 保持原身份。fresh Sync/Intake、自动 mapped 恢复、stdout-only 最小 authoring 及错误三字段均已有来源。当前 Discovery `check_owner_binding` 的多项比较可只定位到 `owner_result`；check/invoke 的收窄错误承接需要沿实际 consumer 说明改进。原合同尚需明确本项场景中的重读、复用和下一 consumer。

输入为当前 live #692、完整原 owner 合同、实际代码/测试和适用项目 authority。原案例当时安装快照、完整原聊天和运行时根因没有取得；这些未知不得改写为已确认，也不变成本批新验证门禁。

本批无计划外后继功能。D1 satisfying PR 合并后，整体 AC692-06 的 Completion、Closure、Finish、归档与资源处置仍须由各原 owner 完成；不能用本批代码或合并替代。若本批确实有未覆盖义务，回整体 owner 判断，不靠声明全量掩盖缺口。

## 4. 本批调用方、场景与流程

| 场景 | 调用方与前置/触发 | 行为与可观察结果 |
| --- | --- | --- |
| D1-S01 | 无相关 formal Task；原 selector 收到局部修复 | 依据实际影响、风险和验证判断。购买提示与支付核心分开分析；UI 表象不自动证明低风险。已有 Task 不走新身份绕过。 |
| D1-S02 | 原 Create Issue 成功后转为正式 Issue | fresh Sync、正式身份与完整 live 正文必须读取；原 Intake 各 owner 区分差额重审与仍适用调查事实，并给下一 consumer 当前有效输出。 |
| D1-S03 | 已有整体范围；原 Author 写 Task/Delivery 需求和方案 | 保留整体/切片各自责任，按来源和实际差额裁剪调查与装配。每个独立语义判断亲自完成，不把上游 pass 当当前判断。 |
| D1-S04 | 已解析 JSON；普通 caller 将当前输入与旧结果配错，或命令输出读取造成内容不一致 | Discovery 在可判定处给实际字段或 evidence 类别，并说明重读、恢复 owner/支持入口。原拦截保持，错误不泄露内容，不从摘要猜根因。 |
| D1-S05 | 正常正文/base/目标变化或无变化普通恢复 | 明确本批触及的路径与未改类别；原 owner 按真实变化刷新受影响判断。mapped 无新增副作用自动承接；新真实选择和独立副作用分别处理。 |

## 5. 完整行为、条件与约束

- **D1-R01（R692-01；S01/S03）**：沿现有 selector 与执行 owner，补足局部修复按实际影响判断的具体指导；Issue、文件数、购买词和 UI 表象不能独立决定路线。真实范围/风险变化回原 owner；已有 Task 保持身份和生命周期。
- **D1-R02（R692-02；S02/S03/S05）**：各受影响原 owner 定义触发条件、必须重读/重审的内容、仍适用的调查事实和下一 consumer。草稿转 Issue 读取正式身份、完整正文和实际差额；不复用旧 target pass、伪造 producer 或预设跳过阶段。Task/Delivery 规划须有具体减重方法，不能只再述 Interaction Budget。跨 Skill 重入如有变化，列明合同差额与迁移。
- **D1-R03（R692-02；S05）**：无变化且无新增副作用的 mapped 恢复不询问例行继续。当前对话已经明确请求的同一动作不重复询问；真实 scope/authority 选择、资源、提交、发布、合并保留各自边界。授权及过程不进入任何 artifact。
- **D1-R04（R692-03；S04/S05）**：设计从 Discovery record/check/invoke 和其实际共享检查列出入口/类别/原诊断/不足/恢复 owner。确定性可判定时指到实际字段；只能辨别 evidence 类别时如实说明。明确正文、base、目标身份实际触及范围，未触及类别保留原合同。
- **D1-R05（R692-03；S04）**：诊断说明重读什么、返回哪个原 owner、通过哪个原支持入口重入。内容绑定不一致不等于 UTF-8 根因；JSON 尚未读取成功先按 #695 读取合同处理。不输出正文、敏感值、原始字节片段。不强制新增 code；必要错误细分同步真实消费者、声明及文档。
- **D1-R06（R692-04；全部）**：Markdown/AI 判断路线、充分性、风险与恢复；脚本保持确定性。公共 API 如需变化须明确兼容/迁移；保持现有原子能力、错误合同及拦截。canonical 修改通过原 preset 分发同步 dogfood 和实际受影响平台；不 patch 上游/全局包。
- **D1-R07（R692-04；全部）**：验证仅用既有正常开发、Check、独立 Review 和适用升级流程。真实通过、SKIP/环境阻塞、公共源码、dogfood 和外部采用分别陈述，不宣称完整矩阵或耗时收益。

规范性来源约束由后续 design 第3节维护唯一处置；本需求不复制该矩阵。当前只定义行为和边界，不提前接受具体方案。

## 6. 本批验收、验证方式与未决项

| 本批验收 | 要求/场景与入口 | 预期可观察结果 |
| --- | --- | --- |
| D1-AC01 | R01..03；原 selector/Intake/Author 合同和正常 Planning/Check/Review | 每个受影响环节有具体触发、重读/复用/重审与 consumer；局部影响判断有效，已有 Task 身份和独立 gate 保留；有具体减重差额。 |
| D1-AC02 | R04/05；设计列明的 Discovery 公开 record/check/invoke 及实际共享检查 | 对正常输入/结果配错、输出读取内容不一致及实际触及的 base/目标变化，返回字段或 evidence 类别与原恢复入口；旧绑定仍拦截，一致输入继续原合法出口。 |
| D1-AC03 | R05/06；原 JSON reader 与 Discovery 错误 consumers/声明 | #695 读取层与身份层保持分工；code/field/status/错误形状、schema/catalog、文档和消费者匹配；不泄露正文或把猜测写成根因。 |
| D1-AC04 | R06/07；原 source/installed、package/runtime、平台投影、mode、reapply/drift、sidecar及适用升级 | canonical 与 dogfood/实际受影响投影一致；真实当前范围经 fresh Check、独立完整 Branch Review、PR readiness。未执行的外部采用或完整矩阵明确未验证。 |

本批 AC 对应整体 AC692-01..05；整体 AC692-06 在原 Completion/Closure/Finish 继续。无阻塞 requirements_ready 的产品未决问题。技术机制、具体诊断路径和兼容方案由 Author/独立 Architecture 后续评估，不用未知现场填补需求。

## 7. Canonical 引用与本轮差额

| Authority/实现来源 | 命中范围与差额 |
| --- | --- |
| `docs/requirements/current/json-input-carriers.md`；`docs/design/current/json-input-carriers.md`；`docs/test/current/json-input-carriers.md` | #695 的载体/读取行为为已有基础；本批仅处理成功读取后的内容/身份和原 owner 使用指导。 |
| `docs/requirements/current/task-delivery-lifecycle.md`；`docs/design/current/task-delivery-lifecycle.md`；`docs/test/current/task-delivery-lifecycle.md` | 原 Task/Delivery 身份和 scope/gate 责任；本批不改 public 生命周期，沿真实差额承接。 |
| `docs/{requirements,design,test}/current/knowledge-maintenance.md` | 原 current-knowledge/贡献与晋升责任；具体 Docs Plan 留在 implement，不能提前写 shared current。 |
| `docs/architecture/README.md`、`00-foundation/design-constitution.md`、`06-governance/change-contract.md` | 原 authority-first、AI/script、公共 I/O 和分发约束；实际影响及贡献/ADR由独立 Architecture owner 判定。 |
| `trellis/skills/guru-team/packages/guru-discover-change-context/runtime/{common,record,check,invoke}.py` 与 `tests/` | 当前确定性一致性检查和错误投影；本批列明受影响字段和恢复信息，不推广成全局诊断机制。 |
| `trellis/skills/guru-team/packages/guru-{select-workflow-mode,create-issue,clarify-requirements,author-task-plan}/` 与 canonical workflow/README/preset | 本批差额是各原 owner 的实际调查事实复用和重读指导；现有选路、fresh graph和前项方法不重复计功。 |

以上引用供实际完整读取，不是已完成验证或 Architecture pass。源码与运行副本的本轮同步由原受管机制执行；业务案例和外部安装不从这些链接推定。
