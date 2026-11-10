# #779 D1 委托结果承接与介入方法设计

## 1. 设计目标、需求承接与内容基线

本批承接 [PRD](prd.md) 的 R779-01..06、SC779-01..04 和 AC779-01/02，覆盖 [整体要求](../../prd.md) 的全部选定范围。这是首次 Delivery，没有前序交付。本批目标是在既有 Phase 2 派工合同中补齐委托后的协作方法，同时保持原 discovery、Check 和独立 Review 的责任。

固定开发基线 B 为 `221f74caef372414a1c7d700575742eb1e075af4`，来源为本 Task Intake 已读取的 origin/main 固定观察。Planning H0 同为此提交。最终内容范围为固定 B 到实际 HEAD 的全部提交内容及本批 dirty 增量；Task/session/private-result 不作为实现内容。PR 集成目标是 main，后续目标分支前进不自行改变 B。

适用 Architecture authority 为 `docs/architecture/README.md`（`guru-trellis-architecture`）、`docs/architecture/00-foundation/design-constitution.md`（`guru-trellis-design-constitution-v1`）和 `docs/architecture/06-governance/change-contract.md`。独立 candidate_assessment 的实际出口为 `baseline_current / no_architecture_impact`：本候选仅细化 Phase 2 方法，不改变 owner、公共模型、状态、typed route 或 Architecture decision。本结论只支持当前候选方案；最终规划和实现仍经原 Architecture 各阶段判断。

## 2. 当前系统、边界与目标差额

现有 `trellis/presets/guru-team/spec/workflow/workflow-contract.md` 的 Phase 2 已要求采用 worker 终态及 live facts，并禁止 implementation handoff artifact。`trellis/workflows/guru-team/workflow.md` 2.1 已定义执行、计划外候选资格化和正式检查的原路由。当前缺少的是正常委托后的自主等待、介入条件、运行对应关系、冲突写入交接及结果承接方法。

本批在 canonical workflow-contract 的同一 Phase 2 段补方法正文，在全局 workflow 2.1 加入指向该正文的必要加载引用。精确方法只在 canonical contract 单写。受管 spec 和 workflow 通过原工具维护 owner 同步到当前安装；声明平台入口继续加载同一 workflow/spec，不复制方法。

不改脚本、schema、公共 Skill/profile/exit/DTO、上游 agent/runtime 或业务工具。没有新增状态、运行台账、持久 handoff、授权记录或强制汇报格式。当前没有后继能力切片，也不借本项承接 #734。

## 3. 来源设计处置（唯一）

[来源 #779](https://github.com/castbox/guru-trellis/issues/779) 的“范围与归属”和现行 workflow 构成本批规范性设计约束；六项行为仍由 PRD 定义。逐项处置如下。

| 来源及原承诺 | 处置及落点 | 理由、影响与上游处置 |
| --- | --- | --- |
| #779 范围与归属：复用现有派工/承接，优先 canonical Phase 2 | retain；第2/4节，在原 Phase 2 内增加方法 | 保持唯一方法来源，不新增步骤或 Skill；无需偏离处理 |
| #779 范围与归属：全局 workflow 仅必要引用，主协调者是 workflow 角色 | retain；第4/5节，仅补加载引用 | 原全局编排和 coordinator 职责保持；不虚构独立 implementation Skill |
| #779 范围与归属：受影响 canonical/dogfood/声明平台沿原安装 owner 同步 | retain；第7节，现有 checkout 使用 guru-upgrade-tools | 保留 Task/session 和并行资源，不手工复制受管文件；实际写集由原 owner 冻结 |
| #779 范围与归属：不新增 DTO/状态/台账/handoff/授权/表格/额度/锁/调度器，不强制换代理，不 patch 上游或业务工具 | retain；第2/5/6节，仅写 Markdown 方法 | 无数据或运行机制迁移；不引入定量成本承诺 |
| 现行 Phase 2：worker 终态/live facts 是原 Check 的临时证据，不建 implementation handoff artifact | retain；第4/6节，最小结果仅留当前对话 | 可用事实经适用性判断后采用，不能替代正式语义判断 |
| 现行 workflow 2.1：计划外候选先回主协调者资格化，正式 owner/出口保持 | retain；第4/6节，自主执行限定原委托 | 不把常规自主诊断变成扩张授权；计划外变化仍回现有 discovery |

没有 change/reject 项，也没有待上游接受的设计偏离。

## 4. 模块、职责与设计取舍

**Canonical Phase 2 方法正文**由实施者修改 `trellis/presets/guru-team/spec/workflow/workflow-contract.md`。它接收已批准工作包、实际运行及当前对话结果，定义执行者与主协调者如何协作，不产生新公共对象。执行者自主完成等待、常规诊断、原断言、产物取回和终态；主协调者正常推进独立工作或按平台能力有界等待。必要查询、证据读取和 adb 仍允许。

**全局 workflow**只在 `trellis/workflows/guru-team/workflow.md` 2.1 指向上述方法。它保留 mandatory Skills、原 discovery 与 Check/Review 路由，不复制介入条件或交接步骤。

**原工具维护 owner**负责当前既有 checkout 的受管同步。选择完整 canonical `guru-upgrade-tools`，按 preview、精确写集审查、prepare、原写入边界和 invoke 执行。普通 apply 的旧 Task 阻塞不授权历史迁移或手工覆盖。该 owner 同时核实际 installed runtime、platform selection、mode、sidecar 和 Task/session/peer 保留。

**原 RDT owner**维护生命周期知识单元中的行为、职责和验证关系。第9节定位拟写单元；精确协作方法仍引用 canonical contract，不在知识层再写一套执行指令。

采用原合同内的直接方法修订，能覆盖实际缺口，且没有新增状态维护成本。仅强化初始派工不足以覆盖委托后的介入和写入交接；新增调度器、消息预算或逐轮审批既无本批直接 consumer，也超出来源范围。当前选择不承诺实际节省比例；若后续真实需求改变协调方式，应由原 scope/Architecture owner 重新判断。

## 5. 接口与数据

原调用关系为“已批准 Planning → workflow Phase 2 coordinator → 已配置的 implement/check worker → 原终态结果与 live facts → 原 Check/Review”。本批只补其中的协作方法和加载引用，原输入、typed exit、consumer 及公共阶段均不变。

执行者在当前对话说明完成内容、实际终态、结果位置及未完成项。这些是最小语义内容，不是固定表单或持久 handoff。正常协作不要求逐命令 PID、句柄或 hash；诊断时核本次进程、日志与产物的对应关系。未知事实保持未知。

没有新增 API、字段、存储、schema 或数据迁移。原安装 owner 的临时冻结计划和恢复资料仅服务其既有直接 consumer，不增加本项公共状态。

## 6. 状态、顺序、正常与失败流程

本批没有新增状态机。以下顺序在现有阶段内执行。

1. **正常推进**：执行者按原委托完成工作包内的等待、诊断、断言和产物取回。主协调者推进互不影响的工作，或有界等待，不默认同日志双重跟踪和连续过程指令。日志片段、页面 PASS、命令终态、产物通过及工作包完成分别判断。
2. **介入**：发生需原 owner 决定的真实阻塞、范围/机制变化、冲突写入、用户停止要求或执行者无法继续时，主协调者先核本次运行及具体缺口，再针对缺口处理。猜测不能直接变成重启、重建或修改要求；计划外范围/机制/风险仍回原 discovery。
3. **结果承接或接管**：执行者汇报最小结果。主协调者核当前要求和事实适用性；具体缺口或不一致才补查/重跑。确需接管时，先查现有工作，沿可用原句柄继续；未知终态如实说明，不默认重启。
4. **冲突写入**：主协调者先请求在自然边界暂停。执行者确认当前终态且暂不启动下一轮后，主协调者才写入相关内容，完成后通知恢复。无冲突路径继续并行；没有写入需求时按原委托继续，不逐轮审批。
5. **已经交叠**：主协调者与原执行 owner 核实际影响，披露失效证据，补必要验证，不一律重跑。新增要求作为明确差额交原 owner，不以零碎消息改变隐含完成条件。

主协调者仍判断工作包是否满足要求，识别新缺陷并交原 owner。工程事实、当前语义判断与正式 Check/独立 Review 保持各自证明边界。

## 7. 恢复、兼容、迁移与集成

运行恢复沿已有句柄和真实状态完成，不增加重试或持久恢复协议。原句柄不可用或执行者无法继续时，先说明具体缺口，再由原 owner 决定必要动作。普通未知状态不能当作成功，也不自动要求整包重跑。

本批保持全部公共 I/O 与 consumer，故不需要 public API 或 Task 数据迁移。已有项目需要通过匹配 workflow/preset 的原维护路径采用新方法，源码改动本身不证明已安装或实际 Agent 已采用。当前 checkout 用原 tools-only 路径保留活动 Task/session、历史与并行资源；不得将旧格式 archive 转换混入同步。

工具源选择实际 source HEAD 与完整资产。若当前源不能满足正式 Fork source lock，且原 owner 核实隔离开发模式适用，则明确使用 `local_candidate` 并报告 `formal_fork_source_lock` 未验证。preview/prepare 缺依赖、重叠未完成事务、未知 owned edits 或未解决 sidecar 均先回原工具 owner，不能手工覆盖。真正写集另作可审展示，不把本规划当作该写入动作已批准。

这是全量 D1，无前后 Delivery 业务接口。RDT 隔离 proposed definitions 先进入候选 Check，再由原 owner final_integration 写入并读回，重绑实际完整候选后完成最终 Check 和 committed Review。无 Architecture 差额则不造空贡献或 ADR。

## 8. 验证设计

| ID / 关联 | 层次、入口与输入 | 独立预期与证据边界 |
| --- | --- | --- |
| V779-01 / R779-01..06、SC779-01..04、AC779-01 | 原 Check/独立 Review 读取完整修改段、global 引用及原 discovery/Check/Review consumers | 六项行为的条件、顺序、否定和例外完整；自主执行未越界，最小汇报未变固定审批/台账；正式职责保持。语义审核证明合同充分性，不证明现场节省 |
| V779-02 / AC779-02 | 原 tools owner 的完整 source、preview/prepare/invoke、实际目标 native validation 和 preservation | 实际安装采用目标内容，活动 Task/session/peer 保留，mode 与 sidecar 符合原 owner 合同。只报告执行过的目标与平台 |
| V779-03 / AC779-02 | `bash trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh --repo .`；读实际声明平台投影及 managed specs | canonical/workflow/spec/所选平台一致，原 ownership closure 正确；不能由 parity 推断 Agent 实际行为或外部业务采用 |
| V779-04 / R779-06、知识关系 | 原 RDT candidate/promotion，完整三层拟写及实际 after；最终 `git diff --check` | 要求→职责→验证可追踪，精确方法只单写；晋升后实际内容进入最终质量链；空白或链接不能替代定义 |

验证采用现有正常场景及适用工程事实，先完成正文和原 owner 同步，再运行命中机械检查与正式语义审核。没有改确定性 runtime，不新增只冻结文字的测试。既有安装事实只有输入/依赖/内容仍适用才采用；本轮真实变化覆盖同步与 drift。检查失败只补命中缺口，充分后停止，不为阶段变化重复同质实验。

本批不强制设备、Agent 评测框架、事故重放、消息计数测试或完整多平台升级/Release 矩阵。实际 Agent 成本、业务采用和节省比例保持未验证。

## 9. Canonical 引用、本轮差额与实际未决项

`docs/{requirements,design,test}/current/task-delivery-lifecycle.md` 分别拥有生命周期行为、职责和验证。本轮拟在原完整单元增加 R779/BEH779、D779/CON779、T779 的必要关系，原 RDT owner 在 Phase 2 核实际差额并准备隔离完整 proposed definitions。不会修改 root/current 导航或 unrelated global version。Architecture 的三项 authority 沿第1节使用；当前 candidate_assessment 无需贡献/ADR，最终规划与各实现阶段仍由原 owner 判断。

方法正文及主加载引用落点见第2/4节；质量方法为 `.trellis/spec/workflow/quality-guidelines.md` 的 Test And Validation Value 和 Validation Scope Ownership。现有能力边界保留原 Candidate Applicability And Coverage、discovery 及正式审查合同。

当前没有必要产品选择。实际 tools 写集、依赖模式、安装冲突及最终语义结果尚未形成，均由对应原 owner 在其执行边界核实；它们不是预填通过。
