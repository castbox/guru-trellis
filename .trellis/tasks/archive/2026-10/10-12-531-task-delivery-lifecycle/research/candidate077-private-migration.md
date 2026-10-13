# Research: 新上游 077bb029 候选与 Guru 私有迁移边界

- Query: #531 对接新上游候选的 Plan 2.0、私有 cycle/DTO/checkpoint/事务/history 迁移缺口及 #149/#444/#155 合法受控前序。
- Scope: mixed；当前 Guru canonical 与旧完整运行副本、固定上游 installed 包、上游交接/迁移合同。
- Date: 2026-10-13
- 性质：研究定位，非 Planning/Architecture/Check gate、实现完成或 joint readiness。未执行迁移、安装、远端 Publish/Merge；未切换当前 #531 Task。

## Findings

### 1. 当前来源与事实边界

已读当前 AGENTS.md、`.trellis/workflow.md` 的 continuation、Task `prd.md`/`design.md`/`implement.md`，以及 canonical `trellis/presets/guru-team/spec/workflow/task-delivery-migration.md`。当前 Task 仍由旧完整 workflow 按 `task.json.status` 路由；其恢复 owner 是 Phase 2 Architecture → Check。canonical 新流程与该 Task 的执行安装不是同一件事。

指定 `.trellis/spec/workflow/task-delivery-migration.md` 当前未安装；不能把 canonical 文件当当前 dogfood 已采用的证据。canonical migration spec、approved planning 都仍绑定旧 ce363 候选，需由原 Planning/Architecture owner 对新候选和私有迁移机制重绑定，不由研究者改写准入快照。

新候选来自 `/tmp/trellis31-goal-candidate-slmnvfq2/candidate.json`：

| 身份 | 实际值 |
| --- | --- |
| source fingerprint | `077bb02966156b10f5d7477fedd9d6f8c2953dcd113434cf2ff48393307f2c25` |
| source HEAD | `a85ce75cf6ab52bafce7bcc9c4b6118ce911a0d2`，另有 manifest 明确 fingerprint 的未提交增量，HEAD 本身不识别候选 |
| API/schema/package | Delivery API 1.0 / Task schema 2.0 / 0.7.0-castbox.3 |
| CLI tar SHA | `d09b905a539a0f695d2d2d603eeb20fdd925e98d81f710f04af754fed013e20d` |
| Core tar SHA | `45bbfee507ed4964649610f703a90ba01c5f5cea21fb95d0845f92ed45302967` |

交接正文报告 B05 已修复、实际 native/migrated-native/migrated-custom continuation 成功。研究已读取 installed 新 extractor/迁移 API 的来源，不沿用 ce363 失败断言当前阻塞；本研究未独立重跑这些执行结果，不代填 Guru joint pass。

### 2. 实际 API 与唯一 consumer

以下路径前缀 U = `/tmp/trellis31-goal-candidate-slmnvfq2/installed/node_modules/@mindfoldhq/trellis`，C = 同目录 `@mindfoldhq/trellis-core`。

| 实际接口 | 签名与 consumer |
| --- | --- |
| C `dist/task/migration-v2.d.ts` | `validateTaskV2Projection(source: unknown, projection: unknown): TaskRecordV2`；校验原 owner 给定完整 v2 record 的身份、generation、metadata/tree 保留及阶段所需 current gate。不是状态推导器/归属器。 |
| U `dist/commands/migration2.d.ts` | `collectMigration2Templates(root: string, reviewedSources?: ReadonlyMap<string, RawSnapshot \| null>): Map<string,string>`；prospective collector，无 installed-runtime preflight、下载或写入。 |
| 同上 | `migration2TemplateCandidate(files: Map<string,string>): {candidate_sha256, files: {path,sha256,mode}[]}`；提供冻结 templates 身份给 private Plan2 executor。 |
| 同上 | `migrate2(options: MigrateOptions, input: unknown): Promise<MigrationResult>`；由正式 CLI `migrate --from <actual-installed-version> --plan <private-file> [--dry-run]` 根据 `schema_version: 2.0` 分流。 |
| U `dist/templates/trellis/scripts/common/delivery_store.py:58` | `candidate_content_ref(root: Path, paths: list[str], kind: str \| None = None) -> str`；调用方应传 profile 明确 kind，Git 路径使用 executable-normalized mode，git_free 使用实际 0777 permissions。 |
| 同文件 `:97` | `verify_candidate(root: Path, value: dict) -> None`；按 candidate.kind 重算，git 模式另核验实际 HEAD/base。 |
| Guru `runtime/delivery_projection/adapter.py` | 直接装载目标 `.trellis/scripts/common` 的公共 parser/operations/store/session/runtime_contract；不维护 aggregate/phase。`apply()` 交真实 store，`current()/select()/release()` 交 upstream session。 |

Plan2 闭合字段：`schema_version/source/target/workspaces/installations/tasks/sessions/workflows/templates/files`。

- `source={version,task_schema:legacy|1.0,delivery_api:null}`，`target={version,task_schema:2.0,delivery_api:1.0}`；允许同 package version 的显式 schema cutover。
- workspace 使用实际注册 absolute root 与 project_relative；包括同 repo 对应 suffix 的 sibling roots。
- installation 固定 version/receipt 原 snapshot，不由任意 file decision 替代。
- tasks 每 occupied active/archive leaf 都有 disposition：convert_active/convert_archive/current/defer/history_only；转换才给完整 record。missing-record history_only 可用 source:null，不能造 task record。
- raw snapshot 为 `{content_base64,sha256,mode}`，原 Task bytes/mode 保留为 `<task_ref>/migration/source-task.json`，只作历史。
- 非空旧 commit/pr_url/completedAt 各有 `legacy_facts` producer-owned disposition。completedAt 不能制造 Completion；无法当前归属可明确保留 source_snapshot+reason。
- sessions 枚举所有 common-dir/live local JSON，包括 preserve-only；record 给 schema3。Delivery selection null 或当前 generation 非 terminal identity。没有指定的 session 或后来出现的 session 在写前拒绝。
- workflows 必须显式 `template_id`+contract，与提供的 workflow bytes一致。Guru 为 custom template id，不冒用 bundled native id；custom 移除旧 native workflow receipt key。native 必须实际 bundled rendered bytes相同。
- files 为 typed workspace/project target，owner=template/workflow/artifact/preserve。root planning 明确保留，Delivery planning 新目标由 artifact 写入。每 known artifact 被覆盖；preserve 不授予 write。
- 预检所有 source/target、candidate、authority、session/workflow 之后才写。same-plan 接受精确 source 或 target bytes/modes；third-state 不自动重冻结。

引用：上游 `.trellis/spec/cli/backend/commands-migrate.md` 的 Plan2 段；installed `migration2-schema.js`、`migration2.js:313-394,412-419,502-543,566-614,658-734,776-782`。Core `migration-v2.js` 校验 active implementing/reviewing/publishing 必需 gate applicability，不能由旧 status 自动挑 phase。

### 3. 私有状态归属与目前缺口

| 对象 | 现有 owner/consumer | 可承接能力与缺口 |
| --- | --- | --- |
| 公共 Task/Delivery/session/workflow receipt | upstream Plan2 executor | 上述完整 API 已提供；Guru 不复制模型、schema 或 disposition authority。 |
| TaskBranchBinding/resource ledger/本机 checkout 映射 | Guru task_lifecycle 原 owner | upstream 保留 Task身份/source/generation/branch/worktree metadata；Guru仍需盘点真实 private controls、核验不变 key，保持唯一绑定，不通过目录名重建。 |
| 旧 planning/execution/Check/Review DTO及checkpoint | 各原 semantic producer | 没有 DeliveryKey 的旧输出不静默改名。不可恢复的 current gate 由原 owner fresh 重入；历史提交/远端成功不要求 current pass。尚无有界 private migration entry。 |
| cycle→Delivery归属 | Merge/history + Publish 原 owner | 原 history 可核验 first-parent/two parents/schema1 trailers+GitHub，schema2可返回 key；schema1没有 key。需要原 owner明确每旧cycle/PR/head/generation归属，再把最小结果写公共 migrated record/已有事务恢复输入，不增ledger、不从cycle digest造UUID。 |
| Publish 在途/terminal事务 | guru-publish-task-delivery | owner.py:246-316 已支持新 key 或旧cycle各自事务，source.input被精确绑定；不是自动迁移。`delivery_same_plan_resume`读取旧 source仍可能无key；`unique_task_transaction(...delivery_key)`筛不出旧事务。缺原事务的显式identity migration/恢复输入转换。 |
| Merge 在途/历史成功 | guru-merge-task-delivery | owner.py:393按key/cycle取identity；508-526支持历史record_delivery。旧input/receipt到新 key 的关系仍应由本 owner核验并转换。 |
| Completion/Closure/Finish/Reactivate | 各原 Task closeout owner | 当前新 profiles用 TaskKey；历史成果保留，日期/status不变current completed，generation不重置。旧finished archive转换需足够原Completion/Closure证据；不足则history_only/原owner诊断，不能为了Reactivate补pass。 |
| 包安装/受控rollback | guru-upgrade-installation | 现工具有 exact preimages/modes、source锁、分phase恢复，但实际仍按旧Plan1边界；需受影响Planning明确新机制后改。 |

已发现可定位的安装承接差额：

1. `guru-upgrade-installation/runtime/owner.py:209-213` 在 legacy source 先调用新普通安装的 `diagnose_delivery_installation`；`delivery_installation.py:70-72` 对任何legacy Task拒绝，因此合法Plan2 dry-run也到不了。普通 reapply的拒绝有用；migration preview必须自己核验 prospective Plan2，不能用“已切换安装”的entry precondition挡住来源。
2. `owner.py:418-433` 只理解Plan1 deferred_tasks.expected_sha256、单root直接active record inventory；Plan2的workspace/archive/history_only/session dispositions并未消费。
3. `runtime/files.py:109-114` 的 task_token用单root task_ref拼接，Plan2不能唯一覆盖workspace/ref同名、archive source-history、session与完整preview write set。rollback/preimages必须消费真实Plan2 actions，不能仅备份单root tasks。
4. `owner.py:216-217` 的 target_source_ref只能绑定HEAD；`formal_guru_source()` 对dirty canonical禁止formal source_locked。受控local_candidate应另外冻结完整Guru managed source bytes/modes，不能把本轮dirty candidate称HEAD对应内容，也不能放宽正式发行锁。
5. `delivery_installation.py` 普通apply仍扫描所有legacy并拒绝；上游允许已安装schema2声明下保留old history-only data做reapply。Guru需区别initial cutover与已完成迁移+retained historical identity，不让旧Task进入execution；不能永久dual-read/status fallback。
6. canonical migration spec继续说 D2 尚未提供；后续须按新actual candidate修订能力/exit准入，保留“默认退休尚待matching readiness”。已提供迁移 API 不等于旧私有状态已完成迁移。

### 4. 最小安全顺序（既有accepted scope内建议，未实施）

1. 原 Planning/Architecture owner重绑定两仓精确候选及私有机制，保留D1历史证据来源、不重标旧运行。
2. 在受控副本只读盘点actual version/receipt、全active/archive roots、root planning/artifacts、public/common/local sessions、branch/resource/private controls、各stage checkpoint与在途事务。源树/当前#531 Task不迁。
3. 各原 producer分开核验历史成果、旧cycle归属和当前gate。真实Publish/Merge成功才产生对应 normalized fact；local response fixture只证明投影合同。
4. owner-reviewed完整record使用上游 validator。缺当前pass优先planning phase/no selection，由正确owner fresh gate；已交付历史用terminal facts或source_snapshot，不能伪造前序链。未分配范围仍由整体Completion判断。
5. prospective templates collector固定该installed包；提供Guru customworkflow template_id/contract/bytes，映射Delivery plan bytes同时保留root来源。每session都给明确disposition。私有转换只含明确consumer最小key/事务关联，不能改变upstream phase。
6. 实际CLI dry-run，备份完整raw actions/modes和Guru额外controlled writes；stale停止，既有失败Plan不得自动re-freeze。运行same-plan迁移及私有迁移，成套应用新Guru reader/writer。
7. 读回public Task/current selection、原branch/resource身份、native continuation；后续真实semantic ownersfresh判断。恢复输出丢失由原事务同result，不重复mutation。
8. 定向ordinary reapply/drift/sidecar/rollback验证，以两个frozen候选绑定唯一test实际结果。完整Release矩阵、原会话实际安装恢复和远端动作独立边界。

### 5. #149/#444/#155 的合法受控前序

| 形态 | 迁移前真实旧路径 | 迁移后可观察结果/不得伪造 |
| --- | --- | --- |
| #149 active replan | 真实旧安装Task先正常首次Planning/Activation进入in_progress；已有slice结果/历史保留，再由原Clarify/Author/Approval形成活动后继plan，使用真实owner checkpoint/输出，不能只手改status。 | Task identity/source/generation不变；当前slice获得明确Delivery scope/plan；若无可转换current gate由Planning/Activation fresh进入implementing；不新Task、不reset首次激活，D1旧plan不被覆盖。 |
| #444 clean candidate | 旧安装在Task-root规划处正常实现/check/commit，保留实际HEAD和完整diff、metadata/source；post_commit base整合有真实提交且freshCheck。迁移前没有新Delivery plan路径。 | Plan2原规划bytes映射新planning_root，原HEAD不动；fresh公共Check→clean TaskCommit→首次完整Review。不得用迁移前提前布置新plan路径、metadata/gate空commit或重复commit证明接续。 |
| #155 partial dependency | 真实旧scope有至少两独立consumer场景；一场景正常发现provider事实缺口并blocked，另一场景有独立实际需求/依据。 | 原Task整体义务与blocked事实保留；独立slice合法Planning/实施，不扩provider业务；未满足义务仍阻止整体Completion。不能把dependency缺失改为通过，不能仅两个toyDeliveries宣称原断点恢复。 |

可增加noDelivery Task切换、至少两Delivery、方案返工、全slice撤回stop+release、stdout/DTO丢失以及历史档案reactivate样本；均由原公共/私有owner实调。上游local historical verifier结果不能代替Guru真实远端Publish/Merge成功。

### 6. 待原 owner qualification 的候选（未设severity、未实施）

#### Candidate A：git_free 的 profile显式kind没有传公共hash helper

- candidate_ref: `guru531-candidate077-git-free-kind`。
- observed_behavior: `DeliveryProjection.candidate(...,kind='git_free')` 仍调用 `candidate_content_ref(root,paths)`；helper自动检测Git可能按Git mode算hash，而 `verify_candidate`按显式git_free mode算，正常Git checkout中的非0644/0755文件可不一致。
- locators: Guru `runtime/delivery_projection/adapter.py` 的 candidate()；installed U `common/delivery_store.py:58-84,97-102`。
- minimal_reproduction_hint: 受控Git checkout的实际manual/git_free profile，用正常owner创建permissions 0600或0640的candidate文件，经Guru生成candidate后调用真实installed verify_candidate；不手改artifact/hash。当前Guru declaration是否支持该profile由qualification owner判断。

#### Candidate B：旧clean规划映射的新路径未在原HEAD

- candidate_ref: `guru531-candidate077-migrated-clean-planning-path`。
- observed_behavior: 当前clean_candidate逐一要求新Delivery planning_root下5文件存在HEAD同路径同bytes；Plan2正常从旧Task-root映射的新路径在旧HEAD不存在，会走要求dirty commit的错误出口。仅静态定位，尚未实跑受控#444。
- locators: Guru `guru-create-task-commit/runtime/delivery.py:52-60`；上游 installed migration2.js:522-543,658-679。
- minimal_reproduction_hint: 正常旧安装形成clean已提交候选，保持HEAD完成Plan2 artifact映射/freshCheck，然后实际调用delivery_committed_reentry；记录出口、HEAD前后与新旧规划来源。不得以提前提交未来Delivery目录规避。

## Files Found

- `AGENTS.md` / `.trellis/workflow.md`：当前协作边界与旧Task continuation owner。
- Task `prd.md` / `design.md` / `implement.md`：AC01..09、V06..08、I08和私有状态原owner边界。
- `trellis/presets/guru-team/spec/workflow/task-delivery-migration.md`：canonical迁移支持/退出合同，当前仍旧候选绑定。
- `trellis/presets/guru-team/scripts/python/delivery_installation.py`：普通apply能力诊断，legacy初次切换阻断。
- `trellis/skills/guru-team/packages/guru-upgrade-installation/runtime/{owner,files}.py` 与 `schemas/private-plan.schema.json`：旧upgrade控制面、Plan1形态、source/replay/backup。
- `runtime/delivery_projection/adapter.py`：真实installed public API projection。
- `packages/guru-publish-task-delivery/runtime/owner.py`：cycle/key事务identity与remote成功投影恢复。
- `packages/guru-merge-task-delivery/runtime/{owner,history}.py` 与history query/result schemas：实际GitHub归属核验与历史结果投影。
- `packages/guru-create-task-commit/runtime/delivery.py`：clean committed reentry当前规划路径要求。
- `runtime/task_lifecycle/{identity,session_adapter,results}.py`：Task身份occupation、schema3公共session接续、最小Task DTO。

## External References

- 上游任务研究 `goal-guru-candidate-handoff.md`：完整当前交接，含source/tars/API/schema和已验证边界。
- 上游 `.trellis/spec/cli/backend/commands-migrate.md`：Plan1与Plan2 exact支持合同；spec并未作为独立Markdown安装到tar，实际installed实现/声明已读。
- fixed installed Core `dist/task/migration-v2.{js,d.ts}`；CLI `dist/commands/{migrate,migration2,migration2-schema}.{js,d.ts}`。
- `/tmp/trellis31-packed-oldcopy-v5-result.json`、`/tmp/trellis31-packed-custom-result.json`：上游actual controlled迁移/reapply结果，边界明确非Guru/private/joint/default retirement。

## Related Specs

- `.trellis/spec/workflow/skill-package-contract.md` 的 Public Skill I/O And Private State、qualification-before-severity：输出只含直接consumer所需，不由研究自授finding/route。
- `.trellis/spec/workflow/quality-guidelines.md:146` Validation Scope Ownership：普通Issue定向验证，不扩完整Release矩阵。
- canonical Task/Delivery migration spec：历史事实不等当前pass；原业务恢复与受控样本分报。

## Caveats / Not Found

- 本研究没有给新candidate跑独立migration/continuation；引用交接结果仅作待匹配证据定位。
- Guru未找到cycle/DTO/checkpoint/remote事务的专用Plan2迁移entry；不能把已有新profile运行成功称旧私有数据已迁。
- 未构造或执行#149/#444/#155样本，不报告任何原会话实际恢复。
- 没有修改上游、frozen tar、业务树、产品/test/runtime/planning文件；只产生本research文档。未新增公共模型、history ledger或永久旧status fallback。
- 记忆仅定位当前constitution相关指引，研究判断以当前文件为准；未据记忆恢复旧结果。
