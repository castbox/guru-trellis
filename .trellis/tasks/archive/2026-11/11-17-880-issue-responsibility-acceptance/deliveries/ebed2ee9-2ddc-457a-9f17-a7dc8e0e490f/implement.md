# #880 Issue 责任层与验收场景收敛实施计划

## 1. 输入与引用

- 整体范围：[Task PRD](../../prd.md) R1–R7、AC1–AC2。
- 本批需求：[Delivery PRD](prd.md) D1-R1–R7、D1-AC1–AC2。
- 唯一来源设计处置：[design.md 第3节](design.md#3-来源设计处置唯一)。
- 规范正文：`trellis/skills/guru-team/packages/guru-clarify-requirements/references/issue-content.md`、`trellis/presets/guru-team/spec/workflow/quality-guidelines.md#test-and-validation-value`。
- 现有消费者与 fixture：`guru-review-change-request/references/issue-intake.md`、`guru-create-issue/SKILL.md`、`evals/files/issue-acceptance-boundary-source.json`、`evals/evals.json`。
- RDT current 与 contributions：`docs/{requirements,design,test}/current/{issue-content,behavior-validation-method}.md`；新增 `docs/requirements-design-test-contributions/880-issue-responsibility-acceptance/`。
- Architecture：formal candidate result `no_architecture_impact/no_change`，baseline=`guru-trellis-architecture`，constitution=`guru-trellis-design-constitution-v1/current`。

实施前完整读取上述规范正文、现有 fixture、RDT current 和原安装合同；不把本计划摘要替代正文。

## 2. 有依赖顺序的步骤与文件责任

**I1 更新 Issue 内容规范与教学例。** Owner：`guru-clarify-requirements` package。

- 修改 `trellis/skills/guru-team/packages/guru-clarify-requirements/references/issue-content.md`：在原“验收切面与必要结果”段落加入可组合责任层、目标环境/共享环境/服务部署/业务发布区分、场景集合独立风险与去重。
- 修改 `trellis/skills/guru-team/packages/guru-clarify-requirements/examples/issue-content/acceptance-boundary/process.md`：保留现有组件/CLI/内部 load 时机场景，增加目标环境正例和业务“发布配置”非部署。
- 不复制整套规则到 Clarify/Readiness/Create Issue；现有薄引用继续作为原 owner 入口。
- 完成观察：完整正文语义连贯，结果/证据/场景单一来源清楚，无新增公共字段或 owner。

**I2 窄化跨阶段验证边界。** Owner：workflow quality guideline。

- 修改 `trellis/presets/guru-team/spec/workflow/quality-guidelines.md#test-and-validation-value`：在现有责任边界/最小证据段补目标环境、共享环境、服务部署和业务发布责任；不复制 Issue 场景定义。
- 保持 `review-sufficiency.md` 薄引用、现有 review owner 和停止条件。
- 完成观察：新增表述只有跨阶段必要语义，不形成 per-test 理由或新 Gate。

**I3 扩展现有内容验收 fixture。** Owner：`guru-review-change-request` eval。

- 修改 `trellis/skills/guru-team/packages/guru-review-change-request/evals/files/issue-acceptance-boundary-source.json`：增加有效目标环境结果、业务发布命令及“逐 Issue 部署/重复场景”的无依据建议。
- 修改同 package `evals/evals.json` 的两个语义 criterion：保留必要 target-environment/business-publish 区分，并拒绝把业务发布推导为部署、拒绝同一行为按阶段/方法重复。
- 不新增 eval 平台、runner 或预期泄漏。
- 完成观察：同一 fixture 仍能驱动原 standard-intake 路径，且正反边界均由事实和独立判断覆盖。

**I4 补齐受管分发覆盖。** Owner：preset distribution test。

- 修改 `trellis/presets/guru-team/scripts/python/test_issue_content_distribution.py`，把现有 `acceptance-boundary` 教学示例加入真实 writer/reapply 资产集合。
- 保持用户文件、声明平台、links、零 sidecar 断言。
- 完成观察：canonical 正文/示例和所有声明平台 projection 字节一致。

**I5 创建并整合 RDT proposal。** Owner：`guru-maintain-requirements-design-test-ssot`。

- 新增 `docs/requirements-design-test-contributions/880-issue-responsibility-acceptance/{manifest.yaml,requirements.md,design.md,test.md,traceability.md}`，状态先为 proposed；完整 proposed targets 指向 `docs/{requirements,design,test}/current/issue-content.md` 与 behavior-validation 三文档。
- 实现和真实工程结果可用后，由原 RDT owner 读取完整 target，按 `delta_first` 整合 R880/D880/T880 关系，保留既有 R153/R818/R868/R735/R868-04 条件，写入并 readback；状态更新为 `integrated_pending_review`。
- Architecture no impact，不创建 architecture contribution/ADR。

**I6 同步 dogfood/平台投影。** Owner：`guru-upgrade-tools`/原 installer。

- 从完整 matching candidate 执行 preview→prepare→invoke→readback/reapply，同步 `.trellis/`、`.agents/`、`.claude/`、`.cursor/` 等受管副本。
- 保留 Task/session、用户内容、配置、peers 和缺失的 `.new/.bak` 处理语义。
- 运行 dogfood drift/installed/native 定向检查；不手工覆盖受管副本。

**I7 更新 official context manifests。** Owner：`guru-author-task-plan` + official task.py。

- 用 `.trellis/scripts/task.py add-context <task_ref> implement|check <file> <reason> --delivery <uuid>` 加入本计划实际需要的规范、fixture、RDT 和 Architecture 文件。
- 实施完成后，check context 只补独立 committed review 所需完整来源与验证方法；不复制正文。

## 3. 验证入口、输入与预期观察

**V1 真实 Agent 语义行为。** 入口：现有 `guru-review-change-request` native eval case `standard-intake-authoring-acceptance-boundary` 或同 package 原 runner。输入：更新后的 fixture，不得向执行 Agent 注入预期。观察：原 Clarify/Readiness完整正文处理保留组件/CLI/目标环境承诺，删除消费方整站 E2E、共享 test 部署、业务发布误推部署及重复 Agent 场景，最终原 public output 与 criterion 一致。证据为完整 transcript、工具 receipt 和独立 grade，不是关键词。

**V2 Eval 发现与 package 合同。** 入口：

```bash
python3 -m unittest trellis.skills.guru-team.packages.guru-review-change-request.tests.test_contract
python3 -m unittest trellis.skills.guru-team.packages.guru-review-change-request.tests.test_runtime
```

预期：eval corpus JSON/shape、现有 runtime 合同和 case discovery 通过。若环境入口不同，使用 package 已声明测试入口，不以修改被测 Skill 消除设施错误。

**V3 分发与 reapply。** 入口：现有 real writer tests：

```bash
python3 trellis/presets/guru-team/scripts/python/test_issue_content_distribution.py
python3 trellis/presets/guru-team/scripts/python/test_review_sufficiency_distribution.py
```

输入：与该 checkout 匹配的实际 Trellis CLI/dist/templates/scripts。预期：所有声明平台 bytes、示例、owner links、用户保留、reapply、drift、零 sidecar 通过。仅证明分发/结构。

**V4 本 checkout 受管采用。** 入口：原 `guru-upgrade-tools` 完整 candidate flow。预期：tools/workflow/preset/skill/projections 与 canonical 一致，installed/native/validation/drift 通过，Task/session/配置/peers 保持，`unverified` 边界如实记录。`local_candidate` 不证明正式 source lock 或 Release。

**V5 工程完整性。** 入口：实际变更 package tests、Guru source/installed validation、JSON、bash、Task context、canonical/installed drift 和 `git diff --check`。只补受影响差额，不运行完整多平台矩阵或 Release。

## 4. 停止条件与适用回退点

- 需要改变产品目标、责任层或验收场景时回原 Clarify；Author 不静默补语义。
- 需要新增 public schema/DTO/typed exit/runtime state、第二验证 source 或架构责任时回 Author/Architecture candidate assessment。
- fixture/native runner 的设施失败与产品失败分开；保留失败，修复真实装配缺口或改用能回答同一问题的原入口，不弱化语义断言。
- Evidence 已充分证明对应行为、引用和分发时停止追加实验；不因更换阶段、reviewer 或会话重跑无变化检查。
- 受管同步冲突、sidecar、dirty unrelated/peer 不匹配时停在原 installer/tools owner 恢复，不手改 manifest、覆盖用户文件或 reset/checkout。
- 没有数据库、服务、部署或持久化状态变更，因此没有对应回滚协议；Git/PR 发布仍按原副作用边界。

## 5. Delivery Policy（唯一）

Policy=`full`。本 D1 覆盖整体 R1–R7 / AC1–AC2 的全部实现和工程结果，不留下后续 Delivery 责任。完整 Completion 仍要求真实 Agent AC1、分发/本目标采用 AC2 和正式独立 committed Review；Delivery 合并不自动等于 Task Completion。

没有临时能力限制。若 AC1 的真实 Agent runner 在本环境确实不可执行，必须作为明确未验证边界保留，不能以 fixture/stub/静态断言替代整体 Completion。

## 6. Docs SSOT Plan（唯一）

Strategy=`delta_first`。

| 当前 authority | 本批差额 | 原 writer / 直接 consumer |
| --- | --- | --- |
| `docs/requirements/current/issue-content.md` | R880 责任层、环境/发布、场景集合去重 | RDT owner / Clarify、Author、Readiness |
| `docs/design/current/issue-content.md` | D880 原正文落点、owner 薄引用与分发 | RDT owner / planning、review |
| `docs/test/current/issue-content.md` | T880 混合 Agent 与分发验证 | RDT owner / Check、Branch/Delivery Review、Completion |
| `docs/requirements/current/behavior-validation-method.md` | R880 跨阶段环境/部署/业务发布边界 | RDT owner / validation consumers |
| `docs/design/current/behavior-validation-method.md` | D880 质量规则新增的最小边界 | RDT owner / planning/review |
| `docs/test/current/behavior-validation-method.md` | T880 定向测试与复用边界 | RDT owner / Check、Review |

先写 task-owned contribution，真实实现和工程结果后由原 RDT owner 在 TaskCommit 前整合/readback，状态为 `integrated_pending_review`。共享导航无需更新。Architecture candidate 无影响，不生成 contribution/ADR。提交后同一独立 committed Review 审核实际 after；Doc 整合不产生质量 pass。
