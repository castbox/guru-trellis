## 变更摘要

- 完整移除 Guru Team 旧的 tracked `.trellis/guru-team/handoff.json`、`intake-handoff.schema.json` 和 `handoff_path` 公共 API。
- 新增 task-local、可移植的 `task-start-context.json`，只保存仓库相对路径、branch/base/SHA、issue scope 等可提交事实；禁止本机绝对路径、worktree/runtime/preflight/developer 私有状态。
- 新增 gitignored `.trellis/.runtime/guru-team/workspaces|tasks/*.json` 本机缓存，并支持结合当前 checkout、task context 与 `git worktree list` 重建 workspace boundary。
- 重构 prepare/check/review/finish/publish 与 preset installer：安全清理未修改的 obsolete managed artifacts，保留并报告用户修改冲突。
- 增加 push 后 remote marketplace verifier：先验证远端分支 SHA，再在远端 clone 执行 workflow init/preview/switch 和 preset reapply；只有 verifier artifact 与 issue ledger 两个 metadata tail 文件允许提交，任何 pending/failed/stale/tampered 状态都在 `gh pr create` 前阻断。
- 补强 Branch Review Gate 的多轮审查元数据：支持显式跨代理 closure，同时严格验证 fresh reviewer、round relation、HEAD、角色和 finding 生命周期。

## 影响范围

- 影响 Guru Team workflow marketplace、preset installer、companion validator/recorder、schema、README/requirements/spec 以及 Codex、Claude、Cursor、Trellis 平台入口。
- 不修改 Trellis upstream、全局 npm 包、`node_modules` 或官方 task lifecycle。
- 不处理 workspace journal / `add_session.py` 冲突，该后续由 #97 负责；#98、#99、#100 继续保持独立 follow-up。
- 稳定 tag `v0.6.5-guru.3` 当前不存在，本 PR 不创建 release tag。

## 文档同步 / Docs SSOT

- 计划策略：`ssot_first`。
- Durable SSOT 已同步：canonical workflow、`.trellis/spec/workflow/**`、requirements、README、preset README、schema/validator 合同与五平台 overlay 文案一致。
- Task delta 已回并 durable docs；task-local planning、implementation handoff、Phase 2、十二轮 raw review 与最终 rollup 仅保留本任务审计历史。
- 当前 PR 限制：remote marketplace `passed` 证据只能在 reviewed content push 后由 deterministic verifier 生成；创建 PR 前 finish-work 必须完成该后置门禁。

## 验证结果

- Canonical core tests：251 项通过。
- Preset installer tests：30 项通过。
- Closure/final reviewer 正负矩阵、active-reference scanner 与 11-target mutation regression 通过。
- 临时已初始化仓库的 all-platform preset 安装通过，无未处理 `.new` / `.bak`。
- Python compile、managed shell syntax、JSON/JSONL、task validation、workspace boundary、planning approval、agent assignment、commit messages、dogfood overlay drift、canonical/dogfood byte equality、`git diff --check` 均通过。
- Branch Review 共十二轮：历史 findings 全部闭环；fresh Round 12 final reviewer 对 `origin/main...be3e27b6a09ede95819aca36d52319a9cde199be` 得出 P0/P1/P2/P3 全 0。
- 远端 marketplace verification 当前仍为结构化 `required=true,status=pending`；这是 push 前预期状态，不代表已通过。finish-work 必须在 PR 创建前生成 schema-valid passed artifact、更新 ledger、提交精确两文件 metadata tail 并复核 remote HEAD。

## Review Gate

- Review source：独立代理。
- Final reviewer：Round 12 `019f4c44-ab1f-74f1-94b5-d44e1395feb5`。
- Reviewed range：`origin/main...be3e27b6a09ede95819aca36d52319a9cde199be`。
- Gate 结论：通过，零 findings；`review.md` 链接 Round 1–12 全部 immutable raw reports。

## Issue 关闭范围

Closes #96

Refs #53

Follow-up：#97、#98、#99、#100（不关闭）。

## 安全说明

- 未发现 token、private key、`.env`、数据库 URL、签名 URL、客户数据或敏感原始记录。
- `task-start-context.json` 禁止本机绝对路径与 runtime/preflight/worktree 私有状态；`.trellis/.runtime/**` 保持 gitignored、可删除和可重建。
- Verifier artifact 只记录必要状态、SHA、digest、size 与命令结果，不记录凭据。
- 本次无 CI/CD、Docker/Compose、Kubernetes/Kustomize、数据库 migration、Makefile、依赖锁文件或业务服务部署影响；无需生产迁移或运行时配置变更。
