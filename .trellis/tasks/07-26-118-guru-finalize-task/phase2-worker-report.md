# Issue #118 Fresh Phase 2 检查报告

## 检查完成

### 检查身份与边界

- 角色：独立 `trellis-check` 阶段二检查代理
  `/root/issue118_phase2_check`；未参与实现。
- Task：`.trellis/tasks/07-26-118-guru-finalize-task`。
- Worktree：
  `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/118-guru-finalize-task`。
- Branch：`feat/118-guru-finalize-task`；base 为 `main`。
- 检查 HEAD 与 `origin/main`：
  `7820a9eeec2a2a75fb52fba156a7211d9f9fb09c`。
- 检查范围：完整当前 working-tree implementation、task planning/ledger/agent
  recovery、canonical/installed/platform package、runtime、preset、durable docs、
  tests 与 clean throwaway 安装链路。
- 本代理没有修改产品代码、schema、test、durable docs、planning artifact、
  `agent-assignment.json` 或 `phase2-check.json`；唯一 tracked/untracked 写入为本报告。
  本轮测试生成的 ignored `__pycache__` 已精确清理。
- 未执行 commit、push、PR、Issue mutation、finish-work 或 publication。

Fresh entry gate：

- workspace boundary 通过；expected workspace 与 actual repo root 均为当前 #118
  worktree，source checkout clean，suspicious source artifacts 为空；
- planning approval 通过，`typed_exit=approved`，artifact SHA-256 为
  `1bcc7712aa1c8a74f72ecfa4a90d8384d77fbd7a6ed95f65714737ffa600c9c6`，
  facts SHA-256 为
  `9d0d14bada5d4990a3f62402bdb5b28275fd1c7bf20476cdd01f1145defbeb70`；
- `check.jsonl` 只有 seed row，因此按 fallback 完整读取 `prd.md`、`design.md`、
  `implement.md`，并展开 workflow、preset、Docs SSOT、Skill package 与
  `trellis-meta` 适用合同；
- agent assignment checker 通过；两次 implementation stale cutover 均有合法
  predecessor/replacement 事件，最终 implementer 已 completed，本 check agent 身份独立。

### 已检查文件

- Task scope：`prd.md`、`design.md`、`implement.md`、`planning-approval.json`、
  `issue-scope-ledger.json`、`agent-assignment.json` 与 implementation handoff events。
- Canonical finalizer package：
  `trellis/skills/guru-team/packages/guru-finalize-task/**`，包括 Skill/contract、
  Interface 1.3、六类 input、六个 `exit_id` output、consumer/projection、private
  schema、examples、wrappers、八 case eval corpus 与 package tests。
- Runtime：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`、四个
  finalization bash wrappers、canonical closeout schema 与 602-test runtime suite。
- Producer/consumer graph：#116/#117 Interface、canonical/installed registry、
  extension inventories、consumer schemas 与 target-owned authoring examples。
- Distribution：canonical、`.trellis/guru-team`、`.agents`、Codex、Claude、Cursor
  copies；preset installer、ownership validator、dogfood overlay drift 与 throwaway
  verifier。
- Durable docs：repository/workflow/preset README，`.trellis/spec/workflow/**`、
  `.trellis/spec/preset/**` 与 `.trellis/spec/docs/public-docs.md`。
- Explicit no-write paths：canonical/dogfood global workflow、upstream
  `trellis-finish-work` Skill/Command/Prompt、preset overlays 与 official `task.py`。

### Scope-first finding qualification

| 候选 | Requirement / planning trigger | 正常路径复现 | Disposition / severity |
| --- | --- | --- | --- |
| `C-DOC-01` durable Docs SSOT 仍把 finalizer 写成 planned/unavailable | `prd.md` R14/R15、`design.md` Docs SSOT Plan 的 `ssot_first` 与“durable docs 不得互相冲突”、implementer terminal handoff 的 docs reconciliation claim | 正常阅读 current durable specs，会同时得到 finalizer 未实现、五条 authoring edge、live 12/46；而 current registry/discovery/README 为 active 13/52、十二条 edge，global markers 才是 deferred 12/46/27 | `current_scope` / `P2`，finding `F-DOC-01` |
| `C-SCHEMA-02` 同一 closeout-plan schema id 存在两个不同合同 | `prd.md` R2/R9/R14、AC2/AC11 与 `design.md` owner-private schema/distribution contract | `discover-skill-contract` 正常返回 package private schema；将真实 closeout plan 的 `inputs` 置空并重算 digest 后，package Draft 2020-12 schema接受，runtime canonical schema以 `minProperties` 拒绝 | `current_scope` / `P2`，finding `F-SCHEMA-02` |

没有 scope-change proposal、malicious/forgery/TOCTOU/locking/fault-injection
proposal，也没有第三个 current-scope candidate。

### 已修复问题

本代理按 handoff 不得修改产品实现，因此没有执行 tracked self-fix。只删除了本轮测试
生成且实施 handoff 前不存在的 ignored `__pycache__`，未改变 Git diff。

### 未修复问题

#### F-DOC-01（P2，open）：`ssot_first` durable docs reconciliation 未完成

Current stale locators 包括：

- `.trellis/spec/preset/upstream-ownership.md:276` 仍写 five target-owned examples；
- `.trellis/spec/preset/upstream-ownership.md:299` 仍写 finalizer only planned；
- `.trellis/spec/preset/installer.md:538`、`:543`、`:550`、`:562`、`:577`、
  `:579`、`:593` 仍写 planned/unimplemented、12/46 或拒绝 #118 producer edge；
- `.trellis/spec/docs/public-docs.md:344`、`:356`、`:372`、`:383`、`:394`、
  `:405`、`:417`、`:425`、`:438`、`:445` 仍把 current README/package state 写为
  planned、five-edge 或 12/46；
- `.trellis/spec/workflow/quality-guidelines.md:105`、`:639` 仍要求 combined live
  closure 12/46，且全文没有 finalizer quality owner section；
- `.trellis/spec/workflow/index.md:132` 的 current publication owner 导航仍写
  12/46 closure。

这些不是历史注释的无害残留：文件以 durable/current 安装、public docs 与 quality
SSOT 口径指示当前行为，正常维护者会据此拒绝已经 active 的 package/public edges。
需要在实现阶段统一更新 current package 13/52、十二条 authoring handoff 与 deferred
global 12/46/27 的分层语义，并补 durable-doc regression assertions。#119 的 global
invocation/order、#132 overlay cleanup 仍必须保持未实现。

#### F-SCHEMA-02（P2，open）：package private closeout schema 弱化同一 `$id`

- Runtime owner：
  `trellis/workflows/guru-team/schemas/closeout-plan.schema.json:35` 要求
  `inputs.minProperties=6`，每项为 closed `{path,sha256}`。
- Package/private discovery owner：
  `trellis/skills/guru-team/packages/guru-finalize-task/schemas/closeout-plan.schema.json:35`
  仅要求 `inputs.type=object`。
- 两者 `$id` 都是
  `https://github.com/castbox/guru-trellis/trellis/workflows/guru-team/schemas/closeout-plan.schema.json`，
  但 SHA-256 分别为
  `78ea2893f61eaa81333948342b7bb206f9c0bf91b8b7d37b366b9d7e3b9efc35`
  与
  `fcf997d15bd0d6ce76901f22b327dd1c6b64b5311f8e00176454ec60b5d2cc97`。
- 正常 cross-validator probe 对同一重算 digest 的 `inputs={}` plan 给出
  `runtime REJECT`、`package ACCEPT`。Source/installed package validator 当前均通过，
  说明现有 test 没有覆盖这个 identity/semantic divergence。

Runtime `validate_closeout_plan()` 仍会 fail closed，因此本轮没有证明错误 transaction
已执行；缺陷在于 package discovery 对 owner-private checkpoint 发布了错误 schema truth。
实现应统一同一 schema identity 的约束，并增加 source/installed/private-schema
regression，至少证明空/畸形 `inputs` 在 package 与 runtime 两侧一致拒绝。

## 验证结果

### Semantic adequacy

| 维度 | 结论 | Evidence |
| --- | --- | --- |
| requirements | 通过 | #118 close scope、#115/#119/#132/#105 边界与 unusual exclusions 保持正确 |
| design | 通过 | semantic owner / deterministic engine、六 profiles/exits 与 recovery design 已承接 |
| implementation | 失败 | `F-SCHEMA-02` 使 private schema identity 与 runtime truth 不一致 |
| tests | 失败 | 全套测试通过，但未发现两个 current-scope regression，需补 targeted assertions |
| docs_ssot | 失败 | `F-DOC-01` 违反 approved `ssot_first` reconciliation |
| cross_layer | 失败 | package discovery schema 与 runtime schema 对同一 id 给出不同结果 |
| compatibility | 通过 | #105 transaction/recovery regression 全量通过，legacy finish observable semantics 保留 |
| deployment_and_operations | 通过 | 无 dependency、CI/CD、container、Compose、K8s/Helm/Kustomize、DB migration、Makefile、deploy 或 data-write 变化 |
| agent_recovery | 通过 | implementation replacement chain 与独立 check assignment 均由 checker 验证 |
| verification_completeness | 失败 | 本轮检查完整，但两个 open current-scope findings 阻止 Phase 2 pass |

### Commands and tests

- Lint：通过。
  - `bash -n` 覆盖 canonical/preset/installed/finalizer wrappers；
  - `py_compile` 使用 repo 外 cache prefix，三处生产 Python 入口通过；
  - `git diff --check` 通过；task validation 通过。
- TypeCheck：不适用。仓库没有独立 configured type checker；由 compile、schema
  validators 与 unittest 覆盖。
- Tests：命令层全部通过，但语义结论因 findings 为失败。
  - Runtime full suite：602 tests，13 skipped，exit 0；
  - Skill package full suite：176 tests，exit 0；
  - Preset full suite：45 tests，exit 0；
  - Finalizer package：3 tests，exit 0；
  - Installed finalizer shared real-wrapper eval：8/8 passed，覆盖六个 actual exits；
  - source/installed validators：passed，13 active、0 planned/legacy，global markers
    按 #119 boundary 保持 12/46/27；
  - source/installed contract/eval discovery：六 profiles、六 exits、八 cases；
  - canonical/installed/shared/Codex/Claude/Cursor finalizer package：逐文件
    byte-identical；
  - ownership：43 frozen / 43 active / 0 removed；dogfood overlay drift passed；
  - no-write assertion：global workflow、upstream Finish assets、overlay、official
    `task.py` 均零 diff；
  - repository sidecar/cache final scan：无 `.new`、`.bak`、`.pyc`。

### Platform and installation evidence

- Shared：fresh installed real public wrapper 8/8 passed；actual exit 先选择 per-exit
  schema，随后才断言 `expected_exit`，native request 不含 `expected_exit`。
- Codex：implementation evidence 中 trusted worktree Git root 的 real adapter
  `verification_required` passed；full package tests覆盖 trusted-root argv/protocol。
- Claude：stdin/file/single-JSON protocol tests passed；本机 real CLI 因 external
  `401 Invalid API key` 诚实记录为 `execution_error`，不得声称 native passed。
- Cursor：authentication unavailable 路径稳定返回 `unsupported`；未伪造 pass。
- Independent clean throwaway：
  `TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1` 执行
  `verify-throwaway-install.sh /tmp/guru-118-phase2-throwaway.D7u9B1`，terminal
  exit 0，结果为
  `Verified public marketplace discovery plus local unpublished workflow sample`。
  覆盖 clean init、marketplace discovery、preview/switch、preset install/reapply、
  `trellis update`、managed `.new/.bak` recovery、平台分发、source/installed
  validators、production eval、closeout/workspace probes与最终零 sidecar/cache。
- Exact pushed feature-ref remote verification 仍是 publication-time limitation：当前
  branch 未 commit/push，本地 unpublished sample 不冒充 remote-ref pass。

## 证据交接

- 阶段二：本报告覆盖完整 current dirty scope、planning/provenance、implementation
  handoff、agent recovery、code/schema/test/docs/distribution/install 与全部适用命令。
  它足以支持主会话生成 `implementation_required` 的 `phase2-check.json` 输入，但不能
  支撑 `passed`。
- Docs SSOT：approved strategy 为 `ssot_first`；README、package contract 与核心
  workflow specs 已更新，但五个 durable spec surface 仍与 active 13/52 graph 冲突，
  所以 reconciliation 失败。
- Findings：`F-DOC-01` 与 `F-SCHEMA-02` 均为 open current-scope P2；修复后必须由
  独立 check agent 对完整 task scope、全部 tests、Docs SSOT 与 clean throwaway 重新
  执行一轮 full Phase 2，不能只做 focused rerun。
- Scope：Issue ledger 只关闭 #118；#115 related，#119/#132 follow-up；#105 不发生
  Issue mutation。CI/CD、安全、部署与数据面无新增影响。
- Branch Review：尚未进入；当前无 task commit、无 committed branch diff、无
  `review.md`/review gate。本报告不能替代后续 Branch Review。

## 结论

`implementation_required`。

两项 open P2 finding 均可在受支持的正常路径复现，不依赖恶意篡改或超范围机制。
在 durable Docs SSOT 与 closeout private schema identity 修复并完成新一轮完整 Phase 2
之前，不得调用 task commit、Branch Review、publication review 或 finalization。
