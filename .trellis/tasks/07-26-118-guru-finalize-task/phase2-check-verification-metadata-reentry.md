# Issue #118 verification metadata re-entry 修复 Phase 2 独立检查报告

## 检查完成

### 检查身份与结论

- 角色：全新独立 Phase 2 `trellis-check` reviewer。
- Agent：`/root/issue118_phase2_verification_reentry`。
- Task：`.trellis/tasks/07-26-118-guru-finalize-task`。
- Worktree：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/118-guru-finalize-task`。
- Branch：`feat/118-guru-finalize-task`。
- Base：`origin/main@7820a9eeec2a2a75fb52fba156a7211d9f9fb09c`。
- Checked HEAD：`77ad13f0a65f652e68e655afbe11917aa659df5c` 加当前未提交 verification metadata re-entry runtime、tests、handoff 与本报告 delta。
- Authority：Issue #118 accepted-current comment `5045036678`；close scope 仍只有 #118。
- Finding inventory：P0=0、P1=0、P2=0、P3=0。
- Phase 2 语义结论：`passed`；clean throwaway最终重跑exit 0。仍须保留下文 Claude 401与 unpushed exact ref外部残余，禁止把这两项改写为 pass。
- 本报告不调用 recorder/checker，不写 `phase2-check.json`、Branch Review、publication 或 finalization gate；不授权 commit、push、PR、archive、Issue mutation、deploy 或 production write。

Workspace boundary validator 终态通过：expected workspace 与 actual repo root 均为上述独立 worktree；source checkout `/Users/wumengye/Documents/GoProjects/guru-trellis` 位于 `main`、clean，`suspicious_source_artifacts=[]`。Planning approval checker 返回 `status=ok`、`typed_exit=approved`，三份 planning artifacts 的批准 digest current；`check.jsonl` 只有 seed row，因此按 fallback 读取 approved artifacts 并选择 workflow、preset、docs、Skill package 与 quality specs。

### 已检查文件

- Planning 与 authority：`prd.md`、`design.md`、`implement.md`、`planning-approval.json`、Issue #118 accepted-current boundary、`issue-scope-ledger.json` 与 current implementation handoff。
- 本轮实现：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`。
- Dogfood runtime：`.trellis/guru-team/scripts/python/guru_team_trellis.py`。
- Regression：`trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`。
- Public package 与 owner contracts：`guru-finalize-task`、`guru-verify-extension-installation`、`guru-review-task-publication` 的 canonical/installed contracts、Interface、schemas、examples、wrappers 与 tests。
- Durable Docs SSOT：`.trellis/spec/workflow/workflow-contract.md`、`skill-package-contract.md`、`companion-scripts.md`、`quality-guidelines.md`，以及 docs/preset indexes 与安装、ownership 规范。
- Distribution：canonical registry、native adapter、preset installer、source/installed package discovery、Agents/Codex/Claude/Cursor package copies、overlay drift 与 upstream ownership。
- Branch evidence：Round 11、Round 12、Round 9 raw report与 current `agent-assignment.json` identity binding。
- Explicit no-write boundary：global workflow、upstream `trellis-finish-work` Skill/Command/Prompt/Agent family、preset overlays、official `.trellis/scripts/task.py`、#119 global integration 与 #132 overlay cleanup surfaces。
- Official Trellis reference：docs 首页、自定义 workflow、自定义 Skill 与 spec template marketplace；当前实现继续使用 marketplace、preset、Skill 与 project-local runtime 扩展面，没有修改 upstream Trellis 源码或全局 npm。

### P1 closure 语义复核

`F-VERIFICATION-METADATA-REENTRY-01` 的 normal-path root cause 与修复边界均成立：

1. Verification re-entry profile 先调用现有 #117 owner checker；publication profile 与其它非 verification profile 不获得该 augmentation。
2. 只有 checked verification `status=ok` 且 `typed_exit=verified|not_required` 时，finalizer 才显式打开 `allow_verification_metadata`。
3. 默认值保持关闭；即使 caller 直接传入 exact verification path，缺少 owner binding 仍 fail closed。
4. Allowlist 只增加当前 task 的唯一 `marketplace-verification.json`；任意其它 metadata 继续失败。
5. Task-bearing standalone `not_required` 只在 immutable plan 明确 `marketplace.required=false`、owner task/repo/remote/ref/HEAD 与 verification ref 全部一致时成立。
6. Generic #117 checker、public profile、Interface/schema/DTO/typed exit、confirmation 与 #105 transaction ordering均未扩张。

四条新增 real regression 不使用 `GURU_TEAM_EVAL_STAGING=1` 的 terminal shortcut。正向路径实际经过 #117 recorder、public checker/wrapper、#118 real preview、finalization gate recorder/checker与 #118 public invocation；负面路径覆盖 arbitrary metadata 与 missing explicit owner binding。结果为 `Ran 4 tests in 3.082s`、`OK`。

因此 P1 required closure 在 implementation/Phase 2 范围内成立。Formal Branch Review finding closure 仍须由后续独立 closure reviewer绑定新 task commit；本报告不自行修改 Round 12 owner evidence。

### P3 requalification 语义复核

`F-ROUND9-TRAILING-WHITESPACE-01` 不再资格化为 current implementation finding。Round 9 raw report当前 objective identity为：

```text
SHA-256 b1424b1a0a5080730383834c820ad4f50d20f15216f2aec7a9c5a2177dbab3ce
size    18367 bytes
lines   283
```

该 SHA-256 与 size 精确匹配 `agent-assignment.json` Round 9 owner binding。Current assignment checker返回 `status=ok`、12 review rounds、12 reuse decisions、412 effective status events。删除空格会改变 immutable raw report bytes并使 mandatory assignment/review evidence identity fail closed；修改历史 digest、增加 ignore、扩大 recorder或改写 raw report都超出本 finding closure 的合法动作。

Lint事实仍须原样记录：

```text
git diff --check
exit 0

git diff --check origin/main...HEAD
exit 2
.trellis/tasks/07-26-118-guru-finalize-task/reviews/round-009-finding-closure.md:203: trailing whitespace.
```

`git diff --check origin/main` 也只命中同一处。结论是 lint signal 真实，但候选修复与更强的 immutable raw-evidence contract冲突；本项重资格化为 nonblocking rejected candidate/observation，P3 current finding count为 0。后续 finding-closure report必须保留此理由，不得声称完整 committed range 的 `git diff --check` exit 0。

### 已修复问题

- 文件：无额外 implementation file。
- 问题：验证命令生成 ignored `__pycache__`/`.pyc`，会污染 final hygiene；clean throwaway 临时根在 terminal ENOSPC 后占用约 1.5 GiB。
- 修复：确认首次 verifier 及子进程全部终止后，精确删除本轮 `/private/tmp/guru-118-phase2-reentry.zRVyEJ` 与 repo 内 untracked Python cache；没有删除其它 agent/旧会话目录，没有修改 tracked implementation 或 task evidence。主会话释放四个明确属于 #118 旧轮次且无进程的 eval目录后，本 reviewer只重跑一次完整 verifier；`/private/tmp/guru-118-phase2-reentry-final.pCRoOc` outer terminal exit 0。确认无匹配子进程后已精确删除该 final root。后续 Python 检查使用 `PYTHONDONTWRITEBYTECODE=1`。

未发现需要自修复的 code、schema、config、docs 或 test finding。本 reviewer 未修改 P1 implementation；只审核 implementation agent 已提交到 working tree 的 delta。

### 未修复问题

- Claude live single-case runner终态 process exit 0，但 eval status=`execution_error`。Native transcript显示 CLI returncode 1、`api_error_status=401`、`Failed to authenticate. API Error: 401 Invalid API key`、0 tokens、无 permission denial。该项是外部 credential blocker；package-controlled Claude protocol tests通过，但不得声称 Claude native success。
- Current feature branch未 push，remote不存在 exact feature ref。Exact-ref marketplace verification必须在 content push后由 #117 owner semantic gate执行；本 Phase 2 不授权 push或模拟该 evidence。
- Existing `phase2-check.json`、Branch Review、publication/finalization evidence与 task commit均早于当前 runtime/test/handoff delta。主会话必须按 owner workflow重新生成 freshness evidence，本 reviewer未修改这些 artifacts。

以上是外部验证限制或下游 freshness work，不是 open P0-P3 implementation finding。Clean throwaway首次 ENOSPC已由同一 reviewer在额外空间释放后通过唯一一次完整重跑闭合，不再是 unresolved item。

### 验证结果

#### Tests

- Runtime full：624 passed，13 skipped。
- Skill package / production eval full：179 passed。
- Preset installer：45 passed；upstream ownership：9 passed。
- `guru-finalize-task` package：5 passed。
- `guru-verify-extension-installation` package：10 passed。
- `guru-review-task-publication` package：18 passed。
- Focused verifier runtime：27 passed。
- Focused publication allowlist：2 passed。
- #105/closeout transaction class：102 passed。
- P1新增 real/negative regression：4 passed。
- Source shared real public-wrapper eval：8/8 passed。
- Installed shared real public-wrapper eval：8/8 passed。
- Package-controlled four-platform adapter tests：2/2 passed。
- Cursor live single-case：稳定返回 contract-expected `unsupported`，没有伪造 public success。
- Claude live single-case：external `401` execution error，如上，不计作 pass。

主要 fresh命令：

```text
python3 -m unittest trellis.workflows.guru-team.scripts.python.test_guru_team_trellis
python3 -m unittest trellis.skills.guru-team.tests.test_skill_packages
python3 -m unittest trellis.presets.guru-team.scripts.python.test_apply_guru_team_trellis_preset
python3 -m unittest trellis.presets.guru-team.scripts.python.test_upstream_ownership
python3 -m unittest trellis.skills.guru-team.packages.guru-finalize-task.tests.test_contract
python3 -m unittest trellis.skills.guru-team.packages.guru-verify-extension-installation.tests.test_contract
python3 -m unittest trellis.skills.guru-team.packages.guru-review-task-publication.tests.test_contract
trellis/workflows/guru-team/scripts/bash/run-skill-evals.sh --root . --mode source --skill guru-finalize-task --adapter shared --run-root /tmp/guru-118-phase2-reentry.zRVyEJ/eval-source --json
.trellis/guru-team/scripts/bash/run-skill-evals.sh --root . --mode installed --skill guru-finalize-task --adapter shared --run-root /tmp/guru-118-phase2-reentry.zRVyEJ/eval-installed --json
.trellis/guru-team/scripts/bash/run-skill-evals.sh --root . --mode source --skill guru-finalize-task --adapter claude --case publication-review-stale --run-root /tmp/guru-118-phase2-reentry.zRVyEJ/eval-claude-live --json
TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1 PYTHONPYCACHEPREFIX=/private/tmp/guru-118-phase2-reentry-final.pCRoOc/pycache trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh /private/tmp/guru-118-phase2-reentry-final.pCRoOc/throwaway
```

#### Lint 与 TypeCheck

- Lint：当前未提交 implementation、tests、handoff 与本报告 delta通过 `git diff --check`。完整 committed range仍因上文 immutable Round 9 raw evidence返回 exit 2；该事实已按 P3 rejected candidate记录，不伪称全 range lint exit 0。
- Bash syntax、JSON parse、Python compile、task validation、source/installed contract validators、overlay drift、upstream ownership与 protected-path no-diff assertions均通过。
- TypeCheck：通过适用门禁。仓库没有独立 configured static type checker；canonical runtime、dogfood runtime、native adapter、preset installer的 Python compile及全量动态测试覆盖关键类型路径。
- Canonical/dogfood runtime `cmp`通过，bytes一致。
- Canonical/installed shared/Agents/Codex/Claude/Cursor finalizer package `diff -qr`通过。
- Source/installed discovery均为 6 input profiles、6 exits、2 private artifacts；eval discovery均为8 cases、4 adapters。

#### Distribution、安装与 update

- Source/installed package validators通过：13 active、0 planned、0 legacy；installed sidecar/removal/conflict均为0。
- Preset apply 与 dogfood overlay drift通过；upstream ownership inventory current。
- Protected paths相对 `origin/main` 无 diff：global workflow、official `task.py`、preset overlays、upstream `trellis-finish-work` family。
- Dependency、CI、container、K8s、DB migration、Makefile与Terraform surface扫描无变化。
- Clean throwaway最终重跑terminal exit 0，覆盖 public marketplace discovery、local unpublished current workflow sample、fresh init、preset install/reapply、official Trellis update、managed `.new/.bak` 路径、source/installed validators、三平台 distribution、wrapper smoke、initial/after-update installed #105 closeout、task-workspace smoke、ownership、overlay drift与 no-developer fixture。Initial与after-update closeout均验证 local/remote/PR HEAD equality、fresh archived PR binding、archive preflight与 `pr_ready=true`。首次 ENOSPC run不计作pass，但最终唯一重跑完整通过。

### 证据交接

- Phase 2覆盖：approved task scope、normal-path P1 closure、P3 requalification、runtime/package/preset/ownership suites、real wrappers、platform adapters、#105 transaction regressions、distribution、protected boundaries、Docs SSOT、安全/部署与 terminal hygiene。
- Finding inventory：P0/P1/P2/P3=`0/0/0/0`。P1 implementation closure成立；P3为 nonblocking rejected candidate/observation。Formal Round 12 finding closure与fresh final review仍由后续独立 identities完成。
- Docs SSOT：plan strategy=`ssot_first`，结果=`no_docs_update_needed`。Durable specs与 finalizer package contract已要求 owner-check-first、same plan/ref/HEAD、finalizer-only exact verification metadata augmentation与 arbitrary metadata fail-closed；本轮只是 code/test correctness修复，没有新的 durable语义 delta。
- Durable docs/task-history区分：`.trellis/spec/**` 与 package contract是 current behavior SSOT；本 report与 implementation handoff仅保存 task-local实施/验证历史，不成为第二份 behavior SSOT。
- Safety/deploy：未发现 secret、credential-bearing remote、signed URL、客户数据或原始 provider payload泄露；没有 dependency/config/CI/container/K8s/DB/deploy/production data影响。
- Freshness：checked HEAD保持 `77ad13f0a65f652e68e655afbe11917aa659df5c`；source checkout clean；current task worktree只包含本次 code/test/handoff、本报告及主会话并行 review/assignment/commit-plan metadata。Assignment checker终态 `status=ok`。
- 本报告可支撑主会话在 `phase2-check.json` 中记录 semantic `passed`，前提是 recorder如实保留 Claude 401、unpushed exact-ref与 full-range whitespace observation；clean throwaway应记录首次 ENOSPC及最终唯一重跑exit 0，不得只截取中间失败或省略最终覆盖。

### 结论

`F-VERIFICATION-METADATA-REENTRY-01` 已由严格 owner binding、默认关闭的 exact allowlist与四条 real regression闭合；#116/#117 public DTO、generic checker、#105事务、#119/#132边界均保持不变。`F-ROUND9-TRAILING-WHITESPACE-01` 的修复会破坏 mandatory immutable raw-evidence identity，因此不再是 current P3 finding。

Phase 2 semantic route为 `passed`，P0-P3 open均为0。进入 task commit与独立 Branch Review前，主会话必须重建 current Phase 2 evidence，并如实携带本报告列出的外部验证残余；不得进入 publication/finalization side effects，直到后续 gates current并取得各自 mandatory confirmation。
