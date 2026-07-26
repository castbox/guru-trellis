# Issue #118 Phase 2 Round 2 独立完整检查报告

## 检查完成

### 检查身份与边界

- 检查代理：`/root/issue118_phase2_check`，逻辑角色为“阶段二检查代理”。
- 检查轮次：Round 2；这是修复 Round 1 findings 后对完整 scope、完整 dirty diff、
  全部适用验证与 clean throwaway 的新一轮检查，不是 focused rerun。
- Worktree：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/118-guru-finalize-task`。
- Task：`.trellis/tasks/07-26-118-guru-finalize-task`。
- Branch：`feat/118-guru-finalize-task`。
- Base / reviewed HEAD：`7820a9eeec2a2a75fb52fba156a7211d9f9fb09c`。
- 证据根：`/tmp/guru-118-phase2-round2.WJn89P`。
- Workspace boundary 重新通过：expected workspace 与 actual repo root 一致；source
  checkout clean；`suspicious_source_artifacts=[]`。
- Planning approval 重新通过：`typed_exit=approved`，artifact SHA-256
  `1bcc7712aa1c8a74f72ecfa4a90d8384d77fbd7a6ed95f65714737ffa600c9c6`，
  facts SHA-256
  `9d0d14bada5d4990a3f62402bdb5b28275fd1c7bf20476cdd01f1145defbeb70`。
- `check.jsonl` 只有 seed row，因此按 fallback 读取三份 planning artifacts、
  `get_context.py --mode packages` 返回的 workflow/preset/docs 三层 spec、
  `trellis-check`、`guru-check-task`、`trellis-meta` 及其相关架构/平台/customization
  references。
- 本代理未修改 product、planning、`agent-assignment.json` 或 `phase2-check.json`；
  唯一 repo write 是本报告。未 commit、push、创建 PR、修改 GitHub 或执行 finish。

### 已检查文件

- Planning 与 scope：`prd.md`、`design.md`、`implement.md`、
  `issue-scope-ledger.json`、planning approval、implementation/check recovery chain、
  live Issue #118 正文与 accepted-current comment `5045036678`。
- Canonical package：`trellis/skills/guru-team/packages/guru-finalize-task/**`，包括
  Skill、contract、Interface 1.3、六 profile、六 exit schema/example、consumer、
  projection、private artifact、五个 wrapper、八 case production eval 与 package tests。
- Runtime：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py` 的 preview、
  publication/#117 owner checking、route validation、gate record/check、transition
  executor、#105 transaction delegate、public invocation 与 602-test regression suite。
- Graph 与 distribution：#116/#117 interfaces、registry、extension manifest、consumer
  schemas、shared/Codex/Claude/Cursor copies、installed runtime、eval adapter、preset
  installer/verifier、ownership inventory 与 generated dogfood files。
- Durable Docs SSOT：repository/workflow/preset README；
  `.trellis/spec/workflow/{index,quality-guidelines,skill-package-contract,workflow-contract}.md`；
  `.trellis/spec/preset/{installer,upstream-ownership}.md`；
  `.trellis/spec/docs/public-docs.md`。
- Explicit no-write：canonical/dogfood global workflow、upstream
  `trellis-finish-work` Skill/Command/Prompt、preset overlays、official `task.py`。
- 安装/升级：clean throwaway marketplace discovery、local unpublished canonical sample、
  preset initial install/reapply、`trellis update`、managed hash、`.new/.bak` recovery、
  platform distribution、contract/eval discovery、real wrapper 与最终 sidecar/cache scan。

### Scope-first candidate qualification

| Candidate | Trigger | 正常路径复现 | Disposition |
| --- | --- | --- | --- |
| `C-ROUTE-01`：`published` 前缺少 #117 semantic evidence precondition | `prd.md` R6/R10、AC6；`design.md` 3.1/5/6；accepted-current 的 #117 minimal DTO ownership | `publication_ready`、`transaction_state=prepared`、`marketplace.required=true` 且没有 verified/not-required owner evidence 时，`finalization_validate_route` 仍接受 `published`；executor 只在 `context.verification` 非空时传 `external_verification`，否则 legacy delegate 自行运行 deterministic marketplace verification 并继续 transaction | `current_scope` / `P1` / finding `F-ROUTE-01` |
| `C-DTO-02`：空 `route.output` 缺少 per-exit 校验 | `prd.md` R7/R12、AC2/AC9；Interface 1.3 每 exit 独立 closed schema | `resume_finalization` 的 `output={}` 因 `if output:` 条件被 gate validator 接受；同一个 `{}` 被 declared public schema 拒绝，之后 public wrapper 才返回 `typed_output_invalid` | `current_scope` / `P2` / finding `F-DTO-02` |
| `C-DOC-HIST`：Round 1 durable docs finding | Docs SSOT Plan `ssot_first` | current docs 已统一 active package `13/52`、authoring handoff `12`、deferred global `12/46/27`；剩余 `planned`/`five` 命中明确描述 historical state 或“原五条 + finalizer 七条” | `resolved_in_current_diff`，无 current finding |
| `C-SCHEMA-HIST`：Round 1 closeout schema finding | R2/R9/R14、AC2/AC11 | runtime/package/installed/shared/Codex/Claude/Cursor 八份 schema canonical JSON digest 均为 `ad99793a59b4fd13836894fb1431d3a791ae7a4593418100ea04d5181f8b8d3e`；full tests 的 cross-validator negative regression 通过 | `resolved_in_current_diff`，无 current finding |
| `C-OOS-01`：恶意/伪造/并发/锁/TOCTOU/额外 fault/crash/cross-OS 提议 | Current authority 明确排除，正常路径无 trigger | 不需要这些机制即可复现两个 current findings；本轮没有扩张测试或实现 | `out_of_scope` / route=`none` |

### 已修复问题

- 无。本轮角色仅允许写新的原始检查报告；两个 current-scope finding 需要回到实现阶段。

### 未修复问题

#### F-ROUTE-01（P1，open）：`published` 缺少 #117 semantic evidence precondition

- 文件：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:30174`、
  `:30236`、`:30472`、`:30513`、`:29511`。
- 问题：route validator 只约束 `verification_required` 与 `reprepare_required` 的
  state compatibility，没有约束 `published` 必须拥有同 task/plan/reviewed HEAD 的
  #117 `verified|not_required` owner-checked evidence。`cmd_execute_finalization_transition`
  对 `published` 仅在 `context["verification"]` 非空时注入 `external_verification`；否则
  legacy `cmd_finish_work` 会自行执行 deterministic marketplace verification 并继续
  PR/archive/ready transaction。
- 影响：公共 semantic finalizer 可以从初始 publication profile 直接授权 terminal
  route，缺少需求要求的 #117 applicability/adequacy/findings semantic owner result；
  因此 R6/R10、AC6 及 closed-loop owner boundary 未满足。
- 修复要求：保持 #105 compatibility transaction 不变，在 finalizer-owned objective
  checker/executor boundary 补齐 profile/state/#117 evidence precondition；需要 verification
  的 initial publication 正常路径必须先 content push 后返回 `verification_required`，
  `published` 只能消费 current same-plan `verified|not_required` evidence 或正文允许的
  terminal ready recovery。增加对应 negative/positive runtime 与 real-wrapper regression。

#### F-DTO-02（P2，open）：gate checker 可通过不满足 selected exit schema 的空 output

- 文件：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:30186`、
  `:30190`、`:30395`、`:30535`、`:24927`；
  `trellis/skills/guru-team/packages/guru-finalize-task/schemas/semantic-review-input.schema.json:45`；
  `schemas/task-finalization-gate.schema.json` 的同名 `route.output`。
- 问题：两个 private gate schema 只声明 `output` 为任意 object；runtime 仅在 object
  truthy 时选择并校验 per-exit schema。`{}` 因而通过 record/check。除 executor 后续
  客观填充的 route 外，no-side-effect route 原样返回空 output；public wrapper 才发现
  actual-exit schema 缺少 `exit_id`/业务字段并失败。
- 影响：checker-passed owner gate 不能保证它声明的唯一 external exit 可被序列化，
  R7/R12、AC2/AC9 的 actual-exit per-schema contract 未在 recorder/checker boundary 闭环。
- 修复要求：为 AI-authored output 与 executor-materialized output 建立 closed、按 exit
  区分的 gate shape/validator；所有 no-side-effect exits 在 gate pass 前必须通过其
  per-exit schema，executor-materialized exits 也必须有明确的 pre/post 条件，禁止依赖
  object truthiness。增加 empty/missing/extra/wrong-exit negative regressions。

### Semantic adequacy

| Dimension | 结果 | Current-round evidence |
| --- | --- | --- |
| requirements | 失败 | `F-ROUTE-01` 违反 R6/R10/AC6；`F-DTO-02` 违反 R7/R12/AC2/AC9 |
| design | 失败 | 实现未承接设计中的 #117 owner boundary 与 per-exit gate/output closure |
| implementation | 失败 | runtime 正常路径复现两个 finding；其余 single-engine、preview、archive/PR transaction 回归通过 |
| tests | 失败 | 602/178/45/3 与 8/8 均通过，但缺少能拒绝两个正常误用的 regression |
| docs_ssot | 通过 | `ssot_first` durable docs 已完成 Round 1 reconciliation；docs 正确描述目标 contract，但 code 与之不一致 |
| cross_layer | 失败 | AI gate -> objective checker -> executor -> public wrapper 间缺少 route precondition 与 DTO validity closure |
| compatibility | 通过 | #105 runtime 全量回归、2026-07-03/04 与 #100 families 由 602-test suite 保持通过；upstream no-write 通过 |
| deployment_and_operations | 通过 | 无 dependency、CI/CD、container、Compose、K8s/Helm/Kustomize、DB migration、Makefile、deploy 或 data-write 变化 |
| agent_recovery | 通过（待 terminal metadata 落盘） | implementation correction chain 已闭合；本代理 same-agent recovery 已由 `evt-0173-cb1e1a013f` 关联 `evt-0172-0769d117e8`，main 将在本 terminal handoff 后记录 completed 再跑 checker |
| verification_completeness | 失败 | 本轮检查完整且所有命令终态已知，但两个 open current-scope findings 阻止 Phase 2 pass |

### 验证结果

- Lint：通过。Bash syntax、Python compile、`git diff --check`、task validate、ownership、
  drift、byte identity、sidecar/cache 与 no-write 均 exit 0。
- TypeCheck：不适用。仓库没有独立 configured type checker；Python compile、JSON
  schema validators 与 unittest 提供适用的静态/合同覆盖。
- Tests：命令层通过；语义结论为失败。
  - Runtime：602 tests，13 skipped，exit 0。
  - Skill package：178 tests，exit 0。
  - Preset：45 tests，exit 0。
  - Finalizer package：3 tests，exit 0。
  - Installed shared real public wrapper：8/8 passed，六 actual exits 全覆盖。
  - Source/installed：13 active、0 planned、0 legacy；global markers 保持 12/46/27。
  - Contract discovery：六 input profiles、六 output contracts、两个 private artifacts；
    source/installed bytes 相同。
  - Eval discovery：八 cases、四 adapters；source/installed bytes 相同。
  - Ownership：43 frozen / 43 active / 0 removed；dogfood overlay drift 为零。
  - Canonical/installed/shared/Codex/Claude/Cursor package 逐文件 byte-identical。
  - Clean throwaway：exit 0，覆盖 public marketplace discovery、local unpublished
    canonical workflow sample、initial install/reapply、`trellis update`、managed hash、
    `.new/.bak` recovery、platform copies、wrapper/eval/ownership/sidecar checks。

### 精确命令证据

所有表内命令均从 task worktree root 执行；stdout/stderr 从进程启动时分别写入证据根。
`e3b0c442...` 是空流 SHA-256。每行格式为
`ID | exit | stdout sha/bytes | stderr sha/bytes | exact argv`。

| ID | exit | stdout SHA-256 / bytes | stderr SHA-256 / bytes | Exact argv |
| --- | ---: | --- | --- | --- |
| `E00` | 0 | `89842a60...` / 126 | `e3b0c442...` / 0 | `PYTHONPYCACHEPREFIX=/tmp/guru-118-phase2-round2.WJn89P/pycache-entry python3 ./.trellis/scripts/task.py current --source` |
| `E01` | 0 | `d90a36bf...` / 40198 | `e3b0c442...` / 0 | `./.trellis/guru-team/scripts/bash/check-workspace-boundary.sh --json --task .trellis/tasks/07-26-118-guru-finalize-task` |
| `E02` | 0 | `bcf2b0e3...` / 738 | `e3b0c442...` / 0 | `./.trellis/guru-team/scripts/bash/check-planning-approval.sh --json --task .trellis/tasks/07-26-118-guru-finalize-task` |
| `E03` | 0 | `5adbfc63...` / 82 | `e3b0c442...` / 0 | `PYTHONPYCACHEPREFIX=/tmp/guru-118-phase2-round2.WJn89P/pycache-entry python3 ./.trellis/scripts/get_context.py --mode packages` |
| `E04` | 0 | `ebe06e29...` / 2548 | `abd0eba9...` / 4427 | `PYTHONPYCACHEPREFIX=/tmp/guru-118-phase2-round2.WJn89P/pycache-runtime python3 trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py` |
| `E05` | 0 | `e3b0c442...` / 0 | `cf87eec0...` / 4290 | `PYTHONPYCACHEPREFIX=/tmp/guru-118-phase2-round2.WJn89P/pycache-packages python3 trellis/skills/guru-team/tests/test_skill_packages.py` |
| `E06` | 0 | `e3b0c442...` / 0 | `35335b25...` / 809 | `PYTHONPYCACHEPREFIX=/tmp/guru-118-phase2-round2.WJn89P/pycache-preset python3 trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py` |
| `E07` | 0 | `e3b0c442...` / 0 | `3b7a5734...` / 101 | `PYTHONPYCACHEPREFIX=/tmp/guru-118-phase2-round2.WJn89P/pycache-finalizer python3 trellis/skills/guru-team/packages/guru-finalize-task/tests/test_contract.py` |
| `E08` | 0 | `1c6b31cc...` / 1346 | `e3b0c442...` / 0 | `.trellis/guru-team/scripts/bash/check-skill-packages.sh --root . --mode source --json` |
| `E09` | 0 | `4c2be482...` / 1535 | `e3b0c442...` / 0 | `.trellis/guru-team/scripts/bash/check-skill-packages.sh --root . --mode installed --json` |
| `E10` | 0 | `07476c6b...` / 13490 | `e3b0c442...` / 0 | `trellis/workflows/guru-team/scripts/bash/discover-skill-contract.sh --root . --mode source --skill guru-finalize-task --json` |
| `E11` | 0 | `07476c6b...` / 13490 | `e3b0c442...` / 0 | `.trellis/guru-team/scripts/bash/discover-skill-contract.sh --root . --mode installed --skill guru-finalize-task --json` |
| `E12` | 0 | `42a4d8d5...` / 3375 | `e3b0c442...` / 0 | `trellis/workflows/guru-team/scripts/bash/discover-skill-evals.sh --root . --mode source --skill guru-finalize-task --json` |
| `E13` | 0 | `42a4d8d5...` / 3375 | `e3b0c442...` / 0 | `.trellis/guru-team/scripts/bash/discover-skill-evals.sh --root . --mode installed --skill guru-finalize-task --json` |
| `E14` | 0 | `f7ecfc98...` / 7527 | `e3b0c442...` / 0 | `PYTHONPYCACHEPREFIX=/tmp/guru-118-phase2-round2.WJn89P/pycache-evals .trellis/guru-team/scripts/bash/run-skill-evals.sh --root . --mode installed --skill guru-finalize-task --adapter shared --run-root /tmp/guru-118-phase2-round2.WJn89P/eval-installed --json` |
| `E15` | 0 | `5403ca75...` / 1731 | `e3b0c442...` / 0 | `trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json` |
| `E16` | 0 | `b3bafca5...` / 1790 | `e3b0c442...` / 0 | `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh --repo .` |
| `E17` | 0 | `e3b0c442...` / 0 | `e3b0c442...` / 0 | `find trellis/workflows/guru-team/scripts/bash trellis/presets/guru-team/scripts/bash .trellis/guru-team/scripts/bash trellis/skills/guru-team/packages/guru-finalize-task/scripts .trellis/guru-team/skills/packages/guru-finalize-task/scripts .agents/skills/guru-finalize-task/scripts .codex/skills/guru-finalize-task/scripts .claude/skills/guru-finalize-task/scripts .cursor/skills/guru-finalize-task/scripts -type f -name '*.sh' -print0 \| xargs -0 bash -n` |
| `E18` | 0 | `e3b0c442...` / 0 | `e3b0c442...` / 0 | `PYTHONPYCACHEPREFIX=/tmp/guru-118-phase2-round2.WJn89P/pycache-compile python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py trellis/skills/guru-team/adapters/eval/native_adapter.py` |
| `E19` | 0 | `e3b0c442...` / 0 | `e3b0c442...` / 0 | `git diff --check` |
| `E20` | 0 | `53258e0e...` / 311 | `e3b0c442...` / 0 | `PYTHONPYCACHEPREFIX=/tmp/guru-118-phase2-round2.WJn89P/pycache-task python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-26-118-guru-finalize-task` |
| `E21` | 0 | `e3b0c442...` / 0 | `e3b0c442...` / 0 | `git diff --exit-code 7820a9eeec2a2a75fb52fba156a7211d9f9fb09c -- trellis/workflows/guru-team/workflow.md .trellis/workflow.md .agents/skills/trellis-finish-work .codex/prompts/trellis-finish-work.md .codex/skills/trellis-finish-work .claude/commands/trellis/finish-work.md .cursor/commands/trellis-finish-work.md trellis/presets/guru-team/overlays .trellis/scripts/task.py` |
| `E22` | 0 | `e3b0c442...` / 0 | `e3b0c442...` / 0 | `for copy_root in .trellis/guru-team/skills/packages/guru-finalize-task .agents/skills/guru-finalize-task .codex/skills/guru-finalize-task .claude/skills/guru-finalize-task .cursor/skills/guru-finalize-task; do diff -qr trellis/skills/guru-team/packages/guru-finalize-task "$copy_root"; done` |
| `E23` | 0 | `3e620c22...` / 57 | `e3b0c442...` / 0 | `git status --short \| sed 's/^...//' \| rg '(^\|/)(\.github\|Dockerfile\|docker-compose\|compose\|k8s\|kustomize\|helm\|charts\|migrations\|Makefile\|go\.mod\|go\.sum\|package(-lock)?\.json\|pyproject\.toml\|requirements[^/]*)($\|/)'`（zero-hit assertion） |
| `E24` | 0 | `181f8800...` / 1659 | `e3b0c442...` / 0 | `jq '{close_issues,related_issues,followup_issues}' .trellis/tasks/07-26-118-guru-finalize-task/issue-scope-ledger.json` |
| `E25` | 0 | `56b12cb9...` / 1040 | `e3b0c442...` / 0 | `rg -n -i 'planned.*guru-finalize-task\|guru-finalize-task.*planned\|future.*guru-finalize-task\|guru-finalize-task.*future\|five (production\|target-owned\|semantic)\|5 (production\|target-owned\|semantic)\|12 active Skills\|46 external exits\|11 target-owned\|package graph.*12\|package closure.*12' <ten durable docs>` |
| `E26` | 0 | `6f65655c...` / 1081 | `e3b0c442...` / 0 | `for schema_file in <eight closeout-plan.schema.json paths>; do jq -cS . "$schema_file" \| shasum -a 256; done` |
| `E27` | 0 | `c0528bff1db470e6667db6a857d43ba5bbc6261207511de463e684a9581d9c08` / 687 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` / 0 | `test ! -e /tmp/guru-118-phase2-round2.WJn89P/finalization-correctness-repair.stdout && test ! -e /tmp/guru-118-phase2-round2.WJn89P/finalization-correctness-repair.stderr && PYTHONPYCACHEPREFIX=/tmp/guru-118-phase2-round2.WJn89P/pycache-correctness-repair python3 /tmp/guru-118-phase2-round2.WJn89P/reproduce-finalization-correctness-repair.py > /tmp/guru-118-phase2-round2.WJn89P/finalization-correctness-repair.stdout 2> /tmp/guru-118-phase2-round2.WJn89P/finalization-correctness-repair.stderr` |
| `E28` | 0 | `1e5b1cb7...` / 4139759 | `bcecc81e...` / 931 | `TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1 PYTHONPYCACHEPREFIX=/tmp/guru-118-phase2-round2.WJn89P/pycache-throwaway trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh /tmp/guru-118-phase2-round2.WJn89P/throwaway` |
| `E29` | 0 | `c1876394...` / 49 | `e3b0c442...` / 0 | `find . -type f \( -name '*.new' -o -name '*.bak' -o -name '*.pyc' \) -print` + `find . -type d -name '__pycache__' -print`（both zero-hit assertions） |

#### Round 2 metadata-only evidence repair

- 本 repair 只替换 `E27` 的 repo-external reproduction evidence，不重跑或改变完整
  Round 2 语义检查、finding qualification、severity、adequacy 或 recommendation。
- 旧 `/tmp/guru-118-phase2-round2.WJn89P/route-gaps.stdout` 与
  `route-gaps.stderr` 已明确排除，不再作为本报告证据；它们后续被一次未纳入报告的
  临时 fixture-shape 调整覆盖，因此不具备 current evidence identity。
- Fresh producer：
  `/tmp/guru-118-phase2-round2.WJn89P/reproduce-finalization-correctness-repair.py`，
  SHA-256
  `7ccde501619f55d344e4451fd177f383b90134b505d4deff4448e889cdccaf07`，
  2691 bytes。
- Fresh stdout：
  `/tmp/guru-118-phase2-round2.WJn89P/finalization-correctness-repair.stdout`，
  SHA-256
  `c0528bff1db470e6667db6a857d43ba5bbc6261207511de463e684a9581d9c08`，
  687 bytes。
- Fresh stderr：
  `/tmp/guru-118-phase2-round2.WJn89P/finalization-correctness-repair.stderr`，
  SHA-256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`，
  0 bytes。
- Fresh result：`exit_code=0`；`F-ROUTE-01` 记录
  `transaction_state=prepared`、`marketplace_required=true`、
  `verification_owner_evidence_present=false` 且
  `published_route_accepted=true`；`F-DTO-02` 记录空 output gate accepted，随后
  selected `resume_finalization` schema 返回三条 required-field error。
- 本次 resume 的 channel tool activity 已记录为 `evt-0186-cdaab9c50b`；completion
  event 由 main 在收到本 metadata-repair terminal handoff 后记录。

Repo snapshot supporting evidence：`git status --short` stdout SHA
`e060ad26af12239dd57012f4de0124e0e88dcb22fc997534a8052706623e0e32`
/ 4140 bytes；`git diff --stat` stdout SHA
`2ee756cf12a06fd5677b8fd07e7c6b8722d72c9f09b5bac32b1bef520b3b9416`
/ 2465 bytes；untracked inventory stdout SHA
`5e26e72808fe730f25a73115568edac80f6ef5c6f43fb6a0b885f09a1a61c075`
/ 34251 bytes；三者 stderr 均为空且 exit 0。

### 证据交接

- 阶段二：本报告覆盖完整 approved scope、planning/provenance、implementation handoff、
  complete dirty state、durable docs、code/schema/test/distribution/install、agent recovery 与
  全部适用命令。它可以支撑 `guru-check-task` 生成 `implementation_required` 输入，不能
  支撑 `passed`。
- Docs SSOT：strategy=`ssot_first`。Round 1 的 stale durable-doc finding 已关闭；current
  durable docs、package contract、README、task delta 对 active 13/52、authoring 12、deferred
  global 12/46/27、#119/#132 boundary 一致。当前不需要第一次 docs merge；实现修复后只需
  复核 docs 仍准确，除非代码合同发生新变化。
- 历史 schema：Round 1 的 same-id divergence 已关闭，八份 canonical digest 相同，
  negative cross-validator regressions 随 full suites 通过。
- Issue scope：`close_issues=[118]`；#115 及 #81 为 related；#119/#132 为 follow-up。
  本轮未改变 #105、#115、#119、#132 或任何 GitHub 状态。
- 平台/安装：Shared real wrapper 8/8；full package tests 覆盖 Codex trusted root、Claude
  input protocol、Cursor unsupported/unavailable 与 shared parsing。Clean throwaway 诚实
  验证 public marketplace + local unpublished canonical sample；exact pushed feature-ref
  仍需在授权 content push 后由 publication-time verification 绑定，不把本地 sample 冒充
  remote-ref pass。
- Agent recovery：main 已记录 same-agent resume `evt-0173-cb1e1a013f` 指向 failed
  `evt-0172-0769d117e8`；本 terminal handoff 后 main 需要记录 completed 并重新运行
  `check-agent-assignment`，再进入任何 Guru Phase 2 recorder。

### 结论

`implementation_required`。

所有 lint/type-appropriate/test/install 命令均已终态并通过，但 `F-ROUTE-01`（P1）与
`F-DTO-02`（P2）是正常受支持路径中的 open current-scope findings。修复后必须由独立
`trellis-check` 身份重新执行完整 Phase 2 round；不得只做两个 finding 的 focused rerun。
