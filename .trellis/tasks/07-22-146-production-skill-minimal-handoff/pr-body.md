## 变更摘要

- 将 `guru-approve-task-plan`、`guru-check-task`、`guru-create-task-commit` 三个 production Skills 迁移到 Interface 1.3 + `minimal_handoff`，覆盖 10 个 public input profiles 与 11 个 typed exits。
- 为每个输入 profile 和 exit 建立 closed schema/example、唯一 consumer contract、薄 projection 与 direct-use proof；public DTO 只保留下一消费者直接需要的字段，runtime facts、digest、完整审查历史与 recovery state 保持 private。
- 为三个 re-entry 路径增加最小 `skill_input_authoring_seed`，由下一个 semantic owner fresh author 完整输入；seed 字段与 fresh authoring 字段互斥，不把 producer private artifact 传给 consumer。
- 闭合 `clarify_scope` routing-only continuation：按三字段 handoff fresh reread task-local context，mandatory invoke requirements clarification，并在 unknown、multiple、unmapped 或 stale 状态下 fail closed。
- 扩展 production eval native adapter，只允许这三个 production packages 使用真实 public wrapper 和 actual-exit schema validation；Stage 0 与其它 package 行为保持不变。
- 同步 canonical、installed、Agents、Codex、Claude、Cursor、workflow/preset registry、production migration manifest、tests 与 durable Docs SSOT。

## 影响范围

- 变更覆盖三个 production Skill packages、10 profiles、11 exits、consumer/projection schemas、shared runtime、native eval adapter、preset installer、五类 installed/platform copies、tests、workflow/requirements/README Docs SSOT 与 task evidence。
- Stage 0 六包继续保持 #145 已完成的 Interface 1.3 minimal handoff，整体 active closure 为 9 Skills/35 exits/21 consumer targets/0 legacy。
- Stable Skill id、typed exit id、semantic owner、human confirmation、planning/Phase 2/commit judgment ownership与 archive read-only 语义保持不变。
- 不修改 Trellis upstream、全局 npm 包或 `node_modules`，不引入 repo-level pre-task cache、workspace journal 或 private runtime state 到公共 package。
- 不涉及 GitHub Actions、Docker/Compose、Kubernetes/Kustomize/Helm、数据库 schema/migration、Makefile、生产配置或业务数据；无需服务部署、停机、配置迁移或数据迁移。

## 验证结果

- Skill package tests：166/166 passed。
- Shared workflow/runtime：557 passed，13 个 capability-dependent tests skipped。
- Preset installer：45/45 passed；upstream ownership：6/6 passed。
- Production source corpora：12/12 passed；Stage 0 source corpora：24/24 passed；全九包 installed corpora 通过。
- Source/installed closure：9 Skills/35 exits/21 targets/0 legacy；installed 1711 managed files，sidecar/removal/conflict 均为 0。
- 108 个 production tracked package files 在 installed、Agents、Codex、Claude、Cursor 五份副本中为 0 mismatch。
- Source/installed validators、dogfood overlay drift、changed JSON、Python/shell syntax、task validation、`git diff --check`、secret/sensitive 与 deployment scans 通过。
- Throwaway install、workflow preview/switch、`trellis update`、preset reapply 与 README 命令交叉核对通过；exact remote feature-branch proof 由本 closeout 在 reviewed content push 后执行。

## Review Gate

- Branch Review 覆盖完整 `origin/main...9519ff8f2c9bd22e697d3ecc8196ad153ea76106` diff，共 629 paths、3 个 task work commits，以及 live Issue #146、R1-R17/AC1-AC22、planning、implementation handoff、fresh Phase 2、三个 commit plans、Docs SSOT、issue scope、install/update/upgrade、部署与安全边界。
- Round 001 发现 production eval adapter scope authority P1 与 `clarify_scope` router P2；补充 live authority、planning/ledger、runtime routing 和 tests 后，由原 finding owner在 Round 002 关闭。
- Round 003 发现 durable flow SSOT 把 #146 completion 写成未来责任的 P3；commit `9519ff8f` 修正后，原 closure 尝试因平台 terminal error 未完成，fresh replacement 在 Round 004 按正式 replacement chain 关闭。
- Round 005 使用从未参与前四轮 finding ownership、closure 或实现的 fresh reviewer 独立审查，P0=0、P1=0、P2=0、P3=0；Branch Review Gate 已绑定当前 HEAD。

## Issue 关闭范围

Closes #146

### 仅关联或后续范围

- Refs #127：Skill-first 流程收敛父级路线，保持 open，不由本 PR 关闭。
- Refs #131：`guru-review-branch` 后续消费者，保持 open，不由本 PR 关闭。
- Refs #132：planning/check/review Skills 后续集成，保持 open，不由本 PR 关闭。

## 安全说明

- 未引入或暴露 token、credential、private key、signed URL、`.env`、数据库 URL、客户数据或敏感 provider 输出；token-boundary secret scan 为 0。
- Public handoff 只包含 consumer 直接使用的最小字段；Git/GitHub/Trellis live facts、digest、完整 scan/review history、file metadata、transaction journal 与 recovery state 保持 runtime private。
- Native adapter 只向 Agent 暴露 public projection、prompt、staged files 与声明 argv；private runtime locator、package root、corpus locator 和 owner checkpoint 不进入 Agent-facing input。
- Hash、digest 与 freshness 只服务 honest-but-fallible 正常流程 correctness；本 PR 不扩展到恶意伪造、hostile input、锁、并发压力、TOCTOU、额外 fault injection、crash consistency 或跨 OS 原子性。
- 没有生产权限、网络服务入口、容器镜像、Kubernetes 资源、数据库或部署副作用。

## Docs SSOT / 文档同步

- `docs_state`：`complete_docs`；`strategy`：`ssot_first`。
- `durable_docs`（长期文档）：15 个 durable paths 已同步，包括 workflow/preset/docs specs，root/workflow/preset README，以及 `docs/requirements/README.md`、`requirement-main.md`、`guru-team-trellis-flow.md`。
- `.trellis/spec/workflow/skill-package-contract.md` 拥有 minimal public/private I/O、consumer/projection、production eval 与 activation 的长期合同；`workflow-contract.md`、`data-contracts.md`、`companion-scripts.md`、`quality-guidelines.md` 分别承接流程、数据、脚本与质量边界。
- Preset/docs/upstream-ownership specs 与公共 README 已同步安装、update/reapply、平台分发和用户入口。
- `task_history_only`：具体命令输出、digest、proposal/action trail、逐轮 finding lifecycle、agent liveness 与 recovery evidence 只保留为 task history，不扩散到公共 Skill package state。
- 当前发布限制：exact remote feature-branch marketplace proof 只能在 reviewed content push 后执行；Remote Marketplace Verification Gate 必须通过并绑定 machine evidence，PR 才能进入 ready。
