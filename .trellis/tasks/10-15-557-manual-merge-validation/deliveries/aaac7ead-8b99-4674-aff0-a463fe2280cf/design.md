# 验证夹具 Delivery 方案

一个实际UTF-8 JSON文件是本Delivery的全部内容能力：validation/manual-merge-557.json。字段由已展示候选文件确定：scenario=manual-merged-delivery-recovery，version=1，task=557-manual-merge-validation，expected_delivery_fact=delivered，completion_owner=guru-review-task-completion；completion_requires依次为actual_merged_content/current_accepted_scope/scope_required_evidence。期望字段只是夹具数据；正式合入/完成结论来自原public owners，不能从该字段推出。

## 机制与唯一消费者

交付前用UTF-8 JSON解析与固定payload SHA-256 d31a7c21fa045f615883365070646ec5f53d3e409de617ac0fb6073769b4b1c9验证候选字节；交付后从真实immutable Git head/merge及repo-bound GitHub PR读回同一内容。文件由内容核验与原Completion直接消费，不承担Task/Delivery身份authority。

原Creation/Author/Architecture/Wording/Approval/Activation/Check/TaskCommit/完整独立Review/Readiness/Publish产生各自真实结果。普通GitHub two-parent merge不添加Guru trailers或生成Merge gate。原Merge的delivery_merged_recovery根据existing public Publication关联和actual PR/head/merge/parents/base记录事实；原Completion对整体scope、actual content和证据亲自判断；query2只读已记录事实。没有新的模型、writer、ledger或状态转换。

完整matching CLI/Core/Guru、project authority和runtime是本地gitignored验证支撑。专用base/head共享独立最小Git历史，远端repo为castbox/guru-trellis；base为codex/557-validation-base，head为codex/557-validation-head。PR内容仅夹具与必要正式Task/Delivery资产，不把本地安装支撑作为产品变更。

## 来源承诺唯一处置

| Source | Commitment | Disposition and landing |
| --- | --- | --- |
| current-request:557-live-validation / scope | 一个实际JSON夹具经正式公开owners发布后观察真实普通merge/恢复/Completion | retain；本章机制与implement唯一执行顺序承接，不填owner judgment fixture。 |
| current-request:557-live-validation / verification | 真实CI状态、内容与scope-required evidence由原owners读取 | retain；CI不新增要求，missing不是green，实际缺口保持未完成出口。 |
| README.md / 独立公开链验证基线 | 工具与工程authority留本地，软件/业务Release边界独立 | retain；gitignore支撑隔离，专用验证PR只承接夹具与必要Task资产。 |

没有另一份normative design或advisory方案需要导入；不重写Source #557产品方案。全部源承诺retain，尚无外部效果声明。

## Architecture

实际独立candidate_assessment为no_architecture_impact；使用当前.89 baseline/constitution和原owners。没有contribution/ADR/promotion职责；final_plan仍需Wording后独立实际审查。用户计划接受与各Git/GitHub动作保留其当前独立边界。
