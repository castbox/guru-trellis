# 完善阶段成果状态收敛与任务完成证据一致性：整体需求

## 1. 来源与术语

| 标识 | Locator 与章节 | 角色 | 本 Task 用途 |
| --- | --- | --- | --- |
| SRC649 | https://github.com/castbox/guru-trellis/issues/649；目标、原 owner 分工、场景、验收、边界及 2026-10-21 修订补充 | Direct Source，要求 | 整体范围、六维状态及验收；已完整读取 |
| DEP648 | https://github.com/castbox/guru-trellis/issues/648；实际交付及匹配安装 | 必要前置、历史事实 | 消费约束、关键前提及 gate 适用 operation 判断，不重做已完成范围 |
| SAMPLE637 | `docs/requirements-design-test-contributions/637-candidate-review-reuse/test.md`；当前状态、后续实际结果、尚未验证 | 当前样本与原始证据 | 只纠正可证明过期的当前描述，保留旧失败、历史及未证边界 |
| RESULT637 | `.trellis/tasks/archive/2026-10/10-20-637-candidate-review-reuse/task.json`；原公共结果及 PR #644 | 正式结果定位入口 | 对照 Check、full_review、Delivery、Completion 和 Git／PR 事实；归档存在不单独证明通过 |
| MECH638 | https://github.com/castbox/guru-trellis/issues/638；既有最终整合机制 | 已交付兼容约束 | 保留 candidate Check → final_integration → 实际候选重绑 → final Check → 完整 committed Review |
| LOCAL | `AGENTS.md`、`.trellis/workflow.md`、`.trellis/spec/workflow/workflow-contract.md` | 仓库与流程约束 | Markdown 判断、确定性脚本及现有授权边界 |

Task 承担整体 accepted scope；Delivery 是其中一个切片。合并、文档存在和命令绿色不单独证明整体完成。当前成果指当前规范、指南、派生说明和测试预期；历史观察与冻结版本保留原身份。

六个状态维度分别为：合同 authority、源码实现、制品部署／入口可达、能力初始化／启用、消费者采用、原业务请求端到端验收。各维度只描述实际核实的能力、对象和环境。

## 2. 背景与问题

正常阶段推进中，能力已实现或注册，当前说明和测试仍可能保留前一阶段的临时限制。必要实施遗漏、方案自行增加的无依据前置、真实外部取证缺口和无关待验证项也可能被混为一类，造成错误完成结论。

#637 当前入口包含无清晰截止点的未完成描述，而原公共结果已有后续 Check、full_review、Delivery 和 Completion。需要逐项核实差额，不能据此推定其它安装、发布、业务采用或矩阵已完成。调查中的业务案例仅证明流程问题，不决定业务 API，也不代表整个版本已完成或撤回。

#638 已提供最终写入及候选承接机制；它本身不证明状态语义正确。本项在原 owners 内补足该责任。

## 3. 目标与非目标

整体目标是让原 owners 在规划、实施、Check、Delivery Review 和 Completion 中准确收敛阶段成果，分别表达事实、证据缺口和剩余责任。

交付范围包括原 Skill 的 step-local Markdown、既有模板／示例、命中原生评测和当前 RDT／Architecture，以及 #637 有限修正。整体完成要求本项独立真实 Agent 评测、#648 自身行为验证的有效承接及匹配安装后的真实多 Delivery 组合验收。

非目标：不启动其它 Issue，不修改 Backend 现场或业务代码，不决定业务 API 演进／兼容方案；不新增阶段、审核人、台账、审批链、公共 DTO／schema／exit、runtime 状态或重复 CI；不扩成通用文档清理或完整多平台升级／Release 矩阵。无阶段限制变化的合法交付不制造文档、字段或无意义验证。

## 4. 真实调用方、场景与流程

| 场景 | 调用方与前置 | 触发及行为 | 可观察结果 |
| --- | --- | --- | --- |
| S649-01 | Author、实现、RDT／Architecture；前序 Delivery 只交付合同并附临时限制 | 后继实现满足解除条件，维护当前定义、说明和断言 | 当前入口不执行失效限制；历史合同保留原观察；其它能力仍有独立剩余责任 |
| S649-02 | Delivery Review／Completion；实现完成但环境证据未到 | 分别核对六维 | 实现完成与环境未验证分别表达；不宣称启用，不将源码改判为未实现 |
| S649-03 | Completion；必要后台消费者未实现 | 判断真实实施缺口 | 返回原实施／规划 owner，不标为外部待证 |
| S649-04 | 规划／Architecture、Completion；方案增加启用前置 | 消费 #648 约束来源、必要性和 operation 适用判断；对照真实外部前提 | 无依据前置回原机制／Architecture；有依据外部缺口沿原 evidence_refresh |
| S649-05 | 原文档 owner；正式结果晚于正文，当前入口仍写旧未完成 | 核对公共结果和 Git／PR，以截止点及引用承接 | 不追写自身最终 pass／HEAD；旧失败和未知保留，真实文件修订仍按受影响覆盖重审 |
| S649-06 | Delivery Review／Completion；同范围只有部分能力实现 | 按能力、对象、环境判定 | 局部完成不扩为整体完成；局部限制不扩成整个版本／Task 冻结 |
| S649-07 | Delivery Review／Completion；合同合入、源码实现、制品部署，Control／phase 未开放 | 分开表达六维及切换证据依赖 | 前三项保持成立；能力未激活、原请求验收未完成；只阻断依赖切换的声明 |
| S649-08 | task-free owner；有界本地修改，或涉及状态／gate 逻辑 | 结果限定 edited paths、本地目标检查和真实 unverified boundaries；gate 同时消费 #648 | 不声明部署、激活、采用或端到端验收；单 operation gate 不扩大为全接口不可用 |
| S649-09 | 原 owners；没有阶段限制变化的普通交付 | 正常执行原合同 | 无台账、空文档、状态字段或额外阶段 |

组合验收须真实执行前序合同限制 → 后继实现与当前说明／断言收敛 → candidate Check → final_integration → 实际重绑 → final Check → committed Review → Delivery Review／Completion。包含原约束冲突、合法修订和原 owner 重入，不能以预填结果或正确 exit 替代 Agent 判断。

## 5. 行为要求

| 要求 | 行为及完整边界 | 场景 |
| --- | --- | --- |
| R649-01 | Author 在原正文、Delivery Policy、实施步骤及 Docs Plan 中写明本批真实临时限制的对象、原因、解除条件、阶段边界和后继责任；不登记所有文档 | S01、S09 |
| R649-02 | 实现及原 RDT／Architecture 在条件满足时更新当前规范、指南、派生说明和适用断言；当前入口不靠过期指令及散落覆盖说明拼装含义；历史和冻结版本不追改 | S01、S05 |
| R649-03 | Check 判断实际行为、当前说明、测试预期是否一致；错误断言即使命令绿色也不提供语义通过依据 | S01、S06 |
| R649-04 | Delivery Review 核对本批成果及发布载荷，Completion 核对整体 scope、全部实际 Delivery 和当前结果入口。六个适用维度分别取证，不适用说明理由；不同层次不能相互推导 | S02、S06、S07 |
| R649-05 | 未激活或环境／切换证据缺失只阻断依赖能力的启用、采用或验收；不否定已成立的合同、源码或部署事实，不阻断无关成果 | S02、S07 |
| R649-06 | Completion 区分必要实现未完成、无依据机制前置、真实外部证据未到及无关待验证。分别回原实施／规划／Architecture、原 evidence_refresh 或合法完成路径，不能统一当外部待补 | S03、S04、S06 |
| R649-07 | 当前结果写候选／观察截止点和真实剩余边界；“当时尚未验证”只描述当时。后续事实由原公共结果和 Git／PR 提供，入口准确引用；正文不回写自身最终 pass、最终 HEAD 或归档后结果 | S05 |
| R649-08 | #637 先重读原未验证项及真实后续结果，只改可证明过期的当前描述。保留原命令、旧失败和当时未知；未证安装、发布、业务采用及矩阵仍保留 | S05 |
| R649-09 | 共享当前定义仍由原 final_integration 实际写入，再重绑实际候选、final Check、完整 committed Review。说明性文件修订也审受影响覆盖，不因“补结果”免审；适用工程事实可复用，不重放已完成设计、测试、合并或晋升 | S01、S05、组合 |
| R649-10 | Closure／Finish 只执行原终态、归档及 bookkeeping；不取得共享 Docs 写入权、不替代质量审核，不为自身结果制造空业务 Delivery、额外提交或递归 gate | S05、组合 |
| R649-11 | task-free 完成报告只声明 edited paths、本地目标检查及明确未验证边界；涉及状态／gate 同时消费 #648 operation 范围，不声明部署、激活、采用或端到端验收 | S08 |
| R649-12 | 在原 Check／Delivery Review／Completion native 入口补上述场景与对照，真实 Agent 自主判断并调用原 wrappers；独立评测和组合分别执行，不向被测 Agent 提供预期答案 | 全部 |

## 6. 约束与依赖

- #648 必须 fresh 核验实际交付及匹配安装。创建前已核验其 CLOSED／COMPLETED、PR #654 和 bookkeeping #655 合入，main 为 `319202beab79c7666ecdb855291bf117e43d407e`，source／installed package 与 dogfood drift 检查通过。这不代替本项行为验收，不将 #648 有效 false、execution_error／no-grade 改称全部通过。
- 保留现行公共 Skill／profile／exit／schema、runtime 状态、授权边界、#637 复用和 #638 单写／最终整合。确需公共 API 变化时回原范围及兼容决策。
- Markdown 定义 AI 判断；脚本仅确定性执行、记录、校验。Semantic Check、独立 committed Review、readiness 和整体 Completion 必须真实发生。
- 只处理 honest-but-fallible 正常路径、遗漏、stale／mismatch、普通实现错误和外部变化；不增加恶意伪造／绕过、竞态压力、锁、fault injection 或非常规加固。
- canonical 修改同步 dogfood；命中 source／installed、声明平台投影、apply／reapply、权限、drift 和零未处理 `.new`／`.bak`。至多一个代表 clean throwaway；完整升级／Release 矩阵由专门门禁承担。
- 没有业务 API、数据库字段或持久化模型变化，因此无需业务数据迁移。业务安装采用、生产效果和完整 Release 不从本仓源码或安装检查推定。

## 7. 可观察验收与验证方式

| 验收 | 关联要求／场景 | 入口与输入 | 预期观察及边界 |
| --- | --- | --- | --- |
| AC649-01 | R01..R11 | 原 step-local Skill、模板／示例及命中 spec | 职责完整；global workflow 只编排；无新公共接口／台账；task-free 边界成立 |
| AC649-02 | R03..R06、R12；S01..S04、S06、S09 | 原 Check／Delivery Review／Completion native 入口，独立真实 Agent 无答案提示样本 | 检出失效限制、错误预期、实施遗漏；保留真实外部待证及无变化；局部不扩大。记录判断及原 wrapper 调用；静态／fixture／exit 不独立证明 |
| AC649-03 | R04..R06、R11..R12；S07..S08 | 真实 Agent 六维对照：合入／实现／部署但未激活；缺切换证据；无依据迁移 gate | 六维分别取证或说明不适用；前三项不被否定；gate 仅影响实际 operation 与相关声明 |
| AC649-04 | R01..R12；组合 | #648 合入且匹配安装后的真实多 Delivery 样本 | 实际合同、后继实现、说明／断言收敛、约束冲突及修订、原 owner 重入、candidate／final 与重绑、最终 Review／Completion；不替代独立评测或 #648 自身验收 |
| AC649-05 | R07..R10；S05 | #637 Test、原公共结果、live PR #644／Git；终态晚于正文对照 | 有限修正截止点和正式引用；保留失败与未知；不追自身最终通过、不免实际文件变化重审；Closure／Finish 不代写共享 Docs |
| AC649-06 | R09、分发约束 | 命中 package／runtime、source／installed、平台、apply／reapply／drift／mode／sidecar；最多一个 clean 安装 | 机械、实际 Agent、安装、远端与外部证据分层；不宣称完整升级／Release 或业务采用 |
| AC649-07 | 全部 | 原 RDT／Architecture、candidate Check／final_integration／final Check／完整 committed Review、Task Completion／Closure／Finish／Cleanup | 当前知识与结果可定位；全部 satisfying PR 已合并且可达 live main；Issue CLOSED／COMPLETED；整体完成、终态和清理分别真实承接 |

## 8. 实际未决项

没有待用户决定的产品或 scope 问题。Markdown 落点、原生评测骨架适配及命中检查集由后续 Author／Architecture 细化；尚未完成的技术规划不构成当前整体需求缺失，也不表示实现计划已被接受。

本项独立评测、组合验收、最终候选、PR／main 交付及整体终态尚未执行。完整升级／Release、外部业务采用及生产效果是明确未验证边界，不作为本 Task 已交付事实。
