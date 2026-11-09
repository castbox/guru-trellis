# D1 tools-only peer 增长与冻结源恢复设计

## 1. 设计目标、需求承接与内容基线

本批覆盖 [PRD](prd.md) 的 R1–R6、AC1–AC4 和全部四个场景，包含实际 #766 原事务恢复。开发基线 B 与 Planning H0 均为 `a5f3ceeabbaccddae65935d97763f5a798f71ca9`，来自已固定 main；PR 目标为 main。内容范围是本批 tools package、其受影响分发、规划和知识差额，不纳入其它工作树业务修改。

独立 candidate_assessment 的 current 结果为 `architecture_impact / target_native`，基线 `guru-trellis-architecture`、constitution `guru-trellis-design-constitution-v1`，决定涉及 ADR-027、ARCH-RUNTIME-LOCATION 和本批 ADR-TOOLS-FROZEN-SOURCE-RECOVERY。它评估机制，未证明实现或最终规划。独立 final_plan、phase2 和原 Check 仍须实际执行。

## 2. 当前系统、边界与目标差额

首个 Delivery，没有前序交付。tools_owner.py 的 begin 在首次写前固定 schema1.0 checkpoint、peer_pointers、源 HEAD/tree token、公共计划和 preimages。resume/rollback 均经 check_source，现有 unchanged_peers 比较整个字典，因此独立 peer 新增也会误阻塞。#759 的 prunable 且缺 .git 精确条件已在 B 内，保持不动。

目标分两部分：原观测键值继续保持；新键只接受已核实的物理隔离 peer。另提供修复 executor 读取原冻结资产源的明示入口，薄复用原恢复 engine。原源、public pair/plan/ref 和备份不改，不创建第二事务。Task/Delivery 判断不进入工具脚本。

## 3. 来源设计处置（唯一）

| 来源与原承诺 | 处置与落点 | 理由、影响与上游处置 |
| --- | --- | --- |
| tools package contract Same-operation resume and rollback：同 source、原计划/preimages、owned freshness | retain：第6、7节；既有 resume/rollback 保持同源含义 | 新入口显式区分 executor 与资产 source；原资产身份校验不弱化，兼容合同成套发布。 |
| RDT runtime-location R718-03/11、D718-03/06：单目标工具、源目标区分、peer选择保持、原rollback | retain：第4、6节 | 新 peer 不入写集；目标验证独立执行。原 RDT owner 按 delta_first 收敛精确补充。 |
| ADR-027、ARCH-RUNTIME-LOCATION：source-loaded、单目标、public兼容先于恢复 | retain 并窄补充：第7节和隔离 Architecture contribution | 原资产仍来自原完整源；修复 executor 的不同源身份只由新profile表达。原Architecture owner在final_integration晋升。 |
| Issue #769 的 ref/plan/preimages/source不变、无reprepare | retain：第5–8节 | 这是验收条件。没有来源要求 projected-only 或以文件投影推断阶段完成。 |

## 4. 模块、职责与设计取舍

`guru-upgrade-tools/runtime/tools_owner.py` 独占确定性工具动作。unchanged_peers 对原 snapshot 每一键检查当前存在且同值；新增键不补入 snapshot。复用 isolated_layout 并对实际工具写集与新增 peer 的物理位置核隔离，避免只忽略新增键却漏过真实共享目标。工具写集由原 preimages/public plan 所有，不扩充备份。peer 查询沿原环境 owner 只读入口；不激活其它 peer 环境。

新增 recover_frozen_source 在当前修复包执行。它从原 checkpoint 的 source 定位完整原 logical asset package，以该包加载 legacy installation helper、preset installer和资产，再调用当前 resume/rollback engine。engine 的 package/source 参数必须明确指向原资产包；当前执行代码与原资产不得通过替换源字节或重写 checkpoint 混为一体。复用引擎的原因是 public/guru/preset/complete 和 rollback 已有阶段合同，另写 projected-only终态器会漏过早期合法阶段并复制验证。

Markdown Skill/contract判断适用性、隔离证据和路由；runtime只校验身份、事实和执行。package Interface、输入/输出schema、examples与migration由同一实施owner成套更新。主协调者拥有规划及知识贡献；独立Architecture只读评估，原maintenance owner独占共享晋升。

## 5. 接口与数据

现有 install、resume、rollback 输入及既有出口语义保持。新增公共输入为 `{profile: recover_frozen_source, action: resume|rollback, recovery_ref: 原ref}`，不接收新source、plan、preimages或目标override。--root指定原目标的准确Git根。当前完整修复源为executor；资产源只能从原cp.source解析并校验。

成功仍返回原 tools_upgraded 或 rolled_back 最小DTO。可续接失败新增 `frozen_recovery_required`，仅携 `profile=recover_frozen_source`、同action和同recovery_ref，唯一consumer是同一tools owner新profile；不能投影成旧resume。永久缺口仍走blocked，不把失败变成功。

不新增checkpoint字段，不刷新peer基线、preimages或固定source identity。既有schema1.0 consumer由显式兼容合同支持；输入和新retry输出使用独立schema及Interface分支，不能把全部profile塞进大量optional字段。

## 6. 状态、顺序、正常与失败流程

先读schema1.0原checkpoint，核root、原source_ref/HEAD、source_tree_token、public dependency_mode及冻结CLI/Core pair，核原owned baseline、隔离与原peer保持，再执行原action。

resume沿原phase：public用原public operation恢复或其原未开始动作；guru按原decision清理旧受管工具；preset仍是pending，运行原资产installer的同操作续接，使用原public recovery ref；complete只验证，不再次安装。不能从已投影文件推断preset完成。公共owner已经完成的写入沿原记录恢复，不prepare新计划。目标own resolver/installed/native和原peer保持通过后，才保存complete并返回tools_upgraded。local_candidate仍明示formal_fork_source_lock未验证。

rollback先核Guru owned freshness，再由公共owner核真实tools/data兼容并rollback，最后按原preimages恢复Guru与载体、验证旧native和peer保持。已rolled_back只重读终态验证。原源变化、原peer值变化、目标或owned内容不匹配继续阻塞；可恢复动作失败保同ref/action交新retry出口，原同源调用仍用原retry语义。

## 7. 恢复、兼容、迁移与集成

旧consumer是修复前schema1.0 tools事务，包括 #766 的既有操作。新修复代码只承担executor，cp.source完整原源仍承担所有资产及原installation helper。兼容入口不重新prepare，不变更旧source token、公有operation/plan、备份或rollback anchor，也不吸收之后的业务编辑。无需数据转换或双写。

既有同源profile继续使用同源合同。新profile与独立retry出口必须同时更新workflow consumer、Skill合同、Interface/schema/examples和MIGRATION-769；旧安装不获新能力，须从完整修复源显式调用。兼容退出条件是这些原事务进入终态且原恢复保留责任结束；届时通过明确迁移删除兼容入口，不增加扫描器或自动删除API。

#766实际恢复在本修复Delivery交付后从新完整修复源执行，保持其旧源HEAD和canonical字节不变；原 #766 Task随后独立Check/Review/交付。#769 Completion必须核这次原操作恢复，不能只以代码或fixture通过结束。

## 8. 验证设计

| ID | 条件、入口与观察 | 范围与AC |
| --- | --- | --- |
| V1 | 用真实Git worktree和原peer_pointers形成before，正常新增独立peer后执行保持检查；核原键值、peer工具/指针/业务bytes及mode未改 | 长期回归，AC1；不mock被测拓扑逻辑。 |
| V2 | 原peer合法选择或指针普通变化，原入口拒绝；共享目标实际不隔离时拒绝 | 长期回归，AC2；保留#759回归，不做攻击或压力。 |
| V3 | 原owner正常创建旧事务，用修复源公共wrapper调用resume/rollback及失败retry；核旧ref/plan/preimages/source恒定、阶段动作和目标结果 | 长期恢复回归，AC3；外部API可用unit边界隔离，但不得宣称真实完整链。 |
| V4 | 真实#766原ref从新源recover_frozen_source恢复，读同public operation与最终目标own resolver/installed/native | 现场验收，AC3/4；不改checkpoint或源，不reprepare。 |
| V5 | 受影响package/recovery测试、source及installed validator、dogfood drift、sidecar/mode与目标native | 分发和安装定向证据，AC4；不承担全多平台矩阵。 |

按quality-guidelines Test And Validation Value选择足以检测缺陷的断言。新增peer后不抛异常还不够，须观察原身份不变和隔离结果；新profile单元测试不能代替公共wrapper/retry consumer与现场恢复。复用仍适用覆盖，补真实缺口，证据充分即停止追加实验。

## 9. Canonical 引用、本轮差额与实际未决项

RDT current/runtime-location的完整requirements/design/test单元承接peer增长和冻结恢复差额。Architecture命中docs/architecture/01-current/runtime-location.md；任务隔离贡献位于docs/architecture/contributions/769-tools-peer-growth-recovery/，含完整proposed current单元和ADR候选。共享导航无独立变更，不登记新主题。

原Architecture维护方在独立phase2和candidate Check后final_integration写/readback；原RDT维护方同步收敛完整单元，再重建candidate执行最终门禁。没有产品未决问题。实现中若发现既有source/installer消费者前提不成立，回本设计和Architecture评估，不自行扩大恢复机制。
