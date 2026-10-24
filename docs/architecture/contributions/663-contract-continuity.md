# 流程合同连续性贡献

Task：663-contract-continuity，generation 0；Delivery：cca947d9-76e6-4de4-92db-d51286d89693。状态：proposed。适用来源为固定 B `e9583202b67750d7b3ec2b7eab4b037c0c52a226` 的 guru-trellis-architecture/constitution-v1/change-contract-v1，以及 [#663](https://github.com/castbox/guru-trellis/issues/663) 的 F1–F4 和约束。

## 真实差额与路径

选择 target_native。before-authority 继续绑定原固定 Git revision；新增最小 absent_locators 只表示三个已声明路径在该 revision 的真实缺失。省略仍要求全部存在。当前 authority、当前候选、committed B..H 和原独立判断不被豁免。Bootstrap phase2 只落实现有 final-integration maintenance 回程；repair_required 薄投影和 archived example 修正不新增 owner 或状态。

拟晋升完整单元为 `docs/architecture/06-governance/change-contract.md` 的“当前候选、晋升与恢复输入”，以及 ADR-CONTRACT-CONTINUITY 与必要 ADR 导航。完整 proposed 目标由本 Task 在实现中形成，经独立 Phase2/candidate Check 后由原 Architecture owner final_integration 整合。当前贡献不是共享 authority，不记录阶段 pass、执行历史或授权。

## 九项 concern

| Concern | 适用性和本项处理 |
| --- | --- |
| authority-binding | applicable：Planning purpose3.0、nonplanning5.0/Delivery3.0 原身份保持，逐路径状态绑定固定 B，不用 H 替代 |
| constitution-binding | applicable：使用 current constitution-v1；概念完整性要求真实缺失可表示，最小复杂度禁止通用恢复/第二状态机 |
| boundary-and-decision | applicable：原 producer/consumer 和 fixed-before 比较职责，ADR-CONTRACT-CONTINUITY 明确缺失与当前完整审核的关系 |
| owner-and-single-writer | applicable：Bootstrap、Review、Architecture 原 semantic owners；脚本仅核 Git/schema；原维护 owner 单写 current |
| compatibility-and-exit | applicable：直接成套演进，已有省略 before 状态的合法输入含义不变；旧失配 seed/example 从当前 Interface 重建，不保留第二 reader |
| gap-and-deviation | applicable：关闭本项四个真实衔接缺口；不新增责任偏移，不声称关闭无关 ARCH-GAP-006/008 或业务缺口 |
| parallel-scope | applicable：本 Task 独立贡献及分支，晋升只触及命中单元并保留真实 current 的有效条件；不写他方 contribution |
| evidence-and-freshness | applicable：正式 wrapper 组合、同输入对照、原生 owner 与 installed 分层；候选与固定范围由各原 owner 当前绑定 |
| review-and-promotion | applicable：完整 proposed definitions→独立 Phase2/candidate Check→原 maintenance 晋升/读回→新 candidate→最终 Check/commit/full Review |

## 兼容与未验证边界

`MIGRATION-663.md` 将定位 matching workflow/package/consumer 和完整 preset reapply；真实 API ID、typed exits 与状态不新增。必要新缺失集合由当前 validator 消费，不是审计载荷。旧 pinned 安装保持其固定合同，新能力在成套采用后生效。

实现、所有 V1–V8、分发及最终门禁尚待执行。受控 schema/provider 通过不证明原生 owner、业务采用或完整 Release。没有单独生产/业务持久化变更。
