# #710：稳定关系、来源与拟晋升边界

## 适用来源及完整目标

适用 before 为完整 Git `2fc49bda6552d1a8bf95dff243ab2de9a9ea8e30`，authority identity 为 `guru-trellis-rdt`；Architecture 公开 identity 为 `guru-trellis-architecture`，入口 `docs/architecture/README.md`，状态 active，适用 before 同 Git。TaskId 为 `710-phase2-recorder-authoring`，generation=0，选定 Delivery 为 `63d55014-9fec-48da-a106-2a7403305977`。

| 来源／用途 | 精确 locator |
| --- | --- |
| 整体 accepted 要求与九条 AC | [Task PRD](../../../.trellis/tasks/10-31-710-phase2-recorder-authoring/prd.md) / §§1–8；[Direct Source #710](https://github.com/castbox/guru-trellis/issues/710) |
| D1 行为、规范性设计处置、consumer/验证与唯一 Docs Plan | [.trellis/tasks/10-31-710-phase2-recorder-authoring/deliveries/63d55014-9fec-48da-a106-2a7403305977/](../../../.trellis/tasks/10-31-710-phase2-recorder-authoring/deliveries/63d55014-9fec-48da-a106-2a7403305977/) 中 prd.md、design.md §§3–9、implement.md §§2–6 |
| 完整 predecessor R/D/T | B 中 `docs/requirements/current/knowledge-maintenance.md`、`docs/design/current/knowledge-maintenance.md`、`docs/test/current/knowledge-maintenance.md`；根导航同 B |
| 精确接口与兼容退出 | [Check contract](../../../trellis/skills/guru-team/packages/guru-check-task/references/contract.md)、其 interface/schema/examples；[MIGRATION-710](../../../trellis/presets/guru-team/MIGRATION-710.md) |
| RDT 维护合同 | [RDT contract](../../../trellis/skills/guru-team/packages/guru-maintain-requirements-design-test-ssot/references/contract.md) / [current-knowledge](../../../trellis/skills/guru-team/packages/guru-maintain-requirements-design-test-ssot/references/current-knowledge.md) |
| 原候选适用性与证据层次 | [workflow-contract](../../../trellis/presets/guru-team/spec/workflow/workflow-contract.md#candidate-applicability-and-coverage) / [quality-guidelines](../../../trellis/presets/guru-team/spec/workflow/quality-guidelines.md#test-and-validation-value) |

三个完整 proposed target 与 manifest 一一对应：[Requirements](proposed/docs/requirements/current/knowledge-maintenance.md)、[Design](proposed/docs/design/current/knowledge-maintenance.md)、[Test](proposed/docs/test/current/knowledge-maintenance.md)。它们完整保留 B 的前驱正文，只追加本批定义。相对链接按最终 target 位置解析；在隔离位置阅读时，本表及 manifest 提供实际映射。没有整体语料迁移或新的 legacy assembly 边界。

## 双向稳定关系

| Requirement / behavior | Design responsibility / contract | Test strategy / scenario | Task AC |
| --- | --- | --- | --- |
| R710-01 / BEH710-AUTHORING | D710-01 / CON710-AUTHORING | T710-01 / SC710-CONTRACT；T710-09 | AC710-01/08 |
| R710-02 / BEH710-CONSUMPTION | D710-02 / CON710-CONSUMPTION | T710-02 / SC710-COMMAND；T710-06；T710-09 | AC710-02/03/05 |
| R710-03 / BEH710-RETIREMENT | D710-03 / CON710-RETIREMENT | T710-03 / SC710-RECOVERY；T710-05 / SC710-INPUT-EXIT；T710-09 | AC710-06/07 |
| R710-04 / BEH710-STALE | D710-04 / CON710-STALE | T710-03；T710-04 / SC710-DIAGNOSTIC；T710-09 | AC710-06/07 |
| R710-05 / BEH710-EVIDENCE | D710-05 / CON710-BOUNDARY | T710-01/02/05；T710-07 / SC710-FINDING；T710-09 | AC710-04/05/08 |
| R710-06 / BEH710-FIRST-NATIVE | D710-06 / CON710-FIRST-NATIVE | T710-06 / SC710-CANDIDATE-FINAL；T710-07；T710-09 | AC710-03/04/08 |
| R710-07 / BEH710-DISTRIBUTION | D710-07 / CON710-ADOPTION | T710-08 / SC710-INSTALL；T710-09 / SC710-FINAL-COVERAGE | AC710-09 |

## 继承、减法与替代

既有 REQ/BEH/DES/CON/TST/SCN 及 R331/R578/R638/R648/R649/R-MECH/R693 的完整定义、否定、例外、顺序、历史和范围全部保留。新 R710/D710/T710 只补其在正常 Check authoring 的具体能力与验证边界，不重编号、不替换其它身份。原完整结果 input 退出是 Check package 的局部 API 变化；其 predecessor/切换/恢复由 MIGRATION-710 和原 Architecture ADR 拥有，RDT 不复制 consumer 清单或自定兼容桥。完整结果 output 和合法消费/恢复未退出。

三个目标的现有入口定位和 authority identity 不变，因此没有 root README/current navigation 拟写或全局版本递增。未命中的 lifecycle、completion、native-compatibility、json-input、local-fix 单元及历史 contributions 不修改；必要最终整合关系已由完整 knowledge 单元保留。

## 候选与最终整合

原 RDT task_impact_sync 在完整实现和本批行为证据齐备后审查提案并调用正式 wrapper；candidate_ready 仅交原 current router，不能证明 shared current 或最终 Check。独立 Architecture 和完整候选 Check 读取全部实施、拟写和受影响未改 consumers。

candidate_checked 后，原 RDT owner 固定真实 target、重读 before/proposed/live current 并比较实际并行差额，保持仍有效条件，实际晋升及 readback 后才返回真实 ssot_current。Architecture 同步由其原 owner 执行。implementation 以同 B 绑定全部 actual after，再由原最终 Architecture/Check 和完整 committed Review 覆盖。当前未执行这些后续操作；实际观察只由 [Test](test.md) 持有。
