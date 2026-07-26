# Issue #118 Phase 2 Round 3 独立完整检查报告

## 检查完成

### 检查身份与边界

- 检查代理：`/root/issue118_phase2_round3_check`，逻辑角色为“阶段二检查代理”。
- Assignment event：`evt-0212-11e11f0952`。
- Worktree：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/118-guru-finalize-task`。
- Task：`.trellis/tasks/07-26-118-guru-finalize-task`。
- Branch：`feat/118-guru-finalize-task`。
- Base / reviewed HEAD：`7820a9eeec2a2a75fb52fba156a7211d9f9fb09c`。
- 证据根：`/tmp/guru-118-phase2-round3.6pRn28`。
- Workspace boundary 通过：expected workspace 与 actual repo root 均为指定 task worktree；source checkout clean；task worktree 为预期 dirty implementation；`suspicious_source_artifacts=[]`。
- Planning approval 通过：`typed_exit=approved`；artifact SHA-256 `1bcc7712aa1c8a74f72ecfa4a90d8384d77fbd7a6ed95f65714737ffa600c9c6`；facts SHA-256 `9d0d14bada5d4990a3f62402bdb5b28275fd1c7bf20476cdd01f1145defbeb70`；approved/current HEAD 相同。
- `check.jsonl` 只有 seed row，因此按 fallback 读取 planning artifacts、workflow/preset/docs specs、`trellis-check` 与 `guru-check-task` 合同。
- 本代理没有修改 product、planning、durable docs、spec、runtime、schema、config、installer 或 tests。唯一 repo writes 是两个 task-local Round 3 probe 与本报告。没有调用 Phase 2 recorder/checker，没有 commit、push、PR、GitHub mutation 或 finish。

### 已检查文件

- Planning/scope：`prd.md`、`design.md`、`implement.md`、`implementation-handoff-round2.md`、`issue-scope-ledger.json`、`task.json`、`task-start-context.json`、planning approval、prior Phase 2 reports/check artifact、agent recovery chain。
- Canonical package：`trellis/skills/guru-team/packages/guru-finalize-task/**`，包括 Skill、contract、Interface 1.3、六 profiles、六 exits、consumer/projection、private artifacts、五 wrappers、八个 production eval cases 与 package tests。
- Runtime：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py` 的 #116/#117 owner checks、preview、route validator、gate recorder/checker、transition executor、#105 closeout delegate、archive recovery、public invocation 与 full regression suite。
- Eval：`trellis/skills/guru-team/adapters/eval/native_adapter.py` 的 finalizer production staging，以及 source/installed discovery、shared real wrapper transcripts。
- Distribution：registry、extension manifest、consumer schemas、canonical/installed shared/Agents/Codex/Claude/Cursor copies、preset installer/verifier、ownership inventory、generated dogfood runtime/package。
- Durable Docs SSOT：repository/workflow/preset README；`.trellis/spec/workflow/{index,quality-guidelines,skill-package-contract,workflow-contract}.md`；`.trellis/spec/preset/{installer,upstream-ownership}.md`；`.trellis/spec/docs/public-docs.md`。
- Explicit no-write：canonical/dogfood global workflow、upstream `trellis-finish-work` Skill/Command/Prompt、preset overlays、official `.trellis/scripts/task.py`。
- 安装/升级：fresh clean throwaway marketplace discovery、local unpublished canonical sample、preset initial install/reapply、`trellis update`、managed hash、`.new/.bak` recovery、platform distribution、contract/eval discovery、wrapper invocation 与 final hygiene。

### Scope-first candidate qualification

| Candidate | Requirement/design trigger | 正常路径复现 | Disposition |
| --- | --- | --- | --- |
| `C-RECOVERY-03`：#117 evidence 被合法 finalization metadata tail 判 stale | `prd.md` R10/R11、AC6/AC8；`design.md` 4.2、5.2、5.3、6 | 同 task/plan/reviewed HEAD 的 `verified` owner result 在 reviewed content HEAD 通过；正常新增 `task-finalization-gate.json` 或 evidence metadata commit 后，#117 checker 同时按 current local HEAD 与 task worktree snapshot 判旧证据 stale。没有类似 publication augmentation 的 finalization allowlist path，无法进入 pre-draft、same-plan、archived/ready recovery。 | `current_scope` / `P1` / `F-RECOVERY-03` |
| `C-MATERIALIZATION-04`：required executor 前可直接发布 terminal DTO | `prd.md` R7/R10/R11/R12、AC6/AC7/AC9；`design.md` 5.1、5.2、5.3、7 | `prepared + verification_required` 和 `evidence_pushed + published` 都可让 checker 接受完整 public DTO；`cmd_invoke_stage0_skill` 直接返回 gate output，transition executor 调用数为 0。前者跳过 content push，后者跳过 draft/projection/archive/three-way HEAD/ready。 | `current_scope` / `P1` / `F-MATERIALIZATION-04` |
| `C-LOCATOR-05`：真实 archive 后 public wrapper locator continuity 断裂 | `prd.md` R7/R11、AC2/AC7；`design.md` 3.2、5.3、6 | Executor 在 active task 上先物化 `published.task_ref=active locator`，随后 archive。真实目录 move 后 active 不存在、resolver 找到 exact archive locator，但 `finalization_task_dir` 要求 resolved locator 仍等于 public input active locator并阻断；公开 `published` example 则使用 archive locator。 | `current_scope` / `P1` / `F-LOCATOR-05` |
| `C-IDENTITY-06`：`verification_required.repo_ref` 未绑定 plan objective facts | `prd.md` R4/R7/R10、AC2/AC5/AC6；`design.md` 3.2、4.1、5.1 | 在 `prepared` 正常 publication entry 中，schema-valid `repo_ref=other/repository` 与 plan `repo=castbox/guru-trellis` 不一致仍通过 route validator并由 wrapper 原样发出；只有下游 #117 task identity checker 才拒绝。 | `current_scope` / `P2` / `F-IDENTITY-06` |
| `C-STATE-07`：`resume_finalization` 缺少 objective-state compatibility | `prd.md` R11、AC8；`design.md` 3.3、5.2、6 | `publication_ready` 的初始 `prepared` state 可选择并通过 `resume_finalization`，尽管设计矩阵把 prepared first-side-effect-unconfirmed 映射到 `blocked`，resume 只属于 same-plan transient/partial/archive/ready retry。 | `current_scope` / `P2` / `F-STATE-07` |
| `C-REPO-ALT`：#117 `repo_ref` 与 plan repo 可能经合法 owner evidence 静默错配 | R6/R10 | #117 workflow evidence 本身把 `repo_ref` 绑定 task-start context；plan executor也在副作用前校验 remote/repository。因此无需伪造 owner artifact 时，独立的“已验证旧 repo + 同 plan_ref 新 repo”路径不可成立。有效问题已收敛为 `C-IDENTITY-06` 的 gate/output mismatch。 | `not_reproducible_supported_path` / route=`none` |
| `C-OOS-01`：恶意伪造、篡改、并发、锁、TOCTOU、额外 fault/crash/cross-OS 加固 | `prd.md` R16 与 repository AGENTS boundary | 五个 findings 均无需这些非常规条件即可复现；本轮没有把排除项引入 implementation recommendation。 | `out_of_scope` / route=`none` |

### 已修复问题

- 无 product 问题由本代理修复；角色边界要求 findings 返回实现阶段。
- 本轮 validators 曾生成且仅生成两个 reviewer temporary cache roots：`.trellis/scripts/common/__pycache__` 与 `trellis/workflows/guru-team/scripts/python/__pycache__`。在确认精确路径后删除其 `.pyc` 与空目录；final hygiene 对 `.new`、`.bak`、`.pyc`、`__pycache__` 的 zero-hit assertion 已通过。没有删除任何其它路径。

### 未修复问题

#### F-RECOVERY-03（P1，open）：#117 current evidence 无法跨 finalizer-owned metadata tail

- 代码：`guru_team_trellis.py:26167`、`:26361`、`:26389`、`:26398`、`:29864`、`:29911`、`:30141`、`:30461`；正常 evidence commit 位于 `:29529`。
- 问题：#117 checker 把 workflow `reviewed_head` 同时当作当前 local HEAD，并把包含 finalizer gate/task delta 的完整 task worktree snapshot 作为 freshness。验证完成后必须写入的 finalizer gate、ledger/evidence metadata 或 evidence commit 都会改变至少一个绑定，旧 owner result随即 stale。`FINALIZATION_COMMITTED_RECOVERY_STATES` 只能在 route validator 中放行 `archived|ready`，但 context 构建更早已被 #117 checker阻断。
- 影响：R10 要求的 verified publication re-entry、R11/AC8 的 same-plan pre-draft 与 committed recovery 在正常 metadata tail 后不可达；#105 engine regression tests 通过不代表新的 owner boundary 可进入该 engine。
- 修复要求：保留 #117 generic owner contract，在 finalizer owner checker 增加精确、plan-bound、allowlist-only 的 finalization augmentation，区分 reviewed content HEAD 与预期 metadata tail；覆盖 gate write、evidence commit/push、active/archive/ready recovery。不得接受任意 task drift，也不得 archive 后通用重验 private evidence。Durable Docs SSOT 需明确此 augmentation，与当前“任何 local HEAD/task worktree drift 均 stale”的通用 #117 表述消除冲突。
- Probe：`round3-evidence/recovery-metadata-tail-probe.py`，SHA-256 `c211610e143dcd90ba54307ae0e5fcfc4126b46b96e9015b39bb4713440158db`，4618 bytes；stdout SHA-256 `647859842783163515cf9c6ded1bbd72a0f760bcba267e7df99607d4a06b5671`，772 bytes；stderr empty；exit 0。

#### F-MATERIALIZATION-04（P1，open）：public wrapper 未证明 required transition 已执行

- 代码：`guru_team_trellis.py:24906`、`:24927`、`:30239`、`:30307`、`:30320`、`:30560`；eval staging `native_adapter.py:2700`、`:2732`、`:2834`、`:2904`、`:2916`。
- 问题：checker 与 public wrapper 之间没有 pre/post execution phase binding。`verification_required` 在 `prepared` 可携带完整 DTO，`published` 在有 current verification 的 `evidence_pushed` 可携带完整 DTO；两者经 checker 后由 public wrapper直接返回。Wrapper 与独立 transition executor 之间没有“已执行合法 next transition”的 objective evidence。
- 影响：可以在 content push 前请求 #117，也可以在 PR/archive/three-way HEAD/ready 全部未发生时返回 terminal `published`。这违反 R10/R11 与 design 5.2 的 `one deterministic transition -> AI route review -> checker refresh -> external DTO` 顺序。
- 修复要求：保持“只有 `published` 可使用 private pre-output marker”的批准边界，不给其它 exit 新增 marker。Pre-executor `published` 必须只接受 exact private marker；`verification_required` 必须由 refreshed objective state证明 content push 已完成；post-executor public DTO 必须绑定实际 transition/PR/ready facts。Public wrapper 只能序列化 checker 已证明 transition 完成的 output，不能仅凭完整 shape 推定完成。
- Eval gap：八个 production cases 均调用真实 `invoke.sh`，但 adapter 对 verification case 预置 `content_pushed`、对 verified/not-required case 预置 `evidence_pushed` 和完整 `published` DTO，且从不执行 real transition executor。因此 8/8 pass 正好漏掉 owner-checker/transaction ordering。

#### F-LOCATOR-05（P1，open）：真实 archive 后 terminal public DTO 无法连续物化

- 代码：`guru_team_trellis.py:29564`、`:29572`、`:29770`、`:30523`；ordinary resolver `:4663`、`:4772`；public example `examples/public-published-output.json`。
- 问题：`finalization_gate_with_published_output` 在 archive 前用 active `task_dir` 生成 `published.task_ref`；archive 后 active path 不存在。下一次 wrapper 用原 public input active locator 时，resolver 能找到 archive path，但 exact-locator equality 立即阻断。真实 output 与公开 example 的 archive locator 语义不一致。
- 影响：即使先正确执行 transition，最终 `published` DTO 仍无法通过真实 public wrapper输出；Finish response 得到一个不存在的 task path，R7/AC2 的 consumer handoff 与 R11/AC7 的 ready terminal closure 均未成立。
- 修复要求：只允许 closeout plan 绑定的 exact former-active locator 向 exact archive locator 的确定性投影；materialized public output 使用 validated archive locator。不得把任意 basename/alias 放宽成 public identity。

#### F-IDENTITY-06（P2，open）：`verification_required.repo_ref` 未绑定 immutable plan

- 代码：`guru_team_trellis.py:30261`、`:30274`、`:30587`；#117 task identity checker `:26138`。
- 问题：route validator 对 non-marker output 只绑定 `task_ref`、`plan_ref`、`reviewed_head`，遗漏 `verification_required.repo_ref == plan.git.repo`。Executor 会写正确 repo，但 pre-execution complete DTO 可带任意 schema-valid GitHub repository identity。
- 影响：checker-passed public output不代表当前 immutable plan；下游 #117 才 fail closed，造成错误 handoff 与无法解释的 verification block，而非在 finalizer owner boundary 精确拒绝。
- 修复要求：在 route/objective checker 中把每个业务 identity field 绑定到其唯一 current fact；对 `verification_required` 至少绑定 exact plan repo。不要依赖 downstream checker补救 producer contract。

#### F-STATE-07（P2，open）：`resume_finalization` 可从非 recovery state 发出

- 代码：`guru_team_trellis.py:30287` 至 `:30337`；design recovery matrix `design.md:168` 至 `:177`。
- 问题：route validator显式检查 `publication_review_stale`、`verification_required`、`reprepare_required` 与 `published`，但没有检查 `resume_finalization`。初始 `publication_ready + prepared` 因而能返回 resume DTO。
- 影响：owner checker 不能证明 route 对应 design 规定的 same-plan transient/partial/archive/draft-to-ready recovery；调用方会 re-enter 相同 Skill，而不执行首次确认/content push 或明确 blocked route。
- 修复要求：复用 #105 state resolver 的 legal-next-transition 事实，精确限定 resume-compatible objective states；对 prepared、reprepare、stale、ready terminal 等非 resume states 增加 negative regression，不把 private state暴露到 public DTO。

其余四个 finding 的合并 probe：`round3-evidence/published-materialization-locator-probe.py`，SHA-256 `9837cc7f4a4650cfd49d7ea142427c3afbbb186056f7a18ead87a3876d751bfb`，11659 bytes；stdout SHA-256 `d42ad301308a7a81ee092bb634261058852a37402e20b5efa9f2c94b54a73463`，1006 bytes；stderr empty；exit 0。

### Semantic adequacy

| Dimension | 结果 | Round 3 evidence |
| --- | --- | --- |
| requirements | 失败 | `F-RECOVERY-03` 违反 R10/R11；`F-MATERIALIZATION-04` 违反 R10-R12；其它 findings 违反 R4/R7/R11 与 AC2/AC5-AC9。 |
| design | 失败 | 5.2 transition/checker ordering、5.3 transaction order、6 recovery matrix 与 public locator/objective identity未被实现。 |
| implementation | 失败 | 五个正常 honest-but-fallible caller/recovery path均可复现；三个 P1 阻断或提前宣告核心 closeout terminal flow。 |
| tests | 失败 | 605/178/45/4 与 8/8 全通过，但 eval staging 不执行 transition/archive，且没有 metadata-tail、wrong repo、prepared resume negative coverage。 |
| docs_ssot | 失败 | `ssot_first` 的 counts、activation、#119/#132 boundary 与 task delta 已合并且正确；但 #117 generic “local HEAD/task drift stale” 与 finalizer必需 metadata tail 缺少明确 augmentation，current durable contract未闭环。 |
| cross_layer | 失败 | #117 evidence -> finalizer checker -> executor -> archive -> public wrapper 之间存在 freshness、phase、locator、repo identity 与 recovery state断点。 |
| compatibility | 失败 | #105 full regression保持通过，但新 finalizer owner boundary无法可靠进入/恢复同一 engine，不能据此声明 observable recovery compatibility。 |
| deployment_and_operations | 通过 | 无 dependency、CI/CD、container、Compose、K8s/Helm/Kustomize、DB migration、Makefile、deploy 或 production data-write 变化。 |
| agent_recovery | 通过（待本轮 terminal event） | 既有 replacement/recovery chains均闭合；Round 3 assignment/current progress证据完整。Main 在收到本报告后需记录 completed 并重跑 assignment validator。 |
| verification_completeness | 失败 | 本检查覆盖完整 scope/diff/matrix且所有命令终态已知，但 product production eval本身没有验证真实 owner-checker/transition/archive链，五个 findings 阻止 Phase 2 pass。 |

### 验证结果

- Lint：通过。Bash syntax、Python compile、`git diff --check`、task validate、ownership、drift、byte identity、executable modes、no-write、no-deploy-impact 与 final hygiene 均 exit 0。
- TypeCheck：不适用。仓库没有独立 configured type checker；Python compile、JSON schema validators 与 unittest 是当前适用静态/合同验证。
- Tests：命令层通过；语义结论失败。
  - Runtime full：605 tests，13 skipped，exit 0。
  - Skill package full：178 tests，exit 0。
  - Preset full：45 tests，exit 0。
  - Finalizer package：4 tests，exit 0。
  - Installed shared real public wrapper：8/8 passed，六 actual exits均覆盖。
  - Source/installed：13 active、0 planned、0 legacy；global markers保持 12 invokes / 46 exits / 27 targets。
  - Contract discovery：六 profiles、六 output contracts、两个 private artifacts；source/installed bytes相同。
  - Eval discovery：八 cases、四 adapters；source/installed bytes相同。
  - Ownership：43 frozen / 43 active / 0 removed；dogfood overlay drift为零。
  - Canonical/installed shared/Agents/Codex/Claude/Cursor package、runtime、adapter与 consumer schemas byte-identical；scripts executable。
  - Fresh clean throwaway：exit 0，覆盖 public marketplace discovery、local unpublished canonical workflow sample、initial install/reapply、`trellis update`、managed hash、`.new/.bak` recovery、platform copies、wrapper/eval/ownership/sidecar checks。

### 精确命令证据

所有命令从 task worktree root执行；stdout/stderr 在进程启动时分别写入 evidence root。表内 `<evidence>` 精确代指 `/tmp/guru-118-phase2-round3.6pRn28`；`e3b0c442...` 为 empty stream。格式：`ID | exit | stdout SHA-256/bytes | stderr SHA-256/bytes | exact argv`。

| ID | exit | stdout SHA-256 / bytes | stderr SHA-256 / bytes | Exact argv |
| --- | ---: | --- | --- | --- |
| `E00` | 0 | `3b2d75bb35e9d1f870e1eb06be1d970d2d2c40cdb7044dcbd76555d1ea6b47b6` / 83 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` / 0 | `pwd` then `git rev-parse --show-toplevel` |
| `E01` | 0 | `89842a60a1a13c76cf84db7b521ac0eb272b390acb21cb66bf8b33c1ef573f39` / 126 | empty / 0 | `PYTHONPYCACHEPREFIX=<evidence>/pycache-entry python3 ./.trellis/scripts/task.py current --source` |
| `E02` | 0 | `a226392e00d45eb09f2e43a605a16105ce0a758ab257ed430de0637420aba9cb` / 40573 | empty / 0 | `PYTHONPYCACHEPREFIX=<evidence>/pycache-boundary ./.trellis/guru-team/scripts/bash/check-workspace-boundary.sh --json --task .trellis/tasks/07-26-118-guru-finalize-task` |
| `E03` | 0 | `bcf2b0e32167f2c8458253c3944d0e71521b0ec29c0df4ed9c278eca7cf761c8` / 738 | empty / 0 | `PYTHONPYCACHEPREFIX=<evidence>/pycache-approval ./.trellis/guru-team/scripts/bash/check-planning-approval.sh --json --task .trellis/tasks/07-26-118-guru-finalize-task` |
| `E04` | 0 | `5adbfc63bab462907d3942e731fec357152f7cb2dc17ff8ee914c948992e967d` / 82 | empty / 0 | `PYTHONPYCACHEPREFIX=<evidence>/pycache-context python3 ./.trellis/scripts/get_context.py --mode packages` |
| `E05` | 0 | `87859f8d6638c788f1994e2bc7ea7559fe3913de25931d5f82125507f293d4a7` / 2548 | `02d1c5f06abc3d67ec78c297541417e6cf5192839f8eb5b75ccbdff2d6eb82b6` / 4430 | `PYTHONPYCACHEPREFIX=<evidence>/pycache-runtime python3 trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py` |
| `E06` | 0 | empty / 0 | `af6c4eb1d146cd2828dc5a9840fceb8db6d83418fee7038be128fa4fddced0aa` / 4290 | `PYTHONPYCACHEPREFIX=<evidence>/pycache-packages python3 trellis/skills/guru-team/tests/test_skill_packages.py` |
| `E07` | 0 | empty / 0 | `485f4c8a8ab70188edb7aad80b669fbdd0850cbce329ecc2f0bdd4521598345f` / 809 | `PYTHONPYCACHEPREFIX=<evidence>/pycache-preset python3 trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py` |
| `E08` | 0 | empty / 0 | `9e4b0e9b0840f3ab7eadc1829b4884276b298e673187157c076ca2930f731df6` / 102 | `PYTHONPYCACHEPREFIX=<evidence>/pycache-finalizer python3 trellis/skills/guru-team/packages/guru-finalize-task/tests/test_contract.py` |
| `E09` | 0 | `647859842783163515cf9c6ded1bbd72a0f760bcba267e7df99607d4a06b5671` / 772 | empty / 0 | `PYTHONPYCACHEPREFIX=<evidence>/pycache-recovery-probe python3 .trellis/tasks/07-26-118-guru-finalize-task/round3-evidence/recovery-metadata-tail-probe.py` |
| `E10` | 0 | `d42ad301308a7a81ee092bb634261058852a37402e20b5efa9f2c94b54a73463` / 1006 | empty / 0 | `PYTHONPYCACHEPREFIX=<evidence>/pycache-published-probe python3 .trellis/tasks/07-26-118-guru-finalize-task/round3-evidence/published-materialization-locator-probe.py` |
| `E11` | 0 | `1c6b31cc2c6df8d7682eb57b6097bdfed893eab3bdaf4c9d4fe42800f5880d2a` / 1346 | empty / 0 | `.trellis/guru-team/scripts/bash/check-skill-packages.sh --root . --mode source --json` |
| `E12` | 0 | `4c2be4822816debd80059fc15990f3c5b89403e734b2007298adf720f0105ed9` / 1535 | empty / 0 | `.trellis/guru-team/scripts/bash/check-skill-packages.sh --root . --mode installed --json` |
| `E13` | 0 | `07476c6bd57804e375a7557774bb4077409e6a2698f2f9b63aa3403df69c60b5` / 13490 | empty / 0 | `trellis/workflows/guru-team/scripts/bash/discover-skill-contract.sh --root . --mode source --skill guru-finalize-task --json` |
| `E14` | 0 | `07476c6bd57804e375a7557774bb4077409e6a2698f2f9b63aa3403df69c60b5` / 13490 | empty / 0 | `.trellis/guru-team/scripts/bash/discover-skill-contract.sh --root . --mode installed --skill guru-finalize-task --json` |
| `E15` | 0 | `42a4d8d55ecebfd388ba413d75078d6dfb35593f492b76aa59765e1f15c52756` / 3375 | empty / 0 | `trellis/workflows/guru-team/scripts/bash/discover-skill-evals.sh --root . --mode source --skill guru-finalize-task --json` |
| `E16` | 0 | `42a4d8d55ecebfd388ba413d75078d6dfb35593f492b76aa59765e1f15c52756` / 3375 | empty / 0 | `.trellis/guru-team/scripts/bash/discover-skill-evals.sh --root . --mode installed --skill guru-finalize-task --json` |
| `E17` | 0 | `4b97698fad4de2b10c43e6ad07fbbb700ee35d4bba90d528d5b914d79a60e9c3` / 7527 | empty / 0 | `PYTHONPYCACHEPREFIX=<evidence>/pycache-evals .trellis/guru-team/scripts/bash/run-skill-evals.sh --root . --mode installed --skill guru-finalize-task --adapter shared --run-root <evidence>/eval-installed --json` |
| `E18` | 0 | `5403ca759ffa967dbcc231bab5f5d000f8b9da2e12bfb82789458eacea1183e5` / 1731 | empty / 0 | `trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json` |
| `E19` | 0 | `b3bafca507c4743e965cd81eed5d8ee845c91589afaf38a18f1702ef854e4bd5` / 1790 | empty / 0 | `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh --repo .` |
| `E20` | 0 | empty / 0 | empty / 0 | `find trellis/workflows/guru-team/scripts/bash trellis/presets/guru-team/scripts/bash .trellis/guru-team/scripts/bash trellis/skills/guru-team/packages/guru-finalize-task/scripts .trellis/guru-team/skills/packages/guru-finalize-task/scripts .agents/skills/guru-finalize-task/scripts .codex/skills/guru-finalize-task/scripts .claude/skills/guru-finalize-task/scripts .cursor/skills/guru-finalize-task/scripts -type f -name '*.sh' -print0 \| xargs -0 bash -n` |
| `E21` | 0 | empty / 0 | empty / 0 | `PYTHONPYCACHEPREFIX=<evidence>/pycache-compile python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py trellis/skills/guru-team/adapters/eval/native_adapter.py` |
| `E22` | 0 | empty / 0 | empty / 0 | `git diff --check` |
| `E23` | 0 | `53258e0eefd6d7cbd1d1af4e22029d99c1893edd325760ec743864222d862c58` / 311 | empty / 0 | `PYTHONPYCACHEPREFIX=<evidence>/pycache-task python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-26-118-guru-finalize-task` |
| `E24` | 0 | empty / 0 | empty / 0 | `git diff --exit-code 7820a9eeec2a2a75fb52fba156a7211d9f9fb09c -- trellis/workflows/guru-team/workflow.md .trellis/workflow.md .agents/skills/trellis-finish-work .codex/prompts/trellis-finish-work.md .codex/skills/trellis-finish-work .claude/commands/trellis/finish-work.md .cursor/commands/trellis/finish-work.md trellis/presets/guru-team/overlays .trellis/scripts/task.py` |
| `E25` | 0 | empty / 0 | empty / 0 | `for copy_root in .trellis/guru-team/skills/packages/guru-finalize-task .agents/skills/guru-finalize-task .codex/skills/guru-finalize-task .claude/skills/guru-finalize-task .cursor/skills/guru-finalize-task; do diff -qr trellis/skills/guru-team/packages/guru-finalize-task "$copy_root"; done; cmp trellis/workflows/guru-team/scripts/python/guru_team_trellis.py .trellis/guru-team/scripts/python/guru_team_trellis.py; cmp trellis/skills/guru-team/adapters/eval/native_adapter.py .trellis/guru-team/skills/adapters/eval/native_adapter.py; cmp trellis/skills/guru-team/consumers/workflow/production/finalize-task-published.schema.json .trellis/guru-team/skills/consumers/workflow/production/finalize-task-published.schema.json; cmp trellis/skills/guru-team/consumers/stop/production/finalize-task-blocked.schema.json .trellis/guru-team/skills/consumers/stop/production/finalize-task-blocked.schema.json` |
| `E26` | 0 | empty / 0 | empty / 0 | `find trellis/skills/guru-team/packages/guru-finalize-task/scripts .trellis/guru-team/skills/packages/guru-finalize-task/scripts .agents/skills/guru-finalize-task/scripts .codex/skills/guru-finalize-task/scripts .claude/skills/guru-finalize-task/scripts .cursor/skills/guru-finalize-task/scripts trellis/workflows/guru-team/scripts/bash .trellis/guru-team/scripts/bash -type f -name '*.sh' -print0 \| while IFS= read -r -d '' file; do test -x "$file"; done` |
| `E27` | 0 | empty / 0 | empty / 0 | `hits=$(git status --short \| sed 's/^...//' \| rg '(^\|/)(\.github\|Dockerfile\|docker-compose\|compose\|k8s\|kustomize\|helm\|charts\|migrations\|Makefile\|go\.mod\|go\.sum\|package(-lock)?\.json\|pyproject\.toml\|requirements[^/]*)($\|/)' \|\| true); test -z "$hits"` |
| `E28` | 0 | `181f88003a001fc46e49c57e4cd39ae586534fc010285d0a690ff0f3549bb4db` / 1659 | empty / 0 | `jq '{close_issues,related_issues,followup_issues}' .trellis/tasks/07-26-118-guru-finalize-task/issue-scope-ledger.json` |
| `E29` | 0 | `de96ba8637820dbf30ab3e200a6d15a0052182d3a37f74532e09e44d5cbd2201` / 1040 | empty / 0 | `rg -n -i 'planned.*guru-finalize-task\|guru-finalize-task.*planned\|future.*guru-finalize-task\|guru-finalize-task.*future\|five (production\|target-owned\|semantic)\|5 (production\|target-owned\|semantic)\|12 active Skills\|46 external exits\|11 target-owned\|package graph.*12\|package closure.*12' README.md trellis/workflows/guru-team/README.md trellis/presets/guru-team/README.md .trellis/spec/workflow/index.md .trellis/spec/workflow/quality-guidelines.md .trellis/spec/workflow/skill-package-contract.md .trellis/spec/workflow/workflow-contract.md .trellis/spec/preset/installer.md .trellis/spec/preset/upstream-ownership.md .trellis/spec/docs/public-docs.md`；命中均为明确 historical state 或“原五条 + finalizer 七条”解释 |
| `E30` | 0 | empty / 0 | empty / 0 | `found=$(find . -type f \( -name '*.new' -o -name '*.bak' -o -name '*.pyc' \) -print; find . -type d -name '__pycache__' -print); test -z "$found"` after exact reviewer-cache cleanup |
| `E31` | 0 | `7f02fb946ea5247a28205e4fb470d95a3f1eb5562653f6c45dba25d70681a3a0` / 4139759 | `6663f8dc019ce9d9a1b8c6776b69cf30d9f92599f95c74bb15117ef1d8894dba` / 930 | `TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1 PYTHONPYCACHEPREFIX=<evidence>/pycache-throwaway trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh <evidence>/throwaway` |
| `E32` | 0 | `e060ad26af12239dd57012f4de0124e0e88dcb22fc997534a8052706623e0e32` / 4140 | empty / 0 | `git status --short`（pre-report snapshot） |
| `E33` | 0 | `59c4fd162f3265b4efa11869c1d4feb1133057b8e351e79546dd360b23042c1c` / 2465 | empty / 0 | `git diff --stat 7820a9eeec2a2a75fb52fba156a7211d9f9fb09c`；38 files, 11208 insertions, 4791 deletions |
| `E34` | 0 | `40eaa5c74436677165ba0c888d5486a6bf6892fd5b5eaff95924837bdbcf9955` / 34598 | empty / 0 | `git ls-files --others --exclude-standard`（415 paths before this report） |

### 未验证项

- 未执行真实 GitHub draft PR/create/ready、archive commit/push 或 issue mutation；本检查角色无这些副作用授权。#105 transaction tests与 clean throwaway提供静态/fixture coverage，但不能替代五个 owner-boundary findings。
- 未验证授权 content push 后的 exact remote feature ref marketplace clean install；throwaway诚实覆盖 public marketplace discovery加 local unpublished canonical sample，不把 local sample声称为 pushed-ref evidence。
- 未验证 #119 global Finish integration或 #132 overlay cleanup；两者明确 out of scope/deferred。
- 没有独立 type checker；已按仓库适用面运行 compile/schema/tests。
- 没有调用 Phase 2 recorder/checker；main 必须先闭合本 agent terminal assignment，再由 `guru-check-task` 把本报告记录为 `implementation_required`，不得记录 `passed`。

### 证据交接

- 阶段二：本报告覆盖 complete approved scope、planning/provenance、implementation handoff、完整 dirty diff、code/schema/config/docs/tests/distribution/install、all six exits、agent recovery 与全部适用 validation。它可支撑 `phase2-check.json` 的 `implementation_required` route，不能支撑 `passed`。
- Docs SSOT：strategy=`ssot_first`。Round 1 已把 active `13/52`、target-owned authoring handoff `12`、deferred global `12/46/27`、#119/#132 boundary合并到 durable docs；#118-only task delta总体一致。`F-RECOVERY-03` 揭示 finalizer-specific #117 metadata-tail augmentation仍缺少 durable contract，修复时必须先收敛该 SSOT，再同步 code/tests。
- Issue scope：`close_issues=[118]`；#81/#115 为 related；#119/#132 为 follow-up。没有 global Finish integration、upstream cleanup 或 #115 closure claim。
- Eval：source/installed corpus与 wrapper机械验证通过，但 staging 不执行 real finalization transition、不跨 active-to-archive，也不重放 #117 metadata-tail owner checker；不得用 8/8 关闭五个 findings。
- Security/deploy：未发现 secret/credential/private data、dependency、CI/CD、container、DB migration 或 production deployment/data-write影响；本轮只使用 repo-external temporary fixtures/logs与 task-local去敏 probes。
- Agent recovery：main 已记录到 `evt-0223-503b4f0c3e` 的 liveness/qualification chain；收到 terminal handoff 后应记录 Round 3 `completed`，运行 assignment validator，然后才能运行 Guru Phase 2 recorder。

### 结论

`implementation_required`。

所有 lint/type-appropriate/full tests/real-wrapper/discovery/install/upgrade/drift/identity/hygiene commands均终态并通过，但五个 current-scope findings仍 open：`F-RECOVERY-03`、`F-MATERIALIZATION-04`、`F-LOCATOR-05` 为 P1，`F-IDENTITY-06`、`F-STATE-07` 为 P2。修复后必须由新的独立 `trellis-check` 身份重新执行完整 Phase 2 round，不得只做 focused rerun。
