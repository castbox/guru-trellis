## 变更摘要

- 新增 active semantic closed-loop Skill `guru-create-task-workspace`，统一承接 reviewed Issue/draft 之后的命名、assignee、副作用计划、AI Review Gate、两类 confirmation、确定性执行与四个 typed exits。
- 为 reviewed draft 增加 exact 0/1/>1 live recovery、create-success/live-reread-failure 重入与 checker-passed created provenance，保证普通失败重试不会重复创建 Issue。
- 首个 GitHub/workspace/task mutation 前复用 shared base resolver/sync；远端 base 前进时返回 `refresh_review` 且保持 zero-business-write。
- 取消 Guru Team preset/install/task creation 对 `.trellis/.developer` 和 `.trellis/workspace/**` 的依赖，同时保留官方 Trellis 对这些路径的支持。
- 将 `task-start-context.json`、`issue-scope-ledger.json`、`context-discovery.json`、`issue-review.json` 固定为 task-local portable evidence，本机 mapping 只进入 gitignored runtime。
- 接入 thin Intake chain、canonical registry/package/runtime/workflow、preset installer、Agents/Codex/Cursor/Claude 与 dogfood copies，并完成 A -> B / B -> A task metadata merge gate。

## 影响范围

- Public Skill：新增 `trellis/skills/guru-team/packages/guru-create-task-workspace/` 的 interface、contract、closed schemas、examples、thin wrappers 与 tests，并从 registry `planned` 提升为 `active`。
- Workflow/runtime：`guru-review-change-request:ready` 进入新 Skill；shared runtime 增加 plan recorder、exact executor、result checker、created Issue recovery、mutation-time base sync 与 official task identity isolation。
- Preset/分发：同步 canonical、dogfood、shared、Agents、Codex、Cursor、Claude managed copies，以及 clean install、update/reapply、no-developer、ownership/drift 与 sidecar 校验。
- Docs SSOT：同步 requirements、workflow/preset/docs specs、根 README、workflow README 与 preset README；task artifacts 只保留 task history 和审查证据。
- 不实现或关闭 #132 的 legacy upstream entry overlay removal；不修改 Trellis upstream、全局 npm 包或 `node_modules`。
- 未修改 CI/CD、Docker/Compose、Kubernetes/Kustomize/Helm、数据库 migration 或 Makefile；不新增服务、镜像、端口、运行时配置或数据库状态，无业务部署资产需要同步。

## 验证结果

- Phase 2 fresh full suite：`644/644` 通过；Round 5 closure 又在当前实现 tree 上 fresh 运行 `644/644` 并通过。
- Round 6 fresh final reviewer 独立运行最高风险 focused runtime `7/7`、package contract `7/7`，全部通过。
- Source/installed Skill validators 通过：303 managed files，`sidecar=0`、`conflict=0`、`removal=0`。
- Upstream ownership 与 dogfood drift 通过：43 个 frozen overlays 未变化，canonical/dogfood/Agents/Codex/Cursor/Claude bytes 与 executable modes 一致。
- Clean throwaway 覆盖 marketplace discovery/preview/switch、preset install、workspace/task creation、no-developer、existing identity preservation、`trellis update` 与 workflow/preset reapply。
- Production A/B fixture 的 A -> B 与 B -> A 两个 merge 顺序均通过，无 shared tracked metadata conflict。
- `py_compile`、`bash -n`、JSON/JSONL parse、task validation、`git diff --check` 与 `.new/.bak` 检查全部通过。
- Reviewed content push 后由 `trellis-finish-work` 执行 exact feature-ref marketplace verification；失败会在 PR 创建前阻塞发布。

## Review Gate

- Branch Review Gate 绑定 Reviewed HEAD `38a51965e5c4af32941c595badb07b4017965861`，覆盖 `origin/main...HEAD` 的 4 commits、124 files 与完整 task scope。
- Round 1-3 关闭 official identity 与 public version findings；Round 4-5 关闭 duplicate Issue recovery、mutation-time base freshness 与 created provenance findings。
- Round 6 使用从未参与 implementation、Phase 2 或 Round 1-5 的 fresh final reviewer `final_review_112_r6`，P0/P1/P2/P3 均为 0。
- 审查覆盖 requirements、Docs SSOT、AI/script boundary、code/schema/config/scripts/tests、install/update/reapply、A/B merge、安全和部署影响。

## Issue 关闭范围

Closes #112

Closes #99

Closes #54

### 仅引用

- Refs #98：Intake Skill family umbrella 保持 open，由 #132 完成最终 Stage 0 closure。
- Refs #53：原始并行 metadata 问题保持 open，由 #132 验证完整 Stage 0 后关闭。
- Follow-up #132：独占 legacy upstream entry overlay removal 与 #98/#53 最终关闭语义。

## Docs SSOT / 文档同步

- Docs state：`stale_docs`。
- Strategy：`ssot_first`。
- Durable docs：requirements、workflow/preset/docs specs、根 README、workflow README 与 preset README 已回写 active Skill lifecycle、mode parity、target authority、recovery、provenance、assignee、base freshness、portable artifacts、no-developer、typed exits、A/B merge 与 install/update/reapply。
- Merged delta：canonical package/runtime/workflow/schema/test、public README 与 managed multi-platform copies 已同步；当前 task delta 已合并回 durable SSOT。
- Task history：planning approval、implementation handoff、Phase 2、commit plans 与六轮 Branch Review 只保留为任务历史证据，不形成第二套公共合同。
- Follow-up / limitation：#132 保持独立；exact remote feature-ref marketplace evidence 由本次 finish transaction 在 push 后生成和绑定。

## 安全说明

- 未发现 token、secret、private key、签名 URL、`.env`、数据库 URL、客户数据或敏感原始记录。
- Public package/schema/example/docs 与四个 task-local artifact 合同不携带本机绝对路径；本机 mapping 只写 gitignored `.trellis/.runtime/guru-team/**`。
- 本任务只覆盖 honest-but-fallible 正常路径、常见操作错误和正文明确的 correctness/compatibility 边界；不引入恶意伪造、hostile input、锁、TOCTOU、额外竞态压力、fault injection 或 cross-OS 原子性机制。
- 无 CI/CD、容器、K8s/Kustomize/Helm、数据库 migration、Makefile 或业务部署变化；回滚可使用 Git revert，并从上一稳定 extension ref 重新应用 workflow/preset。
