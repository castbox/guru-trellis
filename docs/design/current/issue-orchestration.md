# 跨 Issue 协调方法的职责收敛

Identity：RDT-DES-ISSUE-ORCHESTRATION；别名：D731、DAG/Sequence协调闭环。原语义 owner：guru-maintain-requirements-design-test-ssot。来源：Issue #731 与本贡献三层定义；目标：docs/design/current/issue-orchestration.md。Version：issue-orchestration-761；Status：current。原 RDT owner 经本 Delivery candidate Check 后在 final_integration 晋升本完整定义；知识状态不表示实现验收通过。需求 RDT-REQ-ISSUE-ORCHESTRATION；测试 RDT-TST-ISSUE-ORCHESTRATION。Architecture：guru-trellis-architecture；采用既有AI/Markdown判断与工具事实分层，不新增架构authority。

## D731-01 / CON731-OWNER：共享方法单写

canonical spec/workflow/issue-orchestration.md 独占整体终点、当前对话边界、主动解阻、等待有效性及结果核证方法。两 canonical SKILL 显式加载同provider正文；DAG/chain contract 独占调度差异、依赖推进和原出口。心跳加载同一方法并应用于实际轮次，不维护独立决策规则。保留原模型设置、创建pending、资源归属和各仓单集成owner。

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

## D761-01 / CON761-NORMALIZE：唯一规范图

原 DAG package 的 SKILL/interface/dag-contract 定义 repositories 会话映射，key 为 canonical owner/repo，value 可给 project_path/base_branch。节点提供 repository、issue、depends_on；图内键和资源/完成引用归一为 owner/repo#N。仓库缺项读实际项目和 remote；多仓裸整数只有唯一上下文可确定时才解释。歧义和矛盾先解决受影响选择，再判断重复、自边、外部前驱与 cycle。原单仓输入展开为同一规范图，不引入第二 parser、scheduler、公共 schema 或持久协调状态。

原 DAG owner 从动议正式绑定解析成员及职责。初始需求就绪作为事实前置，最终总控依赖实际工程完成，避免把工程引用产品需求误作最终验收依赖。共享方法不拥有成员或图调度，Sequence 不扩大为跨仓。

## D761-02 / CON761-PER-REPO：绑定贯穿原闭环

共享 issue-orchestration 方法按节点仓库定位已保存项目、primary folder、remote 与 selected base。原 DAG owner 调度整个图，节点创建、heartbeat replay、child prompt、恢复及结果核证消费同一绑定。一个仓的默认分支不覆盖另一个仓；协调者/provider 路径不决定目标。pending 槽位、host/cursor、每仓单 integration owner 和原权限继续复用，无新增台账。

## D761-03 / CON761-PROVISION：环境是 admission 前置

只读 preflight 先发现缺口。live/auto 经原语义与动作边界，依据本轮实际工具 schema/支持 UI 选择 clone/登记或具体用户步骤；不虚构项目登记或信任 API。建立后回读 saved project 和 Git 事实。创建、用户信任和 setup 需求分别核验；只有真实运行依赖才配置 setup。私有状态编辑与代点信任不属于实现路径。

环境阻塞在原会话维护，不制造图错误或永久全图停止。原 failure policy 决定独立节点 admission，受影响节点和后继等待具体条件。补齐后刷新受影响事实并续原 run/child，初始 clean/base 检查不得误用于已运行的 dirty worktree。

这些新增信息各有当前消费者：repositories 由创建/恢复/核证使用，qualified graph 由调度和心跳使用；不需审计 artifact、dispatcher 或新 owner。变更只增加原 Markdown 合同与原生事实消费的范围，维护成本为同一共享方法与原 DAG 输入；未来真实能力、身份或 workflow authority 改变时回原 Planning/Architecture，不预留通用环境管理平台。

## 本次变更来源与适用边界

新增来源：https://github.com/castbox/guru-trellis/issues/761。适用前驱为 `8c158381b5bdb61fd961cbb89e23c2d1f659c9aa` 中同一路径的 issue-orchestration-1；R731/D731/T731 稳定身份及有效条件保留；原单仓 integration 责任按所属仓承接，新增跨仓不要求无关仓互等，新增 R761/D761/T761。本完整定义已由原语义 owner 在本 Delivery candidate Check 后的 final_integration 整合并回读；软件验证与 Task 完成仍以原阶段结果和 Git/PR 事实为准。

## D761-04 / CON761-INTEGRATION：各仓原事务责任

同仓仅一 integration owner，直到该仓原 merge 结果和紧邻必要 shared-base closeout 有已知 disposition；原 expected-head、gate 与未知操作恢复不变。无跨仓硬依赖或资源组时，各仓原 child/事务可分别推进，协调者继续观察全部 admitted 工作。原单仓流程只有一个此 owner；不新增共享锁、队列、持久owner表或语义owner。按仓责任已可完整覆盖独立Git/GitHub目标，故不再把原单仓等待扩为全局等待。真实共享资源仍按原排它条件处理。
