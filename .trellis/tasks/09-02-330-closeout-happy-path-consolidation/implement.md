# Implementation Plan

## Checkpoint A. Baseline And Observability

- [x] 枚举四个 package 当前 recommended/compatibility command graph，标出每次 task/Git/GitHub/Trellis read、recorder/checker/projection、mutation、recovery 和 terminal consumer。
- [x] 在现有 fake adapter/transcript harness 上增加 normalized operation counters 与 wall-clock envelope，先固化 old-path baseline。
- [x] 将会话 #118 慢路径去敏为 fixture：包含 Commit/Publication/Finalizer/Merge 命令序列、非默认 `dev` closure mismatch、terminal 后继续调用和约 19.8 分钟重复 CI polling。
- [x] 为每阶段定义 old/new 同 fixture runner；未由 fresh baseline 复现的重复读取不进入重构。

## Checkpoint B. Compatible Stage Facades

- [x] 在 `guru-create-task-commit` 增加/版本化唯一 Happy Path facade，使一次 prepare 加一次确认后事务完成现有 commit pipeline；保留 prepare/check/create/invoke 兼容入口。
- [x] 在 `guru-review-task-publication` 增加/版本化 facade，使 AI semantic result 的 record/check/projection 在一次 invocation 内复用 current snapshot；保留旧 record/check/invoke。
- [x] 在 `guru-finalize-task` 增加/版本化 facade transaction loop，自动承接无新选择的 mapped reprepare/recovery，并在 plan 实质变化时停止。
- [x] 在 `guru-merge-task-pr` 增加/版本化确认后 facade，执行一次 pre snapshot、expected-head merge、一次 post snapshot 和 terminal projection。
- [x] 为 Merge 增加单一 repo/PR/expected-head-bound CI watcher；禁止双 watcher 与 terminal 后 polling。
- [x] 每个 package 的 `commands.json`、`interface.json`、`SKILL.md`、contract、schema/examples/evals/tests 标记唯一推荐入口和兼容入口。

## Checkpoint C. Behavior Equivalence And Regression

- [x] 同 fixture 对比 old/new typed exit、public DTO、semantic recorder input、deterministic blocker、mutation count/order、recovery receipt 与临时状态生命周期。
- [x] Commit 覆盖 success、hook failure、dirty/staged drift、unrelated preservation、active Git operation、stdout-loss recovery。
- [x] Publication 覆盖 ready、metadata-only revision、content/durable drift、external blocker、ledger disposition mismatch。
- [x] Finalizer 覆盖 ready、provenance tail、same-plan reprepare、publication stale、existing PR adoption、stdout-loss recovery、changed-plan reconfirmation。
- [x] Merge 覆盖 checks pending/success/failure、head/base drift、policy/mergeability blocker、default/non-default/refs-only closure、mutation output loss。
- [x] 断言 terminal exit 后 `terminal.post_exit_operation=0`；command invocation 下降至少 50%，重复完整事实读取下降至少 70%。

## Checkpoint D. Happy Path Activation And Docs SSOT

- [x] 先按 `design.md` Docs SSOT Plan 更新 durable workflow、requirements、design、test 与 package-local contracts。
- [x] behavior-equivalence 通过后，更新 canonical workflow/Skill/platform routing，使 Agent 默认只读取公开合同并调用 facade。
- [x] 保持 semantic judgment 在 Markdown/AI owner；runtime 只编排 checked deterministic actions，不接管 route/readiness/finding。
- [x] 更新 command registry、extension manifest、managed path inventory、production contract/eval assertions 与 README 的用户可见调用方式。
- [x] 若 Architecture Planning owner 要求 contribution，按 change contract 写 task-local contribution，并在独立 Branch Review 后 promotion；否则记录 no-update 理由。

## Checkpoint E. Canonical, Dogfood, Installed And Throwaway

- [x] Canonical package/workflow/preset 变更完成后运行 preset apply 同步 dogfood 与 Shared/Codex/Claude/Cursor 投影。
- [x] 逐个检查并处理 `.new`/`.bak`，运行 dogfood overlay drift、managed ownership、source/installed package parity。
- [x] 验证已有 installed preset 的旧兼容入口继续工作。
- [x] 执行一个代表性 clean installed/throwaway closeout Happy Path，覆盖四阶段 facade 与 terminal stop。
- [x] 将完整 release-wide 多平台 exact-candidate matrix 明确保留给 #267，不将其缺失误报为 #330 失败。

## Expected File Scope

- Canonical packages：`trellis/skills/guru-team/packages/{guru-create-task-commit,guru-review-task-publication,guru-finalize-task,guru-merge-task-pr}/**`。
- Shared runtime/registry only when baseline proves necessary：`trellis/skills/guru-team/runtime/**`、`trellis/skills/guru-team/registry.json`、`trellis/skills/guru-team/interfaces/**`、`trellis/skills/guru-team/evals/**`。
- Workflow/distribution：`trellis/workflows/guru-team/**`、`trellis/presets/guru-team/**`、`trellis/index.json`、managed extension/manifest/config assets。
- Durable SSOT：`.trellis/spec/workflow/**`、`docs/requirements/**`、`docs/design/**`、`docs/test/**`，以及 Architecture owner 明确要求的 task-local contribution。
- Generated dogfood/platform projection：`.trellis/guru-team/**`、`.agents/skills/guru-*/**`、`.codex/skills/guru-*/**` 和 preset 声明的 Claude/Cursor/shared destinations。
- Task artifacts：当前 task 的 `prd.md`、`design.md`、`implement.md`、task/ledger；不创建授权、raw transcript、review report 或 implementation handoff artifact。

## Validation Commands

具体 test module 由 Checkpoint A 的 affected-package baseline 收敛；final gate 固定包括以下命令，并补充 affected integration 与 installed/throwaway commands：

```bash
python3 -m json.tool trellis/index.json
find trellis/skills/guru-team/runtime trellis/skills/guru-team/packages -name '*.py' -type f -print0 | xargs -0 python3 -m py_compile
bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh
python3 -m unittest discover -s trellis/skills/guru-team/packages/guru-create-task-commit -p 'test_*.py'
python3 -m unittest discover -s trellis/skills/guru-team/packages/guru-review-task-publication -p 'test_*.py'
python3 -m unittest discover -s trellis/skills/guru-team/packages/guru-finalize-task -p 'test_*.py'
python3 -m unittest discover -s trellis/skills/guru-team/packages/guru-merge-task-pr -p 'test_*.py'
.trellis/guru-team/scripts/bash/check-skill-packages.sh --json --mode source
.trellis/guru-team/scripts/bash/check-skill-packages.sh --json --mode installed
trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
python3 ./.trellis/scripts/task.py validate .trellis/tasks/09-02-330-closeout-happy-path-consolidation
git diff --check
```

还必须运行 affected finish-family/public-wrapper integration、old/new behavior-equivalence harness、operation-count ceilings、preset initial/reapply、existing installed compatibility 和一个代表性 clean throwaway Happy Path。不得用少量 package unit tests 替代这些门禁。

## Performance Evidence

- 硬证据：normalized operation counters、full snapshot 次数、mutation count、terminal 后调用、old/new behavior equality。
- 观察证据：5-10 次代表性运行的 median，拆分 `agent_orchestration_ms`、`deterministic_command_ms`、`github_api_ms`、`external_ci_wait_ms`。
- 若 wall-clock 目标未达但硬验收通过，记录具体数值、环境、外部瓶颈与 follow-up；若 command/read 收敛未达 AC11，则停止 activation，Issue 保持 Open。

## Implementation Evidence

- 四阶段 operation budget 已由 `closeout-118-sanitized.json` 和 package/integration assertions 固化：recommended command invocation 相对 compatibility route 下降至少 50%，重复完整事实读取下降至少 70%，terminal 后 operation 为 0。
- Publication 实际 Happy Path 发现并修复 `PUB-FINDING-001`：允许读取的 `SKILL.md` / public contract 现已完整定义 semantic-result 字段、枚举、route 约束与可验证 JSON 模板，正常调用不再需要读取 runtime/schema/examples/evals/tests。
- package tests 全部通过：Commit Happy Path 4、Commit contract 4、Publication 41、Finalizer 76、Merge 39；closeout integration 4、finish-family integration 6、preset installer 81。
- source/installed package validator、upstream ownership、dogfood overlay drift、task validation、Python compilation 与 `git diff --check` 均通过；preset reapply 后 sidecar 为 0，七个已核验 known-upgrade `.bak` 已按恢复合同处理。
- 代表性 clean installed Happy Path 位于 `/private/tmp/guru-330-installed-q8ZTnb`：四阶段到达 `ready_for_merge` / `merged`，mutation 顺序严格为 `pr_create`、`pr_ready`、`pr_merge`，第二次 Merge facade 调用从 live merged facts 恢复同一 DTO，未再次 mutation，owner-private checkpoint 已消费，terminal transaction artifact 为 0。
- wall-clock 仅保留观察口径；本轮没有把 5-10 次真实 GitHub/CI 样本 median 伪装成硬验收。已知 #118 的约 19.8 分钟主要来自外部 CI polling，#330 的硬成败按 correctness、行为等价、operation budget、freshness/recovery 与 compatibility 判定。
- 完整 release-wide 多平台 exact-candidate matrix 未在 #330 重复执行，继续由 #267 专门承担；这是明确的验证 ownership 边界，不是 #330 失败。
- Phase 2 Architecture 复核结论：`no_architecture_impact`。完整 live diff 保持现有 Architecture Baseline、设计宪法、semantic owner、跨 Skill boundary、single-writer、GAP lifecycle 与 compatibility exit 不变；新增内容仅为四个既有 package 内的兼容 facade、确定性 orchestration、最小临时状态和验证收敛，因此不创建 Architecture contribution 或 ADR。

## Risk And Rollback Points

- 四个 facade 最主要风险是把 semantic route 选择误移入 runtime；contract/runtime review 必须明确 AI result 是输入，script 不得推导 pass/exit。
- Finalizer internal loop 风险最高；每次继续前都要证明 plan identity、scope、authority 和 side-effect set 未变化。
- Merge snapshot 收敛不得删除 mutation-boundary reread或 post-mutation verification，也不得让 watcher观察错误 head。
- Public schema/profile 变更必须 producer/consumer/registry/installed projection 一致；任何半迁移保持旧路径默认。
- 不修改官方 Trellis、全局 npm 或 `node_modules`；不覆盖用户无关 dirty/untracked 文件。

## Pre-Start Gate

- [x] 三份 planning docs 非空、收敛且无 blocking open question。
- [x] Planning wording review 通过。
- [x] `guru-maintain-architecture-baseline:task_impact_sync(stage=planning)` 返回 current checked result。
- [x] `guru-approve-task-plan` 返回 `approved`。
- [x] 向用户展示最新三份规划、关键选择、取舍与未验证边界，并取得后续独立 `确认继续`。
- [x] 获得该确认后才能运行 `task.py start` 和实施；该确认不授权 commit、push、PR、merge、Issue close 或 cleanup。
