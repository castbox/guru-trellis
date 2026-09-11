# 实施计划

## 1. 前置与边界

- [ ] 每次写入前从 #132 worktree 运行 workspace-boundary validator。
- [ ] 以 Issue #132 正文、`main@c8cdd9e7fbb73687cd700c1dbbb7a5907307476f`、PR #167、PR #168、Issue #161 状态和当前 official Trellis docs 为 authority。
- [ ] 不读取或修改 #161 指定 branch/worktree，不修改 Trellis upstream、全局 npm 或 `node_modules`。
- [ ] 若发现 #161 public contract 本身缺陷，停止对应实现并记录复现；只继续 #132-owned projection/installer/ownership 问题。
- [ ] 对当前 `prd.md`、`design.md`、`implement.md` 重跑 planning wording owner 与 Planning owner；只在 checked typed exit 为 `approved` 后继续候选实现审计。

## 2. Durable specs 先行

- [ ] 将 workflow specs 收敛为 global invocation/exit/consumer/fail-closed graph，删除 step-local semantic/runtime 复述。
- [ ] 将 ownership/overlay/installer specs 从 43 active legacy 更新为 43 removed tombstones、3 additive overlays 与 provenance migration state machine。
- [ ] 更新 public docs/README 的安装、update/upgrade、platform discovery、sidecar 与 remote verification说明。

Checkpoint：durable specs 经 diff review 后才修改 inventory、installer 和 canonical workflow。

## 3. Thin workflow 与 public graph

- [ ] 精简 `trellis/workflows/guru-team/workflow.md`，保留 13 mandatory Skill invokes、所有已声明 exits、唯一 consumers/targets 与 global-only rules。
- [ ] 同步 `.trellis/workflow.md`，验证 canonical/dogfood byte equality。
- [ ] 核对 `registry.json`、13 个 `interface.json`、consumer schemas 与 production migration manifests；只修改 #132 projection/consumer/marker 所需文件，不改 owner internal semantics。
- [ ] 增加 regression，拒绝 duplicate/unmapped/consumer-mismatched route、private artifact/runtime-source dependency 与 platform wrapper step-local duplication。

## 4. Ownership 与 overlay 物理迁移

- [ ] 更新 `upstream-ownership.json`：43 条全部改为 `upstream_owned/removed`，保留 frozen history，移除 current payload fields。
- [ ] 调整 schema/validator constants 与 fixtures，使历史 identity 固定、最终 active=0/removed=43。
- [ ] 删除 43 个 upstream overlay files，只保留三个 Guru-owned finish entry。
- [ ] 将 extension manifest managed paths 收敛为精确 Guru namespace；删除 7 个 transitional/broad claims。

## 5. Installer migration

- [ ] 在 installer 中加入 removed tombstone preflight 与 migration result fields。
- [ ] 读取 `.trellis/.template-hashes.json` 的官方 clean hash，区分 clean upstream、known legacy、missing、unknown local edit。
- [ ] 对 generated upstream old Guru payload fail closed 并给出 update/upgrade remediation；对 legacy-only exact payload 执行 reviewed cleanup；对未知编辑保留并生成 `.new`/conflict。
- [ ] 新 installed manifest 不再记录 upstream paths；reapply、platform shrink、known `.bak` recovery 与 staged activation继续保持原合同。
- [ ] 更新 installer/ownership unit fixtures覆盖初始安装、重复 apply、update 后 reapply、known legacy cleanup、unknown edit、invalid provenance 与递归 sidecar。

## 6. Dogfood 与平台投影

- [ ] 使用官方 Trellis update/upgrade 机制恢复 dogfood upstream-owned files，审查 `.template-hashes.json`、`.new/.bak` 与实际 diff。
- [ ] 运行新版 preset apply 同步 `.trellis/guru-team/**` 与 Shared/Codex/Claude/Cursor `guru-*` copies。
- [ ] 删除 dogfood 中不再属于 Guru ownership 的 patched upstream copies，但保留官方 upstream versions。
- [ ] 验证三个 Guru finish entries 与 canonical bytes一致、可执行位正确、无 overlay drift。

## 7. 验证命令

### 7.1 静态与 package graph

```bash
python3 .trellis/guru-team/scripts/python/guru_team_trellis.py check-skill-packages --json --mode source
python3 .trellis/guru-team/scripts/python/guru_team_trellis.py check-skill-packages --json --mode installed
trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
```

### 7.2 Unit/integration

```bash
python3 trellis/presets/guru-team/scripts/python/test_upstream_ownership.py
python3 trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py
python3 trellis/skills/guru-team/tests/test_skill_packages.py
python3 trellis/skills/guru-team/tests/test_finish_family_integration.py
python3 trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py
```

### 7.3 Dogfood apply 与 installed checks

```bash
trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms --json
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
```

逐项审查 apply result 中 installed/unchanged/removals/conflicts/sidecars、managed hashes、platforms 与 source/installed validation；任何 `.new/.bak` 未处理则阻塞。

### 7.4 Clean throwaway combined acceptance

- [ ] 使用 README 中声明的命令执行 marketplace index、clean init、workflow preview/switch。
- [ ] 验证 preset initial apply/reapply。
- [ ] 实际发现 Shared/Codex/Claude/Cursor 的全部 active `guru-*` contracts。
- [ ] 执行 `trellis update` 与目标版本升级，再次 workflow select + preset reapply。
- [ ] 验证 upstream template hashes、Guru managed hashes、legacy cleanup、可执行位与递归零 sidecar。
- [ ] 在 update/reapply 前后运行完整 source/installed/public graph suites。

### 7.5 Remote branch gate

Remote verification 只在 reviewed content push 后由 finalizer/`guru-verify-extension-installation` 执行；不得用本地 throwaway 或 package eval 冒充 pushed-ref evidence。

## 8. Phase 2 与 review

- [ ] 使用 Trellis implement/check sub-agents执行分区实现与独立检查；main session 负责 scope、spec、整合与门禁。
- [ ] `guru-check-task` 对完整 current task scope 作一次 AI-owned semantic judgment，并只返回其最小 typed exit。
- [ ] 所有 finding 成批修复后重新跑受影响验证。
- [ ] Commit 前完成 Docs SSOT reconciliation：任务设计已合并到 durable specs，task artifact 只保留历史与执行证据。
- [ ] `guru-create-task-commit`、`guru-review-branch`、`guru-review-task-publication` 与 finalizer 均使用各自 public contracts；不直接调用兼容脚本绕过 owner。

## 9. 停止条件

- #161 public contract 缺陷；
- ownership migration 需要新的 replacement owner 或超出 #132 的 semantic route；
- unknown local edit 无法安全保留；
- official Trellis update/upgrade 无法恢复 upstream ownership；
- remote/publication/closure authority 变化；
- 任何 mandatory Skill missing、unknown/multiple/unmapped exit 或 consumer mismatch。
