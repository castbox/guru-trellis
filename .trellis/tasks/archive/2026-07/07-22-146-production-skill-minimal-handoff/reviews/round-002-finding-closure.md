# Issue #146 Branch Review Round 002 问题闭环审查报告

## 审查身份与结论摘要

- 逻辑角色：问题闭环审查代理
- technical agent：`/root/review_146_final_r1`
- reuse_decision：`reuse-for-closure`
- finding owner round：`001`
- issue：`https://github.com/castbox/guru-trellis/issues/146`
- base：`origin/main` / `7dc67e9aef08ca4928159d7d13db6fdbd40c5d4c`
- prior reviewed HEAD：`e3efc635e36039f0db94a9d24eddad676ad7fe7b`
- reviewed_head：`c945c73e1779f4e62409883bab5e1f6a907e4584`
- closure delta：`e3efc635e36039f0db94a9d24eddad676ad7fe7b..HEAD`，`25` 个路径
- cumulative diff：`origin/main...HEAD`，`2` 个提交、`628` 个路径
- findings_count：`0`
- closure verdict：`passed`

本轮只判断 Round 001 的 P1-F001 与 P2-F002 是否闭环，并检查 finding-fix
commit 同时携带的 R16 normal-path 修正、fresh Phase 2、commit 002、Docs SSOT、
安全与部署边界是否引入新的 current-scope finding。本报告不是最终放行报告；同一
technical agent 仅因其是 finding owner 被复用作 closure reviewer，后续仍须使用全新
final-release reviewer 审查最新完整 `origin/main...HEAD`。

本代理未修改实现、planning、Phase 2、agent assignment、review gate、旧报告或 commit
plan；未运行 recorder/validator，未 commit、push、创建 PR、finish-work 或关闭 issue。
唯一写入是本 raw report。

## 审查范围与输入证据

本轮 fresh 读取并交叉检查：

- Round 001 raw report
  `reviews/round-001-final-release.md`，SHA-256
  `ac1709e74608a11fab1170cc37f1ba9a338ef436e265e72a65353ea1daddae96`，
  `13932` bytes；
- live Issue #146 当前 OPEN 状态与 R17 authority comment
  `https://github.com/castbox/guru-trellis/issues/146#issuecomment-5053205362`；
- R17 proposal/action exact confirmation、`issue-scope-ledger.json`、R1-R17/AC1-AC22
  的 `prd.md`、`design.md`、`implement.md`、contract wording 与 fresh planning approval；
- Round 001 HEAD 到 reviewed HEAD 的完整 25-path finding-fix diff，以及
  `origin/main...HEAD` 累计 628-path diff中与两个 findings、R16、Docs、部署安全有关的
  source/installed/workflow/runtime/tests/task evidence；
- fresh `phase2-check.json`、task commit plan 002 的 planned commit blob、live committed
  sidecar、actual commit tree/path set 与当前 metadata tail。

## Finding 生命周期

### P1-F001：未获 scope-change 授权即修改 #147 production eval adapter

Round 001 状态：`open`，P1。旧 HEAD 已包含三个 production Skills 的 native owner
staging，但当时五个 accepted-current proposals、live issue authority 与 approved planning
均未授权修改 #147 shared native adapter。

闭环路径选择的是 Round 001 允许的第二条 remediation，即返回 Scope Change Gate，而不是
撤销 adapter：

- 用户 exact confirmation 已绑定 proposal
  `9cb7d74836af661328de1dc5f0e6740840a7a8fbd02e0028a6813a6bde73ebc5`
  与 action
  `82052b7d1f9d04cf49a6ec0b4a3980b71cb6d83e96aef8f796b30acee1fae4ae`。
- Live comment `5053205362` 记录了恢复 `origin/main` adapter 后三个 production corpora
  均正常进入 unsupported owner-staging 分支的 read-only probe，证明仅调整 corpus 无法同时
  保持真实 native/public-wrapper execution。
- Ledger 将该 proposal 记录为
  `scope_change_20260723_production_eval_adapter_owner_staging /
  accepted_current`，并绑定 current live authority、fresh context 与 planning documents。
- Current planning hashes与 ledger 精确一致：
  `prd=96773f0a...`、`design=962a380a...`、`implement=c3d9521f...`；
  planning approval SHA-256 为
  `d0bbefb789805ab0f4f26bd78a75760d1b8ab2412a2fd41b60d4ffbf9b81e335`，
  typed exit 为 `approved`。

最终实现与 R17 界限一致：

- `PRODUCTION_SKILLS` 精确只有
  `guru-approve-task-plan`、`guru-check-task`、`guru-create-task-commit`；
- 三条路径在隔离 fixture 中复用现有 recorder/checker/builder，并进入各自真实 public
  wrapper；actual exit来自 wrapper checked result；
- adapter/native requests均不含 `expected_exit`，runner仍在 actual exit 选择 output
  schema 后独立比较 expected exit；
- finding-fix delta 没有修改 #147 runner、schema、Interface、grader policy、adapter
  protocol或 eval corpora contract；该 delta在 #147 边界只修改 canonical/installed
  `native_adapter.py`，且两份 bytes一致；
- Stage 0 identity、其它 owner dispatch 与 unsupported fallback保持原合同。

独立 normal-path regression：

```text
python3 -m unittest discover -s trellis/skills/guru-team/tests \
  -p test_skill_packages.py \
  -k production_shared_adapter_stages_exact_allowlist_and_real_wrappers
```

结果：`Ran 1 test`，`OK`。测试真实执行三个代表性 production corpora，验证 actual exits、
public wrapper traces、schema/route checks、adapter/native request无 `expected_exit`，并验证
非 allowlist路径仍进入原 unsupported fallback。

闭环结论：`closed`。P1 的问题是缺失 scope authority，不是最终 adapter 行为本身；当前
exact confirmation、live authority、fresh planning/approval、实现边界与回归已完整满足
Round 001 remediation。

### P2-F002：`clarify_scope` target 只有 marker，没有 runtime 路由合同

Round 001 状态：`open`，P2。旧 canonical/dogfood workflow 在 target marker 后直接进入
task activation，没有 AI-readable continuation。

Current canonical `trellis/workflows/guru-team/workflow.md:920-938` 已在 target marker 与
task activation之间明确：

- 只消费 checked `exit_id`、`task_ref`、`proposal_refs`；
- 验证 exact exit/consumer并解析唯一 current task；
- 对 missing、stale、mismatched、multiple、unknown、unmapped输入 fail closed；
- fresh-read live issue authority、task/ledger、planning/approval与全部 proposal refs；
- caller AI 基于 fresh context编写 existing
  `guru-clarify-requirements:active_task_scope_change` 的完整八字段 input；
- 进入 Scope Change Gate并 mandatory invoke active `guru-clarify-requirements` package；
- 禁止第四条 authoring seed、producer DTO扩张和 private-runtime semantic reconstruction。

Dogfood `.trellis/workflow.md` 与 canonical workflow byte-identical。该行为保持 routing-only：
它不代替 clarification Skill 的 semantic judgment、human confirmation或 recorder/checker。

独立 normal-path regression：

```text
python3 -m unittest discover -s trellis/skills/guru-team/tests \
  -p test_skill_packages.py \
  -k task_plan_clarify_scope_router
```

结果：`Ran 2 tests`，`OK`。Source 与 installed/dogfood probes均检查三字段消费、fresh reread、
八字段 authoring、mandatory invocation、fail-closed条件、seed cardinality及 canonical/
dogfood一致性。

闭环结论：`closed`。真实 planning ambiguity 的 `clarify_scope` exit现在有唯一可执行的
workflow continuation，不再依赖 README 推断或 caller猜测。

## R16 修正复核

Finding-fix commit同时修正 task-local context re-entry 在正常 post-commit HEAD 上被误判
`base_head_stale` 的 R16 问题：

- `context_live_base_errors()` 只在 `pre_task` 比较 current HEAD 与 base-sync decision
  HEAD；
- task mode仍验证 selected-base local/remote refs、remote repository 与 task branch，但
  current task HEAD/dirty bytes由 private `task_worktree_state` 精确绑定；
- native owner staging在 task-local profile构造 current task worktree state，并把 owner
  result写入已声明 prior snapshot locator；pre-task路径保持原行为。

独立 regression：

```text
python3 -m unittest \
  trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py \
  -k test_feature_worktree_task_mode_binds_exact_dirty_state_and_public_wrapper
```

结果：`Ran 1 test`，`OK`。测试覆盖 task HEAD advance不产生 `base_head_stale`、stale task
state仍被拒绝、刷新 state后通过，以及 pre-task HEAD advance仍产生 `base_head_stale`。
Canonical/installed runtime bytes一致。未发现该两行 freshness 分层造成新的 current-scope
finding。

## Fresh Phase 2 与 commit 002

- Fresh Phase 2 SHA-256：
  `d7d8556f8caf5d56ee089c32295fbc691803f1ef1ab1075c1e8089a9ca509e76`，
  size `203845` bytes。
- Phase 2 AI Gate：`passed`，`full_rerun=true`，十个 adequacy dimensions全 passed，
  `findings=[]`、`findings_count=0`、typed exit `passed`。
- 当前 full round记录 `58` 项命令；package `166/166`、runtime
  `557 passed / 13 skipped`、preset `45/45`、ownership `6/6`、Stage 0 `24`
  cases与 production `12` cases通过。
- Source/installed discovery、九包 corpora、production allowlist/actual-exit、Stage 0
  manifest frozen、package/platform byte identity、public sample throwaway、update/reapply、
  dogfood drift、sidecar/secret/deployment scans均 exit `0`。
- `throwaway-exact` 因分支尚未 push按合同 exit `2`，Phase 2明确记录为 non-blocking U1，
  没有用 public sample冒充 exact remote branch proof。

Phase 2 pre-commit snapshot HEAD为 Round 001 HEAD，记录 `27` 个 dirty paths。Commit 002
exact-stage set为 `25` 个 paths：

- 有意不提交的 4 个已有 review metadata：
  `review-gate.json`、`review.md`、Round 001 raw report与 plan 001 live sidecar；
- commit时新增的 2 个 machine artifacts：
  fresh `phase2-check.json` 与 plan 002；
- 因而 `27 - 4 + 2 = 25`，没有未覆盖或未提交的 source/runtime/workflow/test路径。

Plan 002 evidence绑定上述 Phase 2 digest、fresh planning approval与 ledger。`exact_stage_paths`、
`result.committed_paths` 和 commit `c945c73...` 的实际 25-path tree集合完全一致，排序后集合
SHA-256均为
`4567b9ae4f54265cb0b3764601f38229e5562fbfa2b95c16f3fad055b5a389ac`；
expected/actual tree均为 `4a2c13affe824af51d688d7cd9d68b42a2dc9f10`。

Commit内 plan 002 blob保持不可变 `planned`，live sidecar为 `committed` 并精确绑定
`c945c73e1779f4e62409883bab5e1f6a907e4584`，符合既有 transaction设计。当前
post-commit dirty paths均为已有 task/review metadata，没有 source drift。

## Docs SSOT

Phase 2 `docs_ssot_plan` 使用 `ssot_first`，15 个 durable paths的当前 SHA-256全部与 artifact
记录一致。既有 durable contracts 已明确：

- production 三包的 real wrapper、existing recorder/checker/builder 与 checker-passed
  actual-exit ownership；
- production semantic eval 的 repo-local owner result、actual-exit schema selection 与
  `expected_exit` 不进入 adapter/native request；
- exactly three production packages、10 profiles、11 exits，以及 Stage 0 6/24 与 combined
  9/35 closure；
- source/installed/platform identity、clean install、upgrade/update/reapply与 zero-sidecar
  要求。

R17 是对上述既有 production eval 合同的最窄 owner-staging实现授权，不需要制造新的公共
API或并行 SSOT。P2-F002 所缺的 AI runtime contract已直接写入 canonical workflow并同步
dogfood，因此 Round 001 的 Docs-to-runtime mismatch已消失。

Round 001 观察项 `.trellis/spec/workflow/index.md` 仍不在 15 个 durable path列表中；该文件
已在累计 task diff中更新、内容与当前 contracts协调，finding-fix delta未再次修改它。本轮
继续记录为 nonblocking observation，不创建 required follow-up。

## 安全、兼容性与部署

- `git diff --check origin/main...HEAD` 通过。
- Finding-fix delta未修改 #147 runner/schema/grader/protocol、stable Skill/exit ids、
  Stage 0 manifest、CI/CD、Docker/container、K8s/Kustomize/Helm、DB migration、
  Terraform、proto或 Makefile。
- Phase 2 secret scan通过；本轮 diff复核未发现 token、secret、private key、签名 URL、
  `.env`、客户数据或敏感原始记录。
- Canonical/installed native adapter、workflow与runtime均 byte-identical；public sample
  clean install/update/reapply通过且无 `.new/.bak`、removal/conflict或 dogfood drift。
- R16、P1、P2均是 supported normal-path correctness/authority修正；没有引入恶意篡改、
  hostile input、并发竞态、TOCTOU、锁或其它排除场景。

## 观察与后续

### Nonblocking observations

- 分支尚未 push，exact current-branch remote marketplace verification未执行成功；必须在
  push 后、PR readiness前补验，且 public sample不能替代 exact ref。
- 审查开始前已有未提交 `agent-assignment.json`、plan 001/002 live sidecars、
  `review-gate.json`、`review.md` 与 Round 001 raw report；它们属于 review/task metadata
  tail。本代理未修改这些文件。

### Required follow-up

- 两个 Round 001 findings均已关闭，没有新的 current-scope P0-P3 finding，也没有需要新
  issue的 follow-up candidate。
- 下一步必须派发一个未出现在 Round 001/002 的全新 final-release reviewer，按最新
  `origin/main...c945c73...` 完整 diff执行最终审查。本报告不得直接转换为 passing Branch
  Review Gate。

## 结论

- P0：`0`
- P1：`0`
- P2：`0`
- P3：`0`
- findings_count：`0`
- P1-F001：`closed`
- P2-F002：`closed`
- reviewed_head：`c945c73e1779f4e62409883bab5e1f6a907e4584`
- reuse_decision：`reuse-for-closure`
- closure verdict：`PASS`
- final-release verdict：`not performed`

Round 001 的 adapter authority与 clarify-scope runtime findings均已由 current authority、
fresh planning/approval、实现、targeted regressions、fresh Phase 2 与 exact commit 002完整
关闭；R16 normal-path修正没有产生新 finding。本轮只完成 finding lifecycle closure，不授权
最终放行、passing Branch Review Gate、push、PR、finish-work或 issue close。
