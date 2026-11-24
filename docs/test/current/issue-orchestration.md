# 跨 Issue 协调的验证策略

Identity：RDT-TST-ISSUE-ORCHESTRATION；别名：T731、主动解阻多轮验证。原语义 owner：guru-maintain-requirements-design-test-ssot。目标：docs/test/current/issue-orchestration.md。Version：issue-orchestration-native-observation；Status：current。原 RDT owner 曾在 #731/#761 的 Delivery final_integration 晋升此前定义；本轮原生监督修订由 task-free 请求承接。来源：Issue #731；关系 RDT-REQ-ISSUE-ORCHESTRATION → RDT-DES-ISSUE-ORCHESTRATION。本文件定义验证方法，实际结果由原Task/Delivery及Git事实提供，不预填通过。

| 验证/场景 | 需求 → 设计 | 入口、输入与必须观察的行为 |
| --- | --- | --- |
| T731-01 / SC731-GOAL | R731-01/02 → D731-01/02 | 真实Agent显式DAG入口、独立/依赖节点和终点前的无建议障碍；调查/商讨/核证、具体原owner动作、结果再判断直至场景终点，独立工作推进而依赖不被削弱 |
| T731-02 / SC731-SERIAL | R731-01/02/03 → D731-02/03 | Sequence两个节点，旧事务已知终止、普通输入/路径/前置错误及不足完成声明；保留旧失败/同身份，合法后续执行且原gate完成后才下一项，至chain_completed |
| T731-03 / SC731-WAIT | R731-04/05 → D731-04 | 已处理不变等待、实际外部变化、结束/超时/无人承接/复查失效；真实复查且条件变化后重新安排，不靠文字去重空转 |
| T731-04 / SC731-BLOCK | R731-03/05 → D731-03/04 | 必需外部条件或producer无支持路径，明确停止边界；先核当前入口/原owner修正及范围内方向，准确最小请求，安全inactive/无pending且操作已安全停妥（已有旧timer须核证停止），至真实blocked |
| T731-05 / SC731-OBSERVE | R731-01/04 → D731-02/04 | 顺利运行、不变真实等待、真实完成；轻量观察，无无意义通知、重复审核或无限重试；未知发送/创建/merge结果先恢复原操作不重复 |
| T731-06 / SC731-BASELINE | R731-06 → D731-05 | 相同或严格等价输入的修改前/候选真实Agent运行；确证缺陷保留首失当和修复后对照，未复现则说明实际覆盖/历史缺口，不制造失败 |
| T731-07 / SC731-PROJECT | R731-06 → D731-01/05 | source/package、原安装owner实际同步与同候选reapply、drift、mode/sidecar；保持显式调用、Codex-only和public I/O，私有tests不泄入public |

多轮trace必须显示发现障碍→调查/商讨/审核→实际处置→接收结果→再判断。提出推荐、发一次指令、命中exit或文件存在都不足。输入只给目标、事实与边界，host-only预期不能进入模型；工具不能代选路线、代发下一指令或构造gate通过。需要理解自然语言的子会话由真实Agent承担，不能让fixture对消息关键词机械推进。

采用历史现场先刷新原入口、provider、版本、终点、停止约束及首失当处置，提供可移植去敏说明；不可访问时标明缺项并用当前正常入口补调查。不得接管原业务会话或复制秘密/授权过程。

分别报告源码/包、实际投影和真实行为。未运行或缺必要分支记未验证；隔离provider不证明真实app、生产效果、全部客户端或完整多平台Release/Upgrade。定向回归按当前入口和实际受影响consumer选择，测试数和静态parity不替充分性判断。

## 跨仓与环境场景

| 验证/场景 | 需求 → 设计 | 入口、输入与必须观察的行为 |
| --- | --- | --- |
| T761-01 / SC761-CROSS-REPO | R761-01/03 → D761-01/02 | 真实 Agent 公开 DAG 入口，从其他协调/provider仓提供两个同号业务 Issue、跨仓边及不同项目/base；观察实际创建参数、全局槽位、硬前驱完整完成后推进和各仓来源/PR/merge/Completion核证，不以编号或单仓完成替代 |
| T761-02 / SC761-INITIATIVE | R761-02 → D761-01 | 正式产品总控/工程成员、初始就绪及信息链接；观察成员选择与真实职责、无人工循环，不自动纳入信息链接 |
| T761-03 / SC761-PROVISION | R761-04 → D761-03 | 当前工具有受支持创建入口及权限；观察能力调查、实际创建、登记/primary/remote/base回读，setup仅按事实需要，创建不当信任 |
| T761-04 / SC761-USER-READY | R761-03/04 → D761-02/03 | 无入口/权限或要求用户信任、独立节点、用户完成前置后复查；观察准确用户步骤、局部等待、独立进度、同run恢复且原child不重建，不替用户信任 |
| T761-05 / SC761-COMPAT | R761-01/03 → D761-01/02 | 原单仓简写DAG与Sequence公开入口定向回归；保持原并行/串行、观察/解阻、pending、未知操作恢复和整体终点。源码及受管安装/reapply/drift/mode/sidecar沿T731-07，新增测试仍源私有 |

上述场景复用原 source-only 独立 coordinator/child Codex 进程和事实 MCP 支持。工具仅返回真实所选动作的事实，不按消息关键词代选下一步、发指令或制造语义 gate。host-only断言不进入模型prompt。真实行为轨迹与源码/安装检查分开评估；隔离能力不证明实际App已支持项目创建、用户完成信任或生产跨仓交付。Fizz背景动议不执行，本普通功能不承担完整多平台Release/Upgrade矩阵。实际结果限当次候选与观察截止，不预填最终Check、Review或Completion结论。

## 本次变更来源与适用边界

新增来源：https://github.com/castbox/guru-trellis/issues/761。适用前驱为 `8c158381b5bdb61fd961cbb89e23c2d1f659c9aa` 中同一路径的 issue-orchestration-1；R731/D731/T731 稳定身份及有效条件保留；原单仓 integration 责任按所属仓承接，新增跨仓不要求无关仓互等，新增 R761/D761/T761。以上为 #731/#761 的历史整合来源；本轮 task-free 修订仅更新原生监督承接，不声明再次执行了该 Delivery 的 final_integration。软件验证与 Task 完成仍以实际阶段结果和 Git/PR 事实为准。

| 验证/场景 | 需求 → 设计 | 入口、输入与必须观察的行为 |
| --- | --- | --- |
| T761-06 / SC761-INDEPENDENT-MERGE | R761-03 → D761-04 | 真实Agent公开DAG入口，两个无依赖/排它资源的仓库PR ready，A原合并操作结果pending。观察B按自身gate和原owner在A仍pending时merge，A原事务回读完成且不重复；同仓单owner和global slots保持。事实carrier返回原操作状态，不按Agent消息或正确路由推进。 |

## 当前聊天原生监督验证

定向检查两个公开入口没有 automation 启动前置，创建子会话后立即观察，并保留游标进行有界等待。Sequence 超时后执行完整观察轮次，并在前项完整完成前不推进下一项。DAG 超时后继续覆盖未完成子会话，不重读无变化的全文或重复派发；有到期外部条件时仍核对原结果。常规进展不结束监督；真实用户步骤及终局仍准确通知。

DAG 定向用例见包内 `tests/forward-cases.md` 的 C1、C4、C7–C7c、C9–C11 和 O5。检查正常入口合同 Mock、真实业务可调用性、局部缺口、写入归属和无变化观察。走查只证明给定事实下的判断，不证明真实 App 调度或生产联调。

恢复场景核证原绑定、未知操作和未观察区间；新run终局不要求虚构timer停止结果。已有旧timer按支持入口停止，失败保留具体缺口并继续允许的观察，未知结果先恢复。source/installed projection、静态forward case与真实原生App行为分别报告；前两者不替代后者，也不证明应用关闭后仍有后台监督。

原生监督迁移来源：2026-11-15 的 task-free 修订。该修订在原 Markdown owner 内替换 timer 前置，未变更 #847/#848 的实现范围，也不声明这两项已交付。

## T883：局部授权与同轮观察

通过公开 DAG Skill 和源私有 [真实 Agent 载体](../../../trellis/skills/guru-team/packages/guru-orchestrate-issue-dag/tests/native-orchestration.md) 验证 R883-01 / D883-01。载体只供事实、实际所选模拟动作与外部事件；独立审核实际轨迹。

| 验证 | 实际观察 |
| --- | --- |
| T883-01 / AC1 | 已覆盖的精确动作由真实协调者安排原 owner，核证结果，无额外确认。 |
| T883-02 / AC2 | 固定原对照的双节点场景和执行设置。协调者提出非终结确认后，由主持者在无用户回复时释放独立 B，观察同一轮读取及推进，A 保持暂停。本轮边界、B 的可读时点和原前置缺失时记为证据不足。 |
| T883-03 / AC3 | 从原节点步骤观察隔离 Git 注册阻塞。核对预览与保留事实、限定清理和实际差额、同一节点原步骤接续。预览范围不符须停下复查。 |
| T883-04 / AC4 | 在隔离 Issue 核对已收敛的精确正文修订的写前事实、写回和实际正文、受影响 Intake 刷新。未决取舍与普通正文漂移仍回原边界。 |

原中断恢复与未知结果处理沿既有适用证据。现行同轮场景基线、载体可观测性、实际候选行为及安装检查分别报告。现场本机清理及 Backend #1944 只作为场景来源；隔离证据不证明 Codex App 原生调度或真实业务发布。

本次隔离结果只覆盖同轮请求、结果回读和 B 推进。保留首轮失败。若达成该观察后才触及宿主时限，按实际截止点报告，整图结算和 Codex App 原生行为需各自的真实证据。

## T917：并行 PR 合并通知

R917-01 → D917-01 复用[隔离真实 Agent 验证载体](../../../trellis/skills/guru-team/packages/guru-orchestrate-issue-dag/tests/native-orchestration.md)。临时仓库以正常提交推进目标。保留起始提交、通知输入、实际派发与调用结果。

| 用例 | 验证入口与观察 |
| --- | --- |
| T917-01 | 无实际阻塞或依赖变化时，协调会话接收合并通知。核对实际派发保留原同步条件与已核对事实，且没有追赶新 SHA 的指令。 |
| T917-02 | 在固定候选审核期间直接送达同类通知。观察原审核继续，核对候选及仍适用的证据，并检查调用轨迹中没有 Reconcile。 |
| T917-03 | 以正常分支提交造成实际 Git 内容冲突。核对原阶段负责人指出具体冲突并选定目标。观察原 Reconcile 入口的首次调用与结果后停止。 |

受管投影和重应用另按 T731-07 记录。临时仓库结果只覆盖当次隔离语义和 Git 行为。真实应用宿主、生产及完整升级与 Release 矩阵沿各自验收。
