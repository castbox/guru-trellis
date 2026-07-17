# #114 实施计划：重实现 wording Skill 并删除 #93 旧 owner

## 前置状态

- [x] 已读取 live issue #114、dependency #109、#93 archived task、当前 runtime/workflow/docs/spec/package installer。
- [x] 已确认需求清楚，未发现必须向用户补问的产品语义。
- [x] 已确定 replacement-first 策略与 planning approval consumer 保留边界。
- [ ] 完成 planning wording review，展示三份文档并取得 fresh post-planning approval。
- [ ] 记录/check planning approval 后运行 `task.py start`。

## 实施步骤

### 1. 建立 canonical package 与公共接口

- 新增 `guru-review-contract-wording` package 的 `SKILL.md`、`interface.json`、contract、schema、example、wrappers、tests。
- 在 `trellis/skills/guru-team/registry.json` 注册 active id 与 workflow route。
- 在 skill package durable spec 中记录 schema id、三个 profile、三个 exits 和 migration boundary。
- 先运行 source package/schema validation，不触碰旧 scanner 删除。

完成条件：source registry/interface/package tests 通过，semantic stage profile 与 workflow/standalone preconditions 被机器校验。

### 2. 实现 generic scope/scanner/evidence runtime

- 在 canonical runtime 增加 `change_request`、`planning_artifacts`、`explicit_paths` scope builders。
- 增加共享 vocabulary/classification version constants 和 generic hit identity/scanner。
- 增加 result builder、schema validation、digest、unchecked、freshness 与 Gate/exit invariant checker。
- 增加 `record-contract-wording-review`、`check-contract-wording-review` CLI 和 extension dispatcher capability。
- 同步 canonical wrapper、installed script inventory、config/manifest/public API 测试。

完成条件：三个 profile 的 positive/fail-closed tests、content-change rescan、stale/hash mismatch、classification matrix 与 typed-exit tests 通过。

### 3. 接入 global workflow 与 profile router

- 在 Phase 0 clarification `clear` 后 mandatory invoke `guru-review-contract-wording`。
- 在 planning artifact presentation 前 mandatory invoke同一 Skill 的 `planning_artifacts` profile。
- 声明 `pass`、`content_changed`、`blocked` 的唯一 consumer markers 与 workflow/stop targets。
- 实现只按已验证 profile 路由的固定 matrix；unknown/multiple/unmapped fail closed。
- Standalone discovery 只提供 direct invocation，不复制内部步骤。

完成条件：workflow package validation 和 route marker tests 证明每个 exit 只有一个 consumer，所有 profile 均有固定 route。

### 4. 迁移 planning approval consumer

- `planning_artifacts` pass 写 current task-local `contract-wording-review.json`。
- `record-planning-approval` 改为接收并验证该 evidence locator，保留 post-planning user confirmation、reviewer/summary/checked dimensions 和三文档 digest。
- 从新 evidence 生成现有审计字段的 deterministic compatibility projection，并绑定 evidence/schema/scope/scan digests。
- `check-planning-approval` 先执行 generic wording checker，再核对 projection 与 planning doc/current approval facts。
- 更新 active legacy approval 的 re-review migration error；不改 archive。
- 更新 active-task clarification、Phase 2、task commit、Branch Review 对 shared planning validator 的回归测试。

完成条件：#93 compatibility test matrix 全部通过；missing/stale/non-pass/unchecked/violation evidence 均阻塞。

### 5. 更新 durable Docs SSOT

- 先更新 canonical package contract、workflow、requirements、workflow/preset README 和 workflow/data/script/quality/overlay specs。
- 各 consumer 只保留 Skill id、profile、evidence schema/version、exit、route 与自己的 obligation。
- 记录旧 `--normative-hit` 到新 wording evidence locator 的 migration。
- 同步 dogfood `.trellis/workflow.md`。

完成条件：Docs SSOT 与新 package/interface/runtime 一致，active docs 不再拥有完整词表、分类和内部 loop 副本。

### 6. Replacement verification 后删除旧实现

- 在步骤 1-5 targeted tests 通过后，删除 `PLANNING_AMBIGUITY_*` planning owner constants。
- 删除 planning 专用 scope/scanner/parse/payload/error helpers 与 `--normative-hit` active parser/usage。
- 删除 workflow/README/spec/platform 中完整规则副本，改为 stable Skill 引用。
- Repo-wide 搜索旧 symbols、旧 flag 和完整规则段；区分 archive/task history 与 active source。
- 若删除导致新链路测试失败，返回修订，不保留双 active owner 作为最终状态。

完成条件：active source 无旧 owner，archive 未改，generic Skill 与 planning consumer tests 仍全部通过。

### 7. Preset、dogfood 与平台同步

- 更新 preset installer/extension manifest/runtime command/schema/package inventories。
- 运行 preset apply 安装到 dogfood shared/Codex/Cursor/Claude roots。
- 运行 dogfood overlay/package drift checks，逐个处理 `.new`/`.bak`。
- 检查生成副本只作为 discovery/installed copy，不成为新的 semantic SSOT。

完成条件：canonical、installed runtime、四平台 copies、manifest managed hashes 一致。

### 8. Throwaway 与 update/reapply 验证

- 创建干净临时 Git repo，按 README 官方命令安装 `guru-team` workflow marketplace 和 preset。
- 运行 installed `check-skill-packages --mode installed`、三个 profile smoke、planning compatibility smoke。
- 执行目标 Trellis 版本 `trellis update`，重新应用 preset。
- 再次校验 workflow markers、package inventory、runtime commands、platform copies、evidence schema/checker。
- 记录 Trellis version、命令、变更文件、`.new`/`.bak` 和结果。

完成条件：新安装与 update/reapply 后均可用；无法执行的外部步骤必须在 Phase 2/PR/final 报告中明确列为未验证风险，不能声称开箱即用 passed。

### 9. Phase 2、提交与 Branch Review

- Dispatch Trellis implement agent 执行上述步骤并提交 implementation handoff。
- Dispatch Trellis check agent 对 task scope、Docs SSOT、code/schema/config/script/preset/overlay/test 做完整 Phase 2 review；机械修复后重跑。
- 记录/check `phase2-check.json`。
- 调用 mandatory `guru-create-task-commit` 只 stage 本 task 文件。
- Commit 后 dispatch independent Branch Review agent 覆盖 `origin/main...HEAD` 完整 diff；finding 修复必须返回 implementation + full Phase 2。
- 记录中文 raw reviews、rollup `review.md` 和 Branch Review Gate，然后停在 `trellis-finish-work` 前。

## 预计变更范围

### Canonical/public sources

- `trellis/skills/guru-team/registry.json`
- `trellis/skills/guru-team/packages/guru-review-contract-wording/**`
- `trellis/skills/guru-team/schemas/**`（仅当 package/interface registry schema 需要承接新 public id）
- `trellis/workflows/guru-team/workflow.md`
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
- `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
- `trellis/workflows/guru-team/scripts/bash/**` 中新增 dispatcher 或 planning adapter wrapper
- `trellis/workflows/guru-team/schemas/**`、config/extension public API 定义（按现有 inventory 所需）
- `trellis/presets/guru-team/scripts/**` 及 installer tests

### Durable docs/spec

- `docs/requirements/requirement-main.md`
- `docs/requirements/guru-team-trellis-flow.md`
- `trellis/workflows/guru-team/README.md`
- `trellis/presets/guru-team/README.md`
- `.trellis/spec/workflow/skill-package-contract.md`
- `.trellis/spec/workflow/workflow-contract.md`
- `.trellis/spec/workflow/data-contracts.md`
- `.trellis/spec/workflow/companion-scripts.md`
- `.trellis/spec/workflow/quality-guidelines.md`
- `.trellis/spec/preset/overlay-guidelines.md`

### Generated installed copies

- `.trellis/guru-team/**`
- `.agents/skills/guru-review-contract-wording/**`
- `.codex/skills/guru-review-contract-wording/**`
- `.cursor/skills/guru-review-contract-wording/**`
- `.claude/skills/guru-review-contract-wording/**`
- 由 preset apply 按 manifest 管理的 workflow/platform copies

## 验证命令计划

具体测试 module 名以实现后的文件为准，最低执行集：

```bash
python3 trellis/workflows/guru-team/scripts/python/guru_team_trellis.py check-skill-packages --json --mode source --root .
python3 -m unittest trellis/skills/guru-team/packages/guru-review-contract-wording/tests/test_contract.py
python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py
python3 -m unittest trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py
python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py .trellis/guru-team/scripts/python/guru_team_trellis.py
bash -n trellis/workflows/guru-team/scripts/bash/*.sh .trellis/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh
python3 -m json.tool trellis/skills/guru-team/registry.json
python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-17-114-contract-wording-review
trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
.trellis/guru-team/scripts/bash/check-skill-packages.sh --json --mode installed
git diff --check
```

Legacy deletion search 固定执行：

```bash
rg -n 'PLANNING_AMBIGUITY_|scan_planning_normative_language|parse_planning_normative_hit|--normative-hit' \
  trellis .trellis/workflow.md .agents .codex .cursor .claude docs
```

命中 archive/task history 时保留并在 evidence 中标为 non-active；命中 active runtime/workflow/docs/platform source 时 gate 失败。

## 测试矩阵

| 场景 | 期望 |
| --- | --- |
| `change_request` 缺 title/body | `blocked`，scope builder fail closed |
| `change_request` authoritative comment 更新 | 旧 evidence stale，refresh/re-entry |
| `planning_artifacts` caller 只传一份文档 | 拒绝 selector，仍固定三文件 |
| `explicit_paths` absolute/traversal/non-md/symlink | `blocked` |
| Vocabulary v2 每个 term | 产生完整 objective hit |
| 九类 retained classification + reason | whitelist 校验通过，其中 violation 仍 unchecked |
| 未分类/未知分类/空 reason | `blocked` |
| AI rewrite 后未重扫 | checker stale/block |
| Rewrite 改变未确认产品语义 | AI Review Gate blocked |
| Zero hits 但 semantic review 缺失 | 不能 `pass` |
| `planning_artifacts:pass` + fresh post-planning confirmation | planning approval record/check passed |
| Missing/stale/non-pass wording evidence | planning approval blocked |
| Pre-#114 active approval | 返回 fresh re-review/migration requirement |
| Archived #93 artifact | 不改写 |
| Unknown/multiple/unmapped exit/profile | fail closed |
| Preset fresh install/update/reapply | package/routes/commands/schema/platform copies current |

## Review Gate 范围

Branch Review 必须覆盖：

- `origin/main...HEAD` 完整 committed diff；
- issue #114 每条 acceptance 与本 task 三份 planning docs；
- semantic Skill 与 deterministic script boundary；
- profile scope 不可缩小、hash/rescan、evidence schema 与 typed exits；
- #93 planning compatibility 与 active legacy migration；
- 新实现通过后旧 owner 真正删除，active source 无双路；
- canonical/installed/platform/dogfood/throwaway/update-reapply 证据；
- Docs SSOT reconciliation；
- secret/redaction 与部署影响结论。

## 回滚点

- Commit 前：保留同一 task worktree 中的 diff，修订新链路直到 replacement tests 通过；不通过时不执行旧 owner 删除。
- Commit 后：以 PR revert 恢复 pre-#114 implementation。由于最终提交不保留双 active owner，禁止用 runtime feature flag 在新旧 scanner 间切换。
