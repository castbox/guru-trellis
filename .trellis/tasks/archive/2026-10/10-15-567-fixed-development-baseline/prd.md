# #567 固定开发基线与按实际阻塞整合

状态：Planning requirements candidate，不代表规划批准、实施或验收通过。

## 来源与身份

Direct Source：[castbox/guru-trellis #567](https://github.com/castbox/guru-trellis/issues/567)，exact_source；本轮 updatedAt=2026-10-15T12:27:38Z，无 comments。TaskId=567-fixed-development-baseline，generation=0，branch=codex/567-fixed-development-baseline。Intake 基线 main@3b165daef0001bd9816c0bf3bbe928bcb59de390；PR target=castbox/guru-trellis:main，二者不形成后续追赶义务。

canonical 的 Candidate migration boundary 保持：开发 Task 继续由完整旧 installed graph 管理；产品 schema2/Delivery 候选在完整 matching 安装中验证，不混用 DTO 或声称开发 Task 已迁移。本轮读取 Architecture .91/active、RDT .97/active、constitution guru-trellis-design-constitution-v1；真实适用变化归原 owner。

## 目标与要求

任务从创建、规划、实施、Check、完整 Branch Review、PR、merge 到 Completion/Finish 可以全程零 reconcile。其他隔离任务推进 base 或共享 remote-tracking ref，不中断固定候选，不成为阶段资格，也不自动使业务 gate 失效。保留全部既有合法原子能力。

| ID | 要求 | 来源行为条款 |
| --- | --- | --- |
| R567-01 | 分离开发基线、Delivery 固定完整候选范围与 PR target。D2 依据真实交付事实确定增量，不重复 D1，不为取得范围自动同步。 | 1、4 |
| R567-02 | 退役默认 mandatory pair guard/Reconcile、临时候选、同步提交、祖先资格与整体 base/ref/version freshness 耦合，不新增同义 gate。 | 2、3、5、19 |
| R567-03 | 在途 Planning/Check/Review 固定 base commit、候选及 authority 适用版本。正常 fetch 和无关 CURRENT/导航/归档/代码推进，不抢占 owner 或阻止正式结果。 | 7、8、9、16 |
| R567-04 | 整合仅由实际 merge conflict、必需检查的具体集成问题、原 merge 已确认的既有服务端更新要求、明确依赖/需求承接、用户主动同步触发。保留既有 GitHub/合并策略，不新增 Ruleset 查询前置。 | 10、11、12 |
| R567-05 | 一次整合固定目标，期间 base 前进不追赶或重启。局部整合只审差额及受影响依赖，不无条件回 Planning、完整 Phase2/TaskCommit/BranchReview。真实需求、方案或实现语义变化归原 owner。 | 13、14 |
| R567-06 | 保留普通冲突、实施前 resolved baseline、实施后 resolved candidate、committed reentry、bounded continuity 与同操作结果恢复。身份、规划、资源和 Delivery 沿原任务，不制造重复、空或同内容提交/gate。 | 15、19 |
| R567-07 | 工程规则、Architecture、工具有明确阶段适用版本；显式适用新 authority 或真实 scope/依赖/方案变化不能被旧快照掩盖。全体 producer/consumer 同步收敛，Markdown 判断，脚本执行事实。 | 16、17、18、20 |
| R567-08 | Completion/Finish 核验全部 scope 和真实 Delivery/证据。历史截点只证明其范围；无关前进不重查，新交付或相关证据变化只补缺少事实和受影响结论。#569 独占查询准备，不互设前置。 | 1、6 |

依赖覆盖 workflow、Planning/Activation、Architecture、RDT、Check、TaskCommit、BranchReview、DeliveryReview/Publish/Merge、Completion/Closure/Finish、continuation 及 runtime/schema/平台投影；根据真实 consumer 修改，不按目录一律忽略或批量改写。

## 验收

每行通过公开 owner/consumer 调用链证明行为及不发生的工作。措辞、单一 validator 或最终偶然走通不代替该证明；实际结果只由唯一 Test 文档记录。

| ID | 场景 | 必须观察的结果 |
| --- | --- | --- |
| A567-01 | A/B 同基线，B 在 A 不同阶段多次独立合并，A 无实际阻塞。 | A 完整规划→实施→Check→完整 Review→PR→merge→收尾；自动 reconcile、同步提交、base 触发回退均为0。 |
| A567-02 | Check/Review 期间另一 registered session 正常 fetch。 | 固定候选正式结果完成并被下游承接，不因 ref 前进重跑。 |
| A567-03 | 其他 Task 归档、journal/导航、无依赖代码与无关 CURRENT 前进。 | 不整合、不使 gate 失效；按实际 authority 适用性判断，不用目录白名单。 |
| A567-04 | 自身已审 PR 合入；明确截点后无关前进或本任务新交付。 | 等价候选正常接续，不为 ancestry 再提交；无关前进不重查，新交付只补缺少事实及受影响 Completion 判断。 |
| A567-05 | PR 后共享 Proto/生成物/架构文档真实冲突。 | 保留双方成果，原 owner 解决并验证必要差额，接续同一 PR/Delivery，不无条件全链回退。 |
| A567-06 | 必需检查发现具体装配/配置/行为集成失败。 | 对应 owner 修复/验证受影响部分，不忽略失败，不重置无关 gate。 |
| A567-07 | 真实整合期间 base 再前进。 | 固定操作完成，不因 SHA 反复重建候选；后续只处理仍存在的实际阻塞。 |
| A567-08 | 用户修订需求、明确依赖承接、主动同步。 | 三类路径合法，真实改变交原 owner，不以旧批准放行。 |
| A567-09 | 旧 Task/Delivery 采用新合同、结果丢失、session 恢复。 | 原身份和完成操作恢复，不先做无必要 Reconcile；工具/数据迁移归 #566 边界。 |
| A567-10 | D1 合入后 D2，期间 B 多次合入，D2 结果丢失恢复。 | D2 完整范围不重复 D1，不要求最新 base，正常链零 reconcile；Completion 覆盖 D1+D2 和全部 scope。 |
| A567-11 | 无文本冲突、checks成功，但原 merge 确认服务端强制更新；对照无此要求的 behind。 | 前者只更新必要差额和验证，保留同 Delivery；后者零 reconcile 合并，无新规则查询 gate。 |
| A567-12 | canonical、dogfood/声明平台、定向 package/runtime、matching installed公开链路、reapply/drift。 | 新行为和原子能力有分层证据，投影一致，sidecar逐项处置；未覆盖诚实列出。 |

## 约束与非目标

保留 Task/Delivery 身份、具体候选内容和事务一致性、独立完整 Branch Review、PR readiness、既有合并规则及副作用边界。内部接口直接演进并同步全部受控 consumer；正常在途状态由原 owner 恢复，有明确迁移合同，不新增无退出双读或 silent break。

不启动 #569 或实现其查询准备；不操作来源业务仓/会话资源；不新增 tag/Release、业务安装、完整多平台 Release矩阵；不增加攻击、故意篡改、锁、竞态压力或 crash/fault矩阵。不扩为独立 digest 性能或 Task 创建扫描优化。

具体机制、源约束处分由 design.md 单写，Delivery Policy 与 Docs SSOT Plan 由 implement.md 单写。本 PRD 不代替 Architecture、Approval 或验证结果。
