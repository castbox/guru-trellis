# #376 实施计划

## Ordered Checklist

1. 对照现有 `guru-reconcile-task-base` contract、workflow、quality guideline 与 test fixture，确认 integration/authority/task-content 三类事实的现状。
2. 在 canonical workflow/spec 与 reconcile package 中收敛独立时钟语义，保持现有 typed exits、consumer 和无关 base delta 的 `resume_target`。
3. 更新 dogfood、preset 及声明平台投影，确保 canonical source 与安装副本一致。
4. 增加/修订正向 fixture：无关 base delta 保持 `reconciled`；真实 authority/planning assumption 变化返回 `planning_stale`；`post_plan` 不因单纯 base 更新回退。
5. 运行 package contract/runtime/eval 定向验证和 source/projection 一致性检查。
6. 通过 Phase 2 check 后，再执行 commit、完整 Branch Review 与 publication readiness；本规划阶段不执行这些动作。

## Validation Commands

```bash
python3 -m json.tool trellis/index.json
find trellis/skills/guru-team/runtime trellis/skills/guru-team/packages -name '*.py' -type f -print0 | xargs -0 python3 -m py_compile
python3 -m py_compile trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py
python3 ./.trellis/scripts/task.py validate .trellis/tasks/09-07-376-reduce-base-interference
git diff --check
```

追加执行 `guru-reconcile-task-base` 的 canonical unittest、runtime subset、eval/contract discovery，以及 preset projection drift 检查。

## Risk Points

- 不能把 base freshness digest、integration delta 或 recorder 输出当作 semantic planning decision。
- 不能把无关 base delta 误路由为 `planning_stale`，也不能放宽真实 authority 变化的 stale 路径。
- 不能覆盖当前 workspace 之外的 `main` dirty 文件、既有 sidecar 或其他 task workspace。

## Pre-start Gate

- 规划文档完成且无阻塞 open question。
- `implement.jsonl` 与 `check.jsonl` 各有真实研究/验证条目。
- 用户明确批准本规划摘要后，才允许 `task.py start` 和实现。

## 2026-09-08 Base Reconciliation

1. 已将精确新基线 `d95f875cc4751c4487444b942901bf5023e44acc` 以 no-commit merge 方式集成，未创建 commit、未 push、未更新 PR。
2. 已保留新基线删除的 clarify-requirements 旧 eval typed-output 注入逻辑；Branch Review finding `BR-376-NATIVE-ADAPTER-3000` 要求移除 #376 的 task-local recipe alias，改由 fixture 复用已有 `base-reconciled`。
3. 已从 Git 三阶段 manifest 重建组合结果，并将 native adapter 哈希更新为当前 canonical/installed 一致字节。
4. 验证范围增加：reconcile package contract/runtime/eval、clarify package 回归、source/installed manifest 与 adapter identity、overlay drift、task/JSON/Python/diff/sidecar 检查。
5. 既存 #108 `.bak` sidecar 与 projection 漂移不属于 #376；不清理、不提交，也不把其全量 reapply 结果纳入本任务。

### Validation Result

- PASS：canonical 与 installed `guru-reconcile-task-base` 各 20 项单测。
- PASS：canonical 与 installed `guru-clarify-requirements` 各 11 项回归测试。
- PASS：reconcile source eval discovery 与 shared adapter 全 7 case；新增 `unrelated-base-delta-reconciled` 保留原 `resume_target`。
- PASS：source package closure（23 packages / 77 commands）、4,729 个 installed manifest 声明文件哈希、reconcile installed/四平台投影字节、workflow/spec/adapter identity、overlay drift、JSON/Python/task/scoped diff 检查。
- BLOCKED BOUNDARY：installed eval discovery 被 #376 范围外的既存 #108 installed projection/`.bak` sidecar 漂移阻断；未清理或吸收该状态。
- SUPERSEDED EVIDENCE：基线集成后的早期全候选 `git diff --check` 曾命中 #377 archive Markdown 的 EOF 空行；当前 finding-fix worktree 已重新执行全量 `git diff --check` 并通过，未修改 #377 归档内容。

## 2026-09-08 Branch Review Finding 修复计划

1. 将 canonical、installed 与 Agents/Codex/Claude/Cursor 的 `unrelated-base-delta-facts.json` staging recipe 从 `base-unrelated-reconciled` 改为已有 `base-reconciled`。
2. 从 canonical/installed `native_adapter.py` 删除 #376 新增的 alias 行，使完整 `origin/main...HEAD` 不再触碰该 6798 行共享文件。
3. 使用仓库现有确定性 manifest 计算/校验规则，更新 `.trellis/guru-team/extension.json` 中受影响文件哈希、`guru-reconcile-task-base` package tree、managed tree/provenance；保留 #377 与其他基线字段。
4. 定向验证 fixture JSON、六份 fixture 字节一致、canonical/installed adapter 字节一致、reconcile eval/contract、installed manifest、task artifact、scoped `git diff --check`，并确认 39 个 `.bak` 数量和内容未被修改。
5. 以 `git diff --name-only origin/main...HEAD` 和 adapter scoped diff 验证 subtraction-first 结果；不执行会吸收范围外 sidecar 的全量 reapply，不执行 commit、push、PR 或 cleanup。

### Branch Review Finding 修复结果

- PASS：六份 `unrelated-base-delta-facts.json` 已统一复用 `base-reconciled`；canonical/installed adapter 已删除 task-local alias，当前 worktree candidate 相对 `origin/main` 的 adapter diff 为空。
- PASS：canonical 与 installed `guru-reconcile-task-base` 各 20 项单测；canonical 与 installed `guru-clarify-requirements` 各 11 项回归测试。
- PASS：source contract discovery、7-case eval discovery 与 shared 7-case production eval；`unrelated-base-delta-reconciled` 仍返回 `reconciled` 并保留 `resume_target=task_activation`。
- PASS：source package closure（23 packages / 77 commands）、4,729 个 installed manifest 声明文件哈希、六份 fixture 与 canonical/installed adapter 字节一致、overlay drift、JSON/Python/task 与全候选 `git diff --check`。
- BOUNDARY：installed 全量 package validation 仍仅被既存 #108 Claude projection 与 39 个 `.bak` provenance drift 阻断；本任务未修改、删除或吸收这些 sidecar。
- BOUNDARY：未执行完整多平台 throwaway、upgrade/update、reapply 或 release-candidate 矩阵；其 owner 仍是专门兼容性或 Release Issue。

## 2026-09-08 Finalizer Base Reconciliation 结果

- Finalizer preview 对 `29ef6d482bb7c13bf65d23b1ffdb806c4afdc531` 返回 `base_reconciliation_required`，新 base 为 `81657210f5508186ed0f09098fdc63c927fdc307`；preview 无副作用。
- 已以 no-commit merge 集成新 base，唯一冲突 `.trellis/guru-team/extension.json` 按 JSON 结构解决：保留两侧 package/file inventory，保留 #376 当前 dirty provenance preimage，不运行全量 preset reapply。
- PASS：canonical reconcile 20/20、installed reconcile 20/20；canonical Discovery 16/16、installed Discovery contract/runtime 7/7 + 9/9。
- PASS：reconcile 与 Discovery package tree digest 和当前 manifest 精确一致；source package validation 23 packages / 77 commands；ownership、overlay drift、task artifact、JSON、Python compilation 与 `git diff --check` 通过。
- BOUNDARY：installed full validation 仍仅被 Issue #108 既存 approve/check/review Claude projection 与 digest provenance drift 阻断；39 个 `.bak` 未修改、未删除、未提交。
- ROUTE：不重新规划或重新实施 #376 业务行为；对本次 tracked manifest composition 运行 fresh Phase 2、Task Commit、完整 Branch Review 与 Publication 后恢复 Finalizer。

## 2026-09-08 Accepted Scope 扩展实施计划

1. 更新 canonical `guru-reconcile-task-base` contract/runtime/evals/tests，使已有完整 review 的 compatible base evolution 在需要刷新 reviewed-content identity 时返回 `review_continuity_required`，保留原 `resume_target`。
2. 在 reconcile package 内增加 expected-head 绑定的确定性 reconciliation executor：仅在 AI 已完成 exact candidate 判断并展示精确 Git 副作用、用户当次确认后执行；创建一个本地 merge/commit，不 push、不改 PR，并验证 prior review/new base ancestry 与 candidate tree。
3. 直接演进 canonical `guru-review-branch:base_continuity`：输入分别绑定 prior full-review commit 与 current reconciled task HEAD；owner-private gate freshness 同时绑定二者，输出 current HEAD 给 Publication。
4. 为语义变化的 review-continuity output、base-continuity input、continuity-passed output、aggregate input、review gate 及需要新增执行 receipt 的 reconcile private schema 使用新的 current-only version；同步 interface/commands/examples/consumers，删除旧版本 current authority，不增加双读或兼容 wrapper。
5. 保持 `guru-review-task-publication` 的当前 reviewed-content 严格门禁，不增加 bypass；仅更新合同与回归，证明 continuity 输出的 current HEAD 可按现有 Publication schema/identity 进入 `ready`。
6. 同步 workflow、quality guidelines、skill/data/workflow contract、canonical package、preset、dogfood 与 Agents/Codex/Claude/Cursor 声明投影；更新 installed manifest 的精确 inventory/digest。
7. 增加真实跨 Skill integration regression：Finalizer base mismatch → reconciliation semantic result → confirmed local reconciliation commit → bounded continuity → Publication ready；断言无 implementation route、无完整 Branch Review replay、prior/current review identity 不混淆且无 remote mutation。
8. 增加负向回归：未确认不写 Git、dirty/stale expected HEAD、prior review 或 new base 非祖先、task HEAD/pair/candidate tree 漂移、task content 或 authority 真实变化时不得 continuity pass。
9. 执行相关 package/runtime 测试、跨 Skill integration、Architecture no-impact check、source/installed validation、ownership、overlay drift、task validation、JSON/Python 与 `git diff --check`；#108 已知 installed projection drift 保持独立边界。
10. 完成 fresh Phase 2、Task Commit 和一次完整最终 Branch Review；该最终 review 审查本次真实合同修复 diff，不是仅因 base 前进而重复旧 review。

### Scope authority

- Live Issue comment: `https://github.com/castbox/guru-trellis/issues/376#issuecomment-5585538277`。
- 本扩展不新增 public exit 或长期兼容路径；语义变化的 public/private schema 直接升级为 current-only，旧 continuity checkpoint 不迁移。

## 2026-09-08 Cross-Skill Continuity 最终实施结果

### 实施中发现与修复

1. **Tree identity 算法不一致**：reconciliation executor 与 checker 曾使用不同的 candidate tree 计算边界，导致合法本地 reconciliation commit 无法稳定承接 prior full-review identity。现已统一为相同的 Git tree identity，并分别绑定 prior full-review commit、new base 与 current reconciled task HEAD。
2. **Installer/validator integration inventory 缺口**：preset installer 与 installed validator 未分发或验证 continuity integration。现已安装并校验 `test_finish_family_integration.py` 与 `test_base_continuity_integration.py`，throwaway initial 和 update-reapply 路径均执行 continuity integration。
3. **Review gate 7.0 producer/consumer allowlist 漂移**：installer、installed validator 与四个平台投影仍引用旧 gate 6.0。现已将 current authority 更新为 `review-gate-7.0.schema.json`，保留 6.0 仅作 legacy inventory，不再参与 runtime current path。
4. **Source/installed runtime import 路径不一致**：continuity integration 只覆盖 source 布局，installed 布局无法解析 package runtime。现已同时加入 `SKILLS` 与 `SKILLS.parent`，覆盖 `trellis/skills/guru-team/runtime` 和 `.trellis/guru-team/runtime` 两种受支持布局。

### 最终验证结果

- PASS：canonical reconcile package `23/23`、Review Branch package `26/26`、Publication package `48/48`。
- PASS：source 与 installed continuity integration 各 `2/2`，skill package integration `9/9`。
- PASS：source package validator 覆盖 23 个 package、78 个 command。
- PASS：installer 定向验证覆盖 gate 7.0 canonical/installed/四平台投影、explicit Claude install 与 all-platform install，共 `3/3`。
- PASS：临时 clean install `/private/tmp/guru-376-dogfood-final.mb1Yw9` 返回 `status=ok`、skill package `status=ok`、installed validation `passed`，且 `new_copies=[]`、`managed_backups=[]`。
- PASS：canonical/installed/platform checksum、ownership、dogfood workflow/overlay drift、task artifact、JSON、Python compilation、shell syntax 与 `git diff --check`。
- PASS：`native_adapter.py` 相对 `origin/main...HEAD` 无 #376 diff；Issue #108 的 39 个 `.bak` 数量和内容保持不变。
- BOUNDARY：installed full validator 仍仅因 Issue #108 的 Claude projection、package digest 与 sidecar inventory drift 失败；本任务不修复、不登记、不删除这些 `.bak`。
- BOUNDARY：完整 installer suite 的剩余失败来自当前 `main` 上与 #376 无关的旧 adapter/discovery 文案断言；不为追求全绿扩张 accepted scope。

### Architecture Phase 2

- Route：`no_architecture_impact`。
- 本实现继续复用既有 semantic owner、deterministic executor、当前对话确认边界和 typed projection；未新增 shared-current writer、dual-read、长期 compatibility、SDK、外部集成、GAP 或 ADR。
- `guru-trellis-architecture-convergence@1` before/after 无 regression；不创建 Architecture contribution 或 ADR。

## 2026-09-08 最终 Branch Review Findings 修复

### Qualified findings

1. `BR-376-RECOVERY-STALE-HEAD`：reconciliation commit 已创建且 recorder 已写入精确 current-pair checkpoint 时，pair guard 必须先验证该 checkpoint，再应用普通 prior-HEAD stale 拒绝；否则正常 commit → record → recovery 序列会被提前阻断。
2. `BR-376-CONTINUITY-DTO-CONTRACT`：`prior_branch_review_commit` 仅由 bounded continuity gate 用于 private ancestry/freshness 校验，Publication 与 continuity router 均不消费该字段；因此从 durable public output wording 删除，不扩大 DTO。
3. `BR-376-STALE-CURRENT-VERSIONS`：Review Branch durable companion/data SSOT 的 current authority 同步为 aggregate input 4.0、base-continuity 2.0、gate 7.0，并保留旧版本仅作为 legacy stale inventory。
4. `BR-376-REAL-PUBLICATION-INTEGRATION`：跨 Skill integration 不再 mock Publication owner/checker，改为构造真实 task、ledger、package/schema 与 Git identity，调用实际 Publication recorder、checker 和 public wrapper。

### Validation result

- PASS：canonical 与 installed reconcile runtime 各 `18/18`；新增 post-reconciliation current-pair 恢复回归。
- PASS：canonical 与 installed Review Branch contract 各 `22/22`；断言 continuity public output 不包含无消费者的 prior review 字段，并锁定 current schema wording。
- PASS：source 与 installed cross-Skill continuity integration 各 `2/2`；真实链路覆盖 reconciliation → bounded continuity → Publication recorder/checker/wrapper → `ready`，负向链路拒绝未审查 base merge。
- PASS：Publication package `48/48`、skill package integration `9/9`、installer targeted `3/3`、source package closure `23 packages / 78 commands`。
- PASS：canonical/installed 字节一致、manifest 受影响 hash/package tree、ownership、dogfood workflow/overlay drift、task、JSON、Python、shell 与 `git diff --check`。
- BOUNDARY：installed full validator 仍仅被 Issue #108 的 Claude projection、package digest 与 39 个 `.bak` sidecar provenance drift 阻断；本 finding fix 未修改、删除或登记这些 sidecar。
- BOUNDARY：未执行完整多平台 upgrade/update/reapply/release-candidate 矩阵；该矩阵仍由专门兼容性或 Release Issue 负责。
