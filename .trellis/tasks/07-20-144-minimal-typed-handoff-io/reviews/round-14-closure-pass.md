# #144 Branch Review Round 14 问题闭环审查报告

## 审查元数据

- 逻辑角色：`问题闭环审查代理`
- 技术身份：`/root/issue_144_round10_replacement_review`
- 复用决定：`reuse-for-closure`
- Finding owner 来源：Round 10/11 `F-BR-P3-011`
- Reviewed HEAD：`87bb90a4c5bd556ba25ca409acfc58ccbbbafa6b`
- Base / merge-base：`origin/main@cbd0396a2ddb7dd0efa613be7b7d93790eb2e34d`
- 完整 diff：101 files，25017 insertions，352 deletions，8 commits
- 当前提交：`fix(trellis): #144 修正 surrogate pattern 消费`
- 审查方式：只读审查完整 `origin/main...HEAD`
- 问题计数：P0=0、P1=0、P2=0、P3=0，`findings_count=0`
- Typed conclusion：`closure_passed`
- 原始报告路径：`.trellis/tasks/07-20-144-minimal-typed-handoff-io/reviews/round-14-closure-pass.md`
- 本代理未编辑文件，未调用 `review-branch`、`check-review-gate`、`record-agent-assignment`、任何 `record-*`、commit、push、PR 或 finish-work。

## Findings

未发现新的 current-scope P0-P3 finding。

## 审查范围

本轮重新核对了 approved `prd.md`、`design.md`、`implement.md`、Docs SSOT Plan、`implementation-handoff.md` 第 20 节、最新 `phase2-check.json`、commit plan 008、issue scope ledger、Round 10/11 原始 finding 报告，以及完整 `origin/main...HEAD` 文件和提交范围。

代码审查覆盖 portable pattern grammar、UTF-16 input projection、pair-aware consuming、zero-width search positions、negative lookahead、anchors、alternation、nullable paths、quantifier backtracking、canonical/installed runtime、fixed/generated Node differential、interface 1.3 schema、production 1.2 compatibility、preset installer 与三平台 inventory。

## F-BR-P3-011 问题生命周期

- Round 10：发现 Python regex 对 trailing newline 的 `$` 语义与 Node/Ajv 不一致，`F-BR-P3-011` 作为 current-scope P3 打开。
- Round 11：trailing-newline 复现已修复，但本 finding owner 发现 `pattern="(?!^|$)"`、`instance="😀"` 的 UTF-16 interior zero-width 差异，finding 保持 open。
- 后续实现将 instance 投影为 UTF-16 code units，使零宽搜索保留 surrogate pair interior boundary，并为 `.`, `\S` 与 negated class 增加 pair-aware consuming。
- Round 12 Phase 2 扩大 isolated-surrogate 对照后，在 4,081 patterns × 7 values = 28,567 comparisons 中发现 154 mismatches。最小复现为 `pattern="^..$"`、`instance="\ud800a"`；finding 继续保持 open。
- Round 13 实现修正 single-unit guard，并通过完整 Phase 2。
- Round 14 由同一 finding owner 复用执行 closure review；本轮独立验证未再发现差异，`F-BR-P3-011` 关闭。

## F-BR-P3-011 闭环判断

Canonical runtime 当前先通过 `skill_utf16_code_units()` 将 Python Unicode string 投影为 JavaScript UTF-16 code units。`skill_ecma_code_point_complement()` 的行为为：

- 在 valid high+low surrogate pair 起点一次消费完整 pair。
- single-unit branch 不能在 valid pair 起点抢先消费 high surrogate。
- single-unit branch 不能从 valid pair 的 interior low surrogate 开始。
- isolated high surrogate 可独立消费。
- isolated low surrogate 可独立消费。
- isolated high/low 前后的 BMP code unit 不会被错误归入 pair。
- 零宽 assertion 仍可在 valid pair 的 UTF-16 interior boundary 成功。
- nullable path、alternation 与 quantifier backtracking 不能把 valid pair 拆成两个 consuming atoms。

该实现是通用 pair-aware translation，不包含 Round 11 或 Round 12 复现值的特判。Production runtime 仍仅使用 Python standard library；Node 只作为测试 oracle。

## 独立目标探针

本轮对以下关键场景逐项比较 canonical runtime 与 Node 20.20.2 原始 `new RegExp(pattern, "u").test(value)`，结果全部一致：

| 场景 | Runtime | Node 20 |
|---|---:|---:|
| `(?!^|$)` 对 astral pair interior 零宽匹配 | true | true |
| `^..$` 对 isolated high + BMP | true | true |
| `^..$` 对 BMP + isolated low | true | true |
| `^.$` 对 valid pair | true | true |
| `^..$` 对 valid pair | false | false |
| `(?!^|$).$` 禁止从 interior low 消费 dot | false | false |
| `(?!^|$)\S$` 禁止从 interior low 消费 nonspace | false | false |
| `^(?:.|){2}$` 对 valid pair nullable alternation | true | true |
| `^(?:a|.){2}$` 对 isolated high + BMP backtracking | true | true |
| `^(?:a|.){2}$` 对 valid pair 不可拆分 | false | false |

## 独立生成对照

本轮另行构造了与仓库测试生成器独立的组合矩阵：

- 2,815 个 accepted patterns。
- 32 个 values。
- Values 覆盖 isolated high/low standalone、各自 BMP 前后、valid pair、pair interior、连续及交错 surrogate、astral/BMP 邻接、两个 astral、line terminators 与 whitespace。
- Patterns 覆盖 `.`, `\S`, positive/negated class、普通 literal、所有主要 nullable/consuming quantifier、两 atom concatenation、capturing-equivalent group、alternation、empty alternative、anchors、negative lookahead、nested negative lookahead 与 backtracking。

独立结果：

- Node 20.20.2：90,080 comparisons，0 mismatch。
- Node 21.7.1：90,080 comparisons，0 mismatch。
- Grammar-rejected generated pattern：0。
- Runtime/Node mismatch：0。

该证据直接覆盖 Round 11 的 zero-width interior 变体和 Round 12 的 isolated-surrogate 变体，支持 `F-BR-P3-011` 已关闭。

## 完整验证证据

本轮实际执行并通过：

- Node 20 Skill package suite：126/126 passed。
- Shared runtime：548 passed，13 skipped。
- Preset installer：39/39 passed。
- Upstream ownership：6/6 passed。
- Source Skill validator：passed；9 active、9 legacy、0 production minimal、35 exit markers。
- Installed Skill validator：passed；384 managed files、Claude/Codex/Cursor、0 sidecar、0 removal、0 conflict。
- Dogfood overlay drift：passed。
- Upstream ownership inventory：43 frozen/active entries、13 managed claims，全部一致。
- Canonical/installed runtime byte comparison：passed。
- Interface 1.3 canonical/installed/representative fixture byte comparison：passed。
- Frozen interface 1.2 schema 与九个 production packages 相对 `origin/main` 无 diff。
- Canonical/installed extension inventory 一致：9 legacy，1.3 production public/private inventory 为空。
- `git diff --check origin/main...HEAD`：passed。
- Recursive `.new`/`.bak` scan：0。
- Runtime Node/version branch scan：0。
- Added TODO/FIXME/skip/xfail scan：0。
- Source checkout：clean，`main@cbd0396a`。
- Live Issue #144、#145、#146：均为 OPEN。

Round 13 Phase 2 的额外证据保持有效：

- Node 20 raw generated differential：4,081 × 33 = 134,673，0 mismatch。
- Node 26 test-only spec-equivalent wrapped differential：134,673，0 mismatch。
- Focused portable-pattern suite在 Node 20/26 均为 4/4。
- Clean public-sample throwaway 覆盖 init、workflow preview/switch、初装、`trellis update`、preset reapply、initial/after-update/no-developer smoke、三平台 copies 与最终零 sidecar。
- Phase 2 `typed_exit=passed`，`F-BR-P3-011` 状态为 `resolved`，open current-scope finding 为 0。

## Commit plan 008

Commit plan 008 精确提交十个 task-reviewed paths，保留 assignment、历史 commit plans、review gate、review rollup 与 Round 1-11 raw reports 等父流程 metadata。

- Commit SHA：`87bb90a4c5bd556ba25ca409acfc58ccbbbafa6b`
- Parent：`7f5a325896c2819b4353b2da2e1c5635182ec930`
- Expected tree 与 actual tree：`34222a9b424fc4e715971a5ee7ea65dde9a66f00`
- 所有 committed path 的 blob/mode 均匹配。
- `hook_mutation=false`
- Commit message 为中文 Conventional Commit，只使用 `Refs #144`。
- 未提前关闭 #144，未把 #145/#146 吸收进当前提交。

当前 task worktree 仅包含父流程维护的 assignment、commit plan 与 review metadata；测试和本轮只读审查未产生 non-metadata dirty path。

## Issue 与范围

Live Issue #144、#145、#146 均为 OPEN。

`issue-scope-ledger.json`：

- 仅 #144 位于 `close_issues`。
- #145/#146 位于 `followup_issues`，继续负责九个 production Skill payload migration。
- #98、#109、#115、#127、#131、#132 仅为 related issues。
- 当前实现未迁移 production payload，范围没有扩张。

F-BR-P3-011 位于 #144 validator 基础设施 current scope；其闭环不改变上述分类。

## Docs SSOT

Docs state 保持 `complete_docs`，批准策略保持 `ssot_first`。

- Exact printable-ASCII portable pattern EBNF 仅由 `.trellis/spec/workflow/skill-package-contract.md` 拥有。
- 该 SSOT 现在明确区分 UTF-16 zero-width search position、valid pair 不可拆分消费、interior low 不可作为 consuming 起点、isolated surrogate 独立消费及 BMP 邻接。
- `.trellis/spec/workflow/companion-scripts.md` 只描述实现边界。
- `.trellis/spec/workflow/quality-guidelines.md` 只规定 fixed/generated regression、七个 surrogate edge values 与 Node differential 义务。
- Root/workflow/preset README 只概括 portable ECMA boundary 并指向 durable contract，没有复制 EBNF。
- `data-contracts.md`、requirements docs、registry/schema id、typed exits 与 workflow routes 无需因本轮内部 matcher 修复而重复变更。
- Implementation handoff 第 20 节中的长期语义 delta 已合并到 durable docs；具体复现值、mismatch 统计、Node 版本与逐轮 finding lifecycle 保持 task-history-only。

未发现 durable docs、runtime、tests、installed bytes 或 approved Docs SSOT Plan 之间的 current-scope 不一致。

## Upgrade / Update 与开箱即用

Canonical 与 installed runtime 字节一致，dogfood overlay drift 为零，ownership inventory 与 managed claims 全部通过。Round 13 fresh throwaway evidence 覆盖：

- Marketplace discovery 与本地未发布 workflow sample。
- Clean repository init。
- Workflow preview/switch。
- Preset 初装。
- Installed wrapper/package smoke。
- `trellis update`。
- Workflow/preset reapply。
- Initial、after-update 与 no-developer fixtures。
- Claude、Codex、Cursor 三平台 copies。
- 最终零 `.new`/`.bak`、零 removal/conflict/sidecar。

未发现新仓库安装、upgrade/update、reapply 或平台 overlay 漂移问题。

当前 feature branch 尚未 push，immutable exact remote feature-ref marketplace verification 仍由 post-push/pre-PR Remote Marketplace Verification Gate 补证。该项不属于本地 implementation finding，也未被 public-sample evidence 冒充为已完成。

## 兼容性

- 九个 production Skills 仍全部为 interface 1.2 + `legacy`。
- Production `minimal_handoff=0`。
- Production public input、typed output 与 private artifact 1.3 inventories 保持为空。
- Interface 1.3 canonical/installed/fixture bytes 一致。
- Existing typed exits、mandatory routes、discovery DTO 与 consumer contracts 未变化。
- #145/#146 migration timeline 保持不变。

F-BR-P3-011 的修复只收紧 #144 新增 validator 的跨 consumer correctness，不造成 public API 破坏或提前 migration。

## 部署与安全

Added-line secret、private key、credential、signed URL 和 database URL 扫描无命中。未发现 `.env`、客户数据或敏感原始记录泄漏。

完整 diff 不涉及：

- CI/CD workflow
- Docker/Compose
- Kubernetes/Kustomize/Helm
- Database migration
- Terraform
- Makefile
- Service/API/worker deployment configuration

因此无服务部署、配置迁移或数据迁移影响。所有复现均使用标准 JSON escaped Unicode 字符串和普通 accepted schema，属于 honest-but-fallible 正常路径，不依赖恶意篡改、竞态、TOCTOU、fault injection 或流程绕过。

## 观察项

Node 26.4.0 raw V8 对少量 astral negated-class pattern 存在已知优化偏差。仓库测试只在 Node 26 oracle 中使用 spec-equivalent `(?:pattern){1}` wrapper 绕过该优化；Node 20 raw original-pattern differential 与本轮 Node 20/21 raw independent differential 均为零 mismatch。Production runtime 不包含 Node/version 分支。

该项是独立 oracle 的上游版本观察，不是当前实现 finding。

## 后续候选

无新的 current-scope 或 out-of-scope follow-up candidate。

#145/#146 已存在并继续负责 production Skill migration，不因本轮 closure 新建或改分类。

## 结论

Round 14 closure pass：

- P0=0
- P1=0
- P2=0
- P3=0
- `findings_count=0`
- `reuse_decision=reuse-for-closure`
- `typed_conclusion=closure_passed`

`F-BR-P3-011` 已关闭，未发现新的 current-scope P0-P3 finding。

该结论只完成 finding owner closure，不是最终 Branch Review 放行。`/root/issue_144_round10_replacement_review` 已作为 finding owner 和 closure agent，不得担任最终放行代理。

下一步必须调度一个此前所有 review rounds 均未使用过的新 `最终放行审查代理`，对当前完整 HEAD 独立审查。只有该最终轮 `findings_count=0`，主会话才能记录 passing Branch Review Gate；之后仍须等待用户明确调用 `trellis-finish-work`。
