# #101 设计：change request readiness semantic closed loop

## 1. 设计目标

把 change request readiness 从旧 task-intake 内联 route 中抽出，形成 `guru-review-change-request` 独占的 step-local semantic SSOT。新 Skill 复用 #111、#113、#114 已产生且已验证的 evidence，不执行 discovery、clarification、wording scan 或 task creation。

## 2. 所有权模型

| 层 | 唯一职责 | 明确排除 |
| --- | --- | --- |
| Global workflow | mandatory invocation、五出口 consumer、fail-closed stop | review dimensions、finding 生成、schema 内部结构 |
| Canonical Skill package | entry contract、semantic review、route decision、finding、human confirmation policy、typed exits | base fetch、repo/history discovery、clarification loop、wording classification、workspace creation |
| Shared runtime | schema、hash、digest、linkage、prerequisite result check、record/check | readiness、reuse、delivery unit、implementation target、finding severity或 exit intent |
| #112 consumer | task workspace side effect 与 task-local `issue-review.json` persistence | #101 semantic review |
| Platform discovery copies | 发现并加载同一 public package | step-local contract 副本与平台专用 route |

## 3. Canonical package

新增目录：

```text
trellis/skills/guru-team/packages/guru-review-change-request/
├── SKILL.md
├── interface.json
├── references/contract.md
├── schemas/change-request-review.schema.json
├── examples/issue-review.json
├── scripts/record-change-request-review.sh
├── scripts/check-change-request-review.sh
└── tests/test_contract.py
```

`interface.json` 使用 `guru-team-skill-interface-1.2`，声明：

- `judgment_mode=semantic`；
- workflow/standalone entry preconditions 一致；
- stage order 为 `forward_behavior -> ai_review_gate -> conditional_human_confirmation -> recorder_validator -> typed_exit`；
- schema id 为 `guru-change-request-review-1.0`；
- artifact basename 为 `issue-review.json`；
- runtime commands 为 `record-change-request-review` 与 `check-change-request-review`；
- external exits 恰好为五项，且 consumer 固定。

Package scripts 只通过 `run-skill-command` dispatcher 调用 installed shared runtime。Public package 不携带 task runtime、workspace path、GitHub credential 或业务私有内容。

## 4. Entry contract

### 4.1 Workflow mode

Caller 传入同一 review round 的完整 evidence payload：

```text
context_ready result
  + requirements clear result
  + change_request wording pass result
  + target locator/current authority facts
  + AI-authored semantic review payload
```

Runtime 先调用现有 prerequisite check functions 验证每份 evidence 的 schema、typed exit、facts digest 与 freshness，再验证三者共同绑定同一 target/content identity。Runtime 不重新执行这些 Skills 的语义步骤。

### 4.2 Standalone mode

Standalone 与 workflow 使用同一 evidence contract。调用方缺少 evidence 时，AI 记录缺失项、finding、affected evidence 与 route reason，并返回 `refresh_context`、`clarify_requirements` 或 `review_wording` 中恰好一项。Standalone 不能合成 passing evidence，也不能降低 `ready` 条件。

### 4.3 Target variants

| kind | Identity | Current facts |
| --- | --- | --- |
| `existing_issue` | repo + issue number + URL | authority update time、title/body hashes、source facts digest |
| `proposed_draft` | reviewed draft id + source request digest | title/body hashes、draft content digest、side-effect-free state |
| `standalone_request` | explicit caller locator + request id | reviewed bytes hash、request digest |

三类 target 均归一为 `target.identity_sha256` 与 `target.content_sha256`。Context、clarity、wording refs 必须指向这两个 current identity；某类 evidence 不适用的 source field 使用 schema 中显式 `null`，不能省略 identity binding。

## 5. Evidence linkage 与 freshness

Result 的 `prerequisites` 固定包含：

- `context`: schema id、`context_ready`、facts/snapshot digest、base head、live target digest、current state digest、history digest、duplicate digest；
- `clarity`: schema id、`clear`、facts/result digest、target/content/scope digest；
- `wording`: schema id、`change_request`、`pass`、facts/scope/scan digest、target content digest。

`evidence_linkage` 记录统一投影：

```json
{
  "target_identity_sha256": "<sha256>",
  "target_content_sha256": "<sha256>",
  "base_head": "<git-sha>",
  "current_state_sha256": "<sha256>",
  "history_sha256": "<sha256>",
  "duplicate_sha256": "<sha256>",
  "clarity_facts_sha256": "<sha256>",
  "wording_facts_sha256": "<sha256>",
  "linkage_sha256": "<sha256>"
}
```

Checker 重建 objective projection 并比较 digest。以下 drift 阻止 `ready`：

- base/live target/scope/query/current/history identity 变化；
- context checker 不再返回 `context_ready`；
- clarity checker 不再返回 `clear` 或绑定不同 target/content/scope；
- wording checker 不再返回 `change_request:pass` 或绑定不同 target content；
- recorder result 与当前 prerequisite bytes 不一致。

Checker 只报告 objective error codes；AI 依据 Skill contract选择 typed exit。

## 6. Semantic review model

### 6.1 Fixed dimensions

`semantic_review.dimensions` 必须包含下列固定 ids，顺序固定：

1. `requirement_completeness`
2. `delivery_unit_consistency`
3. `implementation_target_evidence`
4. `claimed_behavior_current`
5. `current_implementation_gap`
6. `docs_code_tests_consistency`
7. `archived_history_constraints`
8. `duplicate_reuse_validity`
9. `target_authority_current`
10. `prerequisite_hash_linkage`

每项记录 `status`、summary、evidence refs、affected hashes 与 finding ids。`ready` 要求十项 status 均为 `passed`。Schema 和 checker 验证固定集合、顺序、引用闭合与 `ready` objective invariant；AI 独立判断每项是否 passed。

### 6.2 Findings

Finding 结构固定包含：

- `finding_id`
- `category`
- `summary`
- `blocking`
- `evidence_refs`
- `affected_hashes`
- `route_basis`

Category enum 覆盖 requirement gap、delivery conflict、wording gap、context stale、target complete、current/history conflict、duplicate/reuse conflict 与 prerequisite mismatch。该 enum 用于审计结构，不把 category 自动映射为 exit。AI Review Gate 负责 route basis 与最终 exit；runtime 只检查 enum、引用和 consumer。

### 6.3 Scope conclusion

`scope_conclusion` 固定记录：

- requirement/scope basis；
- delivery unit identity；
- `close_issues`、`related_issues`、`followup_issues`；
- duplicate/reuse decision；
- implementation target 与 current gap；
- archived constraints；
- risk boundary；
- excluded scope。

当前 #101 result 的 close projection 必须是 `[101]`。Package schema 不硬编码 issue number；task ledger 与 finish-work 在本任务中校验该 projection。

### 6.4 AI Review Gate

Gate 记录 reviewer、reviewed linkage digest、summary、findings count、scope conclusion digest 和 `status`：

- `passed` 对应 `ready`；
- `reroute` 对应三个 prerequisite exits；
- `blocked` 对应 terminal `blocked`。

Recorder 只接受 AI 已写完整的 Gate。Runtime 不从 zero errors、scanner return、prerequisite checker success 或 dimensions shape 自动生成 Gate status。

Human confirmation 只在 AI 提出会改变已确认 product semantics 的 scope proposal 时发生。该情形不能被 #101 吸收为 `ready`；Skill 返回 `clarify_requirements`，由 #113 拥有 exact proposal 与用户确认。正常 #101 pass 记录 `not_required`。

## 7. Typed exit 与 consumer

| Exit | AI route condition | Unique consumer |
| --- | --- | --- |
| `ready` | 十项通过、无 blocking finding、linkage current | Skill `guru-create-task-workspace` |
| `clarify_requirements` | 用户决策缺口、delivery 冲突、新 draft | Skill `guru-clarify-requirements` |
| `review_wording` | wording evidence 缺失、stale、unchecked、non-pass | Skill `guru-review-contract-wording` |
| `refresh_context` | base/live/scope/query/current/history stale | Skill `guru-sync-base` |
| `blocked` | 目标已完成且无独立缺口，或 delivery 冲突无法消解 | stop `change-request-review-blocked` |

Result 使用一个 scalar `typed_exit`。Schema closed object 拒绝额外 exit 字段；interface/workflow marker validator 拒绝 duplicate consumer、missing target、unknown exit 与 unmapped target。每个 exit 记录 findings 数组、reason、affected evidence/hash 和 exact consumer。

## 8. Artifact schema

`guru-change-request-review-1.0` 使用 closed JSON Schema Draft 2020-12，顶层结构：

```json
{
  "schema_version": "1.0",
  "skill_id": "guru-review-change-request",
  "generated_at": "<rfc3339>",
  "mode": "workflow",
  "target": {},
  "prerequisites": {},
  "evidence_linkage": {},
  "semantic_review": {
    "dimensions": [],
    "findings": [],
    "scope_conclusion": {},
    "ai_review_gate": {}
  },
  "human_confirmation": {},
  "typed_exit": "ready",
  "reason": "<ai-authored>",
  "affected_evidence": [],
  "consumer": {},
  "facts_sha256": "<sha256>"
}
```

Example 使用虚构 repo、issue、hash 与 finding 内容。Example 不指向本 task 或本机路径。

## 9. Runtime commands

Canonical runtime 新增：

```text
record-change-request-review
check-change-request-review
```

Recorder 输入包含 mode、target、三份 prerequisite payload 与 AI-authored payload。Pre-task 模式固定向 stdout 输出 JSON，禁止 `--output` 写 repo。Checker 接受完整 result 与同一 current prerequisite payload，返回验证 status、typed exit、linkage digest 与 facts digest。

Runtime helper 分层：

1. 解析 closed JSON 与 stable enums。
2. 调用既有 context/clarity/wording objective check functions。
3. 构造 target 与 prerequisite linkage projection。
4. 验证 fixed dimensions/findings refs/Gate shape/consumer mapping。
5. 派生 facts digest并检查 current bytes。
6. 返回已记录 typed exit。

Runtime 不调用 `gh issue list`、history reader 或 docs/code/tests search；不创建 task-local artifact；不选择 route。

## 10. Workflow integration

Canonical 与 dogfood workflow 变更：

```text
guru-review-contract-wording:change_request:pass
  -> guru-review-change-request

guru-review-change-request:ready
  -> guru-create-task-workspace
```

Workflow 新增一个 mandatory invoke marker、五个 exit markers和 terminal stop target。`guru-create-task-workspace` 尚未安装时，missing Skill gate 直接停止；旧 `guru-full-task-intake-chain` 不得作为 fallback。

`planning_artifacts:pass` 与 `explicit_paths:pass` route 保持不变。Context、clarity、wording non-pass route 保持各自 owner。

## 11. Replacement-first 删除顺序

1. 新增 package/schema/runtime/commands/tests，保留旧 route。
2. 通过 package、linkage、五出口与 runtime tests。
3. 接入 workflow 新 route 并通过 marker/consumer tests。
4. 验证 `ready` 到 missing #112 package 的 fail-closed 行为。
5. 删除 Guru-owned `change_request:pass -> guru-full-task-intake-chain` route 与 active docs 中重复 readiness owner。
6. Repo-wide search 区分 Guru-owned active source、archived task history 与 frozen upstream overlays。

以下内容不能因 #101 删除：

- #111 current/history discovery；
- #113 clarification/source action；
- #114 wording vocabulary/scanner/classification；
- #112 尚未替代的 environment/issue/worktree/task behavior；
- #128 inventory 中冻结的 upstream/transitional overlay；
- archived tasks 与 finish summaries。

## 12. Distribution 与 ownership

Preset installer 从 canonical registry 安装 package 到：

```text
.trellis/guru-team/skills/packages/guru-review-change-request/
.agents/skills/guru-review-change-request/
.codex/skills/guru-review-change-request/
.cursor/skills/guru-review-change-request/
.claude/skills/guru-review-change-request/
```

`.trellis/guru-team/extension.json` 和 `trellis/guru-team-extension.json` 同步 command、schema、artifact 与 managed-path public API。Installer inventory 与 tests 校验 bytes、mode、registry discovery 和 runtime dispatcher target。

本任务不增加 `trellis/presets/guru-team/overlays/**` 文件。Ownership gate 验证 43 个 frozen path 的 identity/payload 未变化，新增 managed paths 全部命中 anchored Guru-owned namespace。

## 13. Docs SSOT Plan

- Docs state: `stale_docs`
- Strategy: `ssot_first`
- Strategy reason: 本任务新增 public Skill、artifact schema、workflow transition 与 installer contract，长期行为必须进入 canonical/durable SSOT。
- Affected durable sources:
  - `trellis/skills/guru-team/packages/guru-review-change-request/references/contract.md`
  - `trellis/workflows/guru-team/workflow.md`
  - `.trellis/workflow.md`
  - `docs/requirements/requirement-main.md`
  - `docs/requirements/guru-team-trellis-flow.md`
  - `trellis/workflows/guru-team/README.md`
  - `trellis/presets/guru-team/README.md`
  - `.trellis/spec/workflow/skill-package-contract.md`
  - `.trellis/spec/workflow/workflow-contract.md`
  - `.trellis/spec/workflow/data-contracts.md`
  - `.trellis/spec/workflow/companion-scripts.md`
  - `.trellis/spec/workflow/quality-guidelines.md`
  - `.trellis/spec/preset/installer.md`
  - `.trellis/spec/preset/overlay-guidelines.md`
  - `.trellis/spec/preset/upstream-ownership.md`
- Task delta merge: package boundary、input linkage、ten dimensions、five exits、side-effect-free lifecycle、#112 placeholder、replacement 与 verification matrix 写回 durable sources。
- Task history only: Phase 0 临时 stdout evidence、issue search 输出、每轮测试日志、agent handoff 和 review raw reports。
- Merge checkpoint: implement agent 完成 canonical/runtime 后同步 durable docs；Phase 2 final round 和 Branch Review 各执行一次 Docs SSOT reconciliation。

## 14. 验证设计

### Package 与 schema

- frontmatter/interface/registry/stage profile/runtime dependency；
- schema closed shape、stable ids、artifact basename、example validation；
- workflow/standalone preconditions 一致；
- five exits 与 unique consumers；
- missing/unknown/multiple/unmapped exit rejection。

### Linkage 与 semantic boundary

- three target variants positive path；
- context/clarity/wording current linkage positive path；
- each prerequisite missing/stale/wrong exit/wrong target/wrong content hash；
- base/current/history/duplicate digest drift；
- Gate missing、dimension missing、finding ref broken、consumer mismatch；
- scanner/validator success 加空 AI Gate 时仍 fail closed；
- AI-authored exit 被 checker原样验证，不被 runtime 改写。

### Side effect 与 replacement

- pre-task/standalone recorder 后 Git status 与 tracked/untracked set 不变；
- 不产生 `issue-review.json`、cache、index、`.new`、`.bak`；
- wording pass route 进入 #101；
- ready route 指向 #112 stable id；
- #112 package missing 时 fail closed；
- old full-intake readiness route 消失，prerequisite 与 #112 behavior 仍存在；
- upstream ownership frozen identity 不变。

### Distribution

- source/installed package suites；
- canonical/installed/four-platform byte + mode equality；
- preset apply 与 dogfood drift；
- clean throwaway workflow marketplace + preset install；
- `trellis update --force` + workflow switch + preset reapply；
- sidecar/removal/conflict zero audit；
- pushed branch remote marketplace verification。

## 15. 安全、部署与回滚

- 不涉及 production secret、CI/CD pipeline、container image、Kubernetes object、DB migration、Makefile target 或服务部署。
- Evidence 只记录 issue/draft/request 审查所需摘要、hash 与去敏 finding；日志和 PR 禁止出现 token、private key、`.env`、database URL、signed URL 或客户原始数据。
- Pre-task side-effect-free 是 correctness boundary，不是 adversarial authenticity boundary。
- Commit 前若 replacement tests 失败，保留旧 route 并修订新链路；最终分支禁止双 active readiness owner。
- Commit 后回滚通过 PR revert 恢复 pre-#101 状态；不引入 runtime feature flag 或长期双路。
