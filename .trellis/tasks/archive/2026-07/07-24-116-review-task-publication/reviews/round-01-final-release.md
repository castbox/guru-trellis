# #116 Branch Review 第 1 轮最终放行审查原始报告

## 审查身份与结论

- 审查角色：独立 `最终放行审查代理`
- 审查代理：`/root/issue116_branch_review_round1`
- 审查轮次：`round-01`
- 结论：`blocked`
- 问题数量：`1`（P0=`0`，P1=`0`，P2=`1`，P3=`0`）
- 门禁判断：当前报告不能作为 Branch Review Gate 的 final pass evidence；P2-1 必须返回 Phase 2 修复、重新执行完整 check 与 task commit，并由新的完整 Branch Review 复验。

## 审查绑定

- GitHub issue：`castbox/guru-trellis#116`，live 状态为 `OPEN`
- 工作树：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/116-review-task-publication`
- 目标分支：`codex/116-review-task-publication`
- 基线：`origin/main`
- 基线 HEAD：`bdc8f50bcd1e325aed331d4b01107b83ed8ee940`
- 审查范围：`origin/main...aacb6e02e5386578bfe3d046511a0002a51cb581`
- 审查 HEAD：`aacb6e02e5386578bfe3d046511a0002a51cb581`
- 变更规模：330 files，37147 insertions，596 deletions
- 提交：`feat(workflow): #116 实现 task publication 审查闭环`；提交正文记录背景、变更、边界、验证并使用 `Refs #116`，没有提前关闭 issue。
- 远端状态：`git ls-remote --heads origin refs/heads/codex/116-review-task-publication` 无返回；精确 candidate branch 尚未 push，符合当前授权边界，不计实现 finding。
- 工作区边界：`pwd`、Git toplevel、task current source 与 boundary validator 均绑定上述 task worktree；source checkout 干净且 `suspicious_source_artifacts=[]`。审查开始时仅主会话维护的 `agent-assignment.json` 与已执行 commit plan `task-commit-plans/001.json` 存在 metadata tail，本代理未修改这些文件。

## 已检查文件

- Live issue #116、根 `AGENTS.md`、官方 Trellis `index.md`、`custom-workflow.md`、`custom-spec-template-marketplace.md`
- Task `prd.md`、`design.md`、`implement.md`、`check.jsonl`、`planning-approval.json`、`phase2-check.json`、`implementation-handoff.md`、五轮 Phase 2 raw report、`issue-scope-ledger.json`、commit plan
- 八份 curated specs，重点包括 workflow、Skill package、data、companion scripts、preset installer/ownership 与 public docs 合同
- 完整 `origin/main...HEAD` 330-file committed diff，包括 canonical package、private/public schemas、shared runtime、wrapper/evals/tests、workflow、registry/extension、preset/overlays、Codex/Claude/Cursor copies、durable docs 与 task evidence
- Canonical 与 dogfood workflow、canonical 与 selected-platform Skill package、source/installed graph、active/planned skill routes以及 Phase 3.6/3.7 边界

## 已修复问题

无。Branch Review 模式禁止修改实现、规划或 gate artifact；本代理只写本原始审查报告。

## 未修复问题

### P2-1：Publication checker 把任意 task-local working-tree 文件当作允许的 metadata tail

- Finding ref：`BR116-R01-P2-01`
- 场景分类：`normal_required_behavior`
- Qualification：`qualified_current_finding`
- 位置：
  - `trellis/skills/guru-team/packages/guru-review-task-publication/interface.json:30`
  - `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:14085-14115`
  - `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:14943-14956`
- 合同：
  - PRD R3 明确要求 Branch Review 后出现非 allowlisted metadata drift 时失败关闭，R4 的 `metadata_tail_integrity` 要求仅有 allowlisted task metadata tail；
  - design 明确要求 `非 allowlisted tail` 停在 entry gate，且 metadata revision 由 contract closed allowlist 管理；
  - approved implement Step 4 明确要求 allowlist 只接受 contract 指定 publication metadata paths，并要求 `non-allowlisted tail` 负例；
  - public Interface 将 `review_range_and_working_tree` 绑定定义为 `reviewed HEAD plus contract allowlist only`，checker 的 objective scope 也明确包含 metadata tail。
- 事实：`task_publication_repository_binding()` 会把除 `pr-readiness.json` 外的全部 Git status path 写入 repository binding；但 `task_publication_check_errors()` 只把“不在当前 task prefix 且不在 `.trellis/.runtime/`”的路径视为非 metadata drift。它没有建立或检查 publication contract closed allowlist，因此任意 task-local 文件都会被整段 task prefix 豁免。
- 正常路径独立复现：在隔离临时 Git repo 建立已提交 baseline 与 `origin/main`，随后模拟一次普通误操作，新增未跟踪 `.trellis/tasks/fixture/debug-note.md`。调用当前 `task_publication_repository_binding()` 后得到：

  ```json
  {
    "status_paths": [".trellis/tasks/fixture/debug-note.md"],
    "task_prefix": ".trellis/tasks/fixture/",
    "checker_non_metadata_status": [],
    "unexpected_task_local_file_is_rejected": false
  }
  ```

  该场景不需要手工篡改既有 artifact/hash/state，不涉及恶意输入、并发、TOCTOU 或 fault injection。Recorder 与 checker 都重建相同 repository binding，因此 freshness equality 本身也不会拒绝该文件；若 AI payload 的十维结论为 passed，deterministic entry gate 仍可把 `ready` 记录为通过。
- 影响：一个正常遗漏的 task-local 临时说明、导出物或其它未注册文件可以在 Branch Review 后进入 readiness binding，却不触发 contract 要求的 fail-closed allowlist。AI 仍负责 `metadata_tail_integrity` 语义判断，但 deterministic checker 没有兑现其独立的 objective allowlist 合同，honest-but-fallible reviewer 一旦漏看该路径，`ready` 可在非白名单 tail 下被固化。
- 修复要求：
  1. 为 publication entry 定义并复用精确的 contract-owned task metadata/runtime-input allowlist，不得以整个 task directory prefix 代替；
  2. recorder/checker 在 `ready` 路径对每个 `status_paths` 成员做精确 allowlist 校验，非白名单 task-local path 必须形成可复验的 failed entry condition；
  3. 补充 source、installed/runtime 负例：普通新增任意 task-local 文件时 recorder/checker 不得产生或接受 `ready`；同时保留已批准的 assignment/report/commit-plan/body/index/ledger/finalization-specific metadata 正路径；
  4. 修复后同步 canonical、dogfood 与 selected-platform copies，并重新跑 Phase 2 与完整 Branch Review。
- 状态：`unresolved`。

## 候选问题资格审查

| 候选 | 场景分类 | 资格结论 | 证据与处置 |
| --- | --- | --- | --- |
| 任意 task-local 文件被 prefix 级豁免 | `normal_required_behavior` | `qualified_current_finding` | 隔离正常路径稳定复现，记为 `BR116-R01-P2-01` |
| Phase 2 首次 clean throwaway 的一次空响应 | `normal_required_behavior` | `rejected_candidate` | 同一 fixture 随后 7/7 eval 通过，Phase 2 第二次 clean run exit 0；本轮 fresh throwaway 终态见验证结果。没有正常路径 current-scope 复现，不计 finding |
| 远端精确 candidate marketplace 未验证 | `explicit_nonstandard_requirement` | `accepted_limitation` | 分支尚未获 push/finalization 授权，Docs SSOT 与 Phase 2 均明确留给后续 finish-work；不计实现 finding |
| 通过并发/TOCTOU 压力重造 transient empty response | `out_of_scope` | `rejected_candidate` | `AGENTS.md` 明确排除当前需求未要求的并发竞态/TOCTOU/fault injection，不进入 P0-P3 |

## 验证结果

- Lint：通过。`git diff --check origin/main...HEAD` 与当前 worktree diff check 通过；相关 Bash `bash -n`、JSON 解析、Python `py_compile` 通过。
- TypeCheck：不适用。本仓库本变更无独立静态类型检查器；以 Python compile、closed JSON Schema 和 source/installed contract validator 覆盖机器合同。
- Runtime tests：`python3 trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`，570/570 通过，13 skipped。
- Skill package tests：`python3 trellis/skills/guru-team/tests/test_skill_packages.py`，174/174 通过。
- Preset tests：45/45 通过；upstream ownership tests 9/9 通过。
- Publication contract：canonical 16/16、installed 16/16 通过。
- Branch Review contract：canonical 8/8、installed 8/8 通过。
- Wrapper eval：canonical 7/7、installed 7/7 通过，覆盖 initial ready、standalone、return、blocked、stale re-entry 与 metadata revision cases。
- Source/installed graph：11 active Skills、42 exits、25 workflow targets；installed 2100 managed files，0 sidecars、0 removals、0 conflicts。
- Overlay/ownership：dogfood drift 通过；frozen/active/overlay 均为 43，removed=0，五个 reviewed current payload 与 ownership contract 一致。
- Fresh throwaway install/update/reapply：`TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1 ./trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh` exit 0；覆盖 clean init、preset apply、initial/after-update smoke、Trellis update + workflow/preset reapply、无 developer fixture、source/installed validation、ownership/drift、public marketplace discovery 与 local unpublished workflow sample。本轮未出现空响应。
- Platform一致性：canonical/dogfood workflow byte-identical；canonical/installed/Codex/Claude/Cursor publication package 由 source/installed validator、preset transaction 与 throwaway checks 验证。测试产生的 ignored `__pycache__` 不进入 committed diff。
- `.new` / `.bak` / `.orig`：当前 reviewed worktree 递归检查无未处理 sidecar。
- 影响面扫描：完整 diff 无 `.github/`、Docker/K8s/Helm、dependency manifest、DB migration 或 Makefile 变更。

## 证据交接

### 阶段二

- Phase 2 artifact 为 schema 2.0、`guru-check-task:passed -> guru-create-task-commit`，记录五轮独立 checker、F-001 至 F-006 已关闭、十项 adequacy passed 与完整 rerun。
- 本轮独立测试复核了 Phase 2 的主要正路径结论，但额外发现 `BR116-R01-P2-01`。因此既有 `phase2-check.json` 不足以支撑当前 HEAD 的最终放行；修复后必须 fresh Phase 2 check、task commit 与 Branch Review。

### Docs SSOT

- 批准策略：`ssot_first`。
- Phase 2 记录的 16 个 durable paths 当前 SHA-256 全部与 handoff binding 一致；`implementation-handoff.md` 与五轮 raw Phase 2 report 的 digest 也全部匹配。
- Durable docs、workflow、README、registry/package/runtime/tests 对 active `guru-review-task-publication`、11/42 closure、三个 typed exits、planned `guru-finalize-task` stop、远端验证限制整体一致。
- `task_delta_merged=true`；task-history-only 列表、follow-up/current PR limitation 均有明确记录。
- 但 durable contract 同样要求 exact allowlist，当前 runtime 没有兑现；P2-1 修复必须同步对应 durable wording或确认现有 wording无需变化，并重新建立 Docs SSOT evidence。

### Branch Review

- Diff 范围：`origin/main...aacb6e02e5386578bfe3d046511a0002a51cb581`，完整 330-file committed diff，不限于最新编辑。
- 当前 finding：1 个 unresolved P2；无 P0/P1/P3。
- 本报告不能供 Branch Review Gate 记录 pass；只能作为 round-01 blocked/raw finding evidence。
- 本轮没有运行 `review-branch.sh`、`check-review-gate.sh`、任何 Branch Review recorder/validator，也没有修改 implementation/task plan/Phase 2/gate artifacts。

## 安全与部署影响

- 未发现 token、secret、private key、`.env`、数据库 URL、签名 URL、客户数据或敏感原始记录泄漏。
- 变更影响 Guru Team workflow、public Skill package、recorder/checker、schema、preset installer、platform copies、README/spec 与安装/升级行为；extension candidate version 为 `0.6.5-guru.22`，公开 stable source 仍为 `v0.6.5-guru.2`，未提前宣称 candidate 已发布。
- 无 CI/CD、容器、K8s/Helm、DB migration、Makefile、依赖 manifest 或生产服务部署变更。主要回滚面是 marketplace/preset/package 版本与 overlay reapply。
- P2-1 是正常 correctness/fail-closed 缺口，不是 hostile-input security finding。

## Issue Close Scope

- `issue-scope-ledger.json`：primary/close 为 #116；related 为 #115/#131/#144/#146；follow-up 为 #81/#117/#118/#119/#132。
- 当前 commit 仅 `Refs #116`，没有误关闭 related/follow-up。
- 在 P2-1 关闭、fresh review pass、finalization/remote exact ref 验证完成前，不得 close #116。

## 观察项与后续候选

- `publication_review` schema 允许 `review_intent=stale_reentry_review`，而 runtime 只强制 stale profile 使用 stale intent，未反向禁止 initial profile 选择 stale intent。当前 requirement 没有明确要求反向互斥，也未证明正常路径行为失效，不计 finding；若后续要求 profile/intention 双向闭合，可独立澄清。
- `guru-finalize-task` 按 #118 仍是 planned missing-Skill boundary；这是当前明确交付边界，不计 finding。

## 结论

完整 committed diff 存在 1 个可在受支持正常路径独立复现的 current-scope P2 finding：publication checker 没有按 contract closed allowlist 拒绝意外 task-local metadata tail。当前 round 1 不放行，禁止进入 Branch Review Gate pass、finish-work、push、PR 或 issue close；应返回 Phase 2 修复并重新执行完整审查链。
