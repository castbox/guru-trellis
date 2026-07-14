# #110 实现计划：`guru-sync-base`

## 1. Durable contract first

- [ ] 按 [design.md](./design.md) `Docs SSOT Plan` 更新 requirements、workflow specs、preset specs 与 docs specs。
- [ ] 固定 public id、schema id、runtime command、mode preconditions、typed exits 与 consumer，不在 runtime 代码中另建语义。
- [ ] 在 durable contracts 中明确 pre-task repo side-effect boundary 与 AI/script ownership。

## 2. Canonical package

- [ ] 在 `trellis/skills/guru-team/registry.json` 激活 `guru-sync-base`。
- [ ] 新增 `SKILL.md` 与 `references/contract.md`，保持 trigger/routing 与完整闭环责任分层。
- [ ] 新增 interface 1.1 instance，workflow/standalone preconditions 完全一致。
- [ ] 新增 `base-sync-result` schema、去身份化 example、两个 thin runtime wrappers 与 package contract tests。
- [ ] 固定 workflow resolution lease、standalone cleanup、terminal release owner 与 superseded/abort cleanup 合同；typed exit 不得留下无 owner 的临时 evidence。
- [ ] 断言 package 本身不是 self-contained，两个 wrapper 只经 `run-skill-command` 调用 declared runtime command。

## 3. Thin workflow route

- [ ] 在 canonical workflow 的 tool-free route 后添加一次 mandatory `guru-sync-base` invoke。
- [ ] 添加 `synced`、`skipped`、`blocked` 唯一 exit markers。
- [ ] 把 `check-env`、`prepare-task` 与语义读取放到 `synced` route 之后。
- [ ] `synced` consumer 把同一 resolution lease 传给 Phase 0 全部 `prepare-task` 调用；task created、blocked、aborted、superseded terminal route 必须调用 deterministic release，处于用户确认挂起状态时不得提前释放。
- [ ] 保留 `guru-discover-change-context` route id；不实现 #111 的 step-local package。
- [ ] 由 preset apply 同步 dogfood workflow 与平台入口，禁止手工维护重复步骤。

## 4. Shared deterministic runtime

- [ ] 实现 strict branch validator、四级 resolver、remote default probe、fallback cardinality gate 与 canonical resolution digest。
- [ ] 实现 resolve-only/execute 两阶段，executor 重算并绑定 AI 已确认的 resolution bytes/digest。
- [ ] 实现 clean checkout、missing ref、fetch、ancestor、ff-only、divergence 与三方 equality state machine。
- [ ] 实现 success result canonical JSON、SHA-256 与 repo-external evidence file boundary。
- [ ] 实现 read-only result validator与 stdout-only skipped recorder validator。
- [ ] 为现有 `sync-base` command 增加 additive `--release-resolution-evidence` executor mode，校验 external/component/symlink/digest identity 后删除并确认无残留；already-released 只返回结构化事实。
- [ ] 把 planner/executor freshness adapters 改为调用 shared core。
- [ ] 重排 `cmd_prepare`：初始 sync 在 issue/duplicate 读取前；executor sync 在 GitHub/worktree/task mutation 前。
- [ ] 保持 task-start context portable，不写完整 pre-task evidence 或本机 path。

## 5. Preset 与 extension distribution

- [ ] Extension bump 到 `0.6.5-guru.7`，更新 active skill、artifact schema 与 companion script public API。
- [ ] Installer 安装两个 runtime wrappers、canonical installed package 与 selected platform copies。
- [ ] 更新 installer assertions、managed inventory、executable modes 与 version matrix。
- [ ] 运行 canonical `apply.sh --repo . --all-platforms` 同步 dogfood，逐项处理 `.new`/`.bak`。

## 6. Test implementation

- [ ] 补齐 resolver/sync/validator/prepare ordering Python unit matrix。
- [ ] 补齐 package schema/interface/marker/runtime contract tests。
- [ ] 补齐 installer selected-platform、managed hash、drift、sidecar tests。
- [ ] 先扩展测试计划与 contract assertions，再实现 resolution lease/release 单元测试，覆盖 internal path、symlink、digest mismatch、double release、missing lease prepare 与 superseded cleanup。
- [ ] 扩展 throwaway installer：standalone sync、真实 `synced -> prepare-task` planner/mutation guard/release、update/reapply、zero-evidence-residue 与 zero-sidecar。
- [ ] 保持现有 `guru-create-task-commit` 与 full closeout suites 无回归。

## 7. Public docs 与 dogfood consistency

- [ ] 同步根 README、workflow README、preset README 的安装、调用、version、upgrade 与 failure remediation。
- [ ] 同步 canonical/dogfood workflow、canonical/installed/platform package、config template 与 dogfood config。
- [ ] 运行 source/installed skill validation 与 dogfood overlay drift gate。

## 8. Phase 2 verification

- [ ] `python3 -m unittest trellis.skills.guru-team.tests.test_skill_packages`
- [ ] `python3 trellis/skills/guru-team/packages/guru-sync-base/tests/test_contract.py`
- [ ] `python3 trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
- [ ] `python3 trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`
- [ ] `python3 -m json.tool` 校验 registry、interface、schema、extension 与 fixtures。
- [ ] `bash -n` 校验 canonical、preset 与 installed wrappers。
- [ ] `python3 -m py_compile` 校验 workflow companion 与 preset installer。
- [ ] `.trellis/guru-team/scripts/bash/check-skill-packages.sh --json --mode source`
- [ ] `.trellis/guru-team/scripts/bash/check-skill-packages.sh --json --mode installed`
- [ ] `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`
- [ ] `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`
- [ ] Throwaway 明确断言 Phase 0 终态不存在 resolution/result evidence，并证明 `prepare-task` 消费的是 Skill 交付的同一 raw-byte/digest lease。
- [ ] `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-14-110-guru-sync-base`
- [ ] `git diff --check`
- [ ] `git status --short --branch`

## 9. Review 与发布门禁

- [ ] 实现代理交付 handoff 后，由独立 Trellis check 代理覆盖需求、设计、代码、schema、tests、Docs SSOT、preset、dogfood、upgrade/update 与安全边界。
- [ ] F-006 planning revision 必须在实现派发前重新展示 `prd.md`、`design.md`、`implement.md`，取得新的 `explicit-post-planning-review` 确认并重录 schema 1.2 planning approval。
- [ ] 主会话更新 durable spec 判定与 issue scope ledger evidence。
- [ ] 使用 `guru-create-task-commit` 创建 exact task work commit。
- [ ] 独立 Branch Review 覆盖 `origin/main...HEAD` 全量 diff，任意 P0/P1/P2/P3 finding 均返回修复循环。
- [ ] Branch Review Gate 通过后执行 remote marketplace verification。
- [ ] `trellis-finish-work` 创建 draft PR、归档 task、验证 remote HEAD 后标记 ready；PR 只使用 `Closes #110`。

## 10. 回滚点

- Package/runtime 未接入 workflow 前：删除新 canonical package 与 runtime command，恢复 registry/extension。
- Workflow 已接入但 distribution 未完成：禁止 publish，回滚 workflow markers 后重新 apply preset。
- Dogfood 或 throwaway 出现 sidecar：停止，审查每个 `.new`/`.bak`，修复 canonical/managed hash 后重跑全套 gate。
- Prepare ordering 或 base sync 出现 destructive Git behavior：停止实现，不保留实验性 fallback，回到 strict blocked contract。
