# #146 实施计划：production Skills 最小 typed handoff 原子迁移

## 1. 实现前门禁

- [ ] `guru-review-contract-wording:planning_artifacts` 对当前 `prd.md`、`design.md`、
  `implement.md` 返回 checker-passed `pass`。
- [ ] `guru-approve-task-plan` 已完成 planning adequacy、provenance、unusual scenario 与 AI
  Review Gate；用户查看三份最终规划链接后给出独立的 post-planning approval。
- [ ] R12-R16 的五组 proposal/action 已作为 `accepted_current` 绑定 comments
  `5044522718`、`5045340918`、`5047220259`、`5049566946`、`5050065847`，并写入
  `issue-scope-ledger.json` decision trail；仍只关闭 #146。
- [ ] 主会话通过当前 Interface 1.2 owner recorder 记录 schema 2.0
  `planning-approval.json`，`check-planning-approval.sh --json` 验证 current 且 workflow
  消费 `approved` typed exit 后才运行 `task.py start`；尚未实现的 Interface 1.3 public
  wrapper 不作为本次 activation 前置条件。
- [ ] Workspace boundary 指向
  `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/146-production-skill-minimal-handoff`，
  branch 为 `codex/146-production-skill-minimal-handoff`，base 为 `main`。
- [ ] 按 `trellis-before-dev` 加载本 task 的 `implement.jsonl` spec 清单。
- [ ] Implementation 必须由 `trellis-implement` sub-agent执行；Phase 2 必须由独立
  `trellis-check` sub-agent执行。主会话只协调、记录 liveness、运行 recorder/validator、
  消费 typed exits、创建 task commit 与组织 Branch Review。
- [ ] Docs strategy 固定为 `ssot_first`；Middle-platform Knowledge Gate 为“不适用”。

## 2. 有序实现步骤

### Step 1. Durable SSOT、production manifest 与 closure baseline

- [ ] 先更新 `design.md` 11.1 列出的 workflow/package/data/script/quality/preset/public-doc
  specs、requirements/flow SSOT。
- [ ] 新增 closed schema
  `guru-team-production-migration-manifest-1.0` 与
  `migrations/production-minimal-handoff.json`。
- [ ] Manifest 精确登记 3 Skills、11 exits、10 input profiles、outputs、consumer inputs、
  projections、private artifacts、eval bindings 与 `preset_transaction` activation。
- [ ] Stage 0 manifest 保持 6 Skills、24 exits 与既有 activation identity；增加 byte/set
  regression，阻止本任务改写其范围。
- [ ] 扩展 source/installed package validator，以 live registry + Stage 0 manifest +
  production manifest + newly-active 1.3 entries 构造 closure。
- [ ] 增加 9 Skills、35 exits 当前 cardinality 与 missing/extra/duplicate/renamed/unknown/
  legacy/missing-I/O/profile/case mismatch 负例。

Checkpoint：durable contracts、两个 manifest schemas 与 closure fixtures先通过；stable id、
semantic owner、consumer shape 或 product scope 出现变化时停止实现并进入 Scope Change Gate。

### Step 2. Consumer-owned input contracts

- [ ] 为三个 package 实现 `design.md` 4.1 的 10 个 structured profiles，全部使用 closed
  `oneOf`、`profile` discriminator 与完整 examples。
- [ ] `guru-approve-task-plan` inputs 只接收 `task_ref`、authority refs 与 AI-owned
  provenance/adequacy/scenario/confirmation/Gate/route intent。
- [ ] `guru-check-task` inputs 只接收 `task_ref` 与 AI-owned scope/adequacy/finding/
  unverified/evidence locator/Gate/route intent。
- [ ] `guru-create-task-commit` inputs 只接收 `task_ref` 与 AI-owned message intent、path
  authorization、semantic review、human authorization、route/recovery intent。
- [ ] 为 workflow activation/resume/router/stop声明 exact input shape；现有
  `branch-review-or-finding-closure` consumer shape固定为
  `task_ref`/`base_ref`/`committed_head`，并与#131已确认input兼容。Skill consumer input由
  目标package拥有。
- [ ] 把 `guru-approve-task-plan:clarify_scope` consumer改为 routing-only
  `guru-task-plan-clarify-scope-router`，其 closed input精确为
  `exit_id`/`task_ref`/`proposal_refs`；router mandatory invoke existing
  `guru-clarify-requirements:active_task_scope_change`，八字段 target input由 caller AI fresh
  authoring。
- [ ] 为 `approve:revision_required`、`check:passed`、`commit:revision-required` 三条 edge
  声明 target-owned `skill_input_authoring_seed`；分别固定 `design.md` 5.4 的 seed fields，
  并由 target profile required set 推导 closed authoring fields。
- [ ] 每个 target profile 新增 package-local authoring example，只包含 fresh caller AI
  fields；测试证明 seed/authoring 交集为空、union 精确覆盖 required fields。
- [ ] 增加绝对路径、private artifact body、runtime digest/file metadata、unknown property、
  invalid discriminator 与互斥字段同时出现的负例。

Checkpoint：每个 profile 都有唯一真实 caller与 executable invocation example，不存在
optional/null mega object或无人消费 input schema。

### Step 3. 三包 Interface 1.3 与 11 output contracts

- [ ] 把三个 canonical `interface.json` 切换到
  `skill-interface-1.3.schema.json` 与 `schema_version=1.3`。
- [ ] 为 11 exits 各自新增 closed output schema与完整 example；保留
  `revision_required` 和 `revision-required` 的既有字节。
- [ ] 按 `design.md` 5.1 声明 exact DTO fields；`committed` 固定输出
  `task_ref`、`base_ref`、`committed_head`。
- [ ] 声明每个 consumer input与 direct/select/rename/normalize projection；为每个 output
  property登记 `consumer_use_ids` 与目标 consumer pointer。三条 authoring-seed edge 继续
  使用这些 operation，只把 minimal output 映射到 declared seed fields。
- [ ] 增加 unconsumed field、private field、unknown operation、wrong consumer、wrong profile、
  private lookup 与 schema/version mismatch 负例。
- [ ] 将 planning/check/commit state登记为 `gate_evidence|runtime_checkpoint` 与现有
  persistence；不改变 published private artifact schema/body。
- [ ] 更新三个 package 的 `SKILL.md`、`references/contract.md` 与 contract tests，只调整
  public boundary，不改变 semantic closed loop。

Checkpoint：`discover-skill-contract` source mode对三包返回 `minimal_handoff`，11 examples
全部通过对应 output schemas，并且 private artifacts 不出现在 public DTO。

### Step 4. Public wrappers、candidate builder 与 Stage 0 regression

- [ ] 为三包新增 thin `invoke.sh`，Interface 绑定 `run-skill-command`、structured profile、
  `single_typed_exit` stdout 与 stable error schema/example。
- [ ] Shared runtime验证 public input，按 `task_ref` 重读 private/live facts，调用现有 owner
  recorder/checker，并只序列化 checked actual exit 的 DTO。
- [ ] Shared validator/public probe exact-ref target interface/profile，分别验证 projected
  seed 与 target-owned authoring example，执行无覆盖 merge，再完整验证 target profile。
- [ ] 增加 overlap、missing、extra、unknown field、overwrite、literal/default、private
  lookup、semantic inference、runtime-authored judgment 与第五种 projection operation 负例。
- [ ] 实现 declarative projections，不添加任意表达式、private lookup或 semantic routing。
- [ ] 为 `guru-create-task-commit` 新增 deterministic candidate builder；builder生成 exact
  path/hash/mode/object/digest candidate并交给现有 validator/executor。
- [ ] 复用现有 transaction代码与 tests，证明 exact staging、copy/rename/gitlink、hooks、
  index/ref/result publish、rollback、unrelated preservation 与 message semantics不回归。
- [ ] 修复 `stage0_clarity_disposition()`，把 `keep_current_open_issue` 映射为 `retained`。
- [ ] 新增 schema/checker-passed clarification owner result经真实 Stage 0 wrapper返回
  `clear` + `retained` 的 regression；保留其它 disposition routes。
- [ ] Shared `stage0_owner_result` 接收 validated public input；只对
  `guru-discover-change-context:task_local_reentry` 传递 exact `task_locator`，并校验
  owner locator与 `task_locator/prior_snapshot_locator` 精确相同；`pre_task` 保持 `task=None`。
- [ ] 在 context-discovery task-mode private schema/owner result/recorder/checker加入
  `task_worktree_state`，精确绑定 HEAD、完整 path/status/mode/rename/content identity，并用
  同一规则排除 fixed snapshot自身；public DTO不变。
- [ ] AI Gate审查 current dirty scope与 load-bearing working files；recorder/checker只验证已
  审 evidence 与 live worktree exact equality。新增/删除/content/status/mode/rename drift失败
  关闭，`pre_task`/standalone继续要求 clean。
- [ ] Task-mode recorder新增 `--expected-prior-snapshot-sha256`；different-bytes replacement
  在写前验证 prior regular/trackable/schema/identity/exact digest，以及完整 new structural/
  live/AI Gate/worktree facts。
- [ ] Replacement成功后新 snapshot用 optional `superseded_snapshot_sha256` 精确绑定 prior，
  并完成 read-back、trackability、freshness 与真实 installed wrapper `context_ready` 检查；
  任何失败保持 prior bytes，相同 bytes retry结果保持一致。
- [ ] 增加 router cardinality、owner locator、active-task dirty state、post-snapshot drift、
  exact/missing/wrong prior、invalid/stale candidate preserves-prior、same-snapshot idempotency、
  task-local wrapper与pre-task clean regressions。
- [ ] 增加 trace/static tests，证明 wrapper、正常 Agent、consumer 与 eval path不要求 Agent
  读取/import `guru_team_trellis.py`，普通 invocation不加载 `evals/`。

Checkpoint：10 个 profiles与11 exits全部执行真实 wrapper invocation；每次 stdout只含一个
declared exit，actual route只来自 checker-passed owner result。

### Step 5. 三份 corpora 与 9/35 eval closure

- [ ] 三个 package 各新增唯一 canonical `evals/evals.json` 与其 fixtures。
- [ ] 每个 11 exit 与 10 profiles 绑定 current case；case id在 package内唯一，production
  manifest binding非空且无重复。
- [ ] Coverage 包含 initial planning、planning revision/clarification re-entry、initial check、
  finding-fix rerun、planning re-entry、initial/revision/finding-fix/recovery commit 与全部
  success/re-entry/router/stop exits。
- [ ] 三条 authoring-seed edge 的 eval case 使用真实 producer output example + target-owned
  authoring example，证明 merged input 执行真实 consumer wrapper；不得把完整旧 owner
  artifact 或 expected exit 当作 authoring input。
- [ ] `committed` case只验证 DTO投影成 #131 input，不 dispatch Branch Review。
- [ ] 用 `discover-skill-evals`/`run-skill-evals`执行 shared adapter完整 corpora；semantic cases
  提供 repo-local checker-passed owner results。
- [ ] Runner先读取 actual exit并按 actual exit选 output schema，再比较 `expected_exit`；
  测试证明 `expected_exit` 未进入 wrapper、owner result builder或 route selector。
- [ ] 执行 Codex trusted Git context、Claude input protocol、Cursor
  unavailable/unsupported、shared parse/execute 与九份 corpora byte identity tests。
- [ ] Closure validator证明 live active registry的每个 profile/exit均有 current case binding，
  且不存在平台 corpus fork。

Checkpoint：9 Skills、35 exits、全部 active input profiles的 I/O/eval set difference为零；
#147 schema、grader policy、semantic ownership、human review boundary与run evidence无修改。

### Step 6. Registry、extension 与 atomic activation

- [ ] 同时把三个 registry entries切换到1.3 + `minimal_handoff`；active总数保持9。
- [ ] Extension `legacy_skill_ids` 收敛为空，minimal/active inventories精确覆盖9 Skills。
- [ ] 更新 public input/output/private schema inventories、production manifest locator、managed
  assets、commands 与 installed facts。
- [ ] Workflow只更新 package invocation/exit markers和consumer refs；删除已被 package contract
  拥有的重复 public-boundary说明时，必须保持现有 phase route语义。
- [ ] Preset在临时 staging root构造并验证完整 production graph后一次apply；中间 mixed graph
  必须被 source/staged/installed validator拒绝。
- [ ] 增加 pre-#146 installed fixture，验证完整 6 minimal + 3 legacy graph升级为完整 9
  minimal graph，未修改 archive artifacts。

Checkpoint：source tree与staged install均为9个 active minimal entries；任一 legacy/missing/
unknown/mixed状态失败关闭。

### Step 7. Preset、dogfood、四平台与 public docs 同步

- [ ] 更新 preset managed assets、installed manifest、installer tests与throwaway inventory。
- [ ] 运行 canonical preset apply同步 `.trellis/guru-team/`、`.agents/skills/`、
  `.codex/skills/`、`.cursor/skills/`、`.claude/skills/`。
- [ ] 逐项处理 `.new`/`.bak`，不得静默覆盖用户文件；运行 dogfood overlay drift 与 upstream
  ownership检查。
- [ ] 比较三包 Interfaces/schemas/examples/wrappers/evals在 canonical、installed 与 selected
  platform roots的 bytes和 executable mode。
- [ ] 比较 Interface 1.3 schema、三个 target authoring examples、representative fixtures 与
  authoring-seed validator tests 在 canonical/installed/platform roots 的 bytes。
- [ ] 比较 clarify_scope workflow consumer、context-discovery schema/tests、task worktree
  state/replacement runtime 与 selected platform package copies 的 bytes/hashes。
- [ ] 更新 requirements/flow SSOT、root README、workflow README与preset README中的9×35
  production状态、discovery/invocation/eval/upgrade命令与 #131 handoff。

Checkpoint：dogfood source/installed validation均通过，overlay drift为零，递归 sidecar扫描
为空，README命令在throwaway repo执行成功。

### Step 8. Clean throwaway、update/reapply 与 existing-state 验证

- [ ] 在干净临时 repo运行 workflow marketplace init，并校验 `guru-team` id/path/type。
- [ ] 验证已有项目 workflow `--create-new` preview 与正式 switch。
- [ ] 安装 preset，运行九包 contract discovery、9×35 closure、正常
  planning-to-check-to-commit-to-#131 projection transcript。
- [ ] 执行所有 profiles、11 exits、Stage 0 `keep_current_open_issue` regression 与 #145
  6×24 regression。
- [ ] 执行 clarify_scope routing-only projection与 mandatory invocation regression，并证明
  authoring-seed edge cardinality仍为3。
- [ ] 在真实 task branch/dirty worktree执行 owner locator + `task_worktree_state` pass，随后逐类
  制造 path/status/content/mode/rename drift并验证 fail；重复 pre-task/standalone clean contract。
- [ ] 对 fixed context snapshot执行 exact-prior replacement、missing/wrong prior、invalid/stale
  new candidate preserves bytes、same-bytes idempotent retry、superseded binding与installed public
  wrapper `context_ready` probes。
- [ ] 执行三条 authoring-seed edge 的 partition/no-overwrite/full-target-schema probes，
  并证明其它 Skill/workflow/stop consumers 与四种 projection operations 无回归。
- [ ] 从 pre-#146 fixture升级，运行 `trellis update`、preset reapply并重复 source/installed/
  closure/eval验证。
- [ ] 验证 existing active planning/check/commit state通过完整 owner re-entry进入1.3；archive
  仍按旧 schemas只读。
- [ ] 最终扫描 throwaway与dogfood无 `.new`/`.bak`、无 mixed graph、无 private runtime
  Agent import。

### Step 9. Docs reconciliation 与 Phase 2 handoff

- [ ] 对照 Docs SSOT Plan记录实际更新路径、task delta merge、task-history-only内容、
  no-change证据与 PR/follow-up界限。
- [ ] Implementation handoff列出所有修改路径、R/AC承接、validation、existing-state、
  deployment/safety与distribution影响。
- [ ] 独立 `trellis-check` sub-agent检查 durable docs、task artifacts、code、API、schema、
  config、tests、install/update、CI/CD、container、K8s、DB migration与Makefile影响。
- [ ] 主会话只在完整 AI check报告后 record/check `phase2-check.json`，再 mandatory invoke
  `guru-create-task-commit`。

## 3. 预计修改面

### 3.1 Canonical specs、packages 与 runtime

- `.trellis/spec/workflow/{index,skill-package-contract,workflow-contract,data-contracts,companion-scripts,quality-guidelines}.md`
- `.trellis/spec/preset/{installer,overlay-guidelines,upstream-ownership}.md`
- `.trellis/spec/docs/public-docs.md`
- `trellis/skills/guru-team/migrations/production-minimal-handoff.json`
- `trellis/skills/guru-team/schemas/production-migration-manifest.schema.json`
- `trellis/skills/guru-team/schemas/skill-interface-1.3.schema.json`
- `trellis/skills/guru-team/packages/{guru-approve-task-plan,guru-check-task,guru-create-task-commit}/**`
- `trellis/skills/guru-team/packages/guru-discover-change-context/{schemas,tests}/**`
- `trellis/skills/guru-team/registry.json`
- `trellis/workflows/guru-team/workflow.md`
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py` 及 tests
- `trellis/skills/guru-team/tests/test_skill_packages.py`
- `trellis/guru-team-extension.json`

### 3.2 Distribution 与 docs

- `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py` 及 tests
- `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`
- Canonical overlay inventory/source；dogfood copy只作为安装结果
- `.trellis/guru-team/**` 与 shared/Codex/Cursor/Claude installed copies，包含
  `guru-discover-change-context` schema/tests
- `docs/requirements/README.md`、`docs/requirements/requirement-main.md`、
  `docs/requirements/guru-team-trellis-flow.md`
- `README.md`、`trellis/workflows/guru-team/README.md`、
  `trellis/presets/guru-team/README.md`

若实现证明某个预计路径没有 semantic delta，implementation handoff 与 Phase 2 report必须
记录该路径的检查证据与明确 no-change reason。

## 4. Validation commands

新增 test selector在实现时按真实文件名固化；以下命令族全部执行，单个子集通过不能替代
完整门禁。

```bash
python3 -m json.tool trellis/skills/guru-team/migrations/production-minimal-handoff.json
python3 -m json.tool trellis/skills/guru-team/schemas/production-migration-manifest.schema.json
python3 -m unittest discover -s trellis/skills/guru-team/tests -p 'test_*.py'
python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py
python3 trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py
python3 trellis/presets/guru-team/scripts/python/test_upstream_ownership.py
python3 -m py_compile \
  trellis/workflows/guru-team/scripts/python/guru_team_trellis.py \
  trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py
bash -n trellis/workflows/guru-team/scripts/bash/*.sh \
  trellis/presets/guru-team/scripts/bash/*.sh
trellis/workflows/guru-team/scripts/bash/check-skill-packages.sh \
  --root . --json --mode source
trellis/presets/guru-team/scripts/bash/apply.sh --repo .
.trellis/guru-team/scripts/bash/check-skill-packages.sh \
  --root . --json --mode installed
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh --repo .
trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh
python3 ./.trellis/scripts/task.py validate 07-22-146-production-skill-minimal-handoff
.trellis/guru-team/scripts/bash/check-workspace-boundary.sh --json \
  --task .trellis/tasks/07-22-146-production-skill-minimal-handoff
find . -type f \( -name '*.new' -o -name '*.bak' \) -print
git diff --check
```

还必须执行并记录：

```text
- 三包 source/installed contract discovery 与10 profiles真实 invocation probes
- 三包 shared adapter full corpora runs
- 11 exits/profile/case/consumer/projection set equality
- 9 active Skills/35 exits live closure
- passed-to-commit、两个self-reentry与committed-to-#131 projections
- 三条authoring-seed partition + no-overwrite merge + complete target schema probes
- deterministic candidate builder与既有commit transaction regression suite
- actual-exit schema selection + expected_exit non-oracle negative tests
- keep_current_open_issue -> retained真实Stage 0 wrapper regression
- clarify_scope -> routing-only workflow target -> mandatory clarification invocation regression
- task_local_reentry owner-checker exact locator pass与mismatch/unsafe/stale negative tests
- private task_worktree_state active dirty pass与path/status/content/mode/rename drift failures
- formal snapshot exact-prior replacement、preserve-prior failure、same-bytes idempotency、
  superseded binding与installed context_ready wrapper
- #145 6 Skills/24 exits、optional fallback、actual-exit selection与atomic activation regression
- Codex trusted Git、Claude input protocol、Cursor unsupported与九份corpora byte identity
- clean throwaway pre-#146 upgrade + trellis update + preset reapply + full closure rerun
- existing active re-entry + archive read-only fixtures
- normal Agent transcript: public_invocation_only + private_runtime_not_read_by_agent
```

## 5. Review gates

- Contract gate：3×11 exact set、10 profiles、schema ids、consumer/projection与production
  manifest一致。
- Closure gate：9×35 live registry/I/O/eval set difference为零，Stage 0 6×24 identity不变。
- Minimality gate：每个 public output property有direct consumer pointer，private/audit字段未泄漏。
- Authoring-seed gate：范围精确为三条声明 edge；seed/authoring分区完整且无交集，merge无覆盖，
  merged input通过完整target schema，runtime未生成AI judgment。
- Scope-router gate：`clarify_scope` 只进入三字段 routing-only workflow target，existing
  clarification profile仍由caller AI fresh authoring，authoring-seed edge仍精确为3。
- Task-context gate：owner checker使用validated exact task locator；private worktree state与live
  dirty scope精确一致；formal replacement只在exact prior与完整new checks通过后改变fixed bytes。
- Semantic boundary gate：AI仍做scope/review/confirmation/route判断，脚本只执行确定性事实。
- Commit gate：builder只生成private candidate，既有transaction invariants全部通过。
- Invocation gate：每个 profile与11 exits均由真实 public wrapper执行验证。
- Compatibility gate：stable ids/owners/confirmations/private schemas/archive读取不回归，#131
  只消费最小 committed DTO。
- Eval gate：actual exit决定schema，`expected_exit`只作事后断言，四平台不fork corpus。
- Activation gate：source/staged/installed出现mixed production graph时失败关闭。
- Distribution gate：canonical/installed/dogfood/四平台byte/mode一致。
- Upgrade gate：fresh install、pre-#146 upgrade、update/reapply后同样通过且零sidecar。
- Docs gate：Docs SSOT Plan已执行，无current-scope durable docs不一致。

## 6. Rollback points

| Point | Trigger | Action |
| --- | --- | --- |
| RP1 | 三条semantic consumer无法以minimal seed + fresh authoring完成下一步 | 保持实现暂停；只按已确认R12修订target-owned partition/merge/schema proof。若R12仍不足则再次进入Scope Change Gate；不得暴露完整private artifact或由runtime重建AI judgment |
| RP2 | Interface/schema要求stable id或semantic owner变化 | 停止实现，更新规划并重新执行planning approval |
| RP3 | Source validation出现mixed graph | 不执行preset apply，修复完整三包activation后重跑 |
| RP4 | Preset staging/install产生冲突或sidecar | 保留迁移前完整安装，处理canonical/provenance后整包reapply |
| RP5 | Builder实现要求重写transaction算法 | 停止该方向，改为调用既有validator/executor；不得扩张锁/TOCTOU/crash/OS范围 |
| RP6 | #147 policy或#131内部行为出现修改需求 | 停止实现并进入Scope Change Gate |
| RP7 | Existing active/archive兼容失败 | 保留旧schema读取，修复owner re-entry/adapter；不得回写archive |
| RP8 | Native platform能力缺失 | 返回`unsupported`并记录未验证风险，不生成平台corpus |
| RP9 | clarify_scope router要求第4条seed或producer扩字段 | 停止该方向；保留routing-only target与caller AI fresh authoring，若仍不足则重新进入Scope Change Gate |
| RP10 | task-local context checker无法区分合法dirty scope与drift | 保持public DTO不变，修订private `task_worktree_state` capture/compare；不得无条件接受dirty paths或执行Git清理操作 |
| RP11 | snapshot replacement任一prior/new/live/worktree校验失败 | 保留prior bytes并停止re-entry；不得删除、复制、改名snapshot或引入锁/TOCTOU/archive pointer |

## 7. Docs SSOT checkpoint

- Strategy：`ssot_first`。
- 实现前：先更新 `design.md` 11.1 的 durable contracts。
- 实现中：task artifacts只保留delta、取舍与证据，不成为平行长期规范。
- Phase 2前：逐项核对docs、Interfaces、runtime、manifests、registry、extension、installer、
  evals、help与tests一致。
- Commit前：记录实际docs文件、已合并task delta、task-history-only内容、existing-state、
  throwaway/update/reapply与零sidecar证据。

## 8. 完成清单

- [ ] R1-R16均有代码、schema、测试或文档证据。
- [ ] AC1-AC21全部通过。
- [ ] Implementation与check sub-agent liveness/handoff完整。
- [ ] `guru-check-task` checker-passed，零未解决current-scope finding。
- [ ] `guru-create-task-commit`完成reviewed task commit。
- [ ] 独立Branch Review覆盖`origin/main...HEAD`完整diff并通过。
- [ ] `trellis-continue`停在Branch Review Gate；只有用户后续明确调用
  `trellis-finish-work`才执行push、draft PR、archive与ready closeout。
