# #532 设计：在原 Check 边界直接支持空候选集合

## 当前结构与缺口

canonical package 为 `trellis/skills/guru-team/packages/guru-check-task/`。schema 的 candidate_classifications 使用 minItems:1；runtime/common.py 的 validate_candidate_classifications 同时拒绝非 list 与空 list。既有 no-findings 示例包含 candidate:phase2:no-defect，因此只表达非空候选 rejected，不能证明真实零候选。

原 recorder 导出 schema 5.0 与 worktree-content token，checker 校验当前内容、受审路径覆盖、task/planning 关系、引用和 route，public wrapper 再运行原 checker并产生最小 DTO。passed 保留 Check checkpoint 给 Task Commit，并调用原 execution owner 的 retirement helper；其它出口删除 Check checkpoint，execution recovery state 保留。该所有权链保持。

## 选定机制

直接演进现有 Check，无第二套入口或兼容 adapter。

1. AI owner 完成原完整语义审查并形成真实候选集；reviewed_paths 表达受审内容，candidate_classifications 表达实际候选判断。
2. 空集合：三个 qualifier 均没有合法输入，跳过它们。owner 仍完成九项 adequacy、Docs、Architecture、验证充分性和 route 判断，记录空 classifications。
3. 非空集合：执行 normal、solution 与 root 的现有适用边界；拒绝候选不能产生 findings、测试扩张或 planning_stale，eligible 候选仍保留 witness 与真实引用。
4. schema 去除该数组的非空下界（其 type、items、required 与版本不变）；runtime 只拒绝非 list，再执行现有 uniqueness/reference 校验。引用循环不因为 rows 为空提前返回：空 refs 集合仍拒绝任何 finding/scope decision 的悬空引用。
5. public input 2.0、private checkpoint 5.0、四个 exits/consumer 和原 token 算法均保持。不增加字段、exit、script command、gate 或存储。此次是合法值域增加，既有非空有效 payload 语义保持，无旧版本 dual-read。

## 受影响消费者与合同

| Profile / consumer | 同步职责 |
| --- | --- |
| initial_check | 完整初检的真实空集走原 recorder/checker/public wrapper |
| finding_fix_rerun | 修正后完整当前轮可能没有候选；原 finding refs 只作输入回程标识，不制造本轮候选 |
| planning_reentry | 更新规划后的完整当前审查重新形成候选集，不沿用旧分类 |
| resolved_reconciliation | 同一原 checker 校验 conflict-resolved tree；原私有结果与 project-resolved-reconciliation 投影保持 |
| Task Commit | 消费原 retained Check checkpoint，空候选不产生额外字段；当前内容及 anchor 检查保持 |
| guru-activate-task retirement | 仅原 passed 且当前 checker有效时调用；非passed/stale 保留执行恢复状态 |
| qualifier 三 packages | 非空公共输入保持；不修改它们的 runtime/schema |
| preset / platform discovery | canonical 同步 dogfood 与一个 installed 环境；薄入口不复制 Check 内部行为 |

## 方案比较

伪造 no-defect 候选会混淆受审范围与缺陷候选，拒绝采用。给 qualifier 增加通用空集出口会扩张三个独立公共合同，拒绝采用。仅修改 schema 留下 runtime 拒绝，不能闭合公开链路。新增 wrapper 绕过原 checker 会丢失 freshness 和生命周期，拒绝采用。原边界直接放开空集并保留其它校验，能够解决已观察的根因。

## 状态与 authority

Current Requirements/Design 为 current-main-0.6.17-guru.85/active；Architecture 为 current-main-0.6.17-guru.84/active；constitution 为 guru-trellis-design-constitution-v1；项目 change contract 为 guru-trellis-architecture-change-contract-v1。文档只引用这些长期 authority，不复制其流程正文。

AI 持有 scope/充分性/findings/route 判断；Python 只校验集合类型、元素结构、唯一性、引用、内容 identity 与 route consistency。新增集合合法值不把空数组变成 semantic pass。Architecture planning 由 fresh 独立 generic reviewer 读取设计对象与实际 consumers 后给出当前结果；本设计不预设其影响结论。

## 验证设计

package 单元直接运行生产 validator，覆盖空集、现有非空行为和空 refs 下引用一致性。真实公开链路必须使用兼容 preset、正常 task/规划/branch control state、原 recorder/checker/invoke；unit/mock/post_owner eval 不代表 AI semantic_authoring。

真实无候选初检由 AI 完整当前审查提供；实际全 rejected 与有效 finding 使用可审阅的正常观察/缺陷场景，适用 qualifier 真实调用。测试场景的产生不得采用手工伪造 checkpoint/hash 或不合法 workflow bypass。missing evidence 通过正常缺失验证/前置门禁；stale 通过 recorder 后正常受审内容变化。

使用一个干净代表性 Codex installed 环境，安装完整 Guru preset 并运行真实 Check 入口。apply/reapply 观察实际 package 投影与 sidecars；dogfood drift 校验为零。只读取官方 update 受管文件与 template hash/冲突语义，报告实际定向覆盖；不把单环境证据称为完整 upgrade/Release matrix。

## Docs 与持久化

RDT 增量 contribution 按 PRD 的 Docs SSOT Plan 承接。test.md 是实际验证结果唯一长期位置；输出区分 deterministic post-owner 与真实 semantic owner 链路。无需 tracked Check gate、review transcript、跨 Skill qualification cache 或新 ledger。owner-private 临时输入按既有生命周期消费后删除；不写用户授权信息。
