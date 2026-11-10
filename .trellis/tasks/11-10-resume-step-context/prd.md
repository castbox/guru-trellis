# 正常续接与按步上下文查询整体需求

## 1. 来源与术语

本 Task 为 `no_issue`，TaskId=`resume-step-context`、generation=0。来源为当前会话接受的独立请求；#736 只作参考，不进入关闭集合。

| 来源 | 角色及用途 |
| --- | --- |
| `/Users/devSC/Documents/JobProject/guru-validation-evidence/fizz-filter-controlled-2026-11-10/host/resume-step-context-request.md` 全文及实施约束 | 要求和约定设计；冻结 SHA256=`f6b600f9a3076fa991c27fa3654d292789c004c5d2860d259864ccafabeaf53a` |
| 当前会话 2026-11-10 补充 | 要求：current 组合仅输出必要 identity/checkout/key/phase/planning 定位；保留旧 profile，不新增平行入口 |
| https://github.com/castbox/guru-trellis/issues/736 第2、5、6项 | 参考；不接收整 Issue 的资格、审核链和归档责任 |
| `trellis/presets/guru-team/spec/workflow/companion-scripts.md` 的 Skill Contract Discovery、Intermediate Command Stdout | 既有公开查询及 receipt/正式出口边界 |
| `trellis/workflows/guru-team/workflow.md` 的 continuation 和机器标记 | 唯一路由权威，不复制第二份 |

current 指上游公开当前对象查询；路由投影指从实际 Skill/typed exit 查找已声明的唯一 consumer。动态 profile 仍由原 selector 决定。

## 2. 背景与问题

调查基线为 `main@43d8f713865a7d621d838cf851bc358c34d29f29`。`task.py current --json` 已返回 identity/workspace/current_delivery；完整 Delivery/results/candidate paths 不应直接转发。缺口是把现有事实与 Guru checkout ownership 等原校验组合给 consumer。

command `--help` 已提供 profile schema/example，原 discover-skill-contract 与 `runtime/installed.py` 已有 marker/parser。第二个缺口是实际出口的唯一 consumer 投影。旧旅程 Task 在另一个 worktree publishing，范围不同；本项不复用其身份。Fizz 只为历史观察，不是实现对象。

## 3. 目标与非目标

一个 D1 完成两项只读查询、原入口必要接入、受管分发和对应验证。减少重复解析及无关读取，同时保留身份校验、语义判断、恢复与副作用边界。

不修改上游 inventory/start/get_context，不重建 current resolver、第二 profile 导航、平行 Skill/Happy Path wrapper、长期缓存或账本。不合并 Check/Branch Review，不改 qualifier、任务终态、发布、归档，不实施业务功能、预算 hook、设备治理、launcher 重构、批量安装或发布。

## 4. 真实调用方、场景与流程

| ID | 调用方、条件和动作 | 可观察结果 |
| --- | --- | --- |
| S1 | Agent 自己的会话已有合法当前 Task，调用原 ensure 的明确 current profile | 复用 current 并经 Guru 校验，取得最小身份、checkout 与存在时的 Delivery 定位 |
| S2 | 无当前对象或普通 stale/mismatch，执行同一查询 | 无 Task 与 error 可区分，保留原 owner/诊断，不选 inventory、不自动修复绑定 |
| S3 | 调用方已取得真实 typed exit，使用原 discover 的出口查询 | 返回唯一 consumer、原入口及 input/projection 定位；动态 selector 原样保留 |
| S4 | 普通未知出口或开发 fixture 中多重/未映射声明 | 明确停止，不任取 consumer，不执行下一业务动作 |
| S5 | 调用方需要某 profile 的 schema/example | 复用原 help，完整读取当前适用合同及必要依赖 |

## 5. 行为要求

- R1：同一 `guru-ensure-task-checkout` 公共入口增加明确 current profile，复用上游 current；原显式 `delivery_active_task` 输入、输出及消费者保持。
- R2：成功仅投影必要 TaskId/generation/TaskRef、经原 ownership/branch/checkout 校验的位置，以及存在时 DeliveryKey/phase/planning 定位。不返回 results 树、candidate paths、历史或审计包，不冒充阶段通过。
- R3：无对象、stale/mismatch、缺失/冲突沿原身份、绑定、ownership、checkout 或生命周期 owner 处理；保留具体事实或原诊断，不创建/切换/修复状态。
- R4：扩展原 `discover-skill-contract.sh` 的 `--exit` 查询，复用 `MARKER_PATTERNS/workflow_facts` 及 Interface consumer 合同；unknown/multiple/unmapped 明确停止。
- R5：唯一关系返回 consumer 与现有入口/schema/example/input/projection 定位；payload 决定 profile 时返回原 `profile_selector` 合同，不凭 Skill/exit 猜 profile，不另建帮助导航。
- R6：原 workflow/Skill 接入读取完整当前适用合同及必要依赖，历史维护细节只在适用入口加载；不以固定行数截取。顺序、mandatory invocation 与 consumer authority 保持单一。
- R7：只读指不改 Task/Delivery、session、Git、业务状态，不产生资源/绑定。原 managed Python launcher 可能刷新 ignored selection cache，单列该设施事实，不宣称零落盘、不重构。
- R8：只改 Guru canonical，投影通过原安装 owner 维护；保留并行改动与历史 Task/session。新增 profile/输出及 consumer 变更给完整公开兼容合同。
- R9：机械验证与同模型/输入/环境的短原生对照各自限定证明层级；保留首次失败、合法非通过、不利结果、重复查询、装配错误、读取量及人工介入，不据命令次数推断产品缺陷下降。

## 6. 约束与依赖

复用 current、Guru Identity/Ensure、C4/C5、workflow marker、Interface 与受管分发；缺失由原 owner 处理，不建立替代 authority。没有业务数据或数据库迁移。公开新增 profile/DTO 和相邻 consumer 在 D1 设计中收敛。

外部 `host/resume-step-context-comparison-protocol.md` 是验证参考，不是需求 authority；原生执行者只接收冻结 bound/unbound prompt 与正常入口资料，不读验收 protocol。准备绑定/查询成本、待测查询成本、launcher cache 刷新分开记录。

## 7. 可观察验收与验证方式

| ID | 要求、入口与输入 | 预期结果和边界 |
| --- | --- | --- |
| AC1 | R1–R3；原 ensure current profile，合法 Task、有/无 Delivery | 匹配原公开事实与 Guru 校验；只输出必要 identity/checkout/key/phase/planning，无完整结果树 |
| AC2 | R3、R7；无绑定和正常 stale/mismatch 定向案例 | 区分无 Task/error，定位原恢复 owner，不改变 Task/session/Git/业务状态 |
| AC3 | R4、R5；原 discover 的直接 Skill、workflow/stop exit、动态 selector | 唯一路由匹配 authority，原 input/projection 可定位，不猜 profile |
| AC4 | R4；未知出口及局部多重/未映射 fixture | 明确停止；不损坏生产安装或返回任意 consumer |
| AC5 | R5、R6、R8；旧 ensure profile、公开 help 及受影响入口 | 旧调用兼容，新调用完整加载适用合同，不新增平行导航 |
| AC6 | R7–R9；定向 package/runtime 与一次代表性安装投影验证 | 分发、reapply/drift 与并行状态保留；不扩大为完整多平台 Release 矩阵 |
| AC7 | R2、R9；短原生首次对照 | 分别报告正确性、状态边界与实际负担；准备成本单列，不预填通过或节省比例 |

以上为待实施验收，Intake/PRD 通过不证明实现或效果。

## 8. 实际未决项

无待用户回答的产品或范围问题。profile/DTO/consumer 的具体适配属于 Author/Architecture 技术职责。设施不可用时保留具体原生缺证，不能用机械测试代替。
