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
