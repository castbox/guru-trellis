## 变更摘要

- 新增 `guru-review-branch` active closed-loop Skill，使其成为 Phase 3.5 Branch Review 的唯一 semantic owner。
- 建立 Interface 1.3 minimal handoff：public input 固定为 `task_ref`、`base_branch`、`work_commit`、`phase2_ref`、`issue_scope_ref`、`implementation_handoff_ref` 六字段；public output 固定为 `passed`、`implementation_required`、`scope_confirmation_required`、`blocked` 四个 typed exits。
- 闭合独立 reviewer assignment、finding proposal/action、原 owner closure、fresh-final replacement、gate freshness 与 stale/mismatch fail-closed；AI 先完成 semantic judgment，脚本只记录或校验确定性事实。
- 将 `trellis-continue`、workflow 与平台入口收敛为 stable Skill id 的显式调用和唯一 typed-route consumer，不再复制 Branch Review 内部流程。
- 同步 canonical、installed、Agents、Codex、Claude、Cursor、workflow/preset registry、P18 upstream ownership、tests 与 durable Docs SSOT。

## 影响范围

- Skill package：`guru-review-branch` 的 SKILL、interface、public schemas/examples、eval corpus、review-gate schema、recorder、validator 与 contract tests。
- Workflow/runtime：Phase 3.5 mandatory invocation、public wrapper、private live-facts resolution、finding lifecycle、fresh-final 与 gate projection。
- Preset/platform：canonical package 激活，installed runtime 与 Agents/Codex/Claude/Cursor 分发，五个 continue entries 的 thin routing，以及 P18 historical/current ownership validation。
- Docs SSOT：根 README、workflow/preset README 与 workflow/preset specs；active closure 统一为 10 Skills/39 exits，production migration 独立保持 3 Skills/11 exits。
- 不修改 Trellis upstream、全局 npm 包或 `node_modules`；不涉及 GitHub Actions、Docker/Compose、Kubernetes/Kustomize/Helm、业务数据库 schema/migration、Makefile、生产配置或应用 runtime，因此无需服务部署、停机、配置迁移或数据迁移。

## 验证结果

- Fresh Phase 2：shared runtime 566 passed、13 个 capability-dependent tests skipped；Skill package 171/171；preset 45/45；contract 8/8；ownership 9/9。
- Source/installed production eval 各 7/7；package validators 均为 10 active invokes、39 exits、23 targets。
- Installed inventory：1903 managed files，sidecar/removal/conflict 均为 0；canonical/installed shared eval 一致。
- P18 ownership：43/43 historical identities、5 个 current payload bindings、0 error；positive/negative focused checks 3/3。
- 2632 个 changed JSON、295 个 shell 脚本、116 个 Python 文件的语法/编译检查通过；`git diff --check`、task/contract/gate validators、secret/sensitive 与 deployment scans 通过。
- Clean throwaway 已覆盖 marketplace discovery、本地 current canonical、fresh init、existing preview/switch、三平台 preset install、official update、workflow/preset reapply、double apply 与最终 zero-sidecar。
- Reviewed content push 后仍必须由 finish-work transaction 执行 exact remote feature-ref marketplace verification；本地验证不冒充远端发布证据。

## Review Gate

- Branch Review Gate 绑定 `origin/main...c18efe0f73f03d216a7f4e873907569922e800be`，覆盖完整 328-file diff、5 个 task work commits、live Issue #131、planning、implementation handoff、fresh Phase 2、Docs SSOT、issue scope、install/update/upgrade、部署与安全边界。
- 前序 review findings 已按 finding owner、replacement chain 与 committed revision 全部关闭；Round 11 的单次候选经同 HEAD 的稳定复验被资格化为 `rejected_candidate`，没有 severity、implementation route 或 required follow-up。
- Round 12 使用未参与实现、Phase 2、前序 discovery 或 closure 的 fresh reviewer 独立复审，P0=0、P1=0、P2=0、P3=0，scope proposals=0。
- Final gate typed exit 为 `passed`；reviewed HEAD、review report、agent assignment、facts snapshot 与 gate artifact 已精确绑定。

## Issue 关闭范围

Closes #131

### 仅关联或后续范围

- Refs #127：Skill-first 流程收敛父级路线，保持 open，不由本 PR 关闭。
- Refs #130：已完成的 `guru-check-task` 上游依赖，保持既有边界。
- Refs #144：已完成的 Interface 1.3 minimal handoff 基础设施依赖。
- Refs #146：已完成的 planning、Phase 2 与 task commit minimal handoff 生产者依赖。
- Refs #116：`passed` 出口的 publication consumer 后续任务，保持 open，不由本 PR 关闭。
- Refs #132：完整 planning/check/review 集成与 preset upstream overlay 收口，保持 open，不由本 PR 关闭。

## 安全说明

- 未引入或暴露 token、credential、private key、signed URL、`.env`、数据库 URL、客户数据或敏感 provider 输出；secret/sensitive scans 通过。
- Public handoff 只包含 consumer 直接使用的最小字段；Git/GitHub/Trellis live facts、digest、完整 review history、file metadata、assignment checkpoint 与 recovery state 保持 task-local/runtime private。
- Hash、digest 与 freshness 只服务 honest-but-fallible 正常流程 correctness；本 PR 不扩展到恶意伪造、hostile input、锁、并发压力、TOCTOU、额外 fault injection、crash consistency 或跨 OS 原子性。
- 没有生产权限、网络服务入口、容器镜像、Kubernetes 资源、业务数据库或部署副作用。

## Docs SSOT / 文档同步

- `docs_state`：`complete_docs`；`strategy`：`ssot_first`。
- `durable_docs`（durable docs / 长期文档）：durable specs 已同步 Phase 3.5 唯一 semantic owner、Interface 1.3 public/private I/O、四个 typed exits、finding lifecycle、fresh-final、recorder/validator boundary 与平台分发合同。
- 根 README、workflow README、preset README 与 workflow/preset index、installer、overlay、ownership、quality、skill-package contract 均统一陈述 active 10 Skills/39 exits；production migration 仍独立陈述 3 Skills/11 exits。
- Task planning、逐轮 raw review、assignment/status event、digest、临时测试输出与 rejected candidate qualification 仅保留为 task history，不扩散到公共 Skill package state。
- 当前发布限制：exact remote feature-ref marketplace proof 只能在 reviewed content push 后执行；Remote Marketplace Verification Gate 必须通过并绑定 machine evidence，PR 才能进入 ready。
