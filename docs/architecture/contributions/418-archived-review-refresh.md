# #418 Architecture Contribution

Identity：`418-archived-review-refresh-v1`；状态：`promoted_source`；change path：`target_native`。
本贡献已吸收到 `current-main-0.6.17-guru.53` 的 `ARCH-CUR-030`、`ARCH-INT-018` 和 `ADR-010`，
仅保留提升来源，不与 shared current 形成第二 authority。提升前审查范围为
`78651e2068184e9e52a778fe33eda8b2bd7c8e0b...c30eadd6cf6fe4ba204c32c6e89f3f25f892e8f4`。
Promotion-created diff 的后续 gates 与发布仍需独立验证。

## Authority 与范围

- 提升时 expected predecessor：`current-main-0.6.17-guru.52`；当前 baseline：`docs/architecture/README.md` / `current-main-0.6.17-guru.53` / active。
- 当前设计宪法：`docs/architecture/00-foundation/design-constitution.md` / `guru-trellis-design-constitution-v1` / current。
- 项目合同：`docs/architecture/06-governance/change-contract.md` / `guru-trellis-architecture-change-contract-v1`。
- Guru owner 合同：`guru-maintain-architecture-baseline:2.0`。
- 需求：[Issue #418](https://github.com/castbox/guru-trellis/issues/418)，`R418-04/05`。
- 完整技术合同：`.trellis/tasks/09-16-418-closeout-identity-recovery/design.md` 第4节；本文件只记录架构影响、决策与提升责任，不复制DTO正文。

## Before / Target

Before：completed archive不能进入普通Publication；新archive-HEAD review不符合Finalizer原归档锚点。只有错误文案和mapping修复不能闭合复审链。

Promoted result：在Merge、Branch Review、Publication、Finalizer四个原owner内部增加专用只读profile。三个新的success exits显式连接唯一consumer；新PR snapshot不承担批准语义；新Publication审查后才生成可供Finalizer验证的payload。H与A分离，普通mutation路径不变。

Branch Review实际base B作为最小范围身份传至Publication/Finalizer；title/body快照只服务复审内容一致性。Publication新增profile专属finding/blocked union，不把task_work或metadata问题伪装为external blocker。Architecture仍在三个原stage逐次调用，用既有source_exit的闭合集合识别只读范围，AI在需写入或证据不current时返回blocked，validator拒绝该来源下不符合边界的需写出口；普通来源路由不变。

已审查图增量：0 Skill、0 command、4 profile、3 external exit。当前图为 23 Skills / 100 exits / 78 commands；旧四个 Merge 操作/恢复出口仍有效，新增只读出口不改变其语义。

## Required Concerns

| Concern | Applicability | 本任务合同 |
| --- | --- | --- |
| authority-binding | applicable | 同时绑定上述Guru/project/current identities；内容漂移重新进入owner |
| constitution-binding | applicable | 命中concept-semantic-completeness、cohesion-change-isolation、minimum-necessary-complexity、debt-one-way-convergence；正文仍由设计宪法独占 |
| boundary-and-decision | applicable | 专用只读复审与普通active preparation分离；保留ARCH-DOM-002/013/015，新增边以唯一consumer闭合 |
| owner-and-single-writer | applicable | Branch Review独占复审，Publication独占payload语义，Finalizer独占archive continuity与handoff，Merge独占最终merge；只读profile零业务/远端writer |
| compatibility-and-exit | applicable | 新profile/exit独立schema，原profile不放宽；旧gate不升级为pass，不保留legacy shim，原输入消费者继续按原合同工作 |
| gap-and-deviation | applicable | 不关闭ARCH-GAP-006/008，不扩大#398/#419生命周期；修复#418归档复审缺口，无退出双写或scope ledger回潮则拒绝 |
| parallel-scope | applicable | 实施限 task-isolated 范围；shared current 仅由 promotion owner 提升，禁止修改业务 task 状态或替其它 task 重建 mapping |
| evidence-and-freshness | applicable | 规划内容、current authority、完整候选或committed range绑定；test证明A/H、snapshot和零mutation，未运行不得写verified |
| review-and-promotion | applicable | 本贡献经上述完整 committed range 审查后由原 owner 提升；promotion diff 仍须重复 Phase 2/Commit/Review |

## ADR 承接

原 task-local `ADR-418` 草案已由 [accepted ADR-010](../adr/010-archived-review-authority.md)
承接。该文档独占决策、替代方案及代价，本贡献不保留第二份 current 决策正文。

## Project Check 与提升

沿用 `guru-trellis-architecture-convergence:repository:1` descriptor 与原项目 change contract；
九项 concerns 均适用，原 `ARCH-GAP-006/008` 状态和 single-writer 不变。
提升前完整审查和 fresh 301 package tests、installed/focused 证据见
[EVD-028](../evidence/current-evidence.md#evd-028-418-reviewed-promotion-source)，不是新 diff 的重复验证声明。
RDT 由其独立 owner 将 R418/D418/T418 纳入 `.53` 并保持双向 trace。

Native 语义执行、原业务实例与 Release 矩阵仍未验证。新 authority 内容必须再经过 fresh
Phase 2、task commit 和独立完整 Branch Review，之后才可进入 Publication/Acceptance。
