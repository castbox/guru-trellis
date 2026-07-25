# #116 实现交接：guru-review-task-publication

## 1. 实现结论

已完成 `guru-review-task-publication` 的实现边界；本轮实现代理未执行 commit、push、
PR、archive、`guru-finalize-task`、新的 Phase 2 check 或 Branch Review Gate。

本次实现把原 planned publication step 激活为 Interface 1.3 semantic Skill：

- profiles：`publication_review`、`publication_review_stale`；
- typed exits：`ready`、`return_to_task_work`、`blocked`；
- 唯一 consumers：planned `guru-finalize-task`、task-work workflow router、显式 stop；
- 唯一 gate：task-local `pr-readiness.json`；
- active closure：11 Skills / 42 exits；
- `production-minimal-handoff-v1` 继续冻结为 3 Skills / 11 exits。

独立 Phase 2 首轮发现的 `F-001`、`F-002`，finding-fix 后第二轮复审发现的
`F-002` closed-union 残余与 `F-003` installed manifest stale sidecar inventory，
以及第三轮复审发现的 `F-004` publication active route 未同步和 `F-005`
publication content 首次生成顺序缺口，均已在实现轮修复。原
`phase2-check.json`、`phase2-worker-report-round2.md` 与
`phase2-worker-report-round3.md` 保留为失败证据，未被实现代理改写；须由新的独立
`trellis-check` 对 current diff 完整复检。

`guru-review-branch:passed` 继续输出原四字段 DTO bytes，只把 consumer 改为
target-owned `skill_input_authoring_seed`：seed 为
`task_ref/reviewed_head/review_ref`，caller authoring 为
`profile/mode/review_intent`。Global Phase 3.6 workflow caller 在 mandatory
invocation 之前另行负责初始 `pr-body.md` 与 `finish-summary-index.json` 内容候选
写作；这只是 entry preparation，不拥有 ten-dimension publication review、Issue
closure、finding route 或 readiness 判断。

## 2. 主要文件变化

### 2.1 Canonical package、registry 与 workflow

- 新增 `trellis/skills/guru-team/packages/guru-review-task-publication/**`：
  `SKILL.md`、contract、Interface 1.3、public/private schemas、examples、wrapper、
  recorder/checker scripts、tests 与 7-case eval corpus。
- 新增 publication workflow/stop consumer schemas。
- 更新 `trellis/skills/guru-team/registry.json`：
  publication 变为 active，新增 planned `guru-finalize-task`。
- 更新 `guru-review-branch/interface.json` 及 contract tests；原 public output
  schemas/examples 均未修改。
- 更新 canonical/dogfood workflow，新增 Phase 3.6 publication review，原 finish/publish
  阶段顺延。
- 新增 canonical `record-task-publication-review.sh`、
  `check-task-publication-review.sh`。
- 更新 `guru_team_trellis.py`、runtime tests 与 native eval adapter。
- 更新 `trellis/guru-team-extension.json` 到 `0.6.5-guru.22`，同步 command、
  schema、managed asset、active/planned package inventory。

### 2.2 Preset、安装验证与生成副本

- 更新 preset installer tests、throwaway install/update/reapply verifier 和 installed
  closeout fixture。
- 通过 preset apply 生成并校验：
  `.trellis/guru-team/**`、`.agents/skills/guru-review-task-publication/**`、
  `.codex/skills/guru-review-task-publication/**`、
  `.claude/skills/guru-review-task-publication/**`、
  `.cursor/skills/guru-review-task-publication/**`。
- canonical、installed、shared、Codex、Claude、Cursor publication package bytes
  一致，所有 package scripts 保持 executable。

### 2.3 Compatibility 与集成修复

- legacy `pr-readiness.json` reader 保留识别兼容，但新 checker 不把 legacy
  deterministic `ready=true` 当作 semantic pass。
- `build_pr_readiness_snapshot()` 只在 checker-passed `ready` gate 上追加
  `publish_inputs`，保留 semantic review、typed exit 与 opaque `publication_ref`。
- finalization augmentation 使用专用窄化 freshness 规则：普通 publication checker
  不放宽；仅允许 exact task-local `closeout-plan.json` 作为 finalization-owned status
  delta，并校验 plan schema/digest。任何额外 task metadata、durable 或 non-metadata
  drift 继续 fail closed。
- 修复新增 publication output 分支时暴露的 #131 Branch Review
  `scope_confirmation_required.proposal_refs` 投影回归，并用 source/installed actual
  wrapper eval 复验。

### 2.4 Phase 2 findings 修复

- `F-001`：stale profile 现在强制并逐字段绑定 `stale_reason`、
  `reentry_context`、`supersedes_publication_ref`；superseded ref 必须精确等于
  current prior publication identity，wrapper 也必须与 recorder/checker 结果逐字段
  一致。
- recorder/checker 每轮都从 live facts 重建十二项 entry preconditions：
  runtime dependency、task/workspace/identity、Branch Review handoff、Planning、
  Phase 2、issue scope、Docs SSOT、Branch Review evidence、publication content、
  review range/working tree 与 invocation freshness；每项持久化
  `status + facts_sha256`，缺项、非 passed 或 digest 漂移都不能得到 `ready`。
- `F-002`：`pr-readiness.schema.json` 已收敛为 closed semantic、
  deterministic、consumer/publish-inputs 三层，嵌套 object 均关闭未知字段；
  `ready` 强制十维 passed、十二项 entry passed、零未关闭 finding 以及唯一
  `guru-finalize-task` consumer。
- 第二轮 `F-002` 残余已同时在 private schema 与 runtime semantic checker
  fail closed：
  - `ready` 强制三项 conclusions 全部 `passed`、十维全部 `passed`、findings
    全部 closed；
  - `return_to_task_work` 强制至少一个 `finding` dimension、至少一个 open
    `task_work` finding、无 blocked dimension/conclusion，且所有 open finding
    只能指向 `finding` dimension；
  - `blocked` 强制至少一个 blocked dimension、至少一个 open
    `external_blocker` finding、至少一个 blocked conclusion，且所有 open finding
    只能指向 blocked dimension。
- findings 与 dimensions 的引用一致性由 runtime checker 继续补足 JSON Schema
  无法表达的交叉引用：open finding 不得指向 passed dimension，每个非-passed
  dimension 必须有 open finding evidence。
- findings 现在强制非空 summary/scope/evidence/affected/closure；重复 finding id、
  空 closure evidence、缺 stale replacement identity、任一 entry failed 均有
  schema/runtime negative tests。
- throwaway 的真实 closeout 链暴露了 finalization 首次写入 exact
  `closeout-plan.json` 后 entry binding 也会随 repository snapshot 正常变化。专用
  augmentation checker 现在仍重跑十二项条件，只接受该唯一 plan addition 导致的
  repository status 与派生 `review_range_and_working_tree` digest 变化；其它十一项和
  其它 repository 差异必须保持 exact，普通 publication checker 未放宽。
- 第二轮 `F-003` 通过 canonical preset apply/update 路径修复，未绕过或放宽
  installed validator：首次 apply 为 canonical/installed 差异生成 15 个 package
  managed backups 与 1 个 runtime managed backup；逐个核对 current installed copy
  已等于 canonical、backup 为 superseded 旧版本后，仅删除这 16 个 `.bak`，再次执行
  canonical apply。最终 `.trellis/guru-team/extension.json` 的
  `skill_packages.status=ok`，`managed_backups/new_copies/sidecars/conflicts` 均为空，
  actual recursive sidecar scan 也为 0。
- 第三轮 `F-004` 已把 `guru-review-branch:passed` 的 current route 同步到
  canonical/dogfood workflow、Branch Review package、五个 canonical/dogfood
  `trellis-continue` 入口及 durable docs：当前直接进入 active
  `guru-review-task-publication`，其三个 typed exits 均有唯一 consumer；仅
  `ready -> guru-finalize-task` 保持 planned/missing 并 fail closed。未实现
  #118、#119 或 #132，也未修改 finish family。
- 第三轮 `F-005` 已把 publication content 的真实生产顺序写入 global workflow：
  Branch Review passed 后，caller 必须先依据 current reviewed evidence 写入
  task-local `pr-body.md` 与 `finish-summary-index.json`，缺失或客观 malformed
  时不得调用 publication Skill；随后 mandatory invoke active semantic owner。
  这一步不生成 semantic pass 或 route，recorder/checker 仍只在 AI Gate 后复用
  既有确定性 validators。Phase 3.7 只能消费 `ready` 已绑定的 exact bytes，不得
  首次创建、重新生成或修改；metadata-only 变化重进 publication，non-metadata
  变化返回 task work。

## 3. Requirement / Design 承接

- R1-R12、AC1-AC18 的实现面已承接：semantic owner、双入口、十维 review、
  finding route、metadata-only 内部闭环、stale re-entry、唯一 gate、minimal DTO、
  legacy compatibility、real-wrapper eval、11/42 closure、安装/update/reapply。
- `ready` 只指向 planned identity；本任务未定义 #118 target package/schema，也未执行
  finalization 或任何 GitHub mutation。
- `return_to_task_work` 强制回 implementation -> Phase 2 -> commit -> Branch Review；
  `blocked` 只进入显式 stop。
- #131 public output schemas/examples/bytes 保持不变；第三轮 `F-004` 仅按其
  reviewed-current-payload 迁移规则更新同一组五个 continue overlay paths 的
  publication route，43-path inventory 和 frozen identity 不变。
- `production-minimal-handoff-v1` 与 upstream finish-work
  Skill/Command/Prompt assets 均无 diff；未执行 #132 removal。Overlay tree
  只有上述五个 reviewed current payload 的预期内容变化，未增加、删除或改名路径。

## 4. Docs SSOT Plan

策略：`ssot_first`。

实现前先以修订后的 durable docs/spec 为主输入，再实现 package/runtime/preset。Task
delta 已合并到以下 durable authorities：

- `.trellis/spec/workflow/`：
  `skill-package-contract.md`、`workflow-contract.md`、`data-contracts.md`、
  `companion-scripts.md`、`quality-guidelines.md`、`index.md`；
- `.trellis/spec/preset/`：
  `installer.md`、`overlay-guidelines.md`、`upstream-ownership.md`；
- `.trellis/spec/docs/public-docs.md`；
- `README.md`、`docs/requirements/README.md`、
  `docs/requirements/requirement-main.md`、
  `docs/requirements/guru-team-trellis-flow.md`；
- `trellis/workflows/guru-team/README.md`、
  `trellis/presets/guru-team/README.md`。

Durable docs 定义稳定 publication/finalization contract、11/42 closure、五条
active publication route、workflow caller content preparation 与 sole semantic
owner 边界、`pr-readiness.json` 分层、recorder/checker 边界、安装与
update/reapply 口径。已确认 task delta补充具体 field/schema/command/fixture
细节后同步回上述 durable authorities。Phase 2 修复产生的 stale replacement、
十二项 entry binding、closed finding closure 和 exact closeout-plan augmentation
规则已继续合并到 `skill-package-contract.md`、`data-contracts.md`、
`companion-scripts.md`、`quality-guidelines.md` 以及 package contract reference；
第二轮的 typed exit / conclusions / dimensions / findings closed-union 与
schema/runtime 双重 fail-closed 规则也已同步到这四份 workflow spec 和 package
contract reference。durable docs 与 schema/runtime/tests 已重新对齐，task delta
不再承担新的 durable合同。

仅保留为 task history 的内容：`prd.md`、`design.md`、`implement.md`、
planning approval/context/assignment evidence 和本交接文档；这些内容不作为新的 durable
workflow SSOT。

`no_docs_update_needed` 不适用；`bootstrap_or_repair_docs` 不适用。当前 PR 限制是分支未
push，因此无法从 exact remote branch ref执行 current-branch marketplace verifier。
Throwaway 脚本先对此 fail closed，随后使用明确的 public-marketplace sample 模式验证
公开 marketplace discovery，并使用本地 unpublished workflow sample验证本分支 workflow；
remote exact-branch marketplace verification保留给后续 push/finish gate。

## 5. 测试与检查

- `python3 -m unittest ...test_skill_packages --failfast`：
  Round 3 新增顺序测试的首次全量运行只因测试读取了不存在的
  `interface.input_profiles` 而出现一个 `KeyError`；Interface 1.3 的真实结构为
  `modes.workflow/standalone.entry_precondition_ids`。测试已修正为 exact 验证两种
  mode 都包含 `publication_content`，未弱化 workflow ordering、malformed stop 或
  Phase 3.7 no-first-create 断言；最终全量结果见本节末尾 Round 3 验证记录。
- `python3 .../test_guru_team_trellis.py`：最终全量复跑 570 tests passed、
  13 skipped，218.623s。
- preset installer suite：Round 3 全量 54 tests passed，90.835s。
- publication package contract suite：source 16 tests passed，installed 16 tests
  passed；覆盖 schema/example/runtime 一致性、F-001 与两轮 F-002
  positive/negative cases。
- Branch Review package contract suite：8 tests passed（实现期间已执行）。
- publication shared eval：
  source 7/7 passed，installed 7/7 passed；覆盖 workflow/standalone ready、
  return、blocked、stale re-entry、metadata fix ready、durable drift return。
- shared actual wrapper integration：`ready`、`return_to_task_work`、`blocked`
  三种实际 wrapper exit 全部通过；contradictory ready payload 被 actual recorder
  拒绝，模拟错误 recorder 输出后又被 shared runtime checker 以
  `ready requires every publication conclusion to pass` 拒绝。
- Branch Review `scope-confirmation-required`：
  source 与 installed actual wrapper均 passed。
- `verify-throwaway-install.sh`：
  `TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1` 完整通过 clean init/install、
  source/installed 11/42、initial/updated installed closeout、`trellis update`、
  preset reapply、pre-#146 upgrade 和 production shared eval；初次 closeout 为
  issue #105、update 后 closeout 为 issue #106，archive/local/remote/PR head 均
  一致且 readiness 为 ready。
- preset apply：首次按 managed-file 规则生成 16 个 reviewed backups，清理已核对的
  superseded sidecars 后再次 canonical reapply；最终 status `ok`，
  source/installed validator passed，sidecar/conflict/removal/new-copy均为 0。
- dogfood overlay drift passed；canonical runtime/workflow byte compare passed。
- publication canonical/installed/four platform copies `diff -qr` 全部一致，
  package scripts均 executable。
- `git diff --check` passed。
- recursive `.new/.bak/.orig` scan：0；canonical reapply 产生的 15 个 package 与
  1 个 runtime superseded `.bak` 已先逐项核对 current copy 与 canonical 一致、
  backups 非空且为旧 managed bytes，再仅删除这些旧 sidecars并重新生成 manifest。
- Round 3 preset sync 明确使用 `--all-platforms`。一次默认
  `codex + cursor` apply 暴露 selected-platform cleanup，并将四个已恢复的 Claude
  Branch Review local bytes保留为 `.new` conflict；逐项验证 `.new` 等于 canonical
  后，用受控 patch 同步四个 current files、删除 sidecar并重新 all-platform apply。
  最终 Claude publication package 已物化，installed manifest 为 `ok`，
  selected platforms 为 Claude/Codex/Cursor，2100 managed files，0 sidecar、
  0 conflict、0 removal；无无关 deletion 残留。
- Round 3 publication shared eval：source 7/7、installed 7/7 passed；publication
  installed contract 16/16 passed，Claude Branch Review contract 8/8 passed。
- Round 3 runtime suite：570/570 passed，13 skipped，162.670s；preset suite
  54/54 passed；最终 skill full suite 174/174 passed，276.926s。
- Round 3 `verify-throwaway-install.sh` 在
  `TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1` 下 exit 0：重新覆盖 clean
  init/install、initial issue #105 closeout、`trellis update`、workflow/preset
  reapply、after-update issue #106 closeout、无 developer identity fixture、三平台
  installed 2100/0/0/0、11/42/25、ownership/drift 与 shared eval，最终输出
  `Verified public marketplace discovery plus local unpublished workflow sample`。
- 冻结面 `git diff --quiet`：
  production manifest、#131 output schemas/examples、五个 #131 overlay paths、
  overlay tree、finish-work upstream assets全部为 0。

## 6. 交给 trellis-check 的重点

1. 复核 semantic/script boundary：十维 pass、finding route、issue closure、PR body
   充分性、安全/部署判断只能来自 AI owner，recorder/checker 不得决定。
2. 复核 `pr-readiness.json` 三层生命周期、legacy/active/replacement reader，以及
   finalization augmentation 重跑十二项条件且只允许 exact `closeout-plan.json`
   导致的 repository + derived review-range binding 变化的正负边界。
3. 复核 metadata-only revision loop：fresh reread/review；durable/non-metadata drift
   必须返回 task work。
4. 复核 public I/O 最小化、三个 exits 的唯一 consumer、ready planned bridge与
   publication_ref opaque。
5. 复核 #131 output bytes与 3/11 manifest 冻结不变；五个 continue overlay 仅按
   `F-004` 更新 reviewed current payload，43-path inventory 与 finish-work assets
   冻结不变。
6. 复核 11/42 source/installed closure、extension inventory、canonical/platform
   byte parity、executable mode、零 sidecar，尤其验证 typed exit 与
   conclusions/dimensions/findings 的 closed-union 正反例。
7. 复核 Docs SSOT reconciliation，尤其五条 authoring-seed handoff、Phase 3.6
   active publication route、caller content preparation -> sole semantic owner ->
   ready-bound Phase 3.7 consumer 顺序，以及 remote marketplace limitation 表述。

`trellis-check` 阶段可重跑全部验证并审查 current diff；实现阶段有意未执行
remote exact-branch marketplace verification、真实 Codex/Claude/Cursor CLI
在线调用、#118 finalization、commit/push/PR/archive。

## 7. 剩余风险与 follow-up

- exact current branch 的 remote marketplace验证必须等分支 push 后执行，当前结果不能
  声称该远端路径已验证。
- `guru-finalize-task` 仍是 planned identity；publication `ready` 后应由后续 #118 实现，
  本任务不承担最终发布事务。
- 三轮独立 `trellis-check` 的 `F-001` 到 `F-005` 实现缺口均已修复，但
  current diff 尚未经过修复后的新一轮独立 Phase 2 复检与 Branch Review Gate；
  需由后续独立代理完成。

## 8. F-006 finding-fix（Round 4）

### 8.1 修复结论与文件

第四轮独立 Phase 2 的唯一开放 finding `F-006` 已在实现边界修复：

- `docs/requirements/requirement-main.md`：
  `Post-commit Branch Review closed-loop Skill` current section 现在明确区分
  #131 交付时的 historical planned/missing bridge 与 #116 激活后的 current
  contract。Current contract 明确 `guru-review-task-publication` 已是 active
  target，target-owned authoring-seed contract 与 package/interface 拥有 input schema、
  `publication_review` profile 与 `profile/mode/review_intent` authoring fields；
  #131 unchanged `passed` DTO 只投影
  `task_ref/reviewed_head/review_ref` seed。只有 publication `ready` ->
  planned `guru-finalize-task` 因 target 尚未交付继续 fail closed。
- `trellis/skills/guru-team/tests/test_skill_packages.py`：
  在现有
  `test_durable_docs_match_five_authoring_edges_and_three_skill_migration`
  增加定向 durable-doc scanner。Scanner 只提取 current
  `## Post-commit Branch Review closed-loop Skill` section，要求上述 historical
  qualifier 与 current active wording；显式 historical/task-archive section
  不阻断，但把未限定的 current planned/missing 旧文案注入 current section 会被拒绝。
  未新增 script、wrapper 或平行 validator。
- 本 task-local `implementation-handoff.md`：追加本轮修复、验证与后续 Phase 2
  交接证据。

未修改 runtime、schema、workflow、preset、overlay 或 finish family；未实现
#118、#119、#132，未调用 planning/Phase 2 recorder/checker，未 commit、push、
创建 PR、archive 或 finalize。

### 8.2 Docs SSOT Plan reconciliation

策略继续为批准的 `ssot_first`。F-006 指向的 task delta 已合并到 durable
`docs/requirements/requirement-main.md`，该 current requirements section 现在与
既有 active package、workflow route、Interface 1.3 authoring seed 和 11/42 closure
一致。Historical #131 planned/missing 事实只保留为明确限定的交付历史，不再冒充
current contract；只有 #118 owned 的 `guru-finalize-task` 仍为 planned/missing。

Task-history-only 内容继续为 planning artifacts、四轮 raw Phase 2 reports、
historical `phase2-check.json` 与本 handoff。本轮没有新的 durable contract
follow-up；current PR limitation 仍是未 push 分支无法执行 exact remote-branch
marketplace verification。

Durable-doc implementation input 是已批准的 current workflow/spec/package contract
以及 `requirement-main.md` 的 active publication 主体；本轮 task delta input 仅是
Round 4 `F-006` 对同一 current section 的矛盾定位与修复要求。

### 8.3 验证证据

- 定向 regression：
  `python3 trellis/skills/guru-team/tests/test_skill_packages.py
  Stage0MigrationManifestTests.test_durable_docs_match_five_authoring_edges_and_three_skill_migration`
  -> final-bytes 1 test passed，0.117s。
- 完整 Skill package suite：
  `python3 trellis/skills/guru-team/tests/test_skill_packages.py`
  -> final-bytes 174 tests passed，267.372s。
- `python3 -m py_compile
  trellis/skills/guru-team/tests/test_skill_packages.py` -> passed。
- 定向 current-section wording scan：historical qualifier、current active target、
  target-owned authoring seed/package/schema/profile fields、#131 seed、only planned
  finalization route 和 11/42 closure 均命中；未限定旧 current planned/missing
  anchors 为零 -> passed。
- `git diff --check` -> final-bytes passed。

按 Round 4 handoff 未重复 runtime 570-test suite、preset 54-test suite、
publication/Branch Review package suites、actual-wrapper eval 或 throwaway
install/update/reapply；这些完整链路由上一轮 fresh Phase 2 覆盖，本轮只改变 durable
requirements wording、其定向 regression 与 task-local handoff。Exact remote-branch
marketplace verification、真实平台 CLI、#118 finalization、commit/push/PR/archive
仍有意未执行。

### 8.4 交给下一轮 `trellis-check`

下一轮独立 Phase 2 应重点确认：

1. current Branch Review section 对 #131 historical bridge 与 #116 active contract
   的时态/所有权无歧义；
2. scanner 确实只审查 current section，允许明确 historical/task-archive 事实，并拒绝
   current section 中未限定的 planned/missing 旧文案；
3. current 唯一 planned/missing route 仍是
   `guru-review-task-publication:ready -> guru-finalize-task`，没有实现或越权定义
   #118 target；
4. Docs SSOT `task_delta_merged` 可在 fresh full-scope semantic review 后收敛为 true；
5. 本轮三文件增量未影响此前 F-001 至 F-005 closure、distribution、upgrade/update、
   安全、部署或 frozen scope。

本实现代理不记录新的 `phase2-check.json`；现有 artifact 在本轮 docs/test/handoff
变更后应视为历史 `implementation_required` evidence，必须由独立 check 重新完整复检。

## 9. Branch Review finding-fix：BR116-R02-P2-01

### 9.1 修复结论与实现范围

Branch Review Round 2 的 `BR116-R02-P2-01` 已在实现边界修复。此前
publication checker 把整个 current task prefix 与整个
`.trellis/.runtime/` prefix 都视为 metadata，因此普通
`.trellis/tasks/<task>/debug-note.md` 也能绕过
`review_range_and_working_tree`。修复后：

- publication task metadata 直接复用 Branch Review 的 exact allowlist：
  `agent-assignment.json`、`review.md`、`review-gate.json`、assignment 引用的
  `reviews/*.md`，以及唯一的 current-HEAD completed
  `task-commit-plans/NNN.json`；
- publication 只额外允许 `issue-scope-ledger.json`、`pr-body.md` 与
  `finish-summary-index.json`；
- `pr-readiness.json` 继续作为 recorder-owned artifact 从自身 repository
  snapshot 排除；
- runtime path 只在当前 public invocation 显式传入且为
  `.trellis/.runtime/guru-team/` 下 regular file 时允许，runtime prefix 本身不再
  构成 allowlist；
- 任何其他 task-local、runtime 或 repository status path 都记录 failed
  `review_range_and_working_tree`，从而阻止 `ready`；
- finalization augmentation 仍只允许专用调用显式传入当前 task 的 regular
  `closeout-plan.json`。任意其他 `finalization_owned_paths` 值不会扩大
  allowlist；随后原有 exact repository delta、plan digest 和十二项 entry
  binding 复核仍全部执行。

实现没有修改 public input/output schema、Interface 1.3、typed exits、
consumer mapping 或 `publication_ref` 语义。Semantic route、finding、充分性与
issue closure 继续由 AI owner 判断；新增逻辑只校验客观 status path membership。

### 9.2 文件与同步结果

本轮实现拥有并修改：

- canonical runtime 与测试：
  `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`、
  `test_guru_team_trellis.py`；
- installed runtime：
  `.trellis/guru-team/scripts/python/guru_team_trellis.py`；
- canonical package contract：
  `trellis/skills/guru-team/packages/guru-review-task-publication/references/contract.md`；
- preset 生成的 shared/Codex/Claude/Cursor package contract copies；
- durable spec：
  `.trellis/spec/workflow/skill-package-contract.md`；
- preset 生成的 `.trellis/guru-team/extension.json`；
- 本 task-local `implementation-handoff.md`。

通过 `apply.sh --repo . --all-platforms --json` 同步后，canonical/installed
runtime byte-identical；canonical contract 与
`.trellis/guru-team/skills/packages/`、`.agents/`、`.codex/`、`.claude/`、
`.cursor/` 五份 copy byte-identical。首次 contract/runtime 同步分别生成 6 个和
1 个 managed `.bak`；每个 sidecar 都已逐一确认等于同步前版本且不同于新副本，
随后仅删除这些 exact sidecar。最终 reapply 为 `status=ok`、无新 update/backup，
installed manifest 为 2100 managed files，0 sidecar、0 removal、0 conflict。

未修改 planning docs、issue ledger、Branch Review report/gate 或 assignment；
这些 task metadata 的并行变更由主会话拥有。未 commit、push、创建/更新 PR、
关闭 issue、archive 或 finalize。

### 9.3 Docs SSOT Plan reconciliation

策略继续使用批准的 `ssot_first`。本 finding 的 durable task delta 已合并到：

- package step-local contract：定义 publication closed status allowlist；
- `.trellis/spec/workflow/skill-package-contract.md`：定义相同的公共 durable
  workflow contract。

既有 durable contract 已定义 finalization 只能增补 exact validated
`closeout-plan.json`，本轮 runtime 按该 SSOT 保留专用 finalization-owned
projection，没有建立新的平行规则。Public I/O 未变化，因此不需要 schema/interface
迁移。Task-history-only 内容只有本节的 finding、同步与验证轨迹；没有未合并的 durable
docs delta。当前 PR limitation 仍是分支尚未 push，无法验证 exact remote branch
marketplace source；本轮 fresh throwaway 使用 local unpublished workflow sample。

Durable implementation inputs 是 package contract、workflow Skill I/O SSOT 与既有
finalization augmentation contract；task delta input 是
`BR116-R02-P2-01` 对 coarse task/runtime prefix allowlist 的正常路径复现。

### 9.4 验证证据

- 定向 runtime regression：4/4 passed；覆盖普通 `debug-note.md` 被拒绝、exact
  publication metadata 与显式 runtime input 被接受、`pr-readiness.json`
  self-exclusion、exact `closeout-plan.json` 专用增补、任意其他
  finalization-owned 值不能扩张 allowlist、finalization exact positive/negative
  delta 与 stale public wrapper。
- canonical / installed publication package contract：各 16/16 passed。
- 最终 full runtime：571/571 passed，13 skipped，173.603s。
- 最终 full Skill package：174/174 passed，275.466s。
- 最终 preset installer：45/45 passed，93.226s。
- upstream ownership tests：9/9 passed；validator 为 43 active、0 removed、
  13 managed claims。
- source / installed package validator：均 passed，11 active Skills、42 exits、
  25 targets；installed 为 2100 managed、0 sidecar/removal/conflict。
- source / installed publication shared actual-wrapper eval：最终各 7/7 passed。
- `python3 -m py_compile`：canonical runtime/test 与 installed runtime passed。
- `check-dogfood-overlay-drift.sh`、canonical/installed/platform byte parity、
  recursive `.bak/.new` scan、`git diff --check`：均 passed，sidecar=0。
- fresh
  `TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1
  ./trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`：
  最终 exit 0，覆盖 clean init/install、initial closeout、`trellis update`、
  workflow/preset reapply、after-update closeout、developer/no-developer、
  pre-upgrade/absence、source/installed validator、ownership/drift 与 marketplace
  discovery，终态输出
  `Verified public marketplace discovery plus local unpublished workflow sample`。

fresh throwaway 的第一次运行曾真实发现专用 finalization recheck 没有把
`closeout-plan.json` 投影给新 allowlist，因而在 initial closeout fail closed。
修复为仅显式接受 exact current-task plan 后，定向/full suites 和全新 throwaway
全部重跑通过；没有把 `closeout-plan.json` 加入普通 publication metadata
allowlist，也没有放宽其他 status path。

### 9.5 交给下一轮 `trellis-check`

下一轮独立 Phase 2 应重点复核：

1. `debug-note.md` 等普通 task-local 文件、未显式 runtime 文件和任意 repo path
   均使 ready fail closed；
2. exact Branch Review metadata reuse、publication 三文件增量、runtime direct input
   与 `pr-readiness.json` self-exclusion 没有重复或扩大；
3. finalization 只有专用调用的 exact regular `closeout-plan.json` 被接受，且仍需
   exact repository delta、digest 与十二项 entry binding 重算；
4. public I/O、semantic/script boundary、typed-exit consumers 与 #118 planned
   finalization ownership未变化；
5. canonical、installed、三平台 copies、extension manifest、upgrade/update 和
   zero-sidecar 状态与本 handoff 一致。

本实现代理不执行 `trellis-check`、不记录 `phase2-check.json`、不执行 Branch
Review Gate。需要独立 check 对当前未提交 diff 做 fresh full-scope semantic review；
之后再由主会话决定 finding-fix commit 与新的 closure Branch Review。

## 10. Phase 2 Round 6 finding-fix：PH2-116-R6-P2-01

### 10.1 修复结论、根因与相邻审计

`PH2-116-R6-P2-01` 已在实现边界修复。publication repository binding 此前调用
`git_status_paths(root)`；当正常 `git status --porcelain=v1 -z` 命令失败时，该
helper 默认返回空列表，导致真实存在的 unexpected dirty task-local file 被错误投影为
clean repository state。修复后 `task_publication_repository_binding()` 使用既有
`git_status_paths(root, fail_closed=True)`，status 读取失败会以
`Could not inspect Git status paths` 阻断：

- publication repository binding；
- publication review entry 的 `review_range_and_working_tree`；
- `ready` payload checker；
- finalization augmentation recheck。

新增 regression 使用真实临时 Git repository 和真实
`.trellis/tasks/fixture/debug-note.md`，只把 `git status` 的 subprocess 返回模拟为
exit 128；没有手工伪造 binding、artifact、digest 或 status path。修复前现场复现为
`status_paths=[]` 且 `debug_note_exists=True`，修复后上述四层均 fail closed。

相邻调用审计确认：publication runtime block 内只有
`task_publication_repository_binding()` 直接读取 `git_status_paths`；
recorder、checker 与 finalization 均复用该 binding/entry builder，不存在第二个同类
漏点。相邻 Branch Review entry 已使用
`git_status_paths(root, fail_closed=True)`。因此本 finding 只需当前一行 runtime
语义修正与回归覆盖，不扩大到其他 helper 或流程。

### 10.2 文件与同步结果

本轮实现拥有并修改：

- canonical runtime 与 regression：
  `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`、
  `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`；
- preset 生成的 installed runtime：
  `.trellis/guru-team/scripts/python/guru_team_trellis.py`；
- preset 重算的 `.trellis/guru-team/extension.json`；
- 本 task-local `implementation-handoff.md`。

installed runtime 通过
`trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms --json`
生成，没有手工修改。首次 apply 生成的唯一 runtime `.bak` 已逐字确认是同步前版本，
且 diff 只有本 finding 的 `fail_closed=True` 变化后删除。最终 reapply 为
`status=ok`、`updated_managed=[]`、`managed_backups=[]`、`new_copies=[]`；
installed manifest 为 2100 managed files，0 sidecar、0 removal、0 conflict。
canonical/installed runtime byte-identical，recursive `.bak/.new/.orig` scan 为零。

未修改 public schema、Interface 1.3、typed exits、consumer mapping、publication
allowlist、finalization-owned projection 或 finding/route semantic ownership。未执行
recorder/checker、Branch Review Gate、commit、push、PR/issue 更新、archive 或
finalization。工作树中其他 task metadata、durable contract 与平台 contract copy 的
变更来自此前轮次或主会话，不属于本 finding-fix 的新增所有权。

### 10.3 Docs SSOT Plan reconciliation

策略继续使用批准的 `ssot_first`。Durable package/workflow contracts 已明确：
publication 对完整 repository status paths 执行 closed allowlist 校验，无法读取或
证明时必须 fail closed。本轮实现输入首先采用这些 durable SSOT，再用 Round 6
finding 作为 task delta 验证 runtime 是否兑现合同。

因此无需新的 durable docs/spec/overlay 文案：本轮只修复实现与既有 SSOT 的偏差，
没有引入 public I/O、schema、exit、consumer 或 ownership 变化。Task-history-only
内容是 Round 6 raw finding、修复复现、命令选择纠正与本节 handoff；没有待合并的
durable docs delta。当前 PR limitation 仍是分支未 push，无法验证 exact remote
branch marketplace source；fresh throwaway 使用允许的 public-marketplace sample
与 local unpublished workflow sample。

### 10.4 验证证据

- 新增 fail-closed regression：1/1 passed，0.199s。
- 最终定向 publication allow/reject/finalization/stale-wrapper 组合：5/5 passed，
  0.561s。
- full runtime：Ran 572 tests，OK（13 skipped），174.545s。
- full Skill package：174/174 passed，275.961s。
- preset installer：45/45 passed，93.260s。
- upstream ownership：9/9 passed，0.739s。
- canonical / installed publication package contract：各 16/16 passed。
- source / installed package validator：均 passed，11 active Skills、42 exits、
  25 targets；installed 为 2100 managed、0 sidecar/removal/conflict。
- source / installed publication shared actual-wrapper eval：各 7/7 passed。
- canonical runtime/test 与 installed runtime `py_compile`、source/installed byte
  parity、dogfood overlay drift、recursive sidecar scan、`git diff --check`：均
  passed。
- fresh
  `TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1
  ./trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`：
  exit 0。覆盖 clean init/install、initial closeout、`trellis update`、
  workflow/preset reapply、updated closeout、developer/no-developer、
  pre-upgrade/absence、source/installed validator、ownership/drift 与 marketplace
  discovery；updated closeout 在 issue #106 上 archive/local/remote/PR heads
  一致且 PR ready。终态输出
  `Verified public marketplace discovery plus local unpublished workflow sample`。

定向测试编排曾两次使用不存在或错误 class 的 selector，分别产生 unittest loader
error；纠正为真实 test id 后，上述 5/5 组合通过。这是测试命令选择错误，不是产品
失败，也没有用错误 selector 的结果替代验证。

### 10.5 交给下一轮 `trellis-check`

下一轮独立 Phase 2 应重点复核：

1. 正常 `git status` nonzero 时 publication binding、entry、ready checker 与
   finalization augmentation 均 fail closed，且错误不是被投影为空 status；
2. 成功读取 status 时既有 exact metadata allowlist、unexpected-path reject、
   `pr-readiness.json` self-exclusion 和 exact `closeout-plan.json` augmentation
   语义未回归；
3. publication block 不存在相邻的默认-open `git_status_paths` 调用，Branch Review
   已保持 fail-closed；
4. canonical/installed runtime、extension manifest、2100 managed/zero sidecar、
   update/reapply 与 fresh throwaway evidence 一致；
5. Docs SSOT 无新增 delta，public contract、semantic/script boundary 与 #118
   planned finalization ownership均未改变。

本实现代理不执行 `trellis-check`、不记录或更新 `phase2-check.json`，也不执行
Branch Review Gate。需要独立 checker 对当前未提交 full diff 做 fresh semantic
review，再由主会话决定后续 finding-fix commit 与 closure review。

## 11. Branch Review Round 4 finding-fix：BR116-R04-P1-01

### 11.1 修复结论、根因闭环与边界

`BR116-R04-P1-01` 已在实现边界修复。publication package 的 recorder/checker
此前只剥离 canonical source suffix；installed shared 与 `.agents`、`.codex`、
`.cursor`、`.claude` package root 均被误当作 repo root，因而在 package 内错误
拼接 `.trellis/guru-team/scripts/bash/run-skill-command.sh`。两个 wrapper 现在复用
`invoke.sh` 与 Branch Review package 已有的六布局 exact resolver：

- canonical `trellis/skills/guru-team/packages/`；
- installed shared `.trellis/guru-team/skills/packages/`；
- `.agents/skills/`、`.codex/skills/`、`.cursor/skills/`、`.claude/skills/`。

未知布局保持 fail closed；新增 regression 把完整 package copy 到任意临时路径，
在未设置 `GURU_TEAM_DISPATCHER` override 时验证两个命令均拒绝执行。

resolver 修复后的直接正常路径又暴露出同一交付链的确定性遗漏：extension public
API 已声明 `record-task-publication-review` 与
`check-task-publication-review`，但 preset 的 `MANAGED_ASSET_PATHS` 和 executable
清单未安装两条 workflow runtime wrapper。correct dispatcher 因而继续以
`mapped Skill runtime command ... missing` fail closed。两条 exact runtime
wrapper 已纳入 installer managed assets，并增加安装存在性与 executable mode
断言；这是完成 finding 所要求的 fresh install/update/reapply runnable parity，
没有新增 public API、semantic judgment 或 route。

### 11.2 文件、同步与副作用

本轮实现拥有并修改：

- canonical package：
  `trellis/skills/guru-team/packages/guru-review-task-publication/scripts/record-task-publication-review.sh`、
  `scripts/check-task-publication-review.sh`、`tests/test_contract.py`；
- preset installer 与开箱即用验证：
  `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`、
  `test_apply_guru_team_trellis_preset.py`、`test_upstream_ownership.py`、
  `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`；
- preset 生成的 installed shared 与四平台 package 同名副本；
- preset 新安装的
  `.trellis/guru-team/scripts/bash/record-task-publication-review.sh` 与
  `check-task-publication-review.sh`；
- preset 重算的 `.trellis/guru-team/extension.json`；
- 本 task-local `implementation-handoff.md`。

第一次 package 同步按 managed-file 规则为三个已安装 package 文件生成 15 个
`.bak`；确认它们只对应本轮三文件的旧版本后逐个删除，再次 apply 为
`status=ok`。最终 canonical、installed shared 与四平台三个 package 文件
byte-identical、mode 一致；两条 canonical/installed runtime wrapper
byte-identical且均为 executable。installed manifest 为 94 个 managed assets、
2100 个 Skill files，0 sidecar、0 conflict、0 removal；ownership stable facts
更新为 50 个 managed assets。

未修改 planning docs、public schema、Interface 1.3、typed exits、consumer mapping、
publication semantic dimensions、review artifact、review gate、assignment、commit
plan 或 issue ledger。未执行 `trellis-check`、本 task 正式 publication
recorder/checker gate、commit、push、PR/issue 更新、archive 或 finalization。
任务目录中主会话拥有的并行 metadata 与 Round 3/4 raw report 保持原样。

### 11.3 Docs SSOT Plan reconciliation

策略继续使用批准的 `ssot_first`。Durable installer 与 Skill package contracts
已明确要求 active package 的 runtime commands、installed shared 与平台 copies
在 fresh install、`trellis update`、preset reapply 后均真实可运行；本轮以这些
durable SSOT 为主实现输入，以 `BR116-R04-P1-01` 的普通安装复现作为 task delta。

因此无需新的 durable docs/spec/overlay 文案：本轮只修复实现和 installer inventory
对既有 runnable/OOTB SSOT 的偏差，没有改变 public I/O、schema、exit、consumer
或 ownership。Task-history-only 内容是 Round 4 finding、resolver/runtime asset
根因闭环、sidecar 处理、验证轨迹与本节；没有待合并的 durable docs delta。当前
PR limitation 仍是分支未 push，无法验证 exact remote candidate-branch
marketplace source；fresh throwaway 使用允许的 public marketplace sample 与
local unpublished workflow sample。

### 11.4 验证证据

- canonical / installed publication package contract：各 18/18 passed；
  canonical 运行 10.034s，installed 运行 10.507s。新增测试从 `interface.json`
  读取 recorder/checker exact command，在未设置 dispatcher override 时执行六布局，
  并覆盖任意未知布局拒绝。
- direct validator wrapper：canonical recorder/checker 2/2 到达 dispatcher 后按
  canonical 非 installed audited layout 合同返回 rc=2；installed shared 与四平台
  recorder/checker 10/10 返回 rc=0 并显示各自 mapped runtime help。
- full runtime：572/572 passed，13 skipped，167.485s。
- full Skill package：174/174 passed，272.583s。
- preset installer：45/45 passed，84.769s。
- upstream ownership：9/9 passed，0.681s；validator `status=ok`，managed asset
  count=50，facts digest=`738ffab55b80bfec2b5e482d6d25591d30e46d2d5264590b5be61ee56a43f801`。
- source / installed package validator：均 passed，11 active Skills、42 exits、
  25 targets；installed 为 2100 managed、0 sidecar/removal/conflict。
- source / installed publication shared actual-wrapper eval：各 7/7 passed。
- fresh
  `TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1
  ./trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`：
  最终 exit 0；fresh install、`trellis update --force`、preset reapply 三阶段
  recorder/checker smoke 各为 10/10，随后完整通过 existing closeout/eval、
  pre-upgrade/absence、ownership/drift 与 marketplace discovery，终态输出
  `Verified public marketplace discovery plus local unpublished workflow sample`。
- final `bash -n`、`python3 -m py_compile`、canonical/installed/platform byte 与
  mode parity、planning approval、dogfood overlay drift、recursive
  `.bak/.new/.orig` scan、`git diff --check`：均 passed。

定向 package 回归首次运行在 resolver 已正确到达 dispatcher 后，真实暴露两条
installed runtime wrappers 未被 preset 安装；补齐 managed assets 后通过。fresh
throwaway 首次重跑只因 embedded manifest 仍固定断言 92 个 assets 而失败，按新增
两条 exact assets 更新为 94 后从全新临时仓库完整重跑通过。这两次失败均被保留为
安装链覆盖证据，没有用局部测试替代最终 clean throwaway。

### 11.5 交给下一轮 `trellis-check`

下一轮独立 Phase 2 应重点复核：

1. recorder/checker 的六布局 resolver 与 `invoke.sh`、Branch Review package
   既有模式一致，未知布局仍 fail closed；
2. 测试实际执行 `interface.json` 声明的两个 validator commands，且没有隐藏
   `GURU_TEAM_DISPATCHER` override；
3. 两条 publication workflow runtime wrappers 是 preset managed/executable
   assets，fresh install、update、reapply 后 installed shared 与四平台 10 条命令
   均到达 shared dispatcher；
4. public I/O、semantic/script boundary、typed exits、consumer mapping 与
   publication semantic gate 没有变化；
5. canonical/installed/platform parity、manifest 94 assets/2100 Skill files、
   ownership 50 assets、zero-sidecar 与 full throwaway evidence 一致。

本实现代理不执行 `trellis-check`、不记录或更新 `phase2-check.json`，也不执行
Branch Review Gate。需要独立 checker 对当前未提交 full diff 做 fresh semantic
review，再由主会话决定 finding-fix commit 与同 finding owner closure review。

## 12. Phase 2 Round 8 finding-fix（PH2-116-R8-P2-01）

Round 8 唯一 P2 finding 是 preset 测试仍以源码字符串断言 throwaway verifier
包含 `assert len(assets) == 92`，而已经批准并通过前序验证的 verifier、installer
manifest 与 runtime wrapper inventory 均为 94。本轮只把该测试期望同步为 94，
未改变 runtime、installer、managed assets、public I/O、Docs、review/gate、
assignment、commit plan 或 issue scope 行为。

Docs SSOT Plan 继续执行 `ssot_first`：实现输入仍以现有 durable installer、
Skill package、workflow/data/companion contracts 为准；本轮没有新的 durable
docs/spec/overlay delta。仅本节作为 task-history-only finding-fix 记录。分支尚未
push，exact remote candidate-branch marketplace source 的当前 PR limitation
保持不变。

本轮重新执行 Round 8 报告的精确失败 selector、完整 preset 45 项、canonical /
installed shared / 四平台两条 direct wrapper、upstream ownership 9 项及 validator、
source / installed package validator、dogfood overlay drift、sidecar scan、
`git diff --check`、planning approval 与 workspace boundary。结果为：精确
selector 1/1 passed（0.002s），完整 preset 45/45 passed（84.418s）；
canonical 两条 direct wrapper 均按审计布局合同返回 rc=2，installed shared 与
四平台共 10 条均返回 rc=0；ownership 9/9 passed（0.692s）且 validator
`status=ok`、managed assets=50；source / installed package validator 均
passed（11 active Skills、42 exits、25 targets），installed 仍为 2100 managed
files、0 sidecar/removal/conflict；dogfood overlay 无漂移，递归 sidecar 与过期
`assert len(assets) == 92` 均为 0，diff/planning/boundary 均通过，source checkout
保持 clean。

实现代理不重复完整 runtime、完整 Skill package 或 throwaway；Round 8 已记录终态证据：
runtime 572/572 passed（13 skipped）、Skill package 174/174 passed、throwaway
exit 0 且 fresh/update/reapply 三阶段各 10/10。fresh Phase 2 必须重新执行其完整
语义检查矩阵，并重点确认测试源码不再含 92 的过期期望且本轮没有实现行为变化。

## 13. Publication return adoption 与 Phase 2 Round 10 finding-fix

### 13.1 Finding 承接、根因与实现结论

本轮 implementation role 已正式承接 publication `return_to_task_work` 的
`PUB116-TW1`、`PUB116-TW2`，以及 formal Phase 2 Round 10 唯一 finding
`PH2-116-R10-P2-01`。Round 10 对代码、installed copy、全量 suites、分发和
throwaway 的结论是技术修复成立；该 finding 的剩余缺口是 publication return 后
没有 current implementer adoption/completed evidence，也没有 current
implementation handoff。本节补齐 owner handoff，并对现有实现做 fresh 独立核验。

根因是 Phase 3.6 publication review 按合同补齐
`issue-scope-ledger.json.acceptance_evidence` 与固定 pending
`remote_marketplace_verification` 后，旧 Phase 2
`requirement_provenance` 仍绑定 ledger 全文件 digest。Planning 已按
primary/close/related/follow-up issue number-set 建立 scope identity，因此合法的
publication metadata revision 被错误判为 requirement scope stale，阻断了
metadata-only revision loop。

现有 `phase2_requirement_artifact_digest()` 修复已被本 implementation role
adopt，运行时代码无需再次修改。它只在下列两个条件同时成立时复用
`planning_scope_ledger_projection()`：

1. `phase2_evidence_projection()` 的 label 精确为
   `requirement_provenance`；
2. artifact basename 为 `issue-scope-ledger.json`，且 repo-relative path
   位于 `.trellis/tasks/**`。

其它 evidence label、非 task-local 同名 ledger 继续使用
`phase2_path_digest()` 的 full digest；task-local ledger 缺少合法 primary 或完整
issue number-set 时，`planning_scope_ledger_projection()` 以
`WorkflowError(exit_code=2)` fail closed。Helper 只计算确定性 identity/freshness，
不判断 issue scope、finding、adequacy、revision action 或 route。Public Skill
input/output、schema id、typed exits、consumer mapping、publication semantic
dimensions 与 workflow route 均未改变。

### 13.2 文件 adoption、修改与生成边界

本轮授权文件的状态如下：

- adopted、运行时代码未再修改：
  `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`、
  `.trellis/guru-team/scripts/python/guru_team_trellis.py`。两者 SHA-256 均为
  `f7a043e184776c868014050806fc8b9a39e358fc816c9bd7cf38ce4c406498c9`，
  各 `1545787` bytes，mode 均为 `755`，byte-identical；
- modified：
  `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`。
  保留已有 positive/negative regression，并在同一个 test 内补齐其它 label、
  非 task-local ledger 与非法 ledger 三项边界；SHA-256
  `3339b699598a17b725bd1606d61b641f49802064a1079c42bfcdeaaf17768f70`，
  `1169659` bytes；
- deterministic refresh：
  `.trellis/guru-team/extension.json` 仅由 final preset apply 重算；
  `installed_at=2026-07-25T06:12:13Z`，source 仍绑定
  `codex/116-review-task-publication@d7ab98f5c53f470f4d3f3742f8cfca24f8465edd`
  与 dirty tree；SHA-256
  `50b7ee6c0353173d001553f73ad707f8695b1c05c0a0954667a6d93572f4cf5b`，
  `817448` bytes；
- modified task-history-only：
  本 `implementation-handoff.md` 新增 Section 13。

未修改 planning、issue ledger、Phase 2 raw report/gate、publication
gate/body/index、Branch Review artifact、agent assignment、commit plan 或其它
文件。工作树中这些既有并行变更均被保留；source checkout
`/Users/wumengye/Documents/GoProjects/guru-trellis` 仍为
`main@bdc8f50bcd1e325aed331d4b01107b83ed8ee940` 且 clean。

### 13.3 Projection normal-path matrix 与验证

同一 targeted regression 现在固定以下矩阵：

| Case | 预期与结果 |
| --- | --- |
| task-local requirement provenance 增加 acceptance 文本和 pending remote object | projection 完全相等，不 stale |
| task-local requirement provenance 修改 related issue number-set | artifact projection 改变，scope drift fail closed |
| 同一 task-local ledger 使用 `implementation_handoff` label | metadata 变化导致 full digest 改变 |
| repo root 同名 ledger 使用 `requirement_provenance` label | metadata 变化导致 full digest 改变 |
| task-local ledger 的 primary issue number 非法 | `WorkflowError(exit_code=2)`，不降级为 full digest 或空 projection |

本 implementation role 独立执行：

- `python3
  trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py
  PlanningAndPhase2GateTest.test_phase2_requirement_provenance_uses_scope_only_ledger_projection`：
  1/1 passed，0.023s；
- canonical runtime、扩展 regression 与 installed runtime 的
  `python3 -m py_compile`：passed；
- canonical/installed runtime SHA、byte、mode parity：passed；
- 授权五文件 `git diff --check`：passed；
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`：
  `status=ok`，zero drift；
- recursive `.bak/.new/.orig` scan：0；
- source checkout boundary：clean，未被本代理触碰。

Round 10 的 fresh full evidence 可继续作为 adoption 的 broad baseline：
runtime 573 tests（13 skipped）、Skill package 174、preset 45、ownership 9、
publication contract 18x2、eval 7x2 与完整 throwaway 均通过。本轮扩展了既有
single regression 的断言但没有增加 test case count；没有用 Round 10 的旧 full
结果冒充修改后的 full rerun。下一轮独立 Phase 2 必须重新执行完整 suite，预期仍
为 runtime 573 tests，并把 fresh 输出写入新的 raw report。

### 13.4 Final all-platform apply、Docs SSOT 与影响

最终执行
`trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms --json`
得到 exit 0、`status=ok`、`all_platforms=true`，selected platforms 为
Claude/Codex/Cursor。Manifest 当前为 94 managed assets、2100 managed Skill
files；2100 项 action 全为 `unchanged`，`installed=[]`、
`updated_managed=[]`、`new_copies=[]`、`managed_backups=[]`，Skill package
removal/conflict/sidecar 均为 0。Public `.agents` copy 与 installed shared copy
继续由同一 all-platform install 收敛。

Docs SSOT Plan 继续使用已批准的 `ssot_first`。Durable workflow、data、
companion-script、quality 与 Skill package contracts 已经定义 metadata-only
publication revision、Phase 2 freshness、scope drift fail-closed 与
semantic/script boundary；本轮只让 deterministic runtime 和 regression 兑现现有
合同，没有新的 durable docs/spec/overlay delta。官方 Trellis 当前合同仍把
`.trellis/workflow.md` 作为 workflow behavior SSOT，并要求 marketplace 内容可复用
及通过 throwaway 验证；本修复没有修改 upstream Trellis、全局 npm 或
`node_modules`。

新增代码不读取 secret、客户数据、`.env`、签名 URL 或远端 payload；无 CI/CD、
container、K8s、DB migration、Makefile、dependency、配置或生产部署影响。Exact
remote candidate-branch marketplace ref 仍无法验证，因为分支未 push；这是
`UV-R10-01` 的 non-blocking/out-of-scope limitation，由后续 publish/finalization
gate 拥有，不能以 public marketplace sample 冒充 exact remote evidence。

### 13.5 未执行副作用与下一轮 fresh Phase 2 交接

本 implementation role 未调用 Phase 2 recorder/checker，未改
`phase2-check.json`，未执行 task commit、Branch Review Gate、publication
stale re-entry、push、PR/Issue mutation、remote verifier、archive、finish、
finalization、deploy 或 production write。

下一轮必须使用新的独立 checker identity 对完整
`origin/main...HEAD`、当前未提交 diff、Section 13 与 assignment completed evidence
做 fresh full Phase 2，重点确认：

1. `PUB116-TW1` / `PUB116-TW2` 的 scope-only projection 在五项 matrix 中成立，
   `PH2-116-R10-P2-01` 已由 current implementer adoption/handoff 关闭；
2. modified regression 的完整 runtime suite fresh 通过，且 canonical/installed
   runtime、94 assets、2100 Skill files、zero drift/sidecar 保持一致；
3. planning authority、issue number-set 与 Docs SSOT 没有 drift，public I/O 和
   semantic/script boundary 未变化；
4. remote exact-ref limitation 被如实保留，不授权任何发布副作用。

只有 fresh full Phase 2 记录 `passed` 后，主会话才能进入 finding-fix commit，
随后重新执行完整 Branch Review lifecycle 和 publication stale re-entry。
