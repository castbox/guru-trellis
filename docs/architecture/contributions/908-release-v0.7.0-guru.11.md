# #908 v0.7.0-guru.11 发布知识收敛：Architecture 隔离贡献

Identity：`architecture-contribution-908-release-v0.7.0-guru.11-v1`。状态：`integrated_pending_review`。所属 Task 为 `release-v0.7.0-guru.11` / generation 0，Delivery 为 `7fa61b67-258e-49db-9db3-505f1a0c4e3e`。固定 before 为 Git `2acab7fadebf57c2f2560451b9ff2a050d8811f5`。来源为 [Issue #908](https://github.com/castbox/guru-trellis/issues/908)。

当前观察状态：Task 公共 Planning 已 accepted，Delivery 已 Activation 并进入过 checking；初始 independent committed Branch Review 返回 `implementation_required`，F1–F4 仍 open，当前 phase 为 `implementing` rework。该 Review 没有通过，本贡献也没有成为 `reviewed_promoted`。以下第 2–4 节保留 planning 时拟同步、拟调整和拟晋升措辞；其观察截止均为 Activation 前，当前状态以本段和第 7 节为准。

独立 Planning candidate assessment 已返回 `baseline_current / architecture_impact`，change path 为 `target_native`，decision refs 为 `ADR-POSTCOMMIT-INDEPENDENT-REVIEW`、`ADR-024`、`ADR-034`。原 Architecture owner 已在真实工程结果后执行 final integration、写入、readback 和适用性检查；该整合事实只记录为 `integrated_pending_review`，不建立 `reviewed_promoted`。

## 1. 问题与目标

当前 public registry/workflow 已由 `guru-review-branch` 一次完成独立 Check 和完整 Branch Review，通过后由 `guru-publish-task-delivery` 承接 readiness、PR payload、预览和发布。`guru-review-task-delivery` 已从当前 registry/workflow 退出。

若仍把独立 `Delivery Review` 写成 current owner，就会让 Architecture、RDT/Test 和仓库私有 release 合同继续指向不存在的阶段。Planning 时 `ADR-POSTCOMMIT-INDEPENDENT-REVIEW` 仍为 `proposed`，但多个 current consumers 已依赖它的决定；该观察截止于 Activation 前，当前 ADR 已收敛为 accepted/current。本贡献收敛这两类 authority 冲突，不改变已接受产品范围、Task/Delivery 身份、发布候选或历史结果。

## 2. 目标与不变边界

本贡献拟同步以下 current units 和 decision authority：

- `docs/architecture/01-current/system.md`：`ARCH-CUR-051`。
- `docs/architecture/03-domains/ownership.md`：`ARCH-DOM-036`、`ARCH-DOM-055`、`ARCH-DOM-059`。
- `docs/architecture/04-integrations/distribution.md`：`ARCH-INT-015`、`ARCH-INT-020` 和 ADR-status observation。
- `docs/architecture/06-governance/rules.md`：`ARCH-GOV-009`。
- `docs/architecture/adr/postcommit-independent-review.md`：决定 4、窄替代责任句、当前状态和观察截止。

实施中必须复核但不一定修改以下 ADR consumers：

- `docs/architecture/README.md`
- `docs/architecture/01-current/system.md`
- `docs/architecture/03-domains/ownership.md`
- `docs/architecture/03-domains/workflow-context.md`
- `docs/architecture/04-integrations/distribution.md`
- `docs/architecture/06-governance/change-contract.md`
- `docs/architecture/06-governance/rules.md`
- `docs/requirements/current/knowledge-maintenance.md`
- `docs/design/current/knowledge-maintenance.md`
- `docs/design/current/task-delivery-lifecycle.md`
- `docs/test/current/knowledge-maintenance.md`

历史 `ARCH-CUR-032`、旧 #435 阶段描述、历史 contribution、roadmap 和 evidence 保持原身份。它们只解释历史阶段，不继续声明当前 owner。

## 3. 七个 current Architecture units 的拟调整

### ARCH-CUR-051

将“Planning、原维护单写、Delivery Review/readiness和终态不变”改为“Planning、原维护单写、Publication readiness/execute 和终态不变”。保留提交后一次独立 Architecture before/after、九维 Check 和完整 Branch Review 的范围、独立 reviewer 要求及终态职责。

### ARCH-DOM-036

将“Delivery Review 审 payload、Publish 执行”改为“Publication readiness 审 payload、剩余责任和真实证据，Publish 执行”。保留共同因果语义单写、Completion、Closure、Finish 及 unknown production effect 的处理边界。

### ARCH-DOM-055

将当前阶段列表“Approval、实施、Check、Delivery Review 与 Completion”改为“Approval、实施、Check/Branch Review、Publication readiness/execute 与 Completion”。保留 Author、Discovery、Clarify、Architecture、RDT/Architecture single-writer 和普通遗漏回程。

### ARCH-DOM-059

将当前 owner 列表中的 Delivery Review 改为 Publication readiness。保留 Architecture/Check/TaskCommit/Branch Review 覆盖、后继独立审查、工程事实采用、official API single-writer、public DTO 和终态职责。

### ARCH-INT-015

将 repository-private release 链中的 `publication Architecture eligibility/Delivery Review readiness -> Publication` 改为：

```text
publication Architecture eligibility -> guru-publish-task-delivery readiness -> Publication preview/confirmation/execute
```

保留 TaskCommit、固定 B..H、一次独立完整 Review、Merge、Completion、D1/D2 顺序和禁止 early Draft/source-only TaskCommit 的边界。

### ARCH-INT-020

将旧 `Delivery Review reviewed payload -> Delivery Publish` 投影改述为 `Review 后的 Publication readiness result -> guru-publish-task-delivery`。保留 #900 的 current edge、Publish 的 readiness/准确预览/确认执行责任、Merge 的 expected-head 和 Delivery fact 职责，以及 #435 历史边保持 deferred 的事实。

### ARCH-GOV-009

将首个 current owner 判断改为 Branch Review 通过后由 `guru-publish-task-delivery` 同时判断 readiness、真实 PR payload、剩余准备/发布责任和 reviewed-content identity，再展示精确预览并在当前确认后执行发布。保留 Merge、Completion、Closure、Finish、Cleanup 和 reference-only/closing-keyword 边界。

## 4. ADR-POSTCOMMIT-INDEPENDENT-REVIEW 的拟晋升定义

保留 #794 原 Task/Delivery attribution、问题、决定 1–3、5–6、证据、窄替代范围和重评条件。必要调整如下：

1. 决定 4 保留 #794 对 TaskCommit、pre-review commit、独立提交后 Review 和无 early Draft 的决定，但把旧的“Delivery Review 完成并记录 readiness、Publication 只消费 ready”标记为已被 R900/D900 与 #900 窄替代。当前由 `guru-publish-task-delivery` 完成 readiness、中文 Refs-only payload 和精确预览，独立确认后执行发布。
2. “窄替代与保持”中的“Planning candidate/final、Delivery Review、Publication、Completion、Closure、Finish保持各自责任”改为当前责任：“Planning candidate/final、Publication readiness/execute、Completion、Closure、Finish 保持各自责任”。
3. “验证与重评”中的“当前只有候选方案，无实现或发布 pass”改为明确的 #794 观察截止；后续事实由 R900/D900、实际 committed Review、Publication 和 Release 原结果承接，ADR 不追写最终 pass。
4. 状态由 `proposed` 改为 `accepted`。删除“本候选尚未成为共享 current，不能据此跳过当前安装门禁”的当前自述，保留 #794 历史 Task/Delivery 来源。

原 Architecture owner 已比较完整 before、本贡献、实际 current 和 11 个 consumer，并完成写入/readback；当前只能记录 `integrated_pending_review`。初始 committed Branch Review 已返回 `implementation_required`，尚未建立 `reviewed_promoted`。

## 5. RDT/Test 关联

原 RDT owner 同步 `docs/{requirements,design,test}/current/task-delivery-lifecycle.md`、Requirements/Design `knowledge-maintenance.md`、Requirements/Design/Test `completion-closure.md` 与 Test `runtime-location.md` 的命中 current 正文。本贡献不复制其需求、设计或测试定义，只消费其与 Publication readiness、ADR status 和 current consumer 的必要关系。

`T669-06` 与 `#813` 只更新当前阶段名称，保持原观察、证据截止和未验证边界。历史版本结果不改写。

## 6. 迁移、错误处理与并行边界

本变更直接更新既有 current units，不建立 legacy adapter、旁路 reader 或第二 authority。`target_native` 不保留 dual-read。当前错误或旧阶段只按原 public owner 和相关 migration 合同恢复；本贡献不改变 workflow、schema、Skill API、Task 生命周期或远端发布动作。

并行范围仅为本 Task 的隔离贡献及 D1 规划。其他 Task、shared current、无关导航、全局版本和 GAP 不进入本贡献。final integration 遇到 intervening change 时，由原 owner 重读完整目标并语义整合；无法唯一确定时停止，不覆盖他人写入。

## 7. Project check 与证据边界

`guru-trellis-architecture-convergence@1` 已由独立 candidate assessment 判断 applicable、blocking、pass。该判断只属于 candidate assessment 事实，覆盖当时的 authority binding、七个 current units、ADR promotion、11 个 consumer 和 candidate design。其规划时观察截止于 Activation 前：当时它没有产生 final_plan、Approval、Activation 或 committed Review 结果，最终 planning eligibility 尚须由 current final_plan 独立判断；当前可观察状态见本段末句。

上述 candidate assessment 本身不证明最终整合、TaskCommit 或 committed Review 结果。独立观察到的当前事实是 contribution/current 已写入并 readback、TaskCommit 已形成待审 H、初始 committed Review 返回 `implementation_required`；它没有通过。Rework 后的后继内容仍需原 writer、TaskCommit 和受影响 Review 重新承接。Publication、Merge、tag、Release 和本地采用仍分别由其原 owner 的结果承接。
