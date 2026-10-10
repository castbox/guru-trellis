# #453 中间 receipt 与正式 Skill exit 边界

## Authority 与交付边界
Direct Source：[castbox/guru-trellis#453](https://github.com/castbox/guru-trellis/issues/453)，合同 2026-10-10-r1。
当前 source 的 title/body identity 为 d20b1911da89966cf2f8302d09f0f4ba5c8d849ae74d0dd72dde07d613e296e5。
正文是当前 accepted scope；#396、#250、#292 只定义后续顺序，不给本 task 增加要求。
当前项目 authority 从 docs/requirements/README.md、docs/design/README.md、docs/test/README.md、docs/architecture/README.md 的 active current-main-0.6.17-guru.81 读取；历史版本不充当 current runtime。

## 问题与目标
正常 owner review -> record -> check -> invoke 链中，check/record 尚未形成 public exit 时仍输出 status=ok/passed 或内部 typed_exit。当前真实 Intake checker 和 Phase2 源码证实输出边界缺口；该事实不证明每次 Agent 都误报。
本任务修复这一受支持正常路径中的输出边界，并观察真实 Agent 的声明和接续动作。代码/schema tests 与行为效果分开验收。

## 需求
- R453-01：按每个 live interface.judgment_mode 清点 semantic package 的 recorder/checker/executor/preview/recovery 中间 stdout；formal invoke、owner result、receipt 三者有明确边界。
- R453-02：中间成功 stdout 有机器可见的 formal_exit=false，不能独立满足正式阶段通过证据。owner result 的已有闭合 schema 不因 transport 标记而被扩字段。
- R453-03：只有 public scripts/invoke.sh 产生原声明 typed exit。保留全部现有 public DTO、exit/consumer、atomic 能力与 semantic owner；各 package 声明的正向出口满足其当前合同条件后进入正向 consumer，revision/refresh/blocked 走其唯一 consumer 或 stop。
- R453-04：guru-sync-base、guru-ensure-task-checkout 保持 deterministic profile；不新增 AI Review Gate。sync 内部 receipt 与正式出口按相同 transport 边界区分。
- R453-05：中间命令 stdout 通过显式版本迁移，所有当前受控调用方同步投影。旧安装按完整 preset reapply/upgrade 迁移；不静默改变旧格式、不增加永久 dual-read、fallback 或旧格式 parser。
- R453-06：规范、各受影响 package 的 Skill 合同、canonical runtime、preset、dogfood 与声明平台投影一致。
- R453-07：两类真实 Agent 回归使用合法生成的 owner/checker 输出：checker-only；recorder+checker、尚未 invoke。Agent 说明尚无正式出口，自动补完同范围无副作用的 owner/record/check/invoke，不提前进入 downstream、不重复请求确认。
- R453-08：真实语义审查与 invoke 后，分别覆盖正向出口与适用的 revision/blocked 出口；观察声明和实际唯一 consumer/stop。绿色 Python tests、模拟 CLI、字符串匹配和预填 grading 均不代替行为证据。

## 验收
| Case | 场景与观察 | 层与通过条件 |
| --- | --- | --- |
| A453-01 | 按 registry/interface 读取当前 package 与 command 边界 | 每个当前 command 只有一种 stdout 类别；semantic/deterministic 类型不变；public invoke 与 declared mapping 相符 |
| A453-02 | 实际 dispatcher 执行中间 recorder/checker/executor | stdout 通过 receipt schema，formal_exit=false；原 payload 可经薄 projection 供同 owner 继续；public consumer 不把外层当 typed DTO |
| A453-03 | 正式 wrapper 正向与非通过出口 | public DTO/schema 与既有 exit/consumer 不变；atomic 行为与 supported standalone/workflow 入口继续工作 |
| A453-04 | checker-only 真实 Agent run | Agent 说明未取得正式出口，继续同范围合法链；真实 trace 没有提前 downstream、重复确认或伪造 owner |
| A453-05 | record+check 尚未 invoke 真实 Agent run | 同 A453-04；已有真实 owner review 在未 stale 时承接，不为测试重复审批 |
| A453-06 | 两个 run 的最终正向和非通过 route | 正向只进入声明 consumer；非通过明确 revision/blocked 并进入对应 consumer/stop，不声称阶段通过 |
| A453-07 | canonical/dogfood/installed、平台、apply/reapply | package/runtime/schema tests、当前平台投影与 managed hash/mode 检查通过；drift 为零；逐个处理 sidecar |
| A453-08 | 一个代表性 clean install 与旧完整安装迁移 | 固定候选 complete preset 安装和 reapply/update 后实际 wrapper 行为符合新合同；未覆盖的平台/native host/full Release matrix 单列 |

## 不在范围
#396 draft identity/linkage、其他业务仓库代码/历史 PR、人为伪造与恶意绕过、TOCTOU/锁/并发压力/crash consistency、授权 artifact、软件 tag/Release 与完整多平台 Release matrix。
缺真实 native 行为证据时本 task 的 accepted scope 尚未完成；不得宣称误报问题解决或关闭 #453。

## Delivery policy
单个 Delivery slice 覆盖本任务完整 R453-01..08；发布前完成该 slice 的客观与真实行为验收，不以只改 marker 作为独立完成片。
剩余工作仅为本 slice 的 Publication、Merge、Completion、Closure、Finish 与资源处置，由本 task owner 承接；不隐藏未完成的 implementation/eval。
完成要求：满足 accepted scope 的 PR live MERGED 且在 current main 可达，#453 live CLOSED/COMPLETED，真实 Phase2 与独立 committed full-diff Branch Review 成立，Finish/Cleanup 完成或给出精确 nonblocking caller-owned 资源处置。

## Docs SSOT Plan
公共运行合同在 canonical skill/package 与 preset spec 中维护；受影响 package 文档引用同一 receipt 合同，并保留各自 owner/exit 条件。
通过 guru-maintain-requirements-design-test-ssot:task_impact_sync 建立 task-isolated contribution，形成 R453 -> D453 -> T453 trace；shared current 只通过 reviewed promotion 串行激活。
公共 CLI transport 的 Architecture 贡献由 [architecture-contribution.md](./architecture-contribution.md) 承接，采用 target_native 的 current-only 迁移候选；独立 owner 决定其 stage 出口。贡献在独立 Branch Review 后经原 owner 晋升，再重新 Phase2/commit/full-diff review。方案未提出新增 ADR；后续 discovery 若改变 decision/owner/compatibility exit，重新进入 Architecture owner 判断。
task-local 三份规划文档只承接实施计划；不复制 shared authority，不新增审计 ledger、授权或永久 gate 历史。
