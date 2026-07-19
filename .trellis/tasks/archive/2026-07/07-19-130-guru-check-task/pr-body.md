## 变更摘要

- 新增 `guru-check-task` semantic closed-loop Skill，成为 Guru Team Phase 2 task-scope implementation check、scope qualification、finding loop、Docs SSOT reconciliation 与 `phase2-check.json` 的唯一语义 owner。
- 固化 workflow/standalone 共用的 entry contract：绑定 approved planning、requirement provenance、implementation handoff、Issue Scope Ledger、base/HEAD、完整 dirty snapshot、agent assignment/recovery 与 durable docs evidence。
- 固化 scope-before-severity 与完整 adequacy review：先区分 current scope、scope change、follow-up、out of scope，再仅对 current-scope finding 分配 P0-P3，并要求修复后完整重跑。
- 新增 schema 2.0、recorder/checker 与四个 typed exits：`passed`、`implementation_required`、`planning_stale`、`blocked`；script 只记录和校验确定性事实，不替代 AI semantic Gate。
- 收紧 evidence closure 与 freshness：关键 provenance/handoff/docs/repository/command/adequacy evidence 非空，current round 闭合七类 source，checker 重算全部 semantic/Gate/full-round 派生摘要。
- 兼容合法 post-commit Branch Review metadata tail，同时继续拒绝 Phase 2 agent/recovery drift 与未覆盖的 committed path。
- 同步 canonical package、shared runtime、Agents/Codex/Claude/Cursor 安装副本、workflow/preset/extension manifest、tests、durable requirements/spec 与公开 README。

## 影响范围

- Phase 2 workflow：`.trellis/workflow.md` 与 marketplace workflow 通过 stable Skill id mandatory invoke `guru-check-task`，只消费四个 typed exit，不复制 step-local 内部流程。
- Skill package：新增 `SKILL.md`、interface、contract、schema、example、recorder/checker wrappers 与 contract tests，并同步到五套平台安装副本。
- Companion runtime：扩展 Guru Team shared dispatcher、artifact projection、freshness、semantic-derived digest 与 post-commit audit 的确定性校验。
- Preset / marketplace：extension manifest、registry、preset README、workflow README 与 clean install/update/reapply 验证链已同步；stable public id 未发生破坏性变更。
- 兼容性：官方 `trellis-check` 保持 unchanged evidence worker；现有 planning、task commit、Branch Review 与 finish-work owner 边界不变。
- 部署影响：不修改 `.github/workflows`、CI/CD、Docker/Compose、Kubernetes/Kustomize/Helm、数据库 migration、Makefile、业务 API/CLI/worker 或生产配置，无应用部署和数据迁移需求。

## 验证结果

- 6 个关键定向回归通过，覆盖非空 evidence、七类 source closure、全部 semantic 派生字段重算、合法 review metadata tail、Phase 2 agent/recovery drift 与 uncovered committed path。
- 完整五模块测试通过：`673 passed, 13 skipped`，覆盖 Skill package、source validator、shared runtime、preset installer 与 upstream ownership。
- Clean throwaway 通过：public marketplace discovery、workflow preview/switch、preset initial install、`trellis update --force`、workflow/preset reapply 与 after-update smoke 均为 exit 0。
- Ownership checkpoint 为 43，active Skill 为 9，managed files 为 383，conflict/removal/sidecar 为 0。
- Canonical package 与 shared、Agents、Codex、Claude、Cursor 副本逐文件一致；canonical/installed runtime 与 workflow 字节一致。
- Python compile、Bash syntax、JSON parse、task validation、`git diff --check` 与 `.new`/`.bak` scan 全部通过。
- 精确远端 feature-ref marketplace verification 将由正式 `trellis-finish-work` 在 reviewed content push 后、PR 创建前执行并绑定；在该 evidence 变为 passed 前不声明远端分支安装链已通过。

## Review Gate

- Branch Review Gate 已覆盖 `origin/main...HEAD` 完整 93 路径、两次 task commit 与全部 task metadata evidence。
- Round 001 发现 P1 `F-BR-001`：空 entry/adequacy evidence 仍可通过；P2 `F-BR-002`：checker 未重算 semantic/full-round 派生摘要；Gate 后置审计另发现合法 review metadata tail 会误报 stale。
- 修复重新经过 implementation、全新完整 Phase 2 与 finding-fix commit。Round 002 由原 finding owner 以 `reuse-for-closure` 闭环三项问题，findings 为 0。
- Round 003 由未参与实现、Phase 2 或 earlier review round 的 fresh reviewer 独立审查当前完整 diff，最终 `P0=0, P1=0, P2=0, P3=0`。
- Review 明确覆盖需求、设计、实现、测试、Docs SSOT、agent recovery、distribution、upgrade/update、部署、安全与 Issue Scope。

## Issue 关闭范围

Closes #130

### 仅引用或相关

- Refs #127：Skill-first umbrella 架构上下文，本 PR 只交付其 Phase 2 子单元，不关闭。
- Follow-up #81：release/tag-pinned 发布门禁，保持独立。
- Follow-up #108：Phase 2 减法审计能力，保持独立。
- Follow-up #131：`guru-review-branch` closed-loop Skill，保持独立。
- Follow-up #132：planning/check/review routing 集成与 overlay 收敛，保持独立。

## Docs SSOT / 文档同步

- Docs state：`complete_docs`；策略：`ssot_first`。
- Durable docs：已同步根 README、`docs/requirements/**`、`.trellis/spec/workflow/**`、workflow README 与 preset README，覆盖 Phase 2 semantic owner、四出口、scope-first、evidence source closure、derived digest recomputation 与 stable post-commit handoff。
- `task_delta_merged=true`：需求、设计、实现和 review 中形成的长期合同均已合并回 durable owner；runtime、schema、tests 与 distribution bytes 对齐。
- Task-history-only：intake/research、planning approval、implementation/check handoff、agent liveness/recovery、Phase 2/Branch Review finding lifecycle 与 task commit/closeout evidence 仅保留在任务 archive，不进入公共 Skill package state。
- Follow-up / 限制：#81、#108、#131、#132 继续由独立 issue 承接；本 PR 不扩张其范围。远端 feature-ref marketplace evidence 由 finish-work transaction 生成并绑定。

## 安全说明

- 未发现 token、secret、credential、private key、签名 URL、`.env`、数据库 URL、客户数据或敏感原始记录。
- 公共 Skill package、schema、example、manifest 与 durable docs 不包含本机绝对路径；task-local 路径仅存在于审计 artifact。
- Evidence closure 与 digest 重算用于 honest-but-fallible 正常流程 correctness，不新增 hostile-input、anti-tamper、TOCTOU、锁、压力竞态、fault injection 或跨 OS 原子性机制。
- 无网络服务入口、权限模型、生产配置、容器镜像、Kubernetes 资源或数据库迁移变化。
