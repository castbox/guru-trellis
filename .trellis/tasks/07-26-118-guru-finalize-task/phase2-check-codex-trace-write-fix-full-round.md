# Issue #118 Codex native trace writable-root 修复 Phase 2 全量检查报告

## 检查完成

### 检查身份与边界

- 角色：独立 Phase 2 `trellis-check` reviewer。
- Task：`.trellis/tasks/07-26-118-guru-finalize-task`。
- Worktree：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/118-guru-finalize-task`。
- Branch：`feat/118-guru-finalize-task`。
- Base：`origin/main@7820a9eeec2a2a75fb52fba156a7211d9f9fb09c`。
- Checked HEAD：`c04ed1d7a816ac80217953bcf52f7a2a44b645d2` 加当前全部 dirty/untracked task delta。
- Full committed range：`origin/main...c04ed1d7a816ac80217953bcf52f7a2a44b645d2`，
  532 paths，76879 insertions，4767 deletions。
- Authority：live Issue #118 与 accepted-current comment `5045036678`；close scope 仍只包含
  #118。
- Finding inventory：P0=`0`、P1=`0`、P2=`0`、P3=`0`。
- Phase 2 semantic recommendation：typed exit=`passed`，consumer=
  `skill:guru-create-task-commit`。

Workspace boundary validator 通过：expected workspace 与 actual repo root 均为上述 worktree；
source checkout `/Users/wumengye/Documents/GoProjects/guru-trellis` clean，
`suspicious_source_artifacts=[]`。Planning approval checker 通过，approved planning document
digests current。`check.jsonl` 只有 seed row；按合同 fallback 使用已批准 planning artifacts、
匹配的 workflow/preset/docs specs 与完整实现证据，该缺口不阻断。

本 reviewer 未修改 product、durable docs、spec、runtime、tests、planning、ledger 或现有 gate；
只生成本报告和同轮 command evidence。未调用 `record-phase2-check`，未 commit、push、创建或
修改 PR、archive、Ready、merge、deploy、production write 或修改 GitHub Issue。主会话负责在
checker lifecycle completed 后记录新的 `phase2-check.json`。

### Live authority 与 scope 复核

- Issue #118 当前仍要求 `guru-finalize-task` 独占 immutable plan、exact confirmation、content
  push、verification routing、唯一 Draft PR、projection、archive metadata transaction、三方
  HEAD equality、Ready 与封闭 recovery matrix。
- accepted-current comment `5045036678` 继续要求 Interface 1.3、六个 `exit_id`、
  `reprepare_required` 的 target-owned authoring split、真实 public wrapper eval 与
  actual-exit-first schema selection。
- #105 已完成的 transaction semantics 保持不变；#115、#119、#132 仍不属于本 task close
  scope。#119 继续持有 Finish-family integration 与 #115 closure，#132 继续持有 upstream
  overlay cleanup。
- `issue-scope-ledger.json` 保持 `close_issues=[118]`，#81/#115 为 related，#119/#132 为
  follow-up。
- 恶意伪造/篡改、并发 finalizer、锁、TOCTOU、新 fault injection、crash consistency 与跨 OS
  atomicity 仍为明确 out of scope。

### 已检查文件

- Planning 与 authority：`prd.md`、`design.md`、`implement.md`、planning approval、live
  Issue/comment、dependency state 与 current issue ledger。
- Handoff 与 recovery：完整 implementation/check assignment chain、
  `implementation-handoff-codex-trace-write-fix.md`、历史 Phase 2、Branch Review 与 finding
  closure reports。
- 当前修复：`trellis/skills/guru-team/adapters/eval/native_adapter.py`、dogfood installed copy、
  `trellis/skills/guru-team/tests/test_skill_packages.py` 与 extension manifest binding。
- Finalizer runtime 与 tests：canonical/dogfood `guru_team_trellis.py`、完整 runtime tests、
  `CloseoutTransactionContractTest`、finalizer/#116/#117 package tests。
- Public contracts：`guru-finalize-task/**`、producer/consumer bindings、Interface 1.3 schemas、
  examples、real wrapper、shared/Codex/Claude/Cursor corpora 与 adapters。
- Distribution：registry、extension manifest、preset installer、canonical/installed/Agents/
  Codex/Claude/Cursor copies、ownership inventory、dogfood drift 与 clean throwaway chain。
- Durable SSOT：`.trellis/spec/workflow/**`、`.trellis/spec/preset/**`、`.trellis/spec/docs/**`、
  package contract 与 repository/preset/workflow README surfaces。
- Protected no-diff：canonical/dogfood workflow Markdown、upstream `trellis-finish-work`
  Skill/Command/Prompt family、official `.trellis/scripts/task.py` 与 preset overlays。
- Complete scope：全部 532 个 committed paths和当前全部 dirty/untracked paths，不限于最新
  adapter/test delta。

### 实现语义复核

`F-CODEX-TRACE-WRITE-01` 可在受支持的正常路径重现：Codex 使用 trusted Git root 与
`workspace-write`，但 run root 位于 repository 外部；旧 argv 未授权拥有
`native-trace-helper.py`、`native-trace.json` 和 `native-last-message.txt` 的 execution root，
因此 runner 可返回 0 而 structured case 为 `native_trace_unavailable`，真实 wrapper 未执行。

当前 diff 在 Codex `native_argv()` 中把 `native_request_path.resolve().parent` 作为 exact
execution root，并加入 `--add-dir <execution-root>`。既有 trusted-root `--cd`、workdir grant、
public projection grant、output-last-message 与 native protocol 均保留。新增 regression 使用
absolute repository-external run root 和 workspace-enforcing shim；缺少 exact grant 时拒绝旧
合同，授权正确时通过 trace helper 执行真实 finalizer `invoke.sh`。

真实 Codex eval 的 runner rc=`0`，structured run/case=`passed/passed`，
`actual_exit=publication_review_stale`；execution root 位于 repository 外且存在于 `--add-dir`，
trusted root 等于 task worktree，native request 不含 `expected_exit`，trace 最后一个 event 是
真实 `guru-finalize-task/scripts/invoke.sh`，wrapper rc=`0`。因此该 finding 已由当前 diff
解决，normal-path closure 证据充分。

该修复未新增或改变 public profile、DTO、schema、typed exit、consumer、semantic gate、
private transaction state、recovery order 或用户命令，也未承接 #119/#132 scope。

### 十项 adequacy review

1. `requirements`：passed。Live authority、approved planning 与 close-only-#118 ledger 一致。
2. `design`：passed。Exact execution-root grant 属于既有 native adapter writable boundary，
   不改变 finalizer semantic ownership 或 transaction design。
3. `implementation`：passed。Canonical/dogfood adapter byte-identical，manifest 绑定 current；
   grant 精确指向 request parent，没有扩大 repo/public contract ownership。
4. `tests`：passed。Focused regression、runtime、transaction、Skill graph、package、preset、
   ownership、wrapper、adapter 与 clean throwaway coverage 完成。
5. `docs_ssot`：passed。strategy=`ssot_first`；task-level durable delta 已合并，本次修复为
   `no_docs_update_needed`，只恢复实现对现有 trace/real-wrapper SSOT 的符合性。
6. `cross_layer`：passed。Public DTO 与 actual-exit schema ordering 不变，native request 仍排除
   `expected_exit`，owner-private runtime facts未进入 public handoff。
7. `compatibility`：passed。#105 behavior、七个 distinct profiles、六 exits、#116/#117 edges、
   workflow markers `12/46/27` 与 protected surfaces 不变。
8. `deployment_and_operations`：passed。无 dependency、CI/CD、container、Compose、K8s、Helm/
   Kustomize、DB migration、Makefile、Terraform、deploy 或 production-write 影响。
9. `agent_recovery`：passed for semantic handoff。Implementation agent 已 completed，当前
   checker assignment/recovery chain 可由主会话在 terminal handoff 后闭合记录。
10. `verification_completeness`：passed。83 条正式命令、83 个唯一 ID 与 4 条明确 omission
    覆盖完整 scope；外部认证与后续 pushed-ref 状态被诚实界定，没有冒充 pass。

### 已修复问题

- 文件：`trellis/skills/guru-team/adapters/eval/native_adapter.py`、
  `.trellis/guru-team/skills/adapters/eval/native_adapter.py`、
  `trellis/skills/guru-team/tests/test_skill_packages.py`、
  `.trellis/guru-team/extension.json`。
- 问题：`F-CODEX-TRACE-WRITE-01`，repo-external Codex execution root 未进入 writable
  `--add-dir`，可能造成 runner rc=0 但 native trace unavailable、真实 wrapper 未执行。
- 修复：当前 implementation diff 授权 exact execution root，补充会拒绝旧 argv 的真实
  wrapper regression，并同步 canonical/dogfood/manifest identity。本 reviewer 未再修改这些
  文件；全量复核确认 finding 已关闭。

本轮未发现需要 reviewer 自修复的额外 code、schema、config、docs 或 test 问题。

### 未修复问题

- Claude live native case 返回 structured `execution_error`：HTTP 401 `Invalid API key`，
  input/output tokens 均为 0，`permission_denials=[]`。这是外部认证 residual，不是 wrapper、
  corpus 或 adapter protocol defect；不得描述为 Claude live pass。
- Cursor live case 返回预期 stable `unsupported`，原因是 authentication unavailable；未声称
  semantic pass。
- Feature exact ref 尚未 push，remote marketplace/extension verification 尚未发生。这是后续
  #117/#118 finalization owner gate 的预期前置，不是当前 Phase 2 finding，也不授权本 reviewer
  push。
- Full committed `git diff --check origin/main...HEAD` 只报告 immutable Round 9 raw evidence
  line 203 的 historical trailing whitespace；当前 effective diff 通过。改写该历史 raw evidence
  会破坏已绑定 identity，因此不自修复。
- 旧 `phase2-check.json`、task commit、Branch Review、publication review、immutable plan 与
  finalization confirmation 均早于当前 adapter/test/handoff/report delta，必须由主会话依次
  重新执行 owner gates。

以上均不是 current-scope P0-P3 finding。

### 验证结果

- Lint：通过。Current/effective diff whitespace、JSON syntax、Bash syntax、source/installed
  validator、ownership、overlay drift、parity、protected no-diff 与 sensitive-material scan 均
  通过；仅保留上述 immutable historical whitespace observation。
- TypeCheck：通过适用检查。仓库无独立 configured static type checker；changed Python
  `py_compile`、runtime/tests 与 adapter execution 通过。
- Tests：通过。Runtime full `626 passed, 13 skipped`；
  `CloseoutTransactionContractTest` `104 passed`；Skill graph `180 passed`；finalizer package
  `5 passed`；#116/#117 packages `28 passed`；preset installer `45 passed`；ownership tests
  `9 passed`。
- Source/installed validators：通过；13 active，workflow markers `12/46/27`；installed
  inventory 2659 files，零 sidecar/removal/conflict。
- Shared wrapper：source `8/8`、installed `8/8`，覆盖六 exits 及 verified/not-required
  re-entry。
- Codex：真实 trusted-root、repo-external run-root case `passed/passed`，actual exit 为
  `publication_review_stale`，真实 wrapper trace closure 通过。
- Claude/Cursor：分别为 external 401 residual 与 expected unsupported，均未冒充 pass。
- Clean throwaway：rc=`0`；完整 marketplace/init/install/update/reapply/`.new`/`.bak`/
  all-platform/OOTB chain 通过，终态零 sidecar/cache。
- Dogfood/upgrade：replica all-platform apply、installed validator、overlay drift、canonical/
  platform parity 通过；current worktree 因避免覆盖用户并行 delta而有意不重跑 mutating
  all-platform apply。
- Formal command evidence：83 commands、4 intentional omissions；三次 probe setup error
  分别由 corrected focused test names、正确 manifest locator、registry live `state` 字段重跑
  supersede，纠正轮全部通过。

### 证据交接

- 阶段二：覆盖 live authority、approved planning、完整 committed range、全部 current dirty/
  untracked delta、implementation handoff、finding normal-path reproduction/closure、runtime、
  tests、public wrappers、platform adapters、distribution、install/update/reapply、ownership、
  protected boundaries、安全/部署与 repository hygiene。P0/P1/P2/P3=`0/0/0/0`，十项
  adequacy 全部 passed。本报告及同轮 JSON 可支撑主会话生成新的 `phase2-check.json`；recorder
  必须绑定届时 current paths、artifact digests 与 completed checker lifecycle。
- Docs SSOT：plan strategy=`ssot_first`。Task-level durable docs delta 已合并且 current；本次
  Codex fix 的 reconciliation 为 `no_docs_update_needed`，implementation handoff、finding
  closure 与本报告是 task-history-only content。历史 six-to-seven profile refinement 是可达
  standalone `not_required` 正常路径的已记录 refinement，不是新的 scope expansion。#119、
  #132 与 exact pushed-ref verification 保持 follow-up/current PR limitation。
- Branch Review：本轮不执行 Branch Review，也不修改 `review.md`/`review-gate.json`。主会话在
  fresh task commit 后必须由独立 reviewer 覆盖新的完整 `origin/main...HEAD`，再执行
  publication review 与新的 immutable closeout plan/digest confirmation。
- 安全与部署：未发现 secret、credential、signed URL、客户数据或 raw provider payload；
  无 dependency、CI/CD、container、K8s、DB migration、Makefile、deploy 或 production write
  影响。Distribution 影响仅为已验证的 additive Guru package/runtime/schema/preset assets。
- Structured residuals：Claude 401、Cursor unsupported、exact pushed-ref verification pending、
  immutable historical whitespace；均已分类、非阻断且未夸大验证状态。

### 结论

`F-CODEX-TRACE-WRITE-01` 已由当前 diff 在受支持的真实 Codex normal path 上关闭。实现与
Issue #118 accepted-current authority、approved Docs SSOT、Interface 1.3 public/private boundary、
#105 transaction semantics 以及 #119/#132 ownership 一致；完整 regression、wrapper、
distribution、install/update 与静态门禁均通过，没有 open P0-P3 finding。建议 Phase 2 typed
exit=`passed`。

主会话下一步必须先记录本 checker completed event，再运行 Phase 2 recorder/checker、fresh task
commit、独立 Branch Review、publication review 与新的 immutable finalization confirmation；旧
plan、gate 与 confirmation 不得复用。

本报告和 command evidence 的最终 SHA-256、bytes 与 lines 由 terminal handoff提供，避免正文
自引用。
