# 技术设计

## 1. 设计目标

以 #161 已合并 public contracts 为不可重写的 producer/owner 层，将 #132 限定为四类集成工作：global workflow graph、consumer projection、upstream ownership migration、安装与平台 discovery acceptance。最终状态必须让 Trellis upstream 与 Guru Team extension 各自只管理自己的 namespace。

## 2. Authority 与分层

Live integration base 固定为 `main@c8cdd9e7fbb73687cd700c1dbbb7a5907307476f`。PR #167 提供 #161 主体 public contracts，PR #168 只收紧 Trellis template provenance 下的 candidate-hygiene correctness；#132 不扩写该修复，也不重审 #161 owner semantics。

### 2.1 Canonical 层

- Workflow：`trellis/workflows/guru-team/workflow.md`。
- Skill graph：`trellis/skills/guru-team/registry.json`、各 package `interface.json`、per-exit schemas/examples、`consumers/**`。
- Preset：`trellis/presets/guru-team/`、`trellis/guru-team-extension.json`。
- Durable specs：`.trellis/spec/workflow/**`、`.trellis/spec/preset/**`、`.trellis/spec/docs/public-docs.md`。

### 2.2 Installed/dogfood projection

- `.trellis/workflow.md` 必须由 canonical workflow 同步。
- `.trellis/guru-team/**` 与 Shared/Codex/Claude/Cursor 的 `guru-*` package copies 必须由 preset 安装并保持 byte identity。
- Dogfood upstream-owned files 不再由 overlay canonical source 控制；其 bytes 由官方 Trellis init/update/upgrade 管理。

### 2.3 禁止依赖

- Workflow 与平台 entry 不读取 owner private checkpoint 或 `guru_team_trellis.py` 来推导 semantic route。
- Installer/validator 不判断需求、review pass、finding severity、close scope 或 publication readiness。
- Dogfood copy 不能反向成为 canonical source。

### 2.4 Planning continuation

- 当前 task 已是 `in_progress`；Planning schema 3.0 的 owner checkpoint 是 ignored-runtime private evidence，并在 typed output 成功投影后退出。
- 本次基于 PR #168/current main 更新 planning authority 后，重新执行 `guru-review-contract-wording(planning_artifacts)` 与 `guru-approve-task-plan`。
- `approved` 由 `phase-1-task-activation` 消费；对已是 `in_progress` 的同一 task，activation 只重验 workspace/DTO 并执行重复运行结果不变的 `task.py start`，不回写第二份 planning authority。

## 3. Thin workflow graph

Global workflow 为每个 owner 保留一个 invocation marker 和完整 typed exits，出口只映射到一个 consumer 或 stop：

```text
guru-sync-base -> guru-discover-change-context
-> guru-clarify-requirements
-> guru-review-contract-wording
-> guru-review-change-request
-> guru-create-task-workspace
-> planning artifacts / guru-review-contract-wording(planning_artifacts)
-> guru-approve-task-plan
-> task activation / implementation
-> guru-check-task
-> guru-create-task-commit
-> guru-review-branch
-> guru-review-task-publication
-> guru-finalize-task
   verification_required -> guru-verify-extension-installation -> same finalizer
```

Revision、stale、implementation、scope、reprepare/resume exits 只按 interface 中已声明 consumer 路由。Workflow 不复述 owner 的 entry fields、semantic dimensions、finding loop、confirmation、recorder/checker、artifact lifecycle 或 recovery 算法。

Global workflow 仍拥有并只拥有：phase order、interaction budget、workspace boundary、Docs SSOT、Issue Scope Ledger、human artifact presentation、task activation 与 finalizer side-effect boundary。

## 4. Public I/O projection

### 4.1 单一来源

- Producer output：producer package 的 per-exit schema。
- Consumer input：consumer 自己的 input schema。
- Projection：producer `interface.json` 中唯一 `projections[]` edge；操作集合限定为 `direct`、`select`、`rename` 与确定性规范化。
- Target authoring：仅在 target profile 明确需要 fresh semantic fields 时，由 target-owned `skill_input_authoring_seed` 分区拥有。

### 4.2 验证

- `check-skill-packages` 继续验证 13 active Skills、51 exits、consumer uniqueness、schema/example、authoring partition 与 platform copy identity。
- 增加/调整 regression，使 workflow/platform wrapper 不能 import private runtime、不能读取 producer private artifacts，也不能接受多个 consumer。
- #161 package internals、private schemas 与 owner tests 只作为 regression，不在 #132 修改语义。

## 5. Ownership inventory 与 overlay 迁移

### 5.1 Inventory tombstone

43 个历史 entry 保持原 path 与 `baseline_sha256`，统一执行：

- `category: upstream_owned`
- `migration_state: removed`
- 删除 `current_payload_sha256`
- `dogfood_status: removed_with_audit_history`
- `target_business_repo_status: no_longer_installed`
- 保留 replacement owners、blocking/removal issues、producer 与历史说明

Validator 继续固定 43-path baseline identity，但最终必须报告 `active_count=0`、`removed_count=43`。

### 5.2 Overlay 与 managed claims

- 从 `trellis/presets/guru-team/overlays/` 删除 43 个 upstream path。
- 只保留三个 Guru-owned explicit finish entry：Codex、Claude、Cursor 的 `guru-finish-work`。
- `trellis/guru-team-extension.json.public_api.managed_paths` 删除 7 个 transitional claim，保留精确 Guru namespace claims；不得用 broad directory claim 重新覆盖 upstream files。

## 6. Installer migration 状态机

Installer 在任何 target mutation 前读取 checker-passed ownership inventory，并仅针对 `upstream_owned/removed` tombstone 执行客观 migration preflight。

| Target 状态 | 判定依据 | 行为 |
| --- | --- | --- |
| path 不存在 | `lstat` | 不安装、不创建，记录 already-missing/不管理 |
| clean upstream | current hash 匹配 `.trellis/.template-hashes.json` 对应官方 hash | 原样保留，从 Guru managed inventory 移除 |
| upstream-generated path 仍是已知 Guru legacy payload | current hash 匹配 tombstone baseline/current historical payload，且 `generated_in_clean_init=true` | 保留并 fail closed，要求先执行官方 `trellis update/upgrade`；preset 不合成 upstream bytes |
| legacy-only path 仍是已知 Guru payload | current hash 匹配历史 payload，且 `generated_in_clean_init=false` | 删除该已知 managed legacy file，记录 removal |
| 未知或本地修改 | 不匹配 clean upstream 与任何已知 Guru payload | 原文件保留，生成 `.new` remediation sidecar/明确 conflict，阻止成功激活 |

Migration 成功后，installed extension manifest 不再把 43 个 upstream path 列入 `install.managed_assets`。Unresolved `.new/.bak`、invalid provenance 或旧 Guru-generated path 均阻止 `status=ok`。

## 7. Update/upgrade/reapply 顺序

Existing repository 的规范迁移顺序为：

1. 运行官方 `trellis update/upgrade`，让 upstream-generated files 回到官方 template ownership。
2. 重新选择 `guru-team` marketplace workflow；workflow 属于官方支持的 marketplace surface。
3. 运行新版 Guru preset reapply；安装器只恢复 `.trellis/guru-team/**`、`guru-*` discovery copies 与明确 Guru namespace assets。
4. 处理 installer 报告的 `.new/.bak` 或 local-edit conflict。
5. 运行 source/installed contract、ownership、platform identity、dogfood drift 与递归 sidecar checks。

Fresh install 从官方 init files 开始，因此 preset initial apply 不应触碰 upstream-owned files。

## 8. 平台 discovery

- Shared：`.agents/skills/guru-*/**`。
- Codex：Shared discovery 加 `.codex/skills/guru-*/**`，显式 finish entry 使用 `.codex/prompts/guru-finish-work.md`。
- Claude：`.claude/skills/guru-*/**`，显式 finish entry 使用 `.claude/commands/guru/finish-work.md`。
- Cursor：`.cursor/skills/guru-*/**`，显式 finish entry 使用 `.cursor/commands/guru-finish-work.md`。

`trellis-start`、`trellis-continue`、`trellis-finish-work`、Trellis agents/hooks/runtime agents 由 upstream 提供。Mandatory Guru routing 由 active `.trellis/workflow.md` 的 stable Skill markers 保证，不由 auto-match 或 patched upstream entry 保证。

## 9. Docs SSOT Plan

- Docs state：`stale_docs`。
- Strategy：`ssot_first`。
- 原因：现有 durable specs 与 README 明确描述 active transitional overlays 和兼容 router；若先改代码会造成 ownership/installer 行为无 semantic authority。
- 必须更新的 durable docs：
  - `.trellis/spec/workflow/workflow-contract.md`
  - `.trellis/spec/workflow/skill-package-contract.md`
  - `.trellis/spec/workflow/quality-guidelines.md`
  - `.trellis/spec/workflow/companion-scripts.md`
  - `.trellis/spec/preset/upstream-ownership.md`
  - `.trellis/spec/preset/installer.md`
  - `.trellis/spec/preset/overlay-guidelines.md`
  - `.trellis/spec/docs/public-docs.md`
  - `README.md`
  - `trellis/workflows/guru-team/README.md`
  - `trellis/presets/guru-team/README.md`
- Task artifact delta：本设计中的 thin graph、tombstone migration、provenance state machine 与 acceptance matrix 必须合并回上述 durable docs。
- Merge checkpoint：实现第一步先更新 durable specs；代码、schema、tests 只接受与已更新 specs 一致的行为。

## 10. 回滚与风险控制

- Canonical overlay 删除前先使 inventory/schema/validator 表达 removed tombstone；validator 必须在不完整迁移时 fail closed。
- Installer 变化使用 staging repository 原子激活路径；conflict 时只物化 sidecar，不激活任何未完成结果。
- Dogfood 迁移前保留 Git diff 可审查；不清理无关 worktree，不修改 Trellis upstream 或全局包。
- 若 combined acceptance 暴露 #161 public contract 缺陷，停止 #132 projection patch，记录最小复现并回到 #161。
