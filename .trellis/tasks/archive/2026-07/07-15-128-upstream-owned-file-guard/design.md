# #128 技术设计

## 1. 设计摘要

本次变更新增一个 source-repository ownership 控制面：durable spec 承载人类可审查语义，JSON inventory/schema 承载冻结事实，Python validator 执行确定性校验，Bash wrapper 提供稳定 maintainer command。Preset apply、dogfood drift、throwaway install/update/reapply 只消费 validator 结果，不承担 ownership 语义判断。

```text
durable spec + reviewed issue decisions
                |
                v
strict inventory/schema -----> source validator -----> structured facts + exit code
          |                           |                         |
          |                           +--> preset pre-mutation  |
          |                           +--> dogfood drift        |
          |                           +--> throwaway stages     |
          v                                                     v
43 frozen legacy entries                              AI Review Gate 复核语义非回归
```

## 2. 权威输入与边界

### 2.1 语义权威

- GitHub issue #128 定义分类、冻结规则、迁移字段、非回归合同和关闭范围。
- GitHub issue #127 定义最终 upstream/Guru ownership 架构。
- GitHub issues #112、#119、#129、#130、#131 定义 replacement owners；#132 独占 overlay removal。
- `.trellis/spec/preset/upstream-ownership.md` 将成为仓库 durable ownership SSOT。
- 官方 Trellis 文档定义 workflow Markdown、generated files、template hash 和 update 行为。

### 2.2 确定性权威

- `trellis/presets/guru-team/ownership/upstream-ownership.schema.json` 定义结构与 enum。
- `trellis/presets/guru-team/ownership/upstream-ownership.json` 定义 reviewed classification、frozen baseline 和 migration inventory。
- Overlay 文件字节与 SHA-256 是 payload 非回归事实。
- `trellis/guru-team-extension.json.public_api.managed_paths` 是当前 public managed path claim 清单。
- `MANAGED_ASSET_PATHS` 与 skill registry/package inventory 是 installer 实际 managed asset 事实。

### 2.3 禁止边界

- Validator 不得修改 inventory、overlay、manifest、task artifact 或 target repo。
- Validator 不得产生 AI finding、severity、scope classification 或 route intent。
- Gate 不得写入 workflow、Skill package、platform entry 或用户 task runtime。

## 3. 文件布局

```text
.trellis/spec/preset/
  upstream-ownership.md

trellis/presets/guru-team/
  ownership/
    upstream-ownership.schema.json
    upstream-ownership.json
  scripts/bash/
    check-upstream-ownership.sh
  scripts/python/
    validate_upstream_ownership.py
    test_upstream_ownership.py
    fixtures/upstream-ownership/
      positive-baseline.json
      positive-guru-owned-paths.json
      negative-new-upstream-overlay.json
      negative-expanded-legacy.json
      negative-payload-drift.json
      negative-missing-removal-owner.json
      negative-unclassified.json
```

现有 `apply_guru_team_trellis_preset.py`、`check-dogfood-overlay-drift.sh`、`verify-throwaway-install.sh` 只增加 validator 调用，不复制其结构规则。

## 4. Inventory 合同

### 4.1 顶层字段

Inventory 顶层使用固定字段：

- `schema_version`
- `inventory_id`
- `target_trellis_cli`
- `baseline`
- `ownership_categories`
- `guru_owned_rules`
- `managed_path_claims`
- `legacy_entries`

未知顶层字段必须失败。`ownership_categories` 必须恰好包含 `upstream_owned`、`guru_owned`、`transitional_legacy`、`unclassified`。

### 4.2 Frozen baseline

`baseline` 固定：

- base commit `291b57b6c02872320a4dce0626a2f718399b8f56`
- frozen path count `43`
- sorted path-set SHA-256
- active payload aggregate SHA-256
- clean init 命令与 Trellis CLI `0.6.5`
- clean init 结果 `generated=37`、`legacy_not_generated=6`

Validator 必须从实际 overlay tree 重新计算 path count、path-set digest 与 active payload digest。

### 4.3 Legacy entry

每条 `legacy_entries[]` 使用固定字段：

- `path`
- `category`
- `migration_state`
- `baseline_sha256`
- `upstream_producer`
- `current_guru_behavior`
- `replacement_owners[]`
- `blocking_issues[]`
- `removal_issue`
- `update_upgrade_conflict`
- `dogfood_status`
- `target_business_repo_status`

当前状态矩阵：

| category | migration_state | canonical overlay | hash 条件 |
| --- | --- | --- | --- |
| `transitional_legacy` | `active` | 必须存在 | 必须匹配 `baseline_sha256` |
| `upstream_owned` | `removed` | 必须不存在 | 保留历史 `baseline_sha256` |

`guru_owned` 不得出现在 frozen legacy entry；它由 `guru_owned_rules` 与 `managed_path_claims` 分类。`unclassified` 在任何位置都失败。

### 4.4 Replacement owner 映射

- Intake/start/context 类 legacy 行为绑定 #112 与最终 #132。
- Planning approval 与 planning artifact 类 legacy 行为绑定 `guru-approve-task-plan` / #129 与最终 #132。
- Phase 2 check 类 legacy 行为绑定 `guru-check-task` / #130 与最终 #132。
- Branch Review 类 legacy 行为绑定 `guru-review-branch` / #131 与最终 #132。
- Finish entry 类 legacy 行为绑定 `guru-review-task-publication`、`guru-verify-extension-installation`、`guru-finalize-task` / #119 与最终 #132。
- 跨 phase `trellis-continue` legacy 行为同时绑定 #129、#130、#131，removal issue 固定为 #132。

## 5. Managed path 分类

### 5.1 Guru-owned rule

以下 path 规则分类为 `guru_owned`：

- installed `.trellis/guru-team/**`
- canonical `trellis/skills/guru-team/**`
- canonical package id `guru-*`
- installed `.agents/skills/guru-*/**`
- installed `.codex/skills/guru-*/**`
- installed `.cursor/skills/guru-*/**`
- installed `.claude/skills/guru-*/**`

Rule 必须在 JSON inventory 显式声明，validator 必须使用 anchored path matching，不能用任意 substring。

### 5.2 Legacy managed claim

`trellis/guru-team-extension.json.public_api.managed_paths` 中现存 upstream namespace claim 必须在 `managed_path_claims` 标为 `transitional_legacy`，并引用覆盖这些 claim 的 frozen entry。新增 upstream namespace claim 必须失败。

### 5.3 Upstream-owned path

当 frozen entry 在 #132 完成删除后，path category 转为 `upstream_owned`，该 path 必须从 overlay tree 和 legacy managed claims 消失。Validator 不负责执行删除。

## 6. Validator 算法

Validator 按固定顺序运行：

1. 解析 repo root、schema、inventory、extension manifest 与 skill registry。
2. 校验 schema 文件本身是合法 JSON Schema，并校验 inventory 的固定字段与类型。
3. 校验类别集合、path 唯一性、issue number、owner 字段与状态矩阵。
4. 扫描 overlay tree，比较 frozen path set、count、path-set digest、active/removed 状态。
5. 对每个 active entry 计算 SHA-256，并比较 baseline hash 与 aggregate hash。
6. 分类 extension manifest managed claims。
7. 从 installer `MANAGED_ASSET_PATHS` 的 Python AST 提取 `Path(...)` literal，映射到 `.trellis/guru-team/**` 后分类。
8. 校验 active skill id 全部使用 `guru-` prefix，并验证 canonical/installed discovery rule fixture。
9. 输出固定 JSON facts；存在任一错误时返回非零。

成功输出包含 `status=ok`、inventory/schema path、target Trellis CLI、frozen/active/removed count、overlay count、managed claim count、classified count、facts SHA-256。失败输出包含 `status=error`、稳定错误 code、path 和客观 detail。

## 7. Gate 接入

### 7.1 Preset source validation

`apply_guru_team_trellis_preset.py` 在 `repo_root_from_args()` 完成后、`install_assets()` 发生任何 mutation 前调用 validator library。失败时退出码非零，target repo 保持未修改。

`apply.sh` 保持 thin wrapper；Bash 不复制 validation contract。

### 7.2 Dogfood drift

`check-dogfood-overlay-drift.sh` 先执行 `check-upstream-ownership.sh --repo <source> --json`，再执行现有 missing/changed 比较。任一阶段失败均非零退出。

### 7.3 Throwaway

`verify-throwaway-install.sh` 在以下 checkpoint 调用 source validator：

- initial `trellis init` 后、首次 preset apply 前；
- `trellis update --force` 完成后、workflow/preset reapply 前；
- reapply 完成后、最终 dogfood/sidecar 检查前。

首次 apply 与 reapply 仍由 installer 内部 pre-mutation gate 再校验一次。重复调用用于证明各 checkpoint 实际执行 gate，不新增语义 owner。

## 8. Fixture 与测试设计

Fixture 使用 JSON mutation description，测试 helper 在临时 repo 中复制最小 ownership/schema/overlay/manifest/installer facts，再应用 mutation。Fixture 不存储 active task 或本机绝对路径。

Negative fixture 必须分别触发稳定 code：

- `overlay_not_in_frozen_baseline`
- `frozen_baseline_expanded`
- `active_payload_hash_mismatch`
- `missing_replacement_owner`
- `missing_removal_issue`
- `unclassified_path`
- `upstream_owned_managed_claim`

Preset installer 回归必须增加“validator 失败发生在 target mutation 前”的断言。

## 9. Docs SSOT Plan

- `docs_state`: `partial_docs`
- Evidence paths：`.trellis/spec/preset/index.md`、`.trellis/spec/preset/installer.md`、`.trellis/spec/preset/overlay-guidelines.md`、`README.md`、`trellis/presets/guru-team/README.md`、`trellis/workflows/guru-team/README.md`
- `strategy`: `ssot_first`
- 原因：现有文档描述 overlay replacement 和 drift，却没有 upstream ownership 分类、frozen migration inventory 或 no-new-patch gate。
- Durable docs changes：新增 `.trellis/spec/preset/upstream-ownership.md`，更新 preset index/installer/overlay specs 与三份 README。
- Task delta merge：本设计的分类、script boundary、gate checkpoint、update/upgrade 规则必须先进入 durable spec，再作为实现输入。
- Task-history-only：issue 调查时间线、临时 clean-init 命令输出和规划审查记录只保留在 task artifacts。
- Merge checkpoint：实现代理修改 validator 之前，durable spec 必须已写入工作树；Phase 2 final check 必须验证 spec、inventory、代码、测试与 README 一致。

Middle-platform Knowledge Gate：本任务只修改 Trellis extension/preset，不涉及 go-guru、proto-guru、Unity3D Guru SDK 或 Flutter Guru SDK，因此状态为 not applicable。

## 10. 兼容性与回滚

- 本 issue 不改变 target runtime payload；安装结果必须与 base commit 一致。
- 新 validator 是 source maintainer gate，不安装进业务 repo，也不进入 extension runtime command chain。
- 回滚本 issue 时删除新增 ownership 文件与 validator 接入，并恢复 README/spec；不得触碰 43 个 overlay payload。
- 任一实现 diff 命中 workflow、overlay payload、现有 public Skill package 或 platform trigger 时，Phase 2 必须阻塞并回到实现修订。
