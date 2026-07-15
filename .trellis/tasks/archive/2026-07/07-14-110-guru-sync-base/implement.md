# #110 实现计划：`guru-sync-base`

## 1. 修正范围与 durable contract

- [ ] 以 live issue #110 与 [GitHub correction comment](https://github.com/castbox/guru-trellis/issues/110#issuecomment-4976030247) 为需求 SSOT，删除 task/durable docs/code/tests 中自行增加的 repo-external evidence lifecycle、resolution lease、release executor、quarantine、replacement cleanup 与 terminal zero-residue 合同。
- [ ] 根据用户确认的 scope correction 保留 #110 前 `prepare-task` 的 base 候选顺序：`dev -> develop -> main -> master`；GitHub correction comment 与三份 planning artifacts 共同覆盖 live issue Base resolution 小节的旧顺序。
- [ ] 根据 [deterministic Skill scope comment](https://github.com/castbox/guru-trellis/issues/110#issuecomment-4976105007) 将完全机器可验证 Skill 的例外纳入当前 task；修改 `AGENTS.md` 与 durable workflow/spec/docs，明确 semantic/deterministic 双 profile 和禁止降级条件。
- [ ] 按 [design.md](./design.md) `Docs SSOT Plan` 更新 requirements、workflow specs、preset specs 与 docs specs。
- [ ] 固定 public skill id、base result schema id、runtime command、mode preconditions、typed exits 与 consumer；interface schema 按显式 `1.2` 迁移合同升级，不在 runtime 代码中另建语义。
- [ ] 在 durable contracts 中明确 pre-task repo side-effect boundary 与 AI/script ownership。

## 2. Closed-loop interface schema `1.2`

- [ ] 将 `trellis/skills/guru-team/schemas/skill-interface.schema.json` 从 `1.1` 升级到 `1.2`，新增必填 `judgment_mode`，条件约束 semantic 五阶段与 deterministic 三阶段的 exact `ordered_stages`。
- [ ] 修改 canonical 与 installed validator 常量和 exact-field/stage 校验，拒绝旧 `1.1`、缺失/未知 `judgment_mode` 及 profile/stage mismatch。
- [ ] 将 `guru-sync-base/interface.json` 声明为 deterministic；将 `guru-create-task-commit/interface.json` 显式迁移为 semantic，保持后者行为、exit 与 runtime command 不变。
- [ ] 同步 representative fixtures、registry/package/preset tests 与 schema migration 文档；稳定 skill id、external exit id 和 runtime command 不改名。

## 3. Canonical package

- [ ] 在 `trellis/skills/guru-team/registry.json` 激活 `guru-sync-base`。
- [ ] 提供 `SKILL.md` 与 `references/contract.md`，保持 trigger/routing 与完整闭环责任分层。
- [ ] 提供 `judgment_mode=deterministic` interface；删除 Skill 内的 `invocation_intent` 语义判断，改为接收 caller 已路由的 normalized `invocation_mode` 与 route id；workflow/standalone Git preconditions 完全一致，stage 顺序固定为 `forward_behavior -> recorder_validator -> typed_exit`。
- [ ] 提供 `base-sync-result` schema、去身份化 example、两个 thin runtime wrappers 与 package contract tests。
- [ ] 断言 package 本身不是 self-contained，两个 wrapper 只经 `run-skill-command` 调用 declared runtime command。

## 4. Thin workflow route

- [ ] 在 canonical workflow 的 tool-free route 后添加一次 mandatory `guru-sync-base` invoke。
- [ ] 添加 `synced`、`skipped`、`blocked` 唯一 exit markers。
- [ ] 把 `check-env`、`prepare-task` 与语义读取放到 `synced` route 之后。
- [ ] 保留 `guru-discover-change-context` route id；不实现 #111 的 step-local package。
- [ ] Workflow 不复制 Skill 内部步骤，也不承载 `trellis-implement` / `trellis-check` sub-agent 的内部行为。
- [ ] Workflow 的 AI tool-free route classification 保留在 Skill 调用前；Skill 内删除 selected-base AI confirmation、post-execution AI Review Gate 与 conditional human confirmation。
- [ ] 由 preset apply 同步 dogfood workflow 与平台入口，禁止手工维护重复步骤。

## 5. Shared deterministic runtime

- [ ] 实现 strict branch validator、四级 lazy resolver、有序 candidate-first selection、remote default final fallback 与 canonical resolution digest；`source` 只能为 `explicit`、`config`、`config-candidate`、`remote-default`。
- [ ] 实现 stdout-only resolve facts 与 pre-sync digest-bound execute；executor 直接重算 resolver facts，不要求 AI 确认 selected base。
- [ ] Execute 成功后生成绑定同步后 decision checkout 的 `post_sync_resolution_sha256`；validator 同时校验 pre-sync 与 post-sync identity，typed exit 只向下一 consumer 传递 post-sync digest。
- [ ] 实现 clean checkout、missing ref、fetch、ancestor、ff-only、divergence 与三方 equality state machine。
- [ ] 实现 success result canonical JSON 与 SHA-256 stdout facts。
- [ ] 实现 read-only live Git validator与 stdout-only skipped recorder validator；不引入 result evidence file cleanup。
- [ ] 把 planner/executor freshness adapters 改为调用 shared core；每个 guard 消费上一 guard 的 post-sync digest并输出下一 post-sync digest，不跨 fast-forward 复用同步前 digest。
- [ ] 重排 `cmd_prepare`：initial sync 在 issue/duplicate 读取前；executor sync 在 GitHub/worktree/task mutation 前。
- [ ] 保持 task-start context portable，不写完整 pre-task result 或本机 path。

## 6. Preset 与 extension distribution

- [ ] Extension bump 到 `0.6.5-guru.7`，更新 active skill、artifact schema 与 companion script public API。
- [ ] Installer 安装两个 runtime wrappers、canonical installed package 与 selected platform copies。
- [ ] 更新 installer assertions、managed inventory、executable modes 与 version matrix。
- [ ] 运行 canonical preset apply 同步 dogfood，逐项处理 `.new`/`.bak`。

## 7. Test implementation

- [ ] 删除只验证 evidence file、lease、release、quarantine、replacement cleanup 与 zero-residue 的超范围测试。
- [ ] 补齐 resolver/sync/validator/prepare ordering Python unit matrix；必须包含 `dev + main -> dev`、`develop + main -> develop`、`main + master -> main`、自定义候选顺序、候选全空时 remote default、全部来源失败 `blocked` 与 rolling post-sync digest。
- [ ] 新增真实 Git `behind -> resolve -> execute ff-only -> validate -> prepare` 集成回归；断言 prepare 使用新 post-sync digest，pre-sync digest 不可跨 fast-forward 复用，config/branch/dirty/digest drift 均在对应 fetch/mutation 前阻塞。
- [ ] 补齐 package schema/interface/marker/runtime contract tests，包括 schema `1.2` 双 profile正向测试、缺失/未知 mode、错误 stage profile、active interface migration 与旧 `1.1` fail-closed 测试。
- [ ] 补齐 installer selected-platform、managed hash、drift、sidecar tests。
- [ ] 扩展 throwaway installer：behind-base `resolve -> execute ff-only -> validate -> prepare`、already-equal sync、update/reapply 与 zero-sidecar。
- [ ] 保持现有 `guru-create-task-commit` 与 full closeout suites 无回归。

## 8. Public docs 与 dogfood consistency

- [ ] 同步 `AGENTS.md`、requirements、workflow/spec、根 README、workflow README、preset README 的 deterministic 例外、semantic 保留边界、安装、调用、version、upgrade 与 failure remediation。
- [ ] 同步 canonical/dogfood workflow、canonical/installed/platform package、config template 与 dogfood config。
- [ ] 运行 source/installed skill validation 与 dogfood overlay drift gate。

## 9. Phase 2 verification

- [ ] 运行 canonical runtime、skill registry、package 与 preset installer 全量测试，并分别报告实际计数；focused subset 不重复计数。
- [ ] 校验 registry、interface、schema、extension 与 fixtures JSON。
- [ ] 校验所有 active Skill 的 `judgment_mode` 与 exact stage profile，并确认 `guru-create-task-commit`、Phase 2 check、Branch Review 和 PR readiness 的 semantic AI Gate 合同未被放宽。
- [ ] 校验 canonical、preset 与 installed wrappers Bash 语法。
- [ ] 校验 workflow companion 与 preset installer Python compile。
- [ ] 运行 source/installed skill validation 与 dogfood overlay drift gate。
- [ ] 运行 clean throwaway marketplace init/preview/switch、preset apply、behind-base `resolve -> execute ff-only -> validate -> prepare`、already-equal workflow、`trellis update`、workflow/preset reapply 与 zero-sidecar。
- [ ] 运行 task validate、`git diff --check` 与 `git status --short --branch`。

## 10. Review 与发布门禁

- [ ] 修订后的 planning artifacts 通过歧义审查并向用户展示；用户明确确认后重新记录 schema 1.2 planning approval，之后才能派发实现。
- [ ] 实现代理交付 handoff 后，由独立 `trellis-check` sub-agent 覆盖需求、设计、代码、schema、tests、Docs SSOT、preset、dogfood、upgrade/update 与安全边界。
- [ ] 主会话更新 durable spec 判定与 issue scope ledger evidence。
- [ ] 使用 `guru-create-task-commit` 创建 exact task work commit。
- [ ] 独立 Branch Review 覆盖 `origin/main...HEAD` 全量 diff，任意 P0/P1/P2/P3 finding 均返回修复循环。
- [ ] Branch Review Gate 通过后执行 remote marketplace verification。
- [ ] `trellis-finish-work` 创建 draft PR、归档 task、验证 remote HEAD 后标记 ready；PR 只使用 `Closes #110`。

## 11. 回滚点

- Scope correction 未经用户确认：停止实现，不修改 durable docs、runtime、package、preset 或 workflow。
- Interface schema `1.2` 未能同批迁移全部 active interfaces、source/installed validators 与 fixtures：停止实现；validator 必须拒绝通过兼容 fallback 静默接受缺失 `judgment_mode`。
- Package/runtime 未接入 workflow 前：删除新 canonical package 与 runtime command，恢复 registry/extension。
- Workflow 已接入但 distribution 未完成：禁止 publish，回滚 workflow markers 后重新 apply preset。
- Dogfood 或 throwaway 出现 sidecar：停止，审查每个 `.new`/`.bak`，修复 canonical/managed hash 后重跑全套 gate。
- Prepare ordering 或 base sync 出现 destructive Git behavior：停止实现，不保留未经确认的候选或 current-branch fallback，回到经用户确认的 ordered-candidate 与 strict blocked contract。
- Pre-sync digest 被跨 fast-forward 继续用于 prepare，或任一 guard 未把 post-sync digest交给下一边界：停止实现，修复 identity generation 与真实链路回归后重跑 Phase 2。
