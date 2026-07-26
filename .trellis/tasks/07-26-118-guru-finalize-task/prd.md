# #118 实现 guru-finalize-task 事务闭环 Skill

## 1. 目标

交付公共 closed-loop Skill `guru-finalize-task`。该 Skill 使用
`judgment_mode=semantic`，独占 task finalization 的语义判断、精确副作用确认、
immutable closeout plan、单一 draft PR、archive metadata transaction、三方 HEAD
一致校验、draft-to-ready 与正文封闭 recovery state machine。

本 task 只关闭 Issue #118。Issue #115 保持 related，Issue #119 继续持有 Finish
family 的全局 workflow/platform 集成与 #115 关闭职责，Issue #132 继续持有 upstream
overlay 清理职责。

## 2. Authority

- `AUTH-118-BODY`：<https://github.com/castbox/guru-trellis/issues/118>
- `AUTH-118-CURRENT`：<https://github.com/castbox/guru-trellis/issues/118#issuecomment-5045036678>
- `AUTH-AGENTS`：仓库根目录 `AGENTS.md`
- `AUTH-TRELLIS-DOCS`：Trellis 官方 `index.md`、`custom-workflow.md`、
  `custom-skills.md`、`custom-spec-template-marketplace.md`
- `AUTH-SKILL-CONTRACT`：`.trellis/spec/workflow/skill-package-contract.md`
- `AUTH-WORKFLOW-CONTRACT`：`.trellis/spec/workflow/workflow-contract.md`
- `AUTH-116`：`guru-review-task-publication` current Interface 1.3 package
- `AUTH-117`：`guru-verify-extension-installation` current Interface 1.3 package
- `AUTH-105-RUNTIME`：current `guru_team_trellis.py` closeout engine 与对应测试

## 3. 需求

### R1. 公共 Skill 与 ownership

`guru-finalize-task` 必须拥有完整 semantic profile：正向行为、AI Review Gate、命中
条件时的 human confirmation、recorder/validator、单一 typed exit。AI 必须判断 plan、
scope、readiness、recovery route、finding、revision action 与 confirmation 充分性。

### R2. 单一事务引擎

现有 #105 closeout engine 必须成为新 Skill 的唯一 deterministic substrate。实现必须
保持 immutable plan、content push、verification boundary、唯一 draft PR、final
projection、单次 archive metadata transaction、三方 HEAD 一致与 draft-to-ready 的
事务顺序。旧 compatibility 调用与新 package scripts 必须复用同一内部引擎，禁止形成
第二套 closeout 实现。

### R3. Script 边界

Python 与 shell 仅承担 executor、validator、recorder。脚本禁止决定 close scope、plan
充分性、publication readiness、recovery route、PR body 充分性、Docs SSOT、安全结论、
部署结论或 semantic pass。

### R4. 精确 preview 与确认

第一次副作用前，Skill 必须完成 side-effect-free preview，展示 repo、base、HEAD、task、
archive locator、upstream evidence refs、verification requirement、metadata paths、PR
identity strategy、plan digest 与全部副作用。AI 必须审核 immutable plan；human 必须确认
精确 `closeout_plan_digest`。Formal 执行必须重建相同 bytes 与 digest，任何 mismatch
必须在副作用前阻断。

### R5. Distinct public input profiles

Public input 必须采用 Interface 1.3 closed structured profiles，分别承接 publication
entry、`verified` re-entry、`not_required` re-entry、same-plan resume、cross-month
reprepare 与 standalone finalization。每个 profile 必须只携带当前入口直接消费的最小
字段，禁止传入 private artifact body、digest bundle、PR/archive facts 或 transaction state。

### R6. Upstream DTO consumption

Publication entry 必须消费 #116 `ready(exit_id, task_ref, reviewed_head,
publication_ref)` 的业务 seed。Verification re-entry 必须分别消费 #117
`verified(exit_id, task_ref, plan_ref, reviewed_head, verification_ref)` 与
`not_required(exit_id, task_ref, plan_ref, reviewed_head)` 的业务 seed。Target-owned
authoring fields 必须与 producer seed 不重叠，runtime 禁止合成 AI intent/context。

### R7. 六个 public exits

Skill 必须只发布以下六个 external exits，discriminator 统一为 `exit_id`：

- `verification_required`
- `publication_review_stale`
- `resume_finalization`
- `reprepare_required`
- `published`
- `blocked`

每个 exit 必须拥有独立 closed schema、完整 example、唯一 consumer input 与薄
deterministic projection。Unknown、missing、multiple、unmapped 或 consumer mismatch
必须 fail closed。

### R8. Reprepare authoring seed

`reprepare_required` 的 self re-entry 必须使用 target-owned
`skill_input_authoring_seed`。Producer seed 必须精确为 `task_ref`、`reason_code`；target
authoring fields 必须精确承接 fresh reprepare intent/context 与 target discriminators。
两组字段必须互斥，union 必须覆盖 target profile 全部 required fields，merge 必须禁止
overwrite。

### R9. Private state

`closeout-plan.json`、publication readiness、verification evidence、PR identity、archive
facts、recovery facts、path/blob/HEAD/digest facts 与内部状态必须保持 owner-private。
`prepared`、`content_pushed`、`evidence_pushed`、`draft_bound`、
`projection_validated`、`archive_moved`、`archive_pushed` 禁止出现在公共 Skill id、
public DTO、workflow exit 或用户命令中。仓库级 closeout state/index/cache 禁止新增。

### R10. Verification boundary

Verification requirement 必须在 reviewed content push 之后、PR create 与 archive 之前
产生。Finalizer 必须通过 #117 owner checker 验证同一 plan/ref/HEAD 的 current evidence，
禁止重新解释 verifier 语义，禁止在 archive 后通用重验 private artifact。

### R11. PR、archive 与 recovery

Draft PR 必须绑定同 repo/head/base 的唯一 open draft identity。Final summary 必须在取得
真实 PR number/URL 后生成一次。Archive 必须调用未修改的官方
`task.py archive --no-commit`，并只提交 exact task metadata transaction。Ready 前必须
验证 local HEAD、remote branch HEAD、draft PR head SHA 三方一致。正文列出的 prepare、
push、verification、evidence、draft、projection、archive、remote HEAD、ready、cross-month、
active/archived/exact-commit recovery matrix 必须完整继承。

### R12. Production eval

Package-local production eval 必须执行真实 public wrapper。Semantic case 必须引用
repo-local checker-passed owner result；adapter 必须先从实际返回选择 per-exit schema，
随后断言 `expected_exit`。`expected_exit` 禁止进入 adapter/native request。Corpus 必须覆盖
六个 exits，以及 publication、verification、same-plan resume、cross-month reprepare、
published recovery 与 blocked 路径。

### R13. 四平台一致

Shared、Codex、Claude、Cursor corpus 必须 byte-identical。验证必须覆盖 Codex trusted Git
root、Claude input protocol、Cursor unsupported/unavailable 与 shared adapter parsing。

### R14. Canonical、dogfood 与安装

Canonical package、Guru runtime assets、schemas、examples、tests、registry/manifest 与
additive distribution 必须一致。修改 canonical 后必须同步 dogfood package 与声明平台
discovery copies，运行 preset apply 与 overlay drift。Clean throwaway 验证必须覆盖
workflow marketplace、preset install/reapply、Trellis update、managed hash、`.new/.bak`、
四平台分发、命令权限、contract discovery、public wrapper 与开箱运行。

### R15. Issue 与集成边界

本 task 禁止修改或 overlay upstream `trellis-finish-work` Skill、Command、Prompt、Agent、
Hook 或官方 `task.py`。本 task 禁止承接 #119 的 Finish family 全局 entry/order、combined
acceptance、#115 closure，禁止承接 #132 的 upstream overlay 删除。#105 事务语义必须保持
completed 且不执行 Issue mutation。

### R16. 正常运行边界

验收只覆盖 issue 正文列明的正常路径、常见操作失误、correctness/compatibility 边界与
封闭 failure/recovery matrix。恶意 actor、伪造 artifact、攻击模型、并发 finalizer、锁、
TOCTOU、新 fault injection、偶发 crash consistency、跨 OS 原子性均为 out of scope。

## 4. 验收标准

- [ ] AC1：Canonical package 以 `guru-finalize-task` 暴露 semantic five-stage profile，
  package contract 与 Interface 1.3 validator 全部通过。
- [ ] AC2：六个 input profiles、六个 output schemas、examples、consumer inputs、
  projections 与 private artifact declarations 通过 closed-contract validation。
- [ ] AC3：#116 `ready` 与 #117 `verified|not_required` 仅投影最小 seed，target-owned
  authoring merge 无 overlap、overwrite、missing 或 extra field。
- [ ] AC4：`reprepare_required` producer seed 仅含 `task_ref`、`reason_code`，fresh AI
  intent/context 仅来自 target authoring example。
- [ ] AC5：Dry-run 与 formal 生成相同 plan bytes/digest；formal drift 在任何副作用前
  fail closed；exact confirmation 与 digest binding 有自动测试。
- [ ] AC6：Verification exit 严格发生在 content push 后、PR/archive 前；current verified
  或 not-required re-entry 只接受 same plan/ref/HEAD。
- [ ] AC7：唯一 draft、final summary 一次生成、exact archive transaction、三方 HEAD
  一致、ready 后零 commit 均由 production transaction tests 证明。
- [ ] AC8：#105 全 failure/recovery matrix、2026-07-03、2026-07-04 与 #100 regression
  全部通过，旧 compatibility observable behavior 无回归。
- [ ] AC9：Production eval 真实执行 wrapper，actual-exit schema selection 先于
  `expected_exit` assertion；六 exits 与六条业务路径全部命中。
- [ ] AC10：Shared/Codex/Claude/Cursor corpus byte-identical，四个平台专属协议测试全部
  通过。
- [ ] AC11：Canonical、installed shared、Codex、Claude、Cursor package bytes 一致，
  scripts executable，contract discovery 返回新 package 的完整 public/private index。
- [ ] AC12：Preset apply、dogfood overlay drift、clean throwaway workflow marketplace、
  preset install/reapply、update、managed hash、`.new/.bak` 与开箱验证全部通过。
- [ ] AC13：Diff 不修改 upstream Finish family assets，不修改官方 `task.py`，不包含
  #119/#132 owned integration 或 excluded unusual-scenario mechanism。
- [ ] AC14：Issue Scope Ledger 只把 #118 放入 `close_issues`；PR body 只写
  `Closes #118`，#115/#119/#132 只使用非关闭语义。

## 5. Docs 状态与需求影响

当前 durable docs 已描述 #105 deterministic transaction、Interface 1.3、#116 与 #117，
但仍把 `guru-finalize-task` 标记为 planned/future owner。实现必须把公共 package contract、
ownership、I/O、production eval 与安装状态写入 durable SSOT。全局 Finish family 路由与
upstream overlay 状态保持未集成，并明确指向 #119/#132。唯一完整 Docs SSOT Plan 位于
`design.md` 的“Docs SSOT Plan”章节。

## 6. 非目标

- 不关闭 #115、#119、#132、#81 或 #105。
- 不改写 #116 publication review 与 #117 verification 的 semantic ownership。
- 不把 global Finish family entry/order 或 combined acceptance 并入本 task。
- 不修改 upstream/global npm/`node_modules`/官方 `task.py`。
- 不新增内部 transition 对应的公共 Skill、命令或 DTO。
- 不引入本 Issue 未列明的异常、威胁、并发或原子性机制。
