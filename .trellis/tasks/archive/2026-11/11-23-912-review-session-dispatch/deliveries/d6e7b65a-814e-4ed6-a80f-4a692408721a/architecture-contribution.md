# #912 接收会话与正式阶段派发

状态：拟议，供当前规划独立评审。承接 [Issue #912](https://github.com/castbox/guru-trellis/issues/912)。

本次沿用 ADR-035、ADR-EXPLICIT-REVIEW-OBJECT 和 ADR-POSTCOMMIT-INDEPENDENT-REVIEW。实际调用会话先满足原入口自己的 Task 及适用 Delivery 前置。原只读查询判断实际状态，原 Identity、Ensure、Bind 和 Selection 分别核对或补齐。Workflow 拥有跨阶段派发与接回顺序，阶段 Skill 拥有独立评审、具体前置及原正式结果。仅原会话 owner 写必要状态。正向落点为 ARCH-CONTEXT-001 的接收会话约束，及相邻 RDT 单元。候选保持既有无 context 和 final_plan 只读路径。

验证边界：真实新评审者完成实际入口，已有正常会话状态回归证明恢复分支。分发验证证明匹配文本被实际安装。

| Concern | 适用判断与规划依据 |
| --- | --- |
| authority-binding | applicable。固定 B 1174ab49c7187ead613eb338ef1bb5ef1eb0e994，baseline guru-trellis-architecture，project contract guru-trellis-architecture-change-contract-v1。候选与最终规划分别绑定 planning:3.0 的 purpose 及本轮设计。 |
| constitution-binding | applicable。使用 current guru-trellis-design-constitution-v1。职责内聚、概念完整性和最小复杂度由实际执行者前置与复用原会话 owner 承接。 |
| boundary-and-decision | applicable。需求和行为权威为 Task/Delivery Lifecycle。当前接续有确定性读取和各原 owner，目标扩展派发与接回的调用点。target_native，延伸 ADR-035、ADR-EXPLICIT-REVIEW-OBJECT、ADR-POSTCOMMIT-INDEPENDENT-REVIEW 的既定职责。 |
| owner-and-single-writer | applicable。Workflow 编排，原阶段 Skill 持有语义门禁，Bind 与 Selection 各写其会话变更。Architecture 原 owner 整合 ARCH-CONTEXT-001，RDT owner 写三层正文。 |
| compatibility-and-exit | applicable。既有公共命令、输入和无 context 行为可继续使用。保持 final_plan 显式只读入口。matching workflow/Skill 按原分发路径采用。 |
| gap-and-deviation | applicable。#912 的前置遗漏由实际新接收会话通过 V1 关闭。AC03 核对其他出现点及原停止路由。 |
| parallel-scope | applicable。候选与规划限当前 worktree。多个会话可以使用同一对象，独立 reviewer 的 session runtime 与主会话隔离。共享 CURRENT 只由原 owner 整合。 |
| evidence-and-freshness | applicable。V1 验证实际正式入场，V2 覆盖正常状态，V3 覆盖实际派发点与分发。最终规划绑定 design 原始字节，提交后绑定固定 B..H。 |
| review-and-promotion | applicable。最终规划审核实际 design 和本贡献。现有 ADR 已覆盖选择与独立性边界，接收调用点差额进入 ARCH-CONTEXT-001，沿原 final_integration 核对 expected-current、写入及读回，之后独立 Branch Review 再判断整个 after。 |
