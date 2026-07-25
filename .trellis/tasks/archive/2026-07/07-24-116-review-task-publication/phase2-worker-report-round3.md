## 检查完成

### 检查身份与边界

- 角色：round-2 finding-fix 后 fresh independent Phase 2
  `trellis-check` / `guru-check-task` raw reviewer。
- Agent：`/root/issue116_phase2_round3`。
- Task：`.trellis/tasks/07-24-116-review-task-publication`。
- Worktree：
  `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/116-review-task-publication`。
- Branch：`codex/116-review-task-publication`。
- 当前 HEAD 与 reviewed base：
  `bdc8f50bcd1e325aed331d4b01107b83ed8ee940`。当前分支还没有相对
  `origin/main` 的 committed implementation commit；本轮覆盖该 worktree 完整
  tracked/untracked current diff，而不是只看 round-2 patch。
- `check-workspace-boundary.sh --json`：通过。expected workspace 与 actual repo
  root 相同；source checkout
  `/Users/wumengye/Documents/GoProjects/guru-trellis` 为
  `main...origin/main` 且干净；没有 suspicious same-task source artifact。
- `check-planning-approval.sh --json --require-exit approved`：通过。current
  facts SHA-256 为
  `cb056cea49bcbb312188a810f1e72328121095c9496ef408b1e9a5b00e749686`，
  approval artifact SHA-256 为
  `7198c7fc5882bb98ad8388ff43f30f1b0d8499da14b9259f7cab956cabe1234d`。
- Issue scope：primary/close=`#116`；related=`#115/#131/#144/#146`；
  follow-up=`#81/#117/#118/#119/#132`。本轮未把 related/follow-up 扩成 current
  close scope。
- 官方 Trellis 文档 current retrieval 与 contract 对照通过：
  `custom-workflow.md` 继续明确 workflow phase、skill routing 与 breadcrumbs
  由 `.trellis/workflow.md` Markdown 控制，hook 是 parser-only；custom spec
  marketplace 继续只允许可复用工程规范而非 task/runtime/platform state。
- 本 reviewer 没有调用 Phase 2 recorder/checker、Branch Review recorder、
  commit、push、PR、archive 或 finalization；只新增本 task-local raw report。

### 已检查文件与证据

- Task 与 gate：
  `prd.md`、`design.md`、`implement.md`、`planning-approval.json`、
  `issue-scope-ledger.json`、`implementation-handoff.md`、
  `phase2-worker-report.md`、`phase2-worker-report-round2.md`、
  current historical `phase2-check.json`、`agent-assignment.json` 与
  `check.jsonl`。
- Curated specs：
  `.trellis/spec/workflow/{quality-guidelines,skill-package-contract,workflow-contract,data-contracts,companion-scripts}.md`、
  `.trellis/spec/preset/{installer,overlay-guidelines,upstream-ownership}.md`、
  `.trellis/spec/docs/public-docs.md`。
- Canonical publication package：
  `trellis/skills/guru-team/packages/guru-review-task-publication/**`，包括
  Skill、interface、contract、schemas、examples、scripts、eval 与 tests。
- Runtime / wrapper / eval：
  `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`、
  publication recorder/checker shell wrappers、
  `trellis/skills/guru-team/adapters/eval/native_adapter.py` 及对应 installed
  copies。
- Registry / producer / workflow / consumer：
  canonical 与 installed registry/extension、`guru-review-branch` package、
  publication workflow/stop consumer schemas、
  `trellis/workflows/guru-team/workflow.md` 与 `.trellis/workflow.md`。
- Platform / normal entry：
  shared、Codex、Claude、Cursor publication package copies，
  canonical/installed `guru-review-branch` Skill，以及 shared/Codex prompt/
  skill、Claude/Cursor `trellis-continue` entry surfaces。
- Preset / installer / upgrade：
  preset apply、throwaway verifier、installer/ownership tests、
  installed closeout verifier、ownership inventory 与完整 overlay tree。
- Durable/public docs：
  approved Docs SSOT Plan 的 16 个 durable paths，包括 workflow/preset/docs
  specs、三份 requirements 文档、root/workflow/preset README。

### Scope qualification

#### SQ-F001：stale/current invocation 与十二项 entry bindings

- Scenario class：`normal_required_behavior`。
- Scope：current task。
- 结论：保持关闭，未发现 regression。
- Fresh evidence：
  - stale recorder/checker绑定 prior `publication_ref`、`stale_reason`、
    `reentry_context`、十二项 current entry bindings、current artifact/repository/
    review identity 与 facts digest；
  - public wrapper 将 stale public input 与 checked owner result精确比较；
  - source/installed shared actual-wrapper 的 `stale-reentry-ready` 均通过；
  - exact `closeout-plan.json` augmentation positive与额外 metadata drift
    negative均通过。

#### SQ-F002：typed exit / conclusions / dimensions / findings closed consistency

- Scenario class：`normal_required_behavior` / `explicit_requirement`。
- Scope：current task。
- 结论：保持关闭，未发现 regression。
- Fresh evidence：
  - private JSON Schema 与 runtime semantic checker都对
    `ready`、`return_to_task_work`、`blocked` 强制相同 cross-consistency；
  - round-2 的三类 contradictory payload现均被双层拒绝；
  - `return_to_task_work` 的 non-passed dimension/open task-work finding关联、
    `blocked` 的 blocked dimension/external-blocker证据，以及 ready全量 pass/
    finding closure均有正负向覆盖；
  - source/installed publication contract各16 tests通过，contradictory
    recorder/checker targeted test通过。

#### SQ-F003：installed manifest provenance 与 sidecar inventory

- Scenario class：`normal_upgrade_update_path`。
- Scope：current task。
- 结论：保持关闭，未发现 regression。
- Fresh evidence：
  - `.trellis/guru-team/extension.json.skill_packages.status=ok`；
  - conflicts、sidecars、removals均为空，recursive actual
    `.new/.bak/.orig` scan为0；
  - source/installed package validators均通过：11 active Skills、42 exits、
    25 targets；
  - installed publication 16 tests、installed actual-wrapper 7/7均能进入并通过
    owner round；
  - dogfood overlay drift、ownership与preset suites均通过。

#### F-004（P1，blocking）：active publication bridge 未同步到 normal entry 与 authoritative wording

- Scenario class：`normal_required_behavior` /
  `normal_platform_entry_compatibility`。
- Scope：current task。#132仍拥有最终 overlay 收敛，但不能让 #116 激活的当前
  consumer在受支持入口继续执行已经失效的 missing-Skill stop。
- Fresh reproduction无需伪造或篡改任何 artifact：
  1. global canonical/installed workflow已声明 Branch Review `passed` targets
     active `guru-review-task-publication`；
  2. canonical/installed/platform `guru-review-branch/SKILL.md` 仍明确声称
     `passed` targets planned publication Skill，并在 package activated前停在
     missing-Skill boundary；
  3. canonical preset的五个 `trellis-continue` overlay以及 dogfood installed
     copies仍明确声称该 package unavailable，并要求 `passed` fail closed；
  4. preset/runtime tests还把这条 obsolete planned wording作为 positive
     expectation；
  5. `.trellis/spec/workflow/workflow-contract.md`、
     `.trellis/spec/preset/installer.md`、`.trellis/spec/docs/public-docs.md`、
     `docs/requirements/requirement-main.md` 同一 current section中同时声明旧
     planned/unavailable boundary与 #116 active 11/42 closure。
- Contract impact：
  - 违反 PRD R11、AC14/AC15/AC18 的 active bridge、distribution与Docs SSOT
    reconciliation；
  - 正常 `trellis-continue` 平台入口会按入口合同停在旧边界，而 global workflow
    要继续调用 active owner；这是实际 route split，不只是历史措辞；
  - green tests正在保护 obsolete route，因此不能把 test pass解释为 current
    workflow一致。
- Required implementation：
  - 从 canonical source更新 Branch Review package的 active consumer wording及
    contract；
  - 更新五个 canonical `trellis-continue` entries，使 `passed` 指向 active
    publication owner，并同步 installed/platform copies；
  - 修订相应 positive assertions与 durable Docs SSOT，明确只有 publication
    `ready -> guru-finalize-task` 仍处于 planned/missing-Skill stop；
  - 经 canonical preset apply同步，重跑 source/installed package validator、
    overlay/platform tests、drift、throwaway install/update/reapply。

#### F-005（P1，blocking）：publication content 的 authoring 顺序位于 gate 之后

- Scenario class：`normal_required_behavior` /
  `workflow_orchestration_correctness`。
- Scope：current task；这是 active Skill在 global workflow中的可达性，不是
  #118 finalization实现。
- Fresh reproduction无需伪造或异常输入：
  1. publication interface为 workflow/standalone都把 `publication_content`
     列为 mandatory entry precondition，并明确 evidence是 task-local
     `pr-body.md` 与 `finish-summary-index.json`；
  2. PRD/design也把这两个 current files列为 semantic review input；
  3. `docs/requirements/guru-team-trellis-flow.md` artifact table明确二者在
     “Phase 3.6 前”产生；
  4. global canonical/installed workflow却先在 Phase 3.6 mandatory invoke
     publication Skill，只有 `ready` 后进入 Phase 3.7，才指示创建/AI-review
     `finish-summary-index.json` 与创建/review `pr-body.md`；
  5. public authoring partition只有 `profile/mode/review_intent`，没有一个会创建
     初始 content files的前置 authoring step；
  6. native production eval/throwaway adapter在进入 Phase 2/Branch Review/
     publication前预写两文件，因此测试绕过并掩盖真实 workflow顺序。
- Contract impact：
  - 严格按 workflow执行时，Phase 3.6因缺 mandatory content无法进入 owner；
  - 若按 Phase 3.7后生成文件，publication `ready` gate已经 stale，而 compatibility
    augmentation只允许 exact `closeout-plan.json` delta，不允许 body/index初始漂移；
  - 因此 active owner在正常 global workflow中不可达，违反 R1/R4/R11 与
    AC1/AC4/AC14/AC17。
- Required implementation：
  - 在 Phase 3.6 invocation前由明确 owner创建并AI-review初始
    `pr-body.md`/`finish-summary-index.json`，再把 current content交给
    publication Skill；或者在不削弱 semantic entry/gate的前提下重新设计步骤边界；
  - Phase 3.7不得再次作为这两个 mandatory review inputs的首次创建者；
  - 增加不预写 publication content 的真实 workflow/entry negative与positive
    test，避免 adapter fixture替代global orchestration。

### 已修复问题

- 无。
- 本轮是独立 Phase 2 review；F-004/F-005都涉及 canonical workflow、package、
  entries、durable docs、tests与installed copies联动，不属于 reviewer可做的机械修复。

### 未修复问题

- F-004（P1，blocking）：active publication route在global workflow与正常平台入口/
  producer contract之间分裂，durable Docs SSOT和positive tests仍保护旧
  planned/unavailable边界。
- F-005（P1，blocking）：global workflow在 publication gate通过后才首次创建该
  gate的mandatory content，实际正常路径不可达；fixture预写掩盖缺口。

### 十维充分性结论

1. Requirements：失败。F-004违反 active bridge/distribution/Docs reconciliation；
   F-005使R1/R4/R11所要求的active owner正常路径不可执行。
2. Design：失败。active graph声明
   `Branch Review -> publication`，但entry surfaces仍停在planned boundary；
   content precondition与Phase 3.6/3.7 ordering相互矛盾。
3. Implementation：失败。publication schema/runtime/freshness与round-2 findings
   已闭环，但global route/entry/content orchestration仍有两个current P1。
4. Tests：失败。所有自动化命令绿色，但测试一部分正向断言obsolete planned
   wording，真实wrapper/throwaway又预写content，未覆盖正常workflow可达性。
5. Docs SSOT：失败。approved strategy=`ssot_first`；current durable docs同一
   section同时声称 planned/unavailable与active，并与content production order
   自相矛盾，`task_delta_merged=false`。
6. Cross-layer：失败。workflow、producer Skill、platform entries、durable docs与
   fixtures不一致；publication entry与content owner/order不一致。
7. Compatibility：失败。source/installed package API与legacy finalization
   augmentation targeted checks通过，但受支持的 `trellis-continue` 正常入口仍执行
   旧stop合同。
8. Deployment and operations：通过。完整 changed/untracked path scan没有
   GitHub Actions、Docker/Compose、Kubernetes/Helm、DB migration、`.env`、
   Makefile或production deployment surface变更；未执行远端写入。
9. Agent recovery：通过。`agent-assignment.json` 可恢复
   `/root/issue116_implement`、`/root/issue116_phase2_check`、
   `/root/issue116_fix_round1`、`/root/issue116_phase2_rerun`、
   `/root/issue116_fix_round2` 到本
   `/root/issue116_phase2_round3` 的assigned/status/completed链；本报告没有把旧
   Phase 2 pass当成current结论。
10. Verification completeness：通过（足以安全路由实现）。完整package/runtime/
    preset/install/frozen证据与fresh semantic route review已经确认两个normal-path
    blocking findings；exact remote branch marketplace未验证不影响
    `implementation_required`。

### 验证结果

- Lint / deterministic validation：
  - `git diff --check`：通过；
  - dogfood overlay drift：通过；
  - upstream ownership：通过，43 frozen/active paths，11 active与1 planned；
  - source/installed package validator：均通过，11/42/25；
  - installed extension status=`ok`，declared/actual sidecar均为0；
  - repo没有独立 ruff/flake8/shellcheck lint配置。
- TypeCheck：不适用。仓库未配置mypy、pyright或等价静态类型检查；未以import/
  unit test冒充type-check。
- Full tests：
  - runtime：570 passed，13 skipped；
  - skill packages：173 passed；
  - preset：45 passed；
  - publication source/installed contract：16 + 16 passed；
  - source/installed shared actual-wrapper eval：7/7 + 7/7 passed，覆盖两
    profiles、两modes、三exits、stale re-entry、metadata fix与durable drift；
  - targeted actual-wrapper/runtime：5项通过，包括三actual exits、
    contradictory ready recorder/checker rejection、stale invocation binding、
    exact finalization augmentation positive与extra metadata delta negative。
- Frozen/parity：
  - Stage 0 migration保持6 Skills/24 exits；
  - production migration保持3 Skills/11 exits；
  - #131 public output schema/example bytes不变；
  - production/Stage0 manifests、overlay tree、finish-work assets无diff；
  - canonical/installed/shared/Codex/Claude/Cursor publication package
    byte-identical，canonical/installed runtime与adapter byte-identical；
  - package scripts executable。
- Throwaway install/update/reapply：
  - fresh `verify-throwaway-install.sh` 在
    `TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1` 下返回rc=0；
  - 覆盖clean init、public marketplace discovery + local unpublished workflow
    sample、developer/no-developer identities、workflow switch、preset install、
    `trellis update`、workflow/preset reapply、entry/closeout/eval smoke、
    ownership/drift、source/installed validators；
  - clean update产生的官方backup按verifier合同处理，最终extension manifest
    `ok`，无unresolved `.new/.bak/.orig` sidecar。
  - 当前分支未push，因此exact current-branch remote marketplace仍未验证；fresh
    verifier使用public marketplace sample，不能将其表述为exact branch remote
    publication evidence。

### 证据交接

- 本报告可以支撑 `guru-check-task:implementation_required`，不能支撑
  `passed`。
- Docs SSOT reconciliation：
  `strategy=ssot_first`，但`task_delta_merged=false`；F-004/F-005修复后必须重新
  对照16个durable paths，移除current contradictions并全量复审。
- Branch Review：不适用。当前没有task implementation commit；本轮没有生成或记录
  `review.md` / `review-gate.json`。
- 未验证项：exact current-branch remote marketplace verifier须在分支push后由后续
  publish/finish gate执行；本轮public sample只证明公开基线安装机制与本地
  preset/update/reapply路径。

### 结论

当前结论为 `implementation_required`。F-001、F-002、F-003在fresh evidence下保持
关闭，完整自动化与开箱验证大部分稳定；但F-004造成active route在global workflow与
normal entries之间分裂，F-005使publication mandatory content在gate之后才产生。
修复并完整重跑Phase 2之前，不得记录passing `phase2-check.json`，不得进入task
commit、Branch Review、publication review或finalization。
