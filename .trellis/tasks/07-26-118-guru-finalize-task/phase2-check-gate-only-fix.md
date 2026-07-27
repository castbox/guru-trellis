# Issue #118 gate-only freshness 修复 Phase 2 独立检查报告

## 检查完成

### 检查身份与结论

- 角色：全新独立 Phase 2 `trellis-check` reviewer。
- Agent：`/root/issue118_phase2_gate_only_fix`。
- Task：`.trellis/tasks/07-26-118-guru-finalize-task`。
- Worktree：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/118-guru-finalize-task`。
- Branch：`feat/118-guru-finalize-task`。
- Base：`origin/main@7820a9eeec2a2a75fb52fba156a7211d9f9fb09c`。
- Checked HEAD：`4f254b70cfc817bc34e6d20ad508dee91f910846` 加当前未提交 gate-only runtime、tests 与 handoff delta。
- Authority：Issue #118 accepted-current comment `5045036678`；close scope 仍只有 #118。
- Finding inventory：P0=0、P1=0、P2=0、P3=0。
- 语义结论：`passed`。
- 本报告不调用 recorder/checker，不写 `phase2-check.json`、Branch Review、publication 或 finalization gate；不授权 commit、push、PR、archive、Issue mutation、deploy 或 production write。

Workspace boundary validator 终态通过：expected workspace 与 actual repo root 均为上述 worktree；source checkout `/Users/wumengye/Documents/GoProjects/guru-trellis` 位于 `main`、clean，task worktree identity current，suspicious source artifacts 为空。Planning approval checker 返回 `status=ok`、`typed_exit=approved`，`prd.md`、`design.md`、`implement.md` 的已批准 digest current。

### 已检查文件

- Planning 与 task authority：`prd.md`、`design.md`、`implement.md`、`planning-approval.json`、`implementation-handoff-gate-only-fix.md`、Issue #118 accepted-current comment、当前 scope ledger 与旧 gate artifacts 的 freshness 状态。
- 实现：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`。
- Dogfood runtime：`.trellis/guru-team/scripts/python/guru_team_trellis.py`。
- 回归测试：`trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`。
- Durable specs：`.trellis/spec/docs/**`、`.trellis/spec/preset/**`、`.trellis/spec/workflow/**` 中 finalizer、runtime、quality、installer、ownership、public docs 与 Skill package contract 段落。
- Canonical/public package：`trellis/skills/guru-team/packages/guru-finalize-task/**`、registry、eval adapter、public wrappers 与 platform-installed copies。
- Distribution：preset apply/verifier、ownership inventory、overlay drift、source/installed Skill discovery 与 canonical/installed/platform byte identity。
- Explicit no-diff boundary：`trellis/workflows/guru-team/workflow.md`、`.trellis/workflow.md`、upstream `trellis-finish-work` Skill/Command/Prompt/Agent family、`.trellis/scripts/task.py`、`trellis/presets/guru-team/overlays/**` 与 ownership inventory。
- Official reference：Trellis docs 首页、自定义 workflow、自定义 Skill 与 spec template marketplace 文档；当前实现仍使用官方 marketplace/preset/Skill 扩展面。

`check.jsonl` 只有 seed row；按 fallback 执行 `python3 ./.trellis/scripts/get_context.py --mode packages` 后选择上述 workflow、preset、docs 与 quality specs。未把缺少 curated row 当作阻断，但规划审批、三份 planning artifacts 与 Docs SSOT Plan 均已验证。

### 实现语义复核

正常 honest workflow 的复现与根因成立：首次 formal transition 前只有 finalizer-owned `task-finalization-gate.json` 新增，外层 exact-delta 已构造并验证 `finalization_paths=[gate_relative]`，但消除 publication entry-precondition stale 的第二次重算错误硬编码 `[plan_relative]`，把合法 gate-only delta 误判 stale。该路径无需伪造 artifact、并发、锁、TOCTOU 或额外 fault injection。

修复只把第二次 `task_publication_entry_precondition_bindings()` 的 `finalization_owned_paths` 改为同一已验证 `finalization_paths`。因此：

- gate-only exact delta 可以消除 owner-private freshness stale；
- gate-only 加 unexpected metadata 仍 fail closed；
- `require_plan=True` 且 closeout plan 缺失仍 fail closed；
- plan-only 与 gate+plan 路径继续复用同一 exact allowlist；
- 未增加 public input/output、exit、profile、route、schema、state 或 script judgment；
- #105 transaction/recovery semantics、#119 Finish-family integration ownership与 #132 overlay cleanup ownership均未改变。

Canonical 与 dogfood runtime byte-identical；测试直接断言 outer checker 与 entry-precondition recomputation 收到完全相同的 `[gate_relative]`，而不是只断言最终 happy path。

### 已修复问题

- 文件：无额外 implementation file。
- 问题：验证期间 Python 生成 ignored `__pycache__`/`.pyc`，会污染 hygiene 观察；首次 clean throwaway 还因系统临时卷只剩 138 MiB 而在 pre-0.6.5 upgrade eval 阶段触发 `OSError: [Errno 28] No space left on device`。
- 修复：把 repo 内生成 cache 移出并删除；精确删除已终止 verifier temp root 与本轮已完成、不再需要的 Codex/Cursor/shared/installed-shared/cache run roots，未触碰 worktree 证据、用户文件或仍运行的 session。可用空间恢复至 3.4 GiB 后，从头重跑同一 clean throwaway verifier。

未发现需要自修复的代码、schema、config、docs 或 test finding。

### 未修复问题

- Claude source real-native eval 未取得成功：前五个实际 CLI 调用均在约 179-186 秒后返回脱敏 envelope `terminal_reason=api_error`、`api_error_status=401`、`Invalid API key`、0 tokens、无 permission denial；后 3 cases 又在并行临时卷耗尽后于 owner staging 阶段停止。进程自身 terminal exit 0，但 eval status 为 `execution_error`。这是当前本机 Claude credential/临时容量外部残余，不是候选协议断言失败；179-test package suite已覆盖 Claude non-interactive stdin/file protocol、`--safe-mode`、allowed tool、single-JSON envelope 与 error parsing。未重试凭据，也不声称 Claude native pass。
- 当前 feature branch 未 push，且本 task 明确禁止 push。Clean throwaway 只能使用 public marketplace discovery 加 local current canonical workflow/preset/package/runtime sample，不能证明 exact current feature-ref remote marketplace install。Formal finalization 前仍需由 #117 owner workflow 在 content push 后验证 exact remote ref/HEAD。
- 既有 `phase2-check.json`、Branch Review、publication、immutable plan/confirmation 与 finalization evidence 均早于本次 runtime/test/handoff delta，必须由主会话按 owner workflow重新生成；这些 stale artifacts 未被本 reviewer 修改或当作 current pass。

以上均是外部验证限制或下游 freshness work，不是未关闭的 current implementation finding。

### 验证结果

#### Tests

- Gate-only focused：5/5 passed。覆盖既有 exact plan、既有 unexpected metadata、gate-only exact pass、gate-only unexpected metadata reject 与 `require_plan=True` 缺 plan reject。
- `TaskPublicationMetadataAllowlistTest + CloseoutTransactionContractTest`：100/100 passed；#105 transaction/recovery matrix保持绿色。
- Runtime full：620 passed，13 skipped。
- `guru-finalize-task` package：5/5 passed。
- Skill package / production eval full：179/179 passed。
- Preset installer：45/45 passed。
- Upstream ownership：9/9 passed。
- Shared source real public-wrapper eval：8/8 passed。
- Shared installed real public-wrapper eval：8/8 passed。
- Codex source real-native eval：8/8 passed。
- Cursor source real-native eval：8 cases 均稳定返回 contract-expected `unsupported`，没有 public success output。
- Claude source real-native eval：`execution_error`，外部残余如上，不计作 pass。

主要 fresh 命令：

```text
python3 -m unittest trellis.workflows.guru-team.scripts.python.test_guru_team_trellis.TaskPublicationMetadataAllowlistTest trellis.workflows.guru-team.scripts.python.test_guru_team_trellis.CloseoutTransactionContractTest
python3 -m unittest trellis.workflows.guru-team.scripts.python.test_guru_team_trellis
python3 -m unittest trellis.skills.guru-team.packages.guru-finalize-task.tests.test_contract
python3 -m unittest trellis.skills.guru-team.tests.test_skill_packages
python3 -m unittest trellis.presets.guru-team.scripts.python.test_apply_guru_team_trellis_preset
python3 -m unittest trellis.presets.guru-team.scripts.python.test_upstream_ownership
trellis/workflows/guru-team/scripts/bash/run-skill-evals.sh --root . --mode source --skill guru-finalize-task --adapter shared --run-root /tmp/guru-118-phase2-shared.1n7krX --json
.trellis/guru-team/scripts/bash/run-skill-evals.sh --root . --mode installed --skill guru-finalize-task --adapter shared --run-root /tmp/guru-118-phase2-installed-shared.VLuBfB --json
trellis/workflows/guru-team/scripts/python/guru_team_trellis.py run-skill-evals --root . --mode source --skill guru-finalize-task --adapter codex --run-root /tmp/guru-118-phase2-codex.UUm0pp --json
trellis/workflows/guru-team/scripts/python/guru_team_trellis.py run-skill-evals --root . --mode source --skill guru-finalize-task --adapter claude --run-root /tmp/guru-118-phase2-claude.Ac1dRf --json
trellis/workflows/guru-team/scripts/python/guru_team_trellis.py run-skill-evals --root . --mode source --skill guru-finalize-task --adapter cursor --run-root /tmp/guru-118-phase2-cursor.4FRrTj --json
```

#### Lint 与 TypeCheck

- Lint：通过。`git diff --check`、base-to-HEAD 与 dirty JSON parse、`trellis/index.json` parse、changed Bash `bash -n`、source/installed validators、overlay drift 与 no-diff assertions均通过。
- TypeCheck：通过适用门禁。仓库无独立 configured static type checker；canonical runtime、preset installer、native adapter `python3 -m py_compile` 通过，full runtime/package suites覆盖关键动态类型路径。
- Task：最终一次 reviewer 命令误漏 task path，`python3 ./.trellis/scripts/task.py validate` 只返回 CLI usage error，不作为证据；随后用有效命令 `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-26-118-guru-finalize-task` 重跑，terminal exit 0、`All validations passed`。
- Source checkout：最终复核 clean。
- Hygiene：最终 `find` 扫描无 `.new`、`.bak`、`__pycache__`、`.pyc` 或 `.pyo`；报告无占位符或 trailing whitespace；tracked dirty diff `git diff --check` 通过。

#### Distribution、安装与 upgrade/update

- Source/installed `check-skill-packages.sh` 通过：13 active、0 planned/legacy；global markers保持 12 invokes / 46 exits / 27 targets；installed sidecar/removal/conflict 均为 0。
- Source/installed finalizer contract discovery通过；canonical、installed shared、Agents、Codex、Claude、Cursor packages `diff -qr` 通过；全部 finalizer scripts executable。
- `apply.sh --repo . --all-platforms --json` 后 canonical/dogfood runtime byte-identical；dogfood overlay drift passed；ownership freeze 43 active、0 removed。
- Clean throwaway：第一次运行在 pre-0.6.5 upgrade eval 阶段因系统临时卷 `No space left on device` 退出；精确清理本轮已终止/已完成 temp roots 并恢复 3.4 GiB 余量后，从 fresh bootstrap 完整重跑，terminal exit 0。覆盖 public workflow marketplace discovery、fresh init、initial preset install/idempotent reapply、official Trellis 0.6.5 update、workflow preview/switch、preset reapply、managed `.bak`、unknown local edit `.new`、显式 sidecar resolution、source/installed checks、Shared/Agents/Codex/Claude/Cursor package bytes/modes与 wrapper smoke、#105 closeout fixture、developer/no-developer task-workspace fixtures、pre-0.6.5 upgrade evals、ownership freeze、dogfood drift，以及终态 zero sidecar/removal/conflict。最终输出：`Verified public marketplace discovery plus local unpublished workflow sample`。

Clean throwaway 命令：

```text
TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1 trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh
```

该命令显式使用 public marketplace bootstrap 与 local unpublished candidate sample；不会被描述为 current feature-ref remote marketplace verification。

### 证据交接

- 阶段二：覆盖 approved planning、accepted-current authority、effective dirty diff、runtime、tests、package/public wrappers、platform adapter、distribution、install/update/reapply、ownership、no-diff boundary、security/deploy 与 hygiene。P0-P3=0；除明确外部残余外，验证充分。本报告可作为主会话重新生成 `phase2-check.json` 的语义输入，但 recorder 必须绑定届时 current HEAD、dirty paths、report identity 与 fresh agent-assignment evidence。
- Docs SSOT：strategy=`ssot_first`。Durable workflow/preset/package/docs已先于本修复定义 finalizer-owned exact metadata delta、owner-private gate、formal checker freshness 与 unexpected-path fail closed；本次是一行 runtime correctness 修复，不改变 contract。因此 `no_docs_update_needed`，无需对 durable SSOT做首次 merge。`implementation-handoff-gate-only-fix.md` 只保留 task-history delta；#119/#132 与 pushed exact-ref verification继续作为明确 follow-up/PR limitation。
- Branch Review：不适用。本轮是 uncommitted Phase 2 check，不执行 Branch Review、不写 `review.md` 或 `review-gate.json`。后续 Branch Review 必须覆盖 `origin/main...HEAD` 的完整 committed diff 与本轮新 evidence commit。
- Security/deploy：changed paths无 dependency、CI/CD、container、Compose、Kubernetes、Helm/Kustomize、DB migration、Makefile、production config、credential、production data 或 production write surface；未发现部署或 migration 影响。

### 结论

Gate-only freshness 修复与已批准 #118 scope、现有 Docs SSOT、public/private boundary、#105 transaction semantics 及 #119/#132 ownership一致。核心 regression、full suites、public-wrapper、distribution 与静态门禁均通过；finding inventory 为 P0=0、P1=0、P2=0、P3=0，Phase 2 语义结论为 `passed`。

主会话下一步必须先把本次 runtime/test/handoff/report 作为新的 task commit scope，随后重做独立 Branch Review、publication review 与 immutable finalization preparation；旧 gate不能继续复用。

报告最终 SHA-256、bytes 与 lines 在写入完成后由 terminal handoff提供，避免正文自引用导致 digest失真。
