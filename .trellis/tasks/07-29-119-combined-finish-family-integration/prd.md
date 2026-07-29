# 集成 Task 收尾 Skills 并迁移 trellis-finish-work

## 1. 目标

在不重新实现或重新审核 `guru-review-task-publication`、
`guru-verify-extension-installation`、`guru-finalize-task` 内部行为的前提下，完成
Issue #119 尚缺失的 Finish-family combined integration：

- 让 global workflow 只保留 mandatory invocation、全局顺序、13 个 typed exits 的唯一
  consumer/stop 和 fail-closed 边界；
- 新增 Guru namespace 的显式 Finish 平台入口，并给既有
  `trellis-finish-work` 提供有界兼容迁移；
- 用 public Interface 1.3 DTO 和 target-owned authoring partition 验证跨 Skill 路由，
  不读取 owner-private artifact/runtime；
- 完整回归 Issue #105 已明确的事务、failure 和 recovery matrix；
- 完成 clean install、workflow preview/switch、upgrade/update、preset reapply、
  `.new`/`.bak`、dogfood drift 和 Shared/Codex/Claude/Cursor 验收；
- 删除 Finish family 范围内仍存在的重复 SSOT、dead wrapper/helper/test，同时保留由
  #132 明确拥有的全仓 upstream overlay cleanup。

## 2. 当前权威与范围

### 2.1 权威来源

- Live Issue #119 正文及 2026-07-22 accepted-current 评论：
  <https://github.com/castbox/guru-trellis/issues/119>
- Live Issue #105 事务与 recovery 验收：
  <https://github.com/castbox/guru-trellis/issues/105>
- Live Issue #115 umbrella close scope：
  <https://github.com/castbox/guru-trellis/issues/115>
- Live Issue #132 related/follow-up 边界：
  <https://github.com/castbox/guru-trellis/issues/132>
- PR #162 已合并后的 current `main@b034f466755c5c0b4e2e48bf260bb54ef58cb5be`。
- 本次用户明确边界：只补 #119 combined integration，不重做 #116/#117/#118，不移植
  PR #160 task artifacts，不提前实现或关闭 #132。

### 2.2 Issue Scope Ledger

- `close_issues`: `#119`, `#115`
- `related_issues`: `#105`, `#116`, `#117`, `#118`
- `followup_issues`: `#132`

`#105` 保持 completed，不重新关闭；`#132` 只能使用 related/follow-up 语义。

## 3. Acceptance 差额审计

### 3.1 PR #162 / current main 已完成

| 验收项 | 当前证据 | 结论 |
| --- | --- | --- |
| 三个 Finish Skills active | `trellis/skills/guru-team/registry.json` 中三个 package 均为 active Interface 1.3 | 已完成 |
| 13 个 external exits | publication 3、verification 4、finalizer 6；每个 output 均有独立 schema/example | 已完成 |
| 唯一 consumer 与 fail-closed marker | canonical/dogfood workflow 已声明对应 mandatory invocation、consumer/stop marker | 已完成 |
| 核心自动 recovery route | `verification_required`、`publication_review_stale`、`resume_finalization`、`reprepare_required` 已映射到唯一 owner | 已完成 |
| 最小 typed handoff 基础 | 三个 package 使用 `exit_id`、consumer projection、target-owned authoring partition；private artifacts 已分类 | 已完成 |
| #105 deterministic substrate | closeout plan、Draft PR、archive transaction、三方 HEAD、recovery 的生产 engine 和大量回归已存在 | 已完成 |
| 安装基础设施 | preset installer、source/installed package validator、throwaway verifier、update/reapply 和 dogfood drift 工具已存在 | 已完成 |

### 3.2 已交付但未闭合

| 验收项 | 已有交付 | 仍缺失 |
| --- | --- | --- |
| Workflow 薄化 | Phase 3 已按 Skill id 路由，入口不再直接调用 `finish-work.sh` | Phase 3.6/3.7 及通用 finish 说明仍复制较多 owner/transaction/authoring 细节，需要收敛为全局编排合同 |
| 显式 Finish 入口 | 五份 legacy `trellis-finish-work` overlay 已是薄路由 | canonical 名称仍属 upstream namespace；没有 Guru namespace 平台入口，脚本阻断错误和 durable docs 仍把 legacy 名称当主入口 |
| 兼容迁移 | ownership inventory 已把 legacy Finish entries 标为 transitional，blocking issue 为 #119、removal issue 为 #132 | 尚无新 canonical entry、removed/retained compatibility inventory 和新旧入口一致性验收 |
| Cross-skill evidence | package-local corpus 覆盖 3+4+6 exits，现有 eval 已执行 producer projection 与目标 wrapper 的单 Skill 路由 | 尚无覆盖 normal/extension/return/stale/resume/reprepare/published/blocked 的 Finish-family routing-only combined transcripts |
| 安装与更新 | throwaway 已验证 workflow install/switch、preset/update/reapply 和 installed closeout | 断言仍绑定 legacy entry；尚未证明 Guru entry 在初装、update/reapply、三平台 entry 与四 adapter 执行后保持 current |
| #105 regression | 生产 test module 已有完整 transaction/recovery test family | #119 尚未以 current HEAD 完整执行并形成 combined acceptance 证据，throwaway 也未绑定新入口 |
| Docs SSOT | durable specs/README 已描述三个 Skill 和自动 recovery | 主入口命名、#119 closure、#132 retained boundary 和 combined evidence 仍是旧状态 |

### 3.3 尚未完成

- Guru namespace canonical Finish entry 及 Codex/Claude/Cursor 显式适配。
- 新入口在 ownership/extension managed-path 合同中的 additive Guru ownership；不能改变
  Issue #128 的 43 条 frozen legacy identity。
- 新旧入口兼容 inventory：哪些旧路径冻结保留到 #132、哪些 Finish-family 重复说明或
  dead tests 在 #119 删除。
- 八类 combined routing transcripts 与 13-exit/六条关键 producer-consumer edge closure。
- 新入口 clean install、upgrade/update、preset reapply、sidecar、dogfood、四平台验收。
- current implementation 上完整 #105 matrix 的执行证据。

因此 #119 不是 no-code closure。

## 4. 功能需求

### FR-1 薄 workflow 编排

- Canonical 与 dogfood workflow 必须 byte-current，并只拥有 Finish-family 全局顺序、
  stable Skill ids、entry evidence 摘要、mandatory invocation、external exit 到唯一
  consumer/stop 和 short breadcrumb。
- Workflow 不得复制三个 Skill 的 schema 字段教程、十维 publication review、verification
  capability matrix、closeout builder/validator 算法、transaction/recovery 状态实现或
  fault-injection 步骤。
- Missing mandatory Skill，missing/unknown/multiple/unmapped exit，stale/mismatched
  handoff 或无唯一 consumer 必须 fail closed。

### FR-2 Guru namespace 平台入口

- Canonical 日常与 recovery 入口命名为 `guru-finish-work`。
- Codex prompt、Claude command、Cursor command 只做 orientation、加载 live workflow、
  mandatory Skill invocation、typed-exit loop 和最终结果路由，不直接调用 deterministic
  closeout script，不复制 Skill 正文。
- 不创建只有路由作用的第四个 public closed-loop Skill package；Shared 平台继续通过
  global workflow 和三个 active `guru-*` Skills 执行。
- Happy path 只保留 `guru-finalize-task` 首次精确副作用 plan 所需确认，不新增 generic
  `确认继续`，不让用户选择 `verification_required`、resume 或 reprepare flags。

### FR-3 有界 legacy 兼容

- 不修改、重写或新增 upstream namespace `trellis-finish-work`、`trellis-continue` 的
  行为 overlay。
- Issue #128 冻结的 legacy paths 和 digest identity 在 #119 保持不变；现有 legacy
  Finish entry 仅作为 compatibility router 保留，最终物理删除仍由 #132 负责。
- Direct `finish-work.sh` / `publish-pr.sh` 的 fail-closed guidance、README 和新验收应指向
  canonical `guru-finish-work`；生产仍由 `guru-finalize-task` 私下调用既有 internal adapter。
- 不双写 legacy/new artifact schema，不恢复 `--skip-archive` 或
  `--recovery-after-finish-work` 用户选择。

### FR-4 Cross-skill evidence integration

- 验证以下六条关键 edge：
  `#131 passed -> #116`、`#118 publication_review_stale -> #116`、
  `#116 ready -> #118`、`#118 verification_required -> #117`、
  `#117 verified|not_required -> #118`、`#118 reprepare_required -> #118`。
- 每条 `skill_input_authoring_seed` 必须证明 seed/authoring 不相交、union 精确覆盖 target
  required fields、merge 无覆盖且完整 target schema 通过。
- Combined transcripts 覆盖 normal non-extension、extension、return-to-task-work、
  publication stale、same-plan resume、cross-month reprepare、published recovery 和 blocked。
- Transcript 只执行或消费 public wrapper/DTO/consumer contract；native-visible context 不得
  读取 corpus、owner-private artifact 或 import `guru_team_trellis.py`。
- 不创建 routine handoff、重复书面记录或长期 combined transcript artifact；运行结果进入
  test/Phase 2/Branch Review evidence 即可。

### FR-5 #105 完整回归

完整执行 current production matrix：prepare、content push、verifier、evidence
record/commit/push、draft create/reuse、final projection、archive move/commit/push、remote
HEAD check、draft-to-ready、cross-month reprepare、active/archived/exact-commit recovery、
duplicate/fork/closed/replacement PR，以及正文列出的 symlink/path/mode/blob/hook/children/
allowlist drift。每个 failure/retry 继续由既有唯一 production owner 测试 task locator、PR
draft/state、local/remote/PR HEAD、dirty/staged paths、artifact mutation 和唯一 next route。

### FR-6 安装、升级与多平台验收

- Clean throwaway 验证 marketplace index、workflow init、preview、switch。
- Preset 安装三个 Skills、scripts、schemas/config、Guru entry 和声明平台 copies；可执行位、
  managed inventory 与 source/installed equality 正确。
- `trellis update --force` 后重新选择 workflow 并 reapply preset；检查保留/冲突行为、
  managed hashes、`.new`/`.bak`、workspace/developer identity 不被污染。
- Guru entry 在 fresh install 与 update/reapply 后均可发现，legacy entry 只按兼容 inventory
  保留；README 命令不依赖本机隐藏状态。
- Shared/Codex/Claude/Cursor 对同一 Finish corpora 和 combined routes 给出一致结果；平台
  unavailable/unsupported 仍按既有 adapter contract 处理。
- Canonical/dogfood workflow、Guru entries 和 installed packages 通过 drift checks。

### FR-7 减法与文档

- 删除仅验证旧主入口、复制 Skill 内部正文、无生产调用者或已被 public wrapper/consumer
  contract 替代的 Finish-family tests/helpers/说明。
- 对每个疑似 dead surface 先证明生产引用为空或已由 canonical owner 替代；不得删除
  `finish-work.sh`、`publish-pr.sh` compatibility blocker、#105 recovery engine 或 #132
  ownership inventory 中仍需保留的 frozen legacy path。
- Durable requirements/specs/README 更新为 canonical Guru entry、compatibility boundary、
  combined evidence 和 #132 follow-up；task artifact 不成为长期 SSOT。

## 5. 非功能与 AI-first 约束

- Public DTO 维持 Interface 1.3 最小字段；没有直接 consumer 的字段不得新增。
- Git/GitHub/Trellis live facts、digest bundle、完整 review/transaction transcript 保持 private。
- Script 只做 executor/validator/recorder，不能决定 semantic readiness、scope、finding、
  route intent 或 Issue closure。
- 不新增 routine user handoff、implementation handoff、workspace journal、repo-level
  closeout/latest/cache/index。
- Secret、credential、private URL 和敏感原始记录不得进入日志、artifact、Issue 或 PR。

## 6. 正常运行边界

只覆盖 AI 与用户诚实协作下的正常路径、常见操作错误、stale/mismatch、current code
correctness/compatibility 和 Issue #105 明确 matrix。以下全部 out of scope，且不得成为
planning、Phase 2 或 Branch Review finding：

- 恶意 actor、伪造/篡改/欺骗、对抗输入或故意绕过流程；
- 并发 executor 竞态、TOCTOU、锁/原子写协议、分布式锁；
- 正文未要求的额外 fault injection、偶发 crash consistency、跨 OS 原子性；
- #116/#117/#118 Skill 内部重实现或重新审核；
- PR #160 task artifact migration；
- #132 全仓 upstream overlay cleanup、target repo cleanup 或 Issue closure；
- #108 Phase 2/Docs 减法、#106 merge executor/ruleset。

## 7. 验收标准

- [ ] Acceptance audit 中“已交付但未闭合/尚未完成”项全部有 current code、test 或 installation
      evidence，且没有把“已完成”项重新实现。
- [ ] Canonical/dogfood workflow 只保留 Finish-family 薄编排，13 exits 各有唯一 consumer。
- [ ] `guru-finish-work` 在 Codex/Claude/Cursor 可发现并只路由三个 active Skills；Shared
      通过同一 global workflow/Skill contracts 执行。
- [ ] Frozen legacy Finish overlays bytes 不变，兼容 inventory 明确保留到 #132；新
      Guru-owned entry 不改变 frozen 43-path identity。
- [ ] 八类 combined transcripts、六条关键 edges、13 exits closure、private ownership 和
      authoring partition 全部通过。
- [ ] #105 production test module 完整通过，且没有扩张 transaction/failure model。
- [ ] Clean install、workflow preview/switch、update、preset reapply、sidecar、dogfood drift、
      installed closeout initial/after-update 和四 adapter 验收通过。
- [ ] 重复/dead Finish-family surface 已删除或在 retained inventory 中给出唯一 owner 和
      保留理由。
- [ ] Durable Docs SSOT current；PR close scope 仅为 #119/#115，#132 只作 follow-up。

## 8. Docs 状态

当前为 `stale_docs`：durable specs、requirements 和 README 已描述 active Finish Skills，
但仍把 `trellis-finish-work` 当 canonical 主入口，并明确写着 #119 尚未 combined close。
本 task 采用 `ssot_first`；完整 Docs SSOT Plan 见 `design.md`。
