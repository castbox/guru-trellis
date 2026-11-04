# 跨 Issue 协调方法的职责收敛

Identity：RDT-DES-ISSUE-ORCHESTRATION；别名：D731、DAG/Sequence协调闭环。原语义 owner：guru-maintain-requirements-design-test-ssot。来源：Issue #731 与本贡献三层定义；目标：docs/design/current/issue-orchestration.md。Version：issue-orchestration-1；Status：current。原 RDT owner 在 final_integration 晋升本完整定义；知识状态不表示实现验收通过。需求 RDT-REQ-ISSUE-ORCHESTRATION；测试 RDT-TST-ISSUE-ORCHESTRATION。Architecture：guru-trellis-architecture；采用既有AI/Markdown判断与工具事实分层，不新增架构authority。

## D731-01 / CON731-OWNER：共享方法单写

canonical spec/workflow/issue-orchestration.md 独占整体终点、当前对话边界、主动解阻、等待有效性及结果核证方法。两 canonical SKILL 显式加载同provider正文；DAG/chain contract 独占调度差异、依赖推进和原出口。心跳加载同一方法并应用于实际轮次，不维护独立决策规则。保留原模型设置、创建pending、资源归属和单集成owner。

直接在原 Markdown 方法收敛，避免新增协调Skill、调度脚本、台账或固定问答链。新增状态与授权记录会重复既有会话/owner职责，并不能替代语义判断；本选择的维护成本限于共享正文、薄消费及必要验证。未来出现新的真实caller或接口约束时回原Planning/Architecture重审，不能提前预留。

## D731-02 / CON731-LOOP：目标与结果闭环

每轮从当前终点和真实事实判断剩余义务。顺利路径轻量观察；障碍或不足声明触发具体缺口判断，再选择有依据调查、商讨、资源协调、原owner修正或适用独立审核。发出指令后仍接收结果，重新判断剩余目标。无现成建议时核当前可用能力、入口、前置和独立工作；不把调查动作本身当达成。

原正式gate仍由对应owner执行。协调者可以质疑、复核和组织review，不制造pass。普通技术选择在当前范围内处理，只有真实外部条件、未覆盖行动或用户决定才请求最小输入。

## D731-03 / CON731-RECOVER：已知失败与不确定操作

结果未知的发送/创建/merge先核原操作和真实记录，不能盲目重复。原事务已知终止且不可恢复时，保留旧失败，再由原owner核输入/路径/前置修正后的合法后续。保持同Issue/Task/Delivery、公开入口、停止条件和必要producer；不以恢复困难扩大到框架修复或直接证据替门禁。

## D731-04 / CON731-WAIT：等待和终局

等待对象、责任方及复查条件在当前会话维护。实际外部条件和等待有效性优先于子会话文字是否变化；结束/超时/责任方退出/复查失效使旧等待不再足够，重新进入目标与缺口判断。通知去重不抑制事实复查。

真无路径时只暂停实际受影响工作。DAG按原failure policy运行独立工作，Sequence保留当前位置。不存在可推进工作且解阻判断充分后，原settlement安全停妥并回读心跳停止；同run在具体条件补齐后恢复。保留当前用户停止条件和所有原权限边界。

## D731-05 / CON731-VERIFY：事实工具与行为验证

真实协调Agent从显式公开Skill入口读取合成目标/事实/边界。隔离provider只读取事实、传递实际选择的操作并返回结果；需要理解自然语言的子会话处置由真实Agent承担，禁止用keyword/oracle或机械状态推进代替。host-only预期不进Agent上下文。fixture仅证明隔离协调行为，不证明真实app或生产业务。

测试私有源沿既有package tests边界，原安装owner维护共享spec和公共包投影；不修改public I/O。candidate、installed、行为和外部效果各用自己的证据，普通变更不继承完整发布矩阵。
