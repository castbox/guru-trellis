# 必需正文读取的双向追踪

本贡献新增独立完整能力，不替换 R717/D717/T717 的共同审核充分性，也不修改全局入口或版本。三份正文的 repository-relative locator 按仓库根解析；晋升前它们是 proposed 定义，目标由 manifest 指定。

| 原 #848 要求 | Requirement / Behavior | Design / Contract | Test / 场景及整体验收 |
| --- | --- | --- | --- |
| R1 实际范围/全文 | R848-01 / BEH848-FULL | D848-01 / CON848-METHOD | T848-01/02/03/05；AC1/2/4/6 |
| R2 两层预算 | R848-02 / BEH848-BUDGET | D848-01 / CON848-METHOD | T848-01/02/03；AC1/2/4 |
| R3 正文载体 | R848-03 / BEH848-CARRIER | D848-01 / CON848-METHOD | T848-01/03；AC1/4 |
| R4 分层恢复 | R848-04 / BEH848-RECOVER | D848-01/03 / CON848-METHOD/RESULT | T848-01/02；AC1/2/3 |
| R5 短节导航 | R848-05 / BEH848-ENTRY | D848-02 / CON848-ENTRY | T848-03/04；AC4/5 |
| R6 原 stdout/恢复 | R848-06 / BEH848-STDOUT | D848-03 / CON848-RESULT | T848-01/05；AC3/6 |
| R7 受管/实际采用 | R848-07 / BEH848-ADOPT | D848-04 / CON848-DISTRIBUTE | T848-03/04/05；AC4/5/6 |

唯一操作正文在原 companion-scripts 短节。原 installer、workflow、平台 payload 和 provider-aware Skill 只定位它。Architecture Planning no impact 沿原结果承接，本文不建立新的 Architecture authority、公共 API、审核 gate 或长期读取状态。

原 RDT owner 已将三份完整定义写入 manifest 指定的 current 目标并逐份读回，状态为 integrated_pending_review。真实 after 将与实现一起进入 TaskCommit 和固定 committed candidate 的独立完整 Review；此整合事实不提供质量通过。
