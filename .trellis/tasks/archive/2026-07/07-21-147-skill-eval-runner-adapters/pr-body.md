## 变更摘要

- 定义版本化、package-local 的 `evals/evals.json` 行为评测合同，覆盖稳定 case id、typed exit、fixture、deterministic assertions、semantic grading 与 human feedback 边界。
- 新增 `discover-skill-evals` / `run-skill-evals` public commands；runner 实际执行 Interface 1.3 public invocation，记录 actual exit，并按该 exit 的独立 output schema 校验结果。
- 为 shared、Codex、Claude Code、Cursor 提供薄 adapter，统一消费 byte-identical corpus，隔离 prompt/files/native argv，生成 package/repo 外的 trace、transcript、comparison 与 timing evidence。
- current/comparison exact package 分别验证 closed Interface、public assets、corpus 与 fixtures，并生成 side-local invocation/output-schema DTO；合法版本可以声明不同 wrapper，普通结构漂移在执行和 run-root 写入前闭合为结构化 error。
- 同步 canonical workflow、preset inventory、dogfood installed copy、三平台 overlay、representative fixtures、tests、durable Docs SSOT 与 clean install/update/reapply 门禁。

## 影响范围

- 变更覆盖 Guru Team extension、companion runtime、eval schemas、runner/adapters、representative packages、preset/overlay 分发、tests 与文档，共 106 个 reviewed changed files、2 个 task work commits。
- 九个 production Skills 继续保持 Interface 1.2 legacy，不加载 `evals/evals.json`，不迁移其 public payload 或编写完整 coverage corpus；production migration 与 coverage closure 继续由 #145、#146 承接。
- Runner evidence 只用于排障和行为比较，不是 public Skill I/O、typed handoff、gate artifact、checkpoint、审计链或发布证明。
- 不修改 CI/CD、Docker/Compose、Kubernetes/Kustomize/Helm、数据库 schema/migration、Makefile、生产配置、生产数据或权限，无应用部署、配置迁移和数据迁移要求。

## 验证结果

- Shared workflow/runtime：548 passed，13 skipped。
- Skill packages：138 passed；其中最终 finding closure 与 fresh release review 分别独立运行 `EvalRunnerTests`，均为 10 passed。
- Preset installer：39 passed；upstream ownership：6 passed。
- Full throwaway init/update/reapply：exit 0；public marketplace discovery、workflow preview/switch、preset install、installed smoke、`trellis update`、reapply 与 after-update smoke 均通过。
- Installed distribution：400 managed files，0 conflict、0 removal、0 sidecar；canonical/installed/fixture runtime 与 adapter bytes/modes 一致。
- Source/installed package validation、dogfood overlay drift、Python compile、Bash syntax、JSON parse、task validation、`git diff --check` 与递归 `.new`/`.bak` scan 均通过。
- Different-wrapper 正例，以及 missing Interface/outputs/fixture/public assets 的 pre-execution closed failure 负例均通过，无 traceback，失败时不创建 run root。

## Review Gate

- Branch Review 覆盖完整 `origin/main...889387cdfcdf0b0ca8f3e32028c91d19548c3349` 的 106 个文件、2 个 task work commits，以及 planning、implementation handoff、fresh Phase 2、commit plans、Docs SSOT、Issue Scope Ledger 与部署安全边界。
- Round 1 发现 1 个 P1：comparison side 复用 current invocation，合法 wrapper 变化与普通结构漂移不能可靠闭合。
- Commit `889387c` 完成 side-local validation/invocation 修复；Round 2 由原 finding owner 以 `reuse-for-closure` 独立确认 P1 完整关闭，findings=0。
- Round 3 使用从未参与此前 review round 的 fresh reviewer 审查完整 base-to-HEAD diff，P0=0、P1=0、P2=0、P3=0；Review Gate 已绑定当前 HEAD。

## Issue 关闭范围

Closes #147

### 仅关联

- Refs #127：Skill-first 与 upstream extension boundary 的父级架构背景，不由本 PR 关闭。
- Refs #125：standalone runtime dependency 合同背景，不由本 PR 关闭。
- Refs #130：Phase 2 semantic closed-loop Skill 背景，不由本 PR 关闭。

### 后续范围

- #145：迁移 Stage 0 production Skills 并编写其行为用例，不由本 PR 关闭。
- #146：迁移 planning、Phase 2、task commit Skills 并完成 active coverage closure，不由本 PR 关闭。

## 安全说明

- 未引入或暴露 token、credential、private key、signed URL、`.env`、数据库 URL、客户数据或敏感 provider 输出。
- Native adapter 只接收 repo 外 public projection、prompt、staged files、helper 与声明的 argv；private runtime locator、package root 和 corpus locator 不进入 native execution 可见面。
- Corpus、trace 与 digest 校验用于 honest-but-fallible 正常流程 correctness；本 PR 不扩展到恶意篡改、hostile input、非常规竞态、TOCTOU、锁、fault injection 或跨 OS 原子性。
- 无网络服务入口、生产权限、容器镜像、Kubernetes 资源或数据库迁移变化。

## Docs SSOT / 文档同步

- Docs state 为 `complete_docs`，执行策略为 `ssot_first`，task delta 已合并到 durable docs。
- `.trellis/spec/workflow/skill-package-contract.md` 拥有 eval corpus、runner、adapter、comparison、evidence 与 public/private boundary 的长期合同；`quality-guidelines.md` 拥有正负评测门禁。
- `data-contracts.md`、`companion-scripts.md`、preset/docs specs、root/workflow/preset README 与 `docs/requirements/**` 已同步数据边界、脚本职责、分发和用户入口；canonical、installed、fixture 与文档语义一致。
- 逐轮 finding 生命周期、命令输出、hash、agent liveness、planning/check/commit/review 证据只保留为 task history，不扩散到公共 Skill package state。
- 当前 PR 限制：分支尚未 push，因此 exact remote feature-branch marketplace 尚未验证；`trellis-finish-work` 必须在 reviewed content push 后、draft PR 创建前运行 Remote Marketplace Verification Gate 并绑定 passed evidence。
