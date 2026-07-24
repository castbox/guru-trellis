# 第三轮独立 Phase 2 最终复核原始报告

## 1. 检查身份与固定范围

- 检查角色：`trellis-check` 阶段二独立检查代理。
- Issue：`castbox/guru-trellis#131`，检查时状态为 `OPEN`。
- Task：`.trellis/tasks/07-23-131-guru-review-branch`。
- Worktree：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/131-guru-review-branch`。
- Branch：`codex/131-guru-review-branch`。
- Intake base：`origin/main` @ `ea132e350c4b6861fc955f17e590651a46e890ab`。
- 检查 HEAD：`ea132e350c4b6861fc955f17e590651a46e890ab`。
- 完整检查范围：该 HEAD 上 56 个 tracked changed files、5561 insertions /
  933 deletions，以及 task/package/platform 的 current untracked implementation
  files。
- Planning approval：本轮开始和最终复核时均由 current checker 确认为
  `typed_exit=approved`；`facts_sha256=bdb2f2e720b2224eb65af1d0cb87dafde15b82753ef296f0291b7798a336257e`，
  `artifact_sha256=b93c510271199865f738493102c90abd058e6c86f4e9a4f5ffe7139090193e66`。
- Docs SSOT strategy：`ssot_first`。
- `check.jsonl` 只有 seed row；按 Phase 2 协议回退到 current task artifacts、
  `implement.jsonl` 的 11 个 curated specs，以及 live issue/comment/official docs。
- 本报告是本轮唯一新增 artifact；未修改实现、规划或
  `.trellis/tasks/07-23-131-guru-review-branch/phase2-check.json`。后者在写报告前的
  SHA-256 为
  `c856b523ac2e28a8ebb08a8d1f69164bdb6ee96a3bab00a1af79213b68802547`。

检查开始前重新执行 workspace boundary validator，结果为：

- expected workspace 与 actual repo root 均为当前 task worktree；
- source checkout `/Users/wumengye/Documents/GoProjects/guru-trellis` 状态为空；
- task worktree identity 有效；
- suspicious source artifacts 为空。

## 2. 本轮重新读取的依据

### 2.1 Current authority 与 planning

- live GitHub Issue #131 正文及 accepted-current comment；
- Trellis 官方 `index.md`、custom workflow、custom spec template marketplace；
- `prd.md`、`design.md`、`implement.md`；
- `implementation-handoff.md`，包括两轮 finding-fix 历史；
- `task.json`、`task-start-context.json`、`issue-scope-ledger.json`、
  `planning-approval.json`、旧 `phase2-check.json`、`agent-assignment.json`；
- 前两份 Phase 2 原始报告。旧报告只作为 finding 历史输入，没有复用其 pass 结论。

### 2.2 Curated specs 与 durable docs

- `.trellis/spec/workflow/workflow-contract.md`
- `.trellis/spec/workflow/skill-package-contract.md`
- `.trellis/spec/workflow/companion-scripts.md`
- `.trellis/spec/workflow/data-contracts.md`
- `.trellis/spec/workflow/quality-guidelines.md`
- `.trellis/spec/preset/installer.md`
- `.trellis/spec/preset/upstream-ownership.md`
- `.trellis/spec/preset/overlay-guidelines.md`
- `.trellis/spec/docs/public-docs.md`
- `.trellis/spec/guides/cross-layer-thinking-guide.md`
- `.trellis/spec/guides/code-reuse-thinking-guide.md`

### 2.3 实现与分发路径

- canonical `guru-review-branch` package、Interface 1.3、13 个 entry
  preconditions、4 个 typed exits、consumer/projection、schema、examples、eval corpus；
- production runtime 中 recorder、checker、public invocation、task-commit freshness、
  owner evidence 与 finding lifecycle 路径；
- shared native eval adapter；
- registry、migration manifests、extension manifests、workflow markers；
- canonical、installed、`.agents`、`.codex`、`.claude`、`.cursor` copies；
- preset installer、ownership inventory、throwaway verifier、tests；
- 11 个 current-contract durable docs。

现有 upstream reviewer 路径最终保持零 diff：

- `.trellis/agents/check.md`
- `trellis/presets/guru-team/overlays/.trellis/agents/check.md`
- `.agents/skills/trellis-check/**`
- `.codex/agents/trellis-check.toml`
- `.claude/agents/trellis-check.md`
- `.cursor/agents/trellis-check.md`

## 3. F-131-01 至 F-131-05 独立闭包表

| Finding | 本轮独立复现 | Current result | 结论 |
| --- | --- | --- | --- |
| `F-131-01` planning freshness | 从本轮 source `workflow-passed` 真实 owner repo 开始，在已通过 gate 后做普通 `prd.md` 修订，再调用真实 public wrapper | return code 0，stderr 空，DTO 精确为 `{"exit_id":"blocked"}` | 已关闭；stale planning 不再投影 `passed` |
| `F-131-02` task-commit / 13-entry closure | 从本轮 source `standalone-passed` 真实 owner repo 开始，移除 exact `task-commit-plans/001.json`，再调用真实 public wrapper；另运行真实 `blocked-stale` corpus | 缺失 commit handoff 时 return code 0、DTO 精确为 `{"exit_id":"blocked"}`；source/installed `blocked-stale` 均实际为 `blocked` | 已关闭；真实 stale/missing entry route 可达 |
| `F-131-03` finding lifecycle binding | 在真实 `finding-fix-passed` repo 中分别把 `owner_round` 改为不存在的 `99`，以及把 `closure_evidence` 改为不存在的 raw report，再调用实际 recorder dry-run | 两组均 return code 2、stdout 空；分别报告 owner round 不存在，以及 closure report 未登记/没有 current bound closure | 已关闭；recorder 在写 gate 前失败关闭 |
| `F-131-04` objective evidence 与 invocation error 分类 | 以真实 passing finding-fix lifecycle 为 baseline，逐项制造 assignment/raw report/final rollup missing、assignment/raw/final digest stale、closure lifecycle missing；另制造 invalid locator/schema/facts/identity/unknown checker | 7 个 objective evidence 场景均 return code 0、stderr 空、DTO 严格只有 `{"exit_id":"blocked"}`；invalid locator/schema/facts/identity/unknown checker 均 return code 2、stdout 空 | 已关闭；没有 catch-all 把 invocation error 降级成 `blocked` |
| `F-131-05` durable graph cardinality | 逐一读取 11 个 current-contract docs，运行 exact-four regression，并直接检查 production migration manifest 与 live registry/workflow closure | 11 docs 均声明 4 authoring edges；旧 3-edge current assertion 扫描 0；manifest 精确 3 Skills/11 exits/4 authoring edges；live closure 10/39/23 | 已关闭；authoring graph 与 production migration membership 未混淆 |

F-131-04 最终手工分类矩阵使用 `cp -a` 保留 evidence mtime。一次使用
`fs.cpSync` 的早期尝试因复制动作改变 mtime，导致 baseline 自身 `blocked`，已明确
作废，没有作为通过证据。有效矩阵的 baseline 实际返回 `passed`。

有效 F-131-04 矩阵结果：

| Case | Return code | stdout / error |
| --- | --- | --- |
| baseline | 0 | `passed` DTO |
| `missing_assignment` | 0 | `{"exit_id":"blocked"}` |
| `missing_raw_report` | 0 | `{"exit_id":"blocked"}` |
| `missing_final_rollup` | 0 | `{"exit_id":"blocked"}` |
| `stale_assignment_digest` | 0 | `{"exit_id":"blocked"}` |
| `stale_raw_report_digest` | 0 | `{"exit_id":"blocked"}` |
| `stale_final_rollup_digest` | 0 | `{"exit_id":"blocked"}` |
| `missing_closure_lifecycle` | 0 | `{"exit_id":"blocked"}` |
| invalid owner locator | 2 | stdout 空；`owner_result_input_mismatch` |
| invalid owner schema | 2 | stdout 空；`owner_result_not_checked` |
| invalid facts digest | 2 | stdout 空；`owner_result_not_checked` |
| invalid invocation identity | 2 | stdout 空；`owner_result_not_checked` |
| unknown checker | 2 | stdout 空；installed inventory/runtime dependency 层失败关闭 |

## 4. Current-diff semantic review

| Adequacy dimension | 结论 | 本轮证据 |
| --- | --- | --- |
| scope / authority | 通过 | current issue/comment、planning、ledger 与 #131 边界一致；#116/#132 未被静默扩入 |
| implementation behavior | 通过 | 真实 recorder/checker/public wrapper 路径与 F-131-01..04 手工矩阵一致 |
| interface / schema / routing | 通过 | 13 preconditions、4 exits、unique consumers、minimal DTO、invalid invocation 边界均被真实执行验证 |
| finding lifecycle | 通过 | owner round、raw report、closure digest、same-agent/replacement、fresh-final 链均有 runtime 校验和负例 |
| test adequacy | 通过 | package/runtime/installer/ownership/full eval/throwaway 均完整重跑；没有只复用旧测试结果 |
| distribution / parity | 通过 | canonical、installed 和四个平台 package 38 files byte-identical，wrapper executable modes 一致 |
| compatibility / upgrade | 通过 | clean init、existing preview/switch、`trellis update --force`、workflow/preset reapply、no-developer、pre-#146 fixtures 均通过 |
| Docs SSOT | 通过 | `ssot_first` current durable docs、task delta、runtime、manifest、tests 对 4 authoring edges 与 3 Skills/11 exits 一致 |
| deployment / security | 通过 | 无 `.github` workflow、container、K8s、DB migration、Makefile 或业务 service 改动；新增行 credential scan 无命中 |
| evidence / pollution | 通过 | planning current、index 空、source checkout clean、sidecar/cache 0、forbidden reviewer diff 0 |

### P0-P3 findings

本轮没有发现新的 P0、P1、P2 或 P3 finding。

检查只纳入 honest-but-fallible 的正常受支持路径。需要故意伪造 artifact、攻击
digest、TOCTOU、并发压力或恶意绕过才能成立的案例没有进入 current acceptance，也
没有被列为 finding。

## 5. Docs SSOT reconciliation

- Plan strategy：`ssot_first`。
- Durable-doc primary input、task planning delta、runtime、schema、tests 与分发副本
  当前一致。
- 以下 11 个 current-contract 文档均已由专项 regression 与逐文件扫描确认使用
  exactly four authoring edges：
  - `README.md`
  - `trellis/workflows/guru-team/README.md`
  - `trellis/presets/guru-team/README.md`
  - `docs/requirements/README.md`
  - `docs/requirements/requirement-main.md`
  - `docs/requirements/guru-team-trellis-flow.md`
  - `.trellis/spec/workflow/skill-package-contract.md`
  - `.trellis/spec/workflow/companion-scripts.md`
  - `.trellis/spec/workflow/quality-guidelines.md`
  - `.trellis/spec/preset/installer.md`
  - `.trellis/spec/preset/upstream-ownership.md`
- Production migration 独立保持 exactly 3 Skills / 11 exits；live active closure 为
  10 Skills / 39 exits / 23 targets；planned package 只有
  `guru-review-task-publication`。
- Task delta 已合并。旧 Phase 2 reports、复现临时目录、throwaway 输出、sidecar 清理
  历史与本报告只属于 task history，不进入公共 package。
- `implementation-handoff.md` 诚实保留旧 findings 和两轮修复历史；第 11 节是 current
  handoff。其历史重复句不改变 durable contract，也不构成 current behavior defect。

## 6. 验证结果

| 验证项 | 结果 |
| --- | --- |
| `guru-review-branch/tests/test_contract.py` | 8/8 passed |
| source shared real-wrapper eval | 7/7 passed |
| installed shared real-wrapper eval | 7/7 passed |
| `test_skill_packages.py` | 167/167 passed |
| `test_guru_team_trellis.py` | 560/560 passed，13 skipped |
| preset installer tests | 45/45 passed |
| upstream ownership tests | 6/6 passed |
| 11-doc exact-four regression | 1/1 passed |
| source package validator | passed，10/39/23，legacy 0 |
| installed package validator | passed，10/39/23，1903 managed files，sidecar/removal/conflict 0 |
| dogfood overlay drift | passed |
| upstream ownership validator | passed，43 active entries、48 managed assets、10 active/1 planned Skills |
| full throwaway install/update/reapply | passed，exit 0 |
| task context validation | passed，implement 11 / check 0 |
| JSON parse | 2630 files passed |
| Bash syntax | 295 files passed |
| Python compile | 116 files passed，使用临时 `PYTHONPYCACHEPREFIX` |
| `git diff --check` | passed |
| canonical/installed/platform parity | passed |
| wrapper executable modes | passed |
| credential / sensitive absolute path scan | passed；无 secret 命中，无本机路径泄露 |
| sidecar/cache scan | passed；`.new`/`.bak`/`.orig`/`__pycache__`/`.pyc` 均为 0 |
| forbidden reviewer diff | passed，0 |
| index | empty |
| source checkout | clean |

Lint：

- `git diff --check`、JSON parse、Bash `-n`、Python compile、package validators 与
  complete regression 均通过。
- 当前环境未安装 `ruff`、`shellcheck`，仓库也没有声明统一 lint 命令；未把工具缺失
  伪装为已执行。

TypeCheck：

- 仓库未配置 current executable type-check gate，当前环境也没有 `mypy` 或
  `pyright`；本项不适用。
- Python compile 与 560 个 runtime tests 均通过，但没有把它们描述为静态类型检查。

## 7. Throwaway / update / reapply 结论

默认运行 `verify-throwaway-install.sh` 返回 code 2，精确说明：

- default workflow source 是 public `main`；
- current branch 为 `codex/131-guru-review-branch`；
- current workflow 仍是 unpublished dirty content；
- 不允许把 public marketplace sample 冒充 current feature-ref 验证。

随后按明确验证模式设置 `TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1`，完整 verifier
exit 0，覆盖：

- public marketplace discovery；
- local unpublished current workflow sample；
- clean project init；
- Codex/Claude/Cursor selected-platform preset；
- public wrappers 与 eval smoke；
- existing-project preview/switch；
- `trellis update --force`；
- workflow 与 preset reapply；
- no-developer identity fixture；
- pre-#146 upgrade fixture；
- initial/after-update closeout 与 task-workspace；
- source/installed 10/39/23 closure、1903 inventory、overlay ownership、0 sidecar。

最终输出为：

`Verified public marketplace discovery plus local unpublished workflow sample`

## 8. 精确未验证项与非阻塞限制

1. `refs/heads/codex/131-guru-review-branch` 当前未推送，`git ls-remote --heads`
   返回空。因此没有执行 exact remote feature-ref marketplace install。这是明确的
   publication 前限制，不是本地实现 finding；默认 throwaway 已证明不会把 public
   `main` 冒充该 ref。
2. npm 最新 Trellis CLI 为 `0.6.8`，但 approved/current tested baseline 是 `0.6.5`；
   本 task 没有授权把新版兼容扩入 scope。
3. 本轮没有 commit、push、PR、部署或 issue close；这些副作用属于后续 main-session
   gate。
4. `phase2-check.json` 仍诚实保留上一轮 `implementation_required`。本报告只为主会话
   提供重新记录 current Phase 2 结论的 semantic evidence，不自行越权修改 gate
   artifact。

## 9. 已修复问题

- 本轮 reviewer 没有修改实现文件。
- F-131-01 至 F-131-05 均由当前实现闭环，并由本轮独立证据验证；不再列为开放问题。
- 检查过程中清理了 task worktree 内唯一一个忽略的启动缓存目录
  `.trellis/scripts/common/__pycache__`；没有删除 tracked 或用户业务数据。

## 10. 未修复问题

- 无 current-scope P0-P3 问题。
- 第 8 节仅列精确未验证项和后续 gate，不是 implementation finding。

## 11. 证据交接与结论

- 阶段二覆盖：current live authority、planning、11 个 curated specs、完整 current
  uncommitted diff、runtime/schema/config、canonical/installed/platform package、
  installer、tests、durable docs、task artifacts、F-131-01..05 手工负例与 full
  throwaway。
- Docs SSOT：`ssot_first` 已成立；4 authoring edges、3 Skills/11 migration exits、
  10/39/23 live closure在 durable docs、manifest、runtime、tests 与分发副本之间一致。
- 部署/安全：无部署资产或运行时服务变更；无 secret、本机路径、sidecar、cache 或
  source-checkout pollution。
- 开放风险：只有未推送 feature ref 的 exact remote marketplace 验证限制，以及明确
  out-of-scope 的 CLI 0.6.8。
- 本报告可支撑主会话重新记录 current `phase2-check.json`。
- 建议 `guru-check-task` typed exit：`passed`。

最终结论：完整复核未发现问题；相关 lint-equivalent checks、runtime/package/installer
tests、source/installed eval、type applicability review、Docs SSOT reconciliation 与
throwaway/update/reapply 均已获得 current evidence。建议进入 main-session 的 Phase 2
artifact recorder/validator，再进入 task work commit；不得跳过后续 semantic gates。
