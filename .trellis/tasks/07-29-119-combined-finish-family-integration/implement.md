# #119 实现计划

## 1. 实施前门禁

- [ ] 重新运行 workspace boundary，确认只在
      `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/119-combined-finish-family-integration`
      写入。
- [ ] `guru-review-contract-wording:planning_artifacts` 对当前三份规划文件返回 `pass`。
- [ ] `guru-approve-task-plan` 的 adequacy/provenance/unusual-scenario review 无 findings。
- [ ] 展示 `prd.md`、`design.md`、`implement.md` 后获得明确 post-planning approval。
- [ ] 只有 `guru-approve-task-plan:approved` 后才运行 `task.py start`；实现仍需用户单独授权。

## 2. 实现顺序

### 2.1 先更新 durable contract

- [ ] 更新 `.trellis/spec/workflow/workflow-contract.md`：canonical `guru-finish-work`、
      explicit entry boundary、13-exit combined route、legacy compatibility 到 #132。
- [ ] 更新 `.trellis/spec/workflow/companion-scripts.md`：direct helper fail-closed guidance
      指向 Guru entry，internal private marker 保留。
- [ ] 更新 `.trellis/spec/preset/overlay-guidelines.md`：frozen legacy 与 additive Guru entry
      的 ownership/installer/update contract。
- [ ] 更新 `docs/requirements/requirement-main.md`：#119 combined acceptance current、
      #119/#115 close、#132 follow-up、平台矩阵。

### 2.2 薄化 canonical workflow

- [ ] 收敛 `trellis/workflows/guru-team/workflow.md` 的通用 finish 说明、Phase 3.6/3.7 和
      completed breadcrumb，只保留全局 ownership/markers/entry evidence/fail-closed route。
- [ ] 保持 13 个 Finish exits 的 id、consumer 与 marker cardinality 不变；不修改三个
      package/interface/schema/contract。
- [ ] 运行 workflow/source validator，再通过 preset apply 同步 `.trellis/workflow.md`。

### 2.3 新增 Guru namespace entries

- [ ] 新增 Codex `guru-finish-work` prompt、Claude `/guru:finish-work` command、Cursor
      `/guru-finish-work` command canonical overlays。
- [ ] Entry 只读 live workflow、mandatory load 三个 Skill、消费 mapped exits 和输出 terminal
      result；不包含 script flags、artifact schema、transaction algorithm 或 routine handoff。
- [ ] 同步对应 dogfood copies；不新增 `.agents/skills/guru-finish-work` wrapper package。

### 2.4 扩展 additive ownership 与 installer acceptance

- [ ] 在 `trellis/presets/guru-team/ownership/upstream-ownership.json` 增加三个窄
      Guru-owned rule/claim，保留 43 条 `legacy_entries` 和 frozen digests 原值。
- [ ] 在 `trellis/guru-team-extension.json` 增加对应 managed paths。
- [ ] 修改 `validate_upstream_ownership.py`，把 frozen legacy paths 与 declared additive
      Guru overlays 分别验证；未知额外 overlay 继续 fail closed。
- [ ] 更新 `test_upstream_ownership.py` 和 preset installer tests，覆盖 initial install、
      selected platform、known current、unknown local edit `.new`、update/reapply、未选平台不恢复。
- [ ] `apply.sh --repo .` 后逐个处理 `.new`/`.bak`，运行 dogfood drift。

### 2.5 迁移 canonical guidance 与 compatibility inventory

- [ ] 更新 canonical
      `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py` 中 direct
      `finish-work` / `publish-pr` blocker 的 `required_entrypoint` 为 `guru-finish-work`，
      不改 #105 transition semantics 或 private flag；preset apply 同步对应
      `.trellis/guru-team/scripts/python/guru_team_trellis.py` dogfood copy。
- [ ] 更新 README 三份和第 2.1 节列出的 durable contract；旧 `trellis-finish-work` 只在明确的
      compatibility/frozen inventory 中出现。
- [ ] 重构 `FinishWorkEntrypointContractTest` 及 inventory 识别出的仅绑定 legacy 主入口断言：新 Guru entry
      是 canonical，legacy bytes/hash/compat route 单独验收。
- [ ] 记录 retained/removed inventory；删除已被 owner contract 替代的重复正文和 dead tests，
      保留所有有生产 consumer 的 helper。

### 2.6 Cross-skill combined tests

- [ ] 增加 focused Finish-family integration test/fixture，复用三个 package 的 public
      wrapper、schema/example、consumer projection 和 authoring example。
- [ ] 覆盖 normal non-extension、extension、return-to-task-work、publication stale、same-plan
      resume、cross-month reprepare、published recovery、blocked 八类 transcript。
- [ ] 断言 13 exits closure、六条关键 edges、unique consumer、seed/authoring partition、
      no-overwrite merge、target schema、consumer direct use、private field absence。
- [ ] 在 Shared/Codex/Claude/Cursor 运行 byte-identical Finish corpora/combined routes；
      `expected_exit` 只在 wrapper 返回后断言。
- [ ] Transcript 只保存在 temp run root，不新增 task/public DTO 字段或长期 artifact。

### 2.7 Throwaway 与 upgrade/update/reapply

- [ ] 扩展 `verify-throwaway-install.sh`：fresh install 后断言 Guru entries、三 Finish packages、
      combined routes、legacy compatibility inventory 和 zero sidecars。
- [ ] 执行 workflow preview/switch、`trellis update --force`、workflow reselect、preset
      reapply；再次断言 entry bytes/modes、managed inventory、source/installed validation、
      combined routes、`.new`/`.bak` 和 workspace/developer identity preservation。
- [ ] `verify_installed_closeout.py` 在 initial 与 after-update 两次完整执行
      dry-run/formal/Draft PR/archive/ready/exact recovery；入口断言使用 canonical Guru name。
- [ ] README 安装命令从无本机隐藏状态的 throwaway 中实际执行。

### 2.8 Docs SSOT reconciliation

- [ ] 更新 README、workflow README、preset README 的 canonical entry、兼容边界、验证命令。
- [ ] 确认 task-only audit/evidence 没有复制进 durable docs；长期 contract 已回写。
- [ ] 运行 docs/reference scanner，确认非 compatibility context 不再把 legacy name 当主入口。

## 3. 验证命令

以下命令在实现后按风险由窄到宽执行；实际 flag 以当前脚本 `--help` 为准：

```bash
# Boundary and canonical/installed ownership
trellis/workflows/guru-team/scripts/bash/check-workspace-boundary.sh \
  --json --root . --task .trellis/tasks/07-29-119-combined-finish-family-integration
trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh

# Focused installer/ownership/integration tests
python3 trellis/presets/guru-team/scripts/python/test_upstream_ownership.py
python3 trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py
python3 trellis/skills/guru-team/tests/test_skill_packages.py

# Complete #105 transaction/failure/recovery regression
python3 trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py

# Source/installed public Skill contracts
.trellis/guru-team/scripts/bash/check-skill-packages.sh \
  --root . --json --mode source

# Canonical -> dogfood sync and drift
trellis/presets/guru-team/scripts/bash/apply.sh \
  --repo . --platform claude --platform codex --platform cursor
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh

# Clean install, workflow preview/switch, update, reapply, installed closeout
trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh
```

四 adapter Finish eval/combined 命令由 focused integration test 和 throwaway verifier 调用
installed `run-skill-evals.sh`，并为 `shared`、`codex`、`claude`、`cursor` 使用同一 corpus。

## 4. 每步回滚点

- Durable docs + workflow 作为一组；marker validation 失败时回滚该组未提交修改。
- Guru entries + ownership/manifest/installer tests 作为一组；frozen legacy files 永不改写。
- Combined test 只新增 test-owned fixture/runner；若设计不满足 public-only，删除该方案并
  改用已有 public eval runner 组合，不能放宽 private boundary。
- Helper guidance 的合法变化严格限定为文案/API guidance；#105 regression 任一失败即撤销影响 engine 的
  修改并重新设计。
- Throwaway 产生的 repo/remote 仅在临时目录；测试结束清理，不触碰真实 GitHub repo。

## 5. Review Gates

- Phase 2 `guru-check-task` 必须覆盖完整 task scope、Docs SSOT、13 exits、combined routes、
  #105 full module、throwaway/update/reapply 和 platform parity。
- Branch Review 覆盖 `origin/main...HEAD` 全 diff，确认三个 Skill 无职责重叠、workflow 不复制
  owner internals、public DTO 最小、scripts 只做 deterministic role、legacy retained/removal
  inventory 正确、#132 未提前实现。
- Publication readiness 只将 #119/#115 放入 close scope；#105/#116/#117/#118 只 related，
  #132 只 follow-up。

## 6. 明确不执行

- 不修改三个 Finish Skill 的 internal semantic behavior、public schema 或 private artifact。
- 不迁移 PR #160 task artifacts。
- 不实现 #132 的全仓 overlay removal。
- 不增加 malicious/forgery/race/lock/TOCTOU/extra fault/cross-OS crash tests。
- 未获得后续授权前，不运行 `task.py start`、不实现、不 stage/commit/push/PR/merge/close/cleanup。
