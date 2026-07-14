# #122 实现交接

## 结论

`guru-create-task-commit` 已按 `ssot_first` 策略完成 durable docs、canonical
package、runtime、workflow、preset、platform entry、dogfood copy 与测试实现。本交接只
记录实现代理事实，不能替代后续独立 `trellis-check`、`phase2-check.json` 或 Branch
Review Gate。

## R1-R10 承接

| 需求 | 实现结果 |
| --- | --- |
| R1 | production registry 保留 `guru-create-work-commit` reserved tombstone，并激活 `guru-create-task-commit`；extension `0.6.5-guru.5` 登记 skill、artifact schema 与 executor public API。 |
| R2 | canonical/dogfood workflow 只有 1 个 mandatory invoke marker 和 3 个唯一 typed-exit consumers；finding-fix 返回 Phase 2 后重新进入同一 skill。 |
| R3 | candidate validator 绑定 worktree/task/status、planning approval、Phase 2、ledger、base、HEAD 与 NUL-delimited 完整 dirty snapshot。 |
| R4 | package 提供 `task-commit-plans/<sequence>.json` schema/example；AI candidate 记录 exact paths/message/review/authorization/freshness/result，不记录文件正文或本机绝对路径。 |
| R5 | validator 强制四类 path 全覆盖；executor 使用 literal exact path stage，拒绝 artifact 外 staged path，并保留 unrelated 状态。 |
| R6 | Markdown contract 独占 AI Review Gate、conditional confirmation 与 route 判断；runtime 只验证已记录事实。 |
| R7 | `check-commit-messages --candidate-artifact` 复用唯一 `validate_commit_message()`；`create-task-commit` 使用 exact message file 与 `--cleanup=verbatim -F`。 |
| R8 | postcondition 验证 parent、raw message bytes、committed paths、shared parser、unrelated preservation、index/hook mutation，并原子回写唯一 exit；旧 sequence 在新提交后失效。 |
| R9 | step-local 正文只在 canonical package `references/contract.md`；workflow 与五个 continue entry 只保留 stable skill invoke/exit/re-entry。 |
| R10 | preset 向 installed canonical、shared、Codex、Cursor、Claude 分发 package；managed wrapper、manifest、README、dogfood copy、throwaway update/reapply 均已覆盖。 |

## Docs SSOT

- Strategy：`ssot_first`。
- Durable owners 已先于 runtime/schema/installer 实现更新：三份 requirements
  文档、七份 workflow/preset/docs spec、顶层 README、workflow README 与 preset
  README。
- Task delta 已合并：active/reserved id migration、artifact/executor、typed exits、
  re-entry、分发与 upgrade/reapply 合同均进入 durable owner。
- Throwaway 新发现的 Phase 2 self-artifact 递归 digest 缺口已合并到
  `.trellis/spec/workflow/data-contracts.md` 与 package contract：只有 candidate 中
  已绑定 fresh digest 的当前 `phase2-check.json` self path 获得窄 coverage 例外，
  不扩展到其它 task/source/docs/schema/preset/overlay 路径。
- 本任务 `design.md` 第 14 节列出的 durable evidence paths 均有语义变更，无
  no-change evidence path。
- Task-history-only：planning approval、单次命令输出、临时 throwaway repo、真实
  smoke commit SHA、sidecar 处理过程与本交接保留在 task evidence，不进入公共
  package。

## 分发与升级

- Canonical preset apply 最终幂等：`updated_managed=[]`、
  `managed_backups=[]`。
- 首次同步本轮 delta 生成 1 个 runtime 与 5 个 package contract 已知升级 `.bak`；
  已逐个确认只含旧 managed bytes，清理失败 provenance manifest 后由 installer
  重建。
- 最终 source/installed validator：reserved 1、active 1、invoke 1、exit 3；
  dogfood selected platforms 为 Claude/Codex/Cursor，managed skill files 43，
  conflict/removal/sidecar 均为 0。
- Canonical workflow 与 `.trellis/workflow.md` 字节一致；canonical runtime 与
  dogfood runtime 字节一致；overlay drift 通过。

## 验证证据

- Targeted candidate/executor tests：7/7 通过，包含 dirty
  `phase2-check.json` self-evidence 回归。
- Package/preset/runtime full suite：484 tests，124.443s，`OK`。
- Clean throwaway：公开 marketplace discovery 后使用当前未发布 canonical workflow
  样本，preset install 与 source/installed discovery 通过。
- Throwaway initial commit：`e6ce08e097e00355305fd85b416f9f714abb5272`，
  parent `baa5c24c3197cc1e40f3d58b3cefb59edff8fa36`，sequence `001`，
  exact paths 包含 task evidence、fresh Phase 2、candidate 与 source fixture。
- Throwaway finding-fix commit：`217fb13577306d83be2ae2e52ba90b8de0ff2f49`，
  parent 为 initial commit，sequence `002`，包含 fresh Phase 2、sequence 001
  post-result、sequence 002 与 source fix；旧 plan candidate 返回非零。
- 两轮真实 executor 均返回 `status=committed` / `exit=committed`，unrelated file
  内容与 untracked 状态在两轮提交后保持不变。
- Throwaway 后续 `trellis update --force`、workflow preview/switch、workflow
  reapply、preset reapply、source/installed validation、dogfood drift、closeout smoke
  与最终 recursive sidecar scan 全部通过。
- Task validation、phase 2.2/3.4/3.5 context parsing、JSON parse、`py_compile`、
  全量 Bash syntax、`git diff --check`、公共 package/manifest/README 安全扫描通过。

## AC 状态

- AC1-AC11：本地实现与验证证据已覆盖，交由独立 checker 复核语义充分性。
- AC12：local throwaway 已通过；remote current feature-ref marketplace verifier
  仍按合同延后到 reviewed content push 后由 `trellis-finish-work` 生成，当前不能
  宣称 remote feature-ref 已验证。
- AC13：ledger 只把 #122 放入 `close_issues`；#92、#120 仅在
  `related_issues`，work message 只使用 `Refs #122`。
- AC14：公共 package/schema/example/manifest/README 未发现 secret、客户数据、
  `.env` 内容、签名 URL或本机绝对路径。

## 部署与安全影响

本任务只修改 Trellis workflow/preset/runtime/package/docs/test 资产，不增加应用
service、CLI runtime service、worker、queue、migration 或 runtime config。未修改
GitHub Actions、Dockerfile/Compose、Kubernetes/Kustomize、数据库 migration 或
Makefile；无需部署资产同步。Executor 不打印 dirty file content，不 push、不改写历史，
temporary message file 使用 `0600` 并在 `finally` 删除。

## 后续门禁与剩余风险

1. 独立 `trellis-check` 仍需覆盖 R1-R10、AC1-AC14、完整 dirty diff、Docs SSOT、
   parser compatibility、installer/update/security/deployment，并记录
   `phase2-check.json`。
2. 通过 Phase 2 后才使用当前 skill 为本任务创建真实 task work commit；本交接阶段
   未 commit 当前分支。
3. Work commit 后仍需独立 Branch Review Gate；本交接阶段未运行 Branch Review。
4. 当前分支未 push，因此 local throwaway 的 marketplace discovery 来自公开
   `main`，随后明确覆盖当前 canonical workflow 样本完成本地验证。Remote exact
   feature-ref discovery 是唯一已知未覆盖的开箱即用证据，必须在 publish 前补齐。
5. Throwaway 观察到本机 npm 最新 Trellis 为 `0.6.6`，本扩展的已批准兼容目标仍是
   `0.6.5`；本任务不扩展 CLI baseline，后续升级需单独执行兼容性评估。

## Branch Review Round 1 finding-fix delta

本轮实现代理 `trellis_implement_122_round1_fix` 以
`afcab19397a6ebc7cbd571722ba01950b670e620` 为输入 HEAD，只修复
`reviews/round-001-final-release.md` 的 3 个 blocking finding。Round 1 raw report、
`review-findings-round-001.json`、`review-gate.json` 与既有 Phase 2 evidence 未改写。

### Finding 修复

- P1 hook same-path mutation：exact staging 后、hook 执行前使用 `git write-tree`
  绑定完整 expected index tree，并为每个 exact path 记录 expected blob/mode；提交
  后读取真实 commit tree 与逐路径 actual blob/mode。tree、blob、mode 任一不一致均
  写入 strict `blocked` result，`hook_mutation=true`，保留真实 commit/index/worktree
  现场。新增 content+restage、mode+restage 两条负向回归，以及 benign hook 和既有
  no-hook 正向路径。
- P2 literal identity：index 与 HEAD/expected/actual tree 的所有 path-bearing Git
  identity 查询均使用 `git --literal-pathspecs`，并只接受 0 条或 1 条 path bytes
  完全相等的 NUL record；多条、非 exact 或 unmerged index identity fail closed。
  新增 tracked、staged、worktree delete、staged delete 的 metacharacter path 与 decoy
  collision 回归，并覆盖 HEAD tree identity。
- P2 result schema：canonical public schema 把 `result` 收敛为 closed `oneOf`
  状态机；`planned` 无 exit，`revision-required` / `blocked` / `committed` 与同名
  exit 配对且禁止额外字段。`committed` 强制 commit、parent、message、paths、
  preservation、hook 与 tree/blob/mode evidence；全部 `blocked` runtime branch 统一
  写入 failure stage、pre/current HEAD、head-changed、parent/message/path、
  preservation、hook、unexpected staged、tree evidence 与非空 errors。Runtime 在
  atomic write 前执行 public schema 与跨字段 post-result validator。

### Round 1 Docs SSOT

- Strategy 继续使用 `ssot_first`。
- 新公开字段与 deterministic 行为已先合并到 canonical package
  `references/contract.md`、`.trellis/spec/workflow/data-contracts.md` 和
  `.trellis/spec/workflow/companion-scripts.md`，再实现 runtime/schema/tests 并通过
  preset 同步 installed/platform copies。
- 顶层 requirements、flow、workflow route 与 preset install 语义无需改动：既有
  R5/R8 已要求 literal exact identity、hook mutation fail closed 与可审计
  postcondition；本轮只补齐 objective implementation 和公开 result evidence。
- Round 1 raw report、复现输出、临时 throwaway 路径、`.bak` 核对过程与本节属于
  task history，不进入公共 skill package。

### Round 1 分发与验证

- Final targeted：`TaskCommitCandidateExecutorTest` 15 tests 加 canonical package
  contract 4 tests，共 19 tests，6.934s，`OK`。
- Final full package/runtime/preset suite：493 tests，121.590s，`OK`；canonical
  package standalone 4 tests，`OK`。
- Final clean throwaway：默认远端 `main` source 在未 push feature branch 时先正确
  fail closed；显式允许 public marketplace sample 后，公开 discovery 加本地未发布
  canonical workflow 样本完成 initial commit、fresh finding-fix sequence、old-plan
  reject、unrelated preservation、`trellis update --force`、workflow preview/switch、
  preset reapply、source/installed validators、dogfood drift、closeout smoke 与最终
  recursive sidecar scan，exit 0。
- 首次误用 apply 默认平台集时，installer 正确阻塞 Claude removal 与 unresolved
  provenance；随后使用要求的 `--all-platforms`，逐个确认 17 个 `.bak` 均为本次
  更新前的 managed bytes 后清理并重建 manifest。Final idempotent apply 为
  `updated_managed=[]`、`managed_backups=[]`；Claude/Codex/Cursor 共 43 个 managed
  skill files，source/installed passed，conflict/removal/sidecar 为 0，dogfood drift
  passed。
- Final static gates：workspace boundary、planning approval、task validate、phase
  2.2/3.4/3.5 context、changed JSON、canonical/installed `py_compile`、全量 Bash
  syntax、`git diff --check`、wrapper executable、staged-empty、source-checkout clean、
  public asset secret/absolute-path scan 与 recursive `.new/.bak` scan均通过。

### Round 1 后续门禁

1. 必须派发新的独立阶段二检查代理，覆盖本轮完整 dirty diff；本实现代理未写入或
   record `phase2-check.json`。
2. Phase 2 通过并取得独立 commit 授权后，使用 fresh
   `task-commit-plans/002.json` 创建 finding-fix work commit；不得复用 sequence 001。
3. Work commit 后由 finding owner closure review 复核 3 个 finding，再由全新最终
   放行代理审查完整 `origin/main...HEAD`；本实现代理未执行 Branch Review。
4. Remote exact feature-ref marketplace verification 仍需在 reviewed content push
   后完成，当前只可声明 local unpublished workflow sample 通过。

## Branch Review Round 2 C-01 修复 delta

本轮实现代理 `trellis_implement_122_round2_fix` 以
`03e813c5af37dec98c2c77114bc877c774256074` 为输入 HEAD，只修复
`reviews/round-002-finding-closure.md` 与
`review-findings-round-002.json` 的 C-01 P2。未改写 Round 1/2 raw reports、
`review.md`、`review-gate.json`、review findings、agent assignment 或 Phase 2
recorder；未 commit、push、创建 PR 或调用 finish-work。

### C-01 实现结果

- Public schema 从局部 mismatch conditional 扩展为完整
  `failure_stage × head_changed` 状态矩阵：
  - `pre-commit` 必须 HEAD 未变、无 created commit identity；tree 尚未绑定时为
    `null`，已绑定时只能是 matching `actual_source=index` evidence。
  - `commit` 必须有 tree evidence；HEAD 未变时来源为 index 且没有
    parent/message/path identity，HEAD 已变时来源为 commit 且有 message/path
    identity。
  - `postcondition` 必须 HEAD 已变、有 created message/path identity，并使用
    commit-sourced tree evidence；matching tree 的非 tree 错误仍可表示。
- Runtime cross-field validator 实现同一矩阵，并额外校验 `commit_sha` /
  `pre_commit_head` 关系、tree path 唯一覆盖、逐路径 `matches` 与 blob/mode
  一致性、tree `matches` 与 tree/path facts 一致性，以及 `hook_mutation` 与
  tree/path/index/worktree/unrelated drift 的派生关系。
- 指定 tamper 已双重拒绝：`pre-commit + mismatched tree +
  hook_mutation=false` 与 `postcondition + tree_evidence=null +
  head_changed=false` 均同时被 public JSON Schema 和不依赖 schema 的 runtime
  cross-field validation 拒绝。`commit + null tree` 也加入负向矩阵。
- 正向矩阵保留：合法 pre-commit（tree 未绑定/已绑定）、无 mutation failing
  hook、修改 index 的 failing hook、commit 后 mutating hook、matching tree 的
  non-tree postcondition error 均通过；既有 literal/unmerged/tree/blob/mode
  executor 回归继续通过。

### Bug Analysis：failure stage 证据状态机不完整

#### 1. Root Cause Category

- **Category**：B - Cross-Layer Contract；伴随 D - Test Coverage Gap。
- **Specific Cause**：Round 1 把问题建模为“tree mismatch 时必须
  `hook_mutation=true`”的局部条件，没有先从真实 executor 的 `pre-commit`、
  `commit`（HEAD 未变/已变）与 `postcondition` 分支推导字段可达性。结果是 schema
  shape 与 runtime semantics 同时保留了生产者无法创建的组合，而测试只覆盖
  commit-stage mismatch，没有形成阶段 cross-product。

#### 2. Why Fixes Failed

1. Round 1 conditional：只修复已观察到的 mismatch/hook 布尔矛盾，属于
   incomplete scope；没有约束 tree 是否必须存在、`actual_source`、HEAD 与
   commit identity 的组合。
2. Round 1 tests：覆盖正常 commit、failing hook 与 post-commit mutation，但未加入
   pre-commit mismatch、commit/postcondition null-tree 和 wrong-source negative
   matrix，因此 package/runtime tests 全绿仍无法证明四态 result 完整。

#### 3. Prevention Mechanisms

| Priority | Mechanism | Specific Action | Status |
| --- | --- | --- | --- |
| P0 | Durable contract | package contract、`data-contracts.md`、`companion-scripts.md` 共同记录 failure-stage 状态矩阵与 schema/runtime 分工 | DONE |
| P0 | Architecture | Schema 约束 public shape，runtime 校验跨对象 equality/set/derived facts，任一层拒绝即 fail closed | DONE |
| P0 | Test coverage | schema 与 runtime 各自执行完整正负 cross-product，并证明 runtime 在 schema 被 mock 掉时仍独立拒绝两个指定 tamper | DONE |
| P1 | Review checklist | `cross-layer-thinking-guide.md` 新增 tagged result state-machine matrix checklist | DONE |

#### 4. Systematic Expansion

- **Similar Issues**：所有带 `status`、`stage`、`kind`、`failure_stage` 的 artifact，
  尤其是同时存在 derived boolean 与 source tag 的 evidence payload。
- **Design Improvement**：先维护“producer branch -> legal row”矩阵，再把可由 schema
  表达的 shape 与只能由 runtime 表达的 equality/set 关系分别实现。
- **Process Improvement**：review finding 修复不得只为单个 payload 增加 conditional；
  必须加入每个 discriminator row 的至少一个正向和一个负向测试，并覆盖非主错误。

#### 5. Knowledge Capture

- [x] 更新 `.trellis/spec/guides/cross-layer-thinking-guide.md`。
- [x] 更新 `.trellis/spec/workflow/data-contracts.md` 与
  `.trellis/spec/workflow/companion-scripts.md`。
- [x] 更新 canonical package contract/schema/tests，并通过 preset 同步所有 installed
  与 platform copies。
- [x] 无需新 issue：C-01 属于 #122 的 Round 1 F-03 当前闭环范围。

### Round 2 分发与验证

- Targeted `TaskCommitCandidateExecutorTest`：18/18，`OK`；canonical package：
  4/4，`OK`。
- Full package/runtime/preset suite：496/496，126.959s，`OK`。
- Canonical preset `--all-platforms` 同步 runtime 和 5 份 package copies；首次生成
  的 16 个 known-managed `.bak` 逐个与 `HEAD` 旧 managed blob 相等后清理。Sidecar
  存在时生成的 conflict provenance 按 installer remediation 删除 installed
  `extension.json` 后从 canonical 重建；最终 source/installed passed，managed files
  43，conflict/removal/sidecar 为 0，dogfood drift passed。
- Clean throwaway：默认 exact feature-ref 因 branch 未 push 正确 fail closed；使用
  `TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1` 后，公开 `main` workflow discovery 加
  当前本地 preset/package 完成 init、install、source/installed validation、update、
  workflow switch/reapply、preset reapply、closeout failure matrix 与 drift，exit 0。
- Static gates：workspace boundary、planning approval、task validate、phase
  2.2/3.4/3.5 context、全量相关 Bash syntax、canonical/dogfood Python compile、
  changed JSON parse、`git diff --check`、canonical/installed byte equality、recursive
  `.new/.bak=0`、staged-empty、source-checkout clean、安全扫描与 deployment path scan
  全部通过。

### Round 2 后续门禁

1. 必须由 fresh 阶段二检查代理独立复核 C-01 和当前完整 dirty diff；本实现代理不
   记录 `phase2-check.json`，也不判定 finding closed。
2. Fresh Phase 2 通过后必须创建新的 sequence 与独立 commit 授权；不得复用
   sequence 001/002 的 artifact 或授权。
3. Commit 后由原 finding owner 执行 closure review；全部 finding 关闭后仍需 fresh
   最终放行审查代理。
4. Remote exact feature-ref marketplace verification 继续等待 reviewed content
   push 后由 finish-work 执行，当前未通过且未宣称通过。

## Branch Review Round 3 C-01-T1 修复 delta

本轮实现代理 `trellis_implement_122_round3_fix` 以
`1534b545ad6777852cd6d588568a46bedb14bf9c` 为输入 HEAD，只修复
`reviews/round-003-finding-closure.md` 的 `C-01-T1` P2。未修改 runtime、public
schema、canonical contract、durable spec、workflow 或 preset 实现；未改写任何 raw
review、`review.md`、`review-gate.json`、finding artifact、agent assignment、Phase 2
recorder 或 task commit plan；未 commit、push、创建 PR、调用 finish-work 或关闭
issue。

### 永久状态矩阵回归

- Canonical package `tests/test_contract.py` 现在独占共享 test builder：
  `task_commit_blocked_producer_matrix()` 定义 7 个合法 producer rows，完整覆盖
  `pre-commit` tree 未绑定/已绑定、`commit` unchanged HEAD clean/mutated、`commit`
  changed HEAD、`postcondition` clean/mutated。
- 同一 canonical test module 的 `task_commit_schema_negative_matrix()` 定义 15 个
  schema 可表达的 shape/source 负向 case，逐行覆盖 HEAD/identity、tree required 与
  `actual_source`、message/path identity 的缺失或非法组合。Package public-schema test
  对 7 个合法 rows 逐项通过，并对 15 个负向 case 逐项拒绝。
- Runtime test 不再维护第二份手写 producer matrix。它通过只读动态 import 直接复用
  canonical package test builder，并在正常 schema 路径与 mock schema 路径下同时
  验证 7 个合法 rows；15 个 schema negative 在 mock schema 后仍由 runtime
  cross-field validator 独立拒绝。
- `task_commit_runtime_tamper_matrix()` 永久固化 Round 3 / Phase 2 的 12 个
  schema-bypass tamper：pre-commit mismatch、commit null tree、postcondition null
  tree/unchanged HEAD、两类 wrong source、两类 HEAD identity contradiction、duplicate
  path、missing path、blob equality/path match 矛盾、tree aggregate match 矛盾，以及
  mode evidence/derived mutation 矛盾。Clean evidence + `hook_mutation=true` 与 mutation
  evidence + `hook_mutation=false` 两个方向都被覆盖。
- 新测试没有暴露 runtime/schema 行为缺陷，因此本轮没有扩大到实现、schema、contract
  或 spec 修改。

### Round 3 Docs SSOT

- Strategy 继续为 `ssot_first`。Canonical package contract、
  `.trellis/spec/workflow/{data-contracts.md,companion-scripts.md}` 与
  `.trellis/spec/guides/cross-layer-thinking-guide.md` 在输入 HEAD 已正确、完整定义
  `failure_stage × head_changed` producer matrix、schema/runtime 分工和正负
  cross-product 要求，本轮无需更新 durable spec。
- Round 3 的 task delta 已合并到 durable canonical test asset，并通过受控 preset
  同步到 installed/shared/Claude/Codex/Cursor test copies；没有待 merge 的长期测试
  合同 delta。
- 本节、Round 3 raw report、第一次 apply 产生并经 HEAD blob 核实后删除的 5 个
  `.bak`、conflicted installed manifest remediation 过程和单次测试输出只保留为 task
  history，不进入公共 package 或 durable spec。

### Round 3 分发与验证

- 受控 `apply.sh --repo . --all-platforms` 更新 5 个 managed package test copies；5
  个 `.bak` 的 blob 均精确等于 HEAD 中同步前的 managed blob
  `2f0619b16720fb7d990859aa6d9c81acf3889a9a`，核实后清理。按 installer remediation
  删除 conflicted installed `extension.json` 并从 canonical 重建；最终幂等 apply 为
  `updated_managed=[]`、`managed_backups=[]`，43 个 managed files、0
  conflict/removal/sidecar。
- `.trellis/guru-team/extension.json` 只承接受控 installed provenance 更新：package
  tree/test-file digest 更新为当前 canonical bytes，并刷新 source commit/time 与
  deterministic inventory order；没有扩展 public API 或 runtime 行为。
- Targeted `TaskCommitCandidateExecutorTest`：18/18，`OK`；canonical 加 5 个 managed
  package copies standalone：24/24，`OK`。
- Full package/runtime/preset suite：496/496，124.870s，`OK`。
- Clean throwaway：使用脚本支持的
  `TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1`，公开 marketplace discovery 加当前本地
  unpublished canonical sample 完成 initial install、source/installed validation、
  task commit smoke、`trellis update`、workflow/preset reapply、dogfood drift、closeout
  smoke 与 recursive sidecar check，exit 0。该结果不冒充 remote exact feature-ref
  evidence。
- Source/installed skill validators passed；dogfood overlay drift passed；planning
  approval、task validate、phase 2.2/3.4/3.5 context、Python compile、JSON parse 与
  `git diff --check` passed。Phase 2 checker 随后把 duplicate-path 与 clean-evidence
  mutation case 收敛为单一变量 tamper，受控同步后的 canonical 与 5 个 copies
  SHA-256 均为
  `b69224e54da83612b1d92958471a6a0029da42192d62a451beeec963e196ff31`；该修复不改变
  7/15/12 数量或 public contract，只消除其它拒绝条件掩蔽目标断言的风险。
- Source checkout `/Users/wumengye/Documents/GoProjects/guru-trellis` 保持 clean，HEAD
  为 `6b9495a17dc953c7a54c105e39c23a786edcd8a7`；task worktree staged paths 与 recursive
  `.new/.bak` 均为 0。测试-only diff 不涉及 GitHub Actions、Dockerfile/Compose、
  Kubernetes/Kustomize、Helm、migration 或 Makefile，不需要部署资产同步。

### Round 3 后续门禁与 trellis-check focus

1. Fresh 独立阶段二检查必须复核 `C-01-T1`：共享 builder 确实由 package/runtime
   共用，合法矩阵为 7 rows，schema negative 为 15 cases，runtime schema-bypass
   tamper 为 12 cases，并覆盖 derived `hook_mutation` 两个方向。
2. Checker 必须复核 canonical/test copies/installed manifest 的 managed digest、完整
   dirty diff、Docs SSOT no-update 理由、source/installed/drift、throwaway/update/reapply、
   security/deployment 和 workspace hygiene；本实现代理不写入或 record fresh
   `phase2-check.json`。
3. Fresh Phase 2 通过后必须创建新 sequence 004 与取得独立 commit 副作用授权；不得
   复用 sequence 001/002/003 或旧授权。Commit 后由原 finding owner 再次执行 closure
   review；finding 归零后仍需全新最终放行代理审查完整 `origin/main...HEAD`。
4. Remote exact feature-ref marketplace verification 仍等待 reviewed content push 后
   由 finish-work 执行；当前未通过且未宣称通过。

## Branch Review Round 4 C-01-T2 修复 delta

本轮实现代理 `trellis_implement_122_round4_fix` 以
`ce7056793ff49a82bf8275340986225af5b4c868` 为输入 HEAD，只修复
`reviews/round-004-finding-closure.md` 的 `C-01-T2` P2。未修改 runtime、public
schema、canonical contract、durable spec、workflow、preset 实现或 planning docs；
未改写任何 raw review、`review.md`、`review-gate.json`、finding artifact、
`agent-assignment.json`、`phase2-check.json` 或 task commit plan；未 stage、commit、
push、创建 PR、调用 finish-work 或关闭 issue。

### 非掩蔽 runtime tamper 合同

- Canonical package
  `trellis/skills/guru-team/packages/guru-create-task-commit/tests/test_contract.py`
  的 `task_commit_runtime_tamper_matrix()` 仍独占 12 个 schema-bypass tamper 的
  payload SSOT，但每个 case 现在同时携带 `result` 和非空、无重复的
  `expected_errors`。没有新增第二份 label/error mapping。
- Path match case 现在从合法 postcondition row 只把单个 path-level
  `matches` 从 `true` 翻为 `false`；blob、mode、tree identity、aggregate
  `matches` 与 `hook_mutation` 保持合法，因此 runtime 只返回
  `task commit result path match flag contradicts blob/mode evidence.`。
- Aggregate tree match case 现在只把 `tree_evidence.matches` 从 `true` 翻为
  `false`；tree/path identity、各 path `matches` 与 `hook_mutation` 保持合法，
  因此 runtime 只返回
  `task commit result tree match flag contradicts tree/blob/mode evidence.`。
- Postcondition null-tree case 也收敛为只删除 tree evidence，不再同时篡改
  `commit_sha` / `head_changed`。其余 case 保持各自最小 payload；pre-commit
  HEAD identity 的两个相互约束错误使用完整 expected list 精确断言。Runtime test
  对 12/12 直接复用 canonical `expected_errors` 并执行完整列表相等比较，不再只
  断言 `errors` 非空；删除、改名或由其它错误替代任一目标 validator 都会使测试
  失败。
- 当前 matrix 数量保持 7 个合法 producer rows、15 个 schema negatives、12 个
  runtime tampers；runtime/schema/contract 行为没有改变。

### Round 4 Docs SSOT

- Strategy 继续为 `ssot_first`。本轮实现前已复核
  `.trellis/spec/workflow/{workflow-contract.md,companion-scripts.md,data-contracts.md,skill-package-contract.md,quality-guidelines.md}`、
  `.trellis/spec/preset/{installer.md,overlay-guidelines.md}` 与
  `.trellis/spec/guides/{code-reuse-thinking-guide.md,cross-layer-thinking-guide.md}`。
- 现有 durable owner 已要求 package/runtime 共享完整正负 cross-product、derived
  boolean 双向测试、canonical-first 分发和精确 managed-hash upgrade。本轮只让永久
  tests 对既有 validator 形成反事实保护，没有新增 public field、producer row、
  runtime behavior、schema rule、workflow route、installer behavior、部署合同或
  upgrade 语义，因此无需修改 durable docs；这不是切换为
  `no_docs_update_needed`，而是 `ssot_first` 下既有 SSOT 完整且本轮仅补强测试
  证明的 no-change 结果。
- 长期 task delta 已合并到 canonical test builder/runtime assertion，并通过 preset
  同步 installed/shared/Claude/Codex/Cursor package test copies；本节、Round 4 raw
  report、单次命令输出、首次 apply sidecar remediation 和执行时间只属于 task
  history，不进入公共 package 或 durable spec。

### Round 4 精确修改路径

- Canonical work paths：
  - `trellis/skills/guru-team/packages/guru-create-task-commit/tests/test_contract.py`
  - `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
- 受控 installed/provenance paths：
  - `.trellis/guru-team/skills/packages/guru-create-task-commit/tests/test_contract.py`
  - `.agents/skills/guru-create-task-commit/tests/test_contract.py`
  - `.claude/skills/guru-create-task-commit/tests/test_contract.py`
  - `.codex/skills/guru-create-task-commit/tests/test_contract.py`
  - `.cursor/skills/guru-create-task-commit/tests/test_contract.py`
  - `.trellis/guru-team/extension.json`
- Task-local history path：本 `implementation-handoff.md` 章节。

### Round 4 分发与验证

- Targeted runtime matrix：1/1，`OK`；完整
  `TaskCommitCandidateExecutorTest`：18/18，7.235s，`OK`；canonical package：
  4/4，`OK`。
- Canonical 加 5 个 installed/shared/platform package roots：各 4/4，共 24/24，
  全部 `OK`；六份 test bytes SHA-256 均为
  `b17cc36d9ff0817f0d621626b1355a4f8d16b7456308e88790a1b8a4b637b297`。
- Full package/runtime/preset suite：496/496，128.638s，`OK`。
- 首次 `apply.sh --repo . --all-platforms` 按 managed-hash 合同生成 5 个
  `.bak` 并阻塞 installed validation；5 个备份的 SHA-256 均为
  `b69224e54da83612b1d92958471a6a0029da42192d62a451beeec963e196ff31`，
  与各自 `HEAD` managed blob 精确一致。核实后清理备份，并按 installer
  remediation 从 canonical 重建 installed `extension.json`。最终 apply 为
  `updated_managed=[]`、`managed_backups=[]`，43 个 managed files、
  conflict/removal/sidecar 均为 0；source/installed validators 和 dogfood drift
  passed。
- Clean throwaway 使用
  `TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1 verify-throwaway-install.sh` exit 0，
  覆盖 public marketplace discovery + local unpublished canonical sample、fresh
  install、initial/finding-fix task commit、old-plan reject、`trellis update`、
  workflow/preset reapply、source/installed、dogfood drift、closeout smoke 与
  recursive sidecar。该结果不冒充 remote exact feature-ref evidence。
- Workspace boundary、planning approval、task validate、phase 2.2/3.4/3.5 context、
  Python compile、全量相关 Bash syntax、JSON parse、`git diff --check`、
  recursive `.new/.bak=0`、staged-empty 均通过。Source checkout
  `/Users/wumengye/Documents/GoProjects/guru-trellis` 保持 clean，HEAD 为
  `6b9495a17dc953c7a54c105e39c23a786edcd8a7`。
- 本轮 8 个 non-task work paths 的新增行高置信 secret/credential URL/机器用户
  绝对路径命中为 0；未修改 GitHub Actions、Dockerfile/Compose、
  Kubernetes/Kustomize、Helm、migration 或 Makefile，也未增加 service、worker、
  scheduler、queue、runtime config 或数据迁移，因此无需部署资产同步。

### Round 4 后续门禁与 trellis-check focus

1. 必须由 fresh 阶段二检查代理独立复核 `C-01-T2`、12/12 canonical
   `expected_errors`、path/aggregate 单变量 payload、完整当前 dirty diff、Docs
   SSOT no-change 理由、source/installed/drift、throwaway/security/deployment 与
   workspace hygiene；本实现代理不记录或验证 fresh `phase2-check.json`。
2. Fresh Phase 2 通过后必须创建新的 sequence 005 和独立 commit 副作用授权；不得
   复用 sequence 001-004 或旧授权。Commit 后由原 finding owner 执行下一轮 closure
   review；finding 归零后仍需此前未参与任何 review round 的全新最终放行代理审查
   完整 `origin/main...HEAD`。
3. Remote exact feature-ref marketplace verification 继续等待 reviewed content
   push 后由 finish-work 执行；当前未通过且未宣称通过。

## Round 6 findings 实现交接（2026-07-13T15:41:57Z）

### 身份、边界与基线

- 逻辑角色：`实现代理`；技术身份：`trellis_implement_122_round6_fix`。
- 固定 worktree：
  `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/122-guru-create-task-commit`。
- 实现前与实现后 code HEAD 均为
  `163e64168d5d9783c32665da92aebbb4397564a3`；未 stage、commit、push、创建 PR、
  调用 finish-work 或运行 Phase 2 / Branch Review recorder。
- Source checkout `/Users/wumengye/Documents/GoProjects/guru-trellis` 保持 clean，
  HEAD 为 `6b9495a17dc953c7a54c105e39c23a786edcd8a7`。
- Workspace boundary、schema 1.2 planning approval 与 task validation 在实现前后
  均通过；未修改 `prd.md`、`design.md`、`implement.md`。

### F-06-01：非普通 Git operation state fail closed

- Canonical runtime 新增只读 Git operation detector，通过 `git rev-parse
  --git-path` 检测 `MERGE_HEAD`、`CHERRY_PICK_HEAD`、`REVERT_HEAD`、
  `REBASE_HEAD`、`sequencer/`、`rebase-merge/` 与 `rebase-apply/`。返回事实只含
  stable operation id、Git path token 与 marker/directory 类型，不保存绝对路径或
  marker 内容。
- Candidate validator 在进入普通 candidate validation 前拒绝 active state；executor
  在任何 stage 副作用前再次拒绝，并在紧邻 `git commit` 前第三次检查。Runtime
  不消费、清除或修复 marker，也不替代 Markdown skill 的 AI/human confirmation owner。
- 真实 conflict cherry-pick regression 稳定创建 `CHERRY_PICK_HEAD`，证明 candidate
  command 与 executor 都以 exit code 2 / blocked 结束，且 marker bytes、HEAD、index、
  porcelain worktree state 与 candidate bytes 前后完全一致。
- Table-driven objective regression 覆盖上列 7 个 marker/directory state，并验证 detector
  不修改对应 inode。Artifact schema/result state machine 无需为即时 operation state
  新增字段，因此没有制造新的持久化 freshness owner。

### F-06-02：gitlink worktree identity

- `capture_task_commit_snapshot()` 识别 index mode `160000`。非删除 gitlink 必须是
  exact path 自身的 initialized Git worktree，`HEAD^{commit}` 必须唯一，内部
  `git status --porcelain=v1 -z --untracked-files=all --ignore-submodules=none`
  必须 clean；snapshot 记录 `gitlink_head`、`gitlink_initialized=true`、
  `gitlink_dirty=false`。Uninitialized、dirty、unborn 或 root-mismatched 状态 fail closed。
- Deliberate unstaged gitlink delete 保留 delete compatibility，并记录条件删除 identity：
  `gitlink_head=null`、`gitlink_initialized=false`、`gitlink_dirty=null`。普通文件、
  symlink、delete、rename、Unicode 与 pathspec metacharacter 路径的既有 identity 行为
  不变。
- Public schema 仍使用 `guru-task-commit-plan-1.0` / `schema_version=1.0`：三个字段是
  optional/conditional，旧无 gitlink 的 plan 不要求新增字段；mode `160000` 的新安全
  candidate 必须满足 conditional identity。旧 gitlink plan 若缺少这些字段会按安全
  迁移合同 fail closed 并需重新生成，不会被静默接受。
- 真实 A/B/C submodule regression 证明：superproject index 指向 A、B 时 candidate
  validation passed；B 切换到 C 后 snapshot stale，validator/executor blocked，C 未被
  stage，superproject HEAD/index tree/status 与 candidate bytes 不变。另有真实 dirty、
  deinitialized 与 unborn boundary regression。

### F-06-03：global workflow SSOT 收敛

- `trellis/workflows/guru-team/workflow.md` 与 `.trellis/workflow.md` 已删除 task work
  subject/type/scope/body/footer 详细模板。Global workflow 只引用 installed
  `check-commit-messages` shared branch validator 与 mandatory
  `guru-create-task-commit` owner；Phase 3.4 的唯一 invoke、三条 typed-exit route、finding
  repeat 与 fail-closed transition 保持不变。
- Trellis metadata empty-body subject 与 merge payload 仍由非 task-work owner 保留，
  并在 heading/正文中明确与 step-local package 分界；canonical/dogfood workflow
  byte-equal。
- `test_skill_packages.py` 现在直接扫描 canonical 与 dogfood workflow，拒绝完整 work
  template token、任何直接 `git commit`、`validate_commit_message(` 或 parser
  definition，同时要求 shared validator 引用和 mandatory stable skill marker。五个平台
  route-only regression 继续保留。

### Round 6 Docs SSOT

- Strategy：`ssot_first`。Runtime/schema/test 编辑前先更新长期 owner：
  - `README.md`
  - `docs/requirements/README.md`
  - `docs/requirements/requirement-main.md`
  - `docs/requirements/guru-team-trellis-flow.md`
  - `trellis/workflows/guru-team/README.md`
  - `.trellis/spec/workflow/workflow-contract.md`
  - `.trellis/spec/workflow/companion-scripts.md`
  - `.trellis/spec/workflow/data-contracts.md`
  - `.trellis/spec/workflow/skill-package-contract.md`
  - `.trellis/spec/workflow/quality-guidelines.md`
- Task delta 已合并到 requirements、workflow/package owner、operation/gitlink data
  contract 与永久测试。`.trellis/spec/preset/{installer.md,overlay-guidelines.md}`、
  `.trellis/spec/docs/public-docs.md` 与 `trellis/presets/guru-team/README.md` 已复核但
  无需改字节：本轮没有改变 installer 算法、managed path、platform entry 语义、公共安装
  命令或文档语言规则，只更新其分发内容。
- Round 6 raw finding、技术 agent 身份、真实临时仓库命令输出、首次 apply 的 26 个
  `.bak` 处理过程、测试耗时与本节执行时间属于 task-history-only，不进入公共 package。

### Round 6 精确修改路径

- Canonical workflow/runtime/test：
  - `trellis/workflows/guru-team/workflow.md`
  - `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
  - `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
  - `trellis/skills/guru-team/tests/test_skill_packages.py`
- Canonical package 精确文件：
  - `trellis/skills/guru-team/packages/guru-create-task-commit/interface.json`
  - `trellis/skills/guru-team/packages/guru-create-task-commit/references/contract.md`
  - `trellis/skills/guru-team/packages/guru-create-task-commit/schemas/task-commit-plan.schema.json`
  - `trellis/skills/guru-team/packages/guru-create-task-commit/examples/task-commit-plan.json`
  - `trellis/skills/guru-team/packages/guru-create-task-commit/tests/test_contract.py`
- Dogfood workflow/runtime/provenance：
  - `.trellis/workflow.md`
  - `.trellis/guru-team/scripts/python/guru_team_trellis.py`
  - `.trellis/guru-team/extension.json`
- Package installed copies 的精确集合为下列 5 个 root 各自的
  `interface.json`、`references/contract.md`、
  `schemas/task-commit-plan.schema.json`、`examples/task-commit-plan.json`、
  `tests/test_contract.py`：
  - `.trellis/guru-team/skills/packages/guru-create-task-commit/`
  - `.agents/skills/guru-create-task-commit/`
  - `.claude/skills/guru-create-task-commit/`
  - `.codex/skills/guru-create-task-commit/`
  - `.cursor/skills/guru-create-task-commit/`
- Durable docs 精确集合见上一节；task-local 本轮只修改本
  `implementation-handoff.md`。`SKILL.md`、package wrappers、registry、platform
  continue entries、preset overlay 与 installer source 均未修改。

### Round 6 分发、验证、安全与部署

- Canonical runtime SHA-256：
  `e2d67f06ff22444acc3e9e81e11ca2f8c11a7668d06c9379302ee76cdb7735e2`；
  canonical/dogfood runtime byte-equal。Canonical/dogfood workflow byte-equal。
- Canonical package interface SHA-256：
  `6b4c75dbe33d21e5bd65ffb22def5e213341d9cc3fe3caf6986d5871119d2516`；
  package tree digest：
  `750b086748f1d52d6a907dd5442cbabf2536958ff1c416d5fc0198414b7e0b36`。
  Canonical 到 5 个 installed roots 的 40 个 file comparisons 全部 byte-equal。
- `TaskCommitCandidateExecutorTest`：22/22，包含 7-state operation table、真实
  CHERRY_PICK_HEAD、真实 A/B/C gitlink 和 uninitialized/dirty/unborn probes；原 18 个
  ordinary path/hook/result 回归继续通过。
- Canonical 加 5 个 installed/shared/platform package roots：各 4/4，共 24/24；六份
  test bytes SHA-256 均为
  `d80452be80b981bb9933c1a1b936edf0bf7c3ab43b705fde0ad1baa867b2b2a3`。
- Full package/runtime/preset suite：500/500，93.116s，`OK`。
- `TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1
  verify-throwaway-install.sh` exit 0：覆盖 public discovery + local unpublished
  sample、fresh workflow/preset install、initial/finding-fix commit、old-plan reject、
  `trellis update --force`、workflow reapply、preset reapply、source/installed、drift、
  两次 installed closeout smoke 与 recursive sidecar scan。
- 首次 dogfood apply 按 managed-hash 合同生成 26 个 `.bak`；逐个与起始 HEAD 对应
  tracked blob byte-compare 全部相等后清理，并从上一份 valid HEAD provenance 重新执行
  installer。最终 apply：`updated_managed=[]`、`managed_backups=[]`、43 managed files，
  source/installed passed，conflict/removal/sidecar 均为 0；dogfood overlay drift passed，
  recursive `.new/.bak=0`。
- Python compile、相关 Bash syntax、全部 JSON parse、`git diff --check`、phase
  2.2/3.4/3.5 context parsing、workspace boundary、planning approval、task validate、
  staged-empty 与 HEAD-unchanged 全部通过。
- Non-task 新增行 high-confidence private key/token/机器用户绝对路径命中均为 0；
  public artifact 不保存 submodule 文件内容、operation marker 内容或本机绝对路径。
- Deployment path scan 为 0：未修改 GitHub Actions、Dockerfile/Compose、Kubernetes/
  Kustomize、Helm/chart、database migration 或 Makefile；无需应用部署、容器发布、配置
  变更或数据迁移。
- Remote exact feature-ref marketplace verifier 继续按合同 pending；只能在 reviewed
  content push 后由 `trellis-finish-work` 执行，本轮不冒充 publish evidence。

### Round 6 后续 trellis-check focus

1. Fresh Phase 2 检查代理必须独立复核 F-06-01/02/03、22 个真实 Git tests、500-test
   full suite、Docs SSOT、schema 1.0 non-gitlink compatibility、installer recovery、
   throwaway/update/reapply、security/deployment 与 workspace hygiene；本实现代理未记录
   或验证新的 `phase2-check.json`。
2. Phase 2 通过后必须创建新的 task commit sequence，绑定 fresh Phase 2 digest、当前
   pre-commit HEAD、完整 dirty snapshot 与独立 commit 授权；不得复用 sequence 001-005。
3. Commit 后由 Round 6 finding owner `trellis_final_review_122_02` 仅执行 closure review；
   findings 清零后仍须派发此前未参与任何 review round 的 fresh
   `最终放行审查代理` 完整审查 `origin/main...HEAD`。

## Round 7 PHASE2-R6-01 修复交接（2026-07-14）

### 身份、边界与基线

- 逻辑角色：`实现代理`；技术身份：`trellis_implement_122_round7_fix`；平台昵称：
  `Implement-Agent-122-Round7-Fix`。
- 固定 worktree：
  `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/122-guru-create-task-commit`。
- 实现前后 code HEAD 均为
  `163e64168d5d9783c32665da92aebbb4397564a3`；未 stage、commit、push、创建 PR、
  调用 finish-work、运行 task commit executor 或运行 Phase 2 / Branch Review recorder。
- Source checkout `/Users/wumengye/Documents/GoProjects/guru-trellis` 保持 clean，
  HEAD 为 `6b9495a17dc953c7a54c105e39c23a786edcd8a7`。
- Workspace boundary、schema 1.2 planning approval 与 task validation 均通过；未修改
  `prd.md`、`design.md`、`implement.md`、assignment/review/gate/Phase 2 recorder、旧 raw
  report、旧 task commit plan 或 issue ledger。

### 根因与 exact-index 修复

- `PHASE2-R6-01` 的根因是 executor 入口
  `validate_task_commit_candidate()` 已把 artifact 的 reviewed gitlink B 与 worktree B
  比较，但返回后到 `git add` 之间仍有可达窗口。旧实现让 `git add` 从当时的可变
  submodule worktree 重新读取 OID，stage 后只比较 path set，再把已含 C 的 index tree
  作为 expected tree，因此未经审查的 C 可以进入 commit 并返回 `committed`。
- Canonical runtime 现在从同一个 `dirty_snapshot.entries[]` 提取非删除 mode `160000`
  的 `path -> gitlink_head`，没有建立第二个 artifact parser。Executor entry validation
  完成后、任何 stage 副作用前再次读取每个 exact submodule worktree identity；B 已变为
  C、uninitialized、dirty、unborn 或 root-mismatched 时立即以 exit code 2 / blocked
  停止，尚未改变 index 或 candidate。
- 非删除 gitlink 被从普通 `git add` 集合剔除。Executor 使用
  `git update-index --add --cacheinfo 160000 <artifact-gitlink-head> <exact-path>` 把 reviewed
  B 直接写入 exact index，再要求 index identity 精确等于 `(B, 160000)`，并重读 worktree
  HEAD。紧邻 `git commit` 前再次检查 operation state、index OID 和 worktree identity。
  因此更晚的 worktree 竞争也不能把 C 写入 index/commit；expected tree 只能从 artifact
  绑定的 B 构造。
- Deliberate gitlink delete 不具有非删除 `gitlink_head` authority，继续走原 literal
  delete staging；普通文件、symlink、delete、rename、pathspec/Unicode 和已 staged path
  继续复用原 executor 路径。Schema 1.0 的 ordinary legacy plan 仍不要求 gitlink-only
  fields。
- Scripts 仍只校验/执行 objective identity。Scope、AI Review、authorization、route 与
  human confirmation owner 保留在 Markdown package；没有把语义判断写入 Python。

### 永久真实 A/B/C 回归

- `test_gitlink_switch_after_executor_entry_blocks_before_stage_and_never_indexes_c`
  创建真实 superproject/submodule A/B/C history。Superproject index 为 A，candidate
  snapshot/reviewed gitlink 为 B，并先显式证明 candidate validation `errors=[]`。
- 回归在 executor 自己的 entry validation 读取 B 之后、pre-stage 第二次 identity
  读取前受控 checkout C；恰好两次 identity 读取后命中
  `worktree HEAD no longer matches the reviewed gitlink_head`。
- Blocked 断言：HEAD 不变；完整 `git ls-files --stage -z` bytes 不变；gitlink index
  仍为 A 且绝不为 C；candidate bytes 不变且仍为 planned；ordinary operation state
  不变；没有 commit。
- 同一回归随后 checkout 回 B，并复用同一未变 plan 执行真实 executor。结果为
  `committed`，真实 commit tree 的 `deps/dependency` 精确为 `(B, 160000)` 且不为 C，
  证明正向路径也消费 artifact OID，而不是只增加一个重复 freshness check。
- 完整 `TaskCommitCandidateExecutorTest` 为 23/23；原 22 个 operation marker、真实
  cherry-pick、gitlink stale/uninitialized/dirty/unborn、ordinary path、hook、tree/result
  matrix 回归继续通过。

### Round 7 Docs SSOT

- Strategy 继续为 `ssot_first`。Runtime/test 编辑前先更新长期 owner：
  `README.md`、三份 requirements 文档、workflow README、
  `.trellis/spec/workflow/{workflow-contract.md,companion-scripts.md,data-contracts.md,skill-package-contract.md,quality-guidelines.md}`
  与 canonical package contract/interface/schema/example。
- Durable contract 现在统一声明：`gitlink_head` 同时是 snapshot freshness identity 和
  non-deleted mode `160000` exact index OID authority；pre-stage revalidation 负责在指定
  窗口无副作用阻断，artifact-to-index binding 负责让后续竞争不能把 C 写入 index。
- Public schema id 与 `schema_version=1.0` 不变；`gitlink_head.description` 只明确既有
  conditional field 的 executor authority，不要求普通 legacy entry 新增字段。Example
  与 plan digest、interface objective scope、package test 已同步。
- `.trellis/spec/preset/{installer.md,overlay-guidelines.md}`、
  `.trellis/spec/docs/public-docs.md`、`trellis/presets/guru-team/README.md`、canonical/
  dogfood workflow 与 platform overlays 已复核但无需改字节：本轮未改变 installer
  算法、managed path、公共安装命令、workflow phase/marker/route 或 platform entry。
- 本节、Round 6 raw report、真实临时 submodule SHA、单次命令输出、测试耗时和
  `.bak` remediation 过程仅属于 task history，不进入公共 package。

### 精确修改与分发

- Canonical runtime/test：
  `trellis/workflows/guru-team/scripts/python/{guru_team_trellis.py,test_guru_team_trellis.py}`。
- Canonical package：`interface.json`、`references/contract.md`、
  `schemas/task-commit-plan.schema.json`、`examples/task-commit-plan.json`、
  `tests/test_contract.py`。
- Durable docs：顶层 README、三份 requirements、workflow README 与五份 workflow
  specs（见上一节）。
- Controlled dogfood：`.trellis/guru-team/scripts/python/guru_team_trellis.py`、
  `.trellis/guru-team/extension.json`，以及下列五个 roots 的同一组五个 package files：
  `.trellis/guru-team/skills/packages/guru-create-task-commit/`、
  `.agents/skills/guru-create-task-commit/`、`.claude/skills/guru-create-task-commit/`、
  `.codex/skills/guru-create-task-commit/`、`.cursor/skills/guru-create-task-commit/`。
- Canonical/dogfood runtime SHA-256 为
  `c52cda4e4a7aad02ae8962603ecc17c40e2cde2e67433a3bfa9abeef8fada1a7`；runtime test
  SHA-256 为 `0b2c250944f561c0f18ba60331b2669d3e32ed478a07d1dff87d307d155c313d`；
  interface SHA-256 为
  `91be13c42c6fc5f0470258a3cd0155a408d2c1e465582fb0e6a6a2bc0052438e`；package tree
  digest 为 `ecfd6fdb2d1a6243a5c4152b3da2c2f8a35b4de9432fb577a49215be0d8b79a0`。
- 首次 apply 生成 1 个 runtime 与 25 个 package known-managed `.bak`。Runtime 备份
  精确等于 Round 6 记录的 `e2d67f...35e2`；五份 interface/test 备份分别等于 Round 6
  的 `6b4c75...2516` / `d80452...2b2a3`，其余相对文件在五个 roots 间 hash 完全一致。
  核实后按 installer remediation 清理 sidecar、从 canonical 重建 installed manifest；
  最终幂等 apply 为 `updated_managed=[]`、`managed_backups=[]`。

### 验证、安全与部署

- Final targeted：`TaskCommitCandidateExecutorTest` 23/23，16.682s，`OK`；canonical
  package 加五个 installed/shared/platform roots 各 4/4，共 24/24，全部 `OK`。
- Final full package/runtime/preset suite：501/501，135.878s，`OK`。普通文件、symlink、
  delete、rename、literal pathspec/Unicode、legacy plan、deliberate gitlink delete、
  hook/tree/result matrix、installer/closeout 回归全部保留。
- Clean throwaway：`TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1
  verify-throwaway-install.sh` exit 0；覆盖公开 marketplace discovery + local unpublished
  canonical sample、fresh workflow/preset install、initial/finding-fix task commit、old-plan
  reject、`trellis update --force`、workflow preview/switch/reapply、preset reapply、
  source/installed validators、dogfood drift、update 前后两次 installed closeout smoke 与
  recursive sidecar scan。该结果不冒充 remote exact feature-ref evidence。
- Source/installed validators passed：reserved=1、active=1、invoke=1、exit=3；Claude/
  Codex/Cursor，managed files=43，conflict/removal/sidecar 均为 0。Canonical runtime 和
  五组 package files 与 installed copies byte-equal；dogfood overlay drift passed。
- Workspace boundary、planning approval、task validate、phase 2.2/3.4/3.5 parsing、
  canonical/dogfood Python compile、相关 Bash syntax、全部 changed JSON parse、
  `git diff --check` 与 example digest/schema contract 均通过。
- Public non-task added-line high-confidence scan：private key、GitHub/AWS token、
  credential URL 与机器用户绝对路径命中均为 0。Runtime/artifact 不记录 submodule
  内容、Git operation marker 内容或本机绝对路径。
- Deployment path scan 为 0：未修改 GitHub Actions、Dockerfile/Compose、Kubernetes/
  Kustomize、Helm/chart、database migration 或 Makefile；无需应用部署、容器发布、配置
  变更或数据迁移。
- Final pre-handoff hygiene：worktree HEAD 保持 `163e641`，staging=0，recursive
  `.new/.bak=0`，source checkout clean。Remote exact feature-ref verifier 继续按合同
  pending，只能在 reviewed content push 后由 `trellis-finish-work` 执行。

### 后续独立检查 focus

1. Fresh Phase 2 checker 必须独立复核 `PHASE2-R6-01`：entry validation 后/pre-stage
   B-to-C test 的无副作用 blocked 状态，以及正向真实 commit tree 只能为 artifact B。
2. Checker 还需复核 schema 1.0 ordinary/deletion compatibility、23/23、24/24、501/501、
   throwaway/update/reapply、manifest/sidecar、Docs SSOT、安全/部署和 workspace hygiene；
   本实现代理不写入或 record `phase2-check.json`，也不判定 `F-06-02` 已关闭。
3. Fresh Phase 2 通过后必须创建新的 task commit sequence，绑定 fresh Phase 2 digest、
   当前 pre-commit HEAD、完整 dirty snapshot 与独立授权；不得复用 sequence 001-005。
4. Commit 后由 finding owner `trellis_final_review_122_02` 仅执行 closure；全部 finding
   关闭后仍须 fresh `最终放行审查代理` 完整审查当前 `origin/main...HEAD`。

实现侧 blocker：无。

## Round 8 实现交接：关闭 PHASE2-R7-01 exact-index transaction finding

### 边界与结论

- 目标仅为 Round 7 Phase 2 finding `PHASE2-R7-01/P1`：ordinary path、candidate
  self、partial staging、hook 与 publish failure 必须共享 artifact-to-exact-index
  authority 和可恢复事务，禁止把验证后的可变 worktree C 提交进 commit。
- 工作目录保持 task worktree
  `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/122-guru-create-task-commit`；
  实现期间 `HEAD` 保持
  `163e64168d5d9783c32665da92aebbb4397564a3`，source checkout 保持
  `6b9495a17dc953c7a54c105e39c23a786edcd8a7` 且 clean。
- 本轮未运行 `record-phase2-check.sh`、`review-branch.sh` 或 task commit executor，
  未 stage、commit、push、创建 PR 或调用 `trellis-finish-work`。

### 实现与公共合同

- Ordinary non-delete 以 artifact `worktree_sha256 + mode` 为 authority；executor
  使用 `git hash-object -w` 持久化 exact blob，再以
  `git update-index --cacheinfo` 写 isolated index，不再用 live `git add` 重新选择内容。
- Delete 与 rename source 以 artifact-authorized absence 为 authority；executor 用
  exact `update-index --force-remove` 写 isolated index。Gitlink 保留
  `gitlink_head + mode 160000` authority，并在 publication 前重新验证 worktree HEAD。
- Candidate self 只使用第一次 schema/semantic validation 得到的 in-memory plan，按
  deterministic JSON bytes 生成 planned blob；executor 不建立第二 parser，raw bytes
  在 validation 后发生变化也不能成为 authority。
- Staging、hooks 与 `git commit` 在 isolated index、detached transaction HEAD 中运行，
  共享真实 object/config/hook store，但不直接写 live branch、live index 或 candidate。
  Parent、message、path set、tree/blob/mode、worktree、candidate、Git operation state 与
  live-index preimage 全部在真实 ref publication 前验证。
- Publication 持有 live index lock，预写 final index/result，使用 conditional
  `update-ref` 发布真实 branch；index 或 candidate publication 失败时 conditional rollback
  ref，并恢复 exact index/candidate preimage后再返回 structured blocked evidence。
  失败不把 candidate 从 `planned` 改写为 `blocked`；schema 只保留 legacy blocked rows
  的历史验证兼容性。
- Package contract 将不准确的 “validates its blocked facts in memory” 收紧为
  “returns structured blocked command evidence”，与 runtime 的 `WorkflowError.payload`
  和 candidate-byte preservation 一致。
- `run_stdout` 仅在 `env` 非空时把该关键字传给 `run`；`env=None` 保持既有
  `run(cmd, cwd=cwd)` 调用签名，关闭旧 closeout mocks 的 56 个同根因 `TypeError`，
  同时保留 isolated transaction 的显式 environment 支持。

### 永久回归矩阵

- 普通 tracked file validation B 后 worktree B→C：blocked，C 不进入 index/commit。
- Symlink target B→C：blocked，artifact symlink blob/mode 不被 C 替换。
- Delete 后 recreate C：blocked，artifact-authorized absence 不被 C 替换。
- Rename destination B→C：blocked，source absence 与 destination B 均保持 exact。
- Multiple paths 中第二条 B→C：整个 invocation blocked，不发生 partial publish。
- Candidate raw mutation：validated in-memory plan 仍是唯一 authority，raw C 被拒绝。
- 入场 index A、worktree B→C：失败恢复 exact live-index A，不把 B/C 留在 live index。
- Partial isolated-index write、rejecting hook、mutating hook：真实 HEAD/index/candidate
  保持 entry preimage，isolated commit/object 不获得 publication authority。
- Index publication failure：已 conditional advance 的 ref 回滚，index/candidate 恢复；
  回归同时证明成功路径的 ref/tree/index/result 四者一致。
- Round 6 的 7-state Git operation fail-closed 与 gitlink B→C exact binding 回归继续保留。

### SSOT、分发与 sidecar remediation

- `ssot_first` 已完成：五份 workflow specs、顶层/requirements/workflow README、canonical
  runtime/test、canonical package interface/schema/example/contract/test 已同步；task history
  只保留本轮验证、临时 throwaway 和 `.bak` 核对证据。
- Canonical/dogfood runtime SHA-256：
  `402b752e4f1e5516ac35c5ec5f2d57dc59ae9485035d81c2438805082dea93b5`。
  Package interface/contract/schema/example/test SHA-256 分别为
  `51bb90547603a7701e7b7765359847e6828b43c3af1445041c0eadd216c8e34f`、
  `a79725bc23c1191b02f42bd59a27ec3450d7e15f10e2b03dc7c11eac90b731bd`、
  `5f23117f9c00788e49d35d880f6f11fa88fc012a906230a9b5da6c2ffb63f993`、
  `ba7085b0f602f5105fbec80b15eb2620438c23c25820985090c6cd5f8a777fd9`、
  `b25258d511fc2acd71e8a19be719aafed3645e477159ea9c5ba2bb3cf4d8a949`；
  package tree digest 为
  `9fbe097a224202133cfb33b55b119431cc22e7d2b76732661261a22a7037e08c`。
- Compatibility apply 生成的单个 runtime `.bak` 精确等于同步前 installed runtime
  `4ee647801e517be94833e22303f1e01ca67c9e5e7900b2a228b8d0ae79156ccd`；
  contract 收紧产生的五个 `.bak` 均精确等于旧 contract
  `4ac1c75b736a8eab5718333bf1cf18bca5a8f07a506b77e5b43e8ee4c3d1ef9e`。
  核实后清理 sidecars，并从 canonical-equal 43-file installed tree 重建
  `.trellis/guru-team/extension.json`；最终 `status=ok`、conflict/removal/sidecar 均为 0，
  幂等 apply 为 `updated_managed=[]`、`managed_backups=[]`。

### 最终验证

- `TaskCommitCandidateExecutorTest`：32/32，27.817s，`OK`。
- Canonical package 加 `.trellis`、shared、Claude、Codex、Cursor 五 roots：每组 4/4，
  合计 24/24，全部 `OK`。
- 单次完整 canonical package/runtime/preset suite：514/514，146.886s，`OK`；此前
  56 个 `fake_external_run(... env=...)` error 全部消失。
- Clean throwaway：公开 marketplace discovery + local unpublished canonical sample、fresh
  workflow/preset install、initial/finding-fix task commit、old-plan reject、
  `trellis update --force`、workflow preview/switch/reapply、preset reapply、update 前后两次
  installed closeout smoke 与 recursive sidecar scan 全部 exit 0。
- Source/installed validators passed：reserved=1、active=1、invoke=1、exit=3；
  selected platforms 为 Claude/Codex/Cursor，managed files=43，conflict/removal/sidecar=0。
  Canonical/runtime 与五组 package files byte-equal；dogfood overlay drift passed。
- Workspace boundary、planning approval、task validate、phase index/2.2/3.4/3.5 parsing、
  canonical/dogfood Python compile、Bash syntax、全部 changed JSON parse、
  `git diff --check` 均通过。
- Public non-task added-line high-confidence scan对 private key、GitHub/AWS token、
  credential URL 与机器用户绝对路径均为 0 命中。Deployment path scan 为 0：未修改
  GitHub Actions、Dockerfile/Compose、Kubernetes/Kustomize、Helm/chart、database
  migration 或 Makefile；无需部署、容器、配置或数据迁移。
- Remote exact feature-ref marketplace verification 仍按合同 pending；当前 branch 未 push，
  只能在 reviewed content push 后由 `trellis-finish-work` 执行，local throwaway 不冒充该证据。

### 后续独立检查 focus

1. Fresh Phase 2 checker 必须独立攻击普通文件/symlink/delete/rename/multi/candidate-self 的
   B→C authority、entry staged A 恢复、partial isolated write、rejecting/mutating hook、
   index publication rollback 与成功 ref/tree/index/result consistency。
2. Checker 必须覆盖完整 R1-R10、AC1-14、Round 6 git operation/gitlink/workflow closure、
   32/32、24/24、514/514、throwaway/update/reapply/closeout、source/installed/drift、
   Docs SSOT、安全、部署与 workspace hygiene；本实现代理不记录 `phase2-check.json`。
3. Phase 2 通过后必须创建 sequence 006 或更高的新 candidate，绑定 fresh Phase 2 digest、
   当前 pre-commit HEAD 与完整 dirty snapshot；不得复用 sequence 001-005。

Round 8 实现侧 blocker：无。

## Round 9 实现交接：收敛 publication linearization 与 assignment provenance recovery

### 边界与结论

- 本轮关闭 `PHASE2-R8-01` 与 `PHASE2-R8-02`。前者把 ref/candidate/index
  publication 收敛为持锁、可证明 ownership 的事务；后者为 assignment ledger 增加
  digest-bound provenance correction 与 failed-to-termination recovery edge。
- 工作目录保持 task worktree
  `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/122-guru-create-task-commit`；
  最终 `HEAD` 保持 `163e64168d5d9783c32665da92aebbb4397564a3`，source checkout
  保持 `6b9495a17dc953c7a54c105e39c23a786edcd8a7` 且 clean。
- 本实现代理未运行 `record-agent-assignment.sh`、`record-phase2-check.sh`、
  `review-branch.sh`、task commit executor 或 `trellis-finish-work`，未 stage、commit、
  push 或创建 PR；live `agent-assignment.json`、Phase 2 artifacts、review、plan、ledger 与
  planning docs 未由本轮修改。

### `PHASE2-R8-01` publication 事务

- Executor entry 持有真实 `index.lock`；isolated commit validation 与 transaction temp
  清理必须在 publication 前完成。Candidate guard 先预写 candidate result/final index，
  branch ref 只通过 conditional CAS 前进。
- Ref CAS 后立即获取并校验 loose-ref `.lock` guard；candidate result 在 guard 下发布，
  live index 最后 rename，且该 rename 是 success linearization point。其后不得再发生
  fallible check 或 publication write。
- Candidate restore 同时要求 candidate guard 与 executor-published inode/content identity；
  ref rollback 先释放 owned ref guard，再执行 conditional CAS。Live index 在最后 rename
  前始终保持 entry preimage。
- ownership 丢失时必须保留 concurrent candidate/ref/index state，并报告 incomplete
  rollback；不得覆盖并发状态，也不得声称 exact restoration。
- 永久 transaction matrix 为 36/36，新增覆盖 candidate publication failure 与并发真实
  `git add`、success-window 并发 `git add`、并发 candidate writer、CAS 前及 guarded
  success window 内并发 ref、index publication failure/ref rollback、最终
  ref/tree/index/result equality，以及 linearization 后无 index check。

### `PHASE2-R8-02` assignment provenance 合同

- `agent-assignment.json` schema 1.2 新增 `event_corrections[]`，当前唯一 kind 为
  `invalidate-provenance`。Correction 必须绑定 target event digest、保持 same-agent，且只能
  指向 progress/status-request；terminal/completed evidence 不得 invalidated。
- 新增 `recovery_links[]`，当前唯一 kind 为 `failed-to-termination`。Edge 必须以 digest
  绑定同一 agent 的 earlier `failed` 与 later manual/platform
  `terminated-unfinished`；effective progress/status projection 排除已验证 invalidated event，
  raw history 保持不变。
- Recovery traversal 通过新 edge 进入既有 `replacement-started` chain，最终仍必须到达真实
  later `completed`。Validator 拒绝 unknown、duplicate、cross-agent、backward/cyclic、
  wrong-kind 与 tampered reference。
- Recorder 新增 `--invalidate-event-id`、`--correction-reason`、
  `--correction-evidence`、`--link-failed-event-id`、`--link-termination-event-id`、
  `--recovery-reason` 与 `--recovery-evidence`。Corrected synthetic ledger 通过 assignment
  与 Phase 2 assignment validation；legacy invalid ledger 继续 fail closed。Assignment/
  liveness targeted suite 为 30/30。

### SSOT、分发与最终哈希

- 五份 workflow specs、顶层 README、三份 requirements、workflow README、canonical
  runtime/test 与 canonical package contract/interface/schema/example/test 已在 runtime 之前
  同步；`.trellis`、shared、Claude、Codex、Cursor 六个 package roots byte-equal。
- Canonical/dogfood runtime SHA-256 为
  `2cfeaf2cc7872957a019d83b39ac75a8264fb46afc442a902803f84b6f4efd03`；runtime test 为
  `c1a46be7c718a04c2606892e0e460d8be7ab974344a75c22deef565556cbdb09`。
- Package `SKILL.md`、interface、contract、schema、example、validator script、executor
  script 与 test SHA-256 依次为
  `4704c22a1a9745a50dec79860a16a7e00298701c1e3d7f123b754d92d4d1f438`、
  `a0bc665967405db46d32303966b2047dd6f7494ba1958bfa3bb8e89fb18c8d10`、
  `57cac032434a9dcd4477994d41fc9fb875a6747be2384ab9adda05106f9c3860`、
  `1816f08de5b455d6287df3af40e2012e56cbf7d7eb5c4955cfcd1165b1357ac3`、
  `ddce6c5811dcb85be2fff7c31c86ab9bbf5480d272494a40c7b0220eb9341747`、
  `9fdc404c9031dc3ab9581307328492ecc068c5c116bef49c77233af86845b831`、
  `7c5f27828f3fbb7ed328b4eaa98a8bc3074e7970431facd18c759f1d649f0669`、
  `79ea6da6c23f59790a67c8ae748e73d1cd2d9ce1dcbf7fe0ded106c5fb9726cd`；
  package tree digest 为
  `54a6459848b64b5566b4ca997376cffd6e812891454dbe557ce2fe78a9566645`。
- Canonical extension manifest 与 installed manifest SHA-256 分别为
  `ecdb32785a87f5560b2dd97a63f3d0c6ac5e266bbf0d226c56f8e3237a1aacde`、
  `f7586c3a6da0e5806dc2d0e3493b8f3b0a02da91ded1081f63e3e18b03d53c67`。

### 最终验证、安全与部署

- 六个 package roots 各 4/4，合计 24/24；单次 canonical package/runtime/preset suite
  为 522/522，152.779s，`OK`。
- `TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1 verify-throwaway-install.sh` exit 0，覆盖
  public marketplace discovery + local unpublished canonical sample、fresh workflow/preset
  install、initial/finding-fix task commit、old-plan reject、`trellis update --force`、
  workflow preview/switch/reapply、preset reapply、source/installed validators、dogfood drift、
  update 前后两次 installed closeout 与 recursive sidecar scan。
- Final idempotent `apply.sh --repo . --all-platforms --json` 为
  `updated_managed=[]`、`managed_backups=[]`。Source/installed validator 为
  reserved=1、active=1、invoke=1、exit=3；Claude/Codex/Cursor managed files=43，
  conflict/removal/sidecar=0；dogfood drift 与六 roots exact compare 通过。
- Workspace boundary、planning approval、task validate、phase index/2.2/3.4/3.5 parsing、
  canonical/dogfood Python compile、相关 Bash syntax、全部 changed JSON parse、
  `git diff --check` 均通过。Public non-task added-line high-confidence sensitive scan 与
  deployment path scan 均为 0。
- Final hygiene：staging=0、recursive `.new/.bak=0`、source checkout clean。Remote exact
  feature-ref marketplace verification 仍按合同 pending，只能在 reviewed content push 后由
  `trellis-finish-work` 执行；local throwaway 不冒充该证据。

### 主会话 recorder 与后续检查

1. 主会话必须逐个复核并记录 `evt-0132-2f8589a51e`、
   `evt-0135-1a8e9bee22`、`evt-0136-d400b5a1f4` 的 provenance invalidation；每次调用必须
   写入 main-session 自己的 correction judgment/evidence，不得复用实现代理断言冒充判断。
2. 主会话必须复核后记录 `evt-0117-fa1006d803` -> `evt-0118-cd228c71fd` 的
   `failed-to-termination` recovery edge，再运行 `check-agent-assignment.sh`。既有
   `evt-0115` -> resume `evt-0116` -> failed `evt-0117` 将由该 edge 到 termination
   `evt-0118`，再经 replacement `evt-0120` 到 completed `evt-0128`，从而关闭两个 failed
   rows。
3. Fresh Phase 2 checker 必须独立复核 36/36 transaction matrix、30/30 assignment/liveness
   matrix、24/24 package roots、522/522 full suite、throwaway/update/reapply/closeout、
   source/installed/drift、Docs SSOT、安全、部署与 workspace hygiene；本实现代理不记录或
   判定 fresh `phase2-check.json`。
4. Fresh Phase 2 通过后必须创建 sequence 006 或更高的新 candidate，绑定 fresh Phase 2
   digest、当前 pre-commit HEAD、完整 dirty snapshot 与独立授权；不得复用 sequence
   001-005。

Round 9 实现侧 blocker：无。

## Round 10 实现交接：关闭 `PHASE2-R9-01` candidate publication TOCTOU

### 边界与结论

- 本轮唯一目标为 `PHASE2-R9-01/P1`。实现没有继续交换 candidate/index publish
  顺序，也没有声称 OS/Git 提供跨 ref/index/candidate 的绝对同时原子性；事务改用可实现
  的 final candidate identity-read 线性化合同。
- 固定 worktree 为
  `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/122-guru-create-task-commit`；
  实现前后 `HEAD` 均为
  `163e64168d5d9783c32665da92aebbb4397564a3`，staging 始终为空。
- Source checkout `/Users/wumengye/Documents/GoProjects/guru-trellis` 保持 clean，
  `HEAD=6b9495a17dc953c7a54c105e39c23a786edcd8a7`。
- 本实现代理未运行 recorder、task commit executor、review/publish/finish-work，未
  stage、commit、push、创建 PR、reset、revert、stash、amend、rebase 或 force；未修改
  live `agent-assignment.json`、Phase 2/review reports、review artifacts、task plans、
  ledger 或 planning docs。本 task-local 只追加本 handoff 章节。

### 线性化与 rollback 实现

- 真实 Git `index.lock` 现在只作为 sentinel：executor 从入口持有其 fd/path 到
  transaction cleanup，绝不再把该 lock file rename 成 live index。Final index bytes
  写入同目录独立 `.index.*.publication` temp，再在 sentinel 仍存在时
  `os.replace()` 到 live index，真实 `git add` 在整个 publish/rollback 窗口继续被阻断。
- Candidate result 发布、conditional branch ref 前进并获得 loose-ref guard、final index
  发布后，runtime 先验证 open index/ref guard inode、真实 ref SHA、live-index
  inode/content 和 candidate guard。随后对 candidate committed result 做最后一次
  inode/content identity read；该 read 是唯一 success linearization point。
- 若旁路 atomic/editor writer 在最终 read 前写 C，read 必须失败。Executor 在
  `index.lock` sentinel 仍存在时只恢复自己拥有的 live-index preimage，释放 owned ref
  guard 后以 compare-and-swap 回滚 ref；candidate identity ownership 已丢失，因此 C
  原样保留并返回 `blocked`，绝不把 planned/result preimage 覆盖回 C。
- 若 writer 在最终 read 得到 exact identity 后写 C，该写入按线性化顺序是 later
  operation。Executor 不再执行任何会把成功改成 `blocked` 的检查或 publication write，
  只 best-effort 清理 ref/candidate/index guards 与 temps 后返回预构造 payload；C 保留。
- Success payload 在 publication 前完成构造，新增
  `candidate_result_sha256`。Immutable commit tree 中 candidate path 的 planned blob 与
  returned committed-result digest 是先前 transaction 的 authority；mutable candidate
  只要求在线性化点 exact，不宣称后续任意时刻永久相等。
- Candidate guard 仍是所有项目 companion candidate writer 的 mandatory protocol；最终
  identity read 只补足不遵守 guard 的 atomic/editor writer 排序语义。

### 永久回归与兼容性

- `test_candidate_writer_before_final_identity_read_rolls_back_and_is_preserved`
  在旧 finding 使用的 `task_commit_publish_locked_index` 入口正常写 C 并正常返回，不靠
  writer 人为抛错。测试证明 candidate/index guards 均存在、真实 `git add` 非零、final
  read 检出 C、real ref 与 live index 回到 entry preimage、C 被保留，所有 guard/temp
  清理。
- `test_success_window_blocks_git_writers_and_linearizes_at_final_candidate_read`
  在 final candidate identity read 已读取 exact result 后立即写 C，证明 executor 仍
  `committed`、C 保留、真实 ref/commit tree/live index 一致、candidate planned blob 在
  immutable commit tree 中真实存在、`candidate_result_sha256` 与被读取 committed result
  bytes 一致；线性化后故意让旧 index preimage checker 抛错也证明该 checker 不再调用。
- 两条回归替换旧 success-window 与 concurrent-candidate test method，没有增加 suite
  数量；transaction matrix 保持 36/36。Ordinary tracked、symlink、delete、rename、
  multiple path、candidate self、entry-index A/worktree B、Unicode/pathspec、gitlink、
  operation、hook、partial cache、legacy result/schema 与 ref contention 回归全部继续通过。

### Docs SSOT 与分发

- Strategy 继续为 `ssot_first`。Runtime edit 前先更新 durable owners：顶层 README、
  三份 requirements、workflow README、
  `.trellis/spec/workflow/{workflow-contract.md,companion-scripts.md,data-contracts.md,skill-package-contract.md,quality-guidelines.md}`
  与 canonical package contract。
- Durable contract 统一声明 index sentinel、独立 final-index temp、final candidate
  identity-read linearization、pre-read C rollback/preserve、post-read C later-op、
  immutable commit blob/result digest authority 和 post-read cleanup-only 边界。
- Canonical package interface/schema/example/test 与 runtime/tests 随后同步；preset apply
  分发到 `.trellis`、shared、Claude、Codex、Cursor 五个 installed roots并重建 manifest。
  `.trellis/spec/preset/{installer.md,overlay-guidelines.md}`、
  `.trellis/spec/docs/public-docs.md`、preset README、workflow route 与 overlays 经复核
  无需改字节：本轮没有改变 managed path、installer 算法、平台 route、公共安装命令或
  workflow marker。
- 首轮 apply 产生 1 个 runtime 与 25 个 package known-managed `.bak`；它们分别精确
  等于 apply 前 installed runtime/package hashes。最终 payload-prebuild 收紧又产生 1 个
  runtime `.bak`，精确等于同步前 installed runtime
  `053955dab38ab55dd887fd04526a111f022ab4693786af08d0c7b7239558711d`。
  全部逐项确认后清理，并从 canonical 重建 installed manifest；最终幂等 apply 为
  `updated_managed=[]`、`managed_backups=[]`，43 managed files，0
  conflict/removal/sidecar。

### 最终哈希与验证

- Canonical/dogfood runtime SHA-256：
  `21f09708e9f29fe0924df78f8faa5964f1ea0132f46f4dc748196d3df0603379`；
  runtime test SHA-256：
  `12ad21f95d2c31fddc36222c3d8058e8fd012d55dc80a3904a3dceb578d3624c`。
- Package interface/contract/schema/example/test SHA-256 依次为
  `48f0b6a5e345c816c7e1bbccdebb4d16b1459ed0a986c7354a93e05a1285d05a`、
  `083fe3ba9e7a54517a572b5a07f5b9eaa9594d9e97d7b68a0b391b3aa3b83cae`、
  `b62fdf2753dfccfacf635acb20af8274b26acac97cba3d5a6519e24f261848d5`、
  `115abe1ec5a12658d3de4d2477054c60da2e25fc6bbc8878b4c9d7545a9eb5f2`、
  `beea6a5eb307b7e1184f3bad77de51d8aa09afbfebb45220f9600d87abadf82c`；
  package tree digest 为
  `4c63163e52b72ceb9933d86e24d1b36b7cece5ea6c2bec337650d9b08d13a136`。
- Installed manifest SHA-256：
  `a36a814b14889d7810d9e9ec76379aebcfda1ca602a4c4775ca4a3a3abf02666`；
  canonical extension manifest 未变，为
  `ecdb32785a87f5560b2dd97a63f3d0c6ac5e266bbf0d226c56f8e3237a1aacde`。
- Final transaction 36/36，33.790s，`OK`；assignment/liveness 30/30，1.342s，
  `OK`；canonical 加五个 installed/shared/platform package roots各 4/4，合计
  24/24，`OK`。
- Final canonical package/runtime/preset full suite 522/522，155.056s，`OK`。
- Final clean throwaway exit 0：覆盖 public marketplace discovery + local unpublished
  canonical sample、fresh install、initial/finding-fix task commit、old-plan reject、
  `trellis update --force`、workflow preview/switch/reapply、preset reapply、
  source/installed validation、dogfood drift、update 前后两次 installed closeout、
  archive/ready equality 与 recursive sidecar scan。
- Workspace boundary、schema 1.2 planning approval、task validation、phase
  2.2/3.4/3.5 parsing、live `check-agent-assignment --require-current-head`、changed JSON、
  canonical/installed Python compile、全量相关 Bash syntax、branch/working/cached
  `git diff --check`、source/installed/drift 与 canonical/installed byte equality 均通过。
  Live assignment 为 raw 170 / effective 167、3 corrections、1 recovery link，exit 0。

### 安全、部署与后续门禁

- Public non-task added-line 与 sequence 001-005 plan 高置信 private key、GitHub/AWS/
  Slack token、credential URL、signed credential 与机器用户绝对路径扫描均为 0。
- Branch+dirty path scan 没有 GitHub Actions、Dockerfile/Compose、Kubernetes/
  Kustomize、Helm/chart、database migration 或 Makefile 变更。本轮只改变 Trellis
  workflow/runtime/package/docs/tests，不增加 service、worker、queue、scheduler、runtime
  config 或数据迁移，无需部署资产同步。
- 下一步必须由 fresh Phase 2 checker 独立复核 `PHASE2-R9-01`、完整 current diff 与
  本轮所有验证；本实现代理不写入或判定新的 `phase2-check.json`。
- Remote exact feature-ref marketplace verifier 继续按合同 pending；只能在 reviewed
  content push 后由 `trellis-finish-work` 执行，local throwaway 不冒充该 publish evidence。

Round 10 实现侧 blocker：无。

## Round 11 实现交接：关闭 `F-08-01` copy-source authority bypass（2026-07-14）

### 身份、边界与结论

- 逻辑角色：`实现代理`；技术身份：
  `trellis_implement_122_round11_fix`；平台昵称：
  `Implement-Agent-122-Round11`。
- 固定 worktree：
  `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/122-guru-create-task-commit`；
  实现前后 `HEAD=005c41fa755d4fea2d7c4f2bd8463041ffc7fe32`，base 仍为
  `origin/main=6b9495a17dc953c7a54c105e39c23a786edcd8a7`。
- 唯一 current-scope finding `F-08-01` 已在实现侧关闭：新 snapshot
  producer 显式以 `renamed_from` / `copied_from` 区分 rename 与 copy；只有
  rename source 继承 destination 的 deletion/exact-stage authority。Copy source
  绝不因 relation 自动进入 stage；自身 dirty 时必须作为独立
  snapshot path 分类与受审。
- 保持 schema id/version `guru-task-commit-plan-1.0` / `1.0`。`copied_from`
  是可选 additive field，当前 producer 始终显式输出；旧 ordinary plan 省略
  该字段仍通过 public schema，历史 plan result validity 未被静默改写。
- 本代理未修改 planning docs、assignment、Phase 2/review artifact、旧
  task-commit plans 或 issue ledger；未运行 recorder/gate/task commit executor，未
  stage、commit、push、创建 PR、finish-work 或关闭 issue。

### `ssot_first` 与 Docs SSOT

- Runtime/schema edit 前先修改 durable owners：顶层 `README.md`、三份
  `docs/requirements/` 文档、workflow README，以及
  `.trellis/spec/workflow/{workflow-contract.md,companion-scripts.md,data-contracts.md,skill-package-contract.md,quality-guidelines.md}`。
- Canonical package `references/contract.md` 承载 step-local relation/authority 正文；
  `interface.json`、public schema/example/test 与 runtime/tests 随后承接。Global
  workflow、continue entries 和 platform launchers 仍只路由 stable skill/typed exit，
  没有复制 copy/rename 内部合同。
- Task delta 已合并到 durable owners：`F-08-01` 的 relation 分离、rename-only
  deletion inheritance、copy source 独立分类、schema 1.0 兼容与真实 Git
  回归矩阵已从 task finding 收敛为公共合同。
- Task-history-only 保持在本交接/旧 raw report：代理身份、本机 worktree、
  临时 Git repo、测试耗时、单次 `.bak` 哈希核对与命令输出。这些
  active-task 事实没有进入公共 package。
- `.trellis/spec/preset/{installer.md,overlay-guidelines.md}`、
  `.trellis/spec/docs/public-docs.md`、preset README、workflow route/overlay 和 canonical
  extension version 经复核无需改字节：本轮没有改 managed path、installer
  算法、平台路由、安装命令、workflow marker 或 `0.6.5-guru.5`
  兼容基线。

### 实现、schema 与真实 Git 回归

- `capture_task_commit_snapshot()` 继续消费 NUL-delimited porcelain v1，但现在
  fail closed 拒绝同一 record 同时出现 `R`/`C`；`R` 仅写
  `renamed_from`，`C` 仅写 `copied_from`，ordinary row 两者均为
  `null`。Candidate validator 还拒绝 relation 同时非空、非 repo-relative 或
  self-reference。
- Existing exact-stage 派生逻辑只读 `renamed_from`，index binding 也只对
  rename source 写 exact absence。`copied_from` 只是 provenance，不参与
  expected stage set 或 source deletion。
- 真实 `status.renames=copies` 回归覆盖：
  1. reviewed copy destination + independently staged `unrelated-preserved` source：
     candidate exact paths 不包含 source，executor 在 isolated transaction 前因
     unexpected staged source 阻断，HEAD、完整 index bytes、candidate、source
     worktree bytes 和 source/destination commit-tree identities 精确保持；
  2. copy 配置下 clean source：只提交 destination + candidate self，直接验证
     commit tree 仍保留 source blob/mode；
  3. source 本身也 independently reviewed：真实 C relation 提交 source +
     destination + candidate self，直接验证 source blob 为 reviewed update 而不是
     rename-style deletion。
- 既有 rename destination 测试仍要求 source 删除、destination 保留；
  ordinary path、gitlink、candidate-self、operation state、hook、`index.lock`/
  ref/index/candidate publication/rollback/linearization 测试全部保留。

### 分发、upgrade/update 与开箱验证

- Canonical preset `apply.sh --repo . --all-platforms` 同步 canonical runtime 与
  package 到 `.trellis`、shared、Claude、Codex、Cursor，并重建
  `.trellis/guru-team/extension.json`。最终 package tree digest 为
  `e0ab35c13af921582efde477958abeae78e0cdcde074d7eda64355b0b3076c18`；
  manifest SHA-256 为
  `0e2b51ead574eec2b4aec7ae805b2e2788a079e6197c89a0ed2e0a380c4f80a9`。
- 首轮同步生成 1 个 runtime + 25 个 package known-managed `.bak`，全部
  与开始 HEAD 对应旧 managed bytes SHA-256 一致；后续 contract 文案收紧产生
  5 个中间 backup，均等于前一份 managed contract
  `f77c8aa374e4cdce5fe5134310367d6eaaf083dd34b87de8d67a09b437f28f24`。
  全部逐项核对后清理，从 canonical-equal tree 重建 manifest。最终幂等
  apply：`updated_managed=[]`、`managed_backups=[]`，43 managed files，0
  conflict/removal/sidecar；source/installed validator 和 dogfood drift 通过。
- Clean throwaway exit 0：覆盖 public marketplace discovery + local unpublished
  canonical sample、fresh init/preset、initial/finding-fix 真实 task commit、old-plan
  reject、`trellis update --force`、workflow preview/switch/reapply、preset reapply、
  source/installed/drift、update 前后两次 closeout、archive/ready equality 与
  recursive sidecar。

### 精确资产、哈希与验证

- 本轮可提交实现资产为 44 个公共/dogfood path，加本交接共 45
  个 path：5 份 README/requirements durable docs、5 份 workflow specs、
  canonical package 5 份 changed assets、canonical runtime/test 2 份、installed runtime
  + manifest 2 份、以及 5 个 installed/shared/platform roots 各 5 份 package
  copy（共 25）。本轮不使用 `git add -A` / `git add .`，实现代理
  未 stage 任何路径。
- Canonical/dogfood runtime SHA-256：
  `383ccbb80b73dbfbb6bae8a6b0dad9b0559a3c998cddb29a3dcc13f2e908d252`；
  runtime test SHA-256：
  `b36a286df53ab67bb3638d0b60cd3db2687268fe16a648e6939e35a30228fae7`。
- Package interface/contract/schema/example/test SHA-256 依次为
  `237e2395128aae16748ee5ea1002cd15b9dc4666c9803d17b9eac768a2315152`、
  `d125236e341c5c33cb6d791065f07a8abd5131f04aa2fb634d89f0658adcf35d`、
  `8a7f2dce07f7f4b2723ac9ccae23d41636c362e5daa699c2afaca6fa570514e3`、
  `89a3de2235eed74f1fbbb51d8b7db67fb51c1953ee314e9898dc4c62735c4954`、
  `0f8015a0bf07208bcd06a6221e4b6fff2017afc91031783215da9e7a335780cb`。
- Targeted package + copy/rename 回归 `8/8`；`TaskCommitCandidateExecutorTest`
  `39/39`，32.915s；assignment/liveness `30/30`，1.272s；canonical +
  五个 installed/shared/platform roots `24/24`。
- 精确 full discovery 为 canonical package `4/4` + skill infrastructure `58/58` +
  runtime discovery `427/427` + preset `36/36` = `525/525`；runtime 部分
  144.729s，全部 `OK`。测试数从 Round 10 的 522 增加 3 个真实
  Git copy regression，没有删除旧 case。
- Python compile、相关 Bash syntax、6 份关键 JSON parse、branch/working/cached
  `git diff --check`、phase/2.2/3.4/3.5 context parsing、task validate、workspace
  boundary、schema 1.2 planning approval、canonical/dogfood runtime 与 canonical 到 5
  个 package roots 的 40 次 byte equality 全部通过。首次 JSON loop 误用 zsh
  special `path` 变量导致后续 `python3` 不可见，已使用 `file` 变量
  正确重跑 6/6；该无效 harness 命令不计入通过证据。

### 安全、部署、卫生与后续门禁

- Public non-task added-line 高置信 private key、GitHub/AWS/Slack token、
  credential URL、signed credential 和机器用户绝对路径扫描为 0。公共
  schema/example/package 只保存 repo-relative path/digest/结构化事实。
- Branch+dirty path 没有 GitHub Actions、Dockerfile/Compose、Kubernetes/
  Kustomize、Helm/chart、database migration 或 Makefile 资产。本轮不增加
  service、worker、queue、scheduler、runtime config 或数据迁移，无需部署
  资产同步。
- 收尾时 source checkout 仍 clean，source `HEAD=6b9495a17dc953c7a54c105e39c23a786edcd8a7`；task worktree staging=0，recursive `.new/.bak=0`，task
  candidate/ref/index lock 与 publication/transaction temp=0。
- 下一步必须由 fresh Phase 2 checker 独立复核 `F-08-01`、完整
  current diff、Docs SSOT、39/30/24/525、throwaway、安装升级、安全部署与
  workspace hygiene。本实现代理不写入或判定新的
  `phase2-check.json`。
- Remote exact feature-ref marketplace verifier 继续按合同 pending；只能在
  reviewed content push 后由 `trellis-finish-work` 执行，local throwaway 不冒充
  publish evidence。

Round 11 实现侧 blocker：无。
