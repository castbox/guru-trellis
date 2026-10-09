# #466 设计规划

## 1. 当前 authority 与直接演进

绑定 `guru-maintain-architecture-baseline:2.0`、`docs/architecture/README.md` / `current-main-0.6.17-guru.76` / active、`guru-trellis-design-constitution-v1` / current、`guru-trellis-architecture-change-contract-v1`、`guru-trellis-architecture-change-concerns-v1`。

选择 `target_native`：在唯一原则 owner 内直接完善解释，沿现有 semantic gates 和回程消费。五项 identity/short name、公共 Skill/profile/exit/schema identity、runtime 判断边界保持原合同。不存在双读、兼容 adapter、第二审批链或通用复杂度机制。

原则具体正文在实现阶段形成 task-isolated proposed amendment，交给原 Architecture promotion owner；当前 canonical authority 在独立 review 前保持不变。候选 amendment 只承载待晋升增量、明确标为 proposed/non-current，不复制五原则正文或冒充 current；promotion 消费后移除候选副本，历史由贡献与 Git 承接。

## 2. Owner 与修改范围

| Owner / source | 变更职责 |
| --- | --- |
| `docs/architecture/00-foundation/design-constitution.md` | promotion 时承接 R466-01/02 的原则正文与唯一解释；实际正反例集中在其 authority 内。 |
| `docs/architecture/06-governance/change-contract.md` | constitution-binding、项目检查和现有回程消费；只引用 identity 与适用结论，不复制原则正文。 |
| `trellis/skills/guru-team/packages/guru-maintain-architecture-baseline/references/contract.md` | 核对 current authority，对真实 necessity conflict 使用已有路径。 |
| `trellis/skills/guru-team/packages/guru-check-task/references/contract.md` | 完整候选的语义消费；现有新增 task-local consumer 检查扩展为读取当前原则适用结论。 |
| `trellis/skills/guru-team/packages/guru-review-branch/references/contract.md` | exact committed full diff 独立消费 current authority；不复用 Phase 2 pass。 |
| 上述 package 的示例/evals/tests | 中立候选事实与当前路由结果；不复制项目原则正文、不制造规则评分器。 |
| preset installer | 从 canonical 生成 installed/shared/Codex/Claude/Cursor 投影，reapply 后检查 drift/sidecar。 |

`SKILL.md`、全局 workflow、overlay、schema 和 script 只在 current source 的消费遗漏有具体证据时作必要同步；不存在遗漏时保持原内容。全局 workflow 只编排现有出口，不能新增 step-local 判据。任何新增 owner/public I/O 或范围扩张先回现有 qualification/Architecture owner。

## 3. 当前路由与唯一 consumer

| 语义观察 | 原有回程 |
| --- | --- |
| 当前 Requirement 必要，候选机制多余 | 原 candidate owner 完成 qualification 后，`mechanism_revision_required` 经现有 mechanism router 回设计/实现 remove/replace；重跑资格与受影响 gates，不改变需求 scope。 |
| Requirement 只有未知未来依据，与 current 宪法冲突 | `guru-maintain-architecture-baseline:architecture_conflict` -> `guru-architecture-baseline-planning-router` -> 当前 Planning owner；需要修改 source scope 时进入 `guru-clarify-requirements`，取得新 live authority 后重审。 |
| 缺适用合同/必要性证据 | Architecture 的 `contract_incomplete` -> 同一 Planning/repair router；证据缺口或真实意图选择由既有澄清/blocked 承接，不作关键词拒绝。 |
| Phase 2 scope/authority 改变 | `guru-check-task:planning_stale` 的既有 Planning consumer；当前 finding 修复走 `implementation_required`。 |
| Branch Review 当前 finding / 真实 scope choice | 分别使用 `implementation_required` / `scope_confirmation_required` 及现有 consumer，重审完整范围。 |

具体包只定义自身消费及回程，Architecture owner 的判断不会转移给 checker。Planning/Phase2/BranchReview 的 profile->owner 分别为 `planning_scenario_set`->`guru-approve-task-plan`、`phase2_candidate_set`->`guru-check-task`、`branch_review_candidate_set`->`guru-review-branch`。实现前重新核对 current Interface 的唯一映射；不新增外部 exit 或自动 Issue mutation。

## 4. 六类证据

| Case | 正常候选与语义结果 |
| --- | --- |
| C466-01 | 当前 Requirement、consumer、触发与 Acceptance 完整的能力被接受；抽掉必要职责后违反当前合同。 |
| C466-02 | 仅未来灵活性支持的字段、状态、接口、配置及扩展容器被拒绝进入当前实现；当前必要功能 scope 保留。 |
| C466-03 | 真实已发布 consumer 或当前迁移路径的 compatibility 被接受，验证 owner/依赖/边界/退出删除条件；缺当前依赖的未来预留不被包装为 compatibility。 |
| C466-04 | future candidate 只记录边界，不产生当前字段、Schema 或实现分支。 |
| C466-05 | 已批准 Requirement 含投机内容：回 source/Planning revision；不能执行者删 scope，也不能继续 pass。 |
| C466-06 | 当前职责隔离/可维护性合同支持的抽象被接受；未知未来抽象被拒绝；功能绿测不替代全部适用合同。 |

例子是候选事实与可审核结论，不是第二份原则表。Python 测试只校验 fixture shape、现有 route 和投影完整性；语义 review/eval 才判断候选必要性。无 forged artifact 或故意绕过案例。

## 5. Architecture contribution 与 promotion

Task contribution：`docs/architecture/contributions/466-no-speculative-extension.md`，当前为 Planning draft。九项 concern 的适用性、单 writer、before/after 与 expected-current 由该贡献拥有。无新增 architecture decision、原则例外、GAP/owner/compatibility exit 变化，因此不创建 ADR；若实现发现真实 decision 变化，回 Planning 明确当前依据。

先完成 task-isolated candidate 与定向验证；在已提交完整范围上执行独立 Architecture/Branch Review；Architecture owner 重读 live expected current、constitution content identity 和 reviewed contribution，串行 promotion。若 current 已推进，走 `sync_required` 重新对齐同一任务，不覆盖新 authority。promotion 形成 successor current 版本，更新 authority 导航及最小 RDT/spec 投影；版本在当时 live current 上决定。其新 diff 必须 fresh Phase2 Architecture/check、Task Commit 和不同 reviewer 完整 Branch Review，才进入 Delivery。

## 6. Docs SSOT Plan

策略：`ssot_first`。本轮规划只写 task 与上述 contribution。实现阶段在 `docs/requirements-design-test-contributions/466-no-speculative-extension/` 写唯一 requirements/design/test/traceability 增量，以 R466 -> D466 -> C466 引用 current authority；Test 持有唯一实际验证结果。Architecture promotion 后，通过原 RDT owner 同步当前 successor 的三层引用及 Architecture inheritance。

持久规则只在 constitution/change-contract/package 原 owner 上修改；`.trellis/spec` 只更新 locator/version/消费，不抄正文。canonical 改动通过 `apply.sh` 投影到 dogfood，处理每个真实 sidecar；所有 gate/授权不新建 tracked 证明文件。Future candidates 不生成公共字段、checkpoint 或审计评分表。

## 7. 风险与回滚

风险是把必要抽象误判为多余、把 approved scope 自行删掉、fixture 复制正文，或 promotion 后复用旧 gate。六类证据及 fresh stage 独立判断直接覆盖这些风险。回滚由 reviewed diff 和 authority predecessor 历史承接，不增加长期 adapter；不得改写旧验证结果或宣称 Release/生产安装通过。
