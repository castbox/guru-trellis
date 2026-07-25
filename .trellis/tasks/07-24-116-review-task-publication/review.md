# Issue #116 Branch Review 汇总

## 审查范围

- Base：`origin/main@bdc8f50bcd1e325aed331d4b01107b83ed8ee940`
- Reviewed HEAD：`1dd2ef8af1cf583eeaf302a11c4770a07922b0b2`
- 完整范围：`origin/main...1dd2ef8af1cf583eeaf302a11c4770a07922b0b2`
- 规模：337 files、2 commits
- Issue scope：close `[116]`；related `[115,131,144,146]`；follow-up `[81,117,118,119,132]`
- Docs SSOT：`ssot_first`；Phase 2 记录的 16 个 durable paths 当前 digest/size 无漂移

## 审查轮次与生命周期

- [Round 01：完整范围独立审查，发现 1 个 P2](reviews/round-01-final-release.md)
- [Round 02：同身份问题发现 owner 归属与正常路径复现](reviews/round-02-problem-discovery.md)
- [Round 03：原 finding owner 验证修复闭环](reviews/round-03-problem-closure.md)
- [Round 04：全新最终放行审查，发现 1 个 P1](reviews/round-04-final-release.md)

Round 01/02 的 `BR116-R02-P2-01` 已由相同 technical identity 在 Round 03
完成 closure，当前 exact publication allowlist、`pr-readiness.json`
self-exclusion 和 finalization-only `closeout-plan.json` 行为成立。Phase 2 Round 6
的 `PH2-116-R6-P2-01` 也保持关闭，`git status` 失败会贯穿 binding、entry、
checker 与 finalization，而不会退化为空路径集合。

Round 04 使用未参与 implementation、Phase 2 或前述 finding lifecycle 的 fresh
identity，重新覆盖 live Issue #116、accepted-current comment、规划、8 个 curated
spec、完整 committed diff、Phase 2、commit evidence、package/platform
distribution、测试与 fresh install/update/reapply。该轮发现新的正常路径 P1，因而
不能作为最终放行依据；该审查身份现成为此 finding 的技术 owner，修复后只能执行
closure，最终放行仍须换用另一全新身份。

## 当前问题

### BR116-R04-P1-01：publication recorder/checker 在 installed 与平台布局中无法定位 dispatcher

- Severity：`P1`
- Scenario：`normal_required_behavior`
- Status：`open`
- Owner round：`4`
- Reviewed HEAD：`1dd2ef8af1cf583eeaf302a11c4770a07922b0b2`
- 影响路径：
  - `trellis/skills/guru-team/packages/guru-review-task-publication/scripts/record-task-publication-review.sh`
  - `trellis/skills/guru-team/packages/guru-review-task-publication/scripts/check-task-publication-review.sh`
  - installed shared 与 `.agents/.codex/.claude/.cursor` 同名副本
- 合同依据：
  - `interface.json` 的 `publication_review_recorder` / `publication_review_checker`
  - `SKILL.md` 的 `AI Review Gate -> package recorder/checker -> typed exit`
  - `implement.md` Step 5 / Step 11
  - `.trellis/spec/preset/installer.md` 的 fresh install/update/reapply 可运行性
- 正常路径复现：
  - installed shared recorder/checker 2/2 返回 rc 1；
  - `.agents/.codex/.claude/.cursor` recorder/checker 8/8 返回 rc 1；
  - 脚本错误地在各自 package root 下追加
    `.trellis/guru-team/scripts/bash/run-skill-command.sh`。
- 根因：两个 validator wrapper 只剥离 canonical
  `trellis/skills/guru-team/packages/...` suffix，没有复用同包 `invoke.sh` 与
  `guru-review-branch` 已实现的六布局 repo-root resolver。
- 影响：active Skill 在十维 semantic Gate 后不能通过 interface 声明的
  recorder/checker 记录和复验 `pr-readiness.json`，workflow 与 standalone
  均无法形成任一 typed exit。

## 被拒绝候选与限制

- Phase 2 首次 throwaway 的空 response 在后续同 fixture、clean throwaway、
  Branch Review 复验中均未复现，保持 `rejected_candidate`。
- 当前分支尚未 push，因此未执行 exact remote candidate-branch marketplace
  install；public marketplace discovery 与 local unpublished workflow sample
  已验证。该限制不影响本地 recorder/checker 正常路径复现。
- 未使用恶意 artifact/hash/state 篡改、对抗性输入、并发、TOCTOU、锁或 fault
  injection 构造 finding。

## 验证证据

- Runtime：572/572，13 skipped
- Skill packages：174/174
- Preset：45/45
- Ownership：9/9
- Source/installed publication actual-wrapper eval：7/7 × 2
- Exact allowlist/finalization 定向回归：4/4
- Source/installed validators：11 active Skills、42 exits、25 targets；
  installed 2100 managed files，sidecar/removal/conflict 为 0
- Fresh throwaway install/update/reapply：exit 0
- Canonical/installed/platform byte parity、overlay drift、`git diff --check`、
  Python compile、shell syntax：通过
- Recorder/checker multi-root 真实命令执行：installed 2/2、四平台 8/8 失败，
  稳定复现当前 P1

现有绿测不反证该 finding：multi-root wrapper test 只覆盖 `invoke.sh`，actual-wrapper
eval 的 owner staging 直接进入 runtime/dispatcher，fresh throwaway 也没有直接执行
interface 中这两个 validator wrapper。

## Docs SSOT、安全与部署

Docs strategy 仍为 `ssot_first`，16 个 durable paths 与 Phase 2 evidence 一致；
但实现未兑现 installer 与 Skill 合同声明的 installed/platform runnable 语义，因此
当前 Docs SSOT 结论是 `blocked_by_BR116-R04-P1-01`。未发现 secret、credential、
private key、签名 URL、`.env`、数据库 URL、客户数据或敏感原始记录泄漏。无
CI/CD、容器、Kubernetes、Helm、DB migration、Makefile、依赖 manifest 或生产服务
部署变更；存在 workflow、preset、package 与四平台 distribution 影响。

## 结论

当前存在 1 个正常路径稳定复现、属于 #116 current acceptance 的 P1 finding。
Branch Review Gate 的唯一合法出口是 `implementation_required`。必须修复受支持六种
package layout 的 recorder/checker dispatcher resolution，补直接执行 interface
validator commands 的回归，并重新执行完整 Phase 2、finding-fix commit、原 owner
closure 与另一 fresh final release review。当前不得进入 publication review、push、
PR、Issue close、archive 或 finalize。
