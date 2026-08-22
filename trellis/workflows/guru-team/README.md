# Guru Team Trellis Workflow

## GitHub CLI-only contract

Guru Team uses authenticated GitHub CLI as the only GitHub platform channel.
Use `gh issue`, `gh pr`, and `gh run` with explicit `--repo owner/repo`; use
`gh api repos/<owner>/<repo>/...` when no high-level command covers the needed
fields. This covers Issue/PR create/read/edit/comment/labels/state, checks,
reviews, mergeability, Draft/Ready, merge, workflow run/check, and post-merge
status verification. There is no GitHub App, MCP, connector, or browser UI
fallback. Local Git and Git transport remain `git` operations.

本目录维护 Guru 团队可复用的 Trellis workflow。

这个 workflow 的 marketplace id 固定为通用的 `guru-team`。它只承载 global
phase/status route、20 个 mandatory Skill invocation、87 个 typed exit、33 个 workflow
target 与 21 个 stop target，以及 workspace、Docs SSOT、Issue Scope Ledger、human artifact、
interaction 和外部 side-effect boundary。具体 intake、planning、check、review、
publication 与 finalization 判断由对应 active package 独占。

Guru Team extension 版本不等于官方 Trellis CLI 版本，也不等于 `trellis/index.json`
里的 marketplace index schema version。canonical extension version 和目标官方
Trellis CLI 版本位于 `trellis/guru-team-extension.json`；preset installer 会把当前安装版本和 source
provenance 写入目标仓库的 `.trellis/guru-team/extension.json`，并通过
`check-env --json` / `version.sh --json` 暴露给用户和 AI 排障流程。

## Marketplace 安装

```bash
trellis init -y --claude --codex --cursor \
  --workflow guru-team \
  --workflow-source gh:castbox/guru-trellis/trellis#v0.6.5-guru.10
```

`-y` 是团队默认安装路径的一部分，用于跳过交互式 spec template picker。自动验收、
throwaway 安装验证和 README 默认命令都必须使用非交互形式；只有用户明确想手动选择
spec template 时，才去掉 `-y` 或改用官方支持的 `--template <name>`。

稳定安装 source 使用 repo release tag `#v0.6.5-guru.10`，并要求官方 Trellis CLI 安装到
`0.6.5`。维护者刻意跟随最新 `main` / canary 时可以去掉 `#ref` 或改用其它 branch/tag ref，
但应在验证和排障报告中说明 source 是否为 mutable ref，以及是否仍以官方 Trellis `0.6.5`
为目标基线。Guru Team release tag 使用 repo 级 `v<official-trellis-version>-guru.<revision>`，
并与该 tag 所指提交中的 `trellis/guru-team-extension.json.version` 精确映射。本次 stable
source 是 annotated tag `v0.6.5-guru.10`，canonical extension version 为
`0.6.5-guru.36`；tag object 为 `b5fd47e9dc45ca4d6950f87f38d495776ce676ce`，
peeled source commit 为 `5c059f4943edad7dfe25182a78af94759d41f9a1`。对应 GitHub
Release 是 non-draft、non-prerelease、zero-asset release。Repo release tag 与 extension
revision 是独立版本轴；workflow marketplace 与 preset 必须来自同一个 immutable tag。

当前 `main` candidate 为 extension `0.6.5-guru.37` / official Trellis `0.6.15`，已通过
live-derived 六-cell compatibility matrix、installed contracts 和 A/B lifecycle proof；
evidence classification 是 `public_plus_local_candidate`。它不是 stable source，`.37`
tag、GitHub Release、tag-pinned install 与 release smoke 仍由 #267 独占。

已有 Trellis 项目切换 active workflow：

```bash
trellis workflow \
  --marketplace gh:castbox/guru-trellis/trellis#v0.6.5-guru.10 \
  --template guru-team
```

只有在需要生成 `.trellis/workflow.md.new` 做人工 review、且不切换 active
workflow 时，才使用 `--create-new`。

## Companion Assets

Workflow marketplace 只安装 global .trellis/workflow.md；完整 Guru Team extension
由 preset 安装。公共 Skill 唯一 canonical root 是 trellis/skills/guru-team/，
installed 与 Shared/Codex/Claude/Cursor discovery copies 都是 managed projection，
不能反向成为语义来源。

当前 registry 激活 21 Skills / 89 package exits；其中业务 global workflow closure
为 20 个 invokes / 87 个 exits / 54 个 total targets。下列 20 个业务 active ids 参与
global workflow：

- guru-bootstrap-repository-ssot
- guru-maintain-architecture-baseline
- guru-maintain-requirements-design-test-ssot
- guru-select-workflow-mode
- guru-execute-task-free-change
- guru-qualify-normal-scenario
- guru-sync-base
- guru-discover-change-context
- guru-clarify-requirements
- guru-review-contract-wording
- guru-review-change-request
- guru-create-task-workspace
- guru-approve-task-plan
- guru-reconcile-task-base
- guru-check-task
- guru-create-task-commit
- guru-review-branch
- guru-review-task-publication
- guru-finalize-task
- guru-merge-task-pr

`guru-verify-extension-installation` 是唯一不拥有 global
workflow marker。它只接受 clean `castbox/guru-trellis` source checkout 中显式发起的
`source_repository_verification` standalone 调用，并只返回 `verified|blocked`。

Global workflow 只写 phase/status route、mandatory invoke marker、typed exit、唯一
consumer/stop 与全局边界。每个 package interface.json 独占 public input、per-exit
output、consumer input、thin projection、target-owned authoring partition 与 package
内部行为；workflow、README 和平台入口不得从 runtime implementation 或 package
artifact 重建路由。

Active task 的 base 演进统一由 `guru-reconcile-task-base` package 与
`guru-base-reconciliation-router` 承接。Planning approval、Phase 2 pass、Task Commit、
Branch Review pass、Publication ready 与 Finalizer base-only mismatch 六类稳定边界先执行
同一 deterministic pair guard：unchanged pair 直接恢复原 `resume_target`；new pair 才调用
semantic owner。六个 Gate exits 分别恢复原 route、进入 bounded Branch Review continuity、
返回 implementation、返回 Planning、进入 requirement clarification 或 fail closed。Base SHA
变化本身不使 authority、task-content review 或 Publication metadata stale；Finalizer 的
`base_reconciliation_required` 与 `publication_review_stale` 是两个独立合同。

每个 standard task 还必须在 Planning、qualified implementation discovery
boundary expansion、Phase 2、committed full-diff Branch Review、Publication 与
Acceptance/Finish 六个阶段重新调用
`guru-maintain-architecture-baseline:task_impact_sync`。Planning 缺 current
Architecture Baseline、design constitution 或 project change-contract 结果不能批准；
scope/risk/owner/state authority/persistence/SDK/external/architecture boundary 扩大使
旧结果 stale。Phase 2 首次判断 candidate before/after，Branch Review 必须从完整 committed
diff 独立重算，不能复用 Phase 2。Publication 拒绝 missing/stale/conflict/incomplete/
fitness regression/unpromoted state；Finish 只接受 current `no_change` 或
`reviewed_promoted`。Promotion diff 必须重新进入 Phase 2、Task Commit 与 Branch Review，
baseline advance 固定返回 `sync_required`。Global workflow 只拥有这些 stage router；
Publication 与 Finalizer 的业务语义仍由各自 package 独占。

新 Skill 必须引用 installed `.trellis/spec/workflow/semantic-retrieval.md`，不得在 workflow、
README、平台 entry 或 package 中复制中英文概念族。完整 runtime、schema、commands、tests 与
Shared/Codex/Claude/Cursor discovery copies 由 preset 根据 current registry 原子安装。升级顺序
仍是 official update/upgrade、workflow re-selection、same-ref preset reapply、sidecar 处理和
完整 source/installed/platform/drift 验证。

guru-review-branch 是 sole Phase 3.5 semantic owner。Branch Review passed 后，
workflow mandatory invoke guru-review-task-publication；Publication owner 直接从 live
authority 生成并审查 exact Chinese PR title/body。其 ready 4.0 DTO 无损投影 payload，
只有 ready 进入 guru-finalize-task。Finalizer 的 stale、resume 与 reprepare exits
按 Interface 自动路由，不形成新的用户 continuation gate；业务 Finalizer 不调用、投影或
读取 extension verifier。

Finalizer `ready_for_merge` 只证明唯一 PR 已 Ready、expected head 对齐且 close Issues
仍 Open；它不是 finish。Workflow 随即 mandatory invoke `guru-merge-task-pr`。Merge owner
在 target-owned active 2.0 input 中补充并审查中文摘要、primary Issue 和精确
`chore(merge)` subject/body；Finalizer public output 不扩张。随后用 repo-bound `gh`
重建 checks/reviews/mergeability/policy/close-keyword facts，独立展示并确认
expected-head merge，并传递 `--subject/--body-file`；执行后只读验证 PR=MERGED、
双 parent、subject/body、remote base 以及 Issues 由 GitHub 自动关闭。`merged` 才进入
finish response；`merge_blocked` 与 `closure_mismatch` 分别 fail closed，任何 Guru 命令都不
调用 Issue-close API、update PR branch、同步本地 `main` 或清理资源。

Finalizer stale DTO 只增加 Publication 唯一 consumer 直接使用的
`branch_review_commit`；真实 descendant content
drift 只能由 Publication 语义门禁返回现有 Phase 2 router，不能产生 `ready`。

Interface 1.4 的十三条 semantic package handoff 使用 target-owned
skill_input_authoring_seed；producer 只给 minimal seed，target authoring 补齐其自己拥有
的 fresh semantic input，projection 只允许 direct/select/rename/normalize。
`production-current-v4` 是唯一 current manifest，固定绑定 planning/check/commit 与
normal-scenario qualification 四包、20 profiles、15 exits、四条 authoring-seed edges
及 160 x 5 production control。v2/v3 仅作为 immutable legacy assets 保留，不参与
current discovery、invocation 或安装选择。

workflow mode 表示 mandatory global route；standalone 表示平台直接发现。两种模式都
依赖完整、current Guru Team preset，单独复制 Skill 目录不是
self-contained/portable 安装。公共 wrapper 通过 installed executable
.trellis/guru-team/scripts/bash/run-skill-command.sh 调用 shared run-skill-command
dispatcher；canonical validator/discovery/eval/compat wrapper 使用 source checkout 的
`trellis/skills/guru-team/runtime/resolve-python.sh`，installed wrapper 使用目标 checkout 的
`.trellis/guru-team/runtime/resolve-python.sh`。缺 runtime、版本漂移或未解决 sidecar 时必须在
业务副作用前 fail closed，不得回退 PATH Python。

当前 source candidate 的 canonical extension version 为 `0.6.5-guru.37`；上文 pin 的
stable release tag `v0.6.5-guru.10` 仍对应 extension revision `0.6.5-guru.36`。
Source/installed package validation 必须同时验证
registry、20 invokes / 87 exits / 54 combined targets（33 workflow + 21 stop）
business marker graph、21-package/89-exit closure、consumer
uniqueness、projection、selected-platform
byte identity 和 executable mode。

## Workflow Authoring Ownership

Canonical workflow 是 trellis/workflows/guru-team/workflow.md；dogfood
.trellis/workflow.md 必须 byte-identical。Global Markdown 只拥有 phase order、
current-task router、20 mandatory Skill markers、87 exits、33 workflow targets、
21 stop targets、
workspace/task activation、Docs SSOT、Issue Scope Ledger、human artifact、
interaction 与外部 side-effect boundary。Step-local 合同只存在于对应 active
package/interface。

Official Trellis 独占 trellis-start、trellis-continue、trellis-finish-work、官方
hooks、sub-agents、runtime agents、bundled skills 与 meta references。Guru preset
不安装、不 patch、不 managed-upgrade 这些路径；mandatory Guru routing 由 active
workflow markers 和 installed guru-* packages 保证。

Preset overlay tree 只保留三个 Guru-owned explicit entry：

- .codex/prompts/guru-finish-work.md
- .claude/commands/guru/finish-work.md
- .cursor/commands/guru-finish-work.md

这些 entry 只读取 live context 和 .trellis/workflow.md、调用 public Skills、消费
mapped exits，并返回 terminal result。它们不读取 producer-private runtime/artifact，
不复制 package input fields、review dimensions、interaction algorithm 或 executor
commands。

Current-only ownership schema 3.0 固定为 11 条 anchored Guru-owned rules、9 条
managed claims 和上述 3 个 additive overlays，只记录 current Guru-owned assets；
非 current ownership/installed manifest 在 mutation 前统一
fail closed，不存在 projection 或迁移入口。当前完整升级/更新顺序为：

1. 在 disposable npm prefix/container 中执行 `trellis upgrade --tag latest`，核验
   upgrade 前后 CLI version，绝不修改开发机 global npm；
2. 在目标 throwaway project 执行 `trellis update --dry-run`；只有输出明确包含
   `MIGRATION REQUIRED` 时执行 `trellis update --migrate --skip-all`，否则执行
   `trellis update --skip-all`；`--skip-all` 保留已有修改并非交互继续，两条 live
   update 命令不得同时试跑后挑选结果；
3. 用 `--create-new` preview 并重新选择 guru-team marketplace workflow；
4. reapply canonical Guru preset；
5. 处理所有 .new/.bak 与 local-edit conflict；
6. 运行 source/installed package、ownership、platform identity、dogfood drift 与
   recursive zero-sidecar checks。

维护者在 preset mutation 和 combined acceptance 中运行：

    trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json

该 validator 只检查客观 ownership facts，不进入 workflow route，也不替代 AI
semantic judgment。

## Normal Scenario Qualification

Public closed-loop Skill `guru-qualify-normal-scenario` 是新场景资格的唯一语义
Owner。Global workflow 只按 stable id 在
`task_free_pre_write|task_free_evolution|requirements_scope_set|change_request_candidate_set|planning_scenario_set|implementation_discovery|base_impact_candidate_set|phase2_candidate_set|branch_review_candidate_set|publication_candidate_set`
十个 profile 的精确边界 mandatory invoke，并消费四个 exits：

- `classified` -> `guru-normal-scenario-classified-router` -> 原 profile Owner；
- `scope_confirmation_required` ->
  `guru-clarify-requirements:normal_scenario_scope_confirmation`；
- `mechanism_revision_required` ->
  `guru-normal-scenario-mechanism-router` -> 原 Owner remove/replace 后 fresh rerun；
- `blocked` -> `normal-scenario-qualification-blocked`。

Guru caller 只把 worker 结果投影为 invocation-local candidate refs、行为观察、locator
与最小复现线索；每次 worker dispatch 只授权 approved-plan work，planning-external
candidate 在资格完成前不 edit、不补 test、不 self-fix、不赋 severity，也不形成
finding/route。官方 `trellis-*` agent bytes 保持 upstream-owned。Skill decision 与 typed
result 只存在当前 process memory/stdout，不生成 tracked/ignored qualification
result、report、checkpoint、candidate ledger、handoff 或跨进程 locator。Phase 2、Branch
Review、Publication 只在各自既有 owner-private gate 中直接记录其 direct consumer 所需
的最终 terminal classification/witness，不引用 Skill artifact。

Production eval 资产通过 clean-installed public entry 覆盖全部十 profiles，并将 #113
F-001 与 #236 攻击式 scanner 变体同 paired legitimate cases 一起覆盖。Deterministic
release validation 验证 corpus、runner、真实 wrapper、sandbox 与 no-model/fake production
path，不执行 live GPT-5.6 Sol matrix。只有另行完成且绑定 exact
model/prompt/package/matrix 的 live run 才能形成模型行为证据；没有该证据时 Issue、PR、
README 与 release-facing text 均不得声称 pressure matrix 或模型稳定性已经通过，也不
承诺未来永不复发。

本发布未取得 live GPT-5.6 Sol production semantic evidence；deterministic/no-model/
fake-production 结果不能证明 pressure matrix、模型稳定性或未来模型行为。

## Phase 0 Public Transition And Invocation

Phase 0 由六个 mandatory Skills 和 23 个既有 typed exits 构成。正常 forward path 使用
workflow-owned 的五个独立 closed stages：

```text
guru-sync-base -> base_current -> guru-discover-change-context
-> context_current -> guru-clarify-requirements
-> clarity_current -> guru-review-contract-wording
-> wording_current -> guru-review-change-request
-> readiness_current -> guru-create-task-workspace
```

每个 stage 只携带下一 consumer 无法从 live authority 重建的最小 identity/freshness。
Semantic wrapper 通过 `--invocation -` 的 versioned call-local envelope 分开接收 public
input、当前 transition 和本 Skill owner result；owner result 经当前 recorder/checker 复验后消费，不进入下一
stage。正常 pre-task 只使用 stdin/stdout 或 caller memory，在 workspace/task creation 前不写
owner-result、prerequisite、transition、task、workspace 或 ignored-runtime repo 文件。Agent
不读取或 import package-private runtime 来组装输入；它只使用 public projection、command
discovery 与准确 `--help`。

`guru-sync-base` public wrapper 是唯一 authoritative sync。Workflow、platform entry 和 Skill
Markdown 不先执行低层 resolve/execute/check；refresh 丢弃 stale transition 后重新调用一次完整
public Skill。`prepare-task` 仅是 compatibility local diagnostic，不产生 transition，也不进入
正常 Phase 0 路由。任一 missing/stale/cross-stage transition、unknown/multiple/unmapped exit 或
consumer mismatch 都 fail closed。

既有 closed 1.0 public schema/example 保留原路径、`$id` 与 bytes。任何新增 required
transition/provenance field 都使用新的 versioned contract path，由 current Interface 选择；旧
DTO 无法建立 current identity 时重跑 producer，不执行 ambient-field synthesis。

## Phase 0 Base Sync

Tool-free request classification 后，repo-changing route 的第一个 mandatory invocation
是 `guru-sync-base`。它按显式 `--base`、非空 scalar `base_branch`、配置顺序中第一个
existing `base_branch_candidates` ref（缺省 `dev -> develop -> main -> master`）、候选均
不存在时的 remote default 解析 selected base；current branch 不是隐式 fallback。多个
existing candidates 不歧义，配置顺序就是优先级。Deterministic executor 以 pre-sync
resolution digest 绑定重新解析、fetch 与可选 `git merge --ff-only`，同步后生成
`post_sync_resolution` / `post_sync_resolution_sha256`。

上述 resolver、executor 和 checker 只作为 public wrapper 内部 deterministic components 或
focused diagnostic/test entry 使用，正常 workflow 不直接编排它们。`synced` 输出的
`base_current` 保留 source、selected base、remote、ordered candidates、decision HEAD、
local/remote base HEAD 和 post-sync digest；这些角色不得折叠为一个通用 `base_head`。
它是 Sync 唯一 public transition，完整 private result 与 facts digest 只在 Sync owner 内
由 checker 和 public wrapper 消费，下游不得重建。

成功结果使用 `guru-base-sync-result-1.0`，并且必须证明 checkout clean、decision checkout
HEAD、local base HEAD 与 remote-tracking HEAD 三方相等。`sync-base` 在 stdout 输出
resolution/result facts，`check-base-sync --result-json` 校验 schema、pre/post digest 与 live
Git facts，并由 public wrapper 把 source-preserving provenance 投影给下一 consumer；二者不创建 evidence file。该 package
声明 `judgment_mode=deterministic`，没有
selected-base AI confirmation、post-execution AI Review Gate 或 human confirmation；AI 只在
Skill 外负责 tool-free route classification。Stable exits 与唯一 consumers 是：

- `synced` -> `guru-discover-change-context`
- `skipped` -> `original-request-route`
- `blocked` -> `base-sync-blocked`

Workflow mode 中 `synced` 的唯一 consumer 是 `guru-discover-change-context`；
`check-env` 是独立环境诊断；`prepare-task` 只允许显式 compatibility query，不是 workflow
hop。它必须接收同一 reviewed provenance；缺失时在 GitHub read、fetch 或 semantic Intake 前
本地阻断。Remote ref 缺失是否可接受由正式 closed schema/runtime 状态矩阵决定，caller 不得
合成 remote HEAD。Standalone mode 可由所选平台直接发现
同一 Skill，但仍要求完整 compatible preset/runtime；workflow-only
`--record-skipped original-request-route` 不可在 standalone 调用。Managed executable commands 位于
`.trellis/guru-team/scripts/bash/sync-base.sh` 和
`.trellis/guru-team/scripts/bash/check-base-sync.sh`。

## Phase 0 Change Context Discovery

`guru-sync-base:synced` mandatory invoke semantic
`guru-discover-change-context`。Workflow/standalone entry preconditions 完全一致；Skill
固定先读 live change 与 duplicate facts，再 AI review updated-base Docs、
code/API/config/schema/ownership 和 tests/fixtures/throwaway/update，之后形成 canonical
query，执行一次 archived history preview，并由 AI 选择 1 至 3 个 candidates 窄读和完成
AI Review Gate。零候选是成功路径，固定 empty selection/deep reads 与一致的
`mem_review=not_needed` shape，且不得触发其它历史源；duplicate reuse/new target 决策不在本 Skill 内。

History runtime 只枚举 archived `finish-summary.json` 并只投影 `index.*`，使用
`guru-context-history-score-1.0` 产生稳定 query、archive manifest 和 preview digest、
invalid isolation、固定 sort/limit/projection。`trellis mem` 只有四类主证据源都不足以
解释命名 load-bearing decision 时才进入。完整 semantic evidence 保留在当前 AI cognition
与调用期 owner result 中；record/check/public invoke 通过 stdin/stdout 串联，正常
pre-task/standalone 不写 task、workspace 或 runtime artifact。Recorder/checker 执行
published closed Draft 2020-12 `guru-change-context-owner-result-3.0` schema。Active pre-task
input 是 `guru-stage0-discover-change-context-input-pre-task-2.0`；旧 input 1.0 与 owner-result
2.0 bytes 只作为 immutable legacy inventory。Caller 将该 public input 与 Sync actual stdout 的
独立 `base_current` 一起交给 Discovery；checker 结合 live Git 生成 owner-private
`base_observation`，不读取、伪造或重建 upstream private sync result、`facts_sha256` 或 result
identity。正常 HEAD advance
返回 `refresh_base`；dirty、wrong、missing、ambiguous、repo mismatch 或结构错误返回
`blocked`。Git status failure 不得冒充 clean，base stale 在 live issue/draft、
reviewed blob 与 archive preview 前短路。Draft-created-issue binding live 校验原 reviewed
body；caller-authored `refresh_base` 必须与 stable live stale codes 一致，`context_ready`
对同一 stale 拒绝。Archive reader
以普通 file/read/JSON/index-shape failure 形成 portable invalid evidence。
Deep-read locator 按 selected task artifact、canonical GitHub issue/PR 与 exact Git object/ref
三类闭合校验。Closed schema 与结构化 locator 不保存 raw source payload，也不做
跨字段扫描；不写 workspace/runtime/repo cache。

正常 mapped active-task 调用通过 ephemeral task identity 绑定 direct task branch 与当前
task worktree，允许普通进行中 edits，但不创建 checkpoint。只有 active-task owner loop 确实跨调用中断时，才在 ignored
`owner-checkpoints/<task-key>/` 下惰性创建同一 owner 的最小 current checkpoint。正常
mapped exit 不创建 checkpoint；stale 删除 current checkpoint 后从 live authority 完整重跑；
public projection/schema 校验成功后立即 consume-and-clean owner input/result/checkpoint 与
空目录。下游 Clarify 只消费最小 DTO，不读取或删除 Discovery private state。

Source issue 支持 GitHub live `open` / `closed`，runtime 将受支持的 state casing
归一为小写；duplicate candidates 与 draft-created issue binding 仍是 open-only。
Current Docs、code/contracts、tests 的 40 位 Git identity 必须从 `HEAD:<path>` 解析为
exact `blob`，tree、gitlink commit、tag、missing object 或 identity drift 均 fail closed。

Duplicate candidate 的 deterministic fact projection 是 normalized bound `repo`、positive
`number`、`identity=#<number>`、canonical issue URL、`state=open` 与 `updated_at`；pure
gate 从同一次 open duplicate search 返回字段重算排除 reason/observation 的
`facts_sha256`、identity 与 URL；record/check 不运行第二次 search 或 candidate re-read。
`blocked` exit 与 blocked AI Review Gate 在 schema/runtime 中
双向绑定。

Record/check production entry 先执行 pure schema/semantic shape，再执行独立 public input +
`base_current` 的 base-only live gate；repo-bound locator、issue、reviewed blob 与
archive/history 仅在 fresh base 后读取。`refresh_base` 要求重新调用完整 public Sync owner，
不保存 private result chain 或重建 snapshot ancestry。
`change_input` 十组 clue arrays 至少一组非空，issue binding/canonical query 不得
替代。Portable locator 只按 source-specific closed structure 验证，不扫描整份 payload。

Owner-result schema 是 `guru-change-context-owner-result-3.0`；managed commands 是
`preview-change-context-history`、`record-context-discovery` 和
`check-context-discovery`。Exits 是 `context_ready` -> active
`guru-clarify-requirements`、`refresh_base` -> `guru-sync-base`、`blocked` ->
`change-context-blocked`；source/installed validator 同时解析 active Skill consumer 及唯一
workflow/stop target markers。`context_ready` 的 actual stdout 投影为 closed
`context_current`，再与 Clarification 当前 semantic authoring fields 组成 call-local invocation。
代表性 installed transcript 必须调用真实 Sync public wrapper，经 Interface 声明 projection
构造 input 2.0 与独立 actual `base_current`，再调用真实 Discovery wrapper并把 actual
`context_ready` 投影到 Clarify schema。产品 Python tests 经 managed resolver/public wrapper；
low-level Sync executor、private import、手写 private digest 或 PATH Python import 都不算通过。

## Phase 0 Requirements Clarification

`guru-discover-change-context:context_ready` mandatory invoke semantic
`guru-clarify-requirements`。Initial issue/draft、active-task scope change 与 standalone review
共享相同 preconditions、AI Gate、仅服务真实选择/副作用的当前对话交互与 freshness。Repository-answerable questions
必须先由 current Docs/code/tests/history/GitHub/Git evidence 回答或记录不可回答证据，
`answered`至少有一个checked ref。之后每轮只问一个最高价值问题，question id必须来自opened/current-open，
`partial`不得关闭 question，reducer固定为`open_questions = opened - closed`。

AI 拥有 scope/action/交互必要性/pass/block/route 判断。Recorder 派生 proposal/action/
payload/content/result digest；checker 重算 schema/digest并只读验证 live source/context/task
binding。Package 没有 GitHub mutation executor；comment/body 写入仅在 AI 复核 live preimage
并在当前对话完成真实副作用确认后使用 shared repo-bound `gh` adapter，写后必须
重读；reviewed payload、payload digest、mutation result与live content必须一致，授权不进入
recorder/checker。成功 mutation
返回 `refresh_context`，不直接 `clear`。

Pre-task/standalone 结果 stdout-only且无专用 artifact。Active-task owner result 临时绑定
GitHub-visible authority、`issue-scope-ledger.json`、当前 planning/context/task-update 与 re-entry owner；
ledger 只接收不可重新推导的 compact classification。Schema 是
`guru-requirements-clarification-2.0`，commands 是
`record-requirements-clarification` / `check-requirements-clarification`。Active-task Scope Change
Gate mandatory invoke同一Skill。Exits 为 `clear` -> caller-aware
`guru-requirements-clear-router`（initial/draft -> #114 wording，standalone -> caller，active ->
planning review或exact interrupted progression）、`needs_context` -> context discovery、`refresh_context` -> base sync、
`retarget_context` -> base sync 并对 selected open issue 完整重跑 Intake、
`new_task` -> staged #112 full intake route、`blocked` -> fail-closed stop。

Initial/draft `clear` 的 actual stdout 投影为 closed `clarity_current`，只携带 Wording consumer
所需的 current target/context/scope identity；它不携带 clarification owner result 或 artifact
locator。Refresh/retarget exits 废弃当前 transition，并只进入声明的 fresh sync consumer。

只接受 closed 2.0 artifact；其他 schema version 在 normalization 前 fail closed，
recorder/checker 不执行迁移或投影。

Active-task `clear`/`new_task` 要求非空且全部属于七类 terminal decision 的 proposal set；
五类 scope classification 无论 origin 均要求最终 disposition；只有真实产品/范围选择仍未决时才在当前对话询问。
compact owner-result `decision_trail` 精确保存 `trail_id`、proposal id/digest/decision 与 live
GitHub authority kind/URL/content checksum。`issue-scope-ledger.json` 是 closed scope-only 2.0，
只含 schema version 与 primary/close/related/followup issue；trail 和
planning/context/review/stale/interrupted/re-entry 均由 checker 从 owner 或 live facts 重读，
不进入 ledger。`mechanism_removed/replaced` 使用 optional origin，
不进入 trail/action mutation。GitHub authority mutation 后只能 `refresh_context`；context
时间覆盖 live authority 后 task update preimage 绑定当前 context digest，不要求第二次 refresh。Active-task `new_task` 仍只给 #112
side-effect-free reviewed draft。

## Contract Wording Review

`guru-clarify-requirements:clear` 对 initial issue/draft mandatory invoke semantic
`guru-review-contract-wording`；Phase 1 在展示规划链接前再次用固定
`planning_artifacts` profile 调用同一 Skill。Standalone caller 只能用
`explicit_paths` 审查本轮明确指定的 repo-relative Markdown 文件。Canonical package
独占三个 profile、`contract-wording-v2` vocabulary、
`contract-wording-classifications-v1`、AI rewrite/review、confirmation policy、schema
`guru-contract-wording-review-1.0` 与 `pass` / `content_changed` / `blocked` exits；workflow
只拥有 mandatory invocation、profile-aware router 与 fail-closed stop。

Runtime commands 是 `record-contract-wording-review` 与
`check-contract-wording-review`。它们只重建 fixed scope、执行 deterministic scan、派生
digests/unchecked projection，并校验 schema、freshness 和 Gate/exit invariant；不选择
classification、rewrite、semantic pass 或 route。`change_request` selected comment 缺
author/updated time 会 fail closed；live issue revision 由 recorder 派生 confirmed-payload
与 mutation-result digests，并由 checker 绑定 reviewed payload、preimage、current reread
content/source update time。所有 profile 的完整结果都只作为 stdout-only owner-private
证据；`planning_artifacts:pass` 由 typed-exit router 立即消费，不写 task-local
`contract-wording-review.json`。该 profile 仍必须按 canonical contract 显式记录
`semantic_review.ai_review_gate.planning_checked_dimensions`；成功 exit 要求其 exact shape
全部为 true，deterministic runtime 只能验证，planning owner 会直接重读当前三份规划，均不得生成语义
结论。`content_changed` 要求对应 profile 完整重入；任何 active approval 若缺少当前
planning-only binding，必须重新执行完整 AI wording
review，再由 planning owner 重读三文档；禁止手补布尔值或重建 replacement digest chain。
Archived artifact 不改写。

Initial change-request `pass` 的 actual stdout 投影为 closed `wording_current`，使 Readiness
仅依赖当前 transition、live target 和本次 semantic authoring input，不再读取 repo-local
clarity/wording prerequisite bundle。

## Phase 1 Task Plan Approval

Phase 1 在 current `guru-review-contract-wording:planning_artifacts:pass` 后 mandatory
invoke active semantic Skill `guru-approve-task-plan`。Workflow 与 standalone mode 使用相同
八项 entry preconditions，并依赖完整 Guru Team preset、shared dispatcher 与 runtime。
Canonical package 是 planning adequacy、provenance、supported unusual scenarios、AI Gate、
真实选择或副作用的对话内交互必要性和 re-entry 的
唯一 owner；workflow 只声明 invoke、typed routing，并在 checked `approved` 的 consumer target
内拥有 plan presentation、对话停点与 activation transition。

唯一 owner checkpoint 是 ignored-runtime `planning-approval.json`，schema id 为
`guru-planning-approval-3.0`。Runtime commands `record-planning-approval` /
`check-planning-approval` 只记录已完成的 AI semantic result，并校验 schema、task/planning
locator、required file、一个 owner-private 组合 planning-content freshness token 与 closed
exit union，不生成 semantic pass 或 route。该 token 只由相邻 checker 重算以发现同路径内容
漂移，不是授权、semantic approval、public handoff 或全链 authority。四个 exits 是：

- `approved` -> workflow target `phase-1-task-activation`；
- `revision_required` -> `guru-approve-task-plan`；
- `clarify_scope` -> routing-only workflow target
  `guru-task-plan-clarify-scope-router`；该 target 只消费
  `exit_id`/`task_ref`/`proposal_refs`，建立 scope context 后 mandatory invoke
  `guru-clarify-requirements:active_task_scope_change`，完整 semantic input 由
  caller AI 基于 fresh live context 编写；
- `blocked` -> stop `task-plan-approval-blocked`。

Checked `approved` 只证明 planning semantic adequacy。`phase-1-task-activation` 先展示三份
planning 链接、AI 结论、关键选择、替代/取舍和未验证边界，再等待展示后的清晰整体肯定。
提问、修订或歧义回复保持暂停；实质 plan 变化重跑 wording/semantic review 并重新展示，
Phase 0 确认和旧方案回复不能复用。明确 autonomous execution 只省略未变化方案的普通停点，
scope、authority、重大方案或风险变化仍暂停。回复只存在于当前对话，不写入 owner checkpoint、
public DTO、schema 或 archive，recorder/checker 不解析回复。Planning approval 只接受当前 schema 3.0；其它 schema 或字段直接
fail closed，不执行升级、投影或兼容 re-entry。AI 对格式、拼写、链接、
派生文本与 workflow metadata 做 semantic delta classification，只刷新真实依赖；authority、
scope、design、acceptance、behavior 或 verification 变化才重入对应 semantic owner。

## Phase 0 Change Request Readiness

`guru-review-contract-wording:change_request:pass` mandatory invoke semantic
`guru-review-change-request`。Workflow 与 standalone 使用相同 preconditions，只消费 current、
checker-validated context、clarity 与 wording evidence，并绑定同一 target/content identity。
Target 固定为 `existing_issue`、side-effect-free `proposed_draft` 或
`standalone_request`。Canonical package 独占十项 readiness dimensions、findings、delivery
unit、scope conclusion、AI Review Gate、conditional confirmation 与 route judgment；global
workflow 和平台入口不得复制这些 step-local semantics。

Schema 是 `guru-change-request-review-1.0`，稳定 artifact basename 是
`issue-review.json`。`record-change-request-review` / `check-change-request-review` 复用现有
context/clarity/wording objective validators，重建 target projection、linkage 与 facts digest，
只校验 schema/hash/ref/freshness/Gate/consumer/ready invariant，并原样返回 AI-authored exit；
它们不搜索 duplicate/history、不读取 Docs/code/tests 作语义判断，也不生成 finding、delivery
unit、Gate 或 route。Pre-task/standalone 固定 stdout-only，#101 不创建 task、workspace、cache、
sidecar 或 tracked artifact。

五个 stable exits 与唯一 consumers 是：

- `ready` -> active `guru-create-task-workspace`
- `clarify_requirements` -> `guru-clarify-requirements`
- `review_wording` -> `guru-review-contract-wording`
- `refresh_context` -> `guru-sync-base`
- `blocked` -> `change-request-review-blocked`

`ready` 不得回退 `guru-full-task-intake-chain`、`check-env` 或 `prepare-task`。
Active `guru-create-task-workspace` 是唯一 mutation owner，直接消费当前 checked `ready`
exit，并且只持久化有真实后续 consumer 的 task-local `issue-scope-ledger.json`；不写
tracked `issue-review.json`。

`ready` 的 actual stdout 投影为 closed `readiness_current`。Workspace 通过 call-local plan/result
transport 完成已确认 mutation；用户确认仍只存在于当前对话，且不会写入 transition、plan、
result、ledger 或 runtime checkpoint。

## 中文 Conventional Commits

`guru-team` workflow 强制进入 PR 分支或 `main` 的提交使用中文 Conventional
Commits。工作提交和 Trellis metadata 提交 subject 格式为：

```text
{type}({scope}): #{primary_issue} 中文描述
```

工作提交 body 必须按 `背景：`、`变更：`、`边界：`、`验证：` 固定顺序编写，并用
`Refs #<primary_issue>` 作为 footer；不得在 commit message 中使用 close keywords
（`Closes` / `Fixes` / `Resolves` / `Close` / `Fix` / `Resolve`）。Issue 关闭语义只放在 PR body 的
`issue-scope-ledger.json.close_issues` 范围内。Trellis metadata 提交必须为空 body，
例如 `chore(trellis): #73 固化任务收尾元数据`。

本仓库保留 merge commit，最终 merge commit subject/body 必须由 publish payload 或
formatter 明确生成：

```text
chore(merge): #{pull_request} 合并 #{primary_issue} 中文 PR 摘要
```

companion helpers 只做 objective 校验和格式化，不替代 AI review：

```bash
.trellis/guru-team/scripts/bash/check-commit-messages.sh --json --task <task-path>
.trellis/guru-team/scripts/bash/format-merge-commit.sh --json \
  --task <task-path> \
  --pull-request <pr-number> \
  --summary "中文 PR 摘要"
```

Fresh final Phase 2 check 后，canonical workflow mandatory invoke
`guru-create-task-commit`。Skill 为每次提交在 ignored
`.trellis/.runtime/guru-team/task-commit-plans/<task-key>/<sequence>.json` 生成临时
candidate，AI 负责 scope/path/message/mechanical review；展示唯一 commit 副作用并只在
当前对话取得确认后，exact executor 才 stage 计划路径并验证真实 commit。candidate 不含
授权信息、永不 tracked/staged，成功后删除，只返回
`pre_commit_head`/`commit_sha`；Git 可推导的 result/tree evidence 不回写 task handoff，
所以成功提交不会制造 post-commit dirty。失败 candidate 仅用于同一未完成操作的 bounded
recovery；既有 tracked plan 只读兼容。`committed`、`revision-required`、`blocked`
分别由 Branch Review/finding closure、skill re-entry、fail-closed stop 唯一消费；finding
fix 必须先返回完整 Phase 2，并创建新 sequence。

Exact executor 在临时 detached worktree 与 isolated index 中调用真实 `git commit -F`，
因此 repository 的 `pre-commit`、`prepare-commit-msg`、`commit-msg`、`post-commit`
看到的是本次 reviewed candidate，而不是 live workspace 的无关状态。hook 拒绝、改写
message、增加或修改路径会在 live branch 发布前阻断；若 transaction commit 已创建，
失败结果携带其 identity 并保留 candidate/Phase 2 checkpoint。live ref 已推进后的失败
同样返回 created commit 供 bounded recovery，不尝试自定义 rollback。

`finish-work` dry-run 会输出合规 metadata commit subject 和 publish 计划；
`format-merge-commit` payload 会输出 `merge_commit.subject`、`merge_commit.body`
和显式 `gh pr merge ... --subject ... --body-file ...` 命令。维护者合并 PR 时不得使用
GitHub 默认 `Merge pull request #xx from ...` subject，也不得把中文 PR title
`完成：#xx ... (#yy)` 直接作为 commit subject。

## Knowledge Gate 与 Docs SSOT

当任务可能涉及 Guru Team 中台 SDK / framework 时，AI 应按 `.trellis/workflow.md`
检查当前平台是否可用 `guru-knowledge-center` MCP。可用时使用
`project_domain=middle-platform` 和当前 task context 检索，并把 citation 写入
`design.md`、`implement.md` 或 `{TASK_DIR}/research/middle-platform-knowledge.md`。
MCP 不可用时，默认 `optional_warn` 只告警并继续；配置为 `required` 时才阻塞。

Trellis task artifact 不是长期 repo docs 的替代品。Planning 阶段必须创建或更新
同一个 `Docs SSOT Plan`，推荐由 `design.md` 承载权威计划；`prd.md` 记录 docs 状态
和需求影响，`implement.md` 记录 checklist / checkpoint。计划需要记录 docs 状态：
`complete_docs`、`partial_docs`、`stale_docs`、`no_docs`；以及同步策略：
`ssot_first`、`delta_first`、`bootstrap_or_repair_docs`、`no_docs_update_needed`。

`Docs SSOT Plan` 还要列出证据路径、策略理由、当前 task 影响或检查过的 durable docs、
需要 merge 回 durable docs 的 task artifact delta。`delta_first` 必须写 merge checkpoint；
`bootstrap_or_repair_docs` 必须写最小修复范围或受限 follow-up；`no_docs_update_needed`
必须写具体理由。大范围、边界清楚的需求 / 设计 / workflow / API / 数据 / 部署 /
运营 / 测试合同变更应优先 `ssot_first`。无完整 docs 系统的 repo 也要明确记录创建
docs、补 partial / stale docs，或受限 follow-up 的结果。

业务项目内人类可读文档默认使用中文，覆盖 `.trellis/spec/**` 项目规范、
`.trellis/tasks/**` task artifact、`docs/**` durable docs、`00-bootstrap-guidelines`
创建或补齐的 docs SSOT，以及 workflow/helper artifact 中的 summary、evidence、
finding、observation、follow-up candidate、PR title/body 等字段。命令、路径、配置键、
GitHub keyword、外部 API 名称和代码符号等 literal token 可保留英文。`guru-trellis`
源码仓库自身是公共扩展仓库，它的 README、源码注释、脚本帮助和 marketplace metadata
可按分发需要保留英文或双语。

对尚未进入活动 task 路径的文件修改请求，tool-free classification 后的第一跳都是 semantic
`guru-select-workflow-mode`，无论是否已有 Issue、是否出现 task-free 表达或当前是什么
branch。最简显式表达 `这次走 task-free` 直接选择 `task_free`。没有明确表达时，AI 用完成
判断所需的有限本地 repository facts 和 Issue 内容执行三分判断：高置信、边界清楚、局部、
可逆且低风险时自动 `task_free`；大概率适合但 scope/risk 证据不足时只问一次；明显需要
隔离、规划、完整评审或高风险验证时自动 `standard_intake`。Issue 存在、文件数量、路径或
关键词都不能独立决定 mode。模式确定后 mapped exit、普通恢复和同范围重试不重复询问。
只有 standard Intake 的 typed exit `synced` 才进入：

`guru-discover-change-context -> guru-clarify-requirements ->
guru-review-contract-wording -> guru-review-change-request ->
guru-create-task-workspace`。环境检查可独立运行：

```bash
.trellis/guru-team/scripts/bash/check-env.sh --json
```

该兼容入口由 `guru-select-workflow-mode` 的 package-local
`check-workflow-environment` command 独占；extension version/provenance 由
`guru-verify-extension-installation` 的 `show-extension-version` command 独占，
Planning 三文档定位由 `guru-approve-task-plan` 的
`resolve-planning-artifacts` command 独占。三个顶层 wrapper 只转发到对应
package validator，不在 shared kernel 注册业务命令。

Compatibility `prepare-task.sh --json` 只执行显式 local query，不是 workflow hop，也不创建 GitHub
issue、worktree、branch 或 Trellis task。它的确定性实现由
`guru-create-task-workspace/runtime/prepare.py` 独占，不属于 shared kernel。
其实际 CLI 形态为：

```bash
BASE_PROVENANCE_JSON='<exact base_current.base JSON>'
.trellis/guru-team/scripts/bash/prepare-task.sh --json \
  --reviewed-base-provenance "$BASE_PROVENANCE_JSON" \
  "<user request or issue URL>"
```

该 flag 接收一个 JSON scalar，不是 file locator；对象必须 exact 包含 `source`、
`selected_base`、`remote`、`ordered_candidates`、`decision_head`、`local_base_head`、
`remote_base_head` 和 `post_sync_resolution_sha256`。可选 `--base-branch` 只做 equality assertion，
不参与 source reconstruction。
它只在 stdout JSON 中输出 source/proposed issue、duplicate candidates、selected base、
`base_freshness`、branch/task/workspace naming suggestions 与 `naming_quality`；不输出
workspace absolute path、task-create command、authorization/handoff state，也不写 task/runtime
context。在 `gh auth status`、issue read、fetch 与 duplicate search 前，query 必须先验证完整
reviewed base provenance（source、selected base、remote、ordered candidates、
decision/local/remote HEAD 与 post-sync digest）；缺失时本地返回
`missing_reviewed_base_provenance`，不得触发 semantic Intake。Remote ref 缺失是否合法只由正式
schema/runtime 状态矩阵决定。验证通过后才可用 shared strict core 重解析 selected base；
`fetch_performed: false` 或三方 HEAD 不相等都不能成为 `fresh: true`。Selected local base
落后时，只能在 selected-base checkout 上执行 `git merge --ff-only`；wrong checkout、dirty、
missing ref、fetch failure、divergence、resolution drift 或 post-sync mismatch 均 fail closed。
Every compatibility prepare invocation receives the complete reviewed
provenance, not only the post-sync digest. It preserves
explicit/config/config-candidate/remote-default provenance. Issue, branch,
worktree, task, artifact, and runtime mutations belong exclusively to
`guru-create-task-workspace`.

Resolution/result facts remain stdout-only. The query consumes the current
post-sync digest and reruns the shared resolver/sync core before its reads;
workspace mutation freshness is independently owned by
`guru-create-task-workspace`. There is no
resolution lease, release command, result-evidence cleanup, repo runtime record,
or task artifact for these pre-task facts.

`naming_quality` 是 slug / branch / worktree / task 命名质量门禁。AI 读完 issue 后
应生成语义英文 short-name，并通过 `--short-name`、`--workspace-slug`、`--task-slug`
传给脚本；需要特殊分支名时再显式传 `--branch`。推荐 worktree/task slug 格式为
`NNN-business-capability`。未显式传 `--branch` 时，branch 格式为
`<branch-type>/NNN-business-capability`，其中 `branch-type` 只能是 `feat`、`fix`、
`refactor`、`perf`、`test`、`docs`、`style`、`build`、`ci`、`chore`、`revert`，
未知语义 fallback 为 `chore`，例如
`feat/052-resume-detail-inline-attachment-preview`。中文或非 ASCII issue 标题不依赖拼音
transliteration 作为默认分支名；脚本不会智能翻译，只会做确定性类型判定、拼装、冲突检查和
低信息命名阻断。

Active workspace Skill 使用三个 managed runtime commands：

```bash
.trellis/guru-team/scripts/bash/record-task-workspace-plan.sh --json ...
.trellis/guru-team/scripts/bash/create-task-workspace.sh --json ...
.trellis/guru-team/scripts/bash/check-task-workspace-result.sh --json ...
```

Package schemas 是 ignored-runtime `guru-task-workspace-plan-2.0` 与
`guru-task-workspace-result-2.0`。Workflow/standalone preconditions 完全一致。
Reviewed draft invocation 只取得 `github_issue_mutation` confirmation，创建 exact issue 并
重读后固定返回 `refresh_review`；同一调用不创建 branch/worktree/task。完整 Intake 重跑后，
open issue invocation 另行取得 `workspace_and_task_mutation` confirmation。外部出口固定为
`created`、`refresh_review`、`blocked`。Passed + confirmed 才可 mutation；用户拒绝时在
recorder/executor 前停止且不生成 DTO，`reroute` 与 `blocked` 分别生成 checker-validated
zero-write `refresh_review`、`blocked` result。

Draft create 前按 exact open title/body/labels 与 `createdAt >= reviewed plan`执行 0/1/>1
recovery：0 个创建，1 个恢复并 live reread，多个阻断。完整 Intake 重入后的
workflow-created issue必须携带完整 checker-passed created-issue result，并重验 result/binding
digest、reviewed draft identity、current issue 与 fresh context canonical live
existing-issue identity；该 context使用`kind=issue`与 null `issue_binding`。

Assignee 固定按 explicit input、exactly one issue assignee、zero issue assignees 时 current
GitHub login、multiple/unresolved 时 AI/user 选择解析；executor 始终向 official
task-create handler 显式传 reviewed assignee。Executor 在隔离子进程中调用 official
`common.task_store.cmd_create`，并仅在该 handler 调用内禁用 developer accessor，使
`task.json.assignee` 与 `task.json.creator` 都等于 reviewed login。创建成功除 official
`task.json` 外只写 tracked task-local `issue-scope-ledger.json`；其余 Intake evidence、
plan/result 保持 ignored owner-private，本机 mapping 只在 ignored
`.trellis/.runtime/guru-team/**`。Public result 不含 absolute workspace path；checker
从 current config、reviewed slug 与 live Git facts 推导 worktree。

`guru-create-task-workspace` 使用 package-local resolver 统一 planner diagnostic、executor、
checker 与 reuse/recovery 的配置语义。`workspace_mode: worktree` 下，空
`worktree_root` 解析为 `<repo-parent>/<repo-name>-worktrees`，绝对值直接作为规范化根目录，
相对值从 repository root 解析；`workspace_mode: current` 使用当前 checkout 且不调用
`git worktree add`，此时 `worktree_root` 必须为空。缺失/不支持 mode、不可接受路径、
object conflict 或 stale mapping 在 branch/worktree/task/mapping 业务写入前 fail closed。
Public DTO 与 tracked task artifact 不携带本机绝对路径，只有 ignored runtime mapping 保存
与 live workspace 一致的规范化 `workspace_path`。

`workspace_mode: worktree` 下，task artifact 写入边界由 current `task.json`、当前 checkout、
`.trellis/.runtime/guru-team/**`、`git worktree list` 和
`check-workspace-boundary.sh --task` 推导/校验。
在写入或校验 `planning-approval.json`、`phase2-check.json` 或
`review-gate.json` 前，从目标 worktree 运行：

```bash
.trellis/guru-team/scripts/bash/check-workspace-boundary.sh --json --task <task-path>
```

该 validator 只提供机器事实：expected workspace、actual repo root、source checkout
status、task worktree status、source checkout 中可疑同名 task artifact / review
metadata，以及 fail-closed 错误。它不判断 sub-agent 是否 stale，不迁移误写 patch，也不
清理 source checkout；这些仍由 AI/human workflow 决定。手工编辑工具不能接收显式
working directory 时，必须使用 boundary helper 已确认的当前 task worktree 下的绝对路径。

`create-task-workspace` 在 GitHub 或 worktree/task mutation boundary 重验 reviewed
resolution、本地 decision/base/remote-tracking facts，并通过只读 `git ls-remote --heads`
读取当前 remote base HEAD。Initial planner evidence 不能替代 mutation-time guard；不要从过期的
本地 `main` / `dev` 创建任务分支。

Plan 绑定 initial checker-passed `post_sync_resolution_sha256`。Executor 的 mutation guard
不得调用 `execute_base_sync`、fetch、fast-forward 或更新本地 ref。若只读 remote HEAD
发现 remote 前进，必须在 decision HEAD、local base 与 remote-tracking ref 均不变的情况下返回
`refresh_review`，且不创建 issue/workspace/task/artifact/runtime；下一轮完整 Intake 重新进入唯一
authoritative `guru-sync-base` public invocation。Identity 不变才继续。

Guru preset apply/update/reapply 与 workspace executor 不读取、不创建、不复制、不恢复
`.trellis/.developer` 或 `.trellis/workspace/**`，也不要求 `init_developer.py`。Official
Trellis 仍可独立创建和使用 identity/workspace journal；Guru 不删除已有数据，source/target
中 existing identity bytes 在 workspace transaction 前后保持不变。
A/B merge fixture 从同一 clean base 分别走 production recorder/executor/checker 与
task-local archive/commit，再验证 A -> B、B -> A 两个本地 merge 顺序无 Guru metadata
conflict；不创建远程 PR或并发进程。

`no_task` 下 selector 的最小 `task_free` DTO 通过 target-owned authoring seed 调用
semantic `guru-execute-task-free-change`；selector 不增加 checkout 字段。该 Skill 独占写前
checkout suitability、限定编辑、风险匹配的 targeted checks、写后 scope/risk 复核和两个
交互 self-reentry。`completed` 必须绑定实际 edited paths、至少一个 passed check、无 failed
check，以及通过的写后复核，并向 workflow completion consumer 直接投影实际修改路径、
精简检查结果和未验证边界；命令 transcript 与 review narrative 保持 private。

执行中 scope/risk 扩大必须在真实 partial edit 后停止后续写入，并记录新发现、已改路径、
未执行的剩余写入与适用 targeted checks。自动选择的 task-free 重新进入 selector；用户
显式选择的 task-free 不静默升级，由用户选择缩小范围或进入 `standard_intake`。Task-free
不授权 task/worktree/branch、commit、push、PR、merge、tag、release、installation、
cleanup 或关闭 Issue；这些生命周期与发布动作继续独立检查和确认。

`guru-execute-task-free-change` 的 public inputs 为 `selected_route` 与
`interaction_resume`，typed exits 为
`completed|resume_active_task|scope_change|location_required|reselect_mode|explicit_choice_required|blocked`。
完整 preset 发布 `record-task-free-change`、`check-task-free-change` 和
`invoke-guru-execute-task-free-change`；package 不是可脱离 extension runtime 单独复制的工具。

Branch Review Gate、exceptional recovery 与 publish helper 是内部子命令。routine
dispatch/wait/review 不调用 recovery recorder：

```bash
.trellis/guru-team/scripts/bash/record-agent-recovery.sh --json \
  --task ".trellis/tasks/<task>" \
  --event unfinished \
  --logical-role "实现代理" \
  --agent-id "<unfinished-agent-id>" \
  --reason "agent 已明确未完成" \
  --handoff-summary "已完成范围、剩余工作与 blocker"
.trellis/guru-team/scripts/bash/record-agent-recovery.sh --json \
  --task ".trellis/tasks/<task>" \
  --event replacement \
  --logical-role "实现代理" \
  --agent-id "<replacement-agent-id>" \
  --predecessor-event-id "<unfinished-event-id>" \
  --reason "replacement 接手未完成工作" \
  --handoff-summary "接续范围、剩余工作与 blocker"
.trellis/guru-team/scripts/bash/check-agent-recovery.sh --json --task ".trellis/tasks/<task>"
.trellis/guru-team/scripts/bash/check-commit-messages.sh --json --task ".trellis/tasks/<task>"
.trellis/guru-team/scripts/bash/format-merge-commit.sh --json --task ".trellis/tasks/<task>" --pull-request "<pr-number>" --summary "中文 PR 摘要"
.trellis/guru-team/scripts/bash/check-review-gate.sh --json
```

Closeout 不属于这组可手动调用的 recorder/validator 命令。显式 canonical
`guru-finish-work` entry 必须按 live workflow 进入 publication owner 和 active
finalizer；只有 finalizer 的 checked private engine 可以执行 finish helper。

Exceptional sub-agent recovery is activated only after an agent explicitly
returns unfinished and a replacement must inherit the work. The main session
records one minimal `unfinished`/`replacement` chain in ignored
`.trellis/.runtime/guru-team/agent-recovery/<task-key>.json`; routine assignment,
wait windows, progress, status requests, review rounds, and successful completion
do not create artifacts. Mapped stale/re-entry/reprepare routes remain inside the
AI workflow and never become a generic user confirmation prompt.

用户日常可以直接描述任务、贴 issue URL，或说“处理 issue #123”。AI 依赖
Trellis 自动注入的 startup context、workflow-state、hook breadcrumb 或 skill
matcher 判断是否进入 Guru Team issue intake 和 worktree preflight。

用户可以直接描述任务、贴 issue URL，或使用官方 Trellis 提供的
`trellis-start` / `trellis-continue` 入口；这些 upstream-owned 文件不由 Guru preset
覆盖。显式收尾使用 Guru-owned `guru-finish-work`：Codex、Claude、Cursor 分别是同名
prompt、`/guru:finish-work`、`/guru-finish-work`。三个 launcher 都只加载 live
`.trellis/workflow.md` 和 active public graph，不读取 package-private runtime/artifact，
不复制任何 step-local 合同。

Planning start gate 和 Phase 2 check gate 都需要 current task facts 与 owner-private
短生命周期 evidence。进入实现前主会话在三份 planning artifact 与 `Docs SSOT Plan`
就绪后 mandatory invoke `guru-approve-task-plan`。该 Skill 负责全部 entry precondition、
审查、必要 revision/clarification、仅服务真实选择或下一项副作用的当前对话交互、3.0
recorder/checker 和四出口；checked `approved` 进入 workflow-owned
`phase-1-task-activation` plan presentation/review pause，清晰肯定后才执行 pair guard 与
`task.py start`。现有 Open Issue happy path 为四次确认，新建 Issue path 为五次。Phase 0 route DTO、非 3.0 planning input、缺失/过期/non-pass wording、
真实 planning/authority 语义漂移或 exit/Gate/consumer 不一致均 fail closed；owner 只接受
重新检查过的 current invocation。`task.py start` 只是状态写入，
不代表规划已审查。
阶段停止点和阶段完成回复先运行
`resolve-human-artifacts.sh --json --task <task-path>`，只展示实际存在的 `prd.md`、
`design.md` 与 `implement.md` 链接；不要求固定表格，JSON gate/evidence、private
checkpoint 与 PR payload 不进入默认 human artifact 展示。
commit 前先由 unchanged official `trellis-check` 收集实际 terminal evidence，再
mandatory invoke active semantic Skill `guru-check-task`。该 Skill 先做 scope
qualification，再做 current-scope severity、complete adequacy、Docs SSOT review、
finding/full-rerun loop 与最终 AI Gate；它独占 closed
`guru-phase2-check-5.0` 的唯一 ignored-runtime `phase2-check.json` 和 `passed` /
`implementation_required` / `planning_stale` / `blocked` 四出口。
`record-phase2-check.sh` 与 `check-phase2-check.sh` 只处理 AI-authored result 的
确定性 closed schema、`phase2_capture_commit`、`reviewed_content_sha256`、当前
dirty-path coverage、finding/scope linkage 和 route facts；reviewed-content identity
只由 `guru-check-task` public wrapper 内的 checker 在 DTO 投影前重算，不是授权、semantic approval、public handoff 或
全链 authority。几个验证命令、worker 输出或脚本通过不等于 semantic pass。
`phase2-check.json` 是 commit 前的 owner-private 短生命周期 checkpoint，不是 Trellis
原生步骤本身，也不是脚本替代 AI check 的入口。`passed` 只向 Task Commit 投影
`task_ref + phase2_commit_anchor`；public wrapper 在 DTO schema 校验成功后删除自己的 checkpoint。
Task Commit 和 Branch Review 只消费 DTO 与 live Git，不读取、删除或重开 Phase 2 私有状态。

Schema 4.0 只保留 current commit anchor、reviewed-content identity、reviewed paths、实际
validation、Docs SSOT、九个 adequacy 维度、finding lifecycle 与 typed route。Routine
assignment、handoff、liveness、raw worker payload、review round 与 per-file/artifact digest
bundle 不持久化；checker 只验证直接 consumer 所需的结构、freshness、coverage、linkage
与 closed exit union。

Phase 2 必须消费 planning 阶段的 `Docs SSOT Plan`。实现代理只返回最小 terminal result：
material changed behavior/paths、验证结果，以及确有必要的 Docs SSOT outcome 或 bounded follow-up；
不得重写 planning、生成 next-owner checklist 或创建独立 handoff artifact。`guru-check-task`
由 approved plan、task artifacts、implementation terminal result、embedded evidence、live diff 与测试事实
重建完整判断，并按同一策略复核 durable docs、
task artifacts、code/schema/config/deploy/test 和验证/测试覆盖是否一致；`delta_first` 必须在最终
Phase 2 check 前完成 durable docs merge，`ssot_first` 必须以修订后的 durable docs 为主要输入。
如果实现发现长期合同变化超出 plan，必须先更新 planning artifacts 和 `Docs SSOT Plan`，必要时重新
planning approval，再重新 Phase 2 check。

Codex 项目默认使用 `codex.dispatch_mode: sub-agent`，由 main session 调度
`trellis-implement` / `trellis-check`。默认 sub-agent mode 下，main session 只负责
规划、调度、等待、必要时处理异常恢复/替换、记录 Gate evidence、commit 和运行 recorder/validator；实现必须由
`trellis-implement` / channel `implement` 完成并输出最小 terminal result，Phase 2 check 必须由
`trellis-check` / channel `check` 完成并输出可记录到 `phase2-check.json` 的 evidence，
commit 后 Branch Review 必须由独立 review sub-agent 审查完整 `origin/<base>...HEAD`
diff 并向 semantic owner 返回最小 terminal findings/evidence；不创建 per-round report
或 rollup。main session 自己实现、自检、自审或脚本校验通过都不能替代这些边界；
缺少实际 evidence 时 fail closed。因为 Codex sub-agent 使用
`fork_turns="none"` 隔离，dispatch prompt 必须以 `Active task: <task path>` 开头；
sub-agent 若没有拿到该行，则运行 `task.py current --source` 解析当前 task。只有显式配置
`codex.dispatch_mode: inline` 时，Codex 才降级为 main session 直接实现和检查。
Guru Team preset 安装项目级 agent 定义：Codex 使用中文 `description` 表达 UI 语义，
但 `nickname_candidates` 保持 ASCII，因为当前 Codex 会拒绝中文 nickname 候选并忽略
agent 文件；Cursor / Claude / channel runtime agent 使用中文 description 和标题。这些文件中的
`trellis-implement` / `trellis-check` / `trellis-research` 以及 channel runtime 的
`implement` / `check` 是稳定调度标识，不能为了中文展示而改名。

Routine sub-agent assignment、wait、progress、review round 与 completion 不写 task
artifact。只有 agent 明确 unfinished 且 replacement 必须接手时，main session 才写 ignored
agent-recovery checkpoint；普通 mapped exit、stale/re-entry/reprepare 由 AI workflow 自动
承接，不向用户暴露为“确认继续”。

Active `guru-review-branch` 是唯一的 Phase 3.5 semantic owner。Global workflow 与
平台 `trellis-continue` entry 只用 `profile`、`mode`、`task_ref`、`base_ref`、
`branch_review_commit`、`review_intent` 六字段 public input mandatory invoke 该 package，
并消费 `passed`、`implementation_required`、
`scope_confirmation_required`、`blocked` 四个 typed exits。Reviewer lifecycle、
finding qualification、Docs SSOT Gate、recovery checkpoint、private artifacts 与 re-entry
规则均由 package 独占，入口不得复制。

`review-branch.sh` 与 `check-review-gate.sh` 只是 package-owned deterministic
recorder/validator implementation details，在 AI Review Gate 后记录和校验 objective
facts；它们不能替代 semantic review，也不能决定 scope、finding、充分性、pass 或 route。
Phase 2 的官方 `trellis-check` sub-agent 仍只提供 commit 前 raw evidence，active
`guru-check-task` 独占 Phase 2 semantic check；Phase 3.5 的全部判断由
`guru-review-branch` 独占。

`trellis-continue` 不得 push 分支、创建 PR 或调用 `finish-work`，也不得提交
`review-gate.json` 等 Trellis metadata。
PR 发布只从显式 canonical `guru-finish-work` 薄入口开始：该入口先按 live workflow 调用
`guru-review-task-publication`，仅从 `ready` 进入 `guru-finalize-task`。Finalizer 的私有
preview 在内存中生成 exact side-effect plan；只有 same-owner re-entry 需要时才写 ignored
`finalization-transaction.json`，其中 `plan_digest` 只绑定下一 deterministic consumer。
语义 Gate 在当前对话完成真实副作用确认后才执行
reviewed content push、draft PR、final archive
projection、单次 archive metadata commit/push、三方 HEAD 对齐与 draft-to-ready。裸
`finish-work.sh` 默认拒绝普通直接调用；中断由同一 finalizer 自动消费 recovery
route，不暴露内部 flag 或要求用户选择下一条命令。
Prepare 使用已安装的官方 config parser，只支持缺失或空 `hooks.after_archive`；
非空、歧义、不可读、含 NUL 或 symlink 配置在副作用前拒绝，且不会执行 hook。
official move 前重新核对实时 archive 月份、空 index、精确 untracked 集合、regular-file/mode
与 tracked source blob。跨月时同一 entry 从 transaction 与 live facts 重建 mapping，不创建
plan/readiness/evidence commit、不 rewrite history 或迁移目录。`closeout-plan.json` 的
schema/example 仅是 immutable legacy compatibility assets；current Interface、registry、
manifest、prepare、recovery 与 archive 均不选择、创建、读取、移动或保留它。
若历史 Git index 仍跟踪该文件、但 working tree 已删除，current Finalizer 只把它作为
archive transaction 的 active-side retired deletion，并校验 transaction parent blob 与
commit path continuity；不会恢复或归档旧文件。已绑定 `existing_pr_recovery` 且进入
`archive|push_archive|mark_ready` 时，先校验 exact transaction 再判断 pre-PR provenance，
外部 extension source commit 与业务 reviewed-content commit 不同不会覆盖 post-bind stage。
共享 prepare 从 archive root 到 month/final destination 逐层 `lstat` 既有组件，不读取或
跟随 symlink target；任何 symlink（含 dangling、repo 内 target）都拒绝，且 final locator
必须不存在。official move 前重复同一检查，阻止 prepare-to-move 漂移。缺失的
`task.json.children` 视为
空 list、其余值严格校验为 `list[str]`。按官方 active task exact/suffix lookup，只有会被
archive 改写的 active child 阻塞；已归档 child 不阻塞 parent closeout。
Gate 后到 finish-work/archive 只允许 Trellis metadata tail；durable docs、`.trellis/spec/`、
source、tests、schema、config、scripts、preset、overlay、CI/CD、deployment、migration、
Makefile 等 non-metadata drift 必须回到 Phase 2/3。finish-work dry-run 和正式 finish 都不做
首次 Docs SSOT merge。

Finalizer 的 private preview 是无副作用 readiness step：它校验 gate、dirty state、
Publication ready 4.0 DTO 的 exact title/body 与 live facts，并输出 exact side effects、
future archive mapping、transaction stage 与 transitions，不移动或写入文件、不创建 commit、
不 push、不创建 PR，且没有 journal/workspace 计划。
dry-run 回复使用 active task 的 `Markdown 产物 review 表`；正式 archive 后，AI 必须
重新运行 resolver 解析 `.trellis/tasks/archive/YYYY-MM/<task>/...` 路径，并在最终回复输出
archive-path 表，不能复用 archive 前的 active task 链接。

PR body 是给 GitHub reviewer 看的发布材料，不是 Trellis task artifact。Publication
owner 在同一 semantic loop 内生成并审查 body readiness，确认 `变更摘要` 具体、
`影响范围` 明确、`验证结果` 是实际命令与结果、`Review Gate` 写明
`branch_review_commit` / diff range / content identity / findings 状态、`Issue 关闭范围`
只关闭 ledger 中的 `close_issues`，并且
`安全说明` / 部署影响与本次 diff 相符。Body 还必须包含 `Docs SSOT` / `文档同步`
section，说明策略、durable docs 更新或 no-update 理由、已 merge 的 task delta、仅保留
task history 的内容，以及 follow-up / 当前 PR limitation。Publication ready 4.0 DTO
精确输出 `exit_id/task_ref/branch_review_commit/pr_title/pr_body`；Finalizer input 4.0
直接消费 payload，不从 task-local 文件、private checkpoint 或 runtime source 补取。

Guru Team 不调用 `.trellis/scripts/add_session.py`，不读写 `.trellis/workspace/**`。
shared `trellis-start` 只读取 phase/packages/current-task/Git facts，Codex/Cursor
SessionStart overlay 不导入或调用 journal helper，也不打开、枚举、读取或输出 journal。
finish-work 先绑定唯一 draft PR，再从 reviewed PR payload 与 live facts 在 active task 中
一次构建 schema 2 `finish-summary.json`，包含 canonical URL 与唯一 `PR #<number>` ref。
recorder 对 raw base-to-HEAD paths 排序去重后过滤 workspace/runtime
受保护前缀，过滤发生时追加一条不含 path、basename 或数量的固定 contract fact；未发生过滤时
不追加。initial diff、initial untracked 或 final/recovery diff 失败时两个 path 数组都为空，
只追加固定 snapshot-unavailable fact，并重新派生 retrieval text。schema/validator 对所有 path
字段继续拒绝受保护前缀。final summary 在 active task 中严格校验一次，并只随 archive metadata
transaction 提交；archive 后不再回写 artifact 或新增 metadata tail。同一入口在 archive 前根据
transaction、readiness、active locator 与 live facts 恢复。official move 后、精确 archive commit
尚未形成时，仍校验 archived working-tree 布局、dirty/staged path、blob continuity 与官方
`task.json` delta；失败只从 immutable `publication_head` 恢复 task locator 的 tracked bytes。

Current core 固定为 6 个 durable 文件：`task.json`、`prd.md`、`design.md`、`implement.md`、
`issue-scope-ledger.json`、`finish-summary.json`。Publication readiness 与 Finalizer
transaction/gate/request 为 ignored runtime，不进入 archive，terminal
`ready_for_merge` 后全部退休。业务 task 不创建、读取、移动或归档 verifier artifact。

一旦当前 `HEAD` 已是精确 archive commit，recovery 从该 commit blob 读取 `task.json` 与
`finish-summary.json`，并以 Git parent/path/tree/blob lineage 作为 deterministic inputs；本地
archived 文件缺失、篡改及其 dirty state 不阻塞 exact push、remote PR identity、三方 HEAD 或
draft-to-ready。archived recovery 在 GitHub/fast-path 前校验 Git toplevel、配置/effective repo、
当前 head branch、base ref、current HEAD transaction、task identity 和 exact archive locator。
普通 task discovery 与其它命令仍要求 `task.json`；worktree mode 从 current task、runtime mapping
与 Git worktree facts 解析边界。错误 repo、transport、number、额外 URL path、query/fragment、
缺失或替换 PR 均 fail closed。

Publication owner 在 ignored runtime 记录 schema 5.0 `pr-readiness.json`，其 public
`ready` DTO 携带 task、`branch_review_commit` 与 exact `pr_title/pr_body`；Publication
wrapper 校验 DTO 后删除自己的 checkpoint，Finalizer 不读取、删除或提交该 owner
checkpoint。Finalizer transaction 直接绑定 title/body，且不创建独立 evidence commit。
Finalizer 从 reviewed body 的 `变更摘要` 与 live Git/task/ledger/PR facts 一次生成 schema 2
`finish-summary.json`；Discovery 仍可只读检索历史 schema 1 archive。
脚本只做客观结构校验、低信息量短语阻塞、close/ref 语义校验和 reviewed source 门禁；
不能用脚本生成的空泛摘要或 `generated` body 替代 AI 发布判断。


## Source-owned Standalone Installation Verification

`guru-verify-extension-installation` 是 extension installation 唯一 semantic owner，
但不是业务 task、Publication、Finalizer、finish-work、re-entry 或 recovery 的步骤。
它只接受 clean `castbox/guru-trellis` source checkout 中的显式
`source_repository_verification` standalone input，并只返回 `verified|blocked` 给直接
standalone caller。不存在 workflow profile、task-bearing fallback、`not_required` round、
Finalizer projection 或 task-local verification artifact。

Source identity preflight 在 clone、tempdir、installer、artifact write 或任何 Git/GitHub
mutation 前验证 canonical source assets、`origin`、`repo_ref`、requested ref、resolved
commit、当前 HEAD 与 clean checkout。非 source checkout、task-bearing field 或 identity
mismatch 使用稳定 invocation error fail closed，且 executor command count 必须为零。
通过 preflight 后，runtime 才创建 isolated source checkout 和 clean throwaway target，覆盖
new init、preview/switch、preset apply/reapply、`trellis update`、ownership/sidecar、contract
discovery、platform equality、README command 与 redaction。Owner state 只存在 source
session 的 ignored runtime，完成后删除，不写入 `.trellis/tasks/**`。
Current semantic input 固定 `applicability.status=required`，private result 使用独立
5.0 schema identity。Public invocation 只有在 `verified|blocked` terminal DTO 完整校验
后才删除 source-session owner checkpoint；任何失败都保留 checkpoint 供同一 owner 重试。

## Skill 行为评测

安装完整 Guru Team preset 后，可用 `discover-skill-evals` 发现 current Interface
1.4/1.5 package 的 `evals/evals.json`，并用 `run-skill-evals` 经
`shared|codex|claude|cursor` adapter 实际执行 public wrapper。Schema id 是
`guru-team-skill-evals-1.0`，status 闭集为
`passed|evaluation_failed|execution_error|unsupported`。外部 semantic grading
与 human feedback 独立，run evidence 只能位于 repo 外。当前 production Skills
中的二十一个 packages 已维护 canonical corpora 并覆盖全部 89 package exits/profile；六个 Intake
packages 的 23-exit closure 仍独立验证。四个 descriptor 分别绑定
可执行 `shared.sh|codex.sh|claude.sh|cursor.sh`；shared 解析 preset-managed
`guru-team-shared-eval`，其余 adapter 从 `PATH` 解析 `codex|claude|cursor-agent` 并组装平台
专用非交互 argv。Runner 在 native
execution 外读取 canonical corpus；native 只加载 repo/package 外 public-only Skill projection、
prompt/staged files，不接收 canonical package/corpus/private runtime locator。Native CLI 必须通过 repo 外 trace helper
读取 `SKILL.md` 并调用 exact wrapper；`guru-team-skill-eval-native-trace-1.0` receipt 与
request、projection、Skill/wrapper digest、wrapper argv/return code 和返回 DTO 完整绑定后才产生 trace invariant。合法 DTO
缺少 receipt 为 `execution_error`。Native argv、output、context 与 receipt locator 收集到
repo 外 transcript；四平台 projection 中 eval/private runtime raw read 必须真实失败。缺失
native command 为 `unsupported`，不依赖隐藏环境变量替代 adapter。
Semantic case 必须引用 repo-local checker-passed owner result；actual exit 选择 output schema
后才比较 expected exit。Codex 使用 trusted Git root，Claude 使用 safe non-interactive 协议，
Cursor 未登录直接返回 `unsupported`。
Finalizer transaction 同时绑定 `reviewed_content_head` 与 `publication_head`。业务
content push 后直接继续 Draft PR、archive 与 Ready transaction；installed manifest、
README、docs、config、`.trellis/**` 或平台副本 changed path 都不会产生 verifier route。
`reprepare_required` 只服务 Finalizer 自身 current transaction 的稳定重建，不读取 verifier
owner state、verification ref 或 legacy task artifact。
