# Round 7 最终放行审查报告

## 审查身份

- 角色：Issue #96 replacement 最终放行审查代理。
- 执行环境：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/096-task-runtime-boundary`。
- 审查原则：独立复核完整累计 diff；不消费被终止 reviewer 的输出；不回退、覆盖或修复他人改动；审查阶段仅执行只读命令。
- 写入边界：所有只读审查结束后，仅写入本报告与同 task 下的 `review.md`。

## Reviewed HEAD 与 Diff

- Base：`origin/main` = `59d6c0caf404c4c927fe8aada92811d1ced907d5`。
- Reviewed HEAD：`30f4f4a5bc42cfb099ea07fa7e64c9af5dd5e623`。
- Reviewed diff：`origin/main...30f4f4a5bc42cfb099ea07fa7e64c9af5dd5e623`。
- 提交范围：完整六提交，依次为 `a84e572`、`90a2d45`、`f05cd66`、`9c54278`、`f48abcf`、`30f4f4a`。
- 审查开始时存在的非本代理工作树状态：`agent-assignment.json` 已修改、`reviews/round-6.md` 未跟踪；二者均未被本代理回退或覆盖，也不属于上述 committed diff。

## 审查范围

- Live GitHub Issue #96、umbrella Issue #53、follow-up #97/#98/#99/#100 的 close/ref/followup 边界。
- `prd.md`、`design.md`、`implement.md`、`planning-approval.json`、`implementation-handoff.md`、`phase2-check.json`、`issue-scope-ledger.json`、`agent-assignment.json`。
- Round 1–6 raw reports、旧 `review.md`、完整六提交代码与文档 diff。
- Canonical workflow、preset、config、extension manifest、schema、companion scripts、installer、tests、README、requirements、`.trellis/spec/workflow/**`。
- Dogfood `.trellis/workflow.md`、`.trellis/guru-team/**` 与 Codex、Claude、Cursor、Trellis 四个平台活跃 overlay/agent/command/skill 副本。
- 旧 handoff 删除、任务启动上下文、本机运行态、workspace boundary、obsolete cleanup、active reference scanner、remote marketplace verifier、精确双文件 metadata tail、开箱安装与 upgrade/update 门禁、安全和部署影响。

## 只读命令与证据

- 首条环境确认命令验证 `pwd` 与 git top-level 均为目标 worktree，HEAD 为 `30f4f4a5...`，`origin/main` 为 `59d6c0ca...`。
- 使用 GitHub API 读取 live Issue #96 与 #53；#96 当前 open，#53 仍为 open umbrella。
- `git diff --name-status`、`git diff --stat`、`git log`、定向 `sed`/`rg`/`jq` 覆盖完整六提交、任务 artifacts、关键 Python 控制流与测试合同。
- `git diff --check origin/main...30f4f4a5...` 通过。
- Canonical/dogfood SHA-256：workflow、Python helper、`task-start-context` schema、`marketplace-verification` schema 分别完全一致。
- 逐个比较 canonical overlay 与 dogfood 目标文件，无 drift；全仓未发现 `.new` / `.bak`。
- 活跃引用扫描排除历史 `.trellis/tasks/**` 后，未发现 `.trellis/guru-team/handoff.json`、`handoff_path`、`load_handoff` 或 committed `workspace_path` 继续作为运行合同；旧 schema 仅保留于 installer obsolete-cleanup 测试 fixture。
- 读取 Trellis 官方 custom workflow 与 spec template marketplace 文档：本实现继续以 Markdown workflow/overlay 定义 AI 流程，以 companion scripts 执行确定性 executor/validator/recorder 动作；未修改上游 Trellis、全局 npm 或 `node_modules`。
- Phase 2 与 Round 6 clean-clone evidence：core 241 tests、preset 30 tests、42 项 publish/scanner 定向合同、11 个 managed dogfood agent target mutation regression、dogfood drift、Python compile、shell syntax、JSON/JSONL、task validation、workspace boundary 与 commit message 检查均通过。遵守本轮禁止写 repo 的约束，未重新运行可能产生缓存或 mutation 的测试。

## 合同复核

### 旧 Handoff 删除与 Portable Context

- Canonical 与 dogfood 均删除固定 tracked `.trellis/guru-team/handoff.json`、`intake-handoff.schema.json` 和 `handoff_path` 公共配置/API。
- `.trellis/tasks/<task>/task-start-context.json` 为 task-local tracked artifact；schema 使用字段白名单与 `additionalProperties: false`。
- `validate_task_start_context()` 拒绝绝对路径、runtime/preflight/worktree/developer/command 等本机字段；当前实例只包含 repo-relative `task_artifact_dir`、portable slug/id、branch/base/SHA、actor/assignee 与 issue scope/intake 摘要。
- fresh、remote-only、fetch-failed 的 SHA producer→context 映射已有回归测试，Round 1 的 SHA 映射问题已闭环。

### 本机运行态与 Workspace Boundary

- local runtime 固定为 `.trellis/.runtime/guru-team/workspaces/<slug>.json` 与 `tasks/<slug>.json`，由 `.gitignore` 和 preset idempotent 管理；未引入 tracked runtime index 或 developer 维度目录。
- runtime cache 是可丢弃映射；workspace 解析可从当前 checkout、portable task context、runtime cache 与 `git worktree list` 重建。
- workspace boundary 不读取 committed absolute `workspace_path`，finish/publish 在 boundary 失败时 fail closed。
- planner-only、create-worktree、create-task 写路径已拆分；普通 task tracked metadata 使用 task-local 路径，并行任务不共享固定 tracked handoff 文件。

### Installer Obsolete Cleanup

- Installer 只自动删除已知、内容匹配的旧 managed artifact；修改过的 obsolete schema 被保留并报告到 `obsolete_conflicts`，不会静默覆盖用户内容。
- 旧 schema fixture 独立存放，clean clone 不再依赖已从 HEAD 删除的路径；Round 1 clean-clone fixture 问题已闭环。
- Runtime ignore 由 installer 幂等维护；canonical-first、all-platform overlay apply、dogfood drift 与无 `.new/.bak` evidence 已记录。

### 四平台 Active Scanner

- Active-reference scanner 从 canonical overlay managed files 派生 dogfood targets，覆盖 `.codex`、`.claude`、`.cursor`、`.trellis` implement/check agents，并覆盖 start/continue/finish 的 active workflow/skill/prompt/command/docs SSOT。
- 历史 `.trellis/tasks/**` 明确排除，避免把不可变历史报告误判为活跃 API。
- Round 5 漏扫 dogfood agent roots 的 P1 已由第六提交修复；Round 6 的隔离 mutation regression 对 11 个 managed dogfood targets 均能检出 forbidden reference，且未污染真实文件。

### Remote Marketplace Verifier 与 Metadata Tail

- Publish 顺序固定为：push reviewed content HEAD、确认远端 SHA、从远端 branch clone、执行 marketplace init/preview/switch 与 preset reapply、生成 schema-valid verifier artifact、把 ledger AC9 从 structured pending 更新为 passed、仅提交 verifier artifact 与 ledger、push metadata tail、再次校验 artifact/ledger/gate/current/remote HEAD，最后才允许 `gh pr create`。
- failed/partial verifier artifact 也满足 public schema，但 `failed`、`pending`、digest/SHA 不一致或 unexpected dirty path 均阻断 publish。
- `commit_marketplace_verification_metadata()` 与 validator 只接受 `marketplace-verification.json`、`issue-scope-ledger.json` 两个精确 metadata path；测试覆盖顺序无关的精确双文件集合及额外文件拒绝。
- 当前 ledger AC9 为 `required=true`、`status=pending`，符合尚未 push 的阶段事实；它不能满足最终 publish，也未被虚构为 passed。这是预期的后续发布门禁，不是当前 committed implementation finding。

## Docs SSOT 与官方扩展边界

- Canonical `trellis/workflows/guru-team/workflow.md` 与 dogfood `.trellis/workflow.md` 字节一致。
- Workflow README、preset README、根 README、requirements、`.trellis/spec/workflow/**`、config/schema/scripts/tests 与四平台 overlays 对“任务启动上下文 / 本机运行态 / workspace 重建 / remote verifier”使用同一合同。
- Round 4 指出的 active docs/overlay `workspace_path` 旧合同已在后续提交清理；Round 5 指出的 scanner 覆盖缺口也已闭环，当前无残留活跃引用。
- 实现遵守官方扩展面：workflow 行为由 Markdown 定义，spec template 未承载 active task/platform state，脚本只承担确定性执行、校验和记录。
- Out-of-box/update evidence 已覆盖 clean clone、marketplace init/preview/switch、preset reapply、all-platform overlay、obsolete cleanup、runtime ignore、dogfood drift；真实远端 branch 验收被正确保留到 push 后 verifier 阶段，未提前宣称通过。

## 安全、部署与 Issue Scope

- 安全：对 committed diff 的 secret-pattern 只读扫描仅命中历史报告中的“未发现 secret”等说明文字；未发现 token、private key、`.env` 内容、数据库凭据、签名 URL或客户数据。Portable context 不含本机绝对路径，verifier 只记录必要 digest/size/状态证据。
- 部署：changed paths 未触及 CI/CD、Docker/Compose、Kubernetes/Helm、数据库 migration、Makefile、依赖清单或业务服务运行时；影响限于 Guru Team workflow/preset/runtime metadata、文档、schema、tests 与发布门禁。
- Issue scope：`primary_issue`/`close_issues` 仅 #96；#53 仅 related 且保持 open；#97/#98/#99/#100 仅 followup，不得使用 close keyword。
- 稳定标签：远端当前只有 `v0.6.5`、`v0.6.5-guru.1`、`v0.6.5-guru.2`；`v0.6.5-guru.3` 不存在，本 issue 未获授权创建 release tag。

## Round 1–6 问题闭环复核

- Round 1：4 个 P1——SHA 映射、clean-clone obsolete fixture、真实 push 后 marketplace gate、ledger acceptance evidence；均由后续实现和测试闭环。
- Round 2：1 个 P1、1 个 P2——deferred AC9 被错误计为 evidence、failed verifier artifact schema 不一致；均由 structured pending/passed 合同与统一 artifact schema 闭环。
- Round 3：零 findings，允许进入最终放行审查。
- Round 4：1 个 P1——active workflow/docs/overlays 仍引用旧或不存在的 `workspace_path`；由后续 active SSOT 清理闭环。
- Round 5：1 个 P1——scanner 漏扫 dogfood 平台 agent roots；由 canonical-overlay 派生 targets 与 mutation regression 闭环。
- Round 6：零 findings，确认 scanner 修复与完整六提交 diff，可进入新的最终放行审查。

## Findings

- P0：0。
- P1：0。
- P2：0。
- P3：0。

## 结论

对 `origin/main...30f4f4a5bc42cfb099ea07fa7e64c9af5dd5e623` 完整六提交的 replacement 最终放行审查未发现新的 P0–P3 finding。Issue #96 的旧 handoff 概念删除、task-local portable context、gitignored/reconstructible runtime、workspace boundary、installer cleanup、四平台 active scanner、remote marketplace verifier、精确双文件 metadata tail、Docs SSOT、安全、部署和 issue scope 均与需求及已有验证证据一致。

**最终 findings 为零，建议当前 Reviewed HEAD 通过 Branch Review Gate。** 后续 publish 仍必须严格执行 push 后真实 remote marketplace verifier，并在其生成 current、schema-valid、passed evidence 且精确双文件 metadata tail 校验成功后才能创建 PR；不得绕过或提前宣称该远端门禁已通过。
