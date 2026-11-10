# 正常续接查询的来源、拟写目标与追踪

Task：`resume-step-context`，generation 0；Delivery：`a2df31bc-2082-48ce-acba-545c8a6adb3b`。本目录为 delta_first 隔离贡献，状态 proposed。仅新增两项查询的三层完整单元；不复制既有生命周期正文、不修改共享 current/root/index、不记录用户授权。

## 适用来源与替代边界

- 固定工程及适用 RDT/Architecture 内容基线：Git `26630149070e2988ad08102679931468b3535ef8`。既有三层 `docs/{requirements,design,test}/current/task-delivery-lifecycle.md` 的 R531/R657/R679/R694/R713、D/T 对应职责均保留；新增单元只拥有查询行为及其验证，不接管绑定、选择、恢复或阶段门禁。
- 整体 accepted scope：`.trellis/tasks/11-10-resume-step-context/prd.md`，revision `sha256:d114009e2d13a01ef3a8151dd0cc2cabd737945bf5e41755e97d297d6bdb84fe`，R1～R9、AC1～AC7。D1 计划位于 `.trellis/tasks/11-10-resume-step-context/deliveries/a2df31bc-2082-48ce-acba-545c8a6adb3b/` 的 `prd.md`、`design.md`、`implement.md`；本贡献消费其中完整两查询设计和 Docs Plan，不修改原计划或 Task 状态。
- 本次读取公共 Task record 时 D1 为 implementing，planning result 为 `planning-accepted:4a700d88-5840-4b7a-af02-ae9dffb0d72e`；它定位已发生的 Activation，不是本贡献的实现或验收证明。历史计划中的待审批措辞保留其原观察，不由此重跑 Approval。
- 精确 API 继续由 canonical `trellis/skills/guru-team/packages/guru-ensure-task-checkout/` 的 Interface/schema、`trellis/skills/guru-team/runtime/discovery.py`、`runtime/installed.py`、原 discovery shell 和 `trellis/workflows/guru-team/workflow.md` 拥有。本文描述批准目标，不据尚未验证的实现补造事实。
- Architecture 复用 D1 内原 `architecture-contribution.md`；其原 baseline、target_native、独立检查与晋升责任保持，本目录不另写 Architecture 或 ADR。

## 完整拟写定位

| 本目录完整正文 | 晋升目标 | 稳定身份与关系 |
| --- | --- | --- |
| requirements.md | docs/requirements/current/resume-step-context.md | RDT-REQ-RESUME-CONTEXT；RSC-R1～R5／BEH；关联既有 RDT-REQ-LIFECYCLE，不替代 |
| design.md | docs/design/current/resume-step-context.md | RDT-DES-RESUME-CONTEXT；RSC-D1～D5／CON；关联既有 RDT-DES-LIFECYCLE，不替代 |
| test.md | docs/test/current/resume-step-context.md | RDT-TST-RESUME-CONTEXT；RSC-T1～T6；关联既有 RDT-TST-LIFECYCLE，不替代 |

上述是新查询能力的完整 resulting definitions，不是待实施摘要；没有删除、重命名或替换现存稳定 identity。各层正文自身保留别名、状态、来源和必要跨层关系；普通发现沿既有 current 目录合同，不向共享 README/index/全局版本另登记。晋升前同目录三份正文是 proposed 对象，目标路径尚未因本贡献生效。

| 整体要求／AC | 需求 | 设计 | 测试 |
| --- | --- | --- | --- |
| R1/R2、AC1 | RSC-R1 | RSC-D1 | RSC-T1 |
| R3/R7、AC2 | RSC-R2/R5 | RSC-D2/D5 | RSC-T2 |
| R4/R5、AC3/4 | RSC-R3 | RSC-D3 | RSC-T3/T4 |
| R5/R6/R8、AC5 | RSC-R4/R5 | RSC-D4/D5 | RSC-T3/T5 |
| R7/R8/R9、AC6 | RSC-R5 | RSC-D5 | RSC-T2/T5 |
| R2/R9、AC7 | RSC-R5 | RSC-D4/D5 | RSC-T6 |

## 原 owner 后续消费

RDT `task_impact_sync(stage=phase2)` 的 `candidate_ready` 经原 `guru-requirements-design-test-ssot-current-router` 交候选检查，仅传 contribution/authority locator 和适用 authority version。它不晋升、不产生 Check 或 Architecture pass，不推进 Task/Delivery。

implementation 将完整实现、本目录拟写和既有 Architecture contribution 纳入原 candidate/begin_check；独立 Architecture 及原 candidate Check 分别判断。实际 `candidate_checked` 后，原 RDT/Architecture 在各自 final_integration 固定真实目标，重读完整拟写及命中 authority，协调并发条件，写入并读回。真实冲突、来源或义务变化回原 owner，不覆盖他人差额。随后 implementation 纳入所有 after 内容重新绑定候选，最终 Check、完整 committed Review 和原交付/Completion 链另行完成。当前实现、测试、安装、原生效果均保持待验证。
