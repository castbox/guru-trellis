# Issue #131 Branch Review Round 6 问题闭环原始报告

## 审查身份与固定范围

- 逻辑角色：`问题闭环审查代理`，round 6。
- Technical agent：`/root/issue_131_branch_review_final`。
- Continuity：本 technical agent 在 round 4 fresh final review 中独立发现
  `F-131-BR4-01`，并在 round 5 以合法 finding owner 身份保留同一 finding；
  assignment 已记录 round 5 → round 6、`decision=reuse-for-closure`。
- 角色边界：本 agent 未参与 `F-131-BR4-01` 的实现，也未参与 Phase 2 对
  `F-131-P2-R5-01` 的机械修复；本轮只能执行 closure，不能再次担任最终放行审查
  代理。
- Task：`.trellis/tasks/07-23-131-guru-review-branch`。
- Base：`origin/main`。
- Base HEAD / merge base：
  `ea132e350c4b6861fc955f17e590651a46e890ab`。
- Reviewed HEAD：
  `f4e2a62b8264dceb5078fd3ceb2caa3e46c97a53`。
- 完整范围：
  `origin/main...f4e2a62b8264dceb5078fd3ceb2caa3e46c97a53`。
- 完整 diff：320 files changed，35007 insertions，1068 deletions。
- 当前 finding-fix commit：
  `f4e2a62b fix(workflow): #131 收敛分支审查编排`；parent 为
  `38a0e8dd2314b086378e0674f4bd377dc5e6f694`。
- Workspace boundary：expected workspace 与 actual repo root 均为当前 task
  worktree；source checkout HEAD 为
  `ea132e350c4b6861fc955f17e590651a46e890ab` 且 status 为空；
  suspicious source artifacts 为 0。
- 审查开始时仅存在 main-session 已登记的 task metadata tail：
  `agent-assignment.json` 与 `task-commit-plans/004.json`。

本轮只写本 raw report。未修改实现、测试、规划、durable docs、Phase 2、
`review.md`、`review-gate.json`、assignment、task commit plan；未执行 Guru Team
recorder/validator，未 commit、push、创建或修改 PR。

## 当前权威与前置资格

- GitHub Issue `castbox/guru-trellis#131` 当前仍为 open；正文继续要求
  `guru-review-branch` 独占 Branch Review step-local SSOT，workflow 不再复制
  review dimensions、qualification 或 recovery 正文。
- accepted-current comment `#issuecomment-5045031945` 继续要求 thin workflow
  不复制 Branch Review 内部合同；没有新的 issue/comment authority 扩张本轮范围。
- `planning-approval.json` 为 schema 2.0、`typed_exit=approved`；
  `ambiguity_review.status=passed`，`unchecked_normative_hits=[]`，user
  confirmation 为 `post-planning-approval`。当前 planning digests 与记录值精确一致：
  - `prd.md`：
    `6ad8c1137377203441afacc4bd2a1db03e2564cd6f47b1a23c16e1ba612902ec`
  - `design.md`：
    `9b7db338b6c34ed261db10a22b07803fa4950929fbdfecf7dc741da980c5efce`
  - `implement.md`：
    `fa902098b919fa30d8d5a9fee028eb9074f2e40b0cb1a42e4c6530efc2ec53cc`
- `phase2-check.json` 为 schema 2.0、`typed_exit=passed`，把
  `F-131-BR4-01` 与 `F-131-P2-R5-01` 都标记为 `resolved`，并记录
  `full_rerun=true`。
- Phase 2 在 pre-commit HEAD `38a0e8dd...` 上覆盖 13 个 dirty paths；当前提交后
  的四个 non-metadata paths 全部属于该集合：
  - `.trellis/workflow.md`
  - `trellis/workflows/guru-team/workflow.md`
  - `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`
  - `trellis/skills/guru-team/tests/test_skill_packages.py`
- `task-commit-plans/004.json` 精确绑定当前 commit、parent 与 tree：
  expected tree、actual tree、当前 commit tree 均为
  `149df225be6d7b3319a8df0b6bd2bca7e0a043af`，`matches=true`。

上述证据满足本 closure round 的 current HEAD、range、planning、Phase 2、commit、
assignment 与 Docs SSOT 前置条件；没有用 script success 替代本轮语义判断。

## `F-131-BR4-01` 闭环复核

### 原 finding

Round 4/5 证明：虽然旧 Phase 3.5 已包含 active `guru-review-branch` invocation，
global workflow 仍直接给出 Branch Review recorder/checker 调用，并重复 reviewer
roles、qualification、finding closure、fresh final、artifact 与 recorder/checker
规则。普通 main session 读取 workflow 即可遇到第二份行为权威，因此这是
`normal_required_behavior`、P2 current-scope finding。

### 当前实现闭环

当前 canonical 与 dogfood workflow 已完成以下收敛：

- `#### 3.5 Branch Review Gate` 精确保留一次
  `guru-review-branch` mandatory invocation、四个 declared exit markers、两个
  workflow route targets 与一个 fail-closed stop target。
- Phase 3.5 只说明 producer seed projection、target-owned authoring、typed route
  consumer 与 missing/unknown/multiple/stale/unmapped fail-closed；不再复制 13 个
  entry checks、reviewer prompt、qualification、finding lifecycle、raw report、
  fresh final 或 recorder/checker 合同。
- Global task-system/helper/language/finish breadcrumb 不再列出 Branch Review 私有
  artifact bodies、专属 headings、recorder 命令或 metadata-tail schema。
- `### Sub-agent Boundary` 只保留跨 Skill 通用的 platform dispatch identity、
  workspace、等待/liveness、recovery 与“sub-agent completion 不替代 owning Skill
  semantic gate”规则。Branch Review 专属 logical roles、round reuse、finding
  closure、final reviewer 与 artifact construction 已移出 global workflow。
- `review-branch.sh`、`check-review-gate.sh`、
  `--review-source independent-agent`、`--findings-file` 与三个 Branch Review
  logical-role literals 在 canonical/dogfood workflow 中均无残留。
- `trellis/workflows/guru-team/workflow.md` 与 `.trellis/workflow.md`
  byte-identical。

Branch Review step-local 行为没有被删除：canonical 与 installed
`guru-review-branch` package 的 `SKILL.md`、`interface.json` 与
`references/contract.md` 继续独占 13 个 entry preconditions、independent review
dispatch、qualification-before-severity、finding lifecycle、recovery、fresh final、
recorder/validator 与四个 typed exits。

`test_branch_review_workflow_is_routing_only_in_source_and_dogfood` 同时固定
canonical/dogfood 的一次 invocation、四个 exits、禁止残留词与 byte parity；
本轮独立定向重跑通过 1/1。

### Closure 结论

原 normal path 中的第二份 Branch Review 行为 SSOT 已不存在；global route 与 package
step-local owner 当前一致。`F-131-BR4-01` 在 Reviewed HEAD 上已关闭。

## `F-131-P2-R5-01` 状态与回归复核

### Phase 2 finding

Phase 2 发现：旧 throwaway `.new` preview 检查无条件正向要求
`review-source independent-agent`。Public `main` 尚未合入新 workflow 时会偶然通过，
但 exact/current source 正确删除旧文案后反而会失败。这是普通 install/update 路径中
可复现的 P2 correctness/compatibility 缺陷。

### 当前修复

- 当 `USE_LOCAL_WORKFLOW_SAMPLE=1` 时，`.new` 是明确允许的 public marketplace
  discovery sample，只验证它仍是有效 Guru Team workflow；后续 switch、local
  canonical sample、update 与 reapply 仍验证 current Branch Review marker 且拒绝旧
  文案。
- 当使用 exact/current source 时，`.new` preview 直接要求
  `guru-review-branch` mandatory marker，并要求旧文案不存在。
- `test_throwaway_preview_checks_current_branch_review_routing` 固定上述条件分支，阻止
  旧无条件正向 grep 回归；本轮独立定向重跑通过 1/1。
- Fresh Phase 2 在同一最终 implementation tree 上完成完整 throwaway：
  默认模式按预期 exit 2，拒绝 public `main` 冒充未发布 feature ref；
  显式 public-sample 模式 exit 0，覆盖 fresh init、existing preview/switch、
  `trellis update --force`、workflow/preset reapply 与最终无 sidecar。

本轮完整 Skill、preset、source/installed validators、shared eval 与静态门禁重跑均
未发现相关回归。`F-131-P2-R5-01` 在 Reviewed HEAD 上已关闭。

## 完整范围语义复核与候选资格化

本轮不是只审查 `f4e2a62b`。我基于 round 4 对完整 committed range 的 fresh review，
重新读取当前 live authority、approved planning、Phase 2、Docs SSOT、task commit
evidence，并把新 commit 与完整
`origin/main...f4e2a62b8264dceb5078fd3ceb2caa3e46c97a53` 组合复核，覆盖：

- workflow 与 Skill-first SSOT ownership；
- semantic AI judgment 与 deterministic recorder/validator 边界；
- public Skill I/O、四个 exits 与唯一 consumers；
- reviewer qualification、closure、recovery 与 fresh-final role separation；
- canonical、dogfood、installed package 与 selected-platform distribution；
- preset、ownership、throwaway preview、update/reapply 与 sidecar 行为；
- Docs SSOT、task artifacts、测试、安全与部署影响。

候选资格化结果：

- Exact remote feature-ref marketplace install：当前 branch 未获 push 授权且远端 ref
  不存在，属于 publication 前的已知验证限制，不是当前本地实现缺陷；不赋 severity，
  不构成 scope proposal。
- Trellis CLI `0.6.8`、独立 `ruff` / `shellcheck`、`mypy` / `pyright`：
  当前批准基线为 CLI `0.6.5`，仓库未声明这些额外 gate；保持非阻塞未验证项，不赋
  severity。
- 恶意 artifact/hash/state 伪造、TOCTOU、锁、额外并发压力、fault injection、
  crash consistency 与跨 OS atomicity：不能在批准的 normal path 中复现，按明确
  authority 为 `out_of_scope`。

没有新的、可在受支持正常路径中复现且违反当前合同的 P0/P1/P2/P3 finding；没有
unconfirmed nonstandard proposal。

历史 finding 状态：

- Phase 2 `F-131-01..05`：closed。
- Round 1 `F-131-BR-01..04`：closed。
- Round 2 `F-131-BR2-01`：closed。
- Round 4/5 `F-131-BR4-01`：本轮 closed。
- Phase 2 `F-131-P2-R5-01`：本轮复核为 closed。

## Docs SSOT、Phase 2 与提交一致性

- Docs strategy：`ssot_first`。
- `.trellis/spec/workflow/workflow-contract.md` 与
  `.trellis/spec/workflow/skill-package-contract.md` 已把 global routing 与
  step-local closed loop ownership 分开；本次 commit 删除运行 workflow 的第二份
  SSOT，没有产生新的 durable contract delta。
- Throwaway preview 修复承接既有 installer/upgrade-update 合同，不新增 public API、
  schema、exit、consumer projection 或 deployment contract。
- Phase 2 `docs_ssot_plan.task_delta_merged=true`；implementation handoff、Phase 2
  raw report、review rounds 与临时测试输出继续作为 task history。
- Phase 2 evidence 与当前 commit tree 精确连续，四个 post-Phase-2 non-metadata
  changed paths全部已覆盖；不存在需要 Branch Review 首次补写 durable docs 或返回
  Phase 2 的 current-scope inconsistency。
- `#116 guru-review-task-publication` 仍为 planned/missing；`passed` route 在该
  package 不可用时继续 fail closed，本任务没有越界实现 publication。

## 验证结果

| 验证项 | 终态 |
| --- | --- |
| Live Issue #131 与 accepted-current comment | open/current；authority 无新增 scope |
| `git diff --check origin/main...HEAD` | passed，exit 0 |
| `git diff --check origin/main` | passed，exit 0 |
| Closure focused regressions | 2/2 passed |
| `guru-review-branch/tests/test_contract.py` | 8/8 passed |
| Runtime full suite | 566 passed，13 skipped，exit 0 |
| Skill package full suite | 169/169 passed，exit 0 |
| Preset installer suite | 45/45 passed，exit 0 |
| Upstream ownership suite | 6/6 passed，exit 0 |
| Source package validator | passed；10 active Skills / 39 exits / 23 targets |
| Installed package validator | passed；10 active Skills / 39 exits / 23 targets；1903 managed files，0 sidecar/removal/conflict |
| Source shared real-wrapper eval | 7/7 passed |
| Installed shared real-wrapper eval | 7/7 passed |
| Dogfood overlay drift / direct ownership | passed；43 frozen/active paths，0 removed |
| Canonical/dogfood workflow parity | passed |
| JSON parse | 2635 files passed |
| Shell syntax | 295 files `/bin/bash -n` passed |
| Python in-memory compile | 116 files passed |
| Task validation | passed；`implement.jsonl` 11 entries，`check.jsonl` 0 entries |
| Repository sidecar scan | 0 `.new` / `.bak` |

Lint：

- 完整 range 的 `git diff --check`、package/runtime/preset/ownership validators、
  JSON parse 与 shell syntax 均通过。
- 仓库未声明独立 `ruff` / `shellcheck` gate；不把未运行工具表述为通过。

TypeCheck：

- 仓库未配置 `mypy` / `pyright` gate；116 个 Python 文件 compile 与 runtime tests
  通过，但不把它们表述为独立 type-check。

开箱即用 / upgrade-update：

- 本轮独立重跑 preset installer、ownership、dogfood drift、source/installed
  validators、source/installed shared eval 与两项 exact regressions，全部通过。
- Full throwaway 未在 Round 6 再次重复执行；fresh Phase 2 的该项证据已由
  `phase2-check.json`、raw report 与 commit tree continuity 证明对应当前提交内容。
  因而本报告只陈述“同树 Phase 2 已通过”，不冒充本轮独立重跑。
- Exact remote feature-ref install 仍需在未来获得 push 授权并存在远端 ref 后复验。

## 部署与安全影响

- 完整 range 没有 CI/CD workflow、Docker/Compose、Kubernetes/Kustomize、业务数据库
  migration、Makefile 或生产配置变化；两处
  `skills/migrations/production-minimal-handoff.json` 是 Skill contract migration
  manifest，不是数据库 migration，也不要求部署迁移。
- 当前 closure commit 只修改 canonical/dogfood Markdown workflow、throwaway
  deterministic verifier、回归测试及 task-local evidence。
- 未观察到 secret、credential、private key、`.env`、客户数据或签名 URL 泄露。
- 本轮没有执行生产写、部署、push、PR mutation、archive 或 issue close。

## Findings、Scope Proposals 与结论

- Round 6 新 findings：
  - P0：0
  - P1：0
  - P2：0
  - P3：0
- Scope proposals：0。
- `F-131-BR4-01`：closed。
- `F-131-P2-R5-01`：closed。

Round 6 问题闭环审查已完成。本报告可支持主会话记录 closure round 与两项 finding
关闭证据，但不能支持最终 `guru-review-branch:passed` 或最终放行。

下一步必须派发一个未参与 round 4/5 finding discovery、round 6 closure、实现或
Phase 2 的全新 technical reviewer，对当前 HEAD 与完整 `origin/main...HEAD`
执行 Round 7 fresh final review。只有该 reviewer 零 finding 完成且后续 semantic
gate/recorder/validator 全部通过，才能形成最终放行结论。
