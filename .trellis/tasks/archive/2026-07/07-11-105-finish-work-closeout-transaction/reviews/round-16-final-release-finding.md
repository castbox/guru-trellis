# Issue #105 Branch Review Round 16 最终放行审查报告

## 审查身份

- 逻辑角色：最终放行审查代理
- technical agent：`/root/final_release_review_105_round16`
- 独立性：未参与实现、Phase 2 或 Round 1-15
- reviewed_head：`94d44d7d116c22824cf629cef9f4a4cea4a98c52`
- diff_range：`origin/main...HEAD`
- base：`main@3dec302206783fe4ac1296066e9a1789c995d58b`
- reuse_decision：`new-agent`
- findings_count：`2`
- 结论：`fail`

## 审查范围

已只读审核：

- live GitHub Issue #105 及完整需求正文
- `prd.md`、`design.md`、`implement.md`、`planning-approval.json`
- `phase2-check.json`、`issue-scope-ledger.json`、`agent-assignment.json`
- Round 1-15 全部原始报告
- `origin/main...94d44d7` 的完整 50 文件 diff
- 11 个分支提交的实际 commit object
- closeout plan/schema、dry-run/formal digest、remote identity、marketplace evidence、draft PR、final projection、archive transaction、恢复状态机
- direct/archive two-stage symlink resolver、ordinary priority、plan-only fallback 与 committed recovery
- canonical/dogfood workflow、spec、README、preset、overlay、平台入口、manifest 和 installed smoke helper
- 官方 Trellis custom workflow 与 marketplace 文档
- 安全、部署及发布边界

全程未修改文件，未运行 Guru Team recorder/gate validator，未 commit、push 或创建 PR。

## 问题生命周期

Round 1-15 已记录问题的实现闭环未发现代码级回退：

- Round 1 四项 P1 在 Round 2 closed。
- Round 3/4 的 head repository、local transport、raw/effective remote identity 在 Round 5 closed。
- Round 6 的 all-platform provenance、raw task-local body、installed closeout 在 Round 7 closed。
- Round 7 ledger evidence 在 Round 8 closed。
- Round 9 的 post-archive artifact validator P1 经 Round 10-12 修复并 closed。
- raw locator、candidate priority、matching/unmatched alias 等 P2 经 Round 12-15 closed。
- 最新 direct/archive helper 与 ordinary resolver 的 `is_dir + task.json.is_file` predicate 一致；matching alias fail closed，unmatched alias 继续后续真实候选。
- committed fast-path、strict incomplete recovery、plan-only boundary、remote-only ready 未见回退。

Round 16 新发现以下两项当前范围 P1。

## 最终审查

### P1-1：11 个工作提交全部缺少强制 commit body，Branch Review 客观门禁必定失败

证据：

- `.trellis/workflow.md:155-171` 要求每个 work commit body 按固定顺序包含 `背景：`、`变更：`、`边界：`、`验证：`，并以 `Refs #105` 收尾。
- `.trellis/workflow.md:1147-1152` 明确要求 Branch Review 审查 branch commit messages。
- `.trellis/spec/workflow/quality-guidelines.md:47-55` 将 `check-commit-messages.sh` 列为提交前必检项。
- `guru_team_trellis.py:7876-7910` 的客观 validator 对空 work body 返回“工作提交必须包含 commit body”。
- `origin/main..HEAD` 共 11 个提交，从 `b900a3c` 到 `94d44d7`，实际 `%B` 均只有 subject 和空行，没有任何 body。
- `phase2-check.json.validation_commands` 未记录 commit-message 检查；24 个 resolved findings 也未覆盖该缺口。

影响：

当前分支不满足仓库在任务开始前已存在的提交审计合同，不能通过 Branch Review Gate，也不能进入 finish-work。发布后会永久缺失每轮修复的背景、边界、验证和 `Refs #105` 审计信息。

修复要求：

重写本分支 11 个 work commits，为每个提交补齐完整固定 body；随后重新核验 commit range、Phase 2 证据和 Branch Review 生命周期。

### P1-2：五个平台 `trellis-continue` canonical/dogfood 入口仍保留 archive-first/initial-summary 旧合同

证据：

以下 canonical overlay 与 dogfood 安装副本仍写明：

> publishes after archive, initial finish-summary, and immutable readiness recording succeed

涉及：

- `trellis/presets/guru-team/overlays/.agents/skills/trellis-continue/SKILL.md:58`
- `trellis/presets/guru-team/overlays/.claude/commands/trellis/continue.md:52`
- `trellis/presets/guru-team/overlays/.codex/prompts/trellis-continue.md:52`
- `trellis/presets/guru-team/overlays/.codex/skills/trellis-continue/SKILL.md:58`
- `trellis/presets/guru-team/overlays/.cursor/commands/trellis-continue.md:52`
- 对应 `.agents/.claude/.codex/.cursor` dogfood 副本同样存在。

该文字与 #105 当前合同直接冲突：draft PR 在 archive 前绑定，final summary 只构建一次，不存在 initial finish-summary。

`test_guru_team_trellis.py:9432-9457` 已把 exact phrase `after archive and initial finish-summary` 列为 forbidden，但扫描范围只包含三个 spec 和两个 workflow，没有覆盖 preset overlays 或 dogfood 平台入口，因此测试错误放行。

影响：

Trellis 官方文档确认 platform entry/workflow Markdown 是 AI 运行时合同。新安装和 dogfood 项目仍会向 Claude、Codex、Cursor 注入旧事务顺序，违反 R8、Docs SSOT 和开箱即用一致性要求。

修复要求：

同步修改五份 canonical continue overlays，重新 apply preset 更新 dogfood 副本，并把这些 surfaces 纳入旧语义负向扫描；重跑 overlay drift、installed initial/update-reapply smoke 和完整测试。

## 验证证据

独立检查结果：

- canonical test discovery：`404` 项，执行通过
- 直接脚本前半测试：`265/265 pass`
- preset tests：`36/36 pass`
- Python compile：pass
- Bash syntax：pass
- Draft 2020-12 schema：`4/4 pass`
- `git diff --check origin/main...HEAD` 与 metadata tail：pass
- canonical/dogfood Python、workflow、schema、五个 finish entry equality：pass
- `.new/.bak`：无
- `6177fe9..94d44d7` 的 13 个非 metadata 路径与 `phase2-check.json.dirty_paths` 精确相等
- worktree 无非 metadata dirty path

已审核 Phase 2 的 `404/55/21/36`、initial #105 与 update/reapply #106 installed closeout、71 assets 证据。它们未覆盖上述两项 finding。

## Docs SSOT

核心 closeout、resolver、recovery durable docs 与代码主体一致。

但五份 continue canonical overlays 和五份 dogfood 入口保留旧事务描述，且负向测试漏扫这些运行面，因此 Docs SSOT 总结为 `fail`。

## Ledger 与范围

Scope 分类保持正确：

- close：`[105]`
- related：`[53,96,97,100]`
- follow-up：`[98,99,101]`

primary 与 close acceptance evidence 逐字一致，记录 `404/55/21/36/71` 和两轮 installed smoke。两项新 finding 均属于 #105 当前交付和 Branch Review 合同，不能转为 observation 或 follow-up。

## 部署与安全

- 未修改 CI/CD、Dockerfile、Compose、K8s/Kustomize、Helm、数据库 migration 或 Makefile。
- 配置影响限于 Guru Team publish 默认 draft 与 closeout workflow。
- 未发现真实 token、secret、private key、`.env`、客户数据或签名 URL。
- diff 中 `token:secret` 仅为 strict remote parser 的负向测试 fixture。
- remote URL 错误脱敏、credential 拒绝和 fork identity 保护未见回退。

## 观察项

- 当前分支 remote marketplace verifier 与真实 GitHub closeout E2E 尚未执行；按现有合同由 publish-time fail-closed verifier 承接。
- 远端不存在分支 `fix/105-finish-work-closeout-transaction`。
- 远端不存在 `v0.6.5-guru.3` tag；不得声明 stable tag 安装路径已验证。
- 当前未提交内容仅为 task metadata/reviews tail。

## 后续候选

0。两项均为当前范围阻塞项。

## 结论

Round 16 最终放行失败。

- findings_count：`2`
- P0：`0`
- P1：`2`
- P2：`0`
- P3：`0`
- reuse_decision：`new-agent`

必须先修复 commit history 和所有 continue overlay 的旧事务语义，补充回归扫描，重新执行 Phase 2，并由本 finding owner 完成 closure。之后还需派发未参与任何前序轮次的新 technical agent 执行最终放行审查。
