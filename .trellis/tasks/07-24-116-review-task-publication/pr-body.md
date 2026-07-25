# #116 实现 task publication 审查闭环

## 变更摘要

- 新增 active semantic Skill `guru-review-task-publication`，统一 workflow 与 standalone 两种入口、十维 publication review、metadata-only 内部修订闭环和 `ready` / `return_to_task_work` / `blocked` 三个 typed exits。
- 将 AI 语义判断与确定性 recorder/checker 分层：AI 负责 Issue 关闭范围、PR body、验证声明、Docs SSOT、安全/部署影响、finding route 与 readiness；脚本只重建并校验 task、HEAD、artifact、working-tree 和 freshness 事实。
- 建立唯一 task-local `pr-readiness.json` gate、最小 `publication_ref` handoff、planned `guru-finalize-task` consumer，以及 stale re-entry 和 fail-closed public/private I/O 合同。
- 同步 canonical workflow、dogfood workflow、preset installer、shared package 和 Codex/Claude/Cursor/Agents 四个平台副本，并补齐 fresh install、update、reapply 与六布局真实命令验证。

## 影响范围

本变更影响 Guru Team 的 Phase 3.6 收尾控制面、Skill registry、publication recorder/checker、public schemas/evals、preset 管理清单及平台入口。现有 `guru-review-branch:passed` 不再直接进入 finish family，而是先生成 publication content，再显式调用 `guru-review-task-publication`。`ready` 只产生当前 task、reviewed HEAD 与 opaque publication ref，且在 #118 激活 `guru-finalize-task` 前失败关闭；未修改 Trellis 上游源码、全局 npm 包或 `node_modules`。

## 验证结果

- Runtime suite：572 tests passed，13 skipped。
- Full Skill package suite：174 tests passed。
- Publication package contract：canonical 18/18、installed 18/18。
- Actual-wrapper eval：source 7/7、installed 7/7。
- Preset installer：45/45；upstream ownership：9/9。
- Canonical、installed shared 与四个平台 recorder/checker 共 12 条真实命令均符合布局合同；5 组 package byte parity 与 executable mode 一致。
- Source/installed registry validator 均为 11 active Skills、42 exits、25 targets；installed manifest 含 2100 managed files，sidecar/removal/conflict 为 0。
- Fresh throwaway install、Trellis update、preset reapply 三阶段 publication wrappers 均为 10/10，最终 exit 0；public marketplace discovery 与 local unpublished workflow sample 通过。
- `git diff --check`、planning approval、task validation、workspace boundary、dogfood overlay drift、credential-shaped added-line scan 与 deploy-sensitive path scan均通过。
- 两项未修改的 Codex hook test 在 `origin/main` 同样失败，属于 baseline stale assertions，未由 #116 引入；completed compatibility 由 #119 处理。
- 当前分支尚未 push，因此 exact remote candidate-branch marketplace ref 尚未验证；该验证保留给既有 publish gate，当前已验证 public marketplace discovery 与 local unpublished sample。
- 当前 task 的首次 dogfood publication dry-run 在合法补齐 ledger publication metadata 后复现 `phase2_check_requirement_provenance_stale`；该 current-scope finding 已按 `return_to_task_work` 路由，必须修复并重新经过 Phase 2、commit、Branch Review 与 publication review 后才能发布。

## Review Gate

Branch Review 覆盖 `origin/main@bdc8f50bcd1e325aed331d4b01107b83ed8ee940...d7ab98f5c53f470f4d3f3742f8cfca24f8465edd` 的完整 345-file、3-commit 范围。Round 03 与 Round 05 分别由原 finding owner 关闭 P2/P1；Round 06 使用未参与实现、Phase 2、finding discovery 或 closure 的全新 reviewer 完成 fresh final review，P0/P1/P2/P3 均为 0。正式 `guru-review-branch` recorder、checker 与公共 wrapper 均返回 `passed`。

## Issue 关闭范围

Closes #116。

Related：#115、#131、#144、#146，仅建立关联，不关闭。

Follow-up：#81、#117、#118、#119、#132，继续作为独立后续范围，不关闭。

## 安全说明

未发现 token、secret、private key、`.env`、数据库 URL、签名 URL、客户数据或敏感原始记录进入候选变更。没有 CI/CD、Docker/Compose、Kubernetes/Kustomize/Helm、DB migration、Makefile、依赖 manifest 或生产服务部署变化；无需数据库迁移、配置变更或生产回滚步骤。Workflow、runtime、schema、preset 与平台分发兼容性已由 source/installed suites、六布局命令和 fresh install/update/reapply 覆盖。

## Docs SSOT

- strategy：`ssot_first`。
- durable docs：已更新 workflow、Skill I/O、data contract、companion scripts、quality、preset installer、upstream ownership 与 public docs SSOT，以及 canonical/dogfood workflow 和 README。
- merged delta：task 中批准的 semantic owner、双入口、三 exits、单 readiness gate、freshness、return/stale re-entry、registry closure 与 OOTB/update/reapply 规则均已合并到 durable authority。
- task history：`prd.md`、`design.md`、`implement.md`、Phase 2 与六轮 review artifacts 仅保留本任务审计历史，不承担长期流程定义。
- follow-up/limitation：#118 负责 `guru-finalize-task`，#119 负责 finish-family 集成与历史 closeout migration；exact remote candidate ref 验证须在获得 push/finalization 授权后执行。
