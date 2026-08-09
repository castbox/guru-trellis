# #179 删除重复的 Publication handoff 与 finish-summary-index artifact

## 1. Goal

在保留 Publication 语义门禁、docs reconciliation、reviewed-content identity 与 Finalizer 确定性事务的前提下，删除 Publication 到 Finalizer 之间重复的 task-local handoff 文件和 commit-message freshness 链。Publication 一次性生成并审查中文 PR title/body，随后通过最小 typed DTO 交给 Finalizer；Finalizer 从 DTO 与 live Git/GitHub/Trellis authority 完成预览、恢复和发布。

Live authority：<https://github.com/castbox/guru-trellis/issues/179>。

## 2. Confirmed Facts

- #177 已由 PR #182 合并，统一的 `guru-reviewed-content-1.0` 与 `branch_review_commit` 边界已经生效。
- #178 已由 PR #188 合并，owner checkpoint 已收敛为短生命周期 ignored runtime；下游 Skill 不读取上游 private checkpoint。
- 当前 workflow 在 Branch Review 后要求调用方编写 `pr-body.md` 与 `finish-summary-index.json`，Publication 再读取两者，Finalizer 继续读取两者并把哈希写入 closeout plan。
- 当前 Publication `ready` schema 3.0 只输出 `exit_id`、`task_ref`、`branch_review_commit`；Finalizer `publication_ready` schema 3.0 仍从 task-local 文件补取 PR body 与 summary index。
- `finish-summary.json:index.*` 是 archived history discovery 的直接检索输入；本 Issue 删除其 Publication 前置文件，不改写历史 archive。
- `guru-create-task-commit` 在创建工作提交前审查并规范化 commit message；下游 Branch Review、Publication 与 Finalizer 无需把 subject/body/`Refs` 当作第二套内容 freshness authority。
- canonical source 位于 `trellis/workflows/guru-team/**` 与 `trellis/skills/guru-team/**`；`.trellis/**`、`.agents/**`、`.codex/**`、`.claude/**`、`.cursor/**` 是 preset 安装副本。

## 3. Requirements

### R1. 删除 Publication 前置 handoff 文件

- current canonical、dogfood、平台副本与 clean install 不得创建、要求、读取或验证 task-local `finish-summary-index.json`。
- `pr-body.md` 不再属于 tracked/untracked task artifact、human artifact 表、workspace boundary inventory、archive move set或 Finalizer 文件输入。
- 历史 archive 保持只读；实现不得批量改写既有 `finish-summary.json`。

### R2. Publication 直接输出最小 PR payload

- `guru-review-task-publication` 直接读取 approved scope、完整 current diff、验证结果、durable docs、Issue Scope Ledger 与 live issue state，生成一次中文 PR title/body。
- Publication 继续真实审查 PR body quality、close scope、validation claims、Branch Review、Docs SSOT、安全与部署影响、未验证边界和 reviewed-content continuity。
- `ready` DTO 只包含 `exit_id`、`task_ref`、`branch_review_commit`、经审查的 `pr_title` 与 exact UTF-8 `pr_body`；每个字段由 `guru-finalize-task:publication_ready` 直接消费。
- Publication public wrapper 完成 owner check、DTO schema validation 后删除自己的 ignored checkpoint；Finalizer 不读取或删除该 checkpoint。

### R3. Finalizer 从 DTO 与 live facts 工作

- `guru-finalize-task` 从 Publication DTO 获取 PR title/body，从 live Git 获取当前 commit、base-to-HEAD diff、changed paths 与 reviewed-content continuity，从 live ledger/task/GitHub 获取 scope 和 PR identity。
- closeout plan 直接保存事务恢复所需的 exact PR payload，不再保存 `pr-body.md` 或 `finish-summary-index.json` 路径/哈希。
- Finalizer 只调整输入源、schema、projection 与验证边界；#105 transaction order、verification route、Draft PR 唯一绑定、archive transaction、三方 HEAD 校验和 Draft-to-Ready 状态机保持不变。
- Finalizer 从经审查 PR payload、task/ledger、live Git paths 与真实 PR identity 一次性生成 `finish-summary.json` 及其 history retrieval projection；不得要求 AI 先写独立 summary-index 文件。

### R4. 移除重复文档与人工交接格式

- workflow、Skill 和 README 不再要求固定 Docs SSOT 填表或在多个阶段重复展示同一 human artifact 表。
- Phase 1 仍保留一个明确 Docs SSOT Plan；Phase 2、Branch Review 和 Publication 仍核对该计划与 durable docs 的真实差异。
- PR body 仍包含可审查的 Docs SSOT/文档同步结论，但不复制完整 task history、owner checkpoint 或 summary index。

### R5. Commit message 不再承担跨 Skill freshness

- `guru-create-task-commit` 可在首次创建工作提交前继续生成并校验中文 Conventional Commit message。
- Branch Review、Publication 与 Finalizer 的 entry/freshness/recovery 不得因 subject/body/`Refs` 格式失败而要求 metadata-only commit。
- commit 后的内容 identity 只由 `branch_review_commit`、`guru-reviewed-content-1.0` 与 live Git diff 证明；commit message 不是 public handoff 字段、checkpoint 字段或 re-entry token。

### R6. Public API 迁移与唯一 consumer

- stable Skill id、external exit id、workflow target id 与 script command id 保持不变。
- Publication `ready` output 与 Finalizer `publication_ready` input 发布新 schema id；旧 3.0 输入由 current validator fail closed，并提示重新运行 Publication，不保留 alias、compatibility reader 或 migration executor。
- Interface 1.3 projection 静态证明五个 `ready` output 字段均由 Finalizer 直接消费；title/body 不从 private runtime、源码扫描或 task-local替代文件补取。
- extension manifest、registry、package interface、schema/example/eval/test、consumer graph 与 installed inventory 在同一次 current-contract 变更中闭合。

### R7. Distribution 与抗漂移

- durable spec、canonical workflow、canonical Skill/runtime/tests、manifest/preset/README 先修改，再由 preset installer 同步 dogfood 与全平台副本。
- preset reapply 后不得遗留 `.new`/`.bak`；dogfood drift、source/installed package closure 与 ownership 检查全部通过。
- clean throwaway 必须覆盖 fresh workflow/preset install、existing-project workflow preview/switch、official Trellis update、workflow/preset reapply、前后两轮 installed checks 与最终零 sidecar。

## 4. Acceptance Criteria

- [ ] A1. current canonical、dogfood、平台副本和 clean throwaway 对 `finish-summary-index.json` 的生成器、reader、validator、schema dependency、fixture、eval、inventory 与文档引用均为零；历史 archive 只读命中除外。
- [ ] A2. `pr-body.md` 不再出现在 task/human artifact、workspace boundary、closeout input、move/archive、README 或 active test contract 中。
- [ ] A3. Publication `ready` 新 schema 输出 exact `pr_title`/`pr_body` 与必要 identity，Finalizer 新 input schema 通过 target-owned authoring seed 无损消费；每个 output field 有唯一 consumer-use 证明。
- [ ] A4. Publication 十维语义审查保留 PR readiness、scope、validation、Branch Review、Docs SSOT、安全/部署、未验证边界和 content continuity；scripts 不生成语义 pass。
- [ ] A5. Finalizer 以 DTO + live facts 完成 side-effect-free preview，closeout plan 不含两个退役 artifact 的 locator/hash，现有六个 exit 与 transaction 顺序保持不变。
- [ ] A6. 新任务的 `finish-summary.json` 由 Finalizer 一次生成并通过 current schema；history discovery 能检索新 summary，既有 archive summary 仍可读取。
- [ ] A7. Branch Review、Publication、Finalizer 不因 commit subject/body/`Refs` 格式创建或要求 metadata-only commit；reviewed content drift 仍返回 task-work 路由。
- [ ] A8. docs reconciliation 能发现本次 durable docs 缺口，workflow/README 不再要求固定重复表格或跨阶段 human artifact 重放。
- [ ] A9. stable Skill/exit/target/command id 未改变；新 public schema id、旧 shape fail-closed 行为、projection、examples、evals 与 source/installed consumer graph 测试通过。
- [ ] A10. runtime/package/integration/preset tests、Python/shell syntax、JSON/JSONL、task validation、`git diff --check`、ownership、dogfood drift、clean throwaway update/reapply 全部通过。
- [ ] A11. 独立 current-HEAD Phase 2 semantic check 与 Branch Review 对完整 scope 无未关闭 P0-P3 finding；未执行的 remote marketplace 验证明示为未验证，不能折算为通过。

## 5. Out of Scope

- 不完整重写 Finalizer transaction engine、marketplace verification 或 finish-family 总流程；该工作由 #180 承接。
- 不改变 #177 reviewed-content 算法、#178 owner checkpoint 生命周期或历史 archive 内容。
- 不删除 PR readiness、Docs SSOT reconciliation、Branch Review、Issue Scope Ledger 或发布副作用确认。
- 不增加恶意 actor、对抗输入、锁、竞态、TOCTOU、额外 fault injection、crash-consistency 泛化或跨 OS 原子性机制。
