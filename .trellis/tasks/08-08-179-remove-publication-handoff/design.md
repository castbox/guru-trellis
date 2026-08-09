# #179 Technical Design

## 1. Design Summary

采用“Publication owns reviewed payload + Finalizer owns transaction facts + archive summary generated once”模型：

1. Publication AI 从 live authority 和 current reviewed content 生成并审查中文 PR title/body；owner-private readiness checkpoint 只在 public wrapper 投影前保存当前 gate 与 payload，投影成功后删除。
2. `ready` DTO 把 exact title/body、task identity 与 `branch_review_commit` 直接交给 Finalizer。Finalizer 不再打开 Publication 文件或 checkpoint。
3. Finalizer 将 exact payload 纳入 immutable closeout plan，使用 live Git/ledger/GitHub facts完成事务，并在真实 PR identity 绑定后一次生成 archive `finish-summary.json`。

全局 workflow step、stable Skill id、exit id、stop/workflow target 和六出口 Finalizer 状态机保持不变。

## 2. Current-to-Target Contract

| Boundary | Current | Target |
| --- | --- | --- |
| Publication content | workflow caller 写 `pr-body.md` 与 `finish-summary-index.json` | Publication AI 在 owner loop 内生成并审查 `pr_title`/`pr_body` |
| Publication private gate | readiness 绑定两个 task-local 文件 bytes | readiness 绑定 reviewed content 与 exact PR payload；wrapper 成功后删除 |
| Publication `ready` | schema 3.0：`exit_id/task_ref/branch_review_commit` | 新 schema 4.0：增加 `pr_title/pr_body` |
| Finalizer `publication_ready` | schema 3.0：DTO identity + task-local body/index | 新 schema 4.0：target-authored `profile/mode` + DTO 五字段 |
| closeout plan publish input | title + `pr-body.md` hash + summary-index input record | exact title/body 直接进入 immutable plan；plan digest绑定 payload |
| archive summary | AI index file经过 Finalizer补充 runtime facts | Finalizer从 reviewed PR payload与 live task/ledger/Git/PR facts一次生成 |
| commit freshness | 下游重复解析 subject/body/`Refs` | 下游只验证 commit anchor、reviewed-content identity、ancestry 与 diff |
| human docs | 多阶段重复 artifact 表与固定 Docs SSOT 表 | 一个 Phase 1 Docs SSOT Plan + 各 owner 对真实 docs delta 的语义核对 |

## 3. Publication Owner Design

### 3.1 Forward behavior

Publication 直接读取：

- live Issue #179、Issue Scope Ledger 与 close/related/follow-up disposition；
- `origin/<base>...HEAD` 完整 diff、`branch_review_commit`、current worktree 与 `guru-reviewed-content-1.0`；
- current planning docs、durable specs/docs、Phase 2/Branch Review 的最小 typed result和可重读验证事实；
- GitHub repo/base/head identity 与 Finalizer side-effect-free preflight。

AI 生成一个中文 title 与一个 Markdown body。body 继续包含变更摘要、影响范围、验证结果、Review Gate、Issue 关闭范围、安全/部署影响和 Docs SSOT/文档同步结论。该内容直接进入十维 semantic gate，不先落盘为 task artifact。

### 3.2 Private readiness and output

`pr-readiness.json` current schema 增加一个 closed `pr_payload`：

```json
{
  "title": "完成：#179 删除重复的 Publication handoff 与 finish-summary-index artifact",
  "body": "<exact reviewed Markdown bytes as a JSON string>"
}
```

该 payload 有且只有一个生命周期 consumer：Publication public wrapper。wrapper 重跑 objective checker，验证 title/body quality、payload 与 semantic dimensions 的绑定，随后输出：

```json
{
  "exit_id": "ready",
  "task_ref": ".trellis/tasks/08-08-179-remove-publication-handoff",
  "branch_review_commit": "<40-hex commit>",
  "pr_title": "<exact reviewed Chinese title>",
  "pr_body": "<exact reviewed Markdown>"
}
```

DTO schema validation 成功后删除 readiness checkpoint。`return_to_task_work` 与 `blocked` shape不扩张；metadata revision 只在 Publication owner loop 内修改内存中的 payload并重审受影响维度。

## 4. Interface Migration Contract

- 保留 `guru-review-task-publication:ready` 与 `guru-finalize-task:publication_ready` id。
- 将 Publication ready output schema id 从 `guru-production-review-task-publication-output-ready-3.0` 升级为 `...-4.0`。
- 将 Finalizer publication-ready input schema id 从 `guru-finalize-task-input-publication-ready-3.0` 升级为 `...-4.0`，并同步 aggregate input schema id。
- Publication interface 的 `finalization_seed_input.seed_fields` 改为 `task_ref`、`branch_review_commit`、`pr_title`、`pr_body`；`profile/mode` 仍由 Finalizer authoring seed提供。
- `project_ready` 只用 Interface 1.3 `select` projection映射上述四个 seed field；`exit_id` 只作为 route identity，不进入 target profile。
- 旧 3.0 shape在 current wrapper 入口 fail closed，remediation 是从 live authority 重跑 Publication。不得保留 alias、隐式补字段、task-local fallback、旧 schema reader或 migration executor。
- manifest、registry、consumer contract、source/installed package tests必须证明每个 public output field均有直接 consumer。

## 5. Finalizer Input and Recovery

### 5.1 Immutable plan

Finalizer preview 从新 DTO 获取 exact title/body，并在 closeout plan `publish` 中保存两者。plan digest已经绑定完整 canonical plan，因此不再需要 `body_sha256` 作为独立文件 identity，也不再记录 `inputs.pr_body` 或 `inputs.finish_summary_index`。

active retry、same-plan resume、Draft metadata convergence 与 archive recovery从 immutable plan获取 exact payload。remote PR rere读后要求 repo/head/base/HEAD/number/URL/Draft/title/body完全匹配。该 plan payload 是事务恢复直接输入，不是另一个 Skill handoff。

### 5.2 Unchanged engine boundary

下列顺序保持：plan prevalidation -> content push -> extension verification route -> unique Draft create/reuse -> final projection -> official archive move -> one archive commit/push -> local/remote/PR HEAD equality -> Draft ready。

`verification_required`、`publication_review_stale`、`resume_finalization`、`reprepare_required`、`published`、`blocked` 六个 exit与 consumer映射保持不变。#179 不压缩该状态机。

## 6. Finish Summary Without a Pre-Handoff Index

保留 `finish-summary.json` 作为 Finalizer 正常路径的 durable archive output，也保留 `index.*` 作为 `guru-discover-change-context` 的直接历史检索输入。删除的是独立 AI-authored `finish-summary-index.json`。

Finalizer 用一个确定性 builder 生成 current finish-summary：

- `task`、issue refs与 title来自 task/ledger；
- `git.changed_paths`、branch与 content identity来自 live Git；
- PR number/URL/title/body来自唯一绑定的 live Draft与 immutable plan；
- `index.problem`来自 task/issue title；
- `index.outcome`与 `index.changed_behavior`来自已审查 PR body的“变更摘要”section，使用既有 Markdown section parser与 bullet parser；
- `index.affected_surfaces`从 exact changed paths按现有 closed surface classifier生成；
- `index.contract_changes`不再接收第二份 AI 转写，current builder写空数组或仅写由 machine facts触发的固定 contract fact；
- `search_terms`与 `retrieval_text`继续由 task/Git/PR/index facts确定性派生。

若 reviewed PR body无法产生满足 current finish-summary schema 的非空变更摘要，Publication readiness阻塞在 PR body quality；Finalizer不得猜测或补写语义。历史 schema 1 archive维持原 reader；新 summary schema/id在 shape变化时升级，并由 discovery reader按明确 current+historical union读取。

## 7. Commit Identity Boundary

- `guru-create-task-commit` 保留首次提交前的 message authoring与semantic review，因为该步骤直接创建 commit。
- `guru-review-branch` 的 entry evidence从 `commit_handoff` 改名为 commit/diff identity，移除对 subject/body/`Refs` 的 freshness断言。
- Publication 与 Finalizer 不运行 range-level commit-message checker，也不把 message parser结果写进 gate、plan或DTO。
- message格式偏差不改变 reviewed content identity，不触发 revision commit；真实 content drift继续由 descendant diff与 `guru-reviewed-content-1.0` 返回 task work。
- standalone `check-commit-messages` 若仍被保留，只能作为显式质量诊断命令，不能成为 Branch Review/Publication/Finalizer pass条件。

## 8. Docs SSOT Plan

Strategy：`ssot_first`。

| Durable SSOT | 本次权威修订 | Direct consumers |
| --- | --- | --- |
| `.trellis/spec/workflow/skill-package-contract.md` | Publication ready 4.0、Finalizer input 4.0、唯一 consumer/projection、旧 shape fail-closed | package interface/schema/example/eval/tests |
| `.trellis/spec/workflow/data-contracts.md` | readiness payload、closeout plan PR payload、finish-summary单次派生、commit identity | shared runtime与schema |
| `.trellis/spec/workflow/companion-scripts.md` | recorder/checker/wrapper与Finalizer executor边界 | Python runtime与bash wrappers |
| `.trellis/spec/workflow/quality-guidelines.md` | PR payload、无退役artifact、无metadata commit、history retrieval回归矩阵 | Phase 2/Branch/finish integration tests |
| `.trellis/spec/workflow/workflow-contract.md` | Branch Review -> Publication -> Finalizer 路由和无文件 handoff | canonical workflow |
| `.trellis/spec/preset/installer.md` | 新 schema/package资产分发、update/reapply与零sidecar | extension manifest、preset tests、throwaway verifier |
| `.trellis/spec/preset/overlay-guidelines.md`、`.trellis/spec/preset/upstream-ownership.md` | canonical-to-installed同步与ownership不扩张 | overlay apply/drift checks |
| `.trellis/spec/docs/public-docs.md` | 三份README对新Publication/Finalizer/commit边界的统一描述 | root/workflow/preset README |

执行顺序：先修订上述 durable SSOT，再修改 canonical Skill/runtime/workflow/README，随后运行 preset installer同步安装副本。task planning docs只记录本 Issue的需求、设计和验证计划；不新增 publication handoff或 review summary文档。

## 9. Distribution and Upgrade/Update

- canonical：`trellis/workflows/guru-team/**`、`trellis/skills/guru-team/**`、extension manifest、preset scripts/README/ownership。
- installed/dogfood：`.trellis/guru-team/**`、`.trellis/workflow.md`、`.agents/skills/**`、`.codex/skills/**`、`.claude/skills/**`、`.cursor/skills/**`及manifest声明的平台副本。
- 使用 `apply.sh --repo . --all-platforms` 从 canonical同步；逐个审查 `.new`/`.bak`，禁止反向手改canonical。
- clean throwaway执行 fresh init/install、existing workflow preview/switch、official target CLI update、workflow/preset reapply、source/installed checks、Finish-family集成与零sidecar断言。
- 当前 branch尚未push时，exact remote marketplace source验证记为未验证；local unpublished workflow fixture可证明安装机制，但不能冒充远端证据。

## 10. Failure and Recovery Matrix

| Failure | Required behavior |
| --- | --- |
| Publication payload缺section或中文内容不足 | owner内修订并重审；未闭合时不返回`ready` |
| payload/identity在wrapper前漂移 | checker fail closed，回到Publication owner |
| DTO schema/projection失败 | 保留同owner checkpoint供修复，不进入Finalizer |
| Finalizer首次preview发现content drift | 返回`publication_review_stale`或fail closed，不重建task artifact |
| same-plan retry | 从immutable plan恢复exact title/body，不读取`pr-body.md` |
| archive summary builder无法从reviewed payload构造current schema | side-effect-free preflight阻塞，不push、不建PR、不archive |
| commit message格式不合规但reviewed content未变 | 下游不创建metadata commit；继续以content identity审查 |
| durable docs缺口 | 当前owner返回finding/task work；不得用固定表格pass替代真实reconciliation |
| base-evolution recorder覆盖legacy gate | current marker写入同owner ignored transition gate；checker/executor保留并复核legacy gate，成功transition后一次退休两者 |

## 11. Risks and Rollback

- 风险：raw body进入DTO后projection或JSON escaping改变bytes。控制：schema/example/integration测试覆盖UTF-8、换行、尾随空格与Publication output到Finalizer input exact equality。
- 风险：删除文件后same-plan恢复丢失body。控制：immutable plan直接保存payload，active/archive recovery都只读plan或remote immutable identity。
- 风险：finish-summary检索质量下降。控制：用既有PR body section parser生成history projection，并对新/旧archive各做discovery检索回归。
- 风险：source/installed副本漏删旧reader。控制：current-path零命中扫描、package closure、dogfood drift、全平台fixture和throwaway update/reapply。
- 回滚：commit前回退本task reviewed-content变更；不得恢复退役task-local文件作为兼容fallback。Finalizer状态机重构留给#180。
