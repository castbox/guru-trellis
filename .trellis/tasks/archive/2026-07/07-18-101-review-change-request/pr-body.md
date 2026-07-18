## 变更摘要

- 新增公共 `guru-review-change-request` semantic closed-loop Skill，统一承担 pre-task change request readiness、current/history consistency、duplicate/reuse、delivery unit、findings 与 typed exit 判断。
- 消费 current、checker-validated 的 `guru-discover-change-context:context_ready`、`guru-clarify-requirements:clear`、`guru-review-contract-wording:pass`，并校验 target/content identity、facts/hash linkage 与 freshness。
- 固定 `existing_issue`、`proposed_draft`、`standalone_request` 三类 target、十项 readiness dimensions，以及 `ready`、`clarify_requirements`、`review_wording`、`refresh_context`、`blocked` 五个唯一出口。
- AI 独占 readiness、scope、finding、delivery unit 与 route judgment；recorder/checker 只负责 schema、hash、digest、linkage 和 record/check，不能用 scanner/validator 返回值替代 AI Gate。
- Replacement verification 通过后，删除旧 active `change_request:pass -> guru-full-task-intake-chain` readiness owner；保留 clarification `new_task` 合法 route、三个 prerequisite owner 与 #112 的 task workspace/persistence ownership。
- 同步 canonical workflow/package/runtime/registry/extension、preset installer/inventory、Agents/Codex/Cursor/Claude 与 dogfood 副本、requirements、README 和 durable specs。

## 影响范围

- Workflow：Phase 0 在三个 prerequisite 之后显式调用 stable Skill id，并唯一消费五个 typed exits；unknown、multiple、unmapped 或 missing consumer 均 fail closed。
- Skill/runtime：新增 interface、contract、schema、去敏 example、recorder/checker、production runtime 与完整 regression tests；pre-task 与 standalone 路径保持 stdout-only、repo side-effect-free。
- 下游边界：`ready -> guru-create-task-workspace` 只声明 #112 的稳定 consumer；#112 未实现时按 missing-Skill gate 停止，本 PR 不创建 workspace、task 或 `issue-review.json`。
- 分发与升级：canonical、installed、Agents、Codex、Cursor、Claude 六树 package byte/mode 一致，workflow/runtime/registry/wrappers/schema core copies 同步；fresh install 与 update/reapply 均覆盖。
- Ownership：只新增或修改 Guru-owned canonical/package/runtime/preset/platform assets；43 个 upstream-owned frozen overlays 未变化。
- 不实现 #112、#129、#130、#131、#132，不吸收 #111 的 archived `invalid_index_shape` 修复，也不修改 Trellis upstream、全局 npm 包或 `node_modules`。

## 验证结果

- Canonical Skill package contract/schema：`20/20 passed`。
- Shared production runtime：`508/508 passed`。
- Production package/distribution suite：`71/71 passed`。
- Preset installer：`39/39 passed`；upstream ownership：`6/6 passed`，frozen overlays `43/43`。
- 合计核心回归：`644/644 passed`；最终放行 reviewer 另独立重跑 `508 + 71 + 39 + 6` 并通过。
- 覆盖五 exits、missing/stale prerequisite、unknown/multiple/unmapped exit、三 target、current/history/clarity/wording hash linkage、AI Gate 不可被 deterministic result 替代及 #112 fail-closed。
- Source/installed validators 通过：6 active、1 planned、22 exit markers、248 installed files，sidecar/removal/conflict 均为零。
- 六树 40 个 package bytes+mode comparison 与 6 个 core copy pair 均零差异；dogfood overlay drift 通过。
- Clean throwaway fresh install 与 `trellis update --force` + workflow/preset reapply 两阶段各 `20/20`；最终 `.new/.bak/.pyc/.pyo/__pycache__` 为零。
- Remote branch-pinned marketplace verification 由 `trellis-finish-work` 在 reviewed content HEAD push 后、PR 创建前执行；只有通过后才会创建本 PR。

## Review Gate

- Branch Review Gate 绑定 HEAD `81d9c02099854b90d3ec1a9b575a412992be3834`，覆盖 `origin/main...HEAD` 的 96 个 paths 与完整 task scope。
- Round 1 唯一 `P2-implementation-handoff-evidence` 已由真实 implementation handoff、fresh 完整 Phase 2 与 Round 2 closure 闭环。
- Round 3 使用未参与 finding/closure 的 fresh final reviewer，最终开放 findings 为 `P0=0, P1=0, P2=0, P3=0`。
- 审查覆盖需求清晰度、旧 owner 删除、Docs SSOT、五出口、#112 边界、分发/update、ownership、安全和部署影响。

## Issue 关闭范围

Closes #101

- 仅关闭已由 Phase 2、Branch Review 与发布门禁完整覆盖的 Issue #101。
- #98、#112、#111、#113、#114、#128 仅为关联上下文或依赖，不在本 PR 的关闭范围。

## Docs SSOT / 文档同步

- Strategy：`ssot_first`。
- Canonical Skill package 独占三类 target、prerequisite linkage、十项 readiness dimensions、AI/script boundary、五 exits 与 side-effect-free 合同；global workflow 只保留 mandatory invocation、consumer route 和 fail-closed stop。
- Durable docs 已更新 `docs/requirements/**`、root/workflow/preset README，以及 workflow/data/companion/quality/installer/ownership specs。
- Task delta 已全部合并 durable SSOT。
- `task_history`：Phase 0、implementation handoff、Phase 2 与三轮 Branch Review 只保留为 task-history-only evidence。
- `followup_or_limitation`：#112 继续独占 task workspace 创建与 `issue-review.json` persistence；remote branch-pinned marketplace verification 只能在 push 后由 `trellis-finish-work` 完成。

## 安全说明

- 未发现 token、secret、private key、签名 URL、`.env`、数据库 URL、客户数据或敏感原始记录。
- 本次只处理正常运行、常见操作错误及明确 correctness/compatibility 边界，不引入恶意 actor、故意伪造、TOCTOU、锁、额外并发压力、fault injection 或跨 OS 原子性机制。
- 未修改 CI/CD workflow、Dockerfile、Compose、Kubernetes/Kustomize/Helm、数据库 schema/migration、Makefile 或服务部署资产；无业务部署、生产配置或数据库迁移要求。
- 本 PR 不创建 release tag；回滚可使用 Git revert，并从上一稳定 extension ref 重新应用 workflow/preset。
