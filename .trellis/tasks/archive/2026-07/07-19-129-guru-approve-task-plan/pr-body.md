## 变更摘要

- 新增并注册 semantic closed-loop Skill `guru-approve-task-plan`，成为 planning adequacy、requirement provenance、非常规场景专用确认和 `planning-approval.json` 的唯一 step-local owner。
- 将 planning approval evidence 演进到 schema `guru-planning-approval-2.0`，统一 workflow/standalone entry preconditions、AI Review Gate、conditional human confirmation、recorder/validator 与四个 typed exits。
- 为所有 load-bearing planning contract 引入 `explicit_requirement`、`necessary_implementation_choice`、`approved_scope_expansion`、`out_of_scope_proposal` 四类 provenance，并让未确认 proposal fail closed。
- 修复 `approved_scope_expansion` 的 exact proposal digest 绑定：proposal、专用确认和 current requirement authority 必须绑定同一 digest，validator 同时复验 authority ref/SHA 与 freshness。
- 将 canonical package、shared installed runtime、`.agents`、Codex、Claude、Cursor 分发以及 durable Docs SSOT、preset/update/reapply 和回归测试同步到同一合同。

## 影响范围

- Skill 公共 API：新增 `guru-approve-task-plan` package、interface、contract、schema、examples、recorder/validator wrappers 和 package tests。
- Workflow 与 runtime：Phase 1 收敛为 stable Skill mandatory invocation 和唯一 typed-exit routing；shared runtime 只记录、重算和校验确定性事实。
- Downstream：requirements clarification、change-request review、task commit 与 planning consumer 适配 schema 2.0 和新 exit 合同。
- Preset 与平台分发：canonical、installed shared、`.agents`、Codex、Claude、Cursor 五根副本保持一致；Issue #132 冻结的 43 个 upstream-owned overlay 路径未变。
- Durable docs：requirements、workflow/preset/docs specs、根 README、workflow README 和 preset README 已同步 semantic owner、provenance、confirmation、typed exits、migration 和 update/reapply 合同。
- 部署资产：未修改 GitHub Actions、Docker/Compose、Kubernetes/Kustomize、数据库 migration、Makefile 或生产运行时配置，不需要部署迁移或回滚步骤。

## 验证结果

- 完整五模块回归：645/645，exit 0；final reviewer 独立复跑耗时 189.385 秒。
- P1 exact digest binding 与 package 定向测试、planning/Phase 2/dogfood 定向测试：55/55，exit 0。
- Full local-unpublished throwaway：exit 0，覆盖 fresh init、workflow preview/switch、preset apply、官方 `trellis update` 后 reapply、installed validation、closeout harness 与零 sidecar。
- Source/installed package validation：8 个 active Skills、31 个 exits、17 个 targets、343 个 managed files；43/43 ownership、dogfood drift、canonical/dogfood byte equality、JSON/Bash/Python、task/commit validators 与 `git diff --check` 均通过。
- Reviewed content push 后由 finish-work transaction 执行远端 exact feature-ref marketplace verification；本地 throwaway 不替代该发布门禁。

## Review Gate

- Branch Review Gate 绑定 `e06184716f8e973335b527667b49788ff74b112f`，覆盖 `origin/main...HEAD` 的全部 128 个路径。
- Fresh 独立 `最终放行审查代理` 核查 Issue #129、planning、Docs SSOT、implementation handoff、`phase2-check.json`、P1 exact digest、schema/runtime/workflow/package/tests、五根分发、upgrade/update 和部署安全影响。
- P0/P1/P2/P3 findings 均为 0；raw report、`review.md`、agent assignment 和 gate digests 已绑定并由 `check-review-gate.sh` 校验通过。

## Issue 关闭范围

Closes #129

Related: Refs #127, #128, #114, #112。

Follow-up: Refs #130, #131, #132；本 PR 不关闭这些独立后续交付。

## Docs SSOT

- 策略：`ssot_first`。
- Durable docs：`docs/requirements/**`、`.trellis/spec/workflow/**`、`.trellis/spec/preset/**`、`.trellis/spec/docs/**`、根 README、workflow README 和 preset README 是长期主定义。
- Task delta 合并：semantic owner、四类 provenance、非常规场景 dedicated confirmation、schema 2.0 migration、四 typed exits、五根分发及 update/reapply 合同已回写长期文档。
- Task history：planning、approval、sub-agent liveness、Phase 2、raw/final review 和执行时间仅保留为任务历史证据，不形成第二套公共合同。
- Follow-up / 限制：当前 PR 唯一发布期限制是 pushed feature ref 的远端 marketplace verification；该证据由 finish-work transaction 生成、校验并绑定，#130/#131/#132 继续作为独立 issue 交付。

## 安全说明

- 未发现 token、secret、credential、private key、签名 URL、`.env`、数据库 URL、客户数据或敏感原始记录。
- 公共 Skill package、schema、example、manifest 与文档不包含真实本机绝对路径；task-local worktree path 仅作为 workspace-boundary 审计证据。
- 本次实现遵循正常诚实协作边界，不新增 hostile-input、anti-tamper、并发竞态、TOCTOU、锁、fault injection 或跨 OS 原子性机制。
- 无网络服务入口、数据库迁移、容器镜像、Kubernetes 资源或生产配置变化。
