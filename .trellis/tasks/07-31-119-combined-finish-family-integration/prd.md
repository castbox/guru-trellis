# #119：完成 Finish family 集成并迁移 Guru 收尾入口

## 1. 目标

基于 live `main` `7ca1a0b96492cbb265bcd7715d14ac93c897fc98` 补齐
PR #162 与 PR #165 之后仍缺失的 combined Finish-family integration，使
`guru-review-task-publication`、`guru-finalize-task`、
`guru-verify-extension-installation` 的现有 public contracts 由 global workflow、
Guru namespace 平台入口、private runtime projection、production eval 与安装门禁形成
一条完整且可恢复的收尾路径。

本 task 完整验收后，scope ledger 中的 #119 与 #115 进入关闭规划。#105、#116、
#117、#118 保持 related；#132 保持 follow-up。

## 2. 权威与当前基线

- 当前需求权威是 live Issue #119 正文、评论 `issuecomment-5045074001`、Issue #105
  正文、用户本轮边界、仓库 `AGENTS.md` 与 current durable specs。
- PR #162 与 PR #165 已交付三个 Finish Skills、13 个 external exits、六组核心
  producer-consumer routes、mapped exit 自动承接、最小 public DTO 与 AI-first
  interaction contract。本 task 不重做这些交付。
- 冻结 donor `d01111b3628c2a4b00b99ee098703acefe8620c9` 只提供入口文案、eval case、
  private projection threading 与回归结构的语义参考。旧 task artifact、gate、plan、
  liveness、review report、runtime evidence、commit plan 均不进入本 task。

## 3. 功能需求

### 3.1 Global workflow 与 typed exit consumers

- Canonical workflow 与 dogfood workflow 必须继续按 stable Skill id mandatory invoke
  三个 Finish owners，并为每个 external exit 保留一个 consumer 或一个 fail-closed stop。
- 已映射的 verification、publication stale、same-plan resume 与 reprepare route 必须自动
  承接。happy path 不插入通用“确认继续”。
- Workflow、平台入口与 consumer 不读取 producer private gate、checkpoint、transaction
  journal、完整 digest bundle 或 review narrative。
- Missing、stale、unknown、multiple、unmapped exit 或 consumer mismatch 必须停止。

### 3.2 Guru namespace 入口与兼容迁移

- Canonical preset overlay 必须新增三个显式入口：
  `.codex/prompts/guru-finish-work.md`、`.claude/commands/guru/finish-work.md`、
  `.cursor/commands/guru-finish-work.md`。
- 三个入口只加载 live workflow、mandatory Skill ids 与 typed exit routing，不调用
  deterministic closeout script，不复制 package schema，不创建 handoff artifact。
- 日常文档与 global workflow 必须将 `guru-finish-work` 写为收尾入口。
- 现有五个 `trellis-finish-work` overlay 保持 #132 管理的 bounded compatibility asset；
  #119 从其 `blocking_issues` 移除，`removal_issue=132` 保持不变。本 task 不修改其
  upstream payload bytes，也不执行 physical removal。

### 3.3 Cross-skill evidence integration

- 当 current #117 owner result 为 checker-passed `verified` 且 current closeout plan 要求
  extension verification 时，#118 private runtime 必须构建 legacy transaction validator
  所需的内存 projection。
- 该 projection 必须沿 preview/retry、final projection、active archive validation、normal
  archive transaction 与 active-completed recovery 传递，不得覆写 #117 owner artifact，
  不得进入 public DTO。
- Projection 缺失、失配或无法验证时必须在 archive mutation 前停止，并返回当前 owner
  合同声明的 blocker。
- Content push 写入 immutable plan 的精确 `pending_machine` evidence 后，已通过的
  publication semantic review 必须仍可作为 current owner result 被 finalizer 消费。
  该兼容窗口严格限定为 `issue-scope-ledger.json` 中的唯一机器 evidence 变化及其
  artifact/entry/working-tree 派生 binding；任何额外 ledger 语义或 artifact 漂移仍必须
  返回 `publication_review_stale`。

### 3.4 Combined production eval

- `guru-finalize-task` canonical corpus 必须新增
  `publication-ready-published` 与 `same-plan-published` 两个 terminal cases。
- 两个 cases 必须执行 real public wrapper，分别复用 `publication_ready` 与
  `same_plan_resume` input profile，并在 wrapper 返回后断言 `exit_id=published`。
- Shared、Codex、Claude、Cursor 的 installed discovery copies 必须与 canonical corpus
  byte-identical；adapter 不读取 canonical corpus、private runtime 或 owner artifact。

### 3.5 #105 事务与 recovery 回归

- 完整执行现有 #105 deterministic suite，覆盖 prepare、content push、verifier、evidence
  commit/push、draft create/reuse、final projection、archive move/commit/push、remote HEAD、
  draft-to-ready、cross-month reprepare、active/archived/exact-commit recovery、PR identity
  分支、path/mode/blob/hook/children/allowlist drift。
- 新增 regression 必须证明 normal closeout 与 active-completed archive recovery 均消费同一
  checker-passed marketplace projection，并保持 task location、PR draft/state、local/remote/PR
  HEAD、dirty/staged paths、artifact mutation 与唯一 next exit 的既有断言。
- 本 task 不改变 #105 transaction order、finish-summary history contract 或 failure model。
- 回归必须真实覆盖 publication 先绑定、content push 后写 pending ledger、checked
  `verified` re-entry 自动进入 `resume_finalization`/`evidence_ready` 的正常顺序，不得
  通过预先把 pending evidence 写入 publication fixture 规避 freshness 校验。

### 3.6 Clean install、update、preset reapply 与平台验收

- Clean throwaway repo 必须验证 marketplace index、workflow install/preview/switch、preset
  安装、Guru entries、三个 Skills、scripts、schemas、config 与 executable modes。
- 同一 throwaway 必须在 `trellis update` 后重新选择 workflow、重新应用 preset，并验证
  managed hashes、`.new`/`.bak`、Guru entries、legacy compatibility 与完整 closeout transaction。
- CLI upgrade 入口必须使用 ownership inventory 绑定的版本运行
  `trellis upgrade --dry-run --tag <target_trellis_cli>`；该门禁不得修改 host global installation。
- Pre-current-preset upgrade fixture 必须证明 recognized managed files 依合同备份并替换，
  unknown local edits 生成 `.new` 而非静默覆盖。
- Dogfood 必须经 canonical overlay apply 生成，并通过 overlay drift 与 upstream ownership
  checker。
- README 中列出的命令必须由 throwaway verifier 实际执行，流程不得依赖本机隐藏状态。

### 3.7 Ownership、Docs SSOT 与减法

- Canonical source、dogfood copy、installed copy 与 ownership inventory 必须清楚区分。
- `trellis-finish-work` 的五个 transitional entries 不再被 #119 阻塞；#132 继续拥有其
  physical removal 与全仓 upstream overlay convergence。
- 删除本 task 引入面上的 duplicate route assertions、dead helper 或只验证旧日常入口的
  tests；不得删除 #132 管理的 legacy files。
- Durable workflow/spec/README 必须在实现阶段完成 `ssot_first` 同步；task 规划只保存
  provenance、执行顺序与验证记录。

## 4. AI-first 与 public contract 约束

- Public DTO 结构、`exit_id` discriminator、六组 consumer projections 与三个 Skill 的
  semantic ownership保持 current main 语义。
- 不新增 routine handoff、无人消费的 artifact、无人消费的 output field、总聚合 DTO、
  generic continuation prompt 或 consumer 对 producer private state 的解析。
- Script 只执行、记录或校验客观事实；scope、充分性、finding、route 与 PR readiness
  仍由所属 semantic Skill 判断。

## 5. 明确排除

- 不重新实现或重新审核 #116、#117、#118 的 Skill 内部行为。
- 不移植 PR #160，不 cherry-pick、merge 或 rebase 冻结 donor。
- 不实现或关闭 #132，不删除 upstream namespace legacy assets。
- 不扩展 malicious actor、forgery、adversarial input、并发竞态、TOCTOU、锁、分布式锁、
  新 fault injection、偶发 crash consistency、跨 OS atomicity。
- 不 commit、push、创建 PR、merge、关闭 Issue 或清理资源，除非用户针对该动作另行授权。

## 6. 验收标准

- [ ] Canonical 与 dogfood workflow 的 Finish route 只编排 stable Skill ids、13 exits 与唯一
  consumers，并将 `guru-finish-work` 写为日常收尾入口。
- [ ] 三个 Guru namespace 平台入口由 preset 安装，内容薄且跨平台语义一致。
- [ ] 五个 legacy finish entries 保持现有 payload 与 `removal_issue=132`，其
  `blocking_issues` 不含 #119。
- [ ] Checked #117 marketplace evidence 经 private projection 贯通 normal、retry、final
  projection、archive transaction 与 active-completed recovery，不改变 public DTO 或 owner artifact。
- [ ] Finalizer corpus 新增两个 terminal published cases，canonical、installed、Codex、Claude、
  Cursor copies 与 real-wrapper grader 全部通过现有 contract checks。
- [ ] `test_guru_team_trellis.py` 完整通过，新增 normal/recovery regression 通过，#105 matrix
  未被删减。
- [ ] Preset installer tests、ownership tests、Skill package tests、combined integration tests、
  CLI upgrade dry-run、overlay apply/drift 与 clean throwaway install/update/reapply 全部通过。
- [ ] Durable docs/spec/README 完成 Docs SSOT Plan，schema/public I/O 无变化的理由有审计记录。
- [ ] 冻结 donor HEAD、tracked dirty、untracked reports 与 ignored runtime inputs 保持原样。
- [ ] `git diff --check` 通过；工作树只含本 task 授权范围内的规划、实现、测试与文档变更。

## 7. 文档状态

`stale_docs`。唯一 Docs SSOT Plan 位于 `design.md` 的“Docs SSOT Plan”章节。
