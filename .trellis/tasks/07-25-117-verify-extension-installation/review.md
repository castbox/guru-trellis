# #117 Branch Review 汇总

## 审查身份与范围

- 当前 reviewed HEAD：`a47e1fbd7bedb001649814969096076bb70157db`
- 完整 committed 范围：`origin/main...a47e1fbd7bedb001649814969096076bb70157db`
- Merge base：`0cd2498f821b38ce91bd82fa9e232b1528241e5d`
- Round 1/2 原始报告：[初始 finding 报告](reviews/001-final.md)
- Round 3 原始报告：[F1/F2 closure 报告](reviews/002-closure.md)
- Round 4 原始报告：[F7 finding 报告](reviews/003-final.md)
- Round 5 原始报告：[F7 closure 与 F8 finding 报告](reviews/004-f7-closure.md)
- Round 6 原始报告：[F8 closure 报告](reviews/005-f8-closure.md)
- Round 7 原始报告：[fresh final-intent 与 F9 finding 报告](reviews/006-final.md)
- Round 8 原始报告：[F9 closure 报告](reviews/007-f9-closure.md)
- Round 9 原始报告：[fresh final-intent 与 F10 finding 报告](reviews/008-final.md)

Round 8 由未参与 F9 发现与实现的 fresh 闭环 reviewer 覆盖完整范围并关闭
`BR-117-F9`，没有发现新的 qualified finding。Round 9 由未参与任何 earlier
closure 的 fresh reviewer 重新覆盖完整最终范围，但资格化新的 `BR-117-F10`；
因此该轮必须透明登记为问题发现审查，不能冒充 zero-finding final pass。

## 已关闭 finding

### `BR-117-F1` P1：credential URL 脱敏漏检

状态：`closed`

Round 3 已复核 authority-userinfo 检测、artifact write 前 fail-closed、generic public
error、独立 probes、production eval、secret scan 与 canonical/installed bytes。

### `BR-117-F2` P1：task-bearing 调用未验证 task/worktree identity

状态：`closed`

Round 3 已复核 active task、task-start-context、repo、branch、active pointer 与
workspace boundary 统一 gate，以及 wrong task、archived task、wrong repo、
wrong branch、wrong worktree 与 taskless standalone。

### `BR-117-F7` P2：recorder 未执行输入 schema，并接受不存在的 supersession lineage

状态：`closed`

Round 5 已复核 schema-before-access、受控 `WorkflowError`、no-prior/wrong-prior
拒绝、exact-prior supersession、changed-plan re-entry、runtime/package tests 与六处分发
一致性。关闭证据绑定 [F7 closure 与 F8 finding 报告](reviews/004-f7-closure.md)。

### `BR-117-F8` P3：closure raw report 的 EOF 多余空行

状态：`closed`

Task commit 004 仅删除 `reviews/002-closure.md` 的一个 EOF 多余空行。Round 6 在
`3281db77...` 对 exact blob、commit tree、完整 range 与 dirty whitespace gate
完成独立复核，关闭证据绑定 [F8 closure 报告](reviews/005-f8-closure.md)。

### `BR-117-F9` P2：annotated stable tag 未绑定实际 checkout commit identity

状态：`closed`

Task commit 005 分离 direct ref object 与 peeled commit，按 resolved commit checkout，
并在 throwaway 前执行 `git rev-parse --verify HEAD^{commit}` 后精确比较。Round 8
重新验证 branch、lightweight tag、annotated tag、mismatch fail-closed、checker
freshness、public projection、contract、tests、commit tree 与六处分发，关闭证据绑定
[F9 closure 报告](reviews/007-f9-closure.md)。

## 当前 finding

### `BR-117-F10` P2：成功 executor 未保留 installed asset digests

状态：`open`

Round 9 复核成功路径后确认：

- `asset_digests` 仅包含 remote source checkout 的 9 个 `trellis/**` source path；
- facts 未记录 clean throwaway target 中 installed
  workflow/preset/schema/skill/platform assets 的 digest 或 category completeness；
- 所有 selected capabilities 共用最后一个 throwaway command 的总体 status 与
  `evidence_step`，没有逐 capability installed asset evidence；
- schema、example 与 normal-path tests 均未要求 missing/mismatch installed digest
  在 `verified` 前 fail closed。

Live Issue #117、approved PRD 与 design 明确要求 Recorder 在 owner-private evidence
中保留 installed workflow/preset/schema/skill/platform digests，并让 AI Gate 审查
命令事实与安装资产。该缺口存在于任何正常 pushed-ref success path，不依赖恶意输入、
伪造、竞态、TOCTOU 或其它已排除场景，属于
`normal_required_behavior`。完整 qualification 与 required closure 见
[Round 9 原始报告](reviews/008-final.md)。

## 验证、文档与影响

Round 9 fresh 验证通过：

- runtime 596 tests passed、13 skipped；
- Skill package 175、preset + ownership 54；
- canonical/installed contract 各 8/8；
- source/installed validators 各 12 active Skills、46 exits、12 invokes、27 targets；
- installed manifest 2,322 managed files，0 sidecar/removal/conflict；
- dogfood drift、ownership、六处分发、runtime/package equality、JSON/Bash/Python
  syntax、三类 `git diff --check` 与 non-fixture sidecar scan。

这些通过证明当前安装与分发测试没有失败，但不会补写 owner-private artifact 中缺失的
installed asset digests，因而不反证 F10。

Docs SSOT strategy 继续为 `ssot_first`。Durable Issue/PRD/design 已要求 installed
asset digest inventory、逐 capability asset evidence 与 AI adequacy review；F10 是
runtime/schema/example/tests 未完整承接既有 approved SSOT，不能通过弱化文档关闭。
修复应同步必要 runtime、schema、example、contract、tests 与 canonical/installed/
Agents/Codex/Claude/Cursor 分发副本，并重新验证 install/update/reapply 与
upgrade/update 抗漂移。

当前完整范围没有 CI/CD、容器、Compose、K8s/Kustomize、数据库 migration、Makefile、
dependency manifest 或生产数据面变化。F10 是 extension verification evidence
correctness 问题，不新增 hostile-input/security scope；installed digest evidence
仍只能保留去敏 path/digest/category facts，不能持久化 credential URL、secret、
raw command output、临时绝对路径或 native transcript body。

Claude clean-auth source/installed 当前首轮均 7/7；Cursor 按合同返回
`unsupported`。Exact pushed feature-ref clean installation 仍是授权 push 后的
publication gate，当前 local-source throwaway 不冒充该证据，也不替代 F10 修复。

## 当前路由

当前 Branch Review typed exit 必须为 `implementation_required`，唯一 open finding 是
`BR-117-F10`。Implementation owner 修复后，必须重新完成 `guru-check-task`、fresh
task commit、独立 F10 closure 与独立 fresh final review。

本汇总和 raw reports 不授权 publication、push、PR、Issue #117 closure 或
`finish-work`。
