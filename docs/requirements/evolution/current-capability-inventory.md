# Guru Trellis Current Capability Inventory

版本：`current-main-0.6.5-guru.42-to-evolution-revision-2026-08-30`；状态：
`requirements_trace_ready_for_design`。

本文件是 Evolution Requirements 的 current-to-target 能力保留与差集台账。它回答“当前
已经具备哪些可观察能力、目标版本如何承接、哪些只是旧合同形态、哪些是本轮新增目标”，
不定义 target 行为，也不取代任何 current authority。

## 1. Authority 与一致性关系

本 inventory 的 current authority snapshot 为
`source_ref=5650df47fe17fe89b7cb616be6c9551608164832`。该 ref 是 `2026-08-30` fresh
reconciliation 时核实的 selected `origin/main`，包含 #311 PR #313 的 merge commit
`21c7da14798683193b460a5e7c5bd24c7c517804`、#312 PR #314 的 merge commit
`3efcce72a0d47e38ec725aa8c0f8498992f3416f`、#267 release-authority merge `a41b8a34…`、
evidence-fix PR #316 merge `9f560ec1…`、installed platform-selection preservation PR #317 merge
`736ef333…` 与 caller-inventory consistency PR #318 merge `5650df47…`；active
Requirements/Design/Test/Architecture authority 为 `current-main-0.6.5-guru.42`，其 source baseline 为
`d3dca74b3a94569a095594477c15b032526f2381` + #267 expected `.41` serialized promotion delta。所有 current
结论必须用 `git show <source_ref>:<path>` 或等价 immutable object 读取。后续 `origin/main`
漂移不得隐式改变本 inventory，当前未 rebase 的 task worktree 相对路径也不得替代下表 locator
或与该 source snapshot 拼接成虚构 authority。

上一 selected base `736ef3335f1b1b0dcbf92f1e8e53343f922aa32a`、更早 selected base
`9f560ec191851f82768d5e7aa031e6d852c34f14`、
`a41b8a34d237e1863225d069ca9c6b5ad6ae476a`、上一轮 `.41` 的
`source_ref=3efcce72a0d47e38ec725aa8c0f8498992f3416f`、`.40` 的
`source_ref=d907fcc5e17f23b6499648e5e9a208457f2d6f8b` 与更早的
`a4b68d42b25e3d2173fac2db353295043590cca5` 只保留为历史 snapshot/evidence。本轮保留
`.40` 的既有 Gitlink reviewed-content identity、EOF-only blank-line review 能力以及原始
21 Skill/89 exit inventory 作为 comparison evidence；不得继续把这些历史 ref 称为 current locator。

| Authority slice | `source_ref` | `path` | 本 inventory 的使用边界 |
| --- | --- | --- | --- |
| `.42` Requirements 功能与行为 | `5650df47fe17fe89b7cb616be6c9551608164832` | `docs/requirements/versions/current-main-0.6.5-guru.42/requirement-main.md` | current `REQ-*`、`BEH-*` 与产品结果来源；`REQ-052..055` 只描述 fact-only authority/release alignment，PR #317 另增加 canonical runtime 的 platform-selection observable behavior；PR #318 不改变正文 |
| `.42` Requirements 非功能 | `5650df47fe17fe89b7cb616be6c9551608164832` | `docs/requirements/versions/current-main-0.6.5-guru.42/requirement-non-functional.md` | current `NFR-*` 边界来源；tracked `.42` 正文未因 PR #317/#318 增号 |
| `.42` Requirements decisions | `5650df47fe17fe89b7cb616be6c9551608164832` | `docs/requirements/versions/current-main-0.6.5-guru.42/decisions.md` | current 产品取舍、release fact 边界与明确排除项来源 |
| `.42` Design capability inventory | `5650df47fe17fe89b7cb616be6c9551608164832` | `docs/design/versions/current-main-0.6.5-guru.42/capability-inventory.md` | active Skill/interface/external-exit inventory 与 source identity；本文件逐项建立 successor/classification，不复制正文 |
| `.42` Design main | `5650df47fe17fe89b7cb616be6c9551608164832` | `docs/design/versions/current-main-0.6.5-guru.42/design-main.md` | current 实现责任、设计宪法与 change contract 来源；`DES-049..052` 只描述 fact-only promotion lifecycle |
| `.42` Design traceability | `5650df47fe17fe89b7cb616be6c9551608164832` | `docs/design/versions/current-main-0.6.5-guru.42/traceability.md` | Requirements-to-Design 与 package responsibility 追踪来源 |
| `.42` Test strategy | `5650df47fe17fe89b7cb616be6c9551608164832` | `docs/test/versions/current-main-0.6.5-guru.42/test-strategy.md` | current `TST-*`、`SCN-*`、`CASE-*` 与验证 ownership 来源；`TST-036..039` / `SCN-048` 只验证 fact-only authority promotion，PR #317 focused tests 是新增 code evidence |
| `.42` Test plan / evidence | `5650df47fe17fe89b7cb616be6c9551608164832` | `docs/test/versions/current-main-0.6.5-guru.42/test-plan.md` | current Test 执行计划、before-state、矩阵与 evidence boundary；tracked plan 相对 `9f560ec1…` 不变，PR #317 platform matrix evidence 来自 canonical focused tests/task archive，PR #318 只刷新 caller inventory evidence |
| `.42` Test traceability | `5650df47fe17fe89b7cb616be6c9551608164832` | `docs/test/versions/current-main-0.6.5-guru.42/traceability.md` | current Test capability 到 requirement/design 的追踪来源 |
| Architecture Baseline | `5650df47fe17fe89b7cb616be6c9551608164832` | `docs/architecture/README.md` | current Architecture authority 的入口与适用 baseline locator；PR #317 修复 installed platform behavior，并把 latest stable current fact 修正为 `.2/.38/CLI 0.6.15`；PR #318 不改变 baseline |

target 行为的唯一主定义仍是 [`requirement-main.md`](./requirement-main.md) 中对应的
`EVO-REQ-*` 和 [`requirement-non-functional.md`](./requirement-non-functional.md) 中对应的
`EVO-NFR-*`。上表只定位 current authority；本文件摘要、canonical registry/interfaces 与 Git/live
facts 都不得成为平行产品主定义。canonical registry/interfaces 在同一 `source_ref` 下只补充
`code_recovered` 的 active package/route 事实，必要 Git/live facts 只证明当前可观察状态。

本轮只读 reconciliation 表明该 source ref 是 `2026-08-30` 重新绑定的 immutable selected-base
snapshot；本次 rebind 未执行新增 rebase/merge。该 `.42` authority 已同步 `REQ-013/018`、
`DES-010/016`、`TST-015/SCN-013` 对 capability-loss 与独立 consistency/installation gate
的分工，并包含 #311/#312 的 merged source facts。canonical registry/interfaces 的当前派生结果
仍为 21 个 active Skill，各 active interface 的 `external_exits` 合计 89 个，并与同一 source ref
下的 `.42` Design inventory 一致；Test strategy、Test plan/evidence 与 traceability 均绑定同一
snapshot。本轮已从该 exact source 确认 `.42` 相对 `.41` 只增加 `REQ-052..055`、`DES-049..052`、
`TST-036..039`、`SCN-048` 的 release-authority/promotion facts，runtime behavior、public Skill API、
Architecture decision/owner/GAP/compatibility exit 均未改变；因此这些新增 identity 不形成新的
`CUR-CAP-*`、`TARGET-DELTA-*` 或 Evolution fixture。`9f560ec1...736ef333` 则包含 material runtime
advance：Finalizer reprepare 按 parent manifest 精确保留 selected platform set，并在 invalid identity 时于
source checkout/preset apply/commit 前 fail closed；该能力折入 `CUR-CAP-013/014/017`，不形成第 24 个
capability、第 14 个 target delta 或第 51 个 fixture。`736ef333...5650df47` 又只刷新 caller-inventory
identity、Issue disposition、dogfood provenance 与 archive/merge facts，不改变上述能力或集合。本轮同时保持对 `REQ-047..051`、`TST-031..035`、`SCN-041..047`
以及 #312 merged behavior 的 fresh reconciliation：#311 分别折入既有 `CUR-CAP-013/014/017/018/019`，
#312 折入既有 `CUR-CAP-012`；两项都是 selected-base current capability，不再把 #311 错列为 new
target delta。八组 current Test successor closure、`CUR-CAP-001..023` 与 `TARGET-DELTA-001..013`
均绑定同一 snapshot，并在 52 UC / 84 REQ / 34 NFR / 50 fixture candidate 中建立 target
requirement 与 normal-path fixture successor。旧 `9f560ec1...` 与 `d907fcc5...` snapshot 的局部结论只作
comparison。
数量、Skill id、schema/exit shape 和文件布局仅用于核对 current source coverage 与
consistency/installation，不是 capability-loss 比较集、target API、验收常量或必须保留的拆分。

### 1.1 Official Trellis stock source binding

除当前 repository authority 外，本轮还绑定一份独立的官方 Trellis stock source snapshot：
`@mindfoldhq/trellis@0.6.15`，registry `dist.integrity=
sha512-grbF8PToesHojsaWkoG4+Aupih7eZHkXH5y33uzPrWQXwIRewwlM1AoeJEttcXAia9nLZzF/ezuR338PWCKv+A==`，
capture tarball SHA-256=`7b97e4247f54e71f22ff80caa328d9e68fb81908f984f15d70a4d81cc2a0306c`
（`2026-08-25` live verification）。下列相对 package path 是 stock surface 的事实 locator；
本机安装目录只作为本轮读取载体，不是 target source、不可提交的绝对路径，也不替代未来 Design
对 marketplace/preset projection 的 canonical source 选择。后续同名版本、dist-tag、tarball
或模板集合变化都必须建立新的 package snapshot，不得只按版本字符串复用本表。

| Stock source slice | Relative package locator | Verified fact | Target use boundary |
| --- | --- | --- | --- |
| Common commands | `dist/templates/common/commands/{start,continue,finish-work}.md` | `getCommandTemplates()` discovers all three command templates and platform configurators project them according to each platform's command/skill mode | The normalized `trellis-start`, `trellis-continue` and `trellis-finish-work` surfaces are inventory assets; their semantic routing is not target authority |
| Common single-file skills | `dist/templates/common/skills/{before-dev,brainstorm,break-loop,check,update-spec}.md` | `getSkillTemplates()` discovers the five auto-trigger candidates; `wrapWithSkillFrontmatter()` supplies matcher descriptions | The target role is decided per asset below; no stock description alone may select a Guru route |
| Bundled multi-file skills | `dist/templates/common/bundled-skills/{trellis-meta,trellis-channel,trellis-session-insight,trellis-spec-bootstrap}/` | `getBundledSkillTemplates()` enumerates every bundled directory and copies its full tree | There is no generic per-project bundled-skill disable flag; retention/suppression must be handled by the supported projection/maintenance contract |
| Platform worker agents | `dist/templates/<platform>/agents/{trellis-research,trellis-implement,trellis-check}.{md,toml,json}` where emitted | Platform agent templates are separate from common auto-trigger skills and are also projected for supported agent-capable platforms; the extension is platform-specific (`Codex=.toml`, `Claude/Cursor=.md` in this snapshot) | Worker files may remain only as caller-bound providers; they cannot become a second semantic owner |
| Channel runtime workers | `dist/templates/trellis/agents/{check,implement}.md` | Channel workers are loaded by the channel runtime rather than by platform skill matching | They remain controlled worker providers and must return to the spawning Guru caller |
| Projection/update wiring | `dist/templates/common/index.js`, `dist/configurators/shared.js` | Bundled and common templates are collected into each configured platform skill root; the collection has no per-project suppression parameter | Workflow markers and launcher text alone are insufficient collision control |
| Update conflict behavior | `dist/commands/update.js`, `dist/commands/workflow.js` | Missing hashed files are reported as user-deleted/preserved; modified files require a decision; `--force` overwrites, `--create-new` writes a `.new` copy, and update creates a managed backup before writes. After `--dry-run`, the observed `MIGRATION REQUIRED` discriminator selects `trellis update --migrate --skip-all`; otherwise it selects `trellis update --skip-all`, and both branches preserve user modifications | Guru policy must preserve these upstream facts and add an explicit suppression/provenance layer; it must not treat `--force` as semantic approval or collapse the two dry-run branches |

The stock source binding is evidence for the captured package only. Any future CLI version, marketplace
source, platform collector, template set, package integrity or tarball change invalidates this slice and
requires a fresh inventory and review; the target must not silently absorb upstream drift.

#### 1.1.1 Stock control-plane ownership gate

The following ownership tuple is required for every asset before a suppression/provider action can be
considered target-current. It records current facts and the minimum target boundary; it does not claim
that a Guru mutation owner already exists:

| Ownership role | Current fact / target contract | Evidence / blocking rule |
| --- | --- | --- |
| Source owner | Official Trellis CLI collector and the captured package templates own the stock source and official regeneration | `dist/templates/**`, `dist/configurators/**`; a future package/source change invalidates this slice |
| Policy owner | `stock-policy owner` is the single Guru global workflow owner for inventory, explicit-only read binding and suppression policy | `EVO-REQ-068,070,074`; it cannot be auto-dispatched or make product/route decisions |
| Mutation/interception owner | Design must bind a named, supported Guru canonical/marketplace/preset/overlay projection owner for the exact host/path and action; the current workflow/preset do not own official `trellis-*` paths | `.trellis/workflow.md:732..740`, `trellis/presets/guru-team/README.md:910..914`; until that Design binding is current, a suppressed asset cannot become `stock_policy_current` and returns `upstream_suppression_blocked`, while a provider/explicit/worker adapter or caller binding that is missing returns `provider_boundary_blocked` |
| Host/runtime owner | Codex, Claude and Cursor collectors/hooks own their host-specific emission and native context behavior; shared `.agents/skills/**` is one projection layer | §1.2.1 host/context matrix; source-only hosts are not target coverage |

No row in §1.3 may treat `routing_patch`, `content_patch`, absence/quarantine or delete as an
executable target until the mutation/interception owner and exact projection cell are bound in Design.
The `EVO-FIX-STOCK-MAINTENANCE` fixture must exercise the missing-owner branch as well as the safe
branch: suppressed assets use `upstream_suppression_blocked`, while provider/explicit/worker assets
use `provider_boundary_blocked` when their caller-bound adapter or guard is missing. An upstream-owned
path with no supported Guru boundary remains blocked rather than being silently treated as managed.

### 1.2 Supported Guru projection and host relation

本次 Evolution 的 supported runtime host 只包括 `Codex`、`Claude` 与 `Cursor`；`Shared` 是
官方写入的 `.agents/skills/**` 共享投影层，不是第四个独立运行平台，也不得在 coverage、fixture
或成功率中重复计数。官方还会让 Gemini CLI、Pi、Kimi 等 host 读取该共享层，但它们在本候选中
只是 source-only boundary；若要支持其中任一 host，必须建立新的 source snapshot、host matrix
与 fresh Requirements review。

| Projection identity | Kind | Stock emitted path in `@mindfoldhq/trellis@0.6.15` | Host relation | Target rule |
| --- | --- | --- | --- | --- |
| `shared-skill-layer` | shared projection layer | `.agents/skills/**` | Codex、Gemini CLI、Pi、Kimi 等 host 可读取；本候选只把 Codex 作为 supported host | 与 Codex 的 common/bundled asset 只计一次；不得作为独立 top-level owner |
| `codex-host` | supported host | `.agents/skills/**`, `.codex/agents/**`, `.codex/hooks/**`, `.codex/hooks.json` | common commands 以 skill 形式落入 `.agents/skills/**`；`.codex/skills/**` 是用户自有目录，不是本版 stock projection | Guru route 选定后 stock matcher 不得改写；agent/channel 结果必须回到 Guru caller |
| `claude-host` | supported host | `.claude/skills/**`, `.claude/commands/trellis/**`, `.claude/agents/**`, `.claude/hooks/**` | `start` command 在 hooks-enabled 配置中不 emitted；hooks-disabled/no-hook 配置会重新 emitted 为 command surface；`continue`/`finish-work` 仍是 command surface | hook 过滤 start 不等于其它 stock semantic surface 已安全，任一 emission 状态仍须 policy gate |
| `cursor-host` | supported host | `.cursor/skills/**`, `.cursor/commands/trellis-*.md`, `.cursor/agents/**`, `.cursor/hooks/**` | `start` command 在 hooks-enabled 配置中不 emitted；hooks-disabled/no-hook 配置会重新 emitted 为 command surface；其它 command/skill 按配置投影 | 与 Claude 使用同一 semantic contract，不能以平台差异放宽 suppression |

为避免把“没有文件”误当作“已经安全”，每个 asset/context cell 使用以下确定性状态：
`emitted`（该 source 在该 surface 实际投影）、`not-emitted`（明确列出 host/configuration
原因）、`provider-only`（虽可投影但只能在 caller binding 下运行）或
`retained-nonsemantic`（只提供 hook/context/breadcrumb）。`main/default`、`inline`、
`sub-agent`、`channel` 与 `native context/hooks` 是独立维度；未知、未读取或只凭自然语言
推断的 cell 不能通过。

#### 1.2.1 Asset/context emission matrix

下表给出本 snapshot 的逐 asset、逐 surface 结论。`M` 表示 main/default，`I` 表示 inline；
`E`=`emitted`、`N`=`not-emitted`、`P`=`provider-only`、`R`=`retained-nonsemantic`。括号内
必须保留依据（path、hook 或 runtime boundary），后续 Design 只能细化，不得把 `N` 默认为安全。
为避免裸状态，`N[common-subagent]` 表示 common command/skill 没有 stock sub-agent emission，
`N[common-channel]` 表示没有 platform channel surface，`N[native-no-skill]` 表示该 host native
context 不执行该 Skill，`N[host-agent]` 表示只在 host agent path 发出，`N[host-channel]` 表示
只由 channel runtime 发出，`N[worker-not-shared]`/`N[worker-no-subagent]` 表示 worker 不写 shared
skill root 或不再嵌套为 platform sub-agent；`R[startup-context]`、`R[host-dispatch]` 与
`R[channel-context]` 分别表示启动上下文、host dispatch metadata 与 channel runtime context，
不拥有 semantic route。

| Stock asset | shared layer (`M/I`) | Codex host (`M/I`) | Codex sub-agent | Codex channel | Codex native | Claude host (`M/I`) | Claude sub-agent | Claude channel | Claude native | Cursor host (`M/I`) | Cursor sub-agent | Cursor channel | Cursor native |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `trellis-start` | `E/E` (`.agents/skills`) | `E/E` (`.agents/skills`, command-as-skill) | `N[common-subagent]` | `N[common-channel]` | `R[startup-context]` (Codex hook matrix: enabled/disabled/no-hook) | `N@hooks-enabled; E/E@hooks-disabled/no-hook` (hook filters or emits start; neither state is suppression by itself) | `N[common-subagent]` | `N[common-channel]` | `R[startup-context]` | `N@hooks-enabled; E/E@hooks-disabled/no-hook` (hook filters or emits start; neither state is suppression by itself) | `N[common-subagent]` | `N[common-channel]` | `R[startup-context]` |
| `trellis-continue` | `E/E` (`.agents/skills`) | `E/E` (`.agents/skills`, command-as-skill) | `N[common-subagent]` | `N[common-channel]` | `R[startup-context]` | `E/E` (`.claude/commands/trellis`) | `N[common-subagent]` | `N[common-channel]` | `R[startup-context]` | `E/E` (`.cursor/commands/trellis-*.md`) | `N[common-subagent]` | `N[common-channel]` | `R[startup-context]` |
| `trellis-finish-work` | `E/E` (`.agents/skills`) | `E/E` (`.agents/skills`, command-as-skill) | `N[common-subagent]` | `N[common-channel]` | `R[startup-context]` | `E/E` (`.claude/commands/trellis`) | `N[common-subagent]` | `N[common-channel]` | `R[startup-context]` | `E/E` (`.cursor/commands/trellis-*.md`) | `N[common-subagent]` | `N[common-channel]` | `R[startup-context]` |
| `trellis-brainstorm` | `E/E` (`.agents/skills`) | `E/E` (`.agents/skills`) | `N[common-subagent]` | `N[common-channel]` | `N[native-no-skill]` | `E/E` (`.claude/skills`) | `N[common-subagent]` | `N[common-channel]` | `N[native-no-skill]` | `E/E` (`.cursor/skills`) | `N[common-subagent]` | `N[common-channel]` | `N[native-no-skill]` |
| common `trellis-check` | `E/E` (`.agents/skills`) | `E/E` (`.agents/skills`) | `N[common-subagent]` | `N[common-channel]` | `N[native-no-skill]` | `E/E` (`.claude/skills`) | `N[common-subagent]` | `N[common-channel]` | `N[native-no-skill]` | `E/E` (`.cursor/skills`) | `N[common-subagent]` | `N[common-channel]` | `N[native-no-skill]` |
| `trellis-update-spec` | `E/E` (`.agents/skills`) | `E/E` (`.agents/skills`) | `N[common-subagent]` | `N[common-channel]` | `N[native-no-skill]` | `E/E` (`.claude/skills`) | `N[common-subagent]` | `N[common-channel]` | `N[native-no-skill]` | `E/E` (`.cursor/skills`) | `N[common-subagent]` | `N[common-channel]` | `N[native-no-skill]` |
| `trellis-before-dev` | `E/E` (`.agents/skills`) | `E/E` (`.agents/skills`) | `N[common-subagent]` | `N[common-channel]` | `N[native-no-skill]` | `E/E` (`.claude/skills`) | `N[common-subagent]` | `N[common-channel]` | `N[native-no-skill]` | `E/E` (`.cursor/skills`) | `N[common-subagent]` | `N[common-channel]` | `N[native-no-skill]` |
| `trellis-spec-bootstrap` | `E/E` (`.agents/skills`) | `E/E` (`.agents/skills`) | `N[common-subagent]` | `N[common-channel]` | `N[native-no-skill]` | `E/E` (`.claude/skills`) | `N[common-subagent]` | `N[common-channel]` | `N[native-no-skill]` | `E/E` (`.cursor/skills`) | `N[common-subagent]` | `N[common-channel]` | `N[native-no-skill]` |
| `trellis-channel` | `E/E` (`.agents/skills`) | `E/E` (`.agents/skills`) | `N[common-subagent]` | `P` (transport provider) | `N[native-no-skill]` | `E/E` (`.claude/skills`) | `N[common-subagent]` | `P` (transport provider) | `N[native-no-skill]` | `E/E` (`.cursor/skills`) | `N[common-subagent]` | `P` (transport provider) | `N[native-no-skill]` |
| `trellis-meta` | `E/E` (`.agents/skills`) | `E/E` (`.agents/skills`) | `N[common-subagent]` | `N[common-channel]` | `N[native-no-skill]` | `E/E` (`.claude/skills`) | `N[common-subagent]` | `N[common-channel]` | `N[native-no-skill]` | `E/E` (`.cursor/skills`) | `N[common-subagent]` | `N[common-channel]` | `N[native-no-skill]` |
| `trellis-session-insight` | `E/E` (`.agents/skills`) | `E/E` (`.agents/skills`) | `N[common-subagent]` | `N[common-channel]` | `N[native-no-skill]` | `E/E` (`.claude/skills`) | `N[common-subagent]` | `N[common-channel]` | `N[native-no-skill]` | `E/E` (`.cursor/skills`) | `N[common-subagent]` | `N[common-channel]` | `N[native-no-skill]` |
| `trellis-break-loop` | `E/E` (`.agents/skills`) | `E/E` (`.agents/skills`) | `N[common-subagent]` | `N[common-channel]` | `N[native-no-skill]` | `E/E` (`.claude/skills`) | `N[common-subagent]` | `N[common-channel]` | `N[native-no-skill]` | `E/E` (`.cursor/skills`) | `N[common-subagent]` | `N[common-channel]` | `N[native-no-skill]` |
| platform `trellis-research` | `N[host-agent]` (host agent path) | `P/P` (`.codex/agents`) | `P` (`.codex/agents/trellis-research`) | `N[host-channel]` | `R[host-dispatch]` | `P/P` (`.claude/agents`) | `P` (`.claude/agents/trellis-research`) | `N[host-channel]` | `R[host-dispatch]` | `P/P` (`.cursor/agents`) | `P` (`.cursor/agents/trellis-research`) | `N[host-channel]` | `R[host-dispatch]` |
| platform `trellis-implement` | `N[host-agent]` | `P/P` (`.codex/agents`) | `P` (`.codex/agents/trellis-implement`) | `N[host-channel]` | `R[host-dispatch]` | `P/P` (`.claude/agents`) | `P` (`.claude/agents/trellis-implement`) | `N[host-channel]` | `R[host-dispatch]` | `P/P` (`.cursor/agents`) | `P` (`.cursor/agents/trellis-implement`) | `N[host-channel]` | `R[host-dispatch]` |
| platform `trellis-check` | `N[host-agent]` | `P/P` (`.codex/agents`) | `P` (`.codex/agents/trellis-check`) | `N[host-channel]` | `R[host-dispatch]` | `P/P` (`.claude/agents`) | `P` (`.claude/agents/trellis-check`) | `N[host-channel]` | `R[host-dispatch]` | `P/P` (`.cursor/agents`) | `P` (`.cursor/agents/trellis-check`) | `N[host-channel]` | `R[host-dispatch]` |
| channel `check` | `N[worker-not-shared]` | `N[worker-not-shared]` | `N[worker-no-subagent]` | `P` (`.trellis/agents/check.md`) | `R[channel-context]` | `N[worker-not-shared]` | `N[worker-no-subagent]` | `P` (`.trellis/agents/check.md`) | `R[channel-context]` | `N[worker-not-shared]` | `N[worker-no-subagent]` | `P` (`.trellis/agents/check.md`) | `R[channel-context]` |
| channel `implement` | `N[worker-not-shared]` | `N[worker-not-shared]` | `N[worker-no-subagent]` | `P` (`.trellis/agents/implement.md`) | `R[channel-context]` | `N[worker-not-shared]` | `N[worker-no-subagent]` | `P` (`.trellis/agents/implement.md`) | `R[channel-context]` | `N[worker-not-shared]` | `N[worker-no-subagent]` | `P` (`.trellis/agents/implement.md`) | `R[channel-context]` |

The matrix is a source/projection fact table, not a target permission grant. An `E` cell still needs
the role and caller gate below; an `N` cell needs the stated reason; a `P` cell cannot become a top-level
route; and an `R` cell cannot select intent, scope, finding, route or side effect.

`shared layer` 与 `Codex host` 在表中故意分列：前者记录官方写入 `.agents/skills/**` 的一次
source/projection fact，后者记录 Codex 作为 supported host 对该层及其 agents/hooks 的消费关系。
两列不是两个 runtime host，也不能相加为一个额外 host；覆盖计数始终是 shared layer 一次加上
Codex、Claude、Cursor 三个 supported host。表中的每个 host 都有独立的 main/default、
sub-agent、channel 与 native context 列；这些是调用上下文维度，不是额外 host 或额外 projection。

#### 1.2.2 Codex/host hook configuration matrix

`Codex native` 不能用一个 cell 代表所有 hook 状态。以下三种正常配置必须独立读取和验证；
`hooks.json` 的实际 matcher 只是 current evidence，不授予 stock semantic ownership。

| Host/configuration | Current source fact | 必须观察的 emission/context | Suppression 判读 |
| --- | --- | --- | --- |
| Codex `hooks-enabled` | `.codex/hooks.json` 含 `UserPromptSubmit` 与 `SubagentStart`，matcher 覆盖 `trellis-implement`/`trellis-check`/`trellis-research` | shared command/Skill emission、hook context 注入、sub-agent dispatch 与 stock `trellis-start` collision | hook 过滤或 context 注入不等于 suppression；第一项 semantic 行为前仍需 redirect/quarantine/fail closed |
| Codex `hooks-disabled` | 配置明确禁用 hook，但 stock projection 文件仍可能存在 | 同上，尤其验证 command-as-skill/agent emission 是否恢复 | `not-emitted`/hook disabled 不能当作安全；未隔离则 role-local blocked |
| Codex `no-hook` | 无 `.codex/hooks.json` 或等价 hook 配置 | 同上，验证无 hook 时的 native context 缺失与 stock matcher 行为 | absence 不能当作 suppression；必须有独立 policy 结果 |
| Claude `hooks-enabled` | `trellis-start` 在 hooks-enabled 配置中由 Claude hook 过滤；其它 command surface 仍按当前 host projection 发出 | 独立观察 Claude command/skill emission、native context 与 redirect/quarantine/fail closed | hook 过滤不等于 suppression；该 host/configuration 必须在第一项 semantic 行为前隔离 |
| Claude `hooks-disabled/no-hook` | `trellis-start` 在 hooks-disabled/no-hook 配置中重新 emitted 为 Claude command surface | 独立观察 Claude command/skill emission、native context 与 redirect/quarantine/fail closed | emission 或 hook absence 不等于 suppression；该 host/configuration 必须在第一项 semantic 行为前隔离 |
| Cursor `hooks-enabled` | `trellis-start` 在 hooks-enabled 配置中由 Cursor hook 过滤；其它 command/skill surface 仍按当前 host projection 发出 | 独立观察 Cursor command/skill emission、native context 与 redirect/quarantine/fail closed | hook 过滤不等于 suppression；该 host/configuration 必须在第一项 semantic 行为前隔离 |
| Cursor `hooks-disabled/no-hook` | `trellis-start` 在 hooks-disabled/no-hook 配置中重新 emitted 为 Cursor command surface | 独立观察 Cursor command/skill emission、native context 与 redirect/quarantine/fail closed | emission 或 hook absence 不等于 suppression；该 host/configuration 必须在第一项 semantic 行为前隔离 |

每个 concrete host fixture 还必须记录一个可重放的 setup discriminator，而不是只写
`hooks-enabled` 或 `no-hook` 标签。高层 configuration 是 discriminator partition 的派生结果，不是
与七个 setup cell 再做交叉乘积的独立轴。对 Codex、Claude、Cursor 分别读取实际 host/user 配置并记录：
`user_feature_flag=on|off|unknown`、`project_hook_config=present|absent|unknown`、
`one_time_approval=granted|pending|denied|not_applicable|unknown`、实际
`emission` 与 `context_injection`。host 没有一次性批准面时只能记录
`not_applicable`，不得把缺少该面推断为 granted；该 host 的 `enabled_pending`/`enabled_denied` cell
同时明确为 N/A，enabled success 复用 `enabled_approved` cell 但记录
`one_time_approval=not_applicable`。任一 `unknown`、配置缺失但 emission 仍存在、或 setup 与观察
结果不一致，都必须得到对应 role-local blocked。每个 host 只覆盖下列实际适用组合：

| Setup discriminator | 最小 setup | 必须观察 | 结果边界 |
| --- | --- | --- | --- |
| `enabled_approved` | user feature flag on；project hook config present；host 支持 approval 时为 granted，否则为 `not_applicable` | emission、context injection、第一项 semantic 行为前 redirect/quarantine/fail-closed | 归入 `hooks-enabled`；过滤/注入仍不等于 suppression |
| `enabled_pending` | user feature flag on；project hook config present；approval=`pending`；仅适用于存在该 approval surface 的 host | emission、context injection、approval pending 对隔离结果的影响 | 归入 `hooks-enabled`；pending 不是 disabled 或 suppression；无法隔离则 role-local blocked |
| `enabled_denied` | user feature flag on；project hook config present；approval=`denied`；仅适用于存在该 approval surface 的 host | emission、context injection、approval denied 对隔离结果的影响 | 归入 `hooks-enabled`；denied 不是 disabled 或 suppression；无法隔离则 role-local blocked |
| `feature_off_config_present` | user feature flag off；project hook config present；记录 approval 的实际状态或 `not_applicable` | command/Skill 是否仍 emitted、native context 是否注入、第一项 semantic 行为前是否 redirect/quarantine/fail-closed | 归入 `hooks-disabled`；feature off 不能单独证明 suppression；不一致或未隔离则 role-local blocked |
| `feature_on_config_absent` | user feature flag on；project hook config absent；记录 approval=`not_applicable` 或实际可读状态 | command/Skill 是否仍 emitted、native context 是否缺失、第一项 semantic 行为前是否 redirect/quarantine/fail-closed | 归入 `no-hook`；config absence 不能单独证明 suppression；emission 仍存在或未隔离则 role-local blocked |
| `feature_off_config_absent` | user feature flag off；project hook config absent（no-hook）；记录 approval=`not_applicable` 或实际可读状态 | command/Skill emission、native context 缺失与第一项 semantic 行为前隔离 | 归入 `no-hook`；双重 absence 仍不能单独证明 suppression；结果不一致则 role-local blocked |
| `configuration_unknown` | 任一 setup 字段 unknown、权限不可读或配置状态无法唯一解释 | 不得继续进入 semantic 行为 | 不归入正常 configuration success；直接返回 role-local blocked，并从精确 setup repair 重入 |

### 1.3 Stock surface role inventory

下表是本轮对 `@mindfoldhq/trellis@0.6.15` 的 17 个逻辑 stock asset 的完整清单。每个 asset
恰好有一个 role；其中 `suppressed_semantic_route=9`、`provider_only=1`、
`explicit_only=2`、`controlled_worker_provider=5`。`candidate action` 是
后续 Design 的最小决策集合，不是本轮实施决定；本 inventory 不选择或排序候选 action，选择、
兼容性优先级与未选方案否决均只由 `requirement-main.md` 的 `EVO-REQ-071` 主定义。`STOCK-BIND-*`
是逐 asset 的 policy binding，
`STOCK-HANDOFF-*` 是 Requirements 交给 Design 的稳定 handoff；`design_pending` 表示当前
尚无可执行的 Guru mutation/interception owner，不表示允许自动运行。历史表中的
`STOCK-CONSUMER-*` 不是已存在的 interface/typed-exit/workflow consumer；本轮统一视为
`consumer_unbound` 的 Design handoff label，不能作为 Requirements closure 证据。真实 caller、
profile、输入、最小 result/typed exit、回程与 consumer 必须在 §1.3.1 逐项绑定；未绑定的行只
能返回 `provider_boundary_blocked` 或保持 `design_handoff`。下表之外的三类 retained
nonsemantic surface 按 host 拆成九行，不计入 17 个 semantic/provider asset，但仍必须有 source
locator、projection cell、direct consumer、preservation reason 和 fixture。

本文后文所称 `independent_invocation_entry_contract` 只引用
[`requirement-main.md`](./requirement-main.md) 的 `EVO-REQ-010/076` 主定义；inventory 仅记录
能力、fixture、owner/consumer 与 Design handoff，不重复承载 invocation identity、receipt、isolation
或 top-level route 的行为顺序。

| Stock asset | Role | Guru successor / capability | Policy binding / caller | Direct consumer | Projection cell(s) | Mutation/interception status / Design handoff | Collision risk | Candidate action for Design | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `trellis-start` (`common/commands/start.md`) | `suppressed_semantic_route` | `guru-select-workflow-mode` | `STOCK-BIND-START` / `stock-policy suppression boundary` | `guru-select-workflow-mode` | `shared-skill-layer.M/I; codex-host.M/I; claude-host.M/I; cursor-host.M/I` | `design_pending`（upstream-owned path；`STOCK-HANDOFF-001`；blocked=`upstream_suppression_blocked`） | High：自行读取上下文并选路 | routing/content patch、managed absence/quarantine、精确 allowlist delete | `EVO-FIX-STOCK-COEXISTENCE` |
| `trellis-continue` (`common/commands/continue.md`) | `suppressed_semantic_route` | `guru-discover-change-context` | `STOCK-BIND-CONTINUE` / `stock-policy suppression boundary` | `guru-discover-change-context` | `shared-skill-layer.M/I; codex-host.M/I; claude-host.M/I; cursor-host.M/I` | `design_pending`；`STOCK-HANDOFF-002`；blocked=`upstream_suppression_blocked` | High：可绕过 current recovery/entry | routing/content patch、managed absence/quarantine、精确 allowlist delete | `EVO-FIX-STOCK-COEXISTENCE`、`EVO-FIX-HISTORY-RESUME` |
| `trellis-finish-work` (`common/commands/finish-work.md`) | `suppressed_semantic_route` | `guru-finalize-task` | `STOCK-BIND-FINISH` / `stock-policy suppression boundary` | `guru-finalize-task` | `shared-skill-layer.M/I; codex-host.M/I; claude-host.M/I; cursor-host.M/I` | `design_pending`；`STOCK-HANDOFF-003`；blocked=`upstream_suppression_blocked` | High：可重复 archive/cleanup | routing/content patch、managed absence/quarantine、精确 allowlist delete | `EVO-FIX-STOCK-COEXISTENCE`、`EVO-FIX-FINISH-RECOVERY` |
| `trellis-brainstorm` (`common/skills/brainstorm.md`) | `suppressed_semantic_route` | `guru-clarify-requirements` | `STOCK-BIND-BRAINSTORM` / `stock-policy suppression boundary` | `guru-clarify-requirements` | `shared-skill-layer.M/I; codex-host.M/I; claude-host.M/I; cursor-host.M/I` | `design_pending`；`STOCK-HANDOFF-004`；blocked=`upstream_suppression_blocked` | High：形成第二 authoring/question owner | content redirect、managed absence/quarantine、精确 allowlist delete | `EVO-FIX-STOCK-COEXISTENCE`、`EVO-FIX-PLAN-NORMAL` |
| common `trellis-check` (`common/skills/check.md`) | `suppressed_semantic_route` | `guru-check-task` | `STOCK-BIND-COMMON-CHECK` / `stock-policy suppression boundary` | `guru-check-task` | `shared-skill-layer.M/I; codex-host.M/I; claude-host.M/I; cursor-host.M/I` | `design_pending`；`STOCK-HANDOFF-005`；blocked=`upstream_suppression_blocked` | High：可自行判定 finding/PASS | routing/content redirect、managed absence/quarantine、精确 allowlist delete | `EVO-FIX-STOCK-COEXISTENCE`、`EVO-FIX-BRANCH-FINDING` |
| `trellis-spec-bootstrap` (bundled skill) | `suppressed_semantic_route` | `guru-bootstrap-repository-ssot` | `STOCK-BIND-SPEC-BOOTSTRAP` / `stock-policy suppression boundary` | `guru-bootstrap-repository-ssot` | `shared-skill-layer.M/I; codex-host.M/I; claude-host.M/I; cursor-host.M/I` | `design_pending`；`STOCK-HANDOFF-006`；blocked=`upstream_suppression_blocked`；raw asset 不是 provider | High：会自行选择 spec/authority 边界并写入 `.trellis/spec` | managed absence/quarantine、精确 allowlist delete；若需非语义读取须另建 adapter identity | `EVO-FIX-STOCK-COEXISTENCE`、`EVO-FIX-SSOT-BOOTSTRAP` |
| `trellis-update-spec` (`common/skills/update-spec.md`) | `suppressed_semantic_route` | Guru-governed RDT/Architecture/code-spec contribution 后生成最小 `.trellis/spec` projection | `STOCK-BIND-UPDATE-SPEC` / `stock-policy suppression boundary` | repository RDT/Architecture/code-spec governance owner | `shared-skill-layer.M/I; codex-host.M/I; claude-host.M/I; cursor-host.M/I` | `design_pending`；`STOCK-HANDOFF-007`；blocked=`upstream_suppression_blocked`；raw write surface 不保留 | High：可直接写 spec 并形成第二 Docs authority | managed absence/quarantine、精确 allowlist delete；必要启发式移入 Guru-owned source | `EVO-FIX-STOCK-COEXISTENCE`、`EVO-FIX-RDT-LIFECYCLE` |
| `trellis-before-dev` (`common/skills/before-dev.md`) | `suppressed_semantic_route` | `EVO-REQ-026` 的 Guru-owned `implementation_context`，同时服务 task-free 与标准 Phase 2 | `STOCK-BIND-BEFORE-DEV` / `stock-policy suppression boundary` | 每次 invocation 绑定的 exact implementation owner | `shared-skill-layer.M/I; codex-host.M/I; claude-host.M/I; cursor-host.M/I` | `design_pending`；`STOCK-HANDOFF-008`；blocked=`upstream_suppression_blocked`；raw provider identity 不保留 | High：自动匹配会建立第二套 spec 全文读取链 | managed absence/quarantine、精确 allowlist delete；能力由 Guru projection 承接 | `EVO-FIX-STOCK-COEXISTENCE`、`EVO-FIX-FULL-NORMAL` |
| `trellis-channel` (bundled skill) | `provider_only` | channel transport capability | `STOCK-BIND-CHANNEL` / `stock-policy channel transport binding` | `consumer_unbound`（历史 label=`STOCK-CONSUMER-CHANNEL-RESULT`；spawning Guru caller required） | `shared-skill-layer.M/I; codex-host.channel; claude-host.channel; cursor-host.channel` | `design_pending`（transport adapter；`STOCK-HANDOFF-009`；blocked=`provider_boundary_blocked`） | Medium：可能自管 worker route/progress | caller-bound transport adapter、non-auto projection | `EVO-FIX-STOCK-COEXISTENCE`、`EVO-FIX-PARALLEL` |
| `trellis-meta` (bundled skill) | `suppressed_semantic_route` | Guru-owned lazy read-only Trellis reference projection；写请求进入 Guru `new change`/active lifecycle | `STOCK-BIND-META` / `stock-policy suppression boundary` | read -> direct-answer/current caller；write -> exact new-change/active lifecycle owner | `shared-skill-layer.M/I; codex-host.M/I; claude-host.M/I; cursor-host.M/I` | `design_pending`；`STOCK-HANDOFF-010`；blocked=`upstream_suppression_blocked`；raw callable/write surface 不保留 | High：可把说明请求变成 extension 修改并与 Guru lifecycle 重叠 | managed absence/quarantine、精确 allowlist delete；只读能力移入 Guru-owned lazy reference | `EVO-FIX-STOCK-COEXISTENCE` |
| `trellis-session-insight` (bundled skill) | `explicit_only` | memory-query capability | `STOCK-BIND-SESSION-INSIGHT` / `stock-policy explicit binding` | `consumer_unbound`（历史 label=`STOCK-CONSUMER-SESSION-RESULT`；standalone read -> direct-answer owner；embedded -> exact caller handoff） | `shared-skill-layer.M/I; codex-host.M/I; claude-host.M/I; cursor-host.M/I` | `design_pending`（non-auto memory binding；`STOCK-HANDOFF-011`；blocked=`provider_boundary_blocked`） | Medium：会把普通问题改成历史检索 | explicit-only guarded projection | `EVO-FIX-STOCK-COEXISTENCE` |
| `trellis-break-loop` (`common/skills/break-loop.md`) | `explicit_only` | explicit read-only diagnosis plus follow-up recommendation | `STOCK-BIND-BREAK-LOOP` / `stock-policy explicit binding` | `consumer_unbound`（历史 label=`STOCK-CONSUMER-BREAK-LOOP-RESULT`；standalone diagnosis -> direct-answer owner；embedded read-only result -> exact active caller；write intent -> pre-invocation Guru route） | `shared-skill-layer.M/I; codex-host.M/I; claude-host.M/I; cursor-host.M/I` | `design_pending`（diagnostic-only/follow-up-redirect guard；`STOCK-HANDOFF-012`；blocked=`provider_boundary_blocked`） | Medium：自动重复分析或升级成改动 | explicit-only guarded read projection；write intent 在 raw invocation 前回 Guru new change/active caller | `EVO-FIX-STOCK-COEXISTENCE` |
| platform `trellis-research` | `controlled_worker_provider` | `guru-discover-change-context` observation | `STOCK-BIND-RESEARCH-WORKER` / `guru-discover-change-context` | `guru-discover-change-context` | `codex-host.agent; claude-host.agent; cursor-host.agent` | `design_pending`（worker adapter；`STOCK-HANDOFF-013`；blocked=`provider_boundary_blocked`） | Medium：无 caller 时可改 scope/提问 | caller-bound worker projection | `EVO-FIX-STOCK-COEXISTENCE`、`EVO-FIX-FULL-NORMAL` |
| platform `trellis-implement` | `controlled_worker_provider` | task-free 或标准 Phase 2 implementation worker execution | `STOCK-BIND-IMPLEMENT-WORKER` / exact implementation caller per invocation | exact implementation caller（task-free 或标准 Phase 2；每次调用恰好一个） | `codex-host.agent; claude-host.agent; cursor-host.agent` | `design_pending`（worker adapter；`STOCK-HANDOFF-014`；标准 Phase 2 caller 当前为 `current_drift`；blocked=`provider_boundary_blocked`） | High：可自编辑、扩大 scope 或继续阶段 | caller/scope-bound worker projection | `EVO-FIX-STOCK-COEXISTENCE`、`EVO-FIX-BRANCH-FINDING` |
| platform `trellis-check` | `controlled_worker_provider` | `guru-check-task` observation | `STOCK-BIND-CHECK-WORKER` / `guru-check-task` | `guru-check-task` | `codex-host.agent; claude-host.agent; cursor-host.agent` | `design_pending`（worker adapter；`STOCK-HANDOFF-015`；blocked=`provider_boundary_blocked`） | High：可自行判定 PASS/finding | caller-bound observation projection | `EVO-FIX-STOCK-COEXISTENCE`、`EVO-FIX-BRANCH-FINDING` |
| channel `check` (`trellis/agents/check.md`) | `controlled_worker_provider` | `guru-check-task` | `STOCK-BIND-CHANNEL-CHECK` / `guru-check-task` | `guru-check-task` | `codex-host.channel; claude-host.channel; cursor-host.channel` | `design_pending`（channel worker adapter；`STOCK-HANDOFF-016`；blocked=`provider_boundary_blocked`） | Medium-high：可形成第二 check owner | spawning-caller-bound channel projection | `EVO-FIX-STOCK-COEXISTENCE`、`EVO-FIX-PARALLEL` |
| channel `implement` (`trellis/agents/implement.md`) | `controlled_worker_provider` | task-free 或标准 Phase 2 implementation worker execution | `STOCK-BIND-CHANNEL-IMPLEMENT` / exact implementation caller per invocation | exact spawning implementation owner（task-free 或标准 Phase 2；每次恰好一个） | `codex-host.channel; claude-host.channel; cursor-host.channel` | `design_pending`（channel worker adapter；`STOCK-HANDOFF-017`；标准 Phase 2 caller 当前为 `current_drift`；blocked=`provider_boundary_blocked`） | High：自编辑/自验收绕过 Guru scope/check | spawning-caller-bound channel projection | `EVO-FIX-STOCK-COEXISTENCE`、`EVO-FIX-PARALLEL` |

#### 1.3.1 Caller/profile/result/consumer binding

下表把 `provider_only`、`explicit_only` 与 `controlled_worker_provider` 的 caller 词汇收敛为
可验收的调用合同。九项 `suppressed_semantic_route` 不运行 raw caller/profile；其中新增抑制的
`trellis-before-dev`、`trellis-update-spec` 与 `trellis-meta` 分别由 Guru-owned
`implementation_context`、RDT/Architecture/code-spec contribution-to-projection、lazy read-only
reference + new-change lifecycle 承接可观察能力。`current evidence` 只记录 current
snapshot 是否已经存在真实调用链；`design_handoff` 是明确的待绑定边界，不是 active closure。
`typed result/exit` 是最小回程形状，不能让 worker/provider 取得 semantic ownership。

| Asset / worker | Current caller evidence | Required input profile | Minimal result / typed exit | Unique consumer / return | Status |
| --- | --- | --- | --- | --- | --- |
| `trellis-channel` | channel runtime exists; no universal standalone semantic caller | `channel_transport` + spawning caller/handle | `channel_transport_result` or `provider_boundary_blocked` | exact spawning Guru caller; never a top-level route | `consumer_unbound` / `design_handoff` |
| platform `trellis-research` | workflow dispatch text names configured Trellis research worker | `research_observation` + approved scope/source identity | `research_observation_returned` or `provider_boundary_blocked` | `guru-discover-change-context` | `design_handoff` until adapter contract is named |
| platform `trellis-implement` / task-free | `guru-execute-task-free-change` is the available bounded implementation caller | `approved_plan_edit` + exact task/scope | `worker_terminal_result` or `provider_boundary_blocked` | `guru-execute-task-free-change` | `design_handoff` until worker adapter is named |
| platform `trellis-implement` / standard Phase 2 | workflow says “use configured ... implement agents”; no Guru coordinator package is present | `approved_plan_edit` + exact task/scope | `worker_terminal_result` or `provider_boundary_blocked` | standard implementation owner; current `guru-phase2-implementation-coordinator` reference is `current_drift` | `current_drift` / `design_handoff` |
| platform `trellis-check` | workflow dispatch text and `guru-check-task` contract exist; worker result shape is not a Guru public exit | `approved_plan_check` + exact task/diff | `worker_check_evidence` or `provider_boundary_blocked` | `guru-check-task` / phase-2 check owner | `design_handoff` until typed projection is named |
| channel `check` | `.trellis/agents/check.md` is a channel worker; spawning caller is not encoded in the stock file | `channel_check` + spawning caller/task | `channel_check_evidence` or `provider_boundary_blocked` | spawning `guru-check-task` caller | `consumer_unbound` / `design_handoff` |
| channel `implement` / task-free | `.trellis/agents/implement.md` is a channel worker; spawning caller is not encoded in the stock file | `channel_implement_task_free` + approved scope | `channel_implement_result` or `provider_boundary_blocked` | spawning `guru-execute-task-free-change` caller | `consumer_unbound` / `design_handoff` |
| channel `implement` / standard Phase 2 | stock worker has no Guru standard-phase caller binding; current coordinator reference is drift | `channel_implement_standard_phase2` + approved task/scope | `channel_implement_result` or `provider_boundary_blocked` | exact standard Phase 2 implementation owner; no autonomous route | `current_drift` / `design_handoff` |
| `trellis-session-insight` / standalone | no active Guru Skill/interface consumer found in frozen package | `explicit_history_query_standalone` | `explicit_provider_result_current` or `provider_boundary_blocked` | direct-answer owner；result consumption completes the invocation | `consumer_unbound` / `design_handoff` |
| `trellis-session-insight` / embedded | no active Guru Skill/interface consumer found in frozen package | `explicit_history_query_embedded` + exact active caller | `provider_result_current` or `provider_boundary_blocked` | `returned_to_unique_caller` -> exact active caller | `consumer_unbound` / `design_handoff` |
| `trellis-break-loop` / standalone | no active Guru Skill/interface consumer found in frozen package | `explicit_diagnostic_query_standalone` | `explicit_provider_result_current` or `provider_boundary_blocked` | direct-answer owner；read-only result consumption completes the invocation | `consumer_unbound` / `design_handoff` |
| `trellis-break-loop` / embedded | no active Guru Skill/interface consumer found in frozen package | `explicit_diagnostic_query_embedded` + exact active caller | `provider_result_current` or `provider_boundary_blocked` | `returned_to_unique_caller` -> exact active caller；write intent is reclassified before raw invocation | `consumer_unbound` / `design_handoff` |

`guru-phase2-implementation-coordinator` 的 absence 是 current workflow/schema drift；它不能被
Requirements 文字自动“创建”。在 Design 绑定真实 caller、interface/schema/typed exit 和唯一
consumer 前，相关 worker 行只能作为 handoff，不能被 fixture 或 NFR 计为已完成。

历史 `STOCK-CONSUMER-*` label 对仍保留的 explicit/provider asset 只表示待绑定的 result 接收槽，不是
当前接口或 typed exit。Requirements 只规定最小 projection：standalone exact explicit-only 只读请求经
`explicit_provider_result_current` 投影给 direct-answer owner 并完成 invocation；channel/worker 或
embedded read-only 调用经 `returned_to_unique_caller` 回 exact caller；任何写入意图在 raw explicit
invocation 前回到 `new change`/active caller。只有 §1.3.1 绑定了真实 caller/profile/input/
typed result/exit/consumer 后，该行才可在 Design/implementation 阶段变为 current；本 inventory
不把 handoff label 变成 semantic owner，也不声称当前已经闭环。
上述 standalone/embedded profile 行仍只代表两个 logical explicit-only asset，不改变 `explicit=2`
的 role 计数。durable archive/Finish/disposition history query 继续由顶层 history/resume route 拥有，
不会把 standalone session-insight result 改写为 history terminal。

以下三类是保留但不计入上述 17 个 semantic/provider asset 的 `retained_nonsemantic` surface。
每一类按 Codex、Claude、Cursor 拆成独立 host row；表中的 `STOCK-HANDOFF-R01..R09` 是本
Requirements 交给 Design 的 handoff projection identity，不是 current interface、typed exit 或
已实现 direct consumer。每个 row 在下方 handoff contract 中显式绑定待选 owner、最小输入/结果、
唯一回程和 blocked 条件；在该绑定完成前不得声明 `host-native-current` 或 `policy-read-current`：

| Nonsemantic surface | Host / projection cell | Source locator | Direct consumer | Mutation/interception status / Design handoff | Preservation reason | Fixture | Forbidden behavior |
| --- | --- | --- | --- | --- | --- | --- | --- |
| official hooks | Codex / `codex-host.native` | `.codex/hooks/**`, `hooks.json` | handoff projection `STOCK-HANDOFF-R01` (not a current consumer) | `design_handoff`; blocked=`retained_context_blocked` until binding | 注入 workflow/session/sub-agent context | `EVO-FIX-STOCK-COEXISTENCE` | 选择 intent、scope、finding、route 或副作用 |
| official hooks | Claude / `claude-host.native` | `.claude/hooks/**`, settings | handoff projection `STOCK-HANDOFF-R02` (not a current consumer) | `design_handoff`; blocked=`retained_context_blocked` until binding | 注入 workflow/session/sub-agent context | `EVO-FIX-STOCK-COEXISTENCE` | 选择 intent、scope、finding、route 或副作用 |
| official hooks | Cursor / `cursor-host.native` | `.cursor/hooks/**`, config | handoff projection `STOCK-HANDOFF-R03` (not a current consumer) | `design_handoff`; blocked=`retained_context_blocked` until binding | 注入 workflow/session/sub-agent context | `EVO-FIX-STOCK-COEXISTENCE` | 选择 intent、scope、finding、route 或副作用 |
| session/native context injection | Codex / `codex-host.native` | Codex session/native path | handoff projection `STOCK-HANDOFF-R04` (not a current consumer) | `design_handoff`; blocked=`retained_context_blocked` until binding | 保留启动时可观察上下文，不制造第二入口 | `EVO-FIX-STOCK-COEXISTENCE`、`EVO-FIX-STOCK-MAINTENANCE` | 自行执行 semantic Skill 或改变已选 route |
| session/native context injection | Claude / `claude-host.native` | Claude hook/session path | handoff projection `STOCK-HANDOFF-R05` (not a current consumer) | `design_handoff`; blocked=`retained_context_blocked` until binding | 保留启动时可观察上下文，不制造第二入口 | `EVO-FIX-STOCK-COEXISTENCE`、`EVO-FIX-STOCK-MAINTENANCE` | 自行执行 semantic Skill 或改变已选 route |
| session/native context injection | Cursor / `cursor-host.native` | Cursor hook/session path | handoff projection `STOCK-HANDOFF-R06` (not a current consumer) | `design_handoff`; blocked=`retained_context_blocked` until binding | 保留启动时可观察上下文，不制造第二入口 | `EVO-FIX-STOCK-COEXISTENCE`、`EVO-FIX-STOCK-MAINTENANCE` | 自行执行 semantic Skill 或改变已选 route |
| workflow breadcrumb/context | Codex / `shared-skill-layer.workflow` | `.trellis/workflow.md`, marker | handoff projection `STOCK-HANDOFF-R07` (not a current consumer) | `design_handoff`; blocked=`retained_context_blocked` until binding | 让 Codex Guru entry 读取当前 phase/route 状态 | `EVO-FIX-STOCK-MAINTENANCE` | 代替 Guru semantic judgment 或 provider binding |
| workflow breadcrumb/context | Claude / `shared-skill-layer.workflow` | `.trellis/workflow.md`, marker | handoff projection `STOCK-HANDOFF-R08` (not a current consumer) | `design_handoff`; blocked=`retained_context_blocked` until binding | 让 Claude Guru entry 读取当前 phase/route 状态 | `EVO-FIX-STOCK-MAINTENANCE` | 代替 Guru semantic judgment 或 provider binding |
| workflow breadcrumb/context | Cursor / `shared-skill-layer.workflow` | `.trellis/workflow.md`, marker | handoff projection `STOCK-HANDOFF-R09` (not a current consumer) | `design_handoff`; blocked=`retained_context_blocked` until binding | 让 Cursor Guru entry 读取当前 phase/route 状态 | `EVO-FIX-STOCK-MAINTENANCE` | 代替 Guru semantic judgment 或 provider binding |

#### 1.3.2 Retained host handoff contract

下表是九个 retained row 的最小 handoff projection。它只定义 Requirements 到 Design 的边界，
不把抽象 label 伪装成 runtime consumer；Design 必须为每行选择并证明真实 host/policy owner，或
保持下表的 `design_handoff`/`retained_context_blocked` 结果。`retained_context_current` 只能在
owner、输入、结果、回程和 source/projection identity 均 current 后成立。

| Handoff | Host/projection | Required owner boundary | Minimal input | Minimal result | Unique consumer/re-entry | Missing/unsafe result |
| --- | --- | --- | --- | --- | --- | --- |
| `STOCK-HANDOFF-R01` | Codex official hooks | Codex host-policy owner | host/config identity, hook enablement/approval state, emitted/context state, source locator | `retained_context_current` or `retained_context_blocked` | Codex host-policy caller; exact hook action re-entry | `design_handoff` until real owner is bound; then `retained_context_blocked` |
| `STOCK-HANDOFF-R02` | Claude official hooks | Claude host-policy owner | host/config identity, hook enablement/approval state, emitted/context state, source locator | `retained_context_current` or `retained_context_blocked` | Claude host-policy caller; exact hook action re-entry | `design_handoff` until real owner is bound; then `retained_context_blocked` |
| `STOCK-HANDOFF-R03` | Cursor official hooks | Cursor host-policy owner | host/config identity, hook enablement/approval state, emitted/context state, source locator | `retained_context_current` or `retained_context_blocked` | Cursor host-policy caller; exact hook action re-entry | `design_handoff` until real owner is bound; then `retained_context_blocked` |
| `STOCK-HANDOFF-R04` | Codex session/native context | Codex host-context owner | session identity, native context state, source/projection identity | `retained_context_current` or `retained_context_blocked` | Codex host-context caller; exact context reconcile re-entry | `design_handoff` until real owner is bound; then `retained_context_blocked` |
| `STOCK-HANDOFF-R05` | Claude session/native context | Claude host-context owner | session identity, native context state, source/projection identity | `retained_context_current` or `retained_context_blocked` | Claude host-context caller; exact context reconcile re-entry | `design_handoff` until real owner is bound; then `retained_context_blocked` |
| `STOCK-HANDOFF-R06` | Cursor session/native context | Cursor host-context owner | session identity, native context state, source/projection identity | `retained_context_current` or `retained_context_blocked` | Cursor host-context caller; exact context reconcile re-entry | `design_handoff` until real owner is bound; then `retained_context_blocked` |
| `STOCK-HANDOFF-R07` | Codex workflow breadcrumb | Codex workflow-policy owner | workflow identity, marker/phase state, source locator | `retained_context_current` or `retained_context_blocked` | Codex workflow-policy caller; exact breadcrumb read/reconcile re-entry | `design_handoff` until real owner is bound; then `retained_context_blocked` |
| `STOCK-HANDOFF-R08` | Claude workflow breadcrumb | Claude workflow-policy owner | workflow identity, marker/phase state, source locator | `retained_context_current` or `retained_context_blocked` | Claude workflow-policy caller; exact breadcrumb read/reconcile re-entry | `design_handoff` until real owner is bound; then `retained_context_blocked` |
| `STOCK-HANDOFF-R09` | Cursor workflow breadcrumb | Cursor workflow-policy owner | workflow identity, marker/phase state, source locator | `retained_context_current` or `retained_context_blocked` | Cursor workflow-policy caller; exact breadcrumb read/reconcile re-entry | `design_handoff` until real owner is bound; then `retained_context_blocked` |

每个 retained surface 的 host cell、direct consumer、preservation reason 与 fixture 必须逐项
绑定或明确标记为 handoff；未知、重复或无法说明来源的 cell 进入 `retained_context_blocked`，不得用 generic
“hook/context 保留”摘要通过闭包，也不得把 retained row 误算为 suppressed asset。被动
startup/session/native context 即使保留，也只能作为 context 输入，不能作为普通用户请求的
caller、consumer 或 source-rank-1 stimulus。

retained row 的 `context_preserve`/`context_reconcile` 是 host-context action，不属于 17 个
logical asset 的 semantic role，也不能借用 provider-only 的 consumer。其 action state 必须按
`completed`/`pending`/`unknown` 记录，并分别保存 `file_state`、`context_state`、`sidecar_state`；
复用仍 current 的 policy/authority context；仅在 host identity、context/sidecar state 或
decision-relevant facts 变化、过期或未知时定向 fresh reread；仍无法安全恢复时只得到
`retained_context_blocked`，修复后从同一 host/policy consumer 重入。17 个 role row 的 action
family 则按主需求 `EVO-REQ-072` 记录，inventory 只核对其存在、唯一 owner 和 fixture，不另立
action authority。

#### 1.4 Stock role recommendation summary

以下摘要把本轮研究得到的“使用、替代、仅作 provider、仅显式保留”结论分组，方便后续
Design 逐项选择载体；它引用 1.3 的逐 asset 主表，不另立一套 role authority：

| Recommendation | Stock assets | Target treatment | Reason / Guru owner |
| --- | --- | --- | --- |
| Guru 完全替代并抑制 | `trellis-start`, `trellis-continue`, `trellis-finish-work`, `trellis-brainstorm`, common `trellis-check`, raw `trellis-spec-bootstrap`, raw `trellis-before-dev`, raw `trellis-update-spec`, raw `trellis-meta` | `suppressed_semantic_route`（九项）；逐项比较 routing/content patch、managed absence/quarantine 与精确 allowlist delete | Guru entry/lifecycle、`guru-clarify-requirements`、`guru-check-task`、`guru-bootstrap-repository-ssot`、`guru-finalize-task`、Guru-owned `implementation_context`、RDT/Architecture/code-spec governance 与 lazy reference/new-change owner 完整承接可观察能力；raw identity、auto-match 与第二 authority/read chain 不保留 |
| 只作为 caller-bound provider | `trellis-channel`, platform `trellis-research`, `trellis-implement`, `trellis-check`, channel `check`, channel `implement` | `provider_only` 或 `controlled_worker_provider`；必须有 Guru-owned adapter/binding；platform/channel `implement` 都要分别覆盖 task-free 与标准 Phase 2 caller；无法去除 scope/authoring/write/approval decision 时 `provider_boundary_blocked` | 只保留 transport 或 worker observation/execution；结果回到每次调用绑定的唯一 Guru caller |
| 仅明确调用时保留 | `trellis-session-insight`, `trellis-break-loop` | `explicit_only`；普通自然语言不得自动恢复；必要时由 managed quarantine/精确 allowlist 保护 | 分别保留 `trellis mem` 历史检索与只读诊断/follow-up 建议；写入意图在 raw invocation 前回 Guru owner，不取得 RDT/Architecture/product/route authority |
| 保留但不参与语义路由 | official hooks、session/native context injection、workflow breadcrumb/context | `retained_nonsemantic`；不计入 17 个 logical asset 的 role 数，但逐项保留 source/consumer/fixture | 仅注入上下文、phase 或 transport metadata；不得选择 intent、scope、finding、route 或副作用 |

该分组是当前 frozen `0.6.15` stock snapshot 上的 target recommendation，不表示任何 patch、删除、
adapter 或 quarantine 已实现；后续 Design 必须为每个 asset 给出载体、迁移和 update/upgrade/reapply
恢复方案，并保留用户修改保护。

本段只定义 candidate action 词汇和 inventory 投影，不定义 action 的选择或优先级；选择与兼容性理由
必须回指 `requirement-main.md` 的 `EVO-REQ-071`。词汇含义为：`routing_patch` 是在第一项 semantic 行为前把匹配重定向到
Guru owner；`content_patch` 是只修改 Guru canonical/preset/installed projection 的可重应用内容；
managed `absence/quarantine` 是由 Guru preset 以 provenance 管理的缺席或隔离；精确 allowlist
delete 只能删除明确 source/version/path 且不匹配用户修改的 stock asset；`retain explicit-only`
只允许明确 caller 调用。未选 action 不要求实现或单独验证；Design 按 `EVO-REQ-071` 记录选择和否决理由。表中同一 successor contract 下列出的多个 Guru skill 是内部参与者，不能
形成多个 semantic owner。`trellis-brainstorm` 属于必须由 Guru authoring 完全替代的
`suppressed_semantic_route`：`guru-clarify-requirements` 不得在 target runtime 继续加载它作为
questioning provider；可复用的提问启发式必须进入 Guru-owned source，且不保留对 stock 文件的
运行时依赖。raw `trellis-spec-bootstrap` 的现有显式调用只算 current implementation fact，不算 target
provider contract；即使 Design 产生独立 non-semantic adapter，raw asset 仍按 suppression 验收。任何候选都不得修改全局
npm 安装目录、`node_modules` 或 upstream source。

#### 1.5 Evolution prerequisite capability binding

下表把 #311/#312 的 live Issue、PR/merge 与 selected-base facts 分成六个不可互相替代的维度：
`accepted_implementation_scope`、`exact_merge_identity`、`merge_reachability`、
`accepted_scope_findings`、`issue_lifecycle` 与 `open_followup_only`。Issue 的 `OPEN/CLOSED`
状态只保留为 lifecycle fact；它不能替代 accepted scope、merge identity、reachability 或
accepted-scope verification。当前 selected base `5650df47…` 已包含两个 prerequisite merge、PR #317
platform-selection advance 与 PR #318 fact-only caller-inventory/provenance correction，本 inventory 已从该 exact base 完成 fresh rebind、merged behavior
reconciliation 与全部 capability requirement/normal-path fixture 零差集。两项 prerequisite 在本表中均是
`selected_base_current_capability`；fresh Requirements semantic、Strict technical 与确定性闭包审核已针对
同一 exact candidate 通过，因此当前 trace 状态为 `requirements_trace_ready_for_design`。

| Prerequisite | Six-dimension current classification | Inventory state | Current observable capability | Existing target allocation | Required zero-loss evidence |
| --- | --- | --- | --- | --- | --- |
| #311 installed publication provenance source/target separation and verifier failure evidence | `accepted_implementation_scope=current`; `exact_merge_identity=PR-313/21c7da1…`; `merge_reachability=current` from selected base; `accepted_scope_findings=none reported`; `issue_lifecycle=OPEN`; `open_followup_only=true`（production release、错误文件重试、Issue closure） | `selected_base_current_capability` | installed runtime 从 installation manifest/managed-byte/source-commit identity 解析 immutable extension source，和 target reviewed checkout 分开验证；只允许 provenance 字段变化，reviewed-content identity 保持并继续到唯一 publication/Draft PR/archive+push/Ready/`ready_for_merge`，completed mutation 不重放，self-hosted path 保持；standalone verifier 在 cleanup 前形成 non-null structured failure evidence | `CUR-CAP-013,014,017,018,019`; `EVO-REQ-037,053,082..083`; no separate target delta | `EVO-FIX-INSTALLED-PROVENANCE-PUBLICATION`, `EVO-FIX-VERIFIER-FAILURE-EVIDENCE`, `EVO-FIX-EVOLUTION-PREREQUISITE` |
| #312 active-task workspace continuity after base merge | `accepted_implementation_scope=current`; `exact_merge_identity=PR-314/3efcce7…`; `merge_reachability=current` from selected base; `accepted_scope_findings=none reported`; `issue_lifecycle=CLOSED`; `open_followup_only=N/A` | `selected_base_current_capability` | current-base-tracked 且逐路径 clean 的同 task 文件不阻断原 active task/worktree；source/task worktree unrelated dirty 保持隔离且不被误分类/修改；dirty/untracked same-task、review/check metadata 与 cwd/runtime/worktree/task/branch mismatch 仍阻断 | `CUR-CAP-012`; existing base/continuity successor `EVO-REQ-032,082`; no fifth core capability or separate delta | `EVO-FIX-BASE-EVOLUTION`, `EVO-FIX-EVOLUTION-PREREQUISITE` |

PR #317 不是第三个 prerequisite，也不新增 target delta。它把 selected-base installed publication 的
platform-selection observable behavior 补入 `CUR-CAP-013/014/017`：parent manifest 三处 exact selection
一致且合法时，`all_platforms=true` 只映射完整 canonical set，其余 selection 以 repeated `--platform`
保持不变；invalid identity 在 source checkout/preset apply/commit 前 fail closed。target allocation 为
`EVO-REQ-084` / `EVO-NFR-034`，仍由 `EVO-FIX-INSTALLED-PROVENANCE-PUBLICATION` 承接。

当前六维 classification 已移除“OPEN 即未合入”的错误假设：#311 的 OPEN follow-up-only 不单独
阻断，#312 的 CLOSED 也不自动证明全部外部验证完成。若任一 accepted scope 未完成、accepted-scope
finding 未解决、exact merge identity 不可验证、merge 不可从 selected base 到达，或 OPEN 的
follow-up 边界不清，必须得到 `evolution_prerequisite_blocked`；若六维事实 current，则只消除
merge/lifecycle 这一层阻断。本轮 fresh rebind、merged behavior reconciliation 与
requirement/normal-path fixture 零差集已经闭合；fresh Requirements 双审与确定性闭包已通过，本 inventory 当前为
`requirements_trace_ready_for_design`，pre-`REQ-REV-142` Design mapping/review 仍只能标为 stale。
Requirements 不预选 #311 的 Evolution owner、Skill、DTO 或 script。

## 2. Classification

| Classification | 含义 |
| --- | --- |
| `preserved_current` | current 可观察结果与正常场景必须在 target 保持，允许内部 owner 或合同形态变化 |
| `replaced_contract_shape` | 能力结果必须保留，但 current Skill/schema/exit/handoff/文件拆分明确由单一新合同替换 |
| `new_target` | 本轮新增或显著加强的目标；不得把任意 selected-base current capability 或 PASS 冒充为 `new_target` |
| `intentionally_not_retained` | 经产品决定不保留的旧合同、冗余过程或实现形态；不得作为 capability loss 阻塞迁移 |

一项能力可以同时是 `preserved_current + replaced_contract_shape`：前者约束用户结果，后者
明确旧 API/owner/handoff 不具有兼容权利。

本台账的 Skill/interface/schema/command/distribution/installed successor 完整性属于 trace 与
consistency/installation 合同，不等同于 capability loss。capability-loss gate 只比较
`workflow`、`task_data`、`docs_authority`；两类 gate 任一漂移都阻断，但后一类 drift 本身不构成
capability loss。

## 3. Current 可观察能力总表

| Stable capability id | Current 可观察能力 | Classification | Current authority / evidence | 上一版 inventory 对应 | Target successor | Acceptance fixtures | 保留与 loss 边界 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `CUR-CAP-001` | 通过官方 Trellis workflow/spec marketplace、Markdown workflow、Skill、preset/overlay 和 deterministic companion runtime 扩展，不修改上游源码或 npm 安装 | `preserved_current + replaced_contract_shape` | `REQ-002,006,013`; `BEH-009`; `NFR-001` | Registry/package/platform closure | `EVO-REQ-051..055` | `EVO-FIX-PROJECTION`, `EVO-FIX-CLEAN-INSTALL`, `EVO-FIX-MIGRATION` | 保留官方扩展面与 canonical source；不保留 current package/API layout |
| `CUR-CAP-002` | global workflow 与 step-local semantic owner 分层，AI 判断与 deterministic executor/validator 分层，typed route 未映射时 fail closed | `preserved_current + replaced_contract_shape` | `REQ-003..004,008`; `NFR-002..003`; `CASE-001..002` | 全部 active interfaces 的 consumer closure | `EVO-REQ-010,024..025,034,051`; `EVO-NFR-007,014..015` | `EVO-FIX-TASK-FREE`, `EVO-FIX-FRESH-SCOPE`, `EVO-FIX-BRANCH-FINDING`, `EVO-FIX-PROVIDER-RECOVERY`, `EVO-FIX-RDT-LIFECYCLE` | 保留唯一 semantic owner、唯一 consumer/stop 与脚本边界；不保留 current Skill/exit/schema id |
| `CUR-CAP-003` | 标准请求完成 mode selection、current change context、需求澄清、duplicate/prerequisite/scope readiness，再进入资源准备 | `preserved_current + replaced_contract_shape` | `REQ-001,005,012,044..045`; `BEH-001,006`; `SCN-001,004` | `guru-select-workflow-mode`, `guru-discover-change-context`, `guru-clarify-requirements`, `guru-review-change-request` | `EVO-REQ-002..010,059` | `EVO-FIX-INTAKE-CLEAR`, `EVO-FIX-INTAKE-REVIEWED-DESIGN`, `EVO-FIX-INTAKE-UNCLEAR`, `EVO-FIX-CHANGE-REQUEST` | 保留 clear/unclear/duplicate/prerequisite/recovery 结果；target 将 active duplicate、completed duplicate、scope clarification、prerequisite blocked、resolution blocked 与 ready 分开，分别返回 exact owner、terminal 或 readiness re-entry，不创建重复资源；不保留 current Phase 0 顺序、aggregate 或 private result |
| `CUR-CAP-004` | selected base 按明确 precedence 绑定 exact authority checkout；detached invocation 可读取/同步 authority，unsafe/ambiguous/dirty/mismatch fail closed | `preserved_current + replaced_contract_shape` | `REQ-036..045`; `SCN-034..040`; `TST-027..030` | `guru-sync-base`, `guru-discover-change-context` | `EVO-REQ-009,060`; `EVO-NFR-010` | `EVO-FIX-DETACHED-READ`, `EVO-FIX-BASE-REFRESH` | 保留 selection/binding/safe refresh 与 downstream freshness；不保留 Sync/Discovery producer-private payload |
| `CUR-CAP-005` | requirement 信息不足时交互澄清，明确 contract wording 与 change readiness 可执行有界 semantic review | `preserved_current + replaced_contract_shape` | `REQ-001,003..005`; `BEH-001`; canonical active interfaces | `guru-clarify-requirements`, `guru-review-contract-wording`, `guru-review-change-request` | `EVO-REQ-003..008,057,059` | `EVO-FIX-INTAKE-UNCLEAR`, `EVO-FIX-WORDING-EXPLICIT`, `EVO-FIX-CHANGE-REQUEST` | 保留交互式澄清和显式 wording specialist review；top-level specialist 只承接 `REQ-UC-EVO-037..038` 两个受支持 profile，通用只读 Requirements/Design/代码/Architecture review 仍直接回答。review-only 与 change-scoped wording 边界、revision/blocked 回程由唯一 caller 承接，standalone pass/revision 在报告结果后直接完成而不等待额外选择，wording review 不再是 normal Planning mandatory gate |
| `CUR-CAP-006` | 在精确副作用确认后创建或复用语义命名的 task/worktree/branch，并隔离并行资源；current workflow 已接受 `确认继续` 等清晰 dialogue-local 肯定且禁止 identity 复述 | `preserved_current + replaced_contract_shape` | `REQ-005,011..012,020,042`; `BEH-001`; `SCN-001,007`；current `.trellis/workflow.md` confirmation boundary | `guru-create-task-workspace`，以及 Commit/Merge 的 dialogue-local confirmation contract | `EVO-REQ-011,033,059,081`; `EVO-NFR-011,017` | `EVO-FIX-NO-ISSUE`, `EVO-FIX-PARALLEL`, `EVO-FIX-FULL-NORMAL`, `EVO-FIX-SEMANTIC-CONFIRMATION` | 保留完整 current 计划后的语义肯定、exact-action scope、plan drift 后重新展示、READY merge 与 identity-repetition prohibition；统一扩展到全部副作用 owner，script/validator/recorder 不解析或持久化确认。不保留 preparation/task creation coupling、固定口令或 digest challenge |
| `CUR-CAP-007` | 标准 task 形成 `prd.md`、`design.md`、`implement.md`，可交互澄清并接受一次完整 semantic plan approval | `preserved_current + replaced_contract_shape` | `BEH-002`; `SCN-002`; current workflow 与 planning package | `guru-clarify-requirements`, `guru-approve-task-plan`，以及 upstream planning authoring | `EVO-REQ-012..026,064` | `EVO-FIX-PLAN-NORMAL`, `EVO-FIX-FRESH-EQUIVALENT`, `EVO-FIX-FRESH-SCOPE`, `EVO-FIX-TECH-REVISION`, `EVO-FIX-RDT-LIFECYCLE` | 保留 task planning 的 current intent/delta、finding/revision 和一次 approval；authoring 改为 Guru-owned RDT-first 单闭环，三份 task 文件降为 repository RDT 的引用/projection/contribution mapping，不保留 upstream `trellis-brainstorm`、wrapper author 或 task-planning-as-project-authority |
| `CUR-CAP-008` | caller 明确需要时，可独立审核 contract wording 或判断受支持 normal scenario，并把每类结果返回其唯一 caller/owner | `preserved_current + replaced_contract_shape` | canonical active interfaces；current package semantic contracts | `guru-review-contract-wording`, `guru-qualify-normal-scenario` | `EVO-REQ-023,057..058` | `EVO-FIX-WORDING-EXPLICIT`, `EVO-FIX-QUALIFY-EXPLICIT` | 这两项是 target top-level specialist 的完整受支持 profile 集。review-only wording 只覆盖 `pass`、route-level `specialist_revision_required`、`blocked`；standalone pass/revision 报告后到达 `workflow_completed`，active caller 的同类结果回到其 current route，后续修改按 `independent_invocation_entry_contract`（行为顺序只由 `requirement-main.md` 的 `EVO-REQ-010/076` 主定义）重新建立 identity/envelope、一次 admission receipt、isolation 与 top-level route；change-scoped wording 的 `content_changed` 只由 active change caller 完整重入；qualification 四类结果及 scope/mechanism 前提失败投影的 `qualification_blocked` 均有对应唯一 owner/re-entry，standalone classified 明确完成；普通直接派生验收与其它通用只读 semantic review 不例行调用，也不产生第二 planning owner |
| `CUR-CAP-009` | 标准 task 在全生命周期消费 Architecture Baseline/constitution/change contract，区分 no-impact、change path、conflict、contribution/ADR、fitness、freshness 与 serialized promotion | `preserved_current + replaced_contract_shape` | `REQ-027..035`; `BEH-007`; `TST-018..026`; Architecture 2.0 authority | `guru-maintain-architecture-baseline` | `EVO-REQ-013..020,026..031,033,035,040,061,063`; `EVO-NFR-011,015` | `EVO-FIX-ARCH-NO-IMPACT`, `EVO-FIX-ARCH-ALIGNED`, `EVO-FIX-ARCH-CONFLICT`, `EVO-FIX-ARCH-INCOMPLETE`, `EVO-FIX-ARCH-NEW-DECISION`, `EVO-FIX-ARCH-REVISION`, `EVO-FIX-ARCH-NO-ADR`, `EVO-FIX-FRESH-EQUIVALENT`, `EVO-FIX-FRESH-SCOPE`, `EVO-FIX-ARCH-DOWNSTREAM-FRESHNESS`, `EVO-FIX-ARCH-PROMOTION`, `EVO-FIX-PARALLEL` | 保留 Architecture 方法论、从 Planning 到 Publication/Acceptance/Finish 的 current binding、task-local contribution 与 shared-current promotion；不保留 2.0 profile/schema/exit shape |
| `CUR-CAP-010` | 有界 task-free change 可按明确产品边界在 current checkout 执行、检查、finding 修订/recheck、位置或 active-task 恢复、blocked，或在 scope/risk 演进后带 exact partial-work identity 升级为标准 route | `preserved_current + replaced_contract_shape` | canonical mode/task-free contract；current mode/ownership requirements | `guru-select-workflow-mode`, `guru-execute-task-free-change` | `EVO-REQ-010..011,034,047,050..051`; `EVO-NFR-007..010` | `EVO-FIX-TASK-FREE`, `EVO-FIX-LATEST-INTENT` | 保留显式/自动选择、一次 choice、有界执行、适用 check、scope/risk evolution、恢复/blocked 与 concise terminal result；target 新增同 scope reconciliation、异 scope isolation 和唯一 resume owner，不生成 standard planning/archive 只是 target 收窄，不声称 current 已完全满足 |
| `CUR-CAP-011` | Implementation 消费 approved scope，Phase 2 对 task scope/实现/测试/文档/Architecture 完成 semantic finding loop，并执行 scope-relevant 最小可靠验证 | `preserved_current + replaced_contract_shape` | `REQ-003..004,032`; `BEH-003`; `NFR-004`; `TST-003..004,018` | `guru-check-task` | `EVO-REQ-027..029,065`; `EVO-NFR-014..015` | `EVO-FIX-FULL-NORMAL`, `EVO-FIX-BRANCH-FINDING`, `EVO-FIX-RDT-DOWNSTREAM-FRESHNESS` | 保留完整 semantic check 与 targeted validation ownership；新增 current RDT binding/contribution 的下游消费和中间回写，不保留 aggregate/handoff/private checkpoint |
| `CUR-CAP-012` | 精确 staging/commit，base movement impact reconciliation，exact committed full-diff independent Branch Review 与 finding closure | `preserved_current + replaced_contract_shape` | `REQ-005,012,032`; `BEH-004,006`; `SCN-002,004` | `guru-create-task-commit`, `guru-reconcile-task-base`, `guru-review-branch` | `EVO-REQ-029..034,082` | `EVO-FIX-BRANCH-FINDING`, `EVO-FIX-BASE-EVOLUTION`, `EVO-FIX-EVOLUTION-PREREQUISITE`, `EVO-FIX-FULL-NORMAL` | 保留 commit identity、fresh review 与最早受影响点 re-entry；#312 合入后还必须把 current-base-tracked clean same-task 文件放行、source/task worktree unrelated dirty 保持原归属且不被误分类或修改、真实 dirty/untracked same-task/review-metadata/identity blocker 保留，且从 fresh selected-base snapshot 证明后才能计为 current；不保留 current wrapper/transition shape |
| `CUR-CAP-013` | 从 current plan、committed diff、验证与 live authority 选择 `github_pr`/`none`，形成 route-specific readiness，并支持 provider recovery；installed publication 使用与 target reviewed checkout 分离的 immutable extension source，并保持 parent installed platform selection | `preserved_current + replaced_contract_shape` | `REQ-009,012,020,047..049`; `BEH-005..006`; `TST-008,011,017,031..032`; `SCN-041..044`; PR #317 platform matrix | `guru-review-task-publication`, `guru-finalize-task` 的 provider route | `EVO-REQ-035..041,053,082,084`; `EVO-NFR-010,033..034` | `EVO-FIX-FULL-NORMAL`, `EVO-FIX-NONE`, `EVO-FIX-PROVIDER-RECOVERY`, `EVO-FIX-INSTALLED-PROVENANCE-PUBLICATION`, `EVO-FIX-EVOLUTION-PREREQUISITE` | 保留 PR truthfulness、expected-head、两种 provider、forward recovery、source/target checkout 分离、provenance-only metadata tail、exact platform-set preservation 与远端副作用前 fail-closed；单平台/subset 不得扩张，invalid selection 必须在 source checkout/preset apply/commit 前阻断；target 补齐 route selection authority/freshness，且 `none` 不作为 provider failure fallback；不保留 Issue Scope Ledger aggregate 或 current Finalizer shape |
| `CUR-CAP-014` | Acceptance、Finalize、Merge、Issue closure-current/not-applicable 与 terminal projection 使用 exact task/head/archive/live provider facts，stale/mismatch fail closed；installed provenance reprepare 保持 reviewed-content、parent platform selection 与 terminal publication continuity | `preserved_current + replaced_contract_shape` | `REQ-011,014,020,047..049`; `BEH-005,008,010`; `TST-010,012,017,031..032`; `SCN-041..044`; PR #317 platform matrix | `guru-finalize-task`, `guru-merge-task-pr` | `EVO-REQ-036..043,053,082,084`; `EVO-NFR-009..010,033..034` | `EVO-FIX-FULL-NORMAL`, `EVO-FIX-NONE`, `EVO-FIX-PROVIDER-RECOVERY`, `EVO-FIX-FINISH-RECOVERY`, `EVO-FIX-HISTORY-RESUME`, `EVO-FIX-INSTALLED-PROVENANCE-PUBLICATION`, `EVO-FIX-EVOLUTION-PREREQUISITE` | 保留 terminal correctness、merge/closure verification、forward recovery，以及从 exact platform-preserving reprepare 到唯一 Draft PR/summary/archive+push/Ready/`ready_for_merge` 的 continuity 与 completed mutation 零重放；target 仍为 invalid platform identity、Archive/Finish/Cleanup partial failure保留 exact owner、live reread 与只补未完成动作的 re-entry；不保留 placeholder/retired-locator/current owner 切法 |
| `CUR-CAP-015` | task index/archive/finish-summary 可查询；Finish/cleanup 只处理 exact owned resource 并保护 retained ref/history | `preserved_current + replaced_contract_shape` | `REQ-005,011..012,014,020`; `BEH-006,008,010`; `TST-009..012` | `guru-finalize-task`, `guru-merge-task-pr` 及 task history runtime | `EVO-REQ-039..043,046..047,054,067`; `EVO-NFR-009..011,013` | `EVO-FIX-HISTORY-RESUME`, `EVO-FIX-ACTIVE-DISPOSITION`, `EVO-FIX-LATEST-INTENT`, `EVO-FIX-FULL-NORMAL`, `EVO-FIX-NONE`, `EVO-FIX-FINISH-RECOVERY`, `EVO-FIX-MIGRATION` | 保留可发现历史、partial recovery、owned cleanup、latest-intent continuation 与 reachability；target 区分 archive/finish/disposition durable history query 的独立 completed/blocked terminal 与 active-work resume，补齐 unique/equivalent-stale recovery、not-found/multiple/unresolved-material-stale block、suspended work 的唯一 resume owner、active lifecycle retain/suspend、零资源 no-op abandonment、有资源 confirmed abandonment、cleanup 拒绝唯一 choice、remote-boundary disposition，以及资源前 exact plan，并要求 disposition result 在 cleanup 后仍由唯一 history owner 可查询；为 Finish/Cleanup/disposition cleanup 分别定义 blocked、exact-boundary re-entry、已完成/待执行动作与 partial-resource live facts；existing migration 在 cutover 前盘点 active/resumable work 与 archive/finish/history，成功后全部经新合同保持可恢复/可查询/可达且无 legacy runtime consumer；不保留 workspace journal、完整 stdout、授权或长摘要 |
| `CUR-CAP-016` | Requirements/Design/Test 与 Architecture 各有 shared current SSOT；新/残缺仓库可 bootstrap/repair，task 通过 isolated contribution 与 reviewed serialized promotion 演进 | `preserved_current + replaced_contract_shape` | `REQ-007,019,027..035`; `BEH-007`; `TST-006,016,018..024` | `guru-maintain-requirements-design-test-ssot`, `guru-maintain-architecture-baseline`, `guru-bootstrap-repository-ssot` | `EVO-REQ-018..020,031,033,061..065`; `EVO-NFR-011,015` | `EVO-FIX-SSOT-BOOTSTRAP`, `EVO-FIX-RDT-LIFECYCLE`, `EVO-FIX-RDT-DOWNSTREAM-FRESHNESS`, `EVO-FIX-ARCH-PROMOTION`, `EVO-FIX-PARALLEL` | 保留唯一 shared current、traceability、bootstrap/repair、contribution/promotion；target 将 RDT 提升为所有 standard task 的前置与下游 current authority，task planning 不再是平行 SSOT；不保留 current profile/public DTO/recorder layout |
| `CUR-CAP-017` | canonical/dogfood/installed/shared `.agents/skills` layer/Codex/Claude/Cursor 与 official install/update/upgrade/workflow switch 可分别执行 capability-loss 和 consistency/installation 验证；shared layer 只计一次，installed Finalizer reprepare 精确保留 manifest platform selection，standalone verifier 与内嵌 caller 保持明确 ownership，failed standalone verification 在 cleanup 前保留 structured evidence | `preserved_current + replaced_contract_shape` | `REQ-002,006,013,016..019,035,043,046,049..051`; `BEH-009,011`; `TST-005,014..016,025..035`; `SCN-041..047`; PR #317 platform matrix | 全 registry packages；`guru-finalize-task` owns installed reprepare，`guru-verify-extension-installation` 为 standalone owner，安装/迁移/Release caller 消费内嵌 finding | `EVO-REQ-010,051..056,083..084`; `EVO-NFR-009..010,012..016,033..034` | `EVO-FIX-ENTRY-ROUTING`, `EVO-FIX-PROJECTION`, `EVO-FIX-CLEAN-INSTALL`, `EVO-FIX-MIGRATION`, `EVO-FIX-RELEASE`, `EVO-FIX-INSTALLED-PROVENANCE-PUBLICATION`, `EVO-FIX-VERIFIER-FAILURE-EVIDENCE` | target 先按 terminal intent 与 target live current state exactly-one 选择 standalone projection、clean install、existing migration 或 Release；capability-loss 与 consistency/installation gate 继续分离。installed reprepare 的三处 selected lists/`all_platforms` 必须 exact valid，合法 subset 不扩张，invalid identity 在 source checkout/preset apply/commit 前 fail closed。standalone failure 必须在 cleanup 前形成 stage/cell/command/exit/safe-tail/hash/size evidence，matrix 外 failure 明确归入 postcheck；内嵌 gate 只返回最小 finding。Release wait、publication/post-publish recovery 与 new-candidate 边界保持；target 只投影新合同，不保留旧 route/schema/artifact consumer |
| `CUR-CAP-018` | verifier 从 live registry/interfaces 派生 active package/command/complete inventory 供 consistency/installation equality，capability-loss inventory 独立只含 `workflow/task_data/docs_authority`，两者都不依赖固定 magic count，并可向当前 caller 返回最小 gate finding；failed execution 必有 non-null structured failure | `preserved_current + replaced_contract_shape` | `REQ-015,018,051`; `TST-013,015,035`; `SCN-010,013,046` | `.42` inventory 全 21 active Skill/89 exits及 verifier failure schema | `EVO-REQ-053,055..056,083`; `EVO-NFR-010,012..013,016` | `EVO-FIX-PROJECTION`, `EVO-FIX-CLEAN-INSTALL`, `EVO-FIX-MIGRATION`, `EVO-FIX-RELEASE`, `EVO-FIX-VERIFIER-FAILURE-EVIDENCE` | 保留 live derivation、三组 before/after capability-loss detection、独立 consistency/installation equality与 cleanup 前 non-null failure evidence；21/89 只作为 `.42` source identity，其变化可阻断 consistency 但不得自动记为 capability loss。standalone consumer 独占 evidence 与 blocked/re-entry，内嵌 consumer 不取得该 ownership |
| `CUR-CAP-019` | static/package/semantic/integration/distribution/live/release evidence 分层；普通 change 只运行 accepted scope 所需最小可靠集合，专项 owner 才声明完整矩阵或 Release；失败证据按实际执行层与 unverified boundary 诚实分类 | `preserved_current` | `REQ-009,050..051`; `NFR-004..005`; `TST-001..009,033..035`; `SCN-045..047` 与 Test “选择规则” | inventory 的 #260/#283/#311 boundary 说明 | `EVO-REQ-028,035,051,056,083`; `EVO-NFR-010,014,016,033` | `EVO-FIX-PLAN-NORMAL`, `EVO-FIX-FULL-NORMAL`, `EVO-FIX-ARCH-PROMOTION`, `EVO-FIX-RDT-LIFECYCLE`, `EVO-FIX-RELEASE`, `EVO-FIX-INSTALLED-PROVENANCE-PUBLICATION`, `EVO-FIX-VERIFIER-FAILURE-EVIDENCE` | 保留 proof boundary、SKIP/unverified honesty、最小 validation ownership、credential-safe failure evidence 与 verifier/Finalizer 零交叉消费；流程精简不得把它删除 |
| `CUR-CAP-020` | 两个正常并行 task 的 workspace/provider/archive/Finish/cleanup 隔离，`github_pr` 与 `none` 都可完成，shared current 单写 | `preserved_current + replaced_contract_shape` | `REQ-020,034`; `BEH-011`; `TST-009,017,024`; `SCN-007,015..016,030` | delivery、finalize、merge、SSOT packages 的组合能力 | `EVO-REQ-033,037..043`; `EVO-NFR-011` | `EVO-FIX-PARALLEL`, `EVO-FIX-FULL-NORMAL`, `EVO-FIX-NONE` | 保留隔离、两种 provider、merge order/recovery/reachability；不保留 current metadata/handoff 切分 |
| `CUR-CAP-021` | initial request 是 simple conversation 或 non-file-changing request 时直接回答；即使主题涉及 Issue/task-like work，只要仅请求信息也不创建 GitHub Issue/Trellis task、不询问是否创建，并且不调用 file-changing mode selection | `preserved_current + replaced_contract_shape` | `source_ref=5650df47fe17fe89b7cb616be6c9551608164832` 的 `.trellis/workflow.md:30..38` 与 canonical `trellis/workflows/guru-team/workflow.md:30..38` | global workflow 的 pre-Skill Guru Team Gate | `EVO-REQ-010,034,049,055`; `EVO-NFR-009` | `EVO-FIX-ENTRY-ROUTING` | 保留普通 non-file-changing direct answer、Issue/task-like information request 与不绑定 active lifecycle 的通用只读 review 仍直接回答，以及零 Issue/task/mode 副作用；target 先执行 active-user-intent lifecycle preclassification，再将独立请求纳入六类 exactly-one entry，只有 wording review-only/normal-scenario qualification 两个 profile 进入 specialist，并为 live fact unavailable 定义透明 unverified terminal，不保留 current Markdown 条目顺序或隐式 route shape |
| `CUR-CAP-022` | Phase 2 对 task scope 内相关 Gitlink 的 reviewed-content identity 同时绑定 superproject mode `160000`、commit/index pointer；已初始化 Gitlink 还绑定 root、clean status 与 `HEAD` content identity。无关 Gitlink 仍完全排除，且该读取不授予 Task Commit staging authority | `preserved_current + replaced_contract_shape` | `source_ref=5650df47fe17fe89b7cb616be6c9551608164832`；`82fb5172`/`f8d8b20d`；`.trellis/spec/workflow/{data-contracts,quality-guidelines}.md` 与 `guru-check-task` reviewed-content runtime/tests | retained current delta | `EVO-REQ-028`; `EVO-NFR-014,018` | `EVO-FIX-BRANCH-FINDING`, `EVO-FIX-SUBMODULE-BOUNDARY`, `EVO-FIX-FULL-NORMAL` | 保留相关 Gitlink 的 pointer/content freshness 与无关 Gitlink 隔离；target 可更换内部算法/DTO，但不得退化为仅路径名、普通 blob hash、递归 submodule scope 或隐式 staging authority |
| `CUR-CAP-023` | Branch Review 遇到文本文件仅在 EOF 多出一个或多个空行且 meaningful bytes 不变时，只记录无严重度、非阻断 observation；其它会改变语义或 parser/linter/formatter 合同的 whitespace 仍正常审核 | `preserved_current + replaced_contract_shape` | `source_ref=5650df47fe17fe89b7cb616be6c9551608164832`；`73973273`；`guru-review-branch/SKILL.md`、`references/contract.md` 与 contract tests | retained current delta | `EVO-REQ-030`; `EVO-NFR-014` | `EVO-FIX-BRANCH-FINDING` | 保留 EOF-only observation 的窄例外与其它 whitespace 的正常 finding 资格；不得泛化为忽略 trailing spaces、indentation、字符串/配置值、编码或格式合同变化 |

## 4. Current `.42` active Skill coverage index

本表是与 `.42` Design inventory 的逐行一致性检查。每个 current Skill 都至少映射到一个
`CUR-CAP-*`；target 是否继续使用同名 Skill 由后续 Design 决定。

| Current `.42` Skill id | Current capability successor | Target requirement successor | 结论 |
| --- | --- | --- | --- |
| `guru-select-workflow-mode` | `CUR-CAP-003,010` | `EVO-REQ-010` | 可观察 mode/task-free 分流保留，Skill id/exit 可替换 |
| `guru-sync-base` | `CUR-CAP-004` | `EVO-REQ-009,060` | exact base authority 能力保留，private result shape 不保留 |
| `guru-discover-change-context` | `CUR-CAP-003,004` | `EVO-REQ-002,059..060` | fresh context 能力保留，不允许 consumer 读取 producer-private result |
| `guru-clarify-requirements` | `CUR-CAP-003,005,007` | `EVO-REQ-002..008,012` | 逐问澄清和 requirement readiness 保留，normal authoring owner 重构 |
| `guru-review-contract-wording` | `CUR-CAP-005,008` | `EVO-REQ-025,057` | 显式 specialist 能力保留；review-only 与 change-scoped caller 分流，standalone `pass`/`specialist_revision_required` 在完整报告后直接完成，`blocked` 只按原 owner fresh re-entry；`content_changed` 只由 active change caller 完整重入，normal Planning 调用为 0 |
| `guru-review-change-request` | `CUR-CAP-003,005` | `EVO-REQ-059` | duplicate/prerequisite/independent-unit readiness 保留且不重复 authoring；target 将 ready、active duplicate、completed duplicate、scope clarification、prerequisite blocked 与 resolution blocked 分成六类互斥结果，并为每类绑定唯一 owner、terminal 或 exact readiness re-entry |
| `guru-create-task-workspace` | `CUR-CAP-006` | `EVO-REQ-011,059` | exact resource preparation 保留，owner coupling 可替换 |
| `guru-approve-task-plan` | `CUR-CAP-007` | `EVO-REQ-024..026` | 一次完整 planning approval 保留 |
| `guru-qualify-normal-scenario` | `CUR-CAP-008` | `EVO-REQ-023,058` | 仅 explicit current caller 需要时保留；`classified`、scope confirmation、mechanism revision、blocked 各由唯一 owner 消费并在修复后 fresh 重入 |
| `guru-execute-task-free-change` | `CUR-CAP-010` | `EVO-REQ-010,034,051` | 有界 task-free 闭环保留并收窄长期 artifact；不借用 standard approved-plan/Phase 2 合同 |
| `guru-check-task` | `CUR-CAP-011,022` | `EVO-REQ-027..029` | Phase 2 semantic finding loop 与相关 Gitlink reviewed-content identity 保留 |
| `guru-create-task-commit` | `CUR-CAP-012` | `EVO-REQ-029..031` | exact commit 与 fresh candidate binding 保留 |
| `guru-reconcile-task-base` | `CUR-CAP-012,015` | `EVO-REQ-026,032` | base evolution impact/recovery 保留，不重建 task |
| `guru-review-branch` | `CUR-CAP-012,023` | `EVO-REQ-029..031` | committed full-diff independent review 与 EOF-only non-blocking observation 保留 |
| `guru-review-task-publication` | `CUR-CAP-013` | `EVO-REQ-035..036` | truthful publication readiness 保留 |
| `guru-finalize-task` | `CUR-CAP-013..015,017,020` | `EVO-REQ-037..043,084` | provider/finalization/history/terminal 结果与 installed platform selection 保留；target 为 Archive/Finish 与 Cleanup 分别定义 `finish_blocked`/`cleanup_blocked`、live reread、已完成/待执行事实和 exact owner re-entry，不重放已完成副作用；installed reprepare 对合法 selection 精确投影，对 invalid identity 在 source checkout/preset apply/commit 前 fail closed，owner/helper shape 可替换 |
| `guru-merge-task-pr` | `CUR-CAP-014,020` | `EVO-REQ-037,040..042` | expected-head merge 与 closure verification 保留；target 先由 Finish 形成 archive-bound `ready_for_merge`，再由 Merge、Closure、delivery terminal、Cleanup 顺序消费，partial failure 只交给 exact stage owner 恢复且不重复 provider 副作用 |
| `guru-verify-extension-installation` | `CUR-CAP-017..019` | `EVO-REQ-010,052..056` | standalone installation/capability verification 保留，target inventory live-derived；distribution 先按 live target state exactly-one 选择 standalone projection、clean install、existing migration 或 Release。Release confirmation 缺失/拒绝/stale 各有等待、零副作用 terminal 或 pre-publish re-entry；publication/post-publish failure 绑定 immutable identity，可恢复失败 exact re-entry，语义 defect 终止为 `release_published_unverified`；后续修订只引用 `requirement-main.md` 的 `independent_invocation_entry_contract`，重新建立 identity/envelope、一次 admission receipt、isolation 与 top-level route，只有分类为 `distribution/release` 才生成 new candidate |
| `guru-maintain-requirements-design-test-ssot` | `CUR-CAP-016` | `EVO-REQ-061..062` | RDT shared-current lifecycle 保留 |
| `guru-maintain-architecture-baseline` | `CUR-CAP-009,016` | `EVO-REQ-013..020,026..031,033,035,040,061,063` | Architecture lifecycle 与 downstream current binding 保留，2.0 API shape 不保留 |
| `guru-bootstrap-repository-ssot` | `CUR-CAP-016` | `EVO-REQ-061` | new/partial/stale/conflicting authority bootstrap/repair 保留 |

差集结论：current `.42` Design inventory 的 21 个 active Skill 均至少有一个 successor；每条一对多
映射均可解释且有 target requirement/fixture 归属，孤儿项与映射冲突均为 0。该结论只证明
Requirements coverage，不证明 target Design 已完成或 target runtime 已实现。

## 5. Current authority coverage closure

| Current authority set | Inventory coverage | 结论 |
| --- | --- | --- |
| `REQ-001..020` | `CUR-CAP-001..003,005..008,011..020` | 全部有 successor |
| `REQ-027..035` | `CUR-CAP-009,011..012,016,020` | 全部有 successor |
| `REQ-036..046` | `CUR-CAP-003..004,017` | 全部有 successor |
| `REQ-047..051` + PR #317 platform-selection runtime advance | `CUR-CAP-013..014,017..019` | #311 installed publication、verifier failure evidence与 exact platform-set preservation 全部有 successor；PR #317 不创建独立 current requirement id |
| `BEH-001..011` | `CUR-CAP-001..017,020` | 全部有 successor |
| `NFR-001..005` | `CUR-CAP-001..004,011,017..019` | 全部有 successor |
| `.42 TST-001..035`, `SCN-001..016,024..047`, `CASE-001..002` + PR #317 focused platform matrix | 下节逐组映射到 `CUR-CAP-*`、target requirement 与 target fixture | 无 current product/test capability 被静默删除；target Test planning 已投影 50 个 `planned_not_executed` fixture；pre-`REQ-REV-142` Design review 已 stale，current exact candidate 的 fresh Design review 与确定性闭包已通过，但 fixture execution 仍未发生 |
| `.42 REQ-052..055`, `DES-049..052`, `TST-036..039`, `SCN-048` | `EVO-EVD-048` / `REQ-REV-139` 的 authority/release fact-only classification | 只证明 `.42` unique-current、`.3/.39/CLI 0.6.15` identity separation 与 promotion freshness；不产生新的 `CUR-CAP-*`、`TARGET-DELTA-*`、Evolution fixture 或 runtime behavior |
| `a41b8a34...9f560ec1` selected-base delta | `EVO-EVD-049` / `REQ-REV-140` 的 release-lifecycle/provenance fact-only classification | 只修正 #267 post-merge lifecycle evidence、dogfood source provenance、task archive 与 PR #316 merge facts；`.42` behavior authority、extension/CLI version 及 23/13/50/73/21/89 集合不变 |
| `9f560ec1...736ef333` selected-base delta | `EVO-EVD-050` / `REQ-REV-141` 的 material current-capability classification | PR #317 修复 installed Finalizer platform selection preservation，并修正 latest stable current fact；折入 `CUR-CAP-013/014/017` 与既有 fixture，产生第 84 项 target requirement / 第 34 项 NFR，但 52/23/13/50/73/21/89 集合不变；旧 Requirements/Design review stale |
| `736ef333...5650df47` selected-base delta | `EVO-EVD-051` / `REQ-REV-142` 的 fact-only classification | PR #318 只刷新 Finalizer caller-inventory identity、#267 related-only disposition、dogfood provenance 与 task archive/merge facts；runtime、public contracts、`.42`、Release identity、52/84/34/23/13/50/73/39/43/37/21/89 和 #311/#312/#317 successor 均不变；旧 exact-base review stale |

`.42` Requirements 未定义 `REQ-021..026`，编号从 `REQ-020` 跳到 `REQ-027` 是 current
authority 的既有事实，不是本 inventory 的 coverage 缺口。

### 5.1 Current Test capability successor closure

本表以 `.42` `test-strategy.md` 与 `traceability.md` 的产品行为编号为 capability source，不复制测试正文。
`test-plan.md` 是同一 Test authority 下的执行计划、before-state、矩阵与 evidence boundary；它不
新增 `TST/SCN/CASE` 编号，也不形成第七组 capability slice。
每组都明确 current observable capability、target requirement 与至少一个 acceptance fixture；
后续 target Test 只能细化这些 successor，不能在 Design/Test 中静默删除 source capability。

| Current Test authority slice | Current capability successor | Target requirement successor | Target fixture successor | 差集结论 |
| --- | --- | --- | --- | --- |
| `TST-001..004`, `SCN-001..004`, `CASE-001..002` | `CUR-CAP-002..003,011..012,016,019` | `EVO-REQ-002..034,051,059..065` | `EVO-FIX-INTAKE-CLEAR`, `EVO-FIX-PLAN-NORMAL`, `EVO-FIX-BRANCH-FINDING`, `EVO-FIX-RDT-LIFECYCLE`, `EVO-FIX-FULL-NORMAL` | static/package/semantic/integration 与 consumer closure 全部有 successor |
| `TST-005..008`, `SCN-005..006` | `CUR-CAP-001..002,013,016..019` | `EVO-REQ-028,035,051..056,061..065` | `EVO-FIX-SSOT-BOOTSTRAP`, `EVO-FIX-RDT-LIFECYCLE`, `EVO-FIX-PROJECTION`, `EVO-FIX-CLEAN-INSTALL`, `EVO-FIX-MIGRATION`, `EVO-FIX-RELEASE` | distribution/SSOT/compatibility/live proof boundary 全部有 successor |
| `TST-009..012`, `SCN-007..009` | `CUR-CAP-012..015,020` | `EVO-REQ-029..043` | `EVO-FIX-PARALLEL`, `EVO-FIX-HISTORY-RESUME`, `EVO-FIX-PROVIDER-RECOVERY`, `EVO-FIX-FINISH-RECOVERY`, `EVO-FIX-FULL-NORMAL`, `EVO-FIX-NONE` | parallel/history/recovery/Archive-Finish-Cleanup blocked re-entry/terminal projection 全部有 successor |
| `TST-013..017`, `SCN-010..016` | `CUR-CAP-013..020` | `EVO-REQ-035..043,051..056,061..065` | `EVO-FIX-PROJECTION`, `EVO-FIX-CLEAN-INSTALL`, `EVO-FIX-MIGRATION`, `EVO-FIX-RELEASE`, `EVO-FIX-FULL-NORMAL`, `EVO-FIX-NONE`, `EVO-FIX-PARALLEL` | live inventory、三组 capability-loss、独立 consistency/installation、installed SSOT 与 A-B lifecycle 全部有 successor |
| `TST-018..026`, `SCN-024..033` | `CUR-CAP-009,011..012,016..017,019..020` | `EVO-REQ-013..020,026..035,040,051..056,061..065` | `EVO-FIX-ARCH-NO-IMPACT`, `EVO-FIX-ARCH-ALIGNED`, `EVO-FIX-ARCH-CONFLICT`, `EVO-FIX-ARCH-INCOMPLETE`, `EVO-FIX-ARCH-NEW-DECISION`, `EVO-FIX-ARCH-REVISION`, `EVO-FIX-ARCH-NO-ADR`, `EVO-FIX-ARCH-DOWNSTREAM-FRESHNESS`, `EVO-FIX-ARCH-PROMOTION`, `EVO-FIX-PARALLEL`, `EVO-FIX-PROJECTION`, `EVO-FIX-CLEAN-INSTALL`, `EVO-FIX-MIGRATION` | Architecture lifecycle/constitution/change contract/project check/promotion/projection 全部有 successor |
| `TST-027..030`, `SCN-034..040` | `CUR-CAP-004,006,017..019` | `EVO-REQ-009,011,028,051..056,060` | `EVO-FIX-DETACHED-READ`, `EVO-FIX-BASE-REFRESH`, `EVO-FIX-FULL-NORMAL`, `EVO-FIX-PROJECTION`, `EVO-FIX-CLEAN-INSTALL`, `EVO-FIX-MIGRATION`, `EVO-FIX-RELEASE` | base selection/sync/provenance/distribution 全部有 successor |
| `TST-031..032`, `SCN-041..044` + PR #317 focused platform matrix | `CUR-CAP-013..014,017` | `EVO-REQ-037,053,082,084`; `EVO-NFR-034` | `EVO-FIX-INSTALLED-PROVENANCE-PUBLICATION`, `EVO-FIX-EVOLUTION-PREREQUISITE` | Finalizer source/target binding、exact installed platform-set preservation、invalid identity pre-apply fail-close 与完整 publication terminal 全部有 successor |
| `TST-033..035`, `SCN-045..047` | `CUR-CAP-017..019` | `EVO-REQ-051..056,083` | `EVO-FIX-PROJECTION`, `EVO-FIX-CLEAN-INSTALL`, `EVO-FIX-MIGRATION`, `EVO-FIX-RELEASE`, `EVO-FIX-INSTALLED-PROVENANCE-PUBLICATION`, `EVO-FIX-VERIFIER-FAILURE-EVIDENCE` | installed distribution isolation、representative closeout 与 cleanup 前 structured verifier failure evidence 全部有 successor |

集合差集：以上 source slice 的并集恰好为 `TST-001..035`、`SCN-001..016,024..047` 与
`CASE-001..002`；source 孤儿 0、映射冲突 0、未知 target fixture 0。具体 target Design/Test case
shape 已由 [`docs/test/evolution/`](../../test/evolution/README.md) 建立为 planning projection，
50 个 fixture 仍全部为 `planned_not_executed`；pre-`REQ-REV-142` Design mapping/review 已 stale，不得用
`.42`/`.41` PASS 或旧
49-row closure 冒充 target evidence。
`test-plan.md` 的执行记录与 evidence boundary 只作为上述 source slice 的约束，不改变该编号并集。

## 6. New target deltas

以下结果不能写成 `preserved_current`；任意 selected-base current capability、inventory row 或 PASS
也不得冒充这些 `new_target` 已存在。`Target core capability`
只记录该 delta 主要服务的顶层产品难点，不替代 `EVO-REQ-*` 与 fixture 的验收主定义：

| Delta id | New target | Target core capability | Target authority | Acceptance |
| --- | --- | --- | --- | --- |
| `TARGET-DELTA-001` | Guru-owned 单一 authoring 闭环完全替代 upstream `trellis-brainstorm`，并保留逐个最高价值问题的交互式澄清；`new change` 只承接有明确文件变更目标的请求，非文件变更请求不得借 mode selection 进入该闭环 | `EVO-CAP-001,EVO-CAP-002` | `EVO-REQ-004,010,012,024..025` | `EVO-FIX-INTAKE-UNCLEAR`, `EVO-FIX-ENTRY-ROUTING`, `EVO-FIX-PLAN-NORMAL` |
| `TARGET-DELTA-002` | `design.md` 首次实质写作前实际消费 current baseline、constitution、change contract，并 reconciliation Issue 中已审阅设计 | `EVO-CAP-003` | `EVO-REQ-013,015..017,021..022` | `EVO-FIX-INTAKE-REVIEWED-DESIGN`, `EVO-FIX-ARCH-ALIGNED`, `EVO-FIX-ARCH-CONFLICT` |
| `TARGET-DELTA-003` | normal Planning 去掉 mandatory wording/qualification wrapper，只保留一次 authoring 和一次 approval；top-level specialist 只保留 wording review-only 与 supported normal-scenario qualification 两个 profile，通用只读 semantic review 直接回答。显式 specialist 仍按 review-only/change-scoped 边界调用，active caller 的所有结果回到唯一 caller/owner，standalone `pass`/revision findings 在完整报告后直接完成当前 invocation，blocked 只按 route-local owner fresh re-entry，不再增加“修改或 stop”等待状态，也不把 blocked 或 revision 伪装为成功 | `EVO-CAP-001,EVO-CAP-004` | `EVO-REQ-010,023..025,057..058` | `EVO-FIX-ENTRY-ROUTING`, `EVO-FIX-PLAN-NORMAL`, `EVO-FIX-WORDING-EXPLICIT`, `EVO-FIX-QUALIFY-EXPLICIT` |
| `TARGET-DELTA-004` | normal workflow 以 applicable repository RDT、Architecture Baseline 与 task `prd.md`/`design.md`/`implement.md` 的稳定 locator/identity/order 作为主要可缓存 context，把 live delta 放在最小变化 tail；AI owner 直接据此自主判断。无 consumer 交接、human-style assignment/signoff/transaction handoff、already-current fact restatement、重复 unchanged 正文/累计输出注入、不必要脚本/gate/验证和内部过程噪声均为 0，阶段后卸载无用 private evidence；LLM cache 只作优化，不设置 cache hit 或相对性能数值门槛 | `EVO-CAP-004` | `EVO-REQ-044..050`; `EVO-NFR-001..008` | `EVO-FIX-PLAN-NORMAL`, `EVO-FIX-FULL-NORMAL`, `EVO-FIX-LONG-OUTPUT` |
| `TARGET-DELTA-005` | latest-intent closure 只追踪 `requirement-main.md` 主定义的输入/结果组合、唯一 consumer、identity/freshness evidence 与 exact re-entry coverage；不在 inventory 另立行为合同。`independent_request_isolation_pending` 还必须证明每次 re-evaluation 恰好得到 progress-refresh、safe-clear/re-entry 或 no-progress/invalid-handle/non-consumable-owner -> `independent_request_isolation_blocked`，不得无界 pending；旧 identity/envelope/candidate/receipt reuse、重复或遗漏 receipt、错误默认 new change、无 consumer pending、无进展仍 pending 的计数必须为 0 | `EVO-CAP-001,EVO-CAP-004` | `EVO-REQ-010..011,041,043,046..048,067,076`; `EVO-NFR-009,011` | `EVO-FIX-LATEST-INTENT`, `EVO-FIX-HISTORY-RESUME`, `EVO-FIX-ACTIVE-DISPOSITION`, `EVO-FIX-PARALLEL` |
| `TARGET-DELTA-006` | task-free 具有可判定的显式/自动适用边界、finding/recheck、unique/blocked recovery 和 scope/risk expansion；post-write escalation 保留 exact partial-work identity，在任何标准资源副作用前完成 scope/owner/isolation plan confirmation，并在资源准备后完成唯一归属 reconciliation/isolation，不生成正式 planning、task/archive history 或 standard cleanup resource | `EVO-CAP-001,EVO-CAP-004` | `EVO-REQ-010..011,047,050..051`; `EVO-NFR-007..010` | `EVO-FIX-TASK-FREE`, `EVO-FIX-HISTORY-RESUME` |
| `TARGET-DELTA-007` | 最终 candidate 只含新合同；distribution/release 顶层入口先按 terminal intent、candidate 与 target live current state exactly-one 选择 standalone projection、clean install、existing migration 或 exact Release，选择前不执行 route 副作用。对 install/migration 必须先由 `EVO-REQ-010` 的 `distribution_state_preclassification` 分类：active `.trellis/workflow.md` 缺失且无任何可归属 official Trellis/Guru managed installation state 才是 `clean_target`；可唯一归属的 official Trellis config/template-hash/scripts/spec/task/workspace/manifest（即使 workflow/Guru projection 缺失）、可识别 Guru current、可唯一归属的 partial/legacy Guru managed surface、sidecar、lifecycle、history/ref，或 identity/provenance/owner 与当前安全 transition plan 均唯一收敛的 non-Guru active workflow，才是 `existing_migration_target`；上述 facts 或 plan 未 current 的 non-Guru active workflow 先标记 `foreign_workflow`，它既不进入 clean 也不进入 migration，只能得到 `distribution_state_blocked`，收敛后只重入 preclassification 并转入 existing migration；mixed/unknown/unowned/multiple identity 同样 blocked，clarification/live repair 前全部 route 副作用为 0。Delivery 与四类 distribution action（含 Release）的外部动作共享 exact-provider binding、live reread、unknown-outcome、幂等、有界重试和 owning-boundary recovery。projection 独立验证 `workflow/task_data/docs_authority` capability loss，以及 Skill API/interface/schema/command、distribution/managed-installed inventory、mode/template hash/sidecar、平台 parity、extension identity/version binding consistency；后一类不构成 capability loss。top-level standalone failure 由 projection owner 得到 `projection_validation_blocked` 并从 exact surface re-entry；内嵌于 clean install、migration 或 Release pre-publish 的 gate 只返回最小 finding，不取得顶层 ownership，分别由 caller 得到 `clean_install_blocked`、按 live cutover state 分类的 migration terminal 或 `release_pre_publish_blocked`。clean repository 不消费 migration terminal；existing repository 在 cutover 前盘点 active/resumable work、archive/finish/history 与 retained ref，不能由新合同承接时保持 pre-migration current 并阻塞，成功后这些结果经新合同保持可恢复/可查询/可达，legacy runtime consumer 与旧新混合 graph 均为 0；WORKFLOW-SWITCH 的 byte-equal predicate 只在固定顺序抵达该 boundary 后形成 cutover observation，invocation-entry byte equality 不提前改变前序 finding 分类；Release 严格分为 pre-publish gate、`ready_for_release_confirmation`、immutable publication 与 tag-pinned post-publish verification。confirmation 缺失只保持 current wait，明确拒绝以 `release_not_published` 零 publication 副作用完成，candidate/decision-relevant facts 变化必须使旧 wait/确认失效并返回 pre-publish；pre-publish blocked 或 candidate 变化后生成 new candidate identity 并完整重跑，live facts 变化重读并重跑全部受影响 gate；partial publication、post-publish prerequisite failure 分别只从原 immutable identity 的 publication/post-publish owner 恢复，不能返回 pre-publish 或重放发布；已发布 candidate 的语义 defect 终止为 `release_published_unverified`，原 tag/Release 不可变；后续修订按 `independent_invocation_entry_contract`（主定义见 `requirement-main.md` 的 `EVO-REQ-010/076`）重新建立 identity/envelope、一次 admission receipt、isolation 与 top-level route，只有分类为 `distribution/release` 才生成 new candidate，发布后不提供旧合同 fallback | `EVO-CAP-001..004` | `EVO-REQ-010,039,052..056`; `EVO-NFR-010,012..015` | `EVO-FIX-ENTRY-ROUTING`, `EVO-FIX-PROJECTION`, `EVO-FIX-PROVIDER-RECOVERY`, `EVO-FIX-CLEAN-INSTALL`, `EVO-FIX-MIGRATION`, `EVO-FIX-RELEASE` |
| `TARGET-DELTA-008` | repository RDT 成为 standard task 的上位文档中心：Planning 前置回读/impact，task 三件套只承载 current authority 引用、task-local delta/contribution 与执行/验证/交付 mapping；RDT、适用 Architecture Baseline 与 task 三件套共同形成稳定 primary context，实施与审查持续回写并验证 current RDT lifecycle，不另建 handoff authority | `EVO-CAP-002` | `EVO-REQ-002,012,021,024,027..030,035,044..046,061..065` | `EVO-FIX-PLAN-NORMAL`, `EVO-FIX-RDT-LIFECYCLE`, `EVO-FIX-RDT-DOWNSTREAM-FRESHNESS`, `EVO-FIX-FULL-NORMAL` |
| `TARGET-DELTA-009` | parent repository task 默认完全排除 Git submodule 的 authority、RDT、代码、状态、副作用与验证；显式 submodule change 进入独立 repository workflow | `EVO-CAP-001,EVO-CAP-002` | `EVO-REQ-002,010..011,061,066`; `EVO-NFR-018` | `EVO-FIX-SUBMODULE-BOUNDARY`, `EVO-FIX-FULL-NORMAL` |
| `TARGET-DELTA-010` | 既有 active lifecycle 在 exact recovery 后拥有独立 disposition 闭环：无不可逆远端副作用时可 retain/suspend；abandon 的 exact plan 若 deletable owned resource 为 0 则 no-op 完成，存在删除副作用时才取得 current cleanup 确认。确认缺失只等待；明确拒绝必须消费回复中的唯一 retain/suspend choice 或只询问一次真实 choice，不得产生双 terminal；stale、资源不唯一与 partial cleanup 都有明确 blocked exact re-entry。已有不可逆远端副作用时不回滚、不删除、不冒充 cancelled，原 owner 保持 candidate 不变并收敛既定 terminal、forward-recovered terminal 或 terminal block，之后只清理获 current 确认的 eligible local owned resources；全部结果保留 cleanup 后仍可由唯一 history owner 查询的最小 durable disposition/history，并到达 completion 或 route-local block | `EVO-CAP-001,EVO-CAP-004` | `EVO-REQ-010,034,042..043,047,067`; `EVO-NFR-009,016..017` | `EVO-FIX-REQUEST-STOP`, `EVO-FIX-HISTORY-RESUME`, `EVO-FIX-ACTIVE-DISPOSITION` |
| `TARGET-DELTA-011` | 对 17 个 logical stock asset 建立 Guru-owned exactly-one role、successor/provider caller、必要的 caller/profile/input/typed-result/direct-consumer、projection cell、Design handoff 与 source-class collision prevention；shared layer 只计一次，九项 suppressed semantic route 不得在 Guru entry/lifecycle owner 之外自行执行，并必须先证明 Guru successor 已无损承接可观察能力。唯一 provider 只返回 caller-bound channel transport，五项 worker 只返回 caller-bound research/implementation/check result，两项 explicit 只返回显式 history query 或只读 diagnosis/recommendation；Guru-owned spec/reference successor 不得重新归入这些 raw role。standalone exact explicit-only 只读结果必须投影为 `explicit_provider_result_current` 并由 direct-answer owner 完成，channel/worker 与 embedded read-only result 只回 exact caller，任何 follow-up 写入意图在 raw explicit invocation 前回到 `new change`/active caller；每个 asset 的 action 选择与兼容性理由只按 `requirement-main.md` 的 `EVO-REQ-071` 绑定并追踪，不在 inventory 另立选择顺序，也不要求穷举未选 action | `EVO-CAP-001,EVO-CAP-004` | `EVO-REQ-068..080`; `EVO-NFR-019..032`; `REQ-UC-EVO-047..048` | `EVO-FIX-STOCK-COEXISTENCE` |
| `TARGET-DELTA-012` | 对 stock suppression/provider policy 建立最小 source/version/path、必要 template hash/manifest、独立 `file_state`/`context_state`/`sidecar_state`、user modification、`.new/.bak` sidecar、fresh install、existing migration、update dry-run 两条 exact command 分支、workflow switch 与 preset reapply 的可恢复 provenance 和 blocked/re-entry；每个 role row 与 retained host row 只对 Design 选定 action 建立 action state，首次全 pending/partial/unknown 先进入 recovery-required 状态，retained 不安全结果为 `retained_context_blocked`；不得覆盖用户修改、留下 mixed graph、静默丢失 current capability 或把 upstream regeneration 当作自动恢复；未选 action 不要求额外验证 | `EVO-CAP-001,EVO-CAP-004` | `EVO-REQ-072..080`; `EVO-NFR-022..032`; `REQ-UC-EVO-049..050` | `EVO-FIX-STOCK-MAINTENANCE` |
| `TARGET-DELTA-013` | 全部副作用 owner 使用同一 dialogue-local semantic confirmation：完整 current 计划后的任一清晰语义肯定充分且只授权刚展示 action；未展示/疑问/限制/修改/拒绝/material drift 保持零副作用并重建计划或 route-local 收敛；READY PR merge 不要求固定 `合并PR`；固定 prompt/口令、`确认执行 <hash>`、identity/摘要复述、script parsing 与 authorization persistence 全部为 0 | `EVO-CAP-001,EVO-CAP-004` | `EVO-REQ-081`; `EVO-NFR-017`; `REQ-UC-EVO-051` | `EVO-FIX-SEMANTIC-CONFIRMATION` |

`TARGET-DELTA-007` 的 distribution-state 分类只摘要引用 `requirement-main.md` 中
`EVO-REQ-010` 的主定义；本 inventory 不另立第二份 transition 合同。

## 7. Intentionally not retained

| Removed shape/process | Current relation | 不保留理由 | 仍须证明的 successor |
| --- | --- | --- | --- |
| 21 active Skill、89 exits 及其具体 Skill/exit/schema id | selected-base `.42` inventory source identity | 固化数量会把 target 耦合 current graph | `CUR-CAP-001..023` 的 observable result 全量通过 |
| upstream `trellis-brainstorm` 作为 planning author | current workflow authoring mechanism | 用户已决定 Guru Team 完全替代 | `TARGET-DELTA-001..002` |
| raw upstream `trellis-spec-bootstrap` 作为 spec-boundary author | current bootstrap implementation path | 会自行选择 `.trellis/spec` 边界并写 authority，和 Guru bootstrap/RDT owner 冲突 | `TARGET-DELTA-011..012` 与 `EVO-FIX-SSOT-BOOTSTRAP` |
| raw upstream `trellis-before-dev` 的 auto-match/provider identity 与独立 spec 全文读取链 | current pre-implementation helper shape | 与 invocation-scoped authority reuse、task-free/标准 Phase 2 唯一 implementation owner 重叠 | `EVO-REQ-026` 的 Guru-owned `implementation_context`，并由两种 implementation profile 各自消费 |
| raw upstream `trellis-update-spec` 的直接写入与 code-spec authority | current auto-trigger write surface | 会绕过 repository RDT/Architecture/code-spec contribution governance，形成第二 Docs authority | Guru change lifecycle -> governed contribution/promotion -> 最小 `.trellis/spec` projection |
| raw upstream `trellis-meta` 的 callable/write surface | current bundled reference/maintenance shape | 普通自然语言可能抢占 direct answer 或绕过 canonical workflow/preset/overlay change lifecycle | Guru-owned lazy read-only reference projection；写请求由 `new change`/active lifecycle 承接 |
| task `prd.md`/`design.md`/`implement.md` 作为 repository Requirements/Design/Test 的替代或平行 authority | upstream/current task-centric planning model | 会允许 task planning 冒充或绕过 shared RDT，破坏项目长期文档中心与跨 task 连续性 | `TARGET-DELTA-008`：RDT-first 回读、task-local projection/contribution、serialized promotion 与 downstream freshness |
| parent task 默认递归处理 Git submodule | current/历史 repository discovery 与 validation 行为 | 无关 nested repository 状态会扩大 scope、制造副作用和阻塞，且不能成为 parent RDT/code authority | `TARGET-DELTA-009`：默认排除；显式 submodule change 使用独立 repository workflow |
| Issue Scope Ledger 与 `close_issues/related_issues/followup_issues` aggregate | current/历史 closeout shape | shared aggregate 不是 live closure authority | `CUR-CAP-013..015` 从 current Issue/diff/live provider 形成真实结果 |
| normal-path mandatory wording review / normal-scenario qualification | current specialist Skill 可用 | 重复 semantic owner、增加正常路径成本；若不区分 review-only/change-scoped 或忽略非成功 exit，会造成 caller ownership 漂移 | specialist standalone 与显式 active-caller 能力保留，所有 typed result 仍须唯一消费/重入，normal 调用为 0 |
| producer-private result、digest、完整 scan/stdout、授权记录、长篇 handoff summary、无 consumer gate artifact | current runtime/process shape | 可重建或无直接 consumer，扩大上下文并制造耦合 | 最小 public result、必要 private evidence 生命周期与 durable history |
| 固定 confirmation prompt/口令、`确认执行 <hash>`、identity/hash/digest/SHA/摘要复述与 script-side confirmation parser | 曾在正常协作中出现但与 current workflow semantic confirmation authority 冲突的过程形态 | 把 AI 语义判断下放给用户和字符串 matcher，制造无真实选择的往返并误把 digest 当授权 authority | `TARGET-DELTA-013`：完整计划、AI semantic affirmation、exact-action scope、stale re-display 与零 persistence |
| Architecture 2.0 的具体 profile/schema/exit id | current public contract shape | 保留方法论，不保留旧 API | `CUR-CAP-009,016` 的全生命周期 Architecture 结果 |
| 每个普通 change 都执行完整平台/Release matrix | 从来不是 current ownership 要求 | 会违背最小可靠验证 ownership | `CUR-CAP-019`：普通 scope-targeted，专项 owner 执行 exact matrix |
| legacy route、dual-read/write、wrapper、fallback 或只为旧 artifact 存活的 adapter | target migration 候选 | 用户明确要求只保留新合同；这里不保留的是旧 runtime consumer/合同形态，但不得导致既有 durable finish/history result 丢失 | existing migration 后全投影只含新合同；迁移前 active/resumable work 与 archived finish/history result 经新合同保持可恢复/可查询，retained ref/history 保持可达 |

## 8. Inventory completion contract

进入 Evolution Design 前，本 inventory 必须满足：

以下 completion contract 证明 current-to-target trace closure；其中 active Skill/interface/schema/
command/distribution/installed inventory 的 successor 完整性属于 consistency/installation trace，
不得扩大 `workflow/task_data/docs_authority` 三组 capability-loss comparison。

1. `.42` Design capability inventory 的每个 active Skill 都至少有一个明确的 current capability
   successor/classification；每条一对多映射都必须可解释且不得产生孤儿或冲突项。当前 successor
   差集、孤儿项与映射冲突均为 0。
2. `.42` 中具有产品意义的 `REQ-*`、`BEH-*`、`NFR-*` 与 Test capability 不得出现未分类孤儿；
   当前差集为 0。
3. 每个 `preserved_current` / `replaced_contract_shape` 项都能到达 target `EVO-REQ-*` 与至少
   一个 acceptance fixture；无法到达时必须补需求或显式改为 `intentionally_not_retained`。
4. `new_target` 不得引用任意 selected-base current capability、inventory row 或 PASS 冒充已实现；只能在 target Design/Test 建立 successor
   evidence 后成为 candidate capability。
5. Design 若改变本表的 capability 边界或发现 current omission，必须先回到 Requirements
   修订本 inventory 和对应 target requirement，不能在 Design 中静默补能力。
6. `EVO-CAP-001..004` 每项至少有一个 `TARGET-DELTA-*` 归属和一个可达 acceptance fixture；
   当前四项均已覆盖，Design 必须逐项承接，不能再把 RDT lifecycle 吞并回泛化 authority continuity。
7. 本节 1.2 的每个 shared-layer/host projection cell 与每个 supported host context cell 都必须
   有明确 `emitted`、`not-emitted`、`provider-only` 或 `retained-nonsemantic` 结论和依据；
   shared layer 只计一次，Codex/Claude/Cursor 三个 host 的 `main/default`、`inline`,
   `sub-agent`、`channel`、`native context/hooks` 五类 context 不得有未知项。Codex native
   以及 Claude/Cursor `trellis-start` 必须按 `hooks-enabled`、`hooks-disabled`、`no-hook` 独立
   取证；三类标签必须由 `EVO-REQ-080` 的七个互斥 setup discriminator cell 派生，不得与其做
   交叉乘积。每个 concrete fixture 恰好选择一个适用 cell：
   `enabled_approved`、`enabled_pending`、`enabled_denied`、`feature_off_config_present`,
   `feature_on_config_absent`、`feature_off_config_absent`、`configuration_unknown`；每 cell
   都记录 `user_feature_flag`、`project_hook_config`、`one_time_approval`、`emission`、
   `context_injection`。不存在 one-time approval surface 的 host 将 pending/denied cell 按 host/provider
   fact 标为 N/A，enabled success 记录 `one_time_approval=not_applicable`；unknown、配置/观察不一致
   或缺少真实 owner 时只能得到 role-local blocked。
   官方其它平台只能标为 source-only boundary，不得被计入 Guru target coverage。
8. 本节 1.3 的 17 个 logical stock asset 必须各出现且仅出现一次；每个 logical asset 的 role 必须属于四类枚举
   `suppressed_semantic_route`、`provider_only`、`explicit_only` 或
   `controlled_worker_provider`，且
   每行同时具备 successor/caller、真实 current direct consumer 或明确的 consumer handoff projection、projection cell、mutation/interception
   status、Design handoff、collision risk、candidate action 与 acceptance fixture。角色计数必须
   为 `suppressed_semantic_route=9`、`provider_only=1`、`explicit_only=2`、
   `controlled_worker_provider=5`。每个 provider/worker logical asset 还必须在 §1.3.1 具备 caller、
   profile、输入范围、最小 result/typed exit、真实 current consumer 或明确 handoff projection、回程与
   current/draft status；两个 explicit logical asset 还必须分别覆盖互斥的 standalone/embedded
   profile。`consumer_unbound`/`current_drift` 只能作为明确 Design handoff，不能计入 current
   closure。`retained_nonsemantic` 是不计入这 17 个 logical asset 的独立
   surface 类别；其三类 surface 必须拆成九个 host-bound row（每类三 host），各有 source
   locator、真实 host/policy consumer 或明确 handoff projection、mutation/status、preservation reason 与 fixture；任一未知、
   重复、孤儿或多重 role 都是 Requirements 阻断项。
9. `EVO-FIX-STOCK-COEXISTENCE` 必须先证明 `active_user_intent` 的 lifecycle preclassification
   （`lifecycle_bound_user_intent`/`independent_user_request`/`lifecycle_intent_binding_blocked`）再证明 suppressed semantic route 的 auto-dispatch 在第一项
   semantic 行为前由 admission guard redirect 或 fail closed（admission 不执行精确移除、patch、
   quarantine 或 delete），provider/worker result 回到唯一 caller，且
   不产生第二 owner、gate、question、全文读取或副作用；被动 startup/session/native context 不得
   抢占普通请求。`EVO-FIX-STOCK-MAINTENANCE` 只需证明每个 asset 的 Design 选定 action 在
   fresh/migration/update/upgrade/reapply/user-modification/sidecar 场景下都有 current 或
   caller-owned blocked/re-entry 结果：standalone policy/projection 对 suppressed asset 只产生
   `upstream_suppression_blocked`、对 provider/explicit/worker asset 只产生
   `provider_boundary_blocked`；clean-install、migration、Release 内嵌检查分别由其 caller 产生
   `clean_install_blocked`、`pre_migration_current_preserved \| migration_blocked` 或
   `release_pre_publish_blocked`。已选 role/target/action 必须标为 completed/pending/unknown，
   首次全 pending 必须显式得到 `stock_policy_action_required`，并绑定当前
   `file_state`/`context_state`/`sidecar_state`、不可逆边界与唯一恢复 owner；已完成或不可逆 action
   不得重放，recovery 前只在 identity/decision-relevant facts 变化时定向 fresh reread，并只从
   对应 exact policy/caller/host owner 重入。未选 action 不要求额外验证。retained row 的不安全结果
   为 `retained_context_blocked`，不得借用 provider result；child validator 不得夺取 caller ownership，
   且每个结果必须只从对应 exact owner 重入。standalone exact explicit-only 只读结果还必须可投影为
   `explicit_provider_result_current` 并由 direct-answer owner 完成；channel/worker 与 embedded read-only
   result 只回 exact caller，任何写入意图在 raw explicit invocation 前回到 `new change`/active caller。
10. `EVO-REQ-053` clean-install closure 必须使用独立 clean fixture，并先证明
    `distribution_state_preclassification=clean_target`：初始 repository 的 active
    `.trellis/workflow.md` 缺失，且无任何可归属 official Trellis/Guru managed installation state；
    可唯一归属的 official Trellis config/template-hash/scripts/spec/task/workspace/manifest 即使 workflow 与
    Guru projection 均缺失也必须转入 migration，不能当作普通用户文件；non-Guru workflow 的
    identity/provenance/owner 或当前安全 transition plan 未唯一收敛时，必须先得到
    `foreign_workflow -> distribution_state_blocked`，不得进入 clean 或 migration；收敛后只重入
    preclassification 并转为 `existing_migration_target`，source workflow 保留到唯一 cutover，不得要求
    先 mutation。partial/legacy Guru surface 必须转入 migration，mixed/unknown/unowned/multiple identity
    必须得到 `distribution_state_blocked`。source/candidate identity、`trellis/index.json` identity、
    fresh-init/preset provider stimulus、application/validation current、created resources、shared layer
    与 Codex/Claude/Cursor projection cells、executable bit、user modification/sidecar state 和
    exact-step blocked/re-entry 均必须可查询。`EVO-REQ-054` migration closure 是一个
    `distribution_state_preclassification=existing_migration_target` 的 existing-migration composite invocation，五个 provider substep 必须按
    `MIG-CELL-INSTALL -> MIG-CELL-UPGRADE -> MIG-CELL-UPDATE -> MIG-CELL-WORKFLOW-SWITCH -> MIG-CELL-PRESET-REAPPLY`
顺序覆盖；不能以一个 substep 的结果代替其它 substep，也不能把现有 verifier 的单次 composite
result（当前 existing cell 仅覆盖 `UPGRADE -> UPDATE(dry-run 分支) -> WORKFLOW-SWITCH ->
PRESET-REAPPLY`，不含 preservation-mode INSTALL）解释成五个独立 terminal 或五-cell target
closure。共享一次 migration preflight、WORKFLOW-SWITCH 显式 `--force`
    application（或在该有序 boundary 对已字节相等 target 的 current 观测）形成的唯一 cutover，以及一次 post-cutover final validation；
    invocation entry 读取到 byte-equal target 不得提前推进 composite cutover，也不得把此前适用 substep
    finding 改判为 post-cutover；
    每个 substep 另绑定 source/target、applicability、provider flag/profile、step-local live delta、
    provider owner、exact-step blocked/re-entry 与受影响 sidecar，composite context 只盘点一次
    active/resumable/archive/finish/history/retained-ref、RDT/Architecture authority 与最终
    legacy-consumer absence。每个 invocation 只执行 applicability 为 applicable 的 substep；每个
    `not_applicable` 必须有 provider/help 或 live-state 依据，五项全 N/A 仍形成 composite current 并
    执行一次 final validation。任何 substep 未覆盖、INSTALL 误用 `--workflow` 声称替换 existing workflow、
    或 step-local result 冒充 `new_contract_current` 的计数均为 0；WORKFLOW-SWITCH preview/preflight
    及其之前的适用 substep 出现 finding 时，composite 可在未进入 cutover、未执行 final validation 时
    直接得到 `pre_migration_current_preserved` 并停止；进入 `migration_cutover_current` 后必须形成
    `migration_preset_reapply_current`（适用 step current，或有依据的 `not_applicable` current
    observation），并只在全部适用 substep current 后执行一次 final validation。cutover 后的
    WORKFLOW-SWITCH、PRESET-REAPPLY 或 final-validation finding 按 live state forward recover，并分别
    重入 `migration_cutover_current`、`migration_preset_reapply_current` 或
    `migration_final_validation_current`，最终只产生 `new_contract_current` 或 `migration_blocked`；final validation current 前 target consumer
    调用数为 0。三类是唯一 composite terminal，substep 不产生独立 terminal，cutover 前的 finding
    不得直接产生 `migration_blocked`。
11. 每个需要 repository authority 的 normal invocation 必须有一个只建立一次、可被所有下游
    caller/worker 复用的 private invocation-scoped `context_envelope`；其中的
    `authority_context`、含 provenance 的 `stock_policy_context` 与 `provider_context` 是按需
    projection，不是独立回读链。task-free 与标准 Phase 2 implementation 还必须从该 envelope
    派生同一 Guru-owned `implementation_context` 合同，每次恰好绑定一个 implementation owner；
    raw `trellis-before-dev` 调用数与第二套 spec 全文回读链均为 0。`new change -> standard change`
    的 Intake 只绑定 current RDT
    Requirements/Design/Test、authoring/review/lifecycle contract 与必要 live facts，Architecture
    slice 明确为 N/A；进入 pre-design Planning 后，同一 envelope 才按需绑定 Architecture Baseline/
    constitution/change contract 与适用片段。active task 的 `prd.md`/`design.md`/`implement.md` 只绑定
    current authority locator/identity、task-local delta、reconciliation 与 execution/validation/delivery
    mapping，不成为平行 RDT/Architecture。适用 RDT、Architecture 与 task 三件套按稳定 locator/identity/
    order 形成 context prefix，current live facts 与 delta 形成最小变化 tail；host/model/provider cache
    只能优化该读取，不进入 authority、freshness 或 PASS。其它 normal invocation 按最小 applicability 绑定 current
    RDT 与 Architecture 的 identity/适用片段、stock source/projection 和必要 live facts；不适用 slice
    明确为 N/A。direct answer、非 stock stop/history/specialist、task-free 与 standalone read 只绑定其
    答案或受影响 surface 所需的最小 facts。每个 AI owner 直接从上述 current context 自主判断，不消费
    前一 owner 的 assignment/signoff/transaction handoff 或重复事实摘要。没有语义依赖变化时不得重复
    读取完整 authority/package provenance 或把 task-local artifact 当作 SSOT，发生变化时只从最早受影响
    owner 定向失效对应 projection 和下游 freshness。该项只验证 envelope/projection/consumer/freshness
    结果，不新增 public schema、cache artifact 或实现载体。
12. `EVO-FIX-LATEST-INTENT` 的 inventory closure 只核验 `requirement-main.md` 主定义列出的输入/结果组合及其 fixture 可达性；其中 `REQ-REV-100` 的 bound override identity/envelope/receipt boundary 必须有独立 closure 行。每个组合必须有唯一 consumer、identity/freshness evidence 与 exact re-entry successor，覆盖率为 100%。`independent_request_isolation_pending` 的 progress-refresh、safe-clear/re-entry 与 no-progress/invalid-handle/non-consumable-owner -> `independent_request_isolation_blocked` 三类 liveness 分支也必须逐一可达；无界 pending、无进展仍 pending、重复 pending、pending 无 consumer、重复或遗漏 receipt、旧 identity/envelope/candidate/receipt reuse 或错误默认 new change 的计数必须为 0。具体行为与顺序只由 `requirement-main.md` 主定义，inventory 不重复定义。
13. #311/#312 的 accepted scope、exact merge identity 与 selected-base reachability 已由 PR #313/#314
    与 `source_ref=5650df47…` 分维度证明；本 inventory 也已从该 exact merge/base identity fresh rebind
    `.42` RDT、Architecture、capability 与 Test authority，并把两项 reclassify 为
    `selected_base_current_capability`。#311 必须通过 `CUR-CAP-013/014/017/018/019` 到达
    `EVO-REQ-037,053,082..084`、installed/self-hosted publication、exact platform-set preservation、
    verifier failure evidence 与
    prerequisite fixture；#312 必须通过 `CUR-CAP-012` 到达 `EVO-REQ-032,082`、clean-tracked
    continuation、unrelated-dirty isolation 与 real-blocker fixture。`CUR-CAP-001..023`、
    `TARGET-DELTA-001..013`、`EVO-REQ-001..084`、`EVO-NFR-001..034` 和 50 个 normal-path fixture 的
    Requirements-stage successor 差集、旧 snapshot/review 复用、source/target 混淆、platform subset
    扩张/invalid identity 延迟失败、null verifier failure、completed mutation replay 与 unrelated-dirty
    误分类计数均为 0。fresh Requirements 双审与确定性闭包已针对同一 exact identity 通过，本 inventory 当前为
    `requirements_trace_ready_for_design`；该 Requirements-stage closure 本身不证明 Design successor current。
    pre-`REQ-REV-142` Design mapping/review 仍为 stale historical evidence；Requirements ready 后执行的 current
    fresh Design review 与确定性闭包已建立 `evolution_refactor_eligible`，本 completion contract 仍不得复用旧
    Design gate。
14. `.42` 相对 `.41` 的 `REQ-052..055`、`DES-049..052`、`TST-036..039`、`SCN-048` 必须保持
    `fact_only_authority_alignment`：它们只承接 `.42` unique-current、`.3/.39/CLI 0.6.15` identity
    separation、serialized promotion 与未验证 Release gate，不得生成第 24 个 `CUR-CAP-*`、第 14 个
    `TARGET-DELTA-*`、第 51 个 Evolution fixture、额外 public Skill/exit 或新的 Design responsibility。
    `a41b8a34...9f560ec1` 的四提交 delta 同样保持 fact-only：只允许更新 exact source locator、#267
    lifecycle evidence、dogfood provenance 与 archive/merge facts，不得改变该 capability-loss closure。
15. `9f560ec1...736ef333` 的 PR #317 delta 是 material current behavior advance，不得归入上一条
    fact-only classification。它必须经 `CUR-CAP-013/014/017 -> EVO-REQ-084 / EVO-NFR-034 ->
    EVO-FIX-INSTALLED-PROVENANCE-PUBLICATION` 形成 successor；不得生成第 24 个 `CUR-CAP-*`、第 14 个
    `TARGET-DELTA-*`、第 51 个 fixture、第 74 个 Design responsibility 或额外 public Skill/exit。
16. `736ef333...5650df47` 的 PR #318 delta 必须保持 `fact_only_inventory_provenance_alignment`：只允许
    更新 exact source locator、Finalizer caller-inventory identity、#267 related-only disposition、dogfood
    provenance 与 task archive/merge facts；不得改变任一 observable behavior、public Skill contract、`.42`
    authority、Release identity、`CUR-CAP-*`、`TARGET-DELTA-*`、fixture、Design responsibility、Skill 或 exit。
