## 变更摘要

- 新增公共 `guru-sync-base` Skill，在 repo-changing intake 的第一条 repo/network action 中确定 selected base、执行 explicit refspec fetch 与安全 `git merge --ff-only`，并验证 local base、remote base 和 decision checkout HEAD 完全一致。
- 固定 base 解析顺序为显式 `--base`、scalar `base_branch`、按配置顺序首个 existing `base_branch_candidates`、remote default；缺省候选保持 `dev -> develop -> main -> master`，不回退 current branch。
- 将 Skill interface 升级到 schema `1.2`，显式区分 `semantic` 五阶段与 `deterministic` 三阶段；`guru-sync-base` 使用完全机器可验证的 deterministic profile，既有语义审查门禁保持不变。
- 使用 stdout-only pre/post resolution facts 和滚动 digest 绑定 resolve、execute、validator 与 `prepare-task` mutation guards，不引入跨步骤临时 evidence lifecycle。
- 同步 canonical workflow/package、runtime、schema、preset、Codex/Cursor/Claude/Agents 平台副本、dogfood、durable docs/spec 与 public README。

## 影响范围

- Workflow：repo-changing Phase 0 显式 mandatory invoke `guru-sync-base`，并为 `synced`、`skipped`、`blocked` 提供唯一 consumer 或 fail-closed stop。
- Skill 与 runtime：新增 active package、interface、contract、result schema、example、thin wrappers、`sync-base` / `check-base-sync` companion commands，以及共享 resolver/sync/validator core。
- `prepare-task`：planner 在 issue read 前复用同一 core；issue、worktree、task mutation guards 逐次消费上一轮 post-sync digest并重验 freshness。
- 分发与升级：extension version 更新为 `0.6.5-guru.7`，preset managed inventory、平台副本、throwaway install、`trellis update` 和 preset reapply 合同同步。
- 不实现 #111 的 `guru-discover-change-context`；不修改 Trellis upstream、全局 npm 包或 `node_modules`。

## 验证结果

- Runtime 292 项、Skill registry/package 67 项、canonical `guru-sync-base` contract 5 项、Preset 37 项，共 401 项通过。
- 43 个变更 JSON parse、17 个 Bash syntax、22 个 Python AST/compile 与 `git diff --check origin/main...HEAD` 通过。
- Source/installed package validator、canonical/dogfood workflow drift、Agents/Codex/Cursor/Claude 六份 package byte/mode 一致性通过。
- Extension inventory 校验 83 个 managed skill files、76 个 preset assets，`conflicts=0`、`removals=0`、`sidecars=0`、`new_copies=0`、`managed_backups=0`。
- Clean throwaway 通过 fresh workflow/preset install、preview/switch、真实 behind `resolve -> ff-only -> validate -> prepare`、already-equal、rolling digest、`trellis update` 与 reapply，`.new/.bak` 为 0。
- 远端 branch-pinned marketplace verification 由 `trellis-finish-work` 在 reviewed HEAD push 后、PR 创建前执行；失败会阻塞发布。

## Review Gate

- Branch Review Gate 已绑定 HEAD `ed5fa7baed955f8ba5f84119f4bc177ad170c2d7`，覆盖 `origin/main...HEAD` 的 124 文件完整 diff与 4 个 task work commits。
- F-001 至 F-007 均有 finding owner、closure 和 fresh final reviewer 证据；Round 7 使用未参与 Round 1-6 的全新技术代理完成最终放行。
- 最终开放 findings 为 `P0=0, P1=0, P2=0, P3=0`。审查覆盖 live #110 scope corrections、规划、Docs SSOT、实现、测试、Phase 2、task commit、开箱即用、upgrade/update、部署与安全影响。

## Issue 关闭范围

Closes #110

### 仅引用或后续

- Refs #98：父 umbrella，仅保留架构与集成上下文，本 PR 不关闭。
- Follow-up #111：独立实现 `guru-discover-change-context`，不属于本 PR 的交付或关闭范围。

## Docs SSOT

- `strategy`：`ssot_first`；`docs_state` 为 `partial_docs`。
- `durable docs`：已更新 `AGENTS.md`、`docs/requirements/**`、`.trellis/spec/**`、canonical workflow/package contract、仓库 README、workflow README 与 preset README。
- `merged delta`：已回写 deterministic Skill 例外、schema `1.2` 迁移、四级 ordered base resolution、pre/post rolling digest、live Git validator、typed exits、`prepare-task` reuse、分发和验证矩阵。
- `task history`：issue 检索、scope correction 决策、sub-agent liveness、Phase 2 与七轮 Branch Review 过程仅保留为任务历史证据。
- `follow-up / limitation`：#111 独立承接 context discovery；branch-pinned remote marketplace 验证由本次 finish-work 发布事务完成，不恢复历史 repo-external evidence 设计。

## 安全说明

- 同步副作用限定为 explicit refspec fetch 与 selected-base checkout 上的 `git merge --ff-only`；dirty、missing、diverged、wrong checkout、digest/config/ref drift 均在对应副作用前 fail closed。
- 不包含 token、secret、private key、签名 URL、`.env`、数据库 URL、客户数据或持久化本机绝对路径；不引入 repo-external evidence file、lease/release、quarantine 或额外攻击/并发威胁模型。
- 未修改 `.github/workflows`、服务/API、业务 CLI、worker、数据库 schema/migration、Dockerfile、Compose、Kubernetes/Kustomize/Helm 或 Makefile，无业务部署拓扑、运行时配置或数据库迁移要求。
- 本 PR 不创建 release tag；回滚使用 Git revert，并从上一 extension ref 重新应用 workflow/preset。
