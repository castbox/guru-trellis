## 变更摘要

- 新增 Trellis upstream ownership durable contract、严格 JSON Schema 与 machine-readable inventory，把当前 43 个 preset legacy overlay 固定为不可扩张的 `path + baseline_sha256` 身份集合，并为每条记录补齐 upstream producer、现有 Guru 责任、replacement owner、blocking/removal issue、removal prerequisite、update/upgrade 语义和安装状态。
- 新增 source-only `validate_upstream_ownership.py` 与 `check-upstream-ownership.sh`。Validator 只检查分类、路径、hash、manifest、owner、prerequisite 和 materialized projection 等确定性事实，不判断是否值得 patch upstream，也不进入用户任务 runtime invocation。
- 将 ownership gate 接入 preset 安装前检查、dogfood overlay drift 和完整 throwaway initial/update/reapply/finish 验证链；installer 在修改目标仓库前 fail closed。
- 固化首次 removal 前后的双 projection 合同：active 条目校验当前 payload bytes，removed 条目校验 Git 历史 materialized baseline，禁止通过同步改写 inventory/hash 绕过 frozen identity。
- 对 malformed inventory、extension manifest 和 Skill registry 输入统一输出稳定、可解析的 JSON error，不再泄漏 Python traceback 或静默接受错误成员。
- 保持两个 workflow、43 个现有 overlay payload、`guru-sync-base`、`guru-create-task-commit` 及 upstream `trellis-*` discovery/routing 相对 issue base 不变；本 PR 不删除 legacy overlay，也不新增 mandatory Skill invocation。

## 影响范围

- Source maintainer gate：新增 ownership inventory/schema/validator、fixtures/tests 和 Bash 入口，并调整 preset source validation、dogfood drift 与 throwaway validation chain。
- Preset installer：安装前增加只读 ownership preflight；验证失败时目标仓库尚未发生 mutation。Validator 自身不会安装到业务仓库，也不成为 extension runtime command。
- Upgrade / update：`trellis update --force` 后必须重新选择 workflow、reapply preset，并在 initial/update/reapply checkpoint 校验 frozen inventory、active/removed projection 与 sidecar 状态。
- 兼容性：现有 workflow、public Skill id/interface/command/schema/typed exit、platform discovery copy 和 43 个 overlay 安装结果保持不变；后续删除只由 #132 在 replacement owner 完成后执行。
- 公共 API：新增 ownership inventory/schema 和 source validation command；未静默改变既有 stable id、schema id 或 runtime command 语义。

## 验证结果

- Ownership validator：6 个 test method、14 个 positive/negative fixture 全部通过，覆盖 frozen set 扩张、active payload drift、首次 removal、removed baseline rewrite、missing owner/issue、unclassified、upstream managed claim，以及 malformed inventory/manifest/registry 的稳定 JSON 错误合同。
- Preset installer：39 tests passed；workflow runtime：292 tests passed；public Skill package/source/distribution：67 tests passed。
- Frozen/active/removed 为 `43/43/0`，clean-init 分类为 `37/6`；inventory 与 materialized identity 都为 `0ca84016a32cd496c4a9ff2a6bdc6637a1e6393abd3d60f3bf3388657ebf8350`。
- `check-dogfood-overlay-drift.sh` 通过；两个 workflow、43 个 overlay payload、`guru-sync-base`、`guru-create-task-commit` 相对 issue base 均为零 diff。
- 完整 clean throwaway 已覆盖 public marketplace discovery、本分支 workflow sample、initial preset install、`trellis update --force`、workflow switch、preset reapply、三次 ownership checkpoint 和 finish fixture，最终递归 `.new` / `.bak` 为 0。
- JSON Schema、JSON fixtures、Python compile、Bash syntax、`git diff --check` 与 task JSONL validation 全部通过。
- 精确远端 feature-ref marketplace verification 将由 `trellis-finish-work` 在 reviewed content push 后、PR 创建前执行并记录；在该 evidence 变为 passed 前不声明远端分支安装链已通过。

## Review Gate

- Branch Review Gate 已在 HEAD `78006a7b643708bf6ecaa7d9f5a1b8ab8a935eb5` 通过，覆盖 `origin/main...HEAD` 的完整两提交、46-path diff。
- Round 001 发现 P1 BR-001：首次 removal 后可同步改写 active/removed identity；以及 P2 BR-002：malformed inventory/manifest 会触发 traceback。修订提交固定 43 条 canonical identity，拆分 active/removed materialized projection，并统一 malformed input 的稳定 JSON 合同。
- Fresh Phase 2 同范围发现 malformed Skill registry / `supported_platforms` 会被静默接受，已并入 BR-002 修复和回归。
- Round 002 由原 finding owner 对当前 HEAD 完成 closure，开放 finding 为 0；Round 003 由未参与实现、Phase 2 或前序 review 的 fresh reviewer 独立完成最终放行，开放 `P0=0, P1=0, P2=0, P3=0`。
- 审查明确覆盖需求、设计、实现、测试、Docs SSOT、installer/update、canonical/dogfood/platform 非回归、安全、部署影响与 Issue Scope。

## Issue 关闭范围

Closes #128

### 仅引用或相关

- Refs #127：umbrella 架构上下文，本 PR 不关闭。
- Refs #112：Intake replacement owner，本 PR 不实现、不关闭。
- Refs #119：Finish replacement owner，本 PR 不实现、不关闭。
- Follow-up #129、#130、#131：分别实现 planning/check/review closed-loop Skill。
- Follow-up #132：完成 routing 集成并在 replacement prerequisite 满足后删除 43 个 legacy overlay；本 PR 不提前执行 removal。

## Docs SSOT / 文档同步

- Docs state：`partial_docs`；策略：`ssot_first`。
- Durable docs / 长期文档：已新增 `.trellis/spec/preset/upstream-ownership.md`，并同步 `.trellis/spec/preset/index.md`、`installer.md`、`overlay-guidelines.md`、仓库 `README.md`、preset README 与 workflow README。
- Durable contract 已覆盖 ownership 分类、frozen identity、active/removed projection、script boundary、gate checkpoints、update/upgrade 冲突语义、removal prerequisite 与 fail-closed remediation。
- `task_history`：仅保留 issue 调查证据、clean-init 临时输出、planning approval、Phase 2 finding 生命周期、task commit plan、review round 与 liveness 记录；这些内容未进入公共 skill package state。
- `followup_or_limitation`：精确远端 feature-ref marketplace verification 仍须由正式 finish-work 在 push 后完成；#129-#131 承接 planning/check/review Skill，#132 承接 routing 集成和 legacy overlay removal，本 PR 不提前实现。

## 安全说明

- 敏感字面量与任务 artifact 审查未发现 token、secret、private key、数据库 URL、签名 URL、客户数据或本机绝对路径；public JSON error 只包含稳定 `code/path/detail`。
- Validator 使用 source-root containment、严格 schema/type normalization、固定 baseline identity 和显式 inventory membership，错误输入在目标 mutation 与业务副作用前 fail closed。
- 本次不修改 `.github/workflows`、CI/CD、服务/API、业务 CLI、worker、schedule、queue、数据库 schema/migration、Dockerfile、Compose、Kubernetes/Kustomize/Helm、Makefile、运行时配置或 secret 管理，无业务部署拓扑和数据迁移影响。
