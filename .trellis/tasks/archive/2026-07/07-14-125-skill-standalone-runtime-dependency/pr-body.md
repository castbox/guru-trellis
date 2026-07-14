## 变更摘要

- 明确 public Skill 的 `workflow` / `standalone` 只是 routing mode：`standalone` 允许平台 direct discovery，但仍依赖完整且兼容的 Guru Team preset、extension runtime、shared dispatcher 与 managed package inventory。
- 将 Skill interface 升级到 schema 1.1，新增闭集 `runtime_dependency`、mode `routing` 与 validator `runtime_command`；extension manifest 同步发布 `skill_runtime` API capability。
- 新增 shared `run-skill-command` dispatcher。Package command 保持 thin wrapper，只传递 package/validator identity 与原始参数；缺失 manifest、dispatcher、API/command 不兼容、managed drift 或单目录复制都会在业务副作用前 fail closed，并给出完整 preset 安装/升级提示。
- 统一 source validator 与 runtime resolver 的 dispatcher 自指映射判定，关闭“source gate 通过、runtime 调用拒绝”的语义漂移，并加入精确永久回归。
- 同步 canonical workflow/package、preset installer、dogfood 与 Codex/Cursor/Claude 平台副本、安装清单、durable requirements、spec 和 public README。

## 影响范围

- Public Skill 合同：mode routing、runtime dependency、non-portable package 边界、validator command mapping 与 typed closed-loop 语义。
- Guru Team runtime：新增共享 dispatcher，并复用既有 parser、task/gate 解析、Git snapshot、exact staging、transaction、rollback 与 result validation，未把共享实现复制进 Skill package。
- 分发与升级：preset 安装 extension manifest、dispatcher、interface schema、active package 和所选平台 discovery copies；旧 runtime 或残留 `.new` / `.bak` 会阻塞调用。
- 文档：更新 durable requirements、四份 `.trellis/spec/**`、仓库 README、workflow README 与 preset README。
- 兼容性：保留稳定 mode id `workflow` / `standalone`、Skill id 与 typed exits；interface schema identity 从 1.0 升至 1.1，extension 待发布版本递增至 `0.6.5-guru.6`。

## 验证结果

- Canonical package contract：5 tests passed。
- Skill package/source/distribution/runtime dispatcher：65 tests passed。
- Preset installer：36 tests passed。
- Shared runtime：275 tests passed。
- 合计 381 tests passed；F-001 永久回归验证 schema 合法、dispatcher 已发布且 source validator 只返回唯一 self-mapping error。
- `check-skill-packages --mode source` 与 `--mode installed` 通过；installed inventory 为 43 个 managed files、三平台副本、0 sidecar/removal/conflict。
- Direct discovery wrapper probe、JSON/Bash/Python static、canonical/dogfood/platform byte 与 executable mode、dogfood overlay drift、`git diff --check` 和 task JSONL validation 全部通过。
- Clean throwaway 覆盖 public marketplace discovery、本分支 workflow sample、初次 preset 安装、standalone probe、`trellis update`、workflow re-selection、preset reapply、二次 probe、source/installed validation 与 closeout smoke；recursive `.new` / `.bak` 扫描为 0。
- Exact feature-ref remote marketplace verification 由 `trellis-finish-work` 在 reviewed content push 后、PR 创建前绑定远端 HEAD 执行；pending evidence 不能满足发布门禁。

## Review Gate

- Branch Review Gate 已在 HEAD `93d9a416bd6b34a87844dde5d4d9da363af729c2` 通过，范围为 `origin/feat/122-guru-create-task-commit...HEAD` 的完整两提交 diff。
- Round 001 发现 P2 F-001：source validator 接受 dispatcher 自指 `runtime_command`；revision commit 增加 source/runtime 共用判定与精确回归。
- Round 002 由 finding owner 完成 closure，`findings_count=0`；Round 003 由未参与实现、Phase 2、finding 或前序 review 的 fresh reviewer 完成最终放行，`findings_count=0`。
- 最终开放 findings：`P0=0, P1=0, P2=0, P3=0`。审查覆盖需求、设计、实现、测试、Docs SSOT、installer/update、canonical/platform drift、安全与部署影响。

## Issue 关闭范围

Closes #125

### 仅引用或相关

- Refs #122
- 依赖 PR #124；本 PR 是以 `feat/122-guru-create-task-commit` 为 base 的 stacked PR，不改变 #122 / PR #124 的关闭语义。

## Docs SSOT / 文档同步

- Docs state：`partial_docs`；策略：`ssot_first`。
- Durable docs 已更新：`.trellis/spec/workflow/skill-package-contract.md`、`.trellis/spec/workflow/companion-scripts.md`、`.trellis/spec/preset/installer.md`、`.trellis/spec/docs/public-docs.md`、`docs/requirements/**`、canonical workflow/package contract 以及三份 public README。
- 已回写的 task delta：mode routing 定义、runtime dependency 字段、non-portable 边界、fail-closed remediation、dispatcher 单一来源与安装/update-reapply 验证矩阵。
- 仅保留为 task history：stacked base 决策、逐轮 finding/closure、Phase 2 与 Branch Review 执行证据。
- 当前限制：PR #124 合并后必须将本 PR retarget 到 `main`，并按新的 base-to-HEAD diff 重跑 freshness-sensitive Phase 2、Branch Review 与 exact remote marketplace gate。

## 安全说明

- 敏感字面量扫描未发现 token、private key、GitHub token、AWS key、数据库 URL、签名 URL或客户数据；public error 不包含 secret 或本机绝对路径。
- Runtime command 只能来自 closed validator id、installed interface、published command inventory 与 managed executable layout；component-wise `lstat`、manifest/API/inventory、copy hash/mode、sidecar/drift gate 保持 fail closed，不存在 legacy fallback。
- 本次未修改 `.github/workflows`、服务/API、业务 CLI、worker、schedule、queue、数据库 schema/migration、Dockerfile、Compose、Kubernetes/Kustomize/Helm 或 Makefile，无业务部署拓扑与运行时配置变更。
- 本 PR 不发布 release tag；`0.6.5-guru.6` 在对应 merge commit/tag 和远端验证完成前不是 stable source。
