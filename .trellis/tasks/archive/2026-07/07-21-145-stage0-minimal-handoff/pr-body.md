## 变更摘要

- 将 `guru-sync-base`、`guru-discover-change-context`、`guru-clarify-requirements`、`guru-review-contract-wording`、`guru-review-change-request`、`guru-create-task-workspace` 六个 Stage 0 Skills 迁移到 Interface 1.3 + `minimal_handoff`，精确覆盖 24 个 typed exits。
- 为每个结构不同的 public input profile 和每个 exit 建立 closed schema/example、唯一 consumer contract、薄 projection 与 direct-use proof；private artifact、runtime-derived facts、digest 与审查历史不再进入 public handoff DTO。
- 保留 `guru-sync-base` optional base fallback：显式 base 优先；省略时继续由 formal resolver 独占 configured scalar -> ordered candidates -> remote default，不由 semantic producer 硬编码 `main`。
- 闭合 production semantic eval：六份 canonical corpus 通过 shared/Codex/Claude/Cursor adapter 执行真实 public invocation，按 actual exit 选择 output schema，`expected_exit` 仅用于事后断言。
- 将六包作为单一 versioned activation unit 通过 preset staging transaction 安装；unknown local edit 或 installed validation failure 保留旧完整 graph，known managed upgrade 支持 `.bak` 确认与 reapply。
- 同步 canonical、installed、shared、Codex、Claude、Cursor、workflow/preset registry、migration manifest、tests 与 durable Docs SSOT。

## 影响范围

- 变更覆盖 Guru Team Stage 0 六包、24 exits、consumer/projection schemas、shared runtime、eval adapter、preset installer、五类 installed/platform copies、tests、workflow/requirements/README Docs SSOT 与 task evidence。
- `guru-approve-task-plan`、`guru-check-task`、`guru-create-task-commit` 三包继续保持 Interface 1.2 + `legacy`，由 #146 独立迁移。
- Stable Skill id、typed exit id、semantic owner、human confirmation、issue/workspace mutation ownership与 archive read-only 语义保持不变。
- 不修改 Trellis upstream、全局 npm 包或 `node_modules`，不新增 repo-level pre-task cache、workspace journal 或平台专用 corpus。
- 不涉及 GitHub Actions、Docker/Compose、Kubernetes/Kustomize/Helm、数据库 schema/migration、Makefile、dependency lock/config、生产配置或业务数据；无需服务部署、停机、配置迁移或数据迁移。

## 验证结果

- Skill package tests：161/161 passed。
- Shared workflow/runtime：548/548 passed，13 个 capability-dependent tests skipped。
- Preset installer：45/45 passed；upstream ownership：6/6 passed。
- Shared production eval：六包 24/24 cases passed；activation set=`6/24`，active packages=`9`，minimal=`6`，legacy=`3`。
- Source/installed validators、dogfood overlay drift、upstream ownership、changed JSON、Python/shell syntax、task validation、`git diff --check` 与 recursive sidecar scan 通过。
- Canonical 到 installed/shared/Codex/Claude/Cursor 六包 package bytes/modes parity：30/30 passed。
- Full throwaway 验证通过 workflow marketplace discovery、local unpublished workflow sample、clean install、Stage 0 normal/refresh/stop/mutation/recovery smokes、pre-#145 upgrade、workflow preview/switch、`trellis update`、preset reapply、selected-platform parity 与最终零 `.new`/`.bak`。
- 未发布分支 default marketplace guard 按合同 exit 2，未把 public `main` sample 冒充为当前 feature branch proof。

## Review Gate

- Branch Review 覆盖完整 `origin/main...9f941087994eb4ea1e4fa9e0c407f8ba3ffd84f8` diff，共 1258 paths、3 个 task work commits，以及 planning、implementation handoff、fresh Phase 2、三个 commit plans、Docs SSOT、issue scope、upgrade/update、部署与安全边界。
- Round 1 发现 preset conflict mixed graph P1；commit `ded63e71e5bab787c5d795a300e3507142b18521` 修复后由原 finding owner 在 Round 2 关闭。
- Round 3 发现 non-main optional fallback 被改写为显式 `main` 的 P1；commit `9f941087994eb4ea1e4fa9e0c407f8ba3ffd84f8` 修复后由原 finding owner 在 Round 4 关闭。
- Round 5 使用从未参与前四轮 finding ownership、closure 或实现的 fresh reviewer 独立审查，P0=0、P1=0、P2=0、P3=0；Review Gate 已绑定当前 HEAD。

## Issue 关闭范围

Closes #145

### 已关闭依赖引用

- Refs #144：Interface 1.3 optional scalar compatibility authority；保持 closed，不再次关闭。
- Refs #147：production semantic eval runner/adapter authority；保持 closed，不再次关闭。

### 仅关联或后续范围

- #146：planning、Phase 2 与 task commit 三包迁移，保持 open，不由本 PR 关闭。
- #98、#127、#132：parent/related scope，保持 open，不由本 PR 关闭。

## 安全说明

- 未引入或暴露 token、credential、private key、signed URL、`.env`、数据库 URL、客户数据或敏感 provider 输出；secret-shaped diff scan 为 0。
- Eval/native adapter 只传递 public projection、prompt、staged files 与声明 argv；private runtime locator、package root、corpus locator 和 owner checkpoint 不进入 Agent-facing public input。
- Hash、digest、freshness 与 transaction 只服务 honest-but-fallible 正常流程 correctness；本 PR 不扩展到恶意伪造、hostile input、锁、并发压力、TOCTOU、额外 fault injection、crash consistency 或跨 OS 原子性。
- 没有生产权限、网络服务入口、容器镜像、Kubernetes 资源、数据库或部署副作用。

## Docs SSOT / 文档同步

- `docs_state`：`complete_docs`；`strategy`：`ssot_first`。
- `durable_docs`（长期文档）：`.trellis/spec/workflow/skill-package-contract.md`、`data-contracts.md`、`companion-scripts.md`、`quality-guidelines.md`、`index.md`，`.trellis/spec/preset/installer.md`、`overlay-guidelines.md`、`upstream-ownership.md`，`.trellis/spec/docs/public-docs.md`，root/workflow/preset 三份 README，以及 `docs/requirements/README.md`、`requirement-main.md`、`guru-team-trellis-flow.md`；共 15 个 durable paths，已同步并由 fresh Phase 2 与最终 Branch Review 复核。
- `.trellis/spec/workflow/skill-package-contract.md` 拥有 minimal public/private I/O、consumer/projection、production eval 与 activation 的长期合同；`data-contracts.md`、`companion-scripts.md`、`quality-guidelines.md` 承接数据、脚本与质量边界。
- Preset/docs/upstream-ownership specs、root/workflow/preset README 与 `docs/requirements/**` 已同步安装、upgrade/update、平台分发、optional resolver 和用户入口。
- `task_history_only`：具体命令输出、digest、逐轮 finding 生命周期、agent liveness 与恢复证据只保留为 task history，不扩散到公共 Skill package state。
- 当前发布限制：exact remote feature-branch marketplace proof 只能在 reviewed content push 后执行；`trellis-finish-work` 的 Remote Marketplace Verification Gate 必须通过并绑定 evidence，PR 才能进入 ready。Authenticated Claude native live probe 仍受本地 capability 限制，repository protocol/fake-native/unsupported tests 与四平台 parity 已通过。
