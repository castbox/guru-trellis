# D1 父仓 gitlink 原子内容实施与验证计划

## 1. 输入与引用

完整读取根prd.md R1—R4/AC1—AC4、本批PRD七节、design九节，尤其第3节来源设计处置、第5节上游API及private兼容、第8节验证边界。固定B=b78edbbdc32e77392bc3775366473971050ccb4b、接续H0=4bf6f551a19b313ee3ac1ccc277388e0c888dc2f；无已交付前序。适用规范为quality-guidelines的Test And Validation Value、Reviewed Content Cross-Package Acceptance、Validation Scope Ownership，data-contracts的Check/TaskCommit/Reviewed Content及Architecture change contract。

## 2. 有依赖顺序的步骤与文件责任

- I1，共享事实/Check实施owner：在canonical runtime明确父状态投影和原子entry接口；修改reviewed_content.py和Check common.py，删除child探测，支持父index新增/删除/replacement。修resolved精确当前Taskmetadata豁免和自然fixture。先约定共享接口再派互不重叠模块。
- I2，Commit实施owner：仅拥有guru-create-task-commit runtime/schema/tests及必要包合同；按I1接口收敛snapshot，version=delivery-3.0，旧private重新prepare。isolated index用父OID/absence，保留普通文件及真实hook事务。补实际验证snapshot消费者，不能重建第二candidate authority。
- I3，Review/Reconcile消费者owner：修改原Review/Reconcile/review-change实际状态读取，保留committed/cached父指针及原exact commit；验证verification/upgrade调用链，仅修实际同责任差额。各worker知道存在并行改动，不revert他人文件；共享接口变化由I1协调。
- I4，原RDT/Architecture owner：准备完整隔离拟写和必要consumer引用，独立candidate Check后沿final_integration晋升/readback，再由实现owner重绑真实after并完成最终Check。原source规范child规则必须一起收敛，不能只改执行脚本。
- I5，原upgrade-tools owner：从完整canonical源更新dogfood/platform/spec，保留Task/session/AGENTS。逐项处理sidecar，执行drift/ownership/mode及定向采用验证。独立审核覆盖B..当前完整差额和受影响未改consumer。
- I6，完成本仓Check、精确commit、独立Review、Delivery发布/合并、Completion/Closure/Finish及适用Cleanup。仅处理当前repo/Issue和已有资源；不执行release/tag或上游改造。上游依赖及业务采用由原owner另行承担。

## 3. 验证入口、输入与预期观察

V1使用guru-check-task的test_execution_consumption.py生产wrappers链，接matching public Delivery API，begin_check后保留自然task.json；观察精确Reconcile tree/parents/message和metadata bytes/index。新HEAD正式candidate受上游能力约束，失败明确记录。

V2在runtime/shared及Commit tests建立真实父子Git仓，用update-index建立父指针，测试未初始化/dirty/不同HEAD/缺对象时父身份不变。调用实际capture及_materialize_exact_index，读回tree独立断言新增/更新/删除/mode replacement；改变父index后验证stale。局部机制测试不宣称绕过上游的正式Delivery已通过。

V3先执行受影响package/runtime tests，设置其声明的TRELLIS_DELIVERY_API_COMMON/GURU_UPSTREAM_DELIVERY_SCRIPTS为真实匹配provider，不能隐藏依赖失败。再按shared合同执行同HEAD正式跨owner wrappers；补普通文件/hook回归、业务unstaged/其他Task/unmerged拒绝。沿真实consumer更新无效的旧child断言。既有archive失败用base对照归因，不算本轮通过。

V4使用guru-upgrade-tools原preview/prepare/invoke，随后运行bash trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh --repo <本工作树>，检查实际受管目标和sidecars。必要定向安装采用验证只证明本仓投影；上游正式gitlink交付链/业务现场不在本批验收；缺口如实报告。只有安装行为实际改变才补定向安装验证，完整矩阵不在范围。

## 4. 停止条件与适用回退点

需求/authority变化回Clarify；实际机制变化回Author/candidate assessment；测试真实finding由原实现owner修复再补命中验证。公共API不支持gitlink时只停依赖该能力的外部链路动作，不伪造候选或热补target。受管同步冲突回原升级owner，保留所有Task/session和无关改动。

旧未执行private候选失效重新prepare；已有commit或receipt先由原Commit owner核真实结果并恢复，禁止重复提交。result receipt语义不变时保原格式，不转换授权或历史结果。无产品数据库迁移或release副作用，不新建回滚协议。不reset/revert用户并行内容，不创建额外Task/Delivery。Git/GitHub副作用沿原commit/publication/merge/closure owner执行。

## 5. Delivery Policy（唯一）

policy=full。本Delivery完整覆盖当前accepted Guru侧R1—R4/AC1—AC4；不存在本Task的上游改造或延期业务恢复义务。完成条件为本仓源码、真实同责任consumer/合同和受管投影收敛，真实resolved自然metadata回归、代表性父index原子机制及直接受影响回归/投影一致性通过，独立审核无未处理finding。按实际逻辑分支选择测试，不做child状态×Skill×平台组合矩阵，不新增独立验收artifact、审批或流水线。

上游regular-only、业务工具采用和保留现场复跑属于外部能力边界与原owner，不作为本Issue额外门槛。本Task仅声明Guru侧交付，不宣称上游已采用或业务恢复；不通过排除路径或mock抹去依赖。标准Delivery/Completion/Closure/Finish沿原owner执行，不增加新的验收阶段。

## 6. Docs SSOT Plan（唯一）

strategy=delta_first。原RDT writer准备Check/Commit/shared identity/consumer的完整当前行为、设计和测试差额，直接consumer为这些Skills及其调用者；原Architecture writer准备父仓与child职责、原子内容、上游依赖与采用退出的完整task-owned拟写。必要当前目标通过限定职责目录检索并读取，不向共享根登记摘要。

canonical包SKILL/references/commands/schema和preset data-contracts中旧child准入与旧private候选定义同步替代；保留历史归档原观察。原RDT/Architecture owner在candidate Check后final_integration处理自己authority的完整proposed内容并readback，实现owner重绑after后完成最终Check/Review。data-contracts和所有managed projection沿upgrade-tools同步，不手工copy。

外部采用条件满足后由其原owner更新当时适用指南和断言，本轮历史证据保持原边界。源码、dogfood、目标正式采用和业务效果分别陈述，不把规划或机械投影称作业务恢复。
