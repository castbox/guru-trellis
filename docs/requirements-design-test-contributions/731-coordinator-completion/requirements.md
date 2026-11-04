# 跨 Issue 协调责任与主动解阻

Identity：RDT-REQ-ISSUE-ORCHESTRATION；别名：R731、DAG、Sequence、整体完成、主动解阻。原语义 owner：guru-maintain-requirements-design-test-ssot。适用来源：https://github.com/castbox/guru-trellis/issues/731；定义晋升来源为 docs/requirements-design-test-contributions/731-coordinator-completion。目标位置：docs/requirements/current/issue-orchestration.md。本文在隔离贡献中为 proposed；仅由原 final_integration 晋升到目标后成为 current。知识状态不证明软件安装、运行或整体任务完成。

关系：RDT-DES-ISSUE-ORCHESTRATION（docs/design/current/issue-orchestration.md）；RDT-TST-ISSUE-ORCHESTRATION（docs/test/current/issue-orchestration.md）。完整运行合同为 canonical trellis/presets/guru-team/spec/workflow/issue-orchestration.md，调度分别归两 package 的 DAG/chain contract。

## R731-01 / BEH731-GOAL：整体终点

显式调用两编排 Skill 时，协调 Agent 对全部选定 Issue 的用户约定终点持续负责。持续掌握目标、依赖和剩余义务，保留较早终点及既有范围。发送指令、观察一轮、子会话结束、单 Delivery 合并均不等于整体完成。实现与正式 gate 保留原 owner；协调者的核证不代填 Check、Review 或 Completion。

## R731-02 / BEH731-UNBLOCK：主动解阻

子会话 blocked、失败、等待、无建议或在终点前停下时，协调者判断具体缺口和影响范围。存在有依据的范围内方向时，实际调研仓库/外部事实、与原 Agent 商讨、协调资源、质疑不足的阻塞/推荐/完成声明，或按适用合同组织独立审核。选择下一步交原 owner，并追踪实际结果后再判断。没有现成推荐不是无路证明，询问或机械转发一次不是解阻完成。

方式按真实缺口选择，顺利工作轻量观察，不每轮固定询问、质问、审批或审核。不无依据同配置重试、无限实验、穷举理论方案或反复审计。

## R731-03 / BEH731-RECOVERY：失败与合法后续

区分步骤失败、Check blocked、节点等待与整体终局阻塞。未知副作用先通过原操作恢复，不重复执行。已知旧事务失败且无法恢复时保留首失败和同 Issue/Task/Delivery，核修正输入、路径、前置或范围内实现后是否存在原公开入口的合法后续操作。不能删建身份、改证据、替必需 producer 或擅自修范围外框架。明确停止条件继续有效。

## R731-04 / BEH731-WAIT：可维护等待

外部等待必须有具体责任方、对象和复查条件。复查实际外部条件和原等待有效性，不能只比较子会话文字。操作结束、超时、无人承接或复查条件失效时重新判断和安排处置。心跳静默仅控制通知，去重不得永久保留失效等待。无变化的真实等待保持轻量。

## R731-05 / BEH731-BLOCK：真实阻塞与安全收口

先核当前入口、原 owner 支持的修正/等价路径，以及修复是否在既有范围内。完成有依据的解阻判断且无仍可推进的范围内工作后，才能报告整体终局阻塞。说明目标缺口、已核路径和不能继续原因、责任方最小条件或真实选择、恢复条件及受影响节点，无需穷举或新增证明文件。保持原安全停妥和原生回读；真无路不能只留 ACTIVE 空转，条件补齐后恢复同 run。

DAG 只暂停真正依赖障碍的工作，按原 failure policy 继续合法独立节点；Sequence 当前项完整完成后才推进下一项。不得跳节点、削弱依赖或降低验收。

## R731-06 / BEH731-EVIDENCE：证据与分发

通过两技能正常公开入口运行隔离、诚实的真实 Agent。输入只给目标、事实和边界；可控工具只供事实/子会话状态及实际所选动作结果，不预填正确解法、下一路由或通过结论，不代发指令。观察多轮发现、调查/商讨/审核、执行处置、接收结果和再判断。成功场景到约定终点，真阻塞到准确最小条件及安全收口，等待观察复查和条件变化承接。

实施前刷新采用历史的入口、provider、版本、终点、原约束及首失当处置；提供可移植去敏说明，不能只给本机聊天链接。确证缺陷保留首失当/修复后对照；不复现或历史缺项时诚实说明。源码/package、实际受管投影和真实 Agent 行为分别报告；关键词、parity或案例存在不替行为，无法运行记未验证。

保留显式调用、Codex-only/instruction-only、原调度/身份/资源/单集成 owner/gate/确认/public exits。按原安装 owner 同步并核定向回归、reapply/drift、mode/sidecar，报告实际平台与mode边界。普通本项不承担完整Release/Upgrade矩阵，不接管原业务会话、操作生产或发布版本，不新增脚本调度器、授权记录、持久协调台账或固定审批链。
